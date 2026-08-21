from __future__ import annotations

import configparser
import os
import sqlite3
import threading
import time
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from .segments import extract_segments
from .tree_index import (
    HARD_TEST_DIRS,
    SOURCE_EXTENSIONS,
    is_hard_test_component,
    is_hard_test_filename,
)


# When a catalog snapshot contains vendored third-party trees, those hashes
# must not be attributed to the parent component. Direct files under these
# directories are kept, but child directories are pruned as separate trees.
NESTED_VENDOR_DIRS = {
    "third_party", "third-party", "3rdparty", "3rd_party", "vendor", "vendors",
    "external", "extern", "deps", "dependencies", "contrib", "thirdparty",
}

TEST_SCOPE_DIRS = {
    "test", "tests", "testing", "testsuite", "testsuites",
    "bench", "benchmark", "benchmarks",
    "example", "examples", "demo", "demos",
    "fuzz", "fuzzer", "fuzzers", "oss-fuzz",
}

AUXILIARY_SCOPE_DIRS = {
    "doc", "docs", "documentation",
    "tool", "tools", "script", "scripts",
    "ci", ".github", "cmake",
}


def _normalize_rel_path(value: str) -> str:
    return value.replace("\\", "/").strip("/")


def _has_vendor_boundary(rel_path: str) -> bool:
    parts = [part.lower() for part in Path(_normalize_rel_path(rel_path)).parts]
    return any(part in NESTED_VENDOR_DIRS for part in parts)


def _read_gitmodules(repo_root: Path, cache: dict[Path, dict[str, str]]) -> dict[str, str]:
    """Return ``submodule path -> url`` for one Git worktree.

    ``.gitmodules`` is INI-like, so ConfigParser is sufficient and keeps the
    fingerprint builder independent from the ``git`` executable. Malformed
    files are treated conservatively as having no owned submodules.
    """
    repo_root = repo_root.resolve()
    cached = cache.get(repo_root)
    if cached is not None:
        return cached

    gitmodules = repo_root / ".gitmodules"
    entries: dict[str, str] = {}
    if not gitmodules.is_file():
        cache[repo_root] = entries
        return entries

    parser = configparser.RawConfigParser(interpolation=None)
    try:
        parser.read(gitmodules, encoding="utf-8")
    except (OSError, configparser.Error):
        cache[repo_root] = entries
        return entries

    for section in parser.sections():
        if not section.lower().startswith("submodule "):
            continue
        try:
            path = _normalize_rel_path(parser.get(section, "path"))
            url = parser.get(section, "url").strip()
        except (configparser.Error, KeyError):
            continue
        if path and url:
            entries[path] = url

    cache[repo_root] = entries
    return entries


def _is_relative_submodule_url(url: str) -> bool:
    """True for same-namespace Git submodule URLs such as ``../asio.git``."""
    value = url.strip().replace("\\", "/")
    return value.startswith("../") or value.startswith("./")


def _is_owned_nested_git(
    label_dir: Path,
    current_path: Path,
    *,
    gitmodules_cache: dict[Path, dict[str, str]],
) -> bool:
    """Decide whether a nested Git worktree belongs to the catalog component.

    A nested repository is considered first-party only when all of these hold:

    * it is explicitly declared by an ancestor repository's ``.gitmodules``;
    * its path is outside conventional vendoring boundaries;
    * the declared URL is relative, which keeps ownership in the same Git
      namespace (Boost's ``libs/*`` layout is the motivating case).

    Unknown/absolute/external submodules remain pruned. This is intentionally
    conservative: fingerprint identity must not absorb arbitrary nested repos.
    """
    try:
        rel_from_label = current_path.relative_to(label_dir).as_posix()
    except ValueError:
        return False

    if not rel_from_label or _has_vendor_boundary(rel_from_label):
        return False

    # Find the nearest ancestor repository whose .gitmodules explicitly names
    # this worktree. This also supports recursively-owned submodules.
    repo_root = current_path.parent
    while True:
        try:
            current_path.relative_to(repo_root)
            repo_root.relative_to(label_dir)
        except ValueError:
            break

        entries = _read_gitmodules(repo_root, gitmodules_cache)
        if entries:
            rel = _normalize_rel_path(current_path.relative_to(repo_root).as_posix())
            url = entries.get(rel)
            if url is not None:
                return _is_relative_submodule_url(url)

        if repo_root == label_dir:
            break
        repo_root = repo_root.parent

    return False


def source_scope(rel_path: str) -> str:
    """Classify catalog code by how safely it can establish component identity.

    PRIMARY code may open a fingerprint identity gate. TEST/VENDORED/AUXILIARY
    code remains indexed for provenance/diagnostics but cannot by itself name
    the component. This prevents e.g. fmt/test/gtest hashes from identifying a
    foreign GoogleTest tree as fmt.
    """
    parts = [part.lower() for part in Path(rel_path).parts[:-1]]
    if any(part in NESTED_VENDOR_DIRS for part in parts):
        return "VENDORED"
    if any(part in TEST_SCOPE_DIRS for part in parts):
        return "TEST"
    if any(part in AUXILIARY_SCOPE_DIRS for part in parts):
        return "AUXILIARY"
    return "PRIMARY"

TABLE_SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS segments (
    id INTEGER PRIMARY KEY,
    exact_hash TEXT NOT NULL,
    normalized_hash TEXT NOT NULL,
    component TEXT NOT NULL,
    source_label TEXT NOT NULL,
    kind TEXT NOT NULL,
    source_path TEXT NOT NULL,
    token_count INTEGER NOT NULL,
    scope TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS hash_stats (
    hash_kind TEXT NOT NULL,
    hash TEXT NOT NULL,
    component_frequency INTEGER NOT NULL,
    primary_component_frequency INTEGER NOT NULL,
    PRIMARY KEY(hash_kind, hash)
);
"""

INDEX_SCHEMA = """
CREATE INDEX IF NOT EXISTS idx_segments_exact ON segments(exact_hash);
CREATE INDEX IF NOT EXISTS idx_segments_normalized ON segments(normalized_hash);
CREATE INDEX IF NOT EXISTS idx_segments_component ON segments(component);
CREATE INDEX IF NOT EXISTS idx_segments_scope ON segments(scope);
"""


REQUIRED_SCHEMA_VERSION = "identity-only-v6-owned-submodules"


class FingerprintDB:
    """Local fingerprint DB used strictly for component identity.

    ``source_label`` is catalog provenance only (tag/commit/snapshot). It is
    never used as detected component-version evidence.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._local = threading.local()

    def _conn(self) -> sqlite3.Connection:
        conn = getattr(self._local, "conn", None)
        if conn is None:
            conn = sqlite3.connect(self.path, timeout=30.0)
            conn.row_factory = sqlite3.Row
            self._local.conn = conn
        return conn

    def initialize(self, *, reset: bool = False) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if reset:
            for candidate in (
                self.path,
                Path(str(self.path) + "-wal"),
                Path(str(self.path) + "-shm"),
            ):
                try:
                    candidate.unlink()
                except FileNotFoundError:
                    pass
        conn = sqlite3.connect(self.path)
        try:
            conn.executescript(TABLE_SCHEMA)
            conn.executescript(INDEX_SCHEMA)
            conn.execute(
                "INSERT OR REPLACE INTO meta(key,value) VALUES('schema_version',?)",
                (REQUIRED_SCHEMA_VERSION,),
            )
            conn.commit()
        finally:
            conn.close()

    def schema_version(self) -> str:
        try:
            row = self._conn().execute(
                "SELECT value FROM meta WHERE key='schema_version'"
            ).fetchone()
        except sqlite3.OperationalError:
            return ""
        return str(row[0]) if row else ""

    def validate_compatible(self) -> None:
        version = self.schema_version()
        if version != REQUIRED_SCHEMA_VERSION:
            raise RuntimeError(
                f"fingerprint DB schema {version or '<unknown>'} is incompatible; "
                "rebuild fingerprints.sqlite with build_fingerprint_index.py from v0.12"
            )

    def total_components(self) -> int:
        row = self._conn().execute(
            "SELECT value FROM meta WHERE key='component_count'"
        ).fetchone()
        return int(row[0]) if row else 0

    def lookup_hashes(
        self,
        exact_hashes: Iterable[str],
        normalized_hashes: Iterable[str],
    ) -> tuple[dict[str, list[dict]], dict[str, list[dict]]]:
        conn = self._conn()

        def lookup(column: str, values: Iterable[str]) -> dict[str, list[dict]]:
            vals = list(dict.fromkeys(v for v in values if v))
            out: dict[str, list[dict]] = defaultdict(list)
            for start in range(0, len(vals), 450):
                chunk = vals[start:start + 450]
                if not chunk:
                    continue
                q = ",".join("?" for _ in chunk)
                hash_kind = "exact" if column == "exact_hash" else "normalized"
                try:
                    rows = conn.execute(
                        f"SELECT s.{column} AS h, s.component, s.source_label, s.kind, "
                        f"s.source_path, s.token_count, s.scope, "
                        f"COALESCE(hs.component_frequency, 1) AS component_frequency, "
                        f"COALESCE(hs.primary_component_frequency, 0) AS primary_component_frequency "
                        f"FROM segments s "
                        f"LEFT JOIN hash_stats hs ON hs.hash_kind=? AND hs.hash=s.{column} "
                        f"WHERE s.{column} IN ({q})",
                        [hash_kind, *chunk],
                    ).fetchall()
                except sqlite3.OperationalError as exc:
                    raise RuntimeError(
                        "fingerprint DB uses an old schema; rebuild it with "
                        "build_fingerprint_index.py from v0.5"
                    ) from exc
                for row in rows:
                    out[row["h"]].append(dict(row))
            return dict(out)

        return lookup("exact_hash", exact_hashes), lookup("normalized_hash", normalized_hashes)

    @staticmethod
    def _iter_owned_source_files(label_dir: Path, *, max_file_bytes: int):
        """Yield source files owned by the catalog component.

        Rules:
        - explicitly-owned relative Git submodules may be indexed;
        - unknown/external nested Git repositories remain excluded;
        - child trees under conventional vendoring directories are excluded;
        - direct files under contrib/vendor/etc. are retained.
        """
        nested_roots_pruned = 0
        files_seen = 0
        gitmodules_cache: dict[Path, dict[str, str]] = {}

        for current, dirs, files in os.walk(label_dir):
            current_path = Path(current)
            rel_dir = current_path.relative_to(label_dir).as_posix()
            if rel_dir == ".":
                rel_dir = ""

            # Nested Git worktrees are conservative by default, but official
            # same-namespace submodules declared via .gitmodules may belong to
            # umbrella components such as Boost. Vendored boundaries are still
            # never attributed to the parent component.
            if rel_dir and ((current_path / ".git").is_dir() or (current_path / ".git").is_file()):
                if not _is_owned_nested_git(
                    label_dir, current_path, gitmodules_cache=gitmodules_cache
                ):
                    nested_roots_pruned += 1
                    dirs[:] = []
                    continue

            # Never descend into git metadata.
            dirs[:] = [d for d in dirs if d.lower() != ".git"]

            # contrib/zstd, third_party/foo, deps/bar, ... are separate
            # ownership domains. Keep direct files in contrib itself, but do
            # not attribute its child source trees to the parent component.
            if current_path.name.lower() in NESTED_VENDOR_DIRS:
                nested_roots_pruned += len(dirs)
                dirs[:] = []

            for name in files:
                path = current_path / name
                if path.suffix.lower() not in SOURCE_EXTENSIONS:
                    continue
                try:
                    size = path.stat().st_size
                except OSError:
                    continue
                if size > max_file_bytes:
                    continue
                files_seen += 1
                yield path

        return nested_roots_pruned, files_seen

    @classmethod
    def build_from_catalog(
        cls,
        catalog_root: str | Path,
        out_db: str | Path,
        *,
        max_file_bytes: int = 2_000_000,
        reset: bool = True,
        progress: bool = False,
    ) -> dict:
        """Build an identity-only source fingerprint DB.

        Layout:
            catalog/<component>/<source-label>/...

        ``source-label`` may be a release tag, commit or arbitrary snapshot.
        Multiple labels can improve identity coverage, but the label never
        becomes a detected version.

        Fingerprint ownership is conservative: unknown/external nested Git
        repositories and child trees under conventional vendoring directories
        are not indexed as the parent component. Explicit same-namespace
        relative submodules declared in .gitmodules may be indexed as owned.
        """
        catalog_root = Path(catalog_root).resolve()
        db = cls(out_db)
        db.initialize(reset=reset)

        label_jobs: list[tuple[str, str, Path]] = []
        hard_test_components_skipped = 0
        for component_dir in sorted(p for p in catalog_root.iterdir() if p.is_dir()):
            if is_hard_test_component(component_dir.name):
                hard_test_components_skipped += 1
                continue
            for label_dir in sorted(p for p in component_dir.iterdir() if p.is_dir()):
                label_jobs.append((component_dir.name, label_dir.name, label_dir))

        conn = sqlite3.connect(db.path)
        inserted = 0
        labels_seen: set[tuple[str, str]] = set()
        components_seen: set[str] = set()
        files_scanned = 0
        nested_roots_pruned = 0
        hard_test_dirs_skipped = 0
        hard_test_files_skipped = 0
        files_by_scope: dict[str, int] = defaultdict(int)
        segments_by_scope: dict[str, int] = defaultdict(int)
        build_started = time.perf_counter()

        try:
            # Bulk-load first, build indexes once at the end. This is much
            # faster than maintaining three B-trees on every INSERT.
            conn.executescript("""
                DROP INDEX IF EXISTS idx_segments_exact;
                DROP INDEX IF EXISTS idx_segments_normalized;
                DROP INDEX IF EXISTS idx_segments_component;
                DROP INDEX IF EXISTS idx_segments_scope;
                DELETE FROM hash_stats;
            """)
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA temp_store=MEMORY")

            total_jobs = len(label_jobs)
            for index, (component, source_label, label_dir) in enumerate(label_jobs, start=1):
                t0 = time.perf_counter()
                labels_seen.add((component, source_label))
                components_seen.add(component)
                label_files = 0
                label_segments = 0
                gitmodules_cache: dict[Path, dict[str, str]] = {}

                # We need an explicit walk here so we can count pruned roots.
                for current, dirs, files in os.walk(label_dir):
                    current_path = Path(current)
                    rel_dir = current_path.relative_to(label_dir).as_posix()
                    if rel_dir == ".":
                        rel_dir = ""

                    if rel_dir and ((current_path / ".git").is_dir() or (current_path / ".git").is_file()):
                        if not _is_owned_nested_git(
                            label_dir, current_path, gitmodules_cache=gitmodules_cache
                        ):
                            nested_roots_pruned += 1
                            dirs[:] = []
                            continue

                    kept_dirs = []
                    for d in dirs:
                        low = d.lower()
                        if low == ".git":
                            continue
                        if low in HARD_TEST_DIRS:
                            hard_test_dirs_skipped += 1
                            continue
                        kept_dirs.append(d)
                    dirs[:] = kept_dirs
                    if current_path.name.lower() in NESTED_VENDOR_DIRS:
                        nested_roots_pruned += len(dirs)
                        dirs[:] = []

                    for name in files:
                        if is_hard_test_filename(name):
                            hard_test_files_skipped += 1
                            continue
                        path = current_path / name
                        if path.suffix.lower() not in SOURCE_EXTENSIONS:
                            continue
                        try:
                            if path.stat().st_size > max_file_bytes:
                                continue
                            text = path.read_text(encoding="utf-8", errors="ignore")
                        except OSError:
                            continue

                        files_scanned += 1
                        label_files += 1
                        rel = path.relative_to(label_dir).as_posix()
                        scope = source_scope(rel)
                        files_by_scope[scope] += 1
                        rows = [
                            (
                                seg.exact_hash,
                                seg.normalized_hash,
                                component,
                                source_label,
                                seg.kind,
                                rel,
                                seg.token_count,
                                scope,
                            )
                            for seg in extract_segments(text)
                        ]
                        if rows:
                            conn.executemany(
                                "INSERT INTO segments(exact_hash, normalized_hash, component, source_label, kind, source_path, token_count, scope) VALUES(?,?,?,?,?,?,?,?)",
                                rows,
                            )
                            inserted += len(rows)
                            label_segments += len(rows)
                            segments_by_scope[scope] += len(rows)

                # Keep WAL bounded and make long builds visibly incremental.
                conn.commit()
                if progress:
                    elapsed = time.perf_counter() - t0
                    print(
                        f"[{index:03d}/{total_jobs:03d}] {component}/{source_label} "
                        f"files={label_files} segments={label_segments} {elapsed:.2f}s",
                        flush=True,
                    )

            if progress:
                print("[index] computing component-frequency / IDF metadata...", flush=True)
            conn.executescript("""
                INSERT INTO hash_stats(hash_kind, hash, component_frequency, primary_component_frequency)
                SELECT 'exact', exact_hash,
                       COUNT(DISTINCT component),
                       COUNT(DISTINCT CASE WHEN scope='PRIMARY' THEN component END)
                FROM segments
                GROUP BY exact_hash;

                INSERT INTO hash_stats(hash_kind, hash, component_frequency, primary_component_frequency)
                SELECT 'normalized', normalized_hash,
                       COUNT(DISTINCT component),
                       COUNT(DISTINCT CASE WHEN scope='PRIMARY' THEN component END)
                FROM segments
                GROUP BY normalized_hash;
            """)
            if progress:
                print("[index] creating SQLite indexes...", flush=True)
            conn.executescript(INDEX_SCHEMA)
            conn.execute(
                "INSERT OR REPLACE INTO meta(key,value) VALUES('schema_version',?)",
                (REQUIRED_SCHEMA_VERSION,),
            )
            conn.execute(
                "INSERT OR REPLACE INTO meta(key,value) VALUES('component_count',?)",
                (str(len(components_seen)),),
            )
            conn.execute(
                "INSERT OR REPLACE INTO meta(key,value) VALUES('source_label_count',?)",
                (str(len(labels_seen)),),
            )
            conn.commit()
            conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        finally:
            conn.close()

        elapsed = time.perf_counter() - build_started
        try:
            db_size = db.path.stat().st_size
        except OSError:
            db_size = 0
        return {
            "components": len(components_seen),
            "source_labels": len(labels_seen),
            "files": files_scanned,
            "segments": inserted,
            "nested_roots_pruned": nested_roots_pruned,
            "hard_test_components_skipped": hard_test_components_skipped,
            "hard_test_dirs_skipped": hard_test_dirs_skipped,
            "hard_test_files_skipped": hard_test_files_skipped,
            "files_by_scope": dict(sorted(files_by_scope.items())),
            "segments_by_scope": dict(sorted(segments_by_scope.items())),
            "database_bytes": db_size,
            "elapsed_seconds": round(elapsed, 3),
            "database": str(db.path),
        }

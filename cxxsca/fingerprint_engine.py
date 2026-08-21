from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from .context import ComponentContext
from .fingerprint_db import FingerprintDB
from .models import FingerprintRejection, FingerprintSummary
from .segments import CodeSegment, extract_segments


LOW_SIGNAL_DIRS = {
    "test", "tests", "testing", "testsuite", "testsuites",
    "bench", "benchmark", "benchmarks",
    "example", "examples", "demo", "demos",
    "fuzz", "fuzzer", "fuzzers", "oss-fuzz",
}

IMPLEMENTATION_SUFFIXES = {".c", ".cc", ".cpp", ".cxx", ".m", ".mm"}
HEADER_SUFFIXES = {".h", ".hh", ".hpp", ".hxx", ".inc", ".inl"}


@dataclass(slots=True)
class FingerprintEngineConfig:
    max_files_per_context: int = 120
    max_file_bytes: int = 2_000_000
    min_matches: int = 2
    min_coverage: float = 0.04
    # A hash that occurs in PRIMARY code of too many components is too generic
    # to be useful for identity, even if the bytes match exactly.
    max_hash_component_fanout: int = 12
    high_idf_threshold: float = 0.72


class FingerprintEngine:
    """Deterministic, ML-free component identity matcher.

    v0.5 changes the question from "how many hashes matched?" to "how much
    *discriminative PRIMARY code* matched?".

    Catalog hashes from TEST/VENDORED/AUXILIARY scopes are intentionally not
    allowed to create identity candidates. For PRIMARY hashes, component
    frequency is converted to an IDF-like 0..1 weight: a hash unique to one
    component is strong; a hash shared by many components contributes little.

    Fingerprints remain identity-only and never infer a version.
    """

    def __init__(
        self,
        db: FingerprintDB,
        config: FingerprintEngineConfig | None = None,
    ) -> None:
        self.db = db
        self.config = config or FingerprintEngineConfig()

    @staticmethod
    def _relative_inside_context(ctx: ComponentContext, rel_path: str) -> str:
        rel = rel_path.replace("\\", "/")
        root = (ctx.root_rel or "").strip("/")
        if root and rel.startswith(root + "/"):
            return rel[len(root) + 1 :]
        return rel

    @classmethod
    def _file_priority(cls, ctx: ComponentContext, rec) -> tuple:
        local = cls._relative_inside_context(ctx, rec.rel_path)
        parts = [p.lower() for p in Path(local).parts]
        low_signal = 1 if any(p in LOW_SIGNAL_DIRS for p in parts) else 0
        if rec.suffix in IMPLEMENTATION_SUFFIXES:
            kind = 0
        elif rec.suffix in HEADER_SUFFIXES:
            kind = 1
        else:
            kind = 2

        if 2_048 <= rec.size <= 256_000:
            size_bucket = 0
        elif rec.size < 2_048:
            size_bucket = 1
        else:
            size_bucket = 2

        return (low_signal, kind, size_bucket, rec.rel_path.lower())

    @classmethod
    def _top_group(cls, ctx: ComponentContext, rec) -> str:
        local = cls._relative_inside_context(ctx, rec.rel_path)
        parts = Path(local).parts
        return parts[0].lower() if len(parts) > 1 else "(root)"

    def _select_files(self, ctx: ComponentContext):
        candidates = [
            rec for rec in ctx.source_files
            if rec.size <= self.config.max_file_bytes
        ]
        if len(candidates) <= self.config.max_files_per_context:
            return sorted(candidates, key=lambda r: self._file_priority(ctx, r))

        groups: dict[str, list] = defaultdict(list)
        for rec in candidates:
            groups[self._top_group(ctx, rec)].append(rec)
        for records in groups.values():
            records.sort(key=lambda r: self._file_priority(ctx, r))

        selected = []
        selected_paths: set[str] = set()

        per_group = max(2, min(8, self.config.max_files_per_context // max(1, len(groups))))
        for group in sorted(groups):
            for rec in groups[group][:per_group]:
                if rec.rel_path not in selected_paths:
                    selected.append(rec)
                    selected_paths.add(rec.rel_path)
                    if len(selected) >= self.config.max_files_per_context:
                        return selected

        remaining = sorted(candidates, key=lambda r: self._file_priority(ctx, r))
        for rec in remaining:
            if rec.rel_path in selected_paths:
                continue
            selected.append(rec)
            selected_paths.add(rec.rel_path)
            if len(selected) >= self.config.max_files_per_context:
                break
        return selected

    def _extract(self, ctx: ComponentContext) -> tuple[list[tuple[str, CodeSegment]], int]:
        files = self._select_files(ctx)
        out: list[tuple[str, CodeSegment]] = []
        for rec in files:
            text = ctx.read_text(rec, max_bytes=self.config.max_file_bytes)
            if not text:
                continue
            for seg in extract_segments(text):
                out.append((rec.rel_path, seg))
        return out, len(files)

    @staticmethod
    def _normalized_idf(total_components: int, component_frequency: int) -> float:
        """Return an IDF-like rarity score normalized to 0..1.

        With N catalog components, frequency=1 maps to 1.0. Hashes present in
        almost every component approach 0. The +1 smoothing keeps the function
        stable for tiny fixture databases.
        """
        n = max(1, int(total_components))
        f = max(1, min(n, int(component_frequency)))
        raw = math.log((n + 1.0) / (f + 1.0)) + 1.0
        max_raw = math.log((n + 1.0) / 2.0) + 1.0
        if max_raw <= 0:
            return 1.0
        return max(0.0, min(1.0, raw / max_raw))

    @staticmethod
    def _primary_rows(rows: list[dict]) -> list[dict]:
        return [row for row in rows if row.get("scope") == "PRIMARY"]

    def match(self, ctx: ComponentContext) -> tuple[list[FingerprintSummary], dict]:
        pairs, sampled_files = self._extract(ctx)
        segments = [seg for _, seg in pairs]
        if not segments:
            return [], {
                "segments": 0,
                "exact_hits": 0,
                "normalized_hits": 0,
                "sampled_files": sampled_files,
                "non_primary_hits_ignored": 0,
                "high_fanout_hits_ignored": 0,
                "candidate_rejections": [],
            }

        exact_map, norm_map = self.db.lookup_hashes(
            (s.exact_hash for s in segments),
            (s.normalized_hash for s in segments),
        )
        total_components = max(1, self.db.total_components())
        agg: dict[str, dict] = defaultdict(
            lambda: {
                "weighted": 0.0,
                "idf_sum": 0.0,
                "matched_ids": set(),
                "exact_ids": set(),
                "normalized_ids": set(),
                "high_idf_ids": set(),
                "shared_ids": set(),
                "files": set(),
                "examples": [],
                "methods": set(),
            }
        )
        exact_hit_ids: set[int] = set()
        normalized_hit_ids: set[int] = set()
        non_primary_hits_ignored: set[int] = set()
        high_fanout_hits_ignored: set[int] = set()

        for idx, (rel, seg) in enumerate(pairs):
            exact_rows_all = exact_map.get(seg.exact_hash, [])
            exact_rows = self._primary_rows(exact_rows_all)

            if exact_rows:
                rows = exact_rows
                method = "hash:exact"
                base = 1.0
            else:
                # Exact hits that exist only in TEST/VENDORED/AUXILIARY code
                # are not identity evidence. A normalized PRIMARY hit may still
                # be useful, so try it before dropping the segment.
                if exact_rows_all:
                    non_primary_hits_ignored.add(idx)
                norm_rows_all = norm_map.get(seg.normalized_hash, [])
                norm_rows = self._primary_rows(norm_rows_all)
                if not norm_rows:
                    if norm_rows_all:
                        non_primary_hits_ignored.add(idx)
                    continue
                rows = norm_rows
                method = "hash:normalized"
                base = 0.82

            # hash_stats already counts DISTINCT PRIMARY components, so this is
            # independent of duplicate catalog snapshots/source labels.
            primary_frequency = max(
                1,
                max(int(row.get("primary_component_frequency") or 1) for row in rows),
            )
            if primary_frequency > self.config.max_hash_component_fanout:
                high_fanout_hits_ignored.add(idx)
                continue

            idf = self._normalized_idf(total_components, primary_frequency)
            unique_components = {row["component"] for row in rows}

            # The same segment can appear in several labels of the same
            # component. Count it once per component, not once per snapshot.
            for component in unique_components:
                a = agg[component]
                if idx in a["matched_ids"]:
                    continue
                a["matched_ids"].add(idx)

                token_factor = min(2.0, 0.5 + seg.token_count / 120.0)
                a["weighted"] += base * idf * token_factor
                a["idf_sum"] += idf
                a["files"].add(rel)
                a["methods"].add(method)
                if primary_frequency > 1:
                    a["shared_ids"].add(idx)
                if idf >= self.config.high_idf_threshold:
                    a["high_idf_ids"].add(idx)

                if method == "hash:exact":
                    a["exact_ids"].add(idx)
                    exact_hit_ids.add(idx)
                else:
                    a["normalized_ids"].add(idx)
                    normalized_hit_ids.add(idx)
                if rel not in a["examples"] and len(a["examples"]) < 12:
                    a["examples"].append(rel)

        summaries: list[FingerprintSummary] = []
        candidate_rejections: list[FingerprintRejection] = []
        total = len(segments)
        for component, a in agg.items():
            matched = len(a["matched_ids"])
            coverage = matched / total if total else 0.0
            mean_idf = a["idf_sum"] / matched if matched else 0.0
            shared_ratio = len(a["shared_ids"]) / matched if matched else 0.0
            quality = 1.0 - math.exp(-a["weighted"] / 10.0)
            coverage_factor = math.sqrt(min(1.0, coverage))
            file_factor = min(1.0, len(a["files"]) / 5.0)
            confidence = min(
                0.995,
                max(
                    0.0,
                    0.30
                    + 0.22 * quality
                    + 0.18 * coverage_factor
                    + 0.12 * file_factor
                    + 0.18 * mean_idf
                    - 0.18 * shared_ratio,
                ),
            )
            summary = FingerprintSummary(
                component=component,
                confidence=confidence,
                coverage=coverage,
                exact_matches=len(a["exact_ids"]),
                normalized_matches=len(a["normalized_ids"]),
                matched_segments=matched,
                total_segments=total,
                matched_files=len(a["files"]),
                sampled_files=sampled_files,
                mean_idf=mean_idf,
                high_idf_matches=len(a["high_idf_ids"]),
                shared_matches=len(a["shared_ids"]),
                shared_ratio=shared_ratio,
                weighted_score=a["weighted"],
                methods=tuple(sorted(a["methods"])),
                source_examples=tuple(a["examples"]),
            )

            if matched < self.config.min_matches:
                candidate_rejections.append(FingerprintRejection(
                    component=component,
                    root=ctx.display_root,
                    stage="fingerprint_engine",
                    reject_reason=f"fingerprint_engine:matched_segments<{self.config.min_matches}",
                    confidence=confidence,
                    coverage=coverage,
                    exact_matches=summary.exact_matches,
                    normalized_matches=summary.normalized_matches,
                    matched_segments=matched,
                    total_segments=total,
                    matched_files=summary.matched_files,
                    sampled_files=sampled_files,
                    mean_idf=mean_idf,
                    high_idf_matches=summary.high_idf_matches,
                    shared_matches=summary.shared_matches,
                    shared_ratio=shared_ratio,
                    weighted_score=summary.weighted_score,
                ))
                continue
            if coverage < self.config.min_coverage:
                candidate_rejections.append(FingerprintRejection(
                    component=component,
                    root=ctx.display_root,
                    stage="fingerprint_engine",
                    reject_reason=f"fingerprint_engine:coverage<{self.config.min_coverage:.2f}",
                    confidence=confidence,
                    coverage=coverage,
                    exact_matches=summary.exact_matches,
                    normalized_matches=summary.normalized_matches,
                    matched_segments=matched,
                    total_segments=total,
                    matched_files=summary.matched_files,
                    sampled_files=sampled_files,
                    mean_idf=mean_idf,
                    high_idf_matches=summary.high_idf_matches,
                    shared_matches=summary.shared_matches,
                    shared_ratio=shared_ratio,
                    weighted_score=summary.weighted_score,
                ))
                continue

            summaries.append(summary)

        summaries.sort(
            key=lambda s: (
                -s.confidence,
                -s.mean_idf,
                -s.high_idf_matches,
                -s.coverage,
                -s.matched_files,
                -s.matched_segments,
                s.component,
            )
        )
        return summaries, {
            "segments": total,
            "exact_hits": len(exact_hit_ids),
            "normalized_hits": len(normalized_hit_ids),
            "sampled_files": sampled_files,
            "non_primary_hits_ignored": len(non_primary_hits_ignored),
            "high_fanout_hits_ignored": len(high_fanout_hits_ignored),
            "candidate_rejections": candidate_rejections,
        }

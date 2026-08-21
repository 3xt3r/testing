from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from .models import ResolvedComponent
from .util import is_known_version


def _purl(name: str, version: str) -> str | None:
    if not name or not is_known_version(version):
        return None
    return f"pkg:generic/{quote(name, safe='._-')}@{quote(version, safe='._-+')}"


def component_to_cdx(c: ResolvedComponent) -> dict:
    props = [
        {"name": "component.root", "value": c.root},
        {"name": "detection.confidence", "value": f"{c.confidence:.4f}"},
        {"name": "detection.identity_confirmed", "value": str(bool(c.identity_confirmed)).lower()},
        {"name": "detection.identity_methods", "value": ",".join(c.identity_methods)},
        {"name": "detection.methods", "value": ",".join(c.methods)},
    ]
    for f in c.evidence_files:
        props.append({"name": "evidence.file", "value": f})
    if c.fingerprint_coverage is not None:
        props.extend([
            {"name": "fingerprint.identity.coverage", "value": f"{c.fingerprint_coverage:.4f}"},
            {"name": "fingerprint.identity.exact_matches", "value": str(c.fingerprint_exact_matches)},
            {"name": "fingerprint.identity.normalized_matches", "value": str(c.fingerprint_normalized_matches)},
            {"name": "fingerprint.identity.matched_segments", "value": str(c.fingerprint_matched_segments)},
            {"name": "fingerprint.identity.total_segments", "value": str(c.fingerprint_total_segments)},
            {"name": "fingerprint.identity.matched_files", "value": str(c.fingerprint_matched_files)},
            {"name": "fingerprint.identity.sampled_files", "value": str(c.fingerprint_sampled_files)},
            {"name": "fingerprint.identity.mean_idf", "value": f"{c.fingerprint_mean_idf:.4f}"},
            {"name": "fingerprint.identity.high_idf_matches", "value": str(c.fingerprint_high_idf_matches)},
            {"name": "fingerprint.identity.shared_matches", "value": str(c.fingerprint_shared_matches)},
            {"name": "fingerprint.identity.shared_ratio", "value": f"{c.fingerprint_shared_ratio:.4f}"},
            {"name": "fingerprint.identity.weighted_score", "value": f"{c.fingerprint_weighted_score:.4f}"},
        ])
    if c.metadata_version_source_root:
        props.append({
            "name": "metadata.version.source_root",
            "value": c.metadata_version_source_root,
        })
    for conflict in c.conflicts:
        props.append({"name": "detection.conflict", "value": conflict})

    out = {
        "type": "library",
        "name": c.name,
        "version": c.version,
        "bom-ref": f"pkg:generic/{quote(c.name, safe='._-')}@{quote(c.version, safe='._-+')}#{uuid.uuid4()}",
        "properties": props,
    }
    if c.cpe:
        out["cpe"] = c.cpe
    purl = _purl(c.name, c.version)
    if purl:
        out["purl"] = purl
    if c.vcs:
        out["externalReferences"] = [{"type": "vcs", "url": c.vcs}]
    return out


def make_bom(components: list[ResolvedComponent], *, name: str) -> dict:
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": f"urn:uuid:{uuid.uuid4()}",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "component": {"type": "application", "name": name},
        },
        "components": [component_to_cdx(c) for c in components],
    }


def write_split_sbom(
    components: list[ResolvedComponent],
    known_path: str | Path,
    unknown_path: str | Path,
) -> None:
    known = sorted(
        (c for c in components if is_known_version(c.version)),
        key=lambda x: (x.name.lower(), x.version, x.root),
    )
    unknown = sorted(
        (c for c in components if not is_known_version(c.version)),
        key=lambda x: (x.name.lower(), x.root),
    )

    known_path = Path(known_path)
    unknown_path = Path(unknown_path)
    known_path.parent.mkdir(parents=True, exist_ok=True)
    unknown_path.parent.mkdir(parents=True, exist_ok=True)
    known_path.write_text(
        json.dumps(make_bom(known, name="known"), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    unknown_path.write_text(
        json.dumps(make_bom(unknown, name="unknown"), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

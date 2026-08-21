from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class EvidenceKind(str, Enum):
    IDENTITY = "identity"
    VERSION = "version"
    FINGERPRINT = "fingerprint"
    VCS = "vcs"


@dataclass(frozen=True, slots=True)
class FileRecord:
    abs_path: Path
    rel_path: str
    directory: str
    name: str
    name_lower: str
    suffix: str
    size: int


@dataclass(slots=True)
class TreeIndex:
    root: Path
    files: tuple[FileRecord, ...]
    by_dir: dict[str, tuple[FileRecord, ...]]
    by_name: dict[str, tuple[FileRecord, ...]]
    directories: frozenset[str]
    git_roots: frozenset[str]


@dataclass(slots=True)
class Evidence:
    kind: EvidenceKind
    component: str
    version: str = "unknown"
    confidence: float = 0.0
    method: str = ""
    source_file: str = ""
    vendor: str = ""
    vcs: str = ""
    cpe: str = ""
    # Critical invariant: version/context evidence may describe a candidate,
    # but it cannot create component identity unless this flag is true.
    identity_confirming: bool = False
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class FingerprintSummary:
    """Component-identity evidence from source fingerprints only."""

    component: str
    confidence: float
    coverage: float
    exact_matches: int
    normalized_matches: int
    matched_segments: int
    total_segments: int
    matched_files: int
    sampled_files: int = 0
    # v0.5: discriminative fingerprint metrics. IDF is normalized to 0..1,
    # where 1 means the hash is PRIMARY code of only one catalog component.
    mean_idf: float = 0.0
    high_idf_matches: int = 0
    shared_matches: int = 0
    # Fraction of matched fingerprint segments that also occur as PRIMARY
    # code in more than one catalog component. 0.0 means fully distinctive.
    shared_ratio: float = 0.0
    weighted_score: float = 0.0
    methods: tuple[str, ...] = ()
    source_examples: tuple[str, ...] = ()


@dataclass(slots=True)
class CheckerMetadataObservation:
    """Trusted checker metadata observed at one component context.

    This object never establishes identity. It can only enrich an already
    fingerprint-confirmed descendant of the same component.
    """

    root: str
    component: str
    version: str = "unknown"
    confidence: float = 0.0
    vendor: str = ""
    vcs: str = ""
    cpe: str = ""
    methods: tuple[str, ...] = ()
    evidence_files: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()


@dataclass(slots=True)
class FingerprintRejection:
    component: str
    root: str
    stage: str
    reject_reason: str
    confidence: float = 0.0
    coverage: float = 0.0
    exact_matches: int = 0
    normalized_matches: int = 0
    matched_segments: int = 0
    total_segments: int = 0
    matched_files: int = 0
    sampled_files: int = 0
    mean_idf: float = 0.0
    high_idf_matches: int = 0
    shared_matches: int = 0
    shared_ratio: float = 0.0
    weighted_score: float = 0.0


@dataclass(slots=True)
class ResolvedComponent:
    name: str
    version: str
    confidence: float
    root: str
    vendor: str = ""
    vcs: str = ""
    cpe: str = ""
    identity_confirmed: bool = True
    identity_methods: tuple[str, ...] = ()
    methods: tuple[str, ...] = ()
    evidence_files: tuple[str, ...] = ()
    fingerprint_coverage: float | None = None
    fingerprint_exact_matches: int = 0
    fingerprint_normalized_matches: int = 0
    fingerprint_matched_segments: int = 0
    fingerprint_total_segments: int = 0
    fingerprint_matched_files: int = 0
    fingerprint_sampled_files: int = 0
    fingerprint_mean_idf: float = 0.0
    fingerprint_high_idf_matches: int = 0
    fingerprint_shared_matches: int = 0
    fingerprint_shared_ratio: float = 0.0
    fingerprint_weighted_score: float = 0.0
    conflicts: tuple[str, ...] = ()
    metadata_version_source_root: str = ""


@dataclass(slots=True)
class ScanStats:
    files_indexed: int = 0
    component_contexts: int = 0
    checker_profiles: int = 0
    checker_invocations: int = 0
    fingerprint_contexts: int = 0
    fingerprint_segments: int = 0
    fingerprint_exact_hits: int = 0
    fingerprint_normalized_hits: int = 0
    fingerprint_non_primary_hits_ignored: int = 0
    fingerprint_high_fanout_hits_ignored: int = 0
    fingerprint_candidates_rejected: int = 0
    fingerprint_rejections_by_reason: dict[str, int] = field(default_factory=dict)
    metadata_versions_inherited: int = 0
    components_before_collapse: int = 0
    ownership_family_components_collapsed: int = 0
    exact_duplicate_components_collapsed: int = 0
    components_collapsed: int = 0
    timings: dict[str, float] = field(default_factory=dict)

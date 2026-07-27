"""Score curated NASP drafts against gold compendium files.

The headline metric is core-tier endpoint recovery, with biologically
equivalent gold representations collapsed into one recall unit. Relationship,
polarity, and evidence agreement remain stricter diagnostics layered on the
endpoint match.

Matching normalizes node and relationship strings with the same
`normalize_term` used by the vocabulary gate, so mechanical variants (case,
plurals, `_accumulation`/`_signaling` suffixes) do not count a correct edge as
both missed and extra. Each draft edge pairs with at most one gold edge, so a
differently-worded-but-correct edge is classified once (relationship-only,
evidence-only, or direction difference) rather than penalized twice.
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any

import yaml  # type: ignore

from nasp_compendium.vocab_tiers import normalize_term


_CORRELATIVE_RELS: frozenset[str] = frozenset(
    {"correlates", "negatively_correlates", "does_not_correlate"}
)

_RELATION_POLARITY: dict[str, str] = {
    "activates": "positive",
    "causes": "positive",
    "correlates": "positive",
    "drives": "positive",
    "induces": "positive",
    "required_for": "positive",
    "upregulates": "positive",
    "downregulates": "negative",
    "inhibits": "negative",
    "negatively_correlates": "negative",
    "suppresses": "negative",
    "does_not_correlate": "absent",
    "does_not_drive": "absent",
}


@dataclasses.dataclass(frozen=True)
class EdgeRecord:
    """Normalized edge record used for scoring."""

    source: str
    target: str
    rel: str
    evidence_strength: str
    chain_id: str
    step: str
    context: str
    support: str

    @property
    def triple(self) -> tuple[str, str, str]:
        """Return the exact source-target-relationship scoring triple."""
        return (self.source, self.target, self.rel)

    @property
    def endpoints(self) -> tuple[str, str]:
        """Return the directed source-target endpoints."""
        return (self.source, self.target)

    @property
    def norm_endpoints(self) -> tuple[str, str]:
        """Return normalized source-target endpoints for matching."""
        return (normalize_term(self.source), normalize_term(self.target))

    @property
    def norm_triple(self) -> tuple[str, str, str]:
        """Return the normalized source-target-relationship triple."""
        return (
            normalize_term(self.source),
            normalize_term(self.target),
            normalize_term(self.rel),
        )


@dataclasses.dataclass(frozen=True)
class EdgeMismatch:
    """A paired draft/gold match sharing normalized endpoints."""

    gold: EdgeRecord
    draft: EdgeRecord


@dataclasses.dataclass(frozen=True)
class PaperScore:
    """Scoring result for one draft/gold paper pair."""

    paper_id: str
    draft_path: str
    gold_path: str
    gold_total: int
    draft_total: int
    endpoint_recovered: int
    triple_recovered: int
    exact_recovered: int
    relationship_mismatches: list[EdgeMismatch]
    polarity_mismatches: list[EdgeMismatch]
    evidence_mismatches: list[EdgeMismatch]
    symmetric_direction_differences: list[EdgeMismatch]
    missed: list[EdgeRecord]
    extra: list[EdgeRecord]
    excluded_gold_defects: list[EdgeRecord]
    core_units: int = 0
    core_recovered: int = 0
    supporting_units: int = 0
    supporting_recovered: int = 0
    shortcut_violations: list[EdgeMismatch] = dataclasses.field(
        default_factory=list
    )


@dataclasses.dataclass(frozen=True)
class ScoreReport:
    """Scoring result for one or more paper pairs."""

    papers: list[PaperScore]

    @property
    def gold_total(self) -> int:
        """Return total scored gold edges."""
        return sum(paper.gold_total for paper in self.papers)

    @property
    def draft_total(self) -> int:
        """Return total draft edges."""
        return sum(paper.draft_total for paper in self.papers)

    @property
    def endpoint_recovered_total(self) -> int:
        """Return total gold edges recovered at the endpoint level."""
        return sum(paper.endpoint_recovered for paper in self.papers)

    @property
    def triple_recovered_total(self) -> int:
        """Return total gold edges recovered with matching relationship."""
        return sum(paper.triple_recovered for paper in self.papers)

    @property
    def exact_recovered_total(self) -> int:
        """Return total gold edges recovered with matching triple+evidence."""
        return sum(paper.exact_recovered for paper in self.papers)

    @property
    def missed_total(self) -> int:
        """Return total gold edges with no endpoint match."""
        return sum(len(paper.missed) for paper in self.papers)

    @property
    def extra_total(self) -> int:
        """Return total draft edges with no endpoint match."""
        return sum(len(paper.extra) for paper in self.papers)

    @property
    def excluded_gold_defects_total(self) -> int:
        """Return total excluded gold-defect edges."""
        return sum(len(paper.excluded_gold_defects) for paper in self.papers)

    @property
    def relationship_mismatches_total(self) -> int:
        """Return total same-endpoint relationship mismatches."""
        return sum(len(paper.relationship_mismatches) for paper in self.papers)

    @property
    def polarity_mismatches_total(self) -> int:
        """Return total relationship mismatches that change polarity."""
        return sum(len(paper.polarity_mismatches) for paper in self.papers)

    @property
    def evidence_mismatches_total(self) -> int:
        """Return total matched triples with mismatched evidence strength."""
        return sum(len(paper.evidence_mismatches) for paper in self.papers)

    @property
    def symmetric_direction_differences_total(self) -> int:
        """Return total reversed symmetric-correlation pairs."""
        return sum(
            len(paper.symmetric_direction_differences) for paper in self.papers
        )

    @property
    def endpoint_recall(self) -> float:
        """Return endpoint recall over scored gold edges."""
        return _ratio(self.endpoint_recovered_total, self.gold_total)

    @property
    def endpoint_precision(self) -> float:
        """Return endpoint precision over draft edges."""
        return _ratio(self.endpoint_recovered_total, self.draft_total)

    @property
    def core_units_total(self) -> int:
        """Return total core recall units after equivalence collapsing."""
        return sum(paper.core_units for paper in self.papers)

    @property
    def core_recovered_total(self) -> int:
        """Return total recovered core recall units."""
        return sum(paper.core_recovered for paper in self.papers)

    @property
    def supporting_units_total(self) -> int:
        """Return total supporting units after equivalence collapsing."""
        return sum(paper.supporting_units for paper in self.papers)

    @property
    def supporting_recovered_total(self) -> int:
        """Return total recovered supporting recall units."""
        return sum(paper.supporting_recovered for paper in self.papers)

    @property
    def shortcut_violations_total(self) -> int:
        """Return total draft edges matching forbidden shortcuts."""
        return sum(len(paper.shortcut_violations) for paper in self.papers)

    @property
    def core_recall(self) -> float:
        """Return headline core-tier recall."""
        return _ratio(self.core_recovered_total, self.core_units_total)

    @property
    def supporting_recall(self) -> float:
        """Return separately reported supporting-tier recall."""
        return _ratio(
            self.supporting_recovered_total,
            self.supporting_units_total,
        )

    @property
    def relationship_recall(self) -> float:
        """Return signed relationship recall over scored gold edges."""
        return _ratio(self.triple_recovered_total, self.gold_total)

    @property
    def relationship_precision(self) -> float:
        """Return signed relationship precision over draft edges."""
        return _ratio(self.triple_recovered_total, self.draft_total)

    @property
    def exact_recall(self) -> float:
        """Return relationship-and-evidence recall over scored gold edges."""
        return _ratio(self.exact_recovered_total, self.gold_total)


def score_paths(
    draft_path: Path,
    gold_path: Path,
    *,
    draft_glob: str = "*.md",
    gold_glob: str = "*.gold.md",
    drop_gold_defects: bool = True,
) -> ScoreReport:
    """Score one draft/gold file pair or directories of pairs.

    Args:
      draft_path: Draft file or directory.
      gold_path: Gold file or directory.
      draft_glob: Glob used when `draft_path` is a directory.
      gold_glob: Glob used when `gold_path` is a directory.
      drop_gold_defects: Whether to exclude gold edges flagged as defects.

    Returns:
      ScoreReport containing per-paper scores.
    """
    pairs = _resolve_pairs(
        draft_path=draft_path,
        gold_path=gold_path,
        draft_glob=draft_glob,
        gold_glob=gold_glob,
    )
    return ScoreReport(
        papers=[
            score_pair(
                draft_file=draft_file,
                gold_file=gold_file,
                paper_id=paper_id,
                drop_gold_defects=drop_gold_defects,
            )
            for paper_id, draft_file, gold_file in pairs
        ]
    )


def score_pair(
    draft_file: Path,
    gold_file: Path,
    *,
    paper_id: str | None = None,
    drop_gold_defects: bool = True,
) -> PaperScore:
    """Score one draft file against one gold file.

    Args:
      draft_file: Draft YAML-in-Markdown file.
      gold_file: Gold YAML-in-Markdown file.
      paper_id: Optional paper id for reporting.
      drop_gold_defects: Whether to exclude gold edges flagged as defects.

    Returns:
      PaperScore for the pair.
    """
    draft_loaded = _load_edges(draft_file)
    raw_gold_edges = _load_edges(gold_file)
    draft_edges = [
        edge.record
        for edge in draft_loaded
        if not edge.is_forbidden and not edge.is_excluded
    ]

    excluded_gold_defects: list[EdgeRecord] = []
    forbidden_edges: list[_LoadedEdge] = []
    scored_gold: list[_LoadedEdge] = []
    for edge in raw_gold_edges:
        if drop_gold_defects and edge.is_excluded:
            excluded_gold_defects.append(edge.record)
        elif edge.is_forbidden:
            forbidden_edges.append(edge)
        else:
            scored_gold.append(edge)

    gold_edges = [edge.record for edge in scored_gold]
    match = _match_edges(draft_edges, gold_edges)
    extra, shortcut_violations = _split_shortcut_violations(
        match.extra,
        forbidden_edges,
    )
    core_units, core_recovered, supporting_units, supporting_recovered = (
        _tier_units(scored_gold, match.recovered_gold_indices)
    )
    missed = _missed_after_equiv_collapse(
        scored_gold,
        match.recovered_gold_indices,
    )

    return PaperScore(
        paper_id=paper_id or _paper_key_from_path(draft_file),
        draft_path=str(draft_file),
        gold_path=str(gold_file),
        gold_total=len(gold_edges),
        draft_total=len(draft_edges),
        endpoint_recovered=len(match.pairs),
        triple_recovered=match.triple_recovered,
        exact_recovered=match.exact_recovered,
        relationship_mismatches=match.relationship_mismatches,
        polarity_mismatches=match.polarity_mismatches,
        evidence_mismatches=match.evidence_mismatches,
        symmetric_direction_differences=match.symmetric_direction_differences,
        missed=missed,
        extra=extra,
        excluded_gold_defects=excluded_gold_defects,
        core_units=core_units,
        core_recovered=core_recovered,
        supporting_units=supporting_units,
        supporting_recovered=supporting_recovered,
        shortcut_violations=shortcut_violations,
    )


@dataclasses.dataclass(frozen=True)
class _LoadedEdge:
    """An edge record plus optional gold-scoring metadata."""

    record: EdgeRecord
    is_excluded: bool
    tier: str = "core"
    equiv_group: str = ""
    is_forbidden: bool = False


@dataclasses.dataclass
class _MatchResult:
    """Structured output of one-to-one draft/gold matching."""

    pairs: list[EdgeMismatch]
    triple_recovered: int
    exact_recovered: int
    relationship_mismatches: list[EdgeMismatch]
    polarity_mismatches: list[EdgeMismatch]
    evidence_mismatches: list[EdgeMismatch]
    symmetric_direction_differences: list[EdgeMismatch]
    missed: list[EdgeRecord]
    extra: list[EdgeRecord]
    recovered_gold_indices: set[int]


def _match_edges(
    draft_edges: list[EdgeRecord],
    gold_edges: list[EdgeRecord],
) -> _MatchResult:
    """Pair gold and draft edges by endpoint, best signed matches first.

    Builds every gold/draft candidate that shares normalized endpoints (or
    reversed endpoints for symmetric correlative relationships), ranks pairs by
    match quality, and greedily assigns so each gold and draft edge is used at
    most once. Exact signed relationships outrank same-endpoint alternatives.
    """
    candidates: list[tuple[int, int, int, bool]] = []
    for gold_index, gold_edge in enumerate(gold_edges):
        for draft_index, draft_edge in enumerate(draft_edges):
            endpoint_match, reversed_direction = _endpoints_match(
                gold_edge, draft_edge
            )
            if not endpoint_match:
                continue
            rank = _pair_rank(gold_edge, draft_edge, reversed_direction)
            candidates.append(
                (rank, gold_index, draft_index, reversed_direction)
            )

    candidates.sort(key=lambda item: item[0], reverse=True)
    used_gold: set[int] = set()
    used_draft: set[int] = set()

    pairs: list[EdgeMismatch] = []
    relationship_mismatches: list[EdgeMismatch] = []
    polarity_mismatches: list[EdgeMismatch] = []
    evidence_mismatches: list[EdgeMismatch] = []
    symmetric_direction_differences: list[EdgeMismatch] = []
    triple_recovered = 0
    exact_recovered = 0

    for _, gold_index, draft_index, reversed_direction in candidates:
        if gold_index in used_gold or draft_index in used_draft:
            continue
        used_gold.add(gold_index)
        used_draft.add(draft_index)
        gold_edge = gold_edges[gold_index]
        draft_edge = draft_edges[draft_index]
        mismatch = EdgeMismatch(gold=gold_edge, draft=draft_edge)
        pairs.append(mismatch)

        if reversed_direction:
            symmetric_direction_differences.append(mismatch)
        if not _relations_match(gold_edge.rel, draft_edge.rel):
            relationship_mismatches.append(mismatch)
            if _is_polarity_mismatch(gold_edge.rel, draft_edge.rel):
                polarity_mismatches.append(mismatch)
            continue
        triple_recovered += 1
        if gold_edge.evidence_strength == draft_edge.evidence_strength:
            exact_recovered += 1
        else:
            evidence_mismatches.append(mismatch)

    missed = [
        edge for index, edge in enumerate(gold_edges) if index not in used_gold
    ]
    extra = [
        edge
        for index, edge in enumerate(draft_edges)
        if index not in used_draft
    ]
    return _MatchResult(
        pairs=pairs,
        triple_recovered=triple_recovered,
        exact_recovered=exact_recovered,
        relationship_mismatches=relationship_mismatches,
        polarity_mismatches=polarity_mismatches,
        evidence_mismatches=evidence_mismatches,
        symmetric_direction_differences=symmetric_direction_differences,
        missed=missed,
        extra=extra,
        recovered_gold_indices=set(used_gold),
    )


def _tier_units(
    scored_gold: list[_LoadedEdge],
    recovered_gold_indices: set[int],
) -> tuple[int, int, int, int]:
    """Return tiered unit and recovery counts after equivalence collapsing."""
    groups: dict[str, dict[str, bool]] = {}
    for index, edge in enumerate(scored_gold):
        key = edge.equiv_group or f"__singleton_{index}"
        entry = groups.setdefault(
            key,
            {"has_core": False, "recovered": False},
        )
        if edge.tier == "core":
            entry["has_core"] = True
        if index in recovered_gold_indices:
            entry["recovered"] = True

    core_units = core_recovered = 0
    supporting_units = supporting_recovered = 0
    for entry in groups.values():
        if entry["has_core"]:
            core_units += 1
            core_recovered += int(entry["recovered"])
        else:
            supporting_units += 1
            supporting_recovered += int(entry["recovered"])
    return core_units, core_recovered, supporting_units, supporting_recovered


def _missed_after_equiv_collapse(
    scored_gold: list[_LoadedEdge],
    recovered_gold_indices: set[int],
) -> list[EdgeRecord]:
    """Return unmatched gold edges, excluding satisfied group alternates."""
    satisfied_groups = {
        edge.equiv_group
        for index, edge in enumerate(scored_gold)
        if edge.equiv_group and index in recovered_gold_indices
    }
    return [
        edge.record
        for index, edge in enumerate(scored_gold)
        if index not in recovered_gold_indices
        and edge.equiv_group not in satisfied_groups
    ]


def _split_shortcut_violations(
    extra: list[EdgeRecord],
    forbidden_edges: list[_LoadedEdge],
) -> tuple[list[EdgeRecord], list[EdgeMismatch]]:
    """Split unmatched draft edges into extras and forbidden shortcuts."""
    forbidden_by_endpoints: dict[tuple[str, str], EdgeRecord] = {}
    for edge in forbidden_edges:
        forbidden_by_endpoints.setdefault(
            edge.record.norm_endpoints,
            edge.record,
        )

    remaining: list[EdgeRecord] = []
    violations: list[EdgeMismatch] = []
    for draft_edge in extra:
        gold_edge = forbidden_by_endpoints.get(draft_edge.norm_endpoints)
        if gold_edge is None:
            remaining.append(draft_edge)
        else:
            violations.append(EdgeMismatch(gold=gold_edge, draft=draft_edge))
    return remaining, violations


def _endpoints_match(
    gold_edge: EdgeRecord,
    draft_edge: EdgeRecord,
) -> tuple[bool, bool]:
    """Return whether endpoints match and whether the match is reversed.

    Reversed matches are only allowed for symmetric correlative relationships,
    where direction carries no biological meaning.
    """
    if gold_edge.norm_endpoints == draft_edge.norm_endpoints:
        return True, False
    both_correlative = (
        gold_edge.rel in _CORRELATIVE_RELS
        and draft_edge.rel in _CORRELATIVE_RELS
    )
    reversed_match = gold_edge.norm_endpoints == (
        draft_edge.norm_endpoints[1],
        draft_edge.norm_endpoints[0],
    )
    if both_correlative and reversed_match:
        return True, True
    return False, False


def _pair_rank(
    gold_edge: EdgeRecord,
    draft_edge: EdgeRecord,
    _reversed_direction: bool,
) -> int:
    """Return a match-quality rank so better pairs are assigned first."""
    if _relations_match(gold_edge.rel, draft_edge.rel):
        if gold_edge.evidence_strength == draft_edge.evidence_strength:
            return 5
        return 4
    if not _is_polarity_mismatch(gold_edge.rel, draft_edge.rel):
        return 3
    return 2


def _relations_match(gold_rel: str, draft_rel: str) -> bool:
    """Return whether relation labels match after mechanical normalization."""
    return normalize_term(gold_rel) == normalize_term(draft_rel)


def _is_polarity_mismatch(gold_rel: str, draft_rel: str) -> bool:
    """Return whether two controlled relations assert different polarities."""
    gold_polarity = _RELATION_POLARITY.get(gold_rel)
    draft_polarity = _RELATION_POLARITY.get(draft_rel)
    return (
        gold_polarity is not None
        and draft_polarity is not None
        and gold_polarity != draft_polarity
    )


def format_score_report(
    report: ScoreReport, output_format: str = "text"
) -> str:
    """Format a ScoreReport as text or JSON."""
    if output_format == "json":
        return json.dumps(_report_to_dict(report), indent=2, sort_keys=True)

    lines = [
        "# NASP compendium score",
        "",
        (
            f"Core recall: {report.core_recovered_total}/"
            f"{report.core_units_total} ({report.core_recall:.0%}); "
            f"supporting recall: {report.supporting_recovered_total}/"
            f"{report.supporting_units_total} "
            f"({report.supporting_recall:.0%}); forbidden-shortcut "
            f"violations: {report.shortcut_violations_total}."
        ),
        (
            f"Relationship recall: {report.triple_recovered_total}/"
            f"{report.gold_total} ({report.relationship_recall:.0%}); "
            f"relationship precision: {report.triple_recovered_total}/"
            f"{report.draft_total} ({report.relationship_precision:.0%})."
        ),
        (
            f"Evidence-matched exact recall: {report.exact_recovered_total}/"
            f"{report.gold_total} ({report.exact_recall:.0%}); endpoint "
            f"overlap (diagnostic only): {report.endpoint_recovered_total}/"
            f"{report.gold_total} recall, {report.endpoint_recovered_total}/"
            f"{report.draft_total} precision."
        ),
        (
            f"Missed (no endpoint match): {report.missed_total}; "
            f"extra (no endpoint match): {report.extra_total}; "
            f"relationship-only: {report.relationship_mismatches_total}; "
            f"polarity: {report.polarity_mismatches_total}; "
            f"evidence-only: {report.evidence_mismatches_total}; "
            "symmetric-correlation direction: "
            f"{report.symmetric_direction_differences_total}; "
            f"forbidden shortcuts: {report.shortcut_violations_total}; "
            f"excluded gold defects: {report.excluded_gold_defects_total}."
        ),
        "",
    ]
    for paper in report.papers:
        lines.extend(_format_paper_score(paper))
    return "\n".join(lines).rstrip() + "\n"


def write_score_report(
    report: ScoreReport,
    output_path: Path,
    output_format: str = "json",
) -> Path:
    """Write a formatted score report to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        format_score_report(report, output_format=output_format)
    )
    return output_path


def _ratio(numerator: int, denominator: int) -> float:
    """Return numerator/denominator, or 0.0 when the denominator is zero."""
    return numerator / denominator if denominator else 0.0


def _resolve_pairs(
    *,
    draft_path: Path,
    gold_path: Path,
    draft_glob: str,
    gold_glob: str,
) -> list[tuple[str, Path, Path]]:
    """Resolve draft/gold file pairs from file or directory inputs."""
    if draft_path.is_file() and gold_path.is_file():
        return [(_paper_key_from_path(draft_path), draft_path, gold_path)]

    if not draft_path.exists():
        raise FileNotFoundError(f"Draft path not found: {draft_path}")
    if not gold_path.exists():
        raise FileNotFoundError(f"Gold path not found: {gold_path}")
    if not draft_path.is_dir() or not gold_path.is_dir():
        raise ValueError(
            "Draft and gold inputs must both be files or both be directories."
        )

    drafts = {
        _paper_key_from_path(path): path
        for path in sorted(draft_path.glob(draft_glob))
        if _is_reviewable_file(path) and not path.name.endswith(".gold.md")
    }
    golds = {
        _paper_key_from_path(path): path
        for path in sorted(gold_path.glob(gold_glob))
        if _is_reviewable_file(path)
    }

    pairs: list[tuple[str, Path, Path]] = []
    for paper_id, draft_file in sorted(drafts.items()):
        gold_file = golds.get(paper_id)
        if gold_file is None:
            continue
        pairs.append((paper_id, draft_file, gold_file))

    if not pairs:
        raise FileNotFoundError(
            f"No draft/gold pairs matched {draft_path}/{draft_glob} "
            f"against {gold_path}/{gold_glob}."
        )
    return pairs


def _is_reviewable_file(
    path: Path,
    suffixes: tuple[str, ...] = (".md", ".yaml", ".yml"),
) -> bool:
    """Return whether a file has a supported YAML-in-Markdown suffix."""
    return path.is_file() and path.suffix in suffixes


def _paper_key_from_path(path: Path) -> str:
    """Return a comparable paper key from a draft or gold filename."""
    name = path.name
    for suffix in (
        ".post_patch.draft.md",
        ".draft.md",
        ".gold.md",
        ".md",
        ".yaml",
        ".yml",
    ):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    return name.lower()


def _load_edges(path: Path) -> list[_LoadedEdge]:
    """Load edge records and scoring metadata from a compendium file."""
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        return []
    edges = data.get("edges")
    if not isinstance(edges, list):
        return []
    return [_loaded_edge(edge) for edge in edges if isinstance(edge, dict)]


def _loaded_edge(edge: dict[str, Any]) -> _LoadedEdge:
    """Return one edge with parsed tier, group, and status metadata."""
    return _LoadedEdge(
        record=_edge_record(edge),
        is_excluded=_is_excluded(edge),
        tier=_edge_tier(edge),
        equiv_group=str(edge.get("equiv_group", "")).strip(),
        is_forbidden=_is_forbidden_shortcut(edge),
    )


def _edge_tier(edge: dict[str, Any]) -> str:
    """Return an edge tier, defaulting absent or unknown values to core."""
    tier = str(edge.get("tier", "")).strip().lower()
    return tier if tier in {"core", "supporting"} else "core"


def _is_forbidden_shortcut(edge: dict[str, Any]) -> bool:
    """Return whether an edge is a forbidden-shortcut anti-edge."""
    return str(edge.get("status", "")).strip().lower() == ("forbidden_shortcut")


def _edge_record(edge: dict[str, Any]) -> EdgeRecord:
    """Convert an edge mapping to a normalized EdgeRecord."""
    return EdgeRecord(
        source=str(edge.get("source", "")),
        target=str(edge.get("target", "")),
        rel=str(edge.get("rel", "")),
        evidence_strength=str(edge.get("evidence_strength", "")),
        chain_id=str(edge.get("chain_id", "")),
        step=str(edge.get("step", "")),
        context=str(edge.get("context", "")),
        support=str(edge.get("support", "")),
    )


def _is_excluded(edge: dict[str, Any]) -> bool:
    """Return whether a gold edge is flagged as excluded from scoring.

    Exclusion is a structured decision on the edge mapping: `score_exclude:
    true` or `status: excluded`. Prose annotations are not scanned.
    """
    if str(edge.get("status", "")).strip().lower() == "excluded":
        return True
    flag = edge.get("score_exclude")
    if isinstance(flag, bool):
        return flag
    return str(flag).strip().lower() in {"1", "true", "yes"}


def _report_to_dict(report: ScoreReport) -> dict[str, Any]:
    """Convert a ScoreReport to a JSON-serializable dictionary."""
    return {
        "summary": {
            "gold_total": report.gold_total,
            "draft_total": report.draft_total,
            "core_units_total": report.core_units_total,
            "core_recovered_total": report.core_recovered_total,
            "core_recall": round(report.core_recall, 4),
            "supporting_units_total": report.supporting_units_total,
            "supporting_recovered_total": report.supporting_recovered_total,
            "supporting_recall": round(report.supporting_recall, 4),
            "shortcut_violations_total": report.shortcut_violations_total,
            "endpoint_recovered_total": report.endpoint_recovered_total,
            "endpoint_recall": round(report.endpoint_recall, 4),
            "endpoint_precision": round(report.endpoint_precision, 4),
            "triple_recovered_total": report.triple_recovered_total,
            "relationship_recall": round(report.relationship_recall, 4),
            "relationship_precision": round(report.relationship_precision, 4),
            "exact_recovered_total": report.exact_recovered_total,
            "exact_recall": round(report.exact_recall, 4),
            "missed_total": report.missed_total,
            "extra_total": report.extra_total,
            "relationship_mismatches_total": (
                report.relationship_mismatches_total
            ),
            "polarity_mismatches_total": report.polarity_mismatches_total,
            "evidence_mismatches_total": report.evidence_mismatches_total,
            "symmetric_direction_differences_total": (
                report.symmetric_direction_differences_total
            ),
            "excluded_gold_defects_total": report.excluded_gold_defects_total,
        },
        "papers": [_paper_to_dict(paper) for paper in report.papers],
    }


def _paper_to_dict(paper: PaperScore) -> dict[str, Any]:
    """Convert a PaperScore to a JSON-serializable dictionary."""
    return {
        "paper_id": paper.paper_id,
        "draft_path": paper.draft_path,
        "gold_path": paper.gold_path,
        "gold_total": paper.gold_total,
        "draft_total": paper.draft_total,
        "core_units": paper.core_units,
        "core_recovered": paper.core_recovered,
        "supporting_units": paper.supporting_units,
        "supporting_recovered": paper.supporting_recovered,
        "endpoint_recovered": paper.endpoint_recovered,
        "triple_recovered": paper.triple_recovered,
        "exact_recovered": paper.exact_recovered,
        "missed": [_edge_to_dict(edge) for edge in paper.missed],
        "extra": [_edge_to_dict(edge) for edge in paper.extra],
        "relationship_mismatches": [
            _mismatch_to_dict(mismatch)
            for mismatch in paper.relationship_mismatches
        ],
        "polarity_mismatches": [
            _mismatch_to_dict(mismatch)
            for mismatch in paper.polarity_mismatches
        ],
        "shortcut_violations": [
            _mismatch_to_dict(mismatch)
            for mismatch in paper.shortcut_violations
        ],
        "evidence_mismatches": [
            _mismatch_to_dict(mismatch)
            for mismatch in paper.evidence_mismatches
        ],
        "symmetric_direction_differences": [
            _mismatch_to_dict(mismatch)
            for mismatch in paper.symmetric_direction_differences
        ],
        "excluded_gold_defects": [
            _edge_to_dict(edge) for edge in paper.excluded_gold_defects
        ],
    }


def _edge_to_dict(edge: EdgeRecord) -> dict[str, str]:
    """Convert an EdgeRecord to a JSON-serializable dictionary."""
    return dataclasses.asdict(edge)


def _mismatch_to_dict(mismatch: EdgeMismatch) -> dict[str, Any]:
    """Convert an EdgeMismatch to a JSON-serializable dictionary."""
    return {
        "gold": _edge_to_dict(mismatch.gold),
        "draft": _edge_to_dict(mismatch.draft),
    }


def _format_paper_score(paper: PaperScore) -> list[str]:
    """Format one paper score as Markdown text."""
    lines = [
        f"## {paper.paper_id}",
        "",
        (
            f"- Core recall: {paper.core_recovered}/{paper.core_units}; "
            f"supporting recall: {paper.supporting_recovered}/"
            f"{paper.supporting_units}; forbidden-shortcut violations: "
            f"{len(paper.shortcut_violations)}"
        ),
        (
            f"- Relationship-matched: {paper.triple_recovered}/"
            f"{paper.gold_total}; "
            f"evidence-matched (exact): {paper.exact_recovered}/"
            f"{paper.gold_total}; endpoint overlap (diagnostic): "
            f"{paper.endpoint_recovered}/{paper.gold_total}; "
            f"draft edges: {paper.draft_total}"
        ),
        f"- Missed (no endpoint match): {len(paper.missed)}",
        f"- Extra (no endpoint match): {len(paper.extra)}",
        f"- Relationship-only mismatches: {len(paper.relationship_mismatches)}",
        f"- Polarity mismatches: {len(paper.polarity_mismatches)}",
        f"- Evidence-strength mismatches: {len(paper.evidence_mismatches)}",
        (
            "- Symmetric correlation direction differences: "
            f"{len(paper.symmetric_direction_differences)}"
        ),
        f"- Excluded gold defects: {len(paper.excluded_gold_defects)}",
        "",
    ]
    if paper.missed:
        lines.append("Missed:")
        lines.extend(f"- {_format_edge(edge)}" for edge in paper.missed)
        lines.append("")
    if paper.extra:
        lines.append("Extra:")
        lines.extend(f"- {_format_edge(edge)}" for edge in paper.extra)
        lines.append("")
    if paper.shortcut_violations:
        lines.append("Forbidden-shortcut violations:")
        lines.extend(
            f"- draft {_format_edge(mismatch.draft)} | "
            f"forbidden {_format_edge(mismatch.gold)}"
            for mismatch in paper.shortcut_violations
        )
        lines.append("")
    if paper.relationship_mismatches:
        lines.append("Relationship-only (endpoints match, verb differs):")
        lines.extend(
            f"- gold {_format_edge(mismatch.gold)} | "
            f"draft {_format_edge(mismatch.draft)}"
            for mismatch in paper.relationship_mismatches
        )
        lines.append("")
    return lines


def _format_edge(edge: EdgeRecord) -> str:
    """Format one edge for human-readable output."""
    return f"{edge.source} --[{edge.rel}/{edge.evidence_strength}]--> {edge.target}"  # noqa: E501

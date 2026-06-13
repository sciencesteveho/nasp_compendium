"""Score curated NASP drafts against gold compendium files."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any

import yaml  # type: ignore


REVIEWABLE_SUFFIXES: tuple[str, ...] = (".md", ".yaml", ".yml")
CORRELATIVE_RELS: frozenset[str] = frozenset(
    {"correlates", "negatively_correlates", "does_not_correlate"}
)
GOLD_DEFECT_PHRASES: tuple[str, ...] = (
    "almost certainly wrong",
    "recommend: drop this edge",
    "possible non-edge",
    "placeholder",
    "score_exclude",
    "gold defect",
)


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


@dataclasses.dataclass(frozen=True)
class EdgeMismatch:
    """A paired draft/gold mismatch sharing some edge identity."""

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
    recovered_total: int
    missed: list[EdgeRecord]
    extra: list[EdgeRecord]
    relationship_mismatches: list[EdgeMismatch]
    evidence_mismatches: list[EdgeMismatch]
    symmetric_correlation_differences: list[EdgeMismatch]
    dropped_gold_defects: list[EdgeRecord]


@dataclasses.dataclass(frozen=True)
class ScoreReport:
    """Scoring result for one or more paper pairs."""

    papers: list[PaperScore]

    @property
    def gold_total(self) -> int:
        """Return total scored gold triples."""
        return sum(paper.gold_total for paper in self.papers)

    @property
    def draft_total(self) -> int:
        """Return total draft triples."""
        return sum(paper.draft_total for paper in self.papers)

    @property
    def recovered_total(self) -> int:
        """Return total exact recovered triples."""
        return sum(paper.recovered_total for paper in self.papers)

    @property
    def missed_total(self) -> int:
        """Return total missed gold triples."""
        return sum(len(paper.missed) for paper in self.papers)

    @property
    def extra_total(self) -> int:
        """Return total extra draft triples."""
        return sum(len(paper.extra) for paper in self.papers)

    @property
    def dropped_gold_defects_total(self) -> int:
        """Return total excluded gold-defect triples."""
        return sum(len(paper.dropped_gold_defects) for paper in self.papers)

    @property
    def relationship_mismatches_total(self) -> int:
        """Return total same-endpoint relationship mismatches."""
        return sum(len(paper.relationship_mismatches) for paper in self.papers)

    @property
    def evidence_mismatches_total(self) -> int:
        """Return total exact triples with mismatched evidence strength."""
        return sum(len(paper.evidence_mismatches) for paper in self.papers)

    @property
    def symmetric_correlation_differences_total(self) -> int:
        """Return total reversed symmetric-correlation pairs."""
        return sum(
            len(paper.symmetric_correlation_differences)
            for paper in self.papers
        )

    @property
    def ordinary_missed_total(self) -> int:
        """Return missed edges excluding relationship/symmetric pairs."""
        return sum(len(ordinary_missed_edges(paper)) for paper in self.papers)

    @property
    def ordinary_extra_total(self) -> int:
        """Return extra edges excluding relationship/symmetric pairs."""
        return sum(len(ordinary_extra_edges(paper)) for paper in self.papers)

    @property
    def evidence_exact_recovered_total(self) -> int:
        """Return recovered triples that also match evidence strength."""
        return self.recovered_total - self.evidence_mismatches_total


def score_paths(
    draft_path: Path,
    gold_path: Path,
    *,
    draft_glob: str = "*.md",
    gold_glob: str = "*.gold.md",
    drop_gold_defects: bool = False,
) -> ScoreReport:
    """Score one draft/gold file pair or directories of pairs.

    Args:
      draft_path: Draft file or directory.
      gold_path: Gold file or directory.
      draft_glob: Glob used when `draft_path` is a directory.
      gold_glob: Glob used when `gold_path` is a directory.
      drop_gold_defects: Whether to remove gold edges annotated as defects.

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
    drop_gold_defects: bool = False,
) -> PaperScore:
    """Score one draft file against one gold file.

    Args:
      draft_file: Draft YAML-in-Markdown file.
      gold_file: Gold YAML-in-Markdown file.
      paper_id: Optional paper id for reporting.
      drop_gold_defects: Whether to remove gold edges annotated as defects.

    Returns:
      PaperScore for the pair.
    """
    draft_edges = _load_edges(draft_file)
    raw_gold_edges = _load_edges(gold_file)

    dropped_gold_defects: list[EdgeRecord] = []
    gold_edges: list[EdgeRecord] = []
    for edge in raw_gold_edges:
        if drop_gold_defects and _is_gold_defect(edge):
            dropped_gold_defects.append(edge)
        else:
            gold_edges.append(edge)

    recovered_keys = {
        edge.triple for edge in draft_edges
    } & {edge.triple for edge in gold_edges}
    missed = [edge for edge in gold_edges if edge.triple not in recovered_keys]
    extra = [edge for edge in draft_edges if edge.triple not in recovered_keys]

    return PaperScore(
        paper_id=paper_id or _paper_key_from_path(draft_file),
        draft_path=str(draft_file),
        gold_path=str(gold_file),
        gold_total=len(gold_edges),
        draft_total=len(draft_edges),
        recovered_total=len(recovered_keys),
        missed=missed,
        extra=extra,
        relationship_mismatches=_relationship_mismatches(missed, extra),
        evidence_mismatches=_evidence_mismatches(gold_edges, draft_edges),
        symmetric_correlation_differences=_symmetric_correlation_differences(
            missed, extra
        ),
        dropped_gold_defects=dropped_gold_defects,
    )


def format_score_report(report: ScoreReport, output_format: str = "text") -> str:
    """Format a ScoreReport as text or JSON."""
    if output_format == "json":
        return json.dumps(_report_to_dict(report), indent=2, sort_keys=True)

    lines = [
        "# NASP compendium score",
        "",
        (
            f"Total: recovered {report.recovered_total}/{report.gold_total}; "
            f"evidence-matched recovered "
            f"{report.evidence_exact_recovered_total}/{report.gold_total}; "
            f"draft edges {report.draft_total}; missed {report.missed_total}; "
            f"extra {report.extra_total}; "
            f"dropped gold defects {report.dropped_gold_defects_total}."
        ),
        (
            "Non-overlapping: "
            f"ordinary missed {report.ordinary_missed_total}; "
            f"ordinary extra {report.ordinary_extra_total}; "
            f"relationship-only {report.relationship_mismatches_total}; "
            f"evidence-only {report.evidence_mismatches_total}; "
            "symmetric-correlation direction "
            f"{report.symmetric_correlation_differences_total}."
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
    output_path.write_text(format_score_report(report, output_format=output_format))
    return output_path


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
        raise ValueError("Draft and gold inputs must both be files or both be directories.")

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


def _is_reviewable_file(path: Path) -> bool:
    """Return whether a file has a supported YAML-in-Markdown suffix."""
    return path.is_file() and path.suffix in REVIEWABLE_SUFFIXES


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


def _load_edges(path: Path) -> list[EdgeRecord]:
    """Load normalized edge records from a YAML-in-Markdown file."""
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        return []
    edges = data.get("edges")
    if not isinstance(edges, list):
        return []
    return [_edge_record(edge) for edge in edges if isinstance(edge, dict)]


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


def _is_gold_defect(edge: EdgeRecord) -> bool:
    """Return whether a gold edge is annotated as a scoring defect."""
    text = " ".join(
        [
            edge.context,
            edge.support,
            edge.source,
            edge.target,
            edge.rel,
        ]
    ).lower()
    return any(phrase in text for phrase in GOLD_DEFECT_PHRASES)


def _relationship_mismatches(
    missed: list[EdgeRecord],
    extra: list[EdgeRecord],
) -> list[EdgeMismatch]:
    """Return same-endpoint draft/gold pairs with different relations."""
    mismatches: list[EdgeMismatch] = []
    for gold_edge in missed:
        for draft_edge in extra:
            if gold_edge.endpoints == draft_edge.endpoints and gold_edge.rel != draft_edge.rel:
                mismatches.append(EdgeMismatch(gold=gold_edge, draft=draft_edge))
    return mismatches


def _evidence_mismatches(
    gold_edges: list[EdgeRecord],
    draft_edges: list[EdgeRecord],
) -> list[EdgeMismatch]:
    """Return exact triple matches with different evidence strengths."""
    draft_by_triple = {edge.triple: edge for edge in draft_edges}
    mismatches: list[EdgeMismatch] = []
    for gold_edge in gold_edges:
        draft_edge = draft_by_triple.get(gold_edge.triple)
        if draft_edge is None:
            continue
        if gold_edge.evidence_strength != draft_edge.evidence_strength:
            mismatches.append(EdgeMismatch(gold=gold_edge, draft=draft_edge))
    return mismatches


def _symmetric_correlation_differences(
    missed: list[EdgeRecord],
    extra: list[EdgeRecord],
) -> list[EdgeMismatch]:
    """Return reversed-endpoint correlation pairs."""
    differences: list[EdgeMismatch] = []
    for gold_edge in missed:
        if gold_edge.rel not in CORRELATIVE_RELS:
            continue
        for draft_edge in extra:
            if draft_edge.rel != gold_edge.rel:
                continue
            if (
                gold_edge.source == draft_edge.target
                and gold_edge.target == draft_edge.source
            ):
                differences.append(EdgeMismatch(gold=gold_edge, draft=draft_edge))
    return differences


def _report_to_dict(report: ScoreReport) -> dict[str, Any]:
    """Convert a ScoreReport to a JSON-serializable dictionary."""
    return {
        "summary": {
            "gold_total": report.gold_total,
            "draft_total": report.draft_total,
            "recovered_total": report.recovered_total,
            "evidence_exact_recovered_total": report.evidence_exact_recovered_total,
            "missed_total": report.missed_total,
            "extra_total": report.extra_total,
            "ordinary_missed_total": report.ordinary_missed_total,
            "ordinary_extra_total": report.ordinary_extra_total,
            "relationship_mismatches_total": report.relationship_mismatches_total,
            "evidence_mismatches_total": report.evidence_mismatches_total,
            "symmetric_correlation_differences_total": (
                report.symmetric_correlation_differences_total
            ),
            "dropped_gold_defects_total": report.dropped_gold_defects_total,
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
        "recovered_total": paper.recovered_total,
        "evidence_exact_recovered_total": (
            paper.recovered_total - len(paper.evidence_mismatches)
        ),
        "ordinary_missed": [
            _edge_to_dict(edge) for edge in ordinary_missed_edges(paper)
        ],
        "ordinary_extra": [
            _edge_to_dict(edge) for edge in ordinary_extra_edges(paper)
        ],
        "missed": [_edge_to_dict(edge) for edge in paper.missed],
        "extra": [_edge_to_dict(edge) for edge in paper.extra],
        "relationship_mismatches": [
            _mismatch_to_dict(mismatch) for mismatch in paper.relationship_mismatches
        ],
        "evidence_mismatches": [
            _mismatch_to_dict(mismatch) for mismatch in paper.evidence_mismatches
        ],
        "symmetric_correlation_differences": [
            _mismatch_to_dict(mismatch)
            for mismatch in paper.symmetric_correlation_differences
        ],
        "dropped_gold_defects": [
            _edge_to_dict(edge) for edge in paper.dropped_gold_defects
        ],
    }


def ordinary_missed_edges(paper: PaperScore) -> list[EdgeRecord]:
    """Return missed gold edges not explained by relation/symmetry pairs."""
    explained = {
        mismatch.gold.triple for mismatch in paper.relationship_mismatches
    } | {
        mismatch.gold.triple
        for mismatch in paper.symmetric_correlation_differences
    }
    return [edge for edge in paper.missed if edge.triple not in explained]


def ordinary_extra_edges(paper: PaperScore) -> list[EdgeRecord]:
    """Return extra draft edges not explained by relation/symmetry pairs."""
    explained = {
        mismatch.draft.triple for mismatch in paper.relationship_mismatches
    } | {
        mismatch.draft.triple
        for mismatch in paper.symmetric_correlation_differences
    }
    return [edge for edge in paper.extra if edge.triple not in explained]


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
            f"- Recovered: {paper.recovered_total}/{paper.gold_total}; "
            f"evidence-matched recovered: "
            f"{paper.recovered_total - len(paper.evidence_mismatches)}/"
            f"{paper.gold_total}; draft edges: {paper.draft_total}; "
            f"missed: {len(paper.missed)}; extra: {len(paper.extra)}; "
            f"dropped gold defects: {len(paper.dropped_gold_defects)}"
        ),
        f"- Ordinary missed: {len(ordinary_missed_edges(paper))}",
        f"- Ordinary extra: {len(ordinary_extra_edges(paper))}",
        f"- Relationship-only mismatches: {len(paper.relationship_mismatches)}",
        f"- Evidence-strength mismatches: {len(paper.evidence_mismatches)}",
        (
            "- Symmetric correlation direction differences: "
            f"{len(paper.symmetric_correlation_differences)}"
        ),
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
    return lines


def _format_edge(edge: EdgeRecord) -> str:
    """Format one edge for human-readable output."""
    return f"{edge.source} --[{edge.rel}/{edge.evidence_strength}]--> {edge.target}"

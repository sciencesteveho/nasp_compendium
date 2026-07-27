"""Tests for relationship-aware compendium scoring."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from nasp_compendium import score_compendium


def _write_edges(path: Path, edges_yaml: str) -> Path:
    """Write a minimal YAML-in-Markdown edges file and return its path."""
    path.write_text("edges:\n" + textwrap.dedent(edges_yaml))
    return path


_ONE_EDGE = """
      - chain_id: c
        step: 1
        source: {source}
        target: {target}
        rel: {rel}
        evidence_strength: {evidence}
        context: ctx
        support: sup
        papers: [p]
"""


def _edge(
    source: str,
    target: str,
    rel: str = "activates",
    evidence: str = "direct_measured",
) -> str:
    """Return one edge block for the test fixtures."""
    return _ONE_EDGE.format(
        source=source, target=target, rel=rel, evidence=evidence
    )


def test_self_match_is_perfect(tmp_path: Path) -> None:
    """A file scored against itself recovers every edge exactly."""
    gold = _write_edges(
        tmp_path / "p.gold.md",
        _edge("CGAS", "cGAMP", "produces") + _edge("STING1", "TBK1"),
    )
    score = score_compendium.score_pair(draft_file=gold, gold_file=gold)
    assert score.gold_total == 2
    assert score.endpoint_recovered == 2
    assert score.triple_recovered == 2
    assert score.exact_recovered == 2
    assert not score.missed
    assert not score.extra


def test_normalized_variant_matches_once(tmp_path: Path) -> None:
    """Case/plural/suffix variants of a correct edge do not double-count."""
    gold = _write_edges(
        tmp_path / "p.gold.md", _edge("CGAS", "type_I_IFN_signaling")
    )
    draft = _write_edges(tmp_path / "p.md", _edge("cgas", "type_I_IFNs"))
    score = score_compendium.score_pair(draft_file=draft, gold_file=gold)
    assert score.endpoint_recovered == 1
    assert score.triple_recovered == 1
    assert score.exact_recovered == 1
    assert not score.missed
    assert not score.extra


def test_relationship_mismatch_is_not_double_counted(tmp_path: Path) -> None:
    """Same-polarity verb alternatives are not mislabeled as sign errors."""
    gold = _write_edges(
        tmp_path / "p.gold.md",
        _edge("epigenetic_remodeling", "SASP", "induces"),
    )
    draft = _write_edges(
        tmp_path / "p.md", _edge("epigenetic_remodeling", "SASP", "drives")
    )
    score = score_compendium.score_pair(draft_file=draft, gold_file=gold)
    assert score.endpoint_recovered == 1
    assert score.triple_recovered == 0
    assert len(score.relationship_mismatches) == 1
    assert not score.polarity_mismatches
    assert not score.missed
    assert not score.extra


@pytest.mark.parametrize(
    ("gold_rel", "draft_rel"),
    [
        ("activates", "suppresses"),
        ("drives", "does_not_drive"),
        ("correlates", "negatively_correlates"),
        ("does_not_drive", "suppresses"),
    ],
)
def test_polarity_mismatch_is_not_primary_recovery(
    tmp_path: Path,
    gold_rel: str,
    draft_rel: str,
) -> None:
    """Opposite or absent effects remain endpoint-only diagnostics."""
    gold = _write_edges(tmp_path / "p.gold.md", _edge("A", "B", gold_rel))
    draft = _write_edges(tmp_path / "p.md", _edge("A", "B", draft_rel))

    score = score_compendium.score_pair(draft_file=draft, gold_file=gold)

    assert score.endpoint_recovered == 1
    assert score.triple_recovered == 0
    assert len(score.relationship_mismatches) == 1
    assert len(score.polarity_mismatches) == 1


def test_evidence_mismatch_reported_separately(tmp_path: Path) -> None:
    """A matched triple with different evidence is an evidence mismatch."""
    gold = _write_edges(
        tmp_path / "p.gold.md",
        _edge("CGAS", "STING1", "activates", "direct_measured"),
    )
    draft = _write_edges(
        tmp_path / "p.md",
        _edge("CGAS", "STING1", "activates", "strong_correlative"),
    )
    score = score_compendium.score_pair(draft_file=draft, gold_file=gold)
    assert score.triple_recovered == 1
    assert score.exact_recovered == 0
    assert len(score.evidence_mismatches) == 1


def test_symmetric_correlation_direction_matches(tmp_path: Path) -> None:
    """Same-sign correlation reversal is exact apart from orientation."""
    gold = _write_edges(
        tmp_path / "p.gold.md",
        _edge("ISG15", "MX1", "correlates", "strong_correlative"),
    )
    draft = _write_edges(
        tmp_path / "p.md",
        _edge("MX1", "ISG15", "correlates", "strong_correlative"),
    )
    score = score_compendium.score_pair(draft_file=draft, gold_file=gold)
    assert score.endpoint_recovered == 1
    assert score.triple_recovered == 1
    assert score.exact_recovered == 1
    assert len(score.symmetric_direction_differences) == 1
    assert not score.relationship_mismatches
    assert not score.missed
    assert not score.extra


def test_exact_reversed_correlation_outranks_direct_sign_flip(
    tmp_path: Path,
) -> None:
    """Pairing prefers a signed correlation over endpoint direction."""
    gold = _write_edges(
        tmp_path / "p.gold.md",
        _edge("A", "B", "correlates", "strong_correlative"),
    )
    draft = _write_edges(
        tmp_path / "p.md",
        _edge("A", "B", "negatively_correlates", "strong_correlative")
        + _edge("B", "A", "correlates", "strong_correlative"),
    )

    score = score_compendium.score_pair(draft_file=draft, gold_file=gold)

    assert score.triple_recovered == 1
    assert score.exact_recovered == 1
    assert not score.relationship_mismatches
    assert len(score.symmetric_direction_differences) == 1
    assert [(edge.source, edge.target, edge.rel) for edge in score.extra] == [
        ("A", "B", "negatively_correlates")
    ]


def test_directed_edge_reversal_is_not_a_match(tmp_path: Path) -> None:
    """Reversed endpoints do not match for directed relationships."""
    gold = _write_edges(
        tmp_path / "p.gold.md", _edge("CGAS", "STING1", "activates")
    )
    draft = _write_edges(
        tmp_path / "p.md", _edge("STING1", "CGAS", "activates")
    )
    score = score_compendium.score_pair(draft_file=draft, gold_file=gold)
    assert score.endpoint_recovered == 0
    assert len(score.missed) == 1
    assert len(score.extra) == 1


def test_structured_gold_defect_dropped_by_default(tmp_path: Path) -> None:
    """score_exclude gold edges are dropped by default, kept when disabled."""
    gold_text = (
        "edges:\n"
        + textwrap.dedent(_edge("CGAS", "cGAMP", "produces"))
        + textwrap.dedent(
            """
      - chain_id: d
        step: 1
        source: type_I_IFN
        target: mortality
        rel: does_not_drive
        evidence_strength: strong_correlative
        score_exclude: true
        context: flagged placeholder
        support: sup
        papers: [p]
    """
        )
    )
    gold = tmp_path / "p.gold.md"
    gold.write_text(gold_text)

    dropped = score_compendium.score_pair(draft_file=gold, gold_file=gold)
    assert dropped.gold_total == 1
    assert len(dropped.excluded_gold_defects) == 1

    kept = score_compendium.score_pair(
        draft_file=gold, gold_file=gold, drop_gold_defects=False
    )
    assert kept.gold_total == 2
    assert not kept.excluded_gold_defects


def test_status_excluded_marker_also_drops(tmp_path: Path) -> None:
    """A `status: excluded` edge is treated as a gold defect."""
    gold_text = "edges:\n" + textwrap.dedent(
        """
      - chain_id: d
        step: 1
        source: A
        target: B
        rel: activates
        evidence_strength: direct_measured
        status: excluded
        context: ctx
        support: sup
        papers: [p]
    """
    )
    gold = tmp_path / "p.gold.md"
    gold.write_text(gold_text)
    score = score_compendium.score_pair(draft_file=gold, gold_file=gold)
    assert score.gold_total == 0
    assert len(score.excluded_gold_defects) == 1


def _tagged_edge(
    source: str,
    target: str,
    rel: str = "activates",
    evidence: str = "direct_measured",
    **extra: str,
) -> str:
    """Return one edge block with optional gold-scoring metadata."""
    block = _edge(source, target, rel, evidence).rstrip("\n")
    for key, value in extra.items():
        block += f"\n        {key}: {value}"
    return block + "\n"


def test_missing_supporting_edge_does_not_lower_core_recall(
    tmp_path: Path,
) -> None:
    """A missing supporting edge leaves core recall at 100 percent."""
    gold = _write_edges(
        tmp_path / "p.gold.md",
        _tagged_edge("CGAS", "STING1", tier="core")
        + _tagged_edge("MFN1", "STING1", tier="supporting"),
    )
    draft = _write_edges(tmp_path / "p.md", _edge("CGAS", "STING1"))

    score = score_compendium.score_pair(draft_file=draft, gold_file=gold)

    assert score.core_units == 1
    assert score.core_recovered == 1
    assert score.supporting_units == 1
    assert score.supporting_recovered == 0


def test_missing_core_edge_lowers_core_recall(tmp_path: Path) -> None:
    """A missing core edge lowers core recall."""
    gold = _write_edges(
        tmp_path / "p.gold.md",
        _tagged_edge("CGAS", "STING1", tier="core")
        + _tagged_edge("STING1", "TBK1", tier="core"),
    )
    draft = _write_edges(tmp_path / "p.md", _edge("CGAS", "STING1"))

    score = score_compendium.score_pair(draft_file=draft, gold_file=gold)

    assert score.core_units == 2
    assert score.core_recovered == 1


def test_equivalent_representation_counts_once(tmp_path: Path) -> None:
    """Equivalent gold edges form one recoverable unit."""
    gold = _write_edges(
        tmp_path / "p.gold.md",
        _tagged_edge(
            "cytoplasmic_mt_dsRNA",
            "DDX58",
            equiv_group="dsrna_sensor",
        )
        + _tagged_edge(
            "cytoplasmic_mt_dsRNA",
            "IFIH1",
            equiv_group="dsrna_sensor",
        ),
    )
    draft = _write_edges(
        tmp_path / "p.md",
        _edge("cytoplasmic_mt_dsRNA", "DDX58"),
    )

    score = score_compendium.score_pair(draft_file=draft, gold_file=gold)

    assert score.core_units == 1
    assert score.core_recovered == 1
    assert not score.missed
    assert not score.extra


def test_forbidden_shortcut_is_violation_not_extra(tmp_path: Path) -> None:
    """A forbidden anti-edge match is a shortcut violation, not an extra."""
    gold = _write_edges(
        tmp_path / "p.gold.md",
        _tagged_edge("CGAS", "STING1", tier="core")
        + _tagged_edge(
            "CGAS",
            "SASP",
            rel="drives",
            status="forbidden_shortcut",
        ),
    )
    draft = _write_edges(
        tmp_path / "p.md",
        _edge("CGAS", "STING1") + _edge("CGAS", "SASP", "drives"),
    )

    score = score_compendium.score_pair(draft_file=draft, gold_file=gold)

    assert score.core_units == 1
    assert score.core_recovered == 1
    assert len(score.shortcut_violations) == 1
    assert not score.extra


def test_forbidden_edge_self_match_is_clean(tmp_path: Path) -> None:
    """A gold file does not assert its own forbidden anti-edges as a draft."""
    gold = _write_edges(
        tmp_path / "p.gold.md",
        _tagged_edge("CGAS", "STING1", tier="core")
        + _tagged_edge(
            "CGAS",
            "SASP",
            rel="drives",
            status="forbidden_shortcut",
        ),
    )

    score = score_compendium.score_pair(draft_file=gold, gold_file=gold)

    assert score.core_units == 1
    assert score.core_recovered == 1
    assert not score.shortcut_violations
    assert not score.extra


def test_legacy_gold_preserves_endpoint_recall_units(tmp_path: Path) -> None:
    """Untagged gold edges retain one core unit per endpoint pair."""
    gold = _write_edges(
        tmp_path / "p.gold.md",
        _edge("CGAS", "cGAMP", "produces")
        + _edge("STING1", "TBK1")
        + _edge("TBK1", "IRF3"),
    )
    draft = _write_edges(
        tmp_path / "p.md",
        _edge("CGAS", "cGAMP", "produces") + _edge("STING1", "TBK1"),
    )

    report = score_compendium.score_paths(draft_path=draft, gold_path=gold)

    assert report.core_units_total == report.gold_total
    assert report.core_recovered_total == report.endpoint_recovered_total
    assert report.core_recall == report.endpoint_recall
    assert report.supporting_units_total == 0
    assert report.shortcut_violations_total == 0


def test_directory_scoring_pairs_by_paper_id(tmp_path: Path) -> None:
    """Directory scoring pairs draft and gold files by paper id."""
    draft_dir = tmp_path / "draft"
    gold_dir = tmp_path / "gold"
    draft_dir.mkdir()
    gold_dir.mkdir()
    _write_edges(draft_dir / "paper_a.md", _edge("CGAS", "cGAMP", "produces"))
    _write_edges(
        gold_dir / "paper_a.gold.md", _edge("CGAS", "cGAMP", "produces")
    )
    report = score_compendium.score_paths(
        draft_path=draft_dir, gold_path=gold_dir
    )
    assert len(report.papers) == 1
    assert report.papers[0].paper_id == "paper_a"
    assert report.endpoint_recovered_total == 1


def test_report_formats_render(tmp_path: Path) -> None:
    """Both text and JSON formats render without error."""
    gold = _write_edges(
        tmp_path / "p.gold.md", _edge("CGAS", "cGAMP", "produces")
    )
    report = score_compendium.score_paths(draft_path=gold, gold_path=gold)
    text = score_compendium.format_score_report(report, output_format="text")
    assert "Relationship recall" in text
    assert "endpoint overlap (diagnostic only)" in text
    payload = score_compendium.format_score_report(report, output_format="json")
    assert '"relationship_recall"' in payload
    assert '"polarity_mismatches_total"' in payload

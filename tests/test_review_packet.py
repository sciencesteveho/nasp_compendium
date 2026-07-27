"""Tests for exact-draft validation and advisory review findings."""

from __future__ import annotations

import textwrap
from pathlib import Path

from nasp_compendium import review_packet


def _write_draft(path: Path, edges: str) -> Path:
    """Write a minimal valid curation draft."""
    path.write_text(
        textwrap.dedent(
            """
            paper:
              Test_paper_2026:
                cite: Test et al. (2026)
                url: https://example.org/test
                summary: Test record.
                nucleic_acid_sensors: [DDX58, IFIH1]
                genes: []
                pathways: [cytosolic_RNA_sensing]
                cell_types: []
                mechanisms: [cytoplasmic_mt_dsRNA]
                model_systems: [human_in_vitro]
                evidence_type: [siRNA_knockdown]
                notes: Test fixture.
                relevance_to_project: Test fixture.
            edges:
            """
        )
        + textwrap.dedent(edges)
    )
    return path


def _edge(source: str, target: str) -> str:
    """Return one valid edge fixture."""
    return f"""
      - chain_id: sensing
        step: 1
        source: {source}
        target: {target}
        rel: activates
        evidence_strength: perturbation_supported
        context: Combined sensor perturbation.
        support: Fig. 1a
        papers: [Test_paper_2026]
    """


def test_gate_validates_the_exact_draft(tmp_path: Path) -> None:
    """An invalid draft blocks even when no compendium directory is involved."""
    draft = tmp_path / "invalid.draft.md"
    draft.write_text("edges: []\n")

    blockers = review_packet.gate_blockers(draft)

    assert any("Missing 'paper'" in blocker for blocker in blockers)


def test_context_sensitive_topology_is_advisory(tmp_path: Path) -> None:
    """A grouped combined-sensor result is reviewed without blocking freeze."""
    draft = _write_draft(
        tmp_path / "combined.draft.md",
        _edge("cytoplasmic_mt_dsRNA", "cytosolic_RNA_sensing")
        + _edge("cytosolic_RNA_sensing", "DDX58")
        + _edge("cytosolic_RNA_sensing", "IFIH1"),
    )
    (tmp_path / "invalid_sibling.draft.md").write_text("edges: []\n")

    # Exact-file review must not inherit errors or declarations from siblings.
    assert review_packet.gate_blockers(draft) == []
    packet = review_packet.build_review_packet(draft)
    assert "Status: `READY_FOR_FREEZE`" in packet
    assert "Advisory topology review" in packet
    assert "routed through generic process" in packet


def test_node_literal_verb_rules_are_not_topology_findings() -> None:
    """Debatable node-pair verb choices are not encoded as universal rules."""
    data = {
        "edges": [
            {
                "source": "epigenetic_remodeling",
                "target": "retrotransposon_derepression",
                "rel": "induces",
                "evidence_strength": "perturbation_supported",
            },
            {
                "source": "chromatin_accessibility",
                "target": "SPI1",
                "rel": "activates",
                "evidence_strength": "strong_correlative",
            },
        ]
    }

    assert review_packet._topology_lints(data) == []

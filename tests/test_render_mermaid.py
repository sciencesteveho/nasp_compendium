"""Tests for Mermaid compendium rendering."""

from __future__ import annotations

from pathlib import Path

from nasp_compendium import render_mermaid
from nasp_compendium import write_mermaid_graphs
from nasp_compendium.summarize_compendium import Compendium


def test_render_mermaid_preserves_visual_encodings() -> None:
    """Mermaid source retains node, relation, and evidence styling."""
    compendium = Compendium(
        papers={
            "test_2026": {
                "genes": ["CGAS", "RELA"],
                "pathways": ["type_I_IFN"],
                "mechanisms": ["cellular_senescence"],
            }
        },
        edges=[
            {
                "source": "CGAS",
                "target": "type_I_IFN",
                "rel": "activates",
                "evidence_strength": "direct_measured",
                "papers": ["test_2026"],
            },
            {
                "source": "RELA",
                "target": "type_I_IFN",
                "rel": "suppresses",
                "evidence_strength": "canonical_inferred",
                "papers": ["test_2026"],
            },
            {
                "source": "CGAS",
                "target": "cellular_senescence",
                "rel": "correlates",
                "evidence_strength": "strong_correlative",
                "papers": ["test_2026"],
            },
            {
                "source": "RELA",
                "target": "cellular_senescence",
                "rel": "does_not_drive",
                "evidence_strength": "perturbation_supported",
                "papers": ["test_2026"],
            },
        ],
    )

    mermaid = render_mermaid(compendium)

    assert "flowchart LR" in mermaid
    assert "fontFamily: Arial" in mermaid
    assert "fontSize: 5pt" in mermaid
    assert "font-size:5pt!important" in mermaid
    assert "-- activates -->" in mermaid
    assert "-- suppresses --x" in mermaid
    assert "-- correlates --o" in mermaid
    assert "-- does not drive ---" in mermaid
    assert "stroke:#55A868" in mermaid
    assert "stroke:#C44E52" in mermaid
    assert "stroke-dasharray:5 3" in mermaid
    assert "stroke-dasharray:2 3" in mermaid
    assert "classDef genes fill:#DCE6F2,stroke:#4C72B0" in mermaid


def test_write_mermaid_graphs_includes_combined_and_gold_sources(
    tmp_path: Path,
) -> None:
    """Writer emits one combined graph and one graph per Markdown source."""
    compendium_path = tmp_path / "compendium"
    compendium_path.mkdir()
    (compendium_path / "regular.md").write_text(
        """paper:
  regular_2025:
    genes: [CGAS, STING1]
edges:
  - source: CGAS
    target: STING1
    rel: activates
    evidence_strength: direct_measured
    papers: [regular_2025]
"""
    )
    (compendium_path / "held_out.gold.md").write_text(
        """paper:
  held_out_2026:
    genes: [RELA, IL6]
edges:
  - source: RELA
    target: IL6
    rel: activates
    evidence_strength: direct_measured
    papers: [held_out_2026]
"""
    )
    output_dir = tmp_path / "graphs"

    generated = write_mermaid_graphs(compendium_path, output_dir)

    assert [path.name for path in generated] == [
        "all_literature_graph.mermaid",
        "held_out.gold.mermaid",
        "regular.mermaid",
    ]
    combined = generated[0].read_text()
    assert "CGAS" in combined
    assert "RELA" in combined

"""Tests for compendium graph rendering."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from nasp_compendium import summarize_compendium


def test_render_uses_five_point_arial_text_in_every_layout(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Every graph layout renders graph, node, and edge text as 5 pt Arial."""
    rendered_diagrams: list[Any] = []

    def capture_render(
        diagram: Any,
        outfile: str,
        cleanup: bool,
    ) -> str:
        """Capture a diagram without invoking the Graphviz executable."""
        assert cleanup
        rendered_diagrams.append(diagram)
        Path(outfile).write_text("<svg/>\n")
        return outfile

    monkeypatch.setattr(
        summarize_compendium.graphviz.Digraph,
        "render",
        capture_render,
    )
    compendium = summarize_compendium.Compendium(
        papers={"test_2026": {"genes": ["CGAS", "STING1"]}},
        edges=[
            {
                "source": "CGAS",
                "target": "STING1",
                "rel": "activates",
                "evidence_strength": "perturbation_supported",
                "papers": ["test_2026"],
            }
        ],
    )

    for options in ({}, {"compact": True}, {"annotate_papers": True}):
        summarize_compendium.render(
            compendium,
            output_stem=tmp_path / "graph",
            output_format="svg",
            **options,
        )

    for diagram in rendered_diagrams:
        assert diagram.graph_attr["fontsize"] == "5"
        assert diagram.node_attr["fontsize"] == "5"
        assert diagram.edge_attr["fontsize"] == "5"
        assert diagram.graph_attr["fontname"] == "Arial"
        assert diagram.node_attr["fontname"] == "Arial"
        assert diagram.edge_attr["fontname"] == "Arial"
        assert "fontnames" not in diagram.graph_attr
        assert diagram.renderer == "cairo"


def test_render_increases_layout_spacing_by_seven_and_a_half_percent(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Each graph layout receives 7.5 percent more spacing."""
    rendered_diagrams: list[Any] = []

    def capture_render(
        diagram: Any,
        outfile: str,
        cleanup: bool,
    ) -> str:
        """Capture a diagram without invoking the Graphviz executable."""
        assert cleanup
        rendered_diagrams.append(diagram)
        Path(outfile).write_text("<svg/>\n")
        return outfile

    monkeypatch.setattr(
        summarize_compendium.graphviz.Digraph,
        "render",
        capture_render,
    )
    compendium = summarize_compendium.Compendium(
        papers={"test_2026": {"genes": ["CGAS", "STING1"]}},
        edges=[
            {
                "source": "CGAS",
                "target": "STING1",
                "rel": "activates",
                "evidence_strength": "perturbation_supported",
                "papers": ["test_2026"],
            }
        ],
    )
    layouts = (
        (
            {},
            {
                "sep": "+0.129",
                "esep": "+0.086",
                "nodesep": "0.1075",
                "ranksep": "0.1935 equally",
            },
            "0.01935,0.01075",
        ),
        (
            {"compact": True},
            {
                "sep": "+0.02365",
                "esep": "+0.01075",
                "nodesep": "0.048375",
                "ranksep": "0.1075",
            },
            "0.01935,0.01075",
        ),
        (
            {"annotate_papers": True},
            {
                "sep": "+0.0301",
                "esep": "+0.01505",
                "nodesep": "0.05375",
                "ranksep": "0.112875",
            },
            "0.018275,0.01075",
        ),
    )

    for options, _, _ in layouts:
        summarize_compendium.render(
            compendium,
            output_stem=tmp_path / "graph",
            output_format="svg",
            **options,
        )

    for diagram, (_, graph_spacing, node_margin) in zip(
        rendered_diagrams,
        layouts,
        strict=True,
    ):
        assert {
            key: diagram.graph_attr[key] for key in graph_spacing
        } == graph_spacing
        assert diagram.node_attr["margin"] == node_margin


def test_pdf_render_preserves_an_existing_svg_with_the_same_stem(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """PDF conversion does not clobber an existing SVG output."""
    existing_svg = tmp_path / "graph.svg"
    existing_svg.write_text("existing SVG\n")
    intermediate_paths: list[Path] = []

    def capture_render(
        diagram: Any,
        outfile: str,
        cleanup: bool,
    ) -> str:
        """Write a minimal outlined SVG at the requested temporary path."""
        assert cleanup
        assert diagram.renderer == "cairo"
        Path(outfile).write_text("<svg><path/></svg>\n")
        return outfile

    def capture_conversion(
        svg_path: Path,
        output_path: Path,
        *,
        output_format: str,
    ) -> None:
        """Capture the conversion boundary and write the requested PDF."""
        assert output_format == "pdf"
        intermediate_paths.append(svg_path)
        output_path.write_bytes(b"%PDF-test\n")

    monkeypatch.setattr(
        summarize_compendium.graphviz.Digraph,
        "render",
        capture_render,
    )
    monkeypatch.setattr(summarize_compendium, "can_convert_svg", lambda: True)
    monkeypatch.setattr(
        summarize_compendium,
        "convert_svg",
        capture_conversion,
    )
    compendium = summarize_compendium.Compendium(
        papers={"test_2026": {"genes": ["CGAS", "STING1"]}},
        edges=[
            {
                "source": "CGAS",
                "target": "STING1",
                "rel": "activates",
                "evidence_strength": "direct_measured",
            }
        ],
    )

    summarize_compendium.render(
        compendium,
        output_stem=tmp_path / "graph",
        output_format="pdf",
    )

    assert existing_svg.read_text() == "existing SVG\n"
    assert (tmp_path / "graph.pdf").read_bytes() == b"%PDF-test\n"
    assert len(intermediate_paths) == 1
    assert not intermediate_paths[0].exists()


def test_default_directory_loading_still_excludes_gold_files(
    tmp_path: Path,
) -> None:
    """Non-rendering directory loads keep held-out gold files excluded."""
    (tmp_path / "regular.md").write_text(
        "paper:\n  regular_2025:\n    genes: []\nedges: []\n"
    )
    (tmp_path / "held_out.gold.md").write_text(
        "paper:\n  held_out_2026:\n    genes: []\nedges: []\n"
    )

    compendium = summarize_compendium.Compendium.from_dir(tmp_path)

    assert set(compendium.papers) == {"regular_2025"}

"""Tests for graph-rendering CLI commands."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from nasp_compendium import cli
from nasp_compendium import summarize_compendium


def test_render_graph_combines_regular_and_gold_files(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Combined rendering includes every compendium Markdown file."""
    compendium_dir = tmp_path / "compendium"
    compendium_dir.mkdir()

    def write_compendium(path: Path, paper_id: str) -> None:
        """Write a minimal graph-renderable compendium file."""
        path.write_text(
            f"""paper:
  {paper_id}:
    genes: [CGAS, STING1]
edges:
  - source: CGAS
    target: STING1
    rel: activates
    evidence_strength: perturbation_supported
    papers: [{paper_id}]
"""
        )

    write_compendium(compendium_dir / "regular.md", "regular_2025")
    write_compendium(compendium_dir / "held_out.gold.md", "held_out_2026")
    rendered: list[tuple[set[str], Path, str]] = []

    def capture_render(
        compendium: summarize_compendium.Compendium,
        output_stem: Path,
        output_format: str,
        **_: Any,
    ) -> None:
        """Capture the combined render request."""
        rendered.append((set(compendium.papers), output_stem, output_format))

    monkeypatch.setattr(summarize_compendium, "render", capture_render)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "compendium",
            "render_graph",
            "--compendium-path",
            str(compendium_dir),
            "--out",
            str(tmp_path / "combined.pdf"),
        ],
    )

    cli.main()

    assert rendered == [
        (
            {"held_out_2026", "regular_2025"},
            tmp_path / "combined",
            "pdf",
        )
    ]


def test_render_paper_graphs_writes_one_output_per_markdown_file(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Batch rendering creates one predictably named graph per source file."""
    compendium_dir = tmp_path / "compendium"
    compendium_dir.mkdir()

    def write_compendium(path: Path, paper_id: str) -> None:
        """Write a minimal graph-renderable compendium file."""
        path.write_text(
            f"""paper:
  {paper_id}:
    genes: [CGAS, STING1]
edges:
  - source: CGAS
    target: STING1
    rel: activates
    evidence_strength: perturbation_supported
    papers: [{paper_id}]
"""
        )

    write_compendium(compendium_dir / "alpha.gold.md", "alpha_2025")
    write_compendium(compendium_dir / "beta.md", "beta_2026")
    output_dir = tmp_path / "graphs"
    rendered: list[tuple[set[str], Path, str]] = []

    def capture_render(
        compendium: summarize_compendium.Compendium,
        output_stem: Path,
        output_format: str,
        **_: Any,
    ) -> None:
        """Capture each per-paper render request."""
        rendered.append((set(compendium.papers), output_stem, output_format))

    monkeypatch.setattr(summarize_compendium, "render", capture_render)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "compendium",
            "render_paper_graphs",
            "--compendium-path",
            str(compendium_dir),
            "--output-dir",
            str(output_dir),
            "--format",
            "pdf",
        ],
    )

    cli.main()

    assert output_dir.is_dir()
    assert rendered == [
        ({"alpha_2025"}, output_dir / "alpha.gold", "pdf"),
        ({"beta_2026"}, output_dir / "beta", "pdf"),
    ]


def test_render_mermaid_graphs_writes_repository_sources(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Mermaid CLI writes combined and per-paper source files."""
    compendium_dir = tmp_path / "compendium"
    compendium_dir.mkdir()
    (compendium_dir / "paper.md").write_text(
        """paper:
  paper_2026:
    genes: [CGAS, STING1]
edges:
  - source: CGAS
    target: STING1
    rel: activates
    evidence_strength: direct_measured
    papers: [paper_2026]
"""
    )
    output_dir = tmp_path / "mermaid"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "compendium",
            "render_mermaid_graphs",
            "--compendium-path",
            str(compendium_dir),
            "--output-dir",
            str(output_dir),
        ],
    )

    cli.main()

    assert sorted(path.name for path in output_dir.iterdir()) == [
        "all_literature_graph.mermaid",
        "paper.mermaid",
    ]

"""Regenerate marker-gene docs and module visualizations together."""

from __future__ import annotations

import argparse
from pathlib import Path

from nasp_compendium import render_docs as render_docs_module
from nasp_compendium.visualization import gene_modules


DEFAULT_DOCS_DIR: Path = (
    Path(__file__).resolve().parent.parent / "docs" / "marker_genes"
)


def regenerate(
    input_path: Path,
    docs_dir: Path,
    assets_subdir: str = "assets",
    cmap_sankey: str = "Set1",
    cmap_barplot: str = "tab20c",
) -> None:
    """Render docs and figures from one marker-gene TSV in a single pass.

    Writes one Sankey per module and a whole-taxonomy barplot into
    `docs_dir/assets_subdir`, then renders the Markdown with each module's
    Sankey embedded on its page and the barplot on the index page.

    Args:
      input_path: Path to the marker-gene TSV source file.
      docs_dir: Directory to write Markdown docs into (e.g. docs/marker_genes).
      assets_subdir: Subdirectory of docs_dir for generated figures.
      cmap_sankey: Colormap palette for the per-module Sankey diagrams.
      cmap_barplot: Colormap palette for the taxonomy barplot.
    """
    gene_modules.apply_publication_style()

    assets_dir = docs_dir / assets_subdir
    assets_dir.mkdir(parents=True, exist_ok=True)

    module_figures: dict[str, Path] = {}
    for module_id in gene_modules.list_module_ids(input_path):
        figure_path = (
            assets_dir
            / f"sankey_{render_docs_module.module_stem(module_id)}.png"
        )
        gene_modules.module_taxonomy_sankey(
            input_path,
            module_id=module_id,
            outpath=figure_path,
            cmap=cmap_sankey,
        )
        module_figures[module_id] = figure_path

    index_figure = assets_dir / "taxonomy_class_barplot.png"
    gene_modules.taxonomy_class_barplot(
        input_path,
        outpath=index_figure,
        cmap=cmap_barplot,
    )

    render_docs_module.render_docs(
        input_path=input_path,
        output_dir=docs_dir,
        module_figures=module_figures,
        index_figure=index_figure,
    )


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Regenerate marker-gene docs and module figures."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument(
        "--docs-dir", required=True, type=Path, default=DEFAULT_DOCS_DIR
    )
    return parser.parse_args()


def main() -> None:
    """Run the regeneration pass."""
    args = _parse_args()
    regenerate(input_path=args.input, docs_dir=args.docs_dir)


if __name__ == "__main__":
    main()

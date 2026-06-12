"""Render the NASP marker-genes as readable Markdown files."""

import argparse
import os
from collections.abc import Iterable
from pathlib import Path

import pandas as pd


def _read_marker_table(input_path: Path) -> pd.DataFrame:
    """Read and minimally validate the marker-gene source table."""
    marker_table = pd.read_csv(input_path, sep="\t", dtype=str).fillna("")
    required_columns = {
        "gene_symbol",
        "module_id",
        "module_class",
        "sensor_family",
        "activation_tier",
        "scoring_direction",
        "cell_type_breadth",
        "detectability",
        "also_in_module",
        "doi",
        "aliases",
        "sensor",
        "panel_source",
    }
    if missing_columns := required_columns.difference(marker_table.columns):
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")
    return marker_table


def module_stem(module_id: str) -> str:
    """Return the Markdown filename stem for a module id."""
    return _stemmify(module_id)


def _relative_figure(
    figure_path: Path | None,
    doc_dir: Path,
) -> str | None:
    """Return a POSIX path to a figure relative to the docs directory.

    Args:
      figure_path: Absolute or repo-relative path to the figure, or None.
      doc_dir: Directory the Markdown file is written into.

    Returns:
      A POSIX relative path suitable for a Markdown image link, or None when no
      figure was supplied.
    """
    if figure_path is None:
        return None
    return Path(os.path.relpath(figure_path, doc_dir)).as_posix()


def render_module(
    module_id: str,
    module_table: pd.DataFrame,
    figure_relpath: str | None = None,
) -> str:
    """Render one module's genes as a single Markdown table.

    Args:
      module_id: The module_id, used as the page heading.
      module_table: Rows belonging to this module.
      figure_relpath: Optional path to the module's Sankey figure, relative to
        the Markdown file, embedded beneath the heading.

    Returns:
      Markdown document text for the module.
    """
    lines = [f"# {module_id}", ""]
    if figure_relpath is not None:
        lines += [f"![{module_id} taxonomy]({figure_relpath})", ""]
    lines += [
        "| Gene | Module Class | Sensor Family | Activation Tier | Scoring Direction | Cell Type Breadth | Detectability | Also in Module(s) | DOI | Aliases | Is_Sensor | Panel Source |",  # noqa: E501
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",  # noqa: E501
    ]
    display_columns = [
        "gene_symbol",
        "module_class",
        "sensor_family",
        "activation_tier",
        "scoring_direction",
        "cell_type_breadth",
        "detectability",
        "also_in_module",
        "doi",
        "aliases",
        "sensor",
        "panel_source",
    ]
    ordered = module_table.sort_values(["module_class", "gene_symbol"])
    for _, row in ordered.iterrows():
        values = [_escape_chars(str(row[column])) for column in display_columns]
        lines.append(f"| {' | '.join(values)} |")
    lines.append("")
    return "\n".join(lines)


def render_index(
    module_ids: Iterable[str],
    figure_relpath: str | None = None,
    title: str = "Marker gene taxonomy",
) -> str:
    """Render the marker-gene landing page.

    Args:
      module_ids: Module ids to list, in display order.
      figure_relpath: Optional path to the whole-taxonomy barplot, relative to
        the index file, embedded beneath the heading.
      title: Page heading.

    Returns:
      Markdown document text linking to each module page.
    """
    lines = [f"# {title}", ""]
    if figure_relpath is not None:
        lines += [f"![Module taxonomy]({figure_relpath})", ""]
    lines += ["## Modules", ""]
    lines.extend(
        f"- [{module_id}]({module_stem(module_id)}.md)"
        for module_id in module_ids
    )
    lines.append("")
    return "\n".join(lines)


def _escape_chars(value: str) -> str:
    """Escape characters that break Markdown tables."""
    return value.replace("|", "\\|").replace("\n", " ").strip()


def _stemmify(value: str) -> str:
    """Convert a module identifier into a stable Markdown filename stem."""
    return value.lower().replace("/", "_").replace(" ", "_")


def render_docs(
    input_path: Path,
    output_dir: Path,
    module_figures: dict[str, Path] | None = None,
    index_figure: Path | None = None,
    index_name: str = "index.md",
) -> None:
    """Render all marker-gene Markdown docs from a TSV file.

    Args:
      input_path: Path to the marker-gene TSV source file.
      output_dir: Directory to write the Markdown files into.
      module_figures: Optional mapping from module_id to a Sankey figure path;
        each is embedded on its module page as a link relative to output_dir.
      index_figure: Optional whole-taxonomy figure embedded on the index page.
      index_name: Filename for the generated landing page.
    """
    marker_table = _read_marker_table(input_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    module_figures = module_figures or {}

    rendered_module_ids: list[str] = []
    for module_id, module_table in marker_table.groupby("module_id", sort=True):
        module_key = str(module_id)
        figure_relpath = _relative_figure(
            module_figures.get(module_key), output_dir
        )
        (output_dir / f"{_stemmify(module_key)}.md").write_text(
            render_module(module_key, module_table, figure_relpath),
            encoding="utf-8",
        )
        rendered_module_ids.append(module_key)

    index_relpath = _relative_figure(index_figure, output_dir)
    (output_dir / index_name).write_text(
        render_index(rendered_module_ids, index_relpath),
        encoding="utf-8",
    )


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Render marker-gene TSV records into Markdown docs."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    """Run the Markdown renderer."""
    args = _parse_args()
    render_docs(input_path=args.input, output_dir=args.output_dir)


if __name__ == "__main__":
    main()

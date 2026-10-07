"""Write per-gene annotation columns into the marker-gene panel TSV.

Annotation scripts add derived columns to the curated panel in place. These
helpers copy every curated field verbatim, keep the file's line endings, and
refresh annotation columns already present where they stand, so reruns are
idempotent.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


__all__ = [
    "read_marker_panel",
    "set_gene_annotation",
    "write_marker_panel",
]


def read_marker_panel(path: Path) -> tuple[pd.DataFrame, str]:
    """Read the panel with every field as text.

    Returns:
      The panel and its line terminator (CRLF or LF).
    """
    with path.open(encoding="utf-8", newline="") as handle:
        line_terminator = "\r\n" if handle.readline().endswith("\r\n") else "\n"
    panel = pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False)
    return panel, line_terminator


def set_gene_annotation(
    panel: pd.DataFrame,
    annotation: pd.DataFrame,
    *,
    after: str | None = None,
) -> None:
    """Set per-gene annotation columns on every panel row, in place.

    A column already in the panel is refreshed where it stands. A missing
    column is inserted after the preceding column of `annotation`; the first
    goes after `after`, or at the end when `after` is None. Every row of a gene
    listed in several modules receives the same values.

    Args:
      panel: Output of `read_marker_panel`; modified in place.
      annotation: One row per gene_symbol. Its other columns are written in
        order.
      after: Panel column that new annotation columns follow.

    Raises:
      pandas.errors.MergeError: If `annotation` repeats a gene_symbol.
    """
    row_values = panel[["gene_symbol"]].merge(
        annotation, on="gene_symbol", how="left", validate="many_to_one"
    )

    preceding_column = after
    for column in annotation.columns.drop("gene_symbol"):
        if column not in panel.columns:
            position = (
                len(panel.columns)
                if preceding_column is None
                else list(panel.columns).index(preceding_column) + 1
            )
            panel.insert(position, column, "")
        panel[column] = row_values[column]
        preceding_column = column


def write_marker_panel(
    panel: pd.DataFrame,
    path: Path,
    *,
    line_terminator: str,
    float_format: str = "%.6g",
) -> None:
    """Write the panel as a TSV with `line_terminator` line endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(
        path,
        sep="\t",
        index=False,
        float_format=float_format,
        lineterminator=line_terminator,
    )

"""Visualization utilities for gene modules and their taxonomy."""

import colorsys
from collections.abc import Iterable, Sequence
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.patches import PathPatch
from matplotlib.patches import Rectangle
from matplotlib.path import Path as MplPath
from matplotlib.transforms import blended_transform_factory

from nasp_compendium.display import humanize_module_name


PANEL_COLUMNS = (
    "gene_symbol",
    "module_id",
    "module_class",
    "scoring_direction",
)


DIRECTION_MARKERS: dict[str, tuple[str, str]] = {
    "positive": ("^", "#2a7f62"),
    "inverse": ("v", "#b5452f"),
    "context_dependent": ("D", "#7f7f7f"),
}

MODULE_NODE_COLOR = (0.75, 0.75, 0.75)


def _set_matplotlib_publication_parameters() -> None:
    """Set matplotlib parameters for publication-quality figures."""
    plt.rcParams.update(
        {
            "font.size": 5,
            "axes.titlesize": 5,
            "axes.labelsize": 5,
            "xtick.labelsize": 5,
            "ytick.labelsize": 5,
            "legend.fontsize": 5,
            "figure.titlesize": 5,
            "figure.dpi": 450,
            "font.sans-serif": ["Arial", "Nimbus Sans"],
            "axes.linewidth": 0.25,
            "xtick.major.width": 0.25,
            "ytick.major.width": 0.25,
            "xtick.minor.width": 0.25,
            "ytick.minor.width": 0.25,
        }
    )


def apply_publication_style() -> None:
    """Apply the publication matplotlib rcParams used by these figures.

    Public entry point for callers that render figures outside the functions in
    this module and need the same styling.
    """
    _set_matplotlib_publication_parameters()


def list_module_ids(
    panel_path: str | Path,
    encoding: str = "utf-8",
) -> list[str]:
    """Return the sorted module_ids present in the panel TSV.

    Uses the same normalization as figure rendering, so the returned ids are
    exactly those a Sankey can be drawn for.

    Args:
      panel_path: Path to the panel TSV.
      encoding: Text encoding for the panel file.

    Returns:
      Sorted unique module_ids.
    """
    panel = _load_panel(panel_path, encoding=encoding)
    return sorted(panel["module_id"].unique().tolist())


def _font_size_points(size: object) -> float:
    """Return a matplotlib font size in points."""
    return float(FontProperties(size=size).get_size_in_points())  # type: ignore


def _darken_color(
    color: tuple[float, float, float],
    factor: float = 0.6,
) -> tuple[float, float, float]:
    """Return an darkened variant of an RGB color.

    Args:
      color: Source (r, g, b) in [0, 1].
      factor: Multiplier applied to lightness; lower is darker.

    Returns:
      (r, g, b) with reduced lightness.
    """
    hue, lightness, saturation = colorsys.rgb_to_hls(*color[:3])
    return colorsys.hls_to_rgb(hue, max(0.0, lightness * factor), saturation)


def _load_panel(
    panel_path: str | Path,
    encoding: str = "utf-8",
) -> pd.DataFrame:
    """Load and normalize the gene-module panel TSV.

    Reads the panel, restricts to PANEL_COLUMNS, drops rows missing a gene
    symbol, module_id, or module_class, deduplicates on
    (gene_symbol, module_id, module_class), and fills missing scoring
    directions with an empty string.

    Args:
      panel_path: Path to the panel TSV.
      encoding: Text encoding for the panel file.

    Returns:
      Long-form panel DF with PANEL_COLUMNS, one row per
      (gene_symbol, module_id, module_class).
    """
    panel = pd.read_csv(panel_path, sep="\t", dtype=str, encoding=encoding)
    panel = panel[list(PANEL_COLUMNS)].dropna(
        subset=["gene_symbol", "module_id", "module_class"]
    )
    panel = panel.drop_duplicates(
        subset=["gene_symbol", "module_id", "module_class"]
    )
    panel["scoring_direction"] = panel["scoring_direction"].fillna("")
    return panel.reset_index(drop=True)


def _order_module_genes(
    panel: pd.DataFrame,
    module_id: str,
) -> pd.DataFrame:
    """Select and order one module's genes for the Sankey layout.

    Args:
      panel: Normalized panel from _load_panel.
      module_id: The module_id to extract.

    Returns:
      Module rows ordered by class size (largest first), then class, then gene.
    """
    module = panel[panel["module_id"] == module_id].copy()
    class_sizes = module.groupby("module_class").size()
    module["_class_size"] = module["module_class"].map(class_sizes)
    module = module.sort_values(
        by=["_class_size", "module_class", "gene_symbol"],
        ascending=[False, True, True],
    )
    return module.reset_index(drop=True)


def _prepare_taxonomy_bars(
    counts: pd.DataFrame,
    module_order: Sequence[str] | None,
    exclude_modules: Sequence[str],
) -> tuple[pd.DataFrame, list[str]]:
    """Order module groups by count or optionally pass an explicit module_order.
    Within modules, bars are ordered by count then name.

    Args:
      counts: Counts from `_load_taxonomy_counts`.
      module_order: Optional explicit top-to-bottom module_id order; modules not
        listed are appended by descending gene count.
      exclude_modules: module_ids to remove.

    Returns:
      Tuple of (ordered bars DF with 'module_id', 'module_class', 'n_genes', and
      the ordered list of module_ids present).
    """
    counts = counts[~counts["module_id"].isin(set(exclude_modules))]
    if counts.empty:
        raise ValueError("No rows remain after excluding modules.")

    module_totals = counts.groupby("module_id")["n_genes"].sum()
    if module_order is None:
        ordered_modules = module_totals.sort_values(
            ascending=False
        ).index.tolist()
    else:
        present = set(counts["module_id"])
        ordered_modules = [m for m in module_order if m in present]
        ordered_modules += [
            m
            for m in module_totals.sort_values(ascending=False).index
            if m not in ordered_modules
        ]

    bars = counts.assign(
        module_id=pd.Categorical(
            counts["module_id"], categories=ordered_modules, ordered=True
        )
    ).sort_values(
        ["module_id", "n_genes", "module_class"],
        ascending=[True, False, True],
        ignore_index=True,
    )
    return bars, ordered_modules


def _compute_group_boundaries(
    bars: pd.DataFrame,
    ordered_modules: list[str],
) -> list[tuple[int, int, str]]:
    """Compute (start, end, module_id) row spans for each module group."""
    boundaries: list[tuple[int, int, str]] = []
    start = 0
    for module_id in ordered_modules:
        size = int((bars["module_id"] == module_id).sum())
        if size > 0:
            boundaries.append((start, start + size, module_id))
            start += size
    return boundaries


def _draw_alternating_bands(
    ax: Axes,
    y_positions: np.ndarray,
    group_boundaries: list[tuple[int, int, str]],
    y_padding: float,
) -> None:
    """Shade every other module group with a light background band."""
    for band_index, (start, end, _) in enumerate(group_boundaries):
        if band_index % 2 == 1:
            lo = min(y_positions[start], y_positions[end - 1]) - y_padding
            hi = max(y_positions[start], y_positions[end - 1]) + y_padding
            ax.axhspan(lo, hi, color="0.965", zorder=0)


def _annotate_bars(
    ax: Axes,
    y_positions: np.ndarray,
    n_genes: np.ndarray,
    x_max: float,
) -> None:
    """Annotate horizontal bars with a gene-count label.

    If the rendered label fits inside its bar, it is placed inside the bar,
    right-aligned in white. Otherwise it is placed to the right of the bar in
    black.

    Args:
      ax: Axes containing the bars to annotate.
      y_positions: Y positions of the bars.
      n_genes: Gene count for each bar.
      x_max: Maximum x value across all bars (used to calculate padding).
    """
    annotation_fontsize = _font_size_points(plt.rcParams["font.size"])

    ax.figure.canvas.draw()
    renderer = ax.figure.canvas.get_renderer()  # type: ignore

    inside_padding_px = annotation_fontsize * 0.25 * ax.figure.dpi / 72
    outside_padding_data = x_max * 0.01

    for position, count in zip(y_positions, n_genes, strict=False):
        label_text = f"{int(count):,}"

        probe = ax.text(
            0,
            0,
            label_text,
            fontsize=annotation_fontsize,
            va="center_baseline",
            ha="left",
        )
        text_width_px = probe.get_window_extent(renderer=renderer).width
        probe.remove()

        bar_left_px = ax.transData.transform((0, position))[0]
        bar_right_px = ax.transData.transform((count, position))[0]
        bar_width_px = bar_right_px - bar_left_px

        if text_width_px + 1.5 * inside_padding_px <= bar_width_px:
            inside_x_data = ax.transData.inverted().transform(
                (bar_right_px - inside_padding_px, 0)
            )[0]
            ax.text(
                inside_x_data,
                position,
                label_text,
                va="center_baseline",
                ha="right",
                fontsize=annotation_fontsize,
                color="white",
                zorder=10,
            )
        else:
            ax.text(
                count + outside_padding_data,
                position,
                label_text,
                va="center_baseline",
                ha="left",
                fontsize=annotation_fontsize,
                color="black",
                zorder=10,
            )


def _draw_module_sidebar(
    ax: Axes,
    bars: pd.DataFrame,
    y_positions: np.ndarray,
    group_boundaries: list[tuple[int, int, str]],
    module_colors: dict[str, tuple[float, float, float]],
    y_padding: float,
) -> None:
    """Draw colored module_id labels with gene counts to the right of the axes.

    Measures the widest 'module_id (n)' label via the renderer to size a
    consistent band width, then places a colored rectangle and centered white
    text per module group in a blended (axes-x, data-y) transform.

    Args:
      ax: Target axes.
      bars: Ordered bars DF, used to sum gene counts per module group.
      y_positions: Y positions of all bars.
      group_boundaries: Output of _compute_group_boundaries.
      module_colors: Mapping from module_id to RGB tuple.
      y_padding: Half the bar spacing, used to extend bands beyond bars.
    """
    annotation_fontsize = _font_size_points(plt.rcParams["font.size"])
    ax.figure.canvas.draw()
    renderer = ax.figure.canvas.get_renderer()  # type: ignore

    group_labels = {
        module_id: (
            f"{humanize_module_name(module_id)} "
            f"({int(bars['n_genes'].iloc[start:end].sum())})"
        )
        for start, end, module_id in group_boundaries
    }

    max_label_width_px = 0.0
    for _, _, module_id in group_boundaries:
        probe = ax.text(
            0, 0, group_labels[module_id], fontsize=annotation_fontsize
        )
        max_label_width_px = max(
            max_label_width_px,
            probe.get_window_extent(renderer=renderer).width,
        )
        probe.remove()

    ax_width_px = ax.get_window_extent(renderer=renderer).width
    padding_px = annotation_fontsize * 1.5 * ax.figure.dpi / 72
    band_width = (max_label_width_px + padding_px) / ax_width_px

    trans = blended_transform_factory(ax.transAxes, ax.transData)
    band_x = 1.02

    for start, end, module_id in group_boundaries:
        lo = min(y_positions[start], y_positions[end - 1]) - y_padding
        hi = max(y_positions[start], y_positions[end - 1]) + y_padding
        mid_y = (y_positions[start] + y_positions[end - 1]) / 2.0

        ax.add_patch(
            Rectangle(
                (band_x, lo),
                band_width,
                hi - lo,
                facecolor=module_colors[module_id],
                edgecolor="none",
                transform=trans,
                clip_on=False,
                zorder=3,
            )
        )
        ax.text(
            band_x + band_width / 2,
            mid_y,
            group_labels[module_id],
            va="center",
            ha="center",
            fontsize=annotation_fontsize,
            color="white",
            transform=trans,
            clip_on=False,
            zorder=4,
        )


def _plot_taxonomy_barplot(
    bars: pd.DataFrame,
    ordered_modules: list[str],
    *,
    outpath: str | Path,
    bar_height_in: float,
    fig_width_in: float,
    cmap: str,
    bar_spacing: float,
    bar_height: float,
) -> Path:
    """Render the grouped taxonomy barplot to disk.

    Args:
      bars: Ordered bars DF from _prepare_taxonomy_bars.
      ordered_modules: module_ids in plot order.
      outpath: Output path for the saved figure.
      bar_height_in: Vertical inches allotted per bar.
      fig_width_in: Figure width in inches.
      cmap: Colormap palette for module_id colors.
      bar_spacing: Vertical spacing between adjacent bars in data units.
      bar_height: Height of each bar in data units.

    Returns:
      Path to the written figure file.
    """
    n_bars = len(bars)
    n_genes = bars["n_genes"].to_numpy()

    # Top-to-bottom: first ordered row sits at the top.
    y_positions = (n_bars - 1 - np.arange(n_bars)) * bar_spacing
    y_padding = bar_spacing / 2.0
    plot_height_units = max(1.0, (n_bars - 1) * bar_spacing + bar_height)
    fig_height = max(1.2, bar_height_in * plot_height_units + 0.75)

    fig, ax = plt.subplots(figsize=(fig_width_in, fig_height))

    group_boundaries = _compute_group_boundaries(bars, ordered_modules)
    _draw_alternating_bands(ax, y_positions, group_boundaries, y_padding)

    module_colors = dict(
        zip(
            ordered_modules,
            sns.color_palette(cmap, n_colors=len(ordered_modules)),
            strict=False,
        )
    )
    bar_colors = [module_colors[module_id] for module_id in bars["module_id"]]
    edge_colors = [_darken_color(color, factor=0.80) for color in bar_colors]

    ax.barh(
        y_positions,
        n_genes,
        height=bar_height,
        color=bar_colors,
        linewidth=0.3,
        edgecolor=edge_colors,
        zorder=2,
    )

    _annotate_bars(
        ax=ax,
        y_positions=y_positions,
        n_genes=n_genes,
        x_max=float(n_genes.max()),
    )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(bars["module_class"].tolist())
    ax.set_xlabel("Genes")
    ax.set_ylim(
        y_positions.min() - y_padding,
        y_positions.max() + y_padding,
    )
    ax.margins(y=0)

    _draw_module_sidebar(
        ax=ax,
        bars=bars,
        y_positions=y_positions,
        group_boundaries=group_boundaries,
        module_colors=module_colors,
        y_padding=y_padding,
    )

    sns.despine(ax=ax)
    output_path = Path(outpath)
    fig.savefig(output_path, bbox_inches="tight", dpi=450)
    plt.close(fig)

    return output_path


def taxonomy_class_barplot(
    panel_path: str | Path,
    *,
    outpath: str | Path,
    encoding: str = "utf-8",
    module_order: Sequence[str] | None = None,
    exclude_modules: Sequence[str] = (),
    bar_height_in: float = 0.18,
    fig_width_in: float = 2.75,
    cmap: str = "tab20c",
    bar_spacing: float = 0.5,
    bar_height: float = 0.4125,
) -> Path:
    """Plot module_class bars grouped by module_id, sized by gene count.

    Args:
      panel_path: Path to the panel TSV.
      outpath: Output path for the saved figure.
      encoding: Text encoding for the panel file.
      module_order: Optional explicit top-to-bottom module_id order; unlisted
        modules are appended by descending gene count.
      exclude_modules: module_ids to drop (e.g. an oversized module given its
        own panel so it does not dominate the shared x-axis).
      bar_height_in: Vertical inches allotted per bar.
      fig_width_in: Figure width in inches.
      cmap: Colormap palette for module_id colors.
      bar_spacing: Vertical spacing between adjacent bars in data units.
      bar_height: Height of each bar in data units.

    Returns:
      Path to the written figure file.
    """
    panel = _load_panel(panel_path, encoding=encoding)
    counts = (
        panel.groupby(["module_id", "module_class"], observed=True)
        .size()
        .reset_index(name="n_genes")
    )
    bars, ordered_modules = _prepare_taxonomy_bars(
        counts, module_order=module_order, exclude_modules=exclude_modules
    )
    return _plot_taxonomy_barplot(
        bars,
        ordered_modules,
        outpath=outpath,
        bar_height_in=bar_height_in,
        fig_width_in=fig_width_in,
        cmap=cmap,
        bar_spacing=bar_spacing,
        bar_height=bar_height,
    )


def _sibling_color(
    base_rgb: tuple[float, float, float],
    n_siblings: int,
    sibling_index: int,
) -> tuple[float, float, float]:
    """Return a lightness-shifted variant of base_rgb for a sibling gene.

    Args:
      base_rgb: Parent module_class color as (r, g, b) floats in [0, 1].
      n_siblings: Total number of genes under this module_class.
      sibling_index: 0-based rank of the gene within the class.

    Returns:
      (r, g, b) with lightness shifted across siblings.
    """
    if n_siblings == 1:
        return base_rgb

    hue, lightness, saturation = colorsys.rgb_to_hls(*base_rgb)
    offsets = [-0.15 + 0.30 * i / (n_siblings - 1) for i in range(n_siblings)]
    new_lightness = max(0.15, min(0.85, lightness + offsets[sibling_index]))
    return colorsys.hls_to_rgb(hue, new_lightness, saturation)


def _build_taxonomy_layout(
    module: pd.DataFrame,
    node_gap: float,
    cmap: str,
) -> dict:
    """Compute geometry for a module_id -> module_class -> gene Sankey.

    Each gene contributes unit height; a module_class height is its gene count;
    the module_id node spans all genes. Leftmost two columns are gapless so
    ribbons align cleanly; the gene column carries the gaps.

    Args:
      module: Ordered DF from _order_module_genes.
      node_gap: Gap between adjacent gene nodes as a fraction of node height.
      cmap: Colormap palette for module_class nodes.

    Returns:
      Dict with keys:
        'module_node': {y_top, height}
        'class_segments': list of {label, count, y_top, height, color}
        'gene_nodes': list of {label, direction, y_top, height, color}
        'module_class_ribbons': list of {y_src_top, y_dst_top, height, color}
        'class_gene_ribbons': list of {y_src_top, y_dst_top, height, color}
    """
    classes = module["module_class"].unique().tolist()
    n_classes = len(classes)
    n_genes = len(module)

    palette = sns.color_palette(cmap, n_colors=n_classes)
    class_colors = {
        name: tuple(palette[index]) for index, name in enumerate(classes)
    }
    class_sizes = module.groupby("module_class").size().to_dict()

    # Gene node = 1 unit tall, gap = node_gap units. Normalizing by the total
    # gene-column units keeps one node a fixed fraction of the axes regardless
    # of gene count, so node size is constant once figure height scales with
    # the same unit count.
    gene_units = n_genes + node_gap * (n_genes - 1)
    scale = 1.0 / gene_units
    gene_gap = node_gap * scale
    column_height = n_genes * scale
    gene_column_height = column_height + (n_genes - 1) * gene_gap

    # Left: single module_id node, gapless.
    module_node = {"y_top": 0.5 + column_height / 2.0, "height": column_height}

    # Middle: stacked module_class segments, gapless.
    class_segments: list[dict] = []
    class_cursor = 0.5 + column_height / 2.0
    for name in classes:
        count = class_sizes[name]
        height = count * scale
        class_segments.append(
            {
                "label": name,
                "count": count,
                "y_top": class_cursor,
                "height": height,
                "color": class_colors[name],
            }
        )
        class_cursor -= height

    # module_id -> module_class ribbons (one per class, class-width).
    module_class_ribbons: list[dict] = []
    module_cursor = module_node["y_top"]
    for segment in class_segments:
        module_class_ribbons.append(
            {
                "y_src_top": module_cursor,
                "y_dst_top": segment["y_top"],
                "height": segment["height"],
                "color": segment["color"],
            }
        )
        module_cursor -= segment["height"]

    # Right: gene nodes, gapped. module_class -> gene ribbons (gene-width).
    gene_nodes: list[dict] = []
    class_gene_ribbons: list[dict] = []
    gene_cursor = 0.5 + gene_column_height / 2.0
    class_src_cursor = {seg["label"]: seg["y_top"] for seg in class_segments}
    sibling_index = dict.fromkeys(classes, 0)

    for row in module.itertuples():
        gene_color = _sibling_color(
            base_rgb=class_colors[row.module_class],  # type: ignore
            n_siblings=class_sizes[row.module_class],
            sibling_index=sibling_index[row.module_class],
        )
        sibling_index[row.module_class] += 1

        gene_nodes.append(
            {
                "label": row.gene_symbol,
                "direction": row.scoring_direction,
                "y_top": gene_cursor,
                "height": scale,
                "color": gene_color,
            }
        )
        class_gene_ribbons.append(
            {
                "y_src_top": class_src_cursor[row.module_class],
                "y_dst_top": gene_cursor,
                "height": scale,
                "color": gene_color,
            }
        )
        class_src_cursor[row.module_class] -= scale
        gene_cursor -= scale + gene_gap

    return {
        "module_node": module_node,
        "class_segments": class_segments,
        "gene_nodes": gene_nodes,
        "module_class_ribbons": module_class_ribbons,
        "class_gene_ribbons": class_gene_ribbons,
    }


def _draw_bezier_ribbon(
    ax: Axes,
    x_src: float,
    x_dst: float,
    y_src_top: float,
    y_dst_top: float,
    height: float,
    color: tuple[float, float, float],
    alpha: float = 0.45,
) -> None:
    """Draw one filled ribbon of constant height between two columns.

    Args:
      ax: Target axes.
      x_src: Right x-edge of the source node (axes fraction).
      x_dst: Left x-edge of the destination node (axes fraction).
      y_src_top: Top y of the ribbon at the source.
      y_dst_top: Top y of the ribbon at the destination.
      height: Vertical height of the ribbon (constant across the span).
      color: RGB tuple for the ribbon fill.
      alpha: Ribbon transparency.
    """
    x_ctrl = x_src + 0.5 * (x_dst - x_src)
    y_src_bot = y_src_top - height
    y_dst_bot = y_dst_top - height

    verts = [
        (x_src, y_src_top),
        (x_ctrl, y_src_top),
        (x_ctrl, y_dst_top),
        (x_dst, y_dst_top),
        (x_dst, y_dst_bot),
        (x_ctrl, y_dst_bot),
        (x_ctrl, y_src_bot),
        (x_src, y_src_bot),
        (x_src, y_src_top),
    ]
    codes = [
        MplPath.MOVETO,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.LINETO,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CLOSEPOLY,
    ]
    patch = PathPatch(
        MplPath(verts, codes),
        facecolor=(*color, alpha),
        edgecolor="none",
        zorder=1,
        transform=ax.transAxes,
        clip_on=False,
    )
    ax.add_patch(patch)


def _draw_direction_legend(
    ax: Axes,
    present_directions: Iterable[str],
    fontsize: float,
    y_anchor: float,
) -> None:
    """Add a scoring_direction marker legend for directions present in the
    module.

    Args:
      ax: Target axes.
      present_directions: Directions actually annotated on this module's genes.
      fontsize: Base font size for legend text.
      y_anchor: Vertical axes fraction for the legend's lower edge.
    """
    present = set(present_directions)
    if handles := [
        Line2D(
            [0],
            [0],
            marker=marker,
            color="none",
            markerfacecolor=color,
            markeredgecolor="none",
            markersize=6,
            label=direction,
        )
        for direction, (marker, color) in DIRECTION_MARKERS.items()
        if direction in present
    ]:
        ax.legend(
            handles=handles,
            loc="lower center",
            bbox_to_anchor=(0.425, y_anchor),
            ncol=len(handles),
            frameon=False,
            fontsize=fontsize,
            handletextpad=0.2,
            columnspacing=1.2,
        )
    else:
        return


def _plot_module_sankey(
    module: pd.DataFrame,
    *,
    module_id: str,
    outpath: str | Path,
    node_height_in: float = 0.0125,
    fig_width_in: float = 7.0,
    cmap: str = "tab10",
    node_width: float = 0.0225,
    node_gap: float = 0.525,
) -> Path:
    """Render per module Sankey diagram.

    Args:
      module: Ordered DF from _load_module_genes.
      module_id: The module_id label, used for the left node and title.
      outpath: Output path for the saved figure.
      node_height_in: Vertical inches allotted per gene.
      fig_width_in: Figure width in inches.
      cmap: Colormap palette for module_class nodes.
      node_width: Width of column nodes (axes fraction).
      node_gap: Vertical gap between gene nodes (axes fraction).

    Returns:
      Path to the written figure file.
    """
    layout = _build_taxonomy_layout(module, node_gap=node_gap, cmap=cmap)

    n_genes = len(module)
    gene_units = n_genes + node_gap * (n_genes - 1)
    top_margin_in = 0.2
    bottom_margin_in = 0.4
    axes_height_in = node_height_in * gene_units
    fig_height = axes_height_in + top_margin_in + bottom_margin_in
    legend_gap_in = 0.15
    legend_y_anchor = -legend_gap_in / axes_height_in

    fig, ax = plt.subplots(figsize=(fig_width_in, fig_height))
    fig.subplots_adjust(
        top=1.0 - top_margin_in / fig_height,
        bottom=bottom_margin_in / fig_height,
    )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    x_module_left = 0.10
    x_module_right = x_module_left + node_width
    x_class_left = 0.40
    x_class_right = x_class_left + node_width
    x_gene_left = 0.72
    x_gene_right = x_gene_left + node_width

    module_node = layout["module_node"]

    for segment in layout["class_segments"]:
        ax.add_patch(
            plt.Rectangle(  # type: ignore
                (x_class_left, segment["y_top"] - segment["height"]),
                node_width,
                segment["height"],
                facecolor=segment["color"],
                edgecolor="none",
                zorder=2,
                transform=ax.transAxes,
                clip_on=False,
            )
        )

    for node in layout["gene_nodes"]:
        ax.add_patch(
            plt.Rectangle(  # type: ignore
                (x_gene_left, node["y_top"] - node["height"]),
                node_width,
                node["height"],
                facecolor=node["color"],
                edgecolor="none",
                zorder=2,
                transform=ax.transAxes,
                clip_on=False,
            )
        )

    for ribbon in layout["module_class_ribbons"]:
        _draw_bezier_ribbon(
            ax=ax,
            x_src=x_module_right,
            x_dst=x_class_left,
            y_src_top=ribbon["y_src_top"],
            y_dst_top=ribbon["y_dst_top"],
            height=ribbon["height"],
            color=ribbon["color"],
        )

    for ribbon in layout["class_gene_ribbons"]:
        _draw_bezier_ribbon(
            ax=ax,
            x_src=x_class_right,
            x_dst=x_gene_left,
            y_src_top=ribbon["y_src_top"],
            y_dst_top=ribbon["y_dst_top"],
            height=ribbon["height"],
            color=ribbon["color"],
        )

    fontsize = plt.rcParams["xtick.labelsize"]
    label_pad = 0.008
    marker_pad = 0.012

    # module_id label
    ax.text(
        x_module_left,
        module_node["y_top"] - module_node["height"] / 2.0,
        humanize_module_name(module_id),
        ha="right",
        va="center",
        fontsize=fontsize,
        transform=ax.transAxes,
    )

    # module_class labels w/ gene count
    for segment in layout["class_segments"]:
        ax.text(
            x_class_left - label_pad,
            segment["y_top"] - segment["height"] / 2.0,
            f"{segment['label']} ({segment['count']})",
            ha="right",
            va="center",
            fontsize=fontsize,
            transform=ax.transAxes,
        )

    # gene labels w/ scoring_direction marker
    for node in layout["gene_nodes"]:
        y_mid = node["y_top"] - node["height"] / 2.0
        marker_spec = DIRECTION_MARKERS.get(node["direction"])
        if marker_spec is not None:
            marker, marker_color = marker_spec
            ax.plot(
                x_gene_right + marker_pad,
                y_mid,
                marker=marker,
                markerfacecolor=marker_color,
                markeredgecolor="none",
                markersize=3.25,
                linestyle="none",
                transform=ax.transAxes,
                clip_on=False,
                zorder=3,
            )
        ax.text(
            x_gene_right + marker_pad * 2.0,
            y_mid,
            node["label"],
            ha="left",
            va="center",
            fontsize=fontsize,
            transform=ax.transAxes,
        )

    present_directions = {node["direction"] for node in layout["gene_nodes"]}
    _draw_direction_legend(
        ax,
        present_directions,
        fontsize=fontsize,
        y_anchor=legend_y_anchor,
    )

    output_path = Path(outpath)
    fig.savefig(output_path, bbox_inches="tight", dpi=450)
    plt.close(fig)

    return output_path


def module_taxonomy_sankey(
    panel_path: str | Path,
    *,
    module_id: str,
    outpath: str | Path,
    node_height_in: float = 0.065,
    fig_width_in: float = 5.75,
    cmap: str = "Set1",
) -> Path:
    """Plot per-module Sankey diagram.

    Args:
      panel_path: Path to the panel TSV.
      module_id: The module_id to visualize.
      outpath: Output path for the saved figure.
      node_height_in: Vertical inches allotted per gene.
      fig_width_in: Figure width in inches.
      cmap: Colormap palette for module_class nodes.

    Returns:
      Path to the written figure file.
    """
    panel = _load_panel(panel_path)
    module = _order_module_genes(panel, module_id)
    if module.empty:
        raise ValueError(f"No rows found for module_id '{module_id}'.")

    return _plot_module_sankey(
        module,
        module_id=module_id,
        outpath=outpath,
        node_height_in=node_height_in,
        fig_width_in=fig_width_in,
        cmap=cmap,
    )


# _set_matplotlib_publication_parameters()
# panel = pd.read_csv("nasp_gene_modules_intermediate.txt", sep="\t", dtype=str)
# for module_id in sorted(panel["module_id"].dropna().unique()):
#     module_taxonomy_sankey(
#         "nasp_gene_modules_intermediate.txt",
#         module_id=module_id,
#         outpath=f"sankey_{module_id}.png",
#     )

# taxonomy_class_barplot(
#     "nasp_gene_modules_intermediate.txt",
#     outpath="taxonomy_class_barplot.png",
# )

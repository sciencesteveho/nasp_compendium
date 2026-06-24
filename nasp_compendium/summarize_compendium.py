"""Render the NASP mechanistic compendium as a pathway map."""

from __future__ import annotations

import dataclasses
import shutil
import subprocess
from pathlib import Path
from typing import Any

import graphviz  # type: ignore
import yaml  # type: ignore

from nasp_compendium.style import DEFAULT_ARROWHEAD
from nasp_compendium.style import DEFAULT_BORDER_COLOR
from nasp_compendium.style import DEFAULT_EVIDENCE_STYLE
from nasp_compendium.style import DEFAULT_FILL_COLOR
from nasp_compendium.style import DEFAULT_REL_COLOR
from nasp_compendium.style import ENTITY_BORDER_COLORS
from nasp_compendium.style import ENTITY_FIELDS
from nasp_compendium.style import ENTITY_FILL_COLORS
from nasp_compendium.style import EVIDENCE_STYLES
from nasp_compendium.style import REL_ARROWHEAD
from nasp_compendium.style import REL_COLOR


COMPENDIUM_DIR: Path = (
    Path(__file__).resolve().parent.parent / "docs" / "compendium"
)

GRAPH_FONT: str = "Helvetica"
SVG_FONT_FAMILY: str = "Helvetica, 'Nimbus Sans', Arial, sans-serif"
COMPACT_NONCONSTRAINING_RELS: frozenset[str] = frozenset(
    {
        "contains",
        "correlates",
        "negatively_correlates",
        "does_not_correlate",
        "does_not_drive",
        "binds_recruits",
        "retains",
    }
)


@dataclasses.dataclass(frozen=True)
class Compendium:
    """A loaded NASP knowledge compendium.

    This class manages a directory of per-paper Markdown files. Each .md is
    parsed as plain YAML with two top-level keys:
      paper
      edges

    Attributes:
      papers: Mapping of paper_id to paper metadata dict.
      edges: Flat list of edge dicts across all loaded papers.
    """

    papers: dict[str, dict[str, Any]]
    edges: list[dict[str, Any]]

    @classmethod
    def from_dir(cls, directory: Path) -> Compendium:
        """Load every .md file in directory into one compendium. On collision
        (same paper id appearing in more than one file), the alphabetically
        last file wins.

        Args:
          directory: Directory containing per-paper compendium files.

        Returns:
          `Compendium` aggregating all papers and edges.

        Raises:
          FileNotFoundError: If directory does not exist or is not a directory.
          yaml.YAMLError: If any file is not valid YAML.
        """
        if not directory.exists() or not directory.is_dir():
            raise FileNotFoundError(
                f"Compendium directory not found: {directory}"
            )

        papers: dict[str, dict[str, Any]] = {}
        edges: list[dict[str, Any]] = []

        for md_path in sorted(directory.glob("*.md")):
            if md_path.name.endswith(".gold.md"):
                continue
            file_papers, file_edges = parse_md(md_path)
            papers |= file_papers
            edges.extend(file_edges)

        return cls(papers=papers, edges=edges)

    def filtered(
        self,
        *,
        paper_ids: set[str] | None = None,
        excluded_rels: set[str] | None = None,
    ) -> Compendium:
        """Return a compendium subset filtered by paper id and relationship.

        Args:
          paper_ids: Optional set of paper ids to keep. Edges with multiple
            papers are retained if at least one paper is selected, and their
            `papers` list is narrowed to the selected ids.
          excluded_rels: Optional set of edge relationship labels to remove.

        Returns:
          A new `Compendium` containing filtered paper metadata and edges.
        """
        papers = self.papers
        if paper_ids is not None:
            papers = {
                paper_id: paper
                for paper_id, paper in self.papers.items()
                if paper_id in paper_ids
            }

        filtered_edges: list[dict[str, Any]] = []
        for edge in self.edges:
            if excluded_rels and str(edge.get("rel", "")) in excluded_rels:
                continue

            edge_papers = [str(paper) for paper in edge.get("papers") or []]
            if paper_ids is not None:
                edge_papers = [
                    paper for paper in edge_papers if paper in paper_ids
                ]
                if not edge_papers:
                    continue

            filtered_edge = dict(edge)
            filtered_edge["papers"] = edge_papers
            filtered_edges.append(filtered_edge)

        return Compendium(papers=papers, edges=filtered_edges)


def parse_md(
    path: Path,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    """Parse a per-paper compendium file as YAML.

    Args:
      path: Path to the compendium file.

    Returns:
      (papers, edges) where papers maps paper_id to metadata and edges is a list
      of edge dicts. Either may be empty if its key is absent or the file is not
      a compendium file.
    """
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError:
        print(f"  Skipping {path.name}: not a YAML compendium file")
        return {}, []
    if not isinstance(data, dict) or (
        "paper" not in data and "edges" not in data
    ):
        return {}, []
    papers = data.get("paper") or {}
    edges = data.get("edges") or []
    return papers, edges


def format_citation(paper_id: str) -> str:
    """Convert a paper_id into a short citation format."""
    parts = paper_id.split("_")
    if len(parts) >= 2 and parts[-1].isdigit() and len(parts[-1]) == 4:
        return f"{parts[0]} {parts[-1]}"
    return paper_id


def citation_sort_key(paper_id: str) -> tuple[int, str]:
    """Sort paper ids by publication year, then short citation text."""
    parts = paper_id.split("_")
    year = 9999
    if parts and parts[-1].isdigit() and len(parts[-1]) == 4:
        year = int(parts[-1])
    return year, format_citation(paper_id).lower()


def format_edge_annotation(
    paper_ids: list[str],
    *,
    max_visible: int = 1,
) -> str:
    """Return a compact visible annotation string for an edge."""
    if not paper_ids:
        return ""

    citations = [format_citation(paper_id) for paper_id in paper_ids]
    if len(citations) <= max_visible:
        return ", ".join(citations)

    visible = ", ".join(citations[:max_visible])
    remaining = len(citations) - max_visible
    return f"{visible} +{remaining}"


def node_entity_types(compendium: Compendium) -> dict[str, str]:
    """Map every declared entity name to the field in which it appears.

    Returns:
      A mapping from entity name to entity field (e.g. "genes", "pathways").
      Entities that appear in more than one field are assigned to the first
      field in ENTITY_FIELDS that contains them.
    """
    entity_types: dict[str, str] = {}
    for paper in compendium.papers.values():
        for field in ENTITY_FIELDS:
            for entity in paper.get(field) or []:
                entity_types.setdefault(entity, field)
    return entity_types


def format_node_label(node: str) -> str:
    """Format a node id for display in rendered graphs."""
    return node.replace("BAX_BAK_pore", "BAX/BAK_pore").replace("_", " ")


def aggregate_duplicate_edges(
    edges: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Collapse render-equivalent edges into one edge with merged papers.

    Edges are render-equivalent when they have the same source, target, and
    relationship. The merged edge keeps the first edge's visual attributes and
    combines paper citations in publication-year order.
    """
    by_key: dict[tuple[str, str, str], dict[str, Any]] = {}
    order: list[tuple[str, str, str]] = []

    for edge in edges:
        key = (
            str(edge.get("source", "")),
            str(edge.get("target", "")),
            str(edge.get("rel", "")),
        )
        if key not in by_key:
            merged = dict(edge)
            merged["papers"] = []
            by_key[key] = merged
            order.append(key)

        papers = by_key[key].setdefault("papers", [])
        for paper in edge.get("papers") or []:
            paper_id = str(paper)
            if paper_id not in papers:
                papers.append(paper_id)

    aggregated: list[dict[str, Any]] = []
    for key in order:
        edge = by_key[key]
        edge["papers"] = sorted(
            edge.get("papers") or [],
            key=citation_sort_key,
        )
        aggregated.append(edge)

    return aggregated


def _select_layout_engine(
    layout_engine: str | None,
    compact: bool,
    *,
    default_layout_engine: str = "dot",
    compact_layout_engine: str = "dot",
) -> str:
    """Return the Graphviz engine for the requested rendering mode."""
    if layout_engine:
        return layout_engine
    return compact_layout_engine if compact else default_layout_engine


def _highest_degree_node(edges: list[dict[str, Any]]) -> str | None:
    """Return the node with the most incident rendered edges."""
    degree_by_node: dict[str, int] = {}
    for edge in edges:
        for endpoint in ("source", "target"):
            if node := str(edge.get(endpoint, "")):
                degree_by_node[node] = degree_by_node.get(node, 0) + 1

    if not degree_by_node:
        return None
    return max(degree_by_node, key=lambda node: (degree_by_node[node], node))


def _compact_edge_legend_label(
    legend_rows: tuple[tuple[str, str, str], ...] = (
        ("#55A868", "━━▶", "activation / positive output"),
        ("#C44E52", "━━┤", "inhibition / downregulation"),
        ("#4C72B0", "━━▶", "requirement / production"),
        ("#8172B3", "━━▶", "binding / recruitment"),
        ("#999999", "···○", "correlation / no effect"),
        (DEFAULT_REL_COLOR, "━━━━", "direct or perturbation-supported"),
        (DEFAULT_REL_COLOR, "╍╍╍▶", "canonical inferred"),
        (DEFAULT_REL_COLOR, "···▶", "correlative"),
    ),
) -> str:
    """Return a Graphviz HTML label for the compact edge legend."""
    rows = [
        (
            f'<TR><TD ALIGN="RIGHT"><FONT FACE="{GRAPH_FONT}" '
            f'POINT-SIZE="7" COLOR="{color}">{symbol}</FONT></TD>'
            f'<TD ALIGN="LEFT"><FONT FACE="{GRAPH_FONT}" '
            f'POINT-SIZE="7">{label}</FONT></TD></TR>'
        )
        for color, symbol, label in legend_rows
    ]
    rows_text = "\n".join(rows)
    return (
        "<\n"
        '<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2" CELLPADDING="1">\n'
        f"{rows_text}\n"
        "</TABLE>\n"
        ">"
    )


def _add_compact_edge_legend(
    diagram: graphviz.Digraph,
    anchor_node: str | None,
) -> None:
    """Add a visual compact-mode legend for edge encodings."""
    legend_node = "__edge_legend__"
    diagram.node(
        legend_node,
        label=_compact_edge_legend_label(),
        shape="box",
        style="filled",
        fillcolor="#FFFFFF",
        color="#BBBBBB",
        fontname=GRAPH_FONT,
        margin="0.03,0.025",
    )
    if anchor_node is not None:
        diagram.edge(
            legend_node,
            anchor_node,
            style="invis",
            arrowhead="none",
            constraint="false",
            weight="0",
            minlen="0",
        )


def _compact_edge_is_backbone(
    rel: str,
    source: str,
    target: str,
    *,
    backbone_rels: frozenset[str] = frozenset(
        {
            "activates",
            "causes",
            "drives",
            "induces",
            "required_for",
            "produces",
            "forms_pore_for",
            "suppresses",
            "inhibits",
            "downregulates",
            "upregulates",
        }
    ),
) -> bool:
    """Return whether an edge should define compact-mode LR flow."""
    del source, target
    return rel in backbone_rels


def _edge_constraint(
    rel: str,
    source: str,
    target: str,
    compact: bool,
    *,
    non_constraining_rels: frozenset[str] = frozenset(
        {
            "contains",
            "correlates",
            "negatively_correlates",
            "does_not_correlate",
            "does_not_drive",
        }
    ),
) -> str:
    """Return the Graphviz constraint flag for an edge."""
    if not compact:
        return str(rel not in non_constraining_rels).lower()
    if rel in COMPACT_NONCONSTRAINING_RELS:
        return "false"
    return str(_compact_edge_is_backbone(rel, source, target)).lower()


def _edge_weight(
    rel: str,
    source: str,
    target: str,
    compact: bool,
) -> str:
    """Return the Graphviz weight for an edge."""
    if not compact:
        return "1.0"
    return "2.0" if _compact_edge_is_backbone(rel, source, target) else "0.1"


def _edge_minlen(
    rel: str,
    source: str,
    target: str,
    compact: bool,
) -> str:
    """Return the Graphviz minlen for an edge."""
    if not compact:
        return "1"
    return "1" if _compact_edge_is_backbone(rel, source, target) else "0"


def _node_degrees(edges: list[dict[str, Any]]) -> dict[str, int]:
    """Return incident edge counts for each rendered node."""
    degrees: dict[str, int] = {}
    for edge in edges:
        for endpoint in ("source", "target"):
            if node := str(edge.get(endpoint, "")):
                degrees[node] = degrees.get(node, 0) + 1
    return degrees


def _compact_leaf_rank_groups(
    edges: list[dict[str, Any]],
) -> dict[str, list[str]]:
    """Return weak leaf nodes to keep beside their target in compact mode."""
    degrees = _node_degrees(edges)
    groups: dict[str, set[str]] = {}

    for edge in edges:
        rel = str(edge.get("rel", ""))
        if rel not in COMPACT_NONCONSTRAINING_RELS:
            continue

        source = str(edge.get("source", ""))
        target = str(edge.get("target", ""))
        if not source or not target:
            continue

        if degrees.get(source, 0) == 1 and degrees.get(target, 0) > 1:
            groups.setdefault(target, set()).add(source)
        elif degrees.get(target, 0) == 1 and degrees.get(source, 0) > 1:
            groups.setdefault(source, set()).add(target)

    return {
        anchor: sorted(leaves) for anchor, leaves in groups.items() if leaves
    }


def _add_compact_leaf_rank_groups(
    diagram: graphviz.Digraph,
    rank_groups: dict[str, list[str]],
) -> None:
    """Keep weak leaf nodes in the same compact LR rank as their anchor."""
    for group_index, (anchor, leaves) in enumerate(sorted(rank_groups.items())):
        with diagram.subgraph(name=f"compact_leaf_rank_{group_index}") as group:  # type: ignore
            group.attr(rank="same")
            group.node(anchor)
            for leaf in leaves:
                group.node(leaf)


def render(
    compendium: Compendium,
    output_stem: Path,
    output_format: str = "png",
    rankdir: str = "LR",
    layout_engine: str | None = None,
    annotate_papers: bool = False,
    aggregate_edges: bool = True,
    compact: bool = False,
    graph_font_path: str = (
        "/System/Library/Fonts:"
        "/System/Library/Fonts/Supplemental:"
        "/Library/Fonts:"
        "/usr/share/fonts:"
        "/usr/local/share/fonts"
    ),
) -> None:
    """Render the compendium as a directed pathway diagram via Graphviz.

    Nodes are styled by the entity field in which they are declared. Edges and
    lines are styled by relationship type and evidence strength, respectively.

    Args:
      compendium: The loaded compendium.
      output_stem: Stem for the output file.
      output_format: Graphviz output format.
      rankdir: Graphviz rank direction. `"TB"` is top-to-bottom; `"LR"` is
        left-to-right.
      layout_engine: Optional Graphviz layout engine. Defaults to `dot`.
        `sfdp`, `fdp`, and `neato` are exploratory alternatives.
      annotate_papers: If True, append a short paper citation to each edge
        label.
      aggregate_edges: If True, merge duplicate source-target-rel edges.
      compact: If True, keep a left-to-right pathway layout while hiding
        edge labels and adding a visual edge legend.
      graph_font_path: Graphviz font search path used for deterministic
        font resolution across platforms.
    """
    if not compendium.edges:
        print("  No edges recorded. Add an 'edges:' block to a paper file.")
        return

    edges = (
        aggregate_duplicate_edges(compendium.edges)
        if aggregate_edges
        else compendium.edges
    )
    entity_types = node_entity_types(compendium)
    selected_layout_engine = _select_layout_engine(
        layout_engine,
        compact=compact,
    )

    graph_attr = {
        "rankdir": rankdir,
        "splines": "spline",
        "fontname": GRAPH_FONT,
        "fontnames": "ps",
        "fontpath": graph_font_path,
        "ordering": "out",
        "remincross": "true",
        "outputorder": "edgesfirst",
        "overlap": "prism",
        "sep": "+0.12",
        "esep": "+0.08",
        "nodesep": "0.10",
        "ranksep": "0.18 equally",
        "pack": "true",
        "packmode": "node",
        "packmargin": "0",
        "concentrate": "false",
        "dpi": "450",
        "margin": "0",
        "pad": "0",
        "ratio": "compress",
    }
    node_attr = {
        "shape": "box",
        "style": "rounded,filled",
        "fontname": GRAPH_FONT,
        "fontsize": "5",
        "penwidth": "0.65",
        "margin": "0.018,0.010",
        "width": "0.01",
        "height": "0.01",
        "fixedsize": "false",
    }
    edge_attr = {
        "fontname": GRAPH_FONT,
        "fontsize": "4.5",
        "penwidth": "0.65",
        "arrowsize": "0.28",
        "minlen": "1",
    }

    if compact:
        graph_attr |= {
            "splines": "spline",
            "overlap": "false",
            "sep": "+0.022",
            "esep": "+0.010",
            "nodesep": "0.045",
            "ranksep": "0.10",
            "pack": "true",
            "packmode": "node",
            "concentrate": "false",
            "ratio": "compress",
            "margin": "0",
            "pad": "0",
        }
        node_attr |= {
            "fontname": GRAPH_FONT,
            "fontsize": "5.0",
            "margin": "0.018,0.010",
            "width": "0.01",
            "height": "0.01",
            "penwidth": "0.68",
        }
        edge_attr |= {
            "fontname": GRAPH_FONT,
            "fontsize": "4.2",
            "arrowsize": "0.24",
            "penwidth": "0.60",
            "minlen": "1",
        }
    elif annotate_papers:
        graph_attr |= {
            "splines": "spline",
            "overlap": "false",
            "sep": "+0.028",
            "esep": "+0.014",
            "nodesep": "0.050",
            "ranksep": "0.105",
            "pack": "true",
            "packmode": "node",
            "concentrate": "false",
            "ratio": "compress",
            "margin": "0",
            "pad": "0",
        }
        node_attr |= {
            "fontsize": "4.8",
            "margin": "0.017,0.010",
            "penwidth": "0.62",
        }
        edge_attr |= {
            "fontsize": "3.2",
            "arrowsize": "0.24",
            "penwidth": "0.58",
            "minlen": "1",
        }

    requested_format = output_format.lower()
    render_format = (
        "svg"
        if requested_format == "png" and can_convert_svg_to_png()
        else output_format
    )
    diagram = graphviz.Digraph(
        name="nasp_compendium",
        format=render_format,
        engine=selected_layout_engine,
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
    )

    nodes_used: set[str] = {
        str(edge[endpoint])
        for edge in edges
        for endpoint in ("source", "target")
    }

    for node in sorted(nodes_used):
        entity_field = entity_types.get(node)
        fill_color = ENTITY_FILL_COLORS.get(
            entity_field or "", DEFAULT_FILL_COLOR
        )
        border_color = ENTITY_BORDER_COLORS.get(
            entity_field or "", DEFAULT_BORDER_COLOR
        )
        diagram.node(
            node,
            label=format_node_label(node),
            fillcolor=fill_color,
            color=border_color,
            fontname=GRAPH_FONT,
        )

    if compact or annotate_papers:
        _add_compact_leaf_rank_groups(
            diagram,
            _compact_leaf_rank_groups(edges),
        )

    for edge in edges:
        rel = str(edge.get("rel", ""))
        evidence = str(edge.get("evidence_strength", ""))
        source = str(edge["source"])
        target = str(edge["target"])
        color = REL_COLOR.get(rel, DEFAULT_REL_COLOR)
        relation_label = rel.replace("_", " ")
        edge_label = relation_label
        edge_annotation = ""

        if annotate_papers:
            if paper_ids := [
                str(paper_id) for paper_id in edge.get("papers") or []
            ]:
                citations = ", ".join(
                    format_citation(paper_id) for paper_id in paper_ids
                )
                edge_label = f"{relation_label}\n[{citations}]"
                edge_annotation = format_edge_annotation(paper_ids)

        visible_edge_label = "" if compact or annotate_papers else edge_label
        use_backbone_layout = compact or annotate_papers
        edge_constraint = _edge_constraint(
            rel=rel,
            source=source,
            target=target,
            compact=use_backbone_layout,
        )
        edge_weight = _edge_weight(
            rel=rel,
            source=source,
            target=target,
            compact=use_backbone_layout,
        )
        edge_minlen = _edge_minlen(
            rel=rel,
            source=source,
            target=target,
            compact=use_backbone_layout,
        )

        edge_kwargs: dict[str, str] = {
            "label": visible_edge_label,
            "tooltip": edge_label,
            "color": color,
            "fontcolor": color,
            "fontname": GRAPH_FONT,
            "constraint": edge_constraint,
            "arrowhead": REL_ARROWHEAD.get(rel, DEFAULT_ARROWHEAD),
            "weight": edge_weight,
            "minlen": edge_minlen,
            "style": EVIDENCE_STYLES.get(
                evidence,
                DEFAULT_EVIDENCE_STYLE,
            ),
        }
        if annotate_papers and edge_annotation:
            edge_kwargs["xlabel"] = edge_annotation

        diagram.edge(
            source,
            target,
            **edge_kwargs,
        )

    # if compact:
    #     _add_compact_edge_legend(diagram, _highest_degree_node(edges))

    rendered_path = Path(
        diagram.render(filename=str(output_stem), cleanup=True)
    )
    if render_format.lower() == "svg":
        postprocess_svg(rendered_path)
        if requested_format == "png":
            png_path = output_stem.with_suffix(".png")
            convert_svg_to_png(rendered_path, png_path)
            rendered_path.unlink()
            rendered_path = png_path
    print(f"  Wrote {rendered_path}")


def can_convert_svg_to_png() -> bool:
    """Return whether a local SVG converter is available for PNG output."""
    return shutil.which("rsvg-convert") is not None


def convert_svg_to_png(svg_path: Path, png_path: Path) -> None:
    """Convert a post-processed SVG to PNG."""
    subprocess.run(
        [
            "rsvg-convert",
            "--format",
            "png",
            "--output",
            str(png_path),
            str(svg_path),
        ],
        check=True,
    )


def postprocess_svg(
    svg_path: Path,
    dash_patterns: dict[str, str] | None = None,
) -> None:
    """Post-process Graphviz SVG output for deterministic browser/raster
    style.
    """
    if dash_patterns is None:
        dash_patterns = {
            'stroke-dasharray="5,2"': 'stroke-dasharray="2,1.2"',
            'stroke-dasharray="1,5"': 'stroke-dasharray="1,2"',
        }

    text = svg_path.read_text()
    text = text.replace(
        'font-family="Helvetica,sans-Serif"',
        f'font-family="{SVG_FONT_FAMILY}"',
    )
    text = text.replace(
        'font-family="sans-Serif"',
        f'font-family="{SVG_FONT_FAMILY}"',
    )
    for original, replacement in dash_patterns.items():
        text = text.replace(original, replacement)
    svg_path.write_text(text)


def trace(compendium: Compendium, query: str) -> None:
    """Print every edge connected to `query` as a textual mechanism listing.

    Args:
      compendium: The loaded compendium.
      query: Entity name (matched case-insensitively against edge source and
        target).
    """
    query_lower = query.lower()
    matched = [
        edge
        for edge in compendium.edges
        if query_lower in str(edge.get("source", "")).lower()
        or query_lower in str(edge.get("target", "")).lower()
    ]

    if not matched:
        print(f"\n  No edges involving '{query}'.\n")
        return

    print(f"\n  Edges involving '{query}' ({len(matched)}):\n")
    for edge in matched:
        papers_str = ", ".join(edge.get("papers") or [])
        print(
            f"    {edge['source']} --[{edge.get('rel', '')}]--> "
            f"{edge['target']}  ({papers_str})"
        )
        if edge.get("context"):
            print(f"      {edge['context']}")
        if edge.get("support"):
            print(f"      support: {edge['support']}")
    print()

"""Render NASP compendium records as Mermaid flowcharts."""

from __future__ import annotations

from pathlib import Path

from nasp_compendium.style import DEFAULT_ARROWHEAD
from nasp_compendium.style import DEFAULT_BORDER_COLOR
from nasp_compendium.style import DEFAULT_EVIDENCE_STYLE
from nasp_compendium.style import DEFAULT_FILL_COLOR
from nasp_compendium.style import DEFAULT_REL_COLOR
from nasp_compendium.style import ENTITY_BORDER_COLORS
from nasp_compendium.style import ENTITY_FILL_COLORS
from nasp_compendium.style import EVIDENCE_STYLES
from nasp_compendium.style import REL_ARROWHEAD
from nasp_compendium.style import REL_COLOR
from nasp_compendium.summarize_compendium import Compendium
from nasp_compendium.summarize_compendium import aggregate_duplicate_edges
from nasp_compendium.summarize_compendium import format_node_label
from nasp_compendium.summarize_compendium import node_entity_types
from nasp_compendium.summarize_compendium import parse_md


MERMAID_ARROW_BY_GRAPHVIZ: dict[str, str] = {
    "normal": "-->",
    "tee": "--x",
    "odot": "--o",
    "none": "---",
    "diamond": "-->",
}
MERMAID_DASH_BY_EVIDENCE: dict[str, str | None] = {
    "solid": None,
    "dashed": "5 3",
    "dotted": "2 3",
}


def render_mermaid(
    compendium: Compendium,
    *,
    rankdir: str = "LR",
    aggregate_edges: bool = True,
) -> str:
    """Render `compendium` as deterministic Mermaid flowchart source.

    Graphviz tee and open-circle arrowheads are represented by Mermaid cross
    and circle endings. Diamond endings fall back to a normal arrow because
    Mermaid flowcharts do not provide a diamond edge ending.

    Args:
      compendium: Compendium records to render.
      rankdir: Mermaid flow direction ("LR" or "TB").
      aggregate_edges: Whether to merge duplicate source-target-rel edges.

    Returns:
      Complete Mermaid source ending with a newline.

    Raises:
      ValueError: If `rankdir` is unsupported.
    """
    if rankdir not in {"LR", "TB"}:
        raise ValueError(
            f'Unsupported Mermaid rank direction: "{rankdir}". '
            'Choose "LR" or "TB".'
        )

    edges = (
        aggregate_duplicate_edges(compendium.edges)
        if aggregate_edges
        else compendium.edges
    )
    nodes = sorted(
        {
            str(edge[endpoint])
            for edge in edges
            for endpoint in ("source", "target")
        }
    )
    node_ids = {node: f"n{index}" for index, node in enumerate(nodes)}
    entity_types = node_entity_types(compendium)

    lines = [
        "---",
        "config:",
        "  fontFamily: Arial",
        "  theme: base",
        (
            '  themeCSS: ".nodeLabel,.nodeLabel *,.edgeLabel,.edgeLabel *'
            '{font-family:Arial!important;font-size:5pt!important;}"'
        ),
        "  flowchart:",
        "    curve: basis",
        "    nodeSpacing: 24",
        "    rankSpacing: 36",
        "  themeVariables:",
        "    fontFamily: Arial",
        "    fontSize: 5pt",
        "---",
        f"flowchart {rankdir}",
    ]

    for node in nodes:
        entity_type = entity_types.get(node, "default")
        label = _escape_mermaid_label(format_node_label(node))
        lines.append(f'  {node_ids[node]}["{label}"]:::{entity_type}')

    link_styles: list[str] = []
    for index, edge in enumerate(edges):
        source = str(edge["source"])
        target = str(edge["target"])
        relationship = str(edge.get("rel", ""))
        evidence = str(edge.get("evidence_strength", ""))
        papers = ", ".join(str(paper) for paper in edge.get("papers") or [])
        comment = f"{relationship}; {evidence}"
        if papers:
            comment += f"; {papers}"
        lines.append(f"  %% {comment}")
        relationship_label = _escape_mermaid_label(
            relationship.replace("_", " ")
        )
        arrow = _mermaid_arrow(relationship)
        link = (
            f"-- {relationship_label} {arrow}" if relationship_label else arrow
        )
        lines.append(f"  {node_ids[source]} {link} {node_ids[target]}")
        link_styles.append(_mermaid_link_style(index, relationship, evidence))

    lines.append("")
    lines.extend(_mermaid_class_definitions())
    lines.extend(link_styles)
    lines.append("")
    return "\n".join(lines)


def write_mermaid_graphs(
    compendium_path: Path,
    output_dir: Path,
    *,
    rankdir: str = "LR",
    aggregate_edges: bool = True,
    combined_name: str = "all_literature_graph.mermaid",
) -> tuple[Path, ...]:
    """Write combined and per-file Mermaid graphs.

    Args:
      compendium_path: Directory containing compendium Markdown files.
      output_dir: Directory receiving generated `.mermaid` files.
      rankdir: Mermaid flow direction ("LR" or "TB").
      aggregate_edges: Whether to merge duplicate source-target-rel edges.
      combined_name: Filename for the combined graph.

    Returns:
      Generated paths, with the combined graph first.

    Raises:
      FileNotFoundError: If `compendium_path` is missing or has no Markdown
        files.
      ValueError: If multiple inputs would produce the same output name.
    """
    if not compendium_path.exists() or not compendium_path.is_dir():
        raise FileNotFoundError(
            f"Compendium directory not found: {compendium_path}"
        )
    input_paths = sorted(compendium_path.glob("*.md"))
    if not input_paths:
        raise FileNotFoundError(
            f"No compendium Markdown files found in: {compendium_path}"
        )

    output_names = [_mermaid_output_name(path) for path in input_paths]
    if len(set(output_names)) != len(output_names):
        raise ValueError("Compendium filenames produce duplicate graph names.")

    output_dir.mkdir(parents=True, exist_ok=True)
    combined = Compendium.from_dir(compendium_path, include_gold=True)
    combined_path = output_dir / combined_name
    combined_path.write_text(
        render_mermaid(
            combined,
            rankdir=rankdir,
            aggregate_edges=aggregate_edges,
        )
    )
    generated_paths = [combined_path]

    for input_path, output_name in zip(
        input_paths,
        output_names,
        strict=True,
    ):
        papers, edges = parse_md(input_path)
        output_path = output_dir / output_name
        output_path.write_text(
            render_mermaid(
                Compendium(papers=papers, edges=edges),
                rankdir=rankdir,
                aggregate_edges=aggregate_edges,
            )
        )
        generated_paths.append(output_path)

    return tuple(generated_paths)


def _escape_mermaid_label(label: str) -> str:
    """Escape characters with special meaning in Mermaid labels."""
    return (
        label.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", " ")
    )


def _mermaid_arrow(relationship: str) -> str:
    """Return the closest Mermaid arrow for `relationship`."""
    graphviz_arrow = REL_ARROWHEAD.get(relationship, DEFAULT_ARROWHEAD)
    return MERMAID_ARROW_BY_GRAPHVIZ.get(graphviz_arrow, "-->")


def _mermaid_link_style(
    index: int,
    relationship: str,
    evidence: str,
) -> str:
    """Return one deterministic Mermaid link-style statement."""
    color = REL_COLOR.get(relationship, DEFAULT_REL_COLOR)
    evidence_style = EVIDENCE_STYLES.get(evidence, DEFAULT_EVIDENCE_STYLE)
    attributes = [
        f"stroke:{color}",
        "stroke-width:1px",
    ]
    if dash_pattern := MERMAID_DASH_BY_EVIDENCE.get(evidence_style):
        attributes.append(f"stroke-dasharray:{dash_pattern}")
    return f"  linkStyle {index} {','.join(attributes)};"


def _mermaid_class_definitions() -> list[str]:
    """Return Mermaid node classes matching Graphviz entity colors."""
    class_names = sorted(set(ENTITY_FILL_COLORS) | set(ENTITY_BORDER_COLORS))
    lines = [
        _mermaid_class_definition(
            "default",
            DEFAULT_FILL_COLOR,
            DEFAULT_BORDER_COLOR,
        )
    ]
    lines.extend(
        _mermaid_class_definition(
            class_name,
            ENTITY_FILL_COLORS.get(class_name, DEFAULT_FILL_COLOR),
            ENTITY_BORDER_COLORS.get(class_name, DEFAULT_BORDER_COLOR),
        )
        for class_name in class_names
    )
    return lines


def _mermaid_class_definition(
    class_name: str,
    fill_color: str,
    border_color: str,
) -> str:
    """Return one Mermaid node class definition."""
    return (
        f"  classDef {class_name} fill:{fill_color},stroke:{border_color},"
        "color:#111111,font-family:Arial,font-size:5pt;"
    )


def _mermaid_output_name(compendium_path: Path) -> str:
    """Return the Mermaid filename corresponding to a compendium file."""
    stem = compendium_path.name.removesuffix(".md")
    return f"{stem}.mermaid"

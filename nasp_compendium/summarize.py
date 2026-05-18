"""Render the NASP mechanistic compendium as a pathway map."""

from __future__ import annotations

import argparse
import dataclasses
import sys
from pathlib import Path
from typing import Any

import graphviz  # type: ignore
import yaml  # type: ignore


COMPENDIUM_DIR: Path = Path(__file__).parent / "compendium"

ENTITY_FIELDS: tuple[str, ...] = (
    "genes",
    "pathways",
    "cell_types",
    "mechanisms",
    "model_systems",
    "evidence_type",
)

ENTITY_FILL_COLORS: dict[str, str] = {
    "genes": "#DCE6F2",
    "pathways": "#FCE4D6",
    "mechanisms": "#E2EFDA",
    "cell_types": "#FADBD8",
    "model_systems": "#E8DAEF",
    "evidence_type": "#EAEDED",
}

ENTITY_BORDER_COLORS: dict[str, str] = {
    "genes": "#4C72B0",
    "pathways": "#DD8452",
    "mechanisms": "#55A868",
    "cell_types": "#C44E52",
    "model_systems": "#8172B3",
    "evidence_type": "#937860",
}

DEFAULT_FILL_COLOR: str = "#F2F2F2"
DEFAULT_BORDER_COLOR: str = "#666666"

REL_ARROWHEAD: dict[str, str] = {
    "suppresses": "tee",
    "inhibits": "tee",
    "activates": "normal",
    "drives": "normal",
    "required_for": "normal",
    "produces": "normal",
    "causes": "normal",
    "binds_recruits": "normal",
    "correlates": "odot",
    "induces": "normal",
    "downregulates": "tee",
    "upregulates": "normal",
    "retains": "normal",
    "contains": "diamond",
    "negatively_correlates": "odot",
    "does_not_correlate": "none",
    "does_not_drive": "none",
}

REL_COLOR: dict[str, str] = {
    "suppresses": "#C44E52",
    "inhibits": "#C44E52",
    "activates": "#55A868",
    "drives": "#55A868",
    "required_for": "#4C72B0",
    "produces": "#4C72B0",
    "causes": "#333333",
    "binds_recruits": "#8172B3",
    "correlates": "#999999",
    "induces": "#55A868",
    "downregulates": "#C44E52",
    "upregulates": "#55A868",
    "retains": "#55A868",
    "contains": "#8172B3",
    "negatively_correlates": "#C44E52",
    "does_not_correlate": "#CCCCCC",
    "does_not_drive": "#CCCCCC",
}

EVIDENCE_STYLES: dict[str, str] = {
    "direct_measured": "solid",
    "perturbation_supported": "solid",
    "canonical_inferred": "dashed",
    "strong_correlative": "dotted",
    "weak_correlative": "dotted",
}

DEFAULT_REL_COLOR: str = "#555555"
DEFAULT_ARROWHEAD: str = "normal"
DEFAULT_EVIDENCE_STYLE: str = "solid"


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
            file_papers, file_edges = parse_md(md_path)
            papers |= file_papers
            edges.extend(file_edges)

        return cls(papers=papers, edges=edges)


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


def render(
    compendium: Compendium,
    output_stem: Path,
    output_format: str = "png",
    rankdir: str = "LR",
    annotate_papers: bool = False,
) -> None:
    """Render the compendium as a directed pathway diagram via Graphviz.

    Nodes are styled by the entity field in which they are declared. Edges and
    lines are styled by relationship type and evidence strength, respectively.

    Args:
      compendium: The loaded compendium.
      output_stem: Stem for the output file.
      output_format: Graphviz output format
      rankdir: Graphviz rank direction. "LR" left-to-right; "TB" top-to-bottom.
      annotate_papers: If True, append a short paper citation to each edge
        label.
    """
    if not compendium.edges:
        print("  No edges recorded. Add an 'edges:' block to a paper file.")
        return

    entity_types = node_entity_types(compendium)
    diagram = graphviz.Digraph(
        name="nasp_compendium",
        format=output_format,
        graph_attr={
            "rankdir": rankdir,
            "splines": "spline",
            "overlap": "false",
            "nodesep": "0.4",
            "ranksep": "0.8",
            "fontname": "Helvetica",
            "fontnames": "ps",
            "dpi": "450",
        },
        node_attr={
            "shape": "box",
            "style": "rounded,filled",
            "fontname": "Helvetica",
            "fontsize": "10",
            "penwidth": "1.25",
        },
        edge_attr={
            "fontname": "Helvetica",
            "fontsize": "10",
            "penwidth": "1.25",
        },
    )

    nodes_used: set[str] = {
        str(edge[endpoint])
        for edge in compendium.edges
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
            label=node.replace("_", " "),
            fillcolor=fill_color,
            color=border_color,
        )

    for edge in compendium.edges:
        rel = str(edge.get("rel", ""))
        evidence = str(edge.get("evidence_strength", ""))
        color = REL_COLOR.get(rel, DEFAULT_REL_COLOR)
        edge_label = rel.replace("_", " ")
        if annotate_papers:
            if paper_ids := edge.get("papers") or []:
                citations = "; ".join(format_citation(pid) for pid in paper_ids)
                edge_label = f"{edge_label}\n[{citations}]"
        diagram.edge(
            str(edge["source"]),
            str(edge["target"]),
            label=edge_label,
            color=color,
            fontcolor=color,
            arrowhead=REL_ARROWHEAD.get(rel, DEFAULT_ARROWHEAD),
            style=EVIDENCE_STYLES.get(evidence, DEFAULT_EVIDENCE_STYLE),
        )

    rendered_path = diagram.render(filename=str(output_stem), cleanup=True)
    print(f"  Wrote {rendered_path}")


def trace(compendium: Compendium, query: str) -> None:
    """Print every edge connected to `query` as a textual mechanism listing.

    Args:
      compendium: The loaded compendium.
      query: Entity name. Matched case-insensitively against edge source and
       target.
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


def _parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="NASP compendium CLI")
    parser.add_argument("command", choices=["render", "trace"])
    parser.add_argument(
        "query",
        nargs="?",
        default=None,
        help="Entity name (for 'trace' command)",
    )
    parser.add_argument(
        "--out",
        dest="output_stem",
        default="nasp_pathway_map",
        help="Output filename stem for 'render' (extension is appended)",
    )
    parser.add_argument(
        "--format",
        dest="output_format",
        default="png",
        help="Graphviz output format (svg, pdf, png)",
    )
    parser.add_argument(
        "--rankdir",
        default="LR",
        choices=("LR", "TB"),
        help="Layout direction for 'render' (LR=left-right, TB=top-bottom)",
    )
    parser.add_argument(
        "--annotate-papers",
        dest="annotate_papers",
        action="store_true",
        help="Annotate each edge with a short paper citation (e.g. 'Dou 2017')",
    )
    parser.add_argument(
        "--dir",
        dest="directory",
        default=None,
        help=f"Compendium directory (default: {COMPENDIUM_DIR})",
    )
    return parser.parse_args()


def main() -> None:
    """Parse CLI arguments and dispatch to the requested command."""
    parser = _parse_args()
    args = parser.parse_args()

    directory = Path(args.directory) if args.directory else COMPENDIUM_DIR
    try:
        compendium = Compendium.from_dir(directory)
    except FileNotFoundError as exc:
        print(f"  {exc}")
        sys.exit(1)

    if args.command == "render":
        render(
            compendium,
            output_stem=Path(args.output_stem).with_suffix(""),
            output_format=args.output_format,
            rankdir=args.rankdir,
            annotate_papers=args.annotate_papers,
        )
    elif args.command == "trace":
        if not args.query:
            print("  Usage: python nasp.py trace <entity>")
            sys.exit(1)
        trace(compendium, args.query)


if __name__ == "__main__":
    main()

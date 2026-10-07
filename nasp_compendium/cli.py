"""Command-line entry points for the NASP compendium."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Mapping
from pathlib import Path

import graphviz  # type: ignore

from nasp_compendium import diff_compendium
from nasp_compendium import paper_review
from nasp_compendium import paper_sources
from nasp_compendium import regenerate as regenerate_module
from nasp_compendium import render_docs as render_docs_module
from nasp_compendium import review_packet
from nasp_compendium import score_compendium
from nasp_compendium import summarize_compendium
from nasp_compendium import validate_compendium
from nasp_compendium.render_mermaid import write_mermaid_graphs


COMPENDIUM_DIR: Path = (
    Path(__file__).resolve().parent.parent / "docs" / "compendium"
)


def _build_parser(
    handlers: Mapping[str, Callable[[argparse.Namespace], None]],
) -> argparse.ArgumentParser:
    """Build the top-level parser with one subparser per subcommand."""
    parser = argparse.ArgumentParser(
        prog="compendium",
        description="NASP knowledge compendium CLI.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    _add_render_graph_parser(subparsers)
    _add_render_paper_graphs_parser(subparsers)
    _add_render_mermaid_graphs_parser(subparsers)
    _add_render_docs_parser(subparsers)
    _add_trace_parser(subparsers)
    _add_validate_parser(subparsers)
    _add_diff_parser(subparsers)
    _add_regenerate_parser(subparsers)
    _add_review_packet_parser(subparsers)
    _add_score_parser(subparsers)
    _add_extraction_parsers(subparsers)
    for name, subparser in subparsers.choices.items():
        subparser.set_defaults(func=handlers[name])

    return parser


def _add_extraction_parsers(subparsers: argparse._SubParsersAction) -> None:
    """Expose the local source, figure and exact-draft review workflow."""
    prepare = subparsers.add_parser(
        "prepare_paper",
        help="Index a PDF and supplements into a new local extraction run.",
    )
    prepare.add_argument("pdf", type=Path)
    prepare.add_argument("--run-dir", type=Path, required=True)
    prepare.add_argument("--paper-id", required=True)
    prepare.add_argument("--supplement", type=Path, action="append", default=[])
    page = subparsers.add_parser(
        "render_page", help="Render a one-based PDF page to inspect a figure."
    )
    page.add_argument("pdf", type=Path)
    page.add_argument("page", type=int)
    page.add_argument("--out", type=Path, required=True)
    review = subparsers.add_parser(
        "review_paper",
        help="Validate, freeze and visualize a source-linked draft.",
    )
    review.add_argument("run_dir", type=Path)
    review.add_argument("draft", type=Path)
    review.add_argument("--compendium-path", type=Path, default=COMPENDIUM_DIR)
    review.add_argument(
        "--supplements",
        choices=("complete", "missing", "not_applicable"),
        required=True,
    )
    review.add_argument("--notes-file", type=Path)
    review.add_argument("--no-findings", action="store_true")
    review.add_argument("--model", default="unrecorded")


def _run_prepare_paper(args: argparse.Namespace) -> None:
    """Prepare a new run and hash the current extraction instructions."""
    agent_dir = Path(__file__).resolve().parent.parent / "agent"
    print(
        paper_sources.prepare_paper(
            args.pdf,
            args.run_dir,
            supplements=args.supplement,
            paper_id=args.paper_id,
            instruction_paths=[
                agent_dir / "prompts" / "curate_paper.md",
                agent_dir / "extraction_contract.md",
                agent_dir / "vocabulary.yaml",
            ],
        )
    )


def _run_render_page(args: argparse.Namespace) -> None:
    """Write a page image without overwriting an earlier inspection."""
    print(paper_sources.render_source_page(args.pdf, args.page, args.out))


def _run_review_paper(args: argparse.Namespace) -> None:
    """Freeze an exact draft and its evidence for scientific review."""
    print(
        paper_review.review_paper(
            args.run_dir,
            args.draft,
            compendium_dir=args.compendium_path,
            supplement_coverage=args.supplements,
            notes=args.notes_file.read_text() if args.notes_file else "",
            no_findings=args.no_findings,
            model=args.model,
        )
    )


def _add_render_graph_parser(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the `render_graph` subcommand."""
    render_graph_parser = subparsers.add_parser(
        "render_graph",
        help="Render all compendium files together as one pathway diagram.",
    )
    render_graph_parser.add_argument(
        "--compendium-path",
        dest="compendium_path",
        default=None,
        type=Path,
        help=(
            "Path to the directory of per-paper compendium Markdown files "
            f"(default: {COMPENDIUM_DIR}; excludes .gold.md references)."
        ),
    )
    render_graph_parser.add_argument(
        "--out",
        "--output",
        dest="output_stem",
        default="nasp_pathway_map",
        type=Path,
        help=(
            "Output filename or stem. If an extension is included, it is used "
            "as the Graphviz format unless --format is also supplied."
        ),
    )
    render_graph_parser.add_argument(
        "--format",
        dest="output_format",
        default=None,
        help="Graphviz output format (svg, pdf, png).",
    )
    _add_graph_layout_arguments(render_graph_parser)
    render_graph_parser.add_argument(
        "--paper",
        "--papers",
        dest="paper_ids",
        action="append",
        default=None,
        help=(
            "Render only the specified paper id(s). May be repeated or "
            "comma-separated, e.g. --paper Dou_nature_2017,DeCecco_nature_2019."
        ),
    )


def _add_render_paper_graphs_parser(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the `render_paper_graphs` subcommand."""
    parser = subparsers.add_parser(
        "render_paper_graphs",
        help="Render one pathway diagram per compendium Markdown file.",
    )
    parser.add_argument(
        "--compendium-path",
        dest="compendium_path",
        default=None,
        type=Path,
        help=(
            "Path to the directory of per-paper compendium Markdown files "
            f"(default: {COMPENDIUM_DIR}; excludes .gold.md references)."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default=Path("compendium_graphs"),
        type=Path,
        help=("Directory for per-paper figures (default: compendium_graphs)."),
    )
    parser.add_argument(
        "--format",
        dest="output_format",
        default="png",
        choices=("svg", "pdf", "png"),
        help="Graphviz output format (default: png).",
    )
    _add_graph_layout_arguments(parser)


def _add_graph_layout_arguments(parser: argparse.ArgumentParser) -> None:
    """Add options shared by combined and per-paper graph rendering."""
    parser.add_argument(
        "--rankdir",
        default="LR",
        choices=("LR", "TB"),
        help="Layout direction (TB=top-bottom, LR=left-right).",
    )
    parser.add_argument(
        "--layout-engine",
        default=None,
        choices=("dot", "fdp", "sfdp", "neato"),
        help=(
            "Graphviz layout engine. Defaults to dot. Use fdp, sfdp, or "
            "neato only for exploratory network-style layouts."
        ),
    )
    parser.add_argument(
        "--annotate-papers",
        dest="annotate_papers",
        action="store_true",
        help="Annotate each edge with a short paper citation.",
    )
    parser.add_argument(
        "--exclude-rel",
        "--exclude-edge-type",
        dest="excluded_rels",
        action="append",
        default=None,
        help=(
            "Omit edges with the specified relationship(s). May be repeated or "
            "comma-separated; spaces and hyphens are normalized to underscores."
        ),
    )
    parser.add_argument(
        "--no-aggregate-edges",
        dest="aggregate_edges",
        action="store_false",
        default=True,
        help="Render duplicate source-target-rel edges separately.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help=(
            "Use compact pathway-map mode: left-to-right layout, hidden edge "
            "labels, and a visual edge legend."
        ),
    )


def _add_render_mermaid_graphs_parser(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the `render_mermaid_graphs` subcommand."""
    graph_dir = (
        Path(__file__).resolve().parent.parent / "docs/compendium_graphs"
    )
    parser = subparsers.add_parser(
        "render_mermaid_graphs",
        help="Write combined and per-paper Mermaid flowchart sources.",
    )
    parser.add_argument(
        "--compendium-path",
        default=None,
        type=Path,
        help=(
            "Path to the directory of per-paper compendium Markdown files "
            f"(default: {COMPENDIUM_DIR}; excludes .gold.md references)."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default=graph_dir,
        type=Path,
        help=(f"Directory for generated Mermaid files (default: {graph_dir})."),
    )
    parser.add_argument(
        "--rankdir",
        default="LR",
        choices=("LR", "TB"),
        help="Flow direction (TB=top-bottom, LR=left-right).",
    )
    parser.add_argument(
        "--no-aggregate-edges",
        dest="aggregate_edges",
        action="store_false",
        default=True,
        help="Write duplicate source-target-relationship edges separately.",
    )


def _add_render_docs_parser(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the `render_docs` subcommand."""
    render_docs_parser = subparsers.add_parser(
        "render_docs",
        help="Render the marker-gene TSV as panel-grouped Markdown.",
    )
    render_docs_parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to the marker-gene TSV source file.",
    )
    render_docs_parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory to write the rendered Markdown files into.",
    )


def _add_trace_parser(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the `trace` subcommand."""
    trace_parser = subparsers.add_parser(
        "trace",
        help="Print every edge touching a queried entity.",
    )
    trace_parser.add_argument(
        "query", help="Entity name (matched case-insensitively)."
    )
    trace_parser.add_argument(
        "--dir",
        "--directory",
        dest="directory",
        default=None,
        type=Path,
        help=(
            "Compendium directory of per-paper Markdown files "
            f"(default: {COMPENDIUM_DIR})."
        ),
    )


def _add_validate_parser(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the `validate` subcommand."""
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate compendium YAML schema and curation conventions.",
    )
    validate_parser.add_argument(
        "--dir",
        "--directory",
        dest="directory",
        default=None,
        type=Path,
        help=(
            "Compendium directory of per-paper Markdown files "
            f"(default: {COMPENDIUM_DIR})."
        ),
    )
    validate_parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit nonzero when warnings are found.",
    )


def _add_diff_parser(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the `diff` subcommand."""
    diff_parser = subparsers.add_parser(
        "diff",
        help="Print a structured diff between two compendium states.",
    )
    diff_parser.add_argument(
        "old_path",
        type=Path,
        help="Old compendium directory or single compendium Markdown file.",
    )
    diff_parser.add_argument(
        "new_path",
        type=Path,
        help="New compendium directory or single compendium Markdown file.",
    )
    diff_parser.add_argument(
        "--format",
        choices=("text", "markdown"),
        default="text",
        help="Output format.",
    )


def _add_regenerate_parser(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the `regenerate` subcommand."""
    marker_docs_dir = (
        Path(__file__).resolve().parent.parent / "docs/marker_genes"
    )
    regenerate_parser = subparsers.add_parser(
        "regenerate",
        help="Render marker-gene docs and module figures in one pass.",
    )
    regenerate_parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to the marker-gene TSV source file.",
    )
    regenerate_parser.add_argument(
        "--docs-dir",
        default=marker_docs_dir,
        type=Path,
        help="Directory to write docs and assets into "
        f"(default: {marker_docs_dir}).",
    )


def _add_review_packet_parser(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the `review_packet` subcommand."""
    review_parser = subparsers.add_parser(
        "review_packet",
        help="Write a human-review packet for a draft file or directory.",
    )
    review_parser.add_argument(
        "input_path",
        type=Path,
        help="Draft file or directory to review.",
    )
    review_parser.add_argument(
        "--out",
        "--output",
        dest="output_path",
        required=True,
        type=Path,
        help="Markdown file to write.",
    )
    review_parser.add_argument(
        "--gate",
        action="store_true",
        help="Exit nonzero if the review packet has pre-freeze blockers.",
    )


def _add_score_parser(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the `score` subcommand."""
    score_parser = subparsers.add_parser(
        "score",
        help="Score draft curation files against gold compendium files.",
    )
    score_parser.add_argument(
        "--draft",
        dest="draft_path",
        required=True,
        type=Path,
        help="Draft file or directory to score.",
    )
    score_parser.add_argument(
        "--gold",
        dest="gold_path",
        required=True,
        type=Path,
        help="Gold file or directory to compare against.",
    )
    score_parser.add_argument(
        "--draft-glob",
        default="*.md",
        help="Glob used when --draft is a directory.",
    )
    score_parser.add_argument(
        "--gold-glob",
        default="*.gold.md",
        help="Glob used when --gold is a directory.",
    )
    score_parser.add_argument(
        "--drop-gold-defects",
        dest="drop_gold_defects",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Exclude gold edges flagged with score_exclude/status: excluded "
            "(default: on; use --no-drop-gold-defects to score them)."
        ),
    )
    score_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    score_parser.add_argument(
        "--out",
        "--output",
        dest="output_path",
        type=Path,
        help="Optional file to write the score report.",
    )


def _run_regenerate(args: argparse.Namespace) -> None:
    """Dispatch the `regenerate` subcommand."""
    regenerate_module.regenerate(input_path=args.input, docs_dir=args.docs_dir)


def _load_compendium(
    directory: Path | None,
    *,
    include_gold: bool = False,
) -> summarize_compendium.Compendium:
    """Load the compendium from `directory` or the package default."""
    resolved = directory or COMPENDIUM_DIR
    return summarize_compendium.Compendium.from_dir(
        resolved,
        include_gold=include_gold,
    )


def _run_render_graph(args: argparse.Namespace) -> None:
    """Dispatch the `render_graph` subcommand."""
    compendium = _load_compendium(args.compendium_path)
    compendium = compendium.filtered(
        paper_ids=_parse_csv_values(args.paper_ids),
        excluded_rels=_parse_rel_values(args.excluded_rels),
    )
    output_stem, output_format = _resolve_graph_output(
        args.output_stem,
        args.output_format,
    )
    summarize_compendium.render(
        compendium,
        output_stem=output_stem,
        output_format=output_format,
        rankdir=args.rankdir,
        layout_engine=args.layout_engine,
        annotate_papers=args.annotate_papers,
        aggregate_edges=args.aggregate_edges,
        compact=args.compact,
    )


def _run_render_paper_graphs(args: argparse.Namespace) -> None:
    """Dispatch the `render_paper_graphs` subcommand."""
    compendium_path = args.compendium_path or COMPENDIUM_DIR
    if not compendium_path.exists() or not compendium_path.is_dir():
        raise FileNotFoundError(
            f"Compendium directory not found: {compendium_path}"
        )
    compendium_paths = [
        path
        for path in sorted(compendium_path.glob("*.md"))
        if not path.name.endswith(".gold.md")
    ]
    if not compendium_paths:
        raise FileNotFoundError(
            f"No compendium Markdown files found in: {compendium_path}"
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for compendium_path in compendium_paths:
        papers, edges = summarize_compendium.parse_md(compendium_path)
        compendium = summarize_compendium.Compendium(
            papers=papers,
            edges=edges,
        ).filtered(
            excluded_rels=_parse_rel_values(args.excluded_rels),
        )
        output_name = compendium_path.name.removesuffix(".md")
        summarize_compendium.render(
            compendium,
            output_stem=args.output_dir / output_name,
            output_format=args.output_format,
            rankdir=args.rankdir,
            layout_engine=args.layout_engine,
            annotate_papers=args.annotate_papers,
            aggregate_edges=args.aggregate_edges,
            compact=args.compact,
        )

    print(
        f"  Rendered {len(compendium_paths)} per-paper graph(s) "
        f"in {args.output_dir}"
    )


def _run_render_mermaid_graphs(args: argparse.Namespace) -> None:
    """Dispatch the `render_mermaid_graphs` subcommand."""
    generated_paths = write_mermaid_graphs(
        compendium_path=args.compendium_path or COMPENDIUM_DIR,
        output_dir=args.output_dir,
        rankdir=args.rankdir,
        aggregate_edges=args.aggregate_edges,
    )
    print(
        f"  Wrote {len(generated_paths)} Mermaid graph(s) to {args.output_dir}"
    )


def _run_render_docs(args: argparse.Namespace) -> None:
    """Dispatch the `render_docs` subcommand."""
    render_docs_module.render_docs(
        input_path=args.input, output_dir=args.output_dir
    )


def _run_trace(args: argparse.Namespace) -> None:
    """Dispatch the `trace` subcommand."""
    compendium = _load_compendium(args.directory)
    summarize_compendium.trace(compendium, args.query)


def _run_validate(args: argparse.Namespace) -> None:
    """Dispatch the `validate` subcommand."""
    directory = args.directory or COMPENDIUM_DIR
    result = validate_compendium.validate_directory(directory)
    validate_compendium.print_result(result, strict=args.strict)
    if result.exit_code(strict=args.strict):
        raise ValueError("Compendium validation blocked this operation.")


def _run_diff(args: argparse.Namespace) -> None:
    """Dispatch the `diff` subcommand."""
    diff = diff_compendium.diff_paths(args.old_path, args.new_path)
    print(diff_compendium.format_diff(diff, output_format=args.format))


def _run_review_packet(args: argparse.Namespace) -> None:
    """Dispatch the `review_packet` subcommand."""
    output_path = review_packet.write_review_packet(
        input_path=args.input_path,
        output_path=args.output_path,
    )
    print(f"  Wrote {output_path}")
    if args.gate:
        if blockers := review_packet.gate_blockers(args.input_path):
            print(f"  Pre-freeze gate blocked by {len(blockers)} issue(s).")
            for blocker in blockers[:20]:
                print(f"    - {blocker}")
            raise ValueError("Draft review blocked; fix the reported errors.")


def _run_score(args: argparse.Namespace) -> None:
    """Dispatch the `score` subcommand."""
    report = score_compendium.score_paths(
        draft_path=args.draft_path,
        gold_path=args.gold_path,
        draft_glob=args.draft_glob,
        gold_glob=args.gold_glob,
        drop_gold_defects=args.drop_gold_defects,
    )
    formatted = score_compendium.format_score_report(
        report,
        output_format=args.format,
    )
    if args.output_path is not None:
        score_compendium.write_score_report(
            report,
            output_path=args.output_path,
            output_format=args.format,
        )
        print(f"  Wrote {args.output_path}")
    else:
        print(formatted, end="")


def _print_graphviz_missing_executable() -> None:
    """Print Graphviz installation guidance after a render failure."""
    print(
        "  Graphviz 'dot' executable not found on PATH.\n"
        "  Install the Graphviz binary, then retry:\n"
        "    macOS:  brew install graphviz\n"
        "    Linux:  sudo apt-get install graphviz\n"
        "    conda:  conda install -c conda-forge graphviz"
    )


def _parse_csv_values(values: list[str] | None) -> set[str] | None:
    """Parse repeated comma-separated CLI values into a set."""
    if not values:
        return None
    parsed = {
        item.strip()
        for value in values
        for item in value.split(",")
        if item.strip()
    }
    return parsed or None


def _parse_rel_values(values: list[str] | None) -> set[str] | None:
    """Parse relationship CLI values with light user-input normalization."""
    parsed = _parse_csv_values(values)
    if parsed is None:
        return None
    return {
        value.strip().lower().replace(" ", "_").replace("-", "_")
        for value in parsed
    }


def _resolve_graph_output(
    output_path: Path,
    output_format: str | None,
) -> tuple[Path, str]:
    """Resolve Graphviz output stem/format from CLI filename options."""
    if output_path.suffix:
        suffix_format = output_path.suffix.lstrip(".")
        return output_path.with_suffix(""), output_format or suffix_format
    return output_path, output_format or "png"


def main() -> None:
    """Parse top-level CLI arguments and dispatch to the requested
    subcommand.
    """
    dispatch: dict[str, Callable[[argparse.Namespace], None]] = {
        "render_graph": _run_render_graph,
        "render_paper_graphs": _run_render_paper_graphs,
        "render_mermaid_graphs": _run_render_mermaid_graphs,
        "render_docs": _run_render_docs,
        "trace": _run_trace,
        "validate": _run_validate,
        "diff": _run_diff,
        "regenerate": _run_regenerate,
        "review_packet": _run_review_packet,
        "score": _run_score,
        "prepare_paper": _run_prepare_paper,
        "render_page": _run_render_page,
        "review_paper": _run_review_paper,
    }
    parser = _build_parser(dispatch)
    args = parser.parse_args()
    try:
        args.func(args)
    except graphviz.ExecutableNotFound:
        _print_graphviz_missing_executable()
        sys.exit(1)
    except (FileNotFoundError, FileExistsError, ValueError, ImportError) as exc:
        print(f"  {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()

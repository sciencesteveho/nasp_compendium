"""Freeze a source-linked draft and preview its collective graph change."""

from __future__ import annotations

import html
import json
import re
import tempfile
from pathlib import Path
from typing import Any

import graphviz

from nasp_compendium.diff_compendium import diff_compendia
from nasp_compendium.diff_compendium import format_diff
from nasp_compendium.paper_sources import file_sha256
from nasp_compendium.paper_sources import render_source_page
from nasp_compendium.style import EVIDENCE_STYLES
from nasp_compendium.style import REL_ARROWHEAD
from nasp_compendium.style import REL_COLOR
from nasp_compendium.summarize_compendium import Compendium
from nasp_compendium.summarize_compendium import aggregate_duplicate_edges
from nasp_compendium.summarize_compendium import is_asserted_edge
from nasp_compendium.summarize_compendium import parse_md
from nasp_compendium.validate_compendium import validate_file


def review_paper(
    run_dir: Path,
    draft_path: Path,
    *,
    compendium_dir: Path,
    supplement_coverage: str,
    notes: str,
    no_findings: bool = False,
    model: str = "unrecorded",
) -> Path:
    """Validate and freeze a draft into a new local, interactive review.

    The accepted collection is only read. Repeated reviews create separate
    revisions, each containing the exact draft, manifest, diff and source-page
    images. Missing supplements remain a visible limitation requiring notes.
    A successful structural gate does not certify the scientific claims.

    Args:
      run_dir: Directory created by prepare_paper.
      draft_path: The exact candidate to review.
      compendium_dir: Accepted graph inputs for the proposed integration diff.
      supplement_coverage: complete, missing, or not_applicable after checking.
      notes: Unresolved findings, supplement gaps, or no-findings explanation.
      no_findings: Explicitly accept an empty, explained extraction.
      model: Observable model/settings string; unknown values stay unrecorded.

    Returns:
      Path to the frozen revision's review.html.
    """
    if supplement_coverage not in {"complete", "missing", "not_applicable"}:
        raise ValueError("Inspect supplements and record their coverage first.")
    if (supplement_coverage == "missing" or no_findings) and not notes.strip():
        raise ValueError(
            "Missing supplements or no findings require an explanation."
        )
    manifest = json.loads((run_dir / "run.json").read_text())
    sources = _verified_sources(manifest)
    draft_bytes = draft_path.read_bytes()
    with tempfile.TemporaryDirectory(dir=run_dir) as temporary:
        staging = Path(temporary) / "review"
        staging.mkdir()
        frozen_draft = staging / "draft.md"
        frozen_draft.write_bytes(draft_bytes)
        validation = validate_file(frozen_draft, allow_empty_edges=no_findings)
        if not validation.ok:
            raise ValueError(
                "Draft blocked:\n"
                + "\n".join(issue.message for issue in validation.errors)
            )
        papers, edges = parse_md(frozen_draft)
        if set(papers) != {manifest["paper_id"]}:
            raise ValueError("Draft must contain only the prepared paper ID.")
        if no_findings and edges:
            raise ValueError("A no-findings disposition cannot contain edges.")
        if any(not is_asserted_edge(edge) for edge in edges):
            raise ValueError(
                "Keep evaluation counterexamples in references, "
                "outside extraction drafts."
            )
        candidate = Compendium(papers=papers, edges=edges)
        evidence_links = _prepare_evidence_pages(candidate, sources, staging)
        accepted = Compendium.from_dir(compendium_dir)
        retained = accepted.filtered(
            paper_ids=set(accepted.papers) - set(papers)
        )
        preview = Compendium(
            papers=retained.papers | papers, edges=retained.edges + edges
        )
        diff = format_diff(diff_compendia(accepted, preview))
        (staging / "diff.txt").write_text(diff)
        views = {
            "paper": _graph_view(candidate, evidence_links),
            "collective": _graph_view(preview, evidence_links),
            "accepted": _graph_view(accepted, {}),
        }
        snapshot = dict(manifest)
        snapshot.update(
            {
                "status": "awaiting_scientific_review",
                "draft_sha256": file_sha256(frozen_draft),
                "supplement_coverage": supplement_coverage,
                "notes": notes,
                "disposition": "no_in_scope_findings"
                if no_findings
                else "claims_extracted",
                "model": model,
                "validation_errors": [],
                "validation_warnings": [
                    issue.message for issue in validation.warnings
                ],
                "accepted_inputs": {
                    str(path.resolve()): file_sha256(path)
                    for path in sorted(compendium_dir.glob("*.md"))
                    if not path.name.endswith(".gold.md")
                },
            }
        )
        (staging / "run.json").write_text(json.dumps(snapshot, indent=2) + "\n")
        _write_html(staging / "review.html", views, snapshot, diff)
        revisions = run_dir / "reviews"
        revisions.mkdir(exist_ok=True)
        number = 1
        while (revisions / f"review-{number:04d}").exists():
            number += 1
        destination = revisions / f"review-{number:04d}"
        staging.rename(destination)
    return destination / "review.html"


def _verified_sources(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Reject changed PDFs before attaching evidence to a frozen draft."""
    sources = {source["id"]: source for source in manifest["sources"]}
    if "main" not in sources:
        raise ValueError("Source manifest has no main PDF.")
    for source in sources.values():
        path = Path(source["path"])
        if not path.is_file() or file_sha256(path) != source["sha256"]:
            raise ValueError(
                f"Source changed or missing: {path}. Prepare a new run."
            )
    return sources


def _prepare_evidence_pages(
    candidate: Compendium,
    sources: dict[str, dict[str, Any]],
    output_dir: Path,
) -> dict[tuple[str, str], list[dict[str, str]]]:
    """Resolve explicit PDF page locators and render every cited page once."""
    evidence_links: dict[tuple[str, str], list[dict[str, str]]] = {}
    rendered: set[tuple[str, int]] = set()
    for index, edge in enumerate(candidate.edges, start=1):
        support = edge["support"]
        locators = re.findall(r"\b(main|supplement_\d+) p\.\s*(\d+)\b", support)
        if not locators:
            raise ValueError(
                f"Edge {index} needs a source locator "
                "such as 'main p. 7; Fig. 4h'."
            )
        links = []
        for source_id, page_text in dict.fromkeys(locators):
            page = int(page_text)
            source = sources.get(source_id)
            if source is None or not 1 <= page <= source["pages"]:
                raise ValueError(
                    f"Edge {index} cites unavailable source/page: "
                    f"{source_id} p. {page}."
                )
            relative_path = f"pages/{source_id}-{page:04d}.png"
            if (source_id, page) not in rendered:
                render_source_page(
                    Path(source["path"]), page, output_dir / relative_path
                )
                rendered.add((source_id, page))
            links.append(
                {
                    "label": f"{source_id} p. {page}",
                    "image": relative_path,
                    "pdf": Path(source["path"]).as_uri() + f"#page={page}",
                }
            )
        for paper_id in edge["papers"]:
            evidence_links[(paper_id, support)] = links
    return evidence_links


def _graph_view(
    compendium: Compendium,
    evidence_links: dict[tuple[str, str], list[dict[str, str]]],
) -> dict[str, Any]:
    """Build SVG with stable selectable IDs and all per-paper evidence."""
    edges = aggregate_duplicate_edges(compendium.edges)
    nodes = sorted(
        {edge[endpoint] for edge in edges for endpoint in ("source", "target")}
    )
    node_ids = {node: f"node_{index}" for index, node in enumerate(nodes)}
    graph = graphviz.Digraph(
        graph_attr={
            "rankdir": "LR",
            "bgcolor": "transparent",
            "pad": "0.3",
            "nodesep": "0.35",
            "ranksep": "0.8",
        },
        node_attr={
            "shape": "box",
            "style": "rounded,filled",
            "fillcolor": "#eef4f8",
            "color": "#a0b4c4",
            "fontname": "Arial",
            "fontsize": "12",
        },
        edge_attr={"fontname": "Arial", "fontsize": "10"},
    )
    for node, node_id in node_ids.items():
        graph.node(node, label=node.replace("_", " "), id=node_id)
    for index, edge in enumerate(edges):
        rel = edge["rel"]
        graph.edge(
            edge["source"],
            edge["target"],
            label=rel.replace("_", " "),
            id=f"edge_{index}",
            color=REL_COLOR[rel],
            arrowhead=REL_ARROWHEAD.get(rel, "normal"),
            style=EVIDENCE_STYLES[edge["evidence_strength"]],
        )
        for record in edge["evidence_records"]:
            record["source_links"] = [
                link
                for paper_id in record["papers"]
                for link in evidence_links.get(
                    (paper_id, record.get("support", "")), []
                )
            ]
    svg = (
        graph.pipe(format="svg").decode("utf-8")
        if edges
        else "<p class='empty'>No asserted mechanisms in this view.</p>"
    )
    if edges:
        svg = svg[svg.index("<svg") :]
    return {
        "svg": svg,
        "edges": edges,
        "nodes": node_ids,
        "papers": compendium.papers,
    }


def _write_html(
    path: Path,
    views: dict[str, Any],
    manifest: dict[str, Any],
    diff: str,
) -> None:
    """Embed local assets and escaped data in a standalone review document."""
    asset_dir = Path(__file__).parent / "review_assets"
    template = (asset_dir / "review.html").read_text()
    payload = {"views": views, "manifest": manifest, "diff": diff}
    encoded = (
        json.dumps(payload)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )
    replacements = {
        "{{TITLE}}": html.escape(manifest["paper_id"]),
        "{{DATA}}": encoded,
        "{{CSS}}": (asset_dir / "review.css").read_text(),
        "{{JS}}": (asset_dir / "review.js").read_text(),
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    path.write_text(template, encoding="utf-8")

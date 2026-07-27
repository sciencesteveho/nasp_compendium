"""Build lightweight human-review packets for curated NASP drafts."""

from __future__ import annotations

import collections
import tempfile
from pathlib import Path
from typing import Any

import yaml  # type: ignore

from nasp_compendium import validate_compendium


def build_review_packet(input_path: Path) -> str:
    """Return a Markdown review packet for a draft file or directory.

    Args:
      input_path: Single YAML-in-Markdown draft file or directory containing
        draft files.

    Returns:
      Markdown text summarizing validation, edges, and review hotspots.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Review input not found: {input_path}")

    data_by_path = _load_review_data(input_path)
    validation_result = _validate_input(input_path)

    lines: list[str] = ["# NASP curation review packet", ""]
    lines.extend(_format_validation_summary(validation_result))
    lines.extend(_format_pre_freeze_status(validation_result))

    for path, data in sorted(data_by_path.items()):
        lines.extend(_format_file_review(path, data))

    return "\n".join(lines).rstrip() + "\n"


def write_review_packet(input_path: Path, output_path: Path) -> Path:
    """Write a Markdown review packet and return its path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_review_packet(input_path))
    return output_path


def gate_blockers(input_path: Path) -> list[str]:
    """Return pre-freeze gate blockers for a file or directory.

    Blockers are unambiguous validation errors. Topology, reagent, verb, and
    weak-evidence findings remain advisory because their interpretation depends
    on the experiment and biological context.

    Args:
      input_path: Single draft file or directory of draft files.

    Returns:
      Human-readable validation blockers.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Review input not found: {input_path}")

    return [
        f"validation_error: {issue.path}: {issue.message}"
        for issue in _validate_input(input_path).errors
    ]


def _load_review_data(
    input_path: Path,
    reviewable_suffixes: tuple[str, ...] = (".md", ".yaml", ".yml"),
) -> dict[Path, dict[str, Any]]:
    """Load reviewable YAML files from a file or directory."""
    paths = (
        [input_path]
        if input_path.is_file()
        else sorted(input_path.glob("*.md"))
    )
    data_by_path: dict[Path, dict[str, Any]] = {}
    for path in paths:
        if (
            path.name.endswith(".gold.md")
            or path.suffix not in reviewable_suffixes
        ):
            continue
        data = yaml.safe_load(path.read_text())
        if isinstance(data, dict):
            data_by_path[path] = data
    return data_by_path


def _validate_input(input_path: Path) -> validate_compendium.ValidationResult:
    """Run existing directory validation for a file or directory input."""
    if input_path.is_dir():
        return validate_compendium.validate_directory(input_path)

    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_path = Path(temporary_directory)
        copied_path = temporary_path / input_path.name
        copied_path.write_text(input_path.read_text())
        return validate_compendium.validate_directory(temporary_path)


def _format_validation_summary(
    result: validate_compendium.ValidationResult,
) -> list[str]:
    """Format validation errors and warnings as Markdown."""
    lines = [
        "## Validation",
        "",
        f"- Errors: {len(result.errors)}",
        f"- Warnings: {len(result.warnings)}",
        "",
    ]
    if result.errors:
        lines.extend(("### Errors", ""))
        lines.extend(
            f"- `{issue.path}`: {issue.message}" for issue in result.errors
        )
        lines.append("")

    if result.warnings:
        lines.extend(("### Warnings", ""))
        lines.extend(
            f"- `{issue.path}`: {issue.message}" for issue in result.warnings
        )
        lines.append("")

    return lines


def _format_file_review(path: Path, data: dict[str, Any]) -> list[str]:
    """Format one draft's high-level review summary."""
    lines = [f"## {path.name}", ""]
    lines.extend(_format_edge_summary(data))
    lines.extend(_format_topology_lints(data))
    lines.extend(_format_review_hotspots(data))
    return lines


def _format_pre_freeze_status(
    result: validate_compendium.ValidationResult,
) -> list[str]:
    """Format pre-freeze status from unambiguous validation errors."""
    lines = ["## Pre-freeze status", ""]
    if result.errors:
        lines.extend(
            (
                "- Status: `BLOCKED`",
                f"- Blocking issues: {len(result.errors)}",
                "",
            )
        )
        lines.extend(
            f"- validation_error: `{issue.path}`: {issue.message}"
            for issue in result.errors[:15]
        )
    else:
        lines.extend(("- Status: `READY_FOR_FREEZE`", "- Blocking issues: 0"))
    lines.append("- Topology and review hotspots below are advisory.")
    lines.append("")
    return lines


def _format_edge_summary(data: dict[str, Any]) -> list[str]:
    """Format edge counts by relationship and evidence strength."""
    edges = data.get("edges")
    if not isinstance(edges, list):
        return ["### Edges", "", "- No `edges` list present.", ""]

    rel_counts = collections.Counter(
        str(edge.get("rel", "not_set"))
        for edge in edges
        if isinstance(edge, dict)
    )
    evidence_counts = collections.Counter(
        str(edge.get("evidence_strength", "not_set"))
        for edge in edges
        if isinstance(edge, dict)
    )

    lines = [
        "### Edges",
        "",
        f"- Edge records: {len(edges)}",
        "",
        "Relationship counts:",
    ]
    lines.extend(
        f"- `{rel}`: {count}" for rel, count in sorted(rel_counts.items())
    )
    lines.extend(("", "Evidence-strength counts:"))
    lines.extend(
        f"- `{evidence_strength}`: {count}"
        for evidence_strength, count in sorted(evidence_counts.items())
    )
    lines.append("")
    return lines


def _format_topology_lints(data: dict[str, Any]) -> list[str]:
    """Format advisory topology findings derived from edge patterns."""
    lints = _topology_lints(data)
    lines = ["### Advisory topology review", ""]
    if not lints:
        lines.append("- None detected.")
    else:
        lines.extend(f"- {lint}" for lint in lints)
    lines.append("")
    return lines


def _format_review_hotspots(data: dict[str, Any]) -> list[str]:
    """Format edge records most likely to need human review."""
    edges = data.get("edges")
    if not isinstance(edges, list):
        return []

    weak_support = [
        edge
        for edge in edges
        if isinstance(edge, dict)
        and str(edge.get("evidence_strength"))
        in {"canonical_inferred", "weak_correlative"}
    ]
    verb_review_edges = _verb_review_edges(edges)
    topology_lints = _topology_lints(data)

    lines = [
        "### Review hotspots",
        "",
        f"- Weak/canonical-inferred edges: {len(weak_support)}",
        f"- Verb-review edges: {len(verb_review_edges)}",
        f"- Topology lints: {len(topology_lints)}",
    ]
    if weak_support:
        lines.extend(("", "Weak/canonical-inferred edge examples:"))
        lines.extend(
            f"- {_format_edge_inline(edge)}" for edge in weak_support[:10]
        )
    if verb_review_edges:
        lines.extend(("", "Verb-review examples:"))
        lines.extend(
            f"- {_format_edge_inline(edge)}" for edge in verb_review_edges[:10]
        )
    if topology_lints:
        lines.extend(("", "Topology lint examples:"))
        lines.extend(f"- {lint}" for lint in topology_lints[:10])
    lines.append("")
    return lines


def _verb_review_edges(edges: list[Any]) -> list[dict[str, Any]]:
    """Return edges whose relationship verbs commonly need review."""
    review_targets = {
        "cellular_senescence",
        "retrotransposon_derepression",
        "DNA_damage",
        "type_I_IFN",
        "type_III_IFN",
        "inflammasome_activation",
    }
    broad_causal_targets = review_targets | {
        "tissue_inflammation",
        "fibrosis",
        "accelerated_aging",
        "inflammaging",
        "mortality",
    }
    return [
        edge
        for edge in edges
        if isinstance(edge, dict)
        and (
            (
                str(edge.get("rel")) == "causes"
                and str(edge.get("target")) in broad_causal_targets
            )
            or (
                str(edge.get("rel")) == "drives"
                and str(edge.get("target")) in review_targets
            )
        )
    ]


def _topology_lints(data: dict[str, Any]) -> list[str]:
    """Return advisory topology findings for repeated NASP failure modes."""
    edges = _edges_list(data)
    triples = {
        (
            str(edge.get("source", "")),
            str(edge.get("rel", "")),
            str(edge.get("target", "")),
        )
        for edge in edges
    }
    lints: list[str] = []

    for ligand, rel, sensing_process in sorted(triples):
        if rel != "activates" or not _is_generic_sensing_process(
            sensing_process
        ):
            continue
        if components := sorted(
            target
            for source, process_rel, target in triples
            if source == sensing_process
            and process_rel == "activates"
            and _is_specific_component_node(target)
        ):
            lints.append(
                f"{ligand} is routed through generic process "
                f"{sensing_process} before {', '.join(components)}; review"
                " direct ligand-to-component edges."
            )

    for edge in edges:
        source = str(edge.get("source", ""))
        target = str(edge.get("target", ""))
        if _is_reagent_only_endpoint(source) or _is_reagent_only_endpoint(
            target
        ):
            reagent = source if _is_reagent_only_endpoint(source) else target
            lints.append(
                f"reagent-like endpoint `{reagent}` appears in "
                f"{_format_edge_inline(edge)}; review whether it is a reusable "
                "biological trigger or belongs only in context."
            )
    return lints


def _is_reagent_only_endpoint(
    node: str,
    *,
    reagent_only_endpoints: frozenset[str] = frozenset({"dsDNA90"}),
    reagent_endpoint_prefixes: tuple[str, ...] = (
        "dsDNA",
        "ssDNA",
        "polyIC",
        "poly_I:C",
    ),
) -> bool:
    """Return whether a node looks like an assay reagent, not a graph node."""
    return node in reagent_only_endpoints or any(
        node.startswith(prefix) for prefix in reagent_endpoint_prefixes
    )


def _is_generic_sensing_process(
    node: str,
    *,
    generic_process_nodes: frozenset[str] = frozenset(
        {"cytosolic_RNA_sensing"}
    ),
    sensing_process_suffix: str = "_sensing",
) -> bool:
    """Return whether a node is a generic sensing process."""
    return node in generic_process_nodes or node.endswith(
        sensing_process_suffix
    )


def _is_specific_component_node(node: str) -> bool:
    """Return whether a node looks like a specific gene/protein component."""
    compact = node.replace("_", "").replace("-", "")
    return (
        bool(compact)
        and compact == compact.upper()
        and any(character.isalpha() for character in compact)
        and node not in {"DNA", "RNA"}
        and not _is_generic_sensing_process(node)
    )


def _edges_list(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Return well-formed edge records from a draft."""
    edges = data.get("edges")
    if not isinstance(edges, list):
        return []
    return [edge for edge in edges if isinstance(edge, dict)]


def _format_edge_inline(edge: dict[str, Any]) -> str:
    """Format a compact edge description."""
    return (
        f"`{edge.get('source', '?')}` --"
        f"[{edge.get('rel', '?')}/{edge.get('evidence_strength', '?')}]--> "
        f"`{edge.get('target', '?')}`"
    )

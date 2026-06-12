"""Validate NASP compendium files before curation graph rendering."""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any

import yaml  # type: ignore

from nasp_compendium.style import ENTITY_FIELDS
from nasp_compendium.style import EVIDENCE_STYLES
from nasp_compendium.style import REL_COLOR
from nasp_compendium.vocab_tiers import Vocabulary
from nasp_compendium.vocab_tiers import load_proposed_terms
from nasp_compendium.vocab_tiers import load_vocabulary
from nasp_compendium.vocab_tiers import validate_draft_terms


VOCABULARY_PATH: Path = Path(__file__).with_name("vocabulary.yaml")

VOCABULARY_FIELDS: tuple[str, ...] = (
    "nucleic_acid_sensors",
    "pathways",
    "mechanisms",
    "model_systems",
    "evidence_type",
)

SKIP_EDGE_EXCLUDED_RELS: frozenset[str] = frozenset(
    {
        "contains",
        "correlates",
        "negatively_correlates",
        "does_not_correlate",
        "does_not_drive",
    }
)

SKIP_EDGE_EXCLUDED_CANDIDATE_RELS: frozenset[str] = frozenset(
    SKIP_EDGE_EXCLUDED_RELS | {"downregulates", "upregulates"}
)

SKIP_EDGE_MAX_DEPTH: int = 8

REQUIRED_EDGE_FIELDS: tuple[str, ...] = (
    "chain_id",
    "step",
    "source",
    "target",
    "rel",
    "evidence_strength",
    "context",
    "support",
    "papers",
)

SUSPICIOUS_NODE_NAMES: frozenset[str] = frozenset(
    {
        "CCF",
        "CCF_formation",
        "STING",
        "cGAS",
        "IL8",
        "p65",
        "tumor_formation",
        "fibrotic_tissue_formation",
        "programmed_cell_death",
        "liver_tumorigenesis",
        "lung_inflammation",
        "kidney_fibrosis",
    }
)

ALLOWED_FREE_ENDPOINTS: frozenset[str] = frozenset(
    {
        "cGAMP",
        "cAMP",
        "replicative_exhaustion",
        "dsDNA90",
    }
)


@dataclasses.dataclass(frozen=True)
class ValidationIssue:
    """A single validation error or warning with file-local context."""

    path: Path
    message: str


@dataclasses.dataclass(frozen=True)
class ValidationResult:
    """Collected hard errors and warnings from one validation run."""

    errors: list[ValidationIssue]
    warnings: list[ValidationIssue]

    @property
    def ok(self) -> bool:
        """Return whether validation found no hard errors."""
        return not self.errors

    def exit_code(self, strict: bool) -> int:
        """Return the process exit code for default or strict mode."""
        return 1 if self.errors or (strict and self.warnings) else 0


def validate_directory(directory: Path) -> ValidationResult:
    """Validate every Markdown compendium file in `directory`.

    Args:
      directory: Directory containing per-paper YAML-in-Markdown files.

    Returns:
      ValidationResult containing hard errors and warnings.
    """
    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []
    data_by_path: dict[Path, dict[str, Any]] = {}

    if not directory.exists() or not directory.is_dir():
        errors.append(
            ValidationIssue(
                directory,
                f"Compendium directory not found: {directory}",
            )
        )
        return ValidationResult(errors=errors, warnings=warnings)

    for path in sorted(directory.glob("*.md")):
        data = _load_yaml_file(path, errors)
        if data is not None:
            data_by_path[path] = data

    vocabulary = _load_vocabulary(errors)
    declared_entities = _declared_entities(data_by_path.values())
    seen_edges: dict[tuple[str, str, str, tuple[str, ...]], Path] = {}

    for path, data in data_by_path.items():
        _validate_file_shape(path, data, errors)
        if vocabulary is not None:
            _validate_tiered_vocabulary(
                path,
                data,
                vocabulary,
                declared_entities,
                errors,
                warnings,
            )
        _validate_edges(
            path,
            data.get("edges"),
            declared_entities,
            seen_edges,
            errors,
            warnings,
        )

    _warn_skip_edges(data_by_path, warnings)

    return ValidationResult(errors=errors, warnings=warnings)


def print_result(result: ValidationResult, strict: bool) -> None:
    """Print validation results in a compact CLI-friendly format."""
    if result.errors:
        print(f"\nErrors ({len(result.errors)}):")
        for issue in result.errors:
            print(f"  {issue.path}: {issue.message}")

    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for issue in result.warnings:
            print(f"  {issue.path}: {issue.message}")

    if result.exit_code(strict) == 0:
        print("\nValidation passed.")
    elif result.errors:
        print("\nValidation failed with hard errors.")
    else:
        print("\nValidation failed in strict mode because warnings were found.")


def _load_yaml_file(
    path: Path,
    errors: list[ValidationIssue],
) -> dict[str, Any] | None:
    """Load a compendium file as YAML and enforce top-level mapping shape."""
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        errors.append(
            ValidationIssue(path, f"Cannot parse YAML: {exc.problem or exc}")  # type: ignore
        )
        return None

    if not isinstance(data, dict):
        errors.append(ValidationIssue(path, "Top-level YAML is not a mapping."))
        return None

    return data


def _validate_file_shape(
    path: Path,
    data: dict[str, Any],
    errors: list[ValidationIssue],
) -> None:
    """Validate top-level compendium keys and their expected container types."""
    if "paper" not in data:
        errors.append(ValidationIssue(path, "Missing 'paper'."))
    elif not isinstance(data["paper"], dict):
        errors.append(ValidationIssue(path, "'paper' is not a mapping."))

    if "edges" not in data:
        errors.append(ValidationIssue(path, "Missing 'edges'."))
    elif not isinstance(data["edges"], list):
        errors.append(ValidationIssue(path, "'edges' is not a list."))


def _load_vocabulary(
    errors: list[ValidationIssue],
) -> Vocabulary | None:
    """Load tiered vocabulary from the package YAML file."""
    try:
        vocabulary = load_vocabulary(VOCABULARY_PATH)
    except OSError as exc:
        errors.append(
            ValidationIssue(
                VOCABULARY_PATH,
                f"Cannot read vocabulary.yaml: {exc}",
            )
        )
        return None
    except yaml.YAMLError as exc:
        errors.append(
            ValidationIssue(
                VOCABULARY_PATH,
                f"Cannot parse vocabulary.yaml: {exc.problem or exc}",  # type: ignore
            )
        )
        return None

    for field in VOCABULARY_FIELDS:
        if field not in vocabulary.canonical:
            errors.append(
                ValidationIssue(
                    VOCABULARY_PATH,
                    f"vocabulary.yaml canonical field {field!r} is missing.",
                )
            )

    return vocabulary


def _validate_tiered_vocabulary(
    path: Path,
    data: dict[str, Any],
    vocabulary: Vocabulary,
    declared_entities: set[str],
    errors: list[ValidationIssue],
    warnings: list[ValidationIssue],
) -> None:
    """Classify paper entries and edge endpoints through the tiered gate."""
    proposed_terms = load_proposed_terms(data)
    controlled_terms = _controlled_paper_terms(data)
    endpoint_terms = _edge_endpoint_terms(data.get("edges"))

    controlled_errors, controlled_warnings = validate_draft_terms(
        controlled_terms,
        vocabulary,
        proposed_terms,
        compendium_nodes=set(),
    )
    endpoint_errors, endpoint_warnings = validate_draft_terms(
        endpoint_terms,
        vocabulary,
        proposed_terms,
        compendium_nodes=declared_entities | ALLOWED_FREE_ENDPOINTS,
    )

    for message in _unique_verdict_messages(
        [*controlled_errors, *endpoint_errors]
    ):
        errors.append(ValidationIssue(path, message))
    for message in _unique_verdict_messages(
        [*controlled_warnings, *endpoint_warnings]
    ):
        warnings.append(ValidationIssue(path, message))


def _unique_verdict_messages(verdicts: list[Any]) -> list[str]:
    """Return verdict messages once, preserving first-seen order."""
    seen: set[str] = set()
    messages: list[str] = []
    for verdict in verdicts:
        if verdict.message in seen:
            continue
        seen.add(verdict.message)
        messages.append(verdict.message)
    return messages


def _controlled_paper_terms(data: dict[str, Any]) -> set[str]:
    """Return controlled paper-block terms covered by vocabulary.yaml."""
    terms: set[str] = set()
    paper_block = data.get("paper")
    if not isinstance(paper_block, dict):
        return terms

    for paper in paper_block.values():
        if not isinstance(paper, dict):
            continue
        for field in VOCABULARY_FIELDS:
            values = paper.get(field)
            if isinstance(values, list):
                terms.update(str(value) for value in values)
    return terms


def _edge_endpoint_terms(edges: Any) -> set[str]:
    """Return source and target node strings used by edge records."""
    terms: set[str] = set()
    if not isinstance(edges, list):
        return terms

    for edge in edges:
        if not isinstance(edge, dict):
            continue
        for endpoint in ("source", "target"):
            value = edge.get(endpoint)
            if value is not None:
                terms.add(str(value))
    return terms


def _validate_edges(
    path: Path,
    edges: Any,
    declared_entities: set[str],
    seen_edges: dict[tuple[str, str, str, tuple[str, ...]], Path],
    errors: list[ValidationIssue],
    warnings: list[ValidationIssue],
) -> None:
    """Validate edge-level schema, controlled vocabulary, and curation hints."""
    if not isinstance(edges, list):
        return

    for index, edge in enumerate(edges, start=1):
        label = f"edge {index}"
        if not isinstance(edge, dict):
            errors.append(ValidationIssue(path, f"{label} is not a mapping."))
            continue

        for field in REQUIRED_EDGE_FIELDS:
            if field not in edge:
                errors.append(
                    ValidationIssue(path, f"{label} is missing '{field}'.")
                )

        _validate_edge_values(path, label, edge, errors, warnings)
        _warn_undeclared_entities(
            path, label, edge, declared_entities, warnings
        )
        _warn_duplicate_edge(path, label, edge, seen_edges, warnings)


def _warn_skip_edges(
    data_by_path: dict[Path, dict[str, Any]],
    warnings: list[ValidationIssue],
) -> None:
    """Warn when a paper has both a direct edge and a longer same-paper path.

    This heuristic is scoped per paper. It ignores cross-paper paths, and it
    excludes `contains`, statistical association relations, and negative-finding
    relations (`does_not_correlate`, `does_not_drive`) because those are not
    causal chain steps. Direct `upregulates` and `downregulates` abundance
    edges are not flagged as shortcut candidates because they can legitimately
    coexist with longer upstream signaling chains. The search uses a bounded
    breadth-first traversal with `SKIP_EDGE_MAX_DEPTH` edges to avoid
    pathological cycles. Warnings are review prompts, not proof that an edge is
    invalid.
    """
    edges_by_paper: dict[str, list[tuple[Path, dict[Any, Any]]]] = {}
    for path, data in data_by_path.items():
        edges = data.get("edges")
        if not isinstance(edges, list):
            continue
        for edge in edges:
            if not isinstance(edge, dict):
                continue
            papers = edge.get("papers")
            if not isinstance(papers, list):
                continue
            for paper_id in papers:
                edges_by_paper.setdefault(str(paper_id), []).append(
                    (path, edge)
                )

    for paper_id, paper_edges in sorted(edges_by_paper.items()):
        adjacency = _paper_adjacency(paper_edges)
        for path, edge in paper_edges:
            if not _is_skip_edge_candidate(edge):
                continue
            source = str(edge["source"])
            target = str(edge["target"])
            intermediate_path = _find_supported_path(
                adjacency,
                source,
                target,
                max_depth=SKIP_EDGE_MAX_DEPTH,
            )
            if intermediate_path is None:
                continue
            warnings.append(
                ValidationIssue(
                    path,
                    f"{paper_id} edge '{source} {edge['rel']} {target}' may "
                    "shortcut a supported path: "
                    f"{' -> '.join(intermediate_path)}; review whether this "
                    "collapses an intermediate.",
                )
            )


def _paper_adjacency(
    paper_edges: list[tuple[Path, dict[Any, Any]]],
) -> dict[str, set[str]]:
    """Build source-to-target adjacency from causal chain edges in one paper."""
    adjacency: dict[str, set[str]] = {}
    for _, edge in paper_edges:
        if not _is_skip_path_step(edge):
            continue
        source = str(edge["source"])
        target = str(edge["target"])
        adjacency.setdefault(source, set()).add(target)
    return adjacency


def _is_skip_edge_candidate(edge: dict[Any, Any]) -> bool:
    """Return whether an edge is eligible for skip-edge path checking."""
    return (
        edge.get("source") is not None
        and edge.get("target") is not None
        and edge.get("rel") is not None
        and str(edge.get("rel")) not in SKIP_EDGE_EXCLUDED_CANDIDATE_RELS
    )


def _is_skip_path_step(edge: dict[Any, Any]) -> bool:
    """Return whether an edge can contribute to a supported intermediate
    path.
    """
    return (
        edge.get("source") is not None
        and edge.get("target") is not None
        and edge.get("rel") is not None
        and str(edge.get("rel")) not in SKIP_EDGE_EXCLUDED_RELS
    )


def _find_supported_path(
    adjacency: dict[str, set[str]],
    source: str,
    target: str,
    *,
    max_depth: int,
) -> list[str] | None:
    """Find a path from source to target with at least one intermediate node."""
    queue: list[list[str]] = [[source]]
    visited: set[str] = {source}

    while queue:
        path = queue.pop(0)
        current = path[-1]
        depth = len(path) - 1
        if depth >= max_depth:
            continue

        for neighbor in sorted(adjacency.get(current, set())):
            if current == source and neighbor == target:
                continue
            next_path = [*path, neighbor]
            if neighbor == target and len(next_path) >= 3:
                return next_path
            if neighbor in visited:
                continue
            visited.add(neighbor)
            queue.append(next_path)

    return None


def _validate_edge_values(
    path: Path,
    label: str,
    edge: dict[Any, Any],
    errors: list[ValidationIssue],
    warnings: list[ValidationIssue],
) -> None:
    """Validate controlled edge values and empty context/support warnings."""
    rel = edge.get("rel")
    if rel is not None and rel not in REL_COLOR:
        errors.append(
            ValidationIssue(path, f"{label} has unknown rel: {rel!r}.")
        )

    evidence_strength = edge.get("evidence_strength")
    if (
        evidence_strength is not None
        and evidence_strength not in EVIDENCE_STYLES
    ):
        errors.append(
            ValidationIssue(
                path,
                f"{label} has unknown evidence_strength: "
                f"{evidence_strength!r}.",
            )
        )

    papers = edge.get("papers")
    if papers is not None and (not isinstance(papers, list) or not papers):
        errors.append(
            ValidationIssue(
                path,
                f"{label} has 'papers' that is not a non-empty list.",
            )
        )

    for field in ("context", "support"):
        value = edge.get(field)
        if value is not None and not str(value).strip():
            warnings.append(
                ValidationIssue(path, f"{label} has empty {field}.")
            )

    for endpoint in ("source", "target"):
        node = edge.get(endpoint)
        if _is_suspicious_node_name(node):
            warnings.append(
                ValidationIssue(
                    path,
                    f"{label} has suspicious {endpoint} node: {node!r}.",
                )
            )


def _warn_undeclared_entities(
    path: Path,
    label: str,
    edge: dict[Any, Any],
    declared_entities: set[str],
    warnings: list[ValidationIssue],
) -> None:
    """Warn when an edge endpoint is absent from all paper entity fields."""
    for endpoint in ("source", "target"):
        node = edge.get(endpoint)
        if (
            node is not None
            and str(node) not in declared_entities
            and str(node) not in ALLOWED_FREE_ENDPOINTS
        ):
            warnings.append(
                ValidationIssue(
                    path,
                    f"{label} {endpoint} is not declared in any paper "
                    f"entity field: {node!r}.",
                )
            )


def _warn_duplicate_edge(
    path: Path,
    label: str,
    edge: dict[Any, Any],
    seen_edges: dict[tuple[str, str, str, tuple[str, ...]], Path],
    warnings: list[ValidationIssue],
) -> None:
    """Warn when the same source-target-rel-papers edge appears twice."""
    key = _duplicate_key(edge)
    if key is None:
        return

    if key in seen_edges:
        warnings.append(
            ValidationIssue(
                path,
                f"{label} duplicates exact edge first seen in "
                f"{seen_edges[key]}.",
            )
        )
        return

    seen_edges[key] = path


def _duplicate_key(
    edge: dict[Any, Any],
) -> tuple[str, str, str, tuple[str, ...]] | None:
    """Return the exact-edge duplicate key, if the edge has valid fields."""
    papers = edge.get("papers")
    if not isinstance(papers, list) or not papers:
        return None

    source = edge.get("source")
    target = edge.get("target")
    rel = edge.get("rel")
    if source is None or target is None or rel is None:
        return None

    return (
        str(source),
        str(target),
        str(rel),
        tuple(str(paper) for paper in papers),
    )


def _declared_entities(data_values: object) -> set[str]:
    """Collect entities declared in any paper entity field."""
    entities: set[str] = set()
    for data in data_values:  # type: ignore
        if not isinstance(data, dict) or not isinstance(
            data.get("paper"), dict
        ):
            continue
        for paper in data["paper"].values():
            if not isinstance(paper, dict):
                continue
            for field in ENTITY_FIELDS:
                values = paper.get(field)
                if isinstance(values, list):
                    entities.update(str(value) for value in values)
    return entities


def _is_suspicious_node_name(node: object) -> bool:
    """Return whether a node name matches known naming anti-patterns."""
    if not isinstance(node, str):
        return False
    return node.endswith("_expression") or node in SUSPICIOUS_NODE_NAMES

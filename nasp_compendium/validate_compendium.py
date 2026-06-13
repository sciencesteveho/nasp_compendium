"""Validate NASP compendium files before curation graph rendering."""

from __future__ import annotations

import collections
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


VOCABULARY_PATH: Path = (
    Path(__file__).resolve().parent.parent / "agent" / "vocabulary.yaml"
)

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

CLAIMS_KEY: str = "claims"
CLAIM_EDGE_MATRIX_KEY: str = "claim_edge_matrix"
SUPPORT_CLAIMS_KEY: str = "support_claims"
PAPER_SCOPE_KEY: str = "paper_scope"
BRANCH_TYPE_KEY: str = "branch_type"
GRAPH_CANDIDATE_KEY: str = "graph_candidate"
MAPPED_EDGES_KEY: str = "mapped_edges"
CLAIM_REUSE_WARNING_THRESHOLD: int = 3
ADJUDICATIONS_KEY: str = "adjudications"
ISSUE_TYPE_KEY: str = "issue_type"
DECISION_KEY: str = "decision"
RATIONALE_KEY: str = "rationale"
EMITTED_EDGES_KEY: str = "emitted_edges"
REMOVE_EDGES_KEY: str = "remove_edges"
REJECTED_ALTERNATIVE_KEY: str = "rejected_alternative"
CONVENTION_RULE_KEY: str = "convention_rule"
NEAREST_INTERMEDIATE_SEARCH_KEY: str = "nearest_intermediate_search"
CANDIDATE_EDGES_CONSIDERED_KEY: str = "candidate_edges_considered"

REQUIRED_CLAIM_FIELDS: tuple[str, ...] = (
    "claim_id",
    "evidence_location",
    "claim",
    "assay",
    "disposition",
    "support",
)

ALLOWED_CLAIM_DISPOSITIONS: frozenset[str] = frozenset(
    {
        "edge",
        "context_only",
        "negative",
        "insufficient",
    }
)

ALLOWED_BRANCH_TYPES: frozenset[str] = frozenset(
    {
        "main_spine",
        "sensor_branch",
        "inflammatory_output",
        "cohort_association",
        "state_reversal",
        "negative_specificity",
        "organismal_outcome",
        "context_only",
    }
)

GRAPH_CANDIDATE_BRANCH_TYPES: frozenset[str] = frozenset(
    {
        "main_spine",
        "sensor_branch",
        "inflammatory_output",
        "cohort_association",
        "state_reversal",
        "negative_specificity",
        "organismal_outcome",
    }
)

MATRIX_EDGE_FIELDS: tuple[str, ...] = (
    "source",
    "target",
    "rel",
    "evidence_strength",
)

ADJUDICATION_EDGE_FIELDS: tuple[str, ...] = (
    "source",
    "target",
    "rel",
)

REQUIRED_ADJUDICATION_FIELDS: tuple[str, ...] = (
    "issue_id",
    ISSUE_TYPE_KEY,
    DECISION_KEY,
    RATIONALE_KEY,
)

ALLOWED_ADJUDICATION_ISSUE_TYPES: frozenset[str] = frozenset(
    {
        "hidden_graph_candidate",
        "topology_lint",
        "shortcut_warning",
        "verb_warning",
        "evidence_strength_warning",
        "reagent_endpoint_warning",
        "broad_claim_reuse",
        "gold_or_scope_disagreement",
        "scope_density_warning",
    }
)

ALLOWED_ADJUDICATION_DECISIONS: frozenset[str] = frozenset(
    {
        "emit_edge",
        "revise_edges",
        "keep_context",
        "keep_insufficient",
        "keep_as_is",
        "needs_human_review",
        "reject_as_gold_defect",
    }
)

BRANCHES_REQUIRING_ADJUDICATION: frozenset[str] = frozenset(
    {
        "sensor_branch",
        "inflammatory_output",
        "organismal_outcome",
        "state_reversal",
        "cohort_association",
        "negative_specificity",
    }
)

REAGENT_ONLY_ENDPOINTS: frozenset[str] = frozenset(
    {
        "dsDNA90",
    }
)

REAGENT_ENDPOINT_PREFIXES: tuple[str, ...] = (
    "dsDNA",
    "ssDNA",
    "polyIC",
    "poly_I:C",
)

GENERIC_PROCESS_NODES: frozenset[str] = frozenset(
    {
        "cytosolic_RNA_sensing",
    }
)

SENSING_PROCESS_SUFFIX: str = "_sensing"

SENSOR_COMPONENT_NODES: frozenset[str] = frozenset(
    {
        "DDX58",
        "IFIH1",
    }
)

EDGE_SUPPORTING_CLAIM_DISPOSITIONS: frozenset[str] = frozenset(
    {
        "edge",
        "negative",
    }
)

ALLOWED_PAPER_SCOPES: frozenset[str] = frozenset(
    {
        "mechanism_paper",
        "perturbation_paper",
        "cohort_correlation_paper",
        "atlas_resource",
        "biomarker_validation_paper",
        "review_or_resource",
        "mixed_mechanism_and_correlation",
    }
)

CORRELATIVE_PAPER_SCOPES: frozenset[str] = frozenset(
    {
        "cohort_correlation_paper",
        "atlas_resource",
        "biomarker_validation_paper",
        "review_or_resource",
    }
)

CAUSAL_EDGE_RELS: frozenset[str] = frozenset(
    {
        "activates",
        "drives",
        "induces",
        "causes",
        "required_for",
        "produces",
        "suppresses",
        "inhibits",
        "downregulates",
        "upregulates",
        "retains",
        "forms_pore_for",
        "binds_recruits",
    }
)

OVERCONFIDENT_EVIDENCE_STRENGTHS: frozenset[str] = frozenset(
    {
        "direct_measured",
        "perturbation_supported",
    }
)

CAUSAL_UNCERTAINTY_PHRASES: tuple[str, ...] = (
    "not directly perturbed",
    "not directly tested",
    "not directly measured",
    "not tested",
    "not measured",
    "no direct perturbation",
    "no direct evidence",
    "inferred",
    "proposed",
    "consistent with",
)

DRIVES_TARGET_VERB_REVIEW: frozenset[str] = frozenset(
    {
        "cellular_senescence",
        "retrotransposon_derepression",
        "DNA_damage",
        "type_I_IFN",
        "type_III_IFN",
        "inflammasome_activation",
    }
)

CAUSES_TARGET_VERB_REVIEW: frozenset[str] = frozenset(
    {
        "cellular_senescence",
        "DNA_damage",
        "tissue_inflammation",
        "fibrosis",
        "accelerated_aging",
        "inflammaging",
        "mortality",
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
        if path.name.endswith(".gold.md"):
            continue
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
        claim_records = _validate_claims(path, data, errors, warnings)
        claim_edge_matrix = _validate_claim_edge_matrix(
            path,
            data,
            claim_records,
            errors,
            warnings,
        )
        adjudications = _validate_adjudications(
            path,
            data,
            claim_records,
            errors,
            warnings,
        )
        _warn_unadjudicated_hidden_candidates(
            path,
            claim_records,
            adjudications,
            warnings,
        )
        paper_scopes = _validate_paper_scopes(path, data, warnings)
        _validate_edges(
            path,
            data.get("edges"),
            declared_entities,
            seen_edges,
            errors,
            warnings,
            claim_records=claim_records,
            claim_edge_matrix=claim_edge_matrix,
            adjudications=adjudications,
            paper_scopes=paper_scopes,
            require_claim_support=CLAIMS_KEY in data,
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


def _validate_claims(
    path: Path,
    data: dict[str, Any],
    errors: list[ValidationIssue],
    warnings: list[ValidationIssue],
) -> dict[str, dict[str, Any]]:
    """Validate optional raw-claim records and return records by claim id."""
    claims = data.get(CLAIMS_KEY)
    if claims is None:
        return {}

    if not isinstance(claims, list):
        errors.append(ValidationIssue(path, "'claims' is not a list."))
        return {}

    claim_records: dict[str, dict[str, Any]] = {}
    for index, claim in enumerate(claims, start=1):
        label = f"claim {index}"
        if not isinstance(claim, dict):
            errors.append(ValidationIssue(path, f"{label} is not a mapping."))
            continue

        for field in REQUIRED_CLAIM_FIELDS:
            if field not in claim:
                errors.append(
                    ValidationIssue(path, f"{label} is missing '{field}'.")
                )

        claim_id = claim.get("claim_id")
        if claim_id is None:
            continue
        claim_id_text = str(claim_id)
        if claim_id_text in claim_records:
            errors.append(
                ValidationIssue(
                    path,
                    f"{label} duplicates claim_id {claim_id_text!r}.",
                )
            )
        claim_records[claim_id_text] = claim

        disposition = claim.get("disposition")
        if disposition is not None and disposition not in ALLOWED_CLAIM_DISPOSITIONS:
            errors.append(
                ValidationIssue(
                    path,
                    f"{label} has unknown disposition: {disposition!r}.",
                )
            )

        if not str(claim.get("support", "")).strip():
            warnings.append(ValidationIssue(path, f"{label} has empty support."))

        branch_type = claim.get(BRANCH_TYPE_KEY)
        if branch_type is None:
            warnings.append(
                ValidationIssue(
                    path,
                    f"{label} is missing {BRANCH_TYPE_KEY!r}; add a branch "
                    "type so review packets can audit branch coverage.",
                )
            )
        elif str(branch_type) not in ALLOWED_BRANCH_TYPES:
            errors.append(
                ValidationIssue(
                    path,
                    f"{label} has unknown {BRANCH_TYPE_KEY}: "
                    f"{branch_type!r}.",
                )
            )

        if GRAPH_CANDIDATE_KEY not in claim:
            warnings.append(
                ValidationIssue(
                    path,
                    f"{label} is missing {GRAPH_CANDIDATE_KEY!r}; set it "
                    "to true for claims that should be considered for graph "
                    "edges and false for audit/context-only evidence.",
                )
            )

        if _claim_graph_candidate(claim) and disposition in {
            "context_only",
            "insufficient",
        }:
            warnings.append(
                ValidationIssue(
                    path,
                    f"{label} is graph_candidate but has disposition "
                    f"{disposition!r}; review whether a graph edge or "
                    "explicit rejection rationale is needed.",
                )
            )

        if (
            str(branch_type) in GRAPH_CANDIDATE_BRANCH_TYPES
            and disposition == "context_only"
        ):
            warnings.append(
                ValidationIssue(
                    path,
                    f"{label} has branch_type {branch_type!r} but is marked "
                    "context_only; verify this is not a missed branch edge.",
                )
            )

    return claim_records


def _validate_claim_edge_matrix(
    path: Path,
    data: dict[str, Any],
    claim_records: dict[str, dict[str, Any]],
    errors: list[ValidationIssue],
    warnings: list[ValidationIssue],
) -> dict[str, list[dict[str, Any]]]:
    """Validate optional claim-to-edge matrix entries.

    The matrix is a typed support contract between raw claims and final graph
    edges. It is intentionally optional for older files, but new calibration
    drafts should use it whenever one claim supports multiple chain edges.
    """
    matrix = data.get(CLAIM_EDGE_MATRIX_KEY)
    if matrix is None:
        return {}

    if not isinstance(matrix, list):
        errors.append(
            ValidationIssue(path, f"{CLAIM_EDGE_MATRIX_KEY!r} is not a list.")
        )
        return {}

    edges_by_claim: dict[str, list[dict[str, Any]]] = {}
    for index, record in enumerate(matrix, start=1):
        label = f"{CLAIM_EDGE_MATRIX_KEY} record {index}"
        if not isinstance(record, dict):
            errors.append(ValidationIssue(path, f"{label} is not a mapping."))
            continue

        claim_id = record.get("claim_id")
        if claim_id is None:
            errors.append(ValidationIssue(path, f"{label} is missing 'claim_id'."))
            continue
        claim_id_text = str(claim_id)
        if claim_id_text not in claim_records:
            errors.append(
                ValidationIssue(
                    path,
                    f"{label} references unknown claim_id {claim_id_text!r}.",
                )
            )

        mapped_edges = record.get(MAPPED_EDGES_KEY)
        if not isinstance(mapped_edges, list) or not mapped_edges:
            errors.append(
                ValidationIssue(
                    path,
                    f"{label} has {MAPPED_EDGES_KEY!r} that is not a "
                    "non-empty list.",
                )
            )
            continue

        normalized_mapped_edges: list[dict[str, Any]] = []
        for edge_index, mapped_edge in enumerate(mapped_edges, start=1):
            edge_label = f"{label} mapped edge {edge_index}"
            if not isinstance(mapped_edge, dict):
                errors.append(
                    ValidationIssue(path, f"{edge_label} is not a mapping.")
                )
                continue
            for field in MATRIX_EDGE_FIELDS:
                if field not in mapped_edge:
                    errors.append(
                        ValidationIssue(
                            path,
                            f"{edge_label} is missing {field!r}.",
                        )
                    )
            rel = mapped_edge.get("rel")
            if rel is not None and rel not in REL_COLOR:
                errors.append(
                    ValidationIssue(
                        path,
                        f"{edge_label} has unknown rel: {rel!r}.",
                    )
                )
            evidence_strength = mapped_edge.get("evidence_strength")
            if (
                evidence_strength is not None
                and evidence_strength not in EVIDENCE_STYLES
            ):
                errors.append(
                    ValidationIssue(
                        path,
                        f"{edge_label} has unknown evidence_strength: "
                        f"{evidence_strength!r}.",
                    )
                )
            normalized_mapped_edges.append(mapped_edge)

        edges_by_claim.setdefault(claim_id_text, []).extend(
            normalized_mapped_edges
        )

    if matrix and not edges_by_claim:
        warnings.append(
            ValidationIssue(
                path,
                f"{CLAIM_EDGE_MATRIX_KEY!r} is present but no usable mapped "
                "edges were found.",
            )
        )

    return edges_by_claim



def _validate_adjudications(
    path: Path,
    data: dict[str, Any],
    claim_records: dict[str, dict[str, Any]],
    errors: list[ValidationIssue],
    warnings: list[ValidationIssue],
) -> list[dict[str, Any]]:
    """Validate optional pre-freeze adjudication records."""
    adjudications = data.get(ADJUDICATIONS_KEY)
    if adjudications is None:
        return []

    if not isinstance(adjudications, list):
        errors.append(
            ValidationIssue(path, f"{ADJUDICATIONS_KEY!r} is not a list.")
        )
        return []

    records: list[dict[str, Any]] = []
    seen_issue_ids: set[str] = set()
    for index, record in enumerate(adjudications, start=1):
        label = f"{ADJUDICATIONS_KEY} record {index}"
        if not isinstance(record, dict):
            errors.append(ValidationIssue(path, f"{label} is not a mapping."))
            continue

        for field in REQUIRED_ADJUDICATION_FIELDS:
            if field not in record:
                errors.append(
                    ValidationIssue(path, f"{label} is missing {field!r}.")
                )

        issue_id = record.get("issue_id")
        if issue_id is not None:
            issue_id_text = str(issue_id)
            if issue_id_text in seen_issue_ids:
                errors.append(
                    ValidationIssue(
                        path,
                        f"{label} duplicates issue_id {issue_id_text!r}.",
                    )
                )
            seen_issue_ids.add(issue_id_text)

        issue_type = record.get(ISSUE_TYPE_KEY)
        if issue_type is not None and str(issue_type) not in ALLOWED_ADJUDICATION_ISSUE_TYPES:
            errors.append(
                ValidationIssue(
                    path,
                    f"{label} has unknown {ISSUE_TYPE_KEY}: {issue_type!r}.",
                )
            )

        decision = record.get(DECISION_KEY)
        if decision is not None and str(decision) not in ALLOWED_ADJUDICATION_DECISIONS:
            errors.append(
                ValidationIssue(
                    path,
                    f"{label} has unknown {DECISION_KEY}: {decision!r}.",
                )
            )

        rationale = str(record.get(RATIONALE_KEY, "")).strip()
        if not rationale:
            warnings.append(
                ValidationIssue(
                    path,
                    f"{label} has empty {RATIONALE_KEY!r}; adjudications "
                    "must explain why the draft was changed or left as-is.",
                )
            )

        claim_id = record.get("claim_id")
        if claim_id is not None and str(claim_id) not in claim_records:
            warnings.append(
                ValidationIssue(
                    path,
                    f"{label} references unknown claim_id {str(claim_id)!r}.",
                )
            )

        _validate_adjudication_edge_list(
            path,
            label,
            record,
            EMITTED_EDGES_KEY,
            errors,
            warnings,
        )
        _validate_adjudication_edge_list(
            path,
            label,
            record,
            REMOVE_EDGES_KEY,
            errors,
            warnings,
        )

        if str(decision) in {"emit_edge", "revise_edges"} and not isinstance(
            record.get(EMITTED_EDGES_KEY),
            list,
        ):
            warnings.append(
                ValidationIssue(
                    path,
                    f"{label} decision {decision!r} should include "
                    f"{EMITTED_EDGES_KEY!r} listing the edge(s) that resolve "
                    "the issue.",
                )
            )

        _validate_adjudication_resolution_metadata(
            path, label, record, claim_records, warnings
        )

        records.append(record)

    return records


def _validate_adjudication_resolution_metadata(
    path: Path,
    label: str,
    record: dict[str, Any],
    claim_records: dict[str, dict[str, Any]],
    warnings: list[ValidationIssue],
) -> None:
    """Validate issue-specific metadata that makes adjudication auditable."""
    issue_type = str(record.get(ISSUE_TYPE_KEY, ""))
    decision = str(record.get(DECISION_KEY, ""))

    if issue_type in {"verb_warning", "evidence_strength_warning"}:
        if decision == "keep_as_is":
            for field in (REJECTED_ALTERNATIVE_KEY, CONVENTION_RULE_KEY):
                if not str(record.get(field, "")).strip():
                    warnings.append(
                        ValidationIssue(
                            path,
                            f"{label} keeps a {issue_type} as-is but lacks "
                            f"{field!r}; record the rejected alternative and "
                            "the convention/rule used for the decision.",
                        )
                    )

    if issue_type != "hidden_graph_candidate":
        return
    if decision not in {"keep_context", "keep_insufficient", "keep_as_is"}:
        return

    claim_id = record.get("claim_id")
    claim = claim_records.get(str(claim_id)) if claim_id is not None else None
    branch_type = str(claim.get(BRANCH_TYPE_KEY, "")) if claim else ""
    if branch_type not in BRANCHES_REQUIRING_ADJUDICATION:
        return

    nearest_search = record.get(NEAREST_INTERMEDIATE_SEARCH_KEY)
    if not isinstance(nearest_search, dict):
        warnings.append(
            ValidationIssue(
                path,
                f"{label} keeps high-priority hidden branch {branch_type!r} "
                f"out of the graph but lacks {NEAREST_INTERMEDIATE_SEARCH_KEY!r}; "
                "record whether the nearest supported intermediate edge was searched.",
            )
        )
        return

    searched = nearest_search.get("searched")
    searched_bool = searched is True or str(searched).lower() in {"true", "1", "yes"}
    candidates = nearest_search.get(CANDIDATE_EDGES_CONSIDERED_KEY)
    if not searched_bool or not isinstance(candidates, list):
        warnings.append(
            ValidationIssue(
                path,
                f"{label} has incomplete {NEAREST_INTERMEDIATE_SEARCH_KEY!r}; "
                "set searched: true and list candidate_edges_considered even "
                "when the final decision is to keep the claim out of graph.",
            )
        )


def _validate_adjudication_edge_list(
    path: Path,
    label: str,
    record: dict[str, Any],
    field: str,
    errors: list[ValidationIssue],
    warnings: list[ValidationIssue],
) -> None:
    """Validate emitted/remove edge records inside one adjudication."""
    edge_list = record.get(field)
    if edge_list is None:
        return
    if not isinstance(edge_list, list):
        errors.append(
            ValidationIssue(path, f"{label} has {field!r} that is not a list.")
        )
        return
    for edge_index, edge in enumerate(edge_list, start=1):
        edge_label = f"{label} {field} edge {edge_index}"
        if not isinstance(edge, dict):
            errors.append(ValidationIssue(path, f"{edge_label} is not a mapping."))
            continue
        for edge_field in ADJUDICATION_EDGE_FIELDS:
            if edge_field not in edge:
                errors.append(
                    ValidationIssue(
                        path,
                        f"{edge_label} is missing {edge_field!r}.",
                    )
                )
        rel = edge.get("rel")
        if rel is not None and str(rel) not in REL_COLOR:
            errors.append(
                ValidationIssue(path, f"{edge_label} has unknown rel: {rel!r}.")
            )
        evidence = edge.get("evidence_strength")
        if evidence is not None and str(evidence) not in EVIDENCE_STYLES:
            warnings.append(
                ValidationIssue(
                    path,
                    f"{edge_label} has unknown evidence_strength: {evidence!r}.",
                )
            )


def _warn_unadjudicated_hidden_candidates(
    path: Path,
    claim_records: dict[str, dict[str, Any]],
    adjudications: list[dict[str, Any]],
    warnings: list[ValidationIssue],
) -> None:
    """Warn when graph-useful hidden claims have not been adjudicated."""
    if not claim_records:
        return

    adjudicated_claim_ids = {
        str(record.get("claim_id"))
        for record in adjudications
        if record.get("claim_id") is not None
    }
    for claim_id, claim in sorted(claim_records.items()):
        branch_type = str(claim.get(BRANCH_TYPE_KEY, ""))
        if not _claim_graph_candidate(claim):
            continue
        if str(claim.get("disposition", "")) not in {"context_only", "insufficient"}:
            continue
        if claim_id in adjudicated_claim_ids:
            continue
        message = (
            f"claim {claim_id!r} is a hidden graph candidate without an "
            f"{ADJUDICATIONS_KEY} record; add a structured adjudication before "
            "freezing the draft."
        )
        if branch_type in BRANCHES_REQUIRING_ADJUDICATION:
            message += f" Branch {branch_type!r} is high priority for review."
        warnings.append(ValidationIssue(path, message))

def _validate_paper_scopes(
    path: Path,
    data: dict[str, Any],
    warnings: list[ValidationIssue],
) -> dict[str, str]:
    """Validate optional paper_scope values and return paper_id to scope."""
    paper_scopes: dict[str, str] = {}
    paper_block = data.get("paper")
    if not isinstance(paper_block, dict):
        return paper_scopes

    for paper_id, paper in paper_block.items():
        if not isinstance(paper, dict):
            continue
        scope = paper.get(PAPER_SCOPE_KEY)
        if scope is None:
            continue
        scope_text = str(scope)
        paper_scopes[str(paper_id)] = scope_text
        if scope_text not in ALLOWED_PAPER_SCOPES:
            warnings.append(
                ValidationIssue(
                    path,
                    f"paper {paper_id!r} has unknown paper_scope: "
                    f"{scope_text!r}.",
                )
            )

    return paper_scopes


def _validate_edge_claim_links(
    path: Path,
    label: str,
    edge: dict[Any, Any],
    claim_records: dict[str, dict[str, Any]],
    require_claim_support: bool,
    errors: list[ValidationIssue],
    warnings: list[ValidationIssue],
) -> set[str]:
    """Validate optional edge-to-claim provenance links."""
    support_claims = edge.get(SUPPORT_CLAIMS_KEY)
    if support_claims is None:
        if require_claim_support:
            warnings.append(
                ValidationIssue(path, f"{label} is missing support_claims.")
            )
        return set()

    if not isinstance(support_claims, list) or not support_claims:
        errors.append(
            ValidationIssue(
                path,
                f"{label} has support_claims that is not a non-empty list.",
            )
        )
        return set()

    linked_claim_ids = {str(claim_id) for claim_id in support_claims}

    unknown_claims = [
        str(claim_id)
        for claim_id in support_claims
        if str(claim_id) not in claim_records
    ]
    if unknown_claims:
        errors.append(
            ValidationIssue(
                path,
                f"{label} references unknown support_claims: "
                f"{', '.join(unknown_claims)}.",
            )
        )

    for claim_id in linked_claim_ids & set(claim_records):
        claim = claim_records[claim_id]
        disposition = str(claim.get("disposition", ""))
        if disposition not in EDGE_SUPPORTING_CLAIM_DISPOSITIONS:
            warnings.append(
                ValidationIssue(
                    path,
                    f"{label} links to claim {claim_id!r} with disposition "
                    f"{disposition!r}; edge links should use claims marked "
                    "'edge' or 'negative'.",
                )
            )

    return linked_claim_ids - set(unknown_claims)


def _warn_scope_edge_mismatches(
    path: Path,
    label: str,
    edge: dict[Any, Any],
    paper_scopes: dict[str, str],
    warnings: list[ValidationIssue],
) -> None:
    """Warn when correlative papers emit causal edge relationships."""
    rel = edge.get("rel")
    if rel not in CAUSAL_EDGE_RELS:
        return

    papers = edge.get("papers")
    if not isinstance(papers, list):
        return

    flagged_scopes = sorted(
        {
            paper_scopes.get(str(paper_id))
            for paper_id in papers
            if paper_scopes.get(str(paper_id)) in CORRELATIVE_PAPER_SCOPES
        }
    )
    if not flagged_scopes:
        return

    warnings.append(
        ValidationIssue(
            path,
            f"{label} uses causal rel {rel!r} for paper_scope(s) "
            f"{', '.join(flagged_scopes)}; verify direct perturbation "
            "support or downgrade to a correlative/negative relation.",
        )
    )


def _warn_claim_evidence_mismatches(
    path: Path,
    label: str,
    edge: dict[Any, Any],
    claim_records: dict[str, dict[str, Any]],
    linked_claim_ids: set[str],
    adjudications: list[dict[str, Any]],
    warnings: list[ValidationIssue],
) -> None:
    """Warn when linked claim metadata conflicts with evidence strength."""
    if not linked_claim_ids:
        return

    linked_claims = [
        claim_records[claim_id]
        for claim_id in sorted(linked_claim_ids)
        if claim_id in claim_records
    ]
    if not linked_claims:
        return

    evidence_strength = str(edge.get("evidence_strength", ""))
    evidence_adjudicated = _has_edge_adjudication(
        adjudications, edge, "evidence_strength_warning"
    )
    has_perturbation = _claims_have_field(linked_claims, "perturbation")
    has_measured_readout = _claims_have_field(linked_claims, "measured_readout")

    if evidence_strength == "perturbation_supported" and not has_perturbation:
        warnings.append(
            ValidationIssue(
                path,
                f"{label} is perturbation_supported but its linked claims do "
                "not record a structured perturbation; add one or downgrade "
                "the evidence strength.",
            )
        )

    if evidence_strength == "perturbation_supported" and not has_measured_readout:
        warnings.append(
            ValidationIssue(
                path,
                f"{label} is perturbation_supported but its linked claims do "
                "not record a structured measured_readout; add the readout "
                "or verify this is not only canonical continuity.",
            )
        )

    if evidence_strength == "direct_measured" and not has_measured_readout:
        warnings.append(
            ValidationIssue(
                path,
                f"{label} is direct_measured but its linked claims do not "
                "record a structured measured_readout; add one or verify "
                "that direct measurement is justified by support text.",
            )
        )

    if (
        evidence_strength == "canonical_inferred"
        and has_perturbation
        and has_measured_readout
        and not evidence_adjudicated
    ):
        warnings.append(
            ValidationIssue(
                path,
                f"{label} is canonical_inferred but links to claims with both "
                "perturbation and measured_readout metadata; verify this was "
                "not under-called as canonical.",
            )
        )

    if (
        evidence_strength == "direct_measured"
        and has_perturbation
        and has_measured_readout
        and not evidence_adjudicated
    ):
        warnings.append(
            ValidationIssue(
                path,
                f"{label} is direct_measured but links to claims with both "
                "perturbation and measured_readout metadata; verify whether "
                "perturbation_supported is the normalized evidence class.",
            )
        )

    if (
        evidence_strength in OVERCONFIDENT_EVIDENCE_STRENGTHS
        and _edge_or_claim_text_contains(
            edge,
            linked_claims,
            CAUSAL_UNCERTAINTY_PHRASES,
        )
        and not evidence_adjudicated
    ):
        warnings.append(
            ValidationIssue(
                path,
                f"{label} has {evidence_strength!r} evidence but its edge or "
                "claim text contains causal-uncertainty language; verify the "
                "edge is not overconfident.",
            )
        )


def _warn_claim_edge_semantic_support(
    path: Path,
    label: str,
    edge: dict[Any, Any],
    claim_records: dict[str, dict[str, Any]],
    claim_edge_matrix: dict[str, list[dict[str, Any]]],
    linked_claim_ids: set[str],
    warnings: list[ValidationIssue],
) -> None:
    """Warn when support_claims do not entail the exact edge.

    `support_claims` alone only proves traceability. The optional
    `claim_edge_matrix` and claim `affected_entities` fields make the support
    contract explicit enough to catch broad-claim reuse and collapsed branches.
    """
    if not linked_claim_ids:
        return

    claims = [
        claim_records[claim_id]
        for claim_id in sorted(linked_claim_ids)
        if claim_id in claim_records
    ]
    matrix_claim_ids = [
        claim_id for claim_id in linked_claim_ids if claim_edge_matrix.get(claim_id)
    ]
    if matrix_claim_ids:
        if not any(
            _mapped_edge_matches(edge, mapped_edge)
            for claim_id in matrix_claim_ids
            for mapped_edge in claim_edge_matrix[claim_id]
        ):
            warnings.append(
                ValidationIssue(
                    path,
                    f"{label} links to claims with {CLAIM_EDGE_MATRIX_KEY} "
                    "entries, but none match this exact source/target/rel; "
                    "update the matrix or split the claim.",
                )
            )
        return

    affected_entity_claims = [
        claim for claim in claims if _claim_list_values(claim, "affected_entities")
    ]
    if not affected_entity_claims:
        return

    source = str(edge.get("source", ""))
    target = str(edge.get("target", ""))
    if any(
        {source, target}.issubset(_claim_list_values(claim, "affected_entities"))
        for claim in affected_entity_claims
    ):
        return

    if str(edge.get("evidence_strength", "")) in {
        "direct_measured",
        "perturbation_supported",
    }:
        warnings.append(
            ValidationIssue(
                path,
                f"{label} has high-confidence evidence but no linked claim "
                "lists both edge endpoints in affected_entities and no "
                f"{CLAIM_EDGE_MATRIX_KEY} entry maps the exact edge; verify "
                "the claim really supports this relationship.",
            )
        )


def _warn_broad_claim_reuse(
    path: Path,
    claim_reference_counts: collections.Counter[str],
    claim_edge_matrix: dict[str, list[dict[str, Any]]],
    warnings: list[ValidationIssue],
) -> None:
    """Warn when one claim supports many edges without a typed matrix."""
    for claim_id, count in sorted(claim_reference_counts.items()):
        if count <= CLAIM_REUSE_WARNING_THRESHOLD:
            continue
        if claim_edge_matrix.get(claim_id):
            continue
        warnings.append(
            ValidationIssue(
                path,
                f"claim {claim_id!r} supports {count} edges without a "
                f"{CLAIM_EDGE_MATRIX_KEY} entry; broad claim reuse can hide "
                "branch collapse or evidence-strength drift.",
            )
        )


def _mapped_edge_matches(
    edge: dict[Any, Any],
    mapped_edge: dict[str, Any],
) -> bool:
    """Return whether a matrix mapped edge matches a final edge."""
    for field in ("source", "target", "rel"):
        if str(edge.get(field, "")) != str(mapped_edge.get(field, "")):
            return False

    mapped_evidence = mapped_edge.get("evidence_strength")
    if mapped_evidence is None:
        return True
    return str(edge.get("evidence_strength", "")) == str(mapped_evidence)


def _claim_list_values(claim: dict[str, Any], field: str) -> set[str]:
    """Return a string set from a list-valued claim field."""
    values = claim.get(field)
    if isinstance(values, list):
        return {str(value) for value in values}
    if values is None:
        return set()
    return {str(values)}


def _claim_graph_candidate(claim: dict[str, Any]) -> bool:
    """Return whether a claim is marked as graph-useful."""
    value = claim.get(GRAPH_CANDIDATE_KEY)
    if isinstance(value, bool):
        return value
    if value is None:
        return str(claim.get(BRANCH_TYPE_KEY, "")) in GRAPH_CANDIDATE_BRANCH_TYPES
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _warn_relationship_review_patterns(
    path: Path,
    label: str,
    edge: dict[Any, Any],
    adjudications: list[dict[str, Any]],
    warnings: list[ValidationIssue],
) -> None:
    """Warn on relationship verbs that commonly drift during curation."""
    rel = str(edge.get("rel", ""))
    target = str(edge.get("target", ""))
    if _has_edge_adjudication(adjudications, edge, "verb_warning"):
        return

    if rel == "drives" and target in DRIVES_TARGET_VERB_REVIEW:
        warnings.append(
            ValidationIssue(
                path,
                f"{label} uses 'drives' into {target!r}; review whether "
                "'induces' better represents a trigger-to-state/program edge.",
            )
        )

    if rel == "causes" and target in CAUSES_TARGET_VERB_REVIEW:
        warnings.append(
            ValidationIssue(
                path,
                f"{label} uses broad causal verb 'causes' into {target!r}; "
                "prefer 'induces', 'drives', or 'activates' unless proximal "
                "physical/biochemical causation is being encoded.",
            )
        )



def _warn_topology_review_patterns(
    path: Path,
    label: str,
    edge: dict[Any, Any],
    claim_records: dict[str, dict[str, Any]],
    linked_claim_ids: set[str],
    adjudications: list[dict[str, Any]],
    warnings: list[ValidationIssue],
) -> None:
    """Warn on graph topology patterns that repeatedly caused misses."""
    source = str(edge.get("source", ""))
    target = str(edge.get("target", ""))
    rel = str(edge.get("rel", ""))

    if _is_reagent_only_endpoint(source) or _is_reagent_only_endpoint(target):
        if not _has_edge_adjudication(adjudications, edge, "reagent_endpoint_warning"):
            reagent = source if _is_reagent_only_endpoint(source) else target
            warnings.append(
                ValidationIssue(
                    path,
                    f"{label} uses reagent-only node {reagent!r} "
                    "as a graph endpoint; keep experimental reagents in context unless an adjudication overrides this.",
                )
            )

    if _is_generic_sensing_process(source) and _is_specific_component_node(target):
        if not _has_edge_adjudication(adjudications, edge, "topology_lint"):
            warnings.append(
                ValidationIssue(
                    path,
                    f"{label} makes generic process {source!r} activate specific component {target!r}; "
                    "prefer ligand-to-component edges when specific receptors/adaptors are implicated.",
                )
            )

    if (
        rel == "activates"
        and target in {"SPI1"}
        and not _has_edge_adjudication(adjudications, edge, "verb_warning")
    ):
        warnings.append(
            ValidationIssue(
                path,
                f"{label} uses 'activates' for gene/program abundance target {target!r}; "
                "review whether 'upregulates' is the normalized relation.",
            )
        )

    if (
        source == "epigenetic_remodeling"
        and target == "retrotransposon_derepression"
        and rel == "induces"
        and not _has_edge_adjudication(adjudications, edge, "verb_warning")
    ):
        warnings.append(
            ValidationIssue(
                path,
                f"{label} uses 'induces' for epigenetic_remodeling -> retrotransposon_derepression; "
                "review whether 'drives' is the normalized relation for this chromatin-program edge.",
            )
        )

    if linked_claim_ids and _edge_links_hidden_warning_claim(edge, claim_records, linked_claim_ids):
        if not _has_edge_adjudication(adjudications, edge, "evidence_strength_warning"):
            warnings.append(
                ValidationIssue(
                    path,
                    f"{label} links to claims whose branch/disposition suggests a hidden or uncertain branch; "
                    f"add {ADJUDICATIONS_KEY} if keeping the edge unchanged.",
                )
            )


def _warn_cross_edge_topology_patterns(
    path: Path,
    edges: Any,
    adjudications: list[dict[str, Any]],
    warnings: list[ValidationIssue],
) -> None:
    """Warn on multi-edge topology motifs that should be adjudicated."""
    if not isinstance(edges, list):
        return
    triples = {
        (str(edge.get("source", "")), str(edge.get("rel", "")), str(edge.get("target", "")))
        for edge in edges
        if isinstance(edge, dict)
    }
    if _has_issue_type_adjudication(adjudications, "topology_lint"):
        return

    for ligand, rel, sensing_process in sorted(triples):
        if rel != "activates" or not _is_generic_sensing_process(sensing_process):
            continue
        generic_to_components = [
            target
            for source, process_rel, target in sorted(triples)
            if source == sensing_process
            and process_rel == "activates"
            and _is_specific_component_node(target)
        ]
        if not generic_to_components:
            continue
        warnings.append(
            ValidationIssue(
                path,
                "topology_lint: "
                f"{ligand} is routed through generic process {sensing_process} "
                f"before {', '.join(generic_to_components)}; adjudicate whether "
                "to replace this with direct ligand-to-component edges.",
            )
        )


def _is_reagent_only_endpoint(node: str) -> bool:
    """Return whether a node looks like an assay reagent rather than a graph node."""
    return node in REAGENT_ONLY_ENDPOINTS or any(
        node.startswith(prefix) for prefix in REAGENT_ENDPOINT_PREFIXES
    )


def _is_generic_sensing_process(node: str) -> bool:
    """Return whether a node is a generic sensing process."""
    return node in GENERIC_PROCESS_NODES or node.endswith(SENSING_PROCESS_SUFFIX)


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

def _edge_links_hidden_warning_claim(
    edge: dict[Any, Any],
    claim_records: dict[str, dict[str, Any]],
    linked_claim_ids: set[str],
) -> bool:
    """Return whether linked claims carry hidden-branch risk metadata."""
    for claim_id in linked_claim_ids:
        claim = claim_records.get(claim_id)
        if claim is None:
            continue
        if str(claim.get("disposition", "")) in {"context_only", "insufficient"}:
            return True
    return False


def _has_edge_adjudication(
    adjudications: list[dict[str, Any]],
    edge: dict[Any, Any],
    issue_type: str,
) -> bool:
    """Return whether adjudications mention this edge and issue type."""
    for record in adjudications:
        if str(record.get(ISSUE_TYPE_KEY, "")) != issue_type:
            continue
        for field in (EMITTED_EDGES_KEY, REMOVE_EDGES_KEY, "edge"):
            value = record.get(field)
            records = value if isinstance(value, list) else [value]
            for candidate in records:
                if isinstance(candidate, dict) and _edge_identity_matches(edge, candidate):
                    return True
    return False


def _has_issue_type_adjudication(
    adjudications: list[dict[str, Any]],
    issue_type: str,
) -> bool:
    """Return whether any adjudication records this issue type."""
    return any(str(record.get(ISSUE_TYPE_KEY, "")) == issue_type for record in adjudications)


def _edge_identity_matches(edge: dict[Any, Any], candidate: dict[str, Any]) -> bool:
    """Return whether source/target/rel identify the same edge."""
    return all(
        str(edge.get(field, "")) == str(candidate.get(field, ""))
        for field in ("source", "target", "rel")
    )

def _warn_unreferenced_edge_claims(
    path: Path,
    claim_records: dict[str, dict[str, Any]],
    referenced_claim_ids: set[str],
    warnings: list[ValidationIssue],
) -> None:
    """Warn when an edge-bearing claim is not mapped to any edge."""
    for claim_id, claim in sorted(claim_records.items()):
        disposition = str(claim.get("disposition", ""))
        if (
            disposition in EDGE_SUPPORTING_CLAIM_DISPOSITIONS
            and claim_id not in referenced_claim_ids
        ):
            warnings.append(
                ValidationIssue(
                    path,
                    f"claim {claim_id!r} is marked {disposition!r} but is "
                    "not referenced by any edge; add an edge, change the "
                    "disposition, or document why it was rejected.",
                )
            )


def _claims_have_field(claims: list[dict[str, Any]], field: str) -> bool:
    """Return whether any linked claim has a non-empty structured field."""
    empty_values = {"", "none", "n/a", "na", "not_applicable"}
    return any(
        str(claim.get(field, "")).strip().lower() not in empty_values
        for claim in claims
    )


def _edge_or_claim_text_contains(
    edge: dict[Any, Any],
    claims: list[dict[str, Any]],
    phrases: tuple[str, ...],
) -> bool:
    """Return whether edge/claim prose contains any review-risk phrase."""
    text_parts = [str(edge.get("context", "")), str(edge.get("support", ""))]
    for claim in claims:
        text_parts.extend(
            [
                str(claim.get("claim", "")),
                str(claim.get("support", "")),
            ]
        )
    text = "\n".join(text_parts).lower()
    return any(phrase in text for phrase in phrases)


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
    *,
    claim_records: dict[str, dict[str, Any]],
    claim_edge_matrix: dict[str, list[dict[str, Any]]],
    adjudications: list[dict[str, Any]],
    paper_scopes: dict[str, str],
    require_claim_support: bool,
) -> None:
    """Validate edge-level schema, controlled vocabulary, and curation hints."""
    if not isinstance(edges, list):
        return

    referenced_claim_ids: set[str] = set()
    claim_reference_counts: collections.Counter[str] = collections.Counter()
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
        linked_claim_ids = _validate_edge_claim_links(
            path,
            label,
            edge,
            claim_records,
            require_claim_support,
            errors,
            warnings,
        )
        referenced_claim_ids.update(linked_claim_ids)
        claim_reference_counts.update(linked_claim_ids)
        _warn_claim_evidence_mismatches(
            path,
            label,
            edge,
            claim_records,
            linked_claim_ids,
            adjudications,
            warnings,
        )
        _warn_claim_edge_semantic_support(
            path,
            label,
            edge,
            claim_records,
            claim_edge_matrix,
            linked_claim_ids,
            warnings,
        )
        if require_claim_support:
            _warn_relationship_review_patterns(
                path, label, edge, adjudications, warnings
            )
            _warn_topology_review_patterns(
                path,
                label,
                edge,
                claim_records,
                linked_claim_ids,
                adjudications,
                warnings,
            )
        _warn_scope_edge_mismatches(path, label, edge, paper_scopes, warnings)
        _warn_undeclared_entities(
            path, label, edge, declared_entities, warnings
        )
        _warn_duplicate_edge(path, label, edge, seen_edges, warnings)

    if require_claim_support:
        _warn_cross_edge_topology_patterns(
            path,
            edges,
            adjudications,
            warnings,
        )
    _warn_unreferenced_edge_claims(
        path,
        claim_records,
        referenced_claim_ids,
        warnings,
    )
    _warn_broad_claim_reuse(
        path,
        claim_reference_counts,
        claim_edge_matrix,
        warnings,
    )


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

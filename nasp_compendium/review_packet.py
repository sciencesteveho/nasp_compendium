"""Build lightweight human-review packets for curated NASP drafts."""

from __future__ import annotations

import collections
import tempfile
from pathlib import Path
from typing import Any

import yaml  # type: ignore

from nasp_compendium import validate_compendium


BRANCH_TYPE_KEY: str = "branch_type"
ADJUDICATIONS_KEY: str = "adjudications"
ISSUE_TYPE_KEY: str = "issue_type"
DECISION_KEY: str = "decision"
CURATION_DENSITY_KEY: str = "curation_density"
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
SENSOR_COMPONENT_NODES: frozenset[str] = frozenset({"DDX58", "IFIH1"})


def build_review_packet(input_path: Path) -> str:
    """Return a Markdown review packet for a draft file or directory.

    Args:
      input_path: Single YAML-in-Markdown draft file or directory containing
        draft files.

    Returns:
      Markdown text summarizing validation, provenance, and review hotspots.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Review input not found: {input_path}")

    data_by_path = _load_review_data(input_path)
    validation_result = _validate_input(input_path)

    lines: list[str] = ["# NASP curation review packet", ""]
    lines.extend(_format_validation_summary(validation_result))

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

    Args:
      input_path: Single draft file or directory of draft files.

    Returns:
      Human-readable validation/pre-freeze blockers. An empty list means the
      draft input is ready for freeze.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Review input not found: {input_path}")

    blockers = [
        f"validation_error: {issue.path}: {issue.message}"
        for issue in _validate_input(input_path).errors
    ]
    for path, data in sorted(_load_review_data(input_path).items()):
        blockers.extend(
            f"{path.name}: {blocker}" for blocker in _pre_freeze_blockers(data)
        )
    return blockers


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
    lines.extend(_format_paper_scopes(data))
    lines.extend(_format_pre_freeze_status(data))
    lines.extend(_format_claim_summary(data))
    lines.extend(_format_entity_resolution_summary(data))
    lines.extend(_format_edge_summary(data))
    lines.extend(_format_adjudication_summary(data))
    lines.extend(_format_branch_coverage(data))
    lines.extend(_format_topology_lints(data))
    lines.extend(_format_association_balance(data))
    lines.extend(_format_density_review(data))
    lines.extend(_format_review_hotspots(data))
    return lines


def _format_paper_scopes(data: dict[str, Any]) -> list[str]:
    """Format paper ids and scope labels."""
    paper_block = data.get("paper")
    if not isinstance(paper_block, dict):
        return ["### Paper scope", "", "- Missing `paper` block.", ""]

    lines = ["### Paper scope", ""]
    for paper_id, paper in paper_block.items():
        scope = "not_set"
        if isinstance(paper, dict):
            scope = str(paper.get("paper_scope", "not_set"))
        lines.append(f"- `{paper_id}`: `{scope}`")
    lines.append("")
    return lines


def _format_pre_freeze_status(data: dict[str, Any]) -> list[str]:
    """Format a blocking pre-freeze status from review findings."""
    blockers = _pre_freeze_blockers(data)
    lines = ["### Pre-freeze status", ""]
    if blockers:
        lines.extend(
            ("- Status: `BLOCKED`", f"- Blocking issues: {len(blockers)}", "")
        )
        lines.extend(f"- {blocker}" for blocker in blockers[:15])
    else:
        lines.extend(("- Status: `READY_FOR_FREEZE`", "- Blocking issues: 0"))
    lines.append("")
    return lines


def _format_adjudication_summary(data: dict[str, Any]) -> list[str]:
    """Format structured adjudication records."""
    adjudications = data.get(ADJUDICATIONS_KEY)
    if not isinstance(adjudications, list):
        return [
            "### Adjudications",
            "",
            f"- No `{ADJUDICATIONS_KEY}` block present.",
            "",
        ]

    issue_counts = collections.Counter(
        str(record.get(ISSUE_TYPE_KEY, "not_set"))
        for record in adjudications
        if isinstance(record, dict)
    )
    decision_counts = collections.Counter(
        str(record.get(DECISION_KEY, "not_set"))
        for record in adjudications
        if isinstance(record, dict)
    )

    lines = ["### Adjudications", "", f"- Records: {len(adjudications)}"]
    if issue_counts:
        lines.extend(("", "Issue types:"))
        lines.extend(
            f"- `{issue_type}`: {count}"
            for issue_type, count in sorted(issue_counts.items())
        )
    if decision_counts:
        lines.extend(("", "Decisions:"))
        lines.extend(
            f"- `{decision}`: {count}"
            for decision, count in sorted(decision_counts.items())
        )
    lines.append("")
    return lines


def _format_claim_summary(data: dict[str, Any]) -> list[str]:
    """Format raw-claim provenance coverage."""
    claims = data.get("claims")
    if not isinstance(claims, list):
        return ["### Claims", "", "- No `claims` block present.", ""]

    lines = ["### Claims", "", f"- Claim records: {len(claims)}"]
    if disposition_counts := collections.Counter(
        str(claim.get("disposition", "not_set"))
        for claim in claims
        if isinstance(claim, dict)
    ):
        lines.extend(("", "Claim dispositions:"))
        lines.extend(
            f"- `{disposition}`: {count}"
            for disposition, count in sorted(disposition_counts.items())
        )
    if branch_counts := collections.Counter(
        str(claim.get(BRANCH_TYPE_KEY, "not_set"))
        for claim in claims
        if isinstance(claim, dict)
    ):
        lines.extend(("", "Claim branch types:"))
        lines.extend(
            f"- `{branch_type}`: {count}"
            for branch_type, count in sorted(branch_counts.items())
        )
    if graph_candidate_counts := collections.Counter(
        str(_claim_graph_candidate(claim))
        for claim in claims
        if isinstance(claim, dict)
    ):
        lines.extend(("", "Graph candidates:"))
        lines.extend(
            f"- `{graph_candidate}`: {count}"
            for graph_candidate, count in sorted(graph_candidate_counts.items())
        )
    claim_locations = collections.Counter(
        str(claim.get("evidence_location", "not_set"))
        for claim in claims
        if isinstance(claim, dict)
    )
    lines.extend(("", "Evidence locations:"))
    lines.extend(
        f"- `{location}`: {count}"
        for location, count in claim_locations.most_common(8)
    )
    lines.append("")
    return lines


def _format_entity_resolution_summary(data: dict[str, Any]) -> list[str]:
    """Format entity-resolution decision counts."""
    records = data.get("entity_resolution")
    if not isinstance(records, list):
        return [
            "### Entity resolution",
            "",
            "- No `entity_resolution` block present.",
            "",
        ]

    status_counts = collections.Counter(
        str(record.get("status", "not_set"))
        for record in records
        if isinstance(record, dict)
    )
    lines = ["### Entity resolution", ""]
    lines.extend(
        f"- `{status}`: {count}"
        for status, count in sorted(status_counts.items())
    )
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


def _format_branch_coverage(data: dict[str, Any]) -> list[str]:
    """Format branch-level claim coverage by final graph edges."""
    claims_by_id = _claims_by_id(data)
    edges = data.get("edges")
    if not claims_by_id or not isinstance(edges, list):
        return []

    referenced_claim_ids = _referenced_claim_ids(edges)
    branch_claims: dict[str, list[tuple[str, dict[str, Any]]]] = (
        collections.defaultdict(list)
    )
    for claim_id, claim in claims_by_id.items():
        branch_type = str(claim.get(BRANCH_TYPE_KEY, "not_set"))
        branch_claims[branch_type].append((claim_id, claim))

    lines = ["### Branch coverage", ""]
    for branch_type in sorted(branch_claims):
        records = branch_claims[branch_type]
        graph_candidates = [
            claim_id
            for claim_id, claim in records
            if _claim_graph_candidate(claim)
        ]
        represented = [
            claim_id
            for claim_id in graph_candidates
            if claim_id in referenced_claim_ids
        ]
        hidden = [
            claim_id
            for claim_id, claim in records
            if _claim_graph_candidate(claim)
            and str(claim.get("disposition", ""))
            in {"context_only", "insufficient"}
        ]
        lines.append(
            f"- `{branch_type}`: {len(records)} claims, "
            f"{len(graph_candidates)} graph candidates, "
            f"{len(represented)} represented, "
            f"{len(hidden)} hidden/rejected candidates"
        )

    if hidden_candidates := _hidden_graph_candidate_claims(claims_by_id):
        lines.extend(("", "Graph-candidate claims not emitted as edges:"))
        for claim_id in sorted(hidden_candidates)[:10]:
            claim = claims_by_id[claim_id]
            lines.append(
                f"- `{claim_id}` ({claim.get(BRANCH_TYPE_KEY, 'not_set')}, "
                f"{claim.get('disposition', 'not_set')})"
            )

    lines.append("")
    return lines


def _format_topology_lints(data: dict[str, Any]) -> list[str]:
    """Format topology lints derived from edge patterns."""
    lints = _topology_lints(data)
    lines = ["### Topology lints", ""]
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

    claims_by_id = _claims_by_id(data)
    referenced_claim_ids = _referenced_claim_ids(edges)
    missing_claim_links = (
        [
            edge
            for edge in edges
            if isinstance(edge, dict) and "support_claims" not in edge
        ]
        if claims_by_id
        else []
    )
    weak_support = [
        edge
        for edge in edges
        if isinstance(edge, dict)
        and str(edge.get("evidence_strength"))
        in {"canonical_inferred", "weak_correlative"}
    ]
    unreferenced_edge_claims = _unreferenced_edge_claims(
        claims_by_id,
        referenced_claim_ids,
    )
    overconfident_edges = _overconfident_edges(edges, claims_by_id)
    undercalled_edges = _undercalled_canonical_edges(edges, claims_by_id)
    verb_review_edges = _verb_review_edges(edges)
    matrix_support_gaps = _edges_without_matrix_support(
        data, edges, claims_by_id
    )
    broad_claim_reuse = _broadly_reused_claims(edges, data)
    hidden_graph_candidates = _hidden_graph_candidate_claims(claims_by_id)
    topology_lints = _topology_lints(data)
    unadjudicated_hidden = _unadjudicated_hidden_graph_candidates(data)
    blockers = _pre_freeze_blockers(data)

    lines = [
        "### Review hotspots",
        "",
        f"- Edges missing `support_claims`: {len(missing_claim_links)}",
        f"- Weak/canonical-inferred edges: {len(weak_support)}",
        f"- Edge/negative claims not referenced by any edge: {len(unreferenced_edge_claims)}",  # noqa: E501
        f"- Overconfident evidence-risk edges: {len(overconfident_edges)}",
        f"- Possibly under-called canonical edges: {len(undercalled_edges)}",
        f"- Verb-review edges: {len(verb_review_edges)}",
        f"- Edges without matching claim-edge matrix support: {len(matrix_support_gaps)}",  # noqa: E501
        f"- Broadly reused claims without matrix support: {len(broad_claim_reuse)}",  # noqa: E501
        f"- Hidden graph-candidate claims: {len(hidden_graph_candidates)}",
        f"- Unadjudicated hidden graph-candidate claims: {len(unadjudicated_hidden)}",  # noqa: E501
        f"- Topology lints: {len(topology_lints)}",
        f"- Pre-freeze blockers: {len(blockers)}",
    ]
    if weak_support:
        lines.extend(("", "Weak/canonical-inferred edge examples:"))
        for edge in weak_support[:10]:
            source = edge.get("source", "?")
            rel = edge.get("rel", "?")
            target = edge.get("target", "?")
            evidence_strength = edge.get("evidence_strength", "?")
            lines.append(
                f"- `{source}` --[{rel}/{evidence_strength}]--> `{target}`"
            )

    if overconfident_edges:
        lines.extend(("", "Overconfident evidence-risk examples:"))
        lines.extend(
            f"- {_format_edge_inline(edge)}"
            for edge in overconfident_edges[:10]
        )
    if undercalled_edges:
        lines.extend(("", "Possibly under-called canonical examples:"))
        lines.extend(
            f"- {_format_edge_inline(edge)}" for edge in undercalled_edges[:10]
        )
    if verb_review_edges:
        lines.extend(("", "Verb-review examples:"))
        lines.extend(
            f"- {_format_edge_inline(edge)}" for edge in verb_review_edges[:10]
        )
    if matrix_support_gaps:
        lines.extend(("", "Claim-edge matrix support gaps:"))
        lines.extend(
            f"- {_format_edge_inline(edge)}"
            for edge in matrix_support_gaps[:10]
        )
    if broad_claim_reuse:
        lines.extend(("", "Broadly reused claims without matrix support:"))
        lines.extend(
            f"- `{claim_id}`: {count} linked edges"
            for claim_id, count in broad_claim_reuse[:10]
        )
    if hidden_graph_candidates:
        lines.extend(("", "Hidden graph-candidate claims:"))
        for claim_id in sorted(hidden_graph_candidates)[:10]:
            claim = claims_by_id[claim_id]
            lines.append(
                f"- `{claim_id}` ({claim.get(BRANCH_TYPE_KEY, 'not_set')}, "
                f"{claim.get('disposition', 'not_set')})"
            )

    if unadjudicated_hidden:
        lines.extend(("", "Unadjudicated hidden graph-candidate claims:"))
        for claim_id in sorted(unadjudicated_hidden)[:10]:
            claim = claims_by_id[claim_id]
            lines.append(
                f"- `{claim_id}` ({claim.get(BRANCH_TYPE_KEY, 'not_set')}, "
                f"{claim.get('disposition', 'not_set')})"
            )

    if topology_lints:
        lines.extend(("", "Topology lint examples:"))
        lines.extend(f"- {lint}" for lint in topology_lints[:10])
    if blockers:
        lines.extend(("", "Pre-freeze blockers:"))
        lines.extend(f"- {blocker}" for blocker in blockers[:10])
    if unreferenced_edge_claims:
        lines.extend(("", "Unreferenced edge/negative claims:"))
        lines.extend(
            f"- `{claim_id}`"
            for claim_id in sorted(unreferenced_edge_claims)[:10]
        )
    lines.append("")
    return lines


def _claims_by_id(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Return claim records keyed by claim_id."""
    claims = data.get("claims")
    if not isinstance(claims, list):
        return {}
    records: dict[str, dict[str, Any]] = {
        str(claim["claim_id"]): claim
        for claim in claims
        if isinstance(claim, dict) and claim.get("claim_id") is not None
    }
    return records


def _referenced_claim_ids(edges: list[Any]) -> set[str]:
    """Return all support_claims referenced by edges."""
    claim_ids: set[str] = set()
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        support_claims = edge.get("support_claims")
        if isinstance(support_claims, list):
            claim_ids.update(str(claim_id) for claim_id in support_claims)
    return claim_ids


def _unreferenced_edge_claims(
    claims_by_id: dict[str, dict[str, Any]],
    referenced_claim_ids: set[str],
) -> set[str]:
    """Return edge-bearing claims that no edge references."""
    return {
        claim_id
        for claim_id, claim in claims_by_id.items()
        if str(claim.get("disposition", "")) in {"edge", "negative"}
        and claim_id not in referenced_claim_ids
    }


def _linked_claims(
    edge: dict[str, Any],
    claims_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return claim records linked from one edge."""
    support_claims = edge.get("support_claims")
    if not isinstance(support_claims, list):
        return []
    return [
        claims_by_id[str(claim_id)]
        for claim_id in support_claims
        if str(claim_id) in claims_by_id
    ]


def _overconfident_edges(
    edges: list[Any],
    claims_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return edges whose evidence label may overstate linked support."""
    if not claims_by_id:
        return []

    risky_edges: list[dict[str, Any]] = []
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        evidence_strength = str(edge.get("evidence_strength", ""))
        if evidence_strength not in {
            "direct_measured",
            "perturbation_supported",
        }:
            continue
        claims = _linked_claims(edge, claims_by_id)
        lacks_required_metadata = (
            evidence_strength == "perturbation_supported"
            and not _claims_have_field(claims, "perturbation")
        ) or (
            evidence_strength == "direct_measured"
            and not _claims_have_field(claims, "measured_readout")
        )
        if lacks_required_metadata or _contains_uncertainty_language(
            edge, claims
        ):
            risky_edges.append(edge)
    return risky_edges


def _undercalled_canonical_edges(
    edges: list[Any],
    claims_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return canonical edges linked to perturbation/readout claims."""
    if not claims_by_id:
        return []

    undercalled_edges: list[dict[str, Any]] = []
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        if str(edge.get("evidence_strength")) != "canonical_inferred":
            continue
        claims = _linked_claims(edge, claims_by_id)
        if _claims_have_field(claims, "perturbation") and _claims_have_field(
            claims,
            "measured_readout",
        ):
            undercalled_edges.append(edge)
    return undercalled_edges


def _evidence_strength_warning_edges(
    data: dict[str, Any],
) -> list[dict[str, Any]]:
    """Return edges that need evidence-class adjudication before freeze."""
    claims_by_id = _claims_by_id(data)
    if not claims_by_id:
        return []

    warning_edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for edge in _overconfident_edges(_edges_list(data), claims_by_id):
        key = _edge_identity_tuple(edge)
        if key not in seen:
            warning_edges.append(edge)
            seen.add(key)

    for edge in _edges_list(data):
        evidence_strength = str(edge.get("evidence_strength", ""))
        if evidence_strength not in {"canonical_inferred", "direct_measured"}:
            continue
        claims = _linked_claims(edge, claims_by_id)
        if not (
            _claims_have_field(claims, "perturbation")
            and _claims_have_field(claims, "measured_readout")
        ):
            continue
        key = _edge_identity_tuple(edge)
        if key in seen:
            continue
        warning_edges.append(edge)
        seen.add(key)
    return warning_edges


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


def _claims_have_field(claims: list[dict[str, Any]], field: str) -> bool:
    """Return whether any linked claim has a non-empty structured field."""
    empty_values = {"", "none", "n/a", "na", "not_applicable"}
    return any(
        str(claim.get(field, "")).strip().lower() not in empty_values
        for claim in claims
    )


def _claim_graph_candidate(
    claim: dict[str, Any],
    *,
    graph_candidate_key: str = "graph_candidate",
    graph_candidate_branch_types: frozenset[str] = frozenset(
        {
            "main_spine",
            "sensor_branch",
            "inflammatory_output",
            "cohort_association",
            "state_reversal",
            "negative_specificity",
            "organismal_outcome",
        }
    ),
) -> bool:
    """Return whether a claim is marked as graph-useful."""
    value = claim.get(graph_candidate_key)
    if isinstance(value, bool):
        return value
    if value is None:
        return (
            str(claim.get(BRANCH_TYPE_KEY, "")) in graph_candidate_branch_types
        )
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _hidden_graph_candidate_claims(
    claims_by_id: dict[str, dict[str, Any]],
) -> set[str]:
    """Return graph-useful claims not emitted as graph edges."""
    return {
        claim_id
        for claim_id, claim in claims_by_id.items()
        if _claim_graph_candidate(claim)
        and str(claim.get("disposition", ""))
        in {"context_only", "insufficient"}
    }


def _claim_edge_matrix(
    data: dict[str, Any],
    claim_edge_matrix_key: str = "claim_edge_matrix",
) -> dict[str, list[dict[str, Any]]]:
    """Return matrix mapped edges keyed by claim id."""
    matrix = data.get(claim_edge_matrix_key)
    if not isinstance(matrix, list):
        return {}

    mapped_by_claim: dict[str, list[dict[str, Any]]] = collections.defaultdict(
        list
    )
    for record in matrix:
        if not isinstance(record, dict) or record.get("claim_id") is None:
            continue
        mapped_edges = record.get("mapped_edges")
        if not isinstance(mapped_edges, list):
            continue
        mapped_by_claim[str(record["claim_id"])].extend(
            mapped_edge
            for mapped_edge in mapped_edges
            if isinstance(mapped_edge, dict)
        )
    return dict(mapped_by_claim)


def _edges_without_matrix_support(
    data: dict[str, Any],
    edges: list[Any],
    claims_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return edges linked to matrix claims with no exact matrix match."""
    matrix = _claim_edge_matrix(data)
    if not matrix:
        return []

    support_gaps: list[dict[str, Any]] = []
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        support_claims = edge.get("support_claims")
        if not isinstance(support_claims, list):
            continue
        matrix_claim_ids = [
            str(claim_id)
            for claim_id in support_claims
            if matrix.get(str(claim_id))
        ]
        if not matrix_claim_ids:
            continue
        if not any(
            _mapped_edge_matches(edge, mapped_edge)
            for claim_id in matrix_claim_ids
            for mapped_edge in matrix[claim_id]
        ):
            support_gaps.append(edge)
    return support_gaps


def _broadly_reused_claims(
    edges: list[Any],
    data: dict[str, Any],
    *,
    claim_reuse_warning_threshold: int = 3,
) -> list[tuple[str, int]]:
    """Return heavily reused support claims lacking matrix detail."""
    matrix = _claim_edge_matrix(data)
    claim_counts: collections.Counter[str] = collections.Counter()
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        support_claims = edge.get("support_claims")
        if isinstance(support_claims, list):
            claim_counts.update(str(claim_id) for claim_id in support_claims)
    return [
        (claim_id, count)
        for claim_id, count in sorted(claim_counts.items())
        if count > claim_reuse_warning_threshold and not matrix.get(claim_id)
    ]


def _mapped_edge_matches(
    edge: dict[str, Any],
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


def _contains_uncertainty_language(
    edge: dict[str, Any],
    claims: list[dict[str, Any]],
) -> bool:
    """Return whether edge or claim prose contains uncertainty phrases."""
    phrases = (
        "not directly perturbed",
        "not directly tested",
        "not directly measured",
        "no direct perturbation",
        "no direct evidence",
        "inferred",
        "proposed",
        "consistent with",
    )
    text_parts = [str(edge.get("context", "")), str(edge.get("support", ""))]
    for claim in claims:
        text_parts.extend(
            [str(claim.get("claim", "")), str(claim.get("support", ""))]
        )
    text = "\n".join(text_parts).lower()
    return any(phrase in text for phrase in phrases)


def _pre_freeze_blockers(data: dict[str, Any]) -> list[str]:
    """Return blocking issues that must be adjudicated before finalization."""
    blockers: list[str] = []
    claims_by_id = _claims_by_id(data)
    for claim_id in sorted(_unadjudicated_hidden_graph_candidates(data)):
        claim = claims_by_id[claim_id]
        branch = str(claim.get(BRANCH_TYPE_KEY, "not_set"))
        if branch in BRANCHES_REQUIRING_ADJUDICATION:
            blockers.append(
                f"hidden_graph_candidate `{claim_id}` ({branch}, "
                f"{claim.get('disposition', 'not_set')}) lacks adjudication"
            )

    blockers.extend(f"topology_lint: {lint}" for lint in _topology_lints(data))
    for edge in _verb_review_edges(_edges_list(data)):
        if not _adjudications_cover_edge(data, edge, "verb_warning"):
            blockers.append(f"verb_warning: {_format_edge_inline(edge)}")
        elif not _edge_adjudication_is_complete(data, edge, "verb_warning"):
            blockers.append(
                "incomplete verb_warning adjudication: "
                f"{_format_edge_inline(edge)}"
            )

    for edge in _evidence_strength_warning_edges(data):
        if not _adjudications_cover_edge(
            data, edge, "evidence_strength_warning"
        ):
            blockers.append(
                f"evidence_strength_warning: {_format_edge_inline(edge)}"
            )
        elif not _edge_adjudication_is_complete(
            data, edge, "evidence_strength_warning"
        ):
            blockers.append(
                "incomplete evidence_strength_warning adjudication: "
                f"{_format_edge_inline(edge)}"
            )

    blockers.extend(
        f"incomplete hidden_graph_candidate adjudication: `{claim_id}` "
        "needs nearest_intermediate_search"
        for claim_id in sorted(_incomplete_hidden_graph_adjudications(data))
    )
    blockers.extend(
        f"scope_density_warning: {warning}"
        for warning in _density_warnings(data)
        if not _adjudications_have_issue_type(data, "scope_density_warning")
    )
    blockers.extend(
        f"broad_claim_reuse: `{claim_id}` supports {count} edges without matrix"
        for claim_id, count in _broadly_reused_claims(_edges_list(data), data)
    )
    blockers.extend(
        f"claim_edge_matrix_gap: {_format_edge_inline(edge)}"
        for edge in _edges_without_matrix_support(
            data, _edges_list(data), claims_by_id
        )
    )
    return blockers


def _unadjudicated_hidden_graph_candidates(data: dict[str, Any]) -> set[str]:
    """Return hidden graph-candidate claims lacking adjudication records."""
    claims_by_id = _claims_by_id(data)
    hidden = _hidden_graph_candidate_claims(claims_by_id)
    adjudicated = {
        str(record.get("claim_id"))
        for record in _adjudications_list(data)
        if record.get("claim_id") is not None
    }
    return hidden - adjudicated


def _incomplete_hidden_graph_adjudications(
    data: dict[str, Any],
    *,
    nearest_intermediate_search_key: str = "nearest_intermediate_search",
    candidate_edges_considered_key: str = "candidate_edges_considered",
) -> set[str]:
    """Return hidden claim adjudications missing nearest-intermediate search."""
    claims_by_id = _claims_by_id(data)
    hidden = _hidden_graph_candidate_claims(claims_by_id)
    incomplete: set[str] = set()
    for claim_id in hidden:
        claim = claims_by_id[claim_id]
        if (
            str(claim.get(BRANCH_TYPE_KEY, ""))
            not in BRANCHES_REQUIRING_ADJUDICATION
        ):
            continue
        record = _claim_adjudication_record(
            data, claim_id, "hidden_graph_candidate"
        )
        if record is None:
            continue
        if str(record.get(DECISION_KEY, "")) not in {
            "keep_context",
            "keep_insufficient",
            "keep_as_is",
        }:
            continue
        nearest_search = record.get(nearest_intermediate_search_key)
        if not isinstance(nearest_search, dict):
            incomplete.add(claim_id)
            continue
        searched = nearest_search.get("searched")
        searched_bool = searched is True or str(searched).lower() in {
            "true",
            "1",
            "yes",
        }
        candidates = nearest_search.get(candidate_edges_considered_key)
        if not searched_bool or not isinstance(candidates, list):
            incomplete.add(claim_id)
    return incomplete


def _claim_adjudication_record(
    data: dict[str, Any],
    claim_id: str,
    issue_type: str,
) -> dict[str, Any] | None:
    """Return the first adjudication for a claim and issue type."""
    for record in _adjudications_list(data):
        if str(record.get(ISSUE_TYPE_KEY, "")) != issue_type:
            continue
        if str(record.get("claim_id", "")) == claim_id:
            return record
    return None


def _topology_lints(data: dict[str, Any]) -> list[str]:
    """Return lightweight topology lints for repeated NASP failure modes."""
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

    generic_routes: list[tuple[str, str, list[str]]] = []
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
            generic_routes.append((ligand, sensing_process, components))

    if generic_routes and not _adjudications_have_issue_type(
        data, "topology_lint"
    ):
        lints.extend(
            f"{ligand} is routed through generic process {sensing_process} "
            f"before {', '.join(components)}; review"
            " direct ligand-to-component edges."
            for ligand, sensing_process, components in generic_routes
        )
    for edge in edges:
        source = str(edge.get("source", ""))
        target = str(edge.get("target", ""))
        rel = str(edge.get("rel", ""))
        if (
            _is_reagent_only_endpoint(source)
            or _is_reagent_only_endpoint(target)
        ) and not _adjudications_cover_edge(
            data, edge, "reagent_endpoint_warning"
        ):
            reagent = source if _is_reagent_only_endpoint(source) else target
            lints.append(
                f"reagent-only endpoint `{reagent}` appears"
                f" in {_format_edge_inline(edge)}"
            )
        if (
            _is_generic_sensing_process(source)
            and _is_specific_component_node(target)
            and not _adjudications_cover_edge(data, edge, "topology_lint")
        ):
            lints.append(
                f"generic process-to-component edge {_format_edge_inline(edge)}"
            )
        if rel == "activates" and target in {"SPI1"}:
            lints.append(
                f"verb normalization: {_format_edge_inline(edge)}"
                " may need `upregulates`"
            )
        if (
            source == "epigenetic_remodeling"
            and target == "retrotransposon_derepression"
            and rel == "induces"
        ):
            lints.append(
                f"verb normalization: {_format_edge_inline(edge)}"
                " may need `drives`"
            )
    return lints


def _format_association_balance(data: dict[str, Any]) -> list[str]:
    """Format association-recall warnings for correlative/resource papers."""
    warnings = _association_balance_warnings(data)
    lines = ["### Association balance", ""]
    if warnings:
        lines.extend(f"- {warning}" for warning in warnings)
    else:
        lines.append("- No association-balance warnings.")
    lines.append("")
    return lines


def _format_density_review(data: dict[str, Any]) -> list[str]:
    """Format core/expanded density warnings for resource papers."""
    warnings = _density_warnings(data)
    lines = [
        "### Curation density",
        "",
        f"- Density: `{_curation_density(data)}`",
    ]
    if warnings:
        lines.extend(f"- {warning}" for warning in warnings)
    else:
        lines.append("- No curation-density warnings.")
    lines.append("")
    return lines


def _association_balance_warnings(data: dict[str, Any]) -> list[str]:
    """Return recall-smell warnings for one-sided association extraction."""
    if not _is_correlative_or_resource_scope(data):
        return []

    edges = _edges_list(data)
    positive_outcome_edges = [
        edge
        for edge in edges
        if str(edge.get("rel", "")) == "correlates"
        and str(edge.get("target", "")) in {"aging", "mortality"}
    ]
    protective_edges = [
        edge
        for edge in edges
        if str(edge.get("rel", "")) == "negatively_correlates"
        and str(edge.get("target", "")) in {"aging", "mortality"}
    ]
    if positive_outcome_edges and not protective_edges:
        return [
            "correlative/resource draft has risk-increasing aging/mortality "
            "associations but no protective negatively_correlates edges; verify"
            " IGF1, parabiosis, embryogenesis, or other state-reversal branches"
            " were not dropped."
        ]
    return []


def _density_warnings(
    data: dict[str, Any],
    core_resource_edge_limit: int = 12,
) -> list[str]:
    """Return warnings when resource/correlative drafts over-emit core edges."""
    if not _is_correlative_or_resource_scope(data):
        return []
    if _curation_density(data) == "expanded":
        return []
    edge_count = len(_edges_list(data))
    if edge_count <= core_resource_edge_limit:
        return []
    return [
        f"resource/correlative draft has {edge_count} edges with "
        f"{CURATION_DENSITY_KEY}: core/default; either reduce to core "
        "paper-defining edges or adjudicate scope_density_warning / set "
        f"{CURATION_DENSITY_KEY}: expanded."
    ]


def _curation_density(data: dict[str, Any]) -> str:
    """Return curation density from paper metadata; default is core."""
    paper_block = data.get("paper")
    if not isinstance(paper_block, dict):
        return "core"
    densities = {
        str(paper.get(CURATION_DENSITY_KEY, "core")).strip().lower()
        for paper in paper_block.values()
        if isinstance(paper, dict)
    }
    return "expanded" if "expanded" in densities else "core"


def _is_correlative_or_resource_scope(data: dict[str, Any]) -> bool:
    """Return whether any paper block has a correlative/resource scope."""
    paper_block = data.get("paper")
    if not isinstance(paper_block, dict):
        return False
    scopes = {
        str(paper.get("paper_scope", ""))
        for paper in paper_block.values()
        if isinstance(paper, dict)
    }
    return bool(
        scopes
        & {
            "cohort_correlation_paper",
            "atlas_resource",
            "biomarker_validation_paper",
            "review_or_resource",
        }
    )


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
    """Return whether a node looks like an assay reagent rather than a graph
    node.
    """
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


def _adjudications_list(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Return well-formed adjudication records from a draft."""
    adjudications = data.get(ADJUDICATIONS_KEY)
    if not isinstance(adjudications, list):
        return []
    return [record for record in adjudications if isinstance(record, dict)]


def _edge_adjudication_is_complete(
    data: dict[str, Any],
    edge: dict[str, Any],
    issue_type: str,
    *,
    rejected_alternative_key: str = "rejected_alternative",
    convention_rule_key: str = "convention_rule",
) -> bool:
    """Return whether an edge adjudication has issue-specific metadata."""
    record = _edge_adjudication_record(data, edge, issue_type)
    if record is None:
        return False
    if str(record.get(DECISION_KEY, "")) != "keep_as_is":
        return True
    if issue_type not in {"verb_warning", "evidence_strength_warning"}:
        return True
    return bool(
        str(record.get(rejected_alternative_key, "")).strip()
        and str(record.get(convention_rule_key, "")).strip()
    )


def _edge_adjudication_record(
    data: dict[str, Any],
    edge: dict[str, Any],
    issue_type: str,
) -> dict[str, Any] | None:
    """Return the first adjudication that covers an edge and issue type."""
    for record in _adjudications_list(data):
        if str(record.get(ISSUE_TYPE_KEY, "")) != issue_type:
            continue
        for field in ("edge", "emitted_edges", "remove_edges"):
            value = record.get(field)
            candidates = value if isinstance(value, list) else [value]
            for candidate in candidates:
                if isinstance(candidate, dict) and _edge_identity_matches(
                    edge, candidate
                ):
                    return record
    return None


def _edge_identity_tuple(edge: dict[str, Any]) -> tuple[str, str, str]:
    """Return source/target/rel identity tuple for a draft edge."""
    return (
        str(edge.get("source", "")),
        str(edge.get("target", "")),
        str(edge.get("rel", "")),
    )


def _adjudications_have_issue_type(
    data: dict[str, Any], issue_type: str
) -> bool:
    """Return whether any adjudication has the requested issue type."""
    return any(
        str(record.get(ISSUE_TYPE_KEY, "")) == issue_type
        for record in _adjudications_list(data)
    )


def _adjudications_cover_edge(
    data: dict[str, Any],
    edge: dict[str, Any],
    issue_type: str,
) -> bool:
    """Return whether an adjudication references an edge by
    source/target/rel.
    """
    for record in _adjudications_list(data):
        if str(record.get(ISSUE_TYPE_KEY, "")) != issue_type:
            continue
        for field in ("edge", "emitted_edges", "remove_edges"):
            value = record.get(field)
            candidates = value if isinstance(value, list) else [value]
            for candidate in candidates:
                if isinstance(candidate, dict) and _edge_identity_matches(
                    edge, candidate
                ):
                    return True
    return False


def _edge_identity_matches(
    edge: dict[str, Any], candidate: dict[str, Any]
) -> bool:
    """Return whether source/target/rel identify the same edge."""
    return all(
        str(edge.get(field, "")) == str(candidate.get(field, ""))
        for field in ("source", "target", "rel")
    )


def _format_edge_inline(edge: dict[str, Any]) -> str:
    """Format a compact edge description."""
    return (
        f"`{edge.get('source', '?')}` --"
        f"[{edge.get('rel', '?')}/{edge.get('evidence_strength', '?')}]--> "
        f"`{edge.get('target', '?')}`"
    )

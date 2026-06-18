"""Tiered vocabulary gate for the NASP compendium."""

from __future__ import annotations

import dataclasses
import enum
import re
from collections.abc import Iterable
from pathlib import Path

import yaml


NOISE_SUFFIXES: tuple[str, ...] = (
    "_loci",
    "_locus",
    "_accumulation",
    "_formation",
    "_levels",
    "_expression",
    "_signaling",
    "_signalling",
)


class Tier(enum.Enum):
    """Vocabulary tier a term resolves to."""

    CANONICAL = "canonical"
    PROPOSED = "proposed"
    DRIFT = "drift"
    UNDECLARED = "undeclared"


@dataclasses.dataclass(frozen=True)
class TermVerdict:
    """Outcome of classifying a single term.

    Attributes:
      term: The term exactly as written in the draft.
      tier: The tier the term resolved to.
      blocking: Whether this verdict should fail validation.
      message: Human-readable validation message.
      suggestion: Canonical term to use instead, when one is known.
    """

    term: str
    tier: Tier
    blocking: bool
    message: str
    suggestion: str | None = None


@dataclasses.dataclass
class Vocabulary:
    """Human-owned vocabulary loaded from `vocabulary.yaml`.

    Attributes:
      canonical: Mapping of category name to its set of approved terms.
      drift: Mapping of a forbidden term to its replacement and the reason.
    """

    canonical: dict[str, set[str]]
    drift: dict[str, dict[str, str]]

    def flat_canonical(self) -> set[str]:
        """Return every canonical term across all categories as one set."""
        flat: set[str] = set()
        for terms in self.canonical.values():
            flat.update(terms)
        return flat


def normalize_term(term: str) -> str:
    """Reduce a term to a comparison key for mechanical-variant matching.

    Lowercases, strips a known set of locus/condition/readout suffixes, and
    drops a single trailing plural 's'. This collapses mechanical variants
    (case, `_loci`, `_accumulation`, plurals) onto a shared key. Semantic
    synonyms (e.g. `cytosolic_L1_cDNA` -> `cytoplasmic_retroelement_cDNA`) are
    deliberately NOT handled here; those live in the drift table.
    """
    key = term.strip().lower()
    changed = True
    while changed:
        changed = False
        for suffix in NOISE_SUFFIXES:
            if key.endswith(suffix):
                key = key[: -len(suffix)]
                changed = True
    return re.sub(r"s$", "", key)


def classify_term(
    term: str,
    vocabulary: Vocabulary,
    proposed_terms: set[str],
    compendium_nodes: set[str],
) -> TermVerdict:
    """Classify one term into a tier with a validation verdict.

    Resolution order, first match wins:
      1. drift table -> blocking error, suggest the canonical replacement.
      2. canonical vocabulary -> pass silently.
      3. has a filed proposal in the draft's `proposed_terms` -> non-blocking
         review warning.
      4. normalized key matches an existing canonical or compendium node ->
         blocking error (a mechanical variant of an existing node), suggest it.
      5. otherwise -> blocking 'undeclared' error: use a canonical term or file
         a proposal.

    Args:
      term: The candidate node/term as written.
      vocabulary: The loaded human-owned vocabulary.
      proposed_terms: Terms declared in the draft's own `proposed_terms` block.
      compendium_nodes: Node names already in the active compendium, used for
        the normalized-variant check.

    Returns:
      A TermVerdict describing the tier, whether it blocks, and any suggestion.
    """
    if term in vocabulary.drift:
        entry = vocabulary.drift[term]
        replacement = entry.get("replacement")
        reason = entry.get("reason", "known drift term")
        return TermVerdict(
            term=term,
            tier=Tier.DRIFT,
            blocking=True,
            message=f"'{term}' is a drift term ({reason}); use '{replacement}'.",  # noqa: E501
            suggestion=replacement,
        )

    if term in vocabulary.flat_canonical():
        return TermVerdict(
            term=term,
            tier=Tier.CANONICAL,
            blocking=False,
            message=f"'{term}' is canonical.",
        )

    if term in proposed_terms:
        return TermVerdict(
            term=term,
            tier=Tier.PROPOSED,
            blocking=False,
            message=(
                f"'{term}' is a proposed term pending human review; the draft "
                "carries a proposal for it."
            ),
        )

    if term in compendium_nodes:
        return TermVerdict(
            term=term,
            tier=Tier.CANONICAL,
            blocking=False,
            message=f"'{term}' is already declared in the active compendium.",
        )

    normalized = normalize_term(term)
    existing_by_norm = {
        normalize_term(existing): existing
        for existing in vocabulary.flat_canonical() | compendium_nodes
    }
    if normalized in existing_by_norm:
        suggestion = existing_by_norm[normalized]
        return TermVerdict(
            term=term,
            tier=Tier.UNDECLARED,
            blocking=True,
            message=(
                f"'{term}' looks like a mechanical variant of existing node "
                f"'{suggestion}'; use the existing node."
            ),
            suggestion=suggestion,
        )

    return TermVerdict(
        term=term,
        tier=Tier.UNDECLARED,
        blocking=True,
        message=(
            f"'{term}' is not canonical and has no proposal; either map it to "
            "a canonical node or add it to the draft's proposed_terms block."
        ),
    )


def validate_draft_terms(
    draft_terms: Iterable[str],
    vocabulary: Vocabulary,
    proposed_terms: set[str],
    compendium_nodes: set[str],
) -> tuple[list[TermVerdict], list[TermVerdict]]:
    """Classify every term in a draft and split into errors and warnings.

    Args:
      draft_terms: All distinct node/term strings used by the draft (paper-block
        entries and edge endpoints).
      vocabulary: The loaded human-owned vocabulary.
      proposed_terms: Terms declared in the draft's own `proposed_terms` block.
      compendium_nodes: Node names already present in the active compendium.

    Returns:
      An (errors, warnings) tuple of TermVerdict lists. Errors block the commit
      (DRIFT and UNDECLARED); warnings are review items (PROPOSED).
    """
    errors: list[TermVerdict] = []
    warnings: list[TermVerdict] = []
    for term in sorted(set(draft_terms)):
        verdict = classify_term(
            term, vocabulary, proposed_terms, compendium_nodes
        )
        if verdict.blocking:
            errors.append(verdict)
        elif verdict.tier is Tier.PROPOSED:
            warnings.append(verdict)
    return errors, warnings


def load_vocabulary(path: Path) -> Vocabulary:
    """Load the human-owned vocabulary from `vocabulary.yaml`.

    Expects a top-level `canonical` mapping (category -> list of terms) and an
    optional top-level `drift` mapping (term -> {replacement, reason}).
    """
    with path.open() as handle:
        raw = yaml.safe_load(handle) or {}
    canonical_raw = raw.get("canonical", {}) or {}
    canonical = {
        category: set(terms or []) for category, terms in canonical_raw.items()
    }
    drift = raw.get("drift", {}) or {}
    return Vocabulary(canonical=canonical, drift=drift)


def load_proposed_terms(draft: dict) -> set[str]:
    """Extract pending proposed terms from a parsed draft's inline block.

    The draft may carry a top-level `proposed_terms` list of proposal records;
    only records without a terminal status (promoted/rejected/merged) are
    treated as live proposals. A missing block yields an empty set.
    """
    records = draft.get("proposed_terms", []) or []
    terminal = {"promoted", "rejected", "merged"}
    return {
        record["term"]
        for record in records
        if record.get("status", "pending") not in terminal
    }


if __name__ == "__main__":
    vocab = Vocabulary(
        canonical={
            "mechanisms": {
                "epigenetic_remodeling",
                "retrotransposon_derepression",
                "cytoplasmic_retroelement_cDNA",
                "tissue_inflammation",
            },
            "genes": {"CGAS", "STING1", "AIM2", "SPI1"},
        },
        drift={
            "cytosolic_L1_cDNA_accumulation": {
                "replacement": "cytoplasmic_retroelement_cDNA",
                "reason": "L1 cDNA naming drift",
            },
            "chromatin_accessibility": {
                "replacement": "epigenetic_remodeling",
                "reason": "accessibility is a readout of the remodeling state",
            },
        },
    )
    draft_proposals = {"heterochromatin_organization", "accelerated_aging"}
    active_nodes = vocab.flat_canonical()

    sample_terms = [
        "CGAS",
        "epigenetic_remodeling",
        "heterochromatin_organization",
        "accelerated_aging",
        "chromatin_accessibility",
        "cytosolic_L1_cDNA_accumulation",
        "tissue_inflammation_loci",
        "L1_chromatin_accessibility",
    ]
    found_errors, found_warnings = validate_draft_terms(
        sample_terms, vocab, draft_proposals, active_nodes
    )
    print(f"errors ({len(found_errors)}):")
    for verdict in found_errors:
        print(f"  [{verdict.tier.value}] {verdict.message}")
    print(f"warnings ({len(found_warnings)}):")
    for verdict in found_warnings:
        print(f"  [{verdict.tier.value}] {verdict.message}")

    canonical_verdict = classify_term(
        "CGAS", vocab, draft_proposals, active_nodes
    )
    assert canonical_verdict.tier is Tier.CANONICAL
    assert not canonical_verdict.blocking
    drift_verdict = classify_term(
        "chromatin_accessibility", vocab, draft_proposals, active_nodes
    )
    assert drift_verdict.tier is Tier.DRIFT
    assert drift_verdict.suggestion == "epigenetic_remodeling"
    proposed_verdict = classify_term(
        "heterochromatin_organization", vocab, draft_proposals, active_nodes
    )
    assert proposed_verdict.tier is Tier.PROPOSED
    assert not proposed_verdict.blocking
    variant_verdict = classify_term(
        "tissue_inflammation_loci", vocab, draft_proposals, active_nodes
    )
    assert variant_verdict.suggestion == "tissue_inflammation"
    print("self-tests passed")

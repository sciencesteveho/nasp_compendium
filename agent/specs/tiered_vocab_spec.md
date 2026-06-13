# Spec — Tiered vocabulary gate for the NASP compendium

Date: 2026-05-29
Status: draft for review
Reference implementation: `vocab_tiers.py` (standalone, self-testing)

## Problem

The current gate is binary: a term is either in `vocabulary.yaml` or it
produces an out-of-vocab warning, and the agent is forbidden from editing the
vocabulary. That is safe but it leaves good new nodes in limbo. The Martinez
held-out run is the worked example: `heterochromatin_organization` and
`accelerated_aging` are correct, useful nodes, but they surfaced only as
warnings with no path forward inside the run. At the same time, a pure
"add-on-first-sighting" rule would reintroduce exactly the drift the four
calibrations cleaned up (`cytosolic_L1_cDNA_accumulation`, `CCF_formation`,
`chromatin_accessibility` used as a node instead of `epigenetic_remodeling`).

The fix keeps a human in the approval loop but makes the gate tiered, so the
agent can advance a draft with a new term while flagging it for review rather
than either inventing silently or stalling.

## Principles

1. The agent may *use* a new term in a draft, but only after a canonicalisation
   search comes up empty and only if it files a proposal in the same draft.
2. Coining a node and approving a node are different acts. The agent does the
   first; a human does the second. The schema enforces that separation.
3. The canonicalisation search is an every-time precondition, not a
   later-paper behaviour. The only difference between the first paper to touch
   a concept and a later one is whether the search returns a hit.
4. Validation stays the gate. Drift and undeclared terms block; proposed terms
   warn; canonical terms pass silently.

## Tiers

| Tier | Meaning | Validation | Who acts |
|---|---|---|---|
| `canonical` | Approved term in `vocabulary.yaml` | pass, silent | nobody |
| `proposed` | New term used in a draft with a filed proposal | warning, non-blocking | human promotes/merges/rejects |
| `drift` | Known-bad term with a canonical replacement | error, blocking | agent must use the replacement |
| (undeclared) | New term used with no proposal, or a mechanical variant of an existing node | error, blocking | agent files a proposal or uses the existing node |

"Undeclared" is not a stored tier; it is what a term resolves to when it
matches none of the three and has no proposal. It blocks so that "file the
proposal" is mandatory rather than optional.

## File layout and ownership

| File | Owner | Contains |
|---|---|---|
| `agent/vocabulary.yaml` | human only | `canonical` terms by category, `drift` table |
| draft file, e.g. `calibration_drafts/martinez_2024.md` | agent | the `paper`/`edges` blocks plus an inline `proposed_terms` block |
| `agent/reports/audits/vocabulary_drift_review_<DATE>.md` | human, agent-assisted | running record of promote/merge/reject decisions |

Proposals live *inline in the draft that needs them*, not in a shared sidecar.
This matches how everything else in the compendium is per-paper, avoids
write contention between concurrent drafts, and keeps a term's justification
next to the edges that motivated it. A `compendium collect-proposals` step
(below) is what moves an approved proposal into the human-owned
`vocabulary.yaml`. The agent never writes to `vocabulary.yaml`.

## Schema — `vocabulary.yaml`

Two top-level keys. `canonical` is the existing vocabulary, now nested under a
key; `drift` is new.

```yaml
canonical:
  nucleic_acid_sensors:
    - CGAS
    - STING1
    - AIM2
  genes:
    - SPI1
    - NLRP3
    # ...
  mechanisms:
    - epigenetic_remodeling
    - retrotransposon_derepression
    - cytoplasmic_retroelement_cDNA
    - tissue_inflammation
    - heterochromatin_organization   # after promotion from the Martinez run
    - accelerated_aging              # after promotion from the Martinez run
    # ...
  pathways:
    - cGAS-STING
    # ...
  # cell_types, model_systems, evidence_type, verbs, evidence_strength as today

drift:
  chromatin_accessibility:
    replacement: epigenetic_remodeling
    reason: accessibility is a readout of the remodeling state, not a node
  cytosolic_L1_cDNA_accumulation:
    replacement: cytoplasmic_retroelement_cDNA
    reason: L1 cDNA naming drift
  L1_de-repression:
    replacement: retrotransposon_derepression
    reason: L1 naming drift
  CCF_formation:
    replacement: cytoplasmic_chromatin_fragments
    reason: convention drift; CCF belongs in prose only
```

The `drift` table is the only place semantic synonyms are encoded. The
validator's normalisation handles mechanical variants (case, `_loci`,
`_accumulation`, plurals); it does not and should not guess semantic mappings
like `chromatin_accessibility -> epigenetic_remodeling`. Those are human
decisions recorded here.

## Schema — inline `proposed_terms` block in a draft

A top-level list in the draft file, parallel to `paper` and `edges`. One
record per new term. The record is only valid if `canonicalization_search`
shows the agent actually looked and `nearest_existing` explains why an existing
node will not do.

```yaml
proposed_terms:
  - term: heterochromatin_organization
    category: mechanisms
    paper: Martinez_biorxiv_2024
    motivating_edges:
      - "CGAS binds_recruits heterochromatin_organization"
    canonicalization_search:
      searched:
        - heterochromatin
        - heterochromatin_maintenance
        - H3K9me3
        - epigenetic_remodeling
      result: no_exact_or_normalized_match
    nearest_existing: epigenetic_remodeling
    why_insufficient: >
      epigenetic_remodeling is the loss-of-repressive-chromatin STATE that a
      perturbation drives; this node is the intact, factor-maintained
      heterochromatin compartment that CGAS physically supports. They are
      opposite poles and both are needed (CGAS suppresses epigenetic_remodeling
      AND CGAS binds_recruits heterochromatin_organization).
    proposed_definition: >
      The organised, factor-maintained repressive heterochromatin compartment
      over transposable elements.
    status: pending
```

`status` defaults to `pending`. A human edits it to `promoted`, `merged`
(with a `merged_into:` field), or `rejected` (with a `replacement:` field that
then seeds a new drift entry). Only `pending` records make the term a live
proposed-tier term during validation.

## Validation behaviour

`compendium validate` gains a term-classification pass that runs over every
node string in a draft (paper-block entries and edge endpoints), using the
logic in `vocab_tiers.py`:

- **canonical** -> pass, no output.
- **drift** -> blocking error: ``'X' is a drift term (<reason>); use '<replacement>'.``
- **proposed** (term has a `pending` record in the draft) -> non-blocking
  warning: ``'X' is a proposed term pending human review.`` This is the tier
  that produced the four Martinez warnings; under this spec they are the system
  working, not a defect.
- **mechanical variant** (normalised key matches an existing canonical or
  compendium node) -> blocking error suggesting the existing node. Catches
  `tissue_inflammation_loci`, `L1_chromatin_accessibility`, plural slips.
- **undeclared** (none of the above, no proposal) -> blocking error: use a
  canonical node or file a proposal.

Blocking = the existing "validation failure is a stop condition" rule still
holds. The agent cannot ship a draft that uses a drift term or an undeclared
novel term; it must either canonicalise or file the proposal in the same run.
Skip-edge warnings are unchanged and remain non-blocking review items.

The reference implementation exposes:

- `load_vocabulary(path) -> Vocabulary`
- `load_proposed_terms(draft) -> set[str]`
- `classify_term(term, vocabulary, proposed_terms, compendium_nodes) -> TermVerdict`
- `validate_draft_terms(draft_terms, vocabulary, proposed_terms, compendium_nodes) -> (errors, warnings)`

`classify_term` is pure and order-sensitive (drift, then canonical, then
proposed, then normalised-variant, then undeclared); the `__main__` block runs
the four-behaviour smoke test.

## New CLI surface

- `compendium validate` — gains the term-classification pass above. No new
  flag; tier checking is part of normal validation.
- `compendium propose-terms <draft>` — convenience for the agent: runs the
  canonicalisation search for every undeclared term in a draft and scaffolds
  `proposed_terms` records (with `searched`/`result`/`nearest_existing`
  prefilled) for the curator-agent to complete. Optional; the agent can also
  write the block directly.
- `compendium collect-proposals <dir>` — human-run after review. Reads
  `proposed_terms` records with `status: promoted` across drafts and emits a
  patch to `vocabulary.yaml` (terms added under their `category`) plus, for
  `status: rejected` records, the corresponding `drift` entries. Prints the
  patch for human apply; does not write `vocabulary.yaml` autonomously.

## Agent workflow change (`agent/prompts/curate_paper.md`)

The existing "node-name canonicalisation pass" is upgraded to a hard
precondition for any new term:

1. For each candidate node, run the canonicalisation search across `canonical`
   (all categories) and the active compendium node set, exact then normalised.
2. If a hit: use the canonical/existing node. If the hit is via the `drift`
   table, use the replacement.
3. If no hit: keep the term in the draft AND add a `proposed_terms` record with
   a completed `canonicalization_search` and `nearest_existing`. A new term
   without a record is an error by construction.
4. Run `compendium validate` before commit. Drift/undeclared errors block;
   proposed warnings are expected and listed in the per-paper notes.

This is the operational answer to "check the vocab first": the check is the
precondition for proposing, every time, not a behaviour that only kicks in on
later papers.

## Migration

1. **Adjudicate the four Martinez warnings.** Under this spec they are
   `pending` proposals. `heterochromatin_organization` and `accelerated_aging`
   are good nodes -> promote. `nanopore_methylation_seq` is an `evidence_type`
   value -> promote if the evidence-type vocabulary is gated the same way, else
   leave to the evidence-type list. `nuclear_cGAS_heterochromatin` reads like a
   genotype/locus-baked compound; check it against the gold (which uses
   `heterochromatin_organization`) and most likely `merge` it into
   `heterochromatin_organization` with a drift entry, rather than promote.
2. **Seed the `drift` table** from `agent/reports/audits/vocabulary_drift_review_2026-05-29.md`:
   move `L1_de-repression`, `cytosolic_L1_cDNA_accumulation`, `CCF_formation`,
   and `chromatin_accessibility` (if present as a node term) into `drift` with
   replacements. This is the human edit the test prompt deliberately deferred.
3. **Nest the current flat vocabulary under `canonical:`** and run
   `compendium validate` across `docs/compendium/` to confirm no regressions on
   the four golds + Martinez.

## Open questions for review

- Should `evidence_type`, `model_systems`, and `cell_types` be gated by the
  same tiering, or only `mechanisms`/`genes`/`pathways`? Assay and model names
  drift less and may warrant a looser gate.
- Promotion granularity: promote per-term on review, or batch per calibration
  cycle? Batching keeps `vocabulary.yaml` churn low but delays good nodes.
- Should a `pending` proposal expire? A term proposed but never promoted across
  N papers may indicate it should have been a context detail, not a node.

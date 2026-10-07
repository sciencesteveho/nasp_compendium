
# Regression calibration + fresh held-out test

`compendium score` uses core-tier recall as its primary metric, reports
supporting recall separately, and counts forbidden-shortcut violations.
Relationship, polarity, endpoint, and evidence agreement remain diagnostics.
`compendium review_packet --gate` validates the exact draft; its biological
review findings are advisory.

## Goal

Two tiers. The regression set checks reproducibility against papers that already
informed the instructions. A fresh held-out paper measures generalization.

- REGRESSION SET (Phase 1): mao_2024, lian_2018, martinez_2024,
  tyshkovskiy_2026. Qin_2024 is also a historical regression paper; it is not a
  held-out result because it already informed `curation_lessons.md`.
- FRESH HELD-OUT TEST (Phase 2): one paper supplied by the human runner that is
  absent from prompts, lessons, reports, and prior agent-readable history.

Regression golds live in `docs/compendium/<paper>.gold.md`; PDFs live in
`data/literature/<paper>.pdf`. A fresh holdout reference must remain outside the
repository and outside the agent-readable workspace until its draft is frozen.

## Read first

See `agent/prompts/_shared.md` for the Read-first set, plus
`agent/vocabulary.yaml` and `agent/specs/tiered_vocab_spec.md`. Curate exactly
as those instruct; the only deviations are the constraints below.

## Run one phase per invocation

Run ONLY the phase you are told to run (default: Phase 1). Never run Phase 2 in
the same invocation as Phase 1. Stop at the end of the named phase.

## Hard constraints (both phases)

- Do NOT open, read, grep, or diff any reference during blind curation,
  validation, or review. For Phase 1, treat `docs/compendium/*.gold.md` as
  nonexistent until every regression draft is frozen. In Phase 2, the agent
  does not receive or read the external reference at all.
- When scanning `docs/compendium/` for style/vocab examples, exclude every
  `*.gold.md` file (leakage).
- Do NOT edit `docs/compendium/`, any `*.gold.md`, `agent/vocabulary.yaml`,
  conventions, lessons, prompts, or source code. Do NOT promote/merge proposed
  terms. Do NOT run `compendium regenerate`. Do NOT git add/commit/push.
- Retain the blind `*.post_patch.draft.md`, one aggregate `*.score.json`, and one
  compact audit. Review packets and temporary directories are regenerable and
  remain untracked.
- Do NOT read previous calibration audits, prior draft outputs, prior review
  packets, or prior score JSON in `agent/reports/` before all blind drafts for
  the current phase are written. Treat them as leakage.
- Do NOT use existing `agent/reports/curation_runs/*.draft.md` as style examples.

## Preconditions (check; stop and report if unmet)

- The PDFs for the phase's papers exist in `data/literature/`.
- `agent/reports/curation_runs/` and `agent/reports/audits/` exist.

---

## Phase 1 - regression calibration (four papers)

For each regression paper, working only from its PDF and the agent instructions:

1. Produce a full blind curation draft at
   `agent/reports/curation_runs/<paper_id>.post_patch.draft.md` containing a
   `paper` block and an `edges` list, following `agent/conventions.md`. Add a
   `proposed_terms` block only if a needed node is absent after
   canonicalization.

   Apply these recall and naming rules from conventions:
   - Symmetric association extraction. For correlative/atlas papers, extract
     protective (lifespan-positive, mortality-negative) associations as
     explicit `negatively_correlates` edges, not only risk-increasing
     `correlates` edges. A draft with risk associations and zero protective
     associations is a recall smell; confirm none were dropped.
   - Intervention/state nodes. Encode specific interventions
     (`heterochronic_parabiosis`, `early_embryogenesis`) as their own nodes
     rather than collapsing them into `cell_state_transition`.
   - Evidence-resolved sensor topology. Prefer direct ligand-to-sensor edges
     when individual engagement is supported. Retain a grouped sensing step
     when only a combined sensor perturbation is resolved, and state that limit
     in `context`.
   - Verb-to-readout match. Use `upregulates`/`downregulates` for abundance
     readouts, `induces` for a perturbation-linked state transition, `drives`
     for supported program/phenotype causation.
   - Evidence-to-edge match. If the paper records both a perturbation and a
     measured readout for the edge path, consider `perturbation_supported`
     before choosing `canonical_inferred` or `direct_measured`.
   - Core density for resource papers. For atlas/resource, cohort-correlation,
     or biomarker-validation papers, keep the draft to the paper-defining core
     edges by default. Do not expand every associated marker into graph edges.

2. Build and gate the review packet for each exact draft:
   `compendium review_packet <draft> --out
   agent/reports/audits/<paper_id>.post_patch.review_packet.md --gate`.
   File-mode review validates that draft in isolation. The `--gate` flag exits
   nonzero for validation errors. Topology, verb, evidence-strength, reagent,
   and density findings are advisory: revise them when warranted and record a
   short rationale for scientifically defensible alternatives. A broad output
   edge rejected as a shortcut does not discharge the branch audit: search for
   the nearest supported intermediate (for example `STING1 activates NF-kB`)
   and emit it when supported.

   Re-run until `--gate` exits 0.

3. Only after all four drafts are gate-clean, score each against its gold:
   `compendium score --draft agent/reports/curation_runs/<paper_id>.post_patch.draft.md
   --gold docs/compendium/<paper_id>.gold.md --format json`.
   Also run the directory form once for the totals:
   `compendium score --draft agent/reports/curation_runs --draft-glob
   '*.post_patch.draft.md' --gold docs/compendium --format
   json --out agent/reports/audits/calibration_<YYYY-MM-DD>.score.json`.
   Gold edges marked excluded (see `agent/conventions.md` on gold defects) are
   dropped from the denominator by default. If a draft edge would only exist to
   match such an excluded gold edge, do not emit it. Do not change any draft
   after scoring.

4. Write `agent/reports/audits/calibration_<YYYY-MM-DD>_post_patch.md` using
   the template below. Stop. Do not act on findings.

Between Phase 1 and Phase 2 (human, not the agent): read the audit and edit
`agent/curation_lessons.md` / `agent/conventions.md` / `agent/vocabulary.yaml`
as warranted. Only then run Phase 2.

## Phase 2 - fresh held-out generalization test

Run only when a human has selected a new paper and has kept its reference
outside the repository, Git history, reports, and agent-readable workspace.

1. The invocation supplies only `<paper_id>`, its PDF, and the normal non-gold
   instruction/style inputs. It must not contain expected nodes, edges, branches,
   vocabulary answers, or pass guidance.
2. Curate the paper and write
   `agent/reports/curation_runs/<paper_id>.post_patch.draft.md`.
3. Run the exact-draft review gate. Record the draft SHA-256 and stop the blind
   invocation. Do not score, inspect a reference, or edit the frozen draft.
4. The human verifies the hash and runs the existing scorer against the external
   reference, writing
   `agent/reports/audits/holdout_test_<paper_id>_<YYYY-MM-DD>.score.json`.
5. A later non-blind audit may inspect the score and reference, but the draft
   hash must remain unchanged. Report relationship, polarity, evidence, endpoint
   diagnostic, reference-dispute, and supported-extra categories separately.

### Iterate discipline (important)

- If a held-out paper reveals a gap, fix only a general, cross-paper rule. Never
  add a paper-specific patch or node-name literal. Advisory topology patterns
  become blockers only if independent cases establish an unambiguous invariant.
- Once a holdout informs an instruction edit, graduate it to the regression set
  and select a different fresh holdout.

---

## Scoring interpretation (replaces manual triple counting)

`compendium score` reports core recall first, supporting recall separately,
and forbidden-shortcut violations. It also reports relationship
recall/precision, endpoint overlap, polarity mismatches, same-polarity
relationship alternatives, symmetric correlation orientation, evidence
mismatches, misses, extras, and excluded defects. Classify each difference by
source evidence before changing instructions:

- polarity mismatch -> high-priority sign/claim-status disagreement; first
  determine whether the draft or reference is scientifically correct.
- same-polarity relationship mismatch -> verb or representation difference,
  not an automatic extraction error.
- a supported branch edge that should have been emitted -> branch-audit gap.
- a shortcut edge emitted in place of a supported chain -> shortcut fix.
- a supported reference relationship with no endpoint match -> possible true
  extraction/normalization gap.
- evidence-strength mismatch on a recovered relationship -> evidence-boundary
  issue; inspect edge-specific support rather than copying the reference.
- a supported extra -> possible reference incompleteness or defensible density
  choice; do not suppress it merely to improve precision.
- a miss against an acknowledged gold defect -> exclude with
  `--drop-gold-defects`; do not chase.

## Audit template

```
# Calibration audit <YYYY-MM-DD> (dry run, scored)

## Summary
- Papers, drafts, one-line verdict each.
- compendium score totals: core and supporting recall, shortcut violations,
  relationship recall/precision, exact recovery, endpoint overlap, polarity,
  same-polarity relationship, symmetric orientation, evidence, missed, extra,
  and defects excluded.
- Gate status per paper (gate-clean or list of resolved blockers).

## Per-paper findings
### <PAPER_ID>
- score: core K/N; supporting K/N; shortcuts N; relationship K/N; exact K/N;
  endpoint overlap K/N; polarity [...]; relationship [...]; symmetric [...];
  evidence [...]; missed [...]; extra [...]
- Difference classification (extraction / normalization / representation /
  validator / reference / defensible alternative / ambiguity) per edge.
- Naming-HGNC drift, marker promotion, per-cytokine bloat, proposed-term handling.
- Gate blockers raised and how each was resolved (emit / revise), including
  rejected alternatives and nearest-intermediate searches when relevant.

## Cross-paper failure patterns
## Candidate curation_lessons additions    (draft text only; do not edit files)
## Vocabulary observations                 (do not edit vocabulary.yaml)
## Structural-lint observations            (did any lint over- or under-fire?)
## Generalization note                     (Phase 2 only)
```

## Done criteria

- Drafts in `agent/reports/curation_runs/` parse as YAML with all required edge
  fields; `--gate` exits 0.
- One aggregate `compendium score` JSON is retained, including tiered recall,
  shortcut violations, and relationship/polarity diagnostics.
- One audit file in `agent/reports/audits/` for the phase.
- No new tracked folders; no edits to `docs/compendium/`, `*.gold.md`, vocabulary,
  conventions, lessons, prompts, or source; no commits. `git status` shows only
  the new `agent/reports/` files.

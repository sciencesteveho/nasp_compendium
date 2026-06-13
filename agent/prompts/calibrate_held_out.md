# Calibration + held-out test v2 (DRY RUN, audit only)

This supersedes the manual edge-by-edge comparison. Recovery is now measured by
`compendium score`, the pre-freeze gate is enforced by `compendium
review_packet --gate`, and the topology/verb/evidence/density lints are
structural (they apply to every paper, not a fixed node list).

## Goal

Two tiers. The DEV SET is what we tune lessons/conventions/vocab against. The
HELD-OUT TEST measures whether the tuning generalizes to an unseen paper. Both
are dry runs that produce audits and change nothing under version control.

- DEV SET (Phase 1): mao_2024, lian_2018, martinez_2024, tyshkovskiy_2026
- HELD-OUT TEST (Phase 2): qin_2024 (novel sensor ZC3HAV1 on the STING spine)

Gold files live in `docs/compendium/<paper>.gold.md`; PDFs in
`data/literature/<paper>.pdf`. Do NOT read a paper's gold until its scoring step.

## Read first

AGENTS.md, agent/analysis_prompt.md, agent/conventions.md,
agent/curation_lessons.md, agent/vocabulary.yaml,
agent/specs/tiered_vocab_spec.md. Curate exactly as those instruct; the only
deviations are the constraints below.

## Run one phase per invocation

Run ONLY the phase you are told to run (default: Phase 1). Never run Phase 2 in
the same invocation as Phase 1. Stop at the end of the named phase.

## Hard constraints (both phases)

- Do NOT open, read, grep, or diff any `docs/compendium/*.gold.md` during
  re-curation, validation, or review-packet steps; treat the golds as
  nonexistent until the scoring step of that phase.
- When scanning `docs/compendium/` for style/vocab examples, exclude every
  `*.gold.md` file (leakage).
- Do NOT edit `docs/compendium/`, any `*.gold.md`, `agent/vocabulary.yaml`,
  conventions, lessons, prompts, or source code. Do NOT promote/merge proposed
  terms. Do NOT run `compendium regenerate`. Do NOT git add/commit/push.
- Write tracked outputs only into the existing `agent/reports/curation_runs/` and
  `agent/reports/audits/`. Temporary directories under `/tmp` are allowed for
  subset validation/scoring and must be deleted after use.
- Do NOT read previous calibration audits, prior draft outputs, prior review
  packets, or prior score JSON in `agent/reports/` before all blind drafts for
  the current phase are written. Treat them as leakage.
- Do NOT use existing `agent/reports/curation_runs/*.draft.md` as style examples.

## Preconditions (check; stop and report if unmet)

- The PDFs for the phase's papers exist in `data/literature/`.
- `agent/reports/curation_runs/` and `agent/reports/audits/` exist.

---

## Phase 1 - dev calibration (four papers)

For each dev paper, working only from its PDF and the agent instructions:

1. Produce a full blind curation draft at
   `agent/reports/curation_runs/<paper_id>.post_patch.draft.md` containing, in
   order: `paper` (with `paper_scope`), `claims`, optional `claim_edge_matrix`,
   optional `entity_resolution`, `proposed_terms` only if a needed node is
   absent after canonicalization, optional `adjudications`, then `edges`.

   Every claim includes `claim_id`, `evidence_location`, `claim`, `assay`,
   `disposition`, `branch_type`, `graph_candidate`, `support`, and where
   possible `perturbation`, `measured_readout`, `affected_entities`. Every
   emitted edge has non-empty `support_claims`. For atlas/resource or broad
   correlative papers, set `curation_density: core` in the paper block unless
   the user explicitly asked for an expanded satellite graph.

   Apply these recall and naming rules from conventions:
   - Symmetric association extraction. For correlative/atlas papers, extract
     protective (lifespan-positive, mortality-negative) associations as
     explicit `negatively_correlates` claims/edges, not only risk-increasing
     `correlates` edges. A draft with risk associations and zero protective
     associations is a recall smell; confirm none were dropped.
   - Intervention/state nodes. Encode specific interventions
     (`heterochronic_parabiosis`, `early_embryogenesis`) as their own nodes
     rather than collapsing them into `cell_state_transition`.
   - Direct ligand-to-sensor topology. Do not insert a generic `*_sensing`
     process as an activator of the specific sensor genes that instantiate it.
   - Verb-to-readout match. Use `upregulates`/`downregulates` for abundance
     readouts, `induces` for a perturbation-linked state transition, `drives`
     for supported program/phenotype causation.
   - Evidence-to-claim match. If linked claims record both a perturbation and a
     measured readout for the edge path, consider `perturbation_supported`
     before choosing `canonical_inferred` or `direct_measured`.
   - Core density for resource papers. For `atlas_resource`,
     `cohort_correlation_paper`, or `biomarker_validation_paper`, keep the draft
     to the paper-defining core edges by default. Do not expand every associated
     marker into graph edges unless `curation_density: expanded` is explicitly
     justified and adjudicated.

2. Validate the drafts:
   `compendium validate --dir agent/reports/curation_runs`.
   Expected/OK: non-blocking "proposed term pending" warnings. NOT OK: drift
   terms, undeclared endpoints, missing required edge fields. Record these; do
   not fix the source. (If subset validation is needed, copy only the new
   post-patch drafts to a temporary directory outside version control, validate
   there, then delete it.)

3. Build and gate the review packet for each draft:
   `compendium review_packet <draft> --out
   agent/reports/audits/<paper_id>.post_patch.review_packet.md --gate`.
   The `--gate` flag exits nonzero while any pre-freeze blocker is unresolved.
   For every blocker (hidden graph candidate in a gated branch, topology lint,
   verb warning, evidence-strength warning, reagent endpoint, scope-density
   warning, broad-claim reuse, claim-edge-matrix gap), either revise the draft
   or add a top-level `adjudications:` record (`issue_id`, `issue_type`,
   `decision`, `rationale`, plus `claim_id`/`edge` as needed).

   Required adjudication details:
   - `verb_warning` with `decision: keep_as_is` must include
     `rejected_alternative` and `convention_rule`.
   - `evidence_strength_warning` with `decision: keep_as_is` must include
     `rejected_alternative` and `convention_rule`.
   - `hidden_graph_candidate` with `decision: keep_context`,
     `keep_insufficient`, or `keep_as_is` must include
     `nearest_intermediate_search:` with `searched: true` and
     `candidate_edges_considered: [...]`. A broad claim rejected as a shortcut
     does NOT discharge the branch audit: search for the nearest supported
     intermediate (for example `STING1 activates NF-kB`) and emit it when
     supported.
   - `scope_density_warning` must either reduce the draft to core edges or
     justify `curation_density: expanded`.

   Re-run until `--gate` exits 0 or every remaining blocker is explicitly
   adjudicated as `needs_human_review`, `keep_context`, `keep_insufficient`,
   `keep_as_is`, or `reject_as_gold_defect` with the required metadata above.

4. Only after all four drafts are gate-clean or fully adjudicated, score each
   against its gold:
   `compendium score --draft agent/reports/curation_runs/<paper_id>.post_patch.draft.md
   --gold docs/compendium/<paper_id>.gold.md --drop-gold-defects --format json`.
   Also run the directory form once for the totals:
   `compendium score --draft agent/reports/curation_runs --draft-glob
   '*.post_patch.draft.md' --gold docs/compendium --drop-gold-defects --format
   json --out agent/reports/audits/calibration_<YYYY-MM-DD>.score.json`.
   `--drop-gold-defects` excludes gold edges annotated as acknowledged defects
   from the denominator. If a draft edge would only exist to match such a
   placeholder, do not emit it; record a `reject_as_gold_defect` adjudication.
   Do not change any draft after scoring.

5. Write `agent/reports/audits/calibration_<YYYY-MM-DD>_post_patch.md` using
   the template below. Stop. Do not act on findings.

Between Phase 1 and Phase 2 (human, not the agent): read the audit and edit
`agent/curation_lessons.md` / `agent/conventions.md` / `agent/vocabulary.yaml`
as warranted. Only then run Phase 2.

## Phase 2 - held-out generalization test (qin_2024 only)

Run only after dev-set lessons are stable.

1. Curate qin_2024 blind from `data/literature/qin_2024.pdf`. Do not read any
   gold. Write `agent/reports/curation_runs/Qin_*.post_patch.draft.md`.
2. Validate; build and gate the review packet (same rules as Phase 1 step 3).
3. Score against gold:
   `compendium score --draft <draft> --gold docs/compendium/qin_2024.gold.md
   --drop-gold-defects --format json`.
4. Write `agent/reports/audits/holdout_test_qin_<YYYY-MM-DD>.md`: the per-paper
   rubric plus a one-line PASS/PARTIAL/FAIL and a short generalization note.

Pass guidance: Qin needs no new vocabulary. A clean pass recovers the
cGAS-STING -> TBK1 -> IRF3 -> type_I_IFN spine and the STING1 -> NF-kB ->
tissue_inflammation branch, localizes ZC3HAV1 at STING (downstream of cGAMP, not
at CGAS), captures the sign-flipped `ZC3HAV1 suppresses RIG-I/MDA5-MAVS` and the
TLR-independence negative, with canonical nodes and correct HGNC names, no
invented vocab, no per-cytokine bloat.

### Iterate discipline (important)

- If Qin reveals a gap, fix the GENERAL lesson/convention/structural lint that
  would have caught it across papers. Never write a Qin-specific patch or a
  node-name literal; that is memorizing the test. The structural lints
  (`*_sensing` to a sensor gene, abundance-readout verb, reagent endpoint) and
  claim-metadata checks are the generalizable surface to tune.
- Once Qin has informed a lesson edit, graduate it into the dev set and hold out
  a fresh paper next time.

---

## Scoring interpretation (replaces manual triple counting)

`compendium score` reports per paper and in total: recovered / gold-total,
missed triples, extra triples, ordinary missed/extra after subtracting
relationship/symmetric cases, source-target matches with a relationship-only
mismatch, symmetric correlation direction differences, and evidence-strength
mismatches on recovered triples. Read the JSON for the machine-tracked record
across rounds. Then classify each miss by root cause, because the count alone
does not tell you what to fix:

- relationship-only mismatch -> verb-discipline fix (near miss).
- extra `*_sensing -> sensor` plus a missed direct ligand-to-sensor edge ->
  topology fix (converts a miss and deletes an extra).
- a hidden graph-candidate claim that should have been emitted -> adjudication /
  branch-audit gap.
- a shortcut edge emitted in place of a supported chain -> shortcut fix.
- a gold triple never extracted as a claim -> true claim-recall gap.
- evidence-strength mismatch on a recovered triple -> quality issue; does NOT
  change the recovery count, but should be gated before freeze.
- ordinary missed / ordinary extra -> the residual biological/topological gap
  after removing relation-only and symmetric-correlation near misses.
- a miss against an acknowledged gold defect -> exclude with
  `--drop-gold-defects`; do not chase.

## Audit template

```
# Calibration audit <YYYY-MM-DD> (dry run, scored)

## Summary
- Papers, drafts, one-line verdict each.
- compendium score totals: recovered/gold-total, evidence-matched recovered,
  ordinary missed/extra, relationship-only, symmetric-correlation, evidence-only,
  extra, defects dropped.
- Gate status per paper (gate-clean or list of adjudicated blockers).

## Per-paper findings
### <PAPER_ID>
- score: recovered K/N; ordinary missed [...]; ordinary extra [...];
  rel-only [...]; symmetric [...]; evidence [...]
- Miss classification (verb / topology / hidden-candidate / shortcut /
  claim-recall / gold-defect) per missed triple.
- Naming-HGNC drift, marker promotion, per-cytokine bloat, proposed-term handling.
- Gate blockers raised and how each was resolved (emit / revise / adjudicate),
  including rejected alternatives and nearest-intermediate searches when
  required.

## Cross-paper failure patterns
## Candidate curation_lessons additions    (draft text only; do not edit files)
## Vocabulary observations                 (do not edit vocabulary.yaml)
## Structural-lint observations            (did any lint over- or under-fire?)
## Generalization note                     (Phase 2 only)
```

## Done criteria

- Drafts in `agent/reports/curation_runs/` parse as YAML with all required edge
  fields; `--gate` exits 0 or all blockers are adjudicated.
- `compendium score` recorded (JSON kept) for each paper and in total, with
  ordinary missed/extra distinguished from relationship/symmetric near misses.
- One audit file in `agent/reports/audits/` for the phase.
- No new tracked folders; no edits to `docs/compendium/`, `*.gold.md`, vocabulary,
  conventions, lessons, prompts, or source; no commits. `git status` shows only
  the new `agent/reports/` files.

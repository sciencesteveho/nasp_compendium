# NASP gold-standard redesign

Redesign of three NASP gold standards (Dou 2017, De Cecco 2019, López-Polo
2024) and the evaluation scorer so that the gold measures whether the curation
agent preserves the **biology that matters** — the source and target entities,
the causal direction and sign, the molecular mechanism, and whether the
evidence is direct or indirect — instead of whether it reproduces one curator's
prose. The redesign is additive and backward-compatible: the five existing
golds are untouched and score identically.

This document delivers the seven required outputs. Supporting design detail is
in `docs/design_decisions.md`; per-claim evidence→edge traces are in
`docs/claim_traces.md`.

---

## 1. Central weaknesses of the current gold standards

The prior golds and the prior scorer shared a single failure mode: **they
rewarded wording, not biology.** Concretely:

1. **Every edge counted equally.** A gold with 25 edges gave the same weight to
   the `cGAMP → STING1 → RELA → SASP` mechanistic spine and to a peripheral
   `SASP → immune_cell_recruitment` downstream-phenotype edge. An agent could
   miss the spine and recover the periphery and score the same as the reverse.
   There was no notion that some relationships are *required* and others are
   *credit-if-found*.

2. **Being right in different words counted as being wrong twice.** The prior
   matcher keyed on the `(source, target, rel)` triple. When the agent
   expressed a real relationship with an equivalent representation — RIG-I vs
   MDA5 as the dsRNA sensor, IL6 vs CCL2 vs MMP3 as the late-SASP marker, one
   of three convergent surveillance failures upstream of L1 — it was scored as
   one *missed* gold edge plus one *extra* draft edge. The agent was penalized
   twice for a biologically correct answer phrased differently from the
   curator.

3. **The single most damaging error was invisible.** Collapsing a sensing
   pathway to a shortcut — `CGAS → drives → SASP` (skipping cGAMP → STING1 →
   RELA), or `senescence → drives → SASP` (erasing the entire sensing axis) —
   is the error that destroys the mechanistic value of a curation. In the prior
   scoring it was indistinguishable from a harmless extra edge: both were just
   "an extra." The gold had no way to say "this specific edge is forbidden
   because it asserts a false directness."

4. **Direct vs indirect evidence had no consequence.** Evidence strength was
   recorded but never differentiated in a way tied to whether the mechanism was
   actually established. A canonical-but-unperturbed step (cGAMP → STING1,
   inferred from the field) and a directly measured step (cGAMP quantified by
   LC-MS) were scored the same, so the gold could not express "this link is
   assumed, that one is proven here."

5. **Defect edges were prose, not data.** The one known bad edge (Tyshkovskiy
   `type_I_IFN does_not_drive mortality`) was flagged by a free-text REVIEW
   comment the scorer could only find by string-matching defect phrases —
   brittle and unreproducible.

The through-line: the gold encoded *a* correct description and the scorer
checked for *that* description, so a differently-worded correct curation lost
points and a mechanistically catastrophic shortcut lost none.

---

## 2. Design principles adopted

1. **Tier the relationships.** Split every gold edge into `tier: core`
   (required — the mechanistic claims the paper exists to establish) and
   `tier: supporting` (real, but credit-if-found — modulators, downstream
   phenotypes, in-vivo summaries, marker-level detail). The headline metric is
   **core relationship recall**; supporting recall is reported separately and
   never penalized when missed. Default is `core`, so untagged legacy edges
   keep their old weight.

2. **Score biological equivalence once.** Group interchangeable representations
   of one underlying claim with an `equiv_group` id. The group contributes
   **one** unit to the denominator, is **satisfied** as soon as any member is
   recovered, and the unused alternates are suppressed from *both* missed and
   extra. Being right in different words now counts once, correctly.

3. **Make the forbidden shortcut a scored anti-edge.** A gold edge may carry
   `status: forbidden_shortcut`: a biologically-misleading collapse the agent
   must **not** emit. It is excluded from every recall denominator, and a draft
   edge that matches it is a distinct **`shortcut_violation`** (a precision
   penalty) rather than a silent extra. The most damaging curation error is now
   both named and counted.

4. **Keep evidence strength as a stricter, separate axis.** Evidence-strength
   agreement is reported as its own sub-metric (`evidence-matched`), layered on
   top of endpoint and relationship matching. A right relationship with a
   debatable strength label is visibly "right relationship, different strength"
   — it never reduces core recall.

5. **Structured defects, not prose.** Defect edges are marked with
   `status: excluded` / `score_exclude: true` fields the scorer reads directly.

6. **Additive and backward-compatible.** Every new field (`tier`,
   `equiv_group`, `status`) is optional with a safe default. The validator
   already tolerates unknown edge keys, so no validator change was needed. The
   five legacy golds are unmodified and a regression test locks their scores.

7. **No molecular-level label field (sub-question verdict: Design B).** We
   considered adding an explicit `level` field (molecular / cellular /
   organismal) to each edge. We rejected it. The level is already recoverable
   from the node identity and the `rel` verb (a gene→gene `binds_recruits` edge
   is molecular; a `senescence → tissue_inflammation drives` edge is
   organismal), so a separate field would be redundant data to keep
   consistent, and it would invite scoring by level bucket — exactly the
   wording-over-biology trap we are removing. The tier system already captures
   what a level field was meant to protect: the molecular spine is what we mark
   `core`. See `docs/design_decisions.md` §5 for the full argument.

---

## 3. Files and annotations changed

**New gold files** (drafts left untouched):

- `docs/compendium/dou_2017.gold.md` — 25 edges: 8 core + 15 supporting
  (11 supporting units after 3 equiv groups) + 2 forbidden anti-edges.
- `docs/compendium/dececco_2019.gold.md` — 26 edges: 9 core + 15 supporting
  (9 supporting units after 3 equiv groups) + 2 forbidden anti-edges.
- `docs/compendium/lopez_polo_2024.gold.md` — 31 edges: 9 core + 20 supporting
  (17 supporting units after 3 equiv groups) + 2 forbidden anti-edges.

Each carries the full paper block (controlled entity fields mirrored from the
draft, plus a mechanistic-spine note and an equivalence/forbidden note) and
edge-by-edge `evidence_strength`, `context`, and `support` panels.

**New annotation fields** (all optional, all additive):

- `tier: core | supporting` on every edge (default `core`).
- `equiv_group: <id>` on interchangeable edges.
- `status: forbidden_shortcut` on anti-edges.

**Scorer** (`nasp_compendium/score_compendium.py`): extended `_LoadedEdge` with
`tier` / `equiv_group` / `is_forbidden`; added tier-unit counting, equivalence
collapse (satisfied-once, alternates suppressed from missed/extra), and
forbidden-shortcut splitting; extended `PaperScore` / `ScoreReport` with
`core_recall`, `supporting_recovered`, `shortcut_violations`, and preserved the
existing endpoint metrics. The draft side filters out `forbidden` / `excluded`
rows so gold-only annotations are never read as draft assertions.

**Scorer tests** (`tests/test_score_compendium.py`): added coverage for tiering
(missing supporting doesn't lower core recall; missing core does), equivalence
(counts once, not missed+extra), forbidden shortcut (violation, not silent
extra), a legacy-gold backward-compat lock, and a forbidden-edge self-match
cleanliness test.

**Planning docs**: `docs/design_decisions.md` (schema rationale) and
`docs/claim_traces.md` (per-claim PDF→edge traces) live under `docs/` (not
`docs/compendium/`, so the compendium validator does not parse them as papers).

---

## 4. Before / after, one example per paper

**Dou 2017 — the sensing spine as core; the shortcut forbidden.**
Before: `CGAS → SASP` and the intermediate steps were all edges of equal
weight, and an agent that wrote `CGAS drives SASP` directly lost nothing.
After: `cGAMP → STING1`, `STING1 → RELA`, `RELA → SASP` are `core`; the
denominator requires the spine. `CGAS → drives → SASP` and
`cytoplasmic_chromatin_fragments → drives → SASP` are `status:
forbidden_shortcut` — an agent that emits either scores a `shortcut_violation`.
`IFI16 does_not_drive SASP` is retained as a core specificity negative.

**De Cecco 2019 — the same triple as supporting summary and as forbidden
substitute.** Before: `retrotransposon_derepression → drives → type_I_IFN` was
a single edge; there was no way to say it is a legitimate in-vivo summary but a
forbidden replacement for the cDNA→cGAS→STING spine. After: it appears twice —
once as a `supporting` in-vivo summary edge (credited if found) and once as a
`forbidden_shortcut` anti-edge. The scorer resolves the collision structurally:
a draft's legitimate supporting edge is absorbed by its supporting twin before
shortcut detection runs, so the self-match yields 0 false violations (verified).

**López-Polo 2024 — equivalent sensors counted once; marker collapse
forbidden.** Before: `cytosolic_RNA_sensing → DDX58` and `→ IFIH1` (RIG-I and
MDA5) were two edges; an agent naming only one was marked one missed + one
extra. After: both are `equiv_group: dsrna_sensor` `core` — recovering either
satisfies the one dsRNA-sensor unit. `MAVS → upregulates → CXCL10` (collapsing
the SASP program to one marker) and `cellular_senescence → drives → SASP`
(erasing the axis) are `forbidden_shortcut`.

Measured effect (draft scored against the new gold): all three drafts reach
**100% core recall, 100% supporting recall, 0 shortcut violations.** The only
residual differences are evidence-strength labels — 8 (Dou), 7 (De Cecco),
5 (López-Polo) edges where the curator's strength label differs from the gold's
(e.g. draft calls `cGAMP → STING1` `direct_measured`; gold calls it
`canonical_inferred` because that step was not perturbed in Dou). Under the old
scorer several of these would have surfaced as mismatches; under the new one
they are visibly "right biology, debatable label" and do not touch core recall.

---

## 5. Handling of equivalent, optional, unsupported, and ambiguous claims

- **Equivalent** claims → `equiv_group`. One denominator unit, satisfied once,
  alternates suppressed from missed and extra. Examples: RIG-I/MDA5
  (`dsrna_sensor`); IL6/CCL2/MMP3 late-SASP markers (`sting_late_sasp`,
  `jakstat_late_sasp`); RB1/FOXA1/TREX1 surveillance failures
  (`l1_surveillance`); DDX58→MAVS / IFIH1→MAVS continuity (`sensor_to_mavs`).
- **Optional** claims → `tier: supporting`. Credited when recovered, never
  penalized when missed. Modulators (MFN1/MFN2, POLRMT, PNPT1, ADAR), the
  parallel mtDNA/cGAS-STING branch, downstream in-vivo phenotypes, and
  marker-level detail all live here.
- **Unsupported / forbidden** claims → `status: forbidden_shortcut`. Excluded
  from recall; a draft match is a scored `shortcut_violation`. This is how the
  gold expresses "do not assert this — it is a mechanistically false collapse."
- **Ambiguous** claims → left as a human-adjudication item, not silently
  resolved. The clearest case is the De Cecco summary-vs-forbidden triple
  (§7): the structural rule catches the common failure, but a genuinely
  borderline "summary instead of spine" collapse is flagged for a human.
- **Known-defect** claims → `status: excluded` / `score_exclude: true` (the
  existing structured markers, unchanged).

---

## 6. How the revised standards should be scored

- **Headline metric: core relationship recall** = recovered core units /
  total core units, where an equiv group is one unit satisfied by any member.
  This is the number to track across curation runs.
- **Supporting recall** is reported separately: credited-if-found, never
  subtracted when missed.
- **Forbidden-shortcut violations** are reported as a count and as a precision
  penalty, distinct from ordinary extra edges.
- **Endpoint recall / precision** (the prior metric) is preserved for
  continuity and as the loosest match tier.
- **Evidence-strength agreement** is a stricter sub-metric layered on matched
  edges; it annotates, it does not gate core recall.
- **Defect edges** are dropped from denominators by default.

Match order (unchanged core, extended): normalize endpoints → bucket out
forbidden and excluded gold rows → greedily pair remaining gold and draft edges
best-match-first (endpoints, then relationship, then evidence) → collapse
satisfied equiv groups → split unmatched draft extras into shortcut violations
vs ordinary extras. A perfect curation is 100% core recall, full supporting
credit, and zero shortcut violations.

---

## 7. Remaining human-adjudication items

1. **De Cecco summary-vs-spine collapse.** `retrotransposon_derepression →
   drives → type_I_IFN` is a legitimate `supporting` in-vivo summary and a
   `forbidden` substitute for the cDNA→cGAS→STING spine. The scorer's structural
   rule (supporting twin absorbs the legitimate edge before shortcut detection)
   handles the clean case, but a curation that draws the summary edge *and omits
   the spine* is a real collapse the rule cannot distinguish from a legitimate
   summary. A human should confirm the core spine is present whenever this
   triple appears. (`docs/design_decisions.md` §4.)

2. **Evidence-strength calibration.** The 8/7/5 evidence-only differences are
   defensible either way (is cGAMP → STING1 `canonical_inferred` or
   `direct_measured` in a paper that perturbs STING1 but not the cGAMP-binding
   step directly?). These are curator judgment calls; a human should ratify the
   gold's strength labels rather than treat the scorer's evidence sub-metric as
   ground truth.

3. **Equiv-group membership boundaries.** Whether MMP3 belongs in the same
   late-SASP equivalence class as IL6/CCL2 (it is a protease, not a cytokine)
   is a biological judgment. The current golds group by "co-regulated readout of
   the same program"; a domain expert should confirm each group's membership.

4. **Forbidden-shortcut completeness.** Each gold encodes the two most damaging
   collapses. Whether other shortcuts merit anti-edges (e.g. López-Polo
   `mt-dsRNA → drives → SASP` skipping MAVS) is a curation-policy decision for
   the team.

5. **The parallel-branch tiering in López-Polo.** The mtDNA/cGAS-STING branch
   is marked `supporting` so it does not displace the mt-dsRNA/MAVS spine. If
   the team later decides both branches are co-primary, those four edges should
   be promoted to `core` — a deliberate biological call, not a scoring default.

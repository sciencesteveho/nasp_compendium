### 1. `cross-paper` — Decide whether forbidden shortcuts must be checked before same-endpoint scored edges

**Priority:** Critical

**Verify:**
Decide whether an exact forbidden relationship must be tested before a draft edge is paired to a scored edge that has the same endpoints but a different relationship.

**Inspect:**
`nasp_compendium/score_compendium.py`, `_match_edges` lines 400–474 and `_split_shortcut_violations` lines 524–544; DeCecco Fig. 3b and Extended Data Fig. 7f–g; Dou Fig. 4g and Extended Data Fig. 9b; Jiang Fig. 6a–l; Wang Fig. 6d and Fig. 7a–c.

**Current record:**
DeCecco scores and forbids `retrotransposon_derepression -> type_I_IFN`; Dou scores `CGAS correlates SASP` and forbids `CGAS drives SASP`; Jiang scores `RPSA required_for proinflammatory_cytokines` and forbids `RPSA drives proinflammatory_cytokines`; Wang scores `HNRNPA2B1 upregulates CGAS` and forbids `HNRNPA2B1 activates CGAS`.

**Possible outcomes:**

* **A:** Match exact scored triples, then exact forbidden triples, then same-endpoint relationship mismatches; causal shortcuts receive violations while legitimate alternate relationships remain scoreable.
* **B:** Keep endpoint-first matching and remove or retarget every conflicting scored/forbidden pair; affected gold files lose some summary or anti-edge records.
* **C:** Treat these rows only as relationship tests and remove their forbidden status; shortcut-violation counts become narrower.

**Why it matters:**
Current matching can consume a forbidden draft edge as a relationship mismatch, producing zero shortcut violations.

### 2. `cross-paper` — Decide whether unisolated canonical continuity may count as core recall

**Priority:** Critical

**Verify:**
Set one rule for canonical intermediates that the paper invokes but does not isolate experimentally: core, supporting, or context-only.

**Inspect:**
DeCecco Extended Data Fig. 7c–e; Dou Fig. 1b and Extended Data Fig. 1g; Gulen Figs. 1–3; Lian Fig. 4a–b; Ma Figs. 2d, 2h and 4d; Qin Figs. 1a–d and 3a; Sprenger Figs. 1d,g and 4f.

**Current record:**
Affected core records include DeCecco `CGAS produces cGAMP` and `cGAMP activates STING1`; Dou `CGAS produces cGAMP`; Gulen `TBK1 activates IRF3`, `IRF3 drives type_I_IFN`, and `STING1 drives NF-kB`; Lian `CGAS produces cGAMP`; Ma cGAS–cGAMP–STING–TBK1–IRF3 continuity; Qin cGAS/cGAMP anchors; Sprenger cGAMP/STING/TBK1 continuity.

**Possible outcomes:**

* **A:** Retain invoked continuity as `canonical_inferred` core units; agents must recover canonical topology even when this paper did not test each edge.
* **B:** Retain it as supporting; core recall measures paper-isolated findings while supporting recall measures canonical completeness.
* **C:** Omit unisolated links or use a resolved pathway-level edge; denominators and accepted endpoints shrink.

**Why it matters:**
Different answers can add or remove multiple core units per paper and change what extraction skill the benchmark measures.

### 3. `cross-paper` — Set scoring resolution for combined sensor perturbations

**Priority:** Critical

**Verify:**
Decide whether combined RIG-I/MDA5 perturbation can support separate DDX58 and IFIH1 causal units or only one grouped sensing unit.

**Inspect:**
Lopez-Polo Fig. 2e–g and Fig. 3a–i; Mao Fig. 5k–m; Qin Fig. 2a–g.

**Current record:**
Lopez-Polo separately scores `cytosolic_RNA_sensing activates DDX58`, `... activates IFIH1`, `DDX58 activates MAVS`, and `IFIH1 activates MAVS`; Mao separately scores retroelement RNA activation of DDX58 and IFIH1; Qin uses the broad target `RIG-I/MDA5-MAVS` although only RIG-I is experimentally localized.

**Possible outcomes:**

* **A:** Require individual perturbation or binding evidence for individual causal units; use one grouped sensing-to-MAVS unit where only combined tests exist.
* **B:** Keep individual edges as `canonical_inferred` alternatives in one equivalence unit; endpoint variants receive credit without claiming individual isolation.
* **C:** Retain all individual perturbation-supported units; agents receive multiple core credits from one combined experiment.

**Why it matters:**
This rule changes core unit counts and whether broad pathway attribution is rewarded as sensor-specific extraction.

### 4. `cross-paper` — Decide when a measured distal net effect is a scored summary or a forbidden shortcut

**Priority:** Critical

**Verify:**
Set one policy for source perturbations that change a distal output while the same paper preserves intervening mechanistic steps.

**Inspect:**
DeCecco Fig. 3a–c and Extended Data Fig. 7f–g; Gulen Fig. 4b–d; Lopez-Polo Figs. 1h, 4c–h and 5i; Sprenger Figs. 6d–e and 7.

**Current record:**
Examples are DeCecco `retrotransposon_derepression required_for type_I_IFN`, Gulen `CGAS drives microglial_activation`, Lopez-Polo MFN1/MFN2/POLRMT-to-SASP records, and Sprenger `pyrimidine_metabolism drives type_I_IFN`.

**Possible outcomes:**

* **A:** Score only the nearest supported step and move the distal effect into context; direct distal drafts are forbidden or ordinary extras.
* **B:** Allow distal edges only as supporting summaries; they cannot substitute for core intermediate recall.
* **C:** Accept them as alternate core representations when the source perturbation directly changes the output; mechanistic intermediates become optional.

**Why it matters:**
This convention determines whether agents are rewarded or penalized for collapsing a resolved mechanism into a true but broad net effect.

### 5. `cross-paper` — Decide whether common-upstream co-outcomes support causal mediation edges

**Priority:** Critical

**Verify:**
Decide whether concurrent changes after one upstream intervention justify directed edges between the downstream outcomes.

**Inspect:**
DeCecco Fig. 4c,e and Extended Data Figs. 9–10; Gulen Figs. 1h, 2a–c and 4h–k; Martinez Fig. 1a–f.

**Current record:**
DeCecco scores `SASP drives immune_cell_recruitment` and `immune_cell_recruitment drives tissue_inflammation`; Gulen scores `microglial_activation drives neurodegeneration`, `neurodegeneration drives cognitive_decline`, and `hippocampal_neuron_loss drives cognitive_decline`; Martinez scores `tissue_inflammation drives fibrosis/accelerated_aging`.

**Possible outcomes:**

* **A:** Remove causal mediation edges unless the mediator is independently perturbed; keep co-outcomes in upstream-edge context.
* **B:** Retain non-causal association or membership edges as supporting records.
* **C:** Retain author-model causal edges as core; agents must reproduce mediation not experimentally isolated.

**Why it matters:**
These edges can turn parallel phenotypes into several core causal units and materially alter relationship scoring.

### 6. `cross-paper` — Require explicit tier decisions instead of silently treating every edge as core

**Priority:** Critical

**Verify:**
Decide whether missing `tier` may continue to mean core in candidate gold files or whether every scored edge must be explicitly assigned core or supporting.

**Inspect:**
All records in `gulen_2023.md`, `lian_2018.gold.md`, `mao_2024.gold.md`, `martinez_2024.gold.md`, `qin_2024.gold.md`, and `tyshkovskiy_2026.gold.md`; scorer `_edge_tier` default.

**Current record:**
These six files omit `tier`, so canonical anchors, correlative cohort edges, specificity controls, speculative branches, and central mechanisms all enter headline core recall.

**Possible outcomes:**

* **A:** Require explicit tiers before calibration; paper-defining isolated mechanisms remain core and secondary/canonical/correlative records become supporting.
* **B:** Preserve default-core semantics and adjudicate only individual suspect records.

**Why it matters:**
An implicit default can change headline recall more than any single biological edge decision.

### 7. `cross-paper` — Decide whether `equiv_group` may collapse independent mechanistic branches

**Priority:** Critical

**Verify:**
Confirm whether equivalence means interchangeable representation of one claim, not merely multiple edges with a shared target or theme.

**Inspect:**
DeCecco Fig. 2a–g; Dou Extended Data Fig. 2f–h; Sprenger Extended Data Figs. 1g–h and 3a–b; Wang Figs. 6d and 7a–f.

**Current record:**
Potentially non-equivalent groups are DeCecco `l1_surveillance` (RB1, FOXA1, TREX1), Dou `ifnb1_suppression` (p38 and IL1A), Sprenger `excluded_triggers` (fragmentation, BAX/BAK, RNA sensing), and Wang `amplified_sensor_mrnas` (CGAS, IFI16, STING1).

**Possible outcomes:**

* **A:** Remove these groups and score each independently supported branch; supporting denominators rise.
* **B:** Regroup only genuinely substitutable representations, such as alternative sensor endpoints, and score distinct mechanisms separately.
* **C:** Keep theme-level equivalence; recovery of any member satisfies the whole family.

**Why it matters:**
Over-broad equivalence hides omitted branches and can overstate agent recall.

### 8. `cross-paper` — Define how exhaustive forbidden-shortcut coverage must be

**Priority:** Critical

**Verify:**
Decide whether forbidden rows enumerate every foreseeable endpoint variant or only representative major shortcuts.

**Inspect:**
Lian Figs. 1–7; Lopez-Polo Fig. 3i; Ma Fig. 2d; Martinez Figs. 1–7; Qin Figs. 1–5; Sprenger Figs. 6–7; Jiang Supplementary Fig. 4.

**Current record:**
Lian, Martinez, and Qin have no formal forbidden rows; Lopez-Polo forbids only `MAVS -> CXCL10` despite CCL2/B2M variants; Ma forbids only `PRMT5 -> type_I_IFN`; Sprenger forbids only `YME1L1 -> CGAS`; Jiang covers RELA but not an `NF-kB` endpoint variant.

**Possible outcomes:**

* **A:** Add all high-probability variants that erase paper-defining intermediates; shortcut penalties become comprehensive.
* **B:** Add only one or two major distal variants per paper and document that other collapses count as extras.
* **C:** Remove anti-edge enumeration and rely on relationship/extras diagnostics plus human review.

**Why it matters:**
Equivalent biological shortcuts currently receive different penalties solely because their endpoint spelling was or was not anticipated.

### 9. `tyshkovskiy_2026` — Decide whether this non-mechanistic resource paper belongs in NASP core calibration

**Priority:** Critical

**Verify:**
Decide whether a paper with no nucleic-acid sensor, adaptor, or NASP perturbation should contribute core mechanistic recall units.

**Inspect:**
Abstract; Figs. 1–6; paper Discussion describing mortality clocks and shared ageing signatures.

**Current record:**
Nine non-excluded records default to core, including biomarker, interferon-module, senescence, inflammation, parabiosis, and embryogenesis associations.

**Possible outcomes:**

* **A:** Exclude the paper from mechanistic calibration; retain metadata only.
* **B:** Keep observed-mortality biomarker edges as a separate resource-paper stratum and make clock/module associations supporting.
* **C:** Keep all current records in core recall.

**Why it matters:**
Including a resource paper as ordinary core biology changes what conclusions about extraction performance mean.

### 10. `mao_2024` — Remove or reinterpret the sign-inverted ATF3 negative

**Priority:** Critical

**Verify:**
Verify whether promoter non-binding can justify `ATF3 does_not_drive type_I_IFN` when ATF3 perturbation increases the IFN branch indirectly.

**Inspect:**
Figs. 4g–p and 5g–m; Extended Data Fig. 5c–d.

**Current record:**
`ATF3 does_not_drive type_I_IFN`, `direct_measured`, core.

**Possible outcomes:**

* **A:** Remove the negative and keep promoter non-binding in context; ATF3’s positive net effect remains represented through ERV/RLR intermediates.
* **B:** Replace it with a forbidden positive shortcut `ATF3 drives type_I_IFN`; agents are penalized for skipping the ERV–RNA-sensing chain.
* **C:** Retain the negative only if its target is narrowed to direct promoter regulation rather than the IFN programme.

**Why it matters:**
Current gold rewards an absent causal sign opposite to the paper’s perturbation results.

### 11. `sprenger_2021` — Correct the title-defining pyrimidine mechanism and its proximal target

**Priority:** Critical

**Verify:**
Decide whether the causal source is pyrimidine deficiency/imbalance and whether its scored target should be mtDNA release rather than type-I IFN.

**Inspect:**
Figs. 5–7, especially Fig. 6a–e and Fig. 7; model in Fig. 8.

**Current record:**
`pyrimidine_metabolism drives type_I_IFN`, `perturbation_supported`, supporting.

**Possible outcomes:**

* **A:** Replace with `pyrimidine_imbalance drives cytoplasmic_mtDNA` or `mtDNA_release`; the core topology gains the paper’s metabolic intermediate without a distal shortcut.
* **B:** Keep a proximal corrected edge plus a supporting net IFN summary.
* **C:** Retain the current edge; normal metabolism remains encoded as the positive driver and intermediate recall stays optional.

**Why it matters:**
Source sign and target granularity define whether an agent can recover the paper’s central mechanism.

### 12. `tyshkovskiy_2026` — Separate mortality-clock output from biological mortality

**Priority:** Critical

**Verify:**
Decide whether changes in predicted mortality-associated transcriptomic age may use `mortality` as the biological endpoint.

**Inspect:**
Fig. 6a–e and Extended Data Fig. 9; Methods describing mortality tAge; external parabiosis lifespan citation 54.

**Current record:**
`heterochronic_parabiosis negatively_correlates mortality` and `early_embryogenesis negatively_correlates mortality`, both core.

**Possible outcomes:**

* **A:** Remove both biological edges and retain clock changes in context.
* **B:** Add a reviewed `mortality_associated_transcriptomic_age` endpoint and retarget both edges; model output becomes explicit.
* **C:** Retain `mortality` as a declared proxy; agents receive biological endpoint credit for predicting a clock output.

**Why it matters:**
Conflating proxy predictions with observed deaths can invalidate endpoint-recall conclusions.

### 13. `lopez_polo_2024` — Decide whether the mtDNA/cGAS–STING branch is paper-generated or imported

**Priority:** Critical

**Verify:**
Verify whether this paper resolves BAX/BAK-dependent mtDNA release and individual CGAS/STING wiring or only a combined cGAS/STING contribution to SASP.

**Inspect:**
Fig. 2f,h; Supplementary Fig. 4h,j; Introduction, Results, and Discussion citations to prior mtDNA-release work.

**Current record:**
Supporting chain `BAX/BAK_pore forms_pore_for cytoplasmic_mtDNA`, `cytoplasmic_mtDNA activates CGAS`, `CGAS activates STING1`, `STING1 drives SASP`.

**Possible outcomes:**

* **A:** Replace four units with one supporting set-level `cGAS-STING required_for SASP`; imported mtDNA topology stays in context.
* **B:** Retain the internal branch as `canonical_inferred` supporting continuity and state that only combined CGAS/STING depletion was tested.
* **C:** Keep all four current units as paper-supported findings.

**Why it matters:**
Four expected endpoints currently derive largely from prior biology and a combined perturbation.

### 14. `dececco_2019` — Choose the correct source for reverse-transcriptase dependence

**Priority:** High

**Verify:**
Decide whether the 3TC/K-9 result supports an edge from retrotransposon derepression, reverse-transcriptase activity, or only cDNA production.

**Inspect:**
Fig. 3a–c; Extended Data Figs. 5i, 7f–g, and 9d.

**Current record:**
`retrotransposon_derepression required_for type_I_IFN`, core; same endpoints also appear in a supporting edge and forbidden row.

**Possible outcomes:**

* **A:** Use `L1_reverse_transcriptase_activity required_for type_I_IFN`; add/review the endpoint and remove the same-endpoint conflict.
* **B:** Keep RT dependence only in `retrotransposon_derepression produces cytoplasmic_retroelement_cDNA` context; remove the distal core unit.
* **C:** Retain the current edge and remove its conflicting forbidden treatment.

**Why it matters:**
The manipulated activity is distinct from derepression, and the choice adds or removes a core recall unit.

### 15. `dececco_2019` — Decide how much JAK–STAT causality the IFNAR experiments support

**Priority:** High

**Verify:**
Verify whether IFNAR-dependent STAT activation supports both JAK–STAT edges at `perturbation_supported` strength.

**Inspect:**
Fig. 3d,f; Extended Data Figs. 5m, 6f, and 7a–b.

**Current record:**
Core `type_I_IFN activates JAK-STAT` and `JAK-STAT drives SASP`; supporting JAK–STAT-to-IL6/CCL2/MMP3 equivalence group.

**Possible outcomes:**

* **A:** Keep the first edge perturbation-supported but make `JAK-STAT drives SASP` and marker edges `canonical_inferred`; no JAK or STAT was perturbed for SASP.
* **B:** Replace the second edge with `IFNAR_signaling required_for late_SASP`; preserve the measured receptor-level result.
* **C:** Keep the current branch-continuity interpretation and all five records.

**Why it matters:**
One receptor experiment currently creates two core and one supporting recall units at a more specific pathway level.

### 16. `dececco_2019` — Decide whether the IFN-independent STING1-to-IL1B branch is required

**Priority:** High

**Verify:**
Verify whether the positive STING1-dependent IL1B result should accompany the existing negative `type_I_IFN does_not_drive IL1B` edge.

**Inspect:**
Fig. 3d,f and Extended Data Fig. 7e.

**Current record:**
Core negative `type_I_IFN does_not_drive IL1B`; no positive `STING1 -> IL1B` record.

**Possible outcomes:**

* **A:** Add `STING1 upregulates IL1B`, core or supporting, outside the late-SASP equivalence group.
* **B:** Keep the positive branch only in the negative edge’s context; no new recall unit.

**Why it matters:**
Without the positive branch, an agent can recover the negative while missing the experiment’s pathway-localization result.

### 17. `dou_2017` — Change or retain the SASP-to-IL1A relationship

**Priority:** High

**Verify:**
Decide whether IL1A is a measured SASP component or a downstream state induced by the SASP programme.

**Inspect:**
Fig. 1c, Fig. 2c, and Extended Data Fig. 2b,g–h.

**Current record:**
`SASP induces IL1A`, `direct_measured`, supporting.

**Possible outcomes:**

* **A:** Change to `SASP contains IL1A`; relationship scoring reflects programme membership while preserving reuse in the IFNB1 branch.
* **B:** Replace with a tested regulator-to-IL1A edge if causal regulation is the intended claim.
* **C:** Retain `induces`; agents receive causal relationship credit for component measurement.

**Why it matters:**
Endpoints stay fixed, but relationship and exact-recovery conclusions change.

### 18. `dou_2017` — Decide whether senescence triggers are alternate models or three recall units

**Priority:** High

**Verify:**
Decide whether oncogenic RAS, DNA damage, and replicative exhaustion should remain one supporting equivalence unit.

**Inspect:**
Fig. 1a,c; Figs. 2–3; Extended Data Figs. 1b, 2a–d, 5a–c, and 6a–e.

**Current record:**
Three trigger-to-senescence edges share `equiv_group: senescence_trigger`.

**Possible outcomes:**

* **A:** Keep one unit because these are alternative entry models used to generalize the novel downstream mechanism.
* **B:** Split into three supporting units because exhaustive trigger recovery is part of evaluation.

**Why it matters:**
The choice changes supporting recall weighting without changing the paper’s mechanistic spine.

### 19. `dou_2017` — Retain, narrow, or remove the aggregate MAVS negative

**Priority:** High

**Verify:**
Verify whether the available data support literal `MAVS does_not_correlate SASP` or only absence of a broad coherent association.

**Inspect:**
Extended Data Fig. 9d and Supplementary Table 4; note whether Supplementary Table 4 is available outside the PDF.

**Current record:**
`MAVS does_not_correlate SASP`, supporting, with context claiming CCLE/TCGA specificity.

**Possible outcomes:**

* **A:** Remove the scored negative and keep the mixed panel in context; supporting denominator decreases by one.
* **B:** Retain with narrowed wording: MAVS lacks a broad SASP-program association despite some significant markers.
* **C:** Retain the absolute cross-cohort negative only after Supplementary Table 4 confirms it.

**Why it matters:**
The current aggregate negative can reward an agent for overstating a mixed marker panel.

### 20. `gulen_2023` — Replace the unsupported senescence source of mitochondrial dysfunction

**Priority:** High

**Verify:**
Verify whether Fig. 3e establishes senescence, aging, or only mitochondrial abnormality in aged microglia.

**Inspect:**
Fig. 3e and its legend; surrounding Results text.

**Current record:**
`cellular_senescence induces mitochondrial_dysfunction`, `direct_measured`, core.

**Possible outcomes:**

* **A:** Remove the edge and start the chain at mitochondrial dysfunction.
* **B:** Replace with `aging correlates mitochondrial_dysfunction` at observational strength.
* **C:** Retain only if senescence is independently established in those microglia.

**Why it matters:**
The current core edge inserts an unmeasured biological state and causal direction.

### 21. `gulen_2023` — Set evidence strength for the VDAC pore step

**Priority:** High

**Verify:**
Decide whether VBIT-4 suppression of downstream transcripts supports pore-mediated mtDNA release or only branch plausibility.

**Inspect:**
Fig. 3e–g; Extended Data Fig. 6e; cited external reference 30.

**Current record:**
`mitochondrial_dysfunction drives VDAC_oligomerization`, `canonical_inferred`; `VDAC_oligomerization forms_pore_for cytoplasmic_mtDNA`, `perturbation_supported`.

**Possible outcomes:**

* **A:** Keep the topology but make the pore edge `canonical_inferred`; neither oligomers nor VBIT-4-dependent mtDNA release was measured.
* **B:** Replace with a broader VDAC-dependent branch edge and keep physical pore transit in context.
* **C:** Retain perturbation-supported strength.

**Why it matters:**
Exact-evidence scoring currently credits an atomic pore experiment not performed in this paper.

### 22. `gulen_2023` — Choose the paper-specific STING output topology

**Priority:** High

**Verify:**
Decide whether to retain unmeasured IRF3/NF-kB intermediates, add a direct STING-to-IFN edge, or use both at different tiers.

**Inspect:**
Figs. 1a–e, 2d, and 3c–d; Extended Data Figs. 2f, 3, and 4a–i; external IRF3 reference 27.

**Current record:**
Core `STING1 activates TBK1`, `TBK1 activates IRF3`, `IRF3 drives type_I_IFN`, and `STING1 drives NF-kB`; no `STING1 -> type_I_IFN` record.

**Possible outcomes:**

* **A:** Keep STING–TBK1 paper-supported, keep IRF3 continuity canonical, and remove unassayed NF-kB.
* **B:** Add a supporting direct `STING1 drives type_I_IFN` summary while retaining canonical intermediates.
* **C:** Replace the unmeasured chain with direct perturbation-supported STING-to-IFN output.

**Why it matters:**
The choice changes core endpoints and tests canonical reconstruction versus paper-specific extraction.

### 23. `gulen_2023` — Add or omit the negative showing STING does not maintain senescence

**Priority:** High

**Verify:**
Decide whether post-senescence H-151 non-effects are a required specificity edge.

**Inspect:**
Extended Data Fig. 2c–e and corresponding main text.

**Current record:**
No `STING1 does_not_drive cellular_senescence` edge.

**Possible outcomes:**

* **A:** Add a core or supporting negative; agents must separate SASP control from the senescence state.
* **B:** Keep the negative only in `STING1 drives SASP` context.

**Why it matters:**
This specificity finding blocks a plausible false mechanism and changes negative-edge recall.

### 24. `gulen_2023` — Decide whether frailty is a required organismal endpoint

**Priority:** High

**Verify:**
Decide whether improved grip strength and treadmill performance justify a scored STING-to-frailty edge.

**Inspect:**
Fig. 1f–g and Results text describing frailty.

**Current record:**
No frailty edge; functional outcomes appear only outside the graph.

**Possible outcomes:**

* **A:** Add `STING1 drives frailty`, supporting or core, with H-151 context.
* **B:** Retain functional outcomes in context because broad organismal endpoints are outside gold recall.

**Why it matters:**
The paper’s intervention benefit can be invisible to recall scoring.

### 25. `gulen_2023` — Tier or remove the ND-MG microglial-state edge

**Priority:** High

**Verify:**
Verify whether ND-MG expansion is significant and sufficiently paper-specific to equal DAM and IFN-MG as a core causal unit.

**Inspect:**
Fig. 4e–g and Extended Data Fig. 9b–e.

**Current record:**
Separate default-core `CGAS drives DAM_microglial_state`, `IFN_MG_microglial_state`, and `ND_MG_microglial_state` edges.

**Possible outcomes:**

* **A:** Keep DAM and IFN-MG core; make ND-MG supporting or remove it.
* **B:** Retain all three distinct core states.
* **C:** Use one reactive-microglial-state equivalence unit only if state identity is not the tested extraction capability.

**Why it matters:**
Three state labels currently carry equal core weight despite unequal statistical and external-dataset support.

### 26. `jiang_2023` — Reverse or split the viral-nucleic-acid sensing edge

**Priority:** High

**Verify:**
Decide whether sensing topology should be ligand-to-RPSA and whether viral DNA and RNA deserve separate or equivalent endpoints.

**Inspect:**
Fig. 1d–m and Supplementary Fig. 1g.

**Current record:**
`RPSA binds_recruits viral_nucleic_acids`, `direct_measured`, core.

**Possible outcomes:**

* **A:** Reverse to `viral_nucleic_acids binds_recruits RPSA`; directed endpoint scoring follows ligand-to-sensor convention.
* **B:** Split viral DNA and viral RNA as equivalent alternatives worth one unit.
* **C:** Retain reverse generic direction as an explicit symmetric-binding exception.

**Why it matters:**
The scorer does not generally treat physical-binding direction as symmetric.

### 27. `jiang_2023` — Replace or downgrade the linear SMARCA5–accessibility–RELA chain

**Priority:** High

**Verify:**
Verify whether SMARCA5 was perturbed to test accessibility and whether chromatin accessibility can be said to bind/recruit RELA.

**Inspect:**
Figs. 3b–g, 4c–d, and 5c–h; Supplementary Figs. 5b–g and 7b–d.

**Current record:**
`SMARCA5 activates chromatin_accessibility` followed by `chromatin_accessibility binds_recruits RELA`, both perturbation-supported core.

**Possible outcomes:**

* **A:** Use parallel `RPSA drives chromatin_accessibility` and `SMARCA5 binds_recruits RELA`; retain RPSA-dependent promoter occupancy in context.
* **B:** Keep the linear chain as canonical/inferential continuity.
* **C:** Retain current perturbation-supported topology.

**Why it matters:**
Current chain turns RPSA-loss co-effects into a two-step causal mechanism not isolated experimentally.

### 28. `lian_2018` — Add the directly measured ligand-binding edges

**Priority:** High

**Verify:**
Decide whether dsDNA binding to ZCCHC3 and CGAS is required core recall rather than context for ZCCHC3 activation.

**Inspect:**
Fig. 5a,c and Fig. 6a–d.

**Current record:**
No ligand-to-ZCCHC3 or ligand-to-CGAS edge; binding appears inside `ZCCHC3 activates CGAS` context.

**Possible outcomes:**

* **A:** Add `cytosolic_dsDNA binds_recruits ZCCHC3` and `... binds_recruits CGAS`, both direct-measured core.
* **B:** Add only the novel ZCCHC3 ligand edge and keep canonical CGAS binding in context.
* **C:** Keep both context-only to avoid extra core weighting.

**Why it matters:**
Central ligand/co-sensor evidence is otherwise absent from endpoint recall.

### 29. `lian_2018` — Decide whether ZCCHC3 binding and activation count as two core units

**Priority:** High

**Verify:**
Decide whether physical association and functional activation of the same ZCCHC3–CGAS endpoint pair test distinct extraction capabilities.

**Inspect:**
Figs. 4a–f, 5a–c, 6a–f, and 7a–c.

**Current record:**
Default-core `ZCCHC3 binds_recruits CGAS` and `ZCCHC3 activates CGAS` are separate units.

**Possible outcomes:**

* **A:** Keep both core because binding and co-sensor activation are independently demonstrated.
* **B:** Make binding supporting while activation remains core.
* **C:** Group them as equivalent if either representation is sufficient.

**Why it matters:**
This choice changes headline weighting for one endpoint pair.

### 30. `cross-paper` — Decide when measured activation states become mechanism nodes

**Priority:** High

**Verify:**
Set one rule for representing experimentally measured dimerization, demethylation, translocation, or aggregation as nodes rather than context.

**Inspect:**
Lopez-Polo Figs. 3b–f and 4f; Wang Figs. 3c–d, 4a–f, and 5c–i.

**Current record:**
Lopez-Polo lists `MAVS_aggregation` in metadata but folds it into MAVS edges; Wang folds HNRNPA2B1 dimerization, Arg226 demethylation, and nuclear export into gene-level contexts.

**Possible outcomes:**

* **A:** Keep modification states folded into gene nodes; add only process edges when the state is independently causal and reusable.
* **B:** Add `MAVS_aggregation` and selected HNRNPA2B1 process nodes as supporting/core intermediates.
* **C:** Allow aggregation as a state-as-mechanism exception but keep PTM/export states in context.

**Why it matters:**
The rule changes chain topology and whether agents are rewarded for extracting measured state transitions.

### 31. `lopez_polo_2024` — Remove or narrow the DHX58 functional negative

**Priority:** High

**Verify:**
Verify whether unchanged DHX58 expression establishes that LGP2 does not drive the pathway.

**Inspect:**
Fig. 2e and Supplementary Fig. 4i.

**Current record:**
`cellular_senescence does_not_drive DHX58`, `direct_measured`, core.

**Possible outcomes:**

* **A:** Remove the edge; unchanged abundance is not a functional perturbation.
* **B:** Make it supporting `does_not_correlate` or context-only expression specificity.
* **C:** Retain core if non-induction itself is intended sensor-attribution evidence.

**Why it matters:**
Current gold converts an expression non-change into a core functional exclusion.

### 32. `lopez_polo_2024` — Decide whether the MAVS-to-NF-kB branch is required

**Priority:** High

**Verify:**
Decide whether siMAVS RNA-seq support is sufficient for an explicit parallel NF-kB edge.

**Inspect:**
Fig. 3g–h and external canonical MAVS reference 21.

**Current record:**
Core `MAVS drives type_I_IFN` and `MAVS drives SASP`; no MAVS-to-NF-kB edge.

**Possible outcomes:**

* **A:** Add `MAVS activates NF-kB`, supporting or core, `perturbation_supported`.
* **B:** Keep NF-kB in context because pathway enrichment is not independently validated across models.

**Why it matters:**
Omitting the parallel branch can undercount mechanistic recall; adding it can overread a transcriptomic signature.

### 33. `ma_2021` — Represent PRMT5-mediated CGAS methylation as direct chemistry or net suppression

**Priority:** High

**Verify:**
Decide which edge represents the paper-specific methylation mechanism and whether the singleton equivalence group has any scoring purpose.

**Inspect:**
Figs. 2i–j, 3a–k, 4a–i, and 5a–h; Supplementary Fig. 2l.

**Current record:**
`PRMT5 inhibits CGAS`, `direct_measured`, sole member of `equiv_group: prmt5_cgas_methylation`.

**Possible outcomes:**

* **A:** Use `PRMT5 suppresses CGAS`, `perturbation_supported`; keep direct Arg124 methylation in context and remove the singleton group.
* **B:** Add a reviewed methylation-process representation as a genuine equivalent alternative.
* **C:** Retain current relationship/evidence and group.

**Why it matters:**
The current edge conflates directly measured methylation with perturbation-supported functional suppression.

### 34. `ma_2021` — Adjudicate the cGAS–cGAMP–STING–TBK1–IRF3 evidence boundary

**Priority:** High

**Verify:**
Classify each core spine edge using only experiments that isolate that source–target relation.

**Inspect:**
Figs. 2a–h, 4d–i, and 6a–b,g–h; Supplementary Figs. 2b,d and 4e.

**Current record:**
`CGAS produces cGAMP / perturbation_supported`; `cGAMP activates STING1 / canonical_inferred`; `STING1 activates TBK1 / perturbation_supported`; `TBK1 activates IRF3 / perturbation_supported`; `IRF3 drives type_I_IFN / direct_measured`.

**Possible outcomes:**

* **A:** Keep CGAS-to-cGAMP perturbation-supported, make downstream unisolated wiring canonical, and change IRF3 output to `induces`.
* **B:** Apply strict edge isolation and make all five links canonical unless their source was directly perturbed.
* **C:** Retain current branch-continuity strengths.

**Why it matters:**
Five core exact-recovery expectations depend on where canonical inference ends and paper-specific continuity begins.

### 35. `ma_2021` — Compress or retain the NF-kB cytokine-marker branch

**Priority:** High

**Verify:**
Decide whether Supplementary Fig. 2i–k supports three causal edges or one supporting cytokine-program record.

**Inspect:**
Supplementary Fig. 2i–k.

**Current record:**
`STING1 activates NF-kB`; equivalent `NF-kB drives TNF` and `NF-kB drives IL6`, all supporting.

**Possible outcomes:**

* **A:** Use one `NF-kB drives proinflammatory_cytokines` supporting edge and classify unisolated wiring as canonical.
* **B:** Retain TNF/IL6 as one equivalence unit.
* **C:** Omit the branch because neither STING nor NF-kB was independently perturbed for these outputs.

**Why it matters:**
Marker compression and causal strength change supporting recall and exact diagnostics.

### 36. `ma_2021` — Decide whether the cGAS-dependent in-vivo rescue adds a scored endpoint

**Priority:** High

**Verify:**
Decide whether reduced HSV-1 burden and improved survival deserve a non-shortcut supporting edge.

**Inspect:**
Fig. 6a–j, including loss of survival benefit in `Cgas−/−` mice.

**Current record:**
No antiviral-host-defense, viral-replication, or survival edge.

**Possible outcomes:**

* **A:** Extend the spine with `type_I_IFN drives antiviral_host_defense` or `type_I_IFN suppresses HSV1_replication`, supporting.
* **B:** Keep outcomes in context because IFN itself was not blocked and no approved endpoint avoids a broad shortcut.
* **C:** Add a direct PRMT5/CGAS-to-survival edge and formally accept it as a summary.

**Why it matters:**
The paper’s main in-vivo rescue can be absent from recall or represented at misleading granularity.

### 37. `mao_2024` — Add or omit the SA-ERV-to-senescence feedback edge

**Priority:** High

**Verify:**
Decide whether direct SA-ERV knockdown effects on p16, p21, and LMNB1 warrant a distinct feedback edge.

**Inspect:**
Fig. 5k–m.

**Current record:**
SA-ERV knockdown appears inside `ATF3 induces cellular_senescence` context; no retrotransposon-to-senescence edge.

**Possible outcomes:**

* **A:** Add `retrotransposon_derepression induces cellular_senescence`, `perturbation_supported`, without claiming IFN mediation.
* **B:** Keep the net feedback in context because it skips RLR/IFN intermediates.
* **C:** Add it as a supporting summary that cannot substitute for core pathway recall.

**Why it matters:**
The current graph attributes a distinct rescue experiment to ATF3 and can miss feedback recall.

### 38. `mao_2024` — Retain, demote, or remove the IFN-to-SASP edge

**Priority:** High

**Verify:**
Verify whether IFN is experimentally upstream of the SASP or whether both are parallel ATF3/ERV outputs.

**Inspect:**
Fig. 5a–b and Extended Data Fig. 4d–e,h–i.

**Current record:**
`type_I_IFN drives SASP`, `canonical_inferred`, core.

**Possible outcomes:**

* **A:** Remove the edge and keep SASP as a parallel output.
* **B:** Make it supporting canonical continuity.
* **C:** Retain core despite absent IFN or receptor perturbation.

**Why it matters:**
This edge adds a core causal bridge not isolated by the paper.

### 39. `mao_2024` — Remove or redefine the IFN-to-inflammaging edge

**Priority:** High

**Verify:**
Verify whether inflammaging is an operationally measured endpoint rather than Discussion framing.

**Inspect:**
Fig. 8h–i; Extended Data Fig. 6f–h; Discussion and cited external reference 46.

**Current record:**
`type_I_IFN drives inflammaging`, `strong_correlative`, core.

**Possible outcomes:**

* **A:** Remove the edge; retain `aging correlates type_I_IFN` as the measured bridge.
* **B:** Change to a supporting non-causal association if the observed age-associated inflammatory state is defined as inflammaging.
* **C:** Retain the core causal edge.

**Why it matters:**
Current gold assigns core causal credit to an endpoint not independently measured or perturbed.

### 40. `mao_2024` — Decide whether aging-to-ATF3 and aging-to-epigenetic-remodeling are required

**Priority:** High

**Verify:**
Decide whether these measured aging bridges should be explicit edges or remain context for ERV/IFN associations.

**Inspect:**
Fig. 6a–f; Fig. 8a–c,g,i; Extended Data Fig. 6b,e.

**Current record:**
`aging correlates retrotransposon_derepression` and `aging correlates type_I_IFN`; no aging-to-ATF3 or aging-to-epigenetic-remodeling edge.

**Possible outcomes:**

* **A:** Add both as supporting or core correlative bridges.
* **B:** Add only aging-to-ATF3 because it is a named regulator in the mechanistic spine.
* **C:** Keep both in context to avoid overweighting public/cohort analyses.

**Why it matters:**
These choices determine whether an agent must recover the paper’s link from aging into the mechanistic chain.

### 41. `mao_2024` — Approve the retroelement dsRNA endpoint name and scope

**Priority:** High

**Verify:**
Decide whether `cytoplasmic_retroelement_RNA` is sufficiently specific or should explicitly encode dsRNA.

**Inspect:**
Figs. 2i, 3a–e, and 5k–l; RNA-FISH, strand-specific RNA-seq, J2 dsRIP-seq, and RNase-protection experiments.

**Current record:**
Pending proposed term `cytoplasmic_retroelement_RNA` appears in three core edges.

**Possible outcomes:**

* **A:** Approve `cytoplasmic_retroelement_dsRNA` and retarget the production/sensing edges.
* **B:** Define the existing term narrowly as duplex retroelement RNA and retain it.
* **C:** Use only a grouped `cytosolic_RNA_sensing` endpoint; ligand-specific recall disappears.

**Why it matters:**
One unresolved vocabulary choice affects three core endpoint matches and cross-paper ligand consistency.

### 42. `martinez_2024` — Choose localization or functional-maintenance semantics for nuclear CGAS

**Priority:** High

**Verify:**
Decide whether CGAS directly binds/recruits heterochromatin organization or is required for maintaining it.

**Inspect:**
Fig. 7a–c; Supplementary Fig. 6a; external nucleosome-domain reference 58.

**Current record:**
`CGAS binds_recruits heterochromatin_organization`, `direct_measured`, core.

**Possible outcomes:**

* **A:** Use `CGAS required_for heterochromatin_organization`, `perturbation_supported`; keep colocalization in context.
* **B:** Retain the localization edge but narrow its claim to CGAS/H3K9me3 colocalization.
* **C:** Keep direct binding semantics.

**Why it matters:**
Relationship and evidence scoring currently treat colocalization as direct binding to an organizational process.

### 43. `martinez_2024` — Set causality for chromatin remodeling to retrotransposon derepression

**Priority:** High

**Verify:**
Verify whether chromatin state was independently perturbed or rescued before claiming it drives L1 derepression.

**Inspect:**
Figs. 3a–d, 4a–h, 5e, and 6a–d.

**Current record:**
`epigenetic_remodeling drives retrotransposon_derepression`, `perturbation_supported`, core.

**Possible outcomes:**

* **A:** Retain as perturbation-supported branch continuity under CGAS loss.
* **B:** Downgrade to canonical/inferential author-model wiring.
* **C:** Replace with direct `CGAS suppresses retrotransposon_derepression`, accepting loss of the measured chromatin intermediate.

**Why it matters:**
The edge controls whether co-occurring chromatin and expression changes count as causal topology.

### 44. `martinez_2024` — Demote or remove SPI1 as a causal inflammatory regulator

**Priority:** High

**Verify:**
Decide whether motif enrichment plus modest SPI1 expression supports a causal regulator edge.

**Inspect:**
Fig. 2a–b and Fig. 5b–c; text saying inflammation/fibrosis “may be mediated” by SPI1; external refs. 44–45.

**Current record:**
`SPI1 drives tissue_inflammation`, `perturbation_supported`, core.

**Possible outcomes:**

* **A:** Remove the edge and keep SPI1 as a candidate regulator in context.
* **B:** Retain as supporting `correlates` or `canonical_inferred`.
* **C:** Keep perturbation-supported core despite no SPI1 perturbation, occupancy, or rescue.

**Why it matters:**
Current core scoring rewards an author hypothesis as an experimentally tested regulator.

### 45. `martinez_2024` — Decide whether the speculative AIM2 chain belongs in scored gold

**Priority:** High

**Verify:**
Decide whether cDNA-to-AIM2-to-inflammasome-to-inflammation is core mechanism, supporting hypothesis, or absent.

**Inspect:**
Fig. 1c–d, Fig. 2b–d, and Fig. 5d; text stating AIM2 activation remains unclear.

**Current record:**
Three default-core canonical edges: `cytoplasmic_retroelement_cDNA activates AIM2`, `AIM2 drives inflammasome_activation`, `inflammasome_activation drives tissue_inflammation`.

**Possible outcomes:**

* **A:** Replace the chain with paper-generated `epigenetic_remodeling upregulates AIM2`, supporting or core.
* **B:** Keep the three-edge route as supporting canonical hypothesis, plus the observed AIM2-induction edge.
* **C:** Retain all three as core.

**Why it matters:**
Three headline units currently rest on co-expression and external canonical biology, not AIM2 functional assays.

### 46. `martinez_2024` — Replace or retain the cDNA-to-DNA-damage edge

**Priority:** High

**Verify:**
Verify whether Fig. 4i–j links retroelement cDNA to DNA damage or only links CGAS loss to γH2AX.

**Inspect:**
Fig. 4i–j and external literature on nuclear CGAS/DNA repair.

**Current record:**
`cytoplasmic_retroelement_cDNA induces DNA_damage`, `perturbation_supported`, core.

**Possible outcomes:**

* **A:** Replace with a CGAS-restraint/loss-to-DNA-damage representation; no RT or cDNA perturbation was performed.
* **B:** Retain cDNA-to-damage as supporting canonical inference.
* **C:** Keep the current core edge.

**Why it matters:**
Source choice determines whether agents must infer an untested retrotransposition mechanism.

### 47. `qin_2024` — Narrow the RNA-sensing suppression endpoint

**Priority:** High

**Verify:**
Decide whether ZC3HAV1 suppression should target DDX58 alone or the broader RIG-I/MDA5/MAVS pathway.

**Inspect:**
Fig. 2a–g.

**Current record:**
`ZC3HAV1 suppresses RIG-I/MDA5-MAVS`, `perturbation_supported`, core.

**Possible outcomes:**

* **A:** Retarget to `DDX58`; RIG-I knockdown localizes the result, while MDA5/MAVS were not tested.
* **B:** Keep the pathway endpoint but mark MDA5/MAVS scope as canonical.
* **C:** Split measured RIG-I suppression from optional canonical downstream wiring.

**Why it matters:**
The broad endpoint grants sensor/adaptor recall not generated by this paper.

### 48. `qin_2024` — Choose cytokine output or tissue inflammation as the NF-kB endpoint

**Priority:** High

**Verify:**
Decide whether acute TNF/IL6 transcription, secretion, serum levels, and tissue Il6 constitute `tissue_inflammation`.

**Inspect:**
Figs. 1g–j, 4h–j, and 5c–g.

**Current record:**
`NF-kB drives tissue_inflammation`, `perturbation_supported`, core.

**Possible outcomes:**

* **A:** Retarget to a reviewed `proinflammatory_cytokine_output` programme; no histopathology, infiltrates, or tissue injury was measured.
* **B:** Keep `tissue_inflammation` but define it explicitly as acute systemic/tissue cytokine response.
* **C:** Use individual TNF and IL6 edges, accepting marker-panel expansion.

**Why it matters:**
Endpoint level decides whether cytokine extraction receives credit for a tissue phenotype.

### 49. `qin_2024` — Decide how much of the TLR specificity panel receives recall credit

**Priority:** High

**Verify:**
Decide whether TLR9 alone represents the panel or whether the delivery-dependent TLR3 contrast deserves its own accepted representation.

**Inspect:**
Fig. 2h–m, especially transfected versus extracellular poly(I:C).

**Current record:**
`ZC3HAV1 does_not_drive TLR9`, core; TLR3, TLR4, TLR1/2, and TLR7/8 non-effects remain in context.

**Possible outcomes:**

* **A:** Keep TLR9 as one representative specificity unit.
* **B:** Accept TLR3 and TLR9 as equivalent representations of one TLR-panel unit.
* **C:** Score TLR3 separately because it distinguishes cytosolic RIG-I from extracellular RNA sensing; keep other TLRs in context.

**Why it matters:**
The choice balances useful branch attribution against negative-panel inflation.

### 50. `qin_2024` — Preserve or compress STING1–TBK1 physical recruitment

**Priority:** High

**Verify:**
Decide whether the direct co-immunoprecipitation event should replace or supplement the functional activation edge.

**Inspect:**
Fig. 3j and Fig. 1a–d.

**Current record:**
`STING1 activates TBK1`, `perturbation_supported`, core.

**Possible outcomes:**

* **A:** Replace with `STING1 binds_recruits TBK1`, `direct_measured`; relationship/exact scoring follows the physical experiment.
* **B:** Keep activation and add recruitment as supporting; both mechanisms receive credit.
* **C:** Retain current compression in context.

**Why it matters:**
The paper directly measures recruitment, while generic activation is partly canonical continuity.

### 51. `sprenger_2021` — Add or soften the VDAC pore-to-mtDNA mechanism

**Priority:** High

**Verify:**
Decide whether VBIT-4 effects justify an explicit VDAC pore edge and at what evidence strength.

**Inspect:**
Fig. 2c,e–f; Fig. 7g; cited external VDAC pore reference 3.

**Current record:**
No VDAC endpoint; `mtDNA_release produces cytosolic_dsDNA` is core while metadata and prose claim VDAC-dependent release.

**Possible outcomes:**

* **A:** Add `VDAC_oligomerization forms_pore_for cytoplasmic_mtDNA`, `canonical_inferred`; VBIT-4 supports branch dependence, not physical transit.
* **B:** Replace the generic release-process edge with a VDAC-dependent mtDNA-release edge.
* **C:** Retain current topology and soften VDAC claims in metadata/context.

**Why it matters:**
The scored graph currently omits a claimed central mechanism while prose overstates its paper-specific evidence.

### 52. `sprenger_2021` — Use mitochondrial-specific activation or generic DNA binding for CGAS

**Priority:** High

**Verify:**
Decide whether fractionation/depletion/knockdown evidence supports mtDNA activation of CGAS or physical binding of generic cytosolic dsDNA.

**Inspect:**
Figs. 1d,h, 2b–f, and 4f; Extended Data Figs. 1f and 2b–h.

**Current record:**
`cytosolic_dsDNA binds_recruits CGAS`, `perturbation_supported`, core.

**Possible outcomes:**

* **A:** Change to `cytoplasmic_mtDNA activates CGAS`, `perturbation_supported`.
* **B:** Retain generic `cytosolic_dsDNA` but use `activates`.
* **C:** Keep `binds_recruits` only as `canonical_inferred`; no binding/localization assay was performed.

**Why it matters:**
Endpoint and relationship choices determine whether agents must recover the paper’s mtDNA specificity.

### 53. `sprenger_2021` — Decide whether ASS1/SAMHD1 rescue mechanisms are required

**Priority:** High

**Verify:**
Decide whether the strongest nucleotide-pool rescue experiments should create scored supporting edges or remain evidence for one metabolic edge.

**Inspect:**
Fig. 6a–e and Fig. 7.

**Current record:**
No ASS1 or SAMHD1 edge; both rescues are collapsed into `pyrimidine_metabolism drives type_I_IFN`.

**Possible outcomes:**

* **A:** Add ASS1 and SAMHD1 as separate proximal rescue edges.
* **B:** Put ASS1, SAMHD1, and pyrimidine supplementation in one genuine rescue equivalence unit.
* **C:** Keep all rescue interventions in context for the corrected pyrimidine-imbalance edge.

**Why it matters:**
Current scoring can miss the paper’s reversal evidence entirely or overweight multiple interventions.

### 54. `sprenger_2021` — Add or omit the nuclear-DNA-damage specificity negative

**Priority:** High

**Verify:**
Decide whether absence of DDR signatures and CHK1 phosphorylation is strong enough for a scored negative.

**Inspect:**
Extended Data Fig. 7c–e and Results text on nuclear DNA damage.

**Current record:**
No `nuclear_DNA_damage does_not_drive type_I_IFN` edge, although summary/notes state this exclusion.

**Possible outcomes:**

* **A:** Add a supporting negative; agents must recover the explicit exclusion.
* **B:** Keep it in context because evidence is absence of markers rather than a DDR perturbation.
* **C:** Remove or soften the metadata claim.

**Why it matters:**
The graph and metadata currently impose different specificity expectations.

### 55. `sprenger_2021` — Calibrate the YME1L1-to-SLC25A33 relationship and directness

**Priority:** High

**Verify:**
Decide whether protein-stability evidence establishes direct proteolytic inhibition or broader YME1L1-dependent downregulation.

**Inspect:**
Fig. 3a–b and Extended Data Fig. 4a.

**Current record:**
`YME1L1 inhibits SLC25A33`, `direct_measured`, core.

**Possible outcomes:**

* **A:** Use `YME1L1 downregulates SLC25A33`, `perturbation_supported`.
* **B:** Keep `inhibits` but change evidence to perturbation-supported.
* **C:** Retain direct-measured proteolytic-substrate semantics.

**Why it matters:**
Exact relationship/evidence scoring depends on whether a chase assay proves direct substrate cleavage.

### 56. `tyshkovskiy_2026` — Correct the IGF1 sign or endpoint

**Priority:** High

**Verify:**
Verify whether higher IGF1 associates with shorter maximum lifespan, higher mortality, or neither measured endpoint.

**Inspect:**
Fig. 1h,n and Extended Data Fig. 1o.

**Current record:**
`IGF1 negatively_correlates mortality`, `strong_correlative`, core.

**Possible outcomes:**

* **A:** Change to `IGF1 correlates mortality` if mortality is the intended inverse-lifespan endpoint.
* **B:** Retarget to `maximum_lifespan` with `negatively_correlates`.
* **C:** Remove the edge because IGF1 is not a top mortality-clock or observed-death marker.

**Why it matters:**
Current polarity can reward the opposite biological interpretation.

### 57. `tyshkovskiy_2026` — Replace or retain `type_I_IFN` as the interferon-module endpoint

**Priority:** High

**Verify:**
Decide whether a WGCNA/enrichment module containing IFN-alpha and IFN-gamma responses can be scored as type-I IFN.

**Inspect:**
Fig. 1i; Fig. 3b,e; Fig. 5e; Extended Data Fig. 5d–e.

**Current record:**
`type_I_IFN correlates mortality`, `strong_correlative`, core.

**Possible outcomes:**

* **A:** Replace with a reviewed broad `interferon_signaling` or interferon-response-module endpoint.
* **B:** Keep `type_I_IFN` as supporting approximation.
* **C:** Remove from the NASP graph because no type-I-IFN assay or perturbation exists.

**Why it matters:**
Endpoint scope changes whether broad inflammatory signatures receive sensor-pathway credit.

### 58. `tyshkovskiy_2026` — Retain or remove the senescence-to-mortality association

**Priority:** High

**Verify:**
Verify whether the paper associates an established senescence state with observed mortality rather than only senescence-linked genes and clock behavior.

**Inspect:**
Fig. 2i; replicative-senescence clock analyses; Extended Data Fig. 4d.

**Current record:**
`cellular_senescence correlates mortality`, `strong_correlative`, core.

**Possible outcomes:**

* **A:** Remove to context; no senescence state was modeled against observed deaths.
* **B:** Retarget to mortality-associated clock output and make supporting.
* **C:** Retain broad state association as core.

**Why it matters:**
Current endpoint promotes marker overlap into a core biological state association.

### 59. `tyshkovskiy_2026` — Define which marker evidence qualifies for biological mortality edges

**Priority:** High

**Verify:**
Decide whether marker edges require observed time-to-death/all-cause mortality or may rely on clock coefficients and expected mortality.

**Inspect:**
Fig. 1n; Fig. 5h; Extended Data Figs. 1o and 8k; Fig. 6b for NREP.

**Current record:**
Core CDKN1A, LGALS3, and GPNMB mortality edges mix clock and observed-outcome support; NREP/COL1A1/COL3A1 negative clock markers are omitted.

**Possible outcomes:**

* **A:** Keep only markers validated against observed mortality; cite those panels as decisive and keep clock evidence in context.
* **B:** Admit clock coefficients as mortality edges and add one representative negative marker such as NREP.
* **C:** Separate biological-mortality and clock-marker scoring strata.

**Why it matters:**
One endpoint currently pools observed deaths, expected hazard, and model coefficients.

### 60. `wang_2019` — Correct the dimerization, demethylation, and export topology

**Priority:** High

**Verify:**
Decide whether JMJD6-dependent demethylation causes HNRNPA2B1 export or is a parallel activity gate after dimerization.

**Inspect:**
Figs. 3c–d, 4a–f, and 5c–i.

**Current record:**
`viral_nucleic_acids induces HNRNPA2B1`, then `JMJD6 activates HNRNPA2B1`, with context implying demethylation precedes translocation.

**Possible outcomes:**

* **A:** Keep gene-level nodes but revise context/topology: dimerization gates export and JMJD6 access; demethylation gates IFN activity, not export.
* **B:** Add reviewed process nodes for dimerization, demethylation, and translocation.
* **C:** Retain the current linear model.

**Why it matters:**
Current chain encodes a causal order contradicted by the JMJD6-inhibition localization experiment.

### 61. `wang_2019` — Place STING1 within the initiation complex or keep a terminal necessity edge

**Priority:** High

**Verify:**
Decide whether STING’s physical association and TBK1 placement should be explicit in the core/supporting spine.

**Inspect:**
Supplementary Fig. 8a–i and Discussion model.

**Current record:**
Supporting `STING1 required_for type_I_IFN`; no HNRNPA2B1-to-STING1 or STING1-to-TBK1 edge.

**Possible outcomes:**

* **A:** Replace with `HNRNPA2B1 binds_recruits STING1 / direct_measured` plus `STING1 activates TBK1 / canonical_inferred`.
* **B:** Keep the terminal requirement edge because direct STING-dependent TBK1 activation was not isolated.
* **C:** Promote STING dependency to core while retaining both topology and outcome summary.

**Why it matters:**
Endpoint placement changes whether agents must recover STING as an intermediate or only as output necessity.

### 62. `wang_2019` — Choose pathway-level or cytokine-level specificity negatives

**Priority:** High

**Verify:**
Decide whether NF-kB and RNA-virus pathways are more reusable negative endpoints than IL6/TNF markers.

**Inspect:**
Fig. 2b; Supplementary Figs. 2–4.

**Current record:**
Equivalent `HNRNPA2B1 does_not_drive IL6` and `... TNF`; no NF-kB or RIG-I/MDA5/MAVS negative.

**Possible outcomes:**

* **A:** Replace marker negatives with `HNRNPA2B1 does_not_drive NF-kB` and add an RNA-sensing-pathway negative.
* **B:** Keep one cytokine equivalence unit and place RNA-virus specificity in context.
* **C:** Score both pathway negatives as separate units.

**Why it matters:**
Negative endpoint choice determines whether agents receive credit for branch attribution or marker recall.

### 63. `wang_2019` — Score FTO and METTL3 symmetrically or remove the broad FTO shortcut

**Priority:** High

**Verify:**
Decide whether writer and eraser interventions deserve parallel scored edges and whether either should point directly to type-I IFN.

**Inspect:**
Fig. 7d–e and Supplementary Fig. 12c–g.

**Current record:**
Supporting `FTO suppresses type_I_IFN`; METTL3 appears only in context.

**Possible outcomes:**

* **A:** Add `METTL3 required_for type_I_IFN` as a parallel supporting edge.
* **B:** Retarget both regulators to a reviewed m6A-modification mechanism.
* **C:** Remove FTO as a distal shortcut and keep both regulators in amplification context.

**Why it matters:**
Current gold scores one side of a reciprocal modification mechanism and hides the other.

### 64. `wang_2019` — Narrow the viral-ligand endpoint to DNA or retain a generic sensor claim

**Priority:** Medium

**Verify:**
Decide whether HNRNPA2B1 binding should target viral DNA rather than all viral nucleic acids.

**Inspect:**
Fig. 1a–c; Supplementary Fig. 1c–d; RNA-virus specificity panels in Supplementary Figs. 2–4.

**Current record:**
`HNRNPA2B1 binds_recruits viral_nucleic_acids`, `direct_measured`, core.

**Possible outcomes:**

* **A:** Retarget to a reviewed `viral_DNA` endpoint; RNA-virus non-requirement stays explicit.
* **B:** Keep generic `viral_nucleic_acids` with DNA scope stated in context.

**Why it matters:**
The broad endpoint can give an agent credit for an RNA-sensing role the paper does not demonstrate.

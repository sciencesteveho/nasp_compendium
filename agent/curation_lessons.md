# NASP Curation Lessons

Durable curation lessons distilled from calibration and held-out testing. This
file is agent-facing guidance for biological judgment; it is not a schema,
validator, or ontology. `agent/conventions.md` remains the source of normative
curation rules, and `agent/vocabulary.yaml` remains the controlled vocabulary.

Use this file before drafting edges and again before freezing a draft. The goal
is to prevent recurring curation failures without hard-coding paper-specific
answers.

## Current calibration status

The current lessons were locked after:

- four dev calibration papers: `mao_2024`, `lian_2018`, `martinez_2024`,
  `tyshkovskiy_2026`
- one held-out paper: `qin_2024`

The effective change was not new schema. The useful improvement came from
better final-pass curation judgment:

- recover complete biological branch arms
- prune broad/non-reusable extras
- distinguish unisolated canonical wiring from measured branch continuity
- keep reagent, agonist, virus, dose, and assay-condition endpoints in context
- preserve graph-useful negative specificity findings

Do not continue tuning against these five papers as if they were fresh held-out
data. Use them as a frozen benchmark and expand to new gold standards.

## Pre-freeze operating checklist

Before freezing a draft, check the following in order:

1. What is the main causal spine?
2. What distinct branch arms does the paper support?
3. Are any branch arms represented only by broad labels rather than reusable
   edges?
4. Are there negative or specificity findings that block plausible false edges?
5. Are there supported intermediates that a shortcut edge would erase?
6. Are broad phenotype/output claims routed through nearer reusable
   intermediates?
7. Are direct binding/product/localization edges separated from downstream
   functional activation edges?
8. Are evidence strengths assigned edge-by-edge rather than copied from the
   assay type?
9. Are reagents, drugs, viruses, ligands, cytokine panels, and figure labels kept
   in context unless they define reusable graph nodes?
10. Are resource/atlas associations endpoint-specific and directionally audited?
11. Would a domain expert recognize the paper's central mechanism from the edge
    graph alone?

## 1. Recover branch arms, not just the main spine

Early drafts tend to recover the central mechanistic spine and miss graph-useful
parallel branches. A branch is not complete merely because one edge of that
`branch_type` exists.

Decision rule:
- After drafting the spine, run a dedicated branch pass.
- Search separately for sensor branches, inflammatory-output branches,
  organismal-output branches, cohort/resource associations, state-reversal or
  feedback branches, and negative-specificity controls.
- If a supported branch is not emitted, explain why it remains context-only.

Examples from calibration:
- Lian: an IRF3/type-I-IFN arm did not substitute for the NF-kB arm.
- Martinez: an AIM2/inflammasome route and a SPI1/inflammation route were
  distinct parallel branches.
- Mao: upstream induction, feedback, negative specificity, and aging-bridge
  edges were all graph-useful despite the long main spine.

## 2. Do not erase supported intermediates

Do not collapse a supported path into a headline shortcut. Supported
intermediates keep the graph mechanistic and composable.

Prefer:
- upstream perturbation or state
- molecular intermediate
- sensor or adaptor
- signaling pathway
- program-level output
- phenotype only when functionally or centrally supported

Avoid:
- broad shortcuts such as `STING1 -> cognitive_decline` when intermediates are
  supported
- genotype-baked or figure-label nodes such as `cGAS_KO_inflammation`
- marker-only edges unless the marker is mechanistically reused
- direct edges across cGAMP, cytoplasmic nucleic-acid intermediates, MAVS,
  TBK1/IRF3, JAK-STAT, inflammasome nodes, or other measured intermediates

Shortcut warnings from the validator require classification:
- real catch
- accepted false positive
- intentional documented choice
- needs human review

Do not silently remove or keep a flagged shortcut without recording the reason.

## 3. Recover graph-useful negative specificity findings

Negative findings are graph-useful when they prevent a plausible false
mechanism.

Emit `does_not_drive` or `does_not_correlate` when the paper explicitly rules
out a mechanism that an agent or reader might otherwise infer.

Useful negative findings include:
- pathway-localization controls
- receptor/adaptor specificity controls
- paralog specificity controls
- ligand-class specificity controls
- upstream-versus-downstream placement controls
- sign-flipped DNA-versus-RNA sensing effects

Keep minor redundant negative panels in context when one representative edge
captures the reusable specificity result.

Examples:
- A cGAMP bypass showing a regulator acts downstream of cGAMP can block a false
  CGAS-proximal edge.
- A JAK-STAT non-effect can show a regulator acts in the sensing arm rather than
  IFN-receptor signaling.
- Multiple TLR negative controls may be compressed into one representative
  nucleic-acid TLR edge, with the rest in context, unless the paper makes each
  TLR independently graph-relevant.

## 4. Search for nearest intermediates before adjudicating broad claims away

A broad output claim may be too coarse as written, but it can still imply a
narrower graph-useful edge.

Decision rule:
- Before marking a broad graph-candidate claim `context_only`, search for the
  nearest supported intermediate.
- Prefer that intermediate edge over a source-to-output shortcut.
- Keep the broad phenotype in context unless it is itself a reusable endpoint.

Examples:
- Broad inflammatory output should trigger a search for NF-kB, inflammasome,
  cytokine-program, or tissue-inflammation intermediates.
- Broad aging or inflammaging output should trigger a search for cohort,
  organismal, or tissue-state bridge edges.
- Broad antiviral or infection endpoints usually remain context unless the graph
  has a reusable node for the mechanism.

## 5. Final pruning: keep reusable biology, remove broad extras

Recover biology first, then prune for graph value. The final pass should reduce
broad extras without deleting tested upstream, feedback, or bridge edges.

Keep an edge if it is:
- a reusable mechanism edge
- a directly measured upstream induction edge
- a perturbation-tested feedback/state-reversal edge
- a central aging/inflammaging bridge edge
- a paper-defining resource or marker endpoint
- a negative-specificity edge that blocks a false mechanism

Move to context if it is:
- a redundant net-effect edge already explained by preserved intermediates
- a broad phenotype with no reusable graph endpoint
- a cytokine/ISG/readout panel item
- a reagent, agonist, drug, virus, dose, model condition, or clock-validation
  condition
- a generic stressor association not elevated as a central reusable endpoint

## 6. Evidence strength is edge-specific

Evidence strength describes support for the specific edge, not the paper's
overall assay type.

Use `direct_measured` when the edge-level object is directly measured:
- physical binding or recruitment
- molecular product abundance
- localization or trafficking
- directly observed pore/release product
- directly measured state association when the edge itself is observational

Use `perturbation_supported` when:
- an upstream genetic, molecular, pharmacological, or state perturbation changes
  a directly measured downstream branch readout
- the paper uses that measured readout to place the branch
- the edge is part of measured branch continuity rather than purely generic
  canonical wiring

Use `canonical_inferred` when:
- the paper relies on accepted pathway wiring
- the exact receptor/adaptor/ligand step is not isolated
- a bypass/localization experiment invokes a canonical edge without testing the
  edge itself

Use `strong_correlative` when:
- the support is cohort, atlas, cross-sectional tissue, organismal association,
  module association, or resource-marker association
- an aging/inflammaging bridge is central but not directly perturbed

## 7. Evidence-boundary rule: canonical wiring versus branch continuity

This rule was the most effective calibration improvement.

Do not propagate `perturbation_supported` through unisolated receptor/adaptor
wiring merely because the whole branch changes.

Keep `canonical_inferred` for unisolated wiring such as:
- ligand-to-receptor or ligand-to-adaptor wiring used as pathway anchor
- receptor-to-adaptor steps not specifically isolated
- accepted sensor/adaptor wiring invoked from the literature
- cGAMP-to-STING when cGAMP is used as a bypass/localization stimulus rather
  than to test ligand-receptor activation itself
- cGAS-to-cGAMP when cGAS is invoked but not perturbed or isolated

Use `perturbation_supported` for downstream branch-continuity edges when:
1. an upstream perturbation changes the branch,
2. the downstream readout is directly measured,
3. the authors use the readout to place the branch, and
4. the edge is not merely a generic receptor/adaptor anchor.

Examples:
- Keep RIG-I/DDX58-to-MAVS and MDA5/IFIH1-to-MAVS `canonical_inferred` if
  those specific receptor-to-MAVS edges were not isolated.
- Use `perturbation_supported` for MAVS-to-TBK1, TBK1-to-IRF3, or
  IRF3-to-type-I-IFN when phospho-TBK1, phospho-IRF3, IFNB/IFN-beta, ISGs, or
  equivalent branch readouts change with the upstream perturbation.
- Use `perturbation_supported` for STING-to-TBK1 or STING-to-NF-kB when the
  paper places the branch through STING and measures phospho-TBK1,
  phospho-IkB-alpha, NF-kB activity, or inflammatory output under the relevant
  perturbation.
- Keep cGAMP-to-STING `canonical_inferred` when cGAMP is used to bypass cGAS or
  localize the regulator downstream of cGAMP.

## 8. Relationship verbs: normalize, but do not erase meaning

Relationship type and evidence strength are independent.

Use:
- `activates` for signaling, sensor, adaptor, kinase, transcription-factor, or
  pathway activation
- `induces` for triggering a biological state, transition, program, or output
- `drives` for ongoing causal control of a process, program, or phenotype
- `upregulates` / `downregulates` for abundance, expression, accessibility, or
  activity changes
- `produces` for generation of a molecular intermediate
- `binds_recruits` for direct physical association, recruitment, or
  localization when measured
- `required_for` when loss of the source prevents the target process but the
  mechanism is broader than simple activation
- `suppresses` / `inhibits` for negative functional regulation
- `contains` only for program membership, not causal regulation

Known human-judgment zones:
- `epigenetic_remodeling -> retrotransposon_derepression` may be `induces` when
  framed as a trigger-to-program transition, or `drives` when framed as ongoing
  chromatin-state control. Adjudicate validator warnings rather than blindly
  normalizing.
- `AIM2 -> inflammasome_activation` relationship choice can be
  convention-sensitive. Prefer the repo's normalized relation for the node pair
  unless the paper gives a clear reason to deviate.
- Resource-marker directionality depends on the encoded endpoint. Audit the sign
  relative to mortality, lifespan, expected mortality, age, or maximum lifespan.

## 9. Repressor-loss and inhibitory logic

Do not rely on readers to mentally compose two inhibitory edges.

Allowed representation:
- `cellular_senescence downregulates ADAR`
- `ADAR suppresses cytosolic_RNA_sensing`
- `cellular_senescence induces cytosolic_RNA_sensing` only when supported as a
  summarized consequence, with context explicitly saying it is via ADAR loss
  and/or dsRNA accumulation

Same for mitochondrial RNA or DNA release mechanisms:
- preserve the repressor or containment edge when tested
- allow a summarized consequence edge only if it does not erase the underlying
  mechanism

## 10. Pore-mediated release

Use `forms_pore_for`, not a bare `releases`, for BAX/BAK and VDAC biology.

Preferred:
- `VDAC1 forms_pore_for cytoplasmic_mtDNA`
- `VDAC3 forms_pore_for cytoplasmic_mtDNA`
- `BAX/BAK_pore forms_pore_for cytoplasmic_mt_dsRNA`
- `BAX/BAK_pore forms_pore_for cytoplasmic_mtDNA`

Avoid splitting BAX and BAK into independent mechanistic branches unless the
paper tests them separately.

## 11. Regulators, transcription factors, markers, and programs

Regulators can be graph nodes; marker panels usually remain context.

Promote a transcription factor or regulator to a node when the paper supports:
1. motif/regulatory-region evidence or localization,
2. concordant expression/activity,
3. an author-invoked mediator role, and
4. downstream inflammatory, fibrotic, or tissue-state program support.

When both are supported, preserve both:
- upstream state/regulator induction edge
- regulator-to-output program edge

Example pattern:
- `epigenetic_remodeling upregulates transcription_factor`
- `transcription_factor drives tissue_inflammation`

For SASP and cytokine programs:
- Use `SASP contains IL6` only as a program-membership edge.
- Use `MAVS drives SASP`, `type_I_IFN drives SASP`, or `NF-kB drives SASP` for
  mechanism-level inflammatory output.
- Do not create long lists of `upregulates` edges to individual cytokines unless
  a cytokine is mechanistically central.

## 12. Prefer specific ligand/sensor edges over generic sensing nodes

Generic process nodes can hide reusable biology.

Decision rule:
- If the paper directly implicates a ligand/intermediate and a sensor, curate
  that specific ligand-to-sensor edge.
- Do not insert a generic sensing-process node between them.
- Use broad sensing nodes only when the specific sensor is not identified or
  the process node is itself the reusable mechanism.

Examples:
- Prefer cytoplasmic retroelement RNA to DDX58/IFIH1 when the paper implicates
  RIG-I/MDA5.
- Prefer cytoplasmic retroelement cDNA to AIM2 or CGAS when the paper implicates
  the DNA sensor.
- Keep `cytosolic_RNA_sensing` for genuinely sensor-agnostic process claims.

## 13. Reagents, triggers, viruses, agonists, and assays

Experimental triggers usually stay in context.

Keep in context unless explicitly accepted as reusable endpoints:
- viruses
- synthetic DNA/RNA ligands
- STING agonists
- inhibitors and inactive analogs
- drugs and doses
- transfection conditions
- stimulation time points
- assay readouts
- model tissues and infection endpoints

Accepted exceptions:
- `cGAMP` is a valid endpoint when it is the biological second messenger under
  discussion.
- Some trigger endpoints such as `replicative_exhaustion` or `dsDNA90` may be
  accepted when the convention/vocabulary explicitly allows them.
- If unsure, use `proposed_terms:` rather than silently adding a node.

## 14. Vocabulary and naming discipline

Prefer existing canonical vocabulary over paper-specific node names.

Use:
- `cytoplasmic_chromatin_fragments`, not `CCF`
- `retrotransposon_derepression`
- `cytoplasmic_retroelement_cDNA`
- `cytoplasmic_retroelement_RNA`
- `epigenetic_remodeling`
- `heterochromatin_organization`
- generic tissue outcomes such as `tissue_inflammation`, `fibrosis`,
  `accelerated_aging`, `mortality`, and `inflammaging`

Avoid:
- paper-specific construct names
- genotype-baked nodes
- locus-suffixed L1/ERV nodes unless specifically needed
- figure labels as endpoints
- undeclared abbreviations when an HGNC or canonical node exists

Proposed nodes should be minimized and justified by graph composition need.

## 15. Resource, atlas, cohort, and biomarker papers

Atlas/resource papers require endpoint selection, not mechanism inflation.

Decision rule:
- Use correlative edges for resource/atlas claims.
- Prefer endpoints the paper elevates as central, cross-dataset, validated, or
  reusable.
- Do not convert correlative signatures into causal mechanisms.
- Keep damage/stressor/clock-validation conditions in context unless they are
  central reusable mortality markers, mortality modules, or endpoint-defining
  states.
- Avoid broad generic edges such as `DNA_damage correlates mortality` merely
  because a stressor changes a clock readout.

Endpoint-direction sign audit:
- For every marker-to-mortality or marker-to-lifespan edge, write one line in
  context explaining the endpoint and sign.
- Lifespan-positive or longevity-associated markers usually map to
  `negatively_correlates mortality`.
- Markers negatively associated with maximum lifespan may map to
  `correlates mortality`, depending on the paper's endpoint model.
- If the sign remains ambiguous, record the ambiguity in context and flag for
  human review.

## 16. Claims, matrices, and adjudications

A claim-edge matrix is most useful when a broad claim supports several edges.

Use `claim_edge_matrix:` when:
- one claim supports more than three edges
- a broad claim is reused across several branches
- exact claim-to-edge support may be unclear during review

Every emitted edge should have non-empty `support_claims` when the draft uses a
claims block.

If a graph-candidate claim remains context-only or insufficient, it needs a
specific non-emission rationale. For high-priority branches, search for a
nearest intermediate before adjudicating the claim away.

Adjudications are for deliberate choices, not decoration. Use them when:
- keeping a validator warning
- rejecting an apparent shortcut warning
- preserving a human-judgment verb choice
- choosing one representative specificity edge from a redundant panel
- keeping a graph-candidate claim out of the graph

## 17. Validation success is not biological success

A draft can pass validation and still miss the central biology.

Treat validation as a structural gate only:
- YAML parses
- required fields are present
- node naming is mostly controlled
- support links exist
- obvious topology warnings are surfaced

Then do a biology-only pass:
- Does the graph capture the paper's central mechanism?
- Are all distinct branch arms represented?
- Are negative controls represented when graph-useful?
- Did final pruning remove only non-reusable extras, not tested feedback or
  bridge biology?
- Would a domain expert recognize what the paper showed?

## 18. Calibration differences are lessons, not automatic gold obedience

Gold files are useful for measuring consistency, but not every mismatch should
become a new rule.

Classify mismatches as:
- true missed biology
- relationship-verb drift
- evidence-strength drift
- defensible conservative omission
- draft overcall
- suspected gold defect
- vocabulary/naming mismatch
- density/compression mismatch

Only update lessons or conventions for repeated, generalizable failures.
Do not tune the lessons to memorize dev-paper watchpoints.

## 19. What not to tune further

Do not add new schema fields for:
- branch inventory
- graph roles
- mechanism-only scoring
- motif libraries
- paper-specific watchpoint lists

These increased complexity without durable benefit. The current stable layer is:
claims, optional claim-edge matrix, existing adjudications, validator/review
packet, and this lessons file.

## 20. Practical calibration policy

Use the current five papers as follows:

- Mao, Lian, Martinez, and Tyshkovskiy are dev-calibration papers.
- Qin is the first held-out success report.
- Do not keep tuning against these five unless the goal is reproducibility, not
  improvement.
- Build new gold standards across new topology classes: endosomal TLR sensing,
  DDX/RLR or DDX41 sensing, AIM2 inflammasome, and IFI16 or another DNA
  co-sensor.
- Once the agent handles a broader gold set well, stop tuning and begin adding
  new papers to the compendium.

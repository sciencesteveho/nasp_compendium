# NASP Curation Lessons

Durable curation lessons distilled from calibration and audit rounds. This is
not the rules file; `agent/conventions.md` remains the source of curation rules,
and `agent/vocabulary.yaml` is the machine-readable controlled vocabulary. Read
this file before drafting edges to see what this workflow has historically
gotten wrong or needed human judgment to resolve.

Provenance for each lesson is the calibration round it came from; see the
calibration history table at the end. The underlying audit reports have been
retired now that their conclusions live here.

## Failure patterns

**Main-spine bias.** Early calibrations recovered the central mechanistic spine
but missed graph-useful branch edges. After drafting the spine, run a dedicated
branch pass and scan separately for: in vivo outcome branches,
cohort/correlation branches, cell-state-transition branches, negative
specificity controls, mechanistically reused cytokines, and net-effect edges
that are explicitly perturbation-supported. The first Dou 2017 pass, for
example, missed senescence-trigger edges, IFN suppression, in vivo
immunosurveillance, cancer/senescence-evasion retention, cohort associations,
and the IFI16/MAVS negative findings; all are now recoverable with the branch
pass.

**Shortcut temptation.** There is a standing tendency to collapse supported
chains into shortcut edges (CCF directly driving SASP, DNA damage directly
driving tissue inflammation). Do not write a shortcut edge across an
intermediate the paper actually supports. See `agent/conventions.md`, "No
shortcut edges across supported intermediates."

**Supported intermediates must survive across papers.** Calibration against the
four gold standards showed repeated shortcut drift over canonical signaling
intermediates: cGAMP, JAK-STAT, VDAC oligomerization, cytosolic_RNA_sensing, and
TBK1/IRF3. These are not optional decoration; they keep the graph mechanistic
and prevent headline-only curation. Preserve them unless the paper genuinely
supports only a net effect.

**Context and support under-specification.** A draft can recover the correct
edge set while being weaker than a gold file on dose, timing, cell line, tissue,
perturbation, and figure-panel support. Workflow: draft concise edges first,
then enrich `context` and `support` from the PDF and curated examples before
compendium insertion.

**Validator warnings are review gates, not cleanup noise.** Warnings have
surfaced real metadata drift and undeclared endpoints. Treat a warning as a
prompt for an audit or backfill proposal unless the task explicitly authorizes a
fix. With the tiered vocabulary gate, a proposed-term warning is the system
working as designed, not a defect to silence.

**Regulators can be mechanism nodes; markers usually cannot.** Promote a named
regulator to a node only when motif or regulatory-region evidence, concordant
expression/activity, and an author-invoked mediator role are all present (the
SPI1 promotion in Martinez 2024 is the worked example). Demote multi-gene
cytokine or qPCR/ELISA panel readouts to program-edge context unless an
individual cytokine is mechanistically reused as another edge endpoint.

**Gene-specific evidence beats process paraphrase.** If a paper directly
perturbs or measures a gene-level regulator, use the gene endpoint rather than a
broad process node, unless the process is the actual reusable mechanism.

**Evidence-strength honesty needs a final pass.** Drafts sometimes upgraded
co-occurrence to perturbation support, or downgraded a directly measured
activation or product to canonical inference. Each edge needs an explicit check
against the exact experiment supporting that specific relationship.

**Evidence strength is edge-specific, not assay-specific.** A single directly
observed readout can support different strengths on different edges. Martinez
2024: a directly observed readout after CGAS KO/knockdown is still
`perturbation_supported` for an inferred upstream edge (retrotransposon
derepression producing cytoplasmic cDNA, SPI1 mediating the opened inflammatory
program, cytoplasmic cDNA inducing DNA damage), while histology of the exact
tissue outcome is `direct_measured` for `tissue_inflammation -> fibrosis`.

**Duplicate edges hide evidence instead of adding mechanism.** When the same
source/relationship/target recurs across contexts, merge `support` and `context`
into one edge rather than repeating it across chains.

## Vocabulary clarifications

The controlled vocabulary now uses a tiered gate (`agent/vocabulary.yaml`, with
`canonical` and `drift` sections; see `agent/specs/tiered_vocab_spec.md`). Most
of the clarifications below are encoded there as canonical terms or drift
replacements; they are kept here for the reasoning.

**CCF naming.** Use `cytoplasmic_chromatin_fragments` for chromatin-derived CCF
biology; `CCF` belongs only in prose. `CCF_formation` is convention drift, not a
term to revive; it is in the drift table with `cytoplasmic_chromatin_fragments`
as the replacement.

**Retroelement cDNA naming.** Use `cytoplasmic_retroelement_cDNA` for
L1/retroelement-derived cytoplasmic cDNA or RNA-DNA hybrid intermediates
generated by reverse transcription. DeCecco 2019 was migrated from the CCF node
to this node after curator authorization.

**L1 drift terms.** Do not use `LINE1_transcription`, `cytoplasmic_L1_cDNA`,
`cytosolic_L1_cDNA_accumulation`, or `L1_de-repression` as nodes. Use
`retrotransposon_derepression` and `cytoplasmic_retroelement_cDNA` so De Cecco
2019 and Martinez 2024 compose on the same L1 biology.

**Chromatin-state naming.** Use `epigenetic_remodeling` for accessibility gain
and transposon methylation loss, with locus identity in context. Reserve
`heterochromatin_organization` for the intact, factor-maintained repressive
compartment, rather than histone-mark, locus-suffixed, or genotype-baked nodes.
These are opposite poles and both can be needed in the same paper (CGAS
suppresses `epigenetic_remodeling` and CGAS supports
`heterochromatin_organization`).

**Small molecules and experimental triggers.** `cGAMP` is a valid endpoint, and
`replicative_exhaustion` / `dsDNA90` are valid trigger endpoints, when they are
the biological or experimental entity under test. If unsure whether a new small
molecule or trigger should be a node, file a proposed-term record rather than
silently adding a convention.

**Tissue-agnostic outcomes.** Keep outcomes generic (`tumorigenesis`,
`tissue_inflammation`, `fibrosis`, `apoptosis`); tissue labels belong in
context. Now fully captured as a rule in `agent/conventions.md`, "What is NOT a
node."

**Vocabulary additions go through the tier gate.** `agent/vocabulary.yaml` is
the machine-readable source of truth and is human-owned. The agent may use a new
term in a draft only after a canonicalization search comes up empty and only if
it files an inline `proposed_terms` record in the same draft; a human then
promotes, merges, or rejects it. The agent never writes to
`agent/vocabulary.yaml`.

## Convention edge cases

**SASP membership versus regulation.** `SASP contains X` records measured program
membership; `STING1 upregulates X` or `JAK-STAT upregulates X` records
perturbation-supported causal regulation. These can coexist when both meanings
are graph-useful, but `contains` must not replace a regulatory edge.

**Paralog negative controls.** Multiple negative paralog results can be explicit
`does_not_correlate` or `does_not_drive` edges when they disambiguate
specificity and are useful for graph queries; minor or redundant paralogs stay
in context. Flag the choice for human review.

**Drug specificity controls.** Drugs and inactive analogs usually stay in
`context` when they test a reusable biological mechanism. For DeCecco-style 3TC
and K-9 experiments, the reusable graph node is the mechanism
(`retrotransposon_derepression` or `cytoplasmic_retroelement_cDNA`), not the
reagent.

**Functional activation without direct binding.** When a paper shows pathway
necessity but not physical colocalization or binding, prefer a functional
relation such as `activates` with `perturbation_supported` over `binds_recruits`.
DeCecco's L1 cDNA-to-CGAS edge uses this resolution.

**Skip-edge warnings need classification.** The validator can flag a direct edge
that coexists with a longer same-paper path, but some are legitimate
model-specific or specificity-control branches. Classify each surviving warning
in the per-paper notes as accepted false positive, intentional documented
choice, or real catch, rather than silently removing the edge.

**Structured graph diffs complement rendered PNGs.** Use `compendium diff` for
fast review of paper/entity/edge changes before relying on a rendered graph.

## Mechanistic edge standard

Curate the causal spine first. Add measured marker genes only when they help
interpret the spine.

Prefer:
- upstream perturbation or state
- molecular intermediate
- sensor or adaptor
- signaling pathway
- program-level output
- phenotype, only when supported by functional assays

Avoid:
- broad shortcuts such as `STING1 -> cognitive_decline` when intermediate
  mechanisms are known
- figure-label entities such as `cGAS KO inflammation`
- marker-only edges such as `MAVS -> CCL2` unless the paper directly shows
  MAVS-specific regulation of that molecule and the edge adds mechanistic value
- `does_not_drive` edges in the rendered main graph unless the negative result
  is a true specificity-control branch

## Repressor-loss logic

Do not rely on users to mentally compose two inhibitory edges.

Allowed representation:
- `cellular_senescence downregulates ADAR`
- `ADAR suppresses cytosolic_RNA_sensing`
- `cellular_senescence induces cytosolic_RNA_sensing` only when supported as a
  summarized consequence, with context explicitly saying it is via ADAR loss
  and/or dsRNA accumulation

Same for PNPT1:
- `cellular_senescence downregulates PNPT1`
- `PNPT1 suppresses cytoplasmic_mt_dsRNA`
- `cellular_senescence induces cytoplasmic_mt_dsRNA` when supported by cytosolic
  fractionation / J2 evidence

The rendered graph should show inhibitory edges with tee arrowheads. For
readability, a summarized consequence edge is allowed if it is not used to erase
the underlying mechanism.

## Pore-mediated release

Use `forms_pore_for`, not a bare `releases`, for BAX/BAK and VDAC biology.

Preferred:
- `VDAC1 forms_pore_for cytoplasmic_mtDNA`
- `VDAC3 forms_pore_for cytoplasmic_mtDNA`
- `BAX/BAK_pore forms_pore_for cytoplasmic_mt_dsRNA`
- `BAX/BAK_pore forms_pore_for cytoplasmic_mtDNA`

Avoid splitting BAX and BAK into independent mechanistic branches unless the
paper tests them separately.

## Marker genes and SASP

Use `SASP contains IL6` only as a program-membership edge. Use `MAVS drives
SASP`, `type_I_IFN drives SASP`, or `NF-kB drives SASP` for mechanism-level
inflammatory output. Do not create long lists of `upregulates` edges to
individual cytokines unless those cytokines are mechanistically central.

## Open metadata items

Flagged in prior audits; verify against the current files before the next render
and resolve as metadata-only backfills:

- Dou 2017 paper block may still declare `CCF_formation` under `mechanisms`.
  Revise to `cytoplasmic_chromatin_fragments`; `CCF_formation` is a drift term
  and must not be re-added to the canonical vocabulary.
- DeCecco 2019 has an undeclared `RBL1` edge endpoint. Add `RBL1` to the paper
  `genes` list if the edge remains.

## Calibration history

| Paper / round | Date | Headline lesson |
|---|---:|---|
| Dou 2017 (first pass) | 2026-05-27 | Recover graph-useful branches, negative findings, and supported intermediates; CCF naming drift needed durable conventions. |
| Dou 2017 (post-patch) | 2026-05-27 | Prompt/convention patches addressed main-spine bias, shortcut risk, negative findings, and style-example use. |
| DeCecco 2019 | 2026-05-27 | Generalized beyond Dou; exposed L1 cDNA naming, SASP membership-vs-regulation edge style, and paralog-control judgments. |
| DeCecco 2019 (L1 migration) | 2026-05-27 | Migrated L1-derived cytoplasmic DNA from CCF to `cytoplasmic_retroelement_cDNA` and used functional `activates` for CGAS. |
| Vocabulary infrastructure | 2026-05-27 | Vocabulary drift should be machine-detected and reviewed before terms enter the vocabulary. |
| Skip-edge detection | 2026-05-27 | Skip-edge detection is a useful warning, but model-specific branches can be false positives requiring audit classification. |
| Four gold standards | 2026-05-28 | Hardened anti-shortcut, branch-audit, marker/regulator, evidence-honesty, node-canonicalization, and duplicate-edge lessons before Martinez held-out testing. |
| Martinez 2024 (held-out) | 2026-05-29 | Held-out test of post-audit instructions for L1/chromatin naming, SPI1 promotion, marker demotion, evidence honesty, and phenotype routing. |
| Tiered vocabulary gate | 2026-05-29 | Binary gate left good new nodes in limbo; tiered `canonical`/`proposed`/`drift` gate lets the agent advance a draft while flagging terms for human promotion. |

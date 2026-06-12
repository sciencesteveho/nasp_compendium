# NASP Curation Lessons

This file captures durable curation lessons from calibration and audit reports.
It is not the rules file; `docs/compendium_conventions.md` remains the source of
curation rules. Read this file before drafting edges to see what this workflow
has historically gotten wrong or needed human judgment to resolve.

## Failure patterns

**Main-spine bias.** The first Dou 2017 calibration missed graph-useful branch
edges such as senescence triggers, IFN suppression, in vivo immunosurveillance,
cancer/senescence-evasion retention, cohort associations, and IFI16/MAVS
negative findings. Resolution: prompts now explicitly ask for graph-useful
branch edges, not only the main spine. Source: `dou_2017_calibration_audit.md`
and `dou_2017_post_patch_check.md` for Dou 2017.

**Shortcut temptation.** Dou 2017 exposed a tendency to collapse supported
chains into shortcut edges such as CCF directly driving SASP or DNA damage
directly driving tissue inflammation. Resolution: see
`docs/compendium_conventions.md`, section "No shortcut edges across supported
intermediates." Source: `dou_2017_calibration_audit.md` for Dou 2017.

**Context and support under-specification.** Drafts can recover the correct
edge set while being weaker than gold files on dose, timing, cell line, tissue,
perturbation, and figure-panel support. Resolution: draft concise edges first,
then enrich context/support from the PDF and curated examples before final
compendium insertion. Source: `dou_2017_calibration_audit.md` and
`dececco_2019_calibration_audit.md`.

**Cytosolic DNA overgeneralization.** DeCecco 2019 showed that the agent may use
`cytoplasmic_chromatin_fragments` for any cytosolic DNA species. Check whether
the DNA is chromatin/nuclear-fragment-derived CCF or reverse-transcribed
retroelement cDNA. Resolution: use `cytoplasmic_retroelement_cDNA` for
L1/retroelement cDNA. Source: `dececco_2019_calibration_audit.md`,
`proposed_post_dececco_backfill.md`, and `dececco_2019_l1_cdna_migration.md`.

**Validator warnings are review gates, not cleanup noise.** Dou and DeCecco
warnings identified real metadata drift and undeclared endpoints. Treat warnings
as prompts for audit/backfill proposals unless the task explicitly authorizes a
fix. Source: `vocabulary_extraction.md`,
`proposed_post_dececco_backfill.md`, and `skip_edge_detection.md`.

**Supported intermediates must survive across papers.** Calibration against the
four gold standards showed repeated shortcut drift over cGAMP, JAK-STAT, VDAC,
cytosolic_RNA_sensing, TBK1/IRF3, and branch-specific intermediates; preserve
these chains unless the paper only supports a net effect. Source:
`reports/calibration_audit_2026-05-28.md`.

**Branch auditing is mandatory.** In vivo outcome branches, cohort/correlation
branches, cell-state branches, negative specificity controls, and net-effect
perturbation branches were often thinner than gold even when the main spine was
recovered. Source: `reports/calibration_audit_2026-05-28.md`.

**Regulators can be mechanism nodes, markers usually cannot.** A named
regulator with motif evidence, concordant expression, and an author-invoked
mediator role should be promoted to a node, while multi-gene cytokine panels
usually remain program readouts in context. Source:
`reports/calibration_audit_2026-05-28.md`.

**Evidence-strength honesty needs a final pass.** Drafts sometimes upgraded
co-occurrence to perturbation support or downgraded directly measured activation
to canonical inference; each edge needs an explicit check against the exact
experiment supporting that relationship. Source:
`reports/calibration_audit_2026-05-28.md`.

**Evidence strength is edge-specific, not assay-specific.** Martinez 2024 held-out
testing showed that a directly observed readout after CGAS KO/knockdown can still
be `perturbation_supported` for an inferred upstream edge (for example
retrotransposon_derepression producing cytoplasmic cDNA, SPI1 mediating the
opened inflammatory program, or cytoplasmic cDNA inducing DNA damage), while
histology of the exact tissue outcome can be `direct_measured` for
`tissue_inflammation -> fibrosis`. Source:
`reports/post_patch_check_martinez_2026-05-29.md`.

**Canonical signaling intermediates are not optional decoration.** cGAMP,
JAK-STAT, VDAC oligomerization, cytosolic_RNA_sensing, TBK1/IRF3, and similar
supported intermediates keep the graph mechanistic and prevent headline-only
curation. Source: `reports/calibration_audit_2026-05-28.md`.

**Program branches need their own audit pass.** After the main spine, scan
separately for in vivo outcome branches, cohort/correlation branches,
cell-state branches, negative specificity controls, mechanistically reused
cytokines, and perturbation-supported net-effect edges. Source:
`reports/calibration_audit_2026-05-28.md`.

**Gene-specific evidence beats process paraphrase.** If a paper directly
perturbs or measures a gene-level regulator, use the gene endpoint rather than
a broad process node unless the process is the actual reusable mechanism.
Source: `reports/calibration_audit_2026-05-28.md`.

**Duplicate edges hide evidence instead of adding mechanism.** When the same
source/relationship/target appears in multiple contexts, merge support and
context into one edge rather than repeating it in separate chains. Source:
`reports/calibration_audit_2026-05-28.md`.

**Vocabulary drift in machine metadata needs human review.** The current
vocabulary still contains drift terms such as `CCF_formation`,
`chromatin_accessibility`, `cytosolic_L1_cDNA_accumulation`, and
`L1_de-repression`; propose review in an audit note rather than silently
deleting them during curation. Source: `reports/calibration_audit_2026-05-28.md`.

## Vocabulary clarifications

**CCF naming.** Use `cytoplasmic_chromatin_fragments` for chromatin-derived CCF
biology; `CCF` belongs only in prose. The lingering `CCF_formation` metadata in
Dou 2017 is convention drift, not a term to add back to the vocabulary. Source:
`dou_2017_calibration_audit.md`, `vocabulary_extraction.md`, and
`proposed_post_dececco_backfill.md`.

**Retroelement cDNA naming.** Use `cytoplasmic_retroelement_cDNA` for
L1/retroelement-derived cytoplasmic cDNA or RNA-DNA hybrid intermediates
generated by reverse transcription. DeCecco was migrated from the CCF node to
this node after curator authorization. Source:
`dececco_2019_l1_cdna_migration.md`.

**L1 drift terms.** Do not use `LINE1_transcription`, `cytoplasmic_L1_cDNA`,
`cytosolic_L1_cDNA_accumulation`, or `L1_de-repression` as nodes; use
`retrotransposon_derepression` and `cytoplasmic_retroelement_cDNA` so De Cecco
2019 and Martinez 2024 compose on the same L1 biology. Source:
`reports/calibration_audit_2026-05-28.md`.

**Chromatin-state naming.** Use `epigenetic_remodeling` for accessibility gain
and transposon methylation loss, with locus identity in context; use
`heterochromatin_organization` for the intact factor-maintained compartment
rather than histone-mark, locus-suffixed, or genotype-baked nodes. Source:
`reports/calibration_audit_2026-05-28.md`.

**Small molecules and experimental triggers.** `cGAMP` can be a valid endpoint,
and `replicative_exhaustion`/`dsDNA90` can be valid trigger endpoints when they
are the biological or experimental entity being tested. If unsure whether a new
small molecule or trigger is a node, record the uncertainty in an audit rather
than silently adding a convention. Source: `dou_2017_calibration_audit.md` and
`dou_2017_post_patch_check.md`.

**Tissue-agnostic outcomes.** Keep outcomes generic, such as `tumorigenesis`,
`tissue_inflammation`, `fibrosis`, and `apoptosis`; tissue labels belong in
context. This lesson is now fully captured as a rule in
`docs/compendium_conventions.md`, section "What is NOT a node." Source:
`dou_2017_post_patch_check.md`.

**Vocabulary additions require review.** `nasp_compendium/vocabulary.yaml` is
the machine-readable vocabulary source. Out-of-vocab warnings should be audited:
some are real convention drift, while others may be legitimate new terms that
need human approval before being added. Source: `vocabulary_extraction.md`.

## Convention edge cases

**SASP membership versus regulation.** `SASP contains X` records measured
program membership; `STING1 upregulates X` or `JAK-STAT upregulates X` records
perturbation-supported causal regulation. These can coexist when both meanings
are graph-useful, but `contains` should not replace regulatory edges. Source:
`dececco_2019_calibration_audit.md` and `proposed_post_dececco_backfill.md`.

**Paralog negative controls.** Multiple negative paralog results can be explicit
`does_not_correlate` or `does_not_drive` edges when they disambiguate
specificity and are useful for graph queries; minor or redundant paralogs can
stay in context. Flag the choice for human review. Source:
`dececco_2019_calibration_audit.md` and `proposed_post_dececco_backfill.md`.

**Drug specificity controls.** Drugs and inactive analogs usually stay in
`context` when they test a reusable biological mechanism. For DeCecco-style
3TC/K-9 experiments, the reusable graph node is the mechanism
(`retrotransposon_derepression` or `cytoplasmic_retroelement_cDNA`), not the
reagent. Source: `dececco_2019_calibration_audit.md` and
`proposed_post_dececco_backfill.md`.

**Functional activation without direct binding.** When a paper shows pathway
necessity but not physical colocalization or binding, prefer a functional
relation such as `activates` with `perturbation_supported` over
`binds_recruits`. DeCecco's L1 cDNA-to-CGAS edge uses this resolution. Source:
`dececco_2019_l1_cdna_migration.md`.

**Skip-edge warnings need classification.** The validator can flag direct edges
that coexist with longer same-paper paths, but some are legitimate model-specific
or specificity-control branches. Classify them in audits rather than silently
removing edges. Source: `skip_edge_detection.md`.

**Structured graph diffs complement rendered PNGs.** Use `compendium diff` for
fast review of paper/entity/edge changes before relying on graph render review.
The command was smoke-tested on no-change and synthetic edge-change cases.
Source: `diff_command_smoke_test.md`.

## Mechanistic edge standard

Curate the causal spine first. Add measured marker genes only when they help interpret the spine.

Prefer:
- upstream perturbation or state
- molecular intermediate
- sensor or adaptor
- signaling pathway
- program-level output
- phenotype only when supported by functional assays

Avoid:
- broad shortcuts such as `STING1 -> cognitive_decline` when intermediate mechanisms are known
- figure-label entities such as `cGAS KO inflammation`
- marker-only edges such as `MAVS -> CCL2` unless the paper directly shows MAVS-specific regulation of that molecule and the edge adds mechanistic value
- `does_not_drive` edges in the rendered main graph unless the negative result is a true specificity-control branch

## Repressor-loss logic

Do not rely on users to mentally compose two inhibitory edges.

Allowed representation:
- `cellular_senescence downregulates ADAR`
- `ADAR suppresses cytosolic_RNA_sensing`
- `cellular_senescence induces cytosolic_RNA_sensing` only when supported as a summarized consequence, with context explicitly saying it is via ADAR loss and/or dsRNA accumulation

Same for PNPT1:
- `cellular_senescence downregulates PNPT1`
- `PNPT1 suppresses cytoplasmic_mt_dsRNA`
- `cellular_senescence induces cytoplasmic_mt_dsRNA` when supported by cytosolic fractionation/J2 evidence

The rendered graph should show inhibitory edges with tee arrowheads. For readability, a summarized consequence edge is allowed if it is not used to erase the underlying mechanism.

## Pore-mediated release

Use `forms_pore_for`, not a bare `releases`, for BAX/BAK and VDAC biology.

Preferred:
- `VDAC1 forms_pore_for cytoplasmic_mtDNA`
- `VDAC3 forms_pore_for cytoplasmic_mtDNA`
- `BAX/BAK_pore forms_pore_for cytoplasmic_mt_dsRNA`
- `BAX/BAK_pore forms_pore_for cytoplasmic_mtDNA`

Avoid splitting BAX and BAK into independent mechanistic branches unless the paper tests them separately.

## Marker genes and SASP

Use `SASP contains IL6` only as a program-membership edge.
Use `MAVS drives SASP`, `type_I_IFN drives SASP`, or `NF-kB drives SASP` for mechanism-level inflammatory output.
Do not create long lists of `upregulates` edges to individual cytokines unless those individual cytokines are mechanistically central.


## Calibration history

| Paper | Calibration date | Audit report | Headline lesson |
|---|---:|---|---|
| Dou 2017 | 2026-05-27 | `dou_2017_calibration_audit.md` | Recover graph-useful branches, negative findings, and supported intermediates; CCF naming drift needed durable conventions. |
| Dou 2017 | 2026-05-27 | `dou_2017_post_patch_check.md` | Post-Dou prompt/convention patches addressed main-spine bias, shortcut risk, negative findings, and style-example use. |
| DeCecco 2019 | 2026-05-27 | `dececco_2019_calibration_audit.md` | Workflow generalized beyond Dou, but exposed L1 cDNA naming, SASP component/regulatory edge style, and paralog-control judgments. |
| DeCecco 2019 | 2026-05-27 | `dececco_2019_l1_cdna_migration.md` | Migrated L1-derived cytoplasmic DNA from CCF to `cytoplasmic_retroelement_cDNA` and used functional `activates` for CGAS. |
| Compendium infrastructure | 2026-05-27 | `vocabulary_extraction.md` | Vocabulary drift should be machine-detected and reviewed before adding terms to `vocabulary.yaml`. |
| Compendium infrastructure | 2026-05-27 | `skip_edge_detection.md` | Skip-edge detection is useful as a warning, but model-specific branches can be false positives requiring audit classification. |
| Four gold standards | 2026-05-28 | `reports/calibration_audit_2026-05-28.md` | Hardened anti-shortcut, branch-audit, marker/regulator, evidence-honesty, node-canonicalization, and duplicate-edge lessons before Martinez held-out testing. |
| Martinez 2024 held-out | 2026-05-29 | `reports/post_patch_check_martinez_2026-05-29.md` | Held-out test of the post-audit instructions for L1/chromatin naming, SPI1 promotion, marker demotion, evidence honesty, and phenotype routing. |

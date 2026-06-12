# LLM Paper Analysis Prompt — NASP compendium

You are helping me analyze a research paper for a team-science project on
Nucleic Acid Sensing Pathways (NASPs) in aging and inflammaging. I am a
computational postdoc (PhD in genetics/genomics, ML, single-cell analysis).
I curate every paper I read into a compendium of mechanistic claims that
gets rendered into a pathway map. This prompt produces two outputs from
each paper: a figure-by-figure summary for my own use, and a YAML block I
paste into the compendium.

I will verify every YAML block before committing it. Your job is to get as
close as possible to my conventions — listed below — so verification is
cheap.

---

## OUTPUT 1: Figure-by-figure summary

Summarize this paper for someone with a PhD in genetics and genomics,
experienced in machine learning and large-scale genomics data analysis.

**Premise**: 2-3 sentences. What gap or question motivated this work? What
is the central claim?

**Then for each main figure (Figure 1, 2, 3, etc.) and each sub-panel (A,
B, C, etc.):**

For every sub-panel, state:

- What is being measured or shown (assay, data type, readout)
- What is on each axis / what the visualization encodes
- What samples, conditions, or comparisons are being made
- What the result is and what it means for the paper's argument

Do not just paraphrase the figure legend. Cross-reference the main text to
understand HOW each panel advances the narrative. Explain why this panel
is here: what does it establish, confirm, or extend relative to the panels
before it?

Pay particular attention to **specificity controls** (e.g., "X knockdown
reduces Y but Z knockdown does not") and **negative findings** ("MAVS does
not correlate where STING does"). These often look like asides in the
text but they're central mechanistic information — they become explicit
edges in OUTPUT 2.

Also watch for graph-useful branch mechanisms, not just the main spine:
pathway-bias branches, in vivo consequence branches, cohort/correlative
branches, cell-state-transition branches, and specificity-control
branches. Preserve directly supported intermediates instead of collapsing
them into a shortcut edge.

After all panels in a figure, write one sentence stating what that figure
collectively demonstrates.

This is only for the main figures. If the paper has key mechanistic
evidence in the supplementary figures and those are available, include
those as well, following the same rules.

**After all figures:** Write a 2-3 sentence "Bottom line" stating the
paper's core mechanistic contribution and its main limitations or caveats.

Be thorough. I will present this paper and must be able to explain every
panel, every axis, every comparison.

---

## OUTPUT 2: NASP compendium YAML entry

After the summary, produce a YAML block I can paste directly into my
compendium file. Follow this schema and these rules exactly.

Before extracting edges, consult `docs/curation_lessons.md` for known
failure patterns. `docs/compendium_conventions.md` and
`nasp_compendium/vocabulary.yaml` are canonical; if examples in this prompt
are less complete or differ from those files, follow the conventions and
vocabulary.

### 1. Paper block schema

```yaml
[PAPER_ID]:  # e.g. Dou_nature_2017 — format: LastName_journal_year
  cite: "[CITATION]"
  url: "[URL or DOI]"
  summary: "One sentence: the core mechanistic finding."
  genes:
    # HGNC official symbols, UPPERCASE. ~10-15 most important — genes with
    # functional evidence (KO, KD, overexpression, mutation, ChIP target,
    # cohort association) or central to a validated signature. Not every
    # gene in every supplementary table.
  pathways:
    # Pathway or generalizable signaling-mechanism nodes. Prefer this
    # standardized vocabulary in nasp_compendium/vocabulary.yaml; add new
    # entries only after audit and human review.
    # Examples: cGAS-STING, RIG-I/MDA5-MAVS, NLRP3_inflammasome, NF-kB,
    # type_I_IFN, SASP, JAK-STAT, DNA_damage_response, p38_MAPK,
    # oncogenic_RAS.
  cell_types:
    # Specific. Format: compartment_celltype or state_celltype.
    # Examples: aged_CD8_T_cells, senescent_fibroblasts,
    # alveolar_macrophages, IMR90, primary_hepatocytes. Not "immune cells."
  mechanisms:
    # Processes, phenomena, and cellular states. Prefer this standardized
    # vocabulary in nasp_compendium/vocabulary.yaml; add new only after
    # audit and human review. Use canonical one-word field terms over
    # descriptive paraphrases (`tumorigenesis` not `tumor_formation`;
    # `fibrosis` not `fibrotic_tissue_formation`; `apoptosis` not
    # `programmed_cell_death`).
    # Examples: cytosolic_DNA_sensing, retrotransposon_derepression,
    # cytoplasmic_chromatin_fragments, cytoplasmic_retroelement_cDNA,
    # DNA_damage, cellular_senescence, senescence_evasion,
    # immune_cell_recruitment, immunosurveillance, tissue_inflammation.
  model_systems:
    # Use nasp_compendium/vocabulary.yaml. Examples: human_in_vitro,
    # mouse_in_vivo, mouse_in_vitro, human_cohort, organoid,
    # single_cell_atlas, CCLE_pan_cancer, TCGA_pan_cancer, UK_Biobank,
    # CZ_CELLxGENE.
  evidence_type:
    # Snake_case; use nasp_compendium/vocabulary.yaml. Examples:
    # shRNA_knockdown, genetic_KO, overexpression,
    # pharmacological_inhibition, bulk_RNA_seq, ChIP_qPCR, RT_qPCR,
    # LC_MS_metabolomics, immunoblot, immunofluorescence, IHC.
  notes: >
    Answer these 5 context questions (write "not addressed" if absent):
    1. Tissue/organ:
    2. Species:
    3. Age range or comparison:
    4. Sex-specific effects:
    5. Disease context:
    [Then add any additional mechanistic notes worth remembering — the
    spine of the mechanism, key branch points, specificity controls.]
  relevance_to_project: >
    What can I look for in single-cell/spatial atlas data because of this
    paper? Be specific: gene signatures, cell states, pathway activity
    scores, marker combinations, expected co-variation patterns.
```

### 2. Entity naming conventions

These apply both to entries in the paper block and to edge endpoints. The
same entity must have the same name everywhere — once you pick a name, use
it consistently across the paper block, across edges, and ideally across
papers.

**Prefer canonical field terms over descriptive paraphrases.** Before
composing a multi-word descriptive node name, check whether a one-word
noun already exists in the field literature (MeSH, common review titles,
abstracts). Use `tumorigenesis` not `tumor_formation`; use `fibrosis`
not `fibrotic_tissue_formation`; use `apoptosis` not
`programmed_cell_death`. Descriptive paraphrases are the main path to
near-duplicate nodes that should be one node.

**Genes and proteins.** HGNC official symbols, UPPERCASE. No legacy
aliases, no case variants. A gene and its protein are the same node;
phosphorylated/translocated/dimerized forms live in the edge `context`,
never as separate nodes.

- `CGAS` (not `cGAS`, not `MB21D1`)
- `STING1` (not `STING`, not `TMEM173`)
- `LMNB1` (not `lamin_b1`, not `Lamin B1`)
- `RELA` (not `p65`, not `NF-kB-p65`)
- `CXCL8` (not `IL8` — `IL8` only in edge `context` for readability)

**State-as-mechanism vs state-as-modification.** Most activated forms of
a protein are *state-as-modification* and stay folded into the gene
node: phospho-RELA, dimer-STING1, nuclear-NFKB. They mediate the same
downstream signaling as the parent molecule; the modification is part of
the mechanism, not a different one.

A small number of cases are *state-as-mechanism* and earn their own
node. `oncogenic_RAS` is the canonical example: constitutively-active
Ras is biologically distinct from WT Ras — different upstream cause
(mutation vs ligand), different kinetics (constitutive vs transient),
different downstream consequences (senescence/transformation vs
growth-factor signaling). WT RAS in normal physiology would not
substitute for the `oncogenic_RAS` node in a pathway map.

Test: would knockdown of the gene produce *different* consequences
depending on which state was present? If yes, the states are different
mechanisms and each can warrant its own node. If no, fold into the gene
node with state in context.

**Pathways and generalizable signaling mechanisms.** Use
`nasp_compendium/vocabulary.yaml` and `docs/compendium_conventions.md`.
A gene-level edge always beats a
pathway-level edge when the evidence is gene-specific. If the paper
knocked down CGAS, the edge endpoint is `CGAS`, not `cGAS-STING`.

**Phenomena and cellular states.** snake_case, canonical field terms.
Tissue-agnostic — see anti-pattern below.
`cytoplasmic_chromatin_fragments`, `cellular_senescence`,
`cytoplasmic_retroelement_cDNA`, `senescence_evasion`, `DNA_damage`,
`tissue_inflammation`, `tumorigenesis`, `fibrosis`, `apoptosis`,
`immunosurveillance`.
Use `cytoplasmic_chromatin_fragments` as the CCF node; `CCF` is allowed
only in context/support prose. Reserve `cytoplasmic_chromatin_fragments`
for chromatin- or nuclear-fragment-derived CCF biology, not all cytosolic
DNA species.

Use `cytoplasmic_retroelement_cDNA` for cytoplasmic reverse-transcribed
retroelement DNA, including L1/retroelement-derived cytoplasmic cDNA or
RNA-DNA hybrid intermediates generated by reverse transcription.

**Small molecules.** Lowercase, no underscores unless required: `cGAMP`,
`cAMP`.

**Stimuli and treatments.** Specific name as used in the field, *only*
when the stimulus does not correspond to a named, generalizable
mechanism: `replicative_exhaustion`, `dsDNA90`.

Where the stimulus does correspond to a generalizable mechanism, use
the mechanism — not the reagent. The reagent, dose, and conditions live
in edge `context`. Rule of thumb: if a future paper studying the same
biology might use a different reagent, the node should be the
mechanism. Concrete collapses:

- Constitutively-active Ras alleles regardless of paralog (HRasV12,
  NRasV12, KRasG12D) → `oncogenic_RAS`. Inactive-mutant controls (e.g.
  NRasV12/D38A) go in context.
- DNA-damaging agents (etoposide, ionizing radiation, doxorubicin,
  hydroxyurea, bleomycin) → `DNA_damage`. Agent, dose, and exposure
  duration go in context.
- Drugs and inactive analogs used as specificity controls usually stay
  in context unless the reusable biological entity is the drug mechanism
  itself. For DeCecco-style L1 reverse-transcriptase-dependence
  experiments, 3TC and K-9 belong in `context`; the reusable node is the
  biological mechanism, not the reagent.

Small molecules and specific experimental triggers may be valid edge endpoints
even if they are not listed in the paper block. If you are unsure whether a
new term should be a node, list it as an uncertainty instead of inventing a
new convention.

### 3. What is NOT a node

- **"X_expression."** Genes/proteins are nodes; expression-level
  evidence belongs in the edge `context`. There is no `STING1_expression`
  node — only `STING1` with edges whose context says "in the top STING1
  expression quartile of CCLE".

- **"X_in_cell_type_Y."** Phenomena are not duplicated by cell context.
  CCF in cancer cells is the same node as CCF in senescent cells; the
  context goes in the edge.

- **Tissue-specific outcome nodes.** Don't bake a tissue label into an
  outcome name. `liver_tumorigenesis`, `lung_inflammation`,
  `kidney_fibrosis` should be `tumorigenesis`, `tissue_inflammation`,
  `fibrosis`. Tissue context goes in the edge. Otherwise the same
  outcome fragments per organ.

- **Descriptive paraphrase nodes.** If a canonical one-word field term
  exists, use it. `tumor_formation` is a paraphrase of `tumorigenesis`;
  picking the paraphrase generates a near-duplicate next time someone
  uses the canonical term.

- **States of failure.** "Persistence", "retention of X", "failure to
  clear" are not nodes. They're encoded as the absence of an enabling
  relationship under loss-of-function evidence.

- **Specific reagents standing in for a mechanism.** If a generalizable
  mechanism node exists (`oncogenic_RAS`, `DNA_damage`,
  `cytoplasmic_retroelement_cDNA`), use it.

- **Modification-state pseudo-nodes.** Phospho-RELA, dimer-STING1, and
  similar PTM forms are not nodes; they're the parent gene with state in
  context. (See state-as-modification vs state-as-mechanism above for
  the one case where states do earn their own node.)

- **One-relationship-per-figure.** One mechanistic relationship is one
  edge, even if the paper shows it across multiple figures and cell
  systems. Cite all supporting figures together in `support`.

### 4. No shortcut edges across supported intermediates

If the paper supports a multi-step chain — trigger → intermediate → ...
→ outcome — don't write a shortcut edge directly from the trigger to a
far-downstream outcome that collapses everything in between. Use the
chain. The shortcut hides the mechanism; the chain shows it.

If a different model system simply re-confirms the spine (e.g., the
same CGAS-STING dependence holds in cancer cells, or in mouse liver
after IR), note that confirmation in the spine edges' `context` rather
than creating a shortcut edge.

Concrete anti-examples (drawn from past curation):

- `ionizing_radiation drives tissue_inflammation` collapses IR →
  DNA_damage → cellular_senescence → CCF → CGAS → cGAMP → STING1 →
  RELA → SASP → immune_cell_recruitment into one edge. Wrong. The
  unique claim of the IR experiment was *STING1 in vivo necessity*,
  which folds into the context of `STING1 required_for
  immunosurveillance`.
- `cytoplasmic_chromatin_fragments drives SASP` in cancer cells
  collapses CCF → CGAS → cGAMP → STING1 → RELA → SASP. Wrong. The
  unique cancer claim is `senescence_evasion retains
  cytoplasmic_chromatin_fragments`; the spine's operation in cancer
  cells goes in that edge's `context`.
- `cGAS-STING drives SASP` collapses CGAS → cGAMP → STING1 →
  downstream transcriptional/inflammatory program → SASP when that
  chain is supported by the paper or already represented as the
  reusable compendium spine. Wrong unless the paper truly treats
  cGAS-STING as an unresolved pathway unit and adds no graph-useful
  intermediate.

When tempted to write a multi-step skip, ask: what is the *unique
mechanistic claim* this experiment adds beyond the spine? Usually the
answer is a single atomic edge, with the rest of the experiment
described in `context`.

### 5. Edges schema

```yaml
# Edges from [PAPER_ID]

# Optional YAML comment paraphrasing the supporting evidence in plain English.
  - chain_id: "[short_chain_name]"
    step: 1
    source: "[upstream entity]"
    target: "[downstream entity]"
    rel: "[see vocabulary below]"
    evidence_strength: "[see vocabulary below]"
    context: "One or two sentences describing the evidence, including the
              specific reagents, cell types, tissue context, and conditions
              used."
    support: "Specific figure panels, extended data panels, or sentences."
    papers:
      - [PAPER_ID]
```

### 6. Relationship vocabulary

Use exactly these verbs. If none fits, ask before inventing one.

- `induces` — trigger to state/phenotype (e.g., `oncogenic_RAS induces
  cellular_senescence`)
- `causes` — proximal causation, often physical/biochemical
- `activates` — functional activation, typically post-translational
- `suppresses` — functional suppression demonstrated by loss/gain of
  function
- `inhibits` — synonym of suppresses; prefer `suppresses`
- `downregulates` — transcript/protein abundance decrease
- `upregulates` — transcript/protein abundance increase
- `drives` — causal positive regulation of a downstream phenomenon or
  program
- `required_for` — necessity established by loss-of-function
- `binds_recruits` — physical recruitment/binding/colocalization
- `produces` — catalytic or biosynthetic product (e.g., `CGAS produces
  cGAMP`)
- `contains` — a program/phenotype includes a component (e.g., `SASP
  contains IL1A`)
- `retains` — a state persists across a transition (e.g.,
  `senescence_evasion retains cytoplasmic_chromatin_fragments`)
- `correlates` — statistical association without claimed causal
  direction
- `negatively_correlates` — inverse statistical association
- `does_not_correlate` — explicit specificity control (e.g., `MAVS
  does_not_correlate SASP`)
- `does_not_drive` — negative perturbation result (e.g., `IFI16
  does_not_drive SASP`)

**Negative findings are edges, not omissions.** Include graph-useful
specificity controls and negative findings as explicit
`does_not_correlate` or `does_not_drive` edges.

When multiple negative paralog controls are reported, encode the ones that are
important for disambiguating specificity and likely useful for graph queries as
explicit `does_not_correlate` or `does_not_drive` edges. Minor or redundant
paralog controls can live in the `context` of the positive edge. Flag this
choice in the audit prompt/report for human review rather than silently
ignoring the control.

### 7. Evidence strength vocabulary

- `direct_measured` — the source, target, and relationship are directly
  measured in this paper (colocalization, metabolite detection,
  phosphorylation, dimerization, reporter activation).
- `perturbation_supported` — loss-of-function or gain-of-function
  evidence (shRNA, KO, overexpression, dominant-negative).
- `strong_correlative` — large-cohort statistical association (CCLE,
  TCGA, n≥100).
- `weak_correlative` — small-n correlation.
- `canonical_inferred` — relationship inferred from prior literature,
  not directly measured here. Use sparingly; only when needed for graph
  continuity and the paper explicitly invokes the canonical step.

### 8. Chain organization

`chain_id` groups edges into one mechanistic narrative. Choose chains so
the spine of the paper sits in one chain and branches sit in their own.
Do not split one mechanism into multiple chains by cell type or figure
number.

Rough template for a typical mechanism paper:

- One **spine chain** end-to-end (e.g.,
  `senescence_CCF_cGAS_STING_SASP`).
- One chain per **branch** (e.g., `senescence_IFN_suppression`,
  `immunosurveillance`, `cancer_chronic_CCF_pathway`).
- One chain for **cohort/correlative associations** (e.g.,
  `pan_cancer_pathway_association`).
- One chain for **specificity controls** or negative findings (e.g.,
  `sensor_specificity`).

Single-edge chains are fine when the unique claim of a sub-experiment
reduces to one atomic edge.

Number `step` within each chain. Steps don't have to be strictly
sequential, but they should reflect the mechanistic ordering as the
paper presents it.

### 9. Edge rules

1. **Atomic mechanistic edges whenever possible.** Each edge represents
   one step. Do not collapse intermediates (cGAMP, MAVS, IRF3, NF-kB,
   JAK-STAT, specific cytokines) if the paper measures or directly
   depends on them.

   Use `contains` sparingly. For measured programs, `SASP contains X`
   means X is a measured, graph-useful component of the SASP or related
   program. It does not replace perturbation-supported regulatory edges.
   Use `STING1 upregulates X`, `JAK-STAT upregulates X`, or similar
   regulatory edges when perturbation evidence supports a causal
   upstream regulator for that component. If genes are only readouts of
   an upstream perturbation, keep them in `context` rather than creating
   many weak `contains` edges. Both edge types can coexist when both
   meanings are graph-useful and directly supported.

2. **Pathway-level nodes only when the paper does not resolve the
   internal mechanism.** Use `cGAS-STING` or `RIG-I/MDA5-MAVS` as a
   node only if the paper speaks of the pathway as a unit and does not
   measure individual components. Prefer HGNC gene-level nodes when the
   paper resolves specific genes or proteins (e.g., `DDX58`, `IFIH1`,
   `MAVS`, `CGAS`, `STING1`), with common names such as RIG-I/MDA5 in
   `context` if useful. Do not make a pathway node activate one of its
   own components; `RIG-I/MDA5-MAVS activates MAVS` is an anti-pattern.

3. **Suppressor-loss logic stays suppressive.** If loss or
   downregulation of a suppressor permits pathway activation, encode the
   normal suppressive relationship plus the loss/downregulation evidence;
   do not make the suppressor look like a positive driver. Example:
   `ADAR suppresses cytosolic_RNA_sensing`, with context explaining that
   ADAR1 downregulation relieves dsRNA-editing/sensing suppression and
   can favor DDX58/IFIH1-MAVS activation.

4. **One edge per mechanistic relationship.** If the paper shows `CCF
   recruits CGAS` in IMR90, BJ, MEF, and three cancer cell lines, that
   is one edge with all the figure citations in `support` and the
   cell-type range in `context`. Not six edges.

5. **Every edge has a `support` field** naming the exact figure
   panel(s), extended data panel(s), or text reference(s). Add a YAML
   comment above the edge paraphrasing the evidence in plain English.

6. **No unsupported edges.** Do not infer missing biology from
   background knowledge. The exception is `canonical_inferred`: when
   the paper directly invokes a canonical step but does not test it.

7. **A typical paper yields ~5-20 atomic edges** depending on
   mechanistic depth and how many branches/controls the paper
   includes.

### 10. Examples

These follow the conventions exactly. Use them as a template for format
and level of detail.

```yaml
# CCF colocalize with CGAS puncta in senescent IMR90, BJ, MEF, OIS-evaded IMR90,
# and PANC-1/MDA-MB-468/TOV-21G. Transfected CCF induce SASP in a CGAS-dependent
# manner.
  - chain_id: senescence_CCF_cGAS_STING_SASP
    step: 3
    source: cytoplasmic_chromatin_fragments
    target: CGAS
    rel: binds_recruits
    evidence_strength: direct_measured
    context: "CCF colocalize with CGAS puncta in senescent IMR90, BJ, MEF,
              OIS-evaded IMR90, and multiple cancer cell lines (PANC-1,
              MDA-MB-468, TOV-21G). Transfected chromatin fragments induce
              SASP in a CGAS-dependent manner."
    support: "Fig. 1a; Extended Data Fig. 1c-e; Extended Data Fig. 8a, 8e;
              Extended Data Fig. 4j-k"
    papers:
      - Dou_nature_2017

# Mechanism-over-reagent: HRasV12 and NRasV12 both collapse to oncogenic_RAS,
# alleles and the D38A control go in context.
  - chain_id: senescence_triggers
    step: 1
    source: oncogenic_RAS
    target: cellular_senescence
    rel: induces
    evidence_strength: direct_measured
    context: "Constitutively-active Ras alleles induce senescence with
              downstream cGAS-STING-SASP activation. This paper: HRasV12 in
              IMR90 and BJ fibroblasts (OIS in vitro); NRasV12 in mouse
              hepatocytes via hydrodynamic injection (in vivo). The
              non-oncogenic NRasV12/D38A effector-binding mutant does not
              induce senescence, isolating Ras signaling as the cause rather
              than transgene expression."
    support: "Fig. 1a,c; Fig. 3c-e; Extended Data Fig. 2a-b;
              Extended Data Fig. 6a-e"
    papers:
      - Dou_nature_2017

# Mechanism-over-reagent: etoposide and ionizing radiation both collapse to
# DNA_damage, agents and doses go in context.
  - chain_id: senescence_triggers
    step: 2
    source: DNA_damage
    target: cellular_senescence
    rel: induces
    evidence_strength: direct_measured
    context: "DNA-damaging agents induce senescence with downstream CCF
              formation, cGAMP production, and SASP activation. This paper:
              etoposide at 100 μM (IMR90) and 40 μM (BJ) for in vitro
              DNA-damage-induced senescence; sub-lethal 4 Gy ionizing
              radiation for in vivo senescence in mouse hepatocytes, where
              γH2AX, IL1A, CCF, and cGAMP were all detected."
    support: "Fig. 2; Fig. 3a-b; Extended Data Fig. 2c-d;
              Extended Data Fig. 5a-c"
    papers:
      - Dou_nature_2017

# Tissue-agnostic outcome node: tumorigenesis (canonical MeSH term), with
# liver in context. NOT liver_tumor_formation or liver_tumorigenesis.
  - chain_id: immunosurveillance
    step: 2
    source: immunosurveillance
    target: tumorigenesis
    rel: suppresses
    evidence_strength: strong_correlative
    context: "STING1-null mice that failed to clear NRasV12-positive
              hepatocytes developed intrahepatic NRas-positive liver tumors
              8 months post-injection (7/7 STING1-null vs 0/5 WT). Tissue
              context: liver; the immunosurveillance → tumorigenesis logic
              is not tested in other tissues here."
    support: "Fig. 3h; Extended Data Fig. 6g"
    papers:
      - Dou_nature_2017

# Negative finding as edge: MAVS does not correlate with inflammatory genes
# in CCLE or TCGA, distinguishing the DNA-sensing branch from RNA-sensing.
  - chain_id: pan_cancer_pathway_association
    step: 4
    source: MAVS
    target: SASP
    rel: does_not_correlate
    evidence_strength: strong_correlative
    context: "MAVS (cytosolic RNA-sensing adaptor) shows no association with
              inflammatory genes in CCLE or TCGA. Establishes that the
              pan-cancer correlation is specific to the cytosolic DNA-sensing
              branch and not a generic innate immunity effect."
    support: "Extended Data Fig. 9d; Supplementary Table 4"
    papers:
      - Dou_nature_2017

# Negative finding as edge: IFI16 knockdown does not reduce SASP, while CGAS
# and STING1 knockdown do.
  - chain_id: sensor_specificity
    step: 1
    source: IFI16
    target: SASP
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "IFI16 knockdown did not reduce SASP gene expression in
              established senescent IMR90, distinguishing IFI16 from
              CGAS/STING1. IFI16 has a regulatory but non-essential role for
              dsDNA90-induced response, indicating it is not the primary
              sensor in this context."
    support: "Extended Data Fig. 3j-k"
    papers:
      - Dou_nature_2017
```

Mechanistic chain templates for common NASP biology:

- `LINE-1_derepression → dsRNA → MDA5 → MAVS → IRF3 → type_I_IFN`
- `LINE-1_derepression → cytoplasmic_retroelement_cDNA → CGAS → cGAMP → STING1
  → RELA → SASP`
- `mtDNA_release → TLR9 → NF-kB → IL6`
- `micronuclei_rupture → CGAS → cGAMP → STING1 → IRF3 → type_I_IFN`
- `DNA_damage → cellular_senescence → LMNB1↓ → cytoplasmic_chromatin_fragments
  → CGAS → cGAMP → STING1 → RELA → SASP → immune_cell_recruitment`

---

## Final check

Before you output, verify:

1. Every figure panel in the paper is accounted for in OUTPUT 1,
   including specificity controls and negative findings.
2. The YAML in OUTPUT 2 parses as valid YAML (indentation, quoting, no
   stray characters).
3. Gene symbols are HGNC standard and UPPERCASE; no legacy aliases.
4. Phenomenon and outcome nodes use canonical one-word field terms, not
   descriptive paraphrases (`tumorigenesis` not `tumor_formation`,
   `fibrosis` not `fibrotic_tissue_formation`).
5. Where the paper used specific reagents (Ras alleles, DNA-damaging
   agents, radiation doses), the mechanism node generalizes
   (`oncogenic_RAS`, `DNA_damage`) and the reagent lives in `context`.
6. No tissue-specific outcome nodes (`liver_tumorigenesis`,
   `lung_inflammation`); tissue context goes in the edge.
7. No shortcut edges that collapse supported intermediates. If a
   trigger and a far-downstream outcome are both represented in the
   paper, write the atomic chain; if a confirmation system just
   re-validates the spine, note it in `context` rather than as a new
   skip-edge.
8. Modification-state forms (phospho-X, dimer-X, nuclear-X) are not
   separate nodes — fold into the parent gene with state in context.
   State-as-mechanism exceptions (like `oncogenic_RAS`) are used only
   when the state has a distinct upstream cause and distinct downstream
   consequences from the WT form.
9. Graph-useful negative findings and specificity controls appear as
   `does_not_correlate` / `does_not_drive` edges; minor redundant controls
   kept in context are noted for audit review.
10. One edge per mechanistic relationship, not one edge per figure that
    restates it.
11. The `relevance_to_project` answer is specific and actionable, not
    generic.

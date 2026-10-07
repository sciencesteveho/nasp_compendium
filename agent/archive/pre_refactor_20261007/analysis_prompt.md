
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

Before extracting edges, consult `agent/curation_lessons.md` for known
failure patterns. `agent/conventions.md` and
`agent/vocabulary.yaml` are canonical; if examples in this prompt
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
    # standardized vocabulary in agent/vocabulary.yaml; add new
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
    # vocabulary in agent/vocabulary.yaml; add new only after
    # audit and human review. Use canonical one-word field terms over
    # descriptive paraphrases (`tumorigenesis` not `tumor_formation`;
    # `fibrosis` not `fibrotic_tissue_formation`; `apoptosis` not
    # `programmed_cell_death`).
    # Examples: cytosolic_DNA_sensing, retrotransposon_derepression,
    # cytoplasmic_chromatin_fragments, cytoplasmic_retroelement_cDNA,
    # DNA_damage, cellular_senescence, senescence_evasion,
    # immune_cell_recruitment, immunosurveillance, tissue_inflammation.
  model_systems:
    # Use agent/vocabulary.yaml. Examples: human_in_vitro,
    # mouse_in_vivo, mouse_in_vitro, human_cohort, organoid,
    # single_cell_atlas, CCLE_pan_cancer, TCGA_pan_cancer, UK_Biobank,
    # CZ_CELLxGENE.
  evidence_type:
    # Snake_case; use agent/vocabulary.yaml. Examples:
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

### 2. Entity and node rules

Node naming, what is and is not a node, and the no-shortcut-across-supported-intermediates rule are all defined in `agent/conventions.md` (sections
"Entity naming", "What is NOT a node", and "No shortcut edges across
supported intermediates"). Apply them exactly; they are not restated here.

Key reminders while drafting endpoints:
- Genes/proteins: HGNC official symbols, UPPERCASE (`CGAS`, `STING1`); PTM
  forms stay in edge `context`, not as separate nodes.
- Phenomena/outcomes: canonical one-word field terms, tissue-agnostic
  (`tumorigenesis` not `liver_tumor_formation`).
- Reagents standing in for a mechanism collapse to the mechanism node
  (`oncogenic_RAS`, `DNA_damage`); the reagent/dose lives in `context`.
- If unsure whether something is a node, list it as an uncertainty rather
  than inventing a convention.

### 3. Edges schema

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

### 4. Relationship and evidence vocabulary, chain organization

The controlled relationship verbs, the evidence-strength levels, and the
chain-organization rules are defined in `agent/conventions.md` (sections
"Edge relationship vocabulary", "Evidence strength vocabulary", and "Chain
organization"). Use those verbs exactly; if none fits, ask before inventing
one. Do not restate the vocabulary here.

**Negative findings are edges, not omissions.** Encode graph-useful
specificity controls and negative results as explicit `does_not_correlate`
or `does_not_drive` edges (e.g. `MAVS does_not_correlate SASP`,
`IFI16 does_not_drive SASP`). Minor or redundant paralog controls can stay
in the positive edge's `context`; flag the choice for audit review.

### 5. Edge rules

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

### 6. Examples

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

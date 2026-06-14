paper:

  Tyshkovskiy_Nature_2026:
    cite: "Tyshkovskiy A, Kholdina D, Davitadze M, Molière A, Moldakozhayev A, Tongu Y, Kasahara T, Glubokov D, Eames A, Kats LM, Vladimirova A, Ying K, Liu H, Zhang B, Khasanova U, Moqri M, Van Raamsdonk JM, Harrison DE, Strong R, Abe T, Dmitriev SE, Gladyshev VN. Universal transcriptomic hallmarks of mammalian ageing and mortality. Nature 2026. doi:10.1038/s41586-026-10542-3."
    url: "https://doi.org/10.1038/s41586-026-10542-3"
    summary: "A large-scale transcriptomic biomarker study integrating >11,000 transcriptomes across 4 mammals and >25 tissues to build interpretable clocks of chronological age and expected mortality. Its findings are predominantly correlative gene-trait and module-trait associations, not perturbation-supported causal mechanisms. Universal pro-mortality transcript markers (CDKN1A/p21, LGALS3, GPNMB) rise with age and mortality across species, cell types, and chronic-disease models, and three of them (GPNMB, CDKN1A, LGALS3) are validated at the plasma-protein level against mortality and multimorbidity in UK Biobank. A co-expression module enriched for interferon/innate-immune signalling tracks ageing and mortality, while metabolic/mitochondrial modules track lifespan in the opposite direction. Damage models (inflammation/LPS, replicative senescence, metabolic inhibition, gamma-irradiation) raise transcriptomic age; rejuvenation contexts (immortalization, reprogramming, heterochronic parabiosis, early embryogenesis) lower it. This is a boundary/out-of-scope paper for a NASP mechanism compendium: it contains no nucleic-acid-sensing perturbation and no sensor->adaptor->signalling chain. See the SCOPE audit note before relying on these edges."
    nucleic_acid_sensors: []
    genes:
      - CDKN1A
      - LGALS3
      - GPNMB
      - CST7
      - IGF1
      - NREP
      - COL1A1
      - COL3A1
      - EDA2R
    pathways:
      - type_I_IFN
      - p53_p21
    cell_types:
      - WI38
      - human_diploid_fibroblasts
      - naked_mole_rat_fibroblasts
    mechanisms:
      - mortality
      - cellular_senescence
      - tissue_inflammation
      - DNA_damage
      - cellular_reprogramming
    model_systems:
      - mouse_in_vivo
      - rat_in_vivo
      - macaque_in_vivo
      - human_in_vivo
      - human_in_vitro
      - UK_Biobank_cohort
      - TabulaMurisSenis_scRNA_seq
    evidence_type:
      - bulk_RNA_seq
      - single_cell_RNA_seq
      - single_nucleus_RNA_seq
      - meta_analysis
      - machine_learning_clock
      - WGCNA_module_analysis
      - GSEA
      - survival_analysis
      - plasma_proteomics
      - Cox_proportional_hazards
    notes: >
      SCOPE AUDIT NOTE (read before relying on any edge below).
      This paper does NOT fit the mechanistic NASP template that the five gold
      standards (Dou, De Cecco, Gulen, Lopez-Polo, Martinez) are built on. Those
      papers each have a perturbation-supported causal spine running from a
      trigger through a nucleic-acid sensor and adaptor to a signalling pathway,
      program, and phenotype. This paper has none of that:
        - No nucleic-acid-sensing perturbation. CGAS, STING1, MAVS, RIG-I/DDX58,
          MDA5, AIM2, IFI16, and TLRs are absent from the text. ZBP1 appears once
          as a single entry in a clock-coefficient list (alongside NLRC5, CASP1),
          measured as correlative abundance, never perturbed or placed in a
          sensing chain. "Interferon signalling" appears only as a co-expression
          MODULE LABEL that statistically correlates with mortality, not as a
          perturbed pathway with an upstream sensor.
        - The core results are correlative: regression of >9,000 genes against
          age/mortality/lifespan across a meta-dataset, machine-learning clocks,
          and WGCNA co-expression modules. These are `correlates` /
          `negatively_correlates` relationships at `strong_correlative`, not
          `drives` or `perturbation_supported` causal edges.
        - The interventions (LPS, caloric restriction, Klotho-KO, reprogramming,
          hTERT, gamma-irradiation, oligomycin, 2-DG, heterochronic parabiosis)
          are read out as clock-age (tAge) shifts, not as perturbations that
          isolate a mechanism. Encoding "LPS drives tissue_inflammation" etc.
          would be a shortcut across un-measured intermediates and would
          misrepresent a clock readout as a mechanism.
      Conventions that would be VIOLATED by forcing a mechanistic gold standard
      here, and which I therefore did not do:
        - No shortcut edges across supported intermediates (conventions
          "No shortcut edges"): there is no measured intermediate chain to skip,
          so any trigger->phenotype edge would be a pure shortcut.
        - No "X_expression" nodes and no descriptive-paraphrase / module-label
          nodes (conventions "What is NOT a node"): module names like
          "innate immunity/inflammation" or "chromatin modification (1)" are
          analysis artifacts, not field-canonical mechanism nodes.
        - Evidence-strength honesty (curation_lessons, "evidence strength is
          edge-specific"): cohort-scale regressions are `strong_correlative`;
          they must not be upgraded to `perturbation_supported` because an assay
          (RNA-seq) was run.
      What I curated instead: the small set of relationships the paper actually
      supports, almost all of them correlative, plus the two genuine
      state-reversal findings (heterochronic parabiosis and early embryogenesis
      lowering the mortality-associated transcriptomic state). The clocks,
      modules, and TACO/tAge tooling are described here for browsability but are
      NOT nodes.
      VOCABULARY-REVIEW ITEMS (new terms, flagged per the tiered-vocab gate; not
      added to vocabulary.yaml here): `cellular_reprogramming`,
      `machine_learning_clock`, `WGCNA_module_analysis`, `meta_analysis`,
      `plasma_proteomics`, `Cox_proportional_hazards`, `UK_Biobank_cohort`,
      `TabulaMurisSenis_scRNA_seq`, `naked_mole_rat_fibroblasts`,
      `macaque_in_vivo`, `rat_in_vivo`. Several are evidence_type/model_system
      terms that the gate may treat with a looser policy; flagged for human
      review rather than coined as canonical.
      HUMAN-DECISION REQUIRED: recommend this paper be classified as
      out-of-scope for the NASP mechanism graph, or admitted only as a
      correlative "ageing context" satellite that links existing canonical nodes
      (cellular_senescence, tissue_inflammation, type_I_IFN, DNA_damage) to
      ageing/mortality outcomes. Do not merge its correlative edges into
      mechanistic spines from other papers.
    relevance_to_project: >
      Limited and indirect for a NASP compendium. The usable contribution is a
      set of large-cohort, cross-species ageing/mortality priors on nodes that
      already exist in the compendium: a type_I_IFN / innate-immune
      transcriptional module is robustly pro-mortality and pro-ageing, while
      mitochondrial/metabolic programs are pro-longevity. For single-cell work,
      CDKN1A, LGALS3, and GPNMB are validated pan-tissue pro-mortality markers
      (protein-level for the latter three in UK Biobank) usable as an
      ageing/senescence-burden covariate when interpreting NASP activity in aged
      tissue. It does NOT provide sensor-level mechanism and should not be used
      to assert causal cGAS-STING/IFN wiring.

edges:

# ─────────────────────────────────────────────────────────────────────────────
# SCOPE: This paper supports correlative associations, not a mechanistic spine.
# Almost every edge below is `correlates` / `negatively_correlates` at
# `strong_correlative` (cohort n in the thousands). Two edges capture genuine
# state reversals (parabiosis, embryogenesis). No sensor chain exists to curate.
# See the SCOPE AUDIT NOTE in the paper block. Endpoints reuse existing canonical
# nodes wherever possible; nothing here should be wired into another paper's
# mechanistic chain.
# ─────────────────────────────────────────────────────────────────────────────

# ─── CHAIN 1: universal pro-mortality transcript/protein markers ─────────────

  - chain_id: universal_mortality_markers
    step: 1
    source: CDKN1A
    target: mortality
    rel: correlates
    evidence_strength: strong_correlative
    context: "CDKN1A (p21, a p53-pathway cell-cycle inhibitor) is among the top
      positive features shared by the chronological-age and mortality
      transcriptomic clocks and is consistently upregulated with age and
      age-adjusted mortality across the rodent meta-dataset, across rodents and
      primates, across 48/49 scRNA-seq cell types, and across multiple
      chronic-disease models (Fig. 1n, 2b, 2i, 5d). At the plasma-protein level,
      CDKN1A associates with human time-to-death and multimorbidity in UK Biobank
      (n=51,276; Fig. 5h). This is a cohort-scale statistical association measured
      via clock coefficients and Cox models, not a perturbation; encoded as
      `correlates` / `strong_correlative`. CDKN1A also moves in the rejuvenation
      direction (down) under parabiosis and early embryogenesis (see chains 4-5),
      reinforcing the association without establishing causal direction here."
    support: "Fig. 1n; Fig. 2b, 2i; Fig. 5d, 5h; Extended Data Fig. 2m"
    papers:
      - Tyshkovskiy_Nature_2026

  - chain_id: universal_mortality_markers
    step: 2
    source: LGALS3
    target: mortality
    rel: correlates
    evidence_strength: strong_correlative
    context: "LGALS3 (galectin-3) is a conserved pro-mortality transcript marker,
      upregulated with ageing and age-adjusted mortality across cell types
      (Fig. 2i) and one of the three genes most consistently upregulated across
      chronic-disease models (significant in >=5 of the disease datasets;
      Fig. 5d). Plasma LGALS3 protein associates with human time-to-death and
      multimorbidity in UK Biobank (n=51,647; Fig. 5h). Cohort-scale association,
      not perturbation; `correlates` / `strong_correlative`."
    support: "Fig. 2i; Fig. 5d, 5h"
    papers:
      - Tyshkovskiy_Nature_2026

  - chain_id: universal_mortality_markers
    step: 3
    source: GPNMB
    target: mortality
    rel: correlates
    evidence_strength: strong_correlative
    context: "GPNMB (an inflammation-associated glycoprotein) is a top positive
      feature of both chronological-age and mortality clocks (Fig. 1n), a
      conserved cross-species upregulated ageing marker (Fig. 2b), and among the
      most consistent pro-mortality contributors across chronic diseases
      (Fig. 5d). Plasma GPNMB protein associates with human time-to-death and
      multimorbidity in UK Biobank (n=50,117; Fig. 5h). Cohort-scale association;
      `correlates` / `strong_correlative`."
    support: "Fig. 1n; Fig. 2b; Fig. 5d, 5h"
    papers:
      - Tyshkovskiy_Nature_2026

# IGF1 is the canonical longevity regulator recovered here as a lifespan-positive
# marker; encoded as an inverse association with mortality, not as a perturbation.
  - chain_id: universal_mortality_markers
    step: 4
    source: IGF1
    target: mortality
    rel: negatively_correlates
    evidence_strength: strong_correlative
    context: "Igf1 is among the genes negatively associated with maximum lifespan
      and tends to decline with age in the rodent meta-dataset (mixed-effects
      regression; Fig. 1h, Extended Data Fig. 1o). The paper frames IGF1 as a
      canonical within- and cross-species longevity regulator recovered by the
      correlative signature; it does not perturb IGF1 here. Direction is encoded
      as `negatively_correlates` with mortality to reflect its lifespan-positive
      association; `strong_correlative`. NREP, COL1A1, and COL3A1 are the other
      lifespan-positive (mortality-negative) markers and are kept in this edge's
      context as a regenerative/wound-healing-loss signature rather than as
      separate marker edges, since they are not reused mechanistically."
    support: "Fig. 1h; Fig. 1n; Extended Data Fig. 1o"
    papers:
      - Tyshkovskiy_Nature_2026

# ─── CHAIN 2: interferon/innate-immune co-expression module vs mortality ─────

# The single NASP-adjacent finding, and even this is a correlative MODULE-level
# association, not a sensor-driven pathway. Endpoint is the existing canonical
# type_I_IFN node; the WGCNA module is described in context, not coined as a node.
  - chain_id: ifn_module_mortality_association
    step: 1
    source: type_I_IFN
    target: mortality
    rel: correlates
    evidence_strength: strong_correlative
    context: "A WGCNA co-expression module enriched for interferon / innate-immune
      signalling is positively associated with chronological age and expected
      mortality and negatively associated with maximum lifespan across the rodent
      and multi-species meta-datasets, and its module-specific clock is among the
      strongest pro-mortality responders in chronic-disease and LPS models
      (Fig. 1i, 3b, 3e, 5e; Extended Data Fig. 5d,e). This is a set-level
      statistical association of a transcriptional module, NOT a perturbation of a
      cytosolic-DNA/RNA sensor or of STING/MAVS signalling; no sensor is measured
      or manipulated. Encoded at the canonical `type_I_IFN` pathway node as
      `correlates` / `strong_correlative`. The reciprocal pro-longevity
      association of mitochondrial/oxidative-phosphorylation and lipid-metabolism
      modules is the consistent opposite pole and is kept in context rather than
      curated as a separate metabolism node, since those modules are analysis
      artifacts without a canonical NASP node."
    support: "Fig. 1i; Fig. 3b, 3e; Fig. 5e; Extended Data Fig. 5d, 5e"
    papers:
      - Tyshkovskiy_Nature_2026

# ─── CHAIN 3: ageing/mortality state co-occurs with canonical NASP-relevant states

# Cross-cell-type scRNA-seq shows the pro-mortality shift co-occurs with
# senescence-, inflammation-, and apoptosis-associated transcripts. Correlative
# co-occurrence on existing canonical nodes; deliberately NOT a causal chain.
  - chain_id: mortality_state_cooccurrence
    step: 1
    source: cellular_senescence
    target: mortality
    rel: correlates
    evidence_strength: strong_correlative
    context: "Across 49 scRNA-seq cell types in Tabula Muris Senis, the top shared
      pro-mortality expression changes include upregulation of senescence-,
      inflammation-, and apoptosis-associated genes (Cdkn1a, Lgals3, Casp1,
      S100a8, S100a4) with downregulation of the ECM regulator Sparc (Fig. 2i).
      This records that a senescence-associated transcriptional state co-occurs
      with the mortality-associated state at single-cell resolution; it is a
      correlative co-occurrence, not evidence that senescence drives mortality in
      this paper. `correlates` / `strong_correlative`."
    support: "Fig. 2i; Extended Data Fig. 4d"
    papers:
      - Tyshkovskiy_Nature_2026

  - chain_id: mortality_state_cooccurrence
    step: 2
    source: tissue_inflammation
    target: mortality
    rel: correlates
    evidence_strength: strong_correlative
    context: "Inflammatory transcriptional programs are positively associated with
      ageing and mortality at gene, pathway, and module levels across species and
      are the dominant accelerated module across chronic-disease models and in the
      LPS neuroinflammation model (Fig. 1i, 2i, 3e, 5e). Encoded as a correlative
      association of a canonical inflammation state with mortality. The LPS,
      chronic-disease, and damage models raise the inflammatory module clock but
      are clock readouts rather than mechanism-isolating perturbations, so they
      stay in context and are not separate `drives` edges. `correlates` /
      `strong_correlative`."
    support: "Fig. 1i; Fig. 2i; Fig. 3e; Fig. 5e"
    papers:
      - Tyshkovskiy_Nature_2026

# ─── CHAIN 4: heterochronic parabiosis reverses the mortality-associated state ─

# A genuine intervention effect on the mortality-associated transcriptomic state.
# Still a clock readout, so `strong_correlative`, but it is a real reversal and
# worth an edge; encoded as a negative association of the rejuvenation context
# with the mortality state.
  - chain_id: rejuvenation_state_reversal
    step: 1
    source: heterochronic_parabiosis
    target: mortality
    rel: negatively_correlates
    evidence_strength: strong_correlative
    context: "Old mice in heterochronic parabiosis (sharing circulation with young
      partners) show a significant reduction in the mortality-associated
      transcriptomic state (mortality clock tAge), significant at the attached
      time point and for both clocks after detachment, spanning most module clocks
      (Fig. 6a,c; Extended Data Fig. 9a-c). The strongest contributor is Nrep
      upregulation, with downregulation of Cdkn1a and Vcam1 (Fig. 6b). This is a
      measured reversal of the clock state, read out transcriptomically rather
      than via a mechanism-isolating perturbation, so `strong_correlative`.
      heterochronic_parabiosis is the experimental rejuvenation context node; the
      paralleled epigenetic-age behaviour from prior work is noted as cited
      context, not a separate edge."
    support: "Fig. 6a, 6b, 6c; Extended Data Fig. 9a, 9b, 9c"
    papers:
      - Tyshkovskiy_Nature_2026

# ─── CHAIN 5: early embryogenesis transiently resets the mortality state ──────

  - chain_id: embryogenesis_state_reset
    step: 1
    source: early_embryogenesis
    target: mortality
    rel: negatively_correlates
    evidence_strength: strong_correlative
    context: "Mouse embryogenesis profiles (zygote to birth) show a U-shaped
      transcriptomic-age trajectory with a minimum around E10 (95% CI E8.5-E15),
      i.e. a transient decrease in chronological and mortality clock tAge during
      early development before a monotonic rise, mirroring the DNA-methylation
      'ground zero' rejuvenation phase (Fig. 6d; Extended Data Fig. 9d-g). Key
      contributors downregulated up to E10 and upregulated thereafter include
      Cdkn1a, S100a8, S100a9, and Lgals3. The decrease persists when recomputed on
      phase-specific gene sets, arguing it is not solely global transcriptome
      remodelling. Measured clock-state reset, read out transcriptomically;
      `negatively_correlates` / `strong_correlative`. early_embryogenesis is the
      developmental rejuvenation context node."
    support: "Fig. 6d; Extended Data Fig. 9d, 9e, 9f, 9g"
    papers:
      - Tyshkovskiy_Nature_2026

# ─── CHAIN 6: transcriptomic and DNA-methylation ageing clocks co-accelerate ──

# Cross-modality correlation, included because it is a clean, directly-measured
# human-blood association and the chromatin module is the strongest link; this is
# the one `correlates` edge that is `direct_measured` rather than meta-analytic,
# but it is between two MEASUREMENT MODALITIES, not biological nodes, so it is
# flagged for human review as possibly belonging in context rather than as an edge.
  - chain_id: clock_modality_concordance
    step: 1
    source: type_I_IFN
    target: mortality
    rel: does_not_drive
    evidence_strength: strong_correlative
    context: "REVIEW FLAG (possible non-edge). Across human-blood data,
      transcriptomic mortality clocks and DNA-methylation clocks show correlated
      age acceleration, strongest for the chromatin-modification module clock, and
      transcriptomic mortality clocks predict time to death in Framingham
      (n=3,698) independent of age and sex (Fig. 5f,g). This is a
      modality-concordance and prognostic-performance result about CLOCKS, not a
      biological regulatory relationship between nodes. I could not encode it as a
      faithful node-to-node edge without inventing a clock pseudo-node, which the
      conventions forbid. The `type_I_IFN does_not_drive mortality` placeholder is
      deliberately conservative and almost certainly WRONG as biology; it exists
      only to surface this finding for human review. RECOMMEND: drop this edge and
      record clock concordance as paper-block context, OR admit a dedicated
      out-of-graph 'biomarker performance' annotation that is not part of the
      mechanism graph."
    support: "Fig. 5f, 5g"
    papers:
      - Tyshkovskiy_Nature_2026

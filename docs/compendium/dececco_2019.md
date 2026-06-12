paper:

  DeCecco_nature_2019:
    cite: "De Cecco M, Ito T, Petrashen AP, et al. L1 drives IFN in senescent cells
      and promotes age-associated inflammation. Nature. 2019;566(7742):73-78."
    url: "https://doi.org/10.1038/s41586-018-0784-9"
    summary: "L1 retrotransposons are derepressed in late cellular senescence through
      convergent failure of RB1, TREX1, and FOXA1 surveillance, producing cytoplasmic
      cDNA that activates cGAS-STING1 to drive a type-I interferon response that
      amplifies the mature SASP; lamivudine (3TC) inhibits this axis and reverses
      multiple tissue aging phenotypes in old mice."
    nucleic_acid_sensors:
      - CGAS
      - STING1
    genes:
      - RB1
      - RBL1
      - FOXA1
      - TREX1
      - CGAS
      - STING1
      - IFNAR1
      - IFNAR2
      - IRF7
      - OAS1
      - STAT2
      - CDKN1A
      - CDKN2A
      - IL6
      - CCL2
      - MMP3
      - IL1B
      - LMNB1
    pathways:
      - cGAS-STING
      - type_I_IFN
      - SASP
      - JAK-STAT
    cell_types:
      - senescent_fibroblasts
      - LF1_fibroblasts
      - IMR90
      - WI38
      - aged_dermal_fibroblasts
      - aged_adipocytes
      - aged_hepatocytes
      - aged_skeletal_muscle_cells
    mechanisms:
      - retrotransposon_derepression
      - cytoplasmic_retroelement_cDNA
      - cytosolic_DNA_sensing
      - cellular_senescence
      - SASP_secretion
      - epigenetic_remodeling
      - tissue_inflammation
      - immune_cell_recruitment
    model_systems:
      - human_in_vitro
      - mouse_in_vivo
      - human_cohort
    evidence_type:
      - shRNA_knockdown
      - genetic_KO
      - overexpression
      - pharmacological_inhibition
      - bulk_RNA_seq
      - RT_qPCR
      - ChIP_qPCR
      - immunofluorescence
      - IHC
      - immunoblot
    notes: >
      1. Tissue/organ: Skin (human), white adipose, liver, skeletal muscle, kidney
      (mouse); lung-derived fibroblasts (in vitro).
      2. Species: Human (in vitro LF1/IMR90/WI38 fibroblasts and skin biopsy),
      mouse (C57BL/6J, in vivo).
      3. Age range or comparison: In vitro: early passage vs. 8 weeks (early
      senescence) vs. 16 weeks (late senescence). In vivo: 5 months (young) vs.
      26-29 months (aged); irradiation model at 6 months post-irradiation.
      4. Sex-specific effects: Mouse experiments performed in both sexes; L1 and
      IFN-I upregulation with age observed in both male and female adipose and
      liver (Extended Data Fig. 9a-c, 10g). No sex-specific differences reported.
      5. Disease context: Normal aging and cellular senescence; no disease model.
      Paper proposes relevance to age-associated inflammatory diseases (inflammaging).
      Mechanistic spine: Senescence → RB1 loss (heterochromatin) + FOXA1 gain
      (promoter activation) + TREX1 loss (cDNA clearance) → L1 transcriptional
      derepression → cytoplasmic_retroelement_cDNA (L1 cDNA ssDNA/RNA-DNA
      hybrid) → CGAS activation
      → cGAMP (canonical_inferred) → STING1 → type_I_IFN (via IRF3, canonical) +
      RELA (NF-kB, for SASP) → JAK-STAT (STAT2 phosphorylation, IRF7 induction) →
      amplification of late SASP (CCL2, IL6, MMP3). Early SASP (IL1B) is independent
      of IFN-I. Key specificity controls: (1) RBL1 and RBL2 do not change in
      senescence (RB1-specific); (2) K-9 (methoxy-3TC, cannot inhibit RT) does not
      suppress IFN-I at 10 uM in vitro or in vivo, confirming RT inhibition is
      required; (3) IFNAR1/2 KO suppresses late SASP (CCL2, IL6, MMP3) but not
      IL1B; (4) 3TC does not affect L1 transcript levels, confirming trigger is cDNA
      not RNA; (5) cGAS and STING1 knockdown suppress both IFN-I and late SASP.
      In vivo: ORF1+ cells in aged mouse tissues colocalize with SA-beta-Gal+
      senescent cells. In human skin (Leiden Longevity Study, n=4 subjects, mean
      age 57), 10.7% of dermal fibroblasts are p16+; 10.3% of p16+ cells are also
      ORF1+; ORF1 is absent in p16-negative cells (Extended Data Fig. 8f). 20.4%
      of dermal fibroblasts are pSTAT1+; 5.4% of pSTAT1+ cells are ORF1+ (Extended
      Data Fig. 8g). Mouse ORF1+ frequencies: muscle 0.27% (5 mo) to 3.10% (26 mo)
      males; liver 1.50% to 5.77% males, 2.40% to 5.82% females (Fig. 4a table).
      3TC is senostatic: suppresses IFN-I/SASP without reducing p16 or senescent
      cell number.

edges:

# Edges from DeCecco_nature_2019

# ─── CHAIN 1: L1 surveillance failure → L1 derepression ──────────────────────

# Senescence causes loss of H3K9me3 and H3K27me3 at L1 loci, coinciding with
# RB1 loss of occupancy at the L1 5′ UTR.
  - chain_id: L1_surveillance_failure
    step: 1
    source: cellular_senescence
    target: epigenetic_remodeling
    rel: induces
    evidence_strength: direct_measured
    context: "H3K9me3 and H3K27me3 marks at L1 5′ UTR, ORF1, and ORF2 decline
      significantly in late senescent LF1 fibroblasts (16 weeks) by ChIP-qPCR.
      RB1 ChIP signal at the L1 5′ UTR is present in EP, reduced in early
      senescence (8 weeks), and undetectable in late senescence. This
      heterochromatin loss is the mechanistic basis for L1 transcriptional
      derepression."
    support: "Fig. 2a; Extended Data Fig. 4c"
    papers:
      - DeCecco_nature_2019

# RB1 loss is both a marker and a cause of L1 derepression; bidirectional
# perturbation (OE suppresses, KD enhances) confirms necessity and sufficiency.
# RBL1 and RBL2 do not change — effect is RB1-specific (Extended Data Fig. 4b).
  - chain_id: L1_surveillance_failure
    step: 2
    source: RB1
    target: retrotransposon_derepression
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "RB1 mRNA and protein decline in late senescent LF1 fibroblasts;
      RBL1 and RBL2 do not change (paralog specificity control). RB1 ChIP
      occupancy at L1 5′ UTR is lost in late senescence. RB1 overexpression in
      senescent cells restores L1 5′ UTR occupancy and suppresses L1 mRNA, IFNA,
      and IFNB1. shRB1 knockdown further enhances them. Single shRB1 alone has
      modest effect in EP cells, indicating redundancy with FOXA1 and TREX1
      surveillance."
    support: "Fig. 2a, 2c, 2d; Extended Data Fig. 4b, 4c, 4g, 4h"
    papers:
      - DeCecco_nature_2019

# FOXA1 gain activates L1 transcription by binding the L1 5′ UTR promoter.
  - chain_id: L1_surveillance_failure
    step: 3
    source: FOXA1
    target: retrotransposon_derepression
    rel: drives
    evidence_strength: perturbation_supported
    context: "FOXA1 mRNA and protein increase in late senescent LF1 fibroblasts.
      FOXA1 binds the central region of the L1 5′ UTR by ChIP-qPCR; FOXA1-
      binding site deletion in the L1 5′ UTR reporter reduces both sense and
      antisense transcription. FOXA1 overexpression increases L1, IFNA, and
      IFNB1; shFOXA1 decreases them. ENCODE ChIP-seq confirms FOXA1 binding at
      L1 5′ UTR in multiple cancer cell lines (YY1 positive control, CEBPB
      negative control)."
    support: "Fig. 2b, 2e; Extended Data Fig. 4d, 4e, 4f, 4g, 4h"
    papers:
      - DeCecco_nature_2019

# TREX1 loss allows cytoplasmic L1 cDNA to accumulate; bidirectional
# perturbation confirms necessity and sufficiency.
  - chain_id: L1_surveillance_failure
    step: 4
    source: TREX1
    target: retrotransposon_derepression
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "TREX1 mRNA and protein decline markedly in late senescent LF1
      fibroblasts. TREX1 overexpression suppresses L1, IFNA, and IFNB1 in
      senescent cells; shTREX1 knockdown enhances them. TREX1 is proposed to
      degrade cytoplasmic L1 cDNA; 3TC blocks cytoplasmic ssDNA accumulation,
      consistent with TREX1 acting on the RT product. Triple intervention
      (shRB1 + shTREX1 + FOXA1-OE) in EP cells induces >20-fold L1 and IFN-I,
      demonstrating all three surveillance mechanisms must be simultaneously
      compromised."
    support: "Fig. 2f, 2g; Extended Data Fig. 4a, 4g, 4h"
    papers:
      - DeCecco_nature_2019

# ─── CHAIN 2: L1 cDNA → cGAS → cGAMP → STING1 → IFN-I → JAK-STAT → cytokines

# L1 reverse transcriptase produces cytoplasmic cDNA (ssDNA/RNA-DNA hybrid)
# that is the proximal trigger for innate immune sensing.
  - chain_id: L1_cDNA_cGAS_STING_IFN_SASP
    step: 1
    source: retrotransposon_derepression
    target: cytoplasmic_retroelement_cDNA
    rel: produces
    evidence_strength: direct_measured
    context: "Cytoplasmic ssDNA puncta colocalize with ORF1 protein in late
      senescent LF1 cells by immunofluorescence. BrdU pulse-labeling (2 weeks)
      shows newly synthesized L1 DNA enriched in the cytoplasm of senescent
      cells; 3TC (7.5-10 uM) completely blocks this synthesis. RNA-DNA hybrids
      (S9.6 antibody) colocalize with ORF1 and are lost after RNase treatment,
      consistent with an RNA-DNA hybrid intermediate of reverse transcription.
      3TC does not affect L1 transcript levels (Extended Data Fig. 5i),
      confirming the trigger is cDNA not RNA. BrdU-pulled-down DNA is enriched
      for L1 sequences spanning the full element (Extended Data Fig. 6d, e).
      Confirmed in LF1, IMR90, WI-38, OIS (HaRasV12), and SIPS (20 Gy gamma
      irradiation) models."
    support: "Fig. 3a, 3b, 3c; Extended Data Fig. 6a, 6b, 6c, 6d, 6e"
    papers:
      - DeCecco_nature_2019

# Cytoplasmic L1 cDNA activates CGAS; CGAS knockdown abolishes
# IFN-I and late SASP downstream.
  - chain_id: L1_cDNA_cGAS_STING_IFN_SASP
    step: 2
    source: cytoplasmic_retroelement_cDNA
    target: CGAS
    rel: activates
    evidence_strength: perturbation_supported
    context: "shCGAS knockdown (two independent shRNAs) in late senescent LF1
      cells significantly reduces IFN-I gene expression (IFNA, IRF7, OAS1) and
      late SASP genes (CCL2, IL6, MMP3). Same result in 3x cells. Direct
      colocalization of cytoplasmic L1 cDNA with CGAS puncta is not shown in
      this paper; CGAS activation is inferred from knockdown necessity. The
      paper explicitly invokes CGAS as the cytosolic DNA sensor for L1 cDNA."
    support: "Extended Data Fig. 5l, 7c, 7d, 7e"
    papers:
      - DeCecco_nature_2019

# CGAS produces cGAMP upon DNA binding (canonical step, explicitly invoked).
  - chain_id: L1_cDNA_cGAS_STING_IFN_SASP
    step: 3
    source: CGAS
    target: cGAMP
    rel: produces
    evidence_strength: canonical_inferred
    context: "cGAMP production by CGAS upon cytosolic DNA binding is the
      canonical mechanism explicitly invoked by this paper to explain STING1
      activation downstream of L1 cDNA. cGAMP is not directly measured here
      (unlike Dou 2017 which uses LC-MS); the step is inferred from CGAS and
      STING1 knockdown phenotypes and the paper's citation of the cGAS-STING
      pathway."
    support: "Main text p.75 ('knockdown of the cytosolic DNA-sensing pathway
      components cGAS or STING'); Extended Data Fig. 5l, 7c"
    papers:
      - DeCecco_nature_2019

# cGAMP activates STING1; STING1 knockdown abolishes IFN-I and late SASP.
  - chain_id: L1_cDNA_cGAS_STING_IFN_SASP
    step: 4
    source: cGAMP
    target: STING1
    rel: activates
    evidence_strength: canonical_inferred
    context: "STING1 activation downstream of CGAS/cGAMP is the canonical
      mechanism invoked. shSTING1 knockdown (two independent shRNAs) in late
      senescent and 3x cells reduces IFN-I (IFNA, IRF7, OAS1) and late SASP
      genes (CCL2, IL6, MMP3), confirming STING1 is required. The
      cGAMP-to-STING1 step is not directly measured here."
    support: "Extended Data Fig. 5l, 7c, 7d, 7e"
    papers:
      - DeCecco_nature_2019

# STING1 drives type_I_IFN; this is a late-senescence phenotype distinct from
# the early SASP.
  - chain_id: L1_cDNA_cGAS_STING_IFN_SASP
    step: 5
    source: STING1
    target: type_I_IFN
    rel: drives
    evidence_strength: perturbation_supported
    context: "STING1 knockdown reduces IFNA, IFNB1, IRF7, and OAS1 in both
      late senescent and 3x cells. RNA-seq GSEA confirms IFN-I gene set is
      significantly upregulated SEN-E to SEN-L but not EP to SEN-E (late-
      specific). 68% of 84 IFN-I pathway genes are significantly upregulated
      in late senescent cells by PCR array. 3TC suppresses IFN-I in RS, OIS,
      and SIPS models. IFNA and IFNB1 are induced 15-25-fold in late senescent
      LF1 cells."
    support: "Fig. 1d, 1e, 2h, 3b, 3e; Extended Data Fig. 3, 5l, 7c, 7d"
    papers:
      - DeCecco_nature_2019

# type_I_IFN signals via JAK-STAT (STAT2 phosphorylation, IRF7 induction).
  - chain_id: L1_cDNA_cGAS_STING_IFN_SASP
    step: 6
    source: type_I_IFN
    target: JAK-STAT
    rel: activates
    evidence_strength: direct_measured
    context: "STAT2 protein and IRF7 protein are induced in late senescent LF1
      cells and are reduced by shL1 (a) and 3TC treatment, as shown by
      immunoblot (Fig. 3b). In 3x cells, shL1 and 3TC similarly reduce STAT2
      and IRF7 protein (Extended Data Fig. 7a). IRF9 nuclear translocation (a
      downstream JAK-STAT readout) is used to validate IFNAR1/2 CRISPR knockout
      efficacy (Extended Data Fig. 5m). OAS1 induction (an ISG) is used as a
      downstream readout throughout."
    support: "Fig. 3b; Extended Data Fig. 5m, 7a"
    papers:
      - DeCecco_nature_2019

# JAK-STAT activation amplifies the late/mature SASP (CCL2, IL6, MMP3)
# but not early SASP (IL1B).
  - chain_id: L1_cDNA_cGAS_STING_IFN_SASP
    step: 7
    source: JAK-STAT
    target: SASP
    rel: drives
    evidence_strength: perturbation_supported
    context: "CRISPR-Cas9 knockout of IFNAR1 and IFNAR2 in replicatively
      senescent and SIPS cells suppresses late SASP markers (CCL2, IL6, MMP3)
      but not early SASP (IL1B). 3TC treatment throughout replicative senescence
      dampens late SASP (CCL2, IL6, MMP3) at 16 weeks without affecting IL1B or
      senescence entry (p21, p16 unchanged). shL1 also reduces IL6 and MMP3 in
      late senescent cells (Extended Data Fig. 6f). Establishes IFN-I to JAK-STAT
      as a specific amplifier of the late/mature SASP."
    support: "Fig. 3d, 3f; Extended Data Fig. 6f, 7b"
    papers:
      - DeCecco_nature_2019

# STING1 upregulates canonical late SASP cytokines directly (via NF-kB,
# canonical_inferred intermediate). IL1B, CCL2, IL6, and MMP3 are explicitly
# named as canonical SASP genes in the paper (Fig. 1e legend, main text p.75).
  - chain_id: L1_cDNA_cGAS_STING_IFN_SASP
    step: 8
    source: STING1
    target: IL6
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "shSTING1 knockdown in late senescent LF1 cells reduces IL6, CCL2,
      and MMP3 mRNA. These are the canonical late SASP cytokines amplified by
      the IFN-I/JAK-STAT axis; IL1B (early SASP) is not affected by STING1
      knockdown or IFNAR1/2 KO, establishing a late-SASP-specific regulatory
      arm. NF-kB activation downstream of STING1 is the canonical mechanism
      invoked but not directly measured here."
    support: "Fig. 3d, 3f; Extended Data Fig. 7e"
    papers:
      - DeCecco_nature_2019

  - chain_id: L1_cDNA_cGAS_STING_IFN_SASP
    step: 9
    source: STING1
    target: CCL2
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "As step 8. CCL2 is suppressed by shSTING1, shCGAS, IFNAR1/2 KO,
      shL1, and 3TC in RS and SIPS models."
    support: "Fig. 3d, 3f; Extended Data Fig. 7e"
    papers:
      - DeCecco_nature_2019

  - chain_id: L1_cDNA_cGAS_STING_IFN_SASP
    step: 10
    source: STING1
    target: MMP3
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "As step 8. MMP3 is suppressed by shSTING1, shCGAS, IFNAR1/2 KO,
      shL1, and 3TC in RS and SIPS models and in aged mouse adipose and liver
      in vivo."
    support: "Fig. 3d, 3f, 4c; Extended Data Fig. 7e, 9a, 9b, 9c"
    papers:
      - DeCecco_nature_2019

# JAK-STAT additionally upregulates the same late SASP cytokines via IFN-I
# signaling — this is the IFN-I-specific amplification arm.
  - chain_id: L1_cDNA_cGAS_STING_IFN_SASP
    step: 11
    source: JAK-STAT
    target: IL6
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "IFNAR1/2 CRISPR KO in replicatively senescent and SIPS cells
      suppresses IL6, CCL2, and MMP3 but not IL1B, establishing JAK-STAT
      (downstream of IFN-I/IFNAR) as a specific amplifier of the late SASP.
      This is a second, IFN-I-dependent regulatory arm on the same cytokines
      that STING1/NF-kB also drives."
    support: "Fig. 3d, 3f; Extended Data Fig. 7b"
    papers:
      - DeCecco_nature_2019

  - chain_id: L1_cDNA_cGAS_STING_IFN_SASP
    step: 12
    source: JAK-STAT
    target: CCL2
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "As step 11."
    support: "Fig. 3d, 3f"
    papers:
      - DeCecco_nature_2019

  - chain_id: L1_cDNA_cGAS_STING_IFN_SASP
    step: 13
    source: JAK-STAT
    target: MMP3
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "As step 11."
    support: "Fig. 3d, 3f"
    papers:
      - DeCecco_nature_2019

# ─── CHAIN 3: In vivo aging — L1 → IFN-I → tissue inflammation ───────────────

# L1 is activated in senescent cells in aged mouse tissues and human skin.
  - chain_id: in_vivo_aging_L1_IFN
    step: 1
    source: cellular_senescence
    target: retrotransposon_derepression
    rel: induces
    evidence_strength: direct_measured
    context: "ORF1+ cells increase with age in mouse skeletal muscle (0.27% at
      5 months to 3.10% at 26 months, males) and liver (1.50% to 5.77% males;
      2.40% to 5.82% females), and colocalize with SA-beta-Gal+ senescent cells
      in aged liver. L1 mRNA increases progressively from 5 to 26 to 29 months
      in white adipose, muscle, and liver in both sexes (Extended Data Fig. 10g).
      In human skin biopsies (Leiden Longevity Study, n=4 subjects, mean age 57),
      10.7% of dermal fibroblasts are p16+; 10.3% of p16+ cells are also ORF1+;
      ORF1 is absent in p16-negative cells (Extended Data Fig. 8f). Irradiation-
      induced senescence (6 Gy at 6 months) shows progressive L1 and IFN-I
      co-induction over 3-6 months post-irradiation in adipose."
    support: "Fig. 4a, 4b, 4d; Extended Data Fig. 8b, 8d, 8f, 8h, 10g"
    papers:
      - DeCecco_nature_2019

# 3TC suppresses IFN-I and SASP in aged mice without reducing senescent cell
# number (senostatic mechanism confirmed by K-9 control).
  - chain_id: in_vivo_aging_L1_IFN
    step: 2
    source: retrotransposon_derepression
    target: type_I_IFN
    rel: drives
    evidence_strength: perturbation_supported
    context: "3TC (2 mg/ml in drinking water, 2 weeks) in 26-month C57BL/6
      mice significantly reduces Ifna, Irf7, and Oas1 in white adipose (male
      and female) and liver. Il6, Mmp3, and Pai1 SASP markers are also reduced.
      L1 mRNA and p16 are not significantly reduced, confirming senostatic (not
      senolytic) mechanism. K-9 (methoxy-3TC, cannot inhibit RT) does not reduce
      IFN-I or SASP in vivo at 10 uM, confirming RT inhibition is required."
    support: "Fig. 4c; Extended Data Fig. 9a, 9b, 9c, 9d"
    papers:
      - DeCecco_nature_2019

# SASP drives macrophage recruitment in aged tissues.
  - chain_id: in_vivo_aging_L1_IFN
    step: 3
    source: SASP
    target: immune_cell_recruitment
    rel: drives
    evidence_strength: perturbation_supported
    context: "3TC treatment of 26-month mice reduces F4/80+ macrophage
      infiltration in white adipose to 5-month levels after 2 weeks. Kidney
      macrophage infiltration is reversed by 6 months of 3TC (20-26 months).
      LMNB1-low (senescent) cells colocalize with IL-6+ (SASP) cells in
      whole-mount white adipose (Extended Data Fig. 10a, c). ORF1+ cells
      colocalize with pSTAT1+ cells, indicating IFN-I paracrine signaling in
      the tissue microenvironment (Extended Data Fig. 10b, c)."
    support: "Fig. 4e; Extended Data Fig. 10a, 10b, 10c, 10d"
    papers:
      - DeCecco_nature_2019

  - chain_id: in_vivo_aging_L1_IFN
    step: 4
    source: immune_cell_recruitment
    target: tissue_inflammation
    rel: drives
    evidence_strength: perturbation_supported
    context: "Macrophage (F4/80+) crown-like structures in white adipose and
      kidney are a direct readout of tissue inflammation in aged mice, reversed
      by 3TC. Glomerulosclerosis and skeletal muscle atrophy are also reversed
      by 6-month 3TC. Adipocyte size and adipogenic gene expression (Acaca,
      Cebpa, Fasn, Srebf1) increase with 3TC, and brown adipose Ucp1 increases,
      indicating functional metabolic improvement. Tissue context: white adipose,
      kidney, skeletal muscle."
    support: "Fig. 4e; Extended Data Fig. 10a, 10b, 10d, 10e, 10f"
    papers:
      - DeCecco_nature_2019

# ─── CHAIN 4: Specificity controls ───────────────────────────────────────────

# RBL1 and RBL2 do not change in senescence — RB1 effect is paralog-specific.
  - chain_id: specificity_controls
    step: 1
    source: cellular_senescence
    target: RBL1
    rel: does_not_correlate
    evidence_strength: direct_measured
    context: "RT-qPCR of RBL1 and RBL2 in EP vs. late senescent LF1 cells
      shows no significant change, in contrast to the strong decline of RB1.
      Establishes that L1 derepression is specific to RB1 and not a general
      RB-family effect."
    support: "Extended Data Fig. 4b"
    papers:
      - DeCecco_nature_2019

# 3TC's RT-inhibitory activity (not any off-target anti-inflammatory activity)
# is required for IFN-I suppression — K-9 specificity control.
# The mechanistic claim: L1 reverse transcriptase activity is required for IFN-I.
  - chain_id: specificity_controls
    step: 2
    source: retrotransposon_derepression
    target: type_I_IFN
    rel: required_for
    evidence_strength: perturbation_supported
    context: "Kamuvudine-9 (K-9, tri-methoxy-3TC) cannot be phosphorylated and
      therefore cannot inhibit reverse transcriptase, but retains intrinsic
      anti-inflammatory activity via P2X7/NLRP3 inhibition. K-9 at 10 uM does
      not suppress IFN-I (IFNA, IRF7, OAS1) in late senescent or 3x cells in
      vitro, nor in aged mice in vivo. At 100 uM, K-9 has some SASP-suppressive
      activity (IL1B, IL6, MMP3) consistent with NLRP3 inhibition, but not
      IFN-I suppression. This confirms that RT inhibition — not NLRP3 suppression
      — is the mechanism by which 3TC suppresses IFN-I. The RT activity of L1
      is required for IFN-I induction."
    support: "Extended Data Fig. 7f, 7g; Extended Data Fig. 9d"
    papers:
      - DeCecco_nature_2019

# IFN-I signaling does not drive early SASP (IL1B) — IFN-I is a late SASP
# amplifier only.
  - chain_id: specificity_controls
    step: 3
    source: type_I_IFN
    target: IL1B
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "CRISPR-Cas9 knockout of IFNAR1 and IFNAR2 in replicatively
      senescent and SIPS cells suppresses late SASP (CCL2, IL6, MMP3) but
      leaves IL1B unchanged. 3TC treatment throughout replicative senescence
      does not affect IL1B induction (Fig. 3f). Establishes that IFN-I
      specifically amplifies the late/mature SASP and is not required for the
      early IL-1B-driven SASP."
    support: "Fig. 3d, 3f"
    papers:
      - DeCecco_nature_2019

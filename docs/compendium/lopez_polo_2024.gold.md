
paper:

  LopezPolo_natcomms_2024:
    cite: "López-Polo V, Maus M, Zacharioudakis E, Lafarga M, Stephan-Otto Attolini C, Marques FDM, Kovatcheva M, Gavathiotis E, Serrano M. Release of mitochondrial dsRNA into the cytosol is a key driver of the inflammatory phenotype of senescent cells. Nat Commun. 2024;15:7378."
    url: "https://doi.org/10.1038/s41467-024-51363-0"
    summary: "Senescent cells accumulate and release mitochondrial dsRNA into the cytosol (POLRMT supplies the substrate; PNPT1 and ADAR brakes are lost; BAX/BAK-dependent pores permit escape). Cytosolic mt-dsRNA engages RIG-I (DDX58) and MDA5 (IFIH1), which activate MAVS, and MAVS drives type-I IFN and the SASP while CDKN1A senescence is preserved. A parallel mtDNA/cGAS-STING branch contributes but is secondary. MFN1 promotes and MFN2 suppresses the axis; LGP2 (DHX58) and PKR (EIF2AK2) are specificity negatives."
    nucleic_acid_sensors:
      - DDX58
      - IFIH1
      - DHX58
      - EIF2AK2
      - CGAS
      - STING1
      - MAVS
    genes:
      - POLRMT
      - PNPT1
      - ADAR
      - DDX58
      - IFIH1
      - DHX58
      - EIF2AK2
      - MAVS
      - CGAS
      - STING1
      - BAX
      - BAK1
      - MFN1
      - MFN2
      - IRF3
      - IFNA1
      - IFNB1
      - IL1A
      - IL1B
      - IL6
      - CXCL8
      - CXCL10
      - CCL2
      - SERPINE1
      - B2M
      - CDKN1A
      - CDKN2A
    pathways:
      - RIG-I/MDA5-MAVS
      - cGAS-STING
      - type_I_IFN
      - NF-kB
      - SASP
    cell_types:
      - IMR90
      - SK-MEL-103
      - A549
      - senescent_fibroblasts
      - melanoma_cells
      - lung_adenocarcinoma_cells
      - MEF
    mechanisms:
      - cellular_senescence
      - cytoplasmic_mt_dsRNA
      - cytoplasmic_mtDNA
      - BAX/BAK_pore
      - cytosolic_RNA_sensing
      - cytosolic_DNA_sensing
      - mt_dsRNA_release
      - mtDNA_release
      - MAVS_aggregation
      - tissue_inflammation
      - fibrosis
      - DNA_damage
    model_systems:
      - human_in_vitro
      - mouse_in_vitro
      - mouse_in_vivo
      - human_cohort
    evidence_type:
      - siRNA_knockdown
      - genetic_KO
      - overexpression
      - pharmacological_inhibition
      - bulk_RNA_seq
      - RT_qPCR
      - immunoblot
      - immunofluorescence
      - IHC
      - cytokine_array
      - multiplex_cytokine_assay
    notes: >
      1. Tissue/organ: cultured IMR-90 fibroblasts, SK-MEL-103 melanoma, A549
      lung adenocarcinoma, MEFs, mouse xenografts, infarcted heart, aged mouse
      brain/liver/kidney, and human age-expression datasets (Leiden Longevity
      Study skin, n=4, mean age 57).
      2. Species: human and mouse.
      3. Age range or comparison: proliferating vs senescent cells; young vs old
      mouse tissues; human tissue expression across age.
      4. Sex-specific effects: not a central analysed variable.
      5. Disease context: cellular senescence, fibrosis/myocardial infarction,
      tissue ageing, systemic senescence-associated inflammation.
      Mechanistic spine (all core): senescence raises cytosolic mt-dsRNA;
      BAX/BAK pores release it (DKO loses it); mt-dsRNA activates cytosolic RNA
      sensing; sensing proceeds via RIG-I (DDX58) and MDA5 (IFIH1); each signals
      through MAVS; MAVS drives type-I IFN and the SASP (CDKN1A preserved). The
      two specificity negatives (LGP2/DHX58 unchanged; PKR/EIF2AK2 does not
      drive SASP) are core attribution.
      6. Equivalence, parallel branch, and forbidden: sensor upregulation
      (DDX58, IFIH1) is one expression observation (sensor_induction); RIG-I and
      MDA5 sensing are equivalent (dsrna_sensor); DDX58->MAVS and IFIH1->MAVS are
      the same continuity claim (sensor_to_mavs). POLRMT/PNPT1/ADAR/MFN1/MFN2 are
      supporting modulators. The mtDNA/cGAS-STING branch is retained as
      SUPPORTING, deliberately, so it does not displace the mt-dsRNA/MAVS spine.
      Forbidden shortcuts: MAVS collapsed to a single marker cytokine (CXCL10) as
      if it were the mechanism; senescence 'drives SASP' erasing the sensing axis.
    relevance_to_project: >
      Anchors the RNA-sensing (mt-dsRNA/RIG-I/MDA5-MAVS) arm of the NASP spine,
      complementary to the DNA-sensing arms of Dou (CCF) and De Cecco (L1 cDNA).
      In atlas or perturbation data, treat a MAVS-driven IFN/SASP signature with
      RIG-I/MDA5 induction and preserved CDKN1A as the López-Polo readout, use the
      LGP2/PKR negatives and the supporting-only cGAS-STING branch to attribute
      the signal to the mt-dsRNA/MAVS arm, and treat PNPT1/ADAR as restriction
      brakes and MFN1/MFN2 as opposing tuners for perturbation design.

edges:

# Core: senescence raises cytosolic mt-dsRNA (net).
  - chain_id: mtdsrna_mavs_ifn_sasp
    step: 1
    source: cellular_senescence
    target: cytoplasmic_mt_dsRNA
    rel: induces
    evidence_strength: direct_measured
    context: "Senescent IMR90, SK-MEL-103 and A549 accumulate cytosolic
              mitochondrial dsRNA (J2 staining, mt-dsRNA qPCR), the net result of
              increased supply and lost brakes. The ligand-defining observation of
              the paper."
    support: "Fig. 1a-d, 5a-e; Suppl. 2, 9"
    tier: core
    papers:
      - LopezPolo_natcomms_2024

# Supporting: POLRMT supplies the mt-RNA substrate (IMT1).
  - chain_id: mtdsrna_supply_brakes
    step: 1
    source: POLRMT
    target: cytoplasmic_mt_dsRNA
    rel: produces
    evidence_strength: perturbation_supported
    context: "POLRMT (mitochondrial RNA polymerase) supplies the mt-RNA substrate;
              its inhibition by IMT1 lowers mt-dsRNA. A supply-side modulator of the
              ligand."
    support: "Fig. 1g, 1h; Suppl. 3a-e"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Supporting: senescence downregulates the PNPT1 brake.
  - chain_id: mtdsrna_supply_brakes
    step: 2
    source: cellular_senescence
    target: PNPT1
    rel: downregulates
    evidence_strength: direct_measured
    context: "PNPT1 (which degrades mt-dsRNA) falls in senescence, removing a brake
              on mt-dsRNA accumulation."
    support: "Fig. 1f; Suppl. 1a"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Supporting: PNPT1 restrains mt-dsRNA.
  - chain_id: mtdsrna_supply_brakes
    step: 3
    source: PNPT1
    target: cytoplasmic_mt_dsRNA
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "PNPT1 knockdown raises mt-dsRNA, confirming PNPT1 restrains the
              cytosolic mt-dsRNA pool."
    support: "Suppl. 1a; Fig. 1f"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Supporting: senescence downregulates the ADAR brake.
  - chain_id: mtdsrna_supply_brakes
    step: 4
    source: cellular_senescence
    target: ADAR
    rel: downregulates
    evidence_strength: direct_measured
    context: "ADAR (which edits dsRNA to limit its immunogenicity) falls in
              senescence, removing a second brake."
    support: "Fig. 2a-c; Suppl. 4a-g"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Supporting: ADAR restrains dsRNA immunogenicity.
  - chain_id: mtdsrna_supply_brakes
    step: 5
    source: ADAR
    target: cytosolic_RNA_sensing
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "ADAR editing limits activation of cytosolic RNA sensing; ADAR loss
              increases sensing. A brake acting at the sensing step."
    support: "Fig. 2d; Suppl. 4d-g"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Supporting equivalence sensor_induction: senescence upregulates RIG-I (DDX58).
  - chain_id: sensor_induction
    step: 1
    source: cellular_senescence
    target: DDX58
    rel: upregulates
    evidence_strength: direct_measured
    context: "RIG-I (DDX58) transcript/protein rises in senescence. One
              expression-level observation (with IFIH1) that the dsRNA sensors are
              induced."
    support: "Fig. 2e; 5g"
    tier: supporting
    equiv_group: sensor_induction
    papers:
      - LopezPolo_natcomms_2024

# Supporting equivalence sensor_induction: senescence upregulates MDA5 (IFIH1).
  - chain_id: sensor_induction
    step: 2
    source: cellular_senescence
    target: IFIH1
    rel: upregulates
    evidence_strength: direct_measured
    context: "MDA5 (IFIH1) transcript/protein rises in senescence, equivalent to
              the DDX58 induction as evidence the dsRNA sensors are upregulated."
    support: "Fig. 2e; 5f, 5g"
    tier: supporting
    equiv_group: sensor_induction
    papers:
      - LopezPolo_natcomms_2024

# Core: BAX/BAK pore releases mt-dsRNA (DKO loses it).
  - chain_id: mtdsrna_mavs_ifn_sasp
    step: 2
    source: BAX/BAK_pore
    target: cytoplasmic_mt_dsRNA
    rel: forms_pore_for
    evidence_strength: perturbation_supported
    context: "BAX/BAK double knockout abolishes cytosolic mt-dsRNA release, showing
              BAX/BAK-dependent pores are the route of escape. The strongest
              perturbation and the mechanism of cytosolic access, so core."
    support: "Fig. 2f, 2h; Suppl. 4j"
    tier: core
    papers:
      - LopezPolo_natcomms_2024

# Supporting: BAX/BAK pore also releases mtDNA (parallel branch feeder).
  - chain_id: parallel_mtdna_cgas
    step: 1
    source: BAX/BAK_pore
    target: cytoplasmic_mtDNA
    rel: forms_pore_for
    evidence_strength: perturbation_supported
    context: "The same BAX/BAK pores also release mtDNA, feeding the parallel
              cGAS-STING branch. Supporting because the resolved spine is the
              mt-dsRNA/MAVS arm."
    support: "Fig. 2f, 2h; Suppl. 4j; Discussion"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Core: mt-dsRNA engages cytosolic RNA sensing.
  - chain_id: mtdsrna_mavs_ifn_sasp
    step: 3
    source: cytoplasmic_mt_dsRNA
    target: cytosolic_RNA_sensing
    rel: activates
    evidence_strength: direct_measured
    context: "Cytosolic mt-dsRNA activates cytosolic RNA sensing; mt-dsRNA
              manipulation tracks sensing activation. The ligand-to-sensing step."
    support: "Fig. 1c, 1d, 1g-i; 2f-h; 6"
    tier: core
    papers:
      - LopezPolo_natcomms_2024

# Core equivalence dsrna_sensor: sensing proceeds via RIG-I (DDX58).
  - chain_id: mtdsrna_mavs_ifn_sasp
    step: 4
    source: cytosolic_RNA_sensing
    target: DDX58
    rel: activates
    evidence_strength: perturbation_supported
    context: "Cytosolic RNA sensing proceeds via RIG-I (DDX58); combined sensor
              depletion reduces the output. The paper does not separate RIG-I and
              MDA5 ligand specificity, so recovering either sensor edge satisfies
              the dsRNA-sensor step."
    support: "Fig. 2e-g; 6"
    tier: core
    equiv_group: dsrna_sensor
    papers:
      - LopezPolo_natcomms_2024

# Core equivalence dsrna_sensor: sensing proceeds via MDA5 (IFIH1).
  - chain_id: mtdsrna_mavs_ifn_sasp
    step: 5
    source: cytosolic_RNA_sensing
    target: IFIH1
    rel: activates
    evidence_strength: perturbation_supported
    context: "Cytosolic RNA sensing proceeds via MDA5 (IFIH1), equivalent to the
              RIG-I edge; the two sensors are tested by combined depletion."
    support: "Fig. 2e-g; 6"
    tier: core
    equiv_group: dsrna_sensor
    papers:
      - LopezPolo_natcomms_2024

# Core equivalence sensor_to_mavs: RIG-I signals through MAVS.
  - chain_id: mtdsrna_mavs_ifn_sasp
    step: 6
    source: DDX58
    target: MAVS
    rel: activates
    evidence_strength: perturbation_supported
    context: "RIG-I (DDX58) signals through the adaptor MAVS. DDX58->MAVS and
              IFIH1->MAVS are the same canonical continuity claim (the dsRNA sensor
              signals through MAVS); satisfied once."
    support: "Fig. 2e-g; 3a-i"
    tier: core
    equiv_group: sensor_to_mavs
    papers:
      - LopezPolo_natcomms_2024

# Core equivalence sensor_to_mavs: MDA5 signals through MAVS.
  - chain_id: mtdsrna_mavs_ifn_sasp
    step: 7
    source: IFIH1
    target: MAVS
    rel: activates
    evidence_strength: perturbation_supported
    context: "MDA5 (IFIH1) signals through MAVS, equivalent to the RIG-I->MAVS
              continuity claim."
    support: "Fig. 2e-g; 3a-i"
    tier: core
    equiv_group: sensor_to_mavs
    papers:
      - LopezPolo_natcomms_2024

# Core: MAVS drives type-I IFN.
  - chain_id: mtdsrna_mavs_ifn_sasp
    step: 8
    source: MAVS
    target: type_I_IFN
    rel: drives
    evidence_strength: perturbation_supported
    context: "MAVS knockdown suppresses the type-I IFN response, placing MAVS as
              the adaptor that drives IFN-I from mt-dsRNA sensing."
    support: "Fig. 3a-i; Suppl. 5b"
    tier: core
    papers:
      - LopezPolo_natcomms_2024

# Core: MAVS drives SASP (CDKN1A preserved).
  - chain_id: mtdsrna_mavs_ifn_sasp
    step: 9
    source: MAVS
    target: SASP
    rel: drives
    evidence_strength: perturbation_supported
    context: "MAVS knockdown reduces the SASP while CDKN1A/senescence arrest is
              preserved, showing MAVS drives the inflammatory output specifically.
              Core output of the spine."
    support: "Fig. 3g-i; Suppl. 5b"
    tier: core
    papers:
      - LopezPolo_natcomms_2024

# Supporting parallel branch: mtDNA activates CGAS.
  - chain_id: parallel_mtdna_cgas
    step: 2
    source: cytoplasmic_mtDNA
    target: CGAS
    rel: activates
    evidence_strength: perturbation_supported
    context: "Released mtDNA activates CGAS in the parallel branch; combined
              CGAS/STING depletion reduces cytokines. Supporting, not core, so it
              does not displace the mt-dsRNA/MAVS spine."
    support: "Fig. 2f; Suppl. 4h; Introduction/Discussion"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Supporting parallel branch: CGAS activates STING1.
  - chain_id: parallel_mtdna_cgas
    step: 3
    source: CGAS
    target: STING1
    rel: activates
    evidence_strength: canonical_inferred
    context: "CGAS activates STING1 in the parallel DNA branch (canonical wiring),
              contributing to but not defining the inflammatory output."
    support: "Fig. 2f; Suppl. 4h"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Supporting parallel branch: STING1 drives SASP (parallel contribution).
  - chain_id: parallel_mtdna_cgas
    step: 4
    source: STING1
    target: SASP
    rel: drives
    evidence_strength: perturbation_supported
    context: "STING1 depletion partly reduces the SASP, the parallel-branch
              contribution alongside the primary MAVS output. Supporting."
    support: "Fig. 2f; Suppl. 4h"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Supporting modulator: MFN1 promotes mt-dsRNA.
  - chain_id: mitofusin_tuning
    step: 1
    source: MFN1
    target: cytoplasmic_mt_dsRNA
    rel: drives
    evidence_strength: perturbation_supported
    context: "MFN1 overexpression raises, and MFN1 loss lowers, cytosolic mt-dsRNA.
              A positive tuner of the axis."
    support: "Fig. 4e; Suppl. 7a-c"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Supporting modulator: MFN1 promotes MAVS aggregation.
  - chain_id: mitofusin_tuning
    step: 2
    source: MFN1
    target: MAVS
    rel: drives
    evidence_strength: perturbation_supported
    context: "MFN1 promotes MAVS aggregation/activation, amplifying signalling.
              Supporting modulator edge."
    support: "Fig. 4f; Suppl. 7d-f"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Supporting modulator: MFN1 promotes SASP.
  - chain_id: mitofusin_tuning
    step: 3
    source: MFN1
    target: SASP
    rel: drives
    evidence_strength: perturbation_supported
    context: "MFN1 gain increases the SASP, consistent with its promotion of the
              mt-dsRNA/MAVS axis."
    support: "Fig. 4c, 4d, 4h; Suppl. 6i, 6j, 8c-f"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Supporting modulator: MFN2 suppresses mt-dsRNA.
  - chain_id: mitofusin_tuning
    step: 4
    source: MFN2
    target: cytoplasmic_mt_dsRNA
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "MFN2, opposite to MFN1, suppresses cytosolic mt-dsRNA. A negative
              tuner of the axis."
    support: "Fig. 4e; Suppl. 7a-c"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Supporting modulator: MFN2 suppresses MAVS.
  - chain_id: mitofusin_tuning
    step: 5
    source: MFN2
    target: MAVS
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "MFN2 suppresses MAVS aggregation/activation, opposing MFN1."
    support: "Fig. 4f; Suppl. 7a-f"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Supporting modulator: MFN2 suppresses SASP.
  - chain_id: mitofusin_tuning
    step: 6
    source: MFN2
    target: SASP
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "MFN2 gain lowers the SASP, consistent with its suppression of the
              mt-dsRNA/MAVS axis."
    support: "Fig. 4d; Suppl. 6i, 6j, 7a-f"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Supporting: POLRMT required for SASP in vivo (IMT1).
  - chain_id: mtdsrna_supply_brakes
    step: 6
    source: POLRMT
    target: SASP
    rel: required_for
    evidence_strength: perturbation_supported
    context: "POLRMT inhibition (IMT1) reduces the SASP in vivo, linking the
              mt-RNA supply step to the inflammatory output. Supporting functional
              edge."
    support: "Fig. 5i; Methods"
    tier: supporting
    papers:
      - LopezPolo_natcomms_2024

# Core negative: LGP2 (DHX58) unchanged (sensor specificity).
  - chain_id: sensor_specificity
    step: 1
    source: cellular_senescence
    target: DHX58
    rel: does_not_drive
    evidence_strength: direct_measured
    context: "LGP2 (DHX58) is unchanged in senescence, whereas RIG-I and MDA5 are
              induced, an attribution that the responding dsRNA sensors are RIG-I/
              MDA5 and not LGP2. Core specificity."
    support: "Fig. 2e"
    tier: core
    papers:
      - LopezPolo_natcomms_2024

# Core negative: PKR (EIF2AK2) does NOT drive SASP (specificity).
  - chain_id: sensor_specificity
    step: 2
    source: EIF2AK2
    target: SASP
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "PKR (EIF2AK2) depletion does not reduce the SASP, excluding the other
              cytosolic dsRNA sensor from the output and reinforcing the RIG-I/MDA5
              -> MAVS attribution. Core specificity."
    support: "Fig. 2e; Suppl. 4i"
    tier: core
    papers:
      - LopezPolo_natcomms_2024

# FORBIDDEN SHORTCUT F1: MAVS collapsed to a single marker cytokine (CXCL10).
  - chain_id: forbidden_shortcut
    step: 1
    source: MAVS
    target: CXCL10
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "ANTI-EDGE. MAVS drives the SASP program; naming MAVS as the direct
              regulator of one marker cytokine (CXCL10) collapses the program to a
              single output as if it were the mechanism. The exact anti-pattern the
              curator flagged in the draft (marker-level MAVS -> CXCL10/CCL2/B2M
              edges)."
    support: "n/a (anti-edge; see core step 9, MAVS -> SASP)"
    tier: core
    status: forbidden_shortcut
    papers:
      - LopezPolo_natcomms_2024

# FORBIDDEN SHORTCUT F2: senescence "drives SASP" erasing the sensing axis.
  - chain_id: forbidden_shortcut
    step: 2
    source: cellular_senescence
    target: SASP
    rel: drives
    evidence_strength: perturbation_supported
    context: "ANTI-EDGE. Senescence does produce the SASP, but asserting
              'senescence drives SASP' directly erases the mt-dsRNA -> RIG-I/MDA5 ->
              MAVS sensing axis that is the paper's contribution. The generic
              collapse the gold must penalize."
    support: "n/a (anti-edge; see core steps 1-9)"
    tier: core
    status: forbidden_shortcut
    papers:
      - LopezPolo_natcomms_2024

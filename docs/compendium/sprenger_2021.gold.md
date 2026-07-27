
paper:

  Sprenger_natmetab_2021:
    cite: "Sprenger HG, MacVicar T, Bahat A, et al. Cellular pyrimidine imbalance triggers mitochondrial DNA-dependent innate immunity. Nat Metab. 2021;3(5):636-650."
    url: "https://doi.org/10.1038/s42255-021-00385-9"
    summary: "Loss of the mitochondrial i-AAA protease YME1L stabilizes the pyrimidine nucleotide carrier SLC25A33 and, together with impaired cytosolic de novo pyrimidine synthesis, produces a cellular pyrimidine imbalance. This drives accumulation and VDAC-dependent release of mitochondrial DNA (mtDNA) into the cytosol, which activates the cGAS-STING-TBK1 pathway and interferon-stimulated gene (ISG) expression. SLC25A33 is both necessary and sufficient for the mtDNA-dependent ISG response; rebalancing pyrimidine pools (pyrimidine nucleoside supplementation or ASS1 knockdown) suppresses mtDNA release and inflammation. The response is specific to cytosolic mtDNA sensing and independent of mitochondrial fragmentation, BAX/BAK apoptotic pores, nuclear DNA damage, and RNA sensors."
    nucleic_acid_sensors:
      - CGAS
      - STING1
    genes:
      - YME1L1
      - SLC25A33
      - CGAS
      - STING1
      - TBK1
      - TREX1
      - ASS1
      - CMPK2
      - NME4
      - VDAC1
      - TFAM
      - ISG15
      - USP18
      - IFI44
      - MX1
      - IFNB1
    pathways:
      - cGAS-STING
      - type_I_IFN
    cell_types:
      - mouse_embryonic_fibroblasts
      - HeLa
      - retina
    mechanisms:
      - mtDNA_release
      - cytosolic_dsDNA
      - pyrimidine_metabolism
      - nucleotide_transport
      - VDAC_pore
      - protein_stabilization
    model_systems:
      - mouse_in_vitro
      - human_in_vitro
      - mouse_in_vivo
      - mouse_genetic_model
    evidence_type:
      - genetic_KO
      - RNAi_knockdown
      - overexpression
      - RT_qPCR
      - immunoblot
      - ELISA
      - metabolomics
      - stable_isotope_tracing
      - cell_fractionation
      - proteomics
    notes: >
      1. Tissue/organ: mouse embryonic fibroblasts (MEFs, primary and
      immortalized) and HeLa cells in vitro; mouse retina (neural YME1L-KO,
      "NYKO") in vivo.
      2. Species: mouse and human.
      3. Age range or comparison: not an aging study; comparisons are Yme1l
      wild-type vs knockout/knockdown, plus SLC25A33 overexpression and
      pyrimidine/ASS1 rescue.
      4. Sex-specific effects: not addressed.
      5. Disease context: mitochondrial dysfunction and sterile
      mtDNA-driven interferon inflammation; connects metabolic imbalance to
      cGAS-STING innate immunity.
      Spine: YME1L loss stabilizes SLC25A33 (a YME1L proteolytic substrate);
      SLC25A33-mediated pyrimidine nucleotide transport supports mtDNA
      accumulation; mtDNA is released to the cytosol through VDAC pores;
      cytosolic mtDNA activates cGAS; cGAS-cGAMP activates STING; STING
      activates TBK1; TBK1 drives ISG/type-I-IFN expression. Metabolic layer:
      YME1L supports glutaminolysis and cytosolic de novo pyrimidine synthesis,
      so its loss depletes pyrimidines; ASS1 upregulation diverts aspartate to
      the urea cycle worsening pyrimidine deficiency; supplying pyrimidine
      nucleosides (cytidine/thymidine/uridine) or knocking down ASS1 rebalances
      pyrimidines and abolishes mtDNA release and ISGs. Key negatives: the ISG
      response is independent of mitochondrial fragmentation (DRP1 depletion
      does not blunt it), of BAX/BAK apoptotic mtDNA herniation (persists in
      Bax-/-Bak-/-), of nuclear DNA / TREX1 (TREX1 knockdown boosts it), of a
      nuclear DNA damage response (no CHK1 phosphorylation), and of RNA sensors
      (MDA5/RIG-I/MAVS knockdown does not blunt it); ddC/EtBr mtDNA depletion
      abolishes it. A33 = SLC25A33; NYKO = neural Yme1l knockout.
    relevance_to_project: >
      A metabolic-trigger case on the canonical cGAS-STING spine: the sensed
      ligand is endogenous mtDNA released by a pyrimidine-imbalance mechanism,
      not a pathogen. It is a calibration case for (a) representing an upstream
      metabolic/transport cause (YME1L->SLC25A33->mtDNA) without shortcutting
      to "YME1L loss activates cGAS", (b) encoding a rescue/reversal arm
      (pyrimidine supplementation, ASS1 knockdown) as evidence the trigger is
      metabolic, and (c) recording strong specificity negatives that exclude
      fragmentation, apoptosis, nuclear DNA, and RNA sensing. In atlas data,
      elevated cGAS-STING/ISG output co-occurring with mitochondrial-stress or
      pyrimidine-pathway shifts nominates a cell-intrinsic mtDNA-driven
      interferon state for validation.

edges:

# YME1L proteolysis limits SLC25A33; its loss stabilizes SLC25A33.
  - chain_id: yme1l_mtdna_sting
    step: 1
    source: YME1L1
    target: SLC25A33
    rel: inhibits
    evidence_strength: direct_measured
    context: "SLC25A33 accumulates in Yme1l-/- cells; cycloheximide-chase shows
              increased SLC25A33 protein stability in Yme1l-/- MEFs,
              identifying it as a YME1L proteolytic substrate. YME1L thus
              negatively regulates SLC25A33 abundance."
    support: "Fig. 3a, 3b; Extended Data Fig. 4a"
    tier: core
    papers:
      - Sprenger_natmetab_2021

# SLC25A33 (pyrimidine carrier) is required for and drives mtDNA accumulation.
  - chain_id: yme1l_mtdna_sting
    step: 2
    source: SLC25A33
    target: mtDNA_release
    rel: drives
    evidence_strength: perturbation_supported
    context: "SLC25A33 knockdown or deletion lowers total and cytosolic mtDNA
              in Yme1l-/- cells, and SLC25A33 overexpression in HeLa raises
              total and cytosolic mtDNA. SLC25A33 mediates pyrimidine transport
              linked to mtDNA maintenance; it is necessary and sufficient for
              mtDNA accumulation/release driving the response."
    support: "Fig. 3c-i; Fig. 4a-c"
    tier: core
    papers:
      - Sprenger_natmetab_2021

# mtDNA is released to the cytosol through VDAC pores.
  - chain_id: yme1l_mtdna_sting
    step: 3
    source: mtDNA_release
    target: cytosolic_dsDNA
    rel: produces
    evidence_strength: perturbation_supported
    context: "Cell fractionation shows mtDNA accumulates in cytosolic fractions
              of YME1L-deficient MEFs and HeLa cells. The VDAC oligomerization
              inhibitor VBIT-4 impairs ISG expression in Yme1l-/- and Tfam+/-
              cells, indicating mtDNA egress occurs through VDAC pores; ddC/EtBr
              mtDNA depletion abolishes the response."
    support: "Fig. 2b, 2c, 2e, 2f; Extended Data Fig. 2b-h"
    tier: core
    papers:
      - Sprenger_natmetab_2021

# Cytosolic mtDNA activates cGAS.
  - chain_id: yme1l_mtdna_sting
    step: 4
    source: cytosolic_dsDNA
    target: CGAS
    rel: binds_recruits
    evidence_strength: perturbation_supported
    context: "ISG expression in Yme1l-/- cells depends on cGAS (siRNA) and on
              cytosolic dsDNA (TREX1 knockdown boosts it), and mtDNA depletion
              abolishes it, demonstrating mtDNA-dependent activation of cGAS.
              SLC25A33-overexpression ISGs are likewise cGAS-dependent."
    support: "Fig. 1d, 1h; Fig. 4f; Extended Data Fig. 1f"
    tier: core
    papers:
      - Sprenger_natmetab_2021

# cGAS produces cGAMP (canonical second-messenger step).
  - chain_id: yme1l_mtdna_sting
    step: 5
    source: CGAS
    target: cGAMP
    rel: produces
    evidence_strength: canonical_inferred
    context: "cGAS synthesizes the second messenger cGAMP on dsDNA binding, the
              canonical step linking mtDNA sensing to STING; inferred from the
              demonstrated cGAS- and STING-dependence rather than direct cGAMP
              measurement in this paper."
    support: "canonical (see cGAS/STING dependence, Fig. 1d, 4f)"
    tier: core
    papers:
      - Sprenger_natmetab_2021

# cGAMP activates STING.
  - chain_id: yme1l_mtdna_sting
    step: 6
    source: cGAMP
    target: STING1
    rel: activates
    evidence_strength: perturbation_supported
    context: "ISG expression in Yme1l-/- and in SLC25A33-overexpressing cells is
              STING-dependent (Sting siRNA), placing STING downstream of cGAS on
              the mtDNA-sensing spine."
    support: "Fig. 1d; Fig. 4f"
    tier: core
    papers:
      - Sprenger_natmetab_2021

# STING activates TBK1.
  - chain_id: yme1l_mtdna_sting
    step: 7
    source: STING1
    target: TBK1
    rel: activates
    evidence_strength: perturbation_supported
    context: "The TBK1 inhibitor BX795 suppresses ISG expression in Yme1l-/-
              cells, and the authors assign the response to the
              cGAS-STING-TBK1 pathway."
    support: "Fig. 1g"
    tier: core
    papers:
      - Sprenger_natmetab_2021

# TBK1 drives ISG / type-I IFN expression.
  - chain_id: yme1l_mtdna_sting
    step: 8
    source: TBK1
    target: type_I_IFN
    rel: drives
    evidence_strength: direct_measured
    context: "Loss of YME1L induces a broad ISG signature (RNA-Seq/proteomics;
              Isg15, Usp18, Ifi44, Mx1) and IFN-beta secretion (ELISA); TBK1
              inhibition abolishes it. The signature overlaps mtDNA-stress ISGs
              seen in Tfam+/- cells."
    support: "Fig. 1a-c, 1e, 1g; Fig. 2a"
    tier: core
    papers:
      - Sprenger_natmetab_2021

# METABOLIC LAYER: YME1L loss depletes cellular pyrimidines.
  - chain_id: pyrimidine_imbalance
    step: 1
    source: YME1L1
    target: pyrimidine_metabolism
    rel: required_for
    evidence_strength: direct_measured
    context: "Quantitative metabolomics shows broad nucleotide depletion,
              predominantly pyrimidines, in Yme1l-/- cells and mitochondria;
              13C5,15N2-glutamine tracing shows reduced labelling of pyrimidine
              and purine nucleotides and perturbed glutaminolysis, so YME1L is
              required for efficient de novo pyrimidine synthesis."
    support: "Fig. 5a-d; Extended Data Fig. 6a-c"
    tier: supporting
    papers:
      - Sprenger_natmetab_2021

# METABOLIC LAYER: pyrimidine imbalance drives the mtDNA-dependent ISG response.
  - chain_id: pyrimidine_imbalance
    step: 2
    source: pyrimidine_metabolism
    target: type_I_IFN
    rel: drives
    evidence_strength: perturbation_supported
    context: "Supplying pyrimidine nucleosides (cytidine/thymidine/uridine)
              reduces cytosolic mtDNA and ISG expression in Yme1l-/- cells, and
              ASS1 knockdown (which raises pyrimidine pools by sparing
              aspartate) abolishes ISG expression. Thus the pyrimidine imbalance
              is the metabolic trigger of the mtDNA-dependent response."
    support: "Fig. 6a-e"
    tier: supporting
    papers:
      - Sprenger_natmetab_2021

# NEGATIVE: response is independent of mitochondrial fragmentation (DRP1).
  - chain_id: mechanism_specificity
    step: 1
    source: mitochondrial_fragmentation
    target: type_I_IFN
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "DRP1 depletion restores tubular mitochondria in Yme1l-/- cells yet
              ISG expression increases further, showing ISG stimulation is
              independent of mitochondrial fragmentation."
    support: "Extended Data Fig. 3a"
    tier: supporting
    equiv_group: excluded_triggers
    papers:
      - Sprenger_natmetab_2021

# NEGATIVE: response is independent of BAX/BAK apoptotic mtDNA release.
  - chain_id: mechanism_specificity
    step: 2
    source: BAX_BAK_pore
    target: type_I_IFN
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "YME1L depletion still boosts ISG expression in Bax-/-Bak-/- MEFs,
              and no cytosolic nucleoid accumulation is seen by
              immunocytochemistry, excluding the apoptotic BAX/BAK inner-membrane
              herniation route of mtDNA release."
    support: "Fig. 2d; Extended Data Fig. 3b"
    tier: supporting
    equiv_group: excluded_triggers
    papers:
      - Sprenger_natmetab_2021

# NEGATIVE: response is independent of RNA sensors (MDA5/RIG-I/MAVS).
  - chain_id: mechanism_specificity
    step: 3
    source: RNA_sensing
    target: type_I_IFN
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "Knockdown of the cytosolic RNA receptors MDA5 and RIG-I or of MAVS
              does not blunt ISG expression in Yme1l-/- cells, whereas cGAS/STING
              knockdown does, establishing a dsDNA- not RNA-driven response."
    support: "Extended Data Fig. 1g, 1h"
    tier: supporting
    equiv_group: excluded_triggers
    papers:
      - Sprenger_natmetab_2021

# FORBIDDEN SHORTCUT: YME1L "activates cGAS" skipping SLC25A33/mtDNA.
  - chain_id: forbidden_shortcut
    step: 1
    source: YME1L1
    target: CGAS
    rel: activates
    evidence_strength: perturbation_supported
    context: "ANTI-EDGE. YME1L loss does raise cGAS-dependent ISGs, but naming
              YME1L as a cGAS activator collapses the mechanism: YME1L loss
              stabilizes SLC25A33 and, with pyrimidine imbalance, drives mtDNA
              accumulation and VDAC-dependent cytosolic release, and it is that
              mtDNA that activates cGAS. A draft emitting this single edge has
              taken the forbidden shortcut."
    support: "n/a (anti-edge; see core steps 1-4)"
    tier: core
    status: forbidden_shortcut
    papers:
      - Sprenger_natmetab_2021

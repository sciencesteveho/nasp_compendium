paper:

  LopezPolo_natcomms_2024:
    cite: "López-Polo V, Maus M, Zacharioudakis E, Lafarga M, Stephan-Otto Attolini C, Marques FDM, Kovatcheva M, Gavathiotis E, Serrano M. Release of mitochondrial dsRNA into the cytosol is a key driver of the inflammatory phenotype of senescent cells. Nat Commun. 2024;15:7378."
    url: "https://doi.org/10.1038/s41467-024-51363-0"
    summary: "Senescent cells accumulate and release mitochondrial dsRNA into the cytosol. POLRMT supplies the mitochondrial RNA substrate, PNPT1 and ADAR normally restrain mt-dsRNA accumulation and immunogenicity, BAX/BAK-dependent pores permit mitochondrial nucleic-acid escape, DDX58/RIG-I and IFIH1/MDA5 activate MAVS, and MAVS drives type-I-IFN and SASP output while other senescence features are preserved. MFN1 promotes, whereas MFN2 suppresses, the mt-dsRNA/MAVS/SASP branch; POLRMT or mitofusin inhibition attenuates inflammatory output."
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
      1. Tissue/organ: cultured IMR-90 fibroblasts, SK-MEL-103 melanoma cells,
      A549 lung adenocarcinoma cells, MEFs, mouse xenografts, infarcted heart,
      aged mouse brain/liver/kidney, and human age-expression datasets.
      2. Species: human and mouse.
      3. Age range or comparison: proliferating vs senescent cells; young vs old
      mouse tissues; human tissue expression data across age.
      4. Sex-specific effects: not a central analysed variable in the curated graph.
      5. Disease context: cellular senescence, fibrosis/myocardial infarction model,
      tissue ageing, and systemic senescence-associated inflammation.
      Mechanistic note: the main paper mechanism is mt-dsRNA -> DDX58/IFIH1 ->
      MAVS -> type-I-IFN/SASP. CGAS/STING is retained as a parallel mtDNA branch
      because combined CGAS/STING depletion reduces cytokines, but it should not
      replace the mt-dsRNA/MAVS spine. BAX and BAK are represented as a combined
      BAX/BAK_pore mechanism because the paper mainly tests them together.

edges:

# Edges from LopezPolo_natcomms_2024
#
# Replacement intent:
#   - make the mt-dsRNA/MAVS spine dominant
#   - collapse BAX and BAK into BAX/BAK_pore unless the paper separates them
#   - avoid coarse POLRMT -> tissue_inflammation and MAVS -> CCL2-style edges
#   - preserve ADAR/PNPT1 double-negative logic with explicit brake edges and
#     an explicit net-effect edge from senescence to cytoplasmic_mt_dsRNA
#
# Verb guide:
#   forms_pore_for — physical pore-mediated translocation across a membrane
#   produces       — biosynthetic source of a nucleic-acid substrate
#   suppresses     — normal-function brake
#   downregulates  — senescence-associated loss of a brake
#   upregulates    — senescence-associated increase in a mechanistically central sensor
#   activates      — sensor/adaptor signalling activation
#   drives         — perturbation-supported causal driver
#   required_for   — perturbation removes a required input for an output

# ─── CHAIN 1: senescence creates cytoplasmic mt-dsRNA and removes brakes ─────

  - chain_id: senescence_mt_dsRNA_source
    step: 1
    source: cellular_senescence
    target: cytoplasmic_mt_dsRNA
    rel: induces
    evidence_strength: direct_measured
    context: "J2 immunofluorescence shows increased dsRNA foci in senescent IMR-90, SK-MEL-103, and A549 cells; colocalization separates mitochondrial from extra-mitochondrial foci; strand-specific RT-qPCR detects mitochondrial H- and L-strand RNAs in mitochondria-free cytosolic fractions. In vivo, dsRNA foci are seen in palbociclib-treated xenografts, infarcted/fibrotic heart, and aged mouse tissues. This net-effect edge is intentionally kept alongside the PNPT1 and ADAR brake edges so the double-negative logic is readable in the graph."
    support: "Fig. 1a-d; Fig. 5a-e; Supplementary Fig. 2; Supplementary Fig. 9"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: senescence_mt_dsRNA_source
    step: 2
    source: POLRMT
    target: cytoplasmic_mt_dsRNA
    rel: produces
    evidence_strength: perturbation_supported
    context: "IMT1 inhibition of mitochondrial RNA polymerase for 48 h in senescent cells strongly reduces J2 dsRNA foci and mitochondrial-encoded transcripts (MT-ND1, MT-CO1, MT-ATP8), while short-term treatment preserves mtDNA content and CDKN1A. Retroelement expression is not broadly reduced, supporting mitochondria as the main dsRNA source."
    support: "Fig. 1g,h; Supplementary Fig. 3a-e"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: senescence_mt_dsRNA_source
    step: 3
    source: cellular_senescence
    target: PNPT1
    rel: downregulates
    evidence_strength: direct_measured
    context: "PNPT1 immunofluorescence decreases in senescent IMR-90 and SK-MEL-103 cells. PNPT1 is the mitochondrial RNA-degradosome component that normally prevents mt-dsRNA accumulation; the graph treats this as loss of a normal brake."
    support: "Fig. 1f; Supplementary Fig. 1a"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: senescence_mt_dsRNA_source
    step: 4
    source: PNPT1
    target: cytoplasmic_mt_dsRNA
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "siPNPT1 is used as a positive control for increased dsRNA foci, and prior PNPT1 biology is cited as preventing mt-dsRNA accumulation. Read together with the previous edge, senescence downregulates a suppressor of cytoplasmic mt-dsRNA."
    support: "Supplementary Fig. 1a; Fig. 1f; main text citing PNPT1 mt-dsRNA biology"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: senescence_dsRNA_sensitization
    step: 1
    source: cellular_senescence
    target: ADAR
    rel: downregulates
    evidence_strength: direct_measured
    context: "ADAR1p150 protein decreases in senescent SK-MEL-103 cells by immunoblot and ADAR1 signal decreases in senescent IMR-90/SK-MEL-103 cells by immunofluorescence. This is encoded as senescence-associated loss of a normal dsRNA-editing brake."
    support: "Fig. 2a-c; Supplementary Fig. 4a-g"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: senescence_dsRNA_sensitization
    step: 2
    source: ADAR
    target: cytosolic_RNA_sensing
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "ADAR1 normally edits dsRNA and reduces its inflammatory potency. ADAR1 overexpression reduces SASP/IFN output, while siADAR enhances MAVS/cytokine responses. This is normal-function logic: senescence reduces ADAR, thereby releasing the brake on cytosolic RNA sensing."
    support: "Fig. 2d; Supplementary Fig. 4d-g"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: senescence_dsRNA_sensitization
    step: 3
    source: cellular_senescence
    target: DDX58
    rel: upregulates
    evidence_strength: direct_measured
    context: "RIG-I, encoded by DDX58, is upregulated at the mRNA level after senescence-inducing treatment in IMR-90 and SK-MEL-103 cells and increases with age in human tissue-expression data. This is retained as a gene-level edge because DDX58 is a mechanistically central dsRNA sensor, not a random SASP marker."
    support: "Fig. 2e; Fig. 5g"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: senescence_dsRNA_sensitization
    step: 4
    source: cellular_senescence
    target: IFIH1
    rel: upregulates
    evidence_strength: direct_measured
    context: "MDA5, encoded by IFIH1, is upregulated at the mRNA level after senescence-inducing treatment and in aged mouse/human contexts. It is retained as a mechanistically central sensor edge because combined RIG-I/MDA5 depletion reduces cytokine output."
    support: "Fig. 2e; Fig. 5f,g"
    papers:
      - LopezPolo_natcomms_2024

# ─── CHAIN 2: BAX/BAK-dependent pore release of mitochondrial nucleic acids ──

  - chain_id: BAX_BAK_release
    step: 1
    source: BAX/BAK_pore
    target: cytoplasmic_mt_dsRNA
    rel: forms_pore_for
    evidence_strength: perturbation_supported
    context: "Senescent Bax/Bak-DKO MEFs do not show the cytosolic mitochondrial H- and L-strand RNA accumulation seen in senescent WT MEFs. Combined siBAX+siBAK in senescent IMR-90 cells reduces SASP cytokines more strongly than siRIGI+siMDA5 or siCGAS+siSTING. BAX and BAK are not split into separate edges because the paper tests and interprets them mainly as a combined pore mechanism."
    support: "Fig. 2f,h; Supplementary Fig. 4j"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: BAX_BAK_release
    step: 2
    source: BAX/BAK_pore
    target: cytoplasmic_mtDNA
    rel: forms_pore_for
    evidence_strength: canonical_inferred
    context: "The paper cites prior senescence work showing BAX/BAK-dependent mt-dsDNA escape, and interprets the stronger effect of BAX/BAK depletion as consistent with release of both mt-dsRNA and mt-dsDNA. This is a parallel DNA-sensing branch and should not replace the main mt-dsRNA/MAVS mechanism."
    support: "Fig. 2f,h; Supplementary Fig. 4j; Discussion citing prior mt-dsDNA/BAX-BAK work"
    papers:
      - LopezPolo_natcomms_2024

# ─── CHAIN 3: cytoplasmic mt-dsRNA → cytosolic RNA sensing → MAVS → IFN/SASP ──

  - chain_id: mt_dsRNA_MAVS_SASP
    step: 1
    source: cytoplasmic_mt_dsRNA
    target: cytosolic_RNA_sensing
    rel: activates
    evidence_strength: perturbation_supported
    context: "Cytoplasmic mt-dsRNA is the upstream immunogenic RNA species in senescent cells. IMT1 reduces dsRNA foci and SASP/IFN output, BAX/BAK loss reduces cytosolic mitochondrial RNA, and RIG-I/MDA5 depletion reduces cytokine output. This edge prevents the ADAR brake branch from ending at an isolated cytosolic_RNA_sensing node."
    support: "Fig. 1c,d,g-i; Fig. 2f-h; Fig. 6"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: mt_dsRNA_MAVS_SASP
    step: 2
    source: cytosolic_RNA_sensing
    target: DDX58
    rel: activates
    evidence_strength: perturbation_supported
    context: "RIG-I, encoded by DDX58, is one of the cytosolic dsRNA sensors implicated by combined siRIGI/siMDA5 depletion. The paper does not fully separate RIG-I and MDA5 ligand specificity in senescence, so the sensor edges are split for graph readability while the perturbation context stays combined."
    support: "Fig. 2e-g; Fig. 6"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: mt_dsRNA_MAVS_SASP
    step: 3
    source: cytosolic_RNA_sensing
    target: IFIH1
    rel: activates
    evidence_strength: perturbation_supported
    context: "MDA5, encoded by IFIH1, is the second cytosolic dsRNA sensor implicated by combined siRIGI/siMDA5 depletion. This edge makes the graph topology explicit: mt-dsRNA engages cytosolic RNA sensing, which proceeds through RIG-I/MDA5 rather than stopping at a generic sensing node."
    support: "Fig. 2e-g; Fig. 6"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: mt_dsRNA_MAVS_SASP
    step: 4
    source: DDX58
    target: MAVS
    rel: activates
    evidence_strength: canonical_inferred
    context: "RIG-I/DDX58 signals through MAVS. The paper shows senescence-associated MAVS aggregation and MAVS dependence of IFN/SASP output, so this canonical continuity edge is graph-useful."
    support: "Fig. 2e-g; Fig. 3a-i"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: mt_dsRNA_MAVS_SASP
    step: 5
    source: IFIH1
    target: MAVS
    rel: activates
    evidence_strength: canonical_inferred
    context: "MDA5/IFIH1 signals through MAVS. The paper's perturbation evidence is combined RIG-I/MDA5 depletion plus direct MAVS depletion, so the gene-to-MAVS connection is canonical but necessary to preserve pathway topology."
    support: "Fig. 2e-g; Fig. 3a-i"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: mt_dsRNA_MAVS_SASP
    step: 6
    source: MAVS
    target: type_I_IFN
    rel: drives
    evidence_strength: perturbation_supported
    context: "Senescent cells show MAVS aggregates on mitochondria. siMAVS removes inflammatory/interferon transcriptional signatures and reduces IFN-related genes while preserving CDKN1A. This replaces marker-level MAVS -> CXCL10/CCL2/B2M edges."
    support: "Fig. 3a-i; Supplementary Fig. 5b"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: mt_dsRNA_MAVS_SASP
    step: 7
    source: MAVS
    target: SASP
    rel: drives
    evidence_strength: perturbation_supported
    context: "siMAVS strongly reduces SASP cytokines and other SASP components in senescent IMR-90 cells, without suppressing the senescence marker CDKN1A. The edge is program-level because individual cytokines are output markers rather than distinct mechanistic branches in this paper."
    support: "Fig. 3g-i; Supplementary Fig. 5b"
    papers:
      - LopezPolo_natcomms_2024

# ─── CHAIN 4: parallel mtDNA/cGAS/STING branch from the same pore biology ───

  - chain_id: parallel_mtDNA_cGAS_STING
    step: 1
    source: cytoplasmic_mtDNA
    target: CGAS
    rel: activates
    evidence_strength: canonical_inferred
    context: "The paper cites prior senescence work showing mt-dsDNA release through BAX/BAK and cGAS/STING contribution to SASP. Combined siCGAS+siSTING reduces cytokines in this study, but the primary resolved mechanism is mt-dsRNA/MAVS. This edge prevents cytoplasmic_mtDNA from becoming a dead-end node."
    support: "Fig. 2f; Supplementary Fig. 4h; Introduction and Discussion citing prior mt-dsDNA/cGAS-STING work"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: parallel_mtDNA_cGAS_STING
    step: 2
    source: CGAS
    target: STING1
    rel: activates
    evidence_strength: canonical_inferred
    context: "Canonical DNA-sensing continuity edge for the parallel mtDNA branch. The paper tests combined CGAS/STING depletion rather than separately resolving CGAS-to-STING signalling."
    support: "Fig. 2f; Supplementary Fig. 4h; canonical cGAS-STING signalling"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: parallel_mtDNA_cGAS_STING
    step: 3
    source: STING1
    target: SASP
    rel: drives
    evidence_strength: perturbation_supported
    context: "Combined siCGAS+siSTING reduces cytokine expression in senescent cells. This is kept as a parallel DNA-sensing contribution to SASP, not as the main curation spine for Lopez-Polo 2024."
    support: "Fig. 2f; Supplementary Fig. 4h"
    papers:
      - LopezPolo_natcomms_2024

# ─── CHAIN 5: mitofusins tune mt-dsRNA/MAVS/SASP output ─────────────────────

  - chain_id: mitofusin_mt_dsRNA_branch
    step: 1
    source: MFN1
    target: cytoplasmic_mt_dsRNA
    rel: drives
    evidence_strength: perturbation_supported
    context: "siMFN1 reduces J2 dsRNA foci in senescent cells, whereas siMFN2 increases them; combined siMFN1+siMFN2 resembles siMFN1, indicating MFN1-dominant control. MFN1 is retained as a mechanistic node because it sits upstream of dsRNA foci and MAVS aggregates."
    support: "Fig. 4e; Supplementary Fig. 7a-c"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: mitofusin_mt_dsRNA_branch
    step: 2
    source: MFN1
    target: MAVS
    rel: drives
    evidence_strength: perturbation_supported
    context: "siMFN1 reduces mitochondrial MAVS aggregates, pIRF3, and RIG-I signal in senescent cells. This encodes MFN1 as a positive regulator of the mt-dsRNA/MAVS axis, not merely a mitochondrial morphology factor."
    support: "Fig. 4f; Supplementary Fig. 7d-f"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: mitofusin_mt_dsRNA_branch
    step: 3
    source: MFN1
    target: SASP
    rel: drives
    evidence_strength: perturbation_supported
    context: "siMFN1 and combined siMFN1+siMFN2 reduce SASP/IFN signatures, and pharmacological mitofusin inhibition reduces SASP factors at RNA and protein levels. Other senescence features and short-term viability are preserved."
    support: "Fig. 4c,d,h; Supplementary Fig. 6i,j; Supplementary Fig. 8c-f"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: mitofusin_mt_dsRNA_branch
    step: 4
    source: MFN2
    target: cytoplasmic_mt_dsRNA
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "siMFN2 increases dsRNA foci in senescent cells, opposite to siMFN1. The graph encodes normal MFN2 as suppressive for cytoplasmic mt-dsRNA accumulation."
    support: "Fig. 4e; Supplementary Fig. 7a-c"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: mitofusin_mt_dsRNA_branch
    step: 5
    source: MFN2
    target: MAVS
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "siMFN2 increases MAVS aggregates, whereas siMFN1 reduces them. The antagonistic MFN1/MFN2 effect is retained because it is mechanistically informative and not a marker-only output."
    support: "Fig. 4f; Supplementary Fig. 7a-f"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: mitofusin_mt_dsRNA_branch
    step: 6
    source: MFN2
    target: SASP
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "Single siMFN2 further elevates SASP and IFN-responsive genes, while siMFN1 and siMFN1+2 reduce them. This is encoded as normal MFN2 suppressing SASP output, with MFN1-dominant combined inhibition noted in context."
    support: "Fig. 4d; Supplementary Fig. 6i,j; Supplementary Fig. 7a-f"
    papers:
      - LopezPolo_natcomms_2024

# ─── CHAIN 6: in vivo consequence of mitochondrial transcription inhibition ──

  - chain_id: in_vivo_POLRMT_SASP_branch
    step: 1
    source: POLRMT
    target: SASP
    rel: required_for
    evidence_strength: perturbation_supported
    context: "In a doxorubicin-driven systemic senescence-associated inflammation model, oral IMT1 reduces serum cytokines induced by doxorubicin. This is intentionally targeted to SASP rather than tissue_inflammation, and the upstream mechanism is represented separately by POLRMT -> cytoplasmic_mt_dsRNA -> DDX58/IFIH1 -> MAVS."
    support: "Fig. 5i; Methods, Analysis of cytokines in mouse serum"
    papers:
      - LopezPolo_natcomms_2024

# ─── Specificity controls kept because they define sensor choice ─────────────

  - chain_id: specificity_controls
    step: 1
    source: cellular_senescence
    target: DHX58
    rel: does_not_drive
    evidence_strength: direct_measured
    context: "LGP2, encoded by DHX58, remains unchanged after senescence-inducing treatments, unlike DDX58/RIG-I and IFIH1/MDA5. This negative edge is retained because it distinguishes the senescence-responsive dsRNA sensors from non-responsive dsRNA pathway components."
    support: "Fig. 2e"
    papers:
      - LopezPolo_natcomms_2024

  - chain_id: specificity_controls
    step: 2
    source: EIF2AK2
    target: SASP
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "PKR, encoded by EIF2AK2, is not upregulated in senescence and siPKR does not reduce the cytokines tested, unlike combined siRIGI+siMDA5. This edge is retained as a true sensor-specificity control."
    support: "Fig. 2e; Supplementary Fig. 4i"
    papers:
      - LopezPolo_natcomms_2024

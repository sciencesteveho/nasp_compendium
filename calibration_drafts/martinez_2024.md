paper:

  Martinez_biorxiv_2024:
    cite: "Martinez JC, Morandini F, Fitzgibbons L, et al. cGAS deficient mice display premature aging associated with de-repression of LINE1 elements and inflammation. bioRxiv. 2024."
    url: "https://doi.org/10.1101/2024.10.10.617645"
    summary: "CGAS-deficient mice show accelerated aging with tissue inflammation and fibrosis; mechanistically, nuclear CGAS supports H3K9me3-marked heterochromatin organization, restrains chromatin opening and transposon demethylation, suppresses L1/retrotransposon derepression, and limits cytoplasmic retroelement cDNA, AIM2/inflammasome-associated inflammatory output, SPI1-associated inflammatory chromatin programs, DNA damage, and aging phenotypes."
    nucleic_acid_sensors:
      - CGAS
      - AIM2
      - STING1
    genes:
      - CGAS
      - AIM2
      - SPI1
      - STING1
      - NLRP3
      - NLRP1
      - CASP1
      - IL18
      - IL6
      - NFKB1
      - TNF
    pathways:
      - nuclear_cGAS_heterochromatin
      - AIM2_inflammasome
      - NF-kB
    cell_types:
      - primary_lung_fibroblasts
      - MEF
      - human_diploid_fibroblasts
    mechanisms:
      - heterochromatin_organization
      - epigenetic_remodeling
      - retrotransposon_derepression
      - cytoplasmic_retroelement_cDNA
      - inflammasome_activation
      - tissue_inflammation
      - fibrosis
      - accelerated_aging
      - DNA_damage
    model_systems:
      - mouse_in_vivo
      - mouse_in_vitro
      - human_in_vitro
    evidence_type:
      - genetic_KO
      - siRNA_knockdown
      - bulk_RNA_seq
      - ATAC_seq
      - nanopore_methylation_seq
      - RT_qPCR
      - smiFISH
      - immunofluorescence
      - immunoblot
      - IHC
      - histology
      - STED_microscopy
      - survival_analysis
    notes: >
      1. Tissue/organ: lung primary cells/fibroblasts, lung tissue, liver,
      kidney, mouse embryonic fibroblasts, and human diploid fibroblasts.
      2. Species: mouse and human in vitro.
      3. Age range or comparison: 12-month WT versus cGAS KO for molecular
      profiling; 18-month WT versus cGAS KO for frailty; female lifespan WT
      median 106.7 weeks versus cGAS KO 92.4 weeks.
      4. Sex-specific effects: both sexes show increased frailty; males show
      higher frailty and obesity/body mass, while females show shortened
      lifespan.
      5. Disease context: accelerated aging, inflammaging-like tissue
      inflammation, liver fibrosis, and L1/retrotransposon derepression.
      Mechanistic note: cGAS loss, not STING1 loss or PYHIN-family loss,
      derepresses L1MdA. H3K9me3, ORF1p, ORF2p, ATAC-seq loci, Nanopore
      methylation loci, and the cytokine qPCR panel are evidence in context,
      not graph nodes. SPI1/PU.1 is promoted because opening OCRs are strongly
      enriched for SPI1 motifs, SPI1 is expressed/upregulated, and the authors
      explicitly propose it may mediate inflammatory genes and fibrosis.
      FoxE1/FoxD2 closing-OCR motifs remain contextual because the authors say
      their contribution is unclear.
    relevance_to_project: >
      Look for low CGAS or cGAS-loss states with L1/retrotransposon expression,
      cytoplasmic retroelement cDNA signatures, AIM2/inflammasome markers,
      SPI1-associated inflammatory chromatin programs, tissue inflammation, and
      fibrosis. In spatial or single-cell data, the expected pattern is
      epithelial/stromal CGAS loss or reduced nuclear cGAS maintenance paired
      with transposon derepression, AIM2/inflammasome inflammatory output, SPI1
      activity, and inflammatory/fibrotic tissue neighborhoods.

edges:

  - chain_id: nuclear_cGAS_L1_restraint
    step: 1
    source: CGAS
    target: heterochromatin_organization
    rel: binds_recruits
    evidence_strength: direct_measured
    context: "STED microscopy shows nuclear CGAS puncta/condensates in primary mouse lung cells and human diploid fibroblasts. CGAS signal strongly colocalizes with the H3K9me3 heterochromatin mark, and cGAS KO cells lose H3K9me3 foci and show altered H3K9me3 nuclear distribution. H3K9me3 is kept as context rather than a node."
    support: "Fig. 7a-c; Sup. Fig. 6a"
    papers:
      - Martinez_biorxiv_2024

  - chain_id: nuclear_cGAS_L1_restraint
    step: 2
    source: CGAS
    target: epigenetic_remodeling
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "Loss of CGAS in primary lung cells is associated with 1392 more accessible OCRs by ATAC-seq, increased accessibility over pro-inflammatory promoters including Aim2, increased accessibility over young L1Md elements, and Nanopore-measured loss of methylation across LINE, LTR, SINE, DNA transposon, and L1Md families. Locus identities and ATAC/Nanopore readouts are context for the canonical epigenetic_remodeling node."
    support: "Fig. 5a, 5d, 5e; Fig. 6a-d"
    papers:
      - Martinez_biorxiv_2024

  - chain_id: nuclear_cGAS_L1_restraint
    step: 3
    source: epigenetic_remodeling
    target: retrotransposon_derepression
    rel: drives
    evidence_strength: perturbation_supported
    context: "CGAS KO primary lung cells show increased chromatin accessibility and reduced methylation over young L1Md families, coincident with increased L1MdA/L1MdFanc RNA-seq signal and RT-qPCR-confirmed L1MdA mRNA in lung, kidney, and liver. CGAS siRNA/shRNA knockdown in MEFs also increases L1MdA mRNA, supporting a cell-intrinsic CGAS-loss effect."
    support: "Fig. 3a, 3b; Fig. 4a, 4b; Fig. 5e; Fig. 6c"
    papers:
      - Martinez_biorxiv_2024

  - chain_id: nuclear_cGAS_L1_restraint
    step: 4
    source: retrotransposon_derepression
    target: cytoplasmic_retroelement_cDNA
    rel: produces
    evidence_strength: perturbation_supported
    context: "DNA smiFISH probes targeting L1MdA ORF1p/ORF2p sequence detect elevated cytoplasmic L1 cDNA in cGAS KO primary lung cells and CGAS-knockdown MEFs. Subcellular fractionation followed by DNA qPCR confirms increased cytosolic L1MdA cDNA after CGAS knockdown. ORF1p accumulation supports L1 derepression and remains in context."
    support: "Fig. 3c, 3d; Fig. 4c-h"
    papers:
      - Martinez_biorxiv_2024

  - chain_id: chromatin_opening_SPI1_inflammatory_arm
    step: 1
    source: epigenetic_remodeling
    target: SPI1
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "MEME-ChIP analysis of OCRs opening in cGAS KO primary lung cells shows strong enrichment for SPI1/PU.1 motifs. SPI1 is in the top 15% most expressed genes in RNA-seq and is upregulated in cGAS KO cells (LogFC 0.4, p = 0.0145)."
    support: "Fig. 5c; Source Data 9; RNA-seq described in Results"
    papers:
      - Martinez_biorxiv_2024

  - chain_id: chromatin_opening_SPI1_inflammatory_arm
    step: 2
    source: SPI1
    target: tissue_inflammation
    rel: drives
    evidence_strength: perturbation_supported
    context: "The authors invoke SPI1/PU.1 as a mediator of inflammatory gene expression and the liver fibrosis observed in cGAS KO mice, citing prior fibroblast/fibrotic disease literature and inflammasome-gene regulation. Perturbation support is the cGAS-KO chromatin-opening program with dominant SPI1 motifs and concordant SPI1 expression; SPI1 itself is not knocked down here, which is the limit on this edge. FoxE1/FoxD2 motifs from closing OCRs are not nodes because the authors state their role is unclear."
    support: "Fig. 5b, 5c; Results text on SPI1/PU.1"
    papers:
      - Martinez_biorxiv_2024

  - chain_id: L1cDNA_AIM2_inflammasome
    step: 1
    source: cytoplasmic_retroelement_cDNA
    target: AIM2
    rel: activates
    evidence_strength: canonical_inferred
    context: "cGAS KO cells accumulate cytoplasmic L1 cDNA and show elevated AIM2 expression/accessibility. AIM2 is a canonical cytosolic dsDNA sensor, but the paper does not perform AIM2 perturbation or direct AIM2 activation assays."
    support: "Fig. 2c, 2d; Fig. 3c; Fig. 4g; Fig. 5d; Discussion"
    papers:
      - Martinez_biorxiv_2024

  - chain_id: L1cDNA_AIM2_inflammasome
    step: 2
    source: AIM2
    target: inflammasome_activation
    rel: drives
    evidence_strength: canonical_inferred
    context: "RNA-seq shows enrichment of inflammasome-complex components including Aim2, Nlrp3, Nlrp1a/b, and Casp1, and RT-qPCR confirms AIM2 plus downstream inflammatory targets. The paper proposes AIM2 may compensate for CGAS loss but does not perturb AIM2."
    support: "Fig. 2c, 2d"
    papers:
      - Martinez_biorxiv_2024

  - chain_id: L1cDNA_AIM2_inflammasome
    step: 3
    source: inflammasome_activation
    target: tissue_inflammation
    rel: drives
    evidence_strength: canonical_inferred
    context: "Inflammasome-associated RNA-seq and qRT-PCR readouts in cGAS KO lung tissue include IL18, NFKB/NFkB, TNF alpha, and IL6, and histology shows lung inflammatory infiltration. The cytokine panel is a program readout and remains in context; IL18 is not reused as a separate endpoint."
    support: "Fig. 1c; Fig. 2b-d"
    papers:
      - Martinez_biorxiv_2024

  - chain_id: L1cDNA_DNA_damage
    step: 1
    source: cytoplasmic_retroelement_cDNA
    target: DNA_damage
    rel: induces
    evidence_strength: perturbation_supported
    context: "CGAS-deficient MEFs show increased gamma-H2AX immunostaining along with L1MdA cDNA accumulation after CGAS knockdown. The paper interprets CGAS loss and L1 cDNA accumulation as contributing to DNA damage, but the perturbation is CGAS knockdown rather than direct L1 cDNA perturbation."
    support: "Fig. 4c-j"
    papers:
      - Martinez_biorxiv_2024

  - chain_id: organismal_accelerated_aging
    step: 1
    source: tissue_inflammation
    target: fibrosis
    rel: drives
    evidence_strength: direct_measured
    context: "Histology of cGAS KO mice shows lung neutrophil infiltration/inflammation and elevated liver inflammation with fibrotic tissue. Fibrosis is kept as a tissue-agnostic outcome node; liver context lives in the edge."
    support: "Fig. 1c, 1d"
    papers:
      - Martinez_biorxiv_2024

  - chain_id: organismal_accelerated_aging
    step: 2
    source: tissue_inflammation
    target: accelerated_aging
    rel: drives
    evidence_strength: strong_correlative
    context: "cGAS KO mice show tissue inflammation, increased frailty at 18 months in both sexes, male obesity/body-mass increase, and shortened female lifespan. This organism-level aging association is routed through tissue_inflammation rather than a CGAS-to-accelerated_aging shortcut."
    support: "Fig. 1a-f; Sup. Fig. 1a-f"
    papers:
      - Martinez_biorxiv_2024

  - chain_id: specificity_controls
    step: 1
    source: STING1
    target: retrotransposon_derepression
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "STING KO mice maintain L1MdA repression, indicating L1 derepression is specifically associated with CGAS depletion rather than downstream CGAS-STING pathway disruption. PYHIN-family KO mice also maintain L1MdA repression; that non-HGNC family-level control is kept in context rather than as a separate graph node."
    support: "Sup. Fig. 4; Results text 'Depletion of other cytoplasmic DNA sensors does not lead to L1 activation'"
    papers:
      - Martinez_biorxiv_2024

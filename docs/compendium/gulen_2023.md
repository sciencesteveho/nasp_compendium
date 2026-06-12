paper:

  Gulen_nature_2023:
    cite: "Gulen MF, Samson N, Keller A, Schwabenland M, Liu C, Glück S, Thacker VV, Favre L, Mangeat B, Kroese LJ, Krimpenfort P, Prinz M, Ablasser A. cGAS-STING drives ageing-related inflammation and neurodegeneration. Nature. 2023;620(7973):374-380."
    url: "https://doi.org/10.1038/s41586-023-06373-1"
    summary: "STING inhibition or Sting1 knockout suppresses inflammatory and type-I-IFN phenotypes in senescent human cells, human adipose explants, peripheral organs, and aged mouse brain. In aged microglia, mitochondrial disruption and VDAC1/3-dependent pore biology are linked to cytoplasmic mtDNA, cGAS activity, cGAMP production, STING-TBK1 signalling, type-I-IFN/proinflammatory output, reactive microglial states, TNF-mediated neuronal loss, and cognitive decline. The replacement curation keeps the pathway spine explicit and removes marker-only cytokine shortcut edges."
    nucleic_acid_sensors:
      - CGAS
      - STING1
    genes:
      - CGAS
      - STING1
      - TBK1
      - IRF3
      - VDAC1
      - VDAC3
      - TNF
      - IFNB1
      - IL6
      - IL1B
      - CXCL8
      - CXCL9
      - CXCL10
      - CCL2
      - CCL5
      - CCL7
      - MX1
      - MX2
      - OAS1
      - OAS2
      - IFIT1
      - IFIT3
      - ISG15
      - IFITM3
      - IFI44
      - IFI44L
      - RSAD2
      - B2M
      - IRF7
      - STAT1
      - CDKN1A
      - CDKN2A
    pathways:
      - cGAS-STING
      - type_I_IFN
      - NF-kB
      - JAK-STAT
      - SASP
    cell_types:
      - WI-38_fibroblasts
      - senescent_preadipocytes
      - primary_microglia
      - BV2_cells
      - hippocampal_neurons
      - astrocytes
      - oligodendrocytes
      - DAM_microglial_state
      - IFN_MG_microglial_state
      - ND_MG_microglial_state
    mechanisms:
      - cellular_senescence
      - mitochondrial_dysfunction
      - VDAC_oligomerization
      - cytoplasmic_mtDNA
      - cytosolic_DNA_sensing
      - mtDNA_release
      - tissue_inflammation
      - microglial_activation
      - neurodegeneration
      - hippocampal_neuron_loss
      - cognitive_decline
    model_systems:
      - human_in_vitro
      - human_tissue_explant
      - mouse_in_vivo
      - mouse_in_vitro
      - mouse_genetic_model
    evidence_type:
      - pharmacological_inhibition
      - genetic_KO
      - genetic_gain_of_function
      - siRNA_knockdown
      - bulk_RNA_seq
      - snRNA_seq
      - RT_qPCR
      - immunoblot
      - immunofluorescence
      - ELISA
      - behavioral_testing
      - co_culture
    notes: >
      1. Tissue/organ: senescent human WI-38/BJ fibroblasts; human adipose tissue
      explants; aged mouse kidney, liver, white adipose tissue, and brain; isolated
      primary microglia and BV2 microglia.
      2. Species: human and mouse.
      3. Age range or comparison: young vs aged mice, including very old 26-month
      mice; human cellular senescence models.
      4. Sex-specific effects: not a central analysed variable in the curated graph.
      5. Disease context: physiological ageing, inflammaging, neurodegeneration,
      frailty, and cognitive decline.
      Mechanistic note: retain the chain
      mitochondrial_dysfunction -> VDAC_oligomerization -> cytoplasmic_mtDNA ->
      CGAS -> cGAMP -> STING1 -> TBK1 -> IRF3 -> type_I_IFN/SASP. DAM/IFN-MG/ND-MG
      states belong in a separate microglial cGAS gain-of-function branch, not as
      direct replacements for the upstream mtDNA/cGAS/STING mechanism. TNF is kept
      because neutralization functionally rescues neuronal death; random SASP
      marker genes are kept in context rather than as individual graph edges.

edges:

# Edges from Gulen_nature_2023
#
# Replacement intent:
#   - remove marker-only cytokine edges such as STING1 -> IL1B
#   - remove broad shortcut edges such as STING1 -> cognitive_decline
#   - retain graph-useful branch edges and specificity controls
#   - make pore-mediated mtDNA release explicit with VDAC_oligomerization and
#     forms_pore_for
#
# Verb guide:
#   forms_pore_for — physical pore-mediated translocation across a membrane
#   produces       — biosynthetic or enzymatic production of a signalling molecule
#   activates      — triggers enzymatic or signalling activity
#   drives         — perturbation-supported causal driver
#   induces        — causes a state or phenotype
#   upregulates    — increases abundance of a mechanistically central mediator
#   does_not_drive — tested and found not to regulate a specific branch

# ─── CHAIN 1: senescence/ageing → mtDNA release → cGAS → STING → IFN/SASP ───

# Aged microglia have dysmorphic mitochondria; this is an observed upstream
# ageing-associated state, not a fully resolved cause of VDAC oligomerization.
  - chain_id: aging_mtDNA_cGAS_STING
    step: 1
    source: cellular_senescence
    target: mitochondrial_dysfunction
    rel: induces
    evidence_strength: direct_measured
    context: "TEM of primary microglia from aged (24-27 months) vs young (8-12 weeks) mice shows misshapen mitochondria lacking characteristic internal structure in aged microglia. The paper establishes mitochondrial disruption in aged microglia, but does not resolve the upstream molecular cause of the mitochondrial defect."
    support: "Fig. 3e"
    papers:
      - Gulen_nature_2023

# VDAC oligomerization is the graph node because the paper uses VBIT-4 and cites
# VDAC1/3 oligomers; individual VDAC1 vs VDAC3 contributions are not separated.
  - chain_id: aging_mtDNA_cGAS_STING
    step: 2
    source: mitochondrial_dysfunction
    target: VDAC_oligomerization
    rel: drives
    evidence_strength: canonical_inferred
    context: "The paper links mitochondrial disruption in aged microglia to cytoplasmic mtDNA and tests VBIT-4, an inhibitor of VDAC oligomerization. The mitochondrial_dysfunction -> VDAC_oligomerization edge is an inferred continuity edge from the paper's model and cited VDAC1/3 pore literature, not a direct measurement of oligomer abundance."
    support: "Fig. 3e-g; Extended Data Fig. 6e; main text citing VDAC1/3 oligomer work"
    papers:
      - Gulen_nature_2023

  - chain_id: aging_mtDNA_cGAS_STING
    step: 3
    source: VDAC_oligomerization
    target: cytoplasmic_mtDNA
    rel: forms_pore_for
    evidence_strength: perturbation_supported
    context: "Primary aged microglia show increased cytosolic mitochondrial DNA by qPCR (Mito/CoI elevated, B2m nuclear DNA not elevated) and super-resolution imaging shows cytosolic mtDNA nucleoids adjacent to the mitochondrial outer membrane. Ex vivo VBIT-4 suppresses several type-I-IFN and proinflammatory genes in aged microglia. This is encoded as forms_pore_for because the mechanistic claim is pore-mediated mtDNA fragment release through VDAC oligomers, not generic VDAC1/3 secretion."
    support: "Fig. 3f, 3g; Extended Data Fig. 6d, 6e"
    papers:
      - Gulen_nature_2023

  - chain_id: aging_mtDNA_cGAS_STING
    step: 4
    source: cytoplasmic_mtDNA
    target: CGAS
    rel: activates
    evidence_strength: perturbation_supported
    context: "Aged brain lysates have elevated cGAMP and aged microglia show cytoplasmic mtDNA accumulation. VBIT-4 suppression of IFN/proinflammatory genes links pore-mediated mtDNA release to downstream cGAS-STING output. BV2 senescence experiments further support mtDNA-dependent cGAS inflammatory responses."
    support: "Fig. 2e; Fig. 3f, 3g; Extended Data Fig. 6e; Extended Data Fig. 7"
    papers:
      - Gulen_nature_2023

  - chain_id: aging_mtDNA_cGAS_STING
    step: 5
    source: CGAS
    target: cGAMP
    rel: produces
    evidence_strength: direct_measured
    context: "2'3'-cGAMP is robustly elevated in brain lysates from aged mice compared with young mice. The CgasR241E gain-of-function system also produces cGAMP after 4-OHT activation in proof-of-concept experiments. This edge prevents the graph from collapsing CGAS directly onto STING1."
    support: "Fig. 2e; Extended Data Fig. 8b-d"
    papers:
      - Gulen_nature_2023

  - chain_id: aging_mtDNA_cGAS_STING
    step: 6
    source: cGAMP
    target: STING1
    rel: activates
    evidence_strength: canonical_inferred
    context: "cGAMP is the canonical second messenger produced by CGAS that activates STING1. The paper measures cGAMP, pSTING, and STING-dependent inflammatory output, so this canonical continuity edge is necessary for graph readability."
    support: "Fig. 2e; Fig. 3c; canonical cGAS-STING signalling"
    papers:
      - Gulen_nature_2023

  - chain_id: aging_mtDNA_cGAS_STING
    step: 7
    source: STING1
    target: TBK1
    rel: activates
    evidence_strength: direct_measured
    context: "Aged mouse brain shows increased phosphorylated TBK1 and phosphorylated STING, and H-151 reduces pTBK1 abundance. This is the missing STING1 -> TBK1 edge in the prior graph."
    support: "Fig. 2d; Fig. 3c"
    papers:
      - Gulen_nature_2023

  - chain_id: aging_mtDNA_cGAS_STING
    step: 8
    source: TBK1
    target: IRF3
    rel: activates
    evidence_strength: canonical_inferred
    context: "TBK1 is the canonical kinase upstream of IRF3 in STING signalling. The paper directly measures pTBK1 and downstream type-I-IFN/ISG output; IRF3 is included as a pathway-continuity node rather than as a separately measured phospho-IRF3 endpoint."
    support: "Fig. 2d; Fig. 1a,b,d,e; canonical STING-TBK1-IRF3 signalling"
    papers:
      - Gulen_nature_2023

  - chain_id: aging_mtDNA_cGAS_STING
    step: 9
    source: IRF3
    target: type_I_IFN
    rel: drives
    evidence_strength: canonical_inferred
    context: "The paper repeatedly measures type-I-IFN/ISG programs downstream of STING inhibition or Sting1 loss. IRF3 is retained as the canonical transcriptional bridge from TBK1 to the type-I-IFN program."
    support: "Fig. 1a,b,d,e; Fig. 3a,d; Extended Data Fig. 4a,b,g-i"
    papers:
      - Gulen_nature_2023

  - chain_id: aging_mtDNA_cGAS_STING
    step: 10
    source: STING1
    target: NF-kB
    rel: drives
    evidence_strength: canonical_inferred
    context: "H-151 and Sting1 loss suppress proinflammatory cytokine/chemokine genes as well as IFN-stimulated genes. NF-kB is included as a canonical proinflammatory branch of STING output, but the paper's direct measured nodes are inflammatory genes and tissue phenotypes rather than a dedicated RELA/p65 assay."
    support: "Fig. 1a,b,d,e; Extended Data Fig. 2f; Extended Data Fig. 3"
    papers:
      - Gulen_nature_2023

  - chain_id: aging_mtDNA_cGAS_STING
    step: 11
    source: STING1
    target: SASP
    rel: drives
    evidence_strength: perturbation_supported
    context: "H-151 suppresses proinflammatory genes and type-I-IFN-stimulated genes in senescent WI-38/BJ fibroblasts and human adipose explants, while non-inflammatory senescence features such as CDKN1A are preserved. This replaces individual marker-only STING1 -> IL6/IL1B/CXCL10/CCL2 edges."
    support: "Fig. 1a,b; Extended Data Fig. 2a-f; Extended Data Fig. 3"
    papers:
      - Gulen_nature_2023

  - chain_id: aging_mtDNA_cGAS_STING
    step: 12
    source: STING1
    target: tissue_inflammation
    rel: drives
    evidence_strength: perturbation_supported
    context: "H-151 treatment and Sting1 knockout reduce ageing-related immune markers and inflammatory cell accumulation in peripheral organs, including kidney, liver, and white adipose tissue. This is retained as a tissue-level consequence branch, separate from the molecular STING -> TBK1/IRF3 chain."
    support: "Fig. 1d,e; Extended Data Fig. 4a-f"
    papers:
      - Gulen_nature_2023

# ─── CHAIN 2: STING activity in aged brain → microglia → neurodegeneration ───

  - chain_id: STING_microglia_neurodegeneration
    step: 1
    source: STING1
    target: microglial_activation
    rel: drives
    evidence_strength: perturbation_supported
    context: "Aged hippocampus shows increased pSTING predominantly in IBA1+ microglia, and H-151 reduces microgliosis, lysosomal activation markers, and immune-related brain signatures. Isolated aged microglia show STING-dependent IFN/proinflammatory gene expression ex vivo."
    support: "Fig. 2a; Fig. 3c,d; Extended Data Fig. 4g-i; Extended Data Fig. 5a-c"
    papers:
      - Gulen_nature_2023

  - chain_id: STING_microglia_neurodegeneration
    step: 2
    source: microglial_activation
    target: neurodegeneration
    rel: drives
    evidence_strength: perturbation_supported
    context: "STING inhibition reduces microgliosis and preserves NeuN+ neuronal density and synaptophysin immunoreactivity in aged hippocampus. The graph intentionally avoids the shortcut STING1 -> cognitive_decline by routing the phenotype through microglial activation and neurodegeneration."
    support: "Fig. 2a-c; Extended Data Fig. 5d"
    papers:
      - Gulen_nature_2023

  - chain_id: STING_microglia_neurodegeneration
    step: 3
    source: neurodegeneration
    target: cognitive_decline
    rel: drives
    evidence_strength: perturbation_supported
    context: "H-151 improves Morris water maze and contextual fear-conditioning performance in aged mice while also reducing brain immune signatures and neurodegenerative readouts. The causal chain is interpreted at phenotype level; the direct intervention is STING inhibition, not isolated rescue of neurons alone."
    support: "Fig. 1h; Fig. 2b,c; Extended Data Fig. 4g-i"
    papers:
      - Gulen_nature_2023

# ─── CHAIN 3: microglial cGAS gain-of-function → states → TNF neurotoxicity ──

  - chain_id: microglial_cGAS_GOF_states
    step: 1
    source: CGAS
    target: microglial_activation
    rel: drives
    evidence_strength: perturbation_supported
    context: "Tamoxifen-inducible microglia-enriched CgasR241E expression increases activated IBA1+ microglia in multiple brain regions and elevates inflammatory and IFN-related genes in brain. H-151 attenuates microglial activation in mg-CgasR241E mice, supporting cGAS-STING dependence."
    support: "Fig. 4b-d; Extended Data Fig. 8e-j"
    papers:
      - Gulen_nature_2023

  - chain_id: microglial_cGAS_GOF_states
    step: 2
    source: CGAS
    target: DAM_microglial_state
    rel: drives
    evidence_strength: perturbation_supported
    context: "Single-nucleus RNA-seq of microglia from mg-CgasR241E mice shows expansion of DAM-1/2 states and increased DAM scores. This is kept as a gain-of-function sufficiency branch, not as a direct edge from aged mtDNA to DAM."
    support: "Fig. 4e-g; Extended Data Fig. 9b-e"
    papers:
      - Gulen_nature_2023

  - chain_id: microglial_cGAS_GOF_states
    step: 3
    source: CGAS
    target: IFN_MG_microglial_state
    rel: drives
    evidence_strength: perturbation_supported
    context: "The same microglial CgasR241E snRNA-seq experiment shows expansion of IFN-associated microglia and increased IFN scores. The edge is retained because it is a graph-useful cell-state consequence of cGAS engagement."
    support: "Fig. 4e-g; Extended Data Fig. 9b-e"
    papers:
      - Gulen_nature_2023

  - chain_id: microglial_cGAS_GOF_states
    step: 4
    source: CGAS
    target: ND_MG_microglial_state
    rel: drives
    evidence_strength: perturbation_supported
    context: "Microglial CgasR241E shifts cells toward a neurodegeneration-associated microglial state. This branch belongs downstream of cGAS gain-of-function and should not replace the molecular mtDNA/cGAS/STING/TBK1 pathway."
    support: "Fig. 4e-g; Extended Data Fig. 9b-e"
    papers:
      - Gulen_nature_2023

  - chain_id: microglial_cGAS_TNF_neurotoxicity
    step: 1
    source: CGAS
    target: TNF
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "mg-CgasR241E brains show elevated Tnf mRNA, and CgasR241E microglia co-culture experiments implicate TNF as the dominant neurotoxic soluble mediator. TNF is retained as a gene-level node because anti-TNF functionally rescues neuron death."
    support: "Fig. 4d,j,k; Extended Data Fig. 10g-i"
    papers:
      - Gulen_nature_2023

  - chain_id: microglial_cGAS_TNF_neurotoxicity
    step: 2
    source: TNF
    target: hippocampal_neuron_loss
    rel: drives
    evidence_strength: perturbation_supported
    context: "Conditioned/co-culture experiments show neuronal loss driven by CgasR241E or aged microglia, and TNF neutralization rescues neuronal death. This is the mechanistic bridge between inflammatory microglia and neurodegeneration."
    support: "Fig. 4j,k; Extended Data Fig. 10g-i"
    papers:
      - Gulen_nature_2023

  - chain_id: microglial_cGAS_TNF_neurotoxicity
    step: 3
    source: hippocampal_neuron_loss
    target: cognitive_decline
    rel: drives
    evidence_strength: perturbation_supported
    context: "mg-CgasR241E mice show hippocampal NeuN+ neuron loss and impaired Morris water maze performance. This keeps cognitive decline downstream of a neurodegenerative phenotype rather than drawing a shortcut from STING1 or CGAS directly to cognition."
    support: "Fig. 4h,i"
    papers:
      - Gulen_nature_2023

# ─── Specificity control kept because it changes the neurotoxicity mechanism ──

  - chain_id: specificity_controls
    step: 1
    source: type_I_IFN
    target: hippocampal_neuron_loss
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "Anti-IFNAR blockade does not rescue neuronal death in CgasR241E microglia co-culture, whereas anti-TNF does. This negative edge is retained because it prevents the graph from wrongly routing neurotoxicity through the IFN-I branch."
    support: "Fig. 4j,k; Extended Data Fig. 10h,i"
    papers:
      - Gulen_nature_2023

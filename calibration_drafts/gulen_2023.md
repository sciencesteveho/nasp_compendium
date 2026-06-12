paper:
  Gulen_nature_2023:
    cite: "Gulen MF, Samson N, Keller A, Schwabenland M, Liu C, Glück S, Thacker VV, Favre L, Mangeat B, Kroese LJ, Krimpenfort P, Prinz M, Ablasser A. cGAS-STING drives ageing-related inflammation and neurodegeneration. Nature 2023."
    url: "https://doi.org/10.1038/s41586-023-06373-1"
    summary: "STING1 signaling drives inflammatory SASP outputs in senescent human cells and age-associated peripheral and brain inflammation in mice, with old microglia engaging CGAS-STING1 through mitochondrial cytosolic DNA to promote neurodegeneration and cognitive decline."
    nucleic_acid_sensors:
      - CGAS
      - STING1
    genes:
      - CGAS
      - STING1
      - IL6
      - CXCL8
      - CCL2
      - CXCL10
      - TNF
      - IFNB1
      - IFI44
      - CXCL9
      - CCL5
    pathways:
      - cGAS-STING
      - SASP
      - type_I_IFN
    cell_types:
      - senescent_BJ_fibroblasts
      - senescent_preadipocytes
      - adipose_tissue_explants
      - kidney
      - liver
      - brain
      - microglia
      - hippocampal_neurons
    mechanisms:
      - aging
      - cellular_senescence
      - cytoplasmic_mtDNA
      - inflammaging
      - tissue_inflammation
      - microglial_activation
      - neurodegeneration
      - cognitive_decline
      - mitochondrial_dysfunction
    model_systems:
      - human_in_vitro
      - human_tissue_explant
      - mouse_in_vivo
      - mouse_genetic_model
      - snRNA_seq
    evidence_type:
      - behavioral_testing
      - ELISA
      - genetic_gain_of_function
      - genetic_KO
      - histology
      - IHC
      - pharmacological_inhibition
      - RT_qPCR
      - single_cell_RNA_seq
      - snRNA_seq
    notes: >
      1. Tissue/organ: human fibroblasts, human adipose tissue explants, mouse kidney,
      liver, adipose tissue, brain, hippocampus, and microglia.
      2. Species: human and mouse.
      3. Age range or comparison: old mice around 21-26 months versus young controls,
      plus senescent human cell and tissue models.
      4. Sex-specific effects: not addressed as a central mechanism.
      5. Disease context: aging-related inflammation, neurodegeneration, cognitive decline.
      H-151 and Sting1 knockout support STING1 as a driver of age-associated inflammation.
      Old microglia contain cytosolic mitochondrial DNA that engages CGAS-STING1.
      A microglia-targeted CGAS gain-of-function model shows sufficiency for reactive
      microglial states, neuronal injury, and memory impairment.
    relevance_to_project: >
      In aging brain datasets, look for microglial cGAS-STING/type-I-IFN modules,
      cytosolic mitochondrial DNA stress, inflammatory chemokines, reactive microglial
      states, bystander neuronal loss, and improved inflammatory/tissue-function states
      after STING1 blockade.

edges:
  - chain_id: senescent_human_STING_SASP
    step: 1
    source: cellular_senescence
    target: STING1
    rel: activates
    evidence_strength: direct_measured
    context: "Senescent BJ fibroblasts and pre-adipocytes show STING-dependent inflammatory outputs; STING blockade with H-151 or siRNA reduces SASP markers."
    support: "Fig. 1a-c; Extended Data Fig. 2; Extended Data Fig. 3"
    papers:
      - Gulen_nature_2023
  - chain_id: senescent_human_STING_SASP
    step: 2
    source: STING1
    target: SASP
    rel: drives
    evidence_strength: perturbation_supported
    context: "H-151 and STING1 knockdown suppress IL6, CXCL8/IL8, CCL2/MCP1, and CXCL10 in senescent human cells and obese-patient adipose explants, without simply eliminating senescent cells."
    support: "Fig. 1a-c; Extended Data Fig. 2; Extended Data Fig. 3"
    papers:
      - Gulen_nature_2023
  - chain_id: aged_periphery_STING
    step: 1
    source: aging
    target: STING1
    rel: activates
    evidence_strength: direct_measured
    context: "Aged mice show elevated STING-dependent immune and interferon-stimulated gene expression across peripheral organs."
    support: "Fig. 1d,e; Extended Data Fig. 4a,b,f"
    papers:
      - Gulen_nature_2023
  - chain_id: aged_periphery_STING
    step: 2
    source: STING1
    target: tissue_inflammation
    rel: drives
    evidence_strength: perturbation_supported
    context: "H-151 treatment and Sting1 knockout attenuate inflammatory cytokines, kidney inflammatory clusters and damage markers, and macrophage accumulation in adipose tissue of aged mice."
    support: "Fig. 1d,e; Extended Data Fig. 4a-f"
    papers:
      - Gulen_nature_2023
  - chain_id: aged_periphery_STING
    step: 3
    source: tissue_inflammation
    target: cognitive_decline
    rel: drives
    evidence_strength: perturbation_supported
    context: "STING inhibition improves physical and cognitive performance in aged mice, including Morris water maze and contextual fear conditioning; this draft encodes the organismal phenotype as downstream of age-associated inflammation."
    support: "Fig. 1f-h"
    papers:
      - Gulen_nature_2023
  - chain_id: aged_brain_microglia
    step: 1
    source: aging
    target: microglial_activation
    rel: induces
    evidence_strength: direct_measured
    context: "Aged mouse hippocampus shows microgliosis and age-associated microglial transcriptional states."
    support: "Fig. 2a-d"
    papers:
      - Gulen_nature_2023
  - chain_id: aged_brain_microglia
    step: 2
    source: STING1
    target: microglial_activation
    rel: drives
    evidence_strength: perturbation_supported
    context: "H-151 reduces aged-brain immune gene expression and microgliosis; Sting1 loss/inhibition suppresses inflammatory microglial states."
    support: "Fig. 2a-d; Extended Data Fig. 4g-i"
    papers:
      - Gulen_nature_2023
  - chain_id: aged_brain_microglia
    step: 3
    source: microglial_activation
    target: neurodegeneration
    rel: drives
    evidence_strength: perturbation_supported
    context: "STING-dependent reactive microglial states associate with hippocampal neuron loss/neurotoxicity in aged and CGAS gain-of-function models."
    support: "Fig. 2; Fig. 4; Extended Data Fig. 7"
    papers:
      - Gulen_nature_2023
  - chain_id: aged_brain_microglia
    step: 4
    source: neurodegeneration
    target: cognitive_decline
    rel: drives
    evidence_strength: perturbation_supported
    context: "STING inhibition improves aged-mouse spatial and associative memory, and microglial CGAS gain-of-function impairs memory."
    support: "Fig. 1h; Fig. 4"
    papers:
      - Gulen_nature_2023
  - chain_id: microglial_mtDNA_sensor
    step: 1
    source: mitochondrial_dysfunction
    target: cytoplasmic_mtDNA
    rel: produces
    evidence_strength: direct_measured
    context: "Old microglia show cytosolic DNA derived from perturbed mitochondria."
    support: "Fig. 3"
    papers:
      - Gulen_nature_2023
  - chain_id: microglial_mtDNA_sensor
    step: 2
    source: cytoplasmic_mtDNA
    target: CGAS
    rel: activates
    evidence_strength: direct_measured
    context: "Cytosolic mitochondrial DNA in old microglia engages CGAS activity."
    support: "Fig. 3"
    papers:
      - Gulen_nature_2023
  - chain_id: microglial_mtDNA_sensor
    step: 3
    source: CGAS
    target: STING1
    rel: activates
    evidence_strength: canonical_inferred
    context: "CGAS-to-STING1 signaling is the canonical downstream route from cytosolic DNA sensing and is supported by the STING-dependent old-brain phenotype."
    support: "Fig. 3; Fig. 2"
    papers:
      - Gulen_nature_2023
  - chain_id: CGAS_GOF_microglia
    step: 1
    source: CGAS
    target: microglial_activation
    rel: drives
    evidence_strength: perturbation_supported
    context: "Single-nucleus RNA-seq in a CGAS gain-of-function mouse model shows that microglial CGAS engagement is sufficient to direct ageing-associated reactive microglial transcriptional states."
    support: "Fig. 4; Extended Data Fig. 8"
    papers:
      - Gulen_nature_2023
  - chain_id: CGAS_GOF_microglia
    step: 2
    source: CGAS
    target: neurodegeneration
    rel: drives
    evidence_strength: perturbation_supported
    context: "Microglial CGAS gain-of-function promotes bystander cell inflammation, neurotoxicity, and impaired memory capacity."
    support: "Fig. 4; Extended Data Fig. 8"
    papers:
      - Gulen_nature_2023

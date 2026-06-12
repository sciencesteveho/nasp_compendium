paper:
  LopezPolo_natcomms_2024:
    cite: "López-Polo V, Maus M, Zacharioudakis E, Lafarga M, Stephan-Otto Attolini C, Marques FDM, Kovatcheva M, Gavathiotis E, Serrano M. Release of mitochondrial dsRNA into the cytosol is a key driver of the inflammatory phenotype of senescent cells. Nature Communications 2024."
    url: "https://doi.org/10.1038/s41467-024-51363-0"
    summary: "Senescent cells release mitochondrial dsRNA into the cytosol, where DDX58/IFIH1-MAVS signaling drives SASP; PNPT1 and ADAR loss sensitize this pathway and MFN1 supports mt-dsRNA/MAVS activation."
    nucleic_acid_sensors:
      - DDX58
      - IFIH1
      - MAVS
    genes:
      - POLRMT
      - PNPT1
      - ADAR
      - DDX58
      - IFIH1
      - MAVS
      - MFN1
      - MFN2
      - BAX
      - BAK1
      - IL6
      - IL1B
      - CXCL8
      - CCL2
    pathways:
      - RIG-I/MDA5-MAVS
      - SASP
      - type_I_IFN
    cell_types:
      - IMR90
      - BJ_fibroblasts
      - senescent_fibroblasts
      - fibrotic_lung
      - aged_mouse_tissues
      - melanoma_xenograft
    mechanisms:
      - cellular_senescence
      - cytoplasmic_mt_dsRNA
      - cytosolic_RNA_sensing
      - mt_dsRNA_release
      - BAX/BAK_pore
      - tissue_inflammation
      - fibrosis
      - mitochondrial_dysfunction
    model_systems:
      - human_in_vitro
      - human_tissue_explant
      - mouse_in_vivo
    evidence_type:
      - cytokine_array
      - ELISA
      - genetic_KO
      - immunoblot
      - immunofluorescence
      - pharmacological_inhibition
      - proteomics
      - RT_qPCR
      - siRNA_knockdown
    notes: >
      1. Tissue/organ: senescent fibroblasts, fibrotic/aged tissues, B16-F10 and
      SK-MEL-103 tumor senescence models.
      2. Species: human and mouse.
      3. Age range or comparison: senescent cells, fibrotic tissues, old mice.
      4. Sex-specific effects: not central.
      5. Disease context: senescence-associated inflammation, fibrosis, and therapy-induced senescence.
      The paper supports a mt-dsRNA-to-MAVS SASP axis. POLRMT inhibition reduces
      mt-dsRNA substrate; PNPT1 loss increases mt-dsRNA accumulation; ADAR loss
      increases sensing potency; MFN1, but not MFN2, supports the axis. BAX/BAK
      are presented as release machinery in the summary model.
    relevance_to_project: >
      Look for senescent cells with cytosolic J2/dsRNA signal, mitochondrial RNA
      signatures, low PNPT1/ADAR, DDX58/IFIH1/MAVS activity, MFN1 dependence, and
      SASP reduction after POLRMT or mitofusin inhibition.

edges:
  - chain_id: senescence_mt_dsRNA_MAVS_SASP
    step: 1
    source: cellular_senescence
    target: cytoplasmic_mt_dsRNA
    rel: induces
    evidence_strength: direct_measured
    context: "Multiple senescence triggers produce cytosolic dsRNA foci that map to mitochondrial dsRNA by imaging/fractionation and are reduced by POLRMT inhibition."
    support: "Fig. 1; Fig. 2"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: senescence_mt_dsRNA_MAVS_SASP
    step: 2
    source: POLRMT
    target: cytoplasmic_mt_dsRNA
    rel: drives
    evidence_strength: perturbation_supported
    context: "POLRMT inhibition with IMT1 lowers mt-dsRNA production/accumulation and attenuates the SASP, placing mitochondrial transcription upstream of the dsRNA substrate."
    support: "Fig. 2; Fig. 5"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: senescence_mt_dsRNA_MAVS_SASP
    step: 3
    source: cytoplasmic_mt_dsRNA
    target: DDX58
    rel: activates
    evidence_strength: perturbation_supported
    context: "RIG-I/DDX58 inhibition or knockdown reduces SASP expression while preserving broad senescence hallmarks."
    support: "Fig. 2; Supplementary figures"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: senescence_mt_dsRNA_MAVS_SASP
    step: 4
    source: cytoplasmic_mt_dsRNA
    target: IFIH1
    rel: activates
    evidence_strength: perturbation_supported
    context: "MDA5/IFIH1 inhibition or knockdown reduces SASP expression downstream of cytosolic mt-dsRNA."
    support: "Fig. 2; Supplementary figures"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: senescence_mt_dsRNA_MAVS_SASP
    step: 5
    source: DDX58
    target: MAVS
    rel: activates
    evidence_strength: canonical_inferred
    context: "RIG-I signals through MAVS canonically; the paper tests MAVS necessity for the same SASP axis."
    support: "Fig. 2"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: senescence_mt_dsRNA_MAVS_SASP
    step: 6
    source: IFIH1
    target: MAVS
    rel: activates
    evidence_strength: canonical_inferred
    context: "MDA5 signals through MAVS canonically; the paper tests MAVS necessity for the same SASP axis."
    support: "Fig. 2"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: senescence_mt_dsRNA_MAVS_SASP
    step: 7
    source: MAVS
    target: SASP
    rel: drives
    evidence_strength: perturbation_supported
    context: "MAVS inhibition/knockdown reduces SASP gene expression and secreted inflammatory factors while preserving other senescence hallmarks."
    support: "Fig. 2; Fig. 3"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: PNPT1_ADAR_sensitization
    step: 1
    source: cellular_senescence
    target: PNPT1
    rel: downregulates
    evidence_strength: direct_measured
    context: "PNPT1 levels decline in senescent cells."
    support: "Fig. 3"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: PNPT1_ADAR_sensitization
    step: 2
    source: PNPT1
    target: cytoplasmic_mt_dsRNA
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "PNPT1 mitigates mitochondrial dsRNA accumulation; PNPT1 reduction increases mt-dsRNA burden in senescent cells."
    support: "Fig. 3"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: PNPT1_ADAR_sensitization
    step: 3
    source: cellular_senescence
    target: ADAR
    rel: downregulates
    evidence_strength: direct_measured
    context: "ADAR1/ADAR levels decline in senescent cells."
    support: "Fig. 3"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: PNPT1_ADAR_sensitization
    step: 4
    source: ADAR
    target: cytosolic_RNA_sensing
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "ADAR editing normally reduces the inflammatory potency of dsRNA; ADAR loss hypersensitizes senescent cells to mt-dsRNA sensing."
    support: "Fig. 3"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: mt_dsRNA_release
    step: 1
    source: BAX/BAK_pore
    target: cytoplasmic_mt_dsRNA
    rel: forms_pore_for
    evidence_strength: perturbation_supported
    context: "The model places mitochondrial budding/rupture and BAX/BAK-dependent permeabilization upstream of mt-dsRNA release into the cytosol."
    support: "Fig. 6"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: MFN1_axis
    step: 1
    source: MFN1
    target: cytoplasmic_mt_dsRNA
    rel: drives
    evidence_strength: perturbation_supported
    context: "MFN1 depletion or mitofusin inhibition attenuates mt-dsRNA formation and downstream SASP; MFN2 does not show the same requirement."
    support: "Fig. 4; Fig. 6"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: MFN1_axis
    step: 2
    source: MFN1
    target: MAVS
    rel: activates
    evidence_strength: perturbation_supported
    context: "MFN1 is required for activation of the mt-dsRNA/MAVS/SASP axis, potentially through mitochondrial architecture and MAVS activation."
    support: "Fig. 4; Fig. 6"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: MFN1_axis
    step: 3
    source: MFN2
    target: MAVS
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "MFN2 perturbation does not phenocopy MFN1 requirement for the mt-dsRNA/MAVS/SASP axis."
    support: "Fig. 4"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: in_vivo_inflammation
    step: 1
    source: cellular_senescence
    target: cytoplasmic_mt_dsRNA
    rel: induces
    evidence_strength: direct_measured
    context: "Senescent cells in fibrotic and aged tissues contain dsRNA foci."
    support: "Fig. 5"
    papers:
      - LopezPolo_natcomms_2024
  - chain_id: in_vivo_inflammation
    step: 2
    source: cytoplasmic_mt_dsRNA
    target: tissue_inflammation
    rel: drives
    evidence_strength: perturbation_supported
    context: "IMT1/POLRMT inhibition lowers systemic inflammation associated with senescence in mouse models."
    support: "Fig. 5"
    papers:
      - LopezPolo_natcomms_2024

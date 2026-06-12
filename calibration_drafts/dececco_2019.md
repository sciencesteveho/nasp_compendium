paper:
  DeCecco_nature_2019:
    cite: "De Cecco M, Ito T, Petrashen AP, Elias AE, Skvir NJ, Criscione SW, Caligiana A, Brocculi G, Adney EM, Boeke JD, et al. L1 drives IFN in senescent cells and promotes age-associated inflammation. Nature 2019."
    url: "https://doi.org/10.1038/s41586-018-0784-9"
    summary: "Late senescence derepresses L1, producing cytoplasmic retroelement cDNA that activates CGAS-STING1/type-I-IFN signaling and sustains the mature SASP and inflammaging."
    nucleic_acid_sensors:
      - CGAS
      - STING1
      - MAVS
    genes:
      - RB1
      - RBL1
      - RBL2
      - FOXA1
      - TREX1
      - CGAS
      - STING1
      - IFNAR1
      - IFNAR2
      - IFNA1
      - IFNB1
      - IRF7
      - CCL2
      - IL6
      - MMP3
      - IL1B
    pathways:
      - cGAS-STING
      - type_I_IFN
      - SASP
      - L1_retrotransposition
    cell_types:
      - human_fibroblasts
      - IMR90
      - WI38
      - aged_mouse_tissues
      - human_skin
    mechanisms:
      - cellular_senescence
      - retrotransposon_derepression
      - cytoplasmic_retroelement_cDNA
      - inflammaging
      - tissue_inflammation
    model_systems:
      - human_in_vitro
      - human_cohort
      - mouse_in_vivo
    evidence_type:
      - bulk_RNA_seq
      - ChIP_qPCR
      - genetic_KO
      - IHC
      - immunoblot
      - immunofluorescence
      - pharmacological_inhibition
      - RT_qPCR
      - shRNA_knockdown
    notes: >
      1. Tissue/organ: human fibroblasts, human skin, and aged mouse tissues.
      2. Species: human and mouse.
      3. Age range or comparison: late senescence in vitro and old mice treated with lamivudine.
      4. Sex-specific effects: not addressed.
      5. Disease context: age-associated sterile inflammation.
      The mechanism separates transcriptional derepression of L1 from reverse-transcribed
      cytoplasmic L1 cDNA. 3TC and K-9 are kept in context as reverse transcriptase
      specificity controls. IFN-I is late-onset and maintains the mature SASP.
    relevance_to_project: >
      In senescent cell atlases, look for late-senescent L1/ORF1p, IFNA/IFNB1,
      ISG modules, CGAS/STING1 dependence, and IFNAR-linked maintenance of CCL2,
      IL6, and MMP3 rather than early IL1B.

edges:
  - chain_id: senescence_L1_IFN_SASP
    step: 1
    source: cellular_senescence
    target: RB1
    rel: downregulates
    evidence_strength: direct_measured
    context: "RB1 expression declines during senescence, while RBL1/RBL2 do not show the same decline."
    support: "Fig. 2a; Extended Data Fig. 4b"
    papers:
      - DeCecco_nature_2019
  - chain_id: senescence_L1_IFN_SASP
    step: 2
    source: RB1
    target: retrotransposon_derepression
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "RB1 binds L1 5-prime UTRs in proliferating cells and is lost from L1 during senescence; RB1 knockdown induces L1, and RB1 overexpression restrains L1."
    support: "Fig. 2a-e; Extended Data Fig. 4"
    papers:
      - DeCecco_nature_2019
  - chain_id: senescence_L1_IFN_SASP
    step: 3
    source: cellular_senescence
    target: FOXA1
    rel: upregulates
    evidence_strength: direct_measured
    context: "FOXA1 increases during late senescence and binds/opens L1 loci."
    support: "Fig. 2f-j"
    papers:
      - DeCecco_nature_2019
  - chain_id: senescence_L1_IFN_SASP
    step: 4
    source: FOXA1
    target: retrotransposon_derepression
    rel: drives
    evidence_strength: perturbation_supported
    context: "FOXA1 knockdown reduces L1 expression, supporting FOXA1 as a positive regulator of L1 derepression."
    support: "Fig. 2f-j; Extended Data Fig. 4"
    papers:
      - DeCecco_nature_2019
  - chain_id: senescence_L1_IFN_SASP
    step: 5
    source: cellular_senescence
    target: TREX1
    rel: downregulates
    evidence_strength: direct_measured
    context: "TREX1 expression decreases in senescent cells, removing a cytoplasmic DNA surveillance barrier."
    support: "Extended Data Fig. 4a"
    papers:
      - DeCecco_nature_2019
  - chain_id: senescence_L1_IFN_SASP
    step: 6
    source: retrotransposon_derepression
    target: cytoplasmic_retroelement_cDNA
    rel: produces
    evidence_strength: perturbation_supported
    context: "Long-term BrdU labeling, L1 DNA FISH/qPCR, DNA-RNA hybrid staining, L1 shRNA, and 3TC show that derepressed L1 generates reverse-transcribed cytoplasmic L1 cDNA/RNA-DNA hybrids."
    support: "Fig. 3a,c; Extended Data Fig. 5d,e,g-k; Extended Data Fig. 6a-e"
    papers:
      - DeCecco_nature_2019
  - chain_id: senescence_L1_IFN_SASP
    step: 7
    source: TREX1
    target: cytoplasmic_retroelement_cDNA
    rel: suppresses
    evidence_strength: canonical_inferred
    context: "TREX1 is a canonical cytoplasmic DNA exonuclease, and its decline is proposed to allow L1 cDNA accumulation; the paper measures TREX1 loss but does not perform TREX1 rescue."
    support: "Extended Data Fig. 4a"
    papers:
      - DeCecco_nature_2019
  - chain_id: senescence_L1_IFN_SASP
    step: 8
    source: cytoplasmic_retroelement_cDNA
    target: CGAS
    rel: activates
    evidence_strength: perturbation_supported
    context: "3TC blocks L1 cDNA and IFN-I without reducing L1 RNA; CGAS knockdown inhibits IFN-I in late senescent and 3x cells."
    support: "Fig. 3a,b; Extended Data Fig. 5l; Extended Data Fig. 7c,d"
    papers:
      - DeCecco_nature_2019
  - chain_id: senescence_L1_IFN_SASP
    step: 9
    source: CGAS
    target: STING1
    rel: activates
    evidence_strength: perturbation_supported
    context: "CGAS or STING1 knockdown suppresses IFN-I responses downstream of L1 cDNA."
    support: "Extended Data Fig. 5l; Extended Data Fig. 7c,d"
    papers:
      - DeCecco_nature_2019
  - chain_id: senescence_L1_IFN_SASP
    step: 10
    source: STING1
    target: type_I_IFN
    rel: drives
    evidence_strength: perturbation_supported
    context: "STING1 knockdown reduces IFNA/IFNB1/ISG induction in late senescent and 3x cells."
    support: "Extended Data Fig. 5l; Extended Data Fig. 7c,d"
    papers:
      - DeCecco_nature_2019
  - chain_id: senescence_L1_IFN_SASP
    step: 11
    source: type_I_IFN
    target: SASP
    rel: drives
    evidence_strength: perturbation_supported
    context: "IFNAR1/IFNAR2 CRISPR ablation reduces late SASP markers CCL2, IL6, and MMP3, but not early IL1B, in replicative and stress-induced senescence."
    support: "Fig. 3d; Extended Data Fig. 5m"
    papers:
      - DeCecco_nature_2019
  - chain_id: SASP_components
    step: 1
    source: SASP
    target: CCL2
    rel: contains
    evidence_strength: direct_measured
    context: "CCL2 is a late SASP marker reduced by 3TC, L1 shRNA, cGAS/STING1 knockdown, and IFNAR loss."
    support: "Fig. 3d,f; Extended Data Fig. 6f; Extended Data Fig. 7e"
    papers:
      - DeCecco_nature_2019
  - chain_id: SASP_components
    step: 2
    source: SASP
    target: IL6
    rel: contains
    evidence_strength: direct_measured
    context: "IL6 is a late SASP marker reduced by L1/IFN-I pathway perturbation."
    support: "Fig. 3d,f; Extended Data Fig. 6f; Extended Data Fig. 7e"
    papers:
      - DeCecco_nature_2019
  - chain_id: SASP_components
    step: 3
    source: SASP
    target: MMP3
    rel: contains
    evidence_strength: direct_measured
    context: "MMP3 is a late SASP marker reduced by L1/IFN-I pathway perturbation."
    support: "Fig. 3d,f; Extended Data Fig. 6f; Extended Data Fig. 7e"
    papers:
      - DeCecco_nature_2019
  - chain_id: SASP_components
    step: 4
    source: SASP
    target: IL1B
    rel: contains
    evidence_strength: direct_measured
    context: "IL1B is an early SASP marker that is not materially affected by 3TC or IFNAR loss."
    support: "Fig. 3d,f"
    papers:
      - DeCecco_nature_2019
  - chain_id: in_vivo_aging
    step: 1
    source: retrotransposon_derepression
    target: inflammaging
    rel: drives
    evidence_strength: perturbation_supported
    context: "Lamivudine treatment of aged mice reduces IFN-I activation and age-associated inflammation across multiple tissues, implicating L1 reverse transcriptase activity."
    support: "Fig. 4; Extended Data Fig. 8"
    papers:
      - DeCecco_nature_2019
  - chain_id: specificity_controls
    step: 1
    source: MAVS
    target: type_I_IFN
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "RNA-sensing pathway perturbation does not explain the L1 cDNA-driven IFN-I response as strongly as CGAS/STING1."
    support: "Extended Data Fig. 7c,d"
    papers:
      - DeCecco_nature_2019
  - chain_id: specificity_controls
    step: 2
    source: RBL1
    target: retrotransposon_derepression
    rel: does_not_drive
    evidence_strength: direct_measured
    context: "RBL1 does not decline during senescence like RB1 and is not positioned as the L1 derepression driver."
    support: "Extended Data Fig. 4b"
    papers:
      - DeCecco_nature_2019

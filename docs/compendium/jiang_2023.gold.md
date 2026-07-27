
paper:

  Jiang_natcomms_2023:
    cite: "Jiang Y, Sun S, Quan Y, Wang X, You Y, Zhang X, Zhang Y, Liu Y, Wang B, Xu H, Cao X. Nuclear RPSA senses viral nucleic acids to promote the innate inflammatory response. Nat Commun. 2023;14:8455."
    url: "https://doi.org/10.1038/s41467-023-43784-0"
    summary: "The 40S ribosomal protein RPSA acts as a nuclear innate sensor: it binds HSV-1 genomic DNA and IAV genomic RNA in the nucleus, becomes phosphorylated at Tyr204, recruits the ISWI chromatin remodeler SMARCA5, and increases chromatin accessibility and H3K4me3 at proinflammatory cytokine promoters (Il1b, Il6, Il12b, Tnfa), enabling P65/NF-kB and RNA polymerase II enrichment there. RPSA thereby selectively promotes proinflammatory cytokine transcription without affecting IFN-beta or the upstream NF-kB/MAPK/IRF3 signaling cascades; Rpsa-deficient mice show higher viral load and lower cytokines but unchanged IFN-beta."
    nucleic_acid_sensors:
      - RPSA
    genes:
      - RPSA
      - SMARCA5
      - RELA
      - IL1B
      - IL6
      - IL12B
      - TNF
      - IL1A
      - IFNB1
      - IRF3
    pathways:
      - NF-kB
      - type_I_IFN
      - proinflammatory_cytokines
    cell_types:
      - peritoneal_macrophages
      - bone_marrow_derived_macrophages
      - RAW264.7
      - A549
      - MLE_12
      - mouse_embryonic_fibroblasts
      - HEK293T
    mechanisms:
      - nuclear_nucleic_acid_sensing
      - viral_nucleic_acids
      - chromatin_accessibility
      - histone_methylation
      - tyrosine_phosphorylation
      - epigenetic_remodeling
    model_systems:
      - human_in_vitro
      - mouse_in_vitro
      - mouse_in_vivo
      - mouse_genetic_model
    evidence_type:
      - RNAi_screen
      - genetic_KO
      - overexpression
      - RT_qPCR
      - immunoblot
      - ELISA
      - EMSA
      - CoIP_MS
      - ChIP_seq
      - ATAC_seq
      - DNase_I_hypersensitivity
      - immunofluorescence
      - mutagenesis
      - histology
    notes: >
      1. Tissue/organ: macrophages (peritoneal, BMDM, RAW264.7), lung
      epithelial (A549, MLE-12), MEFs, HEK293T in vitro; mouse lung, brain,
      liver, and blood in vivo (Rpsa-fl/fl Lyz-Cre myeloid conditional KO).
      2. Species: human and mouse; RPSA is sequence-conserved (rmRPSA and
      rhRPSA both bind viral nucleic acids).
      3. Age range or comparison: not an aging study; comparisons are
      Rpsa wild-type vs knockdown/knockout under nuclear-replicating virus
      challenge (HSV-1, IAV).
      4. Sex-specific effects: not addressed.
      5. Disease context: innate antiviral inflammation to nuclear-replicating
      viruses; relevant by extension to NF-kB-driven proinflammatory cytokine
      output as distinct from the type-I IFN arm.
      Spine: nuclear RPSA binds viral DNA/RNA; HSV-1/IAV infection drives
      RPSA Tyr204 phosphorylation; phospho-RPSA recruits SMARCA5 (ISWI); the
      RPSA-SMARCA5 module increases chromatin accessibility and H3K4me3 at
      proinflammatory cytokine promoters; this permits P65 and RNA Pol II
      enrichment there; the net output is proinflammatory cytokine
      transcription (Il1b, Il6, Il12b, Tnfa). Key negatives: RPSA does NOT
      affect IFN-beta (Ifnb) expression, the Ifnb promoter, IRF3 activation,
      or the NF-kB/MAPK signaling cascades themselves; IRF3 is excluded from
      the RPSA/SMARCA5 complex. RPSA is dispensable for cytoplasmic ligand
      responses (poly dA:dT, poly I:C, CpG, cGAMP, TNF-alpha).
      RPSA = 40S ribosomal protein SA (295 aa; N-term aa1-209 ribosomal,
      C-term aa210-295 laminin/interaction); P65 = RELA; ISWI catalytic
      subunit = SMARCA5.
    relevance_to_project: >
      Adds a nucleus-localized sensor that routes to NF-kB-driven
      proinflammatory cytokines while explicitly bypassing the type-I IFN
      arm. This is a clean calibration case for the sensing-vs-output and
      NF-kB-vs-IFN branch distinctions: RPSA is NASP-competent and drives a
      proinflammatory (not interferon) output, and the paper supplies an
      exhaustive set of negative controls (Ifnb, IRF3, cytoplasmic ligands)
      that a curator must preserve rather than collapse into a generic
      "sensor drives inflammation" edge. In atlas data, treat RPSA as a
      candidate modulator whose nuclear phospho-state and SMARCA5
      co-expression may gate proinflammatory cytokine output independently of
      ISG signatures.

edges:

# RPSA physically binds viral nucleic acids in the nucleus (DNA and RNA).
  - chain_id: rpsa_nuclear_sensing
    step: 1
    source: RPSA
    target: viral_nucleic_acids
    rel: binds_recruits
    evidence_strength: direct_measured
    context: "Nuclear RPSA co-immunoprecipitates with HSV-1 genomic DNA and IAV
              genomic RNA in infected BMDMs, and co-localizes with EdU-labeled
              HSV-1 DNA and EU-labeled IAV RNA in the nucleus. Recombinant mouse
              and human RPSA directly bind biotin-HSV-60 dsDNA and IAV gRNA;
              binding is competed by unlabeled dsDNA (HSV-60, VACV-70, poly
              dA:dT, poly dI:dC) and naked genomic DNA but not nucleosomes.
              Only full-length RPSA (295 aa) binds; the interaction is
              sequence-conserved between species."
    support: "Fig. 1d-m; Supplementary Fig. 1g"
    tier: core
    papers:
      - Jiang_natcomms_2023

# Viral infection induces RPSA Tyr204 phosphorylation specifically in the nucleus.
  - chain_id: rpsa_nuclear_sensing
    step: 2
    source: viral_nucleic_acids
    target: RPSA
    rel: induces
    evidence_strength: direct_measured
    context: "HSV-1 and IAV infection selectively increase tyrosine (not
              serine/threonine or acetyl) phosphorylation of RPSA, and only the
              nuclear RPSA pool is phosphorylated within 4 h; cytoplasmic VACV
              infection and cGAMP do not induce it. Mutation Tyr204-to-Ala
              (Y204A) abolishes infection-induced RPSA tyrosine phosphorylation
              and Il1b induction, whereas phosphomimetic Y204D constitutively
              elevates Il1b, defining Tyr204 as the induced modification."
    support: "Fig. 4e-i; Supplementary Fig. 6e-g"
    tier: core
    papers:
      - Jiang_natcomms_2023

# Phospho-Tyr204 RPSA recruits the ISWI remodeler SMARCA5.
  - chain_id: rpsa_nuclear_sensing
    step: 3
    source: RPSA
    target: SMARCA5
    rel: binds_recruits
    evidence_strength: perturbation_supported
    context: "CoIP-MS identifies SMARCA5 (ISWI catalytic subunit) as the top
              RPSA-interacting protein after HSV-1 infection, confirmed by
              nuclear co-IP; the interaction increases with HSV-1 and IAV. The
              interaction is Tyr204-dependent: RPSA-Y204A shows markedly reduced
              SMARCA5 binding whereas Y204D binds persistently. IRF3 is excluded
              from the RPSA/SMARCA5 complex."
    support: "Fig. 4a, 4b, 4j; Supplementary Fig. 6a-d"
    tier: core
    papers:
      - Jiang_natcomms_2023

# RPSA-SMARCA5 increases chromatin accessibility + H3K4me3 at cytokine promoters.
  - chain_id: rpsa_nuclear_sensing
    step: 4
    source: SMARCA5
    target: chromatin_accessibility
    rel: activates
    evidence_strength: perturbation_supported
    context: "ATAC-seq and DNase I hypersensitivity show Rpsa deletion reduces
              chromatin accessibility at Il1b, Il6, Il12b and Tnfa promoters
              (but not Ifnb) after HSV-1 infection; H3K4me3 ChIP-seq/ChIP-qPCR
              show reduced H3K4me3 at the same proinflammatory promoters (not
              Ifnb). SMARCA5 is enriched at Il1b/Il6/Il12b promoters in an
              Rpsa-dependent manner, and SMARCA5-driven rescue of Il1b/Il6
              requires RPSA. Accessibility is STING-independent (STING inhibitor
              and cGAMP do not alter it)."
    support: "Fig. 3b-g; Fig. 4c, 4d; Supplementary Fig. 5b-g"
    tier: core
    papers:
      - Jiang_natcomms_2023

# Increased accessibility permits P65/NF-kB enrichment at cytokine promoters.
  - chain_id: rpsa_nuclear_sensing
    step: 5
    source: chromatin_accessibility
    target: RELA
    rel: binds_recruits
    evidence_strength: perturbation_supported
    context: "P65 ChIP-seq/ChIP-qPCR show Rpsa deficiency reduces P65 (RELA)
              enrichment at Il1b, Il6 and Il12b promoters (not Ifnb), and the
              H3K4me3 signal is lost specifically at NF-kB-binding motifs.
              SMARCA5-P65 association is HSV-1-induced but lost in Rpsa-deficient
              cells, and RPSA-P65 association is lost when SMARCA5 is knocked
              down, placing accessibility upstream of P65 promoter occupancy.
              RNA Pol II enrichment at the same promoters is likewise
              Rpsa-dependent."
    support: "Fig. 5a, 5c-h; Supplementary Fig. 7b-d"
    tier: core
    papers:
      - Jiang_natcomms_2023

# Net output: proinflammatory cytokine transcription (Il1b, Il6, Il12b, Tnfa).
  - chain_id: rpsa_nuclear_sensing
    step: 6
    source: RELA
    target: proinflammatory_cytokines
    rel: drives
    evidence_strength: perturbation_supported
    context: "Rpsa loss (knockdown, myeloid KO, iKO) reduces Il1a, Il1b, Il6,
              Il12b and Tnfa mRNA and secreted protein across macrophages, lung
              epithelia and MEFs under HSV-1/IAV; RPSA overexpression raises
              them; rescue requires wild-type or Y204D RPSA. The RPSA effect is
              abolished by NF-kB inhibitor BAY11-7082, showing complete
              dependence on NF-kB signaling. RPSA depletion does not change HSV-1
              DNA level or the NF-kB/MAPK signaling cascade activation itself."
    support: "Fig. 2a-d; Fig. 5b; Fig. 6b-f"
    tier: core
    papers:
      - Jiang_natcomms_2023

# In vivo requirement: RPSA needed for antiviral inflammation, not IFN.
  - chain_id: rpsa_nuclear_sensing
    step: 7
    source: RPSA
    target: proinflammatory_cytokines
    rel: required_for
    evidence_strength: perturbation_supported
    context: "Rpsa-fl/fl Lyz-Cre mice show higher HSV-1 load in lung and brain
              and higher IAV load in lung, with significantly lower Il1b, Il6,
              Il12b and Tnfa (mRNA and serum protein) and reduced lung/liver
              inflammation by histology and IHC, establishing RPSA as required
              for the in vivo proinflammatory response to nuclear-replicating
              viruses."
    support: "Fig. 6a-l; Supplementary Fig. 8a"
    tier: supporting
    papers:
      - Jiang_natcomms_2023

# CORE NEGATIVE: RPSA does NOT drive type-I IFN / IFN-beta.
  - chain_id: rpsa_ifn_specificity
    step: 1
    source: RPSA
    target: IFNB1
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "Across every system, Rpsa loss leaves Ifnb (IFN-beta) mRNA and
              protein unchanged (myeloid KO serum IFN-beta P=0.59; BMDM Ifnb
              P=0.70) and does not reduce ISGs (Ifit1, Rsad2). ATAC-seq, DNase I,
              H3K4me3 and P65/Pol II ChIP all show the Ifnb promoter is
              unaffected by Rpsa deletion, and IRF3 is excluded from the
              RPSA/SMARCA5 complex. This IFN-independence is a central claim and
              must not be collapsed into a generic sensor-drives-IFN edge."
    support: "Fig. 2a, 2b; Fig. 3c-g; Fig. 4a; Fig. 5g, 5h; Supplementary Fig. 1c"
    tier: core
    papers:
      - Jiang_natcomms_2023

# CORE NEGATIVE: RPSA does NOT act through cytoplasmic ligand pathways.
  - chain_id: rpsa_ifn_specificity
    step: 2
    source: RPSA
    target: NF-kB
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "Rpsa deficiency does not affect proinflammatory cytokine induction
              by cytoplasmic ligands: TLR9 ligand CpG ODN, poly dA:dT, TLR3/RIG-I
              ligand poly I:C, TNF-alpha, or cGAMP. RPSA also does not alter the
              nuclear translocation of phospho-P65, P42/44, P38 or IRF3. RPSA
              acts on chromatin accessibility downstream of, and in parallel to,
              NF-kB activation rather than driving the NF-kB signaling cascade;
              asserting RPSA activates NF-kB signaling is the forbidden reading."
    support: "Fig. 2f-i; Supplementary Fig. 3e-g, Fig. 4a-c"
    tier: supporting
    status: excluded
    score_exclude: true
    papers:
      - Jiang_natcomms_2023

# FORBIDDEN SHORTCUT: RPSA "drives proinflammatory cytokines" skipping SMARCA5/chromatin.
  - chain_id: forbidden_shortcut
    step: 1
    source: RPSA
    target: proinflammatory_cytokines
    rel: drives
    evidence_strength: perturbation_supported
    context: "ANTI-EDGE. RPSA depletion does reduce proinflammatory cytokines,
              but naming RPSA as their direct driver erases the paper's discovery
              — the Tyr204 phosphorylation -> SMARCA5/ISWI recruitment ->
              chromatin accessibility/H3K4me3 -> P65 enrichment epigenetic spine.
              A draft that emits this single edge as the mechanism has taken the
              forbidden shortcut."
    support: "n/a (anti-edge; see core steps 2-6)"
    tier: core
    status: forbidden_shortcut
    papers:
      - Jiang_natcomms_2023

# FORBIDDEN SHORTCUT: RPSA "drives NF-kB" collapsing the epigenetic mechanism into signaling.
  - chain_id: forbidden_shortcut
    step: 2
    source: RPSA
    target: RELA
    rel: activates
    evidence_strength: perturbation_supported
    context: "ANTI-EDGE. RPSA is required for P65/RELA promoter occupancy, but
              asserting RPSA activates RELA (the NF-kB signaling cascade) is
              explicitly contradicted: RPSA does not affect P65 phosphorylation
              or nuclear translocation. RPSA enables P65 to bind chromatin by
              remodeling accessibility, not by activating NF-kB signaling."
    support: "n/a (anti-edge; see core step 5 and Supplementary Fig. 4b, c)"
    tier: core
    status: forbidden_shortcut
    papers:
      - Jiang_natcomms_2023

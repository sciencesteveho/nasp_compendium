
paper:

  DeCecco_nature_2019:
    cite: "De Cecco M, Ito T, Petrashen AP, et al. L1 drives IFN in senescent cells and promotes age-associated inflammation. Nature. 2019;566(7742):73-78."
    url: "https://doi.org/10.1038/s41586-018-0784-9"
    summary: "In late cellular senescence, convergent failure of RB1, FOXA1 and TREX1 surveillance derepresses L1 retrotransposons; L1 reverse transcriptase makes cytoplasmic cDNA that activates cGAS-STING1 to drive a type-I interferon response, which via JAK-STAT amplifies the mature/late SASP (CCL2, IL6, MMP3) but not the early IL1B SASP. The RT inhibitor lamivudine (3TC) blocks the axis and reverses age phenotypes; the non-RT-inhibitory analogue K-9 does not, establishing RT-dependence. The trigger is cDNA, not L1 RNA."
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
      1. Tissue/organ: skin (human), white adipose, liver, skeletal muscle,
      kidney (mouse); lung-derived fibroblasts (in vitro).
      2. Species: human (LF1/IMR90/WI38 fibroblasts and skin biopsy) and mouse
      (C57BL/6J, in vivo).
      3. Age range or comparison: in vitro early passage vs 8 weeks (early
      senescence) vs 16 weeks (late senescence); in vivo 5 months (young) vs
      26-29 months (aged).
      4. Sex-specific effects: both sexes; L1/IFN-I rise with age in both. No
      sex-specific differences reported.
      5. Disease context: normal aging and cellular senescence; proposed
      relevance to inflammaging.
      Mechanistic spine (all core): retrotransposon (L1) derepression makes
      cytoplasmic_retroelement_cDNA (L1 RT, 3TC-blocked); cDNA activates CGAS;
      CGAS makes cGAMP; cGAMP activates STING1; STING1 drives type_I_IFN; IFN
      signals via JAK-STAT; JAK-STAT amplifies the late SASP. RT activity is
      required for IFN-I (3TC vs K-9), and type_I_IFN does NOT drive the early
      IL1B SASP — the precise causal boundary of the paper.
      6. Equivalence and specificity: RB1/FOXA1/TREX1 are three convergent
      surveillance failures upstream of L1 (grouped as l1_surveillance,
      supporting). The late-SASP markers IL6/CCL2/MMP3 are one program read out
      at STING1 (sting_late_sasp) and at JAK-STAT (jakstat_late_sasp). RBL1/RBL2
      unchanged is an RB1-paralog specificity control. Forbidden shortcuts:
      naming L1 cDNA or L1 derepression as the direct driver of type_I_IFN in
      place of the cGAS-STING spine.
    relevance_to_project: >
      Adds the retroelement (L1 cDNA) ligand to the DNA-sensing arm of the NASP
      spine and, unlike Dou, an explicit type-I-IFN -> JAK-STAT -> late-SASP
      output distinct from the early IL1B SASP. In atlas or perturbation data,
      treat an IFN-high/JAK-STAT-high late-SASP signature with L1 derepression as
      the De Cecco readout, use the RT-dependence (3TC) and IL1B negative to
      separate the IFN-amplified late SASP from the IFN-independent early SASP,
      and treat TREX1 as a restriction factor whose loss licenses the axis.

edges:

# Supporting: senescence remodels L1 heterochromatin.
  - chain_id: l1_derepression
    step: 1
    source: cellular_senescence
    target: epigenetic_remodeling
    rel: induces
    evidence_strength: strong_correlative
    context: "Late senescence is accompanied by heterochromatin remodeling at L1
              loci (loss of repressive marks), the chromatin context that permits
              L1 transcriptional derepression."
    support: "Fig. 2a; Extended Data Fig. 4c"
    tier: supporting
    papers:
      - DeCecco_nature_2019

# Supporting equivalence l1_surveillance: RB1 loss derepresses L1.
  - chain_id: l1_surveillance
    step: 1
    source: RB1
    target: retrotransposon_derepression
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "RB1 knockdown derepresses L1; RB1 restrains L1 (bidirectional
              evidence). One of three convergent surveillance failures upstream of
              L1 derepression."
    support: "Fig. 2a, 2c, 2d; Extended Data Fig. 4b, 4c, 4g, 4h"
    tier: supporting
    equiv_group: l1_surveillance
    papers:
      - DeCecco_nature_2019

# Supporting equivalence l1_surveillance: FOXA1 gain drives L1 transcription.
  - chain_id: l1_surveillance
    step: 2
    source: FOXA1
    target: retrotransposon_derepression
    rel: drives
    evidence_strength: perturbation_supported
    context: "FOXA1 induction in senescence activates L1 promoters and drives L1
              transcription. Equivalent to RB1 and TREX1 loss as a surveillance
              failure feeding L1 derepression."
    support: "Fig. 2b, 2e; Extended Data Fig. 4d-h"
    tier: supporting
    equiv_group: l1_surveillance
    papers:
      - DeCecco_nature_2019

# Supporting equivalence l1_surveillance: TREX1 loss lets L1 cDNA accumulate.
  - chain_id: l1_surveillance
    step: 3
    source: TREX1
    target: retrotransposon_derepression
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "TREX1 (the cytoplasmic exonuclease that clears cDNA) falls in
              senescence; its loss lets L1 cDNA accumulate. The third convergent
              surveillance failure; grouped with RB1 and FOXA1."
    support: "Fig. 2f, 2g; Extended Data Fig. 4a, 4g, 4h"
    tier: supporting
    equiv_group: l1_surveillance
    papers:
      - DeCecco_nature_2019

# Core: L1 RT makes cytoplasmic cDNA (3TC-blocked).
  - chain_id: l1_cdna_cgas_sting_ifn
    step: 1
    source: retrotransposon_derepression
    target: cytoplasmic_retroelement_cDNA
    rel: produces
    evidence_strength: direct_measured
    context: "Derepressed L1 reverse transcriptase generates cytoplasmic L1 cDNA,
              detected in the cytosol and blocked by the RT inhibitor lamivudine
              (3TC). This is the ligand-generating step of the axis."
    support: "Fig. 3a-c; Extended Data Fig. 6a-e"
    tier: core
    papers:
      - DeCecco_nature_2019

# Core: L1 cDNA activates CGAS.
  - chain_id: l1_cdna_cgas_sting_ifn
    step: 2
    source: cytoplasmic_retroelement_cDNA
    target: CGAS
    rel: activates
    evidence_strength: perturbation_supported
    context: "Cytoplasmic L1 cDNA engages CGAS; CGAS knockdown suppresses the
              downstream IFN-I and late SASP, placing cDNA sensing at CGAS."
    support: "Extended Data Fig. 5l, 7c-e"
    tier: core
    papers:
      - DeCecco_nature_2019

# Core: CGAS makes cGAMP (canonical here).
  - chain_id: l1_cdna_cgas_sting_ifn
    step: 3
    source: CGAS
    target: cGAMP
    rel: produces
    evidence_strength: canonical_inferred
    context: "CGAS synthesizes cGAMP from the sensed cDNA. The catalytic step is
              the canonical cGAS-STING wiring, confirmed here by CGAS/STING1
              knockdown dependence of the downstream output."
    support: "main text p.75; Extended Data Fig. 5l, 7c"
    tier: core
    papers:
      - DeCecco_nature_2019

# Core: cGAMP activates STING1.
  - chain_id: l1_cdna_cgas_sting_ifn
    step: 4
    source: cGAMP
    target: STING1
    rel: activates
    evidence_strength: canonical_inferred
    context: "cGAMP binds and activates STING1; STING1 knockdown abolishes the
              IFN-I response to L1 cDNA, confirming the cGAMP -> STING1 axis is
              intact here."
    support: "Extended Data Fig. 5l, 7c-e"
    tier: core
    papers:
      - DeCecco_nature_2019

# Core: STING1 drives type-I IFN.
  - chain_id: l1_cdna_cgas_sting_ifn
    step: 5
    source: STING1
    target: type_I_IFN
    rel: drives
    evidence_strength: perturbation_supported
    context: "STING1 depletion suppresses the type-I interferon response in late
              senescence; the IFN-I program (IRF7, OAS1, STAT2 targets) is the
              emphasised output of the cGAS-STING axis here, distinct from Dou's
              NF-kB output."
    support: "Fig. 1d, 1e, 2h, 3b, 3e; Extended Data Fig. 3, 5l, 7c-d"
    tier: core
    papers:
      - DeCecco_nature_2019

# Core: type-I IFN signals via JAK-STAT.
  - chain_id: l1_cdna_cgas_sting_ifn
    step: 6
    source: type_I_IFN
    target: JAK-STAT
    rel: activates
    evidence_strength: perturbation_supported
    context: "Type-I IFN engages IFNAR1/2 -> JAK-STAT (STAT2 phosphorylation, IRF7
              induction). IFNAR1/2 knockout suppresses the late SASP, placing
              JAK-STAT between IFN-I and the amplified SASP."
    support: "Fig. 3b; Extended Data Fig. 5m, 7a"
    tier: core
    papers:
      - DeCecco_nature_2019

# Core: JAK-STAT amplifies late SASP (not IL1B).
  - chain_id: l1_cdna_cgas_sting_ifn
    step: 7
    source: JAK-STAT
    target: SASP
    rel: drives
    evidence_strength: perturbation_supported
    context: "JAK-STAT signaling amplifies the late/mature SASP (CCL2, IL6, MMP3).
              IFNAR1/2 loss reduces these but not the early IL1B SASP, defining the
              IFN-amplified late SASP as the output."
    support: "Fig. 3d, 3f; Extended Data Fig. 6f, 7b"
    tier: core
    papers:
      - DeCecco_nature_2019

# Core: L1 RT activity required for IFN-I (3TC vs K-9).
  - chain_id: rt_dependence
    step: 1
    source: retrotransposon_derepression
    target: type_I_IFN
    rel: required_for
    evidence_strength: perturbation_supported
    context: "The RT inhibitor 3TC suppresses IFN-I, whereas the non-RT-inhibitory
              analogue K-9 does not, showing L1 RT activity is required for the
              IFN-I response. The 3TC/K-9 contrast is the paper's central
              pharmacological/mechanistic claim, so this is core. It is a
              functional requirement edge, not a substitute for the cDNA -> cGAS ->
              STING spine, which is encoded separately."
    support: "Extended Data Fig. 7f, 7g, 9d"
    tier: core
    papers:
      - DeCecco_nature_2019

# Supporting equivalence sting_late_sasp: STING1 upregulates IL6.
  - chain_id: sting_late_sasp
    step: 1
    source: STING1
    target: IL6
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "STING1 knockdown reduces IL6, one marker of the late SASP program.
              IL6/CCL2/MMP3 are equivalent markers of the same STING1-dependent
              late-SASP output."
    support: "Fig. 3d, 3f; Extended Data Fig. 7e"
    tier: supporting
    equiv_group: sting_late_sasp
    papers:
      - DeCecco_nature_2019

# Supporting equivalence sting_late_sasp: STING1 upregulates CCL2.
  - chain_id: sting_late_sasp
    step: 2
    source: STING1
    target: CCL2
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "STING1 knockdown reduces CCL2, equivalent to IL6 and MMP3 as a
              marker of the STING1-dependent late SASP."
    support: "Fig. 3d, 3f; Extended Data Fig. 7e"
    tier: supporting
    equiv_group: sting_late_sasp
    papers:
      - DeCecco_nature_2019

# Supporting equivalence sting_late_sasp: STING1 upregulates MMP3.
  - chain_id: sting_late_sasp
    step: 3
    source: STING1
    target: MMP3
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "STING1 knockdown reduces MMP3, equivalent to IL6 and CCL2 as a
              marker of the STING1-dependent late SASP."
    support: "Fig. 3d, 3f, 4c; Extended Data Fig. 7e, 9a-c"
    tier: supporting
    equiv_group: sting_late_sasp
    papers:
      - DeCecco_nature_2019

# Supporting equivalence jakstat_late_sasp: JAK-STAT upregulates IL6.
  - chain_id: jakstat_late_sasp
    step: 1
    source: JAK-STAT
    target: IL6
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "IFNAR/JAK-STAT blockade reduces IL6, one marker of the late SASP
              amplified through JAK-STAT. IL6/CCL2/MMP3 are equivalent readouts of
              this program."
    support: "Fig. 3d, 3f; Extended Data Fig. 7b"
    tier: supporting
    equiv_group: jakstat_late_sasp
    papers:
      - DeCecco_nature_2019

# Supporting equivalence jakstat_late_sasp: JAK-STAT upregulates CCL2.
  - chain_id: jakstat_late_sasp
    step: 2
    source: JAK-STAT
    target: CCL2
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "IFNAR/JAK-STAT blockade reduces CCL2, equivalent to IL6 and MMP3 as a
              marker of the JAK-STAT-amplified late SASP."
    support: "Fig. 3d, 3f"
    tier: supporting
    equiv_group: jakstat_late_sasp
    papers:
      - DeCecco_nature_2019

# Supporting equivalence jakstat_late_sasp: JAK-STAT upregulates MMP3.
  - chain_id: jakstat_late_sasp
    step: 3
    source: JAK-STAT
    target: MMP3
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "IFNAR/JAK-STAT blockade reduces MMP3, equivalent to IL6 and CCL2 as a
              marker of the JAK-STAT-amplified late SASP."
    support: "Fig. 3d, 3f"
    tier: supporting
    equiv_group: jakstat_late_sasp
    papers:
      - DeCecco_nature_2019

# Supporting: L1 derepressed in senescent cells in aged tissue.
  - chain_id: in_vivo_aging
    step: 1
    source: cellular_senescence
    target: retrotransposon_derepression
    rel: induces
    evidence_strength: strong_correlative
    context: "In aged mouse tissues, ORF1+ (L1) cells colocalize with SA-beta-gal+
              senescent cells; L1 derepression rises with age in adipose and liver.
              An in-vivo correlative summary of the in-vitro spine."
    support: "Fig. 4a, 4b, 4d; Extended Data Fig. 8b-h, 10g"
    tier: supporting
    papers:
      - DeCecco_nature_2019

# Supporting summary edge (NOT the forbidden core substitute): L1 (RT) drives IFN-I
# in aged mice, read out pharmacologically with 3TC/K-9.
  - chain_id: in_vivo_aging
    step: 2
    source: retrotransposon_derepression
    target: type_I_IFN
    rel: drives
    evidence_strength: strong_correlative
    context: "In aged mice, 3TC (but not K-9) lowers tissue IFN-I, a legitimate
              in-vivo summary that L1 RT activity drives IFN-I. This SUPPORTING
              summary edge is retained because the paper makes it for the
              aged-mouse data; it is distinct from the forbidden anti-edge of the
              same triple, which represents offering this summary as the CORE
              mechanism in place of the cDNA -> cGAS -> STING spine."
    support: "Fig. 4c; Extended Data Fig. 9a-d"
    tier: supporting
    papers:
      - DeCecco_nature_2019

# Supporting: SASP recruits macrophages in aged tissue.
  - chain_id: in_vivo_aging
    step: 3
    source: SASP
    target: immune_cell_recruitment
    rel: drives
    evidence_strength: strong_correlative
    context: "The IFN-amplified SASP recruits macrophages in aged tissue; 3TC
              reduces the infiltrate. A downstream in-vivo consequence."
    support: "Fig. 4e; Extended Data Fig. 10a-d"
    tier: supporting
    papers:
      - DeCecco_nature_2019

# Supporting: immune recruitment drives tissue inflammation.
  - chain_id: in_vivo_aging
    step: 4
    source: immune_cell_recruitment
    target: tissue_inflammation
    rel: drives
    evidence_strength: strong_correlative
    context: "Macrophage recruitment drives age-associated tissue inflammation
              (inflammaging), reduced by 3TC. Terminal downstream phenotype."
    support: "Fig. 4e; Extended Data Fig. 10a-f"
    tier: supporting
    papers:
      - DeCecco_nature_2019

# Supporting negative: RBL1/RBL2 unchanged (RB1-paralog specificity).
  - chain_id: specificity_controls
    step: 1
    source: cellular_senescence
    target: RBL1
    rel: does_not_correlate
    evidence_strength: strong_correlative
    context: "RBL1 and RBL2 do not change in senescence, whereas RB1 does,
              establishing that L1 derepression is RB1-specific and not a general
              pocket-protein effect."
    support: "Extended Data Fig. 4b"
    tier: supporting
    papers:
      - DeCecco_nature_2019

# Core negative: IFN-I does NOT drive early IL1B SASP.
  - chain_id: specificity_controls
    step: 2
    source: type_I_IFN
    target: IL1B
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "IFNAR1/2 loss does not reduce the early IL1B SASP, whereas it reduces
              the late CCL2/IL6/MMP3 SASP. 'IFN amplifies the late SASP only' is the
              precise causal boundary of the paper, so this negative is core."
    support: "Fig. 3d, 3f"
    tier: core
    papers:
      - DeCecco_nature_2019

# FORBIDDEN SHORTCUT F1: L1 derepression "drives IFN" offered as the core spine
# substitute (distinct from the supporting in-vivo summary edge above).
  - chain_id: forbidden_shortcut
    step: 1
    source: retrotransposon_derepression
    target: type_I_IFN
    rel: drives
    evidence_strength: perturbation_supported
    context: "ANTI-EDGE. L1 RT activity is required for IFN-I, but offering
              'L1 derepression drives type-I IFN' as the CORE mechanistic account
              collapses the cytoplasmic cDNA -> CGAS -> cGAMP -> STING1 spine. The
              identically-tripled supporting in-vivo summary edge is legitimate;
              this forbidden row exists to catch a draft that draws the summary in
              place of the spine (a human-adjudication case; see design_decisions
              §4)."
    support: "n/a (anti-edge; see core steps 1-5)"
    tier: core
    status: forbidden_shortcut
    papers:
      - DeCecco_nature_2019

# FORBIDDEN SHORTCUT F2: L1 cDNA "drives type-I IFN" skipping the cGAS-STING sensor.
  - chain_id: forbidden_shortcut
    step: 2
    source: cytoplasmic_retroelement_cDNA
    target: type_I_IFN
    rel: drives
    evidence_strength: perturbation_supported
    context: "ANTI-EDGE. Cytoplasmic L1 cDNA is the ligand, but asserting it
              directly drives type-I IFN skips the CGAS -> cGAMP -> STING1 sensor
              chain that is the paper's mechanistic contribution. No legitimate
              supporting edge has this triple, so this anti-edge actively catches
              the shortcut."
    support: "n/a (anti-edge; see core steps 1-5)"
    tier: core
    status: forbidden_shortcut
    papers:
      - DeCecco_nature_2019

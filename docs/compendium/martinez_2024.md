paper:

  Martinez_biorxiv_2024:
    cite: "Martinez JC, Morandini F, Fitzgibbons L, Sieczkiewicz N, Bae SJ, Meadow ME, Hillpot E, Cutting J, Paige V, Biashad SA, Simon M, Sedivy J, Seluanov A, Gorbunova V. cGAS deficient mice display premature aging associated with de-repression of LINE1 elements and inflammation. bioRxiv 2024. doi:10.1101/2024.10.10.617645. Preprint."
    url: "https://doi.org/10.1101/2024.10.10.617645"
    summary: "Contrary to the expectation that removing the cytosolic DNA sensor would dampen inflammaging, cGAS knockout mice age faster. Nuclear CGAS forms H3K9me3-colocalized LLPS condensates that maintain heterochromatin on transposable elements; losing CGAS opens chromatin at L1 and pro-inflammatory loci, demethylates LINE/SINE/LTR/DNA transposon families, and de-represses LINE1, producing cytoplasmic L1 cDNA and ORF1p. The de-repressed cytoplasmic cDNA is proposed to engage AIM2 as a compensatory sensor and DNA damage accumulates, driving tissue inflammation, liver fibrosis, and an accelerated-aging phenotype. STING1 and PYHIN-family knockouts retain L1 repression, establishing the mechanism as nuclear, CGAS-specific, and STING-independent."
    nucleic_acid_sensors:
      - CGAS
      - STING1
      - AIM2
    genes:
      - CGAS
      - STING1
      - AIM2
      - NLRP3
      - NLRP1
      - CASP1
      - IL18
      - IL6
      - TNF
      - NFKB1
      - SPI1
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
      - DNA_damage
      - tissue_inflammation
      - fibrosis
      - accelerated_aging
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
      - STED_microscopy
      - smiFISH
      - immunofluorescence
      - immunoblot
      - RT_qPCR
      - IHC
      - histology
      - survival_analysis
    notes: >
      1. Tissue/organ: primary lung fibroblasts from 12-month-old cGAS KO and WT
      mice for RNA-seq, ATAC-seq, and Nanopore methylation; lung, kidney, and liver
      tissue from 12-month-old mice for qRT-PCR and histology; mouse embryonic
      fibroblasts (MEFs) for siRNA knockdown; human diploid fibroblasts (HDFs) for
      STED microscopy of nuclear cGAS LLPS. Frailty scored at 18 months; female
      lifespan followed to natural death.
      2. Species: mouse (in vivo and in vitro) and human (in vitro HDFs for STED).
      3. Age range or comparison: middle-aged (12-18 month) cGAS KO vs WT, plus
      female lifespan; genotypes are cGAS KO (B6-Cgas-tm1d, JAX 026554), STING KO
      (B6-Sting1-tm1.2Camb, JAX 025805), PYHIN-family KO, and WT C57BL/6.
      4. Sex-specific effects: males show body-mass increase and obesity with frailty
      but no lifespan change; females show shortened lifespan (median 92.4 vs 106.7
      weeks). Both sexes show increased frailty.
      5. Disease context: physiological/accelerated aging and inflammaging; not a
      disease model. The central unexpected finding is that cGAS loss accelerates
      aging through a nuclear, STING-independent mechanism, biologically inverse to
      Gulen 2023 (where STING inhibition is beneficial) and complementary to
      De Cecco 2019 (where L1 cDNA activates cGAS-STING in senescent cells). All
      three compose at the retrotransposon_derepression and
      cytoplasmic_retroelement_cDNA nodes.
      Mechanistic spine: nuclear CGAS maintains heterochromatin_organization
      (H3K9me3 colocalization, LLPS) and thereby suppresses epigenetic_remodeling
      (chromatin opening + transposon demethylation), which otherwise drives
      retrotransposon_derepression -> cytoplasmic_retroelement_cDNA. The same
      epigenetic_remodeling opens SPI1/PU.1-target chromatin and upregulates SPI1,
      which drives the inflammatory (and proposed fibrotic) program as a parallel arm
      to tissue_inflammation. Cytoplasmic L1 cDNA is proposed to engage a compensatory AIM2 inflammasome (canonical_inferred: no AIM2 rescue is
      performed) and to drive DNA_damage (gamma-H2AX). Organismal accelerated_aging
      (frailty, female lifespan, male obesity) and fibrosis route through
      tissue-level outcomes rather than a CGAS -> phenotype shortcut.
      Marker handling: the qRT-PCR panel (IL18, TNF, NFKB1, IL6) is treated as an
      inflammation readout in context, not as four AIM2-specific regulatory edges;
      IL18 is the canonical AIM2-inflammasome output and the others are general
      inflammation markers.
      Specificity: STING KO and PYHIN-family KO mice maintain L1MdA repression
      (Supp. Fig. 4); one does_not_drive edge is kept for STING1 and the redundant
      PYHIN result is folded into its context per the minor-redundant-paralog
      convention. The PYHIN family is not a single HGNC symbol and is not a node.
      Caveats flagged for review: cGAS is the perturbed entity throughout, so the
      L1-cDNA-specific attribution of AIM2 engagement and gamma-H2AX is inferred;
      1,6-hexanediol is not LLPS-specific; senescence GSEA is not enriched in cGAS
      KO fibroblasts (Supp. Fig. 2b), consistent with CGAS being required to
      initiate senescence (ref 36), so the inflammation here is senescence-
      independent and that point lives in context rather than as a separate edge.
    relevance_to_project: >
      In single-cell/spatial atlas data, CGAS-low or CGAS-loss states are predicted
      to show, within the SAME cells: (1) elevated LINE1 / young L1Md (or human L1HS)
      transcript signal and ORF1p; (2) open-chromatin / hypomethylation signatures
      over LINE/SINE/LTR repeats if matched ATAC or methylation is available; (3)
      AIM2-inflammasome activation (AIM2, NLRP3, NLRP1, CASP1, IL18) and a SPI1/PU.1-
      driven myeloid-inflammatory program rather than a classic IFN-I/SASP program;
      (4) gamma-H2AX / DNA-damage scores. Crucially, this is a STING1-independent,
      AIM2-biased inflammatory signature, so it is separable from the cGAS-STING-IFN
      axis: look for L1-high + AIM2-high + STING1-low/inactive cells, and expect
      co-variation with fibrotic (SPI1-high fibroblast) and neutrophil-infiltrated
      tissue niches. A useful contrast score is AIM2-inflammasome vs type_I_IFN
      output conditioned on L1 derepression.

edges:

# Edges from Martinez_biorxiv_2024
#
# Curation intent:
#   - Repressor-loss logic kept suppressive: nuclear CGAS is a brake on
#     epigenetic_remodeling and retrotransposon_derepression, not a positive
#     driver of "maintenance". Loss-of-function (KO/KD) supplies the evidence.
#   - Canonical L1 nodes reused from De Cecco 2019 (retrotransposon_derepression,
#     cytoplasmic_retroelement_cDNA) so the L1 biology composes across papers.
#   - epigenetic_remodeling reused from De Cecco 2019 as the chromatin-opening /
#     demethylation state; ATAC accessibility and Nanopore demethylation are its
#     molecular substance and live in context, not as a separate
#     chromatin_accessibility node.
#   - AIM2 inflammasome arm honestly encoded as canonical_inferred (no AIM2
#     perturbation rescue in this paper).
#   - No genotype-baked nodes (no cGAS_KO_inflammation) and no CGAS -> inflammaging
#     shortcut; the organismal phenotype routes through tissue-level outcomes.
#   - Cytokine panel (TNF/NFKB1/IL6) treated as inflammation readout in context.
#
# Verb guide (only verbs used below):
#   binds_recruits  — physical colocalization / recruitment
#   suppresses      — normal-function negative regulation (loss/gain-of-function)
#   drives          — perturbation-supported positive causal regulation
#   produces        — biosynthetic/enzymatic product of an upstream mechanism
#   activates       — sensor or signalling activation
#   induces         — trigger to a downstream state or phenotype
#   does_not_drive  — tested and found not to regulate a specific branch

# ─── CHAIN 1: nuclear CGAS maintains heterochromatin and restrains L1 ─────────

# Nuclear CGAS physically colocalizes with H3K9me3 and forms LLPS condensates;
# its loss disorganizes the H3K9me3 compartment. Heterochromatin_organization is
# the node CGAS acts on.
  - chain_id: nuclear_cGAS_L1_restraint
    step: 1
    source: CGAS
    target: heterochromatin_organization
    rel: binds_recruits
    evidence_strength: direct_measured
    context: "STED microscopy of WT primary lung cells shows nuclear CGAS in
      condensed clusters that strongly colocalize with H3K9me3 foci; cGAS KO cells
      lose H3K9me3 foci and show an altered, dispersed H3K9me3 distribution (Fig.
      7a; Supp. Fig. 6a). Nuclear CGAS LLPS condensates in human diploid fibroblasts
      are abolished by 1,6-hexanediol, consistent with phase separation (Fig. 7b,c);
      1,6-HD is not LLPS-specific, noted as a limitation. The nucleosome-binding
      domain of CGAS, not the cGAMP-producing domain, is required for phase
      separation on nucleosomal DNA (cited, ref 58). Encoded as binds_recruits
      because the measured claim is physical CGAS/H3K9me3 colocalization and
      CGAS-dependent organization of the heterochromatin compartment."
    support: "Fig. 7a, 7b, 7c; Supp. Fig. 6a"
    papers:
      - Martinez_biorxiv_2024

# Loss of nuclear CGAS opens chromatin and demethylates transposons: CGAS normally
# restrains epigenetic_remodeling. Suppressive (repressor-loss) direction.
  - chain_id: nuclear_cGAS_L1_restraint
    step: 2
    source: CGAS
    target: epigenetic_remodeling
    rel: suppresses
    evidence_strength: perturbation_supported
    context: "ATAC-seq on cGAS KO vs WT primary lung fibroblasts identifies 1392
      more accessible and 200 less accessible OCRs in cGAS KO, with accessibility
      gains concentrated over repetitive elements and the evolutionarily young L1Md
      clade (Fig. 5a, 5e). Nanopore CpG methylation shows significant global
      hypomethylation across DNA, LINE, LTR, and SINE transposon classes (Fig. 6a,b),
      including the active L1MdA_I and L1MdV_I families (Fig. 6c) and nearly all SINE
      families (Fig. 6d). Read with step 1, loss of CGAS-dependent
      heterochromatin_organization permits chromatin opening and transposon
      demethylation; the locus-level ATAC and methylation readouts are the substance
      of this edge and live in context rather than as separate accessibility/
      methylation nodes."
    support: "Fig. 5a, 5e; Fig. 6a, 6b, 6c, 6d"
    papers:
      - Martinez_biorxiv_2024

# Heterochromatin/methylation loss de-represses LINE1; CGAS loss drives L1 mRNA up
# in vivo and in vitro.
  - chain_id: nuclear_cGAS_L1_restraint
    step: 3
    source: epigenetic_remodeling
    target: retrotransposon_derepression
    rel: drives
    evidence_strength: perturbation_supported
    context: "cGAS KO mice show elevated L1MdA mRNA in lung, kidney, and liver by
      qRT-PCR (Fig. 3b) and upregulation of L1MdA_I/II/III and L1MdFanc families in
      primary lung-fibroblast RNA-seq (Fig. 3a). cGAS siRNA in WT MEFs gives a
      ~4-fold increase in L1MdA mRNA (Fig. 4a,b). The largest accessibility and
      demethylation effects are on young, full-length-capable L1Md families,
      coupling the epigenetic_remodeling state (step 2) to transcriptional
      derepression. Node name matches De Cecco 2019 so L1 biology composes."
    support: "Fig. 3a, 3b; Fig. 4a, 4b; Fig. 5e"
    papers:
      - Martinez_biorxiv_2024

# Derepressed L1 yields cytoplasmic L1 cDNA and ORF1p. The L1 mRNA -> ORF2p RT ->
# cytoplasmic cDNA step is standard L1 biology, inferred here for the cDNA-forming
# enzymology but with the cytoplasmic cDNA itself directly measured.
  - chain_id: nuclear_cGAS_L1_restraint
    step: 4
    source: retrotransposon_derepression
    target: cytoplasmic_retroelement_cDNA
    rel: produces
    evidence_strength: perturbation_supported
    context: "DNA smiFISH with probes specific for L1 cDNA (designed not to hybridize
      L1 mRNA) shows severely elevated cytoplasmic L1MdA cDNA in cGAS KO primary lung
      cells (Fig. 3c) and cGAS siRNA MEFs (Fig. 4c,d). Subcellular fractionation with
      RNase treatment and DNA cleanup confirms elevated L1MdA cDNA in the cytoplasmic
      fraction of cGAS siRNA cells, with fractionation purity verified by vinculin/H3
      immunoblot (Fig. 4g,h). ORF1p protein accumulates in cGAS KO primary cells
      (Fig. 3d) and cGAS siRNA MEFs (Fig. 4e,f). ORF2p reverse-transcriptase activity
      generating the cDNA is the canonical L1 mechanism and is not directly perturbed
      here. Node name matches De Cecco 2019 (cytoplasmic_retroelement_cDNA)."
    support: "Fig. 3c, 3d; Fig. 4c, 4d, 4e, 4f, 4g, 4h"
    papers:
      - Martinez_biorxiv_2024

# ─── CHAIN 2: chromatin opening activates SPI1/PU.1 → inflammation ───────────

# Chromatin opening exposes SPI1/PU.1 sites and SPI1 itself is upregulated. SPI1 is
# the dominant motif at opening OCRs and the authors' proposed inflammatory/fibrotic
# mediator, so it earns a node (cf. DeCecco FOXA1 on motif+expression evidence).
  - chain_id: chromatin_opening_SPI1_inflammatory_arm
    step: 1
    source: epigenetic_remodeling
    target: SPI1
    rel: upregulates
    evidence_strength: perturbation_supported
    context: "MEME-ChIP motif analysis of OCRs that open in cGAS KO lung fibroblasts
      gives a dominant SPI1/PU.1 motif (E=4.9e-431; Fig. 5c), and SPI1 itself is in
      the top 15% of expressed genes and upregulated in cGAS KO RNA-seq (logFC 0.4,
      p=0.0145; Fig. 5c text). Encoded as upregulates because the chromatin-opening
      state both exposes SPI1 binding sites genome-wide and raises SPI1 transcript;
      SPI1 is the single most enriched regulator of the opened, inflammation-biased
      chromatin. Closing OCRs are enriched for FoxE1/FoxD2 motifs (E=8.0e-13) whose
      role the authors call unclear; these stay in context."
    support: "Fig. 5c"
    papers:
      - Martinez_biorxiv_2024

# SPI1/PU.1 drives the inflammatory (and proposed fibrotic) program — a parallel
# arm to the L1/AIM2 chain that converges on tissue_inflammation.
  - chain_id: chromatin_opening_SPI1_inflammatory_arm
    step: 2
    source: SPI1
    target: tissue_inflammation
    rel: drives
    evidence_strength: perturbation_supported
    context: "GO analysis of genes downstream of opening promoters is dominated by
      inflammatory terms (alpha-beta T cell activation, TNF-superfamily cytokine
      production, IL-1-beta production, immune-response signalling; Fig. 5b),
      concordant with the RNA-seq inflammatory signature (315 up / 190 down DEGs;
      inflammatory GSEA, Fig. 2a,b). The authors invoke SPI1 as the regulator of this
      program: prior work shows SPI1/PU.1 controls multiple inflammasome genes in
      fibroblasts and drives fibroblast polarization/tissue fibrosis, so they propose
      the inflammatory phenotype and the liver fibrosis 'may be mediated by Spi1'.
      Perturbation support is the cGAS-KO loss-of-function that opens SPI1-target
      chromatin; SPI1 itself is not knocked down here, which is noted as the limit on
      this edge. Skip-edge note: this arm converges on tissue_inflammation with the
      L1 -> cytoplasmic_retroelement_cDNA -> AIM2 -> inflammasome chain but is a
      distinct parallel branch (direct PU.1-driven opening of pro-inflammatory loci),
      not a collapse of the L1/AIM2 intermediates, so it is retained."
    support: "Fig. 2a, 2b; Fig. 5b, 5c"
    papers:
      - Martinez_biorxiv_2024

# ─── CHAIN 3: cytoplasmic L1 cDNA → compensatory AIM2 inflammasome ───────────

# AIM2 is proposed to sense the accumulating cytoplasmic L1 cDNA, compensating for
# CGAS loss. Honestly canonical_inferred: AIM2 is up but never perturbed here.
  - chain_id: L1cDNA_AIM2_inflammasome
    step: 1
    source: cytoplasmic_retroelement_cDNA
    target: AIM2
    rel: activates
    evidence_strength: canonical_inferred
    context: "AIM2 is upregulated at the transcript level (RNA-seq Fig. 2c; qRT-PCR
      Fig. 2d, p<0.01) and becomes more accessible by ATAC in cGAS KO (Fig. 5d). AIM2
      is a canonical cytosolic dsDNA sensor structurally analogous to CGAS, and the
      authors propose it compensates for CGAS loss by sensing the accumulating
      cytoplasmic L1 cDNA. Encoded as canonical_inferred because no AIM2 perturbation
      (siRNA/KO) rescue is performed; the inference rests on co-occurrence of AIM2
      upregulation/accessibility with cytoplasmic_retroelement_cDNA accumulation plus
      prior reports of elevated AIM2 in cGAS-deficient lupus models (refs 10, 32-34).
      The AIM2 transcriptional/accessibility increase is itself a downstream
      consequence of chromatin opening; it is described in context rather than as a
      second epigenetic_remodeling -> AIM2 edge."
    support: "Fig. 2c, 2d; Fig. 5d"
    papers:
      - Martinez_biorxiv_2024

# AIM2 ligand engagement nucleates the inflammasome (ASC/CASP1). Canonical and
# inferred: assembly and CASP1 cleavage are not directly shown.
  - chain_id: L1cDNA_AIM2_inflammasome
    step: 2
    source: AIM2
    target: inflammasome_activation
    rel: drives
    evidence_strength: canonical_inferred
    context: "RNA-seq of cGAS KO lung fibroblasts shows enrichment of the
      inflammasome-complex cellular-component GO term (Fig. 2b) with coordinated
      upregulation of inflammasome components Aim2, Nlrp3, Nlrp1a/b, and Casp1 (Fig.
      2c). IL18, the canonical AIM2-inflammasome output downstream of CASP1, is
      upregulated by qRT-PCR (Fig. 2d, p<0.05). The AIM2 -> ASC -> CASP1 -> IL18
      assembly/cleavage axis is canonical and inferred here; the paper does not
      directly demonstrate inflammasome assembly or CASP1 cleavage, and notes it
      remains unclear why AIM2 is not only upregulated but activated."
    support: "Fig. 2b, 2c, 2d"
    papers:
      - Martinez_biorxiv_2024

# Inflammasome output contributes to tissue-level inflammation. Cytokine panel is
# kept as readout in context, not as four marker edges.
  - chain_id: L1cDNA_AIM2_inflammasome
    step: 3
    source: inflammasome_activation
    target: tissue_inflammation
    rel: drives
    evidence_strength: canonical_inferred
    context: "Tissue inflammation in cGAS KO is shown by lung neutrophil infiltration
      on H&E (Fig. 1c) and inflamed, fibrotic liver with leukocyte infiltrates (Fig.
      1d). The qRT-PCR panel in cGAS KO lung (IL-18 p<0.05, TNF-alpha p<0.0001, NFkB
      p<0.01, IL-6 elevated; Fig. 2d) is consistent with a general inflammatory
      program; IL18 is the inflammasome-specific output while TNF, NFKB1, and IL6 are
      kept in context as non-inflammasome-specific markers rather than as separate
      AIM2 -> cytokine edges. The molecular bridge from inflammasome activation to
      tissue inflammation is encoded as canonical_inferred."
    support: "Fig. 1c, 1d; Fig. 2d"
    papers:
      - Martinez_biorxiv_2024

# ─── CHAIN 4: cytoplasmic L1 cDNA → DNA damage ─────────────────────────────

# gamma-H2AX accumulates on CGAS loss; attributed to L1 genomic instability, but
# the perturbation is on CGAS so the L1-cDNA-specific attribution is inferred.
  - chain_id: L1cDNA_DNA_damage
    step: 1
    source: cytoplasmic_retroelement_cDNA
    target: DNA_damage
    rel: induces
    evidence_strength: perturbation_supported
    context: "cGAS siRNA in WT MEFs significantly increases gamma-H2AX-positive cells
      (~83% vs ~24% in controls, p<0.001; Fig. 4i,j), a canonical double-strand-break
      marker. The authors attribute this to genomic instability from L1
      derepression/retrotransposition driven by cytoplasmic L1 cDNA, but
      retrotransposition events are not directly measured and a contribution from the
      separately reported nuclear-CGAS DNA-repair/replication-fork role cannot be
      excluded. Because the perturbation is on CGAS rather than on
      cytoplasmic_retroelement_cDNA directly, the L1-cDNA-specific attribution is the
      inferred component of this edge."
    support: "Fig. 4i, 4j"
    papers:
      - Martinez_biorxiv_2024

# ─── CHAIN 5: tissue outcomes → organismal accelerated aging ────────────────

# Liver fibrosis is an explicit tissue-agnostic outcome node (matches LopezPolo).
  - chain_id: organismal_accelerated_aging
    step: 1
    source: tissue_inflammation
    target: fibrosis
    rel: drives
    evidence_strength: direct_measured
    context: "cGAS KO livers show a substantial increase in fibrotic tissue with
      leukocyte infiltration on H&E (Fig. 1d), accompanying the lung neutrophil
      infiltration in Fig. 1c. Fibrosis is kept as a tissue-agnostic outcome node;
      the liver context lives in the edge. The SPI1/PU.1 program from CHAIN 2 is the
      authors' proposed mediator of the fibrotic phenotype and is noted in context
      there."
    support: "Fig. 1c, 1d"
    papers:
      - Martinez_biorxiv_2024

# Organism-level accelerated aging routes through tissue inflammation, NOT via a
# CGAS -> inflammaging shortcut (cf. Gulen's avoided STING1 -> cognitive_decline).
  - chain_id: organismal_accelerated_aging
    step: 2
    source: tissue_inflammation
    target: accelerated_aging
    rel: drives
    evidence_strength: strong_correlative
    context: "cGAS KO mice show increased frailty index at 18 months in both sexes
      (Fig. 1a, p<0.001; driven by kyphosis, piloerection, tremors, Supp. Fig. 1d),
      shortened female lifespan (median 92.4 vs 106.7 weeks, p=0.0008 Mantel-Cox,
      Fig. 1e), and male body-mass increase/obesity (Fig. 1b,f; Supp. Fig. 1c,f).
      The accelerated-aging phenotype is associated with, and proposed to be driven
      by, the tissue inflammation and fibrosis above; the link is organism-level and
      correlative rather than a perturbation that isolates inflammation as the cause
      of the aging phenotype. The phenotype is senescence-independent: senescence
      GSEA is not enriched in cGAS KO fibroblasts (Supp. Fig. 2b), consistent with
      CGAS being required to initiate senescence (ref 36)."
    support: "Fig. 1a, 1b, 1e, 1f; Supp. Fig. 1c, 1d, 1f; Supp. Fig. 2b"
    papers:
      - Martinez_biorxiv_2024

# ─── CHAIN 6: specificity control — effect is CGAS-specific, STING-independent ─

# STING1 KO (and PYHIN KO, folded into context) retain L1 repression: L1
# derepression is specific to CGAS loss, not general DNA-sensing-pathway loss.
  - chain_id: specificity_controls
    step: 1
    source: STING1
    target: retrotransposon_derepression
    rel: does_not_drive
    evidence_strength: perturbation_supported
    context: "STING KO mice maintain repression of the L1MdA family at WT-comparable
      levels (Supp. Fig. 4), dissociating nuclear CGAS heterochromatin maintenance
      from canonical cytoplasmic DNA-sensing via STING1. PYHIN-family KO mice
      likewise retain L1MdA repression (Supp. Fig. 4), reinforcing that L1
      derepression is specific to CGAS depletion rather than a general consequence of
      cytosolic-DNA-sensing-pathway loss; the PYHIN result is folded into context per
      the minor-redundant-paralog convention. PYHIN is not a single HGNC symbol and
      is not encoded as a node."
    support: "Supp. Fig. 4"
    papers:
      - Martinez_biorxiv_2024

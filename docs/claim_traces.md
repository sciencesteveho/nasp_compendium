# NASP gold-standard claim traces

This document traces each core claim of the three redesigned papers from its
PDF evidence to the graph edge it should produce, and records the first-pass
scoring annotations (`tier`, `equiv_group`, `status`) that the `.gold.md` files
encode. It is the bridge between the source biology and the gold schema: every
gold edge below is justified by a specific figure/panel, and every `tier` /
`equiv_group` / `forbidden_shortcut` decision is stated with its reason.

Annotation vocabulary (defined fully in `design_decisions.md`):

- **tier: core** — a claim that, if missed or distorted, means the agent failed
  to preserve the central biology of the paper. Scored in the headline
  core-relationship recall denominator.
- **tier: supporting** — a true, evidence-backed claim that enriches the graph
  (triggers, brakes, in-vivo readouts, cohort correlations, negative controls)
  but is not the paper's central mechanistic spine. Credited when found, never
  penalized when missed.
- **equiv_group: `<id>`** — a set of biologically-equivalent alternate
  representations of one claim (pathway-level vs gene-level; grouped sensor
  node vs individual sensors; per-cytokine markers of one program). The group
  is satisfied once; recovering any member counts the whole group as recovered,
  and the denominator counts the group once.
- **status: forbidden_shortcut** — an anti-edge: a biologically misleading
  collapse the agent must NOT emit (e.g. sensor → phenotype skipping the
  second-messenger / adaptor / transcription-factor spine). Not part of any
  recall denominator; a draft edge that matches one is a `shortcut_violation`
  (a precision penalty), not an ordinary extra edge.
- **status: excluded** / **score_exclude: true** — a known gold defect kept for
  the record but dropped from scoring (pre-existing mechanism, unchanged).

Evidence-strength labels are carried unchanged from the curated drafts and were
verified against the source PDFs (Dou 2017 Nature; De Cecco 2019 Nature;
López-Polo 2024 Nat Commun).

---

## 1. Dou et al. 2017 (Nature) — cytoplasmic chromatin → cGAS-STING → NF-kB → SASP

Central discovery: lamin-B1 loss in senescence lets cytoplasmic chromatin
fragments (CCF) form and recruit cGAS; cGAS makes cGAMP (LC-MS-confirmed),
activating STING1 → RELA/NF-kB → SASP. STING1 is required in vivo for
immunosurveillance and tumour suppression, and the axis biases toward NF-kB (not
type-I IFN) because p38 and IL1A suppress IFNB1.

| # | Claim | PDF evidence | Edge (source → [rel] → target) | tier | equiv_group | status |
|---|-------|--------------|-------------------------------|------|-------------|--------|
| 1 | Lamin B1 is lost in senescence | Fig. 1c; refs 4,5,7,11,12 | cellular_senescence → [downregulates] → LMNB1 | supporting | — | — |
| 2 | LMNB1 restrains CCF formation | Ext. Data Fig. 4e-h, 8f-g | LMNB1 → [suppresses] → cytoplasmic_chromatin_fragments | core | — | — |
| 3 | CCF recruit cGAS (colocalize; CGAS-dependent SASP) | Fig. 1a; Ext. Data 1c-e, 8a,8e, 4j-k | cytoplasmic_chromatin_fragments → [binds_recruits] → CGAS | core | — | — |
| 4 | cGAS makes cGAMP (LC-MS) | Fig. 1b; Ext. Data 1g, 5a | CGAS → [produces] → cGAMP | core | — | — |
| 5 | cGAMP activates STING1 (dimerization) | Fig. 1c; Ext. Data 1h-j | cGAMP → [activates] → STING1 | core | — | — |
| 6 | STING1 activates RELA (S536-P, nuclear, promoter occupancy) | Fig. 2g; Ext. Data 4a-d | STING1 → [activates] → RELA | core | — | — |
| 7 | RELA drives SASP transcription | Fig. 2c-e,g; 4e-f; Ext. Data 3c-f,i | RELA → [drives] → SASP | core | — | — |
| 8 | SASP recruits immune cells | Fig. 2f; 3e-f; Ext. Data 3g-h, 6f | SASP → [drives] → immune_cell_recruitment | supporting | — | — |
| 9 | STING1 required for immunosurveillance in vivo | Fig. 3a-b,e,g; Ext. Data 5c,6c-e,7a-e | STING1 → [required_for] → immunosurveillance | core | — | — |
| 10 | Immunosurveillance suppresses tumorigenesis (7/7 vs 0/5) | Fig. 3h; Ext. Data 6g | immunosurveillance → [suppresses] → tumorigenesis | supporting | — | — |
| 11 | Oncogenic RAS induces senescence | Fig. 1a,c; 3c-e; Ext. Data 2a-b,6a-e | oncogenic_RAS → [induces] → cellular_senescence | supporting | senescence_trigger | — |
| 12 | DNA damage induces senescence | Fig. 2; 3a-b; Ext. Data 2c-d,5a-c | DNA_damage → [induces] → cellular_senescence | supporting | senescence_trigger | — |
| 13 | Replicative exhaustion induces senescence | Fig. 1a; Ext. Data 1b | replicative_exhaustion → [induces] → cellular_senescence | supporting | senescence_trigger | — |
| 14 | p38 MAPK active in senescence | ref. 20; Ext. Data 2f | cellular_senescence → [activates] → p38_MAPK | supporting | — | — |
| 15 | p38 suppresses IFNB1 | Ext. Data 2f | p38_MAPK → [suppresses] → IFNB1 | supporting | ifnb1_suppression | — |
| 16 | SASP induces IL1A | Fig. 1c; 2c; Ext. Data 2g-h | SASP → [induces] → IL1A | supporting | — | — |
| 17 | IL1A suppresses IFNB1 (biases to NF-kB) | Ext. Data 2g-h | IL1A → [suppresses] → IFNB1 | supporting | ifnb1_suppression | — |
| 18 | OIS-evaded/cancer cells retain CCF chronically | Fig. 4c-f; Ext. Data 8a-h | senescence_evasion → [retains] → cytoplasmic_chromatin_fragments | supporting | — | — |
| 19 | STING1 expression correlates with SASP (CCLE/TCGA) | Fig. 4g; Ext. Data 9a,10a-d | STING1 → [correlates] → SASP | supporting | pancancer_pathway_corr | — |
| 20 | CGAS expression correlates with SASP | Ext. Data 9b | CGAS → [correlates] → SASP | supporting | pancancer_pathway_corr | — |
| 21 | LMNB1 negatively correlates with SASP | Fig. 4g; Ext. Data 9a,9c | LMNB1 → [negatively_correlates] → SASP | supporting | — | — |
| 22 | MAVS does NOT correlate with SASP (DNA-branch specificity) | Ext. Data 9d; Suppl. Table 4 | MAVS → [does_not_correlate] → SASP | supporting | — | — |
| 23 | IFI16 does NOT drive SASP (sensor specificity) | Ext. Data 3j-k | IFI16 → [does_not_drive] → SASP | core | — | — |
| F1 | **Shortcut**: cGAS "drives SASP" skipping cGAMP→STING1→RELA | — (anti-edge) | CGAS → [drives] → SASP | — | — | forbidden_shortcut |
| F2 | **Shortcut**: CCF "drive SASP" skipping the sensor/adaptor/TF | — (anti-edge) | cytoplasmic_chromatin_fragments → [drives] → SASP | — | — | forbidden_shortcut |

Notes on the Dou annotations:

- **Core spine (rows 2-7, 9, 23).** The paper's novelty is that *chromatin* is
  the ligand and *NF-kB* (not IFN) is the output. Missing any of CCF→CGAS,
  CGAS→cGAMP, cGAMP→STING1, STING1→RELA, RELA→SASP loses that discovery, so all
  are core. STING1→immunosurveillance is the in-vivo functional proof and is
  core. The IFI16 negative control is core because "cGAS, not the other DNA
  sensor IFI16" is a specificity claim central to the paper's attribution.
- **`senescence_trigger` equivalence (rows 11-13).** RAS, DNA damage and
  replicative exhaustion are three interchangeable ways to *enter* senescence
  upstream of the NASP spine. For preserved biology it is enough that the agent
  captured that a senescence stress feeds the pathway; it should not be
  penalized for picking a different trigger than the curator, nor rewarded three
  times for listing all of them.
- **`pancancer_pathway_corr` equivalence (rows 19-20).** "cGAS-STING pathway
  expression tracks SASP across cancer cohorts" is one claim; STING1 and CGAS
  are equivalent proxies for it.
- **`ifnb1_suppression` group (rows 15,17).** Two convergent brakes (p38 and
  IL1A) on the same node IFNB1; either recovers the "IFN is actively suppressed"
  point.
- **Forbidden shortcuts F1-F2.** Both are the canonical failure mode — naming
  the sensor (or the ligand) as the direct cause of the phenotype while dropping
  the second-messenger → adaptor → transcription-factor chain that is the whole
  contribution of the paper.

---

## 2. De Cecco et al. 2019 (Nature) — L1 cDNA → cGAS-STING → type-I IFN → late SASP

Central discovery: in late senescence, convergent failure of RB1, FOXA1 and
TREX1 surveillance derepresses L1; L1 reverse transcriptase makes cytoplasmic
cDNA that activates cGAS-STING to drive type-I IFN, which via JAK-STAT amplifies
the *late* SASP (CCL2/IL6/MMP3) but not the early IL1B SASP. The RT inhibitor
3TC blocks the axis; the non-RT-inhibitory analogue K-9 does not (RT-dependence).

| # | Claim | PDF evidence | Edge (source → [rel] → target) | tier | equiv_group | status |
|---|-------|--------------|-------------------------------|------|-------------|--------|
| 1 | Senescence remodels L1 heterochromatin | Fig. 2a; Ext. Data 4c | cellular_senescence → [induces] → epigenetic_remodeling | supporting | — | — |
| 2 | RB1 loss derepresses L1 (bidirectional) | Fig. 2a,c,d; Ext. Data 4b,4c,4g,4h | RB1 → [suppresses] → retrotransposon_derepression | supporting | l1_surveillance | — |
| 3 | FOXA1 gain drives L1 transcription | Fig. 2b,e; Ext. Data 4d-h | FOXA1 → [drives] → retrotransposon_derepression | supporting | l1_surveillance | — |
| 4 | TREX1 loss lets L1 cDNA accumulate | Fig. 2f,g; Ext. Data 4a,4g,4h | TREX1 → [suppresses] → retrotransposon_derepression | supporting | l1_surveillance | — |
| 5 | L1 RT makes cytoplasmic cDNA (3TC-blocked) | Fig. 3a-c; Ext. Data 6a-e | retrotransposon_derepression → [produces] → cytoplasmic_retroelement_cDNA | core | — | — |
| 6 | L1 cDNA activates cGAS | Ext. Data 5l, 7c-e | cytoplasmic_retroelement_cDNA → [activates] → CGAS | core | — | — |
| 7 | cGAS makes cGAMP (canonical here) | main text p.75; Ext. Data 5l,7c | CGAS → [produces] → cGAMP | core | — | — |
| 8 | cGAMP activates STING1 | Ext. Data 5l,7c-e | cGAMP → [activates] → STING1 | core | — | — |
| 9 | STING1 drives type-I IFN | Fig. 1d,e,2h,3b,3e; Ext. Data 3,5l,7c-d | STING1 → [drives] → type_I_IFN | core | — | — |
| 10 | Type-I IFN signals via JAK-STAT | Fig. 3b; Ext. Data 5m,7a | type_I_IFN → [activates] → JAK-STAT | core | — | — |
| 11 | JAK-STAT amplifies late SASP (not IL1B) | Fig. 3d,f; Ext. Data 6f,7b | JAK-STAT → [drives] → SASP | core | — | — |
| 12 | L1 RT activity required for IFN-I (3TC vs K-9) | Ext. Data 7f,7g,9d | retrotransposon_derepression → [required_for] → type_I_IFN | core | — | — |
| 13 | STING1 upregulates IL6 (late SASP) | Fig. 3d,f; Ext. Data 7e | STING1 → [upregulates] → IL6 | supporting | sting_late_sasp | — |
| 14 | STING1 upregulates CCL2 | Fig. 3d,f; Ext. Data 7e | STING1 → [upregulates] → CCL2 | supporting | sting_late_sasp | — |
| 15 | STING1 upregulates MMP3 | Fig. 3d,f,4c; Ext. Data 7e,9a-c | STING1 → [upregulates] → MMP3 | supporting | sting_late_sasp | — |
| 16 | JAK-STAT upregulates IL6 | Fig. 3d,f; Ext. Data 7b | JAK-STAT → [upregulates] → IL6 | supporting | jakstat_late_sasp | — |
| 17 | JAK-STAT upregulates CCL2 | Fig. 3d,f | JAK-STAT → [upregulates] → CCL2 | supporting | jakstat_late_sasp | — |
| 18 | JAK-STAT upregulates MMP3 | Fig. 3d,f | JAK-STAT → [upregulates] → MMP3 | supporting | jakstat_late_sasp | — |
| 19 | L1 derepressed in senescent cells in aged tissue | Fig. 4a,b,d; Ext. Data 8b-h,10g | cellular_senescence → [induces] → retrotransposon_derepression | supporting | — | — |
| 20 | L1 (RT) drives IFN-I in aged mice (3TC/K-9) | Fig. 4c; Ext. Data 9a-d | retrotransposon_derepression → [drives] → type_I_IFN | supporting | — | — |
| 21 | SASP recruits macrophages in aged tissue | Fig. 4e; Ext. Data 10a-d | SASP → [drives] → immune_cell_recruitment | supporting | — | — |
| 22 | Immune recruitment → tissue inflammation | Fig. 4e; Ext. Data 10a-f | immune_cell_recruitment → [drives] → tissue_inflammation | supporting | — | — |
| 23 | RBL1/RBL2 unchanged (RB1 paralog specificity) | Ext. Data 4b | cellular_senescence → [does_not_correlate] → RBL1 | supporting | — | — |
| 24 | IFN-I does NOT drive early IL1B SASP | Fig. 3d,f | type_I_IFN → [does_not_drive] → IL1B | core | — | — |
| F1 | **Shortcut**: L1 "drives IFN" skipping cDNA→cGAS→STING | — (anti-edge) | retrotransposon_derepression → [drives] → type_I_IFN (as core spine) | — | — | forbidden_shortcut |
| F2 | **Shortcut**: L1 cDNA "drives type-I IFN" skipping the cGAS-STING sensor | — (anti-edge) | cytoplasmic_retroelement_cDNA → [drives] → type_I_IFN | — | — | forbidden_shortcut |

Notes on the De Cecco annotations:

- **Core spine (rows 5-12, 24).** The paper's contribution is the *chain*:
  L1 cDNA is the ligand, cGAS-STING is the sensor, and the emphasised output is
  *type-I IFN → JAK-STAT → late SASP*, distinct from the early IL1B SASP. The
  RT-dependence edge (row 12) is core because the 3TC/K-9 contrast is the
  paper's central pharmacological and mechanistic claim, and the IL1B negative
  edge (row 24) is core because "IFN amplifies the *late* SASP only" is the
  precise causal boundary the paper draws.
- **`l1_surveillance` equivalence (rows 2-4).** RB1, FOXA1 and TREX1 are three
  convergent surveillance failures upstream of L1. They are kept as *supporting*
  (they are context for how L1 is derepressed, not the NASP sensing spine) and
  grouped so the agent is credited for capturing "surveillance failure
  derepresses L1" without being triple-counted for all three.
- **`sting_late_sasp` / `jakstat_late_sasp` equivalences (rows 13-18).** IL6,
  CCL2 and MMP3 are three marker cytokines of one program (the late/mature
  SASP). The per-cytokine edges are equivalent representations; each group is
  satisfied once. They are supporting because the program-level edges
  (STING1→…→IFN and JAK-STAT→SASP) already carry the mechanism.
- **F1 note.** Row 20 (`retrotransposon_derepression → drives → type_I_IFN`) is
  a legitimate *supporting* in-vivo summary edge. The same triple becomes a
  *forbidden shortcut* only when it is offered as the **core** mechanistic
  account in place of the cDNA→cGAS→STING spine. The gold encodes F1 as a
  distinct anti-edge with `status: forbidden_shortcut`; the supporting row 20 is
  retained because the paper does make the summary claim for the aged-mouse
  data. (This asymmetry is discussed in `design_decisions.md` §4.)

---

## 3. López-Polo et al. 2024 (Nat Commun) — mitochondrial dsRNA → RIG-I/MDA5 → MAVS → IFN/SASP

Central discovery: senescent cells accumulate and release mitochondrial dsRNA
into the cytosol (POLRMT supplies substrate; PNPT1 and ADAR brakes are lost;
BAX/BAK pores permit escape); cytosolic mt-dsRNA engages RIG-I (DDX58) and MDA5
(IFIH1) → MAVS → type-I IFN and SASP, while CDKN1A senescence is preserved. A
parallel mtDNA/cGAS-STING branch contributes but is secondary; mitofusins tune
the axis (MFN1 promotes, MFN2 suppresses).

| # | Claim | PDF evidence | Edge (source → [rel] → target) | tier | equiv_group | status |
|---|-------|--------------|-------------------------------|------|-------------|--------|
| 1 | Senescence raises cytosolic mt-dsRNA (net) | Fig. 1a-d,5a-e; Suppl. 2,9 | cellular_senescence → [induces] → cytoplasmic_mt_dsRNA | core | — | — |
| 2 | POLRMT supplies the mt-RNA substrate (IMT1) | Fig. 1g,h; Suppl. 3a-e | POLRMT → [produces] → cytoplasmic_mt_dsRNA | supporting | — | — |
| 3 | Senescence downregulates PNPT1 brake | Fig. 1f; Suppl. 1a | cellular_senescence → [downregulates] → PNPT1 | supporting | — | — |
| 4 | PNPT1 restrains mt-dsRNA | Suppl. 1a; Fig. 1f | PNPT1 → [suppresses] → cytoplasmic_mt_dsRNA | supporting | — | — |
| 5 | Senescence downregulates ADAR brake | Fig. 2a-c; Suppl. 4a-g | cellular_senescence → [downregulates] → ADAR | supporting | — | — |
| 6 | ADAR restrains dsRNA immunogenicity | Fig. 2d; Suppl. 4d-g | ADAR → [suppresses] → cytosolic_RNA_sensing | supporting | — | — |
| 7 | Senescence upregulates RIG-I (DDX58) | Fig. 2e; 5g | cellular_senescence → [upregulates] → DDX58 | supporting | sensor_induction | — |
| 8 | Senescence upregulates MDA5 (IFIH1) | Fig. 2e; 5f,g | cellular_senescence → [upregulates] → IFIH1 | supporting | sensor_induction | — |
| 9 | BAX/BAK pore releases mt-dsRNA (DKO loses it) | Fig. 2f,h; Suppl. 4j | BAX/BAK_pore → [forms_pore_for] → cytoplasmic_mt_dsRNA | core | — | — |
| 10 | BAX/BAK pore also releases mtDNA (parallel) | Fig. 2f,h; Suppl. 4j; Disc. | BAX/BAK_pore → [forms_pore_for] → cytoplasmic_mtDNA | supporting | — | — |
| 11 | mt-dsRNA engages cytosolic RNA sensing | Fig. 1c,d,g-i; 2f-h; 6 | cytoplasmic_mt_dsRNA → [activates] → cytosolic_RNA_sensing | core | — | — |
| 12 | Sensing proceeds via RIG-I (DDX58) | Fig. 2e-g; 6 | cytosolic_RNA_sensing → [activates] → DDX58 | core | dsrna_sensor | — |
| 13 | Sensing proceeds via MDA5 (IFIH1) | Fig. 2e-g; 6 | cytosolic_RNA_sensing → [activates] → IFIH1 | core | dsrna_sensor | — |
| 14 | RIG-I signals through MAVS | Fig. 2e-g; 3a-i | DDX58 → [activates] → MAVS | core | sensor_to_mavs | — |
| 15 | MDA5 signals through MAVS | Fig. 2e-g; 3a-i | IFIH1 → [activates] → MAVS | core | sensor_to_mavs | — |
| 16 | MAVS drives type-I IFN | Fig. 3a-i; Suppl. 5b | MAVS → [drives] → type_I_IFN | core | — | — |
| 17 | MAVS drives SASP (CDKN1A preserved) | Fig. 3g-i; Suppl. 5b | MAVS → [drives] → SASP | core | — | — |
| 18 | mtDNA activates cGAS (parallel branch) | Fig. 2f; Suppl. 4h; Intro/Disc. | cytoplasmic_mtDNA → [activates] → CGAS | supporting | — | — |
| 19 | cGAS activates STING1 (parallel branch) | Fig. 2f; Suppl. 4h | CGAS → [activates] → STING1 | supporting | — | — |
| 20 | STING1 drives SASP (parallel contribution) | Fig. 2f; Suppl. 4h | STING1 → [drives] → SASP | supporting | — | — |
| 21 | MFN1 promotes mt-dsRNA | Fig. 4e; Suppl. 7a-c | MFN1 → [drives] → cytoplasmic_mt_dsRNA | supporting | — | — |
| 22 | MFN1 promotes MAVS aggregation | Fig. 4f; Suppl. 7d-f | MFN1 → [drives] → MAVS | supporting | — | — |
| 23 | MFN1 promotes SASP | Fig. 4c,d,h; Suppl. 6i,j,8c-f | MFN1 → [drives] → SASP | supporting | — | — |
| 24 | MFN2 suppresses mt-dsRNA | Fig. 4e; Suppl. 7a-c | MFN2 → [suppresses] → cytoplasmic_mt_dsRNA | supporting | — | — |
| 25 | MFN2 suppresses MAVS | Fig. 4f; Suppl. 7a-f | MFN2 → [suppresses] → MAVS | supporting | — | — |
| 26 | MFN2 suppresses SASP | Fig. 4d; Suppl. 6i,j,7a-f | MFN2 → [suppresses] → SASP | supporting | — | — |
| 27 | POLRMT required for SASP in vivo (IMT1) | Fig. 5i; Methods | POLRMT → [required_for] → SASP | supporting | — | — |
| 28 | LGP2 (DHX58) unchanged (sensor specificity) | Fig. 2e | cellular_senescence → [does_not_drive] → DHX58 | core | — | — |
| 29 | PKR (EIF2AK2) does NOT drive SASP (specificity) | Fig. 2e; Suppl. 4i | EIF2AK2 → [does_not_drive] → SASP | core | — | — |
| F1 | **Shortcut**: MAVS "drives" a single marker cytokine (CXCL10) not the program | — (anti-edge) | MAVS → [upregulates] → CXCL10 | — | — | forbidden_shortcut |
| F2 | **Shortcut**: senescence "drives SASP" skipping mt-dsRNA→RIG-I/MDA5→MAVS | — (anti-edge) | cellular_senescence → [drives] → SASP | — | — | forbidden_shortcut |

Notes on the López-Polo annotations:

- **Core spine (rows 1, 9, 11-17, 28-29).** The paper's contribution is that the
  ligand is *mitochondrial dsRNA* and the sensor arm is *RIG-I/MDA5 → MAVS* (not
  cGAS-STING as primary). The pore-release edge (row 9) is core because BAX/BAK
  depletion is the strongest perturbation and is the mechanism of cytosolic
  escape. The two specificity negatives (LGP2 unchanged, PKR not required) are
  core because "these dsRNA sensors and not those" is exactly the attribution
  the paper makes.
- **`dsrna_sensor` equivalence (rows 12-13).** The paper does not separate RIG-I
  and MDA5 ligand specificity — they are tested by combined depletion. Recovering
  either sensor edge satisfies "mt-dsRNA engages RIG-I/MDA5 sensing."
- **`sensor_to_mavs` equivalence (rows 14-15).** DDX58→MAVS and IFIH1→MAVS are
  the same canonical continuity claim ("the dsRNA sensor signals through MAVS");
  satisfied once.
- **`sensor_induction` equivalence (rows 7-8).** Senescence-associated
  upregulation of the two sensors is one expression-level observation.
- **Parallel cGAS-STING branch (rows 18-20) is supporting, deliberately.** This
  encodes the paper's own framing: combined CGAS/STING depletion reduces
  cytokines, but the resolved mechanism is mt-dsRNA/MAVS. Keeping it supporting
  (not core) is what stops the parallel branch from displacing the spine.
- **Forbidden shortcuts.** F1 is the exact anti-pattern the curator flagged in
  the draft ("replaces marker-level MAVS → CXCL10/CCL2/B2M edges"): naming MAVS
  as the direct regulator of one output cytokine instead of the SASP program.
  F2 is the generic senescence→SASP collapse that erases the whole sensing axis.

---

## Cross-paper summary of annotation counts

| Paper | core edges | supporting edges | equiv groups | forbidden shortcuts | excluded defects |
|-------|-----------|------------------|--------------|---------------------|------------------|
| Dou 2017 | 8 | 15 | 3 (senescence_trigger, pancancer_pathway_corr, ifnb1_suppression) | 2 | 0 |
| De Cecco 2019 | 9 | 15 | 3 (l1_surveillance, sting_late_sasp, jakstat_late_sasp) | 2 | 0 |
| López-Polo 2024 | 12 | 17 | 4 (sensor_induction, dsrna_sensor, sensor_to_mavs; +none) | 2 | 0 |

Core-edge denominators after equivalence collapse are what the headline
core-relationship recall is computed against; the exact per-paper self-match
numbers are recorded in `verification_log.txt`.

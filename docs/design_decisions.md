# Gold-standard schema design decisions

This document settles the schema the three redesigned gold files use and the
semantics the scorer implements. The goal driving every decision: the gold
standard must measure whether the curation agent **preserved the biology**
(source/target entities, causal direction and sign, molecular mechanism, and
direct-vs-indirect evidence) — not whether it reproduced one curator's exact
wording. Everything below is additive and backward-compatible: a legacy gold
that carries none of the new fields scores exactly as it does today.

## 0. Constraints that shaped the design

- **Additive only.** The validator already tolerates unknown edge keys (it
  checks that *required* fields are present, not that *no other* fields exist —
  confirmed by the pre-existing `score_exclude` / `status: excluded` pair). New
  fields (`tier`, `equiv_group`, `status: forbidden_shortcut`) therefore need no
  validator change and cannot break `validate` on the five legacy golds.
- **One schema, two readers.** The same YAML edge is read by humans (as a
  curation target) and by the scorer. Annotations must be legible to both:
  short controlled strings, defaults that mean "ordinary core edge."
- **Drafts stay untouched.** The redesign creates `*.gold.md` files; the
  `dou_2017.md` / `dececco_2019.md` / `lopez_polo_2024.md` drafts are the
  "agent output under test" and are left exactly as curated.

## 1. `tier: core | supporting` (default `core`)

**Decision.** Every gold edge carries an optional `tier`. Absent ⇒ `core`.

- **core** — the central mechanistic spine. If the agent misses or distorts a
  core edge, it failed to preserve the paper's discovery. Core edges form the
  denominator of the **headline metric** (core-relationship recall).
- **supporting** — true, evidence-backed, graph-worthy, but peripheral to the
  spine: upstream triggers, brakes, in-vivo readouts, cohort correlations,
  marker-cytokine outputs, parallel secondary branches. Supporting recall is
  **reported separately** and is **never** allowed to lower the headline number.

**Why default `core`.** Legacy golds have no `tier` field; treating absent as
`core` means they keep scoring against their full edge list (every edge
required), i.e. exactly today's behaviour. Backward compatibility falls out of
the default.

**Why this is the biggest single fix.** Today every gold edge is equally
"required." A gold that lists a rich in-vivo cohort correlation and the
CGAS→cGAMP→STING1 spine treats them as equally mandatory, so an agent that nails
the spine but omits a cohort scatter-plot edge is scored identically to one that
inverts the spine. Tiering makes "get the mechanism right" the thing the
headline measures.

## 2. `equiv_group: <id>` — biological-equivalence classes

**Decision.** An optional `equiv_group` string tags a set of gold edges that are
**biologically-equivalent alternate representations of one claim**. The scorer
treats the group as a single recoverable unit: recovering *any* member marks the
whole group recovered, and the group contributes **one** unit to its tier's
denominator (not one per member). Edges with no `equiv_group` are singletons
(their own group of one), so legacy behaviour is unchanged.

Four equivalence patterns recur across the three papers and motivated the field:

1. **Pathway-level vs gene-level.** "The cGAS-STING pathway tracks SASP across
   cancers" can be curated as `STING1 → correlates → SASP` or `CGAS → correlates
   → SASP`. Same claim; the agent should not be marked wrong for choosing the
   pathway's other canonical member. (Dou `pancancer_pathway_corr`.)
2. **Grouped-sensor node vs individual sensors.** "mt-dsRNA engages RIG-I/MDA5
   sensing" can be one edge to a `cytosolic_RNA_sensing` node or two edges to
   `DDX58` and `IFIH1`. (López-Polo `dsrna_sensor`, `sensor_to_mavs`.)
3. **Interchangeable upstream triggers.** RAS / DNA-damage / replicative
   exhaustion all enter senescence upstream of the spine; capturing one is
   capturing the claim. (Dou `senescence_trigger`.)
4. **Per-marker outputs of one program.** IL6 / CCL2 / MMP3 are three markers of
   the late SASP; any one represents the program-level output. (De Cecco
   `sting_late_sasp`, `jakstat_late_sasp`.)

**Why "satisfied once" and not "credit every member."** Crediting each member
would let an agent inflate recall by listing all three SASP cytokines while
missing an actual distinct mechanism. Collapsing to one unit keeps recall a
count of *distinct biology recovered*.

**Interaction with tier.** `equiv_group` and `tier` are orthogonal: a group is
scored within its tier. Groups are almost always single-tier by construction; if
members disagree, the scorer takes the strongest (core > supporting) tier for
the group so a core claim can't be demoted by a supporting alias.

## 3. `status: forbidden_shortcut` — scored anti-edges

**Decision.** A gold edge may carry `status: forbidden_shortcut`. Such an edge
is **not** a curation target: it is a biologically-misleading collapse the agent
must **not** emit. It is excluded from every recall denominator. If a draft edge
matches a forbidden-shortcut gold edge (same normalized endpoints), it is
counted as a **`shortcut_violation`** — a distinct precision penalty — rather
than silently folded into "extra edges."

**Why a scored field and not just a validator warning.** The repo already warns
about shortcut edges at curation time, but a warning never reaches the gold
score, so "the agent drew the misleading shortcut" and "the agent drew a
harmless extra edge" are today indistinguishable in the numbers. Promoting the
shortcut to a scored anti-edge makes the single most damaging curation error —
naming a sensor as the direct cause of a phenotype while dropping the
second-messenger→adaptor→transcription-factor spine — visible and penalized.

**What qualifies as a forbidden shortcut (rubric).** An edge whose endpoints are
both real nodes in the paper but which *bypasses* an intermediate the paper
proves is required, such that emitting it would let a reader infer a
mechanistically false directness. Canonical instances encoded in the three
golds:

- `CGAS → drives → SASP` (Dou) — skips cGAMP → STING1 → RELA.
- `cytoplasmic_chromatin_fragments → drives → SASP` (Dou) — skips the entire
  sensor/adaptor/TF chain.
- `cytoplasmic_retroelement_cDNA → drives → type_I_IFN` (De Cecco) — skips
  cGAS-STING.
- `cellular_senescence → drives → SASP` (López-Polo) — erases the mt-dsRNA →
  RIG-I/MDA5 → MAVS axis.
- `MAVS → upregulates → CXCL10` (López-Polo) — collapses the SASP program to one
  marker cytokine as if it were the mechanism.

**The supporting-vs-forbidden asymmetry.** The same triple can be a legitimate
supporting edge in one framing and a forbidden shortcut in another. De Cecco row
20, `retrotransposon_derepression → drives → type_I_IFN`, is a true *summary*
edge for the aged-mouse data (kept as supporting) but a *forbidden* substitute
for the cDNA→cGAS→STING spine. The scorer distinguishes them structurally: the
supporting edge and the forbidden anti-edge are two different gold rows (the
forbidden one carries `status: forbidden_shortcut`), and a draft edge is only a
violation when it matches the row explicitly marked forbidden while the core
spine it bypasses is present as separate core edges. In practice the anti-edge's
purpose is to catch a draft that draws the summary edge *instead of* the spine;
this remains a human-adjudication item where the collapse is subtle (see
`gold_standard_redesign.md` §7).

## 4. Existing defect markers kept unchanged

`score_exclude: true` / `status: excluded` continue to mean "known gold defect,
retained for the record, dropped from scoring" (the tyshkovskiy
`type_I_IFN does_not_drive mortality` placeholder). `forbidden_shortcut` is a
*different* status: excluded-from-denominator like a defect, but additionally
*penalized-if-matched*, which a defect is not. The two never collide because an
edge has one `status`.

## 5. The molecular-level-label question — verdict: **do not add a level field**

The task asks whether gold edges should carry an explicit molecular-level label
(genomic / transcriptional / RNA / protein / post-translational / complex /
localization). Three designs were considered:

**Design A — explicit `level:` enum on every edge.** Adds a controlled field
naming the regulatory layer of each edge.
- *Cost:* a new controlled vocabulary to define, validate, and keep consistent
  across 50-100+ future papers; a per-edge annotation burden on the curator; and
  a second axis the scorer must decide whether to score (if unscored it is
  decorative; if scored it multiplies the ways a biologically-correct edge can
  be marked wrong — the exact brittleness this redesign exists to remove).
- *Benefit:* makes the regulatory layer queryable without parsing node/verb.

**Design B — encode level in the relationship verb + node identity (status
quo, made explicit).** The existing controlled `rel` vocabulary already
partitions by mechanism: `binds_recruits` / `activates` (protein/complex),
`produces` (enzymatic second messenger), `upregulates` / `downregulates` /
`drives` (transcriptional), `suppresses` / `required_for` (functional),
`forms_pore_for` (localization/transport), `correlates` family (statistical).
Node identity carries the rest: a gene symbol is protein-level, `cGAMP` is a
metabolite, `cytoplasmic_mt_dsRNA` is a localized RNA species,
`retrotransposon_derepression` is a genomic-derepression state.
- *Cost:* level is implicit — recovering it requires reading verb+nodes.
- *Benefit:* zero new schema; the information is already present and already
  scored through the triple; nothing new to keep consistent.

**Design C — level as an optional, unscored `note` only where genuinely
ambiguous.** Add free-text only on the handful of edges where verb+node do not
disambiguate (e.g. an `activates` that is transcriptional vs post-translational).

**Verdict: Design B, with Design C as an escape hatch.** Recommend **not**
adding a scored `level` field. The molecular level is already encoded by the
relationship verb and the identity of the two nodes, and is already tested by
the relationship-match (triple) sub-metric — adding a parallel `level` enum
would duplicate that signal and create a second axis on which a correct edge can
be scored wrong, directly reintroducing the brittleness this redesign removes.
Where verb+node truly under-determine the layer (rare; e.g. distinguishing
transcriptional from post-translational `activates`), the curator should sharpen
the **verb** (introduce `phosphorylates` / `transcribes` to the controlled
vocabulary if a paper's mechanism demands it) rather than bolt on a level tag.
The one worked case in these three papers — STING1→RELA is post-translational
(S536 phosphorylation) while RELA→SASP is transcriptional — is already
unambiguous from the verbs (`activates` a protein vs `drives` a program) and the
node types (a kinase-substrate pair vs a TF→program pair), so no new field is
needed here.

## 6. Fields added, in one table

| Field | Values | Default | Scored effect |
|-------|--------|---------|---------------|
| `tier` | `core`, `supporting` | `core` | Selects the recall denominator the edge (or its equiv group) counts in. Core = headline; supporting = reported separately, never penalizes headline. |
| `equiv_group` | short id string | absent ⇒ singleton | Members collapse to one recoverable unit; recovering any one recovers the group; group counts once in its denominator. |
| `status: forbidden_shortcut` | that literal | absent | Edge excluded from all recall denominators; a draft edge matching it is a `shortcut_violation` (precision penalty), not an ordinary extra. |
| `status: excluded` / `score_exclude: true` | unchanged | absent | Known defect: dropped from scoring, not penalized. (Pre-existing.) |

All four are optional. A gold file using none of them is scored exactly as the
current scorer scores it today — the backward-compatibility guarantee that
`test_score_compendium.py` locks with a dedicated legacy-gold test.

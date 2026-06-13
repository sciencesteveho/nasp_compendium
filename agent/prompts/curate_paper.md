# Curate a Paper Into the NASP Compendium

Read first:
- `AGENTS.md`
- `agent/analysis_prompt.md`
- `agent/conventions.md`
- `agent/curation_lessons.md`
- Relevant existing files in `docs/compendium/`
- `nasp_compendium/summarize_compendium.py`
- `nasp_compendium/style.py`

Task:
- Curate one paper from its PDF in `data/literature/`.
- Before drafting edges, scan relevant curated files in `docs/compendium/` for style and chain organization.
- Extract mechanistic claims as YAML using the repo conventions.
- Add a `paper_scope` field under the paper metadata before edge drafting.
  Use one of: `mechanism_paper`, `perturbation_paper`,
  `cohort_correlation_paper`, `atlas_resource`,
  `biomarker_validation_paper`, `review_or_resource`, or
  `mixed_mechanism_and_correlation`. If the scope is mainly correlative or
  resource-like, do not emit causal edge verbs unless a direct perturbation in
  the paper supports the exact relationship. For resource/correlation papers,
  add `curation_density: core` by default unless the user explicitly requested
  an expanded satellite graph.
- Before drafting edges, create a `claims:` block. Each claim should be an
  atomic paper-supported statement with `claim_id`, `evidence_location`,
  `claim`, `assay`, `disposition`, `branch_type`, `graph_candidate`, and
  `support`. Use `disposition: edge`, `negative`, `context_only`, or
  `insufficient`.
- Use `branch_type` to make branch coverage auditable. Choose one of:
  `main_spine`, `sensor_branch`, `inflammatory_output`,
  `cohort_association`, `state_reversal`, `negative_specificity`,
  `organismal_outcome`, or `context_only`. Set `graph_candidate: true` when
  the claim should be considered for a graph edge even if you ultimately reject
  it; set `graph_candidate: false` only for assay/background/context claims.
- Add structured causal-support metadata when possible: `perturbation`,
  `measured_readout`, and `affected_entities`. Use `perturbation: none` only
  for genuinely unperturbed/cohort/resource claims. These fields are not graph
  nodes; they are audit metadata for evidence-strength review.
- Add a top-level `claim_edge_matrix:` block when one claim supports multiple
  chain edges or when evidence strength could be ambiguous. For each claim,
  list `mapped_edges:` with the exact `source`, `target`, `rel`, and
  `evidence_strength` supported by that claim. This is the typed support
  contract that prevents broad claims from justifying unrelated branches.
- Link each edge to one or more raw claims using `support_claims:`. The edge
  support should explain why those claims justify the exact source, target,
  relationship, and evidence-strength choice.
- Do not invent unsupported edges or collapse supported intermediates.
- Recover graph-useful branch edges, not just the main mechanistic spine.
- Preserve directly supported intermediates.
- Include negative findings as explicit edges.
- After drafting the main spine, run a branch checklist: in vivo outcome
  branches, cohort/correlation branches, cell-state branches, negative
  specificity controls, mechanistically reused cytokines, and net-effect edges
  explicitly supported by perturbation. Add graph-useful branches without
  creating shortcuts over supported intermediates.
- Before edge drafting, run a node-name canonicalisation pass: for every
  candidate node, search the existing compendium and `agent/vocabulary.yaml`
  for canonical synonyms, especially L1, mtDNA, mt-dsRNA, CCF, retroelement,
  chromatin accessibility/methylation/`epigenetic_remodeling`, tumorigenesis,
  fibrosis, and senescence terms. If a canonical synonym exists, use it. Add an
  `entity_resolution:` block documenting raw name, canonical name, status
  (`canonical`, `proposed`, `context_only`, or `rejected`), and rationale for
  ambiguous or newly proposed terms.
- Before finalizing program arms, run a regulator-promotion versus
  marker-demotion pass. Promote a regulator to a node when motif or
  regulatory-region evidence, concordant expression/activity, and an
  author-invoked mediator role are all present. Demote cytokine or qPCR/ELISA
  panel readouts to program-edge context unless an individual cytokine is
  mechanistically reused as another edge endpoint.
- Before finalizing organism-level outcomes, run a no-shortcut-to-phenotype
  pass. Route organismal phenotypes through tissue-level outcomes instead of a
  direct `gene -> organismal_phenotype` edge; for example, avoid
  `CGAS -> accelerated_aging` or `CGAS -> inflammaging` when the phenotype is
  mediated by `tissue_inflammation` or `fibrosis`.
- Before finalizing evidence labels, run an evidence-strength audit pass. For
  each edge, verify whether the exact relationship is directly measured,
  perturbation-supported, cohort-correlative, or only canonical. Do not upgrade
  co-occurrence to perturbation support, and do not downgrade directly measured
  activation or product formation to canonical inference. If linked claims
  include both a perturbation and a measured readout for the edge path, consider
  `perturbation_supported` before choosing `canonical_inferred` or
  `direct_measured`.
- Before finalizing the draft, run a claim-disposition checkpoint. Every claim
  marked `edge` or `negative` must be referenced by at least one edge unless it
  is deliberately changed to `context_only` or `insufficient`. Every
  `graph_candidate: true` claim that remains `context_only` or `insufficient`
  must have an explicit reason in `support`. Every edge must be linked to
  claims that justify the exact source, target, relationship, and evidence
  strength. If one broad claim is being used to support more than three edges,
  either split it into smaller atomic claims or add a `claim_edge_matrix` entry
  enumerating the exact edges it supports.
- Before finalizing parallel branches, run a branch-separation audit. For every
  regulator/motif branch and every sensor/inflammasome branch, ask whether the
  paper directly connects those branches or only supports them as parallel
  routes. Do not create a regulator-to-sensor or regulator-to-inflammasome edge
  unless the exact connection is supported.
- Run `compendium review_packet` before freezing the draft. If the packet reports
  hidden graph candidates, topology lints, verb warnings, evidence warnings,
  shortcut warnings, reagent endpoint warnings, matrix support gaps, or broad
  claim reuse, add a top-level `adjudications:` block and revise the draft or
  explicitly retain the choice. Each adjudication must include `issue_id`,
  `issue_type`, `decision`, and `rationale`; use optional `claim_id`, `edge`,
  `emitted_edges`, and `remove_edges` to tie the decision to exact claims or
  edges. Allowed issue types are `hidden_graph_candidate`, `topology_lint`,
  `shortcut_warning`, `verb_warning`, `evidence_strength_warning`,
  `reagent_endpoint_warning`, `broad_claim_reuse`,
  `gold_or_scope_disagreement`, and `scope_density_warning`. Allowed decisions
  are `emit_edge`, `revise_edges`, `keep_context`, `keep_insufficient`,
  `keep_as_is`, `needs_human_review`, and `reject_as_gold_defect`.
  `verb_warning` or `evidence_strength_warning` adjudicated as `keep_as_is`
  must include `rejected_alternative` and `convention_rule`. A high-priority
  hidden graph candidate kept out of the graph must include
  `nearest_intermediate_search:` with `searched: true` and
  `candidate_edges_considered:`.
- Apply these topology lints before freezing: do not make a generic process node
  such as `cytosolic_RNA_sensing` activate the specific sensors that instantiate
  it (`DDX58`, `IFIH1`); prefer direct ligand-to-sensor edges when a ligand and
  specific receptors are supported. Keep experimental reagents such as
  `dsDNA90` in context unless a human-readable adjudication overrides endpoint
  use. A broad inflammatory-output claim rejected as a shortcut does not
  discharge the branch audit; search for the nearest supported intermediate
  such as `STING1 activates NF-kB`. For atlas/resource papers, keep
  `curation_density: core` unless an expanded graph is explicitly adjudicated.
- Use existing curated files in `docs/compendium/` as style examples; match their level of context and support specificity.
- Use `cytoplasmic_retroelement_cDNA` for L1/retroelement-derived cytoplasmic cDNA or RNA-DNA hybrid intermediates; reserve `cytoplasmic_chromatin_fragments` for CCF biology.
- Use `cytoplasmic_retroelement_RNA` for retroelement-derived cytoplasmic RNA
  or dsRNA intermediates; keep ERV/L1/source identity and dsRNA details in
  context unless the source-specific species is itself graph-reusable.
- Do not replace perturbation-supported regulatory cytokine edges with `contains` edges; `SASP contains X` records measured program membership, while `STING1 upregulates X` or `JAK-STAT upregulates X` records causal regulation.
- Do not emit long per-cytokine edges from a multi-gene inflammatory panel.
  Collapse program readouts to program-level edges with marker names in context,
  unless the individual cytokine is the specific mechanistic output and is
  reused elsewhere as an edge endpoint.
- Keep drugs and inactive analogs in `context` when they are specificity controls for a reusable biological mechanism, such as 3TC/K-9 in L1 reverse-transcriptase-dependence experiments.
- For multiple negative paralog controls, make graph-useful specificity controls explicit and leave minor/redundant controls in context; flag the choice in the audit report.
- Avoid duplicate edges: if the same source, relationship, and target are
  supported in multiple contexts, create one edge and merge context/support
  instead of repeating the edge in separate chains.
- Put reagent, dose, tissue, cell line, timing, and perturbation details in `context`.
- Include exact support for every edge, ideally figure or extended-data panels.
- If unsure whether something is a node, list it in the audit report rather than inventing a new convention.

Output:
- Write the draft curation to `agent/reports/curation_runs/`.
- Include top-level blocks in this order when possible: `paper`, `claims`,
  `claim_edge_matrix`, `entity_resolution`, `proposed_terms` if needed,
  `adjudications` if review issues were resolved, then `edges`.
- Write any uncertainty notes or curation concerns to `agent/reports/audits/`.
- If asked to update the compendium, add or edit the relevant file in `docs/compendium/`.

Checks:
- Run `compendium validate --dir docs/compendium`.
- For draft-only calibration directories, run
  `compendium validate --dir calibration_drafts/` or the requested draft
  directory before comparing to gold.
- Validation errors are a stop condition: a draft with any validation error is
  not ready for review or commit. Fix errors before diffing or rendering.
- Skip-edge warnings are not automatic blockers, but every surviving skip-edge
  warning must be classified in per-paper notes as accepted false positive,
  intentional documented choice, or real catch.
- If the compendium changed, run:
  `compendium render_graph --directory docs/compendium --annotate-papers`
- Show diffs for human review.
- List remaining uncertainties explicitly.
- Do not commit.

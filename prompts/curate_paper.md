# Curate a Paper Into the NASP Compendium

Read first:
- `AGENTS.md`
- `analysis_prompt.md`
- `docs/compendium_conventions.md`
- `docs/curation_lessons.md`
- Relevant existing files in `docs/compendium/`
- `nasp_compendium/summarize_compendium.py`
- `nasp_compendium/style.py`

Task:
- Curate one paper from its PDF in `data/literature/`.
- Before drafting edges, scan relevant curated files in `docs/compendium/` for style and chain organization.
- Extract mechanistic claims as YAML using the repo conventions.
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
  candidate node, search the existing compendium and `nasp_compendium/vocabulary.yaml`
  for canonical synonyms, especially L1, mtDNA, mt-dsRNA, CCF, retroelement,
  chromatin accessibility/methylation/`epigenetic_remodeling`, tumorigenesis,
  fibrosis, and senescence terms. If a canonical synonym exists, use it; record
  unresolved divergences in an audit note.
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
  activation or product formation to canonical inference.
- Use existing curated files in `docs/compendium/` as style examples; match their level of context and support specificity.
- Use `cytoplasmic_retroelement_cDNA` for L1/retroelement-derived cytoplasmic cDNA or RNA-DNA hybrid intermediates; reserve `cytoplasmic_chromatin_fragments` for CCF biology.
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
- Write the draft curation to `reports/curation_runs/`.
- Write any uncertainty notes or curation concerns to `reports/audits/`.
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

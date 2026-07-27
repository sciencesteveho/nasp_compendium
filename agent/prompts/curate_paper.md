
# Curate a Paper Into the NASP Compendium

See `agent/prompts/_shared.md` for the Read-first set.

Task:
- Curate one paper from its PDF in `data/literature/`.
- Before drafting edges, scan relevant curated files in `docs/compendium/` for
  style and chain organization, and use them as the format template.
- Produce a `paper` block and an `edges` list following `agent/conventions.md`.
  That is the whole output format; there is no claims, adjudication, or
  entity-resolution layer.
- The rules for what becomes a node, what stays in `context`, which
  relationship and evidence-strength verb to use, and how to organize chains
  all live in `agent/conventions.md`. Apply them; do not restate them here.
  `agent/curation_lessons.md` covers the recurring judgment failures to watch
  for. The reminders below are the ones worth repeating at drafting time:
  - Recover graph-useful branch edges (in vivo outcomes, cohort/correlation
    arms, cell-state transitions, specificity controls), not just the spine.
  - Preserve directly supported intermediates; do not write shortcut edges that
    collapse a supported chain. Route organismal phenotypes through tissue-level
    outcomes rather than a direct `gene -> organismal_phenotype` edge.
  - Include negative and specificity findings as explicit
    `does_not_correlate` / `does_not_drive` edges.
  - Assign `evidence_strength` edge-by-edge from the actual experiment, not
    copied from the assay type.
  - Canonicalize every node name against the existing compendium and
    `agent/vocabulary.yaml` before drafting; if a canonical synonym exists, use
    it. New terms surface as validation warnings for later human review.
  - Put reagent, dose, tissue, cell line, timing, and perturbation details in
    `context`; give every edge an exact `support` (figure/extended-data panel).

Output:
- Write the draft curation (a `paper` block + `edges` list) to
  `agent/reports/curation_runs/`.
- Write any uncertainty notes or curation concerns to `agent/reports/audits/`.
- If asked to update the compendium, add or edit the relevant file in `docs/compendium/`.

Checks:
- See `agent/prompts/_shared.md`.
- Run the exact-draft review gate before presenting the draft as ready. Only
  validate `docs/compendium/` after a file there has actually been added or
  changed.

# Calibrate Against a Gold-Standard Curation

Read first:
- `AGENTS.md`
- `agent/analysis_prompt.md`
- `agent/conventions.md`
- `agent/curation_lessons.md`
- The existing gold-standard file in `docs/compendium/`
- The matching PDF from `data/literature/`
- `nasp_compendium/summarize_compendium.py`
- `nasp_compendium/style.py`

Task:
- Re-curate the paper from the PDF without editing the existing gold-standard file.
- Before drafting edges, scan the gold-standard file and relevant curated files for style and chain organization.
- Compare the draft against the curated file edge by edge.
- Identify missed mechanisms, overcalled edges, shortcut edges, naming drift, weak support, and missing negative findings.
- Recover graph-useful branch edges, not just the main mechanistic spine.
- Preserve directly supported intermediates.
- Include negative findings as explicit edges.
- Use existing curated files in `docs/compendium/` as style examples; compare context and support specificity, not only edge presence.
- Use `cytoplasmic_retroelement_cDNA` for L1/retroelement-derived cytoplasmic cDNA or RNA-DNA hybrid intermediates; reserve `cytoplasmic_chromatin_fragments` for CCF biology.
- Check whether `contains` edges and perturbation-supported regulatory edges are being used for distinct meanings; `contains` should not replace causal edges such as `STING1 upregulates X` or `JAK-STAT upregulates X`.
- Keep drugs and inactive analogs in `context` when they are specificity controls for a reusable biological mechanism, such as 3TC/K-9 in L1 reverse-transcriptase-dependence experiments.
- For multiple negative paralog controls, report whether they should be explicit graph edges or remain in context for human review.
- If unsure whether something is a node, list it in the audit report rather than inventing a new convention.
- Treat differences as calibration findings, not automatic fixes.

Output:
- Write the draft curation to `agent/reports/curation_runs/`.
- Write the calibration audit to `agent/reports/audits/`.
- Do not overwrite existing curated files during calibration.

Checks:
- Run `compendium validate --dir docs/compendium`.
- If the compendium changed, run:
  `compendium render_graph --directory docs/compendium --annotate-papers`
- Show diffs for human review.
- List calibration lessons and remaining uncertainties.
- Do not commit.

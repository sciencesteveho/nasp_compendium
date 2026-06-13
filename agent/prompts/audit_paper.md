# Audit One Compendium Paper

Read first:
- `AGENTS.md`
- `agent/analysis_prompt.md`
- `agent/conventions.md`
- The target file in `docs/compendium/`
- Relevant PDFs from `data/literature/`
- `nasp_compendium/summarize_compendium.py`
- `nasp_compendium/style.py`

Task:
- Audit one curated compendium file against the source PDF.
- Check that every edge is supported, atomic, and uses canonical node names.
- Check that negative findings are represented as explicit edges.
- Check that edge `context` includes model, perturbation, dose, timing, cell type, and tissue details where relevant.
- Check that `support` identifies exact figures or extended-data panels.

Output:
- Write the audit report to `agent/reports/audits/`.
- If fixes are requested, keep edits narrow and avoid unrelated rewrites.

Checks:
- Run `compendium validate --dir docs/compendium`.
- If the compendium changed, run:
  `compendium render_graph --directory docs/compendium --annotate-papers`
- Show diffs for human review.
- List unresolved evidence or naming uncertainties.
- Do not commit.

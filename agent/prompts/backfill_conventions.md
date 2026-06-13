# Backfill Compendium Conventions

Read first:
- `AGENTS.md`
- `agent/analysis_prompt.md`
- `agent/conventions.md`
- Target files in `docs/compendium/`
- Relevant PDFs from `data/literature/` when evidence needs verification
- `nasp_compendium/summarize_compendium.py`
- `nasp_compendium/style.py`

Task:
- Backfill existing compendium entries to match current conventions.
- Prefer canonical node names from `agent/conventions.md`.
- Preserve supported intermediates; do not replace chains with shortcut edges.
- Keep evidence, context, and support faithful to the source paper.
- Do not modify existing compendium files unless the requested backfill requires it.

Output:
- For exploratory work, write notes or draft patches to `agent/reports/curation_runs/`.
- For audit findings, write reports to `agent/reports/audits/`.

Checks:
- Run `compendium validate --dir docs/compendium`.
- If the compendium changed, run:
  `compendium render_graph --directory docs/compendium --annotate-papers`
- Show diffs for human review.
- List any convention choices that still need human review.
- Do not commit.

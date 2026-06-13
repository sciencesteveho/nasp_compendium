# Audit the NASP Compendium

Read first:
- `AGENTS.md`
- `agent/analysis_prompt.md`
- `agent/conventions.md`
- All relevant files in `docs/compendium/`
- Relevant PDFs from `data/literature/`
- `nasp_compendium/summarize_compendium.py`
- `nasp_compendium/style.py`

Task:
- Audit the compendium for schema, naming, edge, and evidence consistency.
- Look for duplicate or near-duplicate nodes.
- Look for shortcut edges that skip supported intermediates.
- Look for missing negative findings and unsupported mechanistic edges.
- Compare recurring nodes and relationships across papers for convention drift.

Output:
- Write the audit report to `agent/reports/audits/`.
- Include concrete file and edge references.
- Separate hard errors, curation warnings, and optional cleanup suggestions.

Checks:
- Run `compendium validate --dir docs/compendium`.
- If the compendium changed, run:
  `compendium render_graph --directory docs/compendium --annotate-papers`
- Show diffs for human review.
- List remaining uncertainties explicitly.
- Do not commit.


# Backfill Compendium Conventions

See `agent/prompts/_shared.md` for the Read-first set.

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
- See `agent/prompts/_shared.md`.

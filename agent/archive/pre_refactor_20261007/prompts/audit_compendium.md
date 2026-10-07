
# Audit the NASP Compendium

See `agent/prompts/_shared.md` for the Read-first set.

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
- See `agent/prompts/_shared.md`.

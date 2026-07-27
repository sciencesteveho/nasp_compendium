
# Audit One Compendium Paper

See `agent/prompts/_shared.md` for the Read-first set (target: the file under audit in `docs/compendium/`).

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
- See `agent/prompts/_shared.md`.

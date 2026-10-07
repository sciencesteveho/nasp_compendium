
# Audit a Frozen Draft Against a Revealed Reference

This is a non-blind reference audit, not an extraction or generalization test.
Use it only after the draft has been frozen and its hash recorded. See
`agent/prompts/_shared.md` for the Read-first set; the matching PDF and revealed
reference are additional audit inputs.

Task:
- Do not re-curate or edit the frozen draft after reading the reference.
- Compare the frozen draft against the reference edge by edge, following the node,
  edge, and evidence rules in `agent/conventions.md`.
- Identify missed mechanisms, overcalled edges, shortcut edges, naming drift, weak support, and missing negative findings.
- For multiple negative paralog controls, report whether they should be explicit graph edges or remain in context for human review.
- If unsure whether something is a node, list it in the audit report rather than inventing a new convention.
- Treat differences as calibration findings, not automatic fixes.

Output:
- Write the calibration audit to `agent/reports/audits/`.
- Record the frozen draft hash and classify reference disagreements; do not
  overwrite the draft, reference, or existing curated files.

Checks:
- See `agent/prompts/_shared.md`.
- Additionally, list calibration lessons and remaining uncertainties.

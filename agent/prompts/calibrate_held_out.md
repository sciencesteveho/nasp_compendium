# Evaluate extraction without exposing answers

Use fresh sessions for each arm. Give both the same PDF/supplements, model,
tool access and budget. Freeze instruction hashes. Run the old archived prompt
and the current extraction prompt on four fresh papers, twice per arm;
counterbalance order. Do not expose golds, prior outputs, reference audits or
one arm's findings to the other. Previously discussed papers are regressions.

Use a source-only workspace and fresh conversation per run, with filesystem
access restricted to that paper, its supplements, the assigned instructions,
vocabulary and output directory. An instruction not to open golds in a shared
repository is insufficient isolation. Keep reference preparation separate.

Freeze every output and hash before revealing a source-vetted, human-ratified
reference. Use an isolated accepted-compendium directory during preparation
and review so collective previews do not reveal answers. Then run
`compendium score --draft DRAFT --gold REFERENCE --format json`.

Report correct signed mechanism recall, evidence agreement, forbidden claims,
and source-adjudicated precision per paper, with paper type and source coverage.
Adjudicate unmatched extras and missing reference claims directly against the
paper. Alternate representations of one finding may be equivalent; independent
biological branches must not share an equivalence group. Exclude unresolved
reference claims from denominators. Keep inference in supporting recall.

Record human review time, source lookups, edits and observable time/tokens/cost.
Proposed acceptance targets: >=95% source-adjudicated precision, >=90% core
recall on each mechanistic paper, zero false core/sign/citation claims, and
median human review <=15 minutes. A no-mechanism/resource paper tests appropriate
abstention and endpoint fidelity. Software tests do not establish these targets.

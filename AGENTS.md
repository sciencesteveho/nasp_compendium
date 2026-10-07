# NASP compendium agent instructions

Curate source-supported mechanistic claims about nucleic-acid sensing in aging,
senescence, inflammation and related disease. Accepted `docs/compendium/*.md`
records contain YAML (`paper` + `edges`) and feed the collective graph.

## Paper extraction and review

Start at `agent/prompts/curate_paper.md`. Read only its scientific/schema
reference, `agent/extraction_contract.md`, and `agent/vocabulary.yaml` before
extraction. Renderer source, historical lessons and reference answers are not
required reading. For record audits use `agent/prompts/audit_paper.md`.

Keep draft runs, extracted text and page images under ignored
`agent/reports/curation_runs/`. Source PDFs live in `data/literature/`; never copy
PDFs or full extracted text into tracked paths. Summarize evidence without
reproducing long copyrighted passages.

Golds (`*.gold.md`) are evaluation references, excluded from ordinary graphs.
Never read them as extraction examples. A user-requested reference audit may
read its target golds; it is not a blind evaluation. Keep reference candidates
outside `docs/compendium/` and preserve originals. Scientific approval is
required before promotion. Never commit; the user makes all commits.

Gate the exact draft before rendering or presenting it as ready. The extraction
workflow produces a frozen graph/evidence review and a proposed collective diff.
Show unresolved findings and source gaps explicitly. Validation does not certify
biology. If accepted files change, validate the collection, show the diff and
render the updated graph.

Independent recall/precision review is optional; follow
`agent/prompts/curate_paper_multi_agent.md` when explicitly selected. The parent
is the sole writer, freezes the draft, keeps reviewers blind to references and
each other, and adjudicates every finding against the paper.

## Coding and API conventions

For changes to code, tests, configuration, packaging, executable workflows,
or technical documentation:

1. Read `.agents/skills/coding-style/SKILL.md` completely.
2. Use its routing table to read every applicable concern reference before
   editing.
3. Apply this root contract and all selected references together.

The skill contains the repository's authoritative software-engineering and
Python API standards. Prefer an existing codebase convention only when it is
more specific and does not conflict with an explicit skill rule.

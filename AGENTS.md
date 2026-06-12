# NASP compendium agent instructions

## Project purpose

This repository curates mechanistic claims about nucleic-acid sensing pathways
(NASPs) in aging, senescence, inflammaging, and related disease contexts.

The central artifact is a set of per-paper compendium files in
`docs/compendium/`. These files are parsed as YAML and rendered into a
mechanistic pathway graph.

## Files Codex must read before curation tasks

Before curating, auditing, or backfilling papers, read:

- `analysis_prompt.md`
- `docs/compendium_conventions.md`
- `docs/curation_lessons.md`
- Relevant existing files in `docs/compendium/`
- `nasp_compendium/summarize_compendium.py`
- `nasp_compendium/style.py`

## Repository layout

- `docs/compendium/`: per-paper mechanistic YAML-in-Markdown files.
- `docs/compendium_conventions.md`: naming, edge, and evidence conventions.
- `docs/marker_genes/`: rendered marker-gene documentation.
- `data/literature/`: local PDFs for curation. These files are not committed.
- `reports/curation_runs/`: draft summaries and temporary curation outputs.
- `reports/audits/`: audit reports.
- `reports/graph_diffs/`: rendered graph comparisons or notes.
- `prompts/`: reusable task prompts for Codex-assisted curation.

## Core commands

Install locally:

```bash
pip install -e .
````

Render the graph:

```bash
compendium render_graph --directory docs/compendium --annotate-papers
```

Trace an entity:

```bash
compendium trace CGAS --directory docs/compendium
```

Validate the compendium:

```bash
compendium validate --dir docs/compendium
```

Diff compendium states for review:

```bash
compendium diff OLD_PATH NEW_PATH --format text
```

## Curation rules

* Do not invent unsupported mechanistic edges.
* Do not collapse supported intermediates into shortcut edges.
* Negative findings are explicit edges, not omissions.
* Prefer gene-level edges when the paper directly tests a gene.
* Use canonical node names from `docs/compendium_conventions.md`.
* Read `docs/curation_lessons.md` for known failure patterns and judgment calls before drafting edges.
* Apply the node anti-pattern, marker/regulator, pore-mediated-release, and
  no-shortcut sections in `docs/compendium_conventions.md` before emitting
  edges; use `docs/curation_lessons.md` for the current calibration lessons.
* Before emitting edges, apply the node-name canonicalisation,
  regulator-promotion/marker-demotion, evidence-strength audit, branch-audit,
  duplicate-edge, and no-shortcut-to-phenotype checks from
  `docs/compendium_conventions.md`, `docs/curation_lessons.md`, and
  `prompts/curate_paper.md`.
* Do not create nodes for expression states, tissue-specific outcomes, or protein modification states.
* Put reagent, dose, tissue, cell line, timing, and perturbation details in `context`.
* Every edge must include exact support, ideally figure panels or extended-data panels.
* When uncertain, leave a note in the audit report instead of silently guessing.
* Validation failure is a stop condition. Do not treat validation errors as
  cleanup noise; fix them before diffing, rendering, or presenting a draft as
  ready.

## Done criteria

For curation or backfill tasks, done means:

1. The relevant `.md` file parses as YAML.
2. `compendium validate --dir docs/compendium` passes.
3. For compendium-modifying patches, `compendium diff` is run before final
   review so entity and edge changes are visible in text.
4. `compendium render_graph --directory docs/compendium --annotate-papers` runs.
5. The diff is shown for human review.
6. Remaining uncertainties are listed explicitly.

## Human-gated steps

Never commit automatically and never commit. All commits must be done manually by user.

Never overwrite a carefully curated existing paper file during calibration.
For calibration, write drafts into `reports/curation_runs/` and compare against
the existing file.

Never copy PDFs from `data/literature/` into tracked paths.
Never commit PDFs or extracted full-text paper files unless explicitly requested.
Curation reports may summarize findings but must not reproduce long copyrighted passages.

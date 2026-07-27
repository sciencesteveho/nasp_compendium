# Shared prompt fragments

Every curation prompt in this directory references this file for its common
"Read first" set and "Checks" footer, so those live in exactly one place.

## Read first

- `AGENTS.md`
- `agent/conventions.md` — the normative rulebook (naming, nodes, edge schema,
  relationship and evidence-strength vocabulary, chain organization)
- `agent/analysis_prompt.md` — the paper-analysis prompt and YAML skeleton
- `agent/curation_lessons.md` — recurring judgment failures to watch for
- `nasp_compendium/summarize_compendium.py` and `nasp_compendium/style.py`
- The task's non-gold target files in `docs/compendium/` and any relevant PDFs
  in `data/literature/`. Calibration prompts define when a revealed gold may be
  read; never infer access from this shared list.

## Checks

- Gate the artifact produced by the task. For a draft, run
  `compendium review_packet <draft> --out <review-packet> --gate`; file-mode
  review validates that exact draft. Do not substitute validation of an
  unchanged `docs/compendium/` directory. For a promoted or edited compendium
  file, also run `compendium validate --dir docs/compendium`.
- Validation errors are a stop condition: a draft with any error is not ready
  for review or promotion.
- Skip-edge warnings are advisory, not blockers, but classify each surviving
  one in per-paper notes as an accepted false positive, documented choice, or
  real catch.
- If the compendium changed, run
  `compendium render_graph --compendium-path docs/compendium --annotate-papers`.
- Show diffs for human review and list remaining uncertainties explicitly.
- Do not commit.

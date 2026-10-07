# Curate a Paper With Independent Recall and Precision Review

This is an opt-in extension of `agent/prompts/curate_paper.md`. It preserves the
same YAML-in-Markdown schema, exact-draft gate, and human-controlled promotion.
The parent agent is the only writer and acts as both curator and adjudicator.

## Inputs

The invocation must provide:

- `<paper_id>`;
- `<paper_path>`, normally `data/literature/<paper_id>.pdf`.

See `agent/prompts/_shared.md` for the normal read-first set. Follow
`agent/prompts/curate_paper.md` for extraction. During blind curation, do not
open or search `*.gold.md`, `agent/calibration/`, `docs/claim_traces.md`,
`docs/design_decisions.md`, `docs/gold_standard_redesign.md`, or prior reports
that could reveal expected edges.

## Non-negotiable boundaries

- Only the parent may write drafts, review packets, audit reports, or figures.
- Reviewers are independent, read-only advisers. They never edit repository
  files and never receive one another's findings.
- There is one authoritative human-review candidate: the revised draft. The
  frozen initial draft is retained only as immutable review evidence.
- Reviewer recommendations are proposals, not decisions. Do not use voting.
- Never write to `docs/compendium/`, promote, overwrite a curated file, or
  commit in this workflow.

## Workflow

### 1. Curate and freeze the initial draft

1. The parent alone curates the paper and writes
   `agent/reports/curation_runs/<paper_id>.initial.draft.md`.
2. Run the exact-file gate:

   ```sh
   compendium review_packet \
     agent/reports/curation_runs/<paper_id>.initial.draft.md \
     --out agent/reports/audits/<paper_id>.initial.review_packet.md \
     --gate
   ```

3. Resolve blocking validation errors before freezing. Advisory findings still
   require scientific judgment; the gate is not a biology score.
4. Compute the initial draft's SHA-256 and record its path and hash in
   `agent/reports/audits/<paper_id>.multi_agent_review.md`.
5. Declare the initial draft frozen. Never edit, replace, or regenerate it
   after recording the hash.

### 2. Run two independent reviews in parallel

Prepare both reviewer task messages before starting either reviewer. Give each
only the same `<paper_path>`, frozen draft path, recorded SHA-256, and normal
non-gold repository instructions. Do not state an expected finding, edge,
answer, or finding count.

Spawn these configured custom agents before waiting for either result:

- `recall_reviewer`: search only for omitted paper-supported mechanisms;
- `precision_reviewer`: audit only emitted content for unsupported or incorrect
  representation.

Do not pass a result, partial result, hint, or follow-up from one reviewer to
the other. Wait until both reviewers have returned. Do not revise any draft
while either review is running.

Each reviewer must return concrete finding IDs, proposed edge changes, and
exact figure, panel, extended-data, or textual support. Treat vague advice as
non-actionable rather than guessing what the reviewer meant.

### 3. Adjudicate and write one revised draft

1. Recompute the frozen draft's SHA-256. If it differs from the recorded hash,
   stop and report that the review input was not preserved.
2. Check every reviewer finding and every proposed edge action directly against
   the paper and repository conventions. If one finding bundles multiple
   changes, adjudicate each change separately. Agreement between reviewers is
   not evidence by itself, and disagreement is not resolved by voting.
3. In `<paper_id>.multi_agent_review.md`, record every finding with:

   - finding ID and reviewer role;
   - decision: `accept`, `reject`, or `modify`;
   - exact paper support checked by the parent;
   - applicable convention;
   - rationale and resulting edge change, or the reason no change was made.

4. Record counts of findings reviewed, accepted, rejected, and modified, plus
   source lookups and elapsed adjudication time when observable.
5. Copy the frozen content into
   `agent/reports/curation_runs/<paper_id>.reviewed.draft.md`, then apply only
   parent-adjudicated changes to that revised file. The parent remains its sole
   writer. Do not add adjudication fields to the compendium YAML schema.

### 4. Validate and hand off for human review

Run the exact-file gate on the revised draft and resolve all blockers:

```sh
compendium review_packet \
  agent/reports/curation_runs/<paper_id>.reviewed.draft.md \
  --out agent/reports/audits/<paper_id>.reviewed.review_packet.md \
  --gate
```

Show the review delta:

```sh
compendium diff \
  agent/reports/curation_runs/<paper_id>.initial.draft.md \
  agent/reports/curation_runs/<paper_id>.reviewed.draft.md \
  --format text
```

Render from a temporary directory containing only a copy of the revised draft.
Do not point the renderer at `docs/compendium/` during blind review because the
combined renderer includes `.gold.md` inputs:

```sh
compendium render_graph \
  --compendium-path <isolated-revised-draft-directory> \
  --annotate-papers \
  --out agent/reports/graph_diffs/<paper_id>.review.svg
```

Recompute and record the revised draft's SHA-256. Present the revised draft,
review packet, diff, render, adjudication report, and remaining uncertainties
to the human. Stop before promotion. Because this workflow does not change
`docs/compendium/`, full-compendium validation and rendering are deferred until
a human explicitly promotes the draft in a separate task.

For a blind evaluation, freeze both the single-agent and multi-agent outputs
before any reference is revealed. Scoring is performed only afterward under
`agent/prompts/calibrate_held_out.md`; never let a reviewer inspect the
reference.

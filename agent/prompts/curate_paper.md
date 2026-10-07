# Extract one paper

Inputs: paper PDF, paper ID, and any available supplementary PDFs.
Read `agent/extraction_contract.md` and `agent/vocabulary.yaml`.
Do not read golds, previous extractions, audit answers or calibration reports
when producing a fresh extraction. No renderer source-code reading is required.

1. Prepare a new ignored run:

   ```sh
   compendium prepare_paper data/literature/PAPER.pdf \
     --paper-id author_2026 --run-dir agent/reports/curation_runs/RUN \
     --supplement data/literature/SUPPLEMENT.pdf
   ```

   Omit `--supplement` when unavailable. Inspect `run.json`, indexed page text
   and sparse-text pages. Check the PDF title/version and whether cited
   supplementary material is present. Missing material is a visible limitation.

2. Read source-first. Identify central experiments, resolved intermediates,
   branches and relevant controls before naming nodes. Inspect decisive figures
   with `compendium render_page PDF PAGE --out RUN/page-N.png`. Keep concise
   working findings and unresolved interpretations in `RUN/notes.md`; no
   exhaustive figure presentation or second claims schema is required.

3. Write `RUN/draft.md` using the contract. For each edge check the actual
   intervention/readout, direction, evidence, context and page/panel locator.
   Revisit Results once for omitted core findings. Background continuity and
   associations must be distinguished from paper-established mechanisms.

4. Run the exact draft gate, fix blockers, then freeze the evidence review:

   ```sh
   compendium review_packet RUN/draft.md --out RUN/packet.md --gate
   compendium review_paper RUN RUN/draft.md --supplements complete \
     --notes-file RUN/notes.md --model OBSERVED_MODEL
   ```

   Set supplements to `missing` with specifics or `not_applicable` when checked.
   For no in-scope findings, explain why in notes and use `review_paper
   --no-findings`; it performs the exact gate with that explicit disposition.
   Record only observable model/settings/time/cost; do not invent telemetry.

5. Inspect the generated `reviews/review-NNNN/review.html`: select claims,
   follow page evidence, check signs and inferred/association controls, and
   inspect the proposed collective graph and text diff. Repair the working
   draft and rerun; prior review revisions remain frozen.

Hand off the latest review link, scientific uncertainties and proposed changes.
Human approval is required for promotion into `docs/compendium/`; never commit.
For an approved promotion, copy the reviewed record, validate the collection,
show `compendium diff` and render the updated graph. Keep source assets local.

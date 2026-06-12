# Curation Retrospective

Read first:
- `AGENTS.md`
- `docs/curation_lessons.md`
- `docs/compendium_conventions.md`
- Recent reports in `reports/audits/`
- Recent prompt changes in `prompts/`
- Relevant curated files in `docs/compendium/`

Task:
- Distill durable curation lessons from recent audits since the last
  retrospective entry.
- Compare candidate lessons against `docs/curation_lessons.md`; do not repeat
  lessons already captured there.
- Classify each new lesson as one of:
  - failure pattern
  - vocabulary clarification
  - convention edge case
- For each lesson, identify the source audit and paper or workflow it came
  from.
- Note whether the lesson should remain a lesson or be proposed for promotion
  to `docs/compendium_conventions.md` as a rule.
- Update the calibration history proposal with new calibration targets,
  dates, audits, and headline lessons.

Output:
- Write a proposal report to
  `reports/audits/curation_retro_YYYYMMDD.md`.
- In that report, include proposed additions to `docs/curation_lessons.md`
  grouped by section.
- Do not silently rewrite `docs/curation_lessons.md`.
- Do not edit curated compendium files.
- Do not commit.

Checks:
- Run `compendium validate --dir docs/compendium`.
- If any compendium file changed, run:
  `compendium render_graph --directory docs/compendium --annotate-papers`
- Show diffs for human review.
- List lessons that should be promoted to conventions separately from lessons
  that should remain as judgment patterns.

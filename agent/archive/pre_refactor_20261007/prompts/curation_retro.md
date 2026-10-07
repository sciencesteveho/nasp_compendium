
# Curation Retrospective

Read first:
- See `agent/prompts/_shared.md` for the Read-first set.
- Recent reports in `agent/reports/audits/`
- Recent prompt changes in `agent/prompts/`

Task:
- Distill durable curation lessons from recent audits since the last
  retrospective entry.
- Compare candidate lessons against `agent/curation_lessons.md`; do not repeat
  lessons already captured there.
- Classify each new lesson as one of:
  - failure pattern
  - vocabulary clarification
  - convention edge case
- For each lesson, identify the source audit and paper or workflow it came
  from.
- Note whether the lesson should remain a lesson or be proposed for promotion
  to `agent/conventions.md` as a rule.
- Update the calibration history proposal with new calibration targets,
  dates, audits, and headline lessons.

Output:
- Write a proposal report to
  `agent/reports/audits/curation_retro_YYYYMMDD.md`.
- In that report, include proposed additions to `agent/curation_lessons.md`
  grouped by section.
- Do not silently rewrite `agent/curation_lessons.md`.
- Do not edit curated compendium files.
- Do not commit.

Checks:
- See `agent/prompts/_shared.md`.
- Additionally, list lessons that should be promoted to conventions separately
  from lessons that should remain as judgment patterns.

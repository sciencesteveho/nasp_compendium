---
name: coding-style
description: >-
  Apply NASP Compendium software-engineering standards for code style, API
  design, testing, packaging, configuration, command-line interfaces, and
  technical documentation.
---

# Apply NASP Compendium Coding Standards

Apply the root `AGENTS.md` contract first. Use this skill to load detailed
standards by stable software-engineering concern rather than by package or
module.

## Route the Task

Read each selected reference completely before editing. Select all that apply:

- Always read [core-engineering.md](references/core-engineering.md) for scope,
  architecture, repository safety, and handoff.
- Read [python-api-design.md](references/python-api-design.md) for Python code,
  public APIs, modules, docstrings, typing, errors, logging, dataclasses, or CLI
  entry points.
- Always read [testing-validation.md](references/testing-validation.md) when
  changing code, tests, configuration, packaging, or executable workflows.

Do not load every reference reflexively. Load the complete set required by the
task; concern boundaries may overlap.

## Interpret Examples

Treat `Avoid` and `Prefer` examples as calibration for the rule immediately
around them. Preserve the demonstrated property, but adapt names and domain
details to the task. Examples are illustrative rather than exhaustive; they do
not authorize copying an abstraction or feature the task does not need.

## Execute

1. Inspect the worktree, relevant public interfaces, and nearby tests.
2. Determine task-specific behavioral and engineering contracts.
3. Implement the smallest correct change under the selected references.
4. Validate from the narrowest relevant check outward.
5. Re-read the diff and hand off exact validation results plus a suggested
   Conventional Commit message.

Do not substitute a reference summary for reading the selected file. Do not
weaken a rule merely because the current module layout changes.

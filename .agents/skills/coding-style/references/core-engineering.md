# Core Engineering and Scope

## Contents

- Scope and repository safety
- Architecture
- Constants and configuration
- Git and handoff

## Scope and Repository Safety

- Make the smallest correct change that satisfies the task.
- Do not modify working code, docstrings, comments, formatting, or tests outside
  scope unless correctness requires it.
- Preserve existing behavior unless the task explicitly requests a change.
- Inspect `git status` and relevant diffs before editing. Existing and untracked
  changes belong to the user unless proven otherwise; preserve them.
- Search references before retaining or introducing a global, API, helper,
  dependency, output key, or file format.
- Do not overwrite, delete, migrate, or regenerate user data without explicit
  authority and a validated recovery path.

## Architecture

- Prefer small, focused functions that compose cleanly over monoliths.
- Prefer small, reusable modules with one clear purpose over catch-all modules.
  Create a module only when it adds reusable value and has a clear scope.
- Do not use single-consumer mixins solely to split a class across files.
- Apply modularity pragmatically. Support a plausible next analysis when that
  clarifies current scientific logic or a concrete extension; avoid speculative
  indirection.
- Do not add a thin wrapper that only renames, forwards, or lightly repackages
  another function. A wrapper must coordinate meaningful steps, isolate
  non-trivial behavior, expose a stable boundary, or clarify reusable logic. It
  must not exist only to satisfy a type checker.
- At one call site, keep simple tuple/dict construction and boolean-to-value
  translation inline. Extract only a cohesive stage, branch, or invariant; line
  count alone does not justify a helper.
- Name modules and functions for their narrow domain result. Avoid generic
  `helpers`, `utils`, `genes`, or `metadata` names when a precise responsibility
  such as resolution, aggregation, or visualization is available.
- When splitting a large public module, use a descriptively named subpackage and
  preserve the original import path as its facade. Avoid `_module.py` domain
  splits; use names such as `aggregation.py`, `continuous.py`, or
  `categorical.py`.
- Put large scientific orchestration in `workflows.py` after a package spans
  several implementation files. Name workflows for their result, such as
  `summarize_dataset`, not `run_*`. CLI entry points still use `main()`.
- Large workflows may use sparse one-line phase comments when they improve
  auditability: load, prepare, analyze, and write.
- A long workflow body must remain a flat sequence of substantive stage calls.
  Move branch-heavy computation into cohesive stages, but keep forwarding and
  argument repackaging inline.
- Treat dependency pins, output tables, serialized schemas, container keys,
  downstream filenames, and manifests as public contracts. Change them
  deliberately and validate consumers.

Example—add behavior, not forwarding layers:

```python
# Avoid: this wrapper only renames an existing operation.
def get_records(path: Path) -> list[Record]:
    """Return records loaded from `path`."""
    return load_records(path)


# Prefer: call `load_records` directly, or add a helper that owns real logic.
def prepare_records(
    path: Path,
    *,
    minimum_quality: float,
) -> list[Record]:
    """Load records and retain those meeting the quality threshold."""
    records = load_records(path)
    return [record for record in records if record.quality >= minimum_quality]
```

## Constants and Configuration

- Keep module scope limited to imports, a logger, `__all__`, type aliases, and
  genuinely shared immutable constants. Treat mutable class attributes and
  registries as global state too; an underscore, `ClassVar`, or uppercase name
  changes visibility or notation, not ownership or mutability.
- Before retaining or adding a module or class constant, identify its owning
  concept and verify one of these conditions:
  1. At least two independent runtime consumers require exactly the same stable
     value, and this module is their authoritative owner.
  2. The name captures stable scientific or domain meaning that an unexplained
     literal would lose.
  Definition plus one use, tuple expansion, cleanup derived from a producer,
  and tests of the same implementation do not count as independent consumers.
- Avoid globals used only once. Keep incidental values local or make them
  function defaults. Do not move a value to a class attribute or a zero-argument
  helper merely to disguise global configuration.
- Repeated column names, generated keys, delimiters, and filenames usually
  belong as keyword-only defaults on the function that owns the output. When a
  coherent configuration must travel through multiple stages, instantiate a
  frozen dataclass at the workflow boundary and pass it explicitly.
- Do not keep mutable lists, dictionaries, sets, palettes, registries, or
  configuration objects at module or class scope. Construct them per call or
  per instance. A justified shared collection must be immutable to callers.
- Give schemas, filenames, and artifact plans one authoritative owner. Derive
  downstream manifests, cleanup targets, and empty outputs from that owner or
  from artifacts actually produced; do not maintain parallel module registries
  that can drift.
- Put shared physical parameters, thresholds, and tuning values in a dedicated
  constants module, grouped by purpose.
- Name constants in `UPPER_SNAKE_CASE` and annotate their types.
- Keep paths, resources, environments, and scheduler settings configurable. Do
  not encode a developer machine or transient infrastructure state.

Example—keep one-owner values with their owner:

```python
# Avoid: a module constant used by only this function.
_DEFAULT_RETRIES: int = 3


def fetch_records(url: str) -> list[Record]:
    """Fetch records from `url`."""
    return request_records(url, retries=_DEFAULT_RETRIES)


# Prefer: expose a local policy as a function default.
def fetch_records(url: str, *, retries: int = 3) -> list[Record]:
    """Fetch records from `url`."""
    return request_records(url, retries=retries)
```

Promote `retries` to a shared constant only when independent callers must use
the same stable policy or the name carries important domain meaning.

Before handoff, inspect every module-level assignment and mutable class
attribute added or retained in changed files. Remove or relocate each value
that fails the ownership test above, and check that the refactor did not create
a second schema, filename list, palette, or configuration source of truth.
Use a text or AST scan over the changed Python paths to enumerate candidates;
do not treat passing Ruff, typing, or tests as evidence that this audit passed,
because those checks generally permit module and class state.

## Git and Handoff

- Re-read the diff for correctness, style, tests, documentation, scientific
  interpretation, API/schema changes, and accidental edits.
- Do not run `git commit`, `git push`, or another state-changing Git command.
- Suggest a Conventional Commit:
  `<type>(<scope>): <description>`, where type is `feat`, `fix`, `docs`,
  `style`, `refactor`, `perf`, `test`, `chore`, or `ci`.
- Make the subject explain why the change matters. Use imperative mood, begin
  with a capital letter, omit the final period, and stay near 72 characters.
- Add a body when the subject is insufficient. For a feature, state the new
  capability or short usage; for a fix, explain the failure and remedy. Add
  `Fixes #<n>` only when an applicable issue exists.

Example—state the reason the change matters:

```text
# Avoid: describes mechanics only.
fix(io): Add a validation condition

# Prefer: identifies the prevented failure.
fix(io): Reject incomplete files before downstream reads
```

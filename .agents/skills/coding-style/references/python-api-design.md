# Python and API Design

## Contents

- Style, imports, names, and comments
- Public surface and ordering
- Functions and documentation
- Typing and signatures
- Dataclasses
- Defensive code and exceptions
- Logging and output
- Command-line entry points

## Style, Imports, Names, and Comments

- Follow the Google Python Style Guide and use 4-space indentation.
- Keep imports at module scope; do not add inline function imports.
- Use standard module aliases, including `numpy as np` and `pandas as pd`,
  rather than importing common functions/classes directly.
- Use Pythonic, descriptive names. Reserve single-letter names for very local,
  conventional uses.
- Within functions, use blank lines between validation, setup, transformation,
  and output blocks; keep tightly coupled statements together.
- Comments explain non-obvious reasoning or scientific constraints. Do not add
  decorative comments or restate code.
- Do not cite design documents, RFCs, tickets, or issue numbers in source
  comments; put that context in a commit or pull request.

Example—import modules under their standard aliases:

```python
# Avoid
from numpy import concatenate
from pandas import concat

# Prefer
import numpy as np
import pandas as pd

values = np.concatenate(chunks)
table = pd.concat(frames)
```

## Public Surface and Ordering

- Prefix internal functions, methods, and classes with `_`; public user-facing
  names must not begin with `_`.
- Do not import `_`-prefixed internals across package boundaries.
- Put primary public functions, classes, and user-facing methods near the top,
  after imports, constants, and dataclasses needed to understand them. Put
  private helpers below. Keep CLI `main()` near the bottom beside its guard.
- A package exporting public names must expose them explicitly from
  `__init__.py` and list them in `__all__`.
- Re-export only names intentionally supported as package-level API.
- Put `__all__` after imports/module globals and before definitions. Exclude
  internal and implementation-only names.
- Omit `__all__` when nothing is intentionally exported; never add an empty
  block.
- Namespace packages may deliberately omit `__init__.py`. Make the choice
  explicit in packaging configuration and add facades only where a package owns
  a user-facing API.

## Functions and Documentation

- Every function must have a docstring. Keep simple docstrings brief; add
  `Args:` and `Returns:` only when they clarify behavior.
- Indent docstring section contents by 2 spaces and keep lines below 80
  characters.
- Preserve an existing function docstring unless behavior changes; update it
  when behavior changes.
- Reference code with single backticks, never double backticks.
- Write literal string choices with plain double quotes, such as "strict" or
  "permissive"; do not wrap quoted values in backticks.
- A public non-dataclass class must end its docstring with a concise
  doctest-style `Example Usage:` using `>>>` and `...` and showing the primary
  construction path followed by at least one representative public operation.
  Assign the instance to a descriptive variable; construction alone is not a
  useful usage example. Keep `Example Usage:` as the final section, after
  attributes or other explanation. These are documentation snippets, not
  executable doctests; do not add doctest directives. Dataclasses are exempt
  because their fields and attributes are normally the documentation surface.
- When construction writes files, show a clear placeholder such as
  `path/to/output`; do not add temporary-directory scaffolding solely for the
  example.
- A standalone public plotting function and each primary public plotting method
  must include a short doctest-style `Example Usage:`. Thin convenience methods
  forwarding to an already documented plotting API are exempt.

Example—combine the exact docstring conventions:

```python
def load_records(
    path: Path,
    *,
    mode: str = "strict",
) -> list[Record]:
    """Load records from `path`.

    Args:
      path: File containing serialized records.
      mode: Validation mode ("strict" or "permissive").

    Returns:
      Parsed records.
    """
```

The function body uses 4-space indentation. Contents under `Args:` and
`Returns:` use 2 spaces. Code uses single backticks, while literal choices use
plain quotes without backticks.

Example—end a public non-dataclass class docstring with representative usage:

```python
class LabelFormatter:
    """Prefix labels consistently.

    Attributes:
      prefix: Text prepended to every label.

    Example Usage:
      >>> formatter = LabelFormatter(
      ...     prefix="sample",
      ... )
      >>> formatter.format_label("001")
      'sample-001'
    """

    def __init__(self, *, prefix: str) -> None:
        """Initialize the formatter.

        Args:
          prefix: Text prepended to every label.
        """
        self.prefix = prefix

    def format_label(self, label: str) -> str:
        """Return `label` with the configured prefix."""
        return f"{self.prefix}-{label}"
```

## Typing and Signatures

- Fully annotate production functions and reusable test helpers, including
  return types. Standard pytest fixture parameters and small test-local fakes
  may omit obvious annotations when they add only noise.
- Fix the underlying type or design problem. Do not use misleading casts, fake
  annotations, broad `Any`, awkward wrappers, or type-checker workarounds.
- When a correct type requires bulky declarations or harmful abstraction, use
  the narrowest `# type: ignore[code]`. Add a reason when the upstream
  limitation or safety argument is not evident.
- `# type: ignore[import]` is acceptable for an external package without usable
  stubs. Keep it narrow; the standard missing-stub case needs no extra comment.
- Never use mutable default arguments. Use `None` as a sentinel and construct
  the value inside the function.
- Use keyword-only parameters when several values are plausibly interchangeable
  or swapping them silently changes meaning. Prefer `kw_only=True` for
  configuration dataclasses with several same-type fields. Do not force it for
  two clearly distinct arguments.
- Annotate inputs with safe abstract interfaces from `collections.abc`, such as
  `Sequence`, `Mapping`, and `Iterable`; annotate returns concretely.
- Discriminate polymorphic inputs with `isinstance`, not `type(x) is`. End an
  exhaustive `if`/`elif` chain with an `else` raising `TypeError`, and confirm
  type before accessing type-specific attributes.
- Put annotation-only imports under `if TYPE_CHECKING:` when they would create a
  circular import, and enable postponed annotations with
  `from __future__ import annotations`.

Example—fix the source type before suppressing a diagnostic:

```python
# Avoid: erase a typing problem without establishing safety.
table = typing.cast(pd.DataFrame, load_table(path))

# Prefer: correct `load_table`'s return annotation when it is under our control.
table = load_table(path)

# Acceptable for a verified upstream-stub limitation.
table = load_table(path)  # type: ignore[assignment]  # Stub is too broad.
```

## Dataclasses

- Do not introduce a dataclass by default. Use direct arguments when values do
  not need to travel together.
- Use a dataclass when values form a real domain concept, pass through several
  functions/layers, are constructed or consumed throughout the repository, or
  make a large configuration clearer than a long argument list.
- If a caller creates an object only to unpack it into one call, skip the
  dataclass. Do not create single-use configuration dataclasses.
- Configuration dataclasses must use `@dataclasses.dataclass(frozen=True)`.
  Create variants with `dataclasses.replace`; do not mutate them.

Example—bundle values only when the object travels as a unit:

```python
# Avoid: construct an object only to unpack it into one call.
@dataclasses.dataclass(frozen=True)
class ExportConfig:
    delimiter: str
    include_index: bool


def export_table(table: pd.DataFrame, config: ExportConfig) -> None:
    """Export `table` using `config`."""
    table.to_csv(
        sep=config.delimiter,
        index=config.include_index,
    )


# Prefer for one direct call.
def export_table(
    table: pd.DataFrame,
    *,
    delimiter: str,
    include_index: bool,
) -> None:
    """Export `table` with the requested formatting."""
    table.to_csv(sep=delimiter, index=include_index)
```

Use a frozen configuration object when several functions consume the same
coherent values; do not infer that every multi-argument function needs one.

## Defensive Code and Exceptions

- Validate realistic failure modes only. Do not obscure normal scientific code
  with guards, abstractions, or fallbacks for impossible states.
- Raise specific exceptions with actionable messages. Include the offending
  value/path and what the caller should change.
- Catch specific exception classes, never bare `except:`. Log enough context to
  locate failure.
- Preserve causes with `raise NewError(...) from error`. Do not swallow
  tracebacks or collapse distinct failures into an opaque `except Exception`.

Example—translate only the failure that can be made more actionable:

```python
try:
    records = load_records(path)
except FileNotFoundError as error:
    raise FileNotFoundError(
        f"Record file not found: {path}. Pass an existing path."
    ) from error
```

## Logging and Output

- Use `logging` for diagnostics, progress, and status. Define one module logger
  with `logging.getLogger(__name__)`; follow the local `logger`/`LOGGER`
  convention.
- Configure handlers once at the entry point, not throughout helpers.
- Reserve `print` for the actual stdout result that a user reads or pipes.
- Defer logging interpolation by passing values as arguments, for example
  `logger.info("Loaded %d cells", n_cells)`. Do not use f-strings, `%`, or
  `.format` to pre-format logging messages.
- Never log credentials, secrets, tokens, or personal data.

Example—keep diagnostics out of stdout and defer interpolation:

```python
# Avoid
print(f"Loaded {len(records)} records from {path}")

# Prefer
logger.info("Loaded %d records from %s", len(records), path)
```

## Command-Line Entry Points

- Every runnable Python module must define a thin `main() -> None` guarded by
  `if __name__ == "__main__": main()`.
- Let `main` perform cross-cutting setup once, parse, dispatch, and optionally
  handle top-level failure. Put domain work in named functions.
- Isolate parsing in `_parse_arguments() -> argparse.Namespace` for a
  single-purpose script or `build_parser(...) -> argparse.ArgumentParser` for
  subcommands. Do not construct parsers amid domain work.
- Pass handlers into a parser factory rather than importing them there. Dispatch
  with `parser.set_defaults(func=...)` and `args.func(args)`.
- Keep script orchestration in private helpers accepting an
  `argparse.Namespace` or explicit values and returning `None`. Only `main` and
  a genuinely shared `build_parser` are public.
- Centralize controlled failure in `main` only for concise user errors, cleanup,
  or structured logging. Otherwise let specific exceptions retain their
  traceback and non-zero exit. Helpers raise; they never call `sys.exit`.

Example—keep parsing and execution separate:

```python
def _parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Validate a record file.")
    parser.add_argument("path", type=Path)
    return parser.parse_args()


def _validate_path(path: Path) -> None:
    """Validate records stored at `path`."""
    validate_records(load_records(path))


def main() -> None:
    """Validate the requested record file."""
    args = _parse_arguments()
    _validate_path(args.path)


if __name__ == "__main__":
    main()
```

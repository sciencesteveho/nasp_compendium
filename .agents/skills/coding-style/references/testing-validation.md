# Testing and Validation

## Test Design

- Cover meaningful behavior and main functionality, including realistic edge
  cases.
- Test through the public interface: assert outputs, side effects, and raised
  errors, not private structure or internal state.
- Avoid brittle tests freezing exact filenames, directory layouts, private
  helpers, or incidental formatting unless they are documented contracts.
- Never write vacuous assertions. Assertions must read like specifications and
  fail when implementation is materially broken; avoid defensive `isinstance`
  or `hasattr` checks of framework behavior.
- Name tests for observable behavior. Cover one behavior per test; if its
  description needs "and", split it.
- Arrange, act, and assert in order with blank lines between. A single-statement
  test may remain compact.
- Give each test a one-line docstring stating observable behavior. A complex
  test may add a short Setup/Act/Assert explanation.
- Keep fixtures minimal. Define a helper used by one test beside it; extract it
  to module scope only when three or more tests share it.
- Use real components and mock only external boundaries such as network APIs,
  cloud services, schedulers, or data stores.

Example—assert the promised property, not mere existence:

```python
# Avoid
def test_normalize() -> None:
    """Normalization returns a value."""
    result = normalize(values)
    assert result is not None


# Prefer
def test_normalize_rows_sum_to_one() -> None:
    """Normalization scales each non-empty row to unit total."""
    values = np.array([[1.0, 3.0], [2.0, 2.0]])

    result = normalize(values)

    assert np.allclose(result.sum(axis=1), 1.0)
```

## Scientific and Data Tests

- Test known-signal and null behavior when an analysis claims to detect signal.
- Cover missing, non-finite, constant, insufficient, and non-estimable inputs
  when the implementation handles those states.
- Test deterministic behavior for randomized methods.
- Add replication-invariance or dependency-aware tests when correlated
  observations could otherwise inflate evidence.
- Exercise supported sparse, dense, lazy, or chunked representations with small
  synthetic data when representation affects correctness.
- Add a bounded-memory regression check where an operation could accidentally
  materialize a large dataset.

## Validation Ladder

Run the narrowest checks establishing correctness, then broaden for shared code
or configuration:

1. `ruff format --check <changed paths>` and `ruff check <changed paths>`;
2. `pyright` for changed typed packages and runnable scripts;
3. focused `pytest` tests for changed behavior;
4. the full relevant suite for shared APIs, workflow orchestration, packaging,
   or tool configuration;
5. domain checks such as `bash -n`, CLI `--help`, dry-run, synthetic analysis,
   or rendered-figure inspection;
6. `git diff --check` and a final diff review.

Do not weaken a configured check just to make it pass. Fix the issue or use the
narrow documented exception allowed by the standards. If a check cannot run,
report the fact and impact; never imply it passed.

# Testing and Validation

## Contents

- Functional regression gate
- Test design
- Assertion contracts
- Scientific and data tests
- Validation ladder

## Functional Regression Gate

- Add or retain a test only when it protects a concrete user-visible, public
  API, or operational behavior. Before writing it, complete: "If this behavior
  regresses, this test fails."
- Reject a regression claim that merely says the implementation no longer
  assigns, contains, or forwards a literal; calls a particular collaborator;
  exposes the same internal field or type; or preserves framework state. Those
  describe implementation changes, not functional failures.
- Derive the expected result from an independent contract, domain invariant, or
  worked example. Do not copy production constants, branches, configuration,
  or object structure into the assertion and call that coverage.
- Require both sides of the counterfactual: an equivalent correct
  implementation must still pass, and a plausible functional defect must fail.
  If the test cannot satisfy both conditions, do not add it.
- Do not create a test merely because code changed. Trivial wiring, imports,
  declarative configuration, and behavior-preserving refactors may need static
  checks, a focused smoke check, or the existing suite rather than a new test.
- Do not invent a contract in the test name or docstring to justify the test.
  Treat an implementation detail as fixed only when an independently documented
  compatibility contract or real downstream consumer requires it.

## Test Design

- Cover meaningful behavior and main functionality, including realistic edge
  cases.
- Test through the public interface: assert outputs, side effects, and raised
  errors, not private structure or internal state.
- Avoid brittle tests freezing exact filenames, directory layouts, private
  helpers, framework object types/order, or incidental formatting unless an
  independently documented compatibility contract with a real consumer
  requires the exact detail.
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
- Use real components by default. Mock external boundaries, or an expensive
  component boundary when testing orchestration. Do not mock a private helper
  merely to inspect call choreography.

## Assertion Contracts

- Before keeping an assertion, name the user-visible, public API, or operational
  failure it detects. Delete it when no material regression would fail.
- Assert the smallest decisive property. Exhaustively recording every reachable
  field, call, type, or formatting choice is not stronger testing.
- Apply the harmless-change check: a private-helper rename, equivalent
  representation, unrelated new field, reordered independent work, or tuned
  default must not fail the test unless an independently documented API
  contract with a real consumer promises that detail.
- Use exact equality for explicit caller inputs, documented ordering/ranking,
  output schemas, serialized keys, deterministic filenames/manifests, and
  mutation, memory, restart, or concurrency contracts.
- When order is not promised, compare membership and multiplicity with `set` or
  `Counter`. Do not freeze iteration or collaborator order accidentally.
- Prefer final return values, persisted artifacts, and observable state over
  collaborator call counts, complete kwargs, or internal phase sequences.
  Assert calls only when batching, retries, forwarding, or order is itself the
  behavior.
- Do not assert fixture setup or third-party framework behavior. Construct the
  required case, call repository code, then assert its result.
- Match exception type and a stable actionable fragment. Do not freeze full
  prose, punctuation, or traceback formatting.

Example—preserve multiplicity without freezing independent call order:

```python
# Avoid: either valid execution order now breaks the test.
assert [call["command"] for call in calls] == ["validate", "render"]

# Prefer: workflow must run each requested command once.
assert Counter(call["command"] for call in calls) == Counter(
    ["validate", "render"]
)
```

Example—require public outputs without forbidding compatible additions:

```python
# Avoid: adding another valid report breaks an unrelated test.
assert len(written_files) == 9

# Prefer: every required downstream artifact exists.
required = {"validation.json", "graph.svg"}
assert required <= set(written_files)
```

Example—test repository behavior, not fixture representation:

```python
# Avoid: this checks how the YAML parser represents the prepared fixture.
assert isinstance(source["context"], dict)

# Prefer: normalization preserves values through the required file round-trip.
normalize_record(source)
write_record(source, path)
assert read_record(path)["context"] == {"tissue": "liver"}
```

Before handoff, challenge each exact list/dict/string snapshot, call count/order,
type/identity check, private-member assertion, and formatting value. Keep it
only when an independent contract or real consumer requires the exact detail;
the test name or docstring cannot establish that contract.

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

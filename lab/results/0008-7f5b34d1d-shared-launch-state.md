# Continuity event 0008 — 7f5b34d1d

## Upstream integration

- SHA: `7f5b34d1d2a28c47ce6e479576a1459a96063650`
- Subject: `Merge f-ctl-drafting-auto (d7cc382ed): Drafting Auto after Off starts with the drafter again`
- Conflicting files:
  - `strata_cli/launch/runner.py`
  - `strata_cli/launch/screens.py`

## Classification

**R3 — shared launch-state drift**

This is the first confirmed continuity event where retaining DeepSeek requires two
independent state machines from different development lines to be composed inside a
shared runtime decision.

It is **not** yet an R4 kernel/memory/tensor-contract break.

## Shared launcher state

Post-removal upstream adds `Runner.layer_back(path)` so an installed model whose draft
layer was explicitly turned off can run setup again when Drafting returns to Auto/MTP/
DFlash2.

The retained DeepSeek line already has `Runner.dsv41_engine_missing(cfg)`, which prevents
an installed DeepSeek model from being considered reusable when its dedicated
`strata-dsv41` engine path is gone and this install has no replacement package.

Both are independently valid reasons that setup must run.

The continuity predicate therefore composes them:

```python
... and not self.layer_back(path) \
    and not self.dsv41_engine_missing(read_config(path))
```

Taking only the upstream side would regress DeepSeek engine recovery. Taking only the
historical DeepSeek side would regress the new Drafting Off -> Auto recovery.

## TUI composition

The same integration changes the Drafting summary row so that an installed config with
the draft layer disabled is displayed as Off when no explicit current choice exists.

The continuity line additionally has the DeepSeek-only Speed summary. The resolved UI
keeps both:

- retained DeepSeek Speed row;
- new upstream Drafting state representation.

## Test-domain drift

Upstream added `tests/snapshot/test_drafting_round_trip.py` after DeepSeek had been
removed. Its implicit domain therefore treated every upstream `MODEL_SET` as a member
of the generic MTP/DFlash2 Drafting state machine.

The continuity matrix has one extra family: `deepseek41`. That family intentionally uses
DSpark and writes no generic `drafting` setting.

The continuity adapter makes the generic round-trip test domain explicit by excluding
`deepseek41`, while the retained DeepSeek semantics continue to be tested by
`tests/terminal/test_drafting_switch.py`.

This is not a test suppression: the two test suites assert two different model-family
contracts.

## Validation

The verified workflow checked:

- DSV41 structural + Python syntax probe;
- the shared `ensure_model` source contains both invalidators;
- `dsv41_engine_missing()` still distinguishes DeepSeek from normal engines;
- the upstream Drafting round-trip matrix for applicable model families;
- retained DeepSeek Drafting/DSpark behavior;
- retained DeepSeek launch-plan behavior.

All passed after the adapter.

## Measurement

- runtime shared-state logical updates: **1**
- UI logical updates: **1**
- test-domain updates: **1**
- kernel/memory contract changes: **0**
- classification: **R3**

Verified checkpoint published to branch `continuity` at:

`304b2d008c5a8417ae903540d270cad50f05d5ea`

This is the first event in the experiment that crosses from build/replay mechanics into a
shared runtime state-machine composition.

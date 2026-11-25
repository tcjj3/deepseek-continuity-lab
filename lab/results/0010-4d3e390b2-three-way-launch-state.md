# Continuity event 0010 — 4d3e390b2

## Upstream integration

- SHA: `4d3e390b2fc8d24c846b973f6f28485b986600ba`
- Subject: `launch: the start's safety net fetches the drafter it falls back to`
- Conflicting file: `strata_cli/launch/runner.py`

## Classification

**R3 — shared launch-state drift**

The shared installed-model reuse predicate now has three independent reasons that setup
must run instead of reusing the installed config:

1. `layer_back(path)`: Drafting was Off and must be restored;
2. `_layer_fetch`: the start's safety net selected a missing fallback drafter;
3. `dsv41_engine_missing(cfg)`: retained DeepSeek's dedicated engine is missing.

The continuity predicate retains all three.

## Validation

- DSV41 structural + Python syntax probe: PASS
- upstream `StartSafetyNet` online/offline/Off cases: PASS
- retained DSV41 missing-engine repair regression: PASS
- retained DSV41 existing-engine/no-network regression: PASS

## Measurement

- shared launcher invalidators composed: **3**
- continuity logical update at this event: **1**
- kernel/memory contract changes: **0**
- classification: **R3**

# Continuity event 0009 — 1f0ace2d1

## Upstream integration

- SHA: `1f0ace2d1a759e336972e2306f07725eb9468a05`
- Subject: `drafting: one drafter per install, never none unless Off was chosen`
- Conflicting file: `strata_cli/launch/runner.py`

## Classification

**R3 — shared setup-interface drift**

The upstream change extends the macOS setup argument allow-list with `--drafter`, so
the Mac setup receives the drafter selected by the launch.

The retained DeepSeek line already extends the same allow-list with
`--dsv41-package`, because DeepSeek uses its own engine package.

Neither capability can replace the other. The continuity interface therefore retains
both:

```python
"--set-default-data-dir", "--feed", "--drafter", "--dsv41-package"
```

## Validation

The verified workflow checked:

- DSV41 structural and Python syntax probe;
- a DeepSeek launch with an explicit `dsv41_package` still passes
  `--dsv41-package` through the Mac setup filter;
- upstream's `MacSetupFetchesThePickedDrafter` regression passes;
- the retained DeepSeek feed-to-setup regression passes.

## Measurement

- shared setup-interface logical updates: **1**
- kernel/memory contract changes: **0**
- classification: **R3**

The verified checkpoint was published to branch `continuity`.

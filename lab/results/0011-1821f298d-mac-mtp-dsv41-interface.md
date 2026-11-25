# Continuity event 0011 — 1821f298d

## Upstream integration

- SHA: `1821f298d4a1de367392a0291ff7d8197b3b0e66`
- Subject: `launch: Drafting Off on a Mac fetches no draft layer`
- Conflicting file: `strata_cli/launch/runner.py`

## Classification

**R3 — shared setup-interface drift**

Upstream extends the macOS setup allow-list with `--mtp`, so Drafting Off reaches
the Mac setup and does not fetch the MTP draft layer. The retained DeepSeek line
already requires `--dsv41-package`, while event 0009 retained upstream's
`--drafter`.

The continuity Mac setup interface therefore carries all three independent options:

```text
--drafter
--mtp
--dsv41-package
```

## Validation

- DSV41 structural + Python syntax probe: PASS
- upstream `MacOffFetchesNothing` regression: PASS
- retained DeepSeek Mac `--dsv41-package` propagation: PASS

## Measurement

- shared setup-interface logical updates: **1**
- kernel/memory contract changes: **0**
- classification: **R3**

The verified checkpoint was published to branch `continuity`.

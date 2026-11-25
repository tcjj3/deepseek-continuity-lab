# Continuity event 0012 — f5ef26889

## Upstream integration

- SHA: `f5ef26889a38367e1b659ca74585688ba4719a34`
- Subject: `Merge f-no-llama-server: the packaged app loads only through the Strata engine`
- Conflicting file: `apps/host/server/index.mjs`

## Classification

**R1 — semantic-preserving upstream cleanup**

This conflict does **not** represent a DeepSeek compatibility cost.

The removed path was the app host's legacy `llama-server` autoload/supervisor path.
Upstream's own patch notes that remembered DeepSeek models were already refused by the
old autostart policy; retained DSV41 runs through Strata's native engine/control path,
not this `llama-server` startup block.

The continuity resolution therefore follows upstream and removes the legacy startup-load
block with **no DeepSeek-specific adapter**.

## Validation

- DSV41 structural + Python syntax probe: PASS
- Node syntax checks for the changed app host: PASS
- upstream `no-llama-server.test.mjs`:
  - fake server supplied through `STRATA_LLAMA_SERVER`: PASS
  - fake server supplied through `PATH`: PASS
- observed fake llama-server starts: **0**

## Measurement

- DeepSeek adapter LOC: **0**
- DeepSeek runtime logical updates: **0**
- kernel/memory contract changes: **0**
- classification: **R1**

The verified checkpoint was published to branch `continuity`.

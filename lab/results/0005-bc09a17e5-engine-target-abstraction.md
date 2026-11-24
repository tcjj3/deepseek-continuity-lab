# Continuity event 0005 — bc09a17e5

## Upstream integration

- SHA: `bc09a17e543f2151782a296907d8b2695c5f5232`
- Subject: `Merge f-pkg-nommq f1d2467b5 into the batch 19 candidate (...)`
- Conflicting files:
  - `spark/build_engine.sh`
  - `tools/test_no_llama_download.py`

## Classification

**R2 — build-system drift**

This is the first confirmed event where upstream introduced a new build abstraction that the retained DeepSeek path had never been migrated into.

It is **not** an execution-architecture break.

## Build abstraction change

Upstream introduced:

```sh
. "$repo/packaging/engine_targets.sh"
targets=$(engine_targets "$cmake" "$build")
```

The helper selects the main Strata targets that actually exist in the configured build tree. Post-removal upstream has no reason to know about `strata-dsv41`.

The retained continuity tree still has:

- `-DSTRATA_BUILD_DSV41="$want_dsv41"`
- target `strata-dsv41`
- packaging/copy logic for the DSV41 executable.

The minimal adapter is therefore:

```sh
targets=$(engine_targets "$cmake" "$build")
[ "$want_dsv41" = ON ] && targets="$targets strata-dsv41"
```

The new upstream abstraction remains unchanged; DSV41 is appended only when the retained build asks for it.

## Test inventory

`tools/test_no_llama_download.py` also moved to the newer upstream script inventory. The continuity version keeps that new inventory and adds back the retained DSV41 packaging/build scripts.

The lab intentionally keeps upstream GitHub workflow YAMLs inert outside `.github/workflows/`, so the workflow-only entries are excluded from this source audit. That lab-control-plane difference is not counted as a Strata/DeepSeek compatibility event.

## Measured compatibility cost

- build logic: **1 LOC**
- runtime code: **0 LOC**
- test inventory: **1 logical set/list merge**
- shared execution-contract changes: **0**

Static DSV41 continuity probe passed after the adapter.

# Continuity event 0006 — 5649b9e52

## Upstream integration

- SHA: `5649b9e5249a14eb4c284634ee130427025a5ea9`
- Subject: `Merge f-mmq-default-off: build the engine without llama.cpp's MMQ kernels by default (...)`
- Position after event 0005: **36 / 551**
- Conflicting file: `spark/build_engine.sh`

## Classification

**R2 — build-system drift**

This is **not** a DeepSeek execution-architecture break.

## Upstream change

The main Strata engine changed its global `STRATA_MMQ` default from ON to OFF. Packaging scripts now name the desired value explicitly so an old CMake cache cannot preserve the previous default.

For DGX Spark, upstream intentionally keeps the old MMQ path:

```sh
-DSTRATA_MMQ=ON
```

with the upstream note that the Spark path had not been measured without MMQ and therefore remained as in 0.2.13.

## Continuity interaction

The retained DSV41 build already adds:

```sh
-DSTRATA_BUILD_DSV41="$want_dsv41"
```

at the same CMake command location. Git conflicts because both histories edit the same argument line, not because the settings are incompatible.

The DSV41 target remains a separate executable. Its target links `strata_prefill`, `strata_dsv41_kernels`, the GPU runtime and BLAS targets; it does not depend on `strata_kq` as its identity or target-selection mechanism.

## Minimal continuity adapter

Take the upstream Spark configuration first, then retain the DSV41 build switch beside it:

```sh
-DSTRATA_BUILD_DSV41="$want_dsv41" -DSTRATA_MMQ=ON
```

Measured compatibility cost:

- build logic: **1 LOC**
- runtime code: **0 LOC**
- kernel/memory contract changes: **0**

The static DSV41 continuity probe passed after the adapter.

A verified checkpoint containing events 0001–0006 is published on branch `continuity`.

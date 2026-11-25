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


## Post-audit correction discovered at event 0015

The original event-0006 result overstated the strength of its Spark verification.

Its upstream-first conflict resolution preserved the new MMQ setting but accidentally
discarded several already-verified DSV41 Spark integration lines from event 0005:

- the `dsv41_default / want_dsv41` initialization;
- appending `strata-dsv41` to the centralized build target list;
- copying the built DSV41 executable into the Spark output folder;
- the DSV41 `--version` smoke check.

The event-0006 adapter then re-added only:

`-DSTRATA_BUILD_DSV41="$want_dsv41"`

which left `want_dsv41` undefined under the script's `set -u`. The static continuity
probe did not execute this platform-specific script and therefore missed the defect.

This is a **continuity-adapter / measurement regression**, not evidence that upstream
made DSV41 incompatible. Event 0015 restores the complete Spark DSV41 invariant while
moving the upstream build to MMQ=OFF, and strengthens the probe with POSIX syntax plus
target/copy/version assertions.

Accordingly:

- the **R2 nature** of event 0006 remains valid;
- its old statement that the Spark path was fully verified is superseded by the
  event-0015 audit;
- the latent defect is excluded from upstream compatibility cost but retained in the
  experiment record.

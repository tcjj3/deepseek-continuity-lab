# Continuity event 0015 — 011247304

## Upstream integration

- SHA: `0112473047401ede9642a43bc60a458e2266912c`
- Subject: `Merge f-spark-nommq: the DGX Spark (ARM64) engine builds without llama.cpp's MMQ, in setup.py and spark/build_engine.sh, with the GB10 numbers`
- Conflicting files:
  - `packaging/ENGINE-COMPONENT.md`
  - `packaging/build_cuda_linux_aarch64.sh`
  - `spark/build_engine.sh`

## Classification

**R2 — build / packaging drift**

This is not a DSV41 arithmetic-contract migration.

Upstream changes the **main Strata** DGX Spark build from `STRATA_MMQ=ON` to
`STRATA_MMQ=OFF`, so the release uses Strata's own fused prompt kernels and no longer
ships `libstrata_kq.so` by default.

Retained DSV41's CUDA prompt implementation does not use the main engine's MMQ expert
path as its arithmetic backend. Its chunk dense-GEMM path keeps cuBLAS on CUDA; the
shared `strata_pf_gemm_f16_ld()` hook is selected under `STRATA_USE_HIP`.

The continuity task is therefore to carry the DSV41 **build/package presence** across
the Spark release-shape change, not to adapt DSV41 arithmetic.

## Continuity adapter

The verified Spark script now combines:

```text
STRATA_BUILD_DSV41=<continuity choice>
STRATA_MMQ=OFF
```

and retains the complete DSV41 Spark invariant:

- define `dsv41_default` / `want_dsv41`;
- configure `STRATA_BUILD_DSV41`;
- append `strata-dsv41` to the centralized target list;
- copy `strata-dsv41` into the output folder;
- execute its `--version` smoke check;
- retain it beside the main engine in the ARM64 package;
- retain the separate `dsv41` feed package.

The package documentation was updated to state that the default Spark package no longer
contains `libstrata_kq.so` while the continuity line still carries `strata-dsv41`.

## Latent adapter-regression audit

While preparing this event, the lab discovered that event 0006's conflict resolution
had accidentally discarded several event-0005 DSV41 Spark integration lines. The old
probe only checked the source/CMake presence and Python syntax, so this platform-script
defect remained latent.

Event 0015 repairs that history and upgrades `lab/tools/probe.sh` with a permanent
`[spark-dsv41]` section that checks:

- POSIX syntax of the two ARM64 build scripts;
- the DSV41 choice variable;
- the DSV41 CMake switch;
- the DSV41 target-list append;
- the DSV41 output copy;
- the DSV41 version smoke check.

This instrumentation repair is not counted as upstream compatibility cost.

## Validation

The verified workflow passed:

- the full continuity static/syntax probe;
- the new Spark-DVS41 invariant probe;
- the complete `tests.terminal.test_linux_aarch64` suite;
- upstream's `test_the_spark_engine_is_built_without_mmq`;
- explicit source assertions for the retained DSV41 package path;
- a source-level execution-contract check showing DSV41 CUDA keeps cuBLAS while the
  shared prefill GEMM hook is HIP-only.

Observed workflow result:

```text
[spark-dsv41] POSIX syntax and retained target/package invariants
STATIC PASS
test_the_spark_engine_is_built_without_mmq ... ok
OK
event 0015 Spark no-MMQ + retained DSV41 invariants PASS
```

## Measurement

- DSV41 execution-contract changes: **0**
- build/package continuity updates: **one composed platform integration**
- instrumentation invariant added: **1**
- classification: **R2**
- architecture break: **no**

Verified continuity checkpoint:

`9ad5773a9b4587a94809fdff3935d3e38f75a707`

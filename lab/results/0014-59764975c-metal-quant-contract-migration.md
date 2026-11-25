# Continuity event 0014 — 59764975c

## Upstream integration

- SHA: `59764975cd8c066b7e9d651b311eed08ed887b60`
- Subject: `Merge f-ggml-out-0215: x86 CUDA / HIP release builds without ggml-base / ggml-cpu, the Metal engine's CPU pool on Strata's quant layer, SYCL dead prompt-kernel files deleted, the web host's llama.cpp download route removed (own-stack steps 1 and 3)`
- Conflicting file: `metal/CMakeLists.txt`

## Classification

**R4 — compatible shared arithmetic-contract migration**

This is the first confirmed event in the experiment that changes a shared execution/arithmetic contract actually used by retained DSV41.

It is **not an architecture break**.

Upstream changes the Metal CPU expert pool from the historical ggml-cpu arithmetic backend to Strata's own quant layer by default and allows a release build with no ggml-base / ggml-cpu targets at all.

The continuity line already had both implementations behind the same caller-facing `pool_quant.hpp` interface:

- `STRATA_OWN_CPU_QUANT=OFF`: historical ggml-cpu type traits / dots;
- `STRATA_OWN_CPU_QUANT=ON`: Strata quant layer.

The retained DeepSeek Metal CPU lane uses this same abstraction, so the event changes the selected arithmetic backend without requiring DSV41 runtime source changes.

## Apple-Silicon numerical oracle

The event was tested on a real GitHub `macos-26` **arm64** runner.

The Strata quant oracle was built against the ggml-cpu NEON reference with:

```text
STRATA_BUILD_DSV41=ON
STRATA_OWN_CPU_QUANT=ON
flavour=neon
```

Then the retained DSV41 `ds4_gg_bench` CPU-lane path was tested for four i-quant types at one and four tokens.

| ggml type id | tokens | compared outputs | bit differences | worst vs double reference |
| --- | ---: | ---: | ---: | ---: |
| 16 (IQ2_XXS) | 1 | 1512 | 0 | 6.57e-09 |
| 16 (IQ2_XXS) | 4 | 6048 | 0 | 8.25e-09 |
| 18 (IQ3_XXS) | 1 | 1016 | 0 | 1.24e-08 |
| 18 (IQ3_XXS) | 4 | 4064 | 0 | 1.24e-08 |
| 21 (IQ3_S) | 1 | 904 | 0 | 1.15e-08 |
| 21 (IQ3_S) | 4 | 3616 | 0 | 1.15e-08 |
| 29 (IQ1_M) | 1 | 1784 | 0 | 5.06e-09 |
| 29 (IQ1_M) | 4 | 7136 | 0 | 9.70e-09 |

Every run returned `OK`.

The important result is not merely tolerance-level agreement: all sampled DSV41 row results were **bit-identical** to the ggml-cpu comparison path in these cases.

## New default: DSV41 without ggml

The retained Metal engine was configured as a release build with the new default:

```text
STRATA_OWN_CPU_QUANT:BOOL=ON
STRATA_BUILD_TESTS=OFF
```

CMake reported:

```text
Strata Metal: no ggml in this build (own CPU pool, tests off)
```

The generated target graph contained no `ggml-base` or `ggml-cpu` targets.

`strata_ds4` built and linked successfully. The compile command for retained
`src/dsv41/ds4_gg_cpu.cpp` contained:

```text
-DSTRATA_OWN_CPU_QUANT=1
```

The resulting executable reported:

```text
strata-dsv41 0.1.60-metal build 202dfbde6
```

and no dynamic ggml dependency was present.

## Historical fallback remains buildable

A second independent Metal build used:

```text
STRATA_OWN_CPU_QUANT:BOOL=OFF
```

That build restored `ggml-base` and `ggml-cpu`, compiled the DSV41 CPU lane without the own-quant macro, and also linked a working `strata_ds4` executable:

```text
strata-dsv41 0.1.60-metal build 202dfbde6
```

Thus the migration does not merely compile in the new configuration: both sides of the contract boundary remain buildable at this checkpoint.

## Continuity adapter

No DSV41 runtime implementation change was required.

The continuity adapter only keeps the Metal option/comment documentation truthful that the shared own-quant option also covers the retained DeepSeek CPU lane.

Measured DSV41 runtime adapter cost:

**0 LOC**

## Result

This event satisfies the lab's R4 definition because the underlying arithmetic implementation used by the retained DeepSeek CPU lane changes from ggml-cpu to Strata's own quant layer.

It does **not** satisfy the stronger architecture-break criterion:

> DSV41 remains behaviorally equivalent without changing its assumptions about the caller-facing CPU-lane contract.

In fact, the pre-existing dual implementation was sufficient to cross the migration.

Verified continuity checkpoint:

`202dfbde6aec16509c4beae2bb6844f69427fd43`

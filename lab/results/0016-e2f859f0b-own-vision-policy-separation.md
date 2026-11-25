# Continuity event 0016 — e2f859f0b

## Upstream integration

- SHA: `e2f859f0bd4fcf0fcf61093c9e83b85eaf9f93f3`
- Subject: `Merge f-0216-vision: strata-vision is Strata's own picture reader on every backend, without llama.cpp's mtmd, llama or ggml (own-stack step 6); the setting and the start-up fallback to llama.cpp's reader go; the Metal reader takes F16 inputs; no -DLLAMA_DIR in the reader builds`
- Initial conflict set: **9 files**

## Classification

**R3 — policy/control separation + R2 packaging drift**

This is **not** an R4 DeepSeek execution-contract break.

The large conflict count came from two historically adjacent but semantically separate
features:

1. the generic Qwen picture-reader fallback to llama.cpp/mtmd;
2. retained DeepSeek's independent DSV41 controls, packages and vision path.

The correct continuity result is not to preserve the old generic fallback. It is to
remove that fallback exactly as upstream does while retaining only the DSV41-specific
semantics.

## Upstream own-vision migration retained

The continuity line follows upstream in removing:

- the `picture_reader` switch;
- `STRATA_VISION_TOWER=mtmd`;
- the llama.cpp/mtmd generic Qwen picture-reader fallback;
- `-DLLAMA_DIR` from the HIP vision build;
- the old generic vision fallback policy/tests.

The resulting Qwen picture reader is the Strata-owned path only.

## DeepSeek semantics retained

The continuity adapter keeps these independent DSV41 features:

- the `deepseek_speedups` compatibility switch;
- the seven-entry `DS4_*` environment contract;
- the App's ability to edit/round-trip retained DS4 environment names;
- DSV41 HIP build/package presence;
- the separate DSV41 Metal vision implementation/license notice;
- DeepSeek's own pack/tower/Read-pictures behavior.

Generated App policy and policy vectors are regenerated from the patched Python
source-of-truth rather than hand-merged.

## Validation

The verified workflow passed all of the following:

- full continuity structural/Python/Spark probe;
- HIP packaging Bash syntax;
- retained `-DSTRATA_BUILD_DSV41=ON`;
- retained `strata-dsv41` packaging;
- absence of legacy `-DLLAMA_DIR`;
- absence of `picture_reader` from the Python switch source;
- presence of `deepseek_speedups`;
- generated-policy `--check`;
- **25 Python policy/speed-switch tests**;
- **24 App policy/speed-switch tests**;
- DeepSeek native-argument tests;
- DeepSeek picture/tower/load tests;
- Qwen picture-load tests from the correct `apps/host` package root.

The App/host tests explicitly confirmed:

- a DeepSeek model gets its own speed switch only;
- all seven DeepSeek compatibility entries round-trip correctly;
- the picture-reader row is gone;
- a DeepSeek pack carrying its picture tower remains picture-capable;
- `--vision off/on` continues to work for retained DSV41;
- a DeepSeek load with Read pictures enabled does **not** ask for a separate reader.

## Permanent probe improvement

Because earlier history showed that platform-specific adapters can be silently lost by a
later replay, this event adds a permanent `[hip-dsv41]` probe that checks:

- `packaging/build_hip_linux.sh` parses as Bash;
- the HIP build still enables DSV41;
- the HIP package still contains `strata-dsv41`;
- the removed legacy `LLAMA_DIR` dependency does not return.

## Measurement

- generic retired feature retained: **0**
- DSV41 policy/control logical separation: **1 composed adapter**
- DSV41 execution-contract changes: **0**
- DSV41 vision implementation changes: **0**
- classification: **R3 + R2**
- architecture break: **no**

Verified continuity checkpoint:

`fd94ce07a7adf90b49eced2c7e3c55afc93897ff`

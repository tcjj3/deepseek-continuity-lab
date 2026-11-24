# Methodology

## 1. Scope

This lab measures whether the retained historical DeepSeek DSV41 implementation can remain compatible with later Strata evolution when the explicit removal series is omitted.

It does not treat technical survivability as proof of maintainer intent, interpersonal motive, or project-governance history.

## 2. Baseline

Upstream baseline:

`e4309aaf325176f90a844ad7833b58552b6ef5e1`

This is the direct parent of:

`5d5029be4e979341639560f9a587b24188d5cbc0` — `DeepSeek out (1/7)`.

The baseline is an ancestor of current Strata `main`, so the experiment can follow the real integration history forward.

## 3. Why first-parent first

The first pass follows `upstream/main --first-parent`.

That answers:

> At what integration point did the retained DeepSeek line first stop surviving the mainline evolution?

If the first failure is a merge commit, that merge is only the integration boundary. The merged side branch should then be inspected or bisected to find the exact internal change.

This avoids double-applying commits from a Git DAG while still preserving a precise path to later drill-down.

## 4. Failure taxonomy

Every stop should be classified before calling it an architecture break.

- **R0 — explicit-removal-policy**  
  A commit exists to disable, reject, hide, or delete DeepSeek.

- **R1 — mechanical-replay**  
  Directory moves, renames, packaging, file layout, generated files, or other changes that do not alter the execution contract.

- **R2 — build-system-drift**  
  CMake target names, build flags, toolchain wiring, or source registration changed.

- **R3 — shared-api-drift**  
  A shared C++/Python API consumed by DSV41 changed.

- **R4 — kernel-or-memory-contract-drift**  
  Tensor layout, planner semantics, memory ownership, scheduler lifecycle, kernel ABI, residency policy, or similar runtime contracts changed.

- **R5 — runtime-semantic-regression**  
  The code compiles and starts but produces wrong output, crashes in inference, or violates a correctness invariant.

- **R6 — performance-regression**  
  Correctness survives but performance changes materially enough to make the retained implementation non-viable.

## 5. Architecture-break criterion

A Git conflict is not enough.

A stronger architecture-break criterion is:

> Retained DSV41 cannot remain behaviorally equivalent without changing one or more assumptions about a shared execution contract.

Mechanical relocation does not qualify by itself.

## 6. Compatibility adapters

Every DeepSeek-specific compatibility fix should be isolated in a separate commit:

`continuity-adapter: <description>`

For each adapter, record:

- triggering upstream SHA;
- classification R1–R6;
- files touched;
- added/deleted LOC;
- shared subsystems affected;
- whether behavior changed;
- whether a real model was needed to validate the fix.

Useful derived metrics include:

- cumulative adapter LOC;
- adapter LOC per 100 upstream integration commits;
- number of touched shared subsystems;
- mechanical vs semantic adapter ratio;
- commits between architecture breaks.

## 7. Probe levels

### Level S — structural

No GPU required. Confirms that the retained DSV41 source, headers, controller path, documentation, and build target declaration still exist.

### Level B — build

Configures the relevant CUDA/HIP backend and builds `strata-dsv41`.

### Level T — tests

Runs selected DeepSeek controller/runtime tests when the environment supports them.

### Level R — real model

Runs a fixed known-good DSV41 model invocation and checks startup/inference behavior.

### Level P — performance

Records latency, throughput, VRAM/RAM residency and other performance measurements under a fixed environment.

## 8. Three-line comparison after official DeepSeek returns

When Strata eventually introduces a new official DeepSeek implementation, compare:

1. historical DSV41 retained by this lab;
2. Strata mainline architecture that evolved without DSV41;
3. the future official DeepSeek implementation.

The important comparison is abstraction-level, not just text diff: loader, tensor format, planner, memory ownership, attention path, MoE routing, kernel interface, scheduling and runtime lifecycle.

# DeepSeek Continuity Lab

This directory contains the control plane for an independent software-evolution experiment.

The source tree at the repository baseline is an exact working-tree snapshot of Strata commit:

`e4309aaf325176f90a844ad7833b58552b6ef5e1`

That commit is the direct parent of `DeepSeek out (1/7)`.

## Research question

If the historical DSV41 implementation had *not* been removed, how long could it have followed later Strata evolution, and at which upstream change would continued compatibility start requiring substantive architectural adaptation?

The experiment deliberately does **not** infer the historical reason for removing DeepSeek. It measures a different, testable question: technical continuity and maintenance cost.

## Repository branches

- `baseline-pre-removal`: pinned snapshot immediately after baseline import.
- `main`: continuity experiment line. Later upstream integration commits may be replayed here while retaining DSV41.

## Upstream relationship

Upstream project: https://github.com/Niko1221/Strata

This is not an official Strata repository or release. The upstream MIT license and copyright notice are preserved.

## Replay rules

1. Fetch the real Strata upstream history.
2. Follow the upstream `main` **first-parent integration timeline** from the baseline.
3. Record and intentionally skip commits whose subject matches the explicit `DeepSeek out (N/7)` removal series.
4. Replay every other integration commit.
5. Filter upstream GitHub workflow changes from the experimental source replay; they are not part of the model/runtime architecture and GitHub token policy makes them a noisy variable.
6. Run the continuity probe immediately after every replayed integration commit.
7. Stop at the first patch conflict or probe failure and classify it before making an adapter.

A first-parent failure at a merge commit identifies the integration point. If needed, the merged branch can then be drilled down separately to find the exact internal commit.

## Quick start

```bash
git clone https://github.com/tcjj3/deepseek-continuity-lab.git
cd deepseek-continuity-lab

python3 lab/tools/replay_upstream.py --dry-run --max 30
python3 lab/tools/replay_upstream.py --max 1
```

The default probe is structural and requires no GPU:

```bash
bash lab/tools/probe.sh
```

For a CUDA build probe:

```bash
CONTINUITY_PROBE_MODE=build \
CONTINUITY_BACKEND=cuda \
bash lab/tools/probe.sh
```

For HIP:

```bash
CONTINUITY_PROBE_MODE=build \
CONTINUITY_BACKEND=hip \
bash lab/tools/probe.sh
```

A known-good real-model invocation can be layered on top without hard-coding a version-specific CLI into the lab:

```bash
CONTINUITY_PROBE_MODE=build \
CONTINUITY_BACKEND=cuda \
CONTINUITY_RUNTIME_CMD='<known-good DSV41 command>' \
bash lab/tools/probe.sh
```

## Adapter rule

Any fix whose purpose is specifically to keep retained DeepSeek working after an upstream change should be committed separately with a subject beginning:

```text
continuity-adapter:
```

Do not mix those adapters into replay commits. That separation is what lets the repository become a measurable maintenance-cost history.

# Continuity event 0007 — 38f63bc59

## Upstream integration

- SHA: `38f63bc59123182b2933809bd623697bb81dc81e`
- Subject: `Version 0.2.14 / engine 0.1.60: Terminal and app 0.2.14, Control and the engine packages 0.1.60`
- Conflicting files:
  - `AGENTS.md`
  - `packaging/UPDATES.md`

## Classification

**R0 — release-policy divergence**

This is not a technical compatibility break.

The upstream version bump deliberately changes the official release semantics after DeepSeek removal:

- current public model-family text no longer lists DeepSeek;
- current Strata/Control/engine versions move to 0.2.14 / 0.1.60;
- DSV41 package names explicitly remain at 0.1.59;
- release instructions change from building a current `--dsv41 RELEASE/dsv41` feed member to carrying the last DSV41 feed forward from the earlier release (or carrying none).

## Continuity rule

The lab is not an alternative official Strata distribution. Therefore it follows upstream's official 0.2.14 release/version metadata instead of rewriting those documents to claim current official DeepSeek support.

Technical continuity is measured separately by the retained source tree, build target, launcher behavior and probes.

At this checkpoint the retained continuity tree still contains the direct DSV41 feed machinery in `packaging/feed_tool.py`, including:

- `--dsv41`;
- `dsv41_dir`;
- construction of the `dsv41` feed member;
- the `strata-dsv41` package prefix.

The official release policy and the experimental technical path are therefore intentionally kept as two different facts.

## Resolution

Take upstream 0.2.14 release metadata for both conflict files.

Measured compatibility cost:

- runtime adapter LOC: **0**
- build adapter LOC: **0**
- release-policy divergence: **explicitly recorded**
- DSV41 technical probe: **PASS**

The resolved checkpoint was pushed to branch `continuity`.

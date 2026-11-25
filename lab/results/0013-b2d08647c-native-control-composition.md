# Continuity event 0013 — b2d08647c

## Upstream integration

- SHA: `b2d08647c5cf769798c9644328d5bde283f71f22`
- Subject: `app: Drafting Off fetches no draft layer; the offline note only when no drafter runs`
- Conflicting file: `apps/host/server/native-control.mjs`

## Classification

**R3 — app native-control config drift**

This event is the deepest control-plane composition observed so far. The App's native
configuration builder gained a new generic Drafting-Off / MTP-offline state while the
continuity line still carries DeepSeek-specific native-control semantics.

Three independent pieces had to coexist:

1. upstream's `MTP_OFFLINE_NOTE` and `--mtp off` propagation;
2. the retained DeepSeek vision default exception;
3. the retained DeepSeek `dsNote` emitted by `buildConfig()`.

## Shared helper convergence

Upstream also added a local `withoutVisionFlag()` helper to `native-control.mjs`.

The continuity line had already extracted the byte-for-byte equivalent helper to
`native-ds-args.mjs` so the DeepSeek argument path could share it.

The continuity resolution therefore keeps the extracted shared helper and removes the
new duplicate local definition. This is a semantic convergence of two development
paths, not a DeepSeek-specific fork.

## DeepSeek vision rule

The generic packaged-app install path defaults an omitted vision choice to:

```js
{ vision: 'no' }
```

The retained DeepSeek path must remain exempt because its picture capability belongs to
the DSV41 pack/engine path rather than the generic Qwen vision-install path.

The continuity expression therefore remains equivalent to:

```js
packaged && args.vision === undefined && args.family !== 'deepseek41'
```

## DeepSeek load note

The upstream offline-note cleanup is retained while the `buildConfig()` destructure
continues to carry `dsNote` and append it to the instance log.

## Validation

The verified workflow ran:

- DSV41 structural + Python syntax probe;
- Node syntax check for `native-control.mjs`;
- upstream `fix0215-drafting-off.test.mjs`;
- upstream App Drafting tests with the locked `apps/host/package-lock.json` environment;
- retained `native-ds-args.test.mjs`;
- retained `native-ds-parallel.test.mjs`;
- the MCP/Terminal installation-interface Python regression suite;
- explicit source assertions for the retained DeepSeek vision and load-note semantics.

All passed.

## Measurement

- App native-control logical updates: **2**
- shared-helper deduplication: **1**
- kernel/memory contract changes: **0**
- classification: **R3**

Verified checkpoint:

`af76d89f2fae7240af10fe50eb75efd30ea0de71`

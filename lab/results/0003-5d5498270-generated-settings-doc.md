# Continuity event 0003 — 5d5498270

## Upstream integration

- SHA: `5d54982709879000c2e2b783c729850ce1949824`
- Subject: `docs: settings page regenerated from the register`
- Distance after adapter 0002: **28 successful first-parent integration commits**
- Conflicting file: `docs/SETTINGS.md`

## Classification

**R1 — generated-artifact drift**

This is **not** an architecture break and carries **0 manual runtime compatibility LOC**.

The file declares itself generated from:

`data/settings-register.json` via `python tools/settings_register.py --docs`.

At this point the continuity branch intentionally retains DeepSeek-related settings that post-removal upstream no longer has. Therefore a regenerated upstream document and a regenerated continuity document are expected to differ.

The first visible conflict is the generated table count:

- continuity: `Switches you can turn on (280)`
- post-removal upstream: `Switches you can turn on (275)`

## Correct resolution rule

Do not hand-merge generated documentation and do not count its generated diff as adapter LOC.

1. Replay the upstream regeneration commit using the upstream generated file.
2. Re-run `python tools/settings_register.py --docs` against the continuity branch's merged register.
3. Commit the regenerated result as a generated continuity adapter.

Measured compatibility cost:

- manual runtime LOC: **0**
- manual source/test LOC: **0**
- generated artifact refresh: **1 file**

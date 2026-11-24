# Continuity event 0001 — 291b91025

## Upstream integration

- SHA: `291b91025e896f5b579a6c1df9de88df8595c0a8`
- Subject: `Merge f-agent-turn b92075d92 into f-p4-int`
- First failure position in the first-parent trial: **28 / 664**
- Conflicting file: `serve/server.py`

## Classification

**R1 — mechanical replay / adjacent capability insertion**

This is **not** an architecture break.

The retained pre-removal server has the DeepSeek parallel capability parser:

```python
self.multi = next((int(x[6:]) for x in f[2:] if x.startswith("multi=") and x[6:].isdigit()), 0)
```

The later upstream integration adds the new batch thinking-hold capability parser at exactly the same insertion point:

```python
self.can_hold_batch = "holdb" in f[2:]
```

Git therefore reports a one-hunk conflict even though the two READY capabilities are orthogonal.

## Evidence

The conflict stages show:

```diff
self.can_hold = "hold" in f[2:]
<<<<<<< HEAD
self.multi = ...
=======
self.can_hold_batch = "holdb" in f[2:]
>>>>>>> 291b91025
```

The same upstream integration later gates the new hold behavior with a check equivalent to:

```python
... and not getattr(self.engine, "multi", 0)
```

so the new batch-hold path explicitly remains separate from the retained DeepSeek multi-engine path.

## Minimal continuity adapter

Keep both capability parsers:

```python
self.can_hold = "hold" in f[2:]
self.can_hold_batch = "holdb" in f[2:]
self.multi = next((int(x[6:]) for x in f[2:] if x.startswith("multi=") and x[6:].isdigit()), 0)
```

Measured DeepSeek-specific compatibility cost: **1 retained line / one conflict hunk**.

No shared execution-contract assumption needs to change, so this event does not satisfy the lab's architecture-break criterion.

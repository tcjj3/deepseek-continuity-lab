# Continuity event 0002 — 4cf79d5dc

## Upstream integration

- SHA: `4cf79d5dc7ef...`
- Subject: `Merge f-agent-turn 018f0d659 into f-p4-int`
- Position after adapter 0001: the **immediately next** first-parent integration commit
- Conflicting file: `tests/split/test_split_gen_keys.py`

## Classification

**R1 — mechanical replay / retained test classification**

This is **not** an architecture break and does not represent a runtime failure.

The continuity side still classifies DeepSeek-only request keys:

```python
OTHER_ENGINES = {"marks", "tail", "shared", "prefill", "rid"}
```

The post-removal upstream side no longer contains those DeepSeek keys and adds the new thinking-budget key:

```python
OTHER_ENGINES = {"prefill", "hold"}
```

Because the retained server still contains the DeepSeek restore-point and multi-request paths, the correct continuity classification is the union:

```python
OTHER_ENGINES = {"marks", "tail", "shared", "prefill", "rid", "hold"}
```

## Interpretation

This conflict is direct evidence of a *post-removal assumption* entering the test suite: upstream can legitimately stop classifying DeepSeek-only keys because upstream removed the feature, while the continuity line cannot.

No DeepSeek execution contract changes here. The adapter only teaches the newer test about the still-retained engine-specific keys.

Measured compatibility cost:

- runtime code: **0 LOC**
- test classification: **1 logical set update** plus comment reconciliation

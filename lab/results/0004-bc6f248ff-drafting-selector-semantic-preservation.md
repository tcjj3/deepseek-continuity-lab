# Continuity event 0004 — bc6f248ff

## Upstream integration

- SHA: `bc6f248ffaf51fd387532209f59a77d6783e6b1e`
- Subject: `Merge f-draft-vocab 925d6fb05 into f-p4-int (... renamed Flash-Next file starts the drafter)`
- Conflicting file: `strata_control/drafting.py`

## Classification

**R1 — semantic-preserving merge**

Measured DeepSeek-specific adapter cost: **0 LOC**.

This conflict touched a shared model-selection path, so it was investigated as a possible R3 event. It did **not** change DeepSeek behavior.

## Why it conflicts

Before this upstream change, an unsupported `model_name` immediately took the non-DFlash2 path. The newer selector first tries to identify a renamed Flash-Next GGUF from the model file itself:

```python
fit = file_fit(args, data_dir) if family is None and not _EXCLUDED_NAME.search(str(name or "")) else ""
if fit == "fits":
    name = known_name_of_file(args) or FILE_FITS_AS
```

The retained pre-removal comment explicitly listed DeepSeek among unsupported models, while post-removal upstream no longer names it.

## DeepSeek path

The retained DeepSeek run config is built by `dsv41_config_for()` with:

- `model_name = "deepseek-v4.1-flash"`
- engine arguments beginning with `--pack <pack>`
- no `--native <GGUF>` argument.

The new `file_fit()` inspects only the path supplied through `--native`. Therefore, for a retained DeepSeek config:

```text
supported_model("deepseek-v4.1-flash") -> false
file_fit(["--pack", ...])              -> "unknown"
supported_model(...)                   -> still false
```

and execution continues through the same unsupported-model early return as before.

## Behavioral verification

The disposable continuity workflow resolved the conflict by taking the newer generic selector block, then executed a DeepSeek-shaped config through the merged `drafting.apply()`.

Assertions passed:

- `file_fit(["--pack", ...]) == "unknown"`
- selected drafter remains `mtp`
- the DeepSeek engine argument list is unchanged.

No compatibility adapter was required.

## Interpretation

This is an important negative result: a shared subsystem evolved substantially, but retained DeepSeek remained naturally outside the new Flash-Next file-identification mechanism. Git reported a conflict; the execution contract did not diverge.

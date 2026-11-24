# Results

Runtime event logs are intentionally written under `.git/continuity-lab/` so the probe itself does not contaminate the source tree being measured.

When a failure is classified and worth preserving, copy the relevant evidence here in a small, human-reviewed record containing:

- upstream SHA;
- replay commit SHA;
- failure class R0–R6;
- conflicting files or failing probe;
- adapter commit, if any;
- build/runtime environment;
- observed behavior.

Do not automatically commit raw model files, secrets, local paths, or large build artifacts.

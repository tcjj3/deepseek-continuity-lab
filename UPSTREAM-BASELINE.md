# Upstream baseline

This repository is an independent compatibility/evolution experiment derived
from the public Strata repository.

- Upstream: https://github.com/Niko1221/Strata
- Exact baseline: `e4309aaf325176f90a844ad7833b58552b6ef5e1`
- Selection rule: exact working-tree state immediately before the
  `DeepSeek out` removal series
- Import model: working-tree snapshot, not rewritten upstream Git history
- Purpose: retain the historical DeepSeek implementation while replaying later
  non-removal upstream changes and measuring compatibility/maintenance cost

Upstream workflow YAML files are preserved as inert reference material under
`lab/upstream-workflows-snapshot/` rather than `.github/workflows/`, because
GitHub does not allow this Actions token to introduce upstream workflow history.

The upstream MIT license and copyright notice are preserved.

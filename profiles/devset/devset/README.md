# `devset`

devset itself, pinned through mise, so every machine and every CI job applies
the profiles with one release, which the weekly bump moves as it moves every
other pin. `check-devset` runs `devset status --exit-code`, so a file that has
drifted from its profile, or an update left unfinished, fails the checks, in CI
as a job of its own.

<!-- facts: written by scripts/catalog.py -->
<!-- /facts -->

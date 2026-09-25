# `github-nightly`

Each night, `nightly` runs every `nightly-*` recipe, each a job of its own, with
the tools mise locks, from one cache its plan fills: the checks too slow for
every change, such as [`cargo-hack`](../cargo-hack/README.md) over each feature,
or links to the web with [`lychee`](../lychee/README.md). A night with no commit
since the last green one is skipped, as [`automation`](../automation/README.md)
sets; a run by hand always runs.

With [`github-watch`](../github-watch/README.md), a failing or stalled night
gets an issue. The jobs that build run on `ubuntu-latest`, or on the runner the
repository variable `CI_RUNNER` names.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                            | Part  | Policy | Notes |
| ------------------------------- | ----- | ------ | ----- |
| `.github/workflows/nightly.yml` | whole | owned  |       |

## Requires

- [`just`](../just/README.md)
- [`github-watch`](../github-watch/README.md)

<!-- /facts -->

# `github-nightly`

Each night, `nightly` runs every `nightly-*` recipe, each a job of its own, with
the tools mise locks, from one cache its plan fills: the checks too slow for
every change, such as [`cargo-hack`](../../cargo/cargo-hack/README.md) over each
feature, or links to the web with [`lychee`](../../docs/lychee/README.md). A
night with no commit since the last green one is skipped, as
[`github-automation`](../../github/github-automation/README.md) sets; a run by
hand always runs.

A failing or stalled night gets an issue from
[`github-watch`](../../github/github-watch/README.md). The jobs that build run
on `ubuntu-latest`, or on the runner the repository variable `CI_RUNNER` names.

<!-- facts: written by devset-collection -->

## Owns

| File                            | Part  | Policy | Notes |
| ------------------------------- | ----- | ------ | ----- |
| `.github/workflows/nightly.yml` | whole | owned  |       |

## Requires

- [`github-automation`](../github-automation/README.md)
- [`github-watch`](../github-watch/README.md)
- [`just`](../../tooling/just/README.md)

<!-- /facts -->

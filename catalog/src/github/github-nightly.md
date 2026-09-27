# `github-nightly`

A nightly run of every `nightly-*` recipe, each a job of its own, watched.

```sh
devset add atxp/github-nightly --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `github` · In [`rust`](../bundles/rust.md): with `nightly`

Each night, `nightly` runs every `nightly-*` recipe, each a job of its own, with
the tools mise locks, from one cache its plan fills: the checks too slow for
every change, such as [`cargo-hack`](../cargo/cargo-hack.md) over each feature,
or links to the web with [`lychee`](../docs/lychee.md). A night with no commit
since the last green one is skipped, as
[`github-automation`](github-automation.md) sets; a run by hand always runs.

A failing or stalled night gets an issue from [`github-watch`](github-watch.md).
The jobs that build run on `ubuntu-latest`, or on the runner the repository
variable `CI_RUNNER` names.

## Owns

| File                            | Part  | Policy | Notes |
| ------------------------------- | ----- | ------ | ----- |
| `.github/workflows/nightly.yml` | whole | owned  |       |

## Requires

- [`github-automation`](github-automation.md)
- [`github-watch`](github-watch.md)
- [`just`](../tooling/just.md)

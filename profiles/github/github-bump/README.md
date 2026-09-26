# `github-bump`

Once a week, `bump` moves everything the repository pins. `just bump` runs every
`bump-*` recipe, each writing what it moved, held back or could not check to a
report; `just fix` settles the files they changed; `just check` is the gate. The
result is one signed commit on `bot/bump`, rebuilt from the default branch each
week, titled `chore(bump): move pinned tools and dependencies`, which
[`git-changelog`](../../git/git-changelog/README.md) lists under Pins. It goes as far as
`bump.mode` in `.github/automation.json`, which
[`github-automation`](../../github/github-automation/README.md) sets:

| `bump.mode`    | Does                                                                        |
| -------------- | --------------------------------------------------------------------------- |
| `branch`       | the commit, and an issue linking to open the pull request                   |
| `pr` (default) | also the pull request, kept up to date; an issue only while the gate is red |
| `merge`        | also merges it once green; a red gate never merges                          |

A pull request opened with a run's own token runs no workflows, so the
repository's checks never report on it. With a GitHub App, whose id is the
variable `BUMP_APP_ID` and whose key the secret `BUMP_APP_KEY`, the pull request
runs them, `merge` waits for them through GitHub's auto-merge, and the commit
may change workflows. Without one, `merge` merges on this run's own gate, and
changes to workflows are left out and named.

A bump that cannot check something fails the run, and
[`github-watch`](../../github/github-watch/README.md) opens an issue for it. The jobs that
build run on `ubuntu-latest`, or on the runner the repository variable
`CI_RUNNER` names, such as `ubuntu-24.04-arm`.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                         | Part  | Policy | Notes |
| ---------------------------- | ----- | ------ | ----- |
| `.github/workflows/bump.yml` | whole | owned  |       |
| `.github/scripts/bump.js`    | whole | owned  |       |

## Requires

- [`just`](../../tooling/just/README.md)
- [`github-watch`](../../github/github-watch/README.md)

<!-- /facts -->

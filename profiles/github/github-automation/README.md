# `github-automation`

The settings the GitHub automation reads, as keys of `.github/automation.json`,
and the helpers that act on them, `.github/scripts/automation.js`. Each issue
and pull request the automation opens carries its kind's labels and type and is
assigned to `assignees`, who are told in a comment what it holds and what is
theirs to do:

| Kind     | Labels          | Type | Opened for                                  |
| -------- | --------------- | ---- | ------------------------------------------- |
| `broken` | `bug`           | Bug  | a failing or stalled workflow, a red bump   |
| `chore`  | `dependencies`  | Task | the weekly bump                             |
| `docs`   | `documentation` | Task | the demo, recorded again at a release's tag |

The bump goes as far as `bump_mode` says, a branch or a pull request; each
automation merges its own pull requests only where the repository turns on its
feature `merge`, as [`github-bump`](../../github/github-bump/README.md) and
[`vhs`](../../docs/vhs/README.md) offer. With the run's own token it merges only
where the default branch's rules require no checks: GitHub holds the checks of a
pull request that token opens for a maintainer to approve, so there it leaves
the pull request to a person, and says so, unless the automation's GitHub App
merges it through auto-merge. A night with no new commit is skipped.

[`github-watch`](../../github/github-watch/README.md),
[`github-bump`](../../github/github-bump/README.md),
[`github-nightly`](../../github/github-nightly/README.md) and
[`vhs`](../../docs/vhs/README.md) read these keys. The policy is `merge`, so a
key the repository changes or adds stays its own, such as `pages`, which names
the site [`github-ci`](../../github/github-ci/README.md) deploys.

<!-- facts: written by devset-collection -->

## Owns

| File                            | Part  | Policy | Notes    |
| ------------------------------- | ----- | ------ | -------- |
| `.github/automation.json`       | keys  | merge  | template |
| `.github/scripts/automation.js` | whole | owned  |          |

## Variables

| Variable    | Default | Asks                                                                              |
| ----------- | ------- | --------------------------------------------------------------------------------- |
| `assignees` | empty   | GitHub logins assigned the automation's issues and pull requests, comma-separated |
| `bump_mode` | `pr`    | How far the weekly bump goes: branch, or pr to open a pull request                |

<!-- /facts -->

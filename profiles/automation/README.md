# `automation`

The settings the GitHub automation reads, as keys of `.github/automation.json`.
An issue for a failing or stalled workflow is labelled `bug` and typed Bug, and
the weekly bump's is labelled `dependencies` and typed Task; both are assigned
to `assignees`. The bump goes as far as `bump_mode` says, and a night with no
new commit is skipped.

[`github-watch`](../github-watch/README.md),
[`github-bump`](../github-bump/README.md) and
[`github-nightly`](../github-nightly/README.md) read these keys. The policy is
`merge`, so a key the repository changes or adds stays its own, such as `pages`,
which names the site [`github-ci`](../github-ci/README.md) deploys.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                      | Part | Policy | Notes    |
| ------------------------- | ---- | ------ | -------- |
| `.github/automation.json` | keys | merge  | template |

## Variables

| Variable    | Default | Asks                                                            |
| ----------- | ------- | --------------------------------------------------------------- |
| `assignees` | empty   | GitHub logins assigned the automation's issues, comma-separated |
| `bump_mode` | `pr`    | How far the weekly bump goes: branch, pr or merge               |

<!-- /facts -->

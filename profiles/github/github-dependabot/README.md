# `github-dependabot`

Weekly updates of the GitHub Actions the workflows use, grouped into one pull
request, past a three-day cooldown, each commit in the Conventional form
`ci(deps): …`, labelled `dependencies` and `automation`, and assigned to the
`assignees` [`github-automation`](../../github/github-automation/README.md)
names too.

Cargo dependencies move with [`cargo-bump`](../../cargo/cargo-bump/README.md),
one at a time; security updates are the repository's setting.

<!-- facts: written by devset-collection -->

## Owns

| File                     | Part  | Policy | Notes    |
| ------------------------ | ----- | ------ | -------- |
| `.github/dependabot.yml` | whole | merge  | template |

## Variables

| Variable    | Default | Asks                                                                              |
| ----------- | ------- | --------------------------------------------------------------------------------- |
| `assignees` | empty   | GitHub logins assigned the automation's issues and pull requests, comma-separated |

<!-- /facts -->

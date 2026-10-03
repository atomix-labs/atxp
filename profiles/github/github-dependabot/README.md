# `github-dependabot`

Weekly updates of the GitHub Actions the workflows use, grouped into one pull
request, past a three-day cooldown, each commit in the Conventional form
`ci(deps): …`, labelled `dependencies` and `automation`, and assigned to the
`assignees` [`github-automation`](../../github/github-automation/README.md)
names too.

Dependabot leaves alone the workflows devset writes, each named in
`exclude-paths` where the profile that writes it is applied: `check.yml` where
[`github-ci`](../../github/github-ci/README.md) is, `release.yml` where
[`github-release`](../../github/github-release/README.md) is, and so on. Their
actions move with their profiles, in a release of the collection that `devset
update` takes; an update to one of them by Dependabot is drift, which
`check-devset` fails. A workflow of the repository's own, as a `platforms.yml`
beside them, is not in the list, and gets its updates.

`exclude-paths`, in `dependabot.yml` on github.com and on GitHub Enterprise
Server from 3.19, is a list of paths or globs, relative to `directory`, that
Dependabot skips before it reads a manifest. It holds for `github-actions` as
for any ecosystem: Dependabot lists `.github/workflows` through the same filter.
It holds for version updates, the ones this file asks for, and not for security
updates, which can still open a pull request against an excluded workflow; close
it, and take the release that moves the action.

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

# `github-dependabot`

Weekly updates of the GitHub Actions the workflows use, grouped into one pull
request, past a three-day cooldown, each commit in the Conventional form
`ci(deps): …`.

Cargo dependencies move with [`cargo-bump`](../../cargo/cargo-bump/README.md),
one at a time; security updates are the repository's setting.

<!-- facts: written by devset-collection -->

## Owns

| File                     | Part  | Policy | Notes |
| ------------------------ | ----- | ------ | ----- |
| `.github/dependabot.yml` | whole | merge  |       |

<!-- /facts -->

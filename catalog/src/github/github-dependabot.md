# `github-dependabot`

Dependabot: weekly updates of the GitHub Actions a repository uses, in one pull
request.

```sh
devset add atxp/github-dependabot --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `github` · In [`rust`](../bundles/rust.md): always

Weekly updates of the GitHub Actions the workflows use, grouped into one pull
request, past a three-day cooldown, each commit in the Conventional form
`ci(deps): …`, and assigned to the `assignees`
[`github-automation`](github-automation.md) names too.

Cargo dependencies move with [`cargo-bump`](../cargo/cargo-bump.md), one at a
time; security updates are the repository's setting.

## Owns

| File                     | Part  | Policy | Notes    |
| ------------------------ | ----- | ------ | -------- |
| `.github/dependabot.yml` | whole | merge  | template |

## Variables

| Variable    | Default | Asks                                                                              |
| ----------- | ------- | --------------------------------------------------------------------------------- |
| `assignees` | empty   | GitHub logins assigned the automation's issues and pull requests, comma-separated |

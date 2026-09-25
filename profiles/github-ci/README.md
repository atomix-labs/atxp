# `github-ci`

One workflow, `check`, on every push to `main`, pull request and merge queue. It
reads the justfile and runs every `check-*` recipe as a job of its own, prepared
as a laptop is: mise-action runs `mise bootstrap`, so every locked tool is
installed and `just setup` runs, then Cargo's build is cached per recipe. What
`just check` runs on a checkout, CI runs, and no list of jobs can fall behind
the recipes. Each job checks out the whole history, which `check-committed` and
`check-git-cliff` read.

Require the job `check` in branch protection: it passes when every recipe does.
The jobs read the repository and nothing else. They run on `ubuntu-latest`, or
on the runner the repository variable `CI_RUNNER` names, such as
`ubuntu-24.04-arm`.

A repository that publishes a site with GitHub Pages names the recipe that
builds it in `.github/automation.json`: `"pages": { "recipe": "check-docs",
"path": "docs/book" }` (`path` defaults to `docs/book`). That job keeps the site
it checked: on a pull request as a preview, kept seven days, and on the default
branch as the deploy, which the job `deploy` publishes once `check` passes. So
the site is built once a change, and what is published is what was checked.
Pages must be set to deploy from GitHub Actions; `deploy` holds the only write
permissions, in the `github-pages` environment. A name that is no check recipe
fails the plan.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                          | Part  | Policy | Notes |
| ----------------------------- | ----- | ------ | ----- |
| `.github/workflows/check.yml` | whole | owned  |       |

## Requires

- [`just`](../just/README.md)

<!-- /facts -->

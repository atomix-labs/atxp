# `github-ci`

GitHub Actions: every `check-*` recipe a job of its own, read from the justfile,
tools from the mise lock; with pages, a site built once and deployed.

```sh
devset add atxp/github-ci --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `github` · In [`rust`](../bundles/rust.md): always

One workflow, `check`, on every push to `main`, pull request and merge queue. It
reads the justfile and runs every `check-*` recipe as a job of its own. The
tools come from one cache, which the job `plan` fills before any recipe runs, so
a changed lock downloads and builds each tool once rather than once a job. A job
installs no Rust toolchain up front: one installs where a recipe first runs
cargo, from `rust-toolchain.toml`. A recipe that runs cargo, rustc, rustdoc or
rustup says so with `[metadata("rust")]` above it, which
[`devset-collection`](../devset/devset-collection.md) holds a collection's
recipes to: its job restores and saves Cargo's build, per recipe, from the
default branch alone, which every pull request and merge group restores; any
other job starts no toolchain at all. That keeps the repository's caches under
GitHub's limit. What `just check` runs on a checkout, CI runs, and no list of
jobs can fall behind the recipes. Each job checks out the whole history, which
`check-git-changelog` reads.

Require the job `check` in the default branch's ruleset, beside
[`git-commits`](../git/git-commits.md)' `title`: it passes when every recipe
does. The jobs read the repository and nothing else. They run on
`ubuntu-latest`, or on the runner the repository variable `CI_RUNNER` names,
such as `ubuntu-24.04-arm`.

With the feature `pages`, which [`mdbook`](../docs/mdbook.md)'s `pages` turns
on, a repository that publishes a site with GitHub Pages names the recipe that
builds it, and the directory it builds the site in, in
`.github/automation.json`: `"pages": { "recipe": "check-docs", "path":
"docs/book" }`. That job keeps the site it checked: on a pull request as a
preview, kept seven days, and on the default branch as the deploy, which the job
`deploy` publishes once `check` passes. So the site is built once a change, and
what is published is what was checked. Pages must be set to deploy from GitHub
Actions; `deploy` holds the only write permissions, in the `github-pages`
environment. A name that is no check recipe, or no path, fails the plan.

The `agents` feature adds the `fixing-ci` skill in `.claude/skills/`: a failing
job reproduced by its recipe, and fixed at its cause.

## Owns

| File                                | Part  | Policy | Notes            |
| ----------------------------------- | ----- | ------ | ---------------- |
| `.github/workflows/check.yml`       | whole | owned  | template         |
| `.claude/skills/fixing-ci/SKILL.md` | whole | owned  | feature `agents` |

## Features

| Feature  | Default | Enables |
| -------- | ------- | ------- |
| `pages`  |         |         |
| `agents` |         |         |

## Requires

- [`github-automation`](github-automation.md)
- [`just`](../tooling/just.md)

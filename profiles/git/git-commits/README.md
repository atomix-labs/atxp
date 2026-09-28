# `git-commits`

committed holds what lands on the default branch to Conventional Commits,
`type(scope): subject`: an allowed type, an imperative subject with no closing
period, and no merge commit. The scope names the part the commit changes, a
profile or a crate. [`git-changelog`](../../git/git-changelog/README.md) writes
the changelog from these subjects, so each says what changed for someone who
reads it there.

A pull request lands squashed, as one commit its title names, so the title is
the subject. Where [`github-ci`](../../github/github-ci/README.md) is applied,
the workflow `title` checks it on every change to the pull request, an edit of
the title included; the default branch's ruleset requires its job `title` beside
`check`. A pull request's own commits never land, and CI leaves them be; a push
to the default branch has what it landed checked, so a squash message edited at
the merge is caught there. On a checkout, `just check-git-commits` checks every
commit the branch adds, for a branch that reads well while it is worked on;
where there is no default branch to compare with, there is nothing to check.
committed comes from its release, one static build for each platform the locks
cover.

Where the repository has a `CONTRIBUTING.md`, a block of it says these rules to
those who contribute.

With `agents`, a block of the repository's `AGENTS.md`, where it has one, says
the same rules to an agent.

<!-- facts: written by devset-collection -->

## Owns

| File                                          | Part  | Policy | Notes                                |
| --------------------------------------------- | ----- | ------ | ------------------------------------ |
| `committed.toml`                              | whole | owned  |                                      |
| `.just/git-commits.just`                      | whole | owned  |                                      |
| `.github/workflows/title.yml`                 | whole | owned  | profile `github-ci`                  |
| `.config/mise/conf.d/devset-git-commits.toml` | whole | owned  |                                      |
| `.config/mise/mise.lock`                      | keys  | owned  |                                      |
| `CONTRIBUTING.md`                             | block | owned  | `CONTRIBUTING.md` exists             |
| `AGENTS.md`                                   | block | owned  | feature `agents`, `AGENTS.md` exists |

## Features

| Feature  | Default | Enables |
| -------- | ------- | ------- |
| `agents` |         |         |

## Recipes

- `check-git-commits`: Checks commits against Conventional Commits: those a
  branch adds, or those a push landed.

<!-- /facts -->

# `git-commits`

committed checks every commit a branch adds to the default branch against
Conventional Commits, `type(scope): subject`: an allowed type, an imperative
subject with no closing period, and no merge commit. The scope names the part
the commit changes, a profile or a crate. [`git-cliff`](../../git/git-changelog/README.md)
writes the changelog from these subjects, so each says what changed for someone
who reads it there.

A pull request is checked out as a merge commit; the check reads the pull
request's own commits, its second parent's. Where there is no default branch to
compare with, there is nothing to check. committed builds with cargo: its
releases have no Linux arm64 build.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                        | Part  | Policy | Notes |
| ------------------------------------------- | ----- | ------ | ----- |
| `committed.toml`                            | whole | owned  |       |
| `.just/git-commits.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-git-commits.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                    | keys  | owned  |       |

## Recipes

- `check-git-commits`: Checks every commit the branch adds to the default branch:
  Conventional Commits, an allowed type.

<!-- /facts -->

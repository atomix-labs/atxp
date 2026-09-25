# `git-cliff`

git-cliff writes `CHANGELOG.md` from the commits at each release: `just
release`, with `RELEASE_VERSION` set, runs `release-git-cliff`, which gives the
release its section. A release lists Features, Bug Fixes, Pins (the weekly
bumps), Refactor, Documentation, CI and Miscellaneous; each entry links its
commit, names its scope, and is marked **breaking** where it is; and the release
ends with its compare link. Release commits, and history that is not
conventional, are left out; [`committed`](../committed/README.md) keeps the rest
conventional.

`repository`, the GitHub repository as `owner/name`, makes the links; it has no
default, so every repository answers it. The changelog's opening paragraph links
`BREAKING-CHANGES.md`, which the repository keeps beside it. `check-git-cliff`
renders the unreleased notes on every change, so a broken configuration is found
before a release needs it.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                        | Part  | Policy | Notes    |
| ------------------------------------------- | ----- | ------ | -------- |
| `cliff.toml`                                | whole | owned  | template |
| `.just/git-cliff.just`                      | whole | owned  |          |
| `.config/mise/conf.d/devset-git-cliff.toml` | whole | owned  |          |
| `.config/mise/mise.lock`                    | keys  | owned  |          |

## Recipes

- `check-git-cliff`: Checks the configuration renders the notes of what is not
  yet released.
- `release-git-cliff`: Writes CHANGELOG.md for v$RELEASE_VERSION.

## Variables

| Variable     | Default | Asks                                                       |
| ------------ | ------- | ---------------------------------------------------------- |
| `repository` | none    | The GitHub repository the changelog links into, owner/name |

<!-- /facts -->

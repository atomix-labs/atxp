# `git-changelog`

git-cliff writes `CHANGELOG.md` from the commits at each release: `just
release`, with `RELEASE_VERSION` set, runs `release-git-changelog`, which gives
the release its section. A release lists Features, Bug Fixes, Pins (the weekly
bumps), Refactor, Documentation, CI and Miscellaneous; each entry links its
commit, names its scope, and is marked **breaking** where it is; and the release
ends with its compare link. Release commits, and history that is not
conventional, are left out; [`git-commits`](../../git/git-commits/README.md)
keeps the rest conventional.

`repository`, the GitHub repository as `owner/name`, makes the links; it has no
default, so every repository answers it. Where the repository has no
`CHANGELOG.md`, it scaffolds one holding the opening paragraph, which each
release writes again. With the feature `breaking-changes`, which
[`project`](../../project/project/README.md)'s turns on, the paragraph links
`BREAKING-CHANGES.md`, which the repository keeps beside it.
`check-git-changelog` renders the unreleased notes on every change, so a broken
configuration is found before a release needs it.

<!-- facts: written by devset-collection -->

## Owns

| File                                            | Part  | Policy | Notes                          |
| ----------------------------------------------- | ----- | ------ | ------------------------------ |
| `CHANGELOG.md`                                  | whole | once   | template, scaffold `changelog` |
| `cliff.toml`                                    | whole | owned  | template                       |
| `.just/git-changelog.just`                      | whole | owned  |                                |
| `.config/mise/conf.d/devset-git-changelog.toml` | whole | owned  |                                |
| `.config/mise/mise.lock`                        | keys  | owned  |                                |

## Features

| Feature            | Default | Enables |
| ------------------ | ------- | ------- |
| `breaking-changes` |         |         |

## Recipes

- `check-git-changelog`: Checks the configuration renders the notes of what is
  not yet released.
- `release-git-changelog`: Writes CHANGELOG.md for v$RELEASE_VERSION.

## Variables

| Variable     | Default | Asks                              |
| ------------ | ------- | --------------------------------- |
| `repository` | none    | The GitHub repository, owner/name |

<!-- /facts -->

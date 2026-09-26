# `shell`

ShellCheck lints every `*.sh` and `*.bash` file the repository owns, tracked or
new, following the files each one sources (`-x`). A file `.gitattributes` marks
`linguist-vendored` or `linguist-generated`, as GitHub reads them, is someone
else's and is left out.
[`github-workflow-lint`](../../github/github-workflow-lint/README.md) runs it on
workflow steps too, where both are applied.

Its one feature, `lint`, on by default, is all of it: a repository that wants
none of ShellCheck applies the profile without its default features.

<!-- facts: written by devset-collection -->

## Owns

| File                                    | Part  | Policy | Notes          |
| --------------------------------------- | ----- | ------ | -------------- |
| `.just/shell.just`                      | whole | owned  | feature `lint` |
| `.config/mise/conf.d/devset-shell.toml` | whole | owned  | feature `lint` |
| `.config/mise/mise.lock`                | keys  | owned  | feature `lint` |

## Features

| Feature | Default | Enables |
| ------- | ------- | ------- |
| `lint`  | yes     |         |

## Recipes

- `check-shell`: Lints every shell script the repository owns, following what
  each sources; one under a vendor/ directory, or that .gitattributes marks
  `linguist-vendored` or `linguist-generated`, is someone else's.

<!-- /facts -->

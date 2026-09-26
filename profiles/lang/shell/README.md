# `shell`

ShellCheck lints every `*.sh` and `*.bash` file the repository owns, tracked or
new, following the files each one sources (`-x`). A file `.gitattributes` marks
`linguist-vendored` or `linguist-generated`, as GitHub reads them, is someone
else's and is left out. [`github-workflow-lint`](../../github/github-workflow-lint/README.md) runs it on
workflow steps too, where both are applied.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                         | Part  | Policy | Notes |
| -------------------------------------------- | ----- | ------ | ----- |
| `.just/shell.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-shell.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                     | keys  | owned  |       |

## Recipes

- `check-shell`: Lints every shell script the repository owns, following
  what each sources; a file .gitattributes marks `linguist-vendored` or
  `linguist-generated` is someone else's.

<!-- /facts -->

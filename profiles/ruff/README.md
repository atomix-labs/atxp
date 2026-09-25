# `ruff`

Ruff lints Python at `line_width`: import sorting, bugbear, pyupgrade, simplify
and Ruff's own rules, beside its defaults; imports at the top of a module; and
every public method documented. Formatting is [`dprint`](../dprint/README.md)'s,
through its Ruff plugin, so one tool formats every file.

It owns those keys of `ruff.toml`, under `merge`: `target-version`, and rules
the repository adds, stay its own.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                   | Part  | Policy | Notes    |
| -------------------------------------- | ----- | ------ | -------- |
| `ruff.toml`                            | keys  | merge  | template |
| `.just/ruff.just`                      | whole | owned  |          |
| `.config/mise/conf.d/devset-ruff.toml` | whole | owned  |          |
| `.config/mise/mise.lock`               | keys  | owned  |          |

## Recipes

- `check-ruff`: Lints every Python file; formatting is dprint's.
- `fix-ruff`: Fixes what Ruff can.

## Variables

| Variable     | Default | Asks                                                  |
| ------------ | ------- | ----------------------------------------------------- |
| `line_width` | `100`   | Line width, shared by the formatters and EditorConfig |

<!-- /facts -->

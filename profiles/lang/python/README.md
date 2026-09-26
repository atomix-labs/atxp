# `python`

Ruff lints Python at `line_width`: import sorting, bugbear, pyupgrade, simplify
and Ruff's own rules, beside its defaults; imports at the top of a module; and
every public method documented. Formatting is
[`dprint`](../../lang/dprint/README.md)'s, through its Ruff plugin, whose
settings this profile keeps as keys of `dprint.json`, so one tool formats every
file.

It owns those keys of `ruff.toml`, under `merge`: `target-version`, and rules
the repository adds, stay its own.

Git ignores Python's bytecode, in a block of `.gitignore`.

Each half is a feature, both on by default: `lint`, Ruff's configuration, pin
and recipes, and `format`, dprint's Ruff settings. Git ignores the bytecode
either way.

<!-- facts: written by devset-collection -->

## Owns

| File                                     | Part  | Policy | Notes                    |
| ---------------------------------------- | ----- | ------ | ------------------------ |
| `ruff.toml`                              | keys  | merge  | template, feature `lint` |
| `.just/python.just`                      | whole | owned  | feature `lint`           |
| `.config/mise/conf.d/devset-python.toml` | whole | owned  | feature `lint`           |
| `.config/mise/mise.lock`                 | keys  | owned  | feature `lint`           |
| `.gitignore`                             | block | owned  |                          |
| `dprint.json`                            | keys  | merge  | feature `format`         |

## Features

| Feature  | Default | Enables      |
| -------- | ------- | ------------ |
| `lint`   | yes     |              |
| `format` | yes     | `dep:dprint` |

## Recipes

- `check-python`: Lints every Python file; formatting is dprint's.
- `fix-python`: Fixes what Ruff can.

## Variables

| Variable     | Default | Asks                                                  |
| ------------ | ------- | ----------------------------------------------------- |
| `line_width` | `100`   | Line width, shared by the formatters and EditorConfig |

## Requires

- [`dprint`](../dprint/README.md): optional

<!-- /facts -->

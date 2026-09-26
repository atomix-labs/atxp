# `toml`

taplo formats every TOML file in one layout: entries and comments aligned,
arrays on one line where they fit and one element a line where they do not, four
spaces of indent, and entries in alphabetical order in dependency tables, where
a blank line keeps `# external` and `# internal` apart. Left out are Cargo's
`target/`, `node_modules/`, and what devset owns whole, `.devset/` and the
profiles' pins in `.config/mise/conf.d/`, which no formatter may rewrite. Every
TOML file a profile ships is in this layout, and devset writes a key it adds to
a file in it too.

It owns those keys of `taplo.toml`, under `merge`: `include`, other rules, and
paths the repository adds to `exclude` stay its own.
[`cargo-manifest`](../../cargo/cargo-manifest/README.md) holds what taplo cannot
see.

Each half is a feature: `format`, taplo's layout, and `lint`, which checks every
TOML file parses and holds it to the schemas `taplo.toml` names; both are on by
default. `schemas` adds devset's own, for every `profile.toml` and
`collection.toml`, which `lint` fetches online; `devset-collection` turns it on.

<!-- facts: written by devset-collection -->

## Owns

| File                                   | Part  | Policy | Notes    |
| -------------------------------------- | ----- | ------ | -------- |
| `taplo.toml`                           | keys  | merge  | template |
| `.just/toml.just`                      | whole | owned  | template |
| `.config/mise/conf.d/devset-toml.toml` | whole | owned  |          |
| `.config/mise/mise.lock`               | keys  | owned  |          |

## Features

| Feature   | Default | Enables |
| --------- | ------- | ------- |
| `format`  | yes     |         |
| `lint`    | yes     |         |
| `schemas` |         |         |

## Recipes

- `check-toml`: Checks every TOML file: in its layout, with `format`; valid, and
  true to its schema where taplo.toml names one, with `lint`.
- `fix-toml`: Formats every TOML file.

## Variables

| Variable     | Default | Asks                                                  |
| ------------ | ------- | ----------------------------------------------------- |
| `line_width` | `100`   | Line width, shared by the formatters and EditorConfig |

<!-- /facts -->

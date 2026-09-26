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

<!-- facts: written by devset-collection -->

## Owns

| File                                   | Part  | Policy | Notes    |
| -------------------------------------- | ----- | ------ | -------- |
| `taplo.toml`                           | keys  | merge  | template |
| `.just/toml.just`                      | whole | owned  |          |
| `.config/mise/conf.d/devset-toml.toml` | whole | owned  |          |
| `.config/mise/mise.lock`               | keys  | owned  |          |

## Recipes

- `check-toml`: Checks that every TOML file is formatted.
- `fix-toml`: Formats every TOML file.

## Variables

| Variable     | Default | Asks                                                  |
| ------------ | ------- | ----------------------------------------------------- |
| `line_width` | `100`   | Line width, shared by the formatters and EditorConfig |

<!-- /facts -->

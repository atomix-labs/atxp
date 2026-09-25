# `rustfmt`

rustfmt on nightly's options, at `line_width`: the 2024 style edition; imports
grouped by module, then std, external crates and the crate's own; comments and
doc examples wrapped; macros' matchers formatted; and hex literals in upper
case. It needs the nightly [`rust-toolchain`](../rust-toolchain/README.md) pins.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                 | Part  | Policy | Notes    |
| -------------------- | ----- | ------ | -------- |
| `rustfmt.toml`       | whole | owned  | template |
| `.just/rustfmt.just` | whole | owned  |          |

## Recipes

- `check-rustfmt`: Checks that every crate is formatted.
- `fix-rustfmt`: Formats every crate.

## Variables

| Variable     | Default | Asks                                                  |
| ------------ | ------- | ----------------------------------------------------- |
| `line_width` | `100`   | Line width, shared by the formatters and EditorConfig |

<!-- /facts -->

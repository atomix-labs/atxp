# `rust-fmt`

rustfmt on nightly's options, at `line_width`: the 2024 style edition; imports
grouped by module, then std, external crates and the crate's own; comments and
doc examples wrapped; macros' matchers formatted; and hex literals in upper
case. It needs the nightly
[`rust-toolchain`](../../rust/rust-toolchain/README.md) pins.

It owns those keys of `rustfmt.toml`, under `merge`: an option the repository
adds, or a value it changes, stays its own.

<!-- facts: written by devset-collection -->

## Owns

| File                  | Part  | Policy | Notes    |
| --------------------- | ----- | ------ | -------- |
| `rustfmt.toml`        | keys  | merge  | template |
| `.just/rust-fmt.just` | whole | owned  |          |

## Recipes

- `check-rust-fmt`: Checks that every crate is formatted.
- `fix-rust-fmt`: Formats every crate.

## Variables

| Variable     | Default | Asks                                                  |
| ------------ | ------- | ----------------------------------------------------- |
| `line_width` | `100`   | Line width, shared by the formatters and EditorConfig |

## Requires

- [`rust-toolchain`](../rust-toolchain/README.md)

<!-- /facts -->

# `rust-fmt`

rustfmt on nightly's options, at `line_width`: the 2024 style edition; imports
grouped by module, then std, external crates and the crate's own; comments and
doc examples wrapped; macros' matchers formatted; and hex literals in upper
case. Those options are nightly's own: with
[`rust-toolchain`](../../rust/rust-toolchain/README.md)'s `channel` `stable`,
`rustfmt.toml` holds only the stable ones, so a stable rustfmt warns of nothing.

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

| Variable     | Default   | Asks                                                        |
| ------------ | --------- | ----------------------------------------------------------- |
| `channel`    | `nightly` | The toolchain: nightly, the one the profiles pin, or stable |
| `line_width` | `100`     | Line width, shared by the formatters and EditorConfig       |

## Requires

- [`rust-toolchain`](../rust-toolchain/README.md)

<!-- /facts -->

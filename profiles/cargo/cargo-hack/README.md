# `cargo-hack`

cargo-hack runs clippy on every crate with each feature on its own, which is how
a feature that compiles only beside another is found. It builds once a feature,
so it runs nightly.

<!-- facts: written by devset-collection -->

## Owns

| File                                         | Part  | Policy | Notes |
| -------------------------------------------- | ----- | ------ | ----- |
| `.just/cargo-hack.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-cargo-hack.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                     | keys  | owned  |       |

## Recipes

- `nightly-cargo-hack`: Lints every crate with each feature alone; a warning
  fails.

## Requires

- [`rust-toolchain`](../../rust/rust-toolchain/README.md)

<!-- /facts -->

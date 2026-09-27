# `cargo-hack`

cargo-hack lints every crate with each of its features alone, nightly, where a
feature can break.

```sh
devset add atxp/cargo-hack --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `cargo` · In [`rust`](../bundles/rust.md): with `nightly`

cargo-hack runs clippy on every crate with each feature on its own, which is how
a feature that compiles only beside another is found. It builds once a feature,
so it runs nightly.

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

- [`rust-toolchain`](../rust/rust-toolchain.md)

# `rust-clippy`

Clippy over every crate, target and feature, warnings denied; tests may unwrap,
panic and print.

```sh
devset add atxp/rust-clippy --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `rust` · In [`rust`](../bundles/rust.md): always

Clippy over every crate, target and feature, with warnings denied; in tests,
`unwrap`, `expect`, panics, printing, `dbg!` and indexing are allowed.

It owns those keys of `clippy.toml`; the repository's own, such as a
`disallowed-methods` list, stay its own. Which lints are denied is the
workspace's `[lints]` table, which [`rust-lints`](rust-lints.md) owns.

## Owns

| File                     | Part  | Policy | Notes |
| ------------------------ | ----- | ------ | ----- |
| `clippy.toml`            | keys  | owned  |       |
| `.just/rust-clippy.just` | whole | owned  |       |

## Recipes

- `check-rust-clippy`: Lints every crate, target and feature; a warning fails.
- `fix-rust-clippy`: Applies clippy's suggestions.

## Requires

- [`rust-toolchain`](rust-toolchain.md)

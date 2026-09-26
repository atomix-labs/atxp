# `rust-clippy`

Clippy over every crate, target and feature, with warnings denied; in tests,
`unwrap`, `expect`, panics, printing, `dbg!` and indexing are allowed.

It owns those keys of `clippy.toml`; the repository's own, such as a
`disallowed-methods` list, stay its own. Which lints are denied is the
workspace's `[lints]` table, which [`lints`](../../rust/rust-lints/README.md) owns.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                | Part  | Policy | Notes |
| ------------------- | ----- | ------ | ----- |
| `clippy.toml`       | keys  | owned  |       |
| `.just/rust-clippy.just` | whole | owned  |       |

## Recipes

- `check-rust-clippy`: Lints every crate, target and feature; a warning fails.
- `fix-rust-clippy`: Applies clippy's suggestions.

<!-- /facts -->

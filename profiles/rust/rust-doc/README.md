# `rust-doc`

rustdoc builds every crate's documentation with every feature, private items
included, and fails on any warning: a broken intra-doc link, a malformed code
block, a missing item it refers to.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                 | Part  | Policy | Notes |
| -------------------- | ----- | ------ | ----- |
| `.just/rust-doc.just` | whole | owned  |       |

## Recipes

- `check-rust-doc`: Builds every crate's documentation, private items included; a
  warning, such as a broken link, fails.

<!-- /facts -->

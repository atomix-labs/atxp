# `rust-doc`

rustdoc builds every crate's documentation with every feature, private items
included, and fails on any warning: a broken intra-doc link, a malformed code
block, a missing item it refers to.

The `agents` feature adds the `writing-rustdoc` skill in `.claude/skills/`: the
house style for docs and comments, with its audit, inventory and lint scripts,
so an agent writes documentation as the repository wants it.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                 | Part  | Policy | Notes |
| -------------------- | ----- | ------ | ----- |
| `.just/rust-doc.just` | whole | owned  |       |

## Recipes

- `check-rust-doc`: Builds every crate's documentation, private items included; a
  warning, such as a broken link, fails.

<!-- /facts -->

# `manifest-lint`

Holds every crate's `Cargo.toml` to one shape, where
[`taplo`](../taplo/README.md), which reads values and not the text around them,
cannot reach: `[package]` keys in their order, with every field the workspace
sets inherited; dependencies under `# external` then `# internal`, each where it
belongs, an internal one inherited from the workspace; `default` first among the
features; no comment but the two markers; and `[lints] workspace = true`. A
crate under a `vendor/` directory is upstream's, and is left alone.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                       | Part  | Policy | Notes |
| -------------------------- | ----- | ------ | ----- |
| `.just/manifest-lint.just` | whole | owned  |       |
| `.just/manifest-lint.py`   | whole | owned  |       |

## Recipes

- `check-manifest-lint`: Holds every crate manifest to one shape: what taplo,
  which reads values, cannot see.

<!-- /facts -->

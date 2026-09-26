# `cargo-unused`

cargo-machete finds dependencies no crate uses. It reads the sources, so it is
fast, and a macro can fool it; [`cargo-shear`](../../cargo/cargo-shear/README.md), which
reads the compiled graph, complements it.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                            | Part  | Policy | Notes |
| ----------------------------------------------- | ----- | ------ | ----- |
| `.just/cargo-unused.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-cargo-unused.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                        | keys  | owned  |       |

## Recipes

- `check-cargo-unused`: Fails on a dependency no crate uses.
- `fix-cargo-unused`: Removes each dependency no crate uses.

<!-- /facts -->

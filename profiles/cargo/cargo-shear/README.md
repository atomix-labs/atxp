# `cargo-shear`

cargo-shear finds dependencies no crate uses. It reads the compiled graph, so it
is thorough, and it catches workspace dependencies no member inherits too;
[`cargo-machete`](../../cargo/cargo-unused/README.md), which reads the sources,
complements it.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                          | Part  | Policy | Notes |
| --------------------------------------------- | ----- | ------ | ----- |
| `.just/cargo-shear.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-cargo-shear.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                      | keys  | owned  |       |

## Recipes

- `check-cargo-shear`: Fails on a dependency no crate uses.
- `fix-cargo-shear`: Removes each dependency no crate uses.

<!-- /facts -->

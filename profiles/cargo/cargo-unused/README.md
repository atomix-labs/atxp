# `cargo-unused`

Dependencies no crate uses. cargo-machete reads the sources, so it is fast, and
a macro can fool it; cargo-shear reads the compiled graph, so it is thorough,
and it catches workspace dependencies no member inherits too. Each is a feature,
`machete` and `shear`, both on by default: `check-cargo-unused` runs the ones
that are on, and `fix-cargo-unused` removes what they find. Both are built with
cargo, so their pins lock no platform.

<!-- facts: written by devset-collection -->

## Owns

| File                                           | Part  | Policy | Notes    |
| ---------------------------------------------- | ----- | ------ | -------- |
| `.just/cargo-unused.just`                      | whole | owned  | template |
| `.config/mise/conf.d/devset-cargo-unused.toml` | whole | owned  | template |
| `.config/mise/mise.lock`                       | keys  | owned  | template |

## Features

| Feature   | Default | Enables |
| --------- | ------- | ------- |
| `machete` | yes     |         |
| `shear`   | yes     |         |

## Recipes

- `check-cargo-unused`: Fails on a dependency no crate uses, by each tool the
  profile's features turn on, and names each tool that found one.
- `fix-cargo-unused`: Removes each dependency no crate uses, by each tool the
  profile's features turn on.

## Requires

- [`rust-toolchain`](../../rust/rust-toolchain/README.md)

<!-- /facts -->

# `msrv`

`check-msrv` builds every crate, with every target and feature, on the oldest
`rust-version` a crate of the workspace declares: that toolchain, installed by
rustup at the minimal profile, is the one the crates say they support, so a
newer API or syntax fails here and not on a user's machine.

It is outside the [`rust`](../rust/README.md) bundle: a repository that builds
only on nightly declares nightly's version, which no stable toolchain has.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File              | Part  | Policy | Notes |
| ----------------- | ----- | ------ | ----- |
| `.just/msrv.just` | whole | owned  |       |
| `.just/msrv.py`   | whole | owned  |       |

## Recipes

- `check-msrv`: Builds every crate on the oldest rust-version one declares,
  every target and feature included.

## Requires

- [`rustup`](../rustup/README.md)

<!-- /facts -->

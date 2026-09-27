# `rust-msrv`

Every crate builds on the rust-version it declares: the oldest toolchain it says
it supports.

```sh
devset add atxp/rust-msrv --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `rust`

`check-rust-msrv` builds every crate, with every target and feature, on the
oldest `rust-version` a crate of the workspace declares: that toolchain,
installed by rustup at the minimal profile, is the one the crates say they
support, so a newer API or syntax fails here and not on a user's machine.

It is outside the [`rust`](../bundles/rust.md) bundle: a repository that builds
only on nightly declares nightly's version, which no stable toolchain has.

## Owns

| File                   | Part  | Policy | Notes |
| ---------------------- | ----- | ------ | ----- |
| `.just/rust-msrv.just` | whole | owned  |       |
| `.just/rust-msrv.py`   | whole | owned  |       |

## Recipes

- `check-rust-msrv`: Builds every crate on the oldest rust-version one declares,
  every target and feature included.

## Requires

- [`rust-toolchain`](rust-toolchain.md)

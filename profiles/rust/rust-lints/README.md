# `rust-lints`

The lint wall, as keys of the workspace `Cargo.toml`: `[workspace.lints]` for
rustc, rustdoc, clippy and cargo. The keys any open-source project can take deny
rustdoc's and cargo's lints, clippy's `all` and `pedantic` groups, and rustc's
lints for correctness: `unsafe_op_in_unsafe_fn`, `unused_must_use`, the 2018
idioms. The `strict` feature, the house policy, adds the wall on top: clippy's
`nursery` and the restriction lints (no `unwrap`, no `panic`, no indexing, no
`as`, no printing, and more), and rustc's `unsafe_code`, `missing_docs`,
`unreachable_pub`, `unused` and the lifetime lints.

Every lint in the keys is one stable rustc knows, so a crate under the wall
builds on stable too. Every other key of `Cargo.toml` is the repository's, and
so is `unexpected_cfgs`, whose `check-cfg` names each repository's own cfgs.

The `nightly` feature adds the two lints only nightly rustc has:
`non_exhaustive_omitted_patterns`, which catches a `match` on a
`#[non_exhaustive]` enum that falls to its wildcard for a variant it could name,
and `implicit_provenance_casts`, which catches a pointer cast to an integer that
exposes its provenance. `check-rust-lints` runs them with `cargo check` on the
nightly [`rust-toolchain`](../../rust/rust-toolchain/README.md) pins, their
features switched on by `-Zcrate-attr`, so no source needs a `#![feature]` and
[`rust-msrv`](../../rust/rust-msrv/README.md) can still prove a crate builds on
stable. A crate that enables them itself, as one built on nightly alone may, is
no fault: the check allows the feature enabled twice.

<!-- facts: written by devset-collection -->

## Owns

| File                    | Part  | Policy | Notes             |
| ----------------------- | ----- | ------ | ----------------- |
| `Cargo.toml`            | keys  | owned  | template          |
| `.just/rust-lints.just` | whole | owned  | feature `nightly` |

## Features

| Feature   | Default | Enables |
| --------- | ------- | ------- |
| `nightly` |         |         |
| `strict`  |         |         |

## Recipes

- `check-rust-lints`: Checks the lints only nightly has: their features come
  from -Zcrate-attr, so no source needs a #![feature], and every crate still
  builds on stable; a crate that enables them itself is no fault.

## Requires

- [`rust-toolchain`](../rust-toolchain/README.md)

<!-- /facts -->

# `lints-nightly`

The two lints only nightly rustc has: `non_exhaustive_omitted_patterns`, which
catches a `match` on a `#[non_exhaustive]` enum that falls to its wildcard for a
variant it could name, and `implicit_provenance_casts`, which catches a pointer
cast to an integer that exposes its provenance. `check-lints-nightly` runs them
with `cargo check` on the nightly
[`rust-toolchain`](../../rust/rust-toolchain/README.md) pins, their features switched on
by `-Zcrate-attr`, so no source needs a `#![feature]`: a crate under
[`lints`](../../rust/rust-lints/README.md) and this still builds on stable, and
[`msrv`](../../rust/rust-msrv/README.md) can prove it.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                       | Part  | Policy | Notes |
| -------------------------- | ----- | ------ | ----- |
| `.just/lints-nightly.just` | whole | owned  |       |

## Recipes

- `check-lints-nightly`: Checks the lints only nightly has: their features come
  from -Zcrate-attr, so no source needs a #![feature], and every crate still
  builds on stable.

## Requires

- [`rust-toolchain`](../../rust/rust-toolchain/README.md)

<!-- /facts -->

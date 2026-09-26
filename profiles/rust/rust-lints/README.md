# `rust-lints`

The lint wall, as keys of the workspace `Cargo.toml`: `[workspace.lints]` for
rustc, rustdoc, clippy and cargo. Clippy's `all`, `pedantic` and `nursery`
groups are denied, with the restriction lints on top.

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
stable.

<!-- facts: written by scripts/catalog.py -->
<!-- /facts -->

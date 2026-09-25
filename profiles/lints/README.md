# `lints`

The lint wall, as keys of the workspace `Cargo.toml`: `[workspace.lints]` for
rustc, rustdoc, clippy and cargo. Clippy's `all`, `pedantic` and `nursery`
groups are denied, with the restriction lints on top.

Two of rustc's lints are nightly's alone, `non_exhaustive_omitted_patterns` and
`implicit_provenance_casts`: every crate enables them, with
`#![feature(non_exhaustive_omitted_patterns_lint, strict_provenance_lints)]`, on
the nightly [`rust-toolchain`](../rust-toolchain/README.md) pins. Every other
key of `Cargo.toml` is the repository's, and so is `unexpected_cfgs`, whose
`check-cfg` names each repository's own cfgs.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File         | Part | Policy | Notes |
| ------------ | ---- | ------ | ----- |
| `Cargo.toml` | keys | owned  |       |

<!-- /facts -->

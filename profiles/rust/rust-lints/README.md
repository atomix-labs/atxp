# `rust-lints`

The lint wall, as keys of the workspace `Cargo.toml`: `[workspace.lints]` for
rustc, rustdoc, clippy and cargo. Clippy's `all`, `pedantic` and `nursery`
groups are denied, with the restriction lints on top.

Every lint here is one stable rustc knows, so a crate under the wall builds on
stable too; the two only nightly has are
[`lints-nightly`](../../rust/lints-nightly/README.md)'s. Every other key of `Cargo.toml`
is the repository's, and so is `unexpected_cfgs`, whose `check-cfg` names each
repository's own cfgs.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File         | Part | Policy | Notes |
| ------------ | ---- | ------ | ----- |
| `Cargo.toml` | keys | owned  |       |

<!-- /facts -->

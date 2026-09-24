# `lints`

The house lint wall, as keys of the workspace `Cargo.toml`: `[workspace.lints]`
for rustc, rustdoc, clippy and cargo. clippy's `all`, `pedantic` and `nursery`
groups are denied, with the restriction lints the house holds to on top.

Every other key of `Cargo.toml` is the repository's, and so is
`unexpected_cfgs`, whose `check-cfg` names each repository's own cfgs. Some
lints are nightly's only: take `rust-nightly` with it.

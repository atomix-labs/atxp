# `cargo-workspace`

A Cargo workspace's own settings. Git ignores Cargo's `target/` at any depth,
rustfmt's `.rs.bk` backups, and MSVC debug files, in a block of `.gitignore`.
`.cargo/config.toml`'s resolver takes, for each dependency, the newest release
the workspace's `rust-version` builds (`incompatible-rust-versions =
"fallback"`), so a lock updated by hand or by a bump never needs a newer Rust.

It owns that block and that key; the repository's own lines, and every other key
of `.cargo/config.toml`, stay its own.

<!-- facts: written by devset-collection -->

## Owns

| File                 | Part  | Policy | Notes |
| -------------------- | ----- | ------ | ----- |
| `.gitignore`         | block | owned  |       |
| `.cargo/config.toml` | keys  | owned  |       |

<!-- /facts -->

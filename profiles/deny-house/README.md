# `deny-house`

The house's cargo-deny policy, as keys of `deny.toml` beside those of the
collection's `cargo-deny`: an unmaintained crate is refused, a crate may appear
at one version only, a git source is pinned by commit, and the crates the house
has chosen against are banned, each with the crate to use instead.

`skip`, `[graph]` and `allow-git` stay the repository's.

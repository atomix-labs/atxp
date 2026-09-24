# `rust-nightly`

The house toolchain, a flavor of the collection's `rust-toolchain`: one pinned
nightly, with rustfmt, clippy, miri, rustc-dev, llvm-tools and the standard
library's sources. It owns `channel` and `components` of `rust-toolchain.toml`;
`targets` stays the repository's.

The nightly moves here, by `just bump-rust-nightly`: to the newest nightly of
the last fourteen days that has every component on every platform the house
builds on, never backwards.

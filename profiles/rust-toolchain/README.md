# `rust-toolchain`

The toolchain a checkout builds with: one pinned nightly, with `rust-src`,
rustfmt, clippy, miri, `rustc-dev` and `llvm-tools`, on rustup's minimal
profile; [`rustup`](../rustup/README.md) installs it on `just setup`. The
nightly moves weekly with atxp's `bump-rust-toolchain`, to the newest nightly of
the last fourteen days that has every component on every platform the locks
cover, never backwards; a repository takes it with `devset update`.

It owns those keys of `rust-toolchain.toml`: `targets` stays the repository's.
`.just/rust-toolchain.just` exports `CARGO_BUILD_TARGET` as the host's triple,
so every cargo command names its target and keeps `RUSTFLAGS` off host build
scripts, which a build under `target-cpu=native` can break; a recipe whose
output must land in `target/doc` rather than `target/<triple>/doc` unsets it.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                        | Part  | Policy | Notes |
| --------------------------- | ----- | ------ | ----- |
| `rust-toolchain.toml`       | keys  | owned  |       |
| `.just/rust-toolchain.just` | whole | owned  |       |

## Requires

- [`rustup`](../rustup/README.md)

<!-- /facts -->

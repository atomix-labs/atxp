# `rust-toolchain`

The toolchain a checkout builds with, on rustup's minimal profile, and rustup
itself where it is missing: `rust-src`, rustfmt and clippy, which the checks
use. With `channel` `nightly`, the default, it is one pinned nightly, which
moves weekly with atxp's `bump-rust-toolchain`, to the newest nightly of the
last fourteen days that has every component on every platform the locks cover,
those the features add included, never backwards; a repository takes it with
`devset update`. With `channel` `stable`, it is the current stable release;
`rust-lints`' `nightly` and `cargo-hack` need the nightly.

Three features add a component each, off unless a repository turns them on,
since no check uses them and each adds to every checkout's download: `miri`,
which runs tests to find undefined behaviour, and `rustc-dev`, for tools that
link the compiler, both with the nightly; and `llvm-tools`, for coverage and
profiling. `devset add atxp/rust-toolchain --features miri` turns one on.

`.just/rust-toolchain.sh` installs rustup with rustup's own installer where it
is missing, with no default toolchain and without editing shell profiles, then
runs `rustup toolchain install`, which installs the toolchain
`rust-toolchain.toml` names, its components included; rustup verifies every
toolchain it downloads. mise runs it as a `preinstall` hook, before it installs
any tool: the tools it builds with cargo need the toolchain, and several builds
at once would each start to install it, over one another. `just setup` runs it
again, as `setup-rust-toolchain`, for a toolchain a bump has moved. Cargo's bin
directory, `$CARGO_HOME/bin`, joins mise's PATH, so wherever mise is active (a
shell, a task, `mise exec`, CI through mise-action) `cargo` and `rustc` are
found without a line in the shell's rc.

It owns those keys of `rust-toolchain.toml`: `targets` stays the repository's.
`.just/rust-toolchain.just` exports `CARGO_BUILD_TARGET` as the host's triple,
so every cargo command names its target and keeps `RUSTFLAGS` off host build
scripts, which a build under `target-cpu=native` can break. The triple is the
machine's, from just's `arch()` and `os()` and the C library, not rustc's, so a
recipe that runs no Rust tool starts no toolchain; a recipe whose output must
land in `target/doc` rather than `target/<triple>/doc` unsets it.

<!-- facts: written by devset-collection -->

## Owns

| File                                             | Part  | Policy | Notes      |
| ------------------------------------------------ | ----- | ------ | ---------- |
| `rust-toolchain.toml`                            | keys  | owned  | template   |
| `.just/rust-toolchain.just`                      | whole | owned  |            |
| `.just/rust-toolchain.sh`                        | whole | owned  | executable |
| `.config/mise/conf.d/devset-rust-toolchain.toml` | whole | owned  |            |

## Features

| Feature      | Default | Enables |
| ------------ | ------- | ------- |
| `miri`       |         |         |
| `rustc-dev`  |         |         |
| `llvm-tools` |         |         |

## Recipes

- `setup-rust-toolchain`: Installs rustup where it is missing, then the
  toolchain rust-toolchain.toml names.

## Variables

| Variable  | Default   | Asks                                                        |
| --------- | --------- | ----------------------------------------------------------- |
| `channel` | `nightly` | The toolchain: nightly, the one the profiles pin, or stable |

## Requires

- [`just`](../../tooling/just/README.md)
- [`mise`](../../tooling/mise/README.md)

<!-- /facts -->

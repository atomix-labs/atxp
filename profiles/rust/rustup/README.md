# `rustup`

`.just/rustup.sh` installs rustup with rustup's own installer where it is
missing, with no default toolchain and without editing shell profiles, then runs
`rustup toolchain install`, which installs the toolchain `rust-toolchain.toml`
names, its components included; rustup verifies every toolchain it downloads.
mise runs it as a `preinstall` hook, before it installs any tool: the tools it
builds with cargo need the toolchain, and several builds at once would each
start to install it, over one another. `just setup` runs it again, as
`setup-rustup`, for a toolchain a bump has moved.

Cargo's bin directory, `$CARGO_HOME/bin`, joins mise's PATH, so wherever mise is
active (a shell, a task, `mise exec`, CI through mise-action) `cargo` and
`rustc` are found without a line in the shell's rc.
[`rust-toolchain`](../../rust/rust-toolchain/README.md) requires it.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                     | Part  | Policy | Notes      |
| ---------------------------------------- | ----- | ------ | ---------- |
| `.just/rustup.just`                      | whole | owned  |            |
| `.just/rustup.sh`                        | whole | owned  | executable |
| `.config/mise/conf.d/devset-rustup.toml` | whole | owned  |            |

## Recipes

- `setup-rustup`: Installs rustup where it is missing, with no toolchain of its
  own, then the toolchain rust-toolchain.toml names.

## Requires

- [`just`](../../tooling/just/README.md)
- [`mise`](../../tooling/mise/README.md)

<!-- /facts -->

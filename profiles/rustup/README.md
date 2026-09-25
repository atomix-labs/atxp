# `rustup`

`just setup` runs `setup-rustup`: it installs rustup with rustup's own installer
where it is missing, with no default toolchain and without editing shell
profiles, then runs `rustup toolchain install`, which installs the toolchain
`rust-toolchain.toml` names, its components included. rustup verifies every
toolchain it downloads.

Cargo's bin directory, `$CARGO_HOME/bin`, joins mise's PATH, so wherever mise is
active (a shell, a task, `mise exec`, CI through mise-action) `cargo` and
`rustc` are found without a line in the shell's rc.
[`rust-toolchain`](../rust-toolchain/README.md) requires it.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                     | Part  | Policy | Notes |
| ---------------------------------------- | ----- | ------ | ----- |
| `.just/rustup.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-rustup.toml` | whole | owned  |       |

## Recipes

- `setup-rustup`: Installs rustup where it is missing, with no toolchain of its
  own, then the toolchain rust-toolchain.toml names.

## Requires

- [`just`](../just/README.md)
- [`mise`](../mise/README.md)

<!-- /facts -->

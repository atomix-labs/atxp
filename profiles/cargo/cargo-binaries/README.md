# `cargo-binaries`

`package-cargo-binaries`, which `just package` runs, builds every binary of the
workspace in release mode for this machine, and archives each as
`dist/<bin>-<version>-<target>.tar.xz`, the binary at the archive's root, with a
`.sha256` beside it. mise's `github:` backend, cargo-binstall and ubi find those
names on their own. On Linux the target is musl, so the binary is static and
runs on any distribution; a crate with C code needs a musl toolchain for it, or
a pure-Rust build. `<version>` is `RELEASE_VERSION`, which
[`github-release`](../../github/github-release/README.md) sets from the tag, or
the workspace's. git ignores `dist/`, in a block of `.gitignore`.

<!-- facts: written by devset-collection -->

## Owns

| File                        | Part  | Policy | Notes      |
| --------------------------- | ----- | ------ | ---------- |
| `.just/cargo-binaries.just` | whole | owned  |            |
| `.just/cargo-binaries.sh`   | whole | owned  | executable |
| `.gitignore`                | block | owned  |            |

## Recipes

- `package-cargo-binaries`: Builds the workspace's binaries for this machine
  into dist/, each archived with its sha256.

## Requires

- [`just`](../../tooling/just/README.md)
- [`rust-toolchain`](../../rust/rust-toolchain/README.md)

<!-- /facts -->

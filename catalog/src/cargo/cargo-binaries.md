# `cargo-binaries`

A release's binaries: the workspace's, built for this machine, static on Linux,
archived with a sha256.

```sh
devset add atxp/cargo-binaries --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `cargo` · In [`rust`](../bundles/rust.md): with `binaries`

`package-cargo-binaries`, which `just package` runs, builds every binary of the
workspace in release mode for this machine, and archives each as
`dist/<bin>-<version>-<target>.tar.xz`, the binary at the archive's root, with a
`.sha256` beside it. mise's `github:` backend, cargo-binstall and ubi find those
names on their own. On Linux the target is musl, so the binary is static and
runs on any distribution; a crate with C code needs a musl toolchain for it, or
a pure-Rust build. `<version>` is `RELEASE_VERSION`, which
[`github-release`](../github/github-release.md) sets from the tag, or the
workspace's. git ignores `dist/`, in a block of `.gitignore`.

With the feature `completions`, off unless the repository turns it on, each
archive also holds `completions/`, beside the binary: what `<bin> completions
<shell>` prints for bash, zsh, fish, elvish and PowerShell, named as each shell
looks for them, `<bin>.bash`, `_<bin>`, `<bin>.fish`, `<bin>.elv` and
`_<bin>.ps1`. It is for a binary whose command line has that subcommand, as one
built with clap_complete does; each platform's archive is built on that
platform, so the binary runs where it is packaged.

## Owns

| File                        | Part  | Policy | Notes      |
| --------------------------- | ----- | ------ | ---------- |
| `.just/cargo-binaries.just` | whole | owned  | template   |
| `.just/cargo-binaries.sh`   | whole | owned  | executable |
| `.gitignore`                | block | owned  |            |

## Features

| Feature       | Default | Enables |
| ------------- | ------- | ------- |
| `completions` |         |         |

## Recipes

- `package-cargo-binaries`: Builds the workspace's binaries for this machine
  into dist/, each archived with its sha256 and its shell completions (with
  `completions`).

## Requires

- [`just`](../tooling/just.md)
- [`rust-toolchain`](../rust/rust-toolchain.md)

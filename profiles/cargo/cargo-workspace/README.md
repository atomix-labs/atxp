# `cargo-workspace`

A Cargo workspace. Where the repository has no `Cargo.toml`, it scaffolds one: a
virtual manifest with `members = ["crates/*"]`, resolver 3, and a
`[workspace.package]` every crate inherits (version, edition 2024,
`rust_version`, `description`, `license`, `authors` and `repository`), and a
first crate, `crates/<name>/`, a library with its crate docs to write. With
`kind` `bin` or `both`, a command line beside it, `crates/<name>-cli/`, whose
binary is `<name>` and which calls the library. `name` defaults to the
directory's. The scaffold is written once and is the repository's from then on;
where a `Cargo.toml` is already there, nothing is written.

Git ignores Cargo's `target/` at any depth, rustfmt's `.rs.bk` backups, and MSVC
debug files, in a block of `.gitignore`. `.cargo/config.toml` sets CPU floors
every realistic machine of each architecture meets (x86-64-v2, CRC32 on Arm, the
first Apple silicon), so a build runs wherever it is copied and a cache CI
runners share never holds an instruction another runner lacks; a build tuned to
its machine sets `RUSTFLAGS="-C target-cpu=native"`, which replaces them. Its
resolver takes, for each dependency, the newest release the workspace's
`rust-version` builds (`incompatible-rust-versions = "fallback"`), so a lock
updated by hand or by a bump never needs a newer Rust.

It owns that block and those keys; the repository's own lines, and every other
key of `.cargo/config.toml`, stay its own.

<!-- facts: written by devset-collection -->

## Owns

| File                                                 | Part  | Policy | Notes                                                       |
| ---------------------------------------------------- | ----- | ------ | ----------------------------------------------------------- |
| `Cargo.toml`                                         | whole | once   | template, scaffold `workspace`                              |
| `crates/{{ name or devset.target }}/Cargo.toml`      | whole | once   | template, scaffold `workspace`                              |
| `crates/{{ name or devset.target }}/src/lib.rs`      | whole | once   | template, scaffold `workspace`                              |
| `crates/{{ name or devset.target }}-cli/Cargo.toml`  | whole | once   | template, scaffold `workspace`, `kind` one of `bin`, `both` |
| `crates/{{ name or devset.target }}-cli/src/main.rs` | whole | once   | template, scaffold `workspace`, `kind` one of `bin`, `both` |
| `.gitignore`                                         | block | owned  |                                                             |
| `.cargo/config.toml`                                 | keys  | owned  |                                                             |

## Variables

| Variable       | Default             | Asks                                                                   |
| -------------- | ------------------- | ---------------------------------------------------------------------- |
| `name`         | empty               | The project's name, and its first crate's; empty takes the directory's |
| `kind`         | `lib`               | What the first crate builds: lib, bin or both                          |
| `description`  | empty               | One line: what the project is                                          |
| `authors`      | empty               | Authors, comma-separated                                               |
| `license`      | `MIT OR Apache-2.0` | The licence, an SPDX expression                                        |
| `repository`   | none                | The GitHub repository, owner/name                                      |
| `rust_version` | `1.98`              | The oldest Rust the workspace builds with                              |

<!-- /facts -->

#!/usr/bin/env bash
# The rule that a crate's docs speak only for itself, against a workspace whose facade's package and
# library differ, as RustCrypto's `md-5` is imported as `md5`: the core may name the facade's package,
# whose library its own name extends, and still not a crate outside its family and dependencies.
#
# Run in atxp's root, with mise and cargo.
set -euo pipefail

root=$PWD
script=$root/profiles/rust/rust-doc/files/.just/rust-doc.py
scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT
cd "$scratch"
mkdir -p crates/foo-core/src crates/foo/src crates/bar-baz/src

cat > Cargo.toml << 'TOML'
[workspace]
members  = ["crates/foo-core", "crates/foo", "crates/bar-baz"]
resolver = "3"
TOML
cat > crates/foo-core/Cargo.toml << 'TOML'
[package]
name    = "foo-core"
version = "0.1.0"
edition = "2024"
TOML
cat > crates/foo/Cargo.toml << 'TOML'
[package]
name    = "foo-rs"
version = "0.1.0"
edition = "2024"

[lib]
name = "foo"

[dependencies]
# internal
foo-core = { path = "../foo-core" }
TOML
cat > crates/bar-baz/Cargo.toml << 'TOML'
[package]
name    = "bar-baz"
version = "0.1.0"
edition = "2024"
TOML
echo '//! Counts the widgets of a list.' > crates/foo/src/lib.rs
echo '//! Counts the widgets of a list.' > crates/bar-baz/src/lib.rs

# The core names its facade by package, as a docs.rs link must: of its family, by the library.
cat > crates/foo-core/src/lib.rs << 'RUST'
//! Counts widgets, which [`foo`](https://docs.rs/foo-rs/latest/foo/) re-exports.
RUST
mise exec -- python3 -B "$script" --workspace

# A crate outside the family and the dependencies is still refused.
cat > crates/foo-core/src/lib.rs << 'RUST'
//! Counts widgets, as [`bar-baz`](https://docs.rs/bar-baz/latest/bar_baz/) does.
RUST
if said=$(mise exec -- python3 -B "$script" --workspace 2>&1); then
    echo "rust-doc: the core named bar-baz, outside its family, and drew no finding" >&2
    exit 1
fi
if ! grep -qF "names \`bar-baz\`, neither this crate nor a dependency" <<< "$said"; then
    printf 'rust-doc: want bar-baz refused, got\n%s\n' "$said" >&2
    exit 1
fi
echo "ok: a crate's docs name its family by package and by library, and nothing else"

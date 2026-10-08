#!/usr/bin/env bash
# The rule that a crate's docs speak only for itself, against a workspace whose facade's package and
# library differ, as RustCrypto's `md-5` is imported as `md5`: the core may name the facade's package,
# whose library its own name extends, and still not a crate outside its family and dependencies.
# Then `check-rust-doc` against a crate whose configuration sets a floor, as a CPU's would: an item
# only the floor builds is held to `-D warnings`, and so is a proc-macro crate beside it.
#
# Run in atxp's root, with git, mise and devset; $DEVSET, a path, runs another build of devset.
set -euo pipefail

root=$PWD
script=$root/profiles/rust/rust-doc/files/.just/rust-doc.py
devset=${DEVSET:-devset}
scratch=$(mktemp -d) work=$(mktemp -d)
trap 'rm -rf "$scratch" "$work"' EXIT
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

# The floor: a cfg that rustc and rustdoc both take, and that an item with a broken link needs. The
# check fails on the link only where the floor and `-D warnings` both reach rustdoc; RUSTDOCFLAGS
# would replace the floor, and the item would go unchecked.
mkdir -p "$work/.cargo" "$work/src"
# Locked, as CI installs; cargo tools built by cargo, as the profiles that pin them say.
export MISE_TRUSTED_CONFIG_PATHS=$work MISE_YES=1 MISE_LOCKED=1 MISE_CARGO_BINSTALL=0
cat > "$work/.cargo/config.toml" << 'TOML'
[target.'cfg(all())']
rustflags    = ["--cfg", "floor"]
rustdocflags = ["--cfg", "floor"]
TOML
cat > "$work/Cargo.toml" << 'TOML'
[package]
name    = "tiles"
version = "0.1.0"
edition = "2024"

[lints.rust]
unexpected_cfgs = { level = "warn", check-cfg = ["cfg(floor)"] }
TOML
cat > "$work/src/lib.rs" << 'RUST'
//! A grid of tiles, its wide rows only above the floor.

/// A row of tiles, as wide as a [`Board`] allows.
#[cfg(floor)]
pub struct WideRow;
RUST

git -C "$work" init -q -b main
cd "$work"
"$devset" -q --no-input add atxp/rust-doc --path "$root/profiles"
mise install -q

if said=$(mise exec -- just check-rust-doc 2>&1); then
    echo "rust-doc: WideRow's link to Board, which does not resolve, drew no error" >&2
    exit 1
fi
if ! grep -qF "unresolved link to \`Board\`" <<< "$said"; then
    printf "rust-doc: want WideRow's link to Board refused, got\n%s\n" "$said" >&2
    exit 1
fi
echo "ok: the doc check holds an item only the floor builds to -D warnings"

# A proc-macro crate, which a named target leaves without rustdocflags: its broken link fails the
# check too, once the floor's item links nothing broken.
cat > src/lib.rs << 'RUST'
//! A grid of tiles, its wide rows only above the floor.

/// A row of tiles, as wide as the board allows.
#[cfg(floor)]
pub struct WideRow;
RUST
cat >> Cargo.toml << 'TOML'

[workspace]
members = ["derive"]
TOML
mkdir -p derive/src
cat > derive/Cargo.toml << 'TOML'
[package]
name    = "tiles-derive"
version = "0.1.0"
edition = "2024"

[lib]
proc-macro = true
TOML
cat > derive/src/lib.rs << 'RUST'
//! Derives for the tiles of a grid.

/// Expands to nothing, as a [`Tile`] holds nothing.
#[proc_macro]
pub fn nothing(_: proc_macro::TokenStream) -> proc_macro::TokenStream {
    proc_macro::TokenStream::new()
}
RUST

if said=$(mise exec -- just check-rust-doc 2>&1); then
    echo "rust-doc: tiles-derive's link to Tile, which does not resolve, drew no error" >&2
    exit 1
fi
if ! grep -qF "unresolved link to \`Tile\`" <<< "$said"; then
    printf "rust-doc: want tiles-derive's link to Tile refused, got\n%s\n" "$said" >&2
    exit 1
fi
echo "ok: the doc check holds a proc-macro crate to -D warnings"

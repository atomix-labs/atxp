#!/usr/bin/env bash
# The book's check against a workspace whose configuration sets a floor, as a CPU's would: a cfg
# that rustc and rustdoc both take, and that an item needs. The item's page is in the API the book
# links into, from the recipe's build of it and from the preprocessor's. Put in RUSTDOCFLAGS, the
# recipe's flags would replace the floor's rustdocflags and break the book's link to the item.
#
# Run in atxp's root, with git, mise and devset; $DEVSET, a path, runs another build of devset.
set -euo pipefail

root=$PWD
devset=${DEVSET:-devset}
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
mkdir -p "$work/.cargo" "$work/src" "$work/docs/src"
# Locked, as CI installs; cargo tools built by cargo, as the profiles that pin them say.
export MISE_TRUSTED_CONFIG_PATHS=$work MISE_YES=1 MISE_LOCKED=1 MISE_CARGO_BINSTALL=0

cat > "$work/.cargo/config.toml" << 'EOF'
[target.'cfg(all())']
rustflags    = ["--cfg", "floor"]
rustdocflags = ["--cfg", "floor"]
EOF
cat > "$work/Cargo.toml" << 'EOF'
[package]
name    = "tiles"
version = "0.1.0"
edition = "2024"

[lints.rust]
unexpected_cfgs = { level = "warn", check-cfg = ["cfg(floor)"] }
EOF
cat > "$work/src/lib.rs" << 'EOF'
//! A grid of tiles, its wide rows only above the floor.

/// A row of tiles, as wide as the floor allows.
#[cfg(floor)]
pub struct WideRow;
EOF
cat > "$work/docs/book.toml" << 'EOF'
[book]
title = "tiles"
EOF
cat > "$work/docs/src/SUMMARY.md" << 'EOF'
# Summary

- [Rows](rows.md)
EOF
cat > "$work/docs/src/rows.md" << 'EOF'
# Rows

A [`WideRow`] holds a row of tiles.
EOF

git -C "$work" init -q -b main
cd "$work"
"$devset" -q --no-input add atxp/mdbook --path "$root/profiles" --no-default-features \
    --features api --var repository=example/tiles
mise install -q

mise exec -- just check-mdbook
if [[ ! -f docs/book/api/tiles/struct.WideRow.html ]]; then
    echo "mdbook: the API has no page for WideRow, which the floor builds and the book links" >&2
    exit 1
fi
echo "ok: the book's API keeps the floor the workspace's configuration sets"

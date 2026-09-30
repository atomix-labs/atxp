#!/usr/bin/env bash
# The manifest check against members that write a dependency in dotted form, as `cargo add` does:
# one in its groups, which draws no finding, and one with the dotted entry under the wrong group,
# which draws that finding alone.
#
# Run in atxp's root, with git, cargo and mise.
set -euo pipefail

check=$PWD/profiles/cargo/cargo-manifest/files/.just/cargo-manifest.py
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cd "$work"
git init -q -b main

cat > Cargo.toml << 'EOF'
[workspace]
members  = ["crates/*"]
resolver = "3"

[workspace.package]
version      = "0.1.0"
edition      = "2024"
rust-version = "1.98"
license      = "MIT"
authors      = ["The atxp Developers"]
publish      = false

[workspace.lints.rust]
unsafe_code = "deny"

[workspace.dependencies]
# internal
tiles-geometry.path    = "crates/geometry"
tiles-geometry.version = "0.1.0"
EOF

# A member `$1`, in `crates/$1`, whose dependency table is on stdin.
member() {
    mkdir -p "crates/$1/src"
    touch "crates/$1/src/lib.rs"
    {
        printf '[package]\nname                   = "%s"\n' "$2"
        printf 'description            = "a member of a workspace the check reads."\n'
        for key in version edition rust-version license authors publish; do
            printf '%-22s = true\n' "$key.workspace"
        done
        printf '\n[lints]\nworkspace = true\n\n[dependencies]\n'
        cat
    } > "crates/$1/Cargo.toml"
}

member geometry tiles-geometry < /dev/null
member paint tiles-paint << 'EOF'
# internal
tiles-geometry.workspace = true
tiles-geometry.features  = []
EOF
member brush tiles-brush << 'EOF'
# external
tiles-geometry.workspace = true
EOF
git add -A

# The member in its groups draws nothing.
mise exec -- python3 -B "$check" crates/paint/Cargo.toml > /dev/null

# The member with its internal entry under `# external` draws that finding, and no other.
if said=$(mise exec -- python3 -B "$check" crates/brush/Cargo.toml); then
    echo "cargo-manifest: a dotted internal entry under # external drew no finding" >&2
    exit 1
fi
expected="crates/brush/Cargo.toml:16  group: \`tiles-geometry\` is internal, under \`# external\`"
if [[ $(grep -c . <<< "$said") != 2 || $(head -1 <<< "$said") != "$expected" ]]; then
    printf 'cargo-manifest: want only\n  %s\ngot\n%s\n' "$expected" "$said" >&2
    exit 1
fi

# A dotted internal entry that pins a version draws that finding.
member stroke tiles-stroke << 'EOF'
# internal
tiles-geometry.version = "0.1.0"
EOF
git add -A
if said=$(mise exec -- python3 -B "$check" crates/stroke/Cargo.toml) || ! grep -q "\`tiles-geometry\` pins a version" <<< "$said"; then
    printf 'cargo-manifest: a dotted entry that pins a version drew\n%s\n' "$said" >&2
    exit 1
fi

# `--fix` moves the dotted entry to its group, and the check then passes.
mise exec -- python3 -B "$check" --fix crates/brush/Cargo.toml > /dev/null
mise exec -- python3 -B "$check" crates/brush/Cargo.toml > /dev/null
echo "ok: the manifest check reads a dependency written in dotted form"

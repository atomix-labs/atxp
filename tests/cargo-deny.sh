#!/usr/bin/env bash
# The dependency check against a crate whose optional dependency, which no default feature turns on,
# carries a licence the policy refuses: the check fails on it, and passes once the repository allows
# that licence for that crate alone, in an exception of its own, which devset leaves in place.
#
# Run in atxp's root, with git, mise and devset; $DEVSET, a path, runs another build of devset.
set -euo pipefail

root=$PWD
devset=${DEVSET:-devset}
scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT
work=$scratch/project
mkdir -p "$work/src" "$scratch/copyleft/src"
# Locked, as CI installs; cargo tools built by cargo, as the profiles that pin them say.
export MISE_TRUSTED_CONFIG_PATHS=$work MISE_YES=1 MISE_LOCKED=1 MISE_CARGO_BINSTALL=0

# The optional dependency, outside the workspace, so that it is no member.
cat > "$scratch/copyleft/Cargo.toml" << 'EOF'
[package]
name    = "copyleft"
version = "0.1.0"
edition = "2024"
license = "GPL-3.0-only"
EOF
touch "$scratch/copyleft/src/lib.rs"

cat > "$work/Cargo.toml" << 'EOF'
[package]
name    = "project"
version = "0.1.0"
edition = "2024"
license = "MIT"
publish = false

[features]
copyleft = ["dep:copyleft"]

[dependencies]
copyleft = { path = "../copyleft", version = "0.1.0", optional = true }
EOF
touch "$work/src/lib.rs"

git -C "$work" init -q -b main
cd "$work"
"$devset" -q --no-input add atxp/cargo-deny --path "$root/profiles"
mise install -q

# The licence of a dependency only a feature brings draws the finding.
if said=$(mise exec -- just check-cargo-deny 2>&1); then
    echo "cargo-deny: the optional dependency's GPL-3.0-only drew no finding" >&2
    exit 1
fi
if ! grep -q "rejected: license is not explicitly allowed" <<< "$said" || ! grep -q "GPL-3.0-only" <<< "$said"; then
    printf "cargo-deny: want the optional dependency's GPL-3.0-only rejected, got\n%s\n" "$said" >&2
    exit 1
fi

# An exception for that crate, a key of the repository's own, is no drift, and the check passes.
sed -i '/^unused-allowed-license/a exceptions = [{ crate = "copyleft", allow = ["GPL-3.0-only"] }]' deny.toml
"$devset" status --exit-code > /dev/null
mise exec -- just check-cargo-deny
echo "ok: the dependency check holds an optional dependency to deny.toml"

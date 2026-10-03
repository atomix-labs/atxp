#!/usr/bin/env bash
# The rust bundle from nothing: applied, with the features given, to an empty repository, then set
# up and checked as a new project is, `./setup.sh --yes && just check`.
#
# Usage: tests/bundle.sh [<feature>,...]
#
# Run in atxp's root, with git, mise and devset; $DEVSET, a path, runs another build of devset.
set -euo pipefail

root=$PWD
devset=${DEVSET:-devset}
features=${1:-}
scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT
# The project takes its directory's name, in its book, its AGENTS.md and its licence: a fixed one,
# since a random one can hold what typos reads as a misspelling.
work=$scratch/project
mkdir "$work"
# Locked, as CI installs; cargo tools built by cargo, as the profiles that pin them say.
export MISE_TRUSTED_CONFIG_PATHS=$work MISE_YES=1 MISE_LOCKED=1 MISE_CARGO_BINSTALL=0

git -C "$work" init -q -b main
flags=(--var repository=example/project --var name=project)
[[ -z $features ]] || flags+=(--features "$features")
(cd "$work" && "$devset" -q --no-input add atxp/rust --path "$root/profiles" "${flags[@]}")
# A crate crates.io publishes carries what its page there shows, which only its owner can write and
# check-cargo-publish names until it is there: here, a stand-in for each.
if [[ ,$features, == *,publish,* ]]; then
    crate=$work/crates/project
    sed -i '/^repository.workspace/r /dev/stdin' "$crate/Cargo.toml" << 'EOF'
homepage               = "https://example.github.io/project/"
keywords               = ["example"]
categories             = ["development-tools"]
EOF
    cat > "$crate/README.md" << 'EOF'
# `project`

The crate the rust bundle starts a project with.
EOF
    for licence in LICENSE-MIT LICENSE-APACHE; do ln -s "../../$licence" "$crate/$licence"; done
fi
(cd "$work" && "$devset" status --exit-code > /dev/null && ./setup.sh --yes && mise exec -- just check)
echo "ok: rust${features:+ with $features}, from nothing"

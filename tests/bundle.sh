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
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
# Locked, as CI installs; cargo tools built by cargo, as the profiles that pin them say.
export MISE_TRUSTED_CONFIG_PATHS=$work MISE_YES=1 MISE_LOCKED=1 MISE_CARGO_BINSTALL=0

git -C "$work" init -q -b main
flags=(--var repository=example/project --var name=project)
[[ -z $features ]] || flags+=(--features "$features")
(cd "$work" && "$devset" -q --no-input init atxp/rust --path "$root/profiles" "${flags[@]}")
(cd "$work" && "$devset" status --exit-code > /dev/null && ./setup.sh --yes && mise exec -- just check)
echo "ok: rust${features:+ with $features}, from nothing"

#!/usr/bin/env bash
# Applies every bundle to every fixture and runs `just check` there with the tools the atoms pin;
# applies every atom alone, then all at once; and runs the setup stub against a repository served
# locally.
#
# Needs devset, or its path in $DEVSET, git, cargo, mise and python3 of 3.11 or later.
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
devset=${DEVSET:-devset}
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
# Locked, as CI installs; cargo tools built by cargo, as the atoms that pin them say.
export MISE_TRUSTED_CONFIG_PATHS=$work MISE_YES=1 MISE_LOCKED=1 MISE_CARGO_BINSTALL=0

# The flags answering every variable that a profile, or one it requires, declares without a
# default: each gets the suite's own answer.
answers() {
    python3 - "$root/profiles/$1" << 'PY'
import sys
import tomllib
from pathlib import Path

seen, flags = set(), []


def visit(directory):
    directory = directory.resolve()
    if directory in seen:
        return
    seen.add(directory)
    manifest = tomllib.loads((directory / "profile.toml").read_text())
    for name, spec in manifest.get("vars", {}).items():
        if "default" not in spec:
            flags.append(f"--var={name}=example/fixture")
    for required in manifest["profile"].get("requires", []):
        visit(directory / required)


visit(Path(sys.argv[1]))
print(" ".join(flags))
PY
}

# Applies each profile named, in order, to the directory `$1`.
apply() {
    local dir=$1 flags
    shift
    for profile in "$@"; do
        read -ra flags <<< "$(answers "$profile")"
        (cd "$dir" && "$devset" -q --no-input init --path "$root/profiles/$profile" "${flags[@]}")
    done
}

bundles=() atoms=()
for manifest in "$root"/profiles/*/profile.toml; do
    id=$(basename "$(dirname "$manifest")")
    if grep -q '^\[files\.' "$manifest"; then atoms+=("$id"); else bundles+=("$id"); fi
done

for fixture in "$root"/tests/fixtures/*/; do
    for bundle in "${bundles[@]}"; do
        dir=$work/$bundle-$(basename "$fixture")
        cp -R "$fixture" "$dir"
        git -C "$dir" init -q
        apply "$dir" "$bundle"
        (cd "$dir" && "$devset" status --exit-code > /dev/null && mise install -q && mise exec -- just check)
        echo "ok: $bundle on $(basename "$fixture")"
    done
done

for atom in "${atoms[@]}"; do
    mkdir "$work/$atom"
    apply "$work/$atom" "$atom"
    (cd "$work/$atom" && "$devset" status --exit-code > /dev/null)
done
echo "ok: every atom applies alone"

# Every atom at once, on the workspace: every payload passes the checks every atom brings, and no
# two atoms collide.
dir=$work/every-atom
cp -R "$root/tests/fixtures/workspace" "$dir"
git -C "$dir" init -q
apply "$dir" "${atoms[@]}"
(cd "$dir" && "$devset" status --exit-code > /dev/null && mise install -q && mise exec -- just check)
echo "ok: every atom at once"

# The setup stub against a repository served from a local bare copy: from a machine without mise,
# again over its clone, from inside with --host, over another repository's directory, as a dry
# run, and with each form of clone URL.
stub=$root/profiles/setup/files/setup.sh
setup=$work/stub
mkdir -p "$setup/home"
cp -R "$root/tests/fixtures/crate" "$setup/src"
git -C "$setup/src" init -q -b main
apply "$setup/src" rust
printf '\nhost-probe:\n    touch host-ran\n' >> "$setup/src/justfile"
git -C "$setup/src" add -A
git -C "$setup/src" -c user.name=suite -c user.email=suite@example.com commit -qm fixture
git clone -q --bare "$setup/src" "$setup/repo.git"
url=file://$setup/repo.git
# A machine without mise: a clean HOME and a PATH without it. The tools and toolchains already
# installed are shared, so nothing is built twice.
data=${MISE_DATA_DIR:-$HOME/.local/share/mise}
cargo=${CARGO_HOME:-$HOME/.cargo} rustup=${RUSTUP_HOME:-$HOME/.rustup}
(cd "$setup" && env HOME="$setup/home" PATH=/usr/bin:/bin MISE_DATA_DIR="$data" \
    CARGO_HOME="$cargo" RUSTUP_HOME="$rustup" bash "$stub" "$url" --yes)
[[ -x $setup/home/.local/bin/mise && -f $setup/repo/rust-toolchain.toml ]]
[[ -x $setup/repo/setup.sh ]]
(cd "$setup" && bash "$stub" "$url" --yes)
(cd "$setup/repo" && bash "$stub" --yes --host)
[[ -f $setup/repo/host-ran ]]
mkdir "$setup/other"
git -C "$setup/other" init -q
git -C "$setup/other" remote add origin https://example.com/other.git
if (cd "$setup" && bash "$stub" "$url" --dir other --yes) > /dev/null 2>&1; then
    echo "setup cloned over another repository's directory" >&2
    exit 1
fi
(cd "$setup" && bash "$stub" "$url" --dir dry --dry-run) > /dev/null 2>&1
[[ ! -e $setup/dry ]]
while read -r protocol repo want; do
    got=$(cd "$setup" && SETUP_PROTOCOL=$protocol bash "$stub" "$repo" --dry-run 2>&1) || true
    grep -qF "would clone $want" <<< "$got" || { echo "setup: $repo over $protocol is not $want" >&2; exit 1; }
done << 'EOF'
ssh github.com/owner/name git@github.com:owner/name.git
ssh example.ghe.com/owner/name example@example.ghe.com:owner/name.git
https example.ghe.com/owner/name https://example.ghe.com/owner/name.git
EOF
echo "ok: setup"

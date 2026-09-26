#!/usr/bin/env bash
# The setup stub against a repository the bundle is applied to, served from a local bare copy: from
# a machine without mise, again over its clone, from inside with --host, over another repository's
# directory, as a dry run, and with each form of clone URL.
#
# Run in atxp's root, with git, mise and devset; $DEVSET, a path, runs another build of devset.
set -euo pipefail

root=$PWD
devset=${DEVSET:-devset}
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
# Locked, as CI installs; cargo tools built by cargo, as the profiles that pin them say.
export MISE_TRUSTED_CONFIG_PATHS=$work MISE_YES=1 MISE_LOCKED=1 MISE_CARGO_BINSTALL=0

stub=$root/profiles/tooling/setup/files/setup.sh
mkdir -p "$work/home"
cp -R "$root/tests/fixtures/crate" "$work/src"
git -C "$work/src" init -q -b main
(cd "$work/src" && "$devset" -q --no-input init atxp/rust --path "$root/profiles" \
    --var repository=example/fixture)
printf '\nhost-probe:\n    touch host-ran\n' >> "$work/src/justfile"
git -C "$work/src" add -A
git -C "$work/src" -c user.name=suite -c user.email=suite@example.com commit -qm fixture
git clone -q --bare "$work/src" "$work/repo.git"
url=file://$work/repo.git

# A machine without mise: a clean HOME and a PATH without it. The tools and toolchains already
# installed are shared, so nothing is built twice.
data=${MISE_DATA_DIR:-$HOME/.local/share/mise}
cargo=${CARGO_HOME:-$HOME/.cargo} rustup=${RUSTUP_HOME:-$HOME/.rustup}
(cd "$work" && env HOME="$work/home" PATH=/usr/bin:/bin MISE_DATA_DIR="$data" \
    CARGO_HOME="$cargo" RUSTUP_HOME="$rustup" bash "$stub" "$url" --yes)
[[ -x $work/home/.local/bin/mise && -f $work/repo/rust-toolchain.toml ]]
[[ -x $work/repo/setup.sh ]]
(cd "$work" && bash "$stub" "$url" --yes)
(cd "$work/repo" && bash "$stub" --yes --host)
[[ -f $work/repo/host-ran ]]

mkdir "$work/other"
git -C "$work/other" init -q
git -C "$work/other" remote add origin https://example.com/other.git
if (cd "$work" && bash "$stub" "$url" --dir other --yes) > /dev/null 2>&1; then
    echo "setup cloned over another repository's directory" >&2
    exit 1
fi
(cd "$work" && bash "$stub" "$url" --dir dry --dry-run) > /dev/null 2>&1
[[ ! -e $work/dry ]]

while read -r protocol repo want; do
    got=$(cd "$work" && SETUP_PROTOCOL=$protocol bash "$stub" "$repo" --dry-run 2>&1) || true
    grep -qF "would clone $want" <<< "$got" || {
        echo "setup: $repo over $protocol is not $want" >&2
        exit 1
    }
done << 'EOF'
ssh github.com/owner/name git@github.com:owner/name.git
ssh example.ghe.com/owner/name example@example.ghe.com:owner/name.git
https example.ghe.com/owner/name https://example.ghe.com/owner/name.git
EOF
echo "ok: setup"

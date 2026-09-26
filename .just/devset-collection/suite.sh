#!/usr/bin/env bash
# The collection's suite. Every profile alone, on an empty directory, with its default features and
# with every feature: it applies, and nothing drifts. Then on each fixture in tests/fixtures/, or on
# an empty directory where there is none: each bundle, a profile that owns no file, with no
# features, and every profile at once, with every feature: each applies, nothing drifts, and
# `just check` passes there with the tools the profiles pin.
#
# Run in the collection's root, with git, mise, Python and devset; $DEVSET, a path, runs another
# build of devset.
set -euo pipefail

root=$PWD
devset=${DEVSET:-devset}
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
# Locked, as CI installs; cargo tools built by cargo, as the profiles that pin them say.
export MISE_TRUSTED_CONFIG_PATHS=$work MISE_YES=1 MISE_LOCKED=1 MISE_CARGO_BINSTALL=0

# One line per profile, `|` between its fields: its name; `bundle` or `profile`; the flag turning
# on its every feature, if it has any; and the flags answering every variable it, or a profile it
# requires, declares without a default, each with the suite's own answer.
listing=$(python3 - "$(dirname "$0")" << 'PY'
import sys

sys.path.insert(0, sys.argv[1])
from catalog import by_name, profiles

found = profiles()
named = by_name(found)


def answers(profile, seen):
    """Flags answering each variable `profile` or a requirement declares without a default."""
    if profile.name in seen:
        return []
    seen.add(profile.name)
    declared = profile.manifest.get("vars", {})
    unanswered = [name for name, spec in declared.items() if "default" not in spec]
    flags = [f"--var={name}=example/fixture" for name in unanswered]
    for required in profile.requires:
        for other in named.get(required, []):
            flags += answers(other, seen)
    return flags


for profile in found:
    kind = "profile" if profile.files else "bundle"
    every = f"--features={','.join(profile.features)}" if profile.features else ""
    print("|".join([profile.name, kind, every, " ".join(answers(profile, set()))]))
PY
)

names=() bundles=()
declare -A every answers
while IFS='|' read -r name kind features flags; do
    names+=("$name")
    [[ $kind == bundle ]] && bundles+=("$name")
    every[$name]=$features answers[$name]=$flags
done <<< "$listing"

# Adds the profile `$2` to the target in `$1`, starting the target where there is none, with the
# flags after them.
add() {
    local dir=$1 name=$2 flags
    shift 2
    read -ra flags <<< "${answers[$name]}"
    if [[ -f $dir/.devset/config.toml ]]; then
        set -- add "suite/$name" "${flags[@]}" "$@"
    else
        set -- init "suite/$name" --path "$root/profiles" "${flags[@]}" "$@"
    fi
    (cd "$dir" && "$devset" -q --no-input "$@")
}

# Checks the target in `$1`: nothing drifts, and `just check` passes with the tools it pins.
checked() (
    cd "$1"
    "$devset" status --exit-code > /dev/null
    mise install -q
    mise exec -- just check
)

for name in "${names[@]}"; do
    mkdir "$work/$name"
    add "$work/$name" "$name"
    (cd "$work/$name" && "$devset" status --exit-code > /dev/null)
    if [[ -n ${every[$name]} ]]; then
        mkdir "$work/$name-every"
        add "$work/$name-every" "$name" "${every[$name]}"
        (cd "$work/$name-every" && "$devset" status --exit-code > /dev/null)
    fi
done
echo "ok: every profile alone, with its default features and with every feature"

fixtures=("$root"/tests/fixtures/*/)
if [[ ! -d ${fixtures[0]} ]]; then
    mkdir "$work/empty"
    fixtures=("$work/empty/")
fi
for path in "${fixtures[@]}"; do
    fixture=$(basename "$path")
    for bundle in "${bundles[@]}"; do
        dir=$work/$bundle-on-$fixture
        cp -R "$path" "$dir"
        git -C "$dir" init -q
        add "$dir" "$bundle" --no-default-features
        checked "$dir"
        echo "ok: $bundle on $fixture, with no features"
    done
    dir=$work/every-profile-on-$fixture
    cp -R "$path" "$dir"
    git -C "$dir" init -q
    for name in "${names[@]}"; do
        read -ra flags <<< "${every[$name]}"
        add "$dir" "$name" "${flags[@]}"
    done
    checked "$dir"
    echo "ok: every profile on $fixture, with every feature"
done

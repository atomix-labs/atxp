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
# on its every feature, if it has any; then, for each way the suite applies it (with its default
# features, with every feature, with none), the flags answering each variable a profile it makes
# active declares without a default, with the suite's own answer.
listing=$(python3 -B - "$(dirname "$0")" << 'PY'
import sys
from collections import defaultdict

sys.path.insert(0, sys.argv[1])
from catalog import by_name, profiles

found = profiles()
named = by_name(found)


def active(name, features, defaults):
    """The profiles active when `name` is applied with `features`, and with its default features
    where `defaults`: what each requires, and the optional requirements its features turn on."""
    wanted = {name: (set(features), defaults)}
    pending = [name]
    while pending:
        profile = named[pending.pop()][0]
        on, defaults = wanted[profile.name]
        declared = profile.manifest.get("features", {})
        queue = list(on) + (declared.get("default", []) if defaults else [])
        turned, deps, weak, forwarded = set(), set(), [], defaultdict(set)
        while queue:
            entry = queue.pop()
            if entry.startswith("dep:"):
                deps.add(entry.removeprefix("dep:"))
            elif "?/" in entry:
                weak.append(entry.split("?/", 1))
            elif "/" in entry:
                dep, feature = entry.split("/", 1)
                deps.add(dep)
                forwarded[dep].add(feature)
            elif entry not in turned:
                turned.add(entry)
                queue += declared.get(entry, [])
        required = {r for r, spec in profile.requires.items() if not spec.get("optional")}
        required |= deps & profile.requires.keys()
        for dep, feature in weak:
            if dep in required:
                forwarded[dep].add(feature)
        for dep in required:
            spec = profile.requires[dep]
            # A profile of another source lends the suite no variables to answer.
            if "git" in spec or dep not in named:
                continue
            features = set(spec.get("features", [])) | forwarded[dep]
            defaults = spec.get("default-features", True)
            had = wanted.get(dep)
            now = (features | (had[0] if had else set()), defaults or bool(had and had[1]))
            if now != had:
                wanted[dep] = now
                pending.append(dep)
    return wanted


def answers(name, features, defaults):
    """The flags answering the variables the profiles active this way declare without a default."""
    unanswered = sorted(
        var
        for active_name in active(name, features, defaults)
        for var, spec in named[active_name][0].manifest.get("vars", {}).items()
        if "default" not in spec
    )
    return " ".join(f"--var={var}=example/fixture" for var in dict.fromkeys(unanswered))


for profile in found:
    kind = "profile" if profile.files else "bundle"
    every = f"--features={','.join(profile.features)}" if profile.features else ""
    ways = [([], True), (list(profile.features), True), ([], False)]
    print("|".join([profile.name, kind, every, *(answers(profile.name, *way) for way in ways)]))
PY
)

names=() bundles=()
declare -A every answers
while IFS='|' read -r name kind features plain all bare; do
    [[ -n $name ]] || continue
    names+=("$name")
    [[ $kind == bundle ]] && bundles+=("$name")
    every[$name]=$features
    answers[plain:$name]=$plain answers[every:$name]=$all answers[bare:$name]=$bare
done <<< "$listing"
if ((${#names[@]} == 0)); then
    echo "ok: no profiles to test"
    exit 0
fi

# Adds the profile `$2` to the target in `$1`, starting the target where there is none, applied
# the way `$3` names (`plain`, `every` or `bare`), with the flags after them.
add() {
    local dir=$1 name=$2 way=$3 flags
    shift 3
    read -ra flags <<< "${answers[$way:$name]}"
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
    add "$work/$name" "$name" plain
    (cd "$work/$name" && "$devset" status --exit-code > /dev/null)
    if [[ -n ${every[$name]} ]]; then
        mkdir "$work/$name-every"
        add "$work/$name-every" "$name" every "${every[$name]}"
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
        add "$dir" "$bundle" bare --no-default-features
        checked "$dir"
        echo "ok: $bundle on $fixture, with no features"
    done
    dir=$work/every-profile-on-$fixture
    cp -R "$path" "$dir"
    git -C "$dir" init -q
    for name in "${names[@]}"; do
        read -ra flags <<< "${every[$name]}"
        add "$dir" "$name" every "${flags[@]}"
    done
    checked "$dir"
    echo "ok: every profile on $fixture, with every feature"
done

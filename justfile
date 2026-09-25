# atxp's own recipes; the block below them is the `just` profile's.

# profiles/*/files/ holds payloads, not configuration for the directories they are in.
export DPRINT_CONFIG_DISCOVERY := "ignore-descendants"

# Checks the catalog, every profile's facts and the spine's imports are current, and every profile
# keeps the rules.
check-catalog:
    mise exec -- python3 scripts/catalog.py --check

# Writes the catalog, every profile's facts and the spine's imports.
fix-catalog:
    mise exec -- python3 scripts/catalog.py

# Checks the setup stub, the mise profile and every workflow run one mise, and the stub's checksums
# are the release's own.
check-mise-version:
    mise exec -- python3 scripts/mise-version.py check

# Moves them all to mise's newest release past the cooldown.
bump-mise-version:
    mise exec -- python3 scripts/mise-version.py bump "${BUMP_REPORT_DIR:+$BUMP_REPORT_DIR/mise-version.md}"

# Moves the pinned nightly to the newest of the last two weeks with every component everywhere.
bump-rust-toolchain:
    mise exec -- python3 scripts/rust-toolchain.py profiles/rust-toolchain/files/rust-toolchain.toml "${BUMP_REPORT_DIR:+$BUMP_REPORT_DIR/rust-toolchain.md}"

# Tests the workflow policies against their own cases.
check-policies:
    mise exec -- conftest verify --policy profiles/policies/files/policy

# After a bump moves the profiles' pins, applies the profiles to this repository again, with the
# devset mise pins.
bump-self:
    mise exec -- devset apply

# Builds the site Pages serves, the setup stub at /setup.sh, and checks that the stub parses.
check-site:
    #!/usr/bin/env bash
    set -euo pipefail
    rm -rf site
    mkdir site
    cp profiles/setup/files/setup.sh site/setup.sh
    bash -n site/setup.sh

# Points the README's quick start at v$RELEASE_VERSION.
release-readme:
    #!/usr/bin/env bash
    set -euo pipefail
    : "${RELEASE_VERSION:?set it: RELEASE_VERSION=x.y.z just release}"
    sed -i.bak -E "s/--tag v[0-9]+\.[0-9]+\.[0-9]+/--tag v$RELEASE_VERSION/" README.md
    rm README.md.bak

# Applies the bundle to every fixture and runs its checks, every profile alone and all at once.
test-profiles:
    mise exec -- tests/run.sh

# >>> devset: just >>>
# Each atom's recipes, where the atom is applied.
import? '.just/actionlint.just'
import? '.just/ansible-lint.just'
import? '.just/cargo-binaries.just'
import? '.just/cargo-bump.just'
import? '.just/cargo-deny.just'
import? '.just/cargo-hack.just'
import? '.just/cargo-machete.just'
import? '.just/cargo-shear.just'
import? '.just/cargo-workspace-lints.just'
import? '.just/clippy.just'
import? '.just/committed.just'
import? '.just/conftest.just'
import? '.just/dprint.just'
import? '.just/git-cliff.just'
import? '.just/lints-nightly.just'
import? '.just/lychee.just'
import? '.just/manifest-lint.just'
import? '.just/mdbook.just'
import? '.just/mise.just'
import? '.just/msrv.just'
import? '.just/nextest.just'
import? '.just/profile-pins.just'
import? '.just/ruff.just'
import? '.just/rumdl.just'
import? '.just/rust-toolchain.just'
import? '.just/rustdoc.just'
import? '.just/rustfmt.just'
import? '.just/rustup.just'
import? '.just/shellcheck.just'
import? '.just/suppressions.just'
import? '.just/taplo.just'
import? '.just/typos.just'
import? '.just/yamllint.just'
import? '.just/zizmor.just'

# Runs every `check-*` recipe, as CI does, and names each that fails.
check: (_each "check")

# Runs every `fix-*` recipe.
fix: (_each "fix")

# Runs every `bump-*` recipe: each moves what its atom pins, and reports to $BUMP_REPORT_DIR.
bump: (_each "bump")

# Runs every `nightly-*` recipe: the checks too slow for every change.
nightly: (_each "nightly")

# Runs every `setup-*` recipe: what a checkout needs before it builds. `mise bootstrap` runs it.
setup: (_each "setup")

# Runs every `host-*` recipe: the machine's own setup, whose steps may ask for sudo.
host: (_each "host")

# Runs every `release-*` recipe for $RELEASE_VERSION: each writes what a release needs.
release: (_each "release")

# Runs every `package-*` recipe: what a release ships, built for this machine into dist/.
package: (_each "package")

# Runs every recipe named `<verb>-*`, and names each that fails.
_each verb:
    #!/usr/bin/env bash
    set -uo pipefail
    failed=()
    for recipe in $(just --justfile '{{ justfile() }}' --summary); do
        [[ $recipe == {{ verb }}-* ]] || continue
        just --justfile '{{ justfile() }}' "$recipe" || failed+=("$recipe")
    done
    if (( ${#failed[@]} )); then
        echo "failed: ${failed[*]}" >&2
        exit 1
    fi
# <<< devset: just <<<

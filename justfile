# The house's own recipes; the block below them is the collection's `just` atom's.

# profiles/dprint-house/files/dprint.json is a payload, not a config for the directory it is in.
export DPRINT_CONFIG_DISCOVERY := "ignore-descendants"

# Moves the house's nightly to the newest of the last two weeks with every component everywhere.
bump-rust-nightly:
    mise exec -- python3 scripts/rust-nightly.py profiles/rust-nightly/files/rust-toolchain.toml "${BUMP_REPORT_DIR:+$BUMP_REPORT_DIR/rust.md}"

# Tests the house's policies against their own cases.
check-policies:
    mise exec -- conftest verify --policy profiles/policies-house/files/policy

# >>> devset: just >>>
# Each atom's recipes, where the atom is applied.
import? '.just/actionlint.just'
import? '.just/cargo-deny.just'
import? '.just/cargo-hack.just'
import? '.just/cargo-machete.just'
import? '.just/cargo-shear.just'
import? '.just/cargo-workspace-lints.just'
import? '.just/clippy.just'
import? '.just/conftest.just'
import? '.just/dprint.just'
import? '.just/lychee.just'
import? '.just/mdbook.just'
import? '.just/mise.just'
import? '.just/nextest.just'
import? '.just/profile-pins.just'
import? '.just/ruff.just'
import? '.just/rumdl.just'
import? '.just/rustdoc.just'
import? '.just/rustfmt.just'
import? '.just/rustup.just'
import? '.just/shellcheck.just'
import? '.just/taplo.just'
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

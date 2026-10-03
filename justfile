# atxp's own recipes; the block below them is the `just` profile's.

# Checks the setup stub, the mise profile and every workflow run one mise, the release's own.
check-mise-version:
    mise exec -- python3 scripts/mise-version.py check

# Moves them all to mise's newest release past the cooldown.
bump-mise-version:
    mise exec -- python3 scripts/mise-version.py bump "${BUMP_REPORT_DIR:+$BUMP_REPORT_DIR/mise-version.md}"

# Moves the pinned nightly to the newest of the last two weeks with every component everywhere.
bump-rust-toolchain:
    mise exec -- python3 scripts/rust-toolchain.py profiles/rust/rust-toolchain/files/rust-toolchain.toml "${BUMP_REPORT_DIR:+$BUMP_REPORT_DIR/rust-toolchain.md}"

# Tests the workflow policies against their own cases.
check-policies:
    mise exec -- conftest verify --policy profiles/github/github-workflow-lint/files/policy

# Applies the profiles to this repository again, with the pins a bump moved.
bump-self:
    mise exec -- devset apply

# Builds the site Pages serves: the catalog, and the setup stub at /setup.sh, which it checks parses.
check-site:
    #!/usr/bin/env bash
    set -euo pipefail
    rm -rf site
    mise exec -- mdbook build catalog --dest-dir site
    cp profiles/tooling/setup/files/setup.sh site/setup.sh
    bash -n site/setup.sh

# Checks the catalog's palette is the book's: the one file mdbook and devset-collection both ship.
check-palette:
    #!/usr/bin/env bash
    set -euo pipefail
    cmp profiles/docs/mdbook/files/*/theme/palette.css profiles/devset/devset-collection/files/catalog/theme/palette.css

# Checks Dependabot's profile leaves alone every workflow a profile writes: each in its list.
check-dependabot-paths:
    #!/usr/bin/env bash
    set -euo pipefail
    template=profiles/github/github-dependabot/files/.github/dependabot.yml
    missing=0
    for file in profiles/*/*/files/.github/workflows/*.yml; do
        profile=$(cut -d/ -f3 <<< "$file")
        path=${file#*/files/}
        if ! grep -qF "[\"$path\", \"$profile\"]" "$template"; then
            echo "$template: no [\"$path\", \"$profile\"] among the workflows devset writes" >&2
            missing=1
        fi
    done
    exit "$missing"

# Points the README's quick start, and the demo the release records, at v$RELEASE_VERSION.
release-readme:
    #!/usr/bin/env bash
    set -euo pipefail
    : "${RELEASE_VERSION:?set it: RELEASE_VERSION=x.y.z just release}"
    for file in README.md docs/demo/parts/demo.tape; do
        sed -i.bak -E "s/(--tag |tag = \")v[0-9]+\.[0-9]+\.[0-9]+/\1v$RELEASE_VERSION/g" "$file"
        rm "$file.bak"
    done

# Tests the setup stub against a repository the bundle is applied to, served from a local copy.
test-setup-stub:
    mise exec -- bash tests/setup-stub.sh

# Tests the agents profile's hooks through the turns they tell apart.
test-agents-hook:
    mise exec -- bash tests/agents-hook.sh

# Tests the catalog check's skill form against skills that break it.
test-skill-form:
    mise exec -- bash tests/skill-form.sh

# Tests the manifest check against members that write a dependency in dotted form.
test-cargo-manifest:
    mise exec -- bash tests/cargo-manifest.sh

# Compiles every Rust example the skills show under the strict lints, each as its block says; with
# skills named, only theirs.
test-skill-examples *skills:
    mise exec -- python3 -B tests/skill_examples.py {{ skills }}

# The nightly takes each feature alone.

# Applies the rust bundle to an empty repository, with no features and with all, then checks it.
test-bundle:
    mise exec -- bash tests/bundle.sh
    mise exec -- bash tests/bundle.sh docs,agents,publish,binaries,oss,nightly,strict

# >>> devset: just >>>
# Each active profile's recipes.
import? '.just/agents.just'
import? '.just/devset.just'
import? '.just/devset-collection.just'
import? '.just/dprint.just'
import? '.just/editorconfig.just'
import? '.just/git-attributes.just'
import? '.just/git-changelog.just'
import? '.just/git-commits.just'
import? '.just/git-ignore.just'
import? '.just/github-automation.just'
import? '.just/github-bump.just'
import? '.just/github-ci.just'
import? '.just/github-dependabot.just'
import? '.just/github-labels.just'
import? '.just/github-release.just'
import? '.just/github-watch.just'
import? '.just/github-workflow-lint.just'
import? '.just/just.just'
import? '.just/markdown.just'
import? '.just/mdbook-tool.just'
import? '.just/mise.just'
import? '.just/project.just'
import? '.just/python.just'
import? '.just/setup.just'
import? '.just/shell.just'
import? '.just/spelling.just'
import? '.just/suppressions.just'
import? '.just/toml.just'
import? '.just/vhs.just'
import? '.just/yaml.just'

# Runs every `check-*` recipe, as CI does, and names each that fails.
check: (_each "check")

# Runs every `fix-*` recipe.
fix: (_each "fix")

# Runs every `bump-*` recipe: each moves what its profile pins, and reports to $BUMP_REPORT_DIR.
bump: (_each "bump")

# Runs every `nightly-*` recipe: the checks too slow for every change.
nightly: (_each "nightly")

# Runs every `test-*` recipe: the suites too slow for `just check`, which CI runs beside it.
test: (_each "test")

# Runs every `setup-*` recipe: what a checkout needs before it builds. `mise bootstrap` runs it.
setup: (_each "setup")

# Runs every `host-*` recipe: the machine's own setup, whose steps may ask for sudo.
host: (_each "host")

# Runs every `release-*` recipe for $RELEASE_VERSION: each writes what a release needs.
release: (_each "release")

# Runs every `package-*` recipe: what a release ships, built for this machine into dist/.
package: (_each "package")

# Runs every `publish-*` recipe: what a release puts in a registry, once the release is out.
publish: (_each "publish")

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

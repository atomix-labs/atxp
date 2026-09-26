# Checks every workflow by each tool the profile's features turn on: actionlint, for syntax,
# expressions and the shell in each step; zizmor's audit, offline, needing no token; conftest,
# holding workflows and actions to the policies in policy/. A file .gitattributes marks
# `linguist-vendored` or `linguist-generated` is someone else's.
check-github-workflow-lint:
    #!/usr/bin/env bash
    set -euo pipefail
    # The files the repository owns among those `$@` names.
    owned() {
        git ls-files -z --cached --others --exclude-standard -- "$@" \
            ':(exclude,attr:linguist-vendored)' ':(exclude,attr:linguist-vendored=true)' \
            ':(exclude,attr:linguist-generated)' ':(exclude,attr:linguist-generated=true)'
    }
    echo "actionlint" >&2
    actionlint
    inputs=()
    while IFS= read -r -d '' file; do [[ -f $file ]] && inputs+=("$file"); done \
        < <(owned '.github/workflows/*.yml' '.github/workflows/*.yaml' '.github/dependabot.yml' \
            '.github/dependabot.yaml' ':(glob)**/action.yml' ':(glob)**/action.yaml')
    if (( ${#inputs[@]} )); then
        echo "zizmor" >&2
        env -u GH_TOKEN -u GITHUB_TOKEN zizmor --offline --config .github/zizmor.yml "${inputs[@]}"
    fi
    inputs=()
    while IFS= read -r -d '' file; do [[ -f $file ]] && inputs+=("$file"); done \
        < <(owned '.github/*.yml' '.github/*.yaml')
    echo "conftest" >&2
    conftest verify --policy policy
    if (( ${#inputs[@]} )); then
        conftest test --policy policy --all-namespaces --combine "${inputs[@]}"
    fi

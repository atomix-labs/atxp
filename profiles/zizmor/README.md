# `zizmor`

zizmor audits every workflow, action and Dependabot configuration the repository
owns for security: template injection, dangerous triggers, broad permissions,
credentials left in a checkout, and more. It runs offline on every change, with
`.github/zizmor.yml`; [`actionlint`](../actionlint/README.md) checks
correctness. A file `.gitattributes` marks `linguist-vendored` or
`linguist-generated` is someone else's and is left out.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                     | Part  | Policy | Notes |
| ---------------------------------------- | ----- | ------ | ----- |
| `.github/zizmor.yml`                     | whole | owned  |       |
| `.just/zizmor.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-zizmor.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                 | keys  | owned  |       |

## Recipes

- `check-zizmor`: Audits every workflow, action and Dependabot config the
  repository owns, offline, so needing no token; a file .gitattributes marks
  `linguist-vendored` or `linguist-generated` is someone else's.

<!-- /facts -->

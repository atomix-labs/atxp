# `yaml`

yamllint checks YAML for what no formatter fixes: duplicate keys, implicit and
explicit octal values, and truthy words other than `true` and `false`. Layout is
the formatter's, so its layout rules are off. It reads the YAML files the
repository owns, tracked or new, less what `.gitattributes` marks
`linguist-vendored` or `linguist-generated`.

It owns those keys of `.yamllint.yaml`, under `merge`, so rules the repository
adds or changes, and its `ignore`, stay its own.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                       | Part  | Policy | Notes |
| ------------------------------------------ | ----- | ------ | ----- |
| `.yamllint.yaml`                           | keys  | merge  |       |
| `.just/yaml.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-yaml.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                   | keys  | owned  |       |

## Recipes

- `check-yaml`: Checks every YAML file the repository owns, tracked or new,
  for what no formatter fixes; a file .gitattributes marks `linguist-vendored`
  or `linguist-generated` is someone else's.

<!-- /facts -->

# `yaml`

Every YAML file, formatted by [`dprint`](../../lang/dprint/README.md)'s YAML
plugin, with double quotes, settings this profile keeps as keys of
`dprint.json`; and checked by yamllint for what no formatter fixes: duplicate
keys, implicit and explicit octal values, and truthy words other than `true` and
`false`. Layout is the formatter's, so its layout rules are off. It reads the
YAML files the repository owns, tracked or new, less what `.gitattributes` marks
`linguist-vendored` or `linguist-generated`.

It owns those keys of `.yamllint.yaml`, under `merge`, so rules the repository
adds or changes, and its `ignore`, stay its own.

Each half is a feature, both on by default: `format`, dprint's, and `lint`,
yamllint's, which installs through pipx with the uv and Python
[`mise`](../../tooling/mise/README.md) pins.

<!-- facts: written by devset-collection -->

## Owns

| File                                   | Part  | Policy | Notes            |
| -------------------------------------- | ----- | ------ | ---------------- |
| `.yamllint.yaml`                       | keys  | merge  | feature `lint`   |
| `.just/yaml.just`                      | whole | owned  | feature `lint`   |
| `.config/mise/conf.d/devset-yaml.toml` | whole | owned  | feature `lint`   |
| `.config/mise/mise.lock`               | keys  | owned  | feature `lint`   |
| `dprint.json`                          | keys  | merge  | feature `format` |

## Features

| Feature  | Default | Enables      |
| -------- | ------- | ------------ |
| `format` | yes     | `dep:dprint` |
| `lint`   | yes     | `dep:mise`   |

## Recipes

- `check-yaml`: Checks every YAML file the repository owns, tracked or new, for
  what no formatter fixes; a file .gitattributes marks `linguist-vendored` or
  `linguist-generated` is someone else's.

## Requires

- [`dprint`](../dprint/README.md): optional
- [`mise`](../../tooling/mise/README.md): optional

<!-- /facts -->

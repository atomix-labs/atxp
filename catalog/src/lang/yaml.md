# `yaml`

YAML: formatted by dprint with double quotes, and checked by yamllint for what
no formatter fixes.

```sh
devset add atxp/yaml --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `lang` · In [`rust`](../bundles/rust.md): always

Every YAML file, formatted by [`dprint`](dprint.md)'s YAML plugin, with double
quotes, settings this profile keeps as keys of `dprint.json`; and checked by
yamllint for what no formatter fixes: duplicate keys, implicit and explicit
octal values, and truthy words other than `true` and `false`. Layout is the
formatter's, so its layout rules are off. It reads the YAML files the repository
owns, tracked or new, less what `.gitattributes` marks `linguist-vendored` or
`linguist-generated`.

It owns those keys of `.yamllint.yaml`, under `merge`, so rules the repository
adds or changes, and its `ignore`, stay its own.

Each half is a feature, both on by default: `format`, dprint's, and `lint`,
yamllint's, which installs through pipx with the uv and Python
[`mise`](../tooling/mise.md) pins.

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
  what no formatter fixes.

## Requires

- [`dprint`](dprint.md): optional
- [`mise`](../tooling/mise.md): optional

# `suppressions`

Every lint suppression proves it still suppresses something, for the tools that
do not report it themselves.

```sh
devset add atxp/suppressions --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `tooling`

A suppression that no longer suppresses anything hides the next real finding.
Rust's `#[expect]` and Ruff's `RUF100` report their own dead ones; this proves
the rest: each `# noqa` for ansible-lint, `# shellcheck disable=` and `//
dprint-ignore` is removed in a copy, and the finding it silenced must come back.
An exclude in `.yamllint.yaml` or `.ansible-lint` that matches no file the tool
checks is dead too.

## Owns

| File                      | Part  | Policy | Notes |
| ------------------------- | ----- | ------ | ----- |
| `.just/suppressions.just` | whole | owned  |       |
| `.just/suppressions.py`   | whole | owned  |       |

## Recipes

- `check-suppressions`: Proves every suppression still suppresses something: `#
  noqa`, `shellcheck disable`, `dprint-ignore`.

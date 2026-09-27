# `mdbook-tool`

mdBook itself, pinned with mise and locked for every platform, so every machine
and CI job builds with the same release. [`mdbook`](../mdbook/README.md), the
book, requires it, and so does
[`devset-collection`](../../devset/devset-collection/README.md)'s catalog site:
one pin, which the weekly bump moves once for both.

<!-- facts: written by devset-collection -->

## Owns

| File                                          | Part  | Policy | Notes |
| --------------------------------------------- | ----- | ------ | ----- |
| `.config/mise/conf.d/devset-mdbook-tool.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                      | keys  | owned  |       |

## Requires

- [`mise`](../../tooling/mise/README.md)

<!-- /facts -->

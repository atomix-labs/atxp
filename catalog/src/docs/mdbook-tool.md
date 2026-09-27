# `mdbook-tool`

mdBook itself, pinned for every machine and job: for a book, and for a
collection's catalog.

```sh
devset add atxp/mdbook-tool --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `docs`

mdBook itself, pinned with mise and locked for every platform, so every machine
and CI job builds with the same release. [`mdbook`](mdbook.md), the book,
requires it, and so does [`devset-collection`](../devset/devset-collection.md)'s
catalog site: one pin, which the weekly bump moves once for both.

## Owns

| File                                          | Part  | Policy | Notes |
| --------------------------------------------- | ----- | ------ | ----- |
| `.config/mise/conf.d/devset-mdbook-tool.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                      | keys  | owned  |       |

## Requires

- [`mise`](../tooling/mise.md)

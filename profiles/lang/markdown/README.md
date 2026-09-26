# `markdown`

Every Markdown file, formatted by [`dprint`](../../lang/dprint/README.md)'s
Markdown plugin, wrapped at 80 with asterisks for emphasis, settings this
profile keeps as keys of `dprint.json`; and linted by rumdl, which fixes what it
can. Line length is the formatter's; the rules rustdoc's intra-doc links and
code spans trip are off; headings are in title case; a heading may repeat under
different parents, as a changelog's sections do under each release; `<details>`,
`<summary>`, `<code>` and `<span>` are the HTML a page may use; and GitHub's
issue and pull request templates, each the body of a page with its own title,
open without a heading.

It owns those keys of `.rumdl.toml`, under `merge`: `exclude`, and `[MD063]
ignore-words`, the names heading case leaves as they are, stay the repository's.

Git ignores rumdl's cache, in a block of `.gitignore`.

Each half is a feature, both on by default: `format`, dprint's, and `lint`,
rumdl's with its configuration, pin, recipes and cache. `links` adds
[`lychee`](../../docs/lychee/README.md), which checks every link into the
repository on each change, and the web's nightly.

<!-- facts: written by devset-collection -->

## Owns

| File                                       | Part  | Policy | Notes            |
| ------------------------------------------ | ----- | ------ | ---------------- |
| `.rumdl.toml`                              | keys  | merge  | feature `lint`   |
| `.just/markdown.just`                      | whole | owned  | feature `lint`   |
| `.config/mise/conf.d/devset-markdown.toml` | whole | owned  | feature `lint`   |
| `.config/mise/mise.lock`                   | keys  | owned  | feature `lint`   |
| `.gitignore`                               | block | owned  | feature `lint`   |
| `dprint.json`                              | keys  | merge  | feature `format` |

## Features

| Feature  | Default | Enables      |
| -------- | ------- | ------------ |
| `format` | yes     | `dep:dprint` |
| `lint`   | yes     |              |
| `links`  |         | `dep:lychee` |

## Recipes

- `check-markdown`: Lints every Markdown file.
- `fix-markdown`: Fixes what rumdl can fix.

## Requires

- [`dprint`](../dprint/README.md): optional
- [`lychee`](../../docs/lychee/README.md): optional

<!-- /facts -->

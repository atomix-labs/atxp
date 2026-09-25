# `rumdl`

rumdl lints every Markdown file, and fixes what it can. Line length is the
formatter's; the rules rustdoc's intra-doc links and code spans trip are off;
headings are in title case; a heading may repeat under different parents, as a
changelog's sections do under each release; and `<details>`, `<summary>`,
`<code>` and `<span>` are the HTML a page may use.

It owns those keys of `.rumdl.toml`, under `merge`: `exclude`, and `[MD063]
ignore-words`, the names heading case leaves as they are, stay the repository's.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                    | Part  | Policy | Notes |
| --------------------------------------- | ----- | ------ | ----- |
| `.rumdl.toml`                           | keys  | merge  |       |
| `.just/rumdl.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-rumdl.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                | keys  | owned  |       |

## Recipes

- `check-rumdl`: Lints every Markdown file.
- `fix-rumdl`: Fixes what rumdl can fix.

<!-- /facts -->

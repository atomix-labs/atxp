# `markdown`

rumdl lints every Markdown file, and fixes what it can. Line length is the
formatter's; the rules rustdoc's intra-doc links and code spans trip are off;
headings are in title case; a heading may repeat under different parents, as a
changelog's sections do under each release; `<details>`, `<summary>`, `<code>`
and `<span>` are the HTML a page may use; and GitHub's issue and pull request
templates, each the body of a page with its own title, open without a heading.

It owns those keys of `.rumdl.toml`, under `merge`: `exclude`, and `[MD063]
ignore-words`, the names heading case leaves as they are, stay the repository's.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                    | Part  | Policy | Notes |
| --------------------------------------- | ----- | ------ | ----- |
| `.rumdl.toml`                           | keys  | merge  |       |
| `.just/markdown.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-markdown.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                | keys  | owned  |       |

## Recipes

- `check-markdown`: Lints every Markdown file.
- `fix-markdown`: Fixes what rumdl can fix.

<!-- /facts -->

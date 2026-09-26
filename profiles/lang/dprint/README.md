# `dprint`

dprint formats Markdown, wrapped at 80 with asterisks for emphasis; YAML, with
double quotes; JSON, on one line where it fits; and Python, CSS and JavaScript,
at `line_width`. Every plugin is pinned by its checksum.

It owns those keys of `dprint.json`, under `merge`. `excludes` leaves out build
output, minified and vendored files, the book's theme, `.just/`, whose recipes
are formatted where they come from, and `CHANGELOG.md`, which
[`git-cliff`](../../git/git-changelog/README.md) lays out; a repository adds its own.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                     | Part  | Policy | Notes    |
| ---------------------------------------- | ----- | ------ | -------- |
| `dprint.json`                            | keys  | merge  | template |
| `.just/dprint.just`                      | whole | owned  |          |
| `.config/mise/conf.d/devset-dprint.toml` | whole | owned  |          |
| `.config/mise/mise.lock`                 | keys  | owned  |          |

## Recipes

- `check-dprint`: Checks that every Markdown, JSON and YAML file is formatted.
- `fix-dprint`: Formats every Markdown, JSON and YAML file.

## Variables

| Variable     | Default | Asks                                                  |
| ------------ | ------- | ----------------------------------------------------- |
| `line_width` | `100`   | Line width, shared by the formatters and EditorConfig |

<!-- /facts -->

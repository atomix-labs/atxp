# `dprint`

dprint, the formatter the language profiles share. It formats JSON, on one line
where it fits, CSS and JavaScript, at `line_width`, and loads the plugin of each
language profile the repository applies, read from devset's graph:
[`markdown`](../../lang/markdown/README.md)'s,
[`yaml`](../../lang/yaml/README.md)'s and
[`python`](../../lang/python/README.md)'s, whose settings are their own keys of
`dprint.json`. Every plugin is pinned by its checksum.

It owns those keys of `dprint.json`, under `merge`. `plugins` and `includes`
follow the profiles applied, so they are its own: a list is one value, which a
repository's edit and a change of the graph would both change. dprint leaves out
what git ignores, so each profile's build output stays out on its own;
`excludes` adds minified files, `.just/`, whose recipes are formatted where they
come from, and `CHANGELOG.md`, which
[`git-changelog`](../../git/git-changelog/README.md) lays out. A repository adds
its own to `excludes`. A `dprint.json` a repository already has keeps its own
`excludes` when the profile adopts it, so add `.just/**` and `CHANGELOG.md` to
them.

<!-- facts: written by devset-collection -->

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

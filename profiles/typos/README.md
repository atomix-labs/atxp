# `typos`

typos checks the spelling of every file the repository owns: code, documents and
configuration. It leaves out what a tool writes (devset's records, the locks
with their checksums, the book mdBook builds, vendored or minified code) and
commit ids, which are no words.

A finding is fixed, or allowed, by hand: `typos --write-changes` would also
correct a misspelling a test means, so no `fix-*` recipe runs it, and neither
does the weekly bump's `just fix`. The words a repository allows, in
`[default.extend-words]`, and the paths it adds to leave out, stay its own: it
owns those keys of `typos.toml` under `merge`.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                    | Part  | Policy | Notes |
| --------------------------------------- | ----- | ------ | ----- |
| `typos.toml`                            | keys  | merge  |       |
| `.just/typos.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-typos.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                | keys  | owned  |       |

## Recipes

- `check-typos`: Checks the spelling of every file the repository tracks. A
  finding is fixed or allowed by hand: `typos --write-changes` also rewrites a
  misspelling a test means, so no fix recipe runs it.

<!-- /facts -->

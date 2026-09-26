# `lychee`

lychee checks the links in every Markdown file git does not ignore, so never in
build output or installed packages. On every change it checks those into the
repository, offline, fragments included; nightly it checks the web's too, which
can fail for reasons no change caused.

Where the repository has no `lychee.toml`, it scaffolds one, which lychee reads
by default: `.devset/` left out, a slow server retried twice, and a rate limit
taken for an answer, not a broken link. It is the repository's from then on.

<!-- facts: written by devset-collection -->

## Owns

| File                                     | Part  | Policy | Notes             |
| ---------------------------------------- | ----- | ------ | ----------------- |
| `lychee.toml`                            | whole | once   | scaffold `lychee` |
| `.just/lychee.just`                      | whole | owned  |                   |
| `.config/mise/conf.d/devset-lychee.toml` | whole | owned  |                   |
| `.config/mise/mise.lock`                 | keys  | owned  |                   |

## Recipes

- `check-lychee`: Checks every link into the repository, offline, in each
  Markdown file git does not ignore.
- `nightly-lychee`: Checks every link, the web's too.

<!-- /facts -->

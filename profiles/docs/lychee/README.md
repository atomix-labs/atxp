# `lychee`

lychee checks the links in every Markdown file git does not ignore, so never in
build output or installed packages. On every change it checks those into the
repository, offline, fragments included; nightly it checks the web's too, which
can fail for reasons no change caused.

Where the repository has no `lychee.toml`, it scaffolds one, which lychee reads
by default: `.devset/` left out, a slow server retried twice, and a rate limit
taken for an answer, not a broken link. It is the repository's from then on.

Where [`mdbook`](../mdbook/README.md) checks the links of the built book, its
`links` feature, the book's pages are left to it: a link there to `/` means the
site's root, which only the built book has.

<!-- facts: written by devset-collection -->

## Owns

| File                                     | Part  | Policy | Notes             |
| ---------------------------------------- | ----- | ------ | ----------------- |
| `lychee.toml`                            | whole | once   | scaffold `lychee` |
| `.just/lychee.just`                      | whole | owned  | template          |
| `.config/mise/conf.d/devset-lychee.toml` | whole | owned  |                   |
| `.config/mise/mise.lock`                 | keys  | owned  |                   |

## Recipes

- `check-lychee`: Checks every link into the repository, offline, in each
  Markdown file git does not ignore; the book's pages are mdbook's where it
  checks the built book, in which a link to `/` has a root.
- `nightly-lychee`: Checks every link, the web's too.

## Variables

| Variable   | Default | Asks                                   |
| ---------- | ------- | -------------------------------------- |
| `book_dir` | `docs`  | Directory of the mdBook, its book.toml |

<!-- /facts -->

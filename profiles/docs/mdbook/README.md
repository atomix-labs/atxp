# `mdbook`

The book, built with mdBook from `book_dir`. Where the repository has no
`book.toml`, it scaffolds a book: `SUMMARY.md`, an introduction, a getting
started page, and a README for its authors, the repository's once written; and
`book.toml` starts with its title and language, and a `SUMMARY.md` entry
pointing at no file an error. Where a book is there, its pages stay as they are.

It owns the rest of `book.toml` under `merge`: the theme, the repository's
links, the site's URL, the stylesheets and scripts the features bring, the
preprocessors, folding and search. And it owns the book's look, under `merge`: a
wider page, collapsible definitions as cards, and a `$` prompt on `console`
blocks. `check-mdbook` lints the book (every page in `SUMMARY.md`, every include
and anchor there, every recipe a page names), builds it, and runs its Rust
examples. `mdbook serve`, run in `book_dir`, serves it, rebuilt on every change.

The features, all but `mermaid` on by default:

- `katex`: math, rendered at build time by mdbook-katex; its stylesheet and
  fonts are vendored, at the version mdbook-katex renders with, so the site
  makes no third-party request.
- `mermaid`: diagrams, drawn by the mermaid mdbook-mermaid ships.
- `api`: the workspace's rustdoc at `/api`, with rustdoc's index page, which
  needs the nightly toolchain, and a link to it in the menu bar.
- `pages`: the book on GitHub Pages, through
  [`github-ci`](../../github/github-ci/README.md)'s `pages`, and the keys of
  `.github/automation.json` that name the recipe and the site.
- `links`: [`lychee`](../../docs/lychee/README.md) checks every link of the
  built book, offline, rustdoc's pages aside.

Git ignores the built book, `book_dir/book/`, in a block of `.gitignore`.

<!-- facts: written by devset-collection -->

## Owns

| File                                                                    | Part  | Policy | Notes                                          |
| ----------------------------------------------------------------------- | ----- | ------ | ---------------------------------------------- |
| `{{ book_dir }}/book.toml`                                              | keys  | merge  | template                                       |
| `{{ book_dir }}/src/SUMMARY.md`                                         | whole | once   | scaffold `book`                                |
| `{{ book_dir }}/src/introduction.md`                                    | whole | once   | scaffold `book`                                |
| `{{ book_dir }}/src/getting-started.md`                                 | whole | once   | scaffold `book`                                |
| `{{ book_dir }}/theme/width.css`                                        | whole | merge  |                                                |
| `{{ book_dir }}/theme/details.css`                                      | whole | merge  |                                                |
| `{{ book_dir }}/theme/prompt.css`                                       | whole | merge  |                                                |
| `{{ book_dir }}/README.md`                                              | whole | once   | scaffold `book`                                |
| `{{ book_dir }}/vendor/katex/katex.min.css`                             | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/vendor/katex/README.md`                                 | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_AMS-Regular.woff2`         | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Caligraphic-Bold.woff2`    | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Caligraphic-Regular.woff2` | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Fraktur-Bold.woff2`        | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Fraktur-Regular.woff2`     | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Main-Bold.woff2`           | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Main-BoldItalic.woff2`     | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Main-Italic.woff2`         | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Main-Regular.woff2`        | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Math-BoldItalic.woff2`     | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Math-Italic.woff2`         | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_SansSerif-Bold.woff2`      | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_SansSerif-Italic.woff2`    | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_SansSerif-Regular.woff2`   | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Script-Regular.woff2`      | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Size1-Regular.woff2`       | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Size2-Regular.woff2`       | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Size3-Regular.woff2`       | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Size4-Regular.woff2`       | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/src/vendor/katex/fonts/KaTeX_Typewriter-Regular.woff2`  | whole | owned  | feature `katex`                                |
| `{{ book_dir }}/mermaid.min.js`                                         | whole | owned  | feature `mermaid`                              |
| `{{ book_dir }}/mermaid-init.js`                                        | whole | owned  | feature `mermaid`                              |
| `{{ book_dir }}/api-link.js`                                            | whole | owned  | feature `api`                                  |
| `.github/automation.json`                                               | keys  | owned  | template, feature `pages`, profile `github-ci` |
| `.just/mdbook.just`                                                     | whole | owned  | template                                       |
| `.just/mdbook.py`                                                       | whole | owned  |                                                |
| `.config/mise/conf.d/devset-mdbook.toml`                                | whole | owned  | template                                       |
| `.config/mise/mise.lock`                                                | keys  | owned  | template                                       |
| `.gitignore`                                                            | block | owned  | template                                       |

## Features

| Feature   | Default | Enables            |
| --------- | ------- | ------------------ |
| `katex`   | yes     |                    |
| `mermaid` |         |                    |
| `api`     | yes     |                    |
| `pages`   | yes     | `github-ci?/pages` |
| `links`   | yes     | `dep:lychee`       |

## Recipes

- `check-mdbook`: Lints the book (every page in SUMMARY.md, every include and
  anchor there, every recipe the prose names), builds it, and runs its Rust
  examples.{% if "api" in devset.features %} The workspace's API lands at /api,
  with rustdoc's index page.{% endif %}{% if "links" in devset.features %} Then
  lychee checks every link of the built book, offline.{% endif %}

## Variables

| Variable     | Default | Asks                                   |
| ------------ | ------- | -------------------------------------- |
| `book_dir`   | `docs`  | Directory of the mdBook, its book.toml |
| `repository` | none    | The GitHub repository, owner/name      |

## Requires

- [`github-ci`](../../github/github-ci/README.md): optional
- [`lychee`](../lychee/README.md): optional
- [`rust-toolchain`](../../rust/rust-toolchain/README.md)

<!-- /facts -->

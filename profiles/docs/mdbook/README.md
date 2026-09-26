# `mdbook`

mdBook builds the book in `book_dir` (default `docs`), and runs every Rust
example in it as a test. Git ignores what it builds, `book/` beside `book.toml`.

Preprocessors a book uses are pinned beside it, by the repository or the profile
that needs them.

<!-- facts: written by devset-collection -->

## Owns

| File                                     | Part  | Policy | Notes    |
| ---------------------------------------- | ----- | ------ | -------- |
| `.just/mdbook.just`                      | whole | owned  | template |
| `.config/mise/conf.d/devset-mdbook.toml` | whole | owned  |          |
| `.config/mise/mise.lock`                 | keys  | owned  |          |
| `.gitignore`                             | block | owned  | template |

## Recipes

- `check-mdbook`: Builds the book, and runs its Rust examples.

## Variables

| Variable   | Default | Asks                                   |
| ---------- | ------- | -------------------------------------- |
| `book_dir` | `docs`  | Directory of the mdBook, its book.toml |

## Requires

- [`rust-toolchain`](../../rust/rust-toolchain/README.md)

<!-- /facts -->

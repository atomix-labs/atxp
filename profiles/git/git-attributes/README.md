# `git-attributes`

Git stores text with LF endings, and checks out Windows batch files with CRLF,
which `cmd.exe` needs. Diffs name the enclosing function in Rust, Python,
Markdown, HTML and CSS.

It owns a block of `.gitattributes`. A line the repository adds after the block
overrides it, as later lines do in Git.

<!-- facts: written by devset-collection -->

## Owns

| File             | Part  | Policy | Notes |
| ---------------- | ----- | ------ | ----- |
| `.gitattributes` | block | owned  |       |

<!-- /facts -->

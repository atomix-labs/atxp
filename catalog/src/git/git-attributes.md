# `git-attributes`

Git attributes: LF in the repository, CRLF for Windows scripts, and
language-aware diffs.

```sh
devset add atxp/git-attributes --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `git` · In [`rust`](../bundles/rust.md): always

Git stores text with LF endings, and checks out Windows batch files with CRLF,
which `cmd.exe` needs. Diffs name the enclosing function in Rust, Python,
Markdown, HTML and CSS.

It owns a block of `.gitattributes`. A line the repository adds after the block
overrides it, as later lines do in Git.

## Owns

| File             | Part  | Policy | Notes |
| ---------------- | ----- | ------ | ----- |
| `.gitattributes` | block | owned  |       |

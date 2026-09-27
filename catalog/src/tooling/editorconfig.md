# `editorconfig`

EditorConfig: UTF-8, LF, a final newline, spaces, and the shared line width.

```sh
devset add atxp/editorconfig --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `tooling` · In [`rust`](../bundles/rust.md): always

The editor settings every file shares: UTF-8, LF line endings, a final newline,
no trailing whitespace, and four spaces, two for data and Markdown. Editors show
`line_width` as a guide.

The policy is `merge`, so sections the repository adds are kept, and merged with
the profile's changes.

## Owns

| File            | Part  | Policy | Notes    |
| --------------- | ----- | ------ | -------- |
| `.editorconfig` | whole | merge  | template |

## Variables

| Variable     | Default | Asks                                                  |
| ------------ | ------- | ----------------------------------------------------- |
| `line_width` | `100`   | Line width, shared by the formatters and EditorConfig |

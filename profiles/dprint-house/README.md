# `dprint-house`

The house dprint, a flavor of the collection's `dprint`: Markdown wrapped at 80
columns with asterisks for emphasis, YAML with double quotes, JSON kept on one
line where it fits, and Python, CSS and JavaScript formatted too. Every plugin
is pinned by its checksum.

It owns those keys of `dprint.json`, under `merge`: `excludes` leaves out build
output, minified and vendored files, the book's theme, and `.just/`, whose
recipes are formatted where they come from; a repository adds its own.

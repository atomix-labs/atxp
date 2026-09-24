# `suppressions`

A suppression that no longer suppresses anything hides the next real finding.
Rust's `#[expect]` and Ruff's `RUF100` report their own dead ones; this proves
the rest: each `# noqa` for ansible-lint, `# shellcheck disable=` and `//
dprint-ignore` is removed in a copy, and the finding it silenced must come back.
An exclude in `.yamllint` or `.ansible-lint` that matches no file is dead too.

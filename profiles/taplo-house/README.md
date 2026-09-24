# `taplo-house`

The house layout for TOML, as keys of `taplo.toml` beside those of the
collection's `taplo`: entries and comments aligned, arrays collapsed where they
fit, four spaces of indent, and entries alphabetized within dependency tables,
where a blank line keeps `# external` and `# internal` apart.

It formats the crate manifests, `**/Cargo.toml`; every other TOML file is
written by the tool that reads it.

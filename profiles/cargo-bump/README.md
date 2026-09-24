# `cargo-bump`

`bump-cargo-bump`, run weekly by `just bump`, moves every Cargo requirement in
every workspace root, one at a time: each to its newest release that is at least
three days old, kept only if the workspace still resolves, features included,
and put back otherwise, with the reason reported. A git dependency pinned by
`rev` moves to its repository's HEAD once that commit is three days old. Then
every lockfile is settled, taking the newest release each crate's `rust-version`
allows.

Crates a root names in `[workspace.metadata.bump] exclude` stay put. Pins
cargo-edit with mise.

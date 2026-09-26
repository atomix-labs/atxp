# `cargo-bump`

`bump-cargo-bump`, run weekly by `just bump`, moves every Cargo requirement in
every workspace root, one at a time: each to its newest release that is at least
three days old, kept only if the workspace still resolves, features included,
and put back otherwise, with the reason reported. A git dependency pinned by
`rev` moves to its repository's HEAD once that commit is three days old. Then
every lockfile is settled, taking the newest release each crate's `rust-version`
allows, as [`cargo-workspace`](../../cargo/cargo-workspace/README.md)'s resolver
key says.

Crates a root names in `[workspace.metadata.bump] exclude` stay put. At a
release, `just release` runs `release-cargo-bump`, which sets every crate's
version to `RELEASE_VERSION` with cargo-edit's `set-version`, and the lock with
them.

<!-- facts: written by devset-collection -->

## Owns

| File                                         | Part  | Policy | Notes |
| -------------------------------------------- | ----- | ------ | ----- |
| `.just/cargo-bump.just`                      | whole | owned  |       |
| `.just/cargo-bump.py`                        | whole | owned  |       |
| `.config/mise/conf.d/devset-cargo-bump.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                     | keys  | owned  |       |

## Recipes

- `bump-cargo-bump`: Moves every Cargo requirement and git revision past the
  cooldown, one at a time, and settles the locks.
- `release-cargo-bump`: Sets every crate's version to $RELEASE_VERSION, and the
  lock with them.

## Requires

- [`rust-toolchain`](../../rust/rust-toolchain/README.md)

<!-- /facts -->

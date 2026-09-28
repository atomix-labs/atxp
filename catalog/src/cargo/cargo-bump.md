# `cargo-bump`

The weekly bump of Cargo requirements and git revisions: one at a time, past the
cooldown, kept if it resolves.

```sh
devset add atxp/cargo-bump --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `cargo` · In [`rust`](../bundles/rust.md): always

`bump-cargo-bump`, run weekly by `just bump`, moves every Cargo requirement in
every workspace root, one at a time: each to its newest release that is at least
three days old, kept only if the workspace still resolves, features included,
and put back otherwise, with the reason reported. A git dependency pinned by
`rev` moves to its repository's HEAD once that commit is three days old. Then
every lockfile is settled, taking the newest release each crate's `rust-version`
allows, as [`cargo-workspace`](cargo-workspace.md)'s resolver key says.

Crates a root names in `[workspace.metadata.bump] exclude` stay put, and a
workspace root under a path a root's `[workspace] exclude` names is not bumped:
an example's or a test fixture's manifest is data, as Cargo says it is. At a
release, `just release` runs `release-cargo-bump`, which sets every crate's
version to `RELEASE_VERSION` with cargo-edit's `set-version`, and the lock with
them.

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

- [`cargo-workspace`](cargo-workspace.md)
- [`rust-toolchain`](../rust/rust-toolchain.md)

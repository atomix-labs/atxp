# `cargo-bump`

`bump-cargo-bump`, run weekly by `just bump`, moves every Cargo requirement in
every workspace root, one at a time: each to its newest release that is at least
three days old, kept only if the workspace still resolves, features included,
and put back otherwise, with the reason reported. A git dependency pinned by
`rev` moves to its repository's HEAD once that commit is three days old. Then
every lockfile is settled, taking the newest release each crate's `rust-version`
allows, as the resolver key in `.cargo/config.toml` says.

Crates a root names in `[workspace.metadata.bump] exclude` stay put.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                         | Part  | Policy | Notes |
| -------------------------------------------- | ----- | ------ | ----- |
| `.just/cargo-bump.just`                      | whole | owned  |       |
| `.just/cargo-bump.py`                        | whole | owned  |       |
| `.config/mise/conf.d/devset-cargo-bump.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                     | keys  | owned  |       |
| `.cargo/config.toml`                         | keys  | owned  |       |

## Recipes

- `bump-cargo-bump`: Moves every Cargo requirement and git revision past the
  cooldown, one at a time, and settles the locks.

<!-- /facts -->

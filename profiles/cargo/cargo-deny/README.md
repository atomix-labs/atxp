# `cargo-deny`

cargo-deny holds the dependency tree to a policy. Yanked and unmaintained crates
are refused; a crate appears at one version only; a licence is one of the
permissive set, private crates aside; no version requirement is a wildcard,
workspace paths aside; and every crate comes from crates.io, a git source pinned
by its commit. The `strict` feature, the house policy, bans the crates with a
better choice, each naming the one to use.

It owns those keys of `deny.toml`: `[graph]`, `skip`, `allow-git` and anything
else the repository adds stay its own. `nightly-cargo-deny` checks the
advisories each night, as they are published without any commit.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                         | Part  | Policy | Notes |
| -------------------------------------------- | ----- | ------ | ----- |
| `deny.toml`                                  | keys  | owned  |       |
| `.just/cargo-deny.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-cargo-deny.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                     | keys  | owned  |       |

## Recipes

- `check-cargo-deny`: Checks advisories, licences, bans and sources.
- `nightly-cargo-deny`: Checks for advisories published since the last change,
  which no commit brings.

<!-- /facts -->

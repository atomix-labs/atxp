# `cargo-workspace-lints`

Fails when a crate does not inherit the workspace's `[workspace.lints]`, which
is how a crate leaves the shared lints without anyone deciding it should.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                                    | Part  | Policy | Notes |
| ------------------------------------------------------- | ----- | ------ | ----- |
| `.just/cargo-workspace-lints.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-cargo-workspace-lints.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                                | keys  | owned  |       |

## Recipes

- `check-cargo-workspace-lints`: Fails when a crate does not inherit the
  workspace's lints.

<!-- /facts -->

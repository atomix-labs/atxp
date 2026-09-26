# `cargo-manifest`

Holds every crate's `Cargo.toml` to one shape, where
[`toml`](../../lang/toml/README.md)'s taplo, which reads values and not the
text around them, cannot reach: `[package]` keys in their order, with every
field the workspace sets inherited; dependencies under `# external` then
`# internal`, each where it belongs, an internal one inherited from the
workspace; `default` first among the features; no comment but the two markers;
and `[lints] workspace = true`. A crate under a `vendor/` directory is
upstream's, and is left alone. `check-cargo-manifest` also runs
cargo-workspace-lints, which fails when a crate does not inherit the
workspace's `[workspace.lints]`, which is how a crate leaves the shared lints
without anyone deciding it should.

The `agents` feature adds the `editing-cargo-manifests` skill in
`.claude/skills/`: the shape this profile checks, and how to add a crate, a
dependency or a feature within it.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                       | Part  | Policy | Notes |
| -------------------------- | ----- | ------ | ----- |
| `.just/cargo-manifest.just` | whole | owned  |       |
| `.just/cargo-manifest.py`   | whole | owned  |       |

## Recipes

- `check-cargo-manifest`: Holds every crate manifest to one shape: what taplo,
  which reads values, cannot see.

<!-- /facts -->

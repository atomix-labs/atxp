# `cargo-manifest`

Holds every crate's `Cargo.toml` to one shape, where
[`toml`](../../lang/toml/README.md)'s taplo, which reads values and not the text
around them, cannot reach: `[package]` keys in their order, with every field the
workspace sets inherited; dependencies under `# external` then `# internal`,
each where it belongs, an internal one inherited from the workspace; `default`
first among the features; no comment but the two markers; and `[lints]
workspace = true`. A crate under a `vendor/` directory is upstream's, and is
left alone. `check-cargo-manifest` also runs cargo-workspace-lints, which fails
when a crate does not inherit the workspace's `[workspace.lints]`, which is how
a crate leaves the shared lints without anyone deciding it should.
`fix-cargo-manifest` puts each dependency under its group, `# external` or `#
internal`, in every manifest the workspace's included, keeping their order and a
blank line between the groups where the table has one; a table already in its
groups keeps its layout, and one with any other line in it is left for the check
to name.

The `agents` feature adds the `editing-cargo-manifests` skill in
`.claude/skills/`: the shape this profile checks, and how to add a crate, a
dependency or a feature within it.

<!-- facts: written by devset-collection -->

## Owns

| File                                                           | Part  | Policy | Notes                      |
| -------------------------------------------------------------- | ----- | ------ | -------------------------- |
| `.just/cargo-manifest.just`                                    | whole | owned  |                            |
| `.just/cargo-manifest.py`                                      | whole | owned  |                            |
| `.config/mise/conf.d/devset-cargo-manifest.toml`               | whole | owned  |                            |
| `.config/mise/mise.lock`                                       | keys  | owned  |                            |
| `.claude/skills/editing-cargo-manifests/SKILL.md`              | whole | owned  | template, feature `agents` |
| `.claude/skills/editing-cargo-manifests/references/sources.md` | whole | owned  | feature `agents`           |

## Features

| Feature  | Default | Enables |
| -------- | ------- | ------- |
| `agents` |         |         |

## Recipes

- `check-cargo-manifest`: Holds every crate manifest to one shape, which taplo,
  reading values, cannot see, and fails when a crate does not inherit the
  workspace's lints.
- `fix-cargo-manifest`: Puts every dependency under its group, `# external` or
  `# internal`, the workspace's included.

## Requires

- [`rust-toolchain`](../../rust/rust-toolchain/README.md)

<!-- /facts -->

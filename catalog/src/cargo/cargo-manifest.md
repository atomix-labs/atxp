# `cargo-manifest`

Every crate manifest in one shape, the workspace's lints inherited, and the
skill for editing them.

```sh
devset add atxp/cargo-manifest --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `cargo` · In [`rust`](../bundles/rust.md): always

Holds the `Cargo.toml` of every crate in the workspace to one shape, where
[`toml`](../lang/toml.md)'s taplo, which reads values and not the text around
them, cannot reach: `[package]` keys in their order, with every field the
workspace sets inherited; dependencies under `# external` then `# internal`,
each where it belongs, an internal one inherited from the workspace; `default`
first among the features; no comment but the two markers; and `[lints]
workspace = true`. The workspace's manifests are those `cargo metadata` names,
so a `Cargo.toml` that is no part of it, a test's fixture or an example's, is
left alone, as a crate under a `vendor/` directory is, which is upstream's.
`check-cargo-manifest` also runs cargo-workspace-lints, which fails when a crate
does not inherit the workspace's `[workspace.lints]`, which is how a crate
leaves the shared lints without anyone deciding it should. `fix-cargo-manifest`
puts each dependency under its group, `# external` or `# internal`, in every
manifest the workspace's included, keeping their order and a blank line between
the groups where the table has one; a table already in its groups keeps its
layout, and one with any other line in it is left for the check to name.

The `agents` feature adds the `editing-cargo-manifests` skill in
`.claude/skills/`: the shape this profile checks, and how to add a crate, a
dependency or a feature within it.

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

- `check-cargo-manifest`: Holds every crate manifest to one shape, and fails
  where a crate does not inherit the lints.
- `fix-cargo-manifest`: Puts every dependency under its group, `# external` or
  `# internal`, the workspace's included.

## Requires

- [`rust-toolchain`](../rust/rust-toolchain.md)

# `cargo-deny`

cargo-deny: yanked and unmaintained crates, one version each, permissive
licences, crates.io only, and the house bans.

```sh
devset add atxp/cargo-deny --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `cargo` · In [`rust`](../bundles/rust.md): always

cargo-deny holds the dependency tree to a policy, with every feature on, so an
optional dependency answers to it as a default one does. Yanked and unmaintained
crates are refused; a crate appears at one version only; a licence is one of the
permissive set, private crates aside; no version requirement is a wildcard,
workspace paths aside; and every crate comes from crates.io, a git source pinned
by its commit. The `strict` feature, the house policy, bans the crates with a
better choice, each naming the one to use.

It owns those keys of `deny.toml`, and `all-features` in `[graph]`. Every other
key is the repository's, and devset keeps it: the rest of `[graph]`, where
`targets` still filters the graph; `allow-git`; and the exceptions a finding may
call for, each with its reason, as `skip` in `[bans]`, `ignore` in
`[advisories]` and `exceptions` in `[licenses]`. `nightly-cargo-deny` checks the
advisories each night, as they are published without any commit.

With `agents`, a block of the repository's `AGENTS.md`, where it has one, tells
an agent that a failure is the maintainer's choice to make.

## Owns

| File                                         | Part  | Policy | Notes                                |
| -------------------------------------------- | ----- | ------ | ------------------------------------ |
| `deny.toml`                                  | keys  | owned  | template                             |
| `.just/cargo-deny.just`                      | whole | owned  |                                      |
| `.config/mise/conf.d/devset-cargo-deny.toml` | whole | owned  |                                      |
| `.config/mise/mise.lock`                     | keys  | owned  |                                      |
| `AGENTS.md`                                  | block | owned  | feature `agents`, `AGENTS.md` exists |

## Features

| Feature  | Default | Enables |
| -------- | ------- | ------- |
| `strict` |         |         |
| `agents` |         |         |

## Recipes

- `check-cargo-deny`: Checks advisories, licences, bans and sources, with every
  feature on.
- `nightly-cargo-deny`: Checks for advisories published since the last change,
  which no commit brings.

## Requires

- [`rust-toolchain`](../rust/rust-toolchain.md)

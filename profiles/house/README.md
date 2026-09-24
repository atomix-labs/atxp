# `house`

A house Rust repository: the collection's atoms at a tag, and the house's own on
top. Where the house holds a different opinion from an atom, it takes the
house's flavor instead (`rustfmt-house` for `rustfmt`, `rust-nightly` for
`rust-toolchain`, `dprint-house`, `rumdl-house`, `ruff-house`); where it adds to
one, its atom owns other keys of the same file (`lints` and `cargo-profiles` in
`Cargo.toml`, `deny-house` in `deny.toml`, `taplo-house`, `vscode-house`).

Cargo dependencies move with the weekly bump, one at a time past the cooldown,
so Dependabot updates the Actions only; security updates are the repository's
setting.

```sh
devset init --git git@github.com:atomix-labs/atxp.git --branch main --path profiles/house
bash SETUP.sh
just check
```

The house's pins move here, and reach a repository with `devset update`. Once
devset is released, the collection's `devset` atom will run that weekly from
`just bump`, beside the repository's own bumps.

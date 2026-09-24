# `just-house`

The house atoms' recipes, imported into the `justfile` in a block of their own
beside the collection's `just` spine, which imports only the collection's atoms:
so `just check`, `just fix` and `just bump` run the house's recipes too.

The block also exports `CARGO_BUILD_TARGET` as the host's triple, so every cargo
command, the collection's recipes included, names its target and keeps
`RUSTFLAGS` off host build scripts. A recipe whose output must land in
`target/doc` rather than `target/<triple>/doc` unsets it.

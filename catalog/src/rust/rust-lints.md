# `rust-lints`

The lint wall, as keys of the workspace Cargo.toml: rustc, rustdoc, clippy and
cargo, and nightly's own lints.

```sh
devset add atxp/rust-lints --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `rust` · In [`rust`](../bundles/rust.md): always

The lint wall, as keys of the workspace `Cargo.toml`: `[workspace.lints]` for
rustc, rustdoc, clippy and cargo. The keys any open-source project can take deny
rustdoc's and cargo's lints, clippy's `all` and `pedantic` groups, and rustc's
lints for correctness: `unsafe_op_in_unsafe_fn`, `unused_must_use`, the 2018
idioms. The `strict` feature, the house policy, adds the wall on top: clippy's
`nursery` and the restriction lints (no `unwrap`, no `panic`, no indexing, no
`as`, no printing, and more), and rustc's `unsafe_code`, `missing_docs`,
`unreachable_pub`, `unused` and the lifetime lints.

Every lint in the keys is one stable rustc knows, so a crate under the wall
builds on stable too. Every other key of `Cargo.toml` is the repository's, and
so is `unexpected_cfgs`, whose `check-cfg` names each repository's own cfgs.

The `nightly` feature adds the two lints only nightly rustc has:
`non_exhaustive_omitted_patterns`, which catches a `match` on a
`#[non_exhaustive]` enum that falls to its wildcard for a variant it could name,
and `implicit_provenance_casts`, which catches a pointer cast to an integer that
exposes its provenance. `check-rust-lints` runs them with `cargo check` on the
nightly [`rust-toolchain`](rust-toolchain.md) pins, their features switched on
by `-Zcrate-attr`, so no source needs a `#![feature]` and
[`rust-msrv`](rust-msrv.md) can still prove a crate builds on stable. A crate
that enables them itself, as one built on nightly alone may, is no fault: the
check allows the feature enabled twice. It goes on past a crate that fails, so
one run names every crate to fix.

The `agents` feature adds the `writing-rust` skill in `.claude/skills/`: how
Rust is written here, in errors, crate and module layout, naming, API design,
ownership and lints, each rule with a bad and a good example that compile under
this wall, and what holds the rule. Where `strict` is on, it teaches the house
policy the wall holds; it explains each lint the wall turns on, and how to
answer one that misreads the code. The `async` feature adds the skill's
reference for async Rust on tokio: locks across `.await`, bounded channels,
blocking work, `JoinSet`, cancellation, `select!`, async traits and tests, and
`tracing`.

The `agents` feature also adds the `writing-unsafe-rust` skill: where unsafe
code goes and how each site is marked, what a `// SAFETY:` proof must establish,
`// INVARIANT:` fields, `unsafe impl Send` and `Sync` with the bounds their
access needs, pointers that keep their provenance and alignment, layout,
`transmute`, `MaybeUninit`, `Pin` and FFI, atomics whose every `// ORDERING:`
names what it pairs with, locks over an `UnsafeCell`, freeing a node no reader
holds, and how the proofs are tested: edge cases, loom models, compile-fail
tests, and Miri where [`rust-toolchain`](rust-toolchain.md) has its `miri`
feature. Each bad example a lint catches fails with that lint, and each good one
compiles under this wall.

## Owns

| File                                                               | Part  | Policy | Notes                             |
| ------------------------------------------------------------------ | ----- | ------ | --------------------------------- |
| `Cargo.toml`                                                       | keys  | owned  | template                          |
| `.just/rust-lints.just`                                            | whole | owned  | feature `nightly`                 |
| `.claude/skills/writing-rust/SKILL.md`                             | whole | owned  | template, feature `agents`        |
| `.claude/skills/writing-rust/references/api-design.md`             | whole | owned  | template, feature `agents`        |
| `.claude/skills/writing-rust/references/async.md`                  | whole | owned  | feature `agents`, feature `async` |
| `.claude/skills/writing-rust/references/errors.md`                 | whole | owned  | template, feature `agents`        |
| `.claude/skills/writing-rust/references/layout.md`                 | whole | owned  | template, feature `agents`        |
| `.claude/skills/writing-rust/references/lints.md`                  | whole | owned  | template, feature `agents`        |
| `.claude/skills/writing-rust/references/naming.md`                 | whole | owned  | feature `agents`                  |
| `.claude/skills/writing-rust/references/ownership.md`              | whole | owned  | template, feature `agents`        |
| `.claude/skills/writing-rust/references/sources.md`                | whole | owned  | template, feature `agents`        |
| `.claude/skills/writing-unsafe-rust/SKILL.md`                      | whole | owned  | template, feature `agents`        |
| `.claude/skills/writing-unsafe-rust/references/atomics.md`         | whole | owned  | template, feature `agents`        |
| `.claude/skills/writing-unsafe-rust/references/pointers.md`        | whole | owned  | template, feature `agents`        |
| `.claude/skills/writing-unsafe-rust/references/safety-comments.md` | whole | owned  | template, feature `agents`        |
| `.claude/skills/writing-unsafe-rust/references/sources.md`         | whole | owned  | template, feature `agents`        |
| `.claude/skills/writing-unsafe-rust/references/verifying.md`       | whole | owned  | template, feature `agents`        |

## Features

| Feature   | Default | Enables |
| --------- | ------- | ------- |
| `agents`  |         |         |
| `async`   |         |         |
| `nightly` |         |         |
| `strict`  |         |         |

## Recipes

- `check-rust-lints`: Checks the lints only nightly has, reporting every crate
  that fails.

## Requires

- [`rust-toolchain`](rust-toolchain.md)

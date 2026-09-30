# `cargo-profiles`

Build profiles as keys of the workspace Cargo.toml: release, bench, dev, test,
profiling and release-fast.

```sh
devset add atxp/cargo-profiles --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `cargo` · In [`rust`](../bundles/rust.md): always

The build profiles, as keys of the workspace `Cargo.toml`: `release`, with fat
LTO and one codegen unit; `dev`, with its dependencies at `opt-level = 3`;
`profiling`, with full debug info; `release-fast`, with thin LTO, for quicker
iteration; and `bench` and `test` beside them. The `strict` feature, the house
policy, sets `panic = "abort"` in `release` and `dev`: a panic ends the process
rather than unwinding through it.

Git ignores what profiling leaves behind (`*.profraw`, `perf.data`, flame
graphs), in a block of `.gitignore`. Every other key of `Cargo.toml` stays the
repository's.

The `agents` feature adds the `tuning-rust-performance` skill in
`.claude/skills/`: measuring before and after a change, with a profiler on the
`profiling` build and a `harness = false` benchmark whose results are committed
with what they were measured on; allocating before a hot path and reusing after,
with a crate's own `clippy.toml` and a counting allocator to hold it; inlining,
`#[cold]`, bounds checks and vectorization, as the assembly shows them; the size
and layout of hot types; what threads cost each other, from false sharing to
spinning, pinning and busy polling; and these profiles, each key and its reason,
and `strict`'s `panic = "abort"`. Each bad example a lint catches fails with
that lint, and each good one compiles under the workspace's lints. Where
[`rust-lints`](../rust/rust-lints.md) has `strict`, it teaches what the strict
lints add; it names the CPU floor only where
[`cargo-workspace`](cargo-workspace.md) is applied, and the recipes of
[`rust-clippy`](../rust/rust-clippy.md) and [`cargo-nextest`](cargo-nextest.md)
only where they are.

## Owns

| File                                                               | Part  | Policy | Notes                      |
| ------------------------------------------------------------------ | ----- | ------ | -------------------------- |
| `Cargo.toml`                                                       | keys  | owned  | template                   |
| `.gitignore`                                                       | block | owned  |                            |
| `.claude/skills/tuning-rust-performance/SKILL.md`                  | whole | owned  | template, feature `agents` |
| `.claude/skills/tuning-rust-performance/references/allocation.md`  | whole | owned  | template, feature `agents` |
| `.claude/skills/tuning-rust-performance/references/codegen.md`     | whole | owned  | template, feature `agents` |
| `.claude/skills/tuning-rust-performance/references/data-layout.md` | whole | owned  | template, feature `agents` |
| `.claude/skills/tuning-rust-performance/references/measuring.md`   | whole | owned  | template, feature `agents` |
| `.claude/skills/tuning-rust-performance/references/sources.md`     | whole | owned  | feature `agents`           |
| `.claude/skills/tuning-rust-performance/references/threads.md`     | whole | owned  | template, feature `agents` |

## Features

| Feature  | Default | Enables |
| -------- | ------- | ------- |
| `agents` |         |         |
| `strict` |         |         |

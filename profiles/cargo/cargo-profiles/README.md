# `cargo-profiles`

The build profiles, as keys of the workspace `Cargo.toml`: `release`, with fat
LTO and one codegen unit; `dev`, with its dependencies at `opt-level = 3`;
`profiling`, with full debug info; `release-fast`, with thin LTO, for quicker
iteration; and `bench` and `test` beside them. The `strict` feature, the house
policy, sets `panic = "abort"` in `release` and `dev`: a panic ends the process
rather than unwinding through it.

Git ignores what profiling leaves behind (`*.profraw`, `perf.data`, flame
graphs), in a block of `.gitignore`. Every other key of `Cargo.toml` stays the
repository's.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File         | Part | Policy | Notes |
| ------------ | ---- | ------ | ----- |
| `Cargo.toml` | keys | owned  |       |

<!-- /facts -->

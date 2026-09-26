# `cargo-profiles`

The build profiles, as keys of the workspace `Cargo.toml`: `release`, with fat
LTO, one codegen unit and `panic = "abort"`; `dev`, with its dependencies at
`opt-level = 3`; `profiling`, with full debug info; `release-fast`, with thin
LTO, for quicker iteration; and `bench` and `test` beside them.

Git ignores what profiling leaves behind (`*.profraw`, `perf.data`, flame
graphs), in a block of `.gitignore`. Every other key of `Cargo.toml` stays the
repository's.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File         | Part | Policy | Notes |
| ------------ | ---- | ------ | ----- |
| `Cargo.toml` | keys | owned  |       |

<!-- /facts -->

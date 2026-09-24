# `cargo-profiles`

The house build profiles, as keys of the workspace `Cargo.toml`: `release` with
fat LTO, one codegen unit and `panic = "abort"`; `dev` with dependencies at
`opt-level = 3`; `profiling`, with full debug info; `release-fast`, thin LTO for
quicker iteration; and `bench` and `test` beside them.

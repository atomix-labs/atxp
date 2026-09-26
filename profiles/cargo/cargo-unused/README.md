# `cargo-unused`

Dependencies no crate uses. cargo-machete reads the sources, so it is fast, and
a macro can fool it; cargo-shear reads the compiled graph, so it is thorough,
and it catches workspace dependencies no member inherits too. Each is a feature,
`machete` and `shear`, both on by default: `check-cargo-unused` runs the ones
that are on, and `fix-cargo-unused` removes what they find. Both are built with
cargo, so their pins lock no platform.

<!-- facts: written by scripts/catalog.py -->
<!-- /facts -->

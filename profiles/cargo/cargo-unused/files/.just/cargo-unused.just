# Fails on a dependency no crate uses.
check-cargo-unused:
    cargo machete

# Removes each dependency no crate uses.
fix-cargo-unused:
    cargo machete --fix

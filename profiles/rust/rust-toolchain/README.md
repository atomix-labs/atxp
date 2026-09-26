# `rust-toolchain`

The toolchain a checkout builds with: one pinned nightly, with `rust-src`,
rustfmt, clippy, miri, `rustc-dev` and `llvm-tools`, on rustup's minimal
profile, and rustup itself where it is missing. The nightly moves weekly with
atxp's `bump-rust-toolchain`, to the newest nightly of the last fourteen days
that has every component on every platform the locks cover, never backwards; a
repository takes it with `devset update`.

`.just/rust-toolchain.sh` installs rustup with rustup's own installer where it
is missing, with no default toolchain and without editing shell profiles, then
runs `rustup toolchain install`, which installs the toolchain
`rust-toolchain.toml` names, its components included; rustup verifies every
toolchain it downloads. mise runs it as a `preinstall` hook, before it installs
any tool: the tools it builds with cargo need the toolchain, and several builds
at once would each start to install it, over one another. `just setup` runs it
again, as `setup-rust-toolchain`, for a toolchain a bump has moved. Cargo's bin
directory, `$CARGO_HOME/bin`, joins mise's PATH, so wherever mise is active (a
shell, a task, `mise exec`, CI through mise-action) `cargo` and `rustc` are
found without a line in the shell's rc.

It owns those keys of `rust-toolchain.toml`: `targets` stays the repository's.
`.just/rust-toolchain.just` exports `CARGO_BUILD_TARGET` as the host's triple,
so every cargo command names its target and keeps `RUSTFLAGS` off host build
scripts, which a build under `target-cpu=native` can break; a recipe whose
output must land in `target/doc` rather than `target/<triple>/doc` unsets it.

<!-- facts: written by scripts/catalog.py -->
<!-- /facts -->

# Checks that every TOML file is formatted.
check-toml:
    RUST_LOG=warn taplo fmt --check

# Formats every TOML file.
fix-toml:
    RUST_LOG=warn taplo fmt

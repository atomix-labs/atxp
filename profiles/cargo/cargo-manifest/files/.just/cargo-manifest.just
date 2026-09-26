# Holds every crate manifest to one shape: what taplo, which reads values, cannot see.
check-cargo-manifest:
    mise exec -- python3 .just/cargo-manifest.py

# Builds every crate's documentation, private items included; a warning, such as a broken link,
# fails.{% if "strict" in devset.features %} Then the house's doc lint, over every crate.{% endif %}
check-rust-doc:
    RUSTDOCFLAGS="-D warnings" cargo doc --workspace --all-features --no-deps --document-private-items
{%- if "strict" in devset.features %}
    mise exec -- python3 -B .just/rust-doc.py --workspace
{%- endif %}

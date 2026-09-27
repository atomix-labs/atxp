# In its layout, with `format`; valid, and true to its schema where taplo.toml names one, with
# `lint`.

# Checks every TOML file.
check-toml:
{%- if "format" in devset.features %}
    RUST_LOG=warn taplo fmt --check
{%- endif %}
{%- if "lint" in devset.features %}
    RUST_LOG=warn taplo lint
{%- endif %}
{%- if "format" in devset.features %}

# Formats every TOML file.
fix-toml:
    RUST_LOG=warn taplo fmt
{%- endif %}

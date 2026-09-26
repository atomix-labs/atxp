# Fails on a dependency no crate uses, by each tool the profile's features turn on, and names each
# tool that found one.
check-cargo-unused:
    #!/usr/bin/env bash
    set -euo pipefail
    failed=()
{%- if "machete" in devset.features %}
    cargo machete || failed+=(cargo-machete)
{%- endif %}
{%- if "shear" in devset.features %}
    cargo shear || failed+=(cargo-shear)
{%- endif %}
{%- raw %}
    (( ${#failed[@]} == 0 )) || { echo "failed: ${failed[*]}" >&2; exit 1; }
{%- endraw %}

# Removes each dependency no crate uses, by each tool the profile's features turn on.
fix-cargo-unused:
{%- if "machete" in devset.features %}
    cargo machete --fix
{%- endif %}
{%- if "shear" in devset.features %}
    cargo shear --fix
{%- endif %}

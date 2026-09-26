{%- set md = devset.layers | selectattr("profile", "equalto", "markdown") | map(attribute="features") | first | default([]) -%}
# A collection's payloads are templates, not configuration for the directories they are in: dprint
# reads no configuration below the root.
export DPRINT_CONFIG_DISCOVERY := "ignore-descendants"

# Checks the catalog and every profile's facts are current, and every profile keeps the collection's
# rules; with `pins`, also every pin locked for every platform, and every dprint plugin checksummed.
check-devset-collection:
    mise exec -- python3 -B .just/devset-collection/catalog.py --check{% if "format" in md %} --dprint{% endif %}
{%- if "pins" in devset.features %}
    mise exec -- python3 -B .just/devset-collection/pins.py check
{%- endif %}

# Writes the catalog and every profile's facts.
fix-devset-collection:
    mise exec -- python3 -B .just/devset-collection/catalog.py{% if "format" in md %} --dprint{% endif %}
{%- if "pins" in devset.features %}

# Moves every pin and dprint plugin past the cooldown, and relocks what moved for every platform.
bump-devset-collection:
    mise exec -- python3 -B .just/devset-collection/pins.py bump "${BUMP_REPORT_DIR:+$BUMP_REPORT_DIR/devset-collection.md}"
{%- endif %}

# Tests every profile: alone, then each bundle and all at once on each fixture, with `just check`.
test-devset-collection:
    mise exec -- bash .just/devset-collection/suite.sh

{%- set md = devset.layers | selectattr("profile", "equalto", "markdown") | map(attribute="features") | first | default([]) -%}
{%- set site = " --site catalog --repository " ~ repository if "site" in devset.features else "" -%}
# A collection's payloads are templates, not configuration for the directories they are in: dprint
# reads no configuration below the root.
export DPRINT_CONFIG_DISCOVERY := "ignore-descendants"

# With `pins`, also every pin locked for every platform, and every dprint plugin checksummed; with
# `site`, the catalog site's pages too, and the site builds where it has them: a collection with no
# profiles yet has none.

# Checks the catalog and every profile's facts are current, and every profile keeps the rules.
check-devset-collection:
    mise exec -- python3 -B .just/devset-collection/catalog.py --check{% if "format" in md %} --dprint{% endif %}{{ site }}
{%- if "pins" in devset.features %}
    mise exec -- python3 -B .just/devset-collection/pins.py check
{%- endif %}
{%- if "site" in devset.features %}
    test ! -f catalog/src/SUMMARY.md || mdbook build catalog
{%- endif %}

# Writes the catalog and every profile's facts.
fix-devset-collection:
    mise exec -- python3 -B .just/devset-collection/catalog.py{% if "format" in md %} --dprint{% endif %}{{ site }}
{%- if "pins" in devset.features %}

# Moves every pin and dprint plugin past the cooldown, and relocks what moved for every platform.
bump-devset-collection:
    mise exec -- python3 -B .just/devset-collection/pins.py bump "${BUMP_REPORT_DIR:+$BUMP_REPORT_DIR/devset-collection.md}"
{%- endif %}

# Tests every profile: alone, then each bundle and all at once on each fixture, with `just check`.
test-devset-collection:
    mise exec -- bash .just/devset-collection/suite.sh

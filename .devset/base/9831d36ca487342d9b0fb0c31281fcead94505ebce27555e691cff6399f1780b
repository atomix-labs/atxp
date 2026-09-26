# Checks the catalog and every profile's facts are current, and every profile keeps the collection's
# rules; with `pins`, also every pin locked for every platform, and every dprint plugin checksummed.
check-devset-collection:
    mise exec -- python3 .just/devset-collection/catalog.py --check --dprint
    mise exec -- python3 .just/devset-collection/pins.py check

# Writes the catalog and every profile's facts.
fix-devset-collection:
    mise exec -- python3 .just/devset-collection/catalog.py --dprint

# Moves every pin and dprint plugin past the cooldown, and relocks what moved for every platform.
bump-devset-collection:
    mise exec -- python3 .just/devset-collection/pins.py bump "${BUMP_REPORT_DIR:+$BUMP_REPORT_DIR/devset-collection.md}"

# Tests every profile: alone, then each bundle and all at once on each fixture, with `just check`.
test-devset-collection:
    mise exec -- bash .just/devset-collection/suite.sh

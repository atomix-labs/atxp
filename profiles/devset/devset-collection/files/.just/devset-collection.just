# Checks every profile's pins are locked for every platform, and every dprint plugin checksummed.
check-devset-collection:
    mise exec -- python3 .just/devset-collection.py check

# Moves every profile's pins and dprint plugins past the cooldown, and relocks what moved.
bump-devset-collection:
    mise exec -- python3 .just/devset-collection.py bump "${BUMP_REPORT_DIR:+$BUMP_REPORT_DIR/profile-pins.md}"

# Checks every profile's pins are locked for every platform, and every dprint plugin checksummed.
check-profile-pins:
    mise exec -- python3 .just/profile-pins.py check

# Moves every profile's pins and dprint plugins past the cooldown, and relocks what moved.
bump-profile-pins:
    mise exec -- python3 .just/profile-pins.py bump "${BUMP_REPORT_DIR:+$BUMP_REPORT_DIR/profile-pins.md}"

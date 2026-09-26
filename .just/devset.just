# Fails when a file devset manages has drifted from its profile, or an update is unfinished.
check-devset:
    devset status --exit-code

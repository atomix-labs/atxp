# Builds the workspace's binaries for this machine into dist/, each archived with its sha256{% if "completions" in devset.features %} and its shell completions{% endif %}.
package-cargo-binaries:
    bash .just/cargo-binaries.sh{% if "completions" in devset.features %} --completions{% endif %}

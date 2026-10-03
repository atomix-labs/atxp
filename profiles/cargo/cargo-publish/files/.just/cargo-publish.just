{%- set owner = repository | split("/") | first -%}
{%- set repo = repository | split("/") | last -%}
# Holds every crate crates.io would publish to what its page shows, then packages and builds it.
[metadata("rust")]
check-cargo-publish:
    mise exec -- python3 .just/cargo-publish.py metadata{% if "mdbook" in devset.profiles %} --book https://{{ owner }}.github.io/{{ repo }}/{% endif %}
    mise exec -- python3 .just/cargo-publish.py check

# Publishes every crate crates.io does not have at its version yet, dependencies first.
publish-cargo-publish:
    mise exec -- python3 .just/cargo-publish.py publish

{%- set templates = devset.layers | selectattr("profile", "equalto", "github-templates") | map(attribute="features") | first | default([]) -%}
{%- set book = devset.layers | selectattr("profile", "equalto", "mdbook") | list -%}
{%- set owner = repository | split("/") | first -%}
{%- set repo = repository | split("/") | last -%}
# Support

Where to take what you have, so it reaches the right place:
{% if book %}
- **The documentation first:** the [book][book] may answer it already.
{%- endif %}
{%- if "discussions" in templates %}
- **A question**, or an idea to talk over: [Discussions][discussions].
{%- endif %}
- **A bug, or a feature to request:** [an issue][issue], whose form asks for
  what a maintainer needs.
- **A vulnerability:** never an issue. [Report it privately][advisory].
{% if book %}
[book]: https://{{ owner }}.github.io/{{ repo }}/
{%- endif %}
{%- if "discussions" in templates %}
[discussions]: https://github.com/{{ repository }}/discussions
{%- endif %}
[issue]: https://github.com/{{ repository }}/issues/new/choose
[advisory]: https://github.com/{{ repository }}/security/advisories/new

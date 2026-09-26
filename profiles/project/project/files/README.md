{%- set p = devset.profiles -%}
{%- set crates = "cargo-publish" in p and "cargo-workspace" in p -%}
{%- set badges = [
  ["github-ci" in p, "[![CI][c1]][c2]"],
  [crates, "[![crates.io][r1]][r2] [![docs.rs][d1]][d2]"],
  ["mdbook" in p, "[![Book][b1]][b2]"],
] -%}
{%- set line -%}
{%- for badge in badges if badge[0] %}{{ badge[1] }}{% if not loop.last %} {% endif %}{% endfor -%}
{%- endset -%}
{%- if line %}
{{ line }}
{% if "github-ci" in p %}
[c1]: https://img.shields.io/github/actions/workflow/status/{{ repository }}/check.yml?branch=main&style=flat-square&label=check
[c2]: https://github.com/{{ repository }}/actions/workflows/check.yml
{%- endif %}
{%- if crates %}
[r1]: https://img.shields.io/crates/v/{{ name or devset.target }}?style=flat-square
[r2]: https://crates.io/crates/{{ name or devset.target }}
[d1]: https://img.shields.io/docsrs/{{ name or devset.target }}?style=flat-square
[d2]: https://docs.rs/{{ name or devset.target }}
{%- endif %}
{%- if "mdbook" in p %}
[b1]: https://img.shields.io/badge/book-read-blue?style=flat-square
[b2]: https://{{ repository | split("/") | first }}.github.io/{{ repository | split("/") | last }}/
{%- endif %}
{% else %}
{%- endif %}

{%- set p = devset.profiles -%}
{%- set crates = "cargo-publish" in p and "cargo-workspace" in p -%}
{%- set published = crate or name or devset.target -%}
{%- set title = name or devset.target -%}
{%- set owner = repository | split("/") | first -%}
{%- set repo = repository | split("/") | last -%}
<!-- dprint-ignore-start -->
{% if logo %}
<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="{{ logo }}-dark.svg">
    <img alt="{{ title }}" src="{{ logo }}-light.svg" height="56">
  </picture>
</h1>
{%- else %}
<h1 align="center">{{ title }}</h1>
{%- endif %}
{%- if description %}

<p align="center">{{ description }}</p>
{%- endif %}
{%- if "github-ci" in p or crates or "mdbook" in p or "devset-badge" in devset.features %}

<p align="center">
{%- if "github-ci" in p %}
  <a href="https://github.com/{{ repository }}/actions/workflows/check.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/{{ repository }}/check.yml?branch=main&amp;style=flat-square&amp;label=check"></a>
{%- endif %}
{%- if crates %}
  <a href="https://crates.io/crates/{{ published }}"><img alt="crates.io" src="https://img.shields.io/crates/v/{{ published }}?style=flat-square"></a>
  <a href="https://docs.rs/{{ published }}"><img alt="docs.rs" src="https://img.shields.io/docsrs/{{ published }}?style=flat-square"></a>
{%- endif %}
{%- if "mdbook" in p %}
  <a href="https://{{ owner }}.github.io/{{ repo }}/"><img alt="Book" src="https://img.shields.io/badge/book-read-blue?style=flat-square"></a>
{%- endif %}
{%- if "devset-badge" in devset.features %}
  <a href="https://github.com/atomix-labs/devset"><img alt="managed with devset" src="https://img.shields.io/badge/managed_with-devset-0969da?style=flat-square&amp;logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+PHRpdGxlPmRldnNldDwvdGl0bGU+PHBhdGggZmlsbD0iI2YwZjZmYyIgZD0ibTE2IDMgMTMgNi41TDE2IDE2IDMgOS41WiIvPjxwYXRoIGZpbGw9Im5vbmUiIHN0cm9rZT0iI2YwZjZmYyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBzdHJva2Utd2lkdGg9IjIuNSIgZD0ibTMgMTYgMTMgNi41TDI5IDE2TTMgMjIuNSAxNiAyOWwxMy02LjUiLz48L3N2Zz4K"></a>
{%- endif %}
</p>
{%- endif %}

<!-- dprint-ignore-end -->

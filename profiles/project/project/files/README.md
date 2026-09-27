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
{%- if "github-ci" in p or crates or "mdbook" in p %}

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
</p>
{%- endif %}

<!-- dprint-ignore-end -->

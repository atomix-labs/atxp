{%- set pitch = description | trim | trim(".") or "what the project does" -%}
{%- set lints = devset.layers | selectattr("profile", "equalto", "rust-lints") | map(attribute="features") | first | default([]) -%}
//! {{ pitch[:1] | upper }}{{ pitch[1:] }}.
//!
//! Say here the problem it solves, the one type or function a reader meets first, and what it
//! leaves out. The manifest's `description` is the line above, its first letter lowercased.
{%- if "strict" in lints %}

#![no_std]
{%- endif %}
{%- if kind in ["bin", "both"] %}

/// Does the crate's work for its command line, which calls it.
pub const fn run() {}
{%- endif %}

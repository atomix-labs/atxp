
## Before You Commit

Run `just check`: CI runs the same checks, and names each that fails. `just fix`
fixes what a formatter or linter can, and `just --list` shows every recipe.
{#- Before You Finish names each pass the repository has, one to a line under what ships it, and
    shows only where one is on. A new pass edits two places: `passes`, joining its own test with
    `or`, and its item in the list. #}
{%- set lints = devset.layers | selectattr("profile", "equalto", "rust-lints") | map(attribute="features") | first | default([]) %}
{%- set passes = "agents" in lints or "readability" in devset.features or "security" in devset.features %}
{%- if passes %}

## Before You Finish

A change beyond a line or two is ready when its passes have run and `just check`
passes:
{# The passes, one to a line. #}
{%- if "agents" in lints %}
- `/review-rust` on a change to Rust code.
{%- endif %}
{%- if "readability" in devset.features %}
- `/review-names` on a change that adds, renames or changes what a public item
  does.
{%- endif %}
{%- if "security" in devset.features %}
- `/review-security` on a change that reads input from outside the process.
{%- endif %}

Each runs in a fresh context and reports; fix what it finds, or say why a
finding does not hold.
{%- endif %}

## Managed Files

Profiles, applied by devset, manage some of the files here. `devset status`
names each, and whether a local change to it is kept or is drift; `devset
explain <file>` says which profile owns what in it. What a profile owns changes
with the profile, on `devset update`. Never edit `.devset/`.


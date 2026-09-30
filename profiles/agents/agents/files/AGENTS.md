
## Before You Commit

Run `just check`: CI runs the same checks, and names each that fails. `just fix`
fixes what a formatter or linter can, and `just --list` shows every recipe.
{#- Before You Finish names each pass the repository has, one to a line under what ships it, and
    shows only where one is on. A new pass edits two places: its own test, joined with `or` to
    `reviews` for a pass that only reports, or to `passes` for one that edits, and its item in the
    list. #}
{%- set lints = devset.layers | selectattr("profile", "equalto", "rust-lints") | map(attribute="features") | first | default([]) %}
{%- set reviews = "agents" in lints or "readability" in devset.features or "security" in devset.features %}
{%- set passes = reviews or "readability" in devset.features %}
{%- if passes %}

## Before You Finish

A change beyond a line or two is ready when its passes have run and `just check`
passes:
{# The passes, one to a line. #}
{%- if "readability" in devset.features %}
- `/humanize` on what the change says to a reader: its comments, docs, names and
  messages.
{%- endif %}
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
{%- if "readability" in devset.features %}
{%- if reviews %}

Each runs in a fresh context and reports: `/humanize` edits, then says what it
changed and what it left, and a review says what it found. Fix what a pass
leaves or finds, or say why a finding does not hold.
{%- else %}

It runs in a fresh context, edits, then says what it changed and what it left.
Fix what it leaves, or say why a tell it left needs no fix.
{%- endif %}
{%- else %}

Each runs in a fresh context and reports; fix what it finds, or say why a
finding does not hold.
{%- endif %}
{%- endif %}

## Managed Files

Profiles, applied by devset, manage some of the files here. `devset status`
names each, and whether a local change to it is kept or is drift; `devset
explain <file>` says which profile owns what in it. What a profile owns changes
with the profile, on `devset update`. Never edit `.devset/`.


{%- set crate = name or devset.target -%}
{%- set pitch = description | trim | trim(".") or "what the project does" -%}
{%- set lints = devset.layers | selectattr("profile", "equalto", "rust-lints") | map(attribute="features") | first | default([]) -%}
//! {{ pitch[:1] | upper }}{{ pitch[1:] }}, from the command line.
//!
//! ```text
//! {{ crate }}
//! ```
{% if "strict" in lints %}
#[cfg_attr(
    test,
    expect(
        clippy::missing_const_for_fn,
        reason = "the entry point, which the test harness replaces, cannot be `const`"
    )
)]
{%- endif %}
fn main() {
    {{ crate | replace("-", "_") }}::run();
}

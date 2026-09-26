//! The {{ name or devset.target }} crate.
//!
//! Say here what the crate is for, the one type or function a reader meets first, and what it
//! deliberately leaves out.
{%- if kind in ["bin", "both"] %}

/// Does the crate's work for its command line, which calls it.
pub const fn run() {}
{%- endif %}

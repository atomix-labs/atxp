//! The binary of a workspace the profiles are applied to.

#![feature(non_exhaustive_omitted_patterns_lint, strict_provenance_lints)]

use std::io::{self, Write as _};

/// Writes the sum of two and two.
fn main() -> io::Result<()> {
    writeln!(io::stdout(), "{:?}", fixture_core::add(2, 2))
}

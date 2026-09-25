//! A crate the profiles are applied to.

/// The sum of `a` and `b`, or `None` where it overflows.
///
/// ```
/// assert_eq!(fixture::add(2, 2), Some(4));
/// ```
#[must_use]
pub const fn add(a: u64, b: u64) -> Option<u64> {
    a.checked_add(b)
}

#[cfg(test)]
mod tests {
    //! The sum, checked.

    #[test]
    fn adds() {
        assert_eq!(super::add(1, 2), Some(3), "one and two make three");
    }
}

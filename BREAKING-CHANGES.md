# Breaking Changes

A migration note for every breaking change, newest release first: what changed,
why, and what a repository does about it. [CHANGELOG.md](CHANGELOG.md) lists
every change; this lists only those a repository must act on.

## Summary

- [v0.2.0](#v020)
  - `lints` no longer carries the two lints only nightly has

## V0.2.0

### `lints` No Longer Carries the Two Lints Only Nightly Has

`non_exhaustive_omitted_patterns` and `implicit_provenance_casts` need a
`#![feature]` in every crate, which no stable toolchain accepts, so a crate
under the wall could not build on stable. They moved to `lints-nightly`, whose
`check-lints-nightly` runs them without one. The `rust` bundle requires both, so
a repository that takes the bundle keeps every lint and drops its `#![feature]`
lines. One that requires `lints` alone adds `lints-nightly`:

```diff
 requires = [
     { git = "https://github.com/atomix-labs/atxp", tag = "v0.2.0", path = "profiles/lints" },
+    { git = "https://github.com/atomix-labs/atxp", tag = "v0.2.0", path = "profiles/lints-nightly" },
 ]
```

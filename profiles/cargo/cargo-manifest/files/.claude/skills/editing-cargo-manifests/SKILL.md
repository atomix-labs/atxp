---
name: editing-cargo-manifests
description: Use when creating a crate, or writing, reviewing or cleaning any `Cargo.toml` in the workspace; when adding, removing or re-pinning a dependency; when adding or reshaping a `[features]` table, or deciding between a feature, an optional dependency and a separate crate; when adding a proc-macro crate; when declaring a `[[bench]]`, `[[bin]]`, `[[example]]` or `[lib]` target; when `std` reaches a `no_std` crate through a default; when the manifest check or the unused-dependency check reports a finding. Covers the manifest's shape, dependencies and their inheritance, features and defaults, and targets.
---

# Editing Cargo Manifests

How a crate's `Cargo.toml` is written in this workspace. A manifest is a
declaration: what the crate is, what it may reach, and what a consumer may
switch on; explanation lives in the crate's docs. taplo settles the layout, and
`.just/cargo-manifest.py` the text around the values; neither decides what
belongs in the crate, which is most of this skill. The rules below are the whole
of it, each with its reason; `references/sources.md` holds the Cargo
documentation behind each.
{%- set lints = devset.layers | selectattr("profile", "equalto", "rust-lints") | map(attribute="features") | first | default([]) %}
{%- set rustdoc = devset.layers | selectattr("profile", "equalto", "rust-doc") | map(attribute="features") | first | default([]) %}

## Rules

### The Shape

1. **Tables in one order, each written only when it has something to say, but
   `[package]` and `[lints]`**, so a reader finds each where it always is:
   `[package]`, any `[package.metadata.*]`, `[features]`, `[lints]`, the
   targets, then `[dependencies]`, `[dev-dependencies]`, `[build-dependencies]`
   and each `[target.'cfg(…)'.dependencies]`.
2. **`[package]` reads `name`, `description`, then the keys the workspace sets,
   each `<key>.workspace = true`: `version`, `edition`, `rust-version`,
   `license`, `authors`, then `publish` or `repository`**, so a crate says only
   its name and pitch, and one edit to the workspace moves every crate.
3. **Every crate has `[lints] workspace = true`, and nothing else under
   `[lints]`**, so no crate leaves the shared lints without anyone deciding it
   should.
4. **Every `[features]` table opens with `default`, even `default = []`**, the
   manifest's word that nothing else is on by default.
5. **No comment but the group markers, `# external` then `# internal`, each once
   and bare, inside a dependency table**; a reason worth keeping goes in the
   crate's docs, a feature's in its `# Crate features` table and a target's in
   its file's `//!`.
6. **Nothing Cargo finds or defaults to by itself**: no `[lib]` or `[[bin]]`
   that restates `src/lib.rs` or `src/main.rs`, no `build = "build.rs"`, no
   `autobins` or its kin, and no `documentation`, since crates.io links docs.rs
   without it.

```toml
[package]
name                   = "tiles-paint"
description            = "brushes that paint tiles onto a board, one square at a time."
version.workspace      = true
edition.workspace      = true
rust-version.workspace = true
license.workspace      = true
authors.workspace      = true

[features]
default = []

serde = ["dep:serde", "tiles-geometry/serde"]

[lints]
workspace = true

[[bench]]
name    = "strokes"
harness = false

[dependencies]
# external
serde     = { workspace = true, optional = true }
thiserror = { workspace = true }
# internal
tiles-geometry = { workspace = true }

[dev-dependencies]
# external
divan = { workspace = true }
```

### Dependencies

1. **Every version lives in `[workspace.dependencies]`, external and internal
   alike, with its `default-features` and the features every member needs; a
   member writes `name = { workspace = true }`, adding at most `features` and
   `optional`, in that order**, so one edit moves every crate; Cargo refuses any
   other key on an inherited dependency.
2. **An internal crate is listed in `[workspace.dependencies]` with its `path`
   and `version`, under `# internal`, and every member inherits it**; the
   manifest check refuses a `path` to a listed crate, and one that leaves the
   member's own directory.
3. **A proc-macro crate sits in its parent's `macros/`, beside a plain library
   holding its token logic, and each reaches the next by `path`**, since a
   `proc-macro = true` crate exports its macros alone and its logic is tested
   through the library; a `path` into the crate's own tree, to a crate the
   workspace does not list, is the one a member writes.
4. **A dependency's default is turned off where it would reach a crate that does
   not want it: an external crate a `no_std` member uses has `default-features =
   false` on its workspace entry**, since Cargo unifies a dependency's features
   across the build, and an override in one member protects that member alone.

### Features

1. **A feature is justified by exactly one of three things: a dependency not
   every user should pay for, a capability the target may not have, `std` or a
   syscall, or a hook only tests need**; a second way of doing the crate's one
   job is not a feature, and a switch that changes what the crate is makes a
   second crate.
2. **Features only add**, since Cargo unifies them across the whole build: a
   `no-std` or `disable-x` feature that one crate turns on takes something from
   every other, and two features that cannot both be on are a defect, so the
   crate splits. Name the thing, `std`, not the switch, `use-std`.
3. **`dep:` on every optional dependency, `serde = ["dep:serde"]`**, since
   without it Cargo makes the dependency's name a public feature, and swapping
   the crate a breaking change.
4. **A feature forwards a dependency's by name, after its `dep:` entries**, as
   `std = ["tiles-geometry/std"]`, or `serde?/std` where `serde` is optional,
   since a dependency's feature is on only where some crate turns it on.
5. **`default` stays small, `[]` unless the crate is no use without something**,
   since a consumer escapes a default only with `default-features = false`, and
   every crate on the way must remember to.
6. **Each feature is permanent**: removing one, or taking it out of `default`,
   breaks the users who rely on it, and each multiplies the builds a feature
   sweep runs.
{%- if "strict" in lints %}

### Std Is the Opt-In

Under `strict`, a library is `no_std` first:

1. **A library writes `#![no_std]` unconditionally, never `cfg_attr`-ed on, and
   `extern crate alloc;` where it allocates**, so a use of `std` is gated on
   purpose and never compiles the day something unifies `std` on.
2. **`std` is a feature that only adds, and never in `default`**, forwarded to
   each dependency that has its own; a crate that is `std`-only by nature, a
   binary, a proc-macro crate or one that owns the syscalls, has no `std`
   feature at all.
{%- endif %}

### Targets

`src/lib.rs`, `src/main.rs`, `tests/*.rs`, `benches/*.rs` and `examples/*.rs`
are found without a table; one is written only for a key that is not its
default:

| written                                                                      | when                                                                                    |
| ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `[lib] proc-macro = true`                                                    | a proc-macro crate                                                                      |
| `[[bench]] name`, `harness = false`                                          | a bench that owns its `main`, as divan's and criterion's do                             |
| `[lib] bench = false`                                                        | such benches take flags that libtest's harness in the library refuses                   |
| `[[bin]] name`, `path`                                                       | a binary named other than its package, or than its file in `src/bin/`                   |
| `required-features` on a `[[bin]]`, `[[example]]`, `[[test]]` or `[[bench]]` | a target that needs a feature the crate does not default to; it does nothing on `[lib]` |

## Steps

1. **A new crate**: its directory where the workspace's `members` finds it, its
   `Cargo.toml` in the shape above, and its entry in `[workspace.dependencies]`
   once another crate uses it{% if "agents" in rustdoc %}; its `description` is the crate summary's pitch
   clause, as `writing-rustdoc` words it{% endif %}.
2. **A dependency**: its entry in `[workspace.dependencies]` under its group,
   with its version and `default-features`, then `{ workspace = true }` in the
   member, with `features` or `optional` where the member needs them.
3. **A feature**: which of the three earns it; `dep:` for an optional
   dependency; the features it forwards; its row in the crate docs' `# Crate
   features` table.
4. **A proc-macro crate**: the pair under the parent's `macros/`, each reached
   by `path`, the macro crate's `[lib] proc-macro = true`.
5. **A target**: only a key that is not its default, from the table above.
6. **A finding**: `just fix` puts each dependency under its group; the rest is
   fixed by hand, as the finding names it.
7. **Before finishing**: `just fix`, then the checks below until they pass.

## Checks

- `just check-cargo-manifest`: the shape above, every internal dependency
  inherited, and every crate on the workspace's lints; `mise exec -- python3
  .just/cargo-manifest.py <path>` checks one manifest.
{%- if "toml" in devset.profiles %}
- `just check-toml`: taplo's layout, each dependency group in alphabetical
  order.
{%- endif %}
{%- if "cargo-unused" in devset.profiles %}
- `just check-cargo-unused`: a dependency nothing uses, or one in the wrong
  table. Where one is reached only through a macro's expansion, both scanners
  are told, in `[package.metadata.cargo-machete]` and
  `[package.metadata.cargo-shear]`, `ignored = ["<name>"]`.
{%- endif %}
{%- if "cargo-deny" in devset.profiles %}
- `just check-cargo-deny`: advisories, licences, bans and sources.
{%- endif %}
{%- if "cargo-hack" in devset.profiles %}
- `just nightly-cargo-hack`: every feature builds alone.
{%- endif %}
- `just check`: all of them. `cargo tree -e features -i <crate>` says who turned
  a feature on.

## What Not to Do

| Thought                                                       | Instead                                                              |
| ------------------------------------------------------------- | -------------------------------------------------------------------- |
| "This dependency's purpose is not obvious; a `#` gloss helps" | No comment: the crate docs say it, where its guarantee is used.      |
| "A paragraph above `[[bench]]` says why it has no harness"    | The bench's `//!` says it.                                           |
| "No feature is on by default, so `default` can go"            | `default = []` is the declaration that none is. Write it.            |
| "`default-features = false` here keeps `std` out"             | It keeps it out of this crate alone: put it on the workspace entry.  |
| "A `no-std` feature reads clearer"                            | Features only add: name the thing, `std`.                            |
| "Two features that conflict; a `compile_error!` will say so"  | Split the crate: the `compile_error!` is the last resort.            |
| "An optional dependency's implicit feature is fine"           | `dep:`, so the crate's name is not a public feature.                 |
| "One more feature is small"                                   | It is permanent, unifies across the build, and multiplies the sweep. |
| "Pin the version here; only this crate uses it"               | Until a second does: `[workspace.dependencies]`.                     |
| "`path = "../tiles-geometry"` is simpler"                     | `{ workspace = true }`; a `path` is for a crate inside this one.     |
| "`[lib] path = "src/lib.rs"`, to be explicit"                 | Cargo finds it: write only a key that is not the default.            |
| "Remove the workspace entry the check says is unused"         | Ask first whether a crate is about to use it.                        |
| "`taplo fmt` passed, so the manifest is clean"                | taplo never sees a comment: run the manifest check.                  |

## References

Read the reference before citing a source for a rule, or where Cargo's own
documentation seems to say otherwise, and again after compaction.

- `references/sources.md`: the Cargo documentation and tools behind each rule,
  where measurement disagrees with them, and what this workspace settles that
  the ecosystem contests.

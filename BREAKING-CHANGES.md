# Breaking Changes

A migration note for every breaking change, newest release first: what changed,
why, and what a repository does about it. [CHANGELOG.md](CHANGELOG.md) lists
every change; this lists only those a repository must act on.

## Summary

- [v0.5.0](#v050)
  - [atxp needs devset 0.2.2](#atxp-needs-devset-022)
  - [`check-mdbook` lints the book, and builds the API](#check-mdbook-lints-the-book-and-builds-the-api)
  - [A site is published only under `pages`](#a-site-is-published-only-under-pages)
  - [The doc lint runs under `strict`](#the-doc-lint-runs-under-strict)
  - [`rustfmt.toml` is the profile's keys, under merge](#rustfmttoml-is-the-profiles-keys-under-merge)
  - [`.cargo/config.toml` sets CPU floors](#cargoconfigtoml-sets-cpu-floors)
- [v0.4.0](#v040)
  - [atxp needs devset 0.2.1](#atxp-needs-devset-021)
  - [Profiles are renamed, and grouped by umbrella](#profiles-are-renamed-and-grouped-by-umbrella)
  - [The bundle takes the core, and features the rest](#the-bundle-takes-the-core-and-features-the-rest)
  - [The house policy is the `strict` feature](#the-house-policy-is-the-strict-feature)
  - [Shared files follow the profiles applied](#shared-files-follow-the-profiles-applied)
  - [A collection's tooling is `devset-collection`](#a-collections-tooling-is-devset-collection)
- [v0.2.0](#v020)
  - `lints` no longer carries the two lints only nightly has

## V0.5.0

### atxp Needs devset 0.2.2

**What changed.** Every profile requires devset 0.2.2, which writes an array of
TOML tables a profile changes as the payload writes it: under 0.2.1, turning on
`toml`'s `schemas` in a repository that has a `taplo.toml` left the file failing
`taplo fmt --check`. The `devset` profile pins 0.2.2.

**What to do.** Take the update with devset 0.2.2, since 0.2.1 refuses a profile
that requires a later release; the pin then moves every machine and job:

```sh
mise exec github:atomix-labs/devset@0.2.2 -- devset update
```

### `check-mdbook` Lints the Book, and Builds the API

**What changed.** `mdbook` scaffolds a book where there is none, and
`check-mdbook` first runs a docs lint: every page listed in `SUMMARY.md`, every
include and anchor, every recipe a page names. With its default features it also
builds the workspace's API with nightly rustdoc, at `/api`, and checks every
link of the built book with lychee. `book.toml`'s `[output.html]` keys and the
theme are the profile's, under merge.

**What to do.** Fix what the lint names. A book that should have neither the API
nor the link check applies `mdbook` as a layer of its own, rather than through
the bundle's `docs`, with the features it keeps:

```toml
[[layers]]
profile          = "atxp/mdbook"
default-features = false
features         = ["katex", "pages"]
```

### A Site Is Published Only Under `pages`

**What changed.** `github-ci`'s `check` workflow builds and deploys a site to
GitHub Pages only with its new feature `pages`, which `mdbook`'s default `pages`
turns on.

**What to do.** Nothing for a book. A repository that publishes a site of its
own turns the feature on, in a layer of its own:

```toml
[[layers]]
profile  = "atxp/github-ci"
features = ["pages"]
```

### The Doc Lint Runs Under `strict`

**What changed.** Under `rust-doc`'s `strict`, which the bundle's `strict` turns
on, `check-rust-doc` also runs the house's doc lint over every crate. The
`writing-rustdoc` skill's `scripts/doc-lint.py` is now `.just/rust-doc.py`.

**What to do.** Fix what the lint names, which `.just/rust-doc.py <crate-dir>`
lists, or leave `strict` off. A script of your own that ran `doc-lint.py` runs
`.just/rust-doc.py`.

### `rustfmt.toml` Is the Profile's Keys, Under Merge

**What changed.** `rust-fmt` owns the keys its payload names, under merge, not
the whole file; the options only nightly rustfmt has are written only where
`channel` is nightly.

**What to do.** Nothing, unless something relied on `devset apply --force`
restoring the whole file: an option the repository added is its own now, and
kept.

### `.cargo/config.toml` Sets CPU Floors

**What changed.** `cargo-workspace` owns keys of `.cargo/config.toml`, among
them CPU floors every build meets: x86-64-v2, CRC32 on Arm, and the first Apple
silicon.

**What to do.** A machine below a floor builds with `RUSTFLAGS` set to what it
has; a build tuned to its own machine sets `RUSTFLAGS="-C target-cpu=native"`,
which replaces them.

## V0.4.0

### atxp Needs devset 0.2.1

**What changed.** Every profile is written for devset 0.2: it requires others by
name, and may offer features and gates. Each requires devset 0.2.1, which writes
a JSON key a profile adds as the payload writes it. devset 0.2 reads no
`.devset/config.toml` written for 0.1. The new profile `devset` pins devset
0.2.1 for every machine and job, and `check-devset` fails on drift.

**What to do.** Install devset 0.2.1 or later, then write `.devset/config.toml`
again with atxp as a source, as devset's
[migration note](https://github.com/atomix-labs/devset/blob/main/BREAKING-CHANGES.md#profiles-are-named-in-sources)
says:

```toml
[sources]
atxp = { git = "https://github.com/atomix-labs/atxp", tag = "v0.4.0" }

[[layers]]
profile  = "atxp/rust"
features = ["agents", "nightly", "strict"]
```

Then run `devset apply`. devset reads the state it wrote as it is: each file an
old name wrote that no profile writes now is removed where it is unchanged, and
left untracked where it was edited, and `devset status` names both.

### Profiles Are Renamed, and Grouped by Umbrella

**What changed.** Each profile is named for its concern and lives in
`profiles/<umbrella>/<name>/`, and profiles that were one concern are one
profile, with a feature for each tool they held. Recipes and pin files follow
their profile's name: `check-taplo` is `check-toml`, `devset-taplo.toml` is
`devset-toml.toml`. Where profiles merged, one recipe runs each tool the
features turn on: `check-github-workflow-lint` runs actionlint, zizmor and
conftest.

| v0.3                                           | v0.4.0                       | Notes                                                                                                          |
| ---------------------------------------------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `actionlint`, `zizmor`, `conftest`, `policies` | `github-workflow-lint`       | features `actionlint`, `zizmor`, `policies`, all on                                                            |
| `ansible-lint`                                 | `ansible`                    |                                                                                                                |
| `automation`                                   | `github-automation`          |                                                                                                                |
| `cargo-machete`, `cargo-shear`                 | `cargo-unused`               | features `machete`, `shear`, both on                                                                           |
| `claude-skills`                                | `rust-doc`, `cargo-manifest` | each skill with its concern, under the feature `agents`; `writing-cargo-manifest` is `editing-cargo-manifests` |
| `clippy`                                       | `rust-clippy`                |                                                                                                                |
| `committed`                                    | `git-commits`                |                                                                                                                |
| `crates-io`                                    | `cargo-publish`              |                                                                                                                |
| `dependabot`                                   | `github-dependabot`          |                                                                                                                |
| `git-cliff`                                    | `git-changelog`              |                                                                                                                |
| `gitattributes`                                | `git-attributes`             |                                                                                                                |
| `gitignore`                                    | `git-ignore`                 | rumdl's and Python's lines move to `markdown` and `python`                                                     |
| `gitignore-rust`                               | `cargo-workspace`            | with the resolver key; the profiling lines go to `cargo-profiles`                                              |
| `lints`, `lints-nightly`                       | `rust-lints`                 | the nightly lints under the feature `nightly`                                                                  |
| `manifest-lint`, `cargo-workspace-lints`       | `cargo-manifest`             | one check, `check-cargo-manifest`                                                                              |
| `msrv`                                         | `rust-msrv`                  |                                                                                                                |
| `nextest`                                      | `cargo-nextest`              |                                                                                                                |
| `profile-pins`                                 | `devset-collection`          | under the feature `pins`                                                                                       |
| `ruff`                                         | `python`                     |                                                                                                                |
| `rumdl`                                        | `markdown`                   |                                                                                                                |
| `rustdoc`                                      | `rust-doc`                   |                                                                                                                |
| `rustfmt`                                      | `rust-fmt`                   |                                                                                                                |
| `rustup`, `rust-toolchain`                     | `rust-toolchain`             | `setup-rustup` is `setup-rust-toolchain`                                                                       |
| `shellcheck`                                   | `shell`                      |                                                                                                                |
| `taplo`                                        | `toml`                       |                                                                                                                |
| `typos`                                        | `spelling`                   |                                                                                                                |
| `vscode-rust`                                  | `vscode`                     |                                                                                                                |
| `yamllint`                                     | `yaml`                       |                                                                                                                |

Every other profile keeps its name. `devset` is new.

**What to do.** Name each layer, and each requirement of a profile of your own,
by its new name. A recipe of your own, or a CI step, that ran a renamed recipe
runs the new one.

### The Bundle Takes the Core, and Features the Rest

**What changed.** `rust` requires what every Rust repository has, and offers the
rest as features, none on by default: `docs` (mdbook), `agents` (the skills),
`publish` (cargo-publish and github-release), `binaries` (cargo-binaries and
github-release), `nightly` (the nightly lints, cargo-hack and github-nightly)
and `strict`. It no longer brings `python`, `vscode` or `suppressions`, and
brings `github-release` only with `publish` or `binaries`.

**What to do.** Turn on the features you want. To keep all that the v0.3 bundle
gave, add the rest as layers of their own:

```toml
[[layers]]
profile  = "atxp/rust"
features = ["agents", "nightly", "strict"]

[[layers]]
profile = "atxp/github-release"

[[layers]]
profile = "atxp/python"

[[layers]]
profile = "atxp/vscode"

[[layers]]
profile = "atxp/suppressions"
```

### The House Policy Is the `strict` Feature

**What changed.** The profiles' defaults suit any open-source Rust project. What
went beyond them is the feature `strict`, of three profiles: `cargo-deny`'s bans
on crates with a better choice, `rust-lints`' nursery, restriction lints and
`unsafe_code`, `missing_docs` and the rest of rustc's wall, and
`cargo-profiles`' `panic = "abort"` in `dev` and `release`.

**What to do.** To keep the house policy, turn `strict` on: the bundle's turns
on all three.

### Shared Files Follow the Profiles Applied

**What changed.** A file several profiles contribute to is written from the
profiles applied, not from what is on disk:

- The justfile imports the recipes of every profile applied, and `just test`
  runs every `test-*` recipe.
- dprint loads its Markdown, YAML and Ruff plugins, and formats those files,
  only where `markdown`, `yaml` or `python` is applied; each owns its settings
  in `dprint.json`.
- `release.yml` takes a crates.io token where `cargo-publish` is applied; its
  plan job no longer reports `crates-io`.
- `vscode` recommends and configures only the tools of the profiles applied.
- `typos.toml` and `dprint.json` no longer exclude `docs/book/`, `docs/theme/`
  or `docs/vendor/`: typos and dprint read `.gitignore`, where `mdbook` ignores
  the book.
- `github-ci` no longer takes `docs/book` as the site's path: a repository that
  names `pages.recipe` in `.github/automation.json` names `pages.path` too.
- `github-ci`, `github-nightly`, `github-bump` and `github-watch` require
  `github-automation`; `github-nightly` and `github-bump` require
  `github-watch`.

**What to do.** Apply `markdown`, `yaml` or `python` to keep that language
formatted. A repository with vendored code in `docs/theme/` or `docs/vendor/`
adds those paths to `extend-exclude` in `typos.toml` and `excludes` in
`dprint.json`; one that publishes a site sets `pages.path`.

### A Collection's Tooling Is `devset-collection`

**What changed.** For a repository of profiles, `profile-pins` is
`devset-collection`: its pin tooling, under the feature `pins`, reports its bump
to `devset-collection.md`. It brings a catalog, which writes a collection's
README tables and each profile's facts and holds its profiles to their rules,
and a suite over `tests/fixtures/`.

**What to do.** Apply `devset-collection` with `features = ["pins"]`. Mark the
catalog's regions in the README, `<!-- catalog: written by devset-collection
-->` to `<!-- /catalog -->`, and each profile README's facts, `<!-- facts:
written by devset-collection -->` to `<!-- /facts -->`, and run `just
fix-devset-collection`.

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

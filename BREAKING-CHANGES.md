# Breaking Changes

A migration note for every breaking change, newest release first: what changed,
why, and what a repository does about it. [CHANGELOG.md](CHANGELOG.md) lists
every change; this lists only those a repository must act on.

## Summary

- [v0.15.0](#v0150)
  - [`github-templates` writes issue forms](#github-templates-writes-issue-forms)
- [v0.14.0](#v0140)
  - [`miri`, `rustc-dev` and `llvm-tools` are features](#miri-rustc-dev-and-llvm-tools-are-features)
- [v0.13.0](#v0130)
  - [A recipe that runs cargo carries `[metadata("rust")]`](#a-recipe-that-runs-cargo-carries-metadatarust)
- [v0.12.0](#v0120)
  - [`git-commits` checks a pull request's title](#git-commits-checks-a-pull-requests-title)
  - [`setup` asks for `repository`](#setup-asks-for-repository)
- [v0.11.0](#v0110)
  - [`devset-collection` asks for `repository`](#devset-collection-asks-for-repository)
- [v0.10.0](#v0100)
  - [atxp needs devset 0.5.0](#atxp-needs-devset-050)
  - [The automation's helpers are `automation.js`, and merging is a feature](#the-automations-helpers-are-automationjs-and-merging-is-a-feature)
- [v0.8.0](#v080)
  - [The README's header is the `project` block](#the-readmes-header-is-the-project-block)
- [v0.7.0](#v070)
  - [atxp needs devset 0.4.0](#atxp-needs-devset-040)
- [v0.6.0](#v060)
  - [atxp needs devset 0.3.0](#atxp-needs-devset-030)
  - [The book's prose links to the API](#the-books-prose-links-to-the-api)
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

## V0.15.0

### `github-templates` Writes Issue Forms

**What changed.** The issue templates are GitHub's YAML forms,
`.github/ISSUE_TEMPLATE/bug_report.yml` and `feature_request.yml`, whose
required fields a reporter fills in; the Markdown templates, `bug_report.md` and
`feature_request.md`, are gone from the profile. devset writes the forms where
they are missing, and takes an old template away where it is as devset wrote it.

**What to do.** Where you edited an old template, devset keeps it, untracked:
move what you added into the form, and remove the Markdown file, so GitHub
offers each kind of issue once.

## V0.14.0

### `miri`, `rustc-dev` and `llvm-tools` Are Features

**What changed.** `rust-toolchain`'s toolchain is `rust-src`, rustfmt and
clippy, which the checks use. miri, `rustc-dev` and `llvm-tools`, which no check
uses and which made up about half of every checkout's and every CI job's
download, are the features `miri`, `rustc-dev` and `llvm-tools`, each off unless
a repository turns it on. The pinned nightly still has all three on every
platform the locks cover.

**What to do.** A repository that runs `cargo miri`, a tool linking the
compiler, or coverage turns on what it uses:

```sh
devset add atxp/rust-toolchain --features miri,rustc-dev,llvm-tools
```

## V0.13.0

### A Recipe That Runs Cargo Carries `[metadata("rust")]`

**What changed.** `github-ci`'s jobs restore Cargo's build only for a recipe
with `[metadata("rust")]` above it, and start no toolchain for any other.
`check-devset-collection` holds a collection's profiles to it: a `check-` or
`nightly-` recipe that runs cargo, rustc, rustdoc or rustup carries the tag, and
no other does. atxp's own profiles carry it already.

**What to do.** In a collection of your own, add the line above each such
recipe, below its comment:

```just
# Lints every crate, target and feature; a warning fails.
[metadata("rust")]
check-rust-clippy:
```

A repository's own recipe that builds with cargo, in its `justfile`, takes the
same line to keep its CI job's cache.

## V0.12.0

### `git-commits` Checks a Pull Request's Title

**What changed.** A pull request lands squashed, as one commit its title names,
so its title is what `git-commits` holds to Conventional Commits: where
`github-ci` is applied, the new workflow `title` checks it on every change to
the pull request, an edit of the title included. CI no longer checks a pull
request's own commits, which never land; a push to the default branch has what
it landed checked. On a checkout, `just check-git-commits` still checks the
branch's commits.

**What to do.** Squash-merge pull requests: in the repository's settings, allow
squash merging alone, titled by the pull request. Require the job `title` beside
`check` in the default branch's ruleset.

### `setup` Asks for `repository`

**What changed.** `setup` writes a Getting Started section into
`CONTRIBUTING.md`, where the repository has one, which names the repository to
fork and clone. It declares `repository`, the variable `project`,
`github-release` and others declare with no default, so a repository that
answered it for one of them has nothing to do.

**What to do.** Where the run asks, answer it with the update:

```sh
devset update atxp --tag v0.12.0 --var repository=<owner>/<name>
```

The section goes at the end of `CONTRIBUTING.md`; move it where it reads best,
and it stays there.

## V0.11.0

### `devset-collection` Asks for `repository`

**What changed.** `devset-collection` declares `repository`, the collection's
GitHub repository as `owner/name`, which its catalog site names in its commands
and links: the feature `site`, off unless a collection turns it on. It is the
variable `project`, `github-release` and others declare, with no default, so a
collection that answered it for one of them has nothing to do; one that did not
is asked on its next run, and with `--no-input` stops there. mdBook's pin also
moves to a profile of its own, `mdbook-tool`, which `mdbook` requires, and its
lock entries move with it.

**What to do.** Where the run asks, answer it with the update:

```sh
devset update atxp --tag v0.11.0 --var repository=<owner>/<name>
```

devset 0.5.1 and older lose mdBook's entries in `.config/mise/mise.lock` as they
move, and `devset status` then reports `mdbook-tool`'s part of it as drift:
`devset apply --force` writes it again. devset 0.5.2, which atxp v0.11.1 pins,
keeps them.

## V0.10.0

### atxp Needs devset 0.5.0

**What changed.** Every profile requires devset 0.5.0, which keeps a JSON object
on one line when a key joins it, as `.github/automation.json`'s `bump` does when
the feature `merge` turns on; it also takes each default in one note and asks
only for a variable with none. The `devset` profile pins 0.5.0.

**What to do.** Take the update with devset 0.5.0, which moves the pin itself:

```sh
mise exec github:atomix-labs/devset@0.5.0 -- devset update atxp --tag v0.10.0
```

### The Automation's Helpers Are `automation.js`, and Merging Is a Feature

**What changed.** `.github/scripts/issue.js` is `.github/scripts/automation.js`
now, shipped by `github-automation`, and labels, assigns and comments on the
automation's pull requests as it did its issues: the weekly bump's, the demo's,
and Dependabot's are assigned to `assignees` too. Merging them is each profile's
feature `merge`, off unless a repository turns it on: `bump.mode` is `branch` or
`pr`, and `bump.merge`, which `github-bump`'s `merge` sets, merges the bump's
pull request once `just check` passes; `vhs`'s `merge` does the same for the
demo's. A `bump.mode` of `merge` still merges, with a warning naming the
feature.

**What to do.** A workflow of the repository's own that requires `issue.js`
requires `automation.js`. Where `bump_mode` was `merge`, turn the feature on and
answer the mode again:

```sh
devset add atxp/github-bump --features merge
devset apply --var bump_mode=pr
```

To have the automation's issues and pull requests assigned, answer `assignees`:
`devset apply --var assignees=<login>`.

## V0.8.0

### The README's Header Is the `project` Block

**What changed.** The README block `project` writes is the whole header now, not
only the badges: centered, the logo the new `logo` variable names, or else the
project's name as the title; the tagline the `description` variable gives; then
the badges. Markdown cannot center, so it is HTML, inside `dprint-ignore`
markers, and the `markdown` profile's rumdl allows the elements it uses. A
README the profile starts opens with the block, and shows the demo the new `vhs`
profile records where that is applied.

**What to do.** Take the update, answering the two variables, then move the
block to the top of the README and remove the README's own `# title` above it,
which the block now writes:

```sh
devset update atxp --tag v0.8.0 --var description="What the project is, in one line" --var logo=docs/src/media/logo
```

`logo` is a path without its ending: the header shows `<logo>-light.svg` on a
light page and `<logo>-dark.svg` on a dark one. Left empty, the header shows the
name. A repository that applies `cargo-workspace` too answers `description` once
for both.

## V0.7.0

### atxp Needs devset 0.4.0

**What changed.** Every profile requires devset 0.4.0, whose ten commands the
profiles' scripts and skills use: the weekly bump moves a source with `devset
update <source> --tag <release>` and takes back a move that conflicts with
`devset apply --abort`; `using-devset` teaches `devset explain` and `devset
apply --continue`; the agents' allow-list names `devset explain` where it named
`devset features`. The `devset` profile pins 0.4.0.

**What to do.** Take the update with devset 0.4.0, which moves the pin itself:

```sh
mise exec github:atomix-labs/devset@0.4.0 -- devset update atxp --tag v0.7.0
```

A script of the repository's own that runs `devset new`, `devset init` with a
layer, `devset features`, `devset update --continue` or `--abort`, or `devset
schema` moves as devset's BREAKING-CHANGES.md says.

## V0.6.0

### atxp Needs devset 0.3.0

**What changed.** Every profile requires devset 0.3.0, which turns a layer's
features on and off from the command line, aligns a TOML key with the table it
joins, and fills a block's markers written empty; it also refuses a
`.devset/config.toml` that lists one profile as two layers. The `devset` profile
pins 0.3.0.

**What to do.** Keep one `[[layers]]` entry for each profile, with the features
of any second one, then take the update with devset 0.3.0:

```sh
mise exec github:atomix-labs/devset@0.3.0 -- devset update
```

### The Book's Prose Links to the API

**What changed.** Under `mdbook`'s `api`, a default feature,
mdbook-rustdoc-links reads a link such as ``[`Entry`]`` in the book as a Rust
path, and links it to the API at `/api`; `check-mdbook` fails on one that does
not resolve, or that names a path the name alone would reach.

**What to do.** Fix what `check-mdbook` names: write the path an item needs,
``[`Entry`][ledger::Entry]``, or only its name where the name resolves.

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

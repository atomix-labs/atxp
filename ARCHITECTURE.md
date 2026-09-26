# Architecture

How the profiles in atxp are built and how they compose: what a profile is, how
it shares a file with a repository and with other profiles, how its recipes,
pins and CI fit together, and the principles behind them.
[CONTRIBUTING.md](CONTRIBUTING.md) says how to change one.

## Overview

[devset](https://github.com/atomix-labs/devset) applies profiles to a repository
as layers, records what it wrote in `.devset/`, and on `devset update` merges
what a profile changed with what the repository changed since. A profile is a
directory in `profiles/`: a `profile.toml` naming the files it owns and how, a
`files/` directory holding them, and a `README.md`.

atxp is one repository of profiles, released as a whole: a tag versions every
profile. Every profile it requires is a sibling path, so one tag pins them all
together.

## Profiles

Most profiles are **atoms**: an atom owns one tool, whole. That is its
configuration; its version, pinned with [mise](https://mise.jdx.dev) in
`.config/mise/conf.d/devset-<id>.toml`, and that version's entry in
`.config/mise/mise.lock`; and its recipes, in `.just/<id>.just`. Some own a
concern rather than a tool: `lints` the lint wall, `cargo-profiles` the build
profiles, `automation` the automation's settings.

The **bundle**, `rust`, owns nothing and requires the profiles a Rust repository
takes; each becomes a layer of its own. A repository that wants less requires
the profiles it wants from a profile of its own.

A profile owns each of its files in one of three ways:

| Part  | Owns                                            | The rest of the file |
| ----- | ----------------------------------------------- | -------------------- |
| whole | the file                                        | none                 |
| keys  | the leaves its TOML, JSON or YAML payload names | the repository's     |
| block | a comment-marked block of lines                 | the repository's     |

and under one of three policies:

| Policy  | A local edit                                                           |
| ------- | ---------------------------------------------------------------------- |
| `owned` | is drift: `devset status` names it, `devset apply --force` restores it |
| `merge` | is kept, and merged with the profile's own changes on `devset update`  |
| `once`  | is the point: the file is written once, then left to the repository    |

Where several profiles share a file, as every atom shares the lock, each owns
its own keys of it, so the file composes as the profiles do. Layout is a
formatter's: devset compares values, never spacing, and writes a key it adds in
the layout its payload gives it.

A value repositories choose is a variable, rendered into a payload marked
`template`; one value that several profiles share, such as `line_width`, is one
variable with one default.

## The Recipe Spine

The `just` profile owns a block of the repository's `justfile`: an `import?` for
every profile's recipe file, which is skipped where the profile is not applied,
and one recipe for each verb, which runs every recipe named for it:

| Recipe         | Runs them all  | Does                                                         |
| -------------- | -------------- | ------------------------------------------------------------ |
| `check-<id>`   | `just check`   | a check; CI runs each as a job of its own                    |
| `fix-<id>`     | `just fix`     | fixes what its check finds                                   |
| `bump-<id>`    | `just bump`    | moves what it pins past a three-day cooldown, and reports it |
| `nightly-<id>` | `just nightly` | a check too slow for every change                            |
| `setup-<id>`   | `just setup`   | what a checkout needs before it builds                       |
| `host-<id>`    | `just host`    | the machine's own setup, whose steps may ask for sudo        |
| `release-<id>` | `just release` | what a release needs, for `$RELEASE_VERSION`                 |
| `package-<id>` | `just package` | what a release ships, built for this machine into `dist/`    |
| `publish-<id>` | `just publish` | what a release puts in a registry, once the release is out   |

A profile adds a recipe by naming it for a verb, and a repository adds one the
same way, outside the block. Nothing lists the recipes twice: the spine finds
them by name, and CI reads them from the justfile.

## Pins

Every tool is pinned to one version, and locked in `.config/mise/mise.lock` for
`linux-arm64`, `linux-x64` and `macos-arm64`, each download with its checksum or
its publisher's provenance. mise installs from the lock, verified, and refuses a
platform the lock lacks. No release younger than three days is chosen.

Pins move weekly. In atxp, `just bump` moves every profile's pins and relocks
them (`bump-devset-collection`), the pinned nightly (`bump-rust-toolchain`), and the
one mise version the setup script, the `mise` profile and every workflow share
(`bump-mise-version`). A release carries them to repositories, which take it
with `devset update`. In a repository, `just bump` moves what the repository
pins itself: its Cargo requirements, one at a time (`cargo-bump`), and its own
tools.

## CI

- `github-ci`'s `check` runs every `check-*` recipe as a job of its own, read
  from the justfile, with the tools the lock pins; the job `check` passes when
  every recipe does. A site one recipe builds is deployed to GitHub Pages from
  the default branch.
- `github-nightly` runs every `nightly-*` recipe each night.
- `github-bump` runs `just bump` weekly, gated by `just check`, to one signed
  commit, then as far as a pull request or a merge.
- `github-watch` opens an issue for any scheduled workflow that fails, stalls or
  is disabled.
- `github-release` publishes a release from its tag: every `package-*` recipe on
  each platform, then the GitHub Release with git-cliff's notes and the
  archives, then every `publish-*` recipe, with a registry's token for the
  workflow where it trusts one.

Commits follow Conventional Commits, which `committed` checks; at a release,
`git-cliff` writes the changelog from them.

## The Repository

```text
profiles/<id>/     every profile: profile.toml, README.md, files/
scripts/           atxp's own tools: the catalog, the mise version, the nightly's bump
tests/run.sh       the suite: the bundle on each fixture, every profile alone and all at once
tests/fixtures/    a crate and a workspace, the repositories the suite applies profiles to
.devset/           atxp's record of the profiles it applies to itself
.just/, .github/   written by those profiles; atxp's own recipes are in the justfile
```

atxp applies to itself every profile that fits a repository of profiles, so its
own checks are the ones it ships. Payloads are templates until devset renders
them, so atxp's formatters leave `profiles/*/files/` alone; the suite checks
every payload rendered, applied to the fixtures.

`scripts/catalog.py` writes what the manifests say: the tables in the README,
the facts block of every profile's README, and the spine's imports.
`check-catalog` fails when any is stale, or when a profile breaks a rule of
CONTRIBUTING.md.

## Design Principles

- **One concern a profile.** A tool's configuration, pin and recipes travel
  together, and no two profiles own one thing.
- **Nothing listed twice.** Recipes are found by name, CI's jobs are read from
  the justfile, and the catalog and every profile's facts are generated from the
  manifests.
- **Checks by construction.** What a profile ships is checked the way a
  repository checks it: the suite applies every profile and runs `just check`.
- **Every download verified.** Tools come from the lock with their checksums,
  plugins with theirs, and nothing younger than the cooldown.
- **A small, uniform surface.** Every profile has the same shape, its recipes
  the same nine verbs, and its README the same two parts.

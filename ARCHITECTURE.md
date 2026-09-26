# Architecture

How the profiles in atxp are built and how they compose: what a profile is, how
it shares a file with a repository and with other profiles, how its features,
recipes, pins, CI and the agent layer fit together, and the principles behind
them. [CONTRIBUTING.md](CONTRIBUTING.md) says how to change one.

## Overview

[devset](https://github.com/atomix-labs/devset) applies profiles to a repository
as layers, records what it wrote in `.devset/`, and on `devset update` merges
what a profile changed with what the repository changed since. A profile is a
directory holding a `profile.toml`, which names the files it owns and how, the
profiles it requires and the features it offers; a `files/` directory holding
the files; and a `README.md`.

atxp is a collection: one source of profiles, released as a whole, so a tag
versions every profile. `collection.toml` names it `atxp`. Its profiles live in
`profiles/<umbrella>/<name>/`, grouped by what they concern, and devset finds
each by its name wherever it is, so a profile requires another by name, and a
repository names each layer `atxp/<name>`.

## Profiles

A profile owns one concern: a tool, as `toml` owns taplo, or a policy, as
`rust-lints` owns the lint wall. With it come its configuration; the version of
each tool, pinned with [mise](https://mise.jdx.dev) in
`.config/mise/conf.d/devset-<name>.toml`, and that version's entry in
`.config/mise/mise.lock`; its recipes, in `.just/<name>.just`, with any helper
beside them; and its output, ignored in its own block of `.gitignore`.

A **feature** is an optional capability of a concern, and only adds: a tool a
concern can do without, as `cargo-unused`'s `machete` and `shear`, or the house
policy, `strict`. A file a feature brings is gated by it, `when = { features =
[...] }`, and a template reads the features on, so one recipe runs each tool its
features turn on. A **requirement** is a concern a profile cannot work without;
an optional one applies only when a feature turns it on.

The **bundle**, `rust`, owns nothing. It requires the core every Rust repository
has, each a layer of its own, and offers the rest as features, none on by
default: `docs`, `agents`, `publish`, `binaries`, `oss`, `nightly` and `strict`.

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

Layout is a formatter's: devset compares values, never spacing, and writes a key
it adds as its payload writes it.

What a project will own and change is a **scaffold**: written once, where the
repository lacks it, and the repository's from then on, as `cargo-workspace`
writes a workspace and its first crate, `project` a README and the licences, and
`mdbook` a book. A **starter** is a whole file written once so that a part has a
file to live in: `just` starts a justfile holding its block, and `agents` an
AGENTS.md holding its own. A repository that has the file keeps it, and gets the
part added.

A value repositories choose is a variable, rendered into a payload marked
`template`; one value that several profiles share, such as `line_width`, is one
variable with one default.

## Shared Files and the Graph

Where several profiles share a file, as every profile with a tool shares the
lock, each owns its own keys of it, so the file composes as the profiles do.
Settings that are one profile's are that profile's keys: `markdown` owns the
`markdown` settings of `dprint.json`.

A list is one value, which two profiles cannot each add to, so the profile that
owns it renders it from the graph: `devset.profiles`, the profiles applied, and
`devset.features`, the features on. Nothing detects a profile on disk:

- `just`'s block imports the recipes of every profile applied.
- `dprint` loads the plugin of each language profile applied, and formats its
  files.
- `release.yml` takes a crates.io token where `cargo-publish` is applied.
- `vscode` recommends and configures the tools of the profiles applied.

A list that follows the graph is its profile's own: an entry a repository adds
to it conflicts with the next change of the graph. So a list a repository adds
to, as a formatter's excludes, stays fixed, since a path that is not there costs
nothing, and each profile ignores its own output in `.gitignore`, which the
formatters read.

## The Recipe Spine

The `just` profile owns a block of the repository's `justfile`: an `import?` for
every applied profile's recipe file, and one recipe for each verb, which runs
every recipe named for it:

| Recipe           | Runs them all  | Does                                                         |
| ---------------- | -------------- | ------------------------------------------------------------ |
| `check-<name>`   | `just check`   | a check; CI runs each as a job of its own                    |
| `fix-<name>`     | `just fix`     | fixes what its check finds                                   |
| `bump-<name>`    | `just bump`    | moves what it pins past a three-day cooldown, and reports it |
| `nightly-<name>` | `just nightly` | a check too slow for every change                            |
| `test-<name>`    | `just test`    | a suite too slow for `just check`, which CI runs beside it   |
| `setup-<name>`   | `just setup`   | what a checkout needs before it builds                       |
| `host-<name>`    | `just host`    | the machine's own setup, whose steps may ask for sudo        |
| `release-<name>` | `just release` | what a release needs, for `$RELEASE_VERSION`                 |
| `package-<name>` | `just package` | what a release ships, built for this machine into `dist/`    |
| `publish-<name>` | `just publish` | what a release puts in a registry, once the release is out   |

A profile adds a recipe by naming it for a verb, and a repository adds one the
same way, outside the block. Nothing lists the recipes twice: the spine finds
them by name, and CI reads them from the justfile.

## Pins

Every tool is pinned to one version, and locked in `.config/mise/mise.lock` for
`linux-arm64`, `linux-x64` and `macos-arm64`, each download with its checksum or
its publisher's provenance. mise installs from the lock, verified, and refuses a
platform the lock lacks. No release younger than three days is chosen. A tool
one feature brings is gated by that feature in the pin and in the lock alike.

Pins move weekly. In atxp, `just bump` moves every profile's pins and dprint
plugins, and relocks them (`bump-devset-collection`); the pinned nightly
(`bump-rust-toolchain`); and the one mise version the setup script, the `mise`
profile and every workflow share (`bump-mise-version`). A release carries them
to repositories, which take it with `devset update`. In a repository, `just
bump` moves what the repository pins itself: its Cargo requirements, one at a
time (`cargo-bump`), and its own tools.

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
  archives, then every `publish-*` recipe, with a registry's token where a
  profile applied publishes to it.

The workflows that read their settings from `.github/automation.json` require
`github-automation`, which owns it. Commits follow Conventional Commits, which
`git-commits` checks; at a release, `git-changelog` writes the changelog from
them.

## The Agent Layer

`agents` gives a coding agent what it reads before it changes a repository:
AGENTS.md, started where there is none, with a block on checking a change and on
the files devset manages; CLAUDE.md, which imports it; and Claude Code's
permissions and Stop hook in `.claude/`. The permissions allow every check and
fix and devset's commands that only read, and deny publishing; the hook keeps
the agent at work until `just check` passes on what it changed.

A profile whose concern an agent needs taught ships a skill, in
`.claude/skills/<skill>/`, under its own `agents` feature: `rust-doc`,
`cargo-manifest`, `devset`, `devset-collection`, `github-ci`, `github-release`
and `mdbook` do. `git-commits`, `cargo-deny` and `mdbook` add a block to
AGENTS.md where there is one. The bundle's `agents` turns on the layer and every
one of them. A skill is a template like any payload, so it names a recipe only
where the profile that provides it is applied.

## The Repository

```text
profiles/<umbrella>/<name>/  every profile: profile.toml, README.md, files/
collection.toml              atxp, as a source names itself
scripts/                     atxp's own tools: the mise version, the nightly's bump
tests/fixtures/              a crate and a workspace, the repositories the suite applies profiles to
tests/setup-stub.sh          the setup stub against a repository served locally
tests/bundle.sh              the bundle applied to an empty repository, with the features given
.devset/                     atxp's record of the profiles it applies to itself
.just/, .github/             written by those profiles; atxp's own recipes are in the justfile
```

atxp applies to itself every profile that fits a repository of profiles, from
`profiles/`, so its own checks are the ones it ships. Payloads are templates
until devset renders them, so atxp's formatters leave `profiles/**/files/`
alone; the suite checks every payload rendered.

A collection's own tooling is a profile too, `devset-collection`, and atxp
applies it with `pins`:

- **The catalog** writes what the manifests say: the tables in the README,
  grouped by umbrella, and the facts block of every profile's README.
  `check-devset-collection` fails when any is stale, or when a profile breaks a
  rule of CONTRIBUTING.md: a name unique and its directory's, requirements the
  collection resolves, recipes named `<verb>-<name>`, helpers beside them, one
  declaration of each variable, one mise across every workflow, and skills in
  the house form that run only the collection's recipes.
- **The pins**: every profile's lock entries match its pins, for every platform,
  gated as its pins are; `bump-devset-collection` moves them.
- **The suite**, `test-devset-collection`: every profile alone, with its default
  features and with every feature, applies without drift; then on each fixture,
  the bundle with no features, and every profile at once with every feature,
  apply, and `just check` passes there.

atxp's own matrix, `tests/bundle.sh`, applies the bundle to an empty repository
with the features given, then runs `./setup.sh` and `just check` there, as a new
project does. `just test` runs it with no features and with every feature, and
`bundle.yml` runs it each night with each feature alone.

## Design Principles

- **One concern a profile.** A tool's configuration, pins, recipes and output
  travel together, and no two profiles own one thing.
- **Features only add.** A repository turns on what it wants, and the house
  policy is one feature among them.
- **Nothing listed twice.** Recipes are found by name, CI's jobs are read from
  the justfile, a shared list is rendered from the graph, and the catalog and
  every profile's facts are generated from the manifests.
- **Checks by construction.** What a profile ships is checked the way a
  repository checks it: the suite applies every profile, with every feature, and
  runs `just check`, and the matrix starts a project from nothing.
- **Every download verified.** Tools come from the lock with their checksums,
  plugins with theirs, and nothing younger than the cooldown.
- **A small, uniform surface.** Every profile has the same shape, its recipes
  the same ten verbs, and its README the same two parts.

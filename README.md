<!-- dprint-ignore-start -->

<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/src/media/logo-dark.svg">
    <img alt="atxp" src="docs/src/media/logo-light.svg" height="56">
  </picture>
</h1>

<p align="center">Profiles for devset, provided by Atomix Labs and used across its own repositories.</p>

<p align="center">
  <a href="https://github.com/atomix-labs/atxp/actions/workflows/check.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/atomix-labs/atxp/check.yml?branch=main&amp;style=flat-square&amp;label=check"></a>
  <a href="https://github.com/atomix-labs/atxp/releases"><img alt="Release" src="https://img.shields.io/github/v/release/atomix-labs/atxp?style=flat-square&amp;sort=semver"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/atomix-labs/atxp?style=flat-square"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="#profiles">Profiles</a> ·
  <a href="https://atomix-labs.github.io/devset/">devset's Manual</a> ·
  <a href="CHANGELOG.md">Changelog</a> ·
  <a href="CONTRIBUTING.md">Contributing</a>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/src/media/demo-dark.gif">
    <img alt="An empty repository takes atxp's rust bundle with one devset add, answering each question with its default; devset explain names the features still off, and devset status finds every file matching its profile" src="docs/src/media/demo-light.gif" width="720">
  </picture>
</p>

<!-- dprint-ignore-end -->

atxp is a collection of [devset] profiles, provided by Atomix Labs and used
across its own repositories: the configuration, recipes and pinned tools a
repository needs, one concern to a profile. Some fit any repository, such as
git, GitHub CI, Markdown, TOML, YAML and the docs; others are for Rust, with a
`rust` bundle that sets up a Rust repository whole. More come as they are
needed. Use them as they are, change a variable or a feature where your taste
differs, build your own collection on top, or contribute a profile.

<details>
<summary>Table of Contents</summary>

- [What You Get](#what-you-get)
- [Quick Start](#quick-start)
- [Features](#features)
- [Staying Current](#staying-current)
- [Build on It](#build-on-it)
- [Profiles](#profiles)
- [Variables](#variables)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

</details>

## What You Get

| Concern           | What the bundle sets up                                                                     |
| ----------------- | ------------------------------------------------------------------------------------------- |
| Formatting        | rustfmt, dprint for Markdown, JSON and YAML, and Taplo for TOML, at one line width          |
| Lints             | Clippy with warnings denied, the lint wall, rumdl, typos, yamllint, ShellCheck, actionlint  |
| Tests             | cargo-nextest and the doctests; with `nightly`, each feature alone, linted by cargo-hack    |
| Dependency policy | cargo-deny, cargo-machete and cargo-shear, and a weekly bump past a three-day cooldown      |
| CI                | GitHub Actions, a job per check, the same `just check` as on a laptop, tools from one lock  |
| Releases          | git-cliff's changelog; with `publish`, crates.io by trusted publishing and a GitHub Release |
| Docs              | with `docs`, an mdBook with math, diagrams and the API, its links checked by lychee         |
| Agents            | with `agents`, AGENTS.md, CLAUDE.md, Claude Code's allow-list, and a skill per profile      |

## Quick Start

In a repository, even an empty one, apply the bundle, set the machine up, and
run every check:

```sh
devset add atxp/rust --git https://github.com/atomix-labs/atxp --tag v0.12.1 --var repository=<owner>/<name>
./setup.sh
just check
```

Features add to the bundle, `devset add atxp/rust --features docs,publish`, and
any profile is a layer of its own: `devset add atxp/vhs`.

What a repository lacks, the profiles write once and leave to it: a workspace
and its first crate, a changelog, a justfile, and with `publish` or `oss` a
README, the licences and the rest of a project's documents. What it has, they
join: a profile that owns part of a file, keys of a TOML or JSON file or a block
of a text file, takes only that part, and the rest stays the repository's.
`devset add --dry-run` shows what would change first.

A machine with nothing on it starts from the published setup script, which
clones the repository first:

```sh
curl -fsSL https://atomix-labs.github.io/atxp/setup.sh | bash -s -- github.com/<owner>/<name>
```

## Features

`rust` requires the core every Rust repository has: the toolchain, formatting,
the lint wall, rustdoc, the dependency policy, tests, build profiles, commits,
the changelog, CI, the weekly bump, and the tools that check every other file.
Its features add the rest, none on by default:

| Feature    | Adds                                                                                                    |
| ---------- | ------------------------------------------------------------------------------------------------------- |
| `docs`     | the book, built and tested with mdBook, with math, the API and its links checked                        |
| `agents`   | the agent layer: AGENTS.md, CLAUDE.md, Claude Code's allow-list and Stop hook, and each profile's skill |
| `publish`  | crates.io, by trusted publishing, the GitHub Release, and the project's documents                       |
| `binaries` | the workspace's binaries, built for each platform, on the GitHub Release                                |
| `oss`      | an open-source project's documents, with a code of conduct, and the issue and pull request templates    |
| `nightly`  | the nightly run: every feature alone with cargo-hack, and nightly rustc's lints                         |
| `strict`   | the house policy: cargo-deny's bans, the full lint wall, the doc lint, `panic = "abort"`                |

## Staying Current

`devset status` shows where every file stands, and `devset update --dry-run`
names the newer releases. `devset update atxp --tag <release>` takes one: each
file gets the profile's changes merged with the repository's own edits, and
where both changed the same lines, devset stops for you to choose, and `devset
apply --continue` finishes. The bundle's weekly bump takes each release in a
pull request, gated by `just check`.

## Build on It

A team's collection can require atxp's profiles and add its own; one tag pins
atxp for all of them:

```toml
# profiles/house/profile.toml, in your own collection
[profile]
name        = "house"
description = "Our Rust repositories: atxp's bundle, with the book, and our deploy workflow"
devset      = ">=0.5.0"

[requires]
rust = { git = "https://github.com/atomix-labs/atxp", tag = "v0.12.1", features = ["docs"] }

[files.".github/workflows/deploy.yml"]
```

[Composing Profiles] in devset's manual has the rest.

## Profiles

Each profile's page in the catalog says what it does and why, then its facts:
the files it owns and when, its features, its recipes, its variables and what it
requires.

<!-- catalog: written by devset-collection -->

The profiles, by group, each with its page in
[the catalog](https://atomix-labs.github.io/atxp/):

- **`agents`**:
  [`agents`](https://atomix-labs.github.io/atxp/agents/agents.html)
- **`bundles`**: [`rust`](https://atomix-labs.github.io/atxp/bundles/rust.html)
- **`cargo`**:
  [`cargo-binaries`](https://atomix-labs.github.io/atxp/cargo/cargo-binaries.html),
  [`cargo-bump`](https://atomix-labs.github.io/atxp/cargo/cargo-bump.html),
  [`cargo-deny`](https://atomix-labs.github.io/atxp/cargo/cargo-deny.html),
  [`cargo-hack`](https://atomix-labs.github.io/atxp/cargo/cargo-hack.html),
  [`cargo-manifest`](https://atomix-labs.github.io/atxp/cargo/cargo-manifest.html),
  [`cargo-nextest`](https://atomix-labs.github.io/atxp/cargo/cargo-nextest.html),
  [`cargo-profiles`](https://atomix-labs.github.io/atxp/cargo/cargo-profiles.html),
  [`cargo-publish`](https://atomix-labs.github.io/atxp/cargo/cargo-publish.html),
  [`cargo-unused`](https://atomix-labs.github.io/atxp/cargo/cargo-unused.html),
  [`cargo-workspace`](https://atomix-labs.github.io/atxp/cargo/cargo-workspace.html)
- **`devset`**:
  [`devset`](https://atomix-labs.github.io/atxp/devset/devset.html),
  [`devset-collection`](https://atomix-labs.github.io/atxp/devset/devset-collection.html)
- **`docs`**: [`lychee`](https://atomix-labs.github.io/atxp/docs/lychee.html),
  [`mdbook`](https://atomix-labs.github.io/atxp/docs/mdbook.html),
  [`mdbook-tool`](https://atomix-labs.github.io/atxp/docs/mdbook-tool.html),
  [`vhs`](https://atomix-labs.github.io/atxp/docs/vhs.html)
- **`git`**:
  [`git-attributes`](https://atomix-labs.github.io/atxp/git/git-attributes.html),
  [`git-changelog`](https://atomix-labs.github.io/atxp/git/git-changelog.html),
  [`git-commits`](https://atomix-labs.github.io/atxp/git/git-commits.html),
  [`git-ignore`](https://atomix-labs.github.io/atxp/git/git-ignore.html)
- **`github`**:
  [`github-automation`](https://atomix-labs.github.io/atxp/github/github-automation.html),
  [`github-bump`](https://atomix-labs.github.io/atxp/github/github-bump.html),
  [`github-ci`](https://atomix-labs.github.io/atxp/github/github-ci.html),
  [`github-dependabot`](https://atomix-labs.github.io/atxp/github/github-dependabot.html),
  [`github-nightly`](https://atomix-labs.github.io/atxp/github/github-nightly.html),
  [`github-release`](https://atomix-labs.github.io/atxp/github/github-release.html),
  [`github-templates`](https://atomix-labs.github.io/atxp/github/github-templates.html),
  [`github-watch`](https://atomix-labs.github.io/atxp/github/github-watch.html),
  [`github-workflow-lint`](https://atomix-labs.github.io/atxp/github/github-workflow-lint.html)
- **`lang`**: [`ansible`](https://atomix-labs.github.io/atxp/lang/ansible.html),
  [`dprint`](https://atomix-labs.github.io/atxp/lang/dprint.html),
  [`markdown`](https://atomix-labs.github.io/atxp/lang/markdown.html),
  [`python`](https://atomix-labs.github.io/atxp/lang/python.html),
  [`shell`](https://atomix-labs.github.io/atxp/lang/shell.html),
  [`spelling`](https://atomix-labs.github.io/atxp/lang/spelling.html),
  [`toml`](https://atomix-labs.github.io/atxp/lang/toml.html),
  [`yaml`](https://atomix-labs.github.io/atxp/lang/yaml.html)
- **`project`**:
  [`project`](https://atomix-labs.github.io/atxp/project/project.html)
- **`rust`**:
  [`rust-clippy`](https://atomix-labs.github.io/atxp/rust/rust-clippy.html),
  [`rust-doc`](https://atomix-labs.github.io/atxp/rust/rust-doc.html),
  [`rust-fmt`](https://atomix-labs.github.io/atxp/rust/rust-fmt.html),
  [`rust-lints`](https://atomix-labs.github.io/atxp/rust/rust-lints.html),
  [`rust-msrv`](https://atomix-labs.github.io/atxp/rust/rust-msrv.html),
  [`rust-toolchain`](https://atomix-labs.github.io/atxp/rust/rust-toolchain.html)
- **`tooling`**:
  [`editorconfig`](https://atomix-labs.github.io/atxp/tooling/editorconfig.html),
  [`just`](https://atomix-labs.github.io/atxp/tooling/just.html),
  [`mise`](https://atomix-labs.github.io/atxp/tooling/mise.html),
  [`setup`](https://atomix-labs.github.io/atxp/tooling/setup.html),
  [`suppressions`](https://atomix-labs.github.io/atxp/tooling/suppressions.html),
  [`vscode`](https://atomix-labs.github.io/atxp/tooling/vscode.html)

<!-- /catalog -->

## Variables

A variable is a value repositories choose; one that several profiles share, such
as `line_width`, is one variable with one default. Answer one on the command
line, `--var line_width=120`; devset asks for any with no default.

<!-- variables: written by devset-collection -->

Every variable, its default, and who declares it:
[Variables](https://atomix-labs.github.io/atxp/variables.html).

<!-- /variables -->

## Documentation

- [AGENTS.md][Agents]: what an agent needs to work here.
- [ARCHITECTURE.md][Architecture]: how the profiles compose, from parts of a
  file to features, the recipe spine, pins and CI.
- [CONTRIBUTING.md][Contributing]: how to change a profile, the commit
  convention, and the checks.
- [RELEASE.md][Release]: how a release is cut.
- [CHANGELOG.md][Changelog]: what changed in each release, written by git-cliff
  from the commits.
- [BREAKING-CHANGES.md][Breaking Changes]: how to move across a breaking change.
- [SECURITY.md][Security]: how to report a vulnerability.

## Contributing

Issues and pull requests are welcome. To work on atxp, fork it, clone your fork,
and run `./setup.sh`, which installs mise and every tool atxp pins:

```sh
git clone https://github.com/<you>/atxp.git && cd atxp
./setup.sh
just check    # every check, as CI runs them
just test     # every profile, applied to scratch repositories and checked
```

[CONTRIBUTING.md][Contributing] has the rest: how a pull request lands, and the
rules every profile keeps. [Report a bug] or [request a profile].

## License

MIT: see [LICENSE][license].

[devset]: https://github.com/atomix-labs/devset
[Composing Profiles]: https://atomix-labs.github.io/devset/composing.html
[Changelog]: CHANGELOG.md
[Breaking Changes]: BREAKING-CHANGES.md
[Agents]: AGENTS.md
[Architecture]: ARCHITECTURE.md
[Contributing]: CONTRIBUTING.md
[Release]: RELEASE.md
[Security]: SECURITY.md
[Report a bug]: https://github.com/atomix-labs/atxp/issues/new?template=bug_report.md
[request a profile]: https://github.com/atomix-labs/atxp/issues/new?template=profile_request.md
[license]: LICENSE

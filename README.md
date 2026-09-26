# atxp

[![CI][ci badge]][ci] [![License][license badge]][license]
[![Tag][tag badge]][tags]

[Changelog] · [Breaking Changes] · [Architecture] · [Contributing] ·
[Report a bug] · [Request a profile]

atxp holds profiles for [devset]: bundles of configuration, recipes and pinned
tools that devset applies to a repository, and keeps up to date without losing
the repository's own edits. They are one set of choices for a Rust repository,
to apply as they are or to build on: each profile owns one concern, grouped by
umbrella, and the `rust` bundle takes the ones every Rust repository needs, with
features for the rest.

<details>
<summary>Table of Contents</summary>

- [Quick Start](#quick-start)
- [The Bundle](#the-bundle)
- [Profiles](#profiles)
- [Variables](#variables)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

</details>

## Quick Start

In a repository, even an empty one, apply the bundle, set the machine up, and
run every check:

```sh
devset init atxp/rust --git https://github.com/atomix-labs/atxp --tag v0.4.0 --var repository=<owner>/<name>
./setup.sh
just check
```

Features add to the bundle, `devset add atxp/rust --features docs,publish`, and
any profile is a layer of its own: `devset add atxp/lychee`.

What a repository lacks, the profiles write once and leave to it: a workspace
and its first crate, a changelog, a justfile, and with `publish` or `oss` a
README, the licences and the rest of a project's documents.

A machine with nothing on it starts from the published setup script, which
clones the repository first:

```sh
curl -fsSL https://atomix-labs.github.io/atxp/setup.sh | bash -s -- github.com/<owner>/<name>
```

`devset update` takes a newer release; `devset status` shows where every file
stands.

## The Bundle

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

## Profiles

The profiles, grouped by umbrella. Each profile's README says what it does and
why, then its facts: the files it owns and when, its features, its recipes, its
variables and what it requires.

<!-- catalog: written by devset-collection -->

### `agents`

| Profile                                      | What                                                                                                                  | Owns                                                                                              |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| [`agents`](profiles/agents/agents/README.md) | What a coding agent reads to work in the repository: AGENTS.md, CLAUDE.md, and Claude Code's allow-list and Stop hook | `AGENTS.md` (block), `CLAUDE.md`, `.claude/settings.json` (keys, merge), `.claude/hooks/check.sh` |

### `bundles`

- [`rust`](profiles/bundles/rust/README.md): A Rust repository: toolchain,
  formatting, lints, dependency policy, tests, commits, the changelog and CI.
  Requires `rust-toolchain`, `rust-fmt`, `rust-clippy`, `rust-lints`,
  `rust-doc`, `cargo-workspace`, `cargo-deny`, `cargo-unused`, `cargo-nextest`,
  `cargo-profiles`, `cargo-manifest`, `cargo-bump`, `git-ignore`,
  `git-attributes`, `git-commits`, `git-changelog`, `github-ci`, `github-bump`,
  `github-watch`, `github-dependabot`, `github-workflow-lint`, `markdown`,
  `toml`, `yaml`, `spelling`, `shell`, `mise`, `just`, `setup`, `editorconfig`,
  `devset`. Features: `docs`, `publish`, `binaries`, `oss`, `nightly`, `strict`,
  `agents`.

### `cargo`

| Profile                                                       | What                                                                                                                                            | Owns                                                                                                                                               |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`cargo-binaries`](profiles/cargo/cargo-binaries/README.md)   | A release's binaries: the workspace's, built for this machine, static on Linux, archived with a sha256                                          |                                                                                                                                                    |
| [`cargo-bump`](profiles/cargo/cargo-bump/README.md)           | The weekly bump of Cargo requirements and git revisions: one at a time, past the cooldown, kept if it resolves                                  | `.config/mise/mise.lock` (keys)                                                                                                                    |
| [`cargo-deny`](profiles/cargo/cargo-deny/README.md)           | cargo-deny: yanked and unmaintained crates, one version each, permissive licences, crates.io only, and the house bans                           | `deny.toml` (keys), `.config/mise/mise.lock` (keys), `AGENTS.md` (block)                                                                           |
| [`cargo-hack`](profiles/cargo/cargo-hack/README.md)           | cargo-hack lints every crate with each of its features alone, nightly, where a feature can break                                                | `.config/mise/mise.lock` (keys)                                                                                                                    |
| [`cargo-manifest`](profiles/cargo/cargo-manifest/README.md)   | Every crate manifest in one shape, the workspace's lints inherited, and the skill for editing them                                              | `.config/mise/mise.lock` (keys), `.claude/skills/editing-cargo-manifests/SKILL.md`, `.claude/skills/editing-cargo-manifests/references/sources.md` |
| [`cargo-nextest`](profiles/cargo/cargo-nextest/README.md)     | cargo-nextest for every test, and cargo for the doctests; in CI, a `ci` profile that runs them all                                              | `.config/nextest.toml`, `.config/mise/mise.lock` (keys)                                                                                            |
| [`cargo-profiles`](profiles/cargo/cargo-profiles/README.md)   | Build profiles as keys of the workspace Cargo.toml: release, bench, dev, test, profiling and release-fast                                       | `Cargo.toml` (keys), `.gitignore` (block)                                                                                                          |
| [`cargo-publish`](profiles/cargo/cargo-publish/README.md)     | crates.io: every crate a release publishes packaged on each change, and published at the release by trusted publishing                          |                                                                                                                                                    |
| [`cargo-unused`](profiles/cargo/cargo-unused/README.md)       | Dependencies no crate uses, found by cargo-machete from the sources and cargo-shear from the compiled graph                                     | `.config/mise/mise.lock` (keys)                                                                                                                    |
| [`cargo-workspace`](profiles/cargo/cargo-workspace/README.md) | A Cargo workspace: scaffolded where there is none, its build output ignored, its builds portable, its requirements resolved within rust-version | `Cargo.toml`, `crates/` (4 files), `.gitignore` (block), `.cargo/config.toml` (keys)                                                               |

### `devset`

| Profile                                                            | What                                                                                                        | Owns                                                                    |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [`devset`](profiles/devset/devset/README.md)                       | devset itself: pinned for every machine and job, and drift from the profiles failing the checks             | `.config/mise/mise.lock` (keys), `.claude/skills/using-devset/SKILL.md` |
| [`devset-collection`](profiles/devset/devset-collection/README.md) | For a collection of profiles: its catalog, the rules its profiles keep, its test suite, and its pins locked | `collection.toml`, `.claude/skills/authoring-devset-profiles/SKILL.md`  |

### `docs`

| Profile                                    | What                                                                                       | Owns                                                                                                                                                                                                 |
| ------------------------------------------ | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`lychee`](profiles/docs/lychee/README.md) | lychee checks every Markdown link: the repository's own on every change, the web's nightly | `lychee.toml`, `.config/mise/mise.lock` (keys)                                                                                                                                                       |
| [`mdbook`](profiles/docs/mdbook/README.md) | mdBook: the book scaffolded, built, tested and linted, with math, diagrams and the API     | `{{ book_dir }}/` (33 files) (keys, merge), `.github/automation.json` (keys), `.config/mise/mise.lock` (keys), `.gitignore` (block), `.claude/skills/writing-the-book/SKILL.md`, `AGENTS.md` (block) |

### `git`

| Profile                                                   | What                                                                                                       | Owns                                                                                              |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| [`git-attributes`](profiles/git/git-attributes/README.md) | Git attributes: LF in the repository, CRLF for Windows scripts, and language-aware diffs                   | `.gitattributes` (block)                                                                          |
| [`git-changelog`](profiles/git/git-changelog/README.md)   | git-cliff writes the changelog from Conventional Commits at each release, grouped, linked, breaking marked | `CHANGELOG.md`, `cliff.toml`, `.config/mise/mise.lock` (keys)                                     |
| [`git-commits`](profiles/git/git-commits/README.md)       | committed holds every commit a branch adds to Conventional Commits, the scope the part it changes          | `committed.toml`, `.config/mise/mise.lock` (keys), `CONTRIBUTING.md` (block), `AGENTS.md` (block) |
| [`git-ignore`](profiles/git/git-ignore/README.md)         | Git ignores what tools keep locally, editors' files, and anything that looks like a secret                 | `.gitignore` (block)                                                                              |

### `github`

| Profile                                                                  | What                                                                                                                                                  | Owns                                                                                                                                                        |
| ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`github-automation`](profiles/github/github-automation/README.md)       | The automation's settings: issue labels and types, who is assigned, how far the weekly bump goes                                                      | `.github/automation.json` (keys, merge)                                                                                                                     |
| [`github-bump`](profiles/github/github-bump/README.md)                   | A weekly bump: every `bump-*` recipe, gated by `just check`, to a signed commit, a PR or a merge                                                      | `.github/workflows/bump.yml`, `.github/scripts/bump.js`                                                                                                     |
| [`github-ci`](profiles/github/github-ci/README.md)                       | GitHub Actions: every `check-*` recipe a job of its own, read from the justfile, tools from the mise lock; with pages, a site built once and deployed | `.github/workflows/check.yml`, `.claude/skills/fixing-ci/SKILL.md`                                                                                          |
| [`github-dependabot`](profiles/github/github-dependabot/README.md)       | Dependabot: weekly updates of the GitHub Actions a repository uses, in one pull request                                                               | `.github/dependabot.yml` (merge)                                                                                                                            |
| [`github-nightly`](profiles/github/github-nightly/README.md)             | A nightly run of every `nightly-*` recipe, each a job of its own, watched                                                                             | `.github/workflows/nightly.yml`                                                                                                                             |
| [`github-release`](profiles/github/github-release/README.md)             | A release from its tag: every package-* recipe on each platform, then the GitHub Release with git-cliff's notes                                       | `RELEASE.md`, `.github/workflows/release.yml`, `.claude/skills/cutting-releases/SKILL.md`                                                                   |
| [`github-templates`](profiles/github/github-templates/README.md)         | GitHub's issue templates and pull request checklist, the repository's once written                                                                    | `.github/` (4 files) (once)                                                                                                                                 |
| [`github-watch`](profiles/github/github-watch/README.md)                 | Every scheduled workflow watched: one that fails, stops running or is disabled gets an issue                                                          | `.github/` (3 files)                                                                                                                                        |
| [`github-workflow-lint`](profiles/github/github-workflow-lint/README.md) | Every GitHub workflow checked: actionlint, zizmor's audit, and conftest against the repository's policies                                             | `.github/actionlint.yaml`, `.github/zizmor.yml`, `policy/workflows/workflows.rego`, `policy/workflows/workflows_test.rego`, `.config/mise/mise.lock` (keys) |

### `lang`

| Profile                                        | What                                                                                                          | Owns                                                                                                            |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| [`ansible`](profiles/lang/ansible/README.md)   | ansible-lint holds every playbook and role in .ansible/ to its production profile, on the pinned ansible-core | `.ansible-lint`, `.config/mise/mise.lock` (keys)                                                                |
| [`dprint`](profiles/lang/dprint/README.md)     | dprint, the formatter: JSON, CSS and JavaScript, and each language profile's plugin; every plugin checksummed | `dprint.json` (keys, merge), `.config/mise/mise.lock` (keys)                                                    |
| [`markdown`](profiles/lang/markdown/README.md) | Markdown: formatted by dprint at 80, and linted by rumdl, headings in title case                              | `.rumdl.toml` (keys, merge), `.config/mise/mise.lock` (keys), `.gitignore` (block), `dprint.json` (keys, merge) |
| [`python`](profiles/lang/python/README.md)     | Python: linted by Ruff at the shared line width, and formatted by dprint through its Ruff plugin              | `ruff.toml` (keys, merge), `.config/mise/mise.lock` (keys), `.gitignore` (block), `dprint.json` (keys, merge)   |
| [`shell`](profiles/lang/shell/README.md)       | ShellCheck lints every shell script the repository tracks, following what each sources                        | `.config/mise/mise.lock` (keys)                                                                                 |
| [`spelling`](profiles/lang/spelling/README.md) | typos checks the spelling of code, documents and configuration; a repository adds its own words               | `typos.toml` (keys, merge), `.config/mise/mise.lock` (keys)                                                     |
| [`toml`](profiles/lang/toml/README.md)         | taplo formats every TOML file in one layout: aligned, four spaces, dependencies in order                      | `taplo.toml` (keys, merge), `.config/mise/mise.lock` (keys)                                                     |
| [`yaml`](profiles/lang/yaml/README.md)         | YAML: formatted by dprint with double quotes, and checked by yamllint for what no formatter fixes             | `.yamllint.yaml` (keys, merge), `.config/mise/mise.lock` (keys), `dprint.json` (keys, merge)                    |

### `project`

| Profile                                         | What                                                                                                      | Owns                                                                                                                                                                                                                       |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`project`](profiles/project/project/README.md) | The documents every project keeps: the README, the licence, how to contribute, security, breaking changes | `README.md` (block), `CONTRIBUTING.md` (block), `LICENSE-MIT` (once), `LICENSE-APACHE` (once), `LICENSE` (once), `SECURITY.md` (once), `BREAKING-CHANGES.md` (once), `CODE_OF_CONDUCT.md` (once), `ARCHITECTURE.md` (once) |

### `rust`

| Profile                                                    | What                                                                                                                                 | Owns                         |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------- |
| [`rust-clippy`](profiles/rust/rust-clippy/README.md)       | Clippy over every crate, target and feature, warnings denied; tests may unwrap, panic and print                                      | `clippy.toml` (keys)         |
| [`rust-doc`](profiles/rust/rust-doc/README.md)             | rustdoc builds every crate's documentation, private items included, warnings denied                                                  | `.claude/` (9 files)         |
| [`rust-fmt`](profiles/rust/rust-fmt/README.md)             | rustfmt on nightly options: imports by module, comments wrapped, doc examples formatted                                              | `rustfmt.toml` (keys, merge) |
| [`rust-lints`](profiles/rust/rust-lints/README.md)         | The lint wall, as keys of the workspace Cargo.toml: rustc, rustdoc, clippy and cargo, and nightly's own lints                        | `Cargo.toml` (keys)          |
| [`rust-msrv`](profiles/rust/rust-msrv/README.md)           | Every crate builds on the rust-version it declares: the oldest toolchain it says it supports                                         |                              |
| [`rust-toolchain`](profiles/rust/rust-toolchain/README.md) | The toolchain a checkout builds with: rustup where missing, then one pinned nightly with miri, rustc-dev, llvm-tools and the sources | `rust-toolchain.toml` (keys) |

### `tooling`

| Profile                                                   | What                                                                                                          | Owns                                                             |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| [`editorconfig`](profiles/tooling/editorconfig/README.md) | EditorConfig: UTF-8, LF, a final newline, spaces, and the shared line width                                   | `.editorconfig` (merge)                                          |
| [`just`](profiles/tooling/just/README.md)                 | The recipe spine: imports every active profile's recipes, and `check`, `fix` and the other verbs run them all | `justfile` (block), `.config/mise/mise.lock` (keys)              |
| [`mise`](profiles/tooling/mise/README.md)                 | mise installs every tool from its lock, verified on every platform, none under three days old                 | `.config/mise/mise.lock` (keys)                                  |
| [`setup`](profiles/tooling/setup/README.md)               | One command readies a machine for a checkout: mise, pinned and verified, then mise bootstrap and just setup   | `setup.sh`, `.devcontainer/devcontainer.json` (once)             |
| [`suppressions`](profiles/tooling/suppressions/README.md) | Every lint suppression proves it still suppresses something, for the tools that do not report it themselves   |                                                                  |
| [`vscode`](profiles/tooling/vscode/README.md)             | VS Code, set up for the tools the target's profiles bring: their extensions and settings                      | `.vscode/extensions.json`, `.vscode/settings.json` (keys, merge) |

<!-- /catalog -->

## Variables

A variable is a value repositories choose; one that several profiles share, such
as `line_width`, is one variable with one default. Answer them on the command
line, `--var line_width=120`, or when devset asks.

<!-- variables: written by devset-collection -->

| Variable                 | Default             | Asks                                                                   | Declared by                                                                                                                                                                                                                                                                                                                                         |
| ------------------------ | ------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `assignees`              | empty               | GitHub logins assigned the automation's issues, comma-separated        | [`github-automation`](profiles/github/github-automation/README.md)                                                                                                                                                                                                                                                                                  |
| `authors`                | empty               | Authors, comma-separated                                               | [`cargo-workspace`](profiles/cargo/cargo-workspace/README.md), [`project`](profiles/project/project/README.md)                                                                                                                                                                                                                                      |
| `book_dir`               | `docs`              | Directory of the mdBook, its book.toml                                 | [`mdbook`](profiles/docs/mdbook/README.md)                                                                                                                                                                                                                                                                                                          |
| `bump_mode`              | `pr`                | How far the weekly bump goes: branch, pr or merge                      | [`github-automation`](profiles/github/github-automation/README.md)                                                                                                                                                                                                                                                                                  |
| `channel`                | `nightly`           | The toolchain: nightly, the one the profiles pin, or stable            | [`rust-fmt`](profiles/rust/rust-fmt/README.md), [`rust-toolchain`](profiles/rust/rust-toolchain/README.md)                                                                                                                                                                                                                                          |
| `collection_description` | empty               | One line: what the collection's profiles are for                       | [`devset-collection`](profiles/devset/devset-collection/README.md)                                                                                                                                                                                                                                                                                  |
| `description`            | empty               | One line: what the project is                                          | [`cargo-workspace`](profiles/cargo/cargo-workspace/README.md)                                                                                                                                                                                                                                                                                       |
| `kind`                   | `lib`               | What the first crate builds: lib, bin or both                          | [`cargo-workspace`](profiles/cargo/cargo-workspace/README.md)                                                                                                                                                                                                                                                                                       |
| `license`                | `MIT OR Apache-2.0` | The licence, an SPDX expression                                        | [`cargo-workspace`](profiles/cargo/cargo-workspace/README.md), [`project`](profiles/project/project/README.md)                                                                                                                                                                                                                                      |
| `line_width`             | `100`               | Line width, shared by the formatters and EditorConfig                  | [`dprint`](profiles/lang/dprint/README.md), [`python`](profiles/lang/python/README.md), [`toml`](profiles/lang/toml/README.md), [`rust-fmt`](profiles/rust/rust-fmt/README.md), [`editorconfig`](profiles/tooling/editorconfig/README.md)                                                                                                           |
| `name`                   | empty               | The project's name, and its first crate's; empty takes the directory's | [`cargo-workspace`](profiles/cargo/cargo-workspace/README.md), [`project`](profiles/project/project/README.md)                                                                                                                                                                                                                                      |
| `repository`             | none                | The GitHub repository, owner/name                                      | [`cargo-workspace`](profiles/cargo/cargo-workspace/README.md), [`mdbook`](profiles/docs/mdbook/README.md), [`git-changelog`](profiles/git/git-changelog/README.md), [`github-release`](profiles/github/github-release/README.md), [`github-templates`](profiles/github/github-templates/README.md), [`project`](profiles/project/project/README.md) |
| `runner_labels`          | empty               | Self-hosted runner labels actionlint accepts, comma-separated          | [`github-workflow-lint`](profiles/github/github-workflow-lint/README.md)                                                                                                                                                                                                                                                                            |
| `rust_version`           | `1.98`              | The oldest Rust the workspace builds with                              | [`cargo-workspace`](profiles/cargo/cargo-workspace/README.md)                                                                                                                                                                                                                                                                                       |

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

Issues and pull requests are welcome: read [CONTRIBUTING.md][Contributing]
first.

## License

MIT: see [LICENSE][license].

[devset]: https://github.com/atomix-labs/devset
[Changelog]: CHANGELOG.md
[Breaking Changes]: BREAKING-CHANGES.md
[Agents]: AGENTS.md
[Architecture]: ARCHITECTURE.md
[Contributing]: CONTRIBUTING.md
[Release]: RELEASE.md
[Security]: SECURITY.md
[Report a bug]: https://github.com/atomix-labs/atxp/issues/new?template=bug_report.md
[Request a profile]: https://github.com/atomix-labs/atxp/issues/new?template=profile_request.md
[ci]: https://github.com/atomix-labs/atxp/actions/workflows/check.yml
[ci badge]: https://img.shields.io/github/actions/workflow/status/atomix-labs/atxp/check.yml?branch=main&style=flat-square&logo=github&label=check
[license]: LICENSE
[license badge]: https://img.shields.io/github/license/atomix-labs/atxp?style=flat-square
[tags]: https://github.com/atomix-labs/atxp/tags
[tag badge]: https://img.shields.io/github/v/tag/atomix-labs/atxp?style=flat-square&sort=semver

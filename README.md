# atxp

[![CI][ci badge]][ci] [![License][license badge]][license]
[![Tag][tag badge]][tags]

[Changelog] · [Breaking Changes] · [Architecture] · [Contributing] ·
[Report a bug] · [Request a profile]

atxp holds profiles for [devset]: bundles of configuration, recipes and pinned
tools that devset applies to a repository, and keeps up to date without losing
the repository's own edits. They are one set of choices for a Rust repository,
to apply as they are or to build on: each profile owns one concern, and the
`rust` bundle takes the ones a Rust repository needs.

<details>
<summary>Table of Contents</summary>

- [Quick Start](#quick-start)
- [Profiles](#profiles)
- [Variables](#variables)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

</details>

## Quick Start

In a repository, apply the bundle, set the machine up, and run every check:

```sh
devset init --git https://github.com/atomix-labs/atxp --tag v0.1.0 --path profiles/rust --var repository=<owner>/<name>
./setup.sh
just check
```

A machine with nothing on it starts from the published setup script, which
clones the repository first:

```sh
curl -fsSL https://atomix-labs.github.io/atxp/setup.sh | bash -s -- github.com/<owner>/<name>
```

`devset update` takes a newer release; `devset status` shows where every file
stands.

## Profiles

Each profile's README says what it does and why, then its facts: the files it
owns, its recipes, its variables and what it requires.

<!-- catalog: written by scripts/catalog.py -->

| Profile                                                             | What                                                                                                                                            | Owns                                                                      |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| [`actionlint`](profiles/actionlint/README.md)                       | actionlint checks every GitHub Actions workflow: syntax, expressions, and the shell in each step                                                | `.github/actionlint.yaml`, `.config/mise/mise.lock` (keys)                |
| [`ansible-lint`](profiles/ansible-lint/README.md)                   | ansible-lint holds every playbook and role in .ansible/ to its production profile, on the pinned ansible-core                                   | `.ansible-lint`, `.config/mise/mise.lock` (keys)                          |
| [`automation`](profiles/automation/README.md)                       | The automation's settings: issue labels and types, who is assigned, how far the weekly bump goes                                                | `.github/automation.json` (keys, merge)                                   |
| [`cargo-binaries`](profiles/cargo-binaries/README.md)               | A release's binaries: the workspace's, built for this machine, static on Linux, archived with a sha256                                          |                                                                           |
| [`cargo-bump`](profiles/cargo-bump/README.md)                       | The weekly bump of Cargo requirements and git revisions: one at a time, past the cooldown, kept if it resolves                                  | `.config/mise/mise.lock`, `.cargo/config.toml` (keys)                     |
| [`cargo-deny`](profiles/cargo-deny/README.md)                       | cargo-deny: yanked and unmaintained crates, one version each, the bans, permissive licences, crates.io only                                     | `deny.toml`, `.config/mise/mise.lock` (keys)                              |
| [`cargo-hack`](profiles/cargo-hack/README.md)                       | cargo-hack lints every crate with each of its features alone, nightly, where a feature can break                                                | `.config/mise/mise.lock` (keys)                                           |
| [`cargo-machete`](profiles/cargo-machete/README.md)                 | cargo-machete finds dependencies no crate uses, fast, from the sources alone                                                                    | `.config/mise/mise.lock` (keys)                                           |
| [`cargo-profiles`](profiles/cargo-profiles/README.md)               | Build profiles as keys of the workspace Cargo.toml: release, bench, dev, test, profiling and release-fast                                       | `Cargo.toml` (keys)                                                       |
| [`cargo-shear`](profiles/cargo-shear/README.md)                     | cargo-shear finds dependencies no crate uses, and workspace dependencies no member inherits                                                     | `.config/mise/mise.lock` (keys)                                           |
| [`cargo-workspace-lints`](profiles/cargo-workspace-lints/README.md) | Every crate in the workspace inherits its lints: `[lints] workspace = true`                                                                     | `.config/mise/mise.lock` (keys)                                           |
| [`claude-skills`](profiles/claude-skills/README.md)                 | Claude Code skills: writing rustdoc and writing Cargo manifests, with their linters                                                             | `.claude/` (12 files)                                                     |
| [`clippy`](profiles/clippy/README.md)                               | Clippy over every crate, target and feature, warnings denied; tests may unwrap, panic and print                                                 | `clippy.toml` (keys)                                                      |
| [`committed`](profiles/committed/README.md)                         | committed holds every commit a branch adds to Conventional Commits, the scope the part it changes                                               | `committed.toml`, `.config/mise/mise.lock` (keys)                         |
| [`conftest`](profiles/conftest/README.md)                           | conftest holds the repository's configuration to its own policies, written and tested in Rego                                                   | `.config/mise/mise.lock` (keys)                                           |
| [`dependabot`](profiles/dependabot/README.md)                       | Dependabot: weekly updates of the GitHub Actions a repository uses, in one pull request                                                         | `.github/dependabot.yml` (merge)                                          |
| [`dprint`](profiles/dprint/README.md)                               | dprint formats Markdown at 80, and YAML, JSON, Python, CSS and JavaScript; every plugin checksummed                                             | `dprint.json` (keys, merge), `.config/mise/mise.lock` (keys)              |
| [`editorconfig`](profiles/editorconfig/README.md)                   | EditorConfig: UTF-8, LF, a final newline, spaces, and the shared line width                                                                     | `.editorconfig` (merge)                                                   |
| [`git-cliff`](profiles/git-cliff/README.md)                         | git-cliff writes the changelog from Conventional Commits at each release, grouped, linked, breaking marked                                      | `cliff.toml`, `.config/mise/mise.lock` (keys)                             |
| [`gitattributes`](profiles/gitattributes/README.md)                 | Git attributes: LF in the repository, CRLF for Windows scripts, and language-aware diffs                                                        | `.gitattributes` (block)                                                  |
| [`github-bump`](profiles/github-bump/README.md)                     | A weekly bump: every `bump-*` recipe, gated by `just check`, to a signed commit, a PR or a merge                                                | `.github/workflows/bump.yml`, `.github/scripts/bump.js`                   |
| [`github-ci`](profiles/github-ci/README.md)                         | GitHub Actions: every `check-*` recipe a job of its own, read from the justfile, tools from the mise lock; a Pages site built once and deployed | `.github/workflows/check.yml`                                             |
| [`github-nightly`](profiles/github-nightly/README.md)               | A nightly run of every `nightly-*` recipe, each a job of its own, watched                                                                       | `.github/workflows/nightly.yml`                                           |
| [`github-release`](profiles/github-release/README.md)               | A release from its tag: every package-* recipe on each platform, then the GitHub Release with git-cliff's notes                                 | `.github/workflows/release.yml`                                           |
| [`github-watch`](profiles/github-watch/README.md)                   | Every scheduled workflow watched: one that fails, stops running or is disabled gets an issue                                                    | `.github/` (3 files)                                                      |
| [`gitignore`](profiles/gitignore/README.md)                         | Git ignores what tools keep locally, editors' files, and anything that looks like a secret                                                      | `.gitignore` (block)                                                      |
| [`gitignore-rust`](profiles/gitignore-rust/README.md)               | Git ignores Cargo's build output, rustfmt's backups and MSVC debug files                                                                        | `.gitignore` (block)                                                      |
| [`just`](profiles/just/README.md)                                   | The recipe spine: imports each atom's recipes, and `check` and `fix` run them all                                                               | `justfile` (block), `.config/mise/mise.lock` (keys)                       |
| [`lints`](profiles/lints/README.md)                                 | The lint wall, as keys of the workspace Cargo.toml: rustc, rustdoc, clippy and cargo                                                            | `Cargo.toml` (keys)                                                       |
| [`lints-nightly`](profiles/lints-nightly/README.md)                 | The lints only nightly has, run on the pinned nightly without a #![feature] in any source                                                       |                                                                           |
| [`lychee`](profiles/lychee/README.md)                               | lychee checks every Markdown link: the repository's own on every change, the web's nightly                                                      | `.config/mise/mise.lock` (keys)                                           |
| [`manifest-lint`](profiles/manifest-lint/README.md)                 | Every crate manifest in one shape: key order, inherited fields, grouped dependencies                                                            |                                                                           |
| [`mdbook`](profiles/mdbook/README.md)                               | mdBook builds the book and runs its Rust examples as tests                                                                                      | `.config/mise/mise.lock` (keys), `.gitignore` (block)                     |
| [`mise`](profiles/mise/README.md)                                   | mise installs every tool from its lock, verified on every platform, none under three days old                                                   | `.config/mise/mise.lock` (keys)                                           |
| [`msrv`](profiles/msrv/README.md)                                   | Every crate builds on the rust-version it declares: the oldest toolchain it says it supports                                                    |                                                                           |
| [`nextest`](profiles/nextest/README.md)                             | cargo-nextest for every test, and cargo for the doctests; in CI, a `ci` profile that runs them all                                              | `.config/nextest.toml`, `.config/mise/mise.lock` (keys)                   |
| [`policies`](profiles/policies/README.md)                           | Policies for GitHub Actions workflows, held by conftest: timeouts, stated permissions, no shadowed results                                      | `policy/workflows/workflows.rego`, `policy/workflows/workflows_test.rego` |
| [`profile-pins`](profiles/profile-pins/README.md)                   | For a repository of profiles: every pin locked for every platform, and bumped past the cooldown                                                 |                                                                           |
| [`ruff`](profiles/ruff/README.md)                                   | Ruff lints Python at the shared line width; formatting is dprint's, through its Ruff plugin                                                     | `ruff.toml` (keys, merge), `.config/mise/mise.lock` (keys)                |
| [`rumdl`](profiles/rumdl/README.md)                                 | rumdl lints Markdown: line length left to the formatter, headings in title case                                                                 | `.rumdl.toml` (keys, merge), `.config/mise/mise.lock` (keys)              |
| [`rust-toolchain`](profiles/rust-toolchain/README.md)               | The toolchain a checkout builds with: one pinned nightly, with miri, rustc-dev, llvm-tools and the sources                                      | `rust-toolchain.toml` (keys)                                              |
| [`rustdoc`](profiles/rustdoc/README.md)                             | rustdoc builds every crate's documentation, private items included, warnings denied                                                             |                                                                           |
| [`rustfmt`](profiles/rustfmt/README.md)                             | rustfmt on nightly options: imports by module, comments wrapped, doc examples formatted                                                         | `rustfmt.toml`                                                            |
| [`rustup`](profiles/rustup/README.md)                               | rustup where it is missing, and the toolchain rust-toolchain.toml names, before mise installs any tool                                          |                                                                           |
| [`setup`](profiles/setup/README.md)                                 | One command readies a machine for a checkout: mise, pinned and verified, then mise bootstrap and just setup                                     | `setup.sh`                                                                |
| [`shellcheck`](profiles/shellcheck/README.md)                       | ShellCheck lints every shell script the repository tracks, following what each sources                                                          | `.config/mise/mise.lock` (keys)                                           |
| [`suppressions`](profiles/suppressions/README.md)                   | Every lint suppression proves it still suppresses something, for the tools that do not report it themselves                                     |                                                                           |
| [`taplo`](profiles/taplo/README.md)                                 | taplo formats every TOML file in one layout: aligned, four spaces, dependencies in order                                                        | `taplo.toml` (keys, merge), `.config/mise/mise.lock` (keys)               |
| [`typos`](profiles/typos/README.md)                                 | typos checks the spelling of code, documents and configuration; a repository adds its own words                                                 | `typos.toml` (keys, merge), `.config/mise/mise.lock` (keys)               |
| [`vscode-rust`](profiles/vscode-rust/README.md)                     | VS Code: the extensions recommended, clippy as the check, dprint and rumdl on save                                                              | `.vscode/extensions.json`, `.vscode/settings.json` (keys, merge)          |
| [`yamllint`](profiles/yamllint/README.md)                           | yamllint checks YAML for what a formatter cannot fix: duplicate keys, octal values, truthy words                                                | `.yamllint.yaml` (keys, merge), `.config/mise/mise.lock` (keys)           |
| [`zizmor`](profiles/zizmor/README.md)                               | zizmor audits GitHub Actions for injection, broad permissions, persisted credentials and unpinned actions                                       | `.github/zizmor.yml`, `.config/mise/mise.lock` (keys)                     |

The bundle:

- [`rust`](profiles/rust/README.md): A Rust repository: formatting, the lint
  wall, dependency policy, tests, commits, the changelog, editor and CI.
  Requires `editorconfig`, `gitattributes`, `gitignore`, `gitignore-rust`,
  `mise`, `just`, `setup`, `rustup`, `rust-toolchain`, `github-ci`,
  `github-watch`, `github-nightly`, `github-bump`, `github-release`,
  `dependabot`, `automation`, `committed`, `git-cliff`, `typos`, `clippy`,
  `rustdoc`, `rustfmt`, `lints`, `lints-nightly`, `cargo-profiles`,
  `cargo-deny`, `cargo-machete`, `cargo-shear`, `cargo-workspace-lints`,
  `cargo-hack`, `cargo-bump`, `manifest-lint`, `nextest`, `taplo`, `dprint`,
  `rumdl`, `ruff`, `yamllint`, `shellcheck`, `actionlint`, `zizmor`, `conftest`,
  `policies`, `suppressions`, `vscode-rust`, `claude-skills`.

<!-- /catalog -->

## Variables

A variable is a value repositories choose; one that several profiles share, such
as `line_width`, is one variable with one default. Answer them on the command
line, `--var line_width=120`, or when devset asks.

<!-- variables: written by scripts/catalog.py -->

| Variable        | Default | Asks                                                            | Declared by                                                                                                                                                                                               |
| --------------- | ------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `assignees`     | empty   | GitHub logins assigned the automation's issues, comma-separated | [`automation`](profiles/automation/README.md)                                                                                                                                                             |
| `book_dir`      | `docs`  | Directory of the mdBook, its book.toml                          | [`mdbook`](profiles/mdbook/README.md)                                                                                                                                                                     |
| `bump_mode`     | `pr`    | How far the weekly bump goes: branch, pr or merge               | [`automation`](profiles/automation/README.md)                                                                                                                                                             |
| `line_width`    | `100`   | Line width, shared by the formatters and EditorConfig           | [`dprint`](profiles/dprint/README.md), [`editorconfig`](profiles/editorconfig/README.md), [`ruff`](profiles/ruff/README.md), [`rustfmt`](profiles/rustfmt/README.md), [`taplo`](profiles/taplo/README.md) |
| `repository`    | none    | The GitHub repository the changelog links into, owner/name      | [`git-cliff`](profiles/git-cliff/README.md)                                                                                                                                                               |
| `runner_labels` | empty   | Self-hosted runner labels actionlint accepts, comma-separated   | [`actionlint`](profiles/actionlint/README.md)                                                                                                                                                             |

<!-- /variables -->

## Documentation

- [ARCHITECTURE.md][Architecture]: how the profiles compose, from parts of a
  file to the recipe spine, pins and CI.
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

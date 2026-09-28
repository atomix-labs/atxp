# atxp

Profiles for devset, provided by Atomix Labs and used across its own
repositories.

[![Release](https://img.shields.io/github/v/release/atomix-labs/atxp?sort=semver&style=flat-square)](https://github.com/atomix-labs/atxp/releases)

A repository takes a profile by its name, and a release by its tag:

```sh
devset add atxp/<profile> --git https://github.com/atomix-labs/atxp --tag <release>
```

[The releases](https://github.com/atomix-labs/atxp/releases) list every tag, and
`devset update --dry-run` names the newer ones later.
[devset's manual](https://atomix-labs.github.io/devset/) says the rest.

## Bundles

- [`rust`](bundles/rust.md): A Rust repository: toolchain, formatting, lints,
  dependency policy, tests, commits, the changelog and CI.

## Profiles

### `agents`

| Profile                      | What                                                                                                                  |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [`agents`](agents/agents.md) | What a coding agent reads to work in the repository: AGENTS.md, CLAUDE.md, and Claude Code's allow-list and Stop hook |

### `bundles`

| Profile                   | What                                                                                                     |
| ------------------------- | -------------------------------------------------------------------------------------------------------- |
| [`rust`](bundles/rust.md) | A Rust repository: toolchain, formatting, lints, dependency policy, tests, commits, the changelog and CI |

### `cargo`

| Profile                                       | What                                                                                                                                            |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| [`cargo-binaries`](cargo/cargo-binaries.md)   | A release's binaries: the workspace's, built for this machine, static on Linux, archived with a sha256                                          |
| [`cargo-bump`](cargo/cargo-bump.md)           | The weekly bump of Cargo requirements and git revisions: one at a time, past the cooldown, kept if it resolves                                  |
| [`cargo-deny`](cargo/cargo-deny.md)           | cargo-deny: yanked and unmaintained crates, one version each, permissive licences, crates.io only, and the house bans                           |
| [`cargo-hack`](cargo/cargo-hack.md)           | cargo-hack lints every crate with each of its features alone, nightly, where a feature can break                                                |
| [`cargo-manifest`](cargo/cargo-manifest.md)   | Every crate manifest in one shape, the workspace's lints inherited, and the skill for editing them                                              |
| [`cargo-nextest`](cargo/cargo-nextest.md)     | cargo-nextest for every test, and cargo for the doctests; in CI, a `ci` profile that runs them all                                              |
| [`cargo-profiles`](cargo/cargo-profiles.md)   | Build profiles as keys of the workspace Cargo.toml: release, bench, dev, test, profiling and release-fast                                       |
| [`cargo-publish`](cargo/cargo-publish.md)     | crates.io: every crate a release publishes packaged on each change, and published at the release by trusted publishing                          |
| [`cargo-unused`](cargo/cargo-unused.md)       | Dependencies no crate uses, found by cargo-machete from the sources and cargo-shear from the compiled graph                                     |
| [`cargo-workspace`](cargo/cargo-workspace.md) | A Cargo workspace: scaffolded where there is none, its build output ignored, its builds portable, its requirements resolved within rust-version |

### `devset`

| Profile                                            | What                                                                                                        |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [`devset`](devset/devset.md)                       | devset itself: pinned for every machine and job, and drift from the profiles failing the checks             |
| [`devset-collection`](devset/devset-collection.md) | For a collection of profiles: its catalog, the rules its profiles keep, its test suite, and its pins locked |

### `docs`

| Profile                              | What                                                                                          |
| ------------------------------------ | --------------------------------------------------------------------------------------------- |
| [`lychee`](docs/lychee.md)           | lychee checks every Markdown link: the repository's own on every change, the web's nightly    |
| [`mdbook`](docs/mdbook.md)           | mdBook: the book scaffolded, built, tested and linted, with math, diagrams and the API        |
| [`mdbook-tool`](docs/mdbook-tool.md) | mdBook itself, pinned for every machine and job: for a book, and for a collection's catalog   |
| [`vhs`](docs/vhs.md)                 | The README's demo: terminal sessions VHS records from docs/demo/, again at each release's tag |

### `git`

| Profile                                   | What                                                                                                                                |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| [`git-attributes`](git/git-attributes.md) | Git attributes: LF in the repository, CRLF for Windows scripts, and language-aware diffs                                            |
| [`git-changelog`](git/git-changelog.md)   | git-cliff writes the changelog from Conventional Commits at each release, grouped, linked, breaking marked                          |
| [`git-commits`](git/git-commits.md)       | committed holds what lands to Conventional Commits: a pull request's title, which its squashed commit takes, and a branch's commits |
| [`git-ignore`](git/git-ignore.md)         | Git ignores what tools keep locally, editors' files, and anything that looks like a secret                                          |

### `github`

| Profile                                                  | What                                                                                                                                                  |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`github-automation`](github/github-automation.md)       | The automation's settings and helpers: labels and types, who is assigned, how far the bump goes                                                       |
| [`github-bump`](github/github-bump.md)                   | A weekly bump: every `bump-*` recipe, gated by `just check`, to a signed commit, a PR or a merge                                                      |
| [`github-ci`](github/github-ci.md)                       | GitHub Actions: every `check-*` recipe a job of its own, read from the justfile, tools from the mise lock; with pages, a site built once and deployed |
| [`github-dependabot`](github/github-dependabot.md)       | Dependabot: weekly updates of the GitHub Actions a repository uses, in one pull request                                                               |
| [`github-nightly`](github/github-nightly.md)             | A nightly run of every `nightly-*` recipe, each a job of its own, watched                                                                             |
| [`github-release`](github/github-release.md)             | A release from its tag: every package-* recipe on each platform, then the GitHub Release with git-cliff's notes                                       |
| [`github-templates`](github/github-templates.md)         | GitHub's issue templates and pull request checklist, the repository's once written                                                                    |
| [`github-watch`](github/github-watch.md)                 | Every scheduled workflow watched: one that fails, stops running or is disabled gets an issue                                                          |
| [`github-workflow-lint`](github/github-workflow-lint.md) | Every GitHub workflow checked: actionlint, zizmor's audit, and conftest against the repository's policies                                             |

### `lang`

| Profile                        | What                                                                                                          |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| [`ansible`](lang/ansible.md)   | ansible-lint holds every playbook and role in .ansible/ to its production profile, on the pinned ansible-core |
| [`dprint`](lang/dprint.md)     | dprint, the formatter: JSON, CSS and JavaScript, and each language profile's plugin; every plugin checksummed |
| [`markdown`](lang/markdown.md) | Markdown: formatted by dprint at 80, and linted by rumdl, headings in title case                              |
| [`python`](lang/python.md)     | Python: linted by Ruff at the shared line width, and formatted by dprint through its Ruff plugin              |
| [`shell`](lang/shell.md)       | ShellCheck lints every shell script the repository tracks, following what each sources                        |
| [`spelling`](lang/spelling.md) | typos checks the spelling of code, documents and configuration; a repository adds its own words               |
| [`toml`](lang/toml.md)         | taplo formats every TOML file in one layout: aligned, four spaces, dependencies in order                      |
| [`yaml`](lang/yaml.md)         | YAML: formatted by dprint with double quotes, and checked by yamllint for what no formatter fixes             |

### `project`

| Profile                         | What                                                                                                      |
| ------------------------------- | --------------------------------------------------------------------------------------------------------- |
| [`project`](project/project.md) | The documents every project keeps: the README, the licence, how to contribute, security, breaking changes |

### `rust`

| Profile                                    | What                                                                                                                                 |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| [`rust-clippy`](rust/rust-clippy.md)       | Clippy over every crate, target and feature, warnings denied; tests may unwrap, panic and print                                      |
| [`rust-doc`](rust/rust-doc.md)             | rustdoc builds every crate's documentation, private items included, warnings denied                                                  |
| [`rust-fmt`](rust/rust-fmt.md)             | rustfmt on nightly options: imports by module, comments wrapped, doc examples formatted                                              |
| [`rust-lints`](rust/rust-lints.md)         | The lint wall, as keys of the workspace Cargo.toml: rustc, rustdoc, clippy and cargo, and nightly's own lints                        |
| [`rust-msrv`](rust/rust-msrv.md)           | Every crate builds on the rust-version it declares: the oldest toolchain it says it supports                                         |
| [`rust-toolchain`](rust/rust-toolchain.md) | The toolchain a checkout builds with: rustup where missing, then one pinned nightly with miri, rustc-dev, llvm-tools and the sources |

### `tooling`

| Profile                                   | What                                                                                                          |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| [`editorconfig`](tooling/editorconfig.md) | EditorConfig: UTF-8, LF, a final newline, spaces, and the shared line width                                   |
| [`just`](tooling/just.md)                 | The recipe spine: imports every active profile's recipes, and `check`, `fix` and the other verbs run them all |
| [`mise`](tooling/mise.md)                 | mise installs every tool from its lock, verified on every platform, none under three days old                 |
| [`setup`](tooling/setup.md)               | One command readies a machine for a checkout: mise, pinned and verified, then mise bootstrap and just setup   |
| [`suppressions`](tooling/suppressions.md) | Every lint suppression proves it still suppresses something, for the tools that do not report it themselves   |
| [`vscode`](tooling/vscode.md)             | VS Code, set up for the tools the target's profiles bring: their extensions and settings                      |

# `project`

The documents every project keeps: the README, the licence, how to contribute,
security, breaking changes.

```sh
devset add atxp/project --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `project` · In [`rust`](../bundles/rust.md): with `publish` · In
[`rust`](../bundles/rust.md): with `oss`

The documents every project keeps, each scaffolded where the repository has none
and the repository's once written: a README, the licence, how to contribute, how
to report a vulnerability, and how to move across a breaking change; with
`conduct`, the Contributor Covenant 2.1; with `support`, a SUPPORT.md, which
GitHub links beside a new issue, saying where a question, a bug and a
vulnerability go; and with `architecture`, a page for how the project is built.

Conduct is reported to `conduct_contact`, an address; left empty, the code of
conduct sends it privately through GitHub's Report content, which reaches the
maintainers once the repository accepts reported content (Settings, Moderation
options).

Two of them keep a managed block:

- The README's header: centered, the logo `logo` names, drawn as
  `<logo>-light.svg` and `<logo>-dark.svg` for each theme, or else the name; the
  tagline `description` gives; and badges that follow the profiles applied: CI
  where [`github-ci`](../github/github-ci.md) is, crates.io and docs.rs where
  [`cargo-publish`](../cargo/cargo-publish.md) publishes the crate `crate`
  names, or else the one [`cargo-workspace`](../cargo/cargo-workspace.md) names,
  the book where [`mdbook`](../docs/mdbook.md) builds one, and, with the feature
  `devset-badge`, off unless the project turns it on, "managed with devset",
  linking devset. Markdown cannot center, so the header is HTML, inside
  `dprint-ignore` markers that keep the formatter from laying it out again. A
  README the project starts from here opens with it, then the demo
  [`vhs`](../docs/vhs.md) records where that is applied; one the project has
  already gets the block at its end, to move to its top in place of its own
  title. Where the README is shown away from the repository too, as crates.io
  shows a crate's, `logo` is a URL, such as
  `https://raw.githubusercontent.com/<owner>/<name>/main/docs/src/media/logo`,
  since a relative path resolves against the page showing it.
- CONTRIBUTING's checks say to run `just check` before a pull request and `just
  fix` for what it can fix; [`git-commits`](../git/git-commits.md) adds the
  commit rules.

`license` chooses the licence files: `MIT OR Apache-2.0`, the default, writes
`LICENSE-MIT` and `LICENSE-APACHE`; `MIT` or `Apache-2.0` writes one `LICENSE`.
The copyright line names `authors`, or else the directory. The Covenant's
contact is left for the project to fill in.

The `agents` feature adds the `writing-readmes` skill in `.claude/skills/`: how
a README is written around the header block, which it never edits and moves to
the top where the block was appended; the pitch, Install, Quick Start, the
project's own sections, then Documentation, Contributing and License, in that
order; commands that run as shown, `cargo add` for a library and `cargo install
--locked` for a command line, from crates.io once the first release is out and
never `--git` after it, naming the package where its binary is named otherwise,
and the minimum Rust from `rust-version`; Cargo features in the rows of the
crate docs' table; the README and the `//!` crate page kept apart; and images
and links that resolve wherever the README is shown. Where
[`cargo-publish`](../cargo/cargo-publish.md) publishes the crates, it teaches
why a README crates.io shows takes absolute URLs, `logo` among them, and how
each crate gets one and what it holds; where [`vhs`](../docs/vhs.md) records the
demo, how its picture is kept. Its templates are a library's, a command line's
and a workspace's README, whole, and it names
[`rust-doc`](../rust/rust-doc.md)'s `writing-rustdoc` for the crate page where
that profile's `agents` is on.

It adds the `drawing-the-logo` skill too: the house style of a logo, a 32 by 32
mark of one filled shape and strokes 2.5 wide in GitHub's two inks, the name
beside it in JetBrains Mono Bold, and the files made from the mark, its dark
variant, the logo, the favicon, the tile, the social card and the book's
favicons; how two or three marks are proposed to the owner, and one applied only
once the owner confirms it, through `logo` and, where
[`mdbook`](../docs/mdbook.md) builds a book, its `book_logo` and `book_social`.
Its `scripts/draw.py` makes every file but the mark, with fontTools, cairosvg
and svgo, and writes devset's and atxp's SVGs again byte for byte from their
marks.

## Owns

| File                                                     | Part  | Policy | Notes                                                             |
| -------------------------------------------------------- | ----- | ------ | ----------------------------------------------------------------- |
| `README.md`                                              | block | owned  | template, feature `readme`                                        |
| `CONTRIBUTING.md`                                        | block | owned  | feature `contributing`                                            |
| `LICENSE-MIT`                                            | whole | once   | template, feature `license`, `license` one of `MIT OR Apache-2.0` |
| `LICENSE-APACHE`                                         | whole | once   | feature `license`, `license` one of `MIT OR Apache-2.0`           |
| `LICENSE`                                                | whole | once   | template, feature `license`, `license` one of `MIT`, `Apache-2.0` |
| `SECURITY.md`                                            | whole | once   | template, feature `security`                                      |
| `BREAKING-CHANGES.md`                                    | whole | once   | template, feature `breaking-changes`                              |
| `CODE_OF_CONDUCT.md`                                     | whole | once   | template, feature `conduct`                                       |
| `SUPPORT.md`                                             | whole | once   | template, feature `support`                                       |
| `ARCHITECTURE.md`                                        | whole | once   | feature `architecture`                                            |
| `.claude/skills/writing-readmes/SKILL.md`                | whole | owned  | template, feature `agents`                                        |
| `.claude/skills/writing-readmes/references/sources.md`   | whole | owned  | feature `agents`                                                  |
| `.claude/skills/writing-readmes/references/templates.md` | whole | owned  | template, feature `agents`                                        |
| `.claude/skills/drawing-the-logo/SKILL.md`               | whole | owned  | template, feature `agents`                                        |
| `.claude/skills/drawing-the-logo/scripts/draw.py`        | whole | owned  | executable, feature `agents`                                      |

## Features

| Feature            | Default | Enables                           |
| ------------------ | ------- | --------------------------------- |
| `readme`           | yes     |                                   |
| `license`          | yes     |                                   |
| `contributing`     | yes     |                                   |
| `security`         | yes     |                                   |
| `breaking-changes` | yes     | `git-changelog?/breaking-changes` |
| `conduct`          |         |                                   |
| `support`          |         |                                   |
| `architecture`     |         |                                   |
| `devset-badge`     |         |                                   |
| `agents`           |         |                                   |

## Variables

| Variable          | Default             | Asks                                                                                                         |
| ----------------- | ------------------- | ------------------------------------------------------------------------------------------------------------ |
| `name`            | empty               | The project's name, and its first crate's; empty takes the directory's                                       |
| `crate`           | empty               | The crate the crates.io and docs.rs badges show; empty takes the project's name                              |
| `description`     | empty               | One line: what the project is                                                                                |
| `logo`            | empty               | The README's logo: its path or URL before `-light.svg` or `-dark.svg`                                        |
| `authors`         | empty               | Authors, comma-separated                                                                                     |
| `license`         | `MIT OR Apache-2.0` | The licence, an SPDX expression                                                                              |
| `repository`      | none                | The GitHub repository, owner/name                                                                            |
| `conduct_contact` | empty               | Where conduct is reported privately, an email address or URL; empty sends it through GitHub's Report content |

## Requires

- [`git-changelog`](../git/git-changelog.md): optional

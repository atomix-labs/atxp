# Variables

A variable is a value each repository chooses; one that several profiles declare
is one variable, with one default. A repository answers with `--var
<name>=<value>`; one with no default, devset asks.

## `assignees`

GitHub logins assigned the automation's issues and pull requests,
comma-separated.

Empty by default · Declared by
[`github-automation`](github/github-automation.md),
[`github-dependabot`](github/github-dependabot.md)

## `authors`

Authors, comma-separated.

Empty by default · Declared by [`cargo-workspace`](cargo/cargo-workspace.md),
[`project`](project/project.md)

## `book_dir`

Directory of the mdBook, its book.toml.

Default `docs` · Declared by [`lychee`](docs/lychee.md),
[`mdbook`](docs/mdbook.md)

## `book_logo`

The book's logo in its menu bar: its path in the book, before `-light.svg` or
`-dark.svg`.

Empty by default · Declared by [`mdbook`](docs/mdbook.md)

## `book_social`

The image a shared link to the book shows: its path in the book, as
media/social.png.

Empty by default · Declared by [`mdbook`](docs/mdbook.md)

## `bump_mode`

How far the weekly bump goes: branch, or pr to open a pull request.

Default `pr` · Declared by [`github-automation`](github/github-automation.md)

## `channel`

The toolchain: nightly, the one the profiles pin, or stable.

Default `nightly` · Declared by [`rust-fmt`](rust/rust-fmt.md),
[`rust-toolchain`](rust/rust-toolchain.md)

## `collection_description`

One line: what the collection's profiles are for.

Empty by default · Declared by
[`devset-collection`](devset/devset-collection.md)

## `conduct_contact`

Where conduct is reported privately, an email address or URL; empty sends it
through GitHub's Report content.

Empty by default · Declared by [`project`](project/project.md)

## `crate`

The crate the crates.io and docs.rs badges show; empty takes the project's name.

Empty by default · Declared by [`project`](project/project.md)

## `description`

One line: what the project is.

Empty by default · Declared by [`cargo-workspace`](cargo/cargo-workspace.md),
[`github-release`](github/github-release.md), [`project`](project/project.md)

## `kind`

What the first crate builds: lib, bin or both.

Default `lib` · Declared by [`cargo-workspace`](cargo/cargo-workspace.md)

## `license`

The licence, an SPDX expression.

Default `MIT OR Apache-2.0` · Declared by
[`cargo-workspace`](cargo/cargo-workspace.md), [`project`](project/project.md)

## `line_width`

Line width, shared by the formatters and EditorConfig.

Default `100` · Declared by [`dprint`](lang/dprint.md),
[`python`](lang/python.md), [`toml`](lang/toml.md),
[`rust-fmt`](rust/rust-fmt.md), [`editorconfig`](tooling/editorconfig.md)

## `logo`

The README's logo: its path or URL before `-light.svg` or `-dark.svg`.

Empty by default · Declared by [`project`](project/project.md)

## `name`

The project's name, and its first crate's; empty takes the directory's.

Empty by default · Declared by [`cargo-workspace`](cargo/cargo-workspace.md),
[`project`](project/project.md)

## `repository`

The GitHub repository, owner/name.

No default · Declared by [`cargo-workspace`](cargo/cargo-workspace.md),
[`devset-collection`](devset/devset-collection.md), [`mdbook`](docs/mdbook.md),
[`git-changelog`](git/git-changelog.md),
[`github-labels`](github/github-labels.md),
[`github-release`](github/github-release.md),
[`github-templates`](github/github-templates.md),
[`project`](project/project.md), [`setup`](tooling/setup.md)

## `runner_labels`

Self-hosted runner labels actionlint accepts, comma-separated.

Empty by default · Declared by
[`github-workflow-lint`](github/github-workflow-lint.md)

## `rust_version`

The oldest Rust the workspace builds with.

Default `1.98` · Declared by [`cargo-workspace`](cargo/cargo-workspace.md)

# `setup`

One command readies a machine for a checkout: mise, pinned and verified, then
mise bootstrap and just setup.

```sh
devset add atxp/setup --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `tooling` · In [`rust`](../bundles/rust.md): always

`setup.sh` readies a machine to develop the repository: it clones the repository
when run elsewhere, installs mise at a pinned version checked against the
release's sha256, then runs `mise bootstrap`, which installs every tool the lock
pins and runs the task `bootstrap`: `just setup`, every `setup-*` recipe the
applied profiles bring. Run it again at any time: what is in place is kept.

```sh
curl -fsSL https://atomix-labs.github.io/atxp/setup.sh | bash -s -- <host>/<owner>/<name>
./setup.sh          # inside a checkout; or `mise bootstrap`, where mise is installed
./setup.sh --host   # also `just host`: the repository's `host-*` recipes, which may use sudo
```

`<host>/<owner>/<name>` is cloned over SSH when the host takes your key, and
over HTTPS after `gh auth login` otherwise; `SETUP_PROTOCOL=ssh` or `https`
decides instead, and any git URL works too. It clones to `./<name>` unless
`--dir` says where. `--activate` adds mise's activation to the shell's rc,
through mise; without it, the line to add is printed. `--yes`, or `CI`, asks
nothing. A devcontainer runs `./setup.sh --yes` as its `postCreateCommand`; the
feature `devcontainer` writes one, Ubuntu's base image, which is the
repository's once written.

A pinned stub is the file at a release tag:
`https://raw.githubusercontent.com/atomix-labs/atxp/<tag>/profiles/tooling/setup/files/setup.sh`.

Where the repository has a `CONTRIBUTING.md`, a block of it, Getting Started,
tells a contributor how to set up: fork and clone, then `./setup.sh`, or the one
line that clones and sets up, from `repository`, the GitHub repository as
`owner/name`.

## Owns

| File                                    | Part  | Policy | Notes                              |
| --------------------------------------- | ----- | ------ | ---------------------------------- |
| `setup.sh`                              | whole | owned  | executable                         |
| `.config/mise/conf.d/devset-setup.toml` | whole | owned  |                                    |
| `.devcontainer/devcontainer.json`       | whole | once   | template, feature `devcontainer`   |
| `CONTRIBUTING.md`                       | block | owned  | template, `CONTRIBUTING.md` exists |

## Features

| Feature        | Default | Enables |
| -------------- | ------- | ------- |
| `devcontainer` |         |         |

## Variables

| Variable     | Default | Asks                              |
| ------------ | ------- | --------------------------------- |
| `repository` | none    | The GitHub repository, owner/name |

## Requires

- [`just`](just.md)
- [`mise`](mise.md)

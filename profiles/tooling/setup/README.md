# `setup`

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
nothing. A devcontainer runs `./setup.sh --yes` as its `postCreateCommand`.

A pinned stub is the file at a release tag:
`https://raw.githubusercontent.com/atomix-labs/atxp/<tag>/profiles/tooling/setup/files/setup.sh`.

<!-- facts: written by devset-collection -->

## Owns

| File                                    | Part  | Policy | Notes      |
| --------------------------------------- | ----- | ------ | ---------- |
| `setup.sh`                              | whole | owned  | executable |
| `.config/mise/conf.d/devset-setup.toml` | whole | owned  |            |

## Requires

- [`just`](../just/README.md)
- [`mise`](../mise/README.md)

<!-- /facts -->

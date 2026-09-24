# atxp

The house's profiles for [devset](https://github.com/atomix-labs/devset), built
on the open collection,
[devset-profiles](https://github.com/atomix-labs/devset-profiles). The
collection holds what every repository agrees on; this holds the house's own
opinions on top: its lint wall, its build profiles, its toolchain, its bans, its
layout for Rust, TOML and Markdown, and its automation.

```sh
devset init --git git@github.com:atomix-labs/atxp.git --branch main --path profiles/house
./setup.sh
just check
```

`setup.sh` comes with the bundle, from the collection's `setup` atom. A machine
with nothing on it starts from the collection's published copy, which clones the
repository first:

```sh
curl -fsSL https://atomix-labs.github.io/devset-profiles/setup.sh | bash -s -- whistler.ghe.com/asia/<name>
```

## The House

`house` requires the collection's atoms at a tag, and these on top. A **flavor**
replaces the collection's atom of the same tool; the rest own their keys of a
file beside the collection's.

| Profile            | Owns                                                          | Beside or instead of        |
| ------------------ | ------------------------------------------------------------- | --------------------------- |
| `lints`            | `[workspace.lints]` keys of `Cargo.toml`                      | beside                      |
| `cargo-profiles`   | `[profile.*]` keys of `Cargo.toml`                            | beside                      |
| `rust-nightly`     | `channel`, `components` of `rust-toolchain.toml`              | instead of `rust-toolchain` |
| `rustfmt-house`    | `rustfmt.toml`                                                | instead of `rustfmt`        |
| `deny-house`       | bans and policy keys of `deny.toml`                           | beside `cargo-deny`         |
| `cargo-bump`       | `bump-cargo-bump`, and a resolver key of `.cargo/config.toml` | beside                      |
| `taplo-house`      | `[formatting]` keys and rules of `taplo.toml`                 | beside `taplo`              |
| `dprint-house`     | `dprint.json`'s keys, every plugin checksummed                | instead of `dprint`         |
| `rumdl-house`      | rules of `.rumdl.toml`                                        | instead of `rumdl`          |
| `ruff-house`       | `lint.select` of `ruff.toml`                                  | beside `ruff`               |
| `ansible-lint`     | `.ansible-lint`, on the house's ansible-core                  | —                           |
| `manifest-lint`    | the house shape of every crate manifest                       | —                           |
| `suppressions`     | every suppression proving itself                              | —                           |
| `policies-house`   | the house's workflow policies, for `conftest`                 | —                           |
| `automation-house` | `.github/automation.json`: labels, types, the bump mode       | —                           |
| `vscode-house`     | the house's keys of `.vscode/settings.json`                   | beside `vscode-rust`        |
| `gitignore-house`  | a block of `.gitignore`: local state, secrets                 | —                           |
| `claude-skills`    | `.claude/skills/`: writing rustdoc, writing manifests         | —                           |

Each profile's `README.md` says what it holds and why.

## Pins

The house's pins move here, weekly: `just bump` runs `bump-profile-pins`, which
moves every tool past the three-day cooldown and relocks it for every platform,
and `bump-rust-nightly`, which moves the nightly to the newest of the last two
weeks with every component on every platform. A repository takes them with
`devset update`.

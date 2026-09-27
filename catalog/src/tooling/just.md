# `just`

The recipe spine: imports every active profile's recipes, and `check`, `fix` and
the other verbs run them all.

```sh
devset add atxp/just --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `tooling` · In [`rust`](../bundles/rust.md): always

The spine every profile's recipes hang from. It owns a block of the `justfile`:
an `import?` of `.just/<name>.just` for each profile the repository applies,
read from devset's graph, so no list of profiles lives here, and ten recipes.

- `just check` runs every `check-*` recipe, and names each that fails. CI makes
  a job of each, so a clean local run is a clean CI run.
- `just fix` runs every `fix-*` recipe.
- `just bump` runs every `bump-*` recipe: each moves what its profile pins.
- `just nightly` runs every `nightly-*` recipe: the checks too slow for every
  change.
- `just test` runs every `test-*` recipe: the suites too slow for `just check`,
  which CI runs beside it.
- `just setup` runs every `setup-*` recipe: what a checkout needs before it
  builds. `mise bootstrap` ends in it.
- `just host` runs every `host-*` recipe: the machine's own setup, whose steps
  may ask for sudo.
- `just release` runs every `release-*` recipe, for the version
  `RELEASE_VERSION` names.
- `just package` runs every `package-*` recipe: what a release ships, built for
  this machine into `dist/`. [`github-release`](../github/github-release.md)
  runs it on each platform.
- `just publish` runs every `publish-*` recipe: what a release puts in a
  registry, as [`cargo-publish`](../cargo/cargo-publish.md) does crates.
  `github-release` runs it once the release is out.

The repository's own recipes live outside the block; where there is no
`justfile`, it starts one with a line saying so. Name one `check-<name>` and
`just check` runs it too. A recipe of the repository's own named after one of
the ten clashes with the spine's, and `just` refuses both: name it
`<verb>-<name>`, as `test-house`, and the verb runs it with the rest; one the
verb should not run, as one taking arguments, takes a name of its own.

## Owns

| File                                   | Part  | Policy | Notes    |
| -------------------------------------- | ----- | ------ | -------- |
| `justfile`                             | block | owned  | template |
| `.config/mise/conf.d/devset-just.toml` | whole | owned  |          |
| `.config/mise/mise.lock`               | keys  | owned  |          |

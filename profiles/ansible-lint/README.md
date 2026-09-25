# `ansible-lint`

ansible-lint holds every playbook and role in `.ansible/` to its `production`
profile, less the `yaml` rules, which [`yamllint`](../yamllint/README.md) holds.
It runs on the ansible-core the playbooks run on, pinned beside it and installed
with it by uv, so no rule judges a version the playbooks never meet.

It is outside the [`rust`](../rust/README.md) bundle: its check needs
`.ansible/`, so a repository with playbooks adds it.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                           | Part  | Policy | Notes |
| ---------------------------------------------- | ----- | ------ | ----- |
| `.ansible-lint`                                | whole | owned  |       |
| `.just/ansible-lint.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-ansible-lint.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                       | keys  | owned  |       |

## Recipes

- `check-ansible-lint`: Lints every playbook and role in .ansible/.

<!-- /facts -->

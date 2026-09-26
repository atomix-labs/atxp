# `ansible`

ansible-lint holds every playbook and role in `.ansible/` to its `production`
profile, less the `yaml` rules, which [`yaml`](../../lang/yaml/README.md) holds.
It runs on the ansible-core the playbooks run on, pinned beside it and installed
with it by uv, so no rule judges a version the playbooks never meet.

It is outside the [`rust`](../../bundles/rust/README.md) bundle: its check needs
`.ansible/`, so a repository with playbooks adds it.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                           | Part  | Policy | Notes |
| ---------------------------------------------- | ----- | ------ | ----- |
| `.ansible-lint`                                | whole | owned  |       |
| `.just/ansible.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-ansible.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                       | keys  | owned  |       |

## Recipes

- `check-ansible`: Lints every playbook and role in .ansible/.

<!-- /facts -->

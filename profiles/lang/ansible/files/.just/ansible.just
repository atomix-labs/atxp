# Lints every playbook and role in .ansible/.
check-ansible:
    cd .ansible && ansible-lint --nocolor -c ../.ansible-lint playbooks/ roles/

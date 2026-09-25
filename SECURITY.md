# Security Policy

How to report a vulnerability in atxp, and which releases are fixed.

## Supported Versions

The latest release only: a fix is released as a new tag, and a repository takes
it with `devset update`.

## Reporting a Vulnerability

Report it privately, through
[GitHub's security advisories](https://github.com/atomix-labs/atxp/security/advisories/new),
not in a public issue.

## Scope

The profiles ship scripts and workflows that run in other repositories' CI and
on developers' machines. A vulnerability is one that lets them do more than they
say: a script or a workflow that leaks a token or a secret, a workflow granted a
permission it does not need, or a download that is not verified against its
checksum.

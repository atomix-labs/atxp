Profiles for [devset](https://github.com/atomix-labs/devset), provided by Atomix
Labs and used across its own repositories:
[the catalog](https://atomix-labs.github.io/atxp/) says what each one does.

<!-- changes -->

## Take It

A repository that takes atxp moves to this release with:

```sh
devset update atxp --tag {tag}
```

One new to atxp starts from a bundle, or from any single profile:

```sh
devset add atxp/rust --git https://github.com/atomix-labs/atxp --tag {tag} --var repository=<owner>/<name>
```

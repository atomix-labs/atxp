# Changelog

Every release, newest first, written by [git-cliff](https://git-cliff.org) from the commits.
[BREAKING-CHANGES.md](BREAKING-CHANGES.md) says how to move across a breaking change.

## [0.3.0](https://github.com/atomix-labs/atxp/releases/tag/v0.3.0) - 2026-09-25

### Features

- [8df82fa](https://github.com/atomix-labs/atxp/commit/8df82fa69b2a1703694e2bb5c921229b0a3ae61c) *(github-release)* Run every publish recipe once the release is out
- [a284e60](https://github.com/atomix-labs/atxp/commit/a284e600a4bbb74bc0f1a1f8631248c4f6697893) *(crates-io)* Publish the workspace's crates at a release
- [9362981](https://github.com/atomix-labs/atxp/commit/93629814e71ec382029955788588341f5e6acc4d) *(just)* Add the publish verb

### Documentation

- [48c6076](https://github.com/atomix-labs/atxp/commit/48c6076c09e9244a348599a2c60a3f274f969b94) Describe the publish verb

### Miscellaneous

- [27ddad7](https://github.com/atomix-labs/atxp/commit/27ddad7f83c8dd873212d85984f420ffc2ec4dd5) Apply the changed profiles to atxp

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.2.2...v0.3.0>

## [0.2.2](https://github.com/atomix-labs/atxp/releases/tag/v0.2.2) - 2026-09-25

### Features

- [dc0567e](https://github.com/atomix-labs/atxp/commit/dc0567ee1af3e4040a2ec0c07d1fa073005cc926) *(rumdl)* Let GitHub's templates open without a heading

### Bug Fixes

- [767ce68](https://github.com/atomix-labs/atxp/commit/767ce688601328fb8ea2163112f6a8cad1d62b8d) *(github-nightly)* Fill one mise cache before the jobs
- [eb1de82](https://github.com/atomix-labs/atxp/commit/eb1de826b81fe9c814237eebf45815dfa08c53d1) *(github-ci)* Fill one mise cache before the jobs
- [0474be5](https://github.com/atomix-labs/atxp/commit/0474be5ac52aba369e1ffc88c20a501dc611a1ce) *(mise)* Let a download take two minutes

### Documentation

- [6c3f291](https://github.com/atomix-labs/atxp/commit/6c3f291733ed0bf2556f01ebf71b5fc94f05c917) *(release)* Run the checks before tagging

### CI

- [905990e](https://github.com/atomix-labs/atxp/commit/905990e53f365569ef98ca32c613f6549c8775fb) Test the profiles with the devset release atxp pins

### Miscellaneous

- [3bec679](https://github.com/atomix-labs/atxp/commit/3bec679739688b31ca7994425b0fd034026fa977) Apply the changed profiles to atxp

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.2.1...v0.2.2>

## [0.2.1](https://github.com/atomix-labs/atxp/releases/tag/v0.2.1) - 2026-09-25

### Features

- [b0ebf4f](https://github.com/atomix-labs/atxp/commit/b0ebf4f4db2af87c27a6d8d93bf47d3b5924856e) *(mdbook)* Ignore the book it builds

### Bug Fixes

- [7656fba](https://github.com/atomix-labs/atxp/commit/7656fba391455882d44259dc4c55ddf75b6083b0) *(release)* Point the quick start at each new tag
- [4dcf4e0](https://github.com/atomix-labs/atxp/commit/4dcf4e08f74497c90319005d363227f2637f154d) *(git-cliff)* Open the changelog in words any repository fits
- [fc960bf](https://github.com/atomix-labs/atxp/commit/fc960bf71ea8f6d5e6cb4ffa9e9457cff8c6922b) *(ci)* Install devset as devset-cli, on stable

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.2.0...v0.2.1>

## [0.2.0](https://github.com/atomix-labs/atxp/releases/tag/v0.2.0) - 2026-09-25

### Features

- [d07019e](https://github.com/atomix-labs/atxp/commit/d07019ec8f866ae53d25699abf3ecea828420871) *(github-release)* Publish a release from its tag
- [27ee6f2](https://github.com/atomix-labs/atxp/commit/27ee6f2338af6b007d8fa35f747a36297c80a949) *(just)* Add the package verb
- [38e6d7f](https://github.com/atomix-labs/atxp/commit/38e6d7f6dc01ef555022bfe3199041d251746d3b) *(cargo-bump)* Set every crate's version at a release
- [0aa4081](https://github.com/atomix-labs/atxp/commit/0aa40818d20a94f22bb8bcc29ef606035bcff50b) *(cargo-binaries)* Package a release's binaries for each platform
- [e4fa9ef](https://github.com/atomix-labs/atxp/commit/e4fa9efdf99580e92e6eb84df4e96783bf9cba74) *(msrv)* Build every crate on the rust-version it declares
- [e8af99b](https://github.com/atomix-labs/atxp/commit/e8af99bd1f9bbdacf5032188d9a416c9e3205ece) *(lints-nightly)* Check the nightly-only lints without a #![feature]

### Refactor

- [36596ee](https://github.com/atomix-labs/atxp/commit/36596ee05aba0948455daacd80a9a0e1e1fdf755) *(lints)* Leave the nightly-only lints to lints-nightly **breaking**

### Documentation

- [0bd432d](https://github.com/atomix-labs/atxp/commit/0bd432d49553a391dba7c6df25d2037a40666289) Describe the release flow and the new profiles

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.1.0...v0.2.0>

## [0.1.0](https://github.com/atomix-labs/atxp/releases/tag/v0.1.0) - 2026-09-25

### Features

- [366bd6a](https://github.com/atomix-labs/atxp/commit/366bd6a2ac45d6aef078f9c0f046a4ce567fcdff) Take in the profiles of devset-profiles, one profile per concern
- [72cb4a4](https://github.com/atomix-labs/atxp/commit/72cb4a4d4e932d1aaf52b3a395cd778a58ba14f7) *(typos)* Check the spelling of every file
- [5ea8e94](https://github.com/atomix-labs/atxp/commit/5ea8e94919f2a11b80532e67ce92063a336465fc) *(git-cliff)* Write the changelog from the commits at each release
- [bc3d6aa](https://github.com/atomix-labs/atxp/commit/bc3d6aa94837bdcbb9bffcd75389bf534f9654f5) *(committed)* Check each commit against Conventional Commits

### Bug Fixes

- [c8dbb1a](https://github.com/atomix-labs/atxp/commit/c8dbb1a79e10b510eddf344bbf7a4da85414d54f) *(rustup)* Install the toolchain before mise builds any tool

### Documentation

- [b81f034](https://github.com/atomix-labs/atxp/commit/b81f034cfc831b93a168b41bccbace8a1c57f469) Write atxp's documents

### CI

- [e733e6e](https://github.com/atomix-labs/atxp/commit/e733e6e9b729d8304f757e03be6a33d680f21f59) Run the profile suite on every change

### Miscellaneous

- [3765079](https://github.com/atomix-labs/atxp/commit/376507961ad6ced9099d3b29f0f3aac020c562be) Apply atxp's profiles to atxp

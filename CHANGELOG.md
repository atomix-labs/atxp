# Changelog

Every release, newest first, written by [git-cliff](https://git-cliff.org) from the commits.
[BREAKING-CHANGES.md](BREAKING-CHANGES.md) says how to move across a breaking change.

## [0.4.0](https://github.com/atomix-labs/atxp/releases/tag/v0.4.0) - 2026-09-26

### Features

- [bc19d2d](https://github.com/atomix-labs/atxp/commit/bc19d2d6149f920d17375a1d3f519b82735427fe) *(git-commits)* Take committed's release, not a cargo build
- [130f7d6](https://github.com/atomix-labs/atxp/commit/130f7d6f70f675fe6cfc3f2374aa6f6d94e26eec) *(github-ci)* Take the site's path from the repository alone **breaking**
- [d915c91](https://github.com/atomix-labs/atxp/commit/d915c911eb563e02f8dddd91520e6c40e63c87b7) Require the toolchain, the workspace and mise where profiles need them
- [a6a9155](https://github.com/atomix-labs/atxp/commit/a6a91557732c1041c67191fcea0319e5384040e5) *(devset-collection)* Move the catalog, pins and suite into a profile **breaking**
- [db92975](https://github.com/atomix-labs/atxp/commit/db92975fb4a80ced9e4fd3ce4fabb56e28e05faa) *(vscode)* Recommend and configure each applied profile's tool **breaking**
- [a66877c](https://github.com/atomix-labs/atxp/commit/a66877c22fd85db9eb0cf797ee6d994e6edccecd) *(spelling)* Leave out only what a tool writes **breaking**
- [6581502](https://github.com/atomix-labs/atxp/commit/65815025155f8e577d93c0a9b21744f4c8109df4) *(github-release)* Render the crates.io step from the graph **breaking**
- [18b6a2b](https://github.com/atomix-labs/atxp/commit/18b6a2b0956d94a83b9fd56f109ccdb1aefa3c2d) *(dprint)* Load each language profile's plugin from the graph **breaking**
- [38dbf35](https://github.com/atomix-labs/atxp/commit/38dbf35ec50a953f9a2ad434f6b8cded75d94f74) *(rust)* Give the bundle features **breaking**
- [6d0be36](https://github.com/atomix-labs/atxp/commit/6d0be363c3f171012db4113d92385e5e45159581) *(just)* Import every active profile's recipes from the graph **breaking**
- [d1f31eb](https://github.com/atomix-labs/atxp/commit/d1f31ebed90e3a258c366650357cc48f3bcfcf19) Make the house policy opt-in strict features **breaking**
- [8036ef8](https://github.com/atomix-labs/atxp/commit/8036ef86ea52c68be36aef7bd5eca2b5f88718e6) Require what each profile needs
- [98db1f8](https://github.com/atomix-labs/atxp/commit/98db1f8fdeb6d9885295b5b11969ffdcd3912c29) *(devset)* Pin devset, and fail the checks on drift
- [6944750](https://github.com/atomix-labs/atxp/commit/69447503686066d51d4b2bc95816ec4003580e27) Ignore each tool's output in the profile that brings the tool **breaking**
- [357812c](https://github.com/atomix-labs/atxp/commit/357812ceeb19d189a7a0012b48df94993b9cc5b1) *(github-workflow-lint)* Take zizmor, conftest and the policies in **breaking**
- [54c1d59](https://github.com/atomix-labs/atxp/commit/54c1d59a256419467e6d19a962337905dba7fce3) *(cargo-manifest)* Take cargo-workspace-lints and the manifest skill in **breaking**
- [a4b5150](https://github.com/atomix-labs/atxp/commit/a4b5150843dea0aefa3e26a1ec06d17c8adf923b) *(cargo-unused)* Take cargo-shear in, each tool a feature **breaking**
- [860a23d](https://github.com/atomix-labs/atxp/commit/860a23dfa49da34c6dfd186352c1525991a1e29f) *(rust-lints)* Take lints-nightly in, as the nightly feature **breaking**
- [3145ae7](https://github.com/atomix-labs/atxp/commit/3145ae7047627de0a40051326deb076e55b2b100) *(rust-toolchain)* Take rustup in **breaking**

### Refactor

- [89f0579](https://github.com/atomix-labs/atxp/commit/89f057957ab3dfc7398b9295af928c07b9e5bf98) Write every profile for devset 0.2 **breaking**
- [a6a15ca](https://github.com/atomix-labs/atxp/commit/a6a15cad3faa3121cd9fea59136e3086e8f0309c) Regroup the profiles under umbrellas, named by concern **breaking**

### Documentation

- [65bcb5e](https://github.com/atomix-labs/atxp/commit/65bcb5ed958aaa27af0199ad3a35d3c7cb247d1a) Write the tree, the bundle's features and the migration
- [91ba81a](https://github.com/atomix-labs/atxp/commit/91ba81abff86ab35404db0701ad6530b41661158) Name each linked profile by its new name

### Miscellaneous

- [b1f7fcb](https://github.com/atomix-labs/atxp/commit/b1f7fcbf584681e845840f9e42314d739a60bf15) Apply the reviewed profiles to atxp
- [56b37a2](https://github.com/atomix-labs/atxp/commit/56b37a2032727d61957f3f93ee84a92301bc4a78) Require devset 0.2.1 in every profile **breaking**
- [3f79840](https://github.com/atomix-labs/atxp/commit/3f79840833d4732a14bda705470dfe711bcedfbf) Apply atxp 0.4 to itself
- [a13693d](https://github.com/atomix-labs/atxp/commit/a13693d95fcb8276182385b6c464afeb37b8a817) Pin devset 0.2.0

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.3.3...v0.4.0>

## [0.3.3](https://github.com/atomix-labs/atxp/releases/tag/v0.3.3) - 2026-09-26

### Features

- [2ba71e3](https://github.com/atomix-labs/atxp/commit/2ba71e3bd59560e3f93753c6d2792073fcdbb1fb) *(github-release)* Attest every archive a release attaches

### Bug Fixes

- [366e517](https://github.com/atomix-labs/atxp/commit/366e517101ce082601f1dfd091cbf869aaff8cff) *(crates-io)* Package without the build while crates.io has the versions

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.3.2...v0.3.3>

## [0.3.2](https://github.com/atomix-labs/atxp/releases/tag/v0.3.2) - 2026-09-25

### Bug Fixes

- [81fc0c5](https://github.com/atomix-labs/atxp/commit/81fc0c5e98d3c28b9aeb5c9b14c02dcebb88b6ca) *(github-release)* Publish with the tools the job installs, not every locked one

### Miscellaneous

- [0687767](https://github.com/atomix-labs/atxp/commit/06877678916f71c65919a2be14bd4814a856c742) Apply the changed profiles to atxp

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.3.1...v0.3.2>

## [0.3.1](https://github.com/atomix-labs/atxp/releases/tag/v0.3.1) - 2026-09-25

### Bug Fixes

- [8839c7c](https://github.com/atomix-labs/atxp/commit/8839c7cd6b10b7a88e2151b42eacddf9a76df588) *(lychee)* Check the Markdown git does not ignore, never build output
- [046a1b0](https://github.com/atomix-labs/atxp/commit/046a1b0c379bac2c7fb1d86638e0eae7ddc12281) *(crates-io)* Check the working tree as it is, and fail with cargo's error

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.3.0...v0.3.1>

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

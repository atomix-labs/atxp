# Changelog

Every release, newest first, written by [git-cliff](https://git-cliff.org) from the commits.
[BREAKING-CHANGES.md](BREAKING-CHANGES.md) says how to move across a breaking change.

## [0.19.0](https://github.com/atomix-labs/atxp/releases/tag/v0.19.0) - 2026-10-03

### Features

- [a968854](https://github.com/atomix-labs/atxp/commit/a9688541bd199fb1ab9846588f64b1369e83aecc) Hold published crates to their crates.io page, and check a repository end to end before its first release ([#140](https://github.com/atomix-labs/atxp/pull/140)) **breaking**

### Bug Fixes

- [4fb25c7](https://github.com/atomix-labs/atxp/commit/4fb25c7fb9504ce6f20cb3442b1b5ab79c7ee5f3) *(rust-lints)* Teach unit-named accessors, derives, imports and search-first; title-case rustdoc headings ([#139](https://github.com/atomix-labs/atxp/pull/139))

### Documentation

- [fd760c4](https://github.com/atomix-labs/atxp/commit/fd760c464b58c85e5137a224c012cf7ec5ea44e3) Record the demo for v0.18.1 ([#137](https://github.com/atomix-labs/atxp/pull/137))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.18.1...v0.19.0>

## [0.18.1](https://github.com/atomix-labs/atxp/releases/tag/v0.18.1) - 2026-10-02

### Bug Fixes

- [8ec9cd3](https://github.com/atomix-labs/atxp/commit/8ec9cd3899ae3fe7e2ca767bfcafa96b8fd60eca) *(cargo-publish)* Build each crate from this check's packages, not an earlier one's ([#135](https://github.com/atomix-labs/atxp/pull/135))

### Documentation

- [c8c1d78](https://github.com/atomix-labs/atxp/commit/c8c1d7879851471dc6b1607dbc600b524d1d7a78) Record the demo for v0.18.0 ([#130](https://github.com/atomix-labs/atxp/pull/130))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.18.0...v0.18.1>

## [0.18.0](https://github.com/atomix-labs/atxp/releases/tag/v0.18.0) - 2026-09-30

### Features

- [db50e41](https://github.com/atomix-labs/atxp/commit/db50e41d6c0ecd60a8031cc72b0c54ae21ed8454) *(agents)* Rewrite what a change says so a careful person wrote it, in humanize ([#128](https://github.com/atomix-labs/atxp/pull/128))
- [f6f4f15](https://github.com/atomix-labs/atxp/commit/f6f4f155b1069c81115337c6b2ffcf1a52cf93b2) *(agents)* Review the names a change adds, in review-names ([#127](https://github.com/atomix-labs/atxp/pull/127))
- [8dea920](https://github.com/atomix-labs/atxp/commit/8dea9204d4179e19291a24e6d04da162221f5755) *(project)* Teach how a README is written here, in writing-readmes ([#125](https://github.com/atomix-labs/atxp/pull/125))
- [455825e](https://github.com/atomix-labs/atxp/commit/455825e2513eda93e5699735966710cada94cec1) *(agents)* Review a change for what an attacker can reach, in review-security ([#124](https://github.com/atomix-labs/atxp/pull/124))
- [4615c0f](https://github.com/atomix-labs/atxp/commit/4615c0f682edd71a0f5fd19a57c049af577cb905) *(agents)* Teach how prose and code read, in writing-prose and writing-readable-code ([#122](https://github.com/atomix-labs/atxp/pull/122))

### Bug Fixes

- [f113ae3](https://github.com/atomix-labs/atxp/commit/f113ae39466fea4c7297fb56560d7f8536666ed0) *(agents)* Deny a guarded recipe named after an allowed one ([#126](https://github.com/atomix-labs/atxp/pull/126))
- [f597ac6](https://github.com/atomix-labs/atxp/commit/f597ac64d59ad483a5202d18ea7485b6a98b9c63) *(rust-lints)* Give review-rust's fork commands it can run, from the repository's root ([#123](https://github.com/atomix-labs/atxp/pull/123))
- [0a243be](https://github.com/atomix-labs/atxp/commit/0a243beb339d1601fc2bfdd618638272ef76257a) *(rust-lints)* Report the error's message from a command a person runs, in writing-rust ([#120](https://github.com/atomix-labs/atxp/pull/120))
- [4a8bb94](https://github.com/atomix-labs/atxp/commit/4a8bb948a27d154668633f617d5b6c3d63b4690e) *(rust-lints)* Refuse a *Params struct in writing-rust's body, as its reference does ([#121](https://github.com/atomix-labs/atxp/pull/121))

### Documentation

- [a0cf8ae](https://github.com/atomix-labs/atxp/commit/a0cf8ae5cda1b39dfcc1e9966cd83cd257fecd0c) Record the demo for v0.17.0 ([#119](https://github.com/atomix-labs/atxp/pull/119))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.17.0...v0.18.0>

## [0.17.0](https://github.com/atomix-labs/atxp/releases/tag/v0.17.0) - 2026-09-30

### Features

- [895bc52](https://github.com/atomix-labs/atxp/commit/895bc52aa683218cbd46a31bb325479b7e08515b) *(rust-lints)* Review a Rust change against the workspace's guides, in review-rust ([#117](https://github.com/atomix-labs/atxp/pull/117))
- [05339ae](https://github.com/atomix-labs/atxp/commit/05339ae098db4e74ff5114ac42fb57fb3943f580) Bring the rustdoc and manifest skills' depth back, agreeing with the code ([#116](https://github.com/atomix-labs/atxp/pull/116))
- [ad09e84](https://github.com/atomix-labs/atxp/commit/ad09e84c89118b96f30641bb9b3fa959e7ce25a5) *(cargo-profiles)* Teach how Rust is made fast here, in tuning-rust-performance ([#113](https://github.com/atomix-labs/atxp/pull/113))
- [80942e8](https://github.com/atomix-labs/atxp/commit/80942e888788ed6094ba8427a997dafd098bc8ea) *(cargo-nextest)* Teach how tests are written here, in writing-rust-tests ([#112](https://github.com/atomix-labs/atxp/pull/112))
- [31052c0](https://github.com/atomix-labs/atxp/commit/31052c08b1d4b655cedf13981ac343de0bdb1667) *(rust-lints)* Teach unsafe code and atomics, in writing-unsafe-rust ([#111](https://github.com/atomix-labs/atxp/pull/111))
- [c819651](https://github.com/atomix-labs/atxp/commit/c819651e9d793bc6d3b8e0b9ad35ea0881a17f53) *(rust-lints)* Teach how Rust is written here, in writing-rust ([#110](https://github.com/atomix-labs/atxp/pull/110))
- [1caf6bd](https://github.com/atomix-labs/atxp/commit/1caf6bd243d157e68f329fb58290f7d617ee44a7) Report every crate a lint check fails, not the first ([#107](https://github.com/atomix-labs/atxp/pull/107))
- [08d4fe5](https://github.com/atomix-labs/atxp/commit/08d4fe5ef40d8a77bcc5d12f2ee7d62a9d6991aa) *(devset-collection)* Hold skills to the guide and pass form ([#105](https://github.com/atomix-labs/atxp/pull/105)) **breaking**

### Bug Fixes

- [2e54642](https://github.com/atomix-labs/atxp/commit/2e546428532e38164408e62a0b7eb5f0fc0be0b8) *(cargo-workspace)* Scaffold a crate as the manifest and rustdoc skills write one ([#115](https://github.com/atomix-labs/atxp/pull/115))
- [2528206](https://github.com/atomix-labs/atxp/commit/2528206612c49c81de8703d6b72a72935998eb95) *(rust-lints)* Keep the CPU floor under the nightly lints ([#114](https://github.com/atomix-labs/atxp/pull/114))
- [a80e7e5](https://github.com/atomix-labs/atxp/commit/a80e7e56fc77f0e6309cc1244dd399be942cda44) Show the skills' fragments and skeletons as text, not Rust ([#106](https://github.com/atomix-labs/atxp/pull/106))

### Documentation

- [8cc3b2a](https://github.com/atomix-labs/atxp/commit/8cc3b2a0c3e2db88e106dfdc7736759411d5dc02) Validate a skill without it, then with it, as its author ([#109](https://github.com/atomix-labs/atxp/pull/109))
- [6177840](https://github.com/atomix-labs/atxp/commit/6177840cddfecb7b31ae7e6949cdb0690abdabe6) Record the demo for v0.16.0 ([#104](https://github.com/atomix-labs/atxp/pull/104))

### Miscellaneous

- [27baeb2](https://github.com/atomix-labs/atxp/commit/27baeb295c9445e6774fd7f80f816cde5d60ff50) Compile every example the skills show ([#108](https://github.com/atomix-labs/atxp/pull/108))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.16.0...v0.17.0>

## [0.16.0](https://github.com/atomix-labs/atxp/releases/tag/v0.16.0) - 2026-09-29

### Features

- [04668cf](https://github.com/atomix-labs/atxp/commit/04668cf5d3b4816fbeeed408809969580cf516b2) *(github-labels)* Keep a few labels as code, and set most of them ([#101](https://github.com/atomix-labs/atxp/pull/101)) **breaking**

### Documentation

- [e619372](https://github.com/atomix-labs/atxp/commit/e619372a126c973087869ae60fe3521764dd6a25) Record the demo for v0.15.4 ([#102](https://github.com/atomix-labs/atxp/pull/102))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.15.4...v0.16.0>

## [0.15.4](https://github.com/atomix-labs/atxp/releases/tag/v0.15.4) - 2026-09-28

### Bug Fixes

- [3aab3fe](https://github.com/atomix-labs/atxp/commit/3aab3feb398f45b243ee3cfc60bbd7e3f1e674fd) *(github-watch)* Count a run by hand as recovery, and say each failure once ([#99](https://github.com/atomix-labs/atxp/pull/99))
- [8d39ac6](https://github.com/atomix-labs/atxp/commit/8d39ac6dd487b5eba494070608e2d7ccb92c2706) *(github-automation)* Leave a merge queue's pull requests to the app ([#98](https://github.com/atomix-labs/atxp/pull/98))
- [225494e](https://github.com/atomix-labs/atxp/commit/225494e164d61de65cfca31fcd8d2629e4c6109c) *(agents)* Check only what a turn changed, with mise's tools ([#97](https://github.com/atomix-labs/atxp/pull/97))

### Documentation

- [d4768bc](https://github.com/atomix-labs/atxp/commit/d4768bc4ef75f7f14e67a6b6603109385b8f26a5) Record the demo for v0.15.3 ([#95](https://github.com/atomix-labs/atxp/pull/95))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.15.3...v0.15.4>

## [0.15.3](https://github.com/atomix-labs/atxp/releases/tag/v0.15.3) - 2026-09-28

### Bug Fixes

- [70a4cbc](https://github.com/atomix-labs/atxp/commit/70a4cbce13bd66dbfc09a42ac91d01bc2549911b) *(github-bump)* Gate a bump that moves mise with the new mise ([#92](https://github.com/atomix-labs/atxp/pull/92))
- [db490fe](https://github.com/atomix-labs/atxp/commit/db490fe240ec37535a709757636a60f05ceb9821) *(cargo-bump)* Leave out a root its workspace excludes ([#88](https://github.com/atomix-labs/atxp/pull/88))
- [8292848](https://github.com/atomix-labs/atxp/commit/82928487875077db2441fef2a31ad37a75ddd7e3) *(devset-collection)* Lock a registry's tools without mise lock ([#87](https://github.com/atomix-labs/atxp/pull/87))

### Pins

- [935fa83](https://github.com/atomix-labs/atxp/commit/935fa83bba2db10163020bc61bf41ec7edfb7d5d) *(bump)* Move pinned tools and dependencies ([#93](https://github.com/atomix-labs/atxp/pull/93))

### Documentation

- [8e2507f](https://github.com/atomix-labs/atxp/commit/8e2507f29e958b68cd094af43de9cbbb021d393e) Record the demo for v0.15.2 ([#86](https://github.com/atomix-labs/atxp/pull/86))

### CI

- [6f89a44](https://github.com/atomix-labs/atxp/commit/6f89a44b3b630f70b3903ba4dcf5d6d544353e9b) Let atxp's weekly bump merge itself once green ([#89](https://github.com/atomix-labs/atxp/pull/89))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.15.2...v0.15.3>

## [0.15.2](https://github.com/atomix-labs/atxp/releases/tag/v0.15.2) - 2026-09-28

### Performance

- [35c9d12](https://github.com/atomix-labs/atxp/commit/35c9d12e9deee3545f4fc2375dc03bcc8a99eb53) *(vhs)* Install only the tools mise downloads in the demo ([#82](https://github.com/atomix-labs/atxp/pull/82))

### Documentation

- [d33850d](https://github.com/atomix-labs/atxp/commit/d33850d07e3edb43494a5a0926adb5dbafcbd28a) Record the demo ([#84](https://github.com/atomix-labs/atxp/pull/84))
- [b213815](https://github.com/atomix-labs/atxp/commit/b2138153291fb5c9e97377ca2d7d0ad1be213c2c) Send questions to Discussions, and link the issue forms ([#83](https://github.com/atomix-labs/atxp/pull/83))
- [5452396](https://github.com/atomix-labs/atxp/commit/54523964142cfc75f8d7c4cc239969088ba93fba) Record the demo for v0.15.1 ([#81](https://github.com/atomix-labs/atxp/pull/81))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.15.1...v0.15.2>

## [0.15.1](https://github.com/atomix-labs/atxp/releases/tag/v0.15.1) - 2026-09-28

### Bug Fixes

- [68bd5df](https://github.com/atomix-labs/atxp/commit/68bd5dfdf92db5b8e9fb32852f9636ffaf5a3e35) *(github-release)* End the notes' description with one period ([#79](https://github.com/atomix-labs/atxp/pull/79))

### Documentation

- [3b74221](https://github.com/atomix-labs/atxp/commit/3b742216d269e3bf12bb47db397c258eb915a8bd) Record the demo for v0.15.0 ([#78](https://github.com/atomix-labs/atxp/pull/78))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.15.0...v0.15.1>

## [0.15.0](https://github.com/atomix-labs/atxp/releases/tag/v0.15.0) - 2026-09-28

### Features

- [997dd37](https://github.com/atomix-labs/atxp/commit/997dd37c5a567a0b433f7013260d1b02875b46dd) *(github-release)* Write a release's notes from the repository's own file ([#73](https://github.com/atomix-labs/atxp/pull/73))
- [ad9e6c1](https://github.com/atomix-labs/atxp/commit/ad9e6c176bb499f698cdb244e7256f356dcd589a) *(project)* Offer a managed-with-devset badge in the header ([#75](https://github.com/atomix-labs/atxp/pull/75))
- [56096c3](https://github.com/atomix-labs/atxp/commit/56096c31bc82e8bcab96b9f859b837bc17e50119) *(github-templates)* Write issue forms, not Markdown templates ([#74](https://github.com/atomix-labs/atxp/pull/74)) **breaking**
- [86a4698](https://github.com/atomix-labs/atxp/commit/86a46985b468b5f7fa7c30eb04956ff51a926890) *(cargo-binaries)* Archive the binary's shell completions ([#72](https://github.com/atomix-labs/atxp/pull/72))

### Documentation

- [e037ac4](https://github.com/atomix-labs/atxp/commit/e037ac44d2bf8bddf98b82a81fe6a92b24dcf9fc) Write atxp's release notes and issue forms, and show its devset badge ([#76](https://github.com/atomix-labs/atxp/pull/76))
- [388d94f](https://github.com/atomix-labs/atxp/commit/388d94fb1fb37a066d23409d1fa8cfe424cbb644) Record the demo ([#70](https://github.com/atomix-labs/atxp/pull/70))
- [48750f2](https://github.com/atomix-labs/atxp/commit/48750f24eda19b54b9034fb3ce46997f517e356c) Record the demo for v0.14.0 ([#69](https://github.com/atomix-labs/atxp/pull/69))

### Miscellaneous

- [46a2fbc](https://github.com/atomix-labs/atxp/commit/46a2fbc146989caceb9fea0372c3963a4d5570cc) *(vhs)* Wrap the demo workflow's header at the line width ([#71](https://github.com/atomix-labs/atxp/pull/71))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.14.0...v0.15.0>

## [0.14.0](https://github.com/atomix-labs/atxp/releases/tag/v0.14.0) - 2026-09-28

### Features

- [83ab5c0](https://github.com/atomix-labs/atxp/commit/83ab5c0e5c05c70e158058447c5b43e47d845c55) *(rust-toolchain)* Make miri, rustc-dev and llvm-tools opt-in features ([#67](https://github.com/atomix-labs/atxp/pull/67)) **breaking**

### Documentation

- [540e882](https://github.com/atomix-labs/atxp/commit/540e8826938ca02b647067bc349544c7aab21e8e) Record the demo for v0.13.2 ([#66](https://github.com/atomix-labs/atxp/pull/66))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.13.2...v0.14.0>

## [0.13.2](https://github.com/atomix-labs/atxp/releases/tag/v0.13.2) - 2026-09-28

### Bug Fixes

- [ca8d870](https://github.com/atomix-labs/atxp/commit/ca8d8706f2638473c97737a966035e865d49c2c2) Retry the automation's GitHub API requests ([#63](https://github.com/atomix-labs/atxp/pull/63))

### Documentation

- [d5bb18c](https://github.com/atomix-labs/atxp/commit/d5bb18cefb09afc0b2df9f854bc19ed21e70b24f) Record the demo for v0.13.1 ([#62](https://github.com/atomix-labs/atxp/pull/62))

### Miscellaneous

- [b753c4d](https://github.com/atomix-labs/atxp/commit/b753c4db30d1fae826b269a2453d23b1589d51a0) Build the bundle's project in a directory of a fixed name ([#64](https://github.com/atomix-labs/atxp/pull/64))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.13.1...v0.13.2>

## [0.13.1](https://github.com/atomix-labs/atxp/releases/tag/v0.13.1) - 2026-09-28

### Bug Fixes

- [bd5cb6a](https://github.com/atomix-labs/atxp/commit/bd5cb6ac03134b2867bac3426dfb01078a02c064) Start no toolchain for a recipe that runs no Rust tool ([#60](https://github.com/atomix-labs/atxp/pull/60))

### Documentation

- [45ba859](https://github.com/atomix-labs/atxp/commit/45ba859f464da1bd519ee1e4b67e3a1ea890b98a) Record the demo for v0.13.0 ([#59](https://github.com/atomix-labs/atxp/pull/59))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.13.0...v0.13.1>

## [0.13.0](https://github.com/atomix-labs/atxp/releases/tag/v0.13.0) - 2026-09-28

### Features

- [5e89824](https://github.com/atomix-labs/atxp/commit/5e89824ae189446cb985839c2c23f23f7d5ccc05) *(git-changelog)* Give performance its own group ([#57](https://github.com/atomix-labs/atxp/pull/57))

### Performance

- [463dadc](https://github.com/atomix-labs/atxp/commit/463dadcb79976b05ae3506f892cf5eecd6ea55a9) Start a Rust toolchain only in jobs whose recipe runs cargo ([#56](https://github.com/atomix-labs/atxp/pull/56)) **breaking**

### Documentation

- [30969e1](https://github.com/atomix-labs/atxp/commit/30969e160e2a32e9c81a0a2e9d60de631cd516f6) Record the demo for v0.12.1 ([#55](https://github.com/atomix-labs/atxp/pull/55))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.12.1...v0.13.0>

## [0.12.1](https://github.com/atomix-labs/atxp/releases/tag/v0.12.1) - 2026-09-28

### Bug Fixes

- [9fee6cc](https://github.com/atomix-labs/atxp/commit/9fee6cc58a6e2e3fba8c4b056b3944a4c8c30b1f) *(mise)* Keep every install from rewriting the lock ([#53](https://github.com/atomix-labs/atxp/pull/53))

### Documentation

- [e24a9a4](https://github.com/atomix-labs/atxp/commit/e24a9a44da837833311b60d50e0cc2545eeac768) Record the demo for v0.12.0 ([#52](https://github.com/atomix-labs/atxp/pull/52))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.12.0...v0.12.1>

## [0.12.0](https://github.com/atomix-labs/atxp/releases/tag/v0.12.0) - 2026-09-28

### Features

- [9fcb794](https://github.com/atomix-labs/atxp/commit/9fcb79403fb754cb1ca26253e10ec790acabda42) *(setup)* Tell contributors how to get a checkout ready ([#50](https://github.com/atomix-labs/atxp/pull/50))
- [2cf8550](https://github.com/atomix-labs/atxp/commit/2cf855003878276c7a5bc67826ca84331ccd6ef9) *(git-commits)* Check a pull request's title, which its squashed commit takes ([#49](https://github.com/atomix-labs/atxp/pull/49)) **breaking**

### Performance

- [daacea5](https://github.com/atomix-labs/atxp/commit/daacea5d81a2a7b4b4aa7ae1534177f36d3b437a) Take prebuilt tools, and have CI install and cache only what a job needs ([#48](https://github.com/atomix-labs/atxp/pull/48))

### Documentation

- [cb6665b](https://github.com/atomix-labs/atxp/commit/cb6665b40c15562a11d8c99e6f2338b134d6616f) Record the demo for v0.11.1 ([#47](https://github.com/atomix-labs/atxp/pull/47))

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.11.1...v0.12.0>

## [0.11.1](https://github.com/atomix-labs/atxp/releases/tag/v0.11.1) - 2026-09-27

### Bug Fixes

- [50f8c06](https://github.com/atomix-labs/atxp/commit/50f8c060dfe020116a6ba07fe90f84c6e6eee9e8) *(devset)* Pin devset 0.5.2

### Documentation

- [37e17fe](https://github.com/atomix-labs/atxp/commit/37e17fec4e46fd3551679a791d92f23336c31329) Say what an older devset does to mdBook's lock entries at v0.11.0
- [329dbdb](https://github.com/atomix-labs/atxp/commit/329dbdb7880d314dd599c987ddda000131467cfd) Record the demo for v0.11.0 ([#44](https://github.com/atomix-labs/atxp/pull/44))

### Miscellaneous

- [7bb755d](https://github.com/atomix-labs/atxp/commit/7bb755d0b4740ddea9d750624a8f8869d072774f) Apply the profiles' changes to atxp

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.11.0...v0.11.1>

## [0.11.0](https://github.com/atomix-labs/atxp/releases/tag/v0.11.0) - 2026-09-27

### Features

- [1c47f02](https://github.com/atomix-labs/atxp/commit/1c47f02b780d0f9f8335c5da32f367b8f5ff2fc0) Publish atxp's catalog at atomix-labs.github.io/atxp
- [926e956](https://github.com/atomix-labs/atxp/commit/926e9566f85a915ea258342d0a02a72eefb63baa) *(devset-collection)* Build a catalog site with the feature `site`
- [8b0f936](https://github.com/atomix-labs/atxp/commit/8b0f9361df48ed51a9172a79ca3bac9ab7d79863) *(mdbook-tool)* Pin mdBook in a profile of its own

### Bug Fixes

- [80abcb0](https://github.com/atomix-labs/atxp/commit/80abcb012649058ca133dd86a242fbea66b02ee1) *(github-automation)* Leave a pull request to a person where main requires checks
- [cff898a](https://github.com/atomix-labs/atxp/commit/cff898ac4953f7243d56c6489103339a62736038) *(github-automation)* Skip the checks of a pull request merged at once
- [6bcdf15](https://github.com/atomix-labs/atxp/commit/6bcdf1549ff9bf13daab4c18d0921a92f7761032) *(markdown)* Leave the case of a book summary's part titles alone

### Documentation

- [f654768](https://github.com/atomix-labs/atxp/commit/f654768d0485e72107e6f4384e32cf26a5c88792) Ask for devset 0.5.0 in the README's house profile
- [91c70c6](https://github.com/atomix-labs/atxp/commit/91c70c66591e5452b1307178d332463efbcdc3dd) Write the v0.11.0 migration
- [bec88bd](https://github.com/atomix-labs/atxp/commit/bec88bd96da45b738dbf24f26d8c65e6429f6c40) Record the demo ([#41](https://github.com/atomix-labs/atxp/pull/41))
- [3e4158a](https://github.com/atomix-labs/atxp/commit/3e4158a4e329b048c32d39b17271e2b29171ffc1) Record atxp's demo without the questions devset 0.5.0 no longer asks

### Miscellaneous

- [73e5400](https://github.com/atomix-labs/atxp/commit/73e54002b4af7415d34a3fb6a759e8e10d2a7a3c) Apply the profiles' changes to atxp, the catalog site on

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.10.0...v0.11.0>

## [0.10.0](https://github.com/atomix-labs/atxp/releases/tag/v0.10.0) - 2026-09-27

### Features

- [67714ad](https://github.com/atomix-labs/atxp/commit/67714ad2e452265eec249788f14867cdad56fa4e) Require devset 0.5.0 **breaking**
- [8a2a9ea](https://github.com/atomix-labs/atxp/commit/8a2a9ead3267721bd57bc469d28fbc78627b329f) *(vhs)* Label and assign the demo's pull request, and merge it with `merge`
- [e83e4bc](https://github.com/atomix-labs/atxp/commit/e83e4bc529f2da6fc229f1ae92976b191b12025d) *(github-automation)* Label, assign and comment on the automation's pull requests **breaking**

### Documentation

- [d9fc49c](https://github.com/atomix-labs/atxp/commit/d9fc49c6a9b438cb7842856b143d5a139e3ba42e) Write the v0.10.0 migration
- [1bd45e1](https://github.com/atomix-labs/atxp/commit/1bd45e13f1f1ae25628290d73a9e99d673da5855) Record the demo for v0.9.1

### Miscellaneous

- [2e6ac01](https://github.com/atomix-labs/atxp/commit/2e6ac01ef2db48b4ab8fd3303853f77b95bf4e4c) Apply the profiles' changes to atxp

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.9.1...v0.10.0>

## [0.9.1](https://github.com/atomix-labs/atxp/releases/tag/v0.9.1) - 2026-09-27

### Bug Fixes

- [93be780](https://github.com/atomix-labs/atxp/commit/93be780b2949a8ea112834b53dcc323bc7c9bdef) *(cargo-manifest)* Check only the workspace's own manifests

### Documentation

- [50e15a0](https://github.com/atomix-labs/atxp/commit/50e15a0c9953cb6f04d2602d1edbf8d9a520682b) Record the demo for v0.9.0

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.9.0...v0.9.1>

## [0.9.0](https://github.com/atomix-labs/atxp/releases/tag/v0.9.0) - 2026-09-27

### Features

- [8407392](https://github.com/atomix-labs/atxp/commit/8407392d90a07fbbbde96f12834dea0874eb95f6) *(mdbook)* Theme the book in GitHub's palette, with a logo and social tags

### Bug Fixes

- [4461291](https://github.com/atomix-labs/atxp/commit/446129160ea221560b50b8c53cd27778dbcf798c) *(markdown)* Keep an mdBook summary's part titles

### Documentation

- [7806c24](https://github.com/atomix-labs/atxp/commit/7806c247f6c12e567c08f2bc6d67d0cda22ba112) Record the demo for v0.8.1

### Miscellaneous

- [a1ea338](https://github.com/atomix-labs/atxp/commit/a1ea338c3b67e4b96e9a306336c8aa42800c7135) Apply the profiles' changes to atxp

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.8.1...v0.9.0>

## [0.8.1](https://github.com/atomix-labs/atxp/releases/tag/v0.8.1) - 2026-09-27

### Documentation

- [7d65dc4](https://github.com/atomix-labs/atxp/commit/7d65dc4b6f838e6962a3679ee488eae543c70ad4) Describe atxp as profiles for any repository, from Atomix Labs
- [c3fb084](https://github.com/atomix-labs/atxp/commit/c3fb0840701998c26816f26630a7c92c9c48665a) Record the demo for v0.8.0

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.8.0...v0.8.1>

## [0.8.0](https://github.com/atomix-labs/atxp/releases/tag/v0.8.0) - 2026-09-27

### Features

- [cad3fa2](https://github.com/atomix-labs/atxp/commit/cad3fa204391678185560e90fac531a3996f9e2e) *(vhs)* Record the README's demo from tapes on each release
- [374af42](https://github.com/atomix-labs/atxp/commit/374af42c11af1837667a947732fbfb7b4cdc2f37) *(project)* Write the README's whole header, logo and tagline included **breaking**
- [e3036d2](https://github.com/atomix-labs/atxp/commit/e3036d277dc561d5a3c1e9a9731bca74ee0d2302) *(markdown)* Admit the README header's HTML

### Bug Fixes

- [7751f34](https://github.com/atomix-labs/atxp/commit/7751f34189c038816631cf629301bc0f456e8990) Show each recipe's whole summary in just --list

### Documentation

- [f5a3bf1](https://github.com/atomix-labs/atxp/commit/f5a3bf191e2543e7ab105db7988fb6f4becb36ef) Say release-readme moves the demo's tag too
- [de7712f](https://github.com/atomix-labs/atxp/commit/de7712ffcb32879c4698713b269d63ce5e199db3) *(project)* Take a URL for the logo where the README is shown elsewhere
- [60383aa](https://github.com/atomix-labs/atxp/commit/60383aa5b3ee923eded5c261c1f454177d7dbf68) Write the v0.8.0 migration
- [5b84b92](https://github.com/atomix-labs/atxp/commit/5b84b92b2818f67aa85f8e87b0ad30bf63b5c75d) Open atxp's README on its header and demo
- [15d898d](https://github.com/atomix-labs/atxp/commit/15d898d7171f55e0e6e02387e5db5b1774e8c6e5) Record atxp's demo
- [4303f68](https://github.com/atomix-labs/atxp/commit/4303f68a0ac4d9dfc92cb3a67f38f41f28b3a18b) Draw atxp's logo

### Miscellaneous

- [e1658c2](https://github.com/atomix-labs/atxp/commit/e1658c21bfaf1d4c73edbf5f572414fb7346266d) Apply the profiles' changes to atxp

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.7.0...v0.8.0>

## [0.7.0](https://github.com/atomix-labs/atxp/releases/tag/v0.7.0) - 2026-09-27

### Features

- [d519d05](https://github.com/atomix-labs/atxp/commit/d519d055163c95db75a00d6d2397d8b2957448a3) *(agents)* Allow devset explain in place of devset features
- [a986eec](https://github.com/atomix-labs/atxp/commit/a986eec13c59cfafa5aa424283397bd19a4b58c9) *(devset)* Move a source with update --tag, and take back a conflict with apply --abort

### Documentation

- [d7bdb7f](https://github.com/atomix-labs/atxp/commit/d7bdb7f7f852a3c778f350087045c26dbaff29fc) Write the v0.7.0 migration
- [24eca7e](https://github.com/atomix-labs/atxp/commit/24eca7e6aba4a303c6d0941f47236a6c7e62ffef) *(devset)* Teach the ten commands in using-devset

### Miscellaneous

- [313396a](https://github.com/atomix-labs/atxp/commit/313396a877a244e4fc8b7d30b159bac8ffee22ed) Apply the profiles' changes to atxp
- [4598374](https://github.com/atomix-labs/atxp/commit/45983744353932b98599d058895fa72882ef2812) Start the suite's targets with add
- [ed43dd2](https://github.com/atomix-labs/atxp/commit/ed43dd2b54e66c647fe6045a2d82488847300d4d) Require and pin devset 0.4.0 **breaking**

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.6.2...v0.7.0>

## [0.6.2](https://github.com/atomix-labs/atxp/releases/tag/v0.6.2) - 2026-09-26

### Bug Fixes

- [e82d649](https://github.com/atomix-labs/atxp/commit/e82d649bf0a1af49936331a48084b5a9efcd5052) *(cargo-binaries)* Leave the archives it packages into dist/ out of git

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.6.1...v0.6.2>

## [0.6.1](https://github.com/atomix-labs/atxp/releases/tag/v0.6.1) - 2026-09-26

### Features

- [750b212](https://github.com/atomix-labs/atxp/commit/750b212b8ff883f35504b792140d3ad4a3a3e79f) *(project)* Name the crate the crates.io and docs.rs badges show

### Bug Fixes

- [0276122](https://github.com/atomix-labs/atxp/commit/02761224d0649ef74b41695b5abb925fedb959e2) *(rust-doc)* Hold a crate to naming the workspace's crates it depends on, whatever their prefix
- [463faf3](https://github.com/atomix-labs/atxp/commit/463faf38b2034780288ebc643e086fafaddb7900) *(cargo-manifest)* Keep a table's layout when putting its dependencies in their groups
- [4e99684](https://github.com/atomix-labs/atxp/commit/4e996847f4e011c86a2d930d69893ee5fc7ccf0a) *(devset-collection)* Show what a recipe does with a feature on as the feature, not the template
- [06bdb8f](https://github.com/atomix-labs/atxp/commit/06bdb8f71fa21adad5bc0efaf49f2f4a64236623) Leave what is vendored to upstream in the shell and spelling checks
- [e09c85f](https://github.com/atomix-labs/atxp/commit/e09c85fb88349589ce6b677aaa0245a9e0378cd2) *(rust-doc)* Read no word in a code span as filler
- [191e223](https://github.com/atomix-labs/atxp/commit/191e22330a8b7975bcb77f2a3028ffd20138b674) *(lychee)* Leave the book's pages to mdbook's check of the built book
- [e7fbb6d](https://github.com/atomix-labs/atxp/commit/e7fbb6d4dcd454301a79b288398d3c9ef89f4f0a) *(rust-lints)* Allow a crate that enables the nightly lints' features itself

### Documentation

- [3bf165e](https://github.com/atomix-labs/atxp/commit/3bf165e6a11248bf6f75288d9bb7947a6a279302) Say how a repository adopting the profiles keeps its recipes and excludes

### Miscellaneous

- [abd0893](https://github.com/atomix-labs/atxp/commit/abd089344836b2cbf60866593ce42a76fa41d51b) Apply the profiles' changes to atxp

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.6.0...v0.6.1>

## [0.6.0](https://github.com/atomix-labs/atxp/releases/tag/v0.6.0) - 2026-09-26

### Features

- [3808a3a](https://github.com/atomix-labs/atxp/commit/3808a3ad7b169edf1b1cdf7cd0408ee8c4086f76) *(devset)* Teach turning features on and off, and placing a block
- [0b1d8b1](https://github.com/atomix-labs/atxp/commit/0b1d8b1648ce3bbf72ba4a4ff91ddfeae20f44f0) *(mdbook)* Link the prose to the API by path, under a page grouping its crates **breaking**
- [4b5f288](https://github.com/atomix-labs/atxp/commit/4b5f288b95f882f583027ed815cd5415bf9d7764) *(cargo-manifest)* Put each dependency under its group with fix-cargo-manifest

### Bug Fixes

- [40a4e33](https://github.com/atomix-labs/atxp/commit/40a4e33f27f94ed7e331ed24f0877c3de37ca2cb) *(cargo-unused)* Put back the group markers a removal takes

### Documentation

- [49e227e](https://github.com/atomix-labs/atxp/commit/49e227e27d3a5d22f79f69b45d4f16c02822bf17) Write the v0.6.0 migration

### Miscellaneous

- [3219030](https://github.com/atomix-labs/atxp/commit/3219030c3803a0439aa9906f67ae2d2d9b25b3cf) Apply the profiles' changes to atxp
- [27db7da](https://github.com/atomix-labs/atxp/commit/27db7da5a3bd551cddce1bbcf89136ad4999ec18) Require and pin devset 0.3.0 **breaking**

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.5.0...v0.6.0>

## [0.5.0](https://github.com/atomix-labs/atxp/releases/tag/v0.5.0) - 2026-09-26

### Features

- [5722710](https://github.com/atomix-labs/atxp/commit/5722710a06ff4feabf409940aa92168cb65fc2e0) *(rust)* Turn on the agent layer and every skill with agents
- [c95db73](https://github.com/atomix-labs/atxp/commit/c95db73bb3eb22692cf5ee2bfb003087d286f916) *(rust-doc)* Write the rustdoc skill for any repository
- [b1918c6](https://github.com/atomix-labs/atxp/commit/b1918c6a80b12e697fd375923e406c758f13617b) *(cargo-manifest)* Write the manifest skill for any repository
- [8fed4d5](https://github.com/atomix-labs/atxp/commit/8fed4d542470169b2c8832ce740a5fd1159bf013) *(cargo-deny)* Say in AGENTS.md what a failure asks of the maintainer
- [5352fc5](https://github.com/atomix-labs/atxp/commit/5352fc5a8b89d543aa10ceb71d39b13936031a38) *(git-commits)* Say the commit rules in AGENTS.md
- [c7650f5](https://github.com/atomix-labs/atxp/commit/c7650f5453aacea46932677ba1eab8c073386086) *(mdbook)* Teach writing the book, and say in AGENTS.md how to check it
- [90e3f5c](https://github.com/atomix-labs/atxp/commit/90e3f5c2cb16e0cc6bb4dc7df7ca85c507aff92f) *(github-ci)* Teach fixing CI
- [4954bd8](https://github.com/atomix-labs/atxp/commit/4954bd892532ef2a90866097fd7b41d2ec5ef3fd) *(github-release)* Teach cutting a release
- [2014694](https://github.com/atomix-labs/atxp/commit/20146947f6118b94005344d1c07c2078cdee7b7c) *(devset-collection)* Teach authoring profiles
- [313d44a](https://github.com/atomix-labs/atxp/commit/313d44ac03709eb184d85a8ab99a803ab0b05411) *(devset)* Teach using devset
- [deca639](https://github.com/atomix-labs/atxp/commit/deca639e1b14f525e76337c62cc9eb151472ee8f) *(agents)* AGENTS.md, CLAUDE.md, the allow-list and the Stop hook
- [62e3988](https://github.com/atomix-labs/atxp/commit/62e3988d0e14309396f79ca79acfe21aecbb93ac) *(devset-collection)* Hold skills to the house form
- [16602d7](https://github.com/atomix-labs/atxp/commit/16602d7815158e3d42cab8c4db0beeca778dc403) *(rust)* Take project and the templates with publish and oss
- [36befcd](https://github.com/atomix-labs/atxp/commit/36befcd78759ae21c751d1c73425cdb4e5a8db83) *(github-templates)* Scaffold issue templates and the pull request checklist
- [c5fcde0](https://github.com/atomix-labs/atxp/commit/c5fcde0e98c6290b0351c40c7d1f69e4c1f83afa) *(devset)* Move each source's tag past the cooldown in the weekly bump
- [fb1c701](https://github.com/atomix-labs/atxp/commit/fb1c7017b7a234ae1da673f90d75165c094f360d) *(mdbook)* Scaffold the book, and give it math, diagrams and the API **breaking**
- [b46acfb](https://github.com/atomix-labs/atxp/commit/b46acfbdfe0fc4ecf1381dbcdb4d15d02fa78923) *(github-ci)* Publish a site only under the pages feature **breaking**
- [26216f3](https://github.com/atomix-labs/atxp/commit/26216f356cb11809dde6f219c5851bf174ea36dd) *(devset-collection)* Hold manifests to devset's schemas
- [2613638](https://github.com/atomix-labs/atxp/commit/2613638bf591f606837bdf84d9b5615bfa10f612) *(vscode)* Follow the language profiles' features
- [ee4bf61](https://github.com/atomix-labs/atxp/commit/ee4bf612f25ab04c3188d16f627dbaa03a261e90) *(dprint)* Load a language's plugin only where its profile formats
- [3233906](https://github.com/atomix-labs/atxp/commit/323390693a9d19e4ac0f203aa60e33dabea3a3b0) *(python)* Lint and format as features
- [26214a2](https://github.com/atomix-labs/atxp/commit/26214a2bac49ed1df9e89dee98a21cbf0cf49af3) *(shell)* Lint as a feature
- [a414122](https://github.com/atomix-labs/atxp/commit/a414122a367cff945074964dc41418b2974a461f) *(yaml)* Format and lint as features
- [21c625a](https://github.com/atomix-labs/atxp/commit/21c625ad33d6a541ea9fc1a610ba2c3a361db162) *(toml)* Format, lint and devset's schemas as features
- [eedb8bf](https://github.com/atomix-labs/atxp/commit/eedb8bf605cdf764167b34019be639fdeb459f5e) *(markdown)* Format, lint and links as features
- [760c140](https://github.com/atomix-labs/atxp/commit/760c1409e1c021bf3e0317b88bb1ac79d7672db5) *(rust-doc)* Run the house's doc lint under strict **breaking**
- [06060fb](https://github.com/atomix-labs/atxp/commit/06060fb8e53356ea7d874209ab1af1d50d59437e) *(rust-toolchain)* Offer the stable channel
- [babde0c](https://github.com/atomix-labs/atxp/commit/babde0cff549495e554ff7b238cadf7bfc08f384) *(project)* Scaffold the documents a project keeps
- [716572a](https://github.com/atomix-labs/atxp/commit/716572a3a38e0e34b3b6d26f7d5d9989a648a3be) *(git-commits)* Say the commit rules in CONTRIBUTING.md
- [92d9d6f](https://github.com/atomix-labs/atxp/commit/92d9d6fd983182ec5aad206158fa6b94ed9542a7) *(rust-fmt)* Own rustfmt.toml's keys, not the whole file **breaking**
- [b8f41da](https://github.com/atomix-labs/atxp/commit/b8f41daa000c688996224cc797dadecf8e9d0673) *(setup)* Offer a devcontainer that runs the setup script
- [e3cd349](https://github.com/atomix-labs/atxp/commit/e3cd3492bc0e99d918bb0bda5ca6803bbd549cf7) *(devset-collection)* Scaffold collection.toml
- [907a8f4](https://github.com/atomix-labs/atxp/commit/907a8f4f669068f039ff964e90f1b70784f96b15) *(github-release)* Scaffold RELEASE.md
- [585af14](https://github.com/atomix-labs/atxp/commit/585af14b65f1819353c1877752ca4b517c6e5d78) *(lychee)* Scaffold lychee.toml
- [e423011](https://github.com/atomix-labs/atxp/commit/e423011dc097592848f50cd1bb1575e864fa49b6) *(just)* Start a justfile where there is none
- [b12d599](https://github.com/atomix-labs/atxp/commit/b12d5999a134ef94841c78722466634ec908df94) *(git-changelog)* Scaffold CHANGELOG.md
- [4a80fcc](https://github.com/atomix-labs/atxp/commit/4a80fcca4ed991184dd73bfdbf490d99fbd8d0a8) *(git-ignore)* Start a .gitignore where there is none
- [f8ca54e](https://github.com/atomix-labs/atxp/commit/f8ca54ea6eb54d9bbedf6f949cd7cfdadc9313d7) *(cargo-workspace)* Scaffold a workspace where there is none **breaking**

### Bug Fixes

- [b704df7](https://github.com/atomix-labs/atxp/commit/b704df70fff1de253adb15058d0419f89790139f) *(git-ignore)* Ignore only Claude Code's local settings, so its shared ones are committed
- [73a38a6](https://github.com/atomix-labs/atxp/commit/73a38a601e68bfba34837a0af64eb0655c3fb95b) *(cargo-workspace)* List the first crate in the workspace's dependencies only for the -cli crate
- [ed9cc2d](https://github.com/atomix-labs/atxp/commit/ed9cc2d090af3be09d192c0b026423e96dd5a544) Run only the recipes the profiles define in the skills

### Documentation

- [3b3c929](https://github.com/atomix-labs/atxp/commit/3b3c929194e0cd25378021fb4d2743138f1d0108) Write the scaffolds, the agent layer and the v0.5.0 migration
- [9949d4a](https://github.com/atomix-labs/atxp/commit/9949d4a9447b6b96f785828095d8e6e05ac62e46) Give atxp an AGENTS.md, and apply the agent layer to it
- [970416e](https://github.com/atomix-labs/atxp/commit/970416ec39dddcacb16c55182a33ee34558c0c9d) *(cargo-publish)* Say what crates.io asks, and that publish brings it

### Miscellaneous

- [29b6219](https://github.com/atomix-labs/atxp/commit/29b6219f8d80d92853b04400a290386d345bbeb6) Apply the profiles' changes to atxp
- [5096541](https://github.com/atomix-labs/atxp/commit/50965419f7eaac397cfdd34aa329af8fcb439eff) Apply the rich profiles to atxp
- [a11cdb9](https://github.com/atomix-labs/atxp/commit/a11cdb9fa8658bc3687dde9d79002b824d2eb147) Require and pin devset 0.2.2 **breaking**
- [a70d58c](https://github.com/atomix-labs/atxp/commit/a70d58c7f7ee4c6ce98ff1aaf3a00cbc8fbf2921) Apply the bundle to nothing, with each feature, and check it

**Full Changelog**: <https://github.com/atomix-labs/atxp/compare/v0.4.0...v0.5.0>

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

# Changelog

Every release, newest first, written by [git-cliff](https://git-cliff.org) from the commits.
[BREAKING-CHANGES.md](BREAKING-CHANGES.md) says how to move across a breaking change.

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

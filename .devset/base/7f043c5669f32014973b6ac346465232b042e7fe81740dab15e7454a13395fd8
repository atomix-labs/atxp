"""A collection's catalog: the README's tables of profiles and variables, the facts block of every
profile's README, and the rules every profile keeps.

Usage: catalog.py [--check] [--dprint] [--site <dir> --repository <owner/name>]

Run in the collection's root. Its profiles are every `profile.toml` under `profiles/`, at any depth,
but a profile's own payloads; the directory each is in groups it. With no flag, writes the README's
tables and every profile's facts. `--check` writes nothing, and fails when any of them is stale, or a
profile or a skill it ships breaks a rule. `--dprint` formats what it writes with dprint, as the
repository formats its Markdown. `--site` also writes the catalog site's pages under `<dir>/src/`,
as site_pages.py says, and the README's tables then name the groups and link to the site. A
directory with no profiles has no catalog.
"""

import bisect
import itertools
import json
import os
import re
import subprocess
import sys
import tomllib
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from site_pages import Site

PROFILES = Path("profiles")
README = Path("README.md")
# The regions this script writes, each between its two markers.
CATALOG = ("<!-- catalog: written by devset-collection -->", "<!-- /catalog -->")
VARIABLES = ("<!-- variables: written by devset-collection -->", "<!-- /variables -->")
FACTS = ("<!-- facts: written by devset-collection -->", "<!-- /facts -->")
STALE = "run `just fix-devset-collection`"
RECIPES = ".just/"
PINS = ".config/mise/conf.d/"
# A pin file's name carries this prefix, so no tool reads it as its own configuration.
PIN_PREFIX = "devset-"
# What a recipe does, each run together by the `just` spine: `just check`, `just fix`, and so on.
VERBS = (
    "check",
    "fix",
    "bump",
    "nightly",
    "test",
    "setup",
    "host",
    "release",
    "package",
    "publish",
)
# A recipe's first line: `@` if quiet, its name, then any parameters, defaults and all; an
# assignment, `x := y`, is not one.
RECIPE = re.compile(r"^@?([a-z][a-z0-9-]*)(?:\s+[^:]*?)?:(?!=)")
# Lines between a recipe's comment and its name: an attribute, `[private]`, or a template's tag.
BETWEEN = ("[", "{%", "{#")
# A Rust tool a recipe runs, which makes it one whose CI job restores and saves Cargo's build; and
# the attribute that says so, which github-ci's plan reads.
RUST_TOOL = re.compile(r"\b(cargo|rustc|rustdoc|rustup)\b")
RUST_TAG = '[metadata("rust")]'
# A workflow step that installs mise, and the version it names.
MISE_ACTION = re.compile(r"^(\s*)(- )?uses: jdx/mise-action@")
MISE_VERSION = re.compile(r"^\s+version:\s*(\S+)\s*$")
PARTS = {"file": "whole", "keys": "keys", "block": "block"}
# A directory that holds this many of a profile's files is shown once, with the count.
GROUPED = 3
# A skill a profile ships: its entry point, in the directory that names it.
SKILLS = ".claude/skills/"
SKILL = re.compile(rf"^{re.escape(SKILLS)}([^/]+)/SKILL\.md$")
# A skill's name is what it does: a guide's a gerund phrase, `writing-rustdoc`; a pass's an
# imperative, `review-rust`, the command a person types.
GERUND = re.compile(r"[a-z]+ing(?:-[a-z0-9]+)*")
IMPERATIVE = re.compile(r"(?![a-z]+ing(?:-|$))[a-z]+(?:-[a-z0-9]+)*")
# A skill's front matter, between its two `---` lines, one field to a line.
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
# A guide says what it is for; a pass also says how it runs: forked, with the session's model,
# while the agent waits for its report.
GUIDE = {"name", "description"}
PASS = GUIDE | {"argument-hint", "context", "agent", "model", "background"}
PASS_MAY = {"allowed-tools"}
PASS_RUNS = {"context": "fork", "model": "inherit", "background": "false"}
PASS_AGENTS = {"Explore", "general-purpose"}
DESCRIPTION = 1024
# Claude re-attaches the first 5,000 tokens of each skill after compaction: a body within this
# survives whole.
BODY = 18_000
# Code in Markdown: a block fenced by backticks or tildes, closed by a fence as long, or a span,
# which may wrap, closed by as many backticks as open it.
CODE = re.compile(
    r"^(?P<ticks>`{3,}).*?^(?P=ticks)`*[ \t]*$"
    r"|^(?P<tildes>~{3,}).*?^(?P=tildes)~*[ \t]*$"
    r"|(?P<span>`+)(?!`).+?(?<!`)(?P=span)(?!`)",
    re.DOTALL | re.MULTILINE,
)
# A link to a file beside it: relative, not a URL or an anchor.
LINK = re.compile(r"\]\((?![a-z]+:|#)([^)#\s]+)")
# The recipes run in code: `just` opening a command, after any variables it sets and through any
# `mise exec --`, then each recipe it runs, the first a word and the rest `<verb>-<name>`; a
# placeholder, as `just check-<name>`, names none.
JUST = re.compile(
    r"(?:^|&&|\|\||;)\s*(?:[A-Z_][A-Z0-9_]*=\S*\s+)*(?:mise\s+exec\s+--\s+)?just\s+"
    r"([a-z][a-z0-9-]*[a-z0-9](?![\w<-])(?:[ \t]+[a-z][a-z0-9]*-[a-z0-9-]*[a-z0-9](?![\w<-]))*)",
    re.M,
)
# A template's line that is only a tag or a comment, which renders to nothing: one, so a line that
# holds text between two tags is not.
TAG = re.compile(r"^\s*(?:\{%(?:(?!%\}).)*%\}|\{#(?:(?!#\}).)*#\})\s*$")
# What a recipe's comment says only with a feature on, which its facts mark with the feature.
WITH = re.compile(
    r'\{%-?\s*if\s+"([a-z0-9-]+)"\s+in\s+devset\.features\s*-?%\}(.*?)\{%-?\s*endif\s*-?%\}',
    re.DOTALL,
)
# What a template renders: a tag, a comment or an expression.
TEMPLATED = re.compile(r"\{[%#{]")
# A template's conditions: what opens, turns and closes one, what a condition names, and a
# variable that holds another layer's features.
TAGS = re.compile(r"\{%-?\s*(if|elif|else|endif|set)\b(.*?)-?%\}", re.DOTALL)
ACTIVE = re.compile(r'"([a-z0-9-]+)"\s+in\s+devset\.profiles')
OWN = re.compile(r'"([a-z0-9-]+)"\s+in\s+devset\.features')
ON = re.compile(r'"([a-z0-9-]+)"\s+in\s+([a-z_]+)\b')
LAYER = re.compile(
    r'([a-z_]+)\s*=\s*devset\.layers\s*\|\s*selectattr\(\s*"profile",\s*"equalto",\s*"([a-z0-9-]+)"'
)
# A condition that holds nothing it names: one of several alternatives, or a negation.
EITHER = re.compile(r"(?<![\w-])(?:or|not)(?![\w-])")
# What an agent reads: every recipe or skill it names must be there when it reads it.
READ = (SKILLS, "AGENTS.md", "CLAUDE.md")
# A code block, at any indent, fenced by backticks or tildes and closed by a fence as long: its
# info string and its body; how a Rust block is marked; what a failing one says it fails with.
FENCE = re.compile(
    r"^ *(?P<fence>`{3,}|~{3,})(?P<info>[^\n`]*)\n(?P<body>.*?)^ *(?P=fence)[`~]*[ \t]*$",
    re.DOTALL | re.MULTILINE,
)
RUST = {"rust", "rust,compile_fail"}
FAILS = re.compile(r"\A *// fails: (?:clippy::[a-z_]+|[a-z_]+|E\d{4})\n")


@dataclass(frozen=True)
class Profile:
    """A profile: its directory, from the collection's root, and its manifest."""

    path: Path
    manifest: dict

    @property
    def name(self):
        """Its name, as `[profile] name` gives it."""
        return self.manifest.get("profile", {}).get("name", "")

    @property
    def description(self):
        """Its one line."""
        return self.manifest.get("profile", {}).get("description", "")

    @property
    def group(self):
        """The directory under `profiles/` that holds its own, or `""` for one at the top."""
        parent = self.path.parent.relative_to(PROFILES)
        return "" if parent == Path() else parent.as_posix()

    @property
    def files(self):
        """Every file it manages, by its path in the target, with its entry."""
        return self.manifest.get("files", {})

    @property
    def requires(self):
        """Every profile it requires, by name, with its entry."""
        return self.manifest.get("requires", {})

    @property
    def features(self):
        """Its features but `default`, each with what it enables."""
        return {k: v for k, v in self.manifest.get("features", {}).items() if k != "default"}

    @property
    def readme(self):
        """Its README."""
        return self.path / "README.md"

    def link(self, start):
        """A link to its README from the directory `start`, named for it."""
        return f"[`{self.name}`]({Path(os.path.relpath(self.readme, start)).as_posix()})"


def profiles():
    """Every profile, in the order of their paths."""
    manifests = sorted(PROFILES.rglob("profile.toml"))
    directories = {manifest.parent for manifest in manifests}
    found = []
    for manifest in manifests:
        # A profile.toml in a profile's `files/` is that profile's payload.
        if any(manifest.is_relative_to(directory / "files") for directory in directories):
            continue
        with manifest.open("rb") as file:
            found.append(Profile(manifest.parent, tomllib.load(file)))
    return found


def recipes(profile):
    """The recipes in its `.just/<name>.just`, each with the comment lines just above it, joined by
    newlines."""
    path = f"{RECIPES}{profile.name}.just"
    if path not in profile.files:
        return []
    found, comment = [], []
    for line in (profile.path / "files" / path).read_text().splitlines():
        if line.startswith("#"):
            comment.append(line.removeprefix("#").strip())
            continue
        if line.startswith(BETWEEN):
            continue
        if recipe := RECIPE.match(line):
            found.append((recipe.group(1), "\n".join(comment)))
        comment = []
    return found


def rust_recipes(profile):
    """Each `check-*` and `nightly-*` recipe in its `.just/<name>.just`: whether its body runs a Rust
    tool, and whether `[metadata("rust")]` is above it."""
    path = f"{RECIPES}{profile.name}.just"
    if path not in profile.files:
        return []
    found, tagged, current = [], False, None
    for line in (profile.path / "files" / path).read_text().splitlines():
        # A body's lines are indented; a blank line or a template's tag at the margin continues it.
        if not line.strip() or line.startswith(("{%", "{#")):
            continue
        if line[:1] in (" ", "\t"):
            if current and not line.strip().startswith("#") and RUST_TOOL.search(line):
                current[1] = True
            continue
        current = None
        if line.startswith("["):
            tagged = tagged or line.strip() == RUST_TAG
        elif (recipe := RECIPE.match(line)) and recipe.group(1).startswith(("check-", "nightly-")):
            current = [recipe.group(1), False, tagged]
            found.append(current)
            tagged = False
        elif not line.startswith("#"):
            tagged = False
    return [tuple(entry) for entry in found]


def described(comment):
    """A recipe's comment as its facts show it: each sentence it says only with a feature on,
    closed by that feature, as `(with `api`)`."""

    def marked(match):
        text = match.group(2).rstrip()
        stop = len(text) - len(text.rstrip(".!?"))
        return f"{text[: len(text) - stop]} (with `{match.group(1)}`){text[len(text) - stop :]}"

    return WITH.sub(marked, comment)


def by_name(found):
    """The profiles, by name: more than one where a name is shared."""
    named = defaultdict(list)
    for profile in found:
        named[profile.name].append(profile)
    return named


def problems(found):
    """Each way a profile breaks the collection's rules."""
    named = by_name(found)
    out = [
        f"{', '.join(str(p.path) for p in same)}: profiles share the name `{name}`"
        for name, same in named.items()
        if len(same) > 1
    ]
    definers = {recipe: profile.name for profile in found for recipe, _ in recipes(profile)}
    shipped = {
        skill.group(1): (profile.name, set(entry.get("when", {}).get("features", [])))
        for profile in found
        for path, entry in profile.files.items()
        if (skill := SKILL.match(path))
    }
    for profile in found:
        out += profile_problems(profile, named) + skill_problems(profile, definers, shipped)
    return out + variable_problems(found) + mise_problems(found)


def profile_problems(profile, named):
    """Each way `profile` breaks a rule of its own."""
    name, where, out = profile.name, profile.path, []
    if name != profile.path.name:
        out.append(f"{where}: [profile] name must be `{profile.path.name}`, its directory")
    if not profile.description or "\n" in profile.description or profile.description.endswith("."):
        out.append(f"{where}: a description is one line, with no closing period")
    if not profile.readme.is_file():
        out.append(f"{where}: has no README.md")
    elif profile.readme.read_text().splitlines()[:1] != [f"# `{name}`"]:
        out.append(f"{where}: README.md opens with the title # `{name}`")
    if not profile.files and not profile.requires:
        out.append(f"{where}: owns no file and requires no profile")
    for path in profile.files:
        if path.startswith(RECIPES) and not helper(name, path):
            out.append(
                f"{where}: {path} is none of {RECIPES}{name}.just, {RECIPES}{name}.<ext> and a file"
                f" under {RECIPES}{name}/"
            )
        if path.startswith(PINS) and path != f"{PINS}{PIN_PREFIX}{name}.toml":
            out.append(f"{where}: {path} is not its pin file, {PINS}{PIN_PREFIX}{name}.toml")
    for recipe, comment in recipes(profile):
        if not re.fullmatch(rf"(?:{'|'.join(VERBS)})-{re.escape(name)}", recipe):
            out.append(
                f"{where}: recipe `{recipe}` is not `<verb>-{name}`, a verb of {code(VERBS)}"
            )
        if "\n" in comment:
            out.append(
                f"{where}: recipe `{recipe}`'s comment is more than one line, and `just --list`"
                " shows only the last: say more in a comment above it, apart by a blank line"
            )
        if TEMPLATED.search(described(comment)):
            out.append(
                f"{where}: recipe `{recipe}`'s comment templates more than a feature's"
                ' `{% if "<feature>" in devset.features %}`, which its facts cannot show'
            )
    for recipe, runs, tagged in rust_recipes(profile):
        if runs and not tagged:
            out.append(
                f"{where}: recipe `{recipe}` runs a Rust tool: `{RUST_TAG}` above it gives its CI"
                " job Cargo's cache"
            )
        if tagged and not runs:
            out.append(f"{where}: recipe `{recipe}` carries `{RUST_TAG}` but runs no Rust tool")
    for required, spec in profile.requires.items():
        if "git" not in spec and required not in named:
            out.append(f"{where}: requires `{required}`, which is no profile of the collection")
    return out


def skill_problems(profile, definers, shipped):
    """Each way what `profile` gives an agent to read breaks the form: a skill's front matter,
    files and fences, and a recipe or skill it names where that one may be absent. `definers`
    gives the profile that defines each recipe, `shipped` the profile that ships each skill, with
    the features it ships with."""
    where, out = profile.path, []
    for path, entry in profile.files.items():
        if not path.startswith(READ):
            continue
        text = (profile.path / "files" / path).read_text()
        if skill := SKILL.match(path):
            name = skill.group(1)
            out += [f"{where}: {path}: {problem}" for problem in front_matter(name, text)]
            out += [f"{where}: {problem}" for problem in reference_problems(profile, name)]
        out += [f"{where}: {path}: {problem}" for problem in fence_problems(text)]
        gates = gate_problems(profile, path, entry, text, definers, shipped)
        out += [f"{where}: {path} {problem}" for problem in gates]
    return out


def gate_problems(profile, path, entry, text, definers, shipped):
    """Each recipe or skill that `text`, the file at `path` that `profile` ships as `entry`, names
    where that one may be absent: another profile's, with no condition in force on that profile,
    or a skill with no condition on the feature it ships with. A skill may name itself. Only a
    template's conditions hold anything: any other file ships its tags as they stand."""
    template = entry.get("template", False)
    when = entry.get("when", {})
    mine = set(when.get("features", []))
    present = {profile.name, *when.get("profiles", [])}
    present |= {required for required, spec in profile.requires.items() if not spec.get("optional")}
    own = path.removeprefix(SKILLS).split("/")[0] if path.startswith(SKILLS) else None
    events, out = (conditions(text) if template else [(0, frozenset())]), []
    for span in CODE.finditer(masked(text) if template else text):
        inner = span.group(0).strip("`")
        start = span.start() + len(span.group(0)) - len(span.group(0).lstrip("`"))
        for match in JUST.finditer(inner):
            for recipe in match.group(1).split():
                owner = definers.get(recipe)
                if recipe in VERBS or owner in present:
                    continue
                if owner is None:
                    out.append(f"names `just {recipe}`, which no profile of the collection defines")
                elif not active(owner, at(events, start + match.start(1))):
                    out.append(
                        f"names `just {recipe}`, which {owner} defines: gate it on"
                        f' `"{owner}" in devset.profiles`'
                    )
        name = inner.removeprefix("/")
        if name not in shipped or name == own:
            continue
        owner, features = shipped[name]
        held = at(events, span.start())
        if owner == profile.name:
            lacking = features - mine - {c[1] for c in held if c[0] == "feature"}
            if lacking:
                out.append(
                    f"names `{name}`, which ships only with its {code(sorted(lacking))}: gate it on"
                    " that feature, through `devset.features`"
                )
            continue
        lacking = {feature for feature in features if ("layer", owner, feature) not in held}
        if lacking:
            out.append(
                f"names `{name}`, which ships only with {owner}'s {code(sorted(lacking))}: gate it"
                " on that feature, through `devset.layers`"
            )
        elif owner not in present and not active(owner, held):
            out.append(
                f'names `{name}`, which {owner} ships: gate it on `"{owner}" in devset.profiles`'
            )
    return out


def active(owner, held):
    """Whether the conditions `held` hold the profile `owner` active: by name, or by a feature."""
    return any(condition[0] in ("profile", "layer") and condition[1] == owner for condition in held)


def masked(text):
    """`text` with each line that is only a template's tag or comment blanked, which renders to
    nothing: what it says is not the file's. Each offset stays where it was."""
    return "".join(
        re.sub(r"[^\n]", " ", line) if TAG.match(line) else line
        for line in text.splitlines(keepends=True)
    )


def conditions(text):
    """The conditions in force from each offset of `text` on: `("profile", p)` where the profile
    `p` is active, `("layer", p, f)` where its feature `f` is on, `("feature", f)` where this
    profile's is. An `else` holds nothing its `if` did, and an `or` or a `not` nothing it names."""
    layers, stack, events = {}, [], [(0, frozenset())]
    for tag in TAGS.finditer(text):
        kind, rest = tag.group(1), tag.group(2)
        if kind == "set":
            if layer := LAYER.search(rest):
                layers[layer.group(1)] = layer.group(2)
            continue
        held = frozenset()
        if not EITHER.search(rest):
            held = frozenset(
                {("profile", p) for p in ACTIVE.findall(rest)}
                | {("feature", f) for f in OWN.findall(rest)}
                | {("layer", layers[v], f) for f, v in ON.findall(rest) if v in layers}
            )
        if kind == "if":
            stack.append(held)
        elif kind in ("elif", "else") and stack:
            stack[-1] = held if kind == "elif" else frozenset()
        elif kind == "endif" and stack:
            stack.pop()
        events.append((tag.end(), frozenset().union(*stack)))
    return events


def at(events, offset):
    """The conditions in force at `offset`, of the `events` `conditions()` gives."""
    return events[bisect.bisect_right([start for start, _ in events], offset) - 1][1]


def fence_problems(text):
    """Each Rust block of `text` marked other than `rust` or `rust,compile_fail`, a failing block
    that does not say what it fails with, and a Rust block that holds template syntax: each is
    compiled as it stands."""
    out = []
    for fence in FENCE.finditer(text):
        info, body = fence.group("info").strip(), fence.group("body")
        line = text.count("\n", 0, fence.start()) + 1
        if (info.startswith("rust") or info.split(",")[0] == "rs") and info not in RUST:
            out.append(
                f"line {line}: a Rust block is `rust` or `rust,compile_fail`, never `{info}`"
            )
        if info == "rust,compile_fail" and not FAILS.match(body):
            out.append(f"line {line}: a failing block opens `// fails: <lint or error code>`")
        if info in RUST and TEMPLATED.search(body):
            out.append(f"line {line}: a Rust block holds no template syntax")
    return out


def front_matter(name, text):
    """Each way the front matter and body of the skill `name`'s SKILL.md, `text`, break the form: a
    guide's, or a pass's where it runs forked."""
    block = FRONT_MATTER.match(text)
    pairs = (line.partition(": ")[::2] for line in block.group(1).splitlines()) if block else ()
    fields = {key: value.strip('"') for key, value in pairs}
    if "context" in fields:
        missing, extra = PASS - set(fields), set(fields) - PASS - PASS_MAY
        if missing or extra or any(fields[k] != v for k, v in PASS_RUNS.items()):
            return [
                f"a pass runs forked: its front matter holds {code(sorted(PASS))}, with "
                "`context: fork`, `model: inherit` and `background: false`, and may hold "
                "`allowed-tools`"
            ]
        if fields["agent"] not in PASS_AGENTS:
            return [f"a pass runs on {code(sorted(PASS_AGENTS))}"]
        shape, example = IMPERATIVE, "an imperative such as `review-rust`"
    else:
        if set(fields) != GUIDE:
            return [
                f"a guide's front matter holds {code(sorted(GUIDE))}, each on one line, and"
                " nothing else"
            ]
        shape, example = GERUND, "a gerund phrase such as `writing-rustdoc`"
    out = []
    if fields["name"] != name or not shape.fullmatch(name):
        out.append(f"`name` is `{name}`, its directory, {example}")
    description = fields["description"]
    if not description.startswith("Use when") or len(description) >= DESCRIPTION:
        out.append(f"`description` starts `Use when`, under {DESCRIPTION} characters")
    if len(text) - block.end() > BODY:
        out.append(f"the body is over {BODY} characters: move depth into `references/`")
    return out


def reference_problems(profile, skill):
    """Each file of the skill that the profile does not declare, each reference its SKILL.md does
    not name, by a link or in code, and each relative link in the skill that leads outside what its
    profile ships: a skill of another profile is named, never linked."""
    root = f"{SKILLS}{skill}/"
    declared = {path for path in profile.files if path.startswith(root)}
    base = profile.path / "files"
    on_disk = {p.relative_to(base).as_posix() for p in (base / root).rglob("*") if p.is_file()}
    out = [f"{path} is not an entry of profile.toml" for path in sorted(on_disk - declared)]
    body = (base / root / "SKILL.md").read_text()
    spans = [span.group(0).strip("`") for span in CODE.finditer(body) if span.group("span")]
    named = {os.path.normpath(root + target) for target in links(body) + spans}
    out += [
        f"{path} is named nowhere in its SKILL.md, so no agent reads it"
        for path in sorted(declared)
        if path.startswith(root + "references/") and path.endswith(".md") and path not in named
    ]
    for path in sorted(declared & on_disk):
        if not path.endswith(".md"):
            continue
        here = os.path.dirname(path)
        for target in links((base / path).read_text()):
            resolved = os.path.normpath(os.path.join(here, target))
            if resolved not in profile.files:
                out.append(f"{path} links `{target}`, which its profile does not ship")
    return out


def links(text):
    """The target of each relative link in `text`, outside its code: a link in a Rust example is
    rustdoc's, not the skill's."""
    return LINK.findall(CODE.sub("", text))


def helper(name, path):
    """Whether `path` in `.just/` is `name`'s: `.just/<name>.<ext>`, or under `.just/<name>/`."""
    rest = path.removeprefix(RECIPES)
    return rest.startswith(f"{name}/") or ("/" not in rest and Path(rest).stem == name)


def variable_problems(found):
    """Each variable declared differently by two profiles: it is one variable, with one default."""
    declared = defaultdict(lambda: defaultdict(list))
    for profile in found:
        for name, spec in profile.manifest.get("vars", {}).items():
            declared[name][json.dumps(spec, sort_keys=True)].append(profile.name)
    out = []
    for name, ways in sorted(declared.items()):
        if len(ways) > 1:
            by = sorted(itertools.chain(*ways.values()))
            out.append(f"variable `{name}`: declared differently by {code(by)}")
    return out


def mise_problems(found):
    """Each workflow a profile ships whose mise differs from the others', or is not named at all."""
    installs = defaultdict(set)
    for profile in found:
        for path in profile.files:
            if path.startswith(".github/workflows/"):
                workflow = profile.path / "files" / path
                for version in mise_versions(workflow.read_text()):
                    installs[version].add(workflow)
    out = [
        f"{path}: a mise-action step names no version" for path in sorted(installs.pop(None, ()))
    ]
    if len(installs) > 1:
        for version, paths in sorted(installs.items()):
            others = ", ".join(sorted(installs.keys() - {version}))
            out += [f"{path}: installs mise {version}, others {others}" for path in sorted(paths)]
    return out


def mise_versions(text):
    """The mise each mise-action step in a workflow installs, `None` where it names none."""
    lines = text.splitlines()
    for at, line in enumerate(lines):
        step = MISE_ACTION.match(line)
        if not step:
            continue
        indent = len(step.group(1)) + len(step.group(2) or "")
        version = None
        for body in lines[at + 1 :]:
            if body.strip() and len(body) - len(body.lstrip()) < indent:
                break
            if named := MISE_VERSION.match(body):
                version = named.group(1).strip("\"'")
        yield version


def owns(profile):
    """What it owns, as the catalog shows it: recipes and pins aside, and a directory that holds
    several of its files shown once."""
    files = {p: spec for p, spec in profile.files.items() if not p.startswith((RECIPES, PINS))}
    shown, notes, grouped = [], set(), set()
    for path, spec in files.items():
        scope, policy = spec.get("scope", "file"), spec.get("policy", "owned")
        note = ", ".join(n for n in (scope != "file" and scope, policy != "owned" and policy) if n)
        directory = group(path, files)
        if directory in grouped:
            continue
        if directory:
            grouped.add(directory)
            count = sum(1 for other in files if other.startswith(directory))
            shown.append((f"`{directory}` ({count} files)", note))
        else:
            shown.append((f"`{path}`", note))
        notes.add(note)
    if len(notes) == 1:
        (note,) = notes
        return ", ".join(path for path, _ in shown) + (f" ({note})" if note else "")
    return ", ".join(path + (f" ({note})" if note else "") for path, note in shown)


def group(path, files):
    """The shallowest directory of `path` that holds GROUPED or more of `files`, with a slash."""
    parts = Path(path).parts[:-1]
    for depth in range(1, len(parts) + 1):
        directory = "/".join(parts[:depth]) + "/"
        if sum(1 for other in files if other.startswith(directory)) >= GROUPED:
            return directory
    return None


def table(found):
    """The README's catalog: under each group's heading, a table of the profiles that own files,
    then those that only require others, each with what it requires and its features."""
    groups = defaultdict(list)
    for profile in found:
        groups[profile.group].append(profile)
    sections = []
    for name, members in sorted(groups.items()):
        lines = [f"### `{name}`", ""] if name else []
        owning = [profile for profile in members if profile.files]
        requiring = [profile for profile in members if not profile.files]
        if owning:
            lines += ["| Profile | What | Owns |", "| --- | --- | --- |"]
            lines += [f"| {p.link(Path())} | {p.description} | {owns(p)} |" for p in owning]
        if owning and requiring:
            lines.append("")
        for profile in requiring:
            required = [r for r, spec in profile.requires.items() if not spec.get("optional")]
            line = f"- {profile.link(Path())}: {profile.description}."
            if required:
                line += f" Requires {code(required)}."
            if profile.features:
                line += f" Features: {code(profile.features)}."
            lines.append(line)
        sections.append("\n".join(lines))
    return "\n\n".join(sections) + "\n"


def variables(found):
    """The README's table of variables: each one's default, what it asks, who declares it."""
    seen = {}
    for profile in found:
        for name, spec in profile.manifest.get("vars", {}).items():
            seen.setdefault(name, (spec, []))[1].append(profile.link(Path()))
    rows = ["| Variable | Default | Asks | Declared by |", "| --- | --- | --- | --- |"]
    for name, (spec, by) in sorted(seen.items()):
        rows.append(
            f"| `{name}` | {default(spec)} | {spec.get('prompt', name)} | {', '.join(by)} |"
        )
    return "\n".join(rows) + "\n"


def default(spec):
    """A variable's default, as the tables show it."""
    if "default" not in spec:
        return "none"
    return f"`{spec['default']}`" if spec["default"] else "empty"


def code(names):
    """`names`, each in backticks, comma-separated."""
    return ", ".join(f"`{name}`" for name in names)


def facts(profile, named):
    """Its facts: the files it owns, its features, its recipes, its variables, what it requires."""
    out = []
    if profile.files:
        out += ["## Owns", "", "| File | Part | Policy | Notes |", "| --- | --- | --- | --- |"]
        for path, spec in profile.files.items():
            part = PARTS[spec.get("scope", "file")]
            policy = "once" if "scaffold" in spec else spec.get("policy", "owned")
            out.append(f"| `{path}` | {part} | {policy} | {', '.join(notes(spec))} |")
        out.append("")
    if profile.features:
        defaults = profile.manifest["features"].get("default", [])
        out += ["## Features", "", "| Feature | Default | Enables |", "| --- | --- | --- |"]
        for name, enables in profile.features.items():
            out.append(f"| `{name}` | {'yes' if name in defaults else ''} | {code(enables)} |")
        out.append("")
    listed = recipes(profile)
    if listed:
        out += ["## Recipes", ""]
        out += [
            f"- `{name}`: {described(doc.replace(chr(10), ' '))}" if doc else f"- `{name}`"
            for name, doc in listed
        ]
        out.append("")
    declared = profile.manifest.get("vars", {})
    if declared:
        out += ["## Variables", "", "| Variable | Default | Asks |", "| --- | --- | --- |"]
        for name, spec in declared.items():
            out.append(f"| `{name}` | {default(spec)} | {spec.get('prompt', name)} |")
        out.append("")
    if profile.requires:
        out += ["## Requires", ""]
        for name, spec in profile.requires.items():
            local = "git" not in spec and name in named
            link = named[name][0].link(profile.path) if local else f"`{name}`"
            how = requirement(spec)
            out.append(f"- {link}: {', '.join(how)}" if how else f"- {link}")
        out.append("")
    return "\n".join(out)


def notes(spec):
    """What the facts note of a file: how it is written, its scaffold, and when it applies."""
    out = [note for note in ("template", "executable") if spec.get(note)]
    if "scaffold" in spec:
        out.append(f"scaffold `{spec['scaffold']}`")
    when = spec.get("when", {})
    out += [f"feature `{feature}`" for feature in when.get("features", [])]
    out += [f"profile `{profile}`" for profile in when.get("profiles", [])]
    out += [f"`{var}` one of {code(values)}" for var, values in when.get("vars", {}).items()]
    out += [f"`{path}` exists" for path in when.get("exists", [])]
    return out


def requirement(spec):
    """How a profile is required: from another source, optionally, with features, without its
    default ones."""
    out = [f"from {spec['git']}"] if "git" in spec else []
    if spec.get("optional"):
        out.append("optional")
    if spec.get("features"):
        out.append(f"with {code(spec['features'])}")
    if spec.get("default-features") is False:
        out.append("without its default features")
    return out


def between(path, text, markers, body):
    """`text`, the file at `path`, with what lies between `markers` replaced by `body`, the markers
    added at the end where missing."""
    begin, end = markers
    if begin not in text:
        text = text.rstrip("\n") + f"\n\n{begin}\n{end}\n"
    start = text.index(begin) + len(begin)
    stop = text.find(end, start)
    if stop < 0:
        sys.exit(f"{path}: {begin} has no {end} after it")
    return f"{text[:start]}\n\n{body}\n{text[stop:]}"


def formatted(path, text, dprint):
    """`text` as `dprint fmt` leaves the file at `path`, where dprint formats; else as it is."""
    if not dprint:
        return text
    try:
        result = subprocess.run(
            ["dprint", "fmt", "--stdin", str(path)],
            input=text,
            text=True,
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        sys.exit(f"dprint could not format {path}: {getattr(error, 'stderr', '') or error}")
    return result.stdout


def readme(found, dprint, site=None):
    """The README, its tables current; the variables' only where a profile declares one. Where the
    site holds them, the README names the groups and links to it."""
    text = README.read_text() if README.is_file() else ""
    text = between(README, text, CATALOG, site.readme_catalog() if site else table(found))
    if VARIABLES[0] in text or any(profile.manifest.get("vars") for profile in found):
        body = site.readme_variables() if site else variables(found)
        text = between(README, text, VARIABLES, body)
    return formatted(README, text, dprint)


def options(args):
    """The flags, and the values `--site` and `--repository` take; `None` when they are wrong."""
    flags, values, rest = set(), {}, list(args)
    while rest:
        arg = rest.pop(0)
        if arg in {"--check", "--dprint"}:
            flags.add(arg)
        elif arg in {"--site", "--repository"} and rest:
            values[arg] = rest.pop(0)
        else:
            return None
    if ("--site" in values) != ("--repository" in values):
        return None
    return flags, values


def main(args):
    parsed = options(args)
    if parsed is None:
        usage = next(line for line in __doc__.splitlines() if line.startswith("Usage:"))
        print(usage, file=sys.stderr)
        return 2
    args, values = parsed
    found = profiles()
    if not found:
        return 0
    dprint = "--dprint" in args
    named = by_name(found)
    site = Site(found, named, values["--repository"]) if "--site" in values else None
    wanted = {README: readme(found, dprint, site)}
    for profile in found:
        if profile.readme.is_file():
            text = between(profile.readme, profile.readme.read_text(), FACTS, facts(profile, named))
            wanted[profile.readme] = formatted(profile.readme, text, dprint)
    if site:
        for path, text in site.pages(values["--site"], wanted).items():
            wanted[path] = formatted(path, text, dprint)
    if "--check" not in args:
        for path, text in wanted.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        if site:
            src = Path(values["--site"]) / "src"
            for old in sorted(src.rglob("*.md")):
                if old not in wanted:
                    old.unlink()
        return 0
    stale = [
        f"{path} is stale: {STALE}"
        for path, text in wanted.items()
        if not path.is_file() or path.read_text() != text
    ]
    out = problems(found) + stale
    for problem in out:
        print(problem, file=sys.stderr)
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

"""A collection's catalog: the README's tables of profiles and variables, the facts block of every
profile's README, and the rules every profile keeps.

Usage: catalog.py [--check] [--dprint]

Run in the collection's root. Its profiles are every `profile.toml` under `profiles/`, at any depth,
but a profile's own payloads; the directory each is in groups it. With no flag, writes the README's
tables and every profile's facts. `--check` writes nothing, and fails when any of them is stale or a
profile breaks a rule. `--dprint` formats what it writes with dprint, as the repository formats its
Markdown. A directory with no profiles has no catalog.
"""

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
# A recipe's first line: its name, then any parameters; an assignment, `x := y`, is not one.
RECIPE = re.compile(r"^([a-z][a-z0-9-]*)(?:\s+[^:=]*)?:(?!=)")
# A workflow step that installs mise, and the version it names.
MISE_ACTION = re.compile(r"^(\s*)(- )?uses: jdx/mise-action@")
MISE_VERSION = re.compile(r"^\s+version:\s*(\S+)\s*$")
PARTS = {"file": "whole", "keys": "keys", "block": "block"}
# A directory that holds this many of a profile's files is shown once, with the count.
GROUPED = 3


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
    """The recipes in its `.just/<name>.just`, each with the comment lines just above it."""
    path = f"{RECIPES}{profile.name}.just"
    if path not in profile.files:
        return []
    found, comment = [], []
    for line in (profile.path / "files" / path).read_text().splitlines():
        if line.startswith("#"):
            comment.append(line.removeprefix("#").strip())
            continue
        if recipe := RECIPE.match(line):
            found.append((recipe.group(1), " ".join(comment)))
        comment = []
    return found


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
    for profile in found:
        out += profile_problems(profile, named)
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
    for recipe, _ in recipes(profile):
        if not re.fullmatch(rf"(?:{'|'.join(VERBS)})-{re.escape(name)}", recipe):
            out.append(
                f"{where}: recipe `{recipe}` is not `<verb>-{name}`, a verb of {code(VERBS)}"
            )
    for required in profile.requires:
        if required not in named:
            out.append(f"{where}: requires `{required}`, which is no profile of the collection")
    return out


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
        out += [f"- `{name}`: {doc}" if doc else f"- `{name}`" for name, doc in listed]
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
            link = named[name][0].link(profile.path) if name in named else f"`{name}`"
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
    """How a profile is required: optionally, with features, without its default ones."""
    out = ["optional"] if spec.get("optional") else []
    if spec.get("features"):
        out.append(f"with {code(spec['features'])}")
    if spec.get("default-features") is False:
        out.append("without its default features")
    return out


def between(text, markers, body):
    """`text` with what lies between `markers` replaced by `body`, the markers added at the end
    where missing."""
    begin, end = markers
    if begin not in text:
        text = text.rstrip("\n") + f"\n\n{begin}\n{end}\n"
    start, stop = text.index(begin) + len(begin), text.index(end)
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


def readme(found, dprint):
    """The README, its tables current; the variables' only where a profile declares one."""
    text = README.read_text() if README.is_file() else ""
    text = between(text, CATALOG, table(found))
    if VARIABLES[0] in text or any(profile.manifest.get("vars") for profile in found):
        text = between(text, VARIABLES, variables(found))
    return formatted(README, text, dprint)


def main(args):
    if not set(args) <= {"--check", "--dprint"}:
        usage = next(line for line in __doc__.splitlines() if line.startswith("Usage:"))
        print(usage, file=sys.stderr)
        return 2
    found = profiles()
    if not found:
        return 0
    dprint = "--dprint" in args
    named = by_name(found)
    wanted = {README: readme(found, dprint)}
    for profile in found:
        if profile.readme.is_file():
            text = between(profile.readme.read_text(), FACTS, facts(profile, named))
            wanted[profile.readme] = formatted(profile.readme, text, dprint)
    if "--check" not in args:
        for path, text in wanted.items():
            path.write_text(text)
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

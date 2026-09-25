#!/usr/bin/env python3
"""The catalog: the README's tables of profiles and variables, each profile README's facts, and the
`just` spine's imports.

Usage: scripts/catalog.py [--check]

Reads every `profiles/<id>/profile.toml`. With no flag, writes the README's tables, the facts block
of every profile's README, and the spine's `import?` lines. `--check` writes nothing, and fails when
any of them is stale or a profile breaks a rule of CONTRIBUTING.md.
"""

import re
import subprocess
import sys

if sys.version_info < (3, 11):
    sys.exit("scripts/catalog.py needs Python 3.11 or later, which has tomllib")

from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parent.parent
PROFILES = ROOT / "profiles"
README = ROOT / "README.md"
SPINE = PROFILES / "just" / "files" / "justfile"
# The regions this script writes, each between its two markers.
CATALOG = ("<!-- catalog: written by scripts/catalog.py -->", "<!-- /catalog -->")
VARIABLES = ("<!-- variables: written by scripts/catalog.py -->", "<!-- /variables -->")
FACTS = ("<!-- facts: written by scripts/catalog.py -->", "<!-- /facts -->")
RECIPES = ".just/"
PINS = ".config/mise/conf.d/"
# A pin file's name carries this prefix, so no tool reads it as its own configuration.
PIN_PREFIX = "devset-"
# What a recipe does, each run together by the spine: `just check`, `just fix`, and so on.
VERBS = ("check", "fix", "bump", "nightly", "setup", "host", "release")
# A recipe's first line: its name, then any parameters; an assignment, `x := y`, is not one.
RECIPE = re.compile(r"^([a-z][a-z0-9-]*)(?:\s+[^:=]*)?:(?!=)")
PARTS = {"file": "whole", "keys": "keys", "block": "block"}


def profiles():
    """Every profile, by id, with its manifest."""
    found = {}
    for manifest in sorted(PROFILES.glob("*/profile.toml")):
        with manifest.open("rb") as file:
            found[manifest.parent.name] = tomllib.load(file)
    return found


def own(atom, manifest, prefix):
    """The one recipe or pin file an atom ships under `prefix`, if it ships exactly one."""
    suffix = ".just" if prefix == RECIPES else ".toml"
    paths = [p for p in manifest.get("files", {}) if p.startswith(prefix) and p.endswith(suffix)]
    return paths[0] if len(paths) == 1 else None


def base(atom, path):
    """Whether `path` is named for `atom`; a pin file carries PIN_PREFIX before the name."""
    stem = Path(path).stem
    if path.startswith(PINS):
        if not stem.startswith(PIN_PREFIX):
            return False
        stem = stem.removeprefix(PIN_PREFIX)
    return stem == atom


def recipes(atom, manifest):
    """The recipes an atom's `.just/` file defines, each with the comment lines just above it."""
    path = own(atom, manifest, RECIPES)
    if path is None:
        return []
    found, comment = [], []
    for line in (PROFILES / atom / "files" / path).read_text().splitlines():
        if line.startswith("#"):
            comment.append(line.removeprefix("#").strip())
            continue
        recipe = RECIPE.match(line)
        if recipe:
            found.append((recipe.group(1), " ".join(comment)))
        comment = []
    return found


def problems(found):
    """Each way a profile breaks the rules of CONTRIBUTING.md."""
    out = []
    for atom, manifest in found.items():
        meta, files = manifest.get("profile", {}), manifest.get("files", {})
        where = f"profiles/{atom}"
        if meta.get("name") != atom:
            out.append(f"{where}: [profile] name must be `{atom}`, its directory")
        description = meta.get("description", "")
        if not description or description.endswith("."):
            out.append(f"{where}: a description is one line, with no closing period")
        readme = PROFILES / atom / "README.md"
        if not readme.is_file():
            out.append(f"{where}: has no README.md")
        elif readme.read_text().splitlines()[:1] != [f"# `{atom}`"]:
            out.append(f"{where}: README.md opens with the title # `{atom}`")
        if not files and not meta.get("requires"):
            out.append(f"{where}: owns no file and requires no profile")
        for prefix, suffix, what in [(RECIPES, ".just", "recipes"), (PINS, ".toml", "pins")]:
            paths = [path for path in files if path.startswith(prefix)]
            named = [path for path in paths if path.endswith(suffix)]
            if len(named) > 1 or any(not base(atom, path) for path in paths):
                name = f"{PIN_PREFIX}{atom}" if prefix == PINS else atom
                out.append(f"{where}: its {what} live in one {prefix}{name}{suffix}, helpers beside it")
        stem = Path(own(atom, manifest, RECIPES) or atom).stem
        for recipe, _ in recipes(atom, manifest):
            if not re.fullmatch(rf"({'|'.join(VERBS)})-{re.escape(stem)}", recipe):
                out.append(f"{where}: recipe `{recipe}` is not one of `{'|'.join(VERBS)}-{stem}`")
    return out


# A directory that holds this many of a profile's files is shown once, with the count.
GROUPED = 3


def owns(manifest):
    """What a manifest owns, as the catalog shows it: recipes and pins aside, and a directory holding
    several of its files shown once."""
    files = {path: spec for path, spec in manifest.get("files", {}).items() if not path.startswith((RECIPES, PINS))}
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
    """The README's catalog: every profile that owns files in a table, then the bundle."""
    rows = ["| Profile | What | Owns |", "| --- | --- | --- |"]
    bundles = []
    for atom, manifest in found.items():
        meta = manifest["profile"]
        link = f"[`{atom}`](profiles/{atom}/README.md)"
        if manifest.get("files"):
            rows.append(f"| {link} | {meta['description']} | {owns(manifest)} |")
        else:
            required = ", ".join(f"`{Path(r).name}`" for r in meta.get("requires", []))
            bundles.append(f"- {link}: {meta['description']}. Requires {required}.")
    return "\n".join(rows) + "\n\nThe bundle:\n\n" + "\n".join(bundles) + "\n"


def variables(found):
    """The README's table of variables: each one's default, what it sets, who declares it."""
    seen = {}
    for atom, manifest in found.items():
        for name, spec in manifest.get("vars", {}).items():
            entry = seen.setdefault(name, {"spec": spec, "by": []})
            entry["by"].append(f"[`{atom}`](profiles/{atom}/README.md)")
    rows = ["| Variable | Default | Asks | Declared by |", "| --- | --- | --- | --- |"]
    for name, entry in sorted(seen.items()):
        spec = entry["spec"]
        rows.append(f"| `{name}` | {default(spec)} | {spec.get('prompt', name)} | {', '.join(entry['by'])} |")
    return "\n".join(rows) + "\n"


def default(spec):
    """A variable's default, as the tables show it."""
    if "default" not in spec:
        return "none"
    return f"`{spec['default']}`" if spec["default"] else "empty"


def facts(atom, manifest):
    """A profile's facts: the files it owns, its recipes, its variables, the profiles it requires."""
    out = []
    files = manifest.get("files", {})
    if files:
        out += ["## Owns", "", "| File | Part | Policy | Notes |", "| --- | --- | --- | --- |"]
        for path, spec in files.items():
            notes = [note for note in ("template", "executable") if spec.get(note)]
            part, policy = PARTS[spec.get("scope", "file")], spec.get("policy", "owned")
            out.append(f"| `{path}` | {part} | {policy} | {', '.join(notes)} |")
        out.append("")
    listed = recipes(atom, manifest)
    if listed:
        out += ["## Recipes", ""]
        out += [f"- `{name}`: {doc}" if doc else f"- `{name}`" for name, doc in listed]
        out.append("")
    declared = manifest.get("vars", {})
    if declared:
        out += ["## Variables", "", "| Variable | Default | Asks |", "| --- | --- | --- |"]
        for name, spec in declared.items():
            out.append(f"| `{name}` | {default(spec)} | {spec.get('prompt', name)} |")
        out.append("")
    required = [Path(r).name for r in manifest["profile"].get("requires", [])]
    if required:
        out += ["## Requires", ""] + [f"- [`{r}`](../{r}/README.md)" for r in required] + [""]
    return "\n".join(out)


def between(text, markers, body):
    """`text` with what lies between `markers` replaced by `body`, the markers added at the end
    where missing."""
    begin, end = markers
    if begin not in text:
        text = text.rstrip("\n") + f"\n\n{begin}\n{end}\n"
    start, stop = text.index(begin) + len(begin), text.index(end)
    return f"{text[:start]}\n\n{body}\n{text[stop:]}"


def formatted(path, text):
    """`text` as `dprint fmt` leaves the file at `path`."""
    try:
        result = subprocess.run(
            ["dprint", "fmt", "--stdin", str(path.relative_to(ROOT))],
            cwd=ROOT,
            input=text,
            text=True,
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        sys.exit(f"dprint could not format {path.relative_to(ROOT)}: {error}")
    return result.stdout


def readme(found):
    """The README, its tables current."""
    text = README.read_text()
    text = between(text, CATALOG, table(found))
    text = between(text, VARIABLES, variables(found))
    return formatted(README, text)


def profile_readme(atom, manifest):
    """A profile's README, its facts current."""
    path = PROFILES / atom / "README.md"
    return formatted(path, between(path.read_text(), FACTS, facts(atom, manifest)))


def spine(found):
    """The spine's justfile, one `import?` for every profile that has recipes."""
    atoms = sorted({f"{RECIPES}{Path(path).name}" for manifest in found.values() for path in manifest.get("files", {}) if path.startswith(RECIPES) and path.endswith(".just")})
    imports = "".join(f"import? '{path}'\n" for path in atoms)
    return re.sub(r"(^import\? '.*'\n)+", imports, SPINE.read_text(), count=1, flags=re.MULTILINE)


def main(args):
    found = profiles()
    wanted = {README: readme(found), SPINE: spine(found)}
    for atom, manifest in found.items():
        if (PROFILES / atom / "README.md").is_file():
            wanted[PROFILES / atom / "README.md"] = profile_readme(atom, manifest)
    if args == ["--check"]:
        stale = [f"{path.relative_to(ROOT)} is stale: run scripts/catalog.py" for path, text in wanted.items() if path.read_text() != text]
        found_problems = problems(found)
        for problem in found_problems + stale:
            print(problem, file=sys.stderr)
        return 1 if found_problems or stale else 0
    if args:
        print(__doc__.strip().splitlines()[3], file=sys.stderr)
        return 2
    for path, text in wanted.items():
        path.write_text(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

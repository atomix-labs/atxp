"""A collection's pins: each profile's tools, their lock entries for every platform, and the dprint
plugins its payloads name.

Usage: pins.py check | lock [<profile>...] | bump [<report>]

Run in the collection's root, which applies the `mise` profile. `check`, offline, fails when a
profile's lock entry does not match its pin, lacks a platform or a checksum, or holds a tool the
profile does not pin, or when a dprint plugin carries no checksum. `lock` rewrites the named
profiles' lock entries, or every one's. `bump` moves every pin and dprint plugin to its newest
release past the cooldown, relocks what moved, and writes a Markdown report.

A pin file may be a template whose tools are each gated by a feature of its profile, between lines
of `{% if "<feature>" in devset.features %}` and `{% endif %}`: the tool's lock entries carry the
same gate, and both files are templates.
"""

import datetime
import hashlib
import importlib.util
import itertools
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from catalog import Profile, profiles

PIN = Path(".config/mise/conf.d")
LOCK = Path(".config/mise/mise.lock")
COOLDOWN = "3d"
COOLDOWN_DAYS = 3
PLUGIN = re.compile(
    r'"(https://plugins\.dprint\.dev/(?:([\w-]+)/)?([\w-]+)-(v?)([\d.]+)\.wasm)'
    r'(?:@([0-9a-f]{64}))?"'
)
BLOCK = re.compile(r'^\[\[?tools\.("[^"]+"|[^."\]]+)', re.MULTILINE)
GATE = re.compile(r'\{%-?\s*if\s+"([\w-]+)"\s+in\s+devset\.features\s*-?%\}')
END = re.compile(r"\{%-?\s*endif\s*-?%\}")


def helper():
    """The mise profile's helper, applied here, whose checks every entry is held to."""
    path = Path(".just/mise.py")
    spec = importlib.util.spec_from_file_location("mise_helper", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MISE = helper()


class Pinned(NamedTuple):
    """A profile that pins tools: its pin file, each tool's version, each gated tool's feature."""

    profile: Profile
    pin: Path
    versions: dict
    gates: dict

    @property
    def lock(self):
        """Its lock payload."""
        return self.profile.path / "files" / LOCK


def untemplated(path):
    """A pin or lock file as TOML, its gates dropped, and the feature that gates each gated tool."""
    plain, gated, feature = [], defaultdict(list), None
    for line in path.read_text().splitlines(keepends=True):
        directive = line.strip()
        if gate := GATE.fullmatch(directive):
            feature = gate.group(1)
        elif END.fullmatch(directive):
            feature = None
        elif directive.startswith(("{%", "{{", "{#")):
            sys.exit(f"{path}: its tools are gated by features alone, each in `{{% if %}}` lines")
        else:
            plain.append(line)
            if feature:
                gated[feature].append(line)
    gates = {
        tool: feature
        for feature, lines in gated.items()
        for tool in tomllib.loads("[tools]\n" + "".join(lines))["tools"]
    }
    return "".join(plain), gates


def pins():
    """Each profile that pins tools, by name."""
    found = {}
    for profile in profiles():
        for path in profile.files:
            if Path(path).parent == PIN and path.endswith(".toml"):
                pin = profile.path / "files" / path
                text, gates = untemplated(pin)
                tools = tomllib.loads(text).get("tools", {})
                versions = {
                    name: spec if isinstance(spec, str) else spec["version"]
                    for name, spec in tools.items()
                }
                if versions:
                    found[profile.name] = Pinned(profile, pin, versions, gates)
    return found


def locked(pinned):
    """Its lock payload's entries, by tool, and the feature that gates each gated tool."""
    if not pinned.lock.is_file():
        return {}, {}
    text, gates = untemplated(pinned.lock)
    return tomllib.loads(text).get("tools", {}), gates


def blocks(text):
    """The lock text of each tool in `text`: its entries and their platform tables."""
    out = {}
    starts = [m.start() for m in re.finditer(r"^\[", text, re.MULTILINE)] + [len(text)]
    for start, end in itertools.pairwise(starts):
        name = BLOCK.match(text, start)
        if name:
            out.setdefault(name.group(1).strip('"'), []).append(text[start:end].rstrip() + "\n")
    return out


def check():
    """Prints every problem with the profiles' pins, and fails if there is one."""
    problems = []
    for name, pinned in pins().items():
        profile, where = pinned.profile, pinned.profile.path
        spec = profile.files.get(str(LOCK))
        if spec is None or spec.get("scope") != "keys":
            problems.append(
                f'{where}: owns its lock entries as keys: [files."{LOCK}"] scope = "keys"'
            )
        if pinned.gates:
            for path in (pinned.pin.relative_to(where / "files"), LOCK):
                if not profile.files.get(str(path), {}).get("template"):
                    problems.append(f'{where}: gates tools, so [files."{path}"] is a template')
        entries, gates = locked(pinned)
        for tool, version in pinned.versions.items():
            problems += MISE.entry_problems(
                tool, version, entries.get(tool, []), f"{where}/files/{LOCK}"
            )
            if gates.get(tool) != pinned.gates.get(tool):
                problems.append(
                    f"{where}/files/{LOCK}: `{tool}` is not gated as its pin is: "
                    f"`pins.py lock {name}` writes it"
                )
        if strays := sorted(set(entries) - set(pinned.versions)):
            problems.append(f"{where}: its lock holds tools it does not pin: {', '.join(strays)}")
    for dprint in dprint_files():
        for match in PLUGIN.finditer(dprint.read_text()):
            if not match.group(6):
                problems.append(f"{dprint}: plugin {match.group(1)} has no @sha256")
    for problem in problems:
        print(problem, file=sys.stderr)
    return 1 if problems else 0


def dprint_files():
    """Every `dprint.json` a profile ships."""
    return [
        profile.path / "files" / "dprint.json"
        for profile in profiles()
        if "dprint.json" in profile.files
    ]


def lock(names):
    """Rewrites each named profile's lock entries, or every one's, for every platform, their
    checksums filled, each gated as its pin gates it."""
    notes = []
    for name, pinned in pins().items():
        if names and name not in names:
            continue
        with tempfile.TemporaryDirectory() as scratch:
            scratch = Path(scratch)
            (scratch / PIN).mkdir(parents=True)
            (scratch / PIN / pinned.pin.name).write_text(untemplated(pinned.pin)[0])
            settings = f'[settings]\nlockfile = true\nminimum_release_age = "{COOLDOWN}"\n'
            (scratch / "mise.toml").write_text(settings)
            env = os.environ | {"MISE_TRUSTED_CONFIG_PATHS": str(scratch)}
            subprocess.run(
                ["mise", "lock", "--platform", ",".join(MISE.PLATFORMS)],
                cwd=scratch,
                env=env,
                check=True,
                capture_output=True,
            )
            notes += [f"`{name}`: {note}" for note in MISE.fill(scratch / LOCK)]
            found = blocks((scratch / LOCK).read_text())
        text = ""
        for tool in pinned.versions:
            entries = "\n".join(found.get(tool, []))
            if gate := pinned.gates.get(tool):
                entries = f'{{% if "{gate}" in devset.features %}}\n{entries}{{% endif %}}\n'
            # A blank line between tools, but after a gate's `endif`, which sets its tool apart.
            if text and not text.endswith("{% endif %}\n"):
                text += "\n"
            text += entries
        # Under a cooldown, `mise lock` records the version asked for as `specifiers`, which
        # `mise install` drops again: left out, the entry is what a repository's install writes.
        text = re.sub(r"^specifiers = .*\n", "", text, flags=re.MULTILINE)
        pinned.lock.parent.mkdir(parents=True, exist_ok=True)
        pinned.lock.write_text(text)
    return notes


def repin(text, name, have, want):
    """`text`, a pin file, with `name` pinned to `want`: inline, or in its own table."""
    key, old = re.escape(name), re.escape(have)
    inline = re.compile(rf'^("?{key}"?\s*=\s*)"{old}"', re.MULTILINE)
    table = re.compile(
        rf'(^\[tools\."?{key}"?\]\s*\n(?:[^\[\n].*\n|\n)*?version\s*=\s*)"{old}"', re.MULTILINE
    )
    text, count = inline.subn(rf'\g<1>"{want}"', text)
    return text if count else table.sub(rf'\g<1>"{want}"', text)


def newer(want, have):
    """Whether `want` is a later version than `have`."""
    return MISE.version_key(want) > MISE.version_key(have)


def github(url):
    """A GitHub API response, authenticated when a token is at hand."""
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "devset-collection"}
    if token := os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as response:
        return json.load(response)


def plugins(moved, held):
    """Moves every dprint plugin in every payload to its newest release past the cooldown."""
    for path in dprint_files():
        plugin_file(path, moved, held)


def plugin_file(path, moved, held):
    """Moves each dprint plugin in `path` to its newest release past the cooldown, checksummed."""
    text = path.read_text()
    cutoff = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=COOLDOWN_DAYS)
    for match in list(PLUGIN.finditer(text)):
        _, owner, name, prefix, have, checksum = match.groups()
        repo = f"{owner}/{name}" if owner else f"dprint/dprint-plugin-{name}"
        releases = [
            r
            for r in github(f"https://api.github.com/repos/{repo}/releases?per_page=30")
            if not r["draft"] and not r["prerelease"]
        ]
        aged = [r for r in releases if datetime.datetime.fromisoformat(r["published_at"]) <= cutoff]
        want, newest = newest_of(aged), newest_of(releases)
        if (
            newest
            and want is not newest
            and newer(newest["tag_name"], (want or {}).get("tag_name", have))
        ):
            held.append(f"dprint plugin `{name}` {newest['tag_name']}")
        # Never backwards: a plugin pinned past the cooldown stays, and only gains its checksum.
        moves = want is not None and newer(want["tag_name"].lstrip("v"), have)
        if not moves and checksum:
            continue
        version = want["tag_name"].lstrip("v") if moves else have
        wasm = (
            next((a for a in want["assets"] if a["name"].endswith(".wasm")), None)
            if moves
            else None
        )
        scope = f"{owner}/" if owner else ""
        new = f"https://plugins.dprint.dev/{scope}{name}-{prefix}{version}.wasm"
        if wasm and (wasm.get("digest") or "").startswith("sha256:"):
            digest = wasm["digest"].removeprefix("sha256:")
        else:
            request = urllib.request.Request(new, headers={"User-Agent": "devset-collection"})
            with urllib.request.urlopen(request) as response:
                digest = hashlib.sha256(response.read()).hexdigest()
        text = text.replace(match.group(0), f'"{new}@{digest}"')
        if version != have:
            moved.append(f"dprint plugin `{name}` {have} -> {version}")
    path.write_text(text)


def newest_of(releases):
    """The release among `releases` with the highest version, if any."""
    return max(releases, key=lambda release: MISE.version_key(release["tag_name"]), default=None)


def report_text(title, sections):
    """A Markdown report: its heading, then each non-empty section as a list."""
    body = "".join(
        f"{name} ({len(items)}):\n\n" + "".join(f"- {item}\n" for item in items) + "\n"
        for name, items in sections
        if items
    )
    return f"### {title}\n\n" + (body or "Nothing to move.\n")


def bump(report):
    """Moves every pin and plugin past the cooldown, relocks, and reports."""
    moved, held, failed, changed = [], [], [], set()
    for name, pinned in pins().items():
        text = pinned.pin.read_text()
        entries, _ = locked(pinned)
        for tool, pin in pinned.versions.items():
            # A track keeps its pin, and moves by its lock.
            wanted = f"{tool}@{pin}" if MISE.track(pin) else tool
            have = next(
                (
                    e["version"]
                    for e in entries.get(tool, [])
                    if MISE.pinned(e.get("version", ""), pin)
                ),
                pin,
            )
            try:
                want = MISE.latest(wanted, COOLDOWN)
                newest = MISE.latest(wanted, "0s")
            except subprocess.CalledProcessError as error:
                failed.append(f"`{tool}`: {(error.stderr or '').strip() or error}")
                continue
            if newest != want and newer(newest, want):
                held.append(f"`{tool}` {newest}")
            if newer(want, have):
                if not MISE.track(pin):
                    text = repin(text, tool, pin, want)
                moved.append(f"`{tool}` {have} -> {want}")
                changed.add(name)
        pinned.pin.write_text(text)
    try:
        plugins(moved, held)
    except OSError as error:
        failed.append(f"dprint plugins: {error}")
    notes = lock(changed) if changed else []
    sections = [
        ("Moved", moved),
        ("Held by the cooldown", held),
        ("Checksums added", notes),
        ("Could not check", failed),
    ]
    text = report_text("Pins", sections)
    if report:
        Path(report).write_text(text)
    else:
        print(text, end="")
    return 1 if failed else 0


def main(args):
    match args:
        case ["check"]:
            return check()
        case ["lock", *names]:
            for note in lock(set(names)):
                print(note)
            return 0
        case ["bump", *report] if len(report) <= 1:
            return bump(report[0] if report else None)
    print(next(line for line in __doc__.splitlines() if line.startswith("Usage:")), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

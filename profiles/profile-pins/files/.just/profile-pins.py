"""A repository of profiles' pins: each tool's version, its lock entry for every platform, and the
dprint plugins its payloads name.

Usage: profile-pins.py check | lock [<profile>...] | bump [<report>]

Run in the repository's root, which holds `profiles/<id>/` and applies the `mise` profile. `check`,
offline, fails when a profile's lock entry does not match its pin, lacks a platform or a checksum, or
holds another profile's tool, or when a dprint plugin carries no checksum. `lock` rewrites the named
profiles' lock entries, or every one's. `bump` moves every pin and dprint plugin to its newest
release past the cooldown, relocks what moved, and writes a Markdown report.
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
import urllib.request
from pathlib import Path

import tomllib

PROFILES = Path("profiles")
PIN = Path(".config/mise/conf.d")
LOCK = Path(".config/mise/mise.lock")
COOLDOWN = "3d"
COOLDOWN_DAYS = 3
PLUGIN = re.compile(
    r'"(https://plugins\.dprint\.dev/(?:([\w-]+)/)?([\w-]+)-(v?)([\d.]+)\.wasm)(?:@([0-9a-f]{64}))?"'
)
BLOCK = re.compile(r'^\[\[?tools\.("[^"]+"|[^."\]]+)', re.MULTILINE)


def helper():
    """The mise profile's helper, applied to this repository, whose checks every entry is held to."""
    path = Path(".just/mise.py")
    spec = importlib.util.spec_from_file_location("mise_helper", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MISE = helper()


def pins():
    """Each atom that pins tools: its pin file, and each tool's version."""
    found = {}
    for pin in sorted(PROFILES.glob(f"*/files/{PIN}/*.toml")):
        with pin.open("rb") as file:
            tools = tomllib.load(file).get("tools", {})
        versions = {
            name: spec if isinstance(spec, str) else spec["version"] for name, spec in tools.items()
        }
        if versions:
            found[pin.parts[len(PROFILES.parts)]] = (pin, versions)
    return found


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
    """Prints every problem with the atoms' pins, and fails if there is one."""
    problems = []
    for atom, (_, versions) in pins().items():
        manifest = tomllib.loads((PROFILES / atom / "profile.toml").read_text())
        spec = manifest.get("files", {}).get(str(LOCK))
        where = f"profiles/{atom}"
        if spec is None or spec.get("scope") != "keys":
            problems.append(
                f'{where}: owns its lock entries as keys: [files."{LOCK}"] scope = "keys"'
            )
        lock = PROFILES / atom / "files" / LOCK
        locked = MISE.entries(lock)
        for name, version in versions.items():
            problems += MISE.entry_problems(
                name, version, locked.get(name, []), f"{where}/files/{LOCK}"
            )
        if strays := sorted(set(locked) - set(versions)):
            problems.append(f"{where}: its lock holds tools it does not pin: {', '.join(strays)}")
    for dprint in sorted(PROFILES.glob("*/files/dprint.json")):
        for match in PLUGIN.finditer(dprint.read_text()):
            if not match.group(6):
                problems.append(f"{dprint}: plugin {match.group(1)} has no @sha256")
    for problem in problems:
        print(problem, file=sys.stderr)
    return 1 if problems else 0


def lock(atoms):
    """Rewrites each atom's lock entries, for every platform, their checksums filled."""
    notes = []
    for atom, (pin, versions) in pins().items():
        if atoms and atom not in atoms:
            continue
        with tempfile.TemporaryDirectory() as scratch:
            scratch = Path(scratch)
            (scratch / PIN).mkdir(parents=True)
            (scratch / PIN / pin.name).write_text(pin.read_text())
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
            notes += [f"`{atom}`: {note}" for note in MISE.fill(scratch / LOCK)]
            found = blocks((scratch / LOCK).read_text())
        text = "\n".join(block for name in versions for block in found.get(name, []))
        # Under a cooldown, `mise lock` records the version asked for as `specifiers`, which
        # `mise install` drops again: left out, the entry is what a repository's install writes.
        text = re.sub(r"^specifiers = .*\n", "", text, flags=re.MULTILINE)
        target = PROFILES / atom / "files" / LOCK
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
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
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "atxp"}
    if token := os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as response:
        return json.load(response)


def plugins(moved, held):
    """Moves every dprint plugin in every payload to its newest release past the cooldown."""
    for path in sorted(PROFILES.glob("*/files/dprint.json")):
        plugin_file(path, moved, held)


def plugin_file(path, moved, held):
    """Moves every dprint plugin `path` names to its newest release past the cooldown, checksummed."""
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
        new = f"https://plugins.dprint.dev/{owner + '/' if owner else ''}{name}-{prefix}{version}.wasm"
        if wasm and (wasm.get("digest") or "").startswith("sha256:"):
            digest = wasm["digest"].removeprefix("sha256:")
        else:
            request = urllib.request.Request(new, headers={"User-Agent": "atxp"})
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
    for atom, (pin, versions) in pins().items():
        text = pin.read_text()
        locked = MISE.entries(PROFILES / atom / "files" / LOCK)
        for name, pinned in versions.items():
            # A track keeps its pin, and moves by its lock.
            wanted = f"{name}@{pinned}" if MISE.track(pinned) else name
            have = next(
                (
                    e["version"]
                    for e in locked.get(name, [])
                    if MISE.pinned(e.get("version", ""), pinned)
                ),
                pinned,
            )
            try:
                want = MISE.latest(wanted, COOLDOWN)
                newest = MISE.latest(wanted, "0s")
            except subprocess.CalledProcessError as error:
                failed.append(f"`{name}`: {(error.stderr or '').strip() or error}")
                continue
            if newest != want and newer(newest, want):
                held.append(f"`{name}` {newest}")
            if newer(want, have):
                if not MISE.track(pinned):
                    text = repin(text, name, pinned, want)
                moved.append(f"`{name}` {have} -> {want}")
                changed.add(atom)
        pin.write_text(text)
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
        case ["lock", *atoms]:
            for note in lock(set(atoms)):
                print(note)
            return 0
        case ["bump", *report] if len(report) <= 1:
            return bump(report[0] if report else None)
    print(__doc__.strip().splitlines()[2], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

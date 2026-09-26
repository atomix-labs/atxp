#!/usr/bin/env python3
"""Moves the pinned nightly to the newest one of the last two weeks that has every component.

Usage: scripts/rust-toolchain.py <rust-toolchain.toml> [<report>]

A nightly qualifies when its manifest has every component the nightly's lines name available for
every platform the locks cover: rustup builds some components only on some nights. The channel
never moves backwards; a check that cannot be made fails the run.
"""

import datetime
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import tomllib

WINDOW = 14
# The triples of the platforms every lock covers: linux-arm64, linux-x64, macos-arm64.
TRIPLES = ("aarch64-unknown-linux-gnu", "x86_64-unknown-linux-gnu", "aarch64-apple-darwin")
CHANNEL = re.compile(r'^(channel\s*=\s*")nightly-(\d{4}-\d{2}-\d{2})(")', re.MULTILINE)
# The components the nightly's lines name; the file is a template, whose other branch is stable's.
COMPONENTS = re.compile(r"^components\s*=\s*(\[[^\]]*\])", re.MULTILINE)


def manifest(day):
    """The nightly manifest of `day`, or None when that night has none."""
    url = f"https://static.rust-lang.org/dist/{day}/channel-rust-nightly.toml"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "atxp"})) as response:
            return tomllib.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def complete(found, components):
    """Whether every component is available on every triple, under its name or its `-preview` one."""
    packages = found.get("pkg", {})
    for component in components:
        package = packages.get(component) or packages.get(f"{component}-preview")
        if package is None:
            return False
        targets = package.get("target", {})
        for triple in TRIPLES:
            target = targets.get(triple) or targets.get("*")
            if not target or not target.get("available"):
                return False
    return True


def main(args):
    if not 1 <= len(args) <= 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    path = Path(args[0])
    text = path.read_text()
    have = CHANNEL.search(text)
    if not have:
        print(f"{path}: no dated nightly `channel` to move", file=sys.stderr)
        return 1
    listed = COMPONENTS.search(text, have.end())
    components = tomllib.loads(f"components = {listed.group(1)}")["components"] if listed else []
    today = datetime.date.today()
    want = None
    for back in range(WINDOW + 1):
        day = (today - datetime.timedelta(days=back)).isoformat()
        if day <= have.group(2):
            break
        found = manifest(day)
        if found and complete(found, components):
            want = day
            break
    if want:
        path.write_text(CHANNEL.sub(rf"\g<1>nightly-{want}\g<3>", text, count=1))
        report = f"### Rust\n\nMoved: nightly-{have.group(2)} -> nightly-{want}.\n"
    else:
        report = f"### Rust\n\nnightly-{have.group(2)} stays: no newer nightly of the last {WINDOW} days has every component on every platform.\n"
    if len(args) == 2:
        Path(args[1]).write_text(report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

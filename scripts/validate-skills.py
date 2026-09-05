#!/usr/bin/env python3
"""Check this repository's flat skill catalog and routing fixtures without model calls.

Checks required single-line frontmatter fields, not arbitrary YAML semantics.
"""

import argparse
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


def validate(root):
    root = Path(root)
    errors = []
    names = set()
    skills = sorted(path for area in ("shared", "dotnet") for path in (root / area).glob("*/SKILL.md"))
    if not skills:
        errors.append("No installable skills found")
    for path in skills:
        text = path.read_text()
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
        if not match:
            errors.append(f"{path}: missing frontmatter")
            continue
        fields = {}
        for key in ("name", "description"):
            values = re.findall(rf"^{key}:\s*([^\n]+)$", match[1], re.M)
            if len(values) != 1 or values[0].strip() in ("|", ">", '""', "''"):
                errors.append(f"{path}: requires one nonempty single-line {key}")
            else:
                fields[key] = values[0].strip().strip('\"\'')
        name = fields.get("name", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name != path.parent.name:
            errors.append(f"{path}: name must match its directory")
        if name in names:
            errors.append(f"{path}: duplicate installed name {name}")
        names.add(name)
    for area in ("shared", "dotnet"):
        for path in (root / area).rglob("*.md"):
            text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
            for target in re.findall(r"\]\(([^)]+)\)", text):
                url = urlsplit(target)
                if url.scheme or not url.path or target.startswith(("/", "~")):
                    continue
                if not (path.parent / unquote(url.path)).exists():
                    errors.append(f"{path}: missing reference {target}")
    try:
        cases = json.loads((root / "evals/routing.json").read_text())
        seen = set()
        for case in cases:
            if not case["id"] or case["id"] in seen:
                errors.append("Routing cases require unique nonempty ids")
            seen.add(case["id"])
            if not case["prompt"].strip() or not case["expectations"] or not all(isinstance(x, str) and x.strip() for x in case["expectations"]):
                errors.append(f"{case['id']}: missing prompt or behavioral expectations")
            for name in case["load"] + case["avoid"]:
                if name not in names:
                    errors.append(f"{case['id']}: unknown skill {name}")
            if set(case["load"]) & set(case["avoid"]):
                errors.append(f"{case['id']}: contradictory routing expectations")
        if not cases:
            errors.append("Routing cases are empty")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        errors.append(f"Invalid routing fixture: {error}")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    errors = validate(parser.parse_args().root)
    for error in errors:
        print(error)
    if errors:
        raise SystemExit(1)
    print("Catalog fields, internal file references, and routing fixture structure pass. Live routing was not tested.")

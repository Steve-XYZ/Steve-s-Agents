#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path


def fail(message: str) -> None:
    raise ValueError(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--settings", required=True)
    parser.add_argument("--backup-dir", required=True)
    parser.add_argument("--required-directory", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    settings_path = Path(args.settings).expanduser()
    backup_dir = Path(args.backup_dir).expanduser()

    if settings_path.is_symlink():
        fail(f"refusing to replace symlinked settings file: {settings_path}")

    if settings_path.exists():
        try:
            data = json.loads(settings_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            fail(f"cannot parse {settings_path}: {error}")
    else:
        data = {}

    if not isinstance(data, dict):
        fail(f"expected a JSON object in {settings_path}")

    permissions = data.get("permissions")
    if permissions is None:
        permissions = {}
        data["permissions"] = permissions
    elif not isinstance(permissions, dict):
        fail(f"expected permissions to be an object in {settings_path}")

    directories = permissions.get("additionalDirectories")
    if directories is None:
        directories = []
        permissions["additionalDirectories"] = directories
    elif not isinstance(directories, list) or not all(
        isinstance(item, str) for item in directories
    ):
        fail(
            f"expected permissions.additionalDirectories to be a string array "
            f"in {settings_path}"
        )

    missing = [item for item in args.required_directory if item not in directories]
    if not missing:
        print("kept")
        return 0

    if args.dry_run:
        print("would-update")
        return 0

    directories.extend(missing)
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    if settings_path.exists():
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(settings_path, backup_dir / ".claude_settings.json")

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f"{settings_path.name}.", suffix=".tmp", dir=settings_path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as temporary_file:
            json.dump(data, temporary_file, indent=2, ensure_ascii=False)
            temporary_file.write("\n")

        if settings_path.exists():
            mode = stat.S_IMODE(settings_path.stat().st_mode)
            os.chmod(temporary_name, mode)
        os.replace(temporary_name, settings_path)
    except Exception:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)
        raise

    print("updated")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)

#!/usr/bin/env python3

import argparse
import json
import os
import re
from pathlib import Path


CONFIG_PATH = Path("libs/hbb_common/src/config.rs")


def required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def patch_config() -> None:
    server = required_env("RENDEZVOUS_SERVER")
    public_key = required_env("RS_PUB_KEY")
    source = CONFIG_PATH.read_text(encoding="utf-8")

    replacements = (
        (
            r'pub const RENDEZVOUS_SERVERS: &\[&str\] = &\[[^\n]+\];',
            f"pub const RENDEZVOUS_SERVERS: &[&str] = &[{json.dumps(server)}];",
        ),
        (
            r'pub const RS_PUB_KEY: &str = [^\n]+;',
            f"pub const RS_PUB_KEY: &str = {json.dumps(public_key)};",
        ),
    )

    for pattern, replacement in replacements:
        source, count = re.subn(pattern, replacement, source, count=1)
        if count != 1:
            raise RuntimeError(f"Expected exactly one config match for {pattern!r}, got {count}")

    CONFIG_PATH.write_text(source, encoding="utf-8")
    print("Custom server configuration injected into hbb_common")


def verify_binaries(paths: list[Path]) -> None:
    expected = {
        "RENDEZVOUS_SERVER": required_env("RENDEZVOUS_SERVER").encode(),
        "RS_PUB_KEY": required_env("RS_PUB_KEY").encode(),
    }
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(item for item in path.rglob("*") if item.is_file())
        else:
            files.append(path)

    found: dict[str, Path] = {}
    for path in files:
        data = path.read_bytes()
        for name, value in expected.items():
            if name not in found and value in data:
                found[name] = path

    missing = [name for name in expected if name not in found]
    if missing:
        raise RuntimeError(f"Compiled output is missing custom values: {', '.join(missing)}")
    locations = ", ".join(f"{name}={path}" for name, path in found.items())
    print(f"Verified compiled custom server configuration: {locations}")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("patch")
    verify = subparsers.add_parser("verify")
    verify.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    if args.command == "patch":
        patch_config()
    else:
        verify_binaries(args.paths)


if __name__ == "__main__":
    main()

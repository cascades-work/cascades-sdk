#!/usr/bin/env python3
"""Validate the Cascades public/private developer-contract boundary."""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "contract.manifest.json"


def fail(message: str) -> None:
    print(f"CONTRACT ERROR: {message}", file=sys.stderr)


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    if manifest.get("policy") != "deny-by-default":
        errors.append("contract manifest must use deny-by-default policy")

    for rel in manifest.get("required_artifacts", []):
        if not (ROOT / rel).exists():
            errors.append(f"required public artifact is missing: {rel}")

    forbidden = set(manifest.get("private_roots_forbidden", []))
    present_roots = {p.name for p in ROOT.iterdir() if p.is_dir()}
    leaked = sorted(forbidden & present_roots)
    if leaked:
        errors.append("private implementation roots present in SDK: " + ", ".join(leaked))

    api = ROOT / manifest["public_api"]["canonical_mirror"]
    compat = ROOT / manifest["public_api"]["compatibility_mirror"]
    if api.exists() and compat.exists() and api.read_bytes() != compat.read_bytes():
        errors.append("OpenAPI canonical and compatibility mirrors differ")

    if api.exists():
        text = api.read_text(encoding="utf-8")
        match = re.search(r"(?m)^\s*version:\s*['\"]?([^'\"\s]+)", text)
        if not match:
            errors.append("OpenAPI info.version could not be located")
        else:
            version = match.group(1)
            if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
                errors.append(f"OpenAPI version is not semantic-version shaped: {version}")

    for error in errors:
        fail(error)
    if errors:
        return 1

    print("Cascades public developer contract boundary: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

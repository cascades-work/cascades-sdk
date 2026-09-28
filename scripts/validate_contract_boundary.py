#!/usr/bin/env python3
"""Validate the Cascades public/private developer-contract boundary."""
from __future__ import annotations

import json
import pathlib
import re
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "contract.manifest.json"
SEMVER = re.compile(
    r"0|[1-9]\d*"
    r"\.(?:0|[1-9]\d*)"
    r"\.(?:0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
)


def fail(message: str) -> None:
    print(f"CONTRACT ERROR: {message}", file=sys.stderr)


def require_list(manifest: dict[str, Any], key: str, errors: list[str]) -> list[Any]:
    value = manifest.get(key)
    if not isinstance(value, list) or not value:
        errors.append(f"manifest field {key!r} must be a non-empty list")
        return []
    return value


def read_info_version(openapi_path: pathlib.Path) -> str | None:
    """Read top-level info.version without accepting unrelated version keys."""
    in_info = False
    info_indent: int | None = None

    for raw in openapi_path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()

        if not in_info:
            if indent == 0 and stripped == "info:":
                in_info = True
                info_indent = indent
            continue

        if indent <= (info_indent or 0) and not stripped.startswith("#"):
            return None

        if re.match(r"^version\s*:", stripped):
            value = stripped.split(":", 1)[1].strip()
            if not value:
                return None
            if value[0:1] in {'"', "'"} and value[-1:] == value[0:1]:
                value = value[1:-1]
            return value

    return None


def main() -> int:
    errors: list[str] = []

    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load contract manifest: {exc}")
        return 1

    if manifest.get("policy") != "deny-by-default":
        errors.append("contract manifest must use deny-by-default policy")

    required = require_list(manifest, "required_artifacts", errors)
    public_roots = require_list(manifest, "public_roots", errors)
    infrastructure_roots = require_list(manifest, "repository_infrastructure_roots", errors)
    forbidden_roots = require_list(manifest, "private_roots_forbidden", errors)

    for item in required:
        if not isinstance(item, dict):
            errors.append("each required_artifacts entry must be an object")
            continue

        rel = item.get("path")
        expected_type = item.get("type")
        if not isinstance(rel, str) or not rel:
            errors.append("required artifact path must be a non-empty string")
            continue
        if expected_type not in {"file", "directory"}:
            errors.append(f"required artifact {rel!r} has invalid type {expected_type!r}")
            continue

        path = ROOT / rel
        if expected_type == "file" and not path.is_file():
            errors.append(f"required public file is missing or wrong type: {rel}")
        elif expected_type == "directory" and not path.is_dir():
            errors.append(f"required public directory is missing or wrong type: {rel}")

    allowed_roots = set(public_roots) | set(infrastructure_roots)
    present_roots = {p.name for p in ROOT.iterdir() if p.is_dir()}
    undeclared = sorted(present_roots - allowed_roots)
    if undeclared:
        errors.append(
            "undeclared top-level directories violate deny-by-default policy: "
            + ", ".join(undeclared)
        )

    leaked = sorted(set(forbidden_roots) & present_roots)
    if leaked:
        errors.append("private implementation roots present in SDK: " + ", ".join(leaked))

    public_api = manifest.get("public_api")
    if not isinstance(public_api, dict):
        errors.append("manifest field 'public_api' must be an object")
        public_api = {}

    canonical_rel = public_api.get("canonical_mirror")
    compatibility_rel = public_api.get("compatibility_mirror")
    if not isinstance(canonical_rel, str) or not canonical_rel:
        errors.append("public_api.canonical_mirror must be a non-empty string")
    if not isinstance(compatibility_rel, str) or not compatibility_rel:
        errors.append("public_api.compatibility_mirror must be a non-empty string")

    api = ROOT / canonical_rel if isinstance(canonical_rel, str) and canonical_rel else None
    compat = ROOT / compatibility_rel if isinstance(compatibility_rel, str) and compatibility_rel else None

    if api is not None and not api.is_file():
        errors.append(f"configured canonical OpenAPI mirror is missing: {canonical_rel}")
    if compat is not None and not compat.is_file():
        errors.append(f"configured compatibility OpenAPI mirror is missing: {compatibility_rel}")

    if api is not None and compat is not None and api.is_file() and compat.is_file():
        if api.read_bytes() != compat.read_bytes():
            errors.append("OpenAPI canonical and compatibility mirrors differ")

        version = read_info_version(api)
        if version is None:
            errors.append("OpenAPI top-level info.version could not be located")
        elif SEMVER.fullmatch(version) is None:
            errors.append(f"OpenAPI info.version is not valid SemVer: {version}")

    for error in errors:
        fail(error)

    if errors:
        return 1

    print("Cascades public developer contract boundary: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

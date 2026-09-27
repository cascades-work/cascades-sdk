#!/usr/bin/env python3
"""Verify public SDK OpenAPI mirrors against the private Cascades platform."""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

def norm(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

def read(path: Path) -> bytes:
    if not path.is_file():
        print(f"error: missing contract file: {path}", file=sys.stderr)
        raise SystemExit(2)
    return norm(path.read_bytes())

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--against", type=Path, required=True)
    args = parser.parse_args()
    source = args.against.resolve()
    expected = read(source)
    failed = False
    for mirror in (root / "api" / "openapi.yaml", root / "contracts" / "api.yaml"):
        if read(mirror) != expected:
            print(f"error: {mirror.relative_to(root)} differs from {source}", file=sys.stderr)
            failed = True
        else:
            print(f"OK: {mirror.relative_to(root)} matches {source}")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())

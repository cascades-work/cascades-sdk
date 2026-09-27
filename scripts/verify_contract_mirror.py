#!/usr/bin/env python3
"""Verify Cascades public OpenAPI mirrors, optionally against the private platform."""

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
    parser.add_argument("--against", type=Path, default=None)
    args = parser.parse_args()

    preferred = root / "api" / "openapi.yaml"
    compatibility = root / "contracts" / "api.yaml"
    preferred_bytes = read(preferred)
    compatibility_bytes = read(compatibility)

    if preferred_bytes != compatibility_bytes:
        print("error: api/openapi.yaml and contracts/api.yaml differ", file=sys.stderr)
        return 1
    print("OK: public OpenAPI mirrors agree")

    if args.against is None:
        return 0

    source = args.against.resolve()
    expected = read(source)
    if preferred_bytes != expected:
        print(f"error: public OpenAPI differs from private source {source}", file=sys.stderr)
        return 1

    print(f"OK: public OpenAPI matches private source {source}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

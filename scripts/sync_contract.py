#!/usr/bin/env python3
"""Mirror the private Cascades OpenAPI contract into the public SDK repository."""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

def lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=root.parent / "cascades" / "apis" / "cascades.openapi.yaml",
    )
    args = parser.parse_args()
    source = args.source.resolve()
    if not source.is_file():
        print(f"error: source contract does not exist: {source}", file=sys.stderr)
        return 2
    data = lf(source.read_bytes())
    for destination in (root / "api" / "openapi.yaml", root / "contracts" / "api.yaml"):
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        print(f"synced: {destination}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

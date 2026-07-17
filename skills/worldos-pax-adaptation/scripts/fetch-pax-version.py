#!/usr/bin/env python3
"""Fetch and pin one public, versioned Pax Historia Firestore document."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
URL_TEMPLATE = (
    "https://firestore.googleapis.com/v1/projects/pax-historia-dev/"
    "databases/(default)/documents/simplePresets/{preset_id}/versions/{version_id}"
)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def fail(message: str, status: int = 1) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(status)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download one exact public Pax preset version without credentials and "
            "refuse to overwrite a semantically different snapshot."
        )
    )
    parser.add_argument("preset_id", help="Pax preset identifier from the preset URL")
    parser.add_argument("version_id", help="Exact Pax version identifier")
    parser.add_argument("output", type=Path, help="Destination for the raw JSON response")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for label, value in (("preset_id", args.preset_id), ("version_id", args.version_id)):
        if not ID_PATTERN.fullmatch(value):
            fail(f"{label} contains unsupported characters")

    url = URL_TEMPLATE.format(
        preset_id=args.preset_id,
        version_id=args.version_id,
    )
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "worldos-pax-adaptation/1"},
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
    except urllib.error.HTTPError as error:
        if error.code in (401, 403):
            fail(f"source denied access with HTTP {error.code}; do not bypass it", 2)
        fail(f"source returned HTTP {error.code}", 2)
    except urllib.error.URLError as error:
        fail(f"source request failed: {error.reason}", 2)

    try:
        document = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        fail(f"source did not return valid JSON: {error}", 2)

    expected_suffix = (
        f"/documents/simplePresets/{args.preset_id}/versions/{args.version_id}"
    )
    if not isinstance(document, dict) or not str(document.get("name", "")).endswith(
        expected_suffix
    ):
        fail("returned Firestore document does not match the requested preset and version", 2)

    canonical = canonical_bytes(document)
    if args.output.exists():
        try:
            existing = json.loads(args.output.read_bytes())
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            fail(f"existing output is not valid readable JSON: {error}", 3)
        if canonical_bytes(existing) != canonical:
            fail("refusing to overwrite a semantically different existing snapshot", 3)
        action = "unchanged"
        stored = args.output.read_bytes()
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(raw)
        action = "created"
        stored = raw

    result = {
        "action": action,
        "sourceUrl": url,
        "output": str(args.output),
        "retrievedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "bytes": len(stored),
        "rawSha256": sha256(stored),
        "canonicalSha256": sha256(canonical),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

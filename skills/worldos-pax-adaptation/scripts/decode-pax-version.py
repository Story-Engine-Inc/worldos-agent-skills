#!/usr/bin/env python3
"""Decode a pinned Firestore document and create a Pax adaptation coverage worksheet."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


VALUE_KEYS = {
    "nullValue",
    "booleanValue",
    "integerValue",
    "doubleValue",
    "timestampValue",
    "stringValue",
    "bytesValue",
    "referenceValue",
    "geoPointValue",
    "arrayValue",
    "mapValue",
}


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def decode_value(value: Any, path: str) -> Any:
    if not isinstance(value, dict):
        fail(f"{path} is not a Firestore typed value")
    present = VALUE_KEYS.intersection(value)
    if len(present) != 1:
        fail(f"{path} must contain exactly one supported Firestore value type")
    kind = next(iter(present))
    payload = value[kind]
    if kind == "nullValue":
        return None
    if kind in {"booleanValue", "doubleValue", "stringValue", "timestampValue", "referenceValue"}:
        return payload
    if kind == "integerValue":
        try:
            return int(payload)
        except (TypeError, ValueError):
            fail(f"{path}.integerValue is invalid")
    if kind == "bytesValue":
        try:
            base64.b64decode(payload, validate=True)
        except (TypeError, ValueError):
            fail(f"{path}.bytesValue is not valid base64")
        return {"$bytesBase64": payload}
    if kind == "geoPointValue":
        if not isinstance(payload, dict):
            fail(f"{path}.geoPointValue is invalid")
        return {"latitude": payload.get("latitude"), "longitude": payload.get("longitude")}
    if kind == "arrayValue":
        if not isinstance(payload, dict):
            fail(f"{path}.arrayValue is invalid")
        return [decode_value(item, f"{path}[{index}]") for index, item in enumerate(payload.get("values", []))]
    fields = payload.get("fields", {}) if isinstance(payload, dict) else None
    if not isinstance(fields, dict):
        fail(f"{path}.mapValue.fields is invalid")
    return {key: decode_value(child, f"{path}.{key}") for key, child in fields.items()}


def item_label(value: Any, fallback: str) -> str:
    if isinstance(value, dict):
        for key in ("title", "name", "label", "id", "uid", "regionID", "regionId"):
            candidate = value.get(key)
            if isinstance(candidate, (str, int)) and str(candidate).strip():
                return str(candidate).strip()[:180]
    return fallback


def char_count(value: Any) -> int:
    if isinstance(value, str):
        return len(value)
    return len(json.dumps(value, ensure_ascii=False, separators=(",", ":")))


def coverage_item(path: str, category: str, label: str, value: Any) -> dict[str, Any]:
    return {
        "id": hashlib.sha256(path.encode("utf-8")).hexdigest()[:16],
        "sourcePath": path,
        "category": category,
        "label": label,
        "sourceChars": char_count(value),
        "disposition": None,
        "worldOwner": None,
        "implementation": None,
        "rationale": None,
        "verification": None,
    }


def append_collection(items: list[dict[str, Any]], root: str, category: str, value: Any) -> None:
    if isinstance(value, list):
        for index, child in enumerate(value):
            path = f"{root}[{index}]"
            items.append(coverage_item(path, category, item_label(child, path), child))
    elif isinstance(value, dict):
        for key, child in value.items():
            path = f"{root}.{key}"
            items.append(coverage_item(path, category, item_label(child, str(key)), child))
    elif value is not None:
        items.append(coverage_item(root, category, root, value))


def build_audit(document: dict[str, Any], decoded: dict[str, Any], raw: bytes) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for field, category in (
        ("rulesText", "rules"),
        ("startingTimelineText", "timeline"),
        ("baseMap", "map"),
    ):
        if field in decoded:
            items.append(coverage_item(field, category, field, decoded[field]))
    for field, category in (
        ("prompts", "prompt"),
        ("regionData", "region"),
        ("recommendedEntities", "entity"),
        ("decisions", "decision"),
        ("dimensions", "dimension"),
        ("eventConsolidations", "timeline"),
    ):
        append_collection(items, field, category, decoded.get(field))
    metadata_fields = [
        field for field in decoded
        if field not in {"rulesText", "startingTimelineText", "baseMap", "prompts", "regionData", "recommendedEntities", "decisions", "dimensions", "eventConsolidations"}
    ]
    if metadata_fields:
        items.append(coverage_item("$metadata", "metadata", "Version and publication metadata", {field: decoded[field] for field in metadata_fields}))
    return {
        "schemaVersion": 1,
        "source": {
            "documentName": document.get("name"),
            "createTime": document.get("createTime"),
            "updateTime": document.get("updateTime"),
            "bytes": len(raw),
            "rawSha256": hashlib.sha256(raw).hexdigest(),
            "canonicalSha256": hashlib.sha256(json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest(),
        },
        "inventory": {
            "topLevelFields": sorted(decoded),
            "rulesTextChars": char_count(decoded.get("rulesText", "")),
            "startingTimelineTextChars": char_count(decoded.get("startingTimelineText", "")),
            "promptCount": len(decoded.get("prompts", [])) if isinstance(decoded.get("prompts"), (list, dict)) else 0,
            "regionCount": len(decoded.get("regionData", [])) if isinstance(decoded.get("regionData"), list) else len(decoded.get("regionData", {})) if isinstance(decoded.get("regionData"), dict) else 0,
            "coverageRows": len(items),
        },
        "coverage": items,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Decode Firestore typed values and create a source-coverage worksheet without copying source prose into the worksheet.")
    parser.add_argument("snapshot", type=Path, help="Pinned raw Firestore JSON")
    parser.add_argument("--normalized", type=Path, required=True, help="Decoded ordinary JSON output")
    parser.add_argument("--audit", type=Path, required=True, help="Coverage worksheet output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw = args.snapshot.read_bytes()
    try:
        document = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        fail(f"snapshot is not valid JSON: {error}")
    fields = document.get("fields") if isinstance(document, dict) else None
    if not isinstance(fields, dict) or not isinstance(document.get("name"), str):
        fail("snapshot is not a Firestore document with name and fields")
    decoded = {key: decode_value(value, key) for key, value in fields.items()}
    audit = build_audit(document, decoded, raw)
    for path, value in ((args.normalized, decoded), (args.audit, audit)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"normalized": str(args.normalized), "audit": str(args.audit), **audit["inventory"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

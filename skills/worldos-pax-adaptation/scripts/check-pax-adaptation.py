#!/usr/bin/env python3
"""Check Pax source coverage and WorldOS prompt/content budgets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


DISPOSITIONS = {"preserve", "rebuild", "omit", "verify"}
PARAGRAPH_SPLIT = re.compile(r"\n\s*\n")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"error: cannot read {path}: {error}", file=sys.stderr)
        raise SystemExit(2)


def text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Require complete source decisions and enforce lean WorldOS prompt budgets.")
    parser.add_argument("audit", type=Path, help="Completed coverage worksheet")
    parser.add_argument("--draft", type=Path, required=True, help="Candidate WorldOS draft JSON")
    args = parser.parse_args()
    audit = load_json(args.audit)
    draft = load_json(args.draft)
    errors: list[str] = []
    warnings: list[str] = []

    rows = audit.get("coverage") if isinstance(audit, dict) else None
    if not isinstance(rows, list) or not rows:
        errors.append("coverage worksheet has no rows")
        rows = []
    seen_paths: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"coverage[{index}] is not an object")
            continue
        path = text(row.get("sourcePath")) or f"coverage[{index}]"
        if path in seen_paths:
            errors.append(f"{path}: duplicate sourcePath")
        seen_paths.add(path)
        disposition = row.get("disposition")
        if disposition not in DISPOSITIONS:
            errors.append(f"{path}: disposition must be preserve, rebuild, omit, or verify")
        elif disposition in {"preserve", "rebuild"}:
            if not text(row.get("worldOwner")).strip():
                errors.append(f"{path}: {disposition} requires worldOwner")
            if not text(row.get("implementation")).strip():
                errors.append(f"{path}: {disposition} requires implementation")
        elif disposition == "omit" and not text(row.get("rationale")).strip():
            errors.append(f"{path}: omit requires rationale")
        elif disposition == "verify" and not text(row.get("verification")).strip():
            errors.append(f"{path}: verify requires verification plan or result")

    if not isinstance(draft, dict):
        errors.append("draft must be an object")
        draft = {}
    config = draft.get("config") if isinstance(draft.get("config"), dict) else {}
    apps = draft.get("apps") if isinstance(draft.get("apps"), list) else []
    system_prompt = text(config.get("systemPrompt"))
    soft_rules = text(config.get("softRulesPrompt"))
    intro = text(config.get("introMd"))
    app_prompts: list[tuple[str, str]] = []
    opening_chars = 0
    for index, app in enumerate(apps):
        if not isinstance(app, dict):
            continue
        slug = text(app.get("app_slug")) or str(index)
        app_config = app.get("config") if isinstance(app.get("config"), dict) else {}
        prompt = text(app_config.get("prompt"))
        if prompt:
            app_prompts.append((slug, prompt))
        if slug == "story":
            opening_chars += len(text(app_config.get("opening")))

    injected = len(system_prompt) + len(soft_rules) + sum(len(prompt) for _, prompt in app_prompts)
    if len(system_prompt) > 32_000:
        errors.append(f"systemPrompt has {len(system_prompt)} characters; target <= 32,000")
    elif len(system_prompt) > 24_000:
        warnings.append(f"systemPrompt has {len(system_prompt)} characters; consider distilling below 24,000")
    if injected > 48_000:
        errors.append(f"estimated injected prompt copy has {injected} characters; target <= 48,000")
    for slug, prompt in app_prompts:
        if len(prompt) > 8_000:
            errors.append(f"app {slug} prompt has {len(prompt)} characters; target <= 8,000")
        elif len(prompt) > 5_000:
            warnings.append(f"app {slug} prompt has {len(prompt)} characters; consider distilling below 5,000")
    if len(intro) > 8_000:
        errors.append(f"introMd has {len(intro)} characters; target <= 8,000")
    if opening_chars > 8_000:
        errors.append(f"Story opening has {opening_chars} characters; target <= 8,000")
    draft_bytes = len(json.dumps(draft, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
    if draft_bytes > 3_500_000:
        errors.append(f"draft is {draft_bytes} bytes; keep below 3,500,000 before MCP validation")
    elif draft_bytes > 3_000_000:
        warnings.append(f"draft is {draft_bytes} bytes and is close to the authoring limit")

    prompt_sources = [("systemPrompt", system_prompt), ("softRulesPrompt", soft_rules), *[(f"apps.{slug}.prompt", prompt) for slug, prompt in app_prompts]]
    paragraphs: dict[str, list[str]] = {}
    for source, value in prompt_sources:
        for paragraph in PARAGRAPH_SPLIT.split(value):
            normalized = " ".join(paragraph.split()).casefold()
            if len(normalized) < 240:
                continue
            paragraphs.setdefault(hashlib.sha256(normalized.encode("utf-8")).hexdigest(), []).append(source)
    for sources in paragraphs.values():
        if len(set(sources)) > 1:
            warnings.append(f"long prompt paragraph is duplicated across {', '.join(sorted(set(sources)))}")

    result = {
        "valid": not errors,
        "coverageRows": len(rows),
        "budget": {
            "systemPromptChars": len(system_prompt),
            "softRulesChars": len(soft_rules),
            "appPromptChars": sum(len(prompt) for _, prompt in app_prompts),
            "estimatedInjectedChars": injected,
            "introChars": len(intro),
            "storyOpeningChars": opening_chars,
            "draftBytes": draft_bytes,
        },
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Deterministic SOP format converter (markdown <-> yaml/json)."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    yaml = None


def detect_format(path: Path, explicit: str | None) -> str:
    if explicit and explicit != "auto":
        return explicit
    ext = path.suffix.lower()
    if ext == ".json":
        return "json"
    if ext in {".yaml", ".yml"}:
        return "yaml"
    return "human-md"


def parse_front_matter(text: str) -> Tuple[Dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text
    meta_text, body = parts
    meta_text = meta_text.replace("---\n", "", 1)
    if yaml is None:
        return {}, body
    parsed = yaml.safe_load(meta_text) or {}
    if not isinstance(parsed, dict):
        return {}, body
    return parsed, body


def parse_markdown(text: str, source_path: Path) -> Dict[str, Any]:
    metadata, body = parse_front_matter(text)
    lines = body.splitlines()
    sections: Dict[str, List[str]] = {}
    current = "root"
    sections[current] = []
    for line in lines:
        m = re.match(r"^##+\s+(.+)$", line.strip())
        if m:
            current = m.group(1).strip().lower()
            sections[current] = []
            continue
        sections.setdefault(current, []).append(line)

    def _section_text(keywords: List[str]) -> str:
        for key, sec in sections.items():
            if any(k in key for k in keywords):
                return "\n".join(sec).strip()
        return ""

    steps: List[Dict[str, str]] = []
    procedure_text = _section_text(["procedure", "steps", "workflow"])
    for line in procedure_text.splitlines():
        m = re.match(r"^\s*(\d+)[\.\)]\s+(.+)$", line.strip())
        if m:
            steps.append({"id": m.group(1), "action": m.group(2).strip()})

    definitions: List[Dict[str, str]] = []
    definitions_text = _section_text(["definition"])
    for line in definitions_text.splitlines():
        line = line.strip().lstrip("-").strip()
        if ":" in line:
            term, definition = line.split(":", 1)
            term = term.strip()
            definition = definition.strip()
            if term and definition:
                definitions.append({"term": term, "definition": definition})

    scope_text = _section_text(["scope"])
    includes, excludes = [], []
    for raw in scope_text.splitlines():
        line = raw.strip().lstrip("-").strip()
        low = line.lower()
        if low.startswith("include"):
            includes.append(line.split(":", 1)[-1].strip() if ":" in line else line)
        elif low.startswith("exclude") or low.startswith("out-of-scope"):
            excludes.append(line.split(":", 1)[-1].strip() if ":" in line else line)

    return {
        "metadata": {
            "id": metadata.get("id") or source_path.stem,
            "version": str(metadata.get("version", "1.0.0")),
            "source_format": "human-md",
        },
        "purpose": _section_text(["purpose"]),
        "scope": {
            "includes": [s for s in includes if s],
            "excludes": [s for s in excludes if s],
            "raw": scope_text,
        },
        "definitions": definitions,
        "steps": steps,
        "raw_sections": {k: "\n".join(v).strip() for k, v in sections.items()},
    }


def parse_yaml_or_json(text: str, source_fmt: str, source_path: Path) -> Dict[str, Any]:
    if source_fmt == "json":
        raw = json.loads(text)
    else:
        if yaml is None:
            raise RuntimeError("PyYAML is required to parse YAML input")
        raw = yaml.safe_load(text)
    if not isinstance(raw, dict):
        raise ValueError("Invalid SOP structure: root must be an object")

    sop = raw.get("sop", raw)
    if not isinstance(sop, dict):
        raise ValueError("Invalid SOP structure: missing sop object")

    metadata = sop.get("metadata", {})
    steps: List[Dict[str, str]] = []
    for idx, item in enumerate(sop.get("steps", []), start=1):
        if isinstance(item, dict):
            steps.append(
                {
                    "id": str(item.get("id", idx)),
                    "action": str(item.get("action", "")).strip(),
                }
            )
    # State machine fallback
    if not steps:
        for idx, item in enumerate(sop.get("states", []), start=1):
            if isinstance(item, dict):
                steps.append(
                    {
                        "id": str(item.get("id", idx)),
                        "action": str(item.get("action", item.get("name", ""))).strip(),
                    }
                )

    definitions = sop.get("definitions", [])
    if not isinstance(definitions, list):
        definitions = []

    scope = sop.get("scope", {})
    if not isinstance(scope, dict):
        scope = {"raw": str(scope)}

    return {
        "metadata": {
            "id": str(metadata.get("id", source_path.stem)),
            "version": str(metadata.get("version", "1.0.0")),
            "source_format": source_fmt,
        },
        "purpose": str(sop.get("purpose", "")),
        "scope": {
            "includes": scope.get("includes", []) if isinstance(scope.get("includes", []), list) else [],
            "excludes": scope.get("excludes", []) if isinstance(scope.get("excludes", []), list) else [],
            "raw": str(scope.get("raw", "")),
        },
        "definitions": [d for d in definitions if isinstance(d, dict)],
        "steps": [s for s in steps if s.get("action")],
        "raw_sections": {"source": sop},
    }


def to_markdown(model: Dict[str, Any]) -> str:
    meta = model["metadata"]
    lines: List[str] = [
        "---",
        f"id: {meta.get('id', '')}",
        f"version: {meta.get('version', '1.0.0')}",
        f"source_format: {meta.get('source_format', 'unknown')}",
        "---",
        "",
        f"# SOP: {meta.get('id', 'unnamed')}",
        "",
        "## Purpose",
        model.get("purpose", "").strip() or "TBD",
        "",
        "## Scope",
    ]
    includes = model.get("scope", {}).get("includes", [])
    excludes = model.get("scope", {}).get("excludes", [])
    if includes:
        lines.append("Includes:")
        lines.extend([f"- {item}" for item in includes])
    if excludes:
        lines.append("Excludes:")
        lines.extend([f"- {item}" for item in excludes])
    if not includes and not excludes:
        raw_scope = model.get("scope", {}).get("raw", "")
        lines.append(raw_scope or "TBD")

    lines.extend(["", "## Definitions"])
    defs = model.get("definitions", [])
    if defs:
        for item in defs:
            lines.append(f"- {item.get('term', 'term')}: {item.get('definition', '')}")
    else:
        lines.append("- TBD: No definitions mapped")

    lines.extend(["", "## Procedure"])
    steps = model.get("steps", [])
    if steps:
        for idx, step in enumerate(steps, start=1):
            lines.append(f"{idx}. {step.get('action', '').strip() or 'TBD'}")
    else:
        lines.append("1. TBD")
    return "\n".join(lines).strip() + "\n"


def to_structured(model: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "sop": {
            "metadata": model.get("metadata", {}),
            "purpose": model.get("purpose", ""),
            "scope": model.get("scope", {}),
            "definitions": model.get("definitions", []),
            "steps": model.get("steps", []),
        }
    }


def default_output_path(source: Path, target_format: str) -> Path:
    ext = {"human-md": ".md", "yaml": ".yaml", "json": ".json"}[target_format]
    return source.with_suffix(ext)


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic SOP format converter.")
    parser.add_argument("source_file", help="Path to source SOP file")
    parser.add_argument("target_format", choices=["human-md", "yaml", "json"])
    parser.add_argument("--source-format", default="auto", choices=["auto", "human-md", "yaml", "json"])
    parser.add_argument("--output", help="Target output path")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Print JSON summary")
    args = parser.parse_args()

    source = Path(args.source_file)
    if not source.exists():
        print(f"ERROR: source file not found: {source}", file=sys.stderr)
        return 2

    source_fmt = detect_format(source, args.source_format)
    text = source.read_text(encoding="utf-8")

    try:
        if source_fmt == "human-md":
            model = parse_markdown(text, source)
        else:
            model = parse_yaml_or_json(text, source_fmt, source)
    except Exception as exc:
        print(f"ERROR: failed to parse source: {exc}", file=sys.stderr)
        return 2

    out_path = Path(args.output) if args.output else default_output_path(source, args.target_format)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if args.target_format == "human-md":
            out_text = to_markdown(model)
            out_path.write_text(out_text, encoding="utf-8")
        elif args.target_format == "json":
            out_data = to_structured(model)
            out_path.write_text(json.dumps(out_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        else:
            if yaml is None:
                raise RuntimeError("PyYAML is required to write YAML output")
            out_data = to_structured(model)
            out_path.write_text(yaml.safe_dump(out_data, sort_keys=False, allow_unicode=False), encoding="utf-8")
    except Exception as exc:
        print(f"ERROR: failed to write output: {exc}", file=sys.stderr)
        return 2

    summary = {
        "status": "ok",
        "source_file": str(source),
        "source_format": source_fmt,
        "target_format": args.target_format,
        "output_file": str(out_path),
        "steps_mapped": len(model.get("steps", [])),
        "definitions_mapped": len(model.get("definitions", [])),
    }
    if args.json_output:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Converted {source} ({source_fmt}) -> {out_path} ({args.target_format})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

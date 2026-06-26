#!/usr/bin/env python3
"""
Dispatch Squad — Task Enrichment (KB Injection)
Law #1: CODE > LLM — Template fill is deterministic.
Source: REUSED from dispatcher.md build_enriched_prompt() (L889-928)

Injects knowledge base context into task prompts based on enrichment level.
Uses domain-registry.yaml to find KB files, enrichment-rules.yaml for levels.

Usage:
    python squads/dispatch/scripts/enrich-task.py task.json --domain marketing_copy --level FULL
    python squads/dispatch/scripts/enrich-task.py task.json --output enriched-prompt.md
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# ENRICHMENT LEVELS (from enrichment-rules.yaml)
# ═══════════════════════════════════════════════════════════════════════════════

ENRICHMENT_CONFIG = {
    "MINIMAL": {"max_kb_chars": 0, "include_business": False},
    "STANDARD": {"max_kb_chars": 4500, "include_business": False},
    "FULL": {"max_kb_chars": 9000, "include_business": True},
}

TARGET_SECTIONS = [
    "## principles", "## princípios",
    "## examples", "## exemplos",
    "## anti-patterns", "## antipatterns",
    "## quick reference",
]


def extract_sections(content: str, targets: List[str], max_chars: int = 4500) -> str:
    """Extract relevant sections from a KB file."""
    sections = []
    lines = content.split("\n")
    capturing = False
    current_section = []

    for line in lines:
        line_lower = line.lower().strip()
        if any(line_lower.startswith(t) for t in targets):
            if current_section:
                sections.append("\n".join(current_section))
            current_section = [line]
            capturing = True
        elif capturing and line.startswith("## ") and not any(line.lower().strip().startswith(t) for t in targets):
            sections.append("\n".join(current_section))
            current_section = []
            capturing = False
        elif capturing:
            current_section.append(line)

    if current_section:
        sections.append("\n".join(current_section))

    combined = "\n\n".join(sections)
    return combined[:max_chars]


def load_kb_context(
    kb_files: List[str],
    project_root: str,
    max_chars: int = 4500,
) -> str:
    """Load and extract relevant sections from KB files."""
    parts = []
    total_chars = 0

    for kb_file in kb_files:
        path = os.path.join(project_root, kb_file)
        if not os.path.exists(path):
            continue

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        remaining = max_chars - total_chars
        if remaining <= 0:
            break

        extracted = extract_sections(content, TARGET_SECTIONS, remaining)
        if extracted:
            parts.append(f"# From: {kb_file}\n{extracted}")
            total_chars += len(extracted)

    return "\n\n---\n\n".join(parts)


def build_enriched_prompt(
    task: dict,
    kb_context: str,
    business_context: Optional[str] = None,
    level: str = "STANDARD",
) -> str:
    """Build enriched prompt for a task.

    Source: REUSED from dispatcher.md build_enriched_prompt() (L889-928)
    CRITICAL: Prompts in ENGLISH for Haiku efficiency.
    """
    parts = []

    # HEADER (STATIC — cached across wave)
    parts.append(f"""## TASK
Execute this atomic task: {task.get('description', task.get('title', 'Unknown'))}
ID: {task.get('task_id', task.get('id', 'unknown'))} | Domain: {task.get('domain', 'unknown')}

## RULES (CRITICAL — Follow exactly)
1. DO NOT ask questions. Execute immediately.
2. Return ONLY the requested output. Nothing else before or after.
3. Execute THIS task only — no more, no less.
4. If writing content for users, write in Portuguese (pt-BR).
5. Verify ALL acceptance criteria before finishing.
""")

    # KB CONTEXT (STATIC — cached for same-domain tasks)
    if level in ("STANDARD", "FULL") and kb_context:
        parts.append(f"""## KNOWLEDGE CONTEXT
Use this context to inform your output:
{kb_context}
""")

    # BUSINESS CONTEXT (STATIC — FULL only)
    if level == "FULL" and business_context:
        parts.append(f"""## BUSINESS CONTEXT
{business_context}
""")

    # TASK SPECIFICS (DYNAMIC — unique per task)
    acceptance = task.get("acceptance_criteria", task.get("acceptance", []))
    if isinstance(acceptance, list):
        criteria_str = "\n".join(f"- [ ] {c}" for c in acceptance)
    else:
        criteria_str = str(acceptance)

    output_path = task.get("output_path", "")

    parts.append(f"""## ACCEPTANCE CRITERIA
{criteria_str}

## OUTPUT
Save output to: {output_path}

## CLOSING
When done, return ONLY a summary in this format:
STATUS: PASS | FAIL
OUTPUT: {output_path}
METRICS: {{word_count}} words, {{section_count}} sections
ISSUES: {{list if any, "none" if clean}}
DO NOT return the full content — it is already saved to the output file.
""")

    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Enrich task prompt with KB context")
    parser.add_argument("task_file", help="Path to task JSON file")
    parser.add_argument("--domain", help="Domain for KB lookup")
    parser.add_argument("--level", default="STANDARD", choices=["MINIMAL", "STANDARD", "FULL"])
    parser.add_argument("--output", help="Output file for enriched prompt")
    parser.add_argument("--root", default=".", help="Project root directory")
    parser.add_argument("--kb-files", nargs="*", help="KB files to load (overrides domain lookup)")
    args = parser.parse_args()

    with open(args.task_file, "r", encoding="utf-8") as f:
        task = json.load(f)

    config = ENRICHMENT_CONFIG.get(args.level, ENRICHMENT_CONFIG["STANDARD"])

    # Load KB context
    kb_context = ""
    if config["max_kb_chars"] > 0:
        kb_files = args.kb_files or task.get("kb_files", [])
        if kb_files:
            kb_context = load_kb_context(kb_files, args.root, config["max_kb_chars"])

    # Build enriched prompt
    prompt = build_enriched_prompt(task, kb_context, level=args.level)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"Enriched prompt written to: {args.output}")
        print(f"Level: {args.level} | KB chars: {len(kb_context)} | Prompt chars: {len(prompt)}")
    else:
        print(prompt)


if __name__ == "__main__":
    main()

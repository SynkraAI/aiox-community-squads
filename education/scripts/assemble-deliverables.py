#!/usr/bin/env python3
"""
Course Deliverables Assembler
Replaces LLM-based generate-deliverables.md task with deterministic file assembly.

Usage:
  python squads/education/scripts/assemble-deliverables.py \
    --domain "python-fundamentals" \
    --type production \
    --minds-path minds/python-fundamentals/ \
    --output output/courses/python-fundamentals/
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Component Manifest — what to collect per deliverable type
# ─────────────────────────────────────────────────────────────────────────────

COMPONENT_GROUPS = {
    "source": {
        "label": "Source Documents",
        "patterns": [
            ("curriculum", "curriculum-*.md"),
            ("modules", "module-*.md"),
            ("lessons", "lesson-*.md"),
        ],
    },
    "assessments": {
        "label": "Assessments",
        "patterns": [
            ("assessments", "diagnostic-*.md"),
            ("assessments", "transfer-*.md"),
            ("assessments", "practice-*.md"),
        ],
    },
    "media": {
        "label": "Media Specifications",
        "patterns": [
            ("media-specs", "media-*.md"),
            ("media-specs", "arcs-*.md"),
        ],
    },
    "reports": {
        "label": "Reports & Validations",
        "patterns": [
            ("reports", "*-report.md"),
            ("reports", "cognitive-load-*.md"),
            ("reports", "mec-*.md"),
            ("reports", "validation-*.md"),
        ],
    },
    "schedules": {
        "label": "Schedules",
        "patterns": [
            ("schedules", "review-schedule.md"),
            ("schedules", "competency-*.md"),
            ("schedules", "knowledge-map*.md"),
        ],
    },
}

DELIVERABLE_TYPES = {
    "production": {
        "label": "Production Package",
        "groups": ["source", "assessments", "media", "schedules"],
        "extra_docs": ["instructor-guide.md"],
    },
    "lms": {
        "label": "LMS Package",
        "groups": ["source", "assessments", "schedules"],
        "extra_docs": ["scorm-config.md", "completion-criteria.md"],
    },
    "mec-submission": {
        "label": "MEC Submission Package",
        "groups": ["source", "assessments", "reports"],
        "extra_docs": ["ppc.md", "faculty-credentials.md"],
    },
}


def find_files(source_dir: str, pattern: str) -> list[Path]:
    """Find files matching a glob pattern in source directory."""
    source = Path(source_dir)
    if not source.exists():
        return []
    return sorted(source.glob(pattern))


def collect_components(minds_path: str) -> dict[str, list[Path]]:
    """Collect all course components from minds directory."""
    collected = {}

    for group_name, group_def in COMPONENT_GROUPS.items():
        files = []
        for _subfolder, pattern in group_def["patterns"]:
            found = find_files(minds_path, f"**/{pattern}")
            files.extend(found)
        # Deduplicate
        seen = set()
        unique = []
        for f in files:
            if f.name not in seen:
                seen.add(f.name)
                unique.append(f)
        collected[group_name] = unique

    return collected


def copy_to_deliverable(
    files: list[Path],
    dest_dir: Path,
    subfolder: str,
) -> list[str]:
    """Copy files to deliverable directory, return list of relative paths."""
    target = dest_dir / subfolder
    target.mkdir(parents=True, exist_ok=True)

    copied = []
    for f in files:
        dest = target / f.name
        shutil.copy2(f, dest)
        copied.append(f"{subfolder}/{f.name}")

    return copied


def generate_index(
    domain: str,
    deliverable_type: str,
    file_manifest: dict[str, list[str]],
    output_dir: Path,
) -> str:
    """Generate INDEX.md for the deliverable package."""
    lines = [
        f"# Course Deliverables: {domain}",
        "",
        f"**Type:** {DELIVERABLE_TYPES.get(deliverable_type, {}).get('label', deliverable_type)}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Location:** `{output_dir}`",
        "",
        "---",
        "",
    ]

    total = 0
    for group_name, files in file_manifest.items():
        label = COMPONENT_GROUPS.get(group_name, {}).get("label", group_name)
        lines.append(f"## {label}")
        lines.append("")
        if files:
            for f in sorted(files):
                lines.append(f"- [`{f}`]({f})")
            total += len(files)
        else:
            lines.append("- *(no files found)*")
        lines.append("")

    lines += [
        "---",
        "",
        f"**Total Files:** {total}",
        "",
        "## Quality Checklist",
        "",
        "- [ ] All curriculum documents present",
        "- [ ] All module designs present",
        "- [ ] All lesson plans present",
        "- [ ] Assessment specifications complete",
        "- [ ] Media specifications present",
        "- [ ] Validation reports clean (no FAIL)",
        "- [ ] Schedule generated",
        "- [ ] INDEX.md reviewed",
        "",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Course Deliverables Assembler — deterministic file collection"
    )
    parser.add_argument("--domain", required=True, help="Course domain name")
    parser.add_argument(
        "--type",
        required=True,
        choices=["production", "lms", "mec-submission", "all"],
        help="Deliverable type",
    )
    parser.add_argument("--minds-path", required=True, help="Path to minds/{domain}/ directory")
    parser.add_argument("--output", default=None, help="Output directory (default: output/courses/{domain}/)")

    args = parser.parse_args()

    minds_path = args.minds_path
    if not os.path.exists(minds_path):
        print(f"ERROR: minds path not found: {minds_path}", file=sys.stderr)
        sys.exit(1)

    output_base = Path(args.output or f"output/courses/{args.domain}")

    # Determine which types to generate
    types_to_generate = (
        list(DELIVERABLE_TYPES.keys()) if args.type == "all" else [args.type]
    )

    # Collect all components
    collected = collect_components(minds_path)
    total_source = sum(len(v) for v in collected.values())
    print(f"Found {total_source} source files in {minds_path}")

    if total_source == 0:
        print("WARNING: No source files found. Check --minds-path.", file=sys.stderr)

    for dtype in types_to_generate:
        type_def = DELIVERABLE_TYPES[dtype]
        dest_dir = output_base / "deliverables" / dtype
        dest_dir.mkdir(parents=True, exist_ok=True)

        print(f"\nAssembling: {type_def['label']}")

        manifest = {}
        for group_name in type_def["groups"]:
            files = collected.get(group_name, [])
            if files:
                copied = copy_to_deliverable(files, dest_dir, group_name)
                manifest[group_name] = copied
                print(f"  {group_name}: {len(copied)} files")
            else:
                manifest[group_name] = []
                print(f"  {group_name}: 0 files (missing)")

        # Generate INDEX.md
        index_md = generate_index(args.domain, dtype, manifest, dest_dir)
        index_path = dest_dir / "INDEX.md"
        index_path.write_text(index_md, encoding="utf-8")
        print(f"  INDEX.md generated")

    # Copy source files to source/ directory
    source_dir = output_base / "source"
    for group_name, files in collected.items():
        if files:
            copy_to_deliverable(files, source_dir, group_name)

    print(f"\nDeliverable package ready at: {output_base}")


if __name__ == "__main__":
    main()

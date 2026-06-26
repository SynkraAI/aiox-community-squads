#!/usr/bin/env python3
"""
Session Usage Report Generator for Claude Code.

Analyzes JSONL session files across all projects to produce a usage report
covering skills, agents, commands, shell runners, and cleanup recommendations.

Usage:
    python3 session-usage-report.py [--days 14] [--output json|markdown|html] [--projects-dir ~/.claude/projects]

Output:
    - JSON: structured data matching session-usage-report-tmpl.yaml
    - Markdown: human-readable report (default)
    - HTML: executive static report for sharing/review

Data Sources:
    - ~/.claude/projects/*/*.jsonl (session files)
    - git log --since (commit categorization)
    - .claude/skills/, .claude/agents/ (available inventory)
"""
import json
import os
import re
import glob
import sys
import argparse
import difflib
from collections import Counter
from datetime import datetime

from session_usage_report_cache import (
    ensure_dir,
    get_cache_paths as build_cache_paths,
    file_fingerprint as build_file_fingerprint,
    cache_key_for_file as build_cache_key_for_file,
    load_session_entries as read_session_entries,
    select_session_branch as select_session_branch_impl,
    serialize_session_result as serialize_session_result_impl,
    deserialize_session_result as deserialize_session_result_impl,
    read_cached_json as read_cached_json_impl,
    write_cached_json as write_cached_json_impl,
    get_session_meta as get_session_meta_impl,
)
from session_usage_report_facets import (
    truncate_middle,
    summarize_tool_use,
    sanitize_meta_for_insights,
    parse_json_object,
    run_insights_command,
    infer_basic_facets,
    normalize_string_list,
    normalize_facets,
    merge_facets,
    make_facet_summary,
    merge_facet_summary,
    finalize_facet_summary,
    build_default_narrative,
    normalize_narrative,
    build_narrative_payload,
    get_session_facets as get_session_facets_impl,
    generate_narrative_insights as generate_narrative_insights_impl,
    build_transcript_excerpt as build_transcript_excerpt_impl,
)
from session_usage_report_html import format_html as render_html_report
from session_usage_report_inventory import (
    get_recent_commits as get_recent_commits_impl,
    discover_inventory as discover_inventory_impl,
)
from session_usage_report_markdown import format_markdown as render_markdown_report
from session_usage_report_pipeline import generate_report as generate_report_impl
from session_usage_report_recommendations import (
    safe_div,
    make_recommendation,
    sort_recommendations,
    build_project_recommendations,
    build_global_recommendations,
    generate_workflow_recommendations,
)

# ─── Constants ────────────────────────────────────────────────────────────────

BUILTIN_COMMANDS = {
    "/clear", "/model", "/compact", "/export", "/config", "/help", "/fast",
    "/memory", "/permissions", "/status", "/doctor", "/review", "/cost",
    "/init", "/bug", "/login", "/logout", "/mcp", "/vim", "/terminal-setup",
    "/add-dir", "/release-notes", "/listen"
}

DEFAULT_USAGE_DATA_DIR = os.path.expanduser("~/.claude/usage-data/claude-code-mastery")
SESSION_META_COUNTER_FIELDS = {
    "slash_commands",
    "skill_invocations",
    "agent_types",
    "shell_runners",
    "tools",
    "tool_error_categories",
    "languages",
}
SESSION_META_SET_FIELDS = {"dates", "files_modified"}
FACET_LIST_FIELDS = {"goal_categories", "friction_points"}
NARRATIVE_FIELDS = {
    "at_a_glance",
    "project_areas",
    "interaction_style",
    "what_works",
    "friction_analysis",
    "suggestions",
    "on_the_horizon",
    "fun_ending",
}
CACHE_WARNING_PATHS = set()
IMPACT_WEIGHTS = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
EFFORT_WEIGHTS = {"Quick": 3, "Medium": 2, "Investment": 1}


def short_name(path):
    """Extract short project name from Claude projects directory path."""
    import re
    base = os.path.basename(path)
    # Strip -Users-{username}-Code- prefix (any username)
    m = re.search(r"-Users-[^-]+-Code-", base)
    if m:
        return base[m.end():]
    # Fallback: strip -Users-{name} prefix
    if "-Users-" in base:
        return base.split("-Users-", 1)[-1]
    return base


def find_projects(projects_dir):
    """Discover all project directories with recent JSONL files."""
    projects = {}
    for d in sorted(glob.glob(os.path.join(projects_dir, "*/"))):
        name = short_name(d.rstrip("/"))
        projects[name] = d.rstrip("/")
    return projects


def parse_timestamp(value):
    """Parse ISO timestamp strings safely."""
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def extract_text_content(message):
    """Extract concatenated text content from a Claude message payload."""
    parts = []

    def collect(value):
        if isinstance(value, str):
            parts.append(value)
            return
        if isinstance(value, list):
            for item in value:
                collect(item)
            return
        if isinstance(value, dict):
            if isinstance(value.get("text"), str):
                parts.append(value["text"])
            if "content" in value:
                collect(value.get("content"))

    if isinstance(message, dict):
        collect(message.get("content", ""))
    else:
        collect(message)
    return " ".join(parts)


def is_human_user_message(entry):
    """Return True when the entry contains actual user-authored text."""
    if entry.get("type") != "user":
        return False

    message = entry.get("message")
    if isinstance(message, str):
        return bool(message.strip())
    if not isinstance(message, dict):
        return False

    content = message.get("content", "")
    if isinstance(content, str):
        return bool(content.strip())
    if not isinstance(content, list):
        return False

    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            if isinstance(block.get("text"), str) and block["text"].strip():
                return True
    return False


def count_line_changes(old_text, new_text):
    """Approximate line additions/removals for Edit tool operations."""
    lines_added = 0
    lines_removed = 0
    for diff_line in difflib.ndiff(
        (old_text or "").splitlines(),
        (new_text or "").splitlines(),
    ):
        if diff_line.startswith("+ "):
            lines_added += 1
        elif diff_line.startswith("- "):
            lines_removed += 1
    return lines_added, lines_removed


def infer_language_label(file_path):
    """Map file extensions to compact language buckets."""
    _, extension = os.path.splitext(str(file_path or "").lower())
    language_map = {
        ".py": "Python",
        ".ts": "TypeScript",
        ".tsx": "TypeScript React",
        ".js": "JavaScript",
        ".jsx": "JavaScript React",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".md": "Markdown",
        ".sh": "Shell",
        ".zsh": "Shell",
        ".css": "CSS",
        ".scss": "SCSS",
        ".html": "HTML",
        ".sql": "SQL",
        ".toml": "TOML",
        ".cjs": "JavaScript",
        ".mjs": "JavaScript",
    }
    return language_map.get(extension, extension.lstrip(".").upper() if extension else "")


def summarize_user_instruction(text, max_chars=180):
    """Keep user instructions compact for narrative evidence packs."""
    clean = " ".join(str(text or "").split())
    if len(clean) <= max_chars:
        return clean
    return clean[: max_chars - 3] + "..."


def classify_tool_error(content):
    """Map tool error text into a stable bucket."""
    lower_content = (content or "").lower()
    if "exit code" in lower_content:
        return "Command Failed"
    if "rejected" in lower_content or "doesn't want" in lower_content:
        return "User Rejected"
    if "string to replace not found" in lower_content or "no changes" in lower_content:
        return "Edit Failed"
    if "modified since read" in lower_content:
        return "File Changed"
    if "exceeds maximum" in lower_content or "too large" in lower_content:
        return "File Too Large"
    if "file not found" in lower_content or "does not exist" in lower_content:
        return "File Not Found"
    return "Other"


def select_dominant_session(entries):
    """Some transcript files contain stray entries from another session; keep the dominant one."""
    counts = Counter()
    for entry in entries:
        session_id = entry.get("sessionId")
        if session_id:
            counts[session_id] += 1
    return counts.most_common(1)[0][0] if counts else None


def build_selected_branch(entries, dominant_session_id):
    """Select the strongest leaf branch for the dominant session."""
    convo_entries = []
    entries_by_uuid = {}
    child_counts = Counter()

    for entry in entries:
        if entry.get("sessionId") != dominant_session_id:
            continue
        if entry.get("type") not in {"user", "assistant"}:
            continue
        uuid = entry.get("uuid")
        if not uuid:
            continue
        convo_entries.append(entry)
        entries_by_uuid[uuid] = entry
        parent_uuid = entry.get("parentUuid")
        if parent_uuid:
            child_counts[parent_uuid] += 1

    if not convo_entries:
        return [], 0

    leaves = [
        entry.get("uuid")
        for entry in convo_entries
        if entry.get("uuid") and child_counts[entry.get("uuid")] == 0
    ]
    if not leaves:
        ordered = sorted(
            convo_entries,
            key=lambda entry: parse_timestamp(entry.get("timestamp")) or datetime.min,
        )
        return ordered, 1

    best_branch = []
    best_score = None

    for leaf_uuid in leaves:
        chain = []
        seen = set()
        current_uuid = leaf_uuid

        while current_uuid and current_uuid not in seen:
            current = entries_by_uuid.get(current_uuid)
            if not current:
                break
            chain.append(current)
            seen.add(current_uuid)
            current_uuid = current.get("parentUuid")

        chain.reverse()

        human_messages = sum(1 for entry in chain if is_human_user_message(entry))
        assistant_messages = sum(1 for entry in chain if entry.get("type") == "assistant")
        tool_uses = 0
        timestamps = []
        for entry in chain:
            ts = parse_timestamp(entry.get("timestamp"))
            if ts:
                timestamps.append(ts)
            message = entry.get("message")
            if isinstance(message, dict):
                content = message.get("content", [])
                if isinstance(content, list):
                    tool_uses += sum(
                        1
                        for block in content
                        if isinstance(block, dict) and block.get("type") == "tool_use"
                    )

        duration_seconds = 0
        if len(timestamps) >= 2:
            duration_seconds = int((timestamps[-1] - timestamps[0]).total_seconds())
        latest_ts = timestamps[-1] if timestamps else datetime.min
        score = (human_messages, duration_seconds, assistant_messages, tool_uses, latest_ts)

        if best_score is None or score > best_score:
            best_score = score
            best_branch = chain

    return best_branch, len(leaves)


def make_metrics_bucket():
    """Shared aggregate structure for per-project and global metrics."""
    return {
        "dates": set(),
        "message_hours": [],
        "branches_total": 0,
        "branches_deduped": 0,
        "user_messages": 0,
        "assistant_messages": 0,
        "duration_minutes": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "tool_errors": 0,
        "tool_error_categories": Counter(),
        "user_interruptions": 0,
        "user_response_times": [],
        "sessions_with_task_agent": 0,
        "sessions_with_mcp": 0,
        "sessions_with_web_search": 0,
        "sessions_with_web_fetch": 0,
        "git_commits": 0,
        "git_pushes": 0,
        "lines_added": 0,
        "lines_removed": 0,
        "files_modified": set(),
        "languages": Counter(),
        "tools": Counter(),
        "session_files": 0,
    }


def merge_metrics(bucket, session_result):
    """Merge a single session analysis into an aggregate bucket."""
    bucket["dates"].update(session_result.get("dates", set()))
    bucket["message_hours"].extend(session_result.get("message_hours", []))
    bucket["branches_total"] += session_result.get("branches_total", 0)
    bucket["branches_deduped"] += session_result.get("branches_deduped", 0)
    bucket["user_messages"] += session_result.get("user_messages", 0)
    bucket["assistant_messages"] += session_result.get("assistant_messages", 0)
    bucket["duration_minutes"] += session_result.get("duration_minutes", 0)
    bucket["input_tokens"] += session_result.get("input_tokens", 0)
    bucket["output_tokens"] += session_result.get("output_tokens", 0)
    bucket["tool_errors"] += session_result.get("tool_errors", 0)
    bucket["tool_error_categories"].update(session_result.get("tool_error_categories", Counter()))
    bucket["user_interruptions"] += session_result.get("user_interruptions", 0)
    bucket["user_response_times"].extend(session_result.get("user_response_times", []))
    bucket["git_commits"] += session_result.get("git_commits", 0)
    bucket["git_pushes"] += session_result.get("git_pushes", 0)
    bucket["lines_added"] += session_result.get("lines_added", 0)
    bucket["lines_removed"] += session_result.get("lines_removed", 0)
    bucket["files_modified"].update(session_result.get("files_modified", set()))
    bucket["languages"].update(session_result.get("languages", Counter()))
    bucket["tools"].update(session_result.get("tools", Counter()))
    bucket["session_files"] += 1

    if session_result.get("uses_task_agent"):
        bucket["sessions_with_task_agent"] += 1
    if session_result.get("uses_mcp"):
        bucket["sessions_with_mcp"] += 1
    if session_result.get("uses_web_search"):
        bucket["sessions_with_web_search"] += 1
    if session_result.get("uses_web_fetch"):
        bucket["sessions_with_web_fetch"] += 1


def finalize_metrics(bucket):
    """Convert mutable aggregate fields into render-friendly values."""
    response_times = bucket.get("user_response_times", [])
    sorted_response_times = sorted(response_times)
    bucket["avg_user_response_seconds"] = round(sum(response_times) / len(response_times), 1) if response_times else 0
    if sorted_response_times:
        middle = len(sorted_response_times) // 2
        if len(sorted_response_times) % 2:
            median = sorted_response_times[middle]
        else:
            median = (sorted_response_times[middle - 1] + sorted_response_times[middle]) / 2
        bucket["median_user_response_seconds"] = round(median, 1)
    else:
        bucket["median_user_response_seconds"] = 0
    bucket["unique_files_modified"] = len(bucket.get("files_modified", set()))
    dates = sorted(bucket.get("dates", set()))
    bucket["date_range"] = f"{dates[0]} to {dates[-1]}" if dates else "unknown"
    bucket["days_active"] = len(dates)
    total_messages = bucket.get("user_messages", 0) + bucket.get("assistant_messages", 0)
    bucket["messages_per_day"] = round(total_messages / len(dates), 1) if dates else 0
    bucket["duration_hours"] = round(bucket.get("duration_minutes", 0) / 60.0, 1)
    return bucket


def normalize_skill_name(key):
    """Normalize slash commands and Skill tool names into a common form."""
    return key.lstrip("/")


def get_cache_paths(cache_root=None):
    """Resolve cache locations used by the report."""
    return build_cache_paths(cache_root, DEFAULT_USAGE_DATA_DIR)


def file_fingerprint(session_file):
    """Stable fingerprint for cache invalidation."""
    return build_file_fingerprint(session_file)


def cache_key_for_file(session_file):
    """Derive a stable cache key from the absolute session path."""
    return build_cache_key_for_file(session_file)


def load_session_entries(session_file):
    """Read a JSONL transcript while tolerating malformed lines."""
    return read_session_entries(session_file)


def select_session_branch(raw_entries):
    """Resolve the dominant session and its strongest branch."""
    return select_session_branch_impl(
        raw_entries,
        select_dominant_session_fn=select_dominant_session,
        build_selected_branch_fn=build_selected_branch,
    )


def serialize_session_result(result):
    """Convert in-memory session analysis into JSON-safe structures."""
    return serialize_session_result_impl(
        result,
        SESSION_META_COUNTER_FIELDS,
        SESSION_META_SET_FIELDS,
    )


def deserialize_session_result(payload):
    """Restore Counters/sets from cached JSON payloads."""
    return deserialize_session_result_impl(
        payload,
        SESSION_META_COUNTER_FIELDS,
        SESSION_META_SET_FIELDS,
    )


def read_cached_json(cache_file):
    """Load a cache file, returning None on corruption or absence."""
    return read_cached_json_impl(cache_file)


def write_cached_json(cache_file, payload):
    """Persist a cache file as formatted JSON."""
    return write_cached_json_impl(
        cache_file,
        payload,
        cache_warning_paths=CACHE_WARNING_PATHS,
    )


def get_session_meta(session_file, cache_root=None, use_cache=True, refresh_cache=False):
    """Load session meta from cache or compute it from the transcript."""
    return get_session_meta_impl(
        session_file,
        analyze_session_fn=analyze_session,
        default_usage_data_dir=DEFAULT_USAGE_DATA_DIR,
        counter_fields=SESSION_META_COUNTER_FIELDS,
        set_fields=SESSION_META_SET_FIELDS,
        cache_warning_paths=CACHE_WARNING_PATHS,
        cache_root=cache_root,
        use_cache=use_cache,
        refresh_cache=refresh_cache,
    )


def build_transcript_excerpt(
    session_file,
    max_chars=30000,
    insights_command=None,
    run_insights_command_fn=None,
):
    """Build a compact transcript for optional LLM insight extraction."""
    return build_transcript_excerpt_impl(
        session_file,
        load_session_entries_fn=load_session_entries,
        select_session_branch_fn=select_session_branch,
        extract_text_content_fn=extract_text_content,
        max_chars=max_chars,
        insights_command=insights_command,
        run_insights_command_fn=run_insights_command_fn or run_insights_command,
    )


def get_session_facets(
    session_file,
    session_meta,
    project_name=None,
    cache_root=None,
    use_cache=True,
    refresh_cache=False,
    insights_command=None,
):
    """Load or compute per-session facets, optionally enriched by an external command."""
    return get_session_facets_impl(
        session_file=session_file,
        session_meta=session_meta,
        cache_root=cache_root,
        use_cache=use_cache,
        refresh_cache=refresh_cache,
        insights_command=insights_command,
        project_name=project_name,
        default_usage_data_dir=DEFAULT_USAGE_DATA_DIR,
        file_fingerprint_fn=file_fingerprint,
        get_cache_paths_fn=build_cache_paths,
        cache_key_for_file_fn=cache_key_for_file,
        read_cached_json_fn=read_cached_json,
        write_cached_json_fn=write_cached_json,
        build_transcript_excerpt_fn=build_transcript_excerpt,
        sanitize_meta_for_insights_fn=sanitize_meta_for_insights,
        run_insights_command_fn=run_insights_command,
    )


def generate_narrative_insights(summary, facet_summary, data, insights_command=None):
    """Generate optional report-level narrative, with deterministic fallback."""
    return generate_narrative_insights_impl(
        summary=summary,
        facet_summary=facet_summary,
        data=data,
        insights_command=insights_command,
        run_insights_command_fn=run_insights_command,
        normalize_skill_name_fn=normalize_skill_name,
    )


def write_text_file(path, content):
    """Write plain text output to a target file."""
    ensure_dir(os.path.dirname(os.path.abspath(path)))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def format_html(data, days, project_roots=None):
    """Render the report as a standalone executive HTML page."""
    return render_html_report(
        data,
        days,
        project_roots=project_roots,
        discover_inventory_fn=discover_inventory,
        get_recent_commits_fn=get_recent_commits,
    )


def format_markdown(data, days, project_roots=None):
    """Render the report as Markdown."""
    return render_markdown_report(
        data,
        days,
        project_roots=project_roots,
        discover_inventory_fn=discover_inventory,
        get_recent_commits_fn=get_recent_commits,
        normalize_skill_name_fn=normalize_skill_name,
        narrative_fields=NARRATIVE_FIELDS,
    )


def analyze_session(session_file):
    """Analyze a single JSONL session file."""
    result = {
        "is_headless": False,
        "slash_commands": Counter(),
        "skill_invocations": Counter(),
        "agent_types": Counter(),
        "shell_runners": Counter(),
        "tools": Counter(),
        "dates": set(),
        "branches_total": 0,
        "branches_deduped": 0,
        "session_id": None,
        "user_messages": 0,
        "assistant_messages": 0,
        "duration_minutes": 0,
        "message_hours": [],
        "input_tokens": 0,
        "output_tokens": 0,
        "tool_errors": 0,
        "tool_error_categories": Counter(),
        "user_interruptions": 0,
        "user_response_times": [],
        "uses_task_agent": False,
        "uses_mcp": False,
        "uses_web_search": False,
        "uses_web_fetch": False,
        "git_commits": 0,
        "git_pushes": 0,
        "lines_added": 0,
        "lines_removed": 0,
        "files_modified": set(),
        "languages": Counter(),
        "user_instruction_snippets": [],
    }

    try:
        raw_entries = load_session_entries(session_file)
        if not raw_entries:
            return result

        dominant_session_id, selected_branch, branch_count = select_session_branch(raw_entries)
        result["session_id"] = dominant_session_id

        # Usage/adoption metrics should reflect all unique events in the dominant
        # session graph, not just the strongest surviving branch.
        if dominant_session_id:
            usage_entries = []
            seen_usage_entries = set()
            for entry in raw_entries:
                if entry.get("sessionId") != dominant_session_id:
                    continue
                entry_key = entry.get("uuid")
                if not entry_key:
                    entry_key = json.dumps(entry, sort_keys=True, ensure_ascii=False)
                if entry_key in seen_usage_entries:
                    continue
                seen_usage_entries.add(entry_key)
                usage_entries.append(entry)
        else:
            usage_entries = selected_branch

        # File-level dates and headless mode markers are still useful even when branch pruning.
        for entry in raw_entries:
            if entry.get("type") == "summary":
                ts = parse_timestamp(entry.get("timestamp"))
                if ts:
                    result["dates"].add(ts.strftime("%Y-%m-%d"))

            if dominant_session_id and entry.get("sessionId") != dominant_session_id:
                continue

            message = entry.get("message")
            if isinstance(message, dict) and message.get("type") == "queue-operation":
                result["is_headless"] = True

        result["branches_total"] = branch_count
        result["branches_deduped"] = max(branch_count - 1, 0)

        # Count usage across the full dominant session graph so workflow adoption
        # is not understated by branch selection.
        for entry in usage_entries:
            ts = parse_timestamp(entry.get("timestamp"))
            if ts:
                result["dates"].add(ts.strftime("%Y-%m-%d"))

            message = entry.get("message")
            if not isinstance(message, dict):
                continue

            usage = message.get("usage", {})
            if isinstance(usage, dict):
                result["input_tokens"] += usage.get("input_tokens", 0) or 0
                result["output_tokens"] += usage.get("output_tokens", 0) or 0

            content = extract_text_content(message)
            for cmd in re.findall(r"<command-name>(.*?)</command-name>", content):
                cmd_clean = "/" + cmd if not cmd.startswith("/") else cmd
                if cmd_clean not in BUILTIN_COMMANDS:
                    result["slash_commands"][cmd_clean] += 1

            msg_content = message.get("content", [])
            if isinstance(msg_content, str):
                if "[Request interrupted by user" in msg_content:
                    result["user_interruptions"] += 1
                continue

            if not isinstance(msg_content, list):
                continue

            for block in msg_content:
                if not isinstance(block, dict):
                    continue

                block_type = block.get("type")
                if block_type == "text":
                    if "[Request interrupted by user" in str(block.get("text", "")):
                        result["user_interruptions"] += 1
                    continue

                if block_type == "tool_result":
                    if block.get("is_error"):
                        error_content = extract_text_content({"content": [block]})
                        result["tool_errors"] += 1
                        result["tool_error_categories"][classify_tool_error(error_content)] += 1
                    continue

                if block_type != "tool_use":
                    continue

                tool_name = block.get("name", "")
                tool_input = block.get("input", {}) or {}
                result["tools"][tool_name] += 1

                if tool_name == "Skill":
                    skill = tool_input.get("skill", "unknown")
                    result["skill_invocations"][skill] += 1

                elif tool_name == "Agent":
                    agent_type = tool_input.get("subagent_type", "general-purpose")
                    result["agent_types"][agent_type] += 1
                    result["uses_task_agent"] = True

                elif tool_name == "Bash":
                    cmd = tool_input.get("command", "")
                    lowered = f" {cmd.strip().lower()} "
                    if " git commit" in lowered or lowered.startswith("git commit "):
                        result["git_commits"] += 1
                    if " git push" in lowered or lowered.startswith("git push "):
                        result["git_pushes"] += 1
                    for sh in re.findall(r"[\w/.-]*\w+\.sh\b", cmd):
                        result["shell_runners"][os.path.basename(sh)] += 1

                if isinstance(tool_name, str) and tool_name.startswith("mcp__"):
                    result["uses_mcp"] = True
                if tool_name == "WebSearch":
                    result["uses_web_search"] = True
                if tool_name == "WebFetch":
                    result["uses_web_fetch"] = True

                file_path = tool_input.get("file_path")
                if isinstance(file_path, str) and file_path:
                    result["files_modified"].add(file_path)
                    language = infer_language_label(file_path)
                    if language:
                        result["languages"][language] += 1

                if tool_name == "Edit":
                    old_text = tool_input.get("old_string", "")
                    new_text = tool_input.get("new_string", "")
                    added, removed = count_line_changes(old_text, new_text)
                    result["lines_added"] += added
                    result["lines_removed"] += removed
                elif tool_name == "Write":
                    write_content = tool_input.get("content", "")
                    if isinstance(write_content, str) and write_content:
                        result["lines_added"] += len(write_content.splitlines()) or 1

        branch_timestamps = []
        last_assistant_ts = None

        for entry in selected_branch:
            ts = parse_timestamp(entry.get("timestamp"))
            if ts:
                branch_timestamps.append(ts)
                result["dates"].add(ts.strftime("%Y-%m-%d"))
                result["message_hours"].append(ts.hour)

            if entry.get("type") == "assistant":
                result["assistant_messages"] += 1
            elif entry.get("type") == "user" and is_human_user_message(entry):
                result["user_messages"] += 1
                instruction = summarize_user_instruction(extract_text_content(entry.get("message", {})))
                if instruction and instruction not in result["user_instruction_snippets"]:
                    result["user_instruction_snippets"].append(instruction)
                if len(result["user_instruction_snippets"]) > 8:
                    result["user_instruction_snippets"] = result["user_instruction_snippets"][:8]
                if last_assistant_ts and ts:
                    response_time = (ts - last_assistant_ts).total_seconds()
                    if 2 < response_time < 3600:
                        result["user_response_times"].append(response_time)

            message = entry.get("message")
            if not isinstance(message, dict):
                continue

            if entry.get("type") == "assistant" and ts:
                last_assistant_ts = ts

        if len(branch_timestamps) >= 2:
            result["duration_minutes"] = int(
                round((branch_timestamps[-1] - branch_timestamps[0]).total_seconds() / 60.0)
            )

    except Exception as e:
        print(f"  Warning: error processing {session_file}: {e}", file=sys.stderr)

    return result


def get_recent_commits(repo_path, days):
    """Get categorized commits from git log."""
    return get_recent_commits_impl(repo_path, days)


def discover_inventory(project_root):
    """Discover available skills, agents, and command directories."""
    return discover_inventory_impl(project_root)


def generate_report(
    projects_dir,
    days,
    project_roots=None,
    cache_dir=None,
    use_cache=True,
    refresh_cache=False,
    insights_command=None,
):
    """Main analysis pipeline."""
    return generate_report_impl(
        projects_dir=projects_dir,
        days=days,
        project_roots=project_roots,
        cache_dir=cache_dir,
        use_cache=use_cache,
        refresh_cache=refresh_cache,
        insights_command=insights_command,
        find_projects_fn=find_projects,
        make_metrics_bucket_fn=make_metrics_bucket,
        merge_metrics_fn=merge_metrics,
        finalize_metrics_fn=finalize_metrics,
        make_facet_summary_fn=make_facet_summary,
        merge_facet_summary_fn=merge_facet_summary,
        finalize_facet_summary_fn=finalize_facet_summary,
        get_session_meta_fn=get_session_meta,
        get_session_facets_fn=get_session_facets,
        load_session_entries_fn=load_session_entries,
        extract_text_content_fn=extract_text_content,
        normalize_skill_name_fn=normalize_skill_name,
        generate_narrative_insights_fn=generate_narrative_insights,
        generate_workflow_recommendations_fn=generate_workflow_recommendations,
    )


def main():
    parser = argparse.ArgumentParser(description="Claude Code Session Usage Report")
    parser.add_argument("--days", type=int, default=14, help="Analysis period in days (default: 14)")
    parser.add_argument("--output", choices=["markdown", "json", "html"], default="markdown", help="Output format")
    parser.add_argument("--projects-dir", default=os.path.expanduser("~/.claude/projects"),
                        help="Claude projects directory")
    parser.add_argument("--repo", action="append", default=[], dest="repos",
                        help="Repository root for inventory analysis (can repeat)")
    parser.add_argument("--cache-dir", default=DEFAULT_USAGE_DATA_DIR,
                        help="Directory used for session-meta/facet caches")
    parser.add_argument("--no-cache", action="store_true",
                        help="Disable reading/writing cache files")
    parser.add_argument("--refresh-cache", action="store_true",
                        help="Ignore cache hits and rebuild cached artifacts")
    parser.add_argument("--insights-command", default=os.environ.get("CLAUDE_CODE_MASTERY_INSIGHTS_COMMAND", ""),
                        help="Optional command that reads JSON from stdin and returns JSON facets/narrative")
    parser.add_argument("--html-file", default="",
                        help="Optional path to write the HTML report when --output html is used")
    args = parser.parse_args()

    # Build project_roots from --repo flags
    project_roots = {}
    for repo in args.repos:
        repo = os.path.expanduser(repo)
        if os.path.isdir(repo):
            project_roots[os.path.basename(repo)] = repo

    print(f"Analyzing sessions from last {args.days} days...", file=sys.stderr)
    data = generate_report(
        args.projects_dir,
        args.days,
        project_roots,
        cache_dir=args.cache_dir,
        use_cache=not args.no_cache,
        refresh_cache=args.refresh_cache,
        insights_command=args.insights_command or None,
    )

    if args.output == "markdown":
        print(format_markdown(data, args.days, project_roots))
    elif args.output == "html":
        html_report = format_html(data, args.days, project_roots)
        if args.html_file:
            write_text_file(args.html_file, html_report)
            print(os.path.abspath(os.path.expanduser(args.html_file)))
        else:
            print(html_report)
    else:
        # Normalize skills for JSON output (same dedup as markdown)
        normalized_skills = Counter()
        for k, v in data["skills"].items():
            normalized_skills[normalize_skill_name(k)] += v
        for k, v in data["headless_skills"].items():
            normalized_skills[normalize_skill_name(k)] += v

        # JSON output (compatible with template)
        print(json.dumps({
            "report": {
                "period_days": args.days,
                "generated_at": datetime.now().isoformat(),
            },
            "summary": {
                **{
                    k: dict(v) if isinstance(v, Counter) else v
                    for k, v in data.get("summary", {}).items()
                },
                "projects": {k: {
                    "interactive": v["interactive"],
                    "headless": v["headless"],
                    "subagents": v["subagents"],
                    "date_range": v["date_range"],
                    "input_tokens": v.get("input_tokens", 0),
                    "output_tokens": v.get("output_tokens", 0),
                    "tool_errors": v.get("tool_errors", 0),
                    "branches_total": v.get("branches_total", 0),
                    "branches_deduped": v.get("branches_deduped", 0),
                    "lines_added": v.get("lines_added", 0),
                    "lines_removed": v.get("lines_removed", 0),
                    "unique_files_modified": v.get("unique_files_modified", 0),
                    "avg_user_response_seconds": v.get("avg_user_response_seconds", 0),
                } for k, v in data["projects"].items()},
            },
            "facets": {
                key: dict(value) if isinstance(value, Counter) else value
                for key, value in data.get("facet_summary", {}).items()
            },
            "narrative": data.get("narrative", {}),
            "recommendations": data.get("recommendations", {}),
            "usage_inventory": data.get("usage_inventory", {}),
            "top_skills": dict(normalized_skills.most_common(30)),
            "top_agents": dict(data["agents"].most_common(20)),
            "top_runners": dict(data["runners"].most_common(15)),
            "top_tools": dict(data.get("tools", Counter()).most_common(20)),
        }, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Aggregation pipeline for the session usage report.

The main script keeps the public API and injects its own patchable callbacks.
"""
import glob
import os
from collections import Counter, defaultdict
from datetime import datetime, timedelta

from session_usage_report_usage import (
    finalize_usage_inventory,
    make_usage_inventory_state,
    update_usage_inventory,
)


META_SESSION_MARKERS = (
    "RESPOND WITH ONLY A VALID JSON OBJECT",
    "record_facets",
    '"mode": "facet"',
    '"mode": "narrative"',
)


def list_recent_sessions(project_path, cutoff):
    """Return main and subagent session files modified within the analysis window."""
    main_sessions = [
        session_file
        for session_file in glob.glob(os.path.join(project_path, "*.jsonl"))
        if datetime.fromtimestamp(os.path.getmtime(session_file)) >= cutoff
    ]
    sub_sessions = [
        session_file
        for session_file in glob.glob(os.path.join(project_path, "*/subagents/*.jsonl"))
        if datetime.fromtimestamp(os.path.getmtime(session_file)) >= cutoff
    ]
    return main_sessions, sub_sessions


def is_meta_session_file(session_file, load_session_entries_fn, extract_text_content_fn, max_user_messages=5):
    """Detect transcripts created by the report/enrichment process itself."""
    try:
        raw_entries = load_session_entries_fn(session_file)
    except OSError:
        return False

    inspected_users = 0
    for entry in raw_entries:
        if entry.get("type") != "user":
            continue
        content = extract_text_content_fn(entry.get("message", {}))
        if any(marker in content for marker in META_SESSION_MARKERS):
            return True
        inspected_users += 1
        if inspected_users >= max_user_messages:
            break
    return False


def has_meaningful_session_activity(session_meta):
    """Allow short sessions through when they still show real work."""
    if session_meta.get("input_tokens", 0) or session_meta.get("output_tokens", 0):
        return True
    if session_meta.get("tool_errors", 0):
        return True
    if session_meta.get("lines_added", 0) or session_meta.get("lines_removed", 0):
        return True
    if session_meta.get("uses_task_agent") or session_meta.get("uses_mcp"):
        return True
    if session_meta.get("uses_web_search") or session_meta.get("uses_web_fetch"):
        return True
    if sum(Counter(session_meta.get("tools", {})).values()):
        return True
    if sum(Counter(session_meta.get("skill_invocations", {})).values()):
        return True
    if sum(Counter(session_meta.get("agent_types", {})).values()):
        return True
    if sum(Counter(session_meta.get("slash_commands", {})).values()):
        return True
    return False


def is_substantive_session(session_meta):
    """Filter out obvious warmup or accidental sessions before facets/reporting."""
    if session_meta.get("user_messages", 0) >= 2:
        return True
    if session_meta.get("duration_minutes", 0) >= 1:
        return True
    return has_meaningful_session_activity(session_meta)


def is_minimal_facet_session(facets):
    """Treat warmup-only facets as non-substantive for narrative/reporting."""
    categories = list(facets.get("goal_categories", []) or [])
    return len(categories) == 1 and categories[0] == "warmup_minimal"


def merge_project_skill_usage(
    project_name,
    project_skills,
    project_commands,
    project_headless_skills,
    project_headless_commands,
    normalize_skill_name_fn,
    skill_projects,
):
    """Normalize and register skill usage across interactive and headless sessions."""
    combined = Counter()
    for counter in (project_skills, project_commands, project_headless_skills, project_headless_commands):
        for key, value in counter.items():
            clean = normalize_skill_name_fn(key)
            combined[clean] += value
            skill_projects[clean].add(project_name)
    return combined


def build_report_summary(all_data, global_metrics, cache_stats):
    """Build the top-level summary block from aggregated counters."""
    total_interactive = sum(project["interactive"] for project in all_data.values())
    total_headless = sum(project["headless"] for project in all_data.values())
    return {
        "total_projects": len(all_data),
        "total_sessions": total_interactive + total_headless,
        "total_sessions_scanned": cache_stats["sessions_scanned"],
        "total_interactive": total_interactive,
        "total_headless": total_headless,
        "total_subagents": sum(project["subagents"] for project in all_data.values()),
        "days_active": global_metrics.get("days_active", 0),
        "messages_per_day": global_metrics.get("messages_per_day", 0),
        "total_duration_hours": global_metrics.get("duration_hours", 0),
        "excluded_meta_sessions": cache_stats["meta_sessions_filtered"],
        "excluded_non_substantive_sessions": cache_stats["non_substantive_filtered"],
        "excluded_minimal_facet_sessions": cache_stats["minimal_facet_filtered"],
        "total_session_files": global_metrics["session_files"],
        "total_branches": global_metrics["branches_total"],
        "total_branches_deduped": global_metrics["branches_deduped"],
        "total_user_messages": global_metrics["user_messages"],
        "total_assistant_messages": global_metrics["assistant_messages"],
        "total_duration_minutes": global_metrics["duration_minutes"],
        "total_input_tokens": global_metrics["input_tokens"],
        "total_output_tokens": global_metrics["output_tokens"],
        "total_tool_errors": global_metrics["tool_errors"],
        "tool_error_categories": global_metrics["tool_error_categories"],
        "total_user_interruptions": global_metrics["user_interruptions"],
        "avg_user_response_seconds": global_metrics["avg_user_response_seconds"],
        "median_user_response_seconds": global_metrics.get("median_user_response_seconds", 0),
        "message_hours": list(global_metrics.get("message_hours", [])),
        "sessions_with_task_agent": global_metrics["sessions_with_task_agent"],
        "sessions_with_mcp": global_metrics["sessions_with_mcp"],
        "sessions_with_web_search": global_metrics["sessions_with_web_search"],
        "sessions_with_web_fetch": global_metrics["sessions_with_web_fetch"],
        "git_commits": global_metrics.get("git_commits", 0),
        "git_pushes": global_metrics.get("git_pushes", 0),
        "total_lines_added": global_metrics["lines_added"],
        "total_lines_removed": global_metrics["lines_removed"],
        "total_unique_files_modified": global_metrics["unique_files_modified"],
        "languages": global_metrics.get("languages", Counter()),
        "session_meta_cache_hits": cache_stats["session_meta_hits"],
        "session_meta_cache_misses": cache_stats["session_meta_misses"],
        "facets_cache_hits": cache_stats["facets_hits"],
        "facets_cache_misses": cache_stats["facets_misses"],
    }


def process_session_meta(
    session_file,
    cache_stats,
    get_session_meta_fn,
    cache_dir,
    use_cache,
    refresh_cache,
):
    """Load cached or computed session meta and update cache stats."""
    cache_stat_key = {"hit": "hits", "miss": "misses"}
    session_result, cache_state = get_session_meta_fn(
        session_file,
        cache_root=cache_dir,
        use_cache=use_cache,
        refresh_cache=refresh_cache,
    )
    cache_stats[f"session_meta_{cache_stat_key[cache_state]}"] += 1
    return session_result


def process_session_facets(
    session_file,
    session_result,
    project_name,
    cache_stats,
    get_session_facets_fn,
    cache_dir,
    use_cache,
    refresh_cache,
    insights_command,
):
    """Load cached or computed session facets and update cache stats."""
    cache_stat_key = {"hit": "hits", "miss": "misses"}
    facets, facet_cache_state = get_session_facets_fn(
        session_file,
        session_result,
        project_name=project_name,
        cache_root=cache_dir,
        use_cache=use_cache,
        refresh_cache=refresh_cache,
        insights_command=insights_command,
    )
    cache_stats[f"facets_{cache_stat_key[facet_cache_state]}"] += 1
    return facets


def register_session_usage(
    project_name,
    project_data,
    session_result,
    session_kind,
    facets,
    facet_summary,
    global_metrics,
    global_agents,
    global_runners,
    global_tools,
    agent_projects,
    tool_projects,
    usage_inventory_state,
    normalize_skill_name_fn,
    merge_metrics_fn,
    merge_facet_summary_fn,
):
    """Merge one accepted session into project/global aggregates."""
    merge_metrics_fn(project_data, session_result)
    merge_metrics_fn(global_metrics, session_result)
    merge_facet_summary_fn(facet_summary, facets)
    global_agents.update(session_result["agent_types"])
    global_runners.update(session_result["shell_runners"])
    global_tools.update(session_result["tools"])
    for agent_name in session_result["agent_types"]:
        agent_projects[agent_name].add(project_name)
    for tool_name in session_result["tools"]:
        tool_projects[tool_name].add(project_name)
    update_usage_inventory(
        state=usage_inventory_state,
        project_name=project_name,
        session_result=session_result,
        session_kind=session_kind,
        normalize_skill_name_fn=normalize_skill_name_fn,
    )


def build_session_evidence(project_name, session_file, session_result, session_kind, facets):
    """Build a compact evidence record for report-level narrative generation."""
    lines_changed = session_result.get("lines_added", 0) + session_result.get("lines_removed", 0)
    return {
        "project": project_name,
        "session_file": os.path.abspath(session_file),
        "session_kind": session_kind,
        "session_id": session_result.get("session_id"),
        "duration_minutes": session_result.get("duration_minutes", 0),
        "tokens": session_result.get("input_tokens", 0) + session_result.get("output_tokens", 0),
        "tool_errors": session_result.get("tool_errors", 0),
        "lines_changed": lines_changed,
        "top_tools": [name for name, _ in Counter(session_result.get("tools", {})).most_common(5)],
        "top_skills": [name for name, _ in Counter(session_result.get("skill_invocations", {})).most_common(5)],
        "top_agents": [name for name, _ in Counter(session_result.get("agent_types", {})).most_common(5)],
        "languages": [name for name, _ in Counter(session_result.get("languages", {})).most_common(5)],
        "underlying_goal": facets.get("underlying_goal", ""),
        "goal_categories": list(facets.get("goal_categories", []) or []),
        "outcome": facets.get("outcome", ""),
        "satisfaction": facets.get("satisfaction", ""),
        "friction_points": list(facets.get("friction_points", []) or []),
        "primary_success": facets.get("primary_success", ""),
        "brief_summary": facets.get("brief_summary", ""),
        "user_instructions_to_claude": list(session_result.get("user_instruction_snippets", []) or []),
    }


def generate_report(
    projects_dir,
    days,
    project_roots=None,
    cache_dir=None,
    use_cache=True,
    refresh_cache=False,
    insights_command=None,
    find_projects_fn=None,
    make_metrics_bucket_fn=None,
    merge_metrics_fn=None,
    finalize_metrics_fn=None,
    make_facet_summary_fn=None,
    merge_facet_summary_fn=None,
    finalize_facet_summary_fn=None,
    get_session_meta_fn=None,
    get_session_facets_fn=None,
    load_session_entries_fn=None,
    extract_text_content_fn=None,
    normalize_skill_name_fn=None,
    generate_narrative_insights_fn=None,
    generate_workflow_recommendations_fn=None,
):
    """Main aggregation pipeline with injected callbacks from the public module."""
    del project_roots

    cutoff = datetime.now() - timedelta(days=days)
    projects = find_projects_fn(projects_dir)

    all_data = {}
    global_skills = Counter()
    global_headless_skills = Counter()
    global_agents = Counter()
    global_runners = Counter()
    global_tools = Counter()
    global_metrics = make_metrics_bucket_fn()
    facet_summary = make_facet_summary_fn()
    skill_projects = defaultdict(set)
    agent_projects = defaultdict(set)
    tool_projects = defaultdict(set)
    usage_inventory_state = make_usage_inventory_state()
    session_evidence = []
    cache_stats = {
        "sessions_scanned": 0,
        "meta_sessions_filtered": 0,
        "non_substantive_filtered": 0,
        "minimal_facet_filtered": 0,
        "session_meta_hits": 0,
        "session_meta_misses": 0,
        "facets_hits": 0,
        "facets_misses": 0,
    }

    for project_name, project_path in projects.items():
        main_sessions, sub_sessions = list_recent_sessions(project_path, cutoff)
        if not main_sessions and not sub_sessions:
            continue
        cache_stats["sessions_scanned"] += len(main_sessions) + len(sub_sessions)

        project_data = {
            "interactive": 0,
            "headless": 0,
            "subagents": 0,
        }
        project_data.update(make_metrics_bucket_fn())
        project_skills = Counter()
        project_headless_skills = Counter()
        project_commands = Counter()
        project_headless_commands = Counter()

        for session_file in main_sessions:
            if is_meta_session_file(session_file, load_session_entries_fn, extract_text_content_fn):
                cache_stats["meta_sessions_filtered"] += 1
                continue

            session_result = process_session_meta(
                session_file=session_file,
                cache_stats=cache_stats,
                get_session_meta_fn=get_session_meta_fn,
                cache_dir=cache_dir,
                use_cache=use_cache,
                refresh_cache=refresh_cache,
            )
            if not is_substantive_session(session_result):
                cache_stats["non_substantive_filtered"] += 1
                continue

            facets = process_session_facets(
                session_file=session_file,
                session_result=session_result,
                project_name=project_name,
                cache_stats=cache_stats,
                get_session_facets_fn=get_session_facets_fn,
                cache_dir=cache_dir,
                use_cache=use_cache,
                refresh_cache=refresh_cache,
                insights_command=insights_command,
            )
            if is_minimal_facet_session(facets):
                cache_stats["minimal_facet_filtered"] += 1
                continue

            register_session_usage(
                project_name=project_name,
                project_data=project_data,
                session_result=session_result,
                session_kind="headless" if session_result["is_headless"] else "interactive",
                facets=facets,
                facet_summary=facet_summary,
                global_metrics=global_metrics,
                global_agents=global_agents,
                global_runners=global_runners,
                global_tools=global_tools,
                agent_projects=agent_projects,
                tool_projects=tool_projects,
                usage_inventory_state=usage_inventory_state,
                normalize_skill_name_fn=normalize_skill_name_fn,
                merge_metrics_fn=merge_metrics_fn,
                merge_facet_summary_fn=merge_facet_summary_fn,
            )
            session_evidence.append(
                build_session_evidence(
                    project_name=project_name,
                    session_file=session_file,
                    session_result=session_result,
                    session_kind="headless" if session_result["is_headless"] else "interactive",
                    facets=facets,
                )
            )

            if session_result["is_headless"]:
                project_data["headless"] += 1
                project_headless_skills.update(session_result["skill_invocations"])
                project_headless_commands.update(session_result["slash_commands"])
            else:
                project_data["interactive"] += 1
                project_skills.update(session_result["skill_invocations"])
                project_commands.update(session_result["slash_commands"])

        for session_file in sub_sessions:
            if is_meta_session_file(session_file, load_session_entries_fn, extract_text_content_fn):
                cache_stats["meta_sessions_filtered"] += 1
                continue

            session_result = process_session_meta(
                session_file=session_file,
                cache_stats=cache_stats,
                get_session_meta_fn=get_session_meta_fn,
                cache_dir=cache_dir,
                use_cache=use_cache,
                refresh_cache=refresh_cache,
            )
            if not is_substantive_session(session_result):
                cache_stats["non_substantive_filtered"] += 1
                continue

            facets = process_session_facets(
                session_file=session_file,
                session_result=session_result,
                project_name=project_name,
                cache_stats=cache_stats,
                get_session_facets_fn=get_session_facets_fn,
                cache_dir=cache_dir,
                use_cache=use_cache,
                refresh_cache=refresh_cache,
                insights_command=insights_command,
            )
            if is_minimal_facet_session(facets):
                cache_stats["minimal_facet_filtered"] += 1
                continue

            register_session_usage(
                project_name=project_name,
                project_data=project_data,
                session_result=session_result,
                session_kind="subagent",
                facets=facets,
                facet_summary=facet_summary,
                global_metrics=global_metrics,
                global_agents=global_agents,
                global_runners=global_runners,
                global_tools=global_tools,
                agent_projects=agent_projects,
                tool_projects=tool_projects,
                usage_inventory_state=usage_inventory_state,
                normalize_skill_name_fn=normalize_skill_name_fn,
                merge_metrics_fn=merge_metrics_fn,
                merge_facet_summary_fn=merge_facet_summary_fn,
            )
            session_evidence.append(
                build_session_evidence(
                    project_name=project_name,
                    session_file=session_file,
                    session_result=session_result,
                    session_kind="subagent",
                    facets=facets,
                )
            )
            project_data["subagents"] += 1

        merge_project_skill_usage(
            project_name=project_name,
            project_skills=project_skills,
            project_commands=project_commands,
            project_headless_skills=project_headless_skills,
            project_headless_commands=project_headless_commands,
            normalize_skill_name_fn=normalize_skill_name_fn,
            skill_projects=skill_projects,
        )

        global_skills.update(project_skills)
        global_skills.update(project_commands)
        global_headless_skills.update(project_headless_skills)
        global_headless_skills.update(project_headless_commands)

        if project_data["interactive"] or project_data["headless"] or project_data["subagents"]:
            finalize_metrics_fn(project_data)
            all_data[project_name] = project_data

    finalize_metrics_fn(global_metrics)
    facet_summary = finalize_facet_summary_fn(facet_summary)
    summary = build_report_summary(all_data, global_metrics, cache_stats)

    data = {
        "projects": all_data,
        "summary": summary,
        "facet_summary": facet_summary,
        "cache": cache_stats,
        "skills": global_skills,
        "headless_skills": global_headless_skills,
        "agents": global_agents,
        "runners": global_runners,
        "tools": global_tools,
        "usage_inventory": finalize_usage_inventory(usage_inventory_state),
        "session_evidence": session_evidence,
        "skill_projects": skill_projects,
        "agent_projects": agent_projects,
        "tool_projects": tool_projects,
    }
    data["narrative"] = generate_narrative_insights_fn(summary, facet_summary, data, insights_command)
    data["recommendations"] = generate_workflow_recommendations_fn(data)
    return data

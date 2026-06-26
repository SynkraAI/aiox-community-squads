#!/usr/bin/env python3
"""
Deterministic usage inventory analytics for session usage reports.
"""
from collections import Counter, defaultdict


def make_entity_bucket():
    """Factory for per-entity usage analytics."""
    return {
        "invocations": 0,
        "sessions": 0,
        "projects": set(),
        "interactive_invocations": 0,
        "headless_invocations": 0,
        "subagent_invocations": 0,
        "interactive_sessions": 0,
        "headless_sessions": 0,
        "subagent_sessions": 0,
        "sessions_with_errors": 0,
        "associated_input_tokens": 0,
        "associated_output_tokens": 0,
        "associated_tool_errors": 0,
        "associated_lines_added": 0,
        "associated_lines_removed": 0,
        "associated_files_modified": 0,
    }


def make_usage_inventory_state():
    """Create mutable inventory state."""
    return {
        "normalized_skills": defaultdict(make_entity_bucket),
        "slash_commands": defaultdict(make_entity_bucket),
        "skill_tools": defaultdict(make_entity_bucket),
        "agents": defaultdict(make_entity_bucket),
        "tools": defaultdict(make_entity_bucket),
        "runners": defaultdict(make_entity_bucket),
    }


def update_entity_bucket(bucket, project_name, session_result, session_kind, invocation_count):
    """Merge one entity occurrence into a usage bucket."""
    bucket["invocations"] += invocation_count
    bucket["sessions"] += 1
    bucket["projects"].add(project_name)
    if session_kind == "interactive":
        bucket["interactive_invocations"] += invocation_count
        bucket["interactive_sessions"] += 1
    elif session_kind == "headless":
        bucket["headless_invocations"] += invocation_count
        bucket["headless_sessions"] += 1
    elif session_kind == "subagent":
        bucket["subagent_invocations"] += invocation_count
        bucket["subagent_sessions"] += 1

    if session_result.get("tool_errors", 0) > 0:
        bucket["sessions_with_errors"] += 1

    bucket["associated_input_tokens"] += session_result.get("input_tokens", 0)
    bucket["associated_output_tokens"] += session_result.get("output_tokens", 0)
    bucket["associated_tool_errors"] += session_result.get("tool_errors", 0)
    bucket["associated_lines_added"] += session_result.get("lines_added", 0)
    bucket["associated_lines_removed"] += session_result.get("lines_removed", 0)
    bucket["associated_files_modified"] += len(session_result.get("files_modified", set()))


def register_counter_usage(state_map, counter, project_name, session_result, session_kind):
    """Register a Counter-like entity set for one session."""
    for entity_name, invocation_count in Counter(counter or {}).items():
        update_entity_bucket(
            state_map[entity_name],
            project_name=project_name,
            session_result=session_result,
            session_kind=session_kind,
            invocation_count=invocation_count,
        )


def update_usage_inventory(state, project_name, session_result, session_kind, normalize_skill_name_fn):
    """Update all inventory views for one accepted session."""
    register_counter_usage(
        state["slash_commands"],
        session_result.get("slash_commands", Counter()),
        project_name,
        session_result,
        session_kind,
    )
    register_counter_usage(
        state["skill_tools"],
        session_result.get("skill_invocations", Counter()),
        project_name,
        session_result,
        session_kind,
    )
    register_counter_usage(
        state["agents"],
        session_result.get("agent_types", Counter()),
        project_name,
        session_result,
        session_kind,
    )
    register_counter_usage(
        state["tools"],
        session_result.get("tools", Counter()),
        project_name,
        session_result,
        session_kind,
    )
    register_counter_usage(
        state["runners"],
        session_result.get("shell_runners", Counter()),
        project_name,
        session_result,
        session_kind,
    )

    normalized_counter = Counter()
    for key, value in Counter(session_result.get("slash_commands", {})).items():
        normalized_counter[normalize_skill_name_fn(key)] += value
    for key, value in Counter(session_result.get("skill_invocations", {})).items():
        normalized_counter[normalize_skill_name_fn(key)] += value
    register_counter_usage(
        state["normalized_skills"],
        normalized_counter,
        project_name,
        session_result,
        session_kind,
    )


def finalize_entity_entries(state_map):
    """Convert mutable per-entity buckets into sorted report entries."""
    entries = []
    for name, bucket in state_map.items():
        sessions = bucket["sessions"]
        associated_lines_changed = bucket["associated_lines_added"] + bucket["associated_lines_removed"]
        associated_tokens = bucket["associated_input_tokens"] + bucket["associated_output_tokens"]
        entries.append({
            "name": name,
            "invocations": bucket["invocations"],
            "sessions": sessions,
            "projects": sorted(bucket["projects"]),
            "projects_count": len(bucket["projects"]),
            "interactive_invocations": bucket["interactive_invocations"],
            "headless_invocations": bucket["headless_invocations"],
            "subagent_invocations": bucket["subagent_invocations"],
            "interactive_sessions": bucket["interactive_sessions"],
            "headless_sessions": bucket["headless_sessions"],
            "subagent_sessions": bucket["subagent_sessions"],
            "sessions_with_errors": bucket["sessions_with_errors"],
            "associated_input_tokens": bucket["associated_input_tokens"],
            "associated_output_tokens": bucket["associated_output_tokens"],
            "associated_tokens": associated_tokens,
            "associated_tool_errors": bucket["associated_tool_errors"],
            "associated_lines_added": bucket["associated_lines_added"],
            "associated_lines_removed": bucket["associated_lines_removed"],
            "associated_lines_changed": associated_lines_changed,
            "associated_files_modified": bucket["associated_files_modified"],
            "avg_invocations_per_session": round(bucket["invocations"] / sessions, 2) if sessions else 0,
            "avg_associated_tokens_per_session": round(associated_tokens / sessions, 1) if sessions else 0,
            "avg_associated_lines_changed_per_session": round(associated_lines_changed / sessions, 1) if sessions else 0,
            "error_session_rate": round(bucket["sessions_with_errors"] / sessions, 3) if sessions else 0,
        })
    return sorted(
        entries,
        key=lambda entry: (
            -entry["invocations"],
            -entry["sessions"],
            -entry["associated_lines_changed"],
            entry["name"],
        ),
    )


def top_entries(entries, key, limit=10):
    """Return the top entities by a derived key."""
    return sorted(
        entries,
        key=lambda entry: (-entry.get(key, 0), -entry.get("invocations", 0), entry.get("name", "")),
    )[:limit]


def finalize_usage_inventory(state):
    """Build a render-friendly usage inventory payload."""
    normalized_entries = finalize_entity_entries(state["normalized_skills"])
    slash_entries = finalize_entity_entries(state["slash_commands"])
    skill_tool_entries = finalize_entity_entries(state["skill_tools"])
    agent_entries = finalize_entity_entries(state["agents"])
    tool_entries = finalize_entity_entries(state["tools"])
    runner_entries = finalize_entity_entries(state["runners"])

    return {
        "summary": {
            "normalized_skills": len(normalized_entries),
            "slash_commands": len(slash_entries),
            "skill_tools": len(skill_tool_entries),
            "agents": len(agent_entries),
            "tools": len(tool_entries),
            "runners": len(runner_entries),
        },
        "normalized_skills": {
            "entries": normalized_entries,
            "top_by_usage": normalized_entries[:10],
            "top_by_impact": top_entries(normalized_entries, "associated_lines_changed"),
            "top_by_context_cost": top_entries(normalized_entries, "associated_tokens"),
            "top_by_friction": top_entries(normalized_entries, "sessions_with_errors"),
        },
        "slash_commands": {
            "entries": slash_entries,
            "top_by_usage": slash_entries[:10],
        },
        "skill_tools": {
            "entries": skill_tool_entries,
            "top_by_usage": skill_tool_entries[:10],
        },
        "agents": {
            "entries": agent_entries,
            "top_by_usage": agent_entries[:10],
            "top_by_impact": top_entries(agent_entries, "associated_lines_changed"),
            "top_by_context_cost": top_entries(agent_entries, "associated_tokens"),
            "top_by_friction": top_entries(agent_entries, "sessions_with_errors"),
        },
        "tools": {
            "entries": tool_entries,
            "top_by_usage": tool_entries[:10],
            "top_by_impact": top_entries(tool_entries, "associated_lines_changed"),
            "top_by_context_cost": top_entries(tool_entries, "associated_tokens"),
            "top_by_friction": top_entries(tool_entries, "sessions_with_errors"),
        },
        "runners": {
            "entries": runner_entries,
            "top_by_usage": runner_entries[:10],
        },
    }

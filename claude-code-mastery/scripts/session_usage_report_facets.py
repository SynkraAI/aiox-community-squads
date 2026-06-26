#!/usr/bin/env python3
"""
Facet and narrative helpers for the session usage report.

The main script injects cache and transcript helpers so its module-level
symbols remain patchable in tests.
"""
import json
import os
import shlex
import subprocess
import sys
from collections import Counter
from datetime import datetime


FACET_LIST_FIELDS = {"goal_categories", "friction_points"}
NARRATIVE_FIELDS = (
    "at_a_glance",
    "project_areas",
    "interaction_style",
    "what_works",
    "friction_analysis",
    "suggestions",
    "on_the_horizon",
    "fun_ending",
)
AT_A_GLANCE_KEYS = (
    "whats_working",
    "whats_hindering",
    "quick_wins",
    "ambitious_workflows",
)


def trim_text(value, limit):
    """Normalize arbitrary values into bounded strings."""
    text = str(value or "").strip()
    if not text:
        return ""
    return text[:limit]


def counter_to_dict(counter, limit=None):
    """Convert counters into plain dicts with optional truncation."""
    items = Counter(counter or {})
    if limit is None:
        return dict(items)
    return dict(items.most_common(limit))


def top_counter_names(counter, limit=3):
    """Return the top key names from a counter."""
    return [name for name, _ in Counter(counter or {}).most_common(limit)]


def normalize_generic_items(items, fields):
    """Normalize a list of dictionaries with field size limits."""
    normalized = []
    for item in items or []:
        if not isinstance(item, dict):
            continue
        row = {}
        for field, limit in fields.items():
            if field.endswith("[]"):
                source_field = field[:-2]
                values = normalize_string_list(item.get(source_field, []))
                row[source_field] = values[:limit]
            elif field.endswith("#int"):
                source_field = field[:-4]
                try:
                    row[source_field] = int(item.get(source_field, 0) or 0)
                except (TypeError, ValueError):
                    row[source_field] = 0
            else:
                row[field] = trim_text(item.get(field, ""), limit)
        if any(value for value in row.values()):
            normalized.append(row)
    return normalized


def normalize_at_a_glance_sections(value):
    """Normalize the 4-part executive glance structure."""
    if not isinstance(value, dict):
        return {key: "" for key in AT_A_GLANCE_KEYS}
    return {
        key: trim_text(value.get(key, ""), 900)
        for key in AT_A_GLANCE_KEYS
    }


def summarize_at_a_glance_sections(sections):
    """Collapse structured at-a-glance content into one sentence for Markdown/JSON compatibility."""
    pieces = []
    labels = {
        "whats_working": "Funcionando",
        "whats_hindering": "Atritos",
        "quick_wins": "Quick wins",
        "ambitious_workflows": "Horizonte",
    }
    for key in AT_A_GLANCE_KEYS:
        text = trim_text((sections or {}).get(key, ""), 180)
        if text:
            pieces.append(f"{labels[key]}: {text}")
    return " | ".join(pieces)


def normalize_project_area_items(items):
    """Normalize project-area cards."""
    return normalize_generic_items(
        items,
        {
            "name": 120,
            "session_count#int": 0,
            "description": 520,
        },
    )


def normalize_what_works_items(items):
    """Normalize impressive-workflow cards."""
    return normalize_generic_items(
        items,
        {
            "title": 120,
            "description": 520,
        },
    )


def normalize_friction_categories(items):
    """Normalize friction categories with examples."""
    return normalize_generic_items(
        items,
        {
            "category": 120,
            "description": 420,
            "examples[]": 4,
        },
    )


def normalize_claude_md_additions(items):
    """Normalize CLAUDE.md addition suggestions."""
    return normalize_generic_items(
        items,
        {
            "addition": 260,
            "why": 260,
            "prompt_scaffold": 180,
        },
    )


def normalize_features_to_try(items):
    """Normalize feature suggestions."""
    return normalize_generic_items(
        items,
        {
            "feature": 120,
            "one_liner": 180,
            "why_for_you": 320,
            "example_code": 420,
        },
    )


def normalize_usage_patterns(items):
    """Normalize new usage pattern cards."""
    return normalize_generic_items(
        items,
        {
            "title": 120,
            "suggestion": 220,
            "detail": 420,
            "copyable_prompt": 420,
        },
    )


def normalize_horizon_opportunities(items):
    """Normalize future opportunity cards."""
    return normalize_generic_items(
        items,
        {
            "title": 120,
            "whats_possible": 420,
            "how_to_try": 240,
            "copyable_prompt": 420,
        },
    )


def normalize_feedback_items(items):
    """Normalize team/model feedback cards."""
    return normalize_generic_items(
        items,
        {
            "title": 140,
            "detail": 420,
            "evidence": 320,
        },
    )


def normalize_fun_ending_card(value):
    """Normalize the ending card structure."""
    if not isinstance(value, dict):
        return {"headline": "", "detail": ""}
    return {
        "headline": trim_text(value.get("headline", ""), 180),
        "detail": trim_text(value.get("detail", ""), 280),
    }


def first_non_empty(*values):
    """Return the first meaningful text candidate."""
    for value in values:
        text = str(value or "").strip()
        if text:
            return text
    return ""


def format_number(value, decimals=None):
    """Format numbers using PT-BR-style separators in narrative text."""
    if isinstance(value, bool):
        return str(value)
    if value is None:
        return "0"
    if isinstance(value, int):
        return f"{value:,}".replace(",", ".")
    if isinstance(value, float):
        if decimals is None:
            decimals = 1
        text = f"{value:,.{decimals}f}"
        return text.replace(",", "_").replace(".", ",").replace("_", ".")
    return str(value)


def truncate_middle(text, max_chars):
    """Keep the beginning and end of a long text block."""
    if len(text) <= max_chars:
        return text
    marker = "\n...[TRUNCATED]...\n"
    keep_each_side = max((max_chars - len(marker)) // 2, 0)
    return f"{text[:keep_each_side]}{marker}{text[-keep_each_side:]}"


def heuristic_chunk_summary(chunk, max_chars=2000):
    """Create a compact deterministic summary for one transcript chunk."""
    lines = [line.strip() for line in chunk.splitlines() if line.strip()]
    if not lines:
        return ""

    def collect(predicate, limit):
        collected = []
        for line in lines:
            if predicate(line):
                collected.append(line)
            if len(collected) >= limit:
                break
        return collected

    summary_lines = []
    summary_lines.extend(collect(lambda line: line.startswith("session_"), 2))
    summary_lines.extend(collect(lambda line: " USER:" in line or line.startswith("[User]:"), 6))
    summary_lines.extend(collect(lambda line: "_TOOLS:" in line or line.startswith("[Tool:"), 8))
    summary_lines.extend(
        collect(
            lambda line: any(keyword in line.lower() for keyword in ("error", "failed", "interrupted", "warning")),
            6,
        )
    )
    summary_lines.extend(lines[-4:])

    deduped = []
    seen = set()
    for line in summary_lines:
        if line not in seen:
            deduped.append(line)
            seen.add(line)

    return truncate_middle("\n".join(deduped), max_chars)


def summarize_transcript_chunk(
    chunk,
    insights_command=None,
    run_insights_command_fn=None,
    max_chars=2000,
):
    """Summarize one transcript chunk, preferring an external adapter when available."""
    if insights_command and run_insights_command_fn:
        try:
            payload = {
                "mode": "summarize_chunk",
                "transcript_chunk": chunk,
            }
            response = run_insights_command_fn(insights_command, payload)
            if isinstance(response, dict):
                summary_text = str(
                    response.get("summary")
                    or response.get("chunk_summary")
                    or response.get("text")
                    or ""
                ).strip()
                if summary_text:
                    return truncate_middle(summary_text, max_chars)
        except Exception:
            pass
    return heuristic_chunk_summary(chunk, max_chars=max_chars)


def summarize_tool_use(tool_name, tool_input):
    """Compact textual summary of a tool_use block for facet enrichment."""
    details = []
    if tool_name == "Skill":
        details.append(f"skill={tool_input.get('skill', 'unknown')}")
    elif tool_name == "Agent":
        details.append(f"subagent_type={tool_input.get('subagent_type', 'general-purpose')}")
    elif tool_name == "Bash":
        command = str(tool_input.get("command", "")).strip()
        if command:
            details.append(f"command={command[:120]}")
    else:
        for field in ("file_path", "url", "query"):
            value = tool_input.get(field)
            if isinstance(value, str) and value:
                details.append(f"{field}={value[:120]}")
    if details:
        return f"{tool_name} ({', '.join(details)})"
    return str(tool_name or "unknown")


def build_transcript_excerpt(
    session_file,
    load_session_entries_fn,
    select_session_branch_fn,
    extract_text_content_fn,
    max_chars=30000,
    insights_command=None,
    run_insights_command_fn=None,
):
    """Build a compact transcript for optional LLM insight extraction."""
    raw_entries = load_session_entries_fn(session_file)
    dominant_session_id, selected_branch, _ = select_session_branch_fn(raw_entries)
    lines = [f"session_file: {os.path.abspath(session_file)}"]
    if dominant_session_id:
        lines.append(f"session_id: {dominant_session_id}")

    for entry in selected_branch:
        entry_type = str(entry.get("type", "unknown")).upper()
        timestamp = entry.get("timestamp") or "unknown"
        message = entry.get("message", {})
        text = extract_text_content_fn(message).strip()
        if text:
            lines.append(f"{timestamp} {entry_type}: {text}")

        if isinstance(message, dict):
            content = message.get("content", [])
            if isinstance(content, list):
                tool_summaries = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        tool_summaries.append(
                            summarize_tool_use(block.get("name", ""), block.get("input", {}) or {})
                        )
                if tool_summaries:
                    lines.append(f"{timestamp} {entry_type}_TOOLS: {'; '.join(tool_summaries)}")

    full_transcript = "\n".join(lines)
    if len(full_transcript) <= 30000:
        return full_transcript

    chunk_size = 25000
    chunks = [
        full_transcript[index:index + chunk_size]
        for index in range(0, len(full_transcript), chunk_size)
    ]
    summaries = [
        summarize_transcript_chunk(
            chunk,
            insights_command=insights_command,
            run_insights_command_fn=run_insights_command_fn,
        )
        for chunk in chunks
    ]
    header = [
        f"session_file: {os.path.abspath(session_file)}",
        f"session_id: {dominant_session_id or 'unknown'}",
        f"[long transcript summarized in {len(chunks)} chunks]",
        "",
    ]
    return truncate_middle("\n".join(header + summaries), max_chars)


def is_warmup_minimal_session(session_meta):
    """Identify sessions that look like cache warmup or trivial setup chatter."""
    lines_changed = session_meta.get("lines_added", 0) + session_meta.get("lines_removed", 0)
    tool_count = sum(Counter(session_meta.get("tools", {})).values())
    skill_count = sum(Counter(session_meta.get("skill_invocations", {})).values())
    agent_count = sum(Counter(session_meta.get("agent_types", {})).values())
    slash_count = sum(Counter(session_meta.get("slash_commands", {})).values())
    token_count = session_meta.get("input_tokens", 0) + session_meta.get("output_tokens", 0)

    if session_meta.get("tool_errors", 0) > 0 or lines_changed > 0:
        return False
    if session_meta.get("uses_task_agent") or session_meta.get("uses_mcp"):
        return False
    if session_meta.get("uses_web_search") or session_meta.get("uses_web_fetch"):
        return False
    if tool_count or skill_count or agent_count or slash_count:
        return False

    return (
        session_meta.get("user_messages", 0) <= 2
        and session_meta.get("assistant_messages", 0) <= 2
        and session_meta.get("duration_minutes", 0) < 1
        and token_count < 300
    )


def sanitize_meta_for_insights(session_meta):
    """Reduce session meta into a compact JSON payload for insight extractors."""
    response_times = session_meta.get("user_response_times", [])
    return {
        "is_headless": session_meta.get("is_headless", False),
        "session_id": session_meta.get("session_id"),
        "branches_total": session_meta.get("branches_total", 0),
        "branches_deduped": session_meta.get("branches_deduped", 0),
        "user_messages": session_meta.get("user_messages", 0),
        "assistant_messages": session_meta.get("assistant_messages", 0),
        "duration_minutes": session_meta.get("duration_minutes", 0),
        "input_tokens": session_meta.get("input_tokens", 0),
        "output_tokens": session_meta.get("output_tokens", 0),
        "tool_errors": session_meta.get("tool_errors", 0),
        "tool_error_categories": dict(session_meta.get("tool_error_categories", Counter())),
        "user_interruptions": session_meta.get("user_interruptions", 0),
        "avg_user_response_seconds": round(sum(response_times) / len(response_times), 1) if response_times else 0,
        "uses_task_agent": session_meta.get("uses_task_agent", False),
        "uses_mcp": session_meta.get("uses_mcp", False),
        "uses_web_search": session_meta.get("uses_web_search", False),
        "uses_web_fetch": session_meta.get("uses_web_fetch", False),
        "git_commits": session_meta.get("git_commits", 0),
        "git_pushes": session_meta.get("git_pushes", 0),
        "lines_added": session_meta.get("lines_added", 0),
        "lines_removed": session_meta.get("lines_removed", 0),
        "message_hours": list(session_meta.get("message_hours", [])[:24]),
        "tools": dict(session_meta.get("tools", Counter()).most_common(10)),
        "skills": dict(session_meta.get("skill_invocations", Counter()).most_common(10)),
        "agents": dict(session_meta.get("agent_types", Counter()).most_common(10)),
        "languages": dict(session_meta.get("languages", Counter()).most_common(10)),
    }


def parse_json_object(text):
    """Parse JSON even when surrounded by incidental text."""
    if not isinstance(text, str) or not text.strip():
        return {}
    stripped = text.strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(stripped[start:end + 1])
        raise


def run_insights_command(command, payload, timeout_seconds=60):
    """Invoke an external insights adapter that reads JSON from stdin."""
    completed = subprocess.run(
        shlex.split(command),
        input=json.dumps(payload, ensure_ascii=False),
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )
    if completed.returncode != 0:
        stderr_text = (completed.stderr or completed.stdout or "").strip()
        raise RuntimeError(stderr_text or f"Insights command failed with exit code {completed.returncode}")
    return parse_json_object(completed.stdout)


def infer_basic_facets(session_meta):
    """Generate deterministic facets even without any LLM command."""
    if is_warmup_minimal_session(session_meta):
        return {
            "underlying_goal": "Sessão curta de warmup ou checagem mínima",
            "goal_categories": ["warmup_minimal"],
            "outcome": "unknown",
            "satisfaction": "unknown",
            "friction_points": [],
            "primary_success": "Sem trabalho substantivo capturado",
            "brief_summary": "Sessão curta sem atividade material suficiente para análise detalhada.",
            "source": "heuristic",
        }

    goal_categories = []
    tools = session_meta.get("tools", Counter())
    skills = session_meta.get("skill_invocations", Counter())

    if tools.get("Edit") or tools.get("Write"):
        goal_categories.append("coding")
    if session_meta.get("uses_web_search") or session_meta.get("uses_web_fetch"):
        goal_categories.append("research")
    if session_meta.get("uses_task_agent") or tools.get("Agent"):
        goal_categories.append("orchestration")
    if session_meta.get("is_headless"):
        goal_categories.append("automation")
    if any(skill in {"deploy", "commit", "release"} for skill in skills):
        goal_categories.append("delivery")
    if not goal_categories:
        goal_categories.append("general")

    friction_points = [category.lower() for category in session_meta.get("tool_error_categories", Counter())]
    if session_meta.get("user_interruptions"):
        friction_points.append("user interruptions")

    changed_lines = session_meta.get("lines_added", 0) + session_meta.get("lines_removed", 0)
    tool_errors = session_meta.get("tool_errors", 0)
    if changed_lines and tool_errors:
        outcome = "partial"
    elif changed_lines:
        outcome = "implemented"
    elif tool_errors:
        outcome = "blocked"
    elif session_meta.get("uses_web_search") or session_meta.get("uses_web_fetch"):
        outcome = "researched"
    else:
        outcome = "unknown"

    if tool_errors > 1 or session_meta.get("user_interruptions", 0) > 1:
        satisfaction = "low"
    elif tool_errors == 0 and session_meta.get("user_interruptions", 0) == 0:
        satisfaction = "high"
    else:
        satisfaction = "medium"

    top_tool = tools.most_common(1)[0][0] if tools else "conversation"
    primary_success = f"Uso dominante de {top_tool}" if tools else "Sessão centrada em troca conversacional"

    return {
        "underlying_goal": f"Sessão focada em {', '.join(goal_categories)}",
        "goal_categories": goal_categories[:5],
        "outcome": outcome,
        "satisfaction": satisfaction,
        "friction_points": friction_points[:5],
        "primary_success": primary_success,
        "brief_summary": (
            f"{session_meta.get('user_messages', 0)} mensagens do usuário, "
            f"{changed_lines} linhas alteradas, "
            f"{tool_errors} erros de tool."
        ),
        "source": "heuristic",
    }


def normalize_string_list(values):
    """Normalize list fields used by facets."""
    result = []
    for value in values or []:
        text = str(value).strip()
        if text and text not in result:
            result.append(text[:120])
    return result


def normalize_facets(facets):
    """Normalize arbitrary facet payloads into the report schema."""
    normalized = {
        "underlying_goal": "",
        "goal_categories": [],
        "outcome": "unknown",
        "satisfaction": "unknown",
        "friction_points": [],
        "primary_success": "",
        "brief_summary": "",
        "source": "heuristic",
    }

    if not isinstance(facets, dict):
        return normalized

    normalized["underlying_goal"] = str(facets.get("underlying_goal", "")).strip()[:240]
    normalized["goal_categories"] = normalize_string_list(facets.get("goal_categories", []))[:5]
    normalized["outcome"] = str(facets.get("outcome", "unknown")).strip().lower()[:40] or "unknown"
    normalized["satisfaction"] = str(facets.get("satisfaction", "unknown")).strip().lower()[:40] or "unknown"
    normalized["friction_points"] = normalize_string_list(facets.get("friction_points", []))[:5]
    normalized["primary_success"] = str(facets.get("primary_success", "")).strip()[:240]
    normalized["brief_summary"] = str(facets.get("brief_summary", "")).strip()[:360]
    normalized["source"] = str(facets.get("source", "heuristic")).strip()[:40] or "heuristic"
    return normalized


def merge_facets(base_facets, enriched_facets):
    """Overlay non-empty facet fields onto the deterministic baseline."""
    merged = dict(base_facets)
    for field, value in enriched_facets.items():
        if field in FACET_LIST_FIELDS:
            if value:
                merged[field] = value
        elif value not in ("", None):
            merged[field] = value
    return normalize_facets(merged)


def get_session_facets(
    session_file,
    session_meta,
    cache_root,
    use_cache,
    refresh_cache,
    insights_command,
    project_name,
    default_usage_data_dir,
    file_fingerprint_fn,
    get_cache_paths_fn,
    cache_key_for_file_fn,
    read_cached_json_fn,
    write_cached_json_fn,
    build_transcript_excerpt_fn,
    sanitize_meta_for_insights_fn,
    run_insights_command_fn,
):
    """Load or compute per-session facets, optionally enriched by an external command."""
    fingerprint = file_fingerprint_fn(session_file)
    cache_paths = get_cache_paths_fn(cache_root, default_usage_data_dir)
    cache_file = os.path.join(cache_paths["facets"], f"{cache_key_for_file_fn(session_file)}.json")

    if use_cache and not refresh_cache:
        cached = read_cached_json_fn(cache_file)
        if cached and cached.get("fingerprint") == fingerprint:
            return normalize_facets(cached.get("facets", {})), "hit"

    facets = infer_basic_facets(session_meta)
    if insights_command:
        try:
            transcript = build_transcript_excerpt_fn(
                session_file,
                insights_command=insights_command,
                run_insights_command_fn=run_insights_command_fn,
            )
            enriched = run_insights_command_fn(
                insights_command,
                {
                    "mode": "facet",
                    "project_name": project_name,
                    "session_file": os.path.abspath(session_file),
                    "session_meta": sanitize_meta_for_insights_fn(session_meta),
                    "transcript": transcript,
                },
            )
            facets = merge_facets(facets, normalize_facets({**enriched, "source": "llm"}))
        except Exception as exc:
            print(f"  Warning: facet enrichment failed for {session_file}: {exc}", file=sys.stderr)

    normalized = normalize_facets(facets)

    if use_cache:
        write_cached_json_fn(
            cache_file,
            {
                "version": 1,
                "session_file": os.path.abspath(session_file),
                "fingerprint": fingerprint,
                "generated_at": datetime.now().isoformat(),
                "facets": normalized,
            },
        )

    return normalized, "miss"


def make_facet_summary():
    """Aggregate structure for per-session facets."""
    return {
        "sessions_with_facets": 0,
        "sources": Counter(),
        "goal_categories": Counter(),
        "outcomes": Counter(),
        "satisfaction": Counter(),
        "friction_points": Counter(),
    }


def merge_facet_summary(bucket, facets):
    """Merge one facet object into the aggregate summary."""
    if not facets:
        return
    bucket["sessions_with_facets"] += 1
    bucket["sources"][facets.get("source", "heuristic")] += 1
    bucket["outcomes"][facets.get("outcome", "unknown")] += 1
    bucket["satisfaction"][facets.get("satisfaction", "unknown")] += 1
    bucket["goal_categories"].update(facets.get("goal_categories", []))
    bucket["friction_points"].update(facets.get("friction_points", []))


def finalize_facet_summary(bucket):
    """Make facet aggregates JSON/render friendly."""
    return {
        "sessions_with_facets": bucket.get("sessions_with_facets", 0),
        "sources": bucket.get("sources", Counter()),
        "goal_categories": bucket.get("goal_categories", Counter()),
        "outcomes": bucket.get("outcomes", Counter()),
        "satisfaction": bucket.get("satisfaction", Counter()),
        "friction_points": bucket.get("friction_points", Counter()),
    }


def build_default_project_areas(data):
    """Create deterministic project-area cards when no LLM is available."""
    areas = []
    for name, project in sorted(
        (data.get("projects") or {}).items(),
        key=lambda item: -(
            item[1].get("interactive", 0)
            + item[1].get("headless", 0)
            + item[1].get("subagents", 0)
        ),
    )[:5]:
        session_count = (
            project.get("interactive", 0)
            + project.get("headless", 0)
            + project.get("subagents", 0)
        )
        description = (
            f"{format_number(session_count)} sessões no período, "
            f"{format_number(project.get('input_tokens', 0))}/{format_number(project.get('output_tokens', 0))} tokens "
            f"e +{format_number(project.get('lines_added', 0))}/-{format_number(project.get('lines_removed', 0))} linhas."
        )
        areas.append(
            {
                "name": name,
                "session_count": session_count,
                "description": description,
            }
        )
    return areas


def build_default_narrative(summary, facet_summary, data=None):
    """Create deterministic narrative blocks from aggregates."""
    data = data or {}
    top_goals = ", ".join(name for name, _ in facet_summary.get("goal_categories", Counter()).most_common(3)) or "general"
    top_outcomes = ", ".join(name for name, _ in facet_summary.get("outcomes", Counter()).most_common(3)) or "unknown"
    top_friction = ", ".join(name for name, _ in facet_summary.get("friction_points", Counter()).most_common(3)) or "sem atritos relevantes"
    top_satisfaction = ", ".join(name for name, _ in facet_summary.get("satisfaction", Counter()).most_common(2)) or "unknown"
    top_skills = top_counter_names(data.get("skills", Counter()), 3)
    top_tools = top_counter_names(data.get("tools", Counter()), 3)
    top_agents = top_counter_names(data.get("agents", Counter()), 2)

    at_a_glance_sections = {
        "whats_working": (
            f"Você concentrou o período em {top_goals} com sinais claros de execução material: "
            f"+{format_number(summary.get('total_lines_added', 0))}/-{format_number(summary.get('total_lines_removed', 0))} linhas "
            f"e {format_number(summary.get('total_unique_files_modified', 0))} arquivos únicos alterados."
        ),
        "whats_hindering": (
            f"Os principais atritos ainda se repetem em {top_friction}, com "
            f"{format_number(summary.get('total_tool_errors', 0))} erros de tool e "
            f"{format_number(summary.get('total_user_interruptions', 0))} interrupções."
        ),
        "quick_wins": (
            "Codificar instruções recorrentes em CLAUDE.md, hooks e skills tende a reduzir repetição de contexto "
            "e capturar padrões já estáveis no histórico."
        ),
        "ambitious_workflows": (
            "Os sinais atuais já sustentam workflows mais autônomos com agents, validação contínua e rotinas "
            "headless, principalmente nas frentes com uso recorrente de skills e scripts."
        ),
    }

    project_area_items = build_default_project_areas(data)
    what_works_items = [
        {
            "title": "Execução com volume real",
            "description": (
                f"Outcomes predominantes: {top_outcomes}. O histórico mostra trabalho concreto em múltiplos arquivos "
                f"e branches deduplicadas ({format_number(summary.get('total_branches_deduped', 0))})."
            ),
        },
        {
            "title": "Uso recorrente de ferramentas",
            "description": (
                f"Skills dominantes: {', '.join(top_skills) or 'n/a'}. "
                f"Tools mais acionadas: {', '.join(top_tools) or 'n/a'}."
            ),
        },
        {
            "title": "Orquestração crescente",
            "description": (
                f"Agents mais visíveis: {', '.join(top_agents) or 'n/a'}. "
                f"Sessões com task agents: {format_number(summary.get('sessions_with_task_agent', 0))}."
            ),
        },
    ]

    friction_categories = [
        {
            "category": "Erros de tool recorrentes",
            "description": (
                f"{format_number(summary.get('total_tool_errors', 0))} erros no período, com destaque para {top_friction}."
            ),
            "examples": [
                f"Categorias observadas: {top_friction}.",
                "Vale codificar guardrails e convenções persistentes nas rotinas mais repetidas.",
            ],
        },
        {
            "category": "Custo de contexto manual",
            "description": (
                "Quando instruções de workflow não ficam persistidas, o sistema depende de correções repetidas em sessão."
            ),
            "examples": [
                "Prompts e convenções recorrentes podem virar skill, hook ou seção dedicada de CLAUDE.md.",
                "Isso reduz atrito sem sacrificar o inventário determinístico do report.",
            ],
        },
    ]

    claude_md_additions = [
        {
            "addition": "Registrar convenções de merge, formato de saída e validações obrigatórias nas áreas mais recorrentes.",
            "why": "O histórico mostra repetição de padrões operacionais que podem ser externalizados para reduzir correções em sessão.",
            "prompt_scaffold": "Adicionar em CLAUDE.md sob uma seção `## Regras Operacionais`.",
        }
    ]
    features_to_try = [
        {
            "feature": "Custom Skills",
            "one_liner": "Empacotar workflows recorrentes em comandos reutilizáveis.",
            "why_for_you": "O inventário mostra skills e slash commands recorrentes o suficiente para consolidar padrões e economizar contexto.",
            "example_code": "Criar `.claude/skills/commit/SKILL.md` ou `.claude/skills/review/SKILL.md` com os passos obrigatórios.",
        },
        {
            "feature": "Hooks",
            "one_liner": "Executar validações automaticamente após eventos críticos.",
            "why_for_you": "Ajuda a capturar erros repetitivos antes que eles virem mais uma rodada manual de correção.",
            "example_code": "Adicionar hooks para lint/typecheck/testes nas rotinas onde o histórico mostra mais fricção.",
        },
    ]
    usage_patterns = [
        {
            "title": "Fechar loops com menos contexto",
            "suggestion": "Transformar instruções repetidas em assets persistentes.",
            "detail": (
                "O report já aponta quais skills, commands, tools e atritos mais se repetem. "
                "Isso permite mover regras estáveis para CLAUDE.md, skills e hooks."
            ),
            "copyable_prompt": "Revise minhas 3 instruções mais repetidas e transforme isso em uma proposta objetiva de CLAUDE.md + hooks + skills.",
        }
    ]
    horizon_opportunities = [
        {
            "title": "Loops mais autônomos",
            "whats_possible": (
                "As frentes com mais uso de agents, runners e edição real já parecem candidatas para ciclos fechados de validação, "
                "checagem e correção automática."
            ),
            "how_to_try": "Comece pelas rotinas com mais fricção operacional e mais custo de contexto.",
            "copyable_prompt": "Desenhe um workflow autônomo para a rotina mais repetida do meu histórico, incluindo validação, correção e checkpoint final.",
        }
    ]

    return {
        "source": "deterministic",
        "at_a_glance": summarize_at_a_glance_sections(at_a_glance_sections),
        "at_a_glance_sections": at_a_glance_sections,
        "project_areas": f"Temas dominantes: {top_goals}.",
        "project_area_items": project_area_items,
        "interaction_style": (
            f"Distribuição de satisfação observada: {top_satisfaction}. "
            f"Tempo médio de resposta do usuário: {format_number(summary.get('avg_user_response_seconds', 0))}s."
        ),
        "what_works": (
            f"Outcomes predominantes: {top_outcomes}. "
            f"Linhas alteradas no período: +{format_number(summary.get('total_lines_added', 0))}/-{format_number(summary.get('total_lines_removed', 0))}."
        ),
        "what_works_items": what_works_items,
        "friction_analysis": f"Atritos mais frequentes: {top_friction}.",
        "friction_categories": friction_categories,
        "suggestions": (
            "Priorizar sessões com maior incidência de erros e interrupções, "
            "e capturar prompts/skills recorrentes nas categorias dominantes."
        ),
        "claude_md_additions": claude_md_additions,
        "features_to_try": features_to_try,
        "usage_patterns": usage_patterns,
        "on_the_horizon": (
            "Há espaço para empurrar mais workflows longos e paralelos nas categorias dominantes, "
            "principalmente onde já existe uso recorrente de skills, scripts e subagents."
        ),
        "horizon_opportunities": horizon_opportunities,
        "feedback": {
            "cc_team_improvements": [],
            "model_behavior_improvements": [],
        },
        "fun_ending": (
            "O histórico mostra uma operação claramente orientada a volume e execução contínua, "
            "com bastante trabalho real acumulado em poucas frentes principais."
        ),
        "fun_ending_card": {
            "headline": "O histórico mostra uma operação orientada a execução contínua.",
            "detail": "Mesmo no fallback determinístico, a assinatura dominante é volume com trabalho material recorrente.",
        },
    }


def normalize_narrative(payload):
    """Normalize narrative sections into the report schema."""
    narrative = {
        "source": "deterministic",
        "at_a_glance_sections": {key: "" for key in AT_A_GLANCE_KEYS},
        "project_area_items": [],
        "what_works_items": [],
        "friction_categories": [],
        "claude_md_additions": [],
        "features_to_try": [],
        "usage_patterns": [],
        "horizon_opportunities": [],
        "feedback": {
            "cc_team_improvements": [],
            "model_behavior_improvements": [],
        },
        "fun_ending_card": {"headline": "", "detail": ""},
    }
    for field in NARRATIVE_FIELDS:
        narrative[field] = ""
    if not isinstance(payload, dict):
        return narrative
    narrative["source"] = str(payload.get("source", "deterministic")).strip()[:40] or "deterministic"
    at_a_glance_sections = normalize_at_a_glance_sections(
        payload.get("at_a_glance_sections") or payload.get("at_a_glance")
    )
    narrative["at_a_glance_sections"] = at_a_glance_sections
    narrative["project_area_items"] = normalize_project_area_items(payload.get("project_area_items", []))
    narrative["what_works_items"] = normalize_what_works_items(payload.get("what_works_items", []))
    narrative["friction_categories"] = normalize_friction_categories(payload.get("friction_categories", []))
    narrative["claude_md_additions"] = normalize_claude_md_additions(payload.get("claude_md_additions", []))
    narrative["features_to_try"] = normalize_features_to_try(payload.get("features_to_try", []))
    narrative["usage_patterns"] = normalize_usage_patterns(payload.get("usage_patterns", []))
    narrative["horizon_opportunities"] = normalize_horizon_opportunities(payload.get("horizon_opportunities", []))
    feedback = payload.get("feedback", {}) if isinstance(payload.get("feedback"), dict) else {}
    narrative["feedback"] = {
        "cc_team_improvements": normalize_feedback_items(
            feedback.get("cc_team_improvements", payload.get("cc_team_improvements", []))
        ),
        "model_behavior_improvements": normalize_feedback_items(
            feedback.get("model_behavior_improvements", payload.get("model_behavior_improvements", []))
        ),
    }
    narrative["fun_ending_card"] = normalize_fun_ending_card(payload.get("fun_ending_card") or payload.get("fun_ending"))
    for field in NARRATIVE_FIELDS:
        narrative[field] = str(payload.get(field, "")).strip()

    if not narrative["at_a_glance"]:
        narrative["at_a_glance"] = summarize_at_a_glance_sections(at_a_glance_sections)
    if not narrative["project_areas"] and narrative["project_area_items"]:
        narrative["project_areas"] = "; ".join(
            f"{item.get('name')}: {item.get('description')}"
            for item in narrative["project_area_items"][:3]
        )
    if not narrative["what_works"] and narrative["what_works_items"]:
        narrative["what_works"] = "; ".join(
            f"{item.get('title')}: {item.get('description')}"
            for item in narrative["what_works_items"][:3]
        )
    if not narrative["friction_analysis"] and narrative["friction_categories"]:
        narrative["friction_analysis"] = "; ".join(
            f"{item.get('category')}: {item.get('description')}"
            for item in narrative["friction_categories"][:3]
        )
    if not narrative["suggestions"]:
        narrative["suggestions"] = first_non_empty(
            " | ".join(
                f"{item.get('feature')}: {item.get('one_liner')}"
                for item in narrative["features_to_try"][:3]
            ),
            " | ".join(
                f"{item.get('title')}: {item.get('suggestion')}"
                for item in narrative["usage_patterns"][:3]
            ),
        )
    if not narrative["on_the_horizon"] and narrative["horizon_opportunities"]:
        narrative["on_the_horizon"] = "; ".join(
            f"{item.get('title')}: {item.get('whats_possible')}"
            for item in narrative["horizon_opportunities"][:3]
        )
    if not narrative["fun_ending"]:
        narrative["fun_ending"] = first_non_empty(
            narrative["fun_ending_card"].get("headline"),
            narrative["fun_ending_card"].get("detail"),
        )
    return narrative


def build_narrative_payload(summary, facet_summary, data, normalize_skill_name_fn):
    """Compact aggregate payload for optional narrative generation."""
    normalized_skills = Counter()
    for key, value in data.get("skills", Counter()).items():
        normalized_skills[normalize_skill_name_fn(key)] += value
    for key, value in data.get("headless_skills", Counter()).items():
        normalized_skills[normalize_skill_name_fn(key)] += value

    projects = []
    for name, project in sorted(
        (data.get("projects") or {}).items(),
        key=lambda item: -(
            item[1].get("interactive", 0)
            + item[1].get("headless", 0)
            + item[1].get("subagents", 0)
        ),
    )[:8]:
        projects.append(
            {
                "name": name,
                "sessions": (
                    project.get("interactive", 0)
                    + project.get("headless", 0)
                    + project.get("subagents", 0)
                ),
                "input_tokens": project.get("input_tokens", 0),
                "output_tokens": project.get("output_tokens", 0),
                "tool_errors": project.get("tool_errors", 0),
                "lines_added": project.get("lines_added", 0),
                "lines_removed": project.get("lines_removed", 0),
            }
        )

    session_evidence = data.get("session_evidence", []) or []
    top_session_summaries = [
        {
            "project": item.get("project"),
            "session_kind": item.get("session_kind"),
            "brief_summary": item.get("brief_summary"),
            "underlying_goal": item.get("underlying_goal"),
            "goal_categories": item.get("goal_categories", []),
            "outcome": item.get("outcome"),
            "satisfaction": item.get("satisfaction"),
            "tool_errors": item.get("tool_errors", 0),
            "lines_changed": item.get("lines_changed", 0),
            "tools": item.get("top_tools", []),
            "skills": item.get("top_skills", []),
            "agents": item.get("top_agents", []),
            "languages": item.get("languages", []),
        }
        for item in sorted(
            session_evidence,
            key=lambda row: (
                row.get("tool_errors", 0),
                row.get("lines_changed", 0),
                row.get("tokens", 0),
            ),
            reverse=True,
        )[:18]
    ]
    friction_details = [
        {
            "project": item.get("project"),
            "summary": item.get("brief_summary"),
            "friction_points": item.get("friction_points", []),
            "tool_errors": item.get("tool_errors", 0),
        }
        for item in session_evidence
        if item.get("friction_points") or item.get("tool_errors", 0) > 0
    ][:16]
    user_instructions = []
    seen_instruction = set()
    for item in session_evidence:
        for instruction in item.get("user_instructions_to_claude", []):
            clean = trim_text(instruction, 220)
            if clean and clean not in seen_instruction:
                seen_instruction.add(clean)
                user_instructions.append(clean)
            if len(user_instructions) >= 20:
                break
        if len(user_instructions) >= 20:
            break

    return {
        "mode": "insight_sections",
        "summary": {key: dict(value) if isinstance(value, Counter) else value for key, value in summary.items()},
        "facet_summary": {key: dict(value) if isinstance(value, Counter) else value for key, value in facet_summary.items()},
        "top_skills": dict(normalized_skills.most_common(10)),
        "top_tools": dict(data.get("tools", Counter()).most_common(10)),
        "top_agents": dict(data.get("agents", Counter()).most_common(10)),
        "top_runners": dict(data.get("runners", Counter()).most_common(10)),
        "top_projects": projects,
        "usage_inventory": data.get("usage_inventory", {}),
        "session_summaries": top_session_summaries,
        "friction_details": friction_details,
        "user_instructions_to_claude": user_instructions,
    }


def generate_narrative_insights(
    summary,
    facet_summary,
    data,
    insights_command,
    run_insights_command_fn,
    normalize_skill_name_fn,
):
    """Generate optional report-level narrative, with deterministic fallback."""
    narrative = normalize_narrative(build_default_narrative(summary, facet_summary, data))
    if not insights_command:
        return narrative

    narrative_payload = build_narrative_payload(summary, facet_summary, data, normalize_skill_name_fn)
    try:
        enriched = run_insights_command_fn(insights_command, narrative_payload)
        return normalize_narrative({**narrative, **enriched, "source": "llm"})
    except Exception as exc:
        if "unsupported_mode" in str(exc):
            try:
                legacy_payload = dict(narrative_payload)
                legacy_payload["mode"] = "narrative"
                enriched = run_insights_command_fn(insights_command, legacy_payload)
                return normalize_narrative({**narrative, **enriched, "source": "llm"})
            except Exception as legacy_exc:
                print(f"  Warning: narrative enrichment failed: {legacy_exc}", file=sys.stderr)
                return narrative
        print(f"  Warning: narrative enrichment failed: {exc}", file=sys.stderr)
        return narrative

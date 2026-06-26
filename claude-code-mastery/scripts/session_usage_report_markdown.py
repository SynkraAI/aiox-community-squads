#!/usr/bin/env python3
"""
Markdown renderer for the session usage report.
"""
from collections import Counter, defaultdict
from datetime import datetime


DEFAULT_NARRATIVE_FIELDS = (
    "at_a_glance",
    "project_areas",
    "interaction_style",
    "what_works",
    "friction_analysis",
    "suggestions",
    "on_the_horizon",
    "fun_ending",
)


def top_usage_entries(data, bucket, key="top_by_usage", limit=8):
    """Return usage-inventory entries for renderer sections."""
    usage_inventory = data.get("usage_inventory", {})
    entries = usage_inventory.get(bucket, {}).get(key, []) or []
    return entries[:limit]


def format_number(value, decimals=None):
    """Format numbers using PT-BR-style separators for rendered reports."""
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


def format_markdown(
    data,
    days,
    project_roots=None,
    discover_inventory_fn=None,
    get_recent_commits_fn=None,
    normalize_skill_name_fn=None,
    narrative_fields=None,
):
    """Render the report as Markdown."""
    normalize_skill_name_fn = normalize_skill_name_fn or (lambda key: str(key or "").lstrip("/"))
    narrative_fields = tuple(narrative_fields or DEFAULT_NARRATIVE_FIELDS)

    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    summary = data.get("summary", {})
    facet_summary = data.get("facet_summary", {})
    narrative = data.get("narrative", {})
    recommendations = data.get("recommendations", {})
    recommendation_summary = recommendations.get("summary", {})

    lines.append("# Claude Code Session Usage Report")
    lines.append("")
    lines.append(f"**Período:** últimos {days} dias | **Gerado em:** {now}")
    lines.append("")

    lines.append("## Resumo")
    lines.append("")
    lines.append("| Projeto | Interativas | Headless | Subagents | Date Range |")
    lines.append("|---------|------------|----------|-----------|------------|")

    total_int = summary.get("total_interactive")
    total_hl = summary.get("total_headless")
    total_sub = summary.get("total_subagents")
    if total_int is None:
        total_int = sum(project["interactive"] for project in data["projects"].values())
    if total_hl is None:
        total_hl = sum(project["headless"] for project in data["projects"].values())
    if total_sub is None:
        total_sub = sum(project["subagents"] for project in data["projects"].values())

    for name, project in sorted(data["projects"].items(), key=lambda item: -(item[1]["interactive"] + item[1]["headless"])):
        lines.append(
            f"| **{name}** | {project['interactive']} | {project['headless']} | "
            f"{project['subagents']} | {project['date_range']} |"
        )
    lines.append(f"| **TOTAL** | **{total_int}** | **{total_hl}** | **{total_sub}** | |")
    lines.append("")

    lines.append("## Métricas de Sessão")
    lines.append("")
    lines.append("| Métrica | Valor |")
    lines.append("|---------|-------|")
    lines.append(f"| Arquivos de sessão analisados | {format_number(summary.get('total_session_files', total_int + total_hl + total_sub))} |")
    lines.append(f"| Sessões escaneadas | {format_number(summary.get('total_sessions_scanned', summary.get('total_session_files', 0)))} |")
    lines.append(f"| Sessões meta excluídas | {format_number(summary.get('excluded_meta_sessions', 0))} |")
    lines.append(f"| Sessões não substantivas excluídas | {format_number(summary.get('excluded_non_substantive_sessions', 0))} |")
    lines.append(f"| Sessões warmup/minimal excluídas | {format_number(summary.get('excluded_minimal_facet_sessions', 0))} |")
    lines.append(f"| Branches detectadas | {format_number(summary.get('total_branches', 0))} |")
    lines.append(f"| Branches deduplicadas | {format_number(summary.get('total_branches_deduped', 0))} |")
    lines.append(f"| Mensagens do usuário | {format_number(summary.get('total_user_messages', 0))} |")
    lines.append(f"| Mensagens do assistant | {format_number(summary.get('total_assistant_messages', 0))} |")
    lines.append(f"| Input tokens | {format_number(summary.get('total_input_tokens', 0))} |")
    lines.append(f"| Output tokens | {format_number(summary.get('total_output_tokens', 0))} |")
    lines.append(f"| Tool errors | {format_number(summary.get('total_tool_errors', 0))} |")
    lines.append(f"| Interrupções do usuário | {format_number(summary.get('total_user_interruptions', 0))} |")
    lines.append(f"| Tempo médio de resposta do usuário (s) | {format_number(summary.get('avg_user_response_seconds', 0))} |")
    lines.append(f"| Linhas adicionadas | {format_number(summary.get('total_lines_added', 0))} |")
    lines.append(f"| Linhas removidas | {format_number(summary.get('total_lines_removed', 0))} |")
    lines.append(f"| Arquivos únicos modificados | {format_number(summary.get('total_unique_files_modified', 0))} |")
    lines.append(f"| Sessões com task agent | {format_number(summary.get('sessions_with_task_agent', 0))} |")
    lines.append(f"| Sessões com MCP | {format_number(summary.get('sessions_with_mcp', 0))} |")
    lines.append(f"| Sessões com WebSearch | {format_number(summary.get('sessions_with_web_search', 0))} |")
    lines.append(f"| Sessões com WebFetch | {format_number(summary.get('sessions_with_web_fetch', 0))} |")
    lines.append(
        f"| Cache session-meta (hit/miss) | "
        f"{format_number(summary.get('session_meta_cache_hits', 0))}/{format_number(summary.get('session_meta_cache_misses', 0))} |"
    )
    lines.append(
        f"| Cache facets (hit/miss) | "
        f"{format_number(summary.get('facets_cache_hits', 0))}/{format_number(summary.get('facets_cache_misses', 0))} |"
    )
    lines.append("")

    if data["projects"]:
        lines.append("## Atividade por Projeto")
        lines.append("")
        lines.append("| Projeto | Tokens In | Tokens Out | Tool Errors | Branches Dedup | Linhas +/- | Arquivos | Resp. méd. (s) |")
        lines.append("|---------|-----------|------------|-------------|---------------|------------|----------|----------------|")
        for name, project in sorted(
            data["projects"].items(),
            key=lambda item: -(item[1]["interactive"] + item[1]["headless"] + item[1]["subagents"]),
        ):
            lines.append(
                f"| **{name}** | {format_number(project.get('input_tokens', 0))} | {format_number(project.get('output_tokens', 0))} | "
                f"{format_number(project.get('tool_errors', 0))} | {format_number(project.get('branches_deduped', 0))} | "
                f"+{format_number(project.get('lines_added', 0))}/-{format_number(project.get('lines_removed', 0))} | {format_number(project.get('unique_files_modified', 0))} | "
                f"{format_number(project.get('avg_user_response_seconds', 0))} |"
            )
        lines.append("")

    lines.append("## Top Skills/Commands")
    lines.append("")
    lines.append("| Skill/Command | Interativas | Headless | Projetos |")
    lines.append("|--------------|-------------|----------|----------|")

    combined = Counter()
    combined_interactive = Counter()
    combined_headless = Counter()
    combined_projects = defaultdict(set)

    for key, value in data["skills"].items():
        normalized = normalize_skill_name_fn(key)
        combined[normalized] += value
        combined_interactive[normalized] += value
    for key, value in data["headless_skills"].items():
        normalized = normalize_skill_name_fn(key)
        combined[normalized] += value
        combined_headless[normalized] += value
    for key, projects in data["skill_projects"].items():
        normalized = normalize_skill_name_fn(key)
        combined_projects[normalized].update(projects)

    for skill, _ in combined.most_common(30):
        interactive = combined_interactive.get(skill, 0)
        headless = combined_headless.get(skill, 0)
        projects = ", ".join(sorted(combined_projects.get(skill, set())))
        lines.append(f"| `{skill}` | {format_number(interactive)} | {format_number(headless)} | {projects} |")
    lines.append("")

    lines.append("## Top Tools")
    lines.append("")
    lines.append("| Tool | Invocações | Projetos |")
    lines.append("|------|-----------|----------|")
    for tool_name, count in data.get("tools", Counter()).most_common(20):
        projects = ", ".join(sorted(data.get("tool_projects", {}).get(tool_name, set())))
        lines.append(f"| `{tool_name}` | {format_number(count)} | {projects} |")
    lines.append("")

    usage_inventory = data.get("usage_inventory", {})
    usage_summary = usage_inventory.get("summary", {})
    if usage_summary:
        lines.append("## Inventário Operacional")
        lines.append("")
        lines.append("| Domínio | Itens rastreados |")
        lines.append("|---------|-----------------|")
        lines.append(f"| Skills normalizadas | {format_number(usage_summary.get('normalized_skills', 0))} |")
        lines.append(f"| Slash commands cruos | {format_number(usage_summary.get('slash_commands', 0))} |")
        lines.append(f"| Skill tool cruos | {format_number(usage_summary.get('skill_tools', 0))} |")
        lines.append(f"| Agents | {format_number(usage_summary.get('agents', 0))} |")
        lines.append(f"| Tools | {format_number(usage_summary.get('tools', 0))} |")
        lines.append(f"| Runners | {format_number(usage_summary.get('runners', 0))} |")
        lines.append("")

        normalized_usage = top_usage_entries(data, "normalized_skills", "top_by_usage")
        if normalized_usage:
            lines.append("### Skills Normalizadas por Uso")
            lines.append("")
            lines.append("| Skill | Invocações | Sessões | Projetos | Linhas +/- | Erro (%) |")
            lines.append("|-------|-----------|---------|----------|------------|----------|")
            for entry in normalized_usage:
                lines.append(
                    f"| `{entry['name']}` | {format_number(entry['invocations'])} | {format_number(entry['sessions'])} | "
                    f"{format_number(entry['projects_count'])} | {format_number(entry['associated_lines_changed'])} | "
                    f"{format_number(entry['error_session_rate'] * 100)} |"
                )
            lines.append("")

        slash_usage = top_usage_entries(data, "slash_commands", "top_by_usage")
        if slash_usage:
            lines.append("### Slash Commands Cruos")
            lines.append("")
            lines.append("| Command | Invocações | Sessões | Interativas | Headless | Subagents |")
            lines.append("|---------|-----------|---------|-------------|----------|-----------|")
            for entry in slash_usage:
                lines.append(
                    f"| `{entry['name']}` | {format_number(entry['invocations'])} | {format_number(entry['sessions'])} | "
                    f"{format_number(entry['interactive_invocations'])} | {format_number(entry['headless_invocations'])} | "
                    f"{format_number(entry['subagent_invocations'])} |"
                )
            lines.append("")

        skill_tool_usage = top_usage_entries(data, "skill_tools", "top_by_usage")
        if skill_tool_usage:
            lines.append("### Skill Tool Cruo")
            lines.append("")
            lines.append("| Skill | Invocações | Sessões | Interativas | Headless | Subagents |")
            lines.append("|-------|-----------|---------|-------------|----------|-----------|")
            for entry in skill_tool_usage:
                lines.append(
                    f"| `{entry['name']}` | {format_number(entry['invocations'])} | {format_number(entry['sessions'])} | "
                    f"{format_number(entry['interactive_invocations'])} | {format_number(entry['headless_invocations'])} | "
                    f"{format_number(entry['subagent_invocations'])} |"
                )
            lines.append("")

        agent_usage = top_usage_entries(data, "agents", "top_by_impact")
        if agent_usage:
            lines.append("### Agents por Impacto Observado")
            lines.append("")
            lines.append("| Agent | Invocações | Sessões | Linhas +/- | Arquivos | Erro (%) |")
            lines.append("|-------|-----------|---------|------------|----------|----------|")
            for entry in agent_usage:
                lines.append(
                    f"| `{entry['name']}` | {format_number(entry['invocations'])} | {format_number(entry['sessions'])} | "
                    f"{format_number(entry['associated_lines_changed'])} | {format_number(entry['associated_files_modified'])} | "
                    f"{format_number(entry['error_session_rate'] * 100)} |"
                )
            lines.append("")

    context_cost_skills = top_usage_entries(data, "normalized_skills", "top_by_context_cost")
    context_cost_tools = top_usage_entries(data, "tools", "top_by_context_cost")
    if context_cost_skills or context_cost_tools:
        lines.append("## Custo de Contexto")
        lines.append("")
        if context_cost_skills:
            lines.append("### Skills com Maior Custo de Contexto")
            lines.append("")
            lines.append("| Skill | Tokens assoc. | Média tokens/sessão | Sessões | Linhas +/- |")
            lines.append("|-------|---------------|---------------------|---------|------------|")
            for entry in context_cost_skills:
                lines.append(
                    f"| `{entry['name']}` | {format_number(entry['associated_tokens'])} | "
                    f"{format_number(entry.get('avg_associated_tokens_per_session', 0))} | {format_number(entry['sessions'])} | "
                    f"{format_number(entry['associated_lines_changed'])} |"
                )
            lines.append("")

        if context_cost_tools:
            lines.append("### Tools com Maior Custo de Contexto")
            lines.append("")
            lines.append("| Tool | Tokens assoc. | Média tokens/sessão | Sessões | Invocações |")
            lines.append("|------|---------------|---------------------|---------|------------|")
            for entry in context_cost_tools:
                lines.append(
                    f"| `{entry['name']}` | {format_number(entry['associated_tokens'])} | "
                    f"{format_number(entry.get('avg_associated_tokens_per_session', 0))} | {format_number(entry['sessions'])} | "
                    f"{format_number(entry['invocations'])} |"
                )
            lines.append("")

    friction_skills = top_usage_entries(data, "normalized_skills", "top_by_friction")
    tool_friction = top_usage_entries(data, "tools", "top_by_friction")
    if friction_skills or tool_friction:
        lines.append("## Fricção Operacional")
        lines.append("")
        if friction_skills:
            lines.append("### Skills com Mais Fricção")
            lines.append("")
            lines.append("| Skill | Sessões com erro | Erro (%) | Sessões | Tokens assoc. |")
            lines.append("|-------|------------------|----------|---------|---------------|")
            for entry in friction_skills:
                lines.append(
                    f"| `{entry['name']}` | {format_number(entry['sessions_with_errors'])} | "
                    f"{format_number(entry['error_session_rate'] * 100)} | {format_number(entry['sessions'])} | "
                    f"{format_number(entry['associated_tokens'])} |"
                )
            lines.append("")

        if tool_friction:
            lines.append("### Tools com Mais Fricção")
            lines.append("")
            lines.append("| Tool | Sessões com erro | Erro (%) | Invocações | Sessões | Tokens assoc. |")
            lines.append("|------|------------------|----------|-----------|---------|---------------|")
            for entry in tool_friction:
                lines.append(
                    f"| `{entry['name']}` | {format_number(entry['sessions_with_errors'])} | "
                    f"{format_number(entry['error_session_rate'] * 100)} | {format_number(entry['invocations'])} | "
                    f"{format_number(entry['sessions'])} | {format_number(entry['associated_tokens'])} |"
                )
            lines.append("")

    lines.append("## Facets de Sessão")
    lines.append("")
    lines.append("| Dimensão | Top Valores |")
    lines.append("|----------|-------------|")
    lines.append(
        f"| Fontes | {', '.join(f'{name} ({format_number(count)})' for name, count in facet_summary.get('sources', Counter()).most_common(5)) or 'n/a'} |"
    )
    lines.append(
        f"| Goal Categories | {', '.join(f'{name} ({format_number(count)})' for name, count in facet_summary.get('goal_categories', Counter()).most_common(5)) or 'n/a'} |"
    )
    lines.append(
        f"| Outcomes | {', '.join(f'{name} ({format_number(count)})' for name, count in facet_summary.get('outcomes', Counter()).most_common(5)) or 'n/a'} |"
    )
    lines.append(
        f"| Satisfaction | {', '.join(f'{name} ({format_number(count)})' for name, count in facet_summary.get('satisfaction', Counter()).most_common(5)) or 'n/a'} |"
    )
    lines.append(
        f"| Friction Points | {', '.join(f'{name} ({format_number(count)})' for name, count in facet_summary.get('friction_points', Counter()).most_common(5)) or 'n/a'} |"
    )
    lines.append("")

    if any(str(narrative.get(field, "")).strip() for field in narrative_fields):
        lines.append("## Insights Narrativos")
        lines.append("")
        narrative_titles = {
            "at_a_glance": "Resumo Executivo",
            "project_areas": "Áreas de Projeto",
            "interaction_style": "Estilo de Interação",
            "what_works": "O Que Está Funcionando",
            "friction_analysis": "Análise de Fricção",
            "suggestions": "Sugestões",
            "on_the_horizon": "No Horizonte",
            "fun_ending": "Fechamento",
        }
        lines.append(f"**Fonte:** {narrative.get('source', 'deterministic')}")
        lines.append("")
        for field in narrative_fields:
            text = str(narrative.get(field, "")).strip()
            if text:
                lines.append(f"### {narrative_titles[field]}")
                lines.append("")
                lines.append(text)
                lines.append("")

    lines.append("## Recomendações Acionáveis")
    lines.append("")
    lines.append("| Métrica | Valor |")
    lines.append("|---------|-------|")
    lines.append(f"| Total de recomendações | {format_number(recommendation_summary.get('total_recommendations', 0))} |")
    lines.append(f"| Alto impacto | {format_number(recommendation_summary.get('high_impact', 0))} |")
    lines.append(f"| Quick Wins | {format_number(recommendation_summary.get('quick_wins', 0))} |")
    lines.append(f"| Ganho estimado por semana | {format_number(recommendation_summary.get('estimated_minutes_saved_per_week', 0))} min |")
    lines.append("")

    for effort in ("Quick", "Medium", "Investment"):
        effort_recommendations = [
            recommendation
            for recommendation in recommendations.get("top_recommendations", [])
            if recommendation.get("effort") == effort
        ]
        if not effort_recommendations:
            continue
        effort_title = {
            "Quick": "Quick Wins",
            "Medium": "Medium Effort",
            "Investment": "Investment Items",
        }[effort]
        lines.append(f"### {effort_title}")
        lines.append("")
        for idx, recommendation in enumerate(effort_recommendations, start=1):
            scope_label = recommendation.get("project") or "global"
            lines.append(
                f"{idx}. **{recommendation.get('title', '')}** "
                f"[{recommendation.get('impact', '')}] ({scope_label}) — "
                f"{recommendation.get('description', '')}"
            )
            lines.append(
                f"   Fase: {recommendation.get('phase', '')} | "
                f"Categoria: {recommendation.get('category', '')} | "
                f"Ganho estimado: {format_number(recommendation.get('estimated_minutes_saved_per_week', 0))} min/semana"
            )
            lines.append(f"   Racional: {recommendation.get('rationale', '')}")
            lines.append(f"   Passos: {'; '.join(recommendation.get('implementation_steps', []))}")
        lines.append("")

    project_recommendation_rows = []
    for project_name, items in recommendations.get("by_project", {}).items():
        top_title = items[0]["title"] if items else "n/a"
        project_recommendation_rows.append((project_name, len(items), top_title))
    if project_recommendation_rows:
        lines.append("### Cobertura por Projeto")
        lines.append("")
        lines.append("| Projeto | Recomendações | Top Item |")
        lines.append("|---------|---------------|----------|")
        for project_name, count, top_title in sorted(project_recommendation_rows, key=lambda row: -row[1]):
            lines.append(f"| **{project_name}** | {format_number(count)} | {top_title} |")
        lines.append("")

    lines.append("## Top Agents (subagent_type)")
    lines.append("")
    lines.append("| Agent | Invocações | Projetos |")
    lines.append("|-------|-----------|----------|")
    for agent, count in data["agents"].most_common(20):
        projects = ", ".join(sorted(data["agent_projects"].get(agent, set())))
        lines.append(f"| `{agent}` | {format_number(count)} | {projects} |")
    lines.append("")

    lines.append("## Top Shell Runners")
    lines.append("")
    lines.append("| Runner | Invocações |")
    lines.append("|--------|-----------|")
    for runner, count in data["runners"].most_common(15):
        lines.append(f"| `{runner}` | {format_number(count)} |")
    lines.append("")

    if project_roots and discover_inventory_fn:
        for root_label, root_path in project_roots.items():
            inventory = discover_inventory_fn(root_path)

            all_used = set()
            for key in combined:
                clean = normalize_skill_name_fn(key).split(":")[0]
                all_used.add(clean)
                all_used.add(normalize_skill_name_fn(key))

            unused_skills = [skill for skill in inventory["skills"] if skill not in all_used]
            if unused_skills:
                lines.append(f"## Skills NUNCA Usados ({root_label})")
                lines.append("")
                for skill in unused_skills:
                    lines.append(f"- `{skill}`")
                lines.append("")

            used_squads = set()
            for key in combined:
                parts = normalize_skill_name_fn(key).split(":")
                if len(parts) >= 2:
                    used_squads.add(parts[0])
                slash_parts = normalize_skill_name_fn(key).split("/")
                if len(slash_parts) >= 1:
                    used_squads.add(slash_parts[0])
                hyphen_parts = normalize_skill_name_fn(key).split("-")
                if len(hyphen_parts) >= 1:
                    used_squads.add(hyphen_parts[0])

            unused_skill_groups = {
                squad: count
                for squad, count in inventory["skill_groups"].items()
                if squad not in used_squads and squad.lower() not in {item.lower() for item in used_squads}
            }
            if unused_skill_groups:
                lines.append(f"## Skill Groups NUNCA Usados ({root_label})")
                lines.append("")
                lines.append("| Squad | Files | Invocações |")
                lines.append("|-------|-------|-----------|")
                for squad, count in sorted(unused_skill_groups.items(), key=lambda item: -item[1]):
                    lines.append(f"| `{squad}` | {format_number(count)} | 0 |")
                lines.append("")

            used_agent_types = set(data["agents"].keys())
            unused_agents = [agent for agent in inventory["agents"] if agent not in used_agent_types]
            if unused_agents:
                lines.append(f"## Agents NUNCA Usados como subagent_type ({root_label})")
                lines.append("")
                for agent in unused_agents:
                    lines.append(f"- `{agent}`")
                lines.append("")

    if project_roots and get_recent_commits_fn:
        for root_label, root_path in project_roots.items():
            commits = get_recent_commits_fn(root_path, days)
            if commits:
                lines.append(f"## Commits por Área ({root_label})")
                lines.append("")
                lines.append("| Área | Commits |")
                lines.append("|------|---------|")
                for area, count in sorted(commits.items(), key=lambda item: -item[1]):
                    lines.append(f"| {area} | {format_number(count)} |")
                lines.append("")

    error_categories = summary.get("tool_error_categories", Counter())
    if error_categories:
        lines.append("## Categorias de Erro de Tool")
        lines.append("")
        lines.append("| Categoria | Ocorrências |")
        lines.append("|-----------|-------------|")
        for category, count in Counter(error_categories).most_common():
            lines.append(f"| {category} | {format_number(count)} |")
        lines.append("")

    return "\n".join(lines)

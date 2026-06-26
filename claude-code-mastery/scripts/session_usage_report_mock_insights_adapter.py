#!/usr/bin/env python3
"""
Mock insights adapter for session-usage-report.py.

Reads JSON from stdin and returns JSON to stdout. Useful to test the
`--insights-command` integration path without depending on an external model.
"""
import json
import sys
from collections import Counter


def truncate(text, max_chars=280):
    """Trim long strings for compact JSON responses."""
    text = str(text or "").strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."


def summarize_chunk(payload):
    """Return a compact transcript chunk summary."""
    chunk = str(payload.get("transcript_chunk", "") or "")
    lines = [line.strip() for line in chunk.splitlines() if line.strip()]
    highlights = []
    for line in lines:
        if " USER:" in line or line.startswith("[User]:"):
            highlights.append(line)
        elif "_TOOLS:" in line or line.startswith("[Tool:"):
            highlights.append(line)
        elif any(token in line.lower() for token in ("error", "failed", "warning", "interrupt")):
            highlights.append(line)
        if len(highlights) >= 6:
            break
    if not highlights:
        highlights = lines[:4]
    return {"summary": truncate("\n".join(highlights), 1200)}


def infer_goal_categories(session_meta):
    """Infer simple goal categories from observed session signals."""
    categories = []
    tools = Counter(session_meta.get("tools", {}))
    skills = Counter(session_meta.get("skills", {}))
    if tools.get("Edit") or tools.get("Write"):
        categories.append("coding")
    if session_meta.get("uses_web_search") or session_meta.get("uses_web_fetch"):
        categories.append("research")
    if session_meta.get("uses_task_agent") or tools.get("Agent"):
        categories.append("orchestration")
    if session_meta.get("is_headless"):
        categories.append("automation")
    if any(skill in {"deploy", "commit", "release"} for skill in skills):
        categories.append("delivery")
    if not categories:
        categories.append("general")
    return categories[:5]


def facet(payload):
    """Return synthetic facet enrichment using transcript + session meta."""
    session_meta = payload.get("session_meta", {}) or {}
    transcript = str(payload.get("transcript", "") or "")
    goal_categories = infer_goal_categories(session_meta)
    tool_errors = int(session_meta.get("tool_errors", 0) or 0)
    lines_changed = int(session_meta.get("lines_added", 0) or 0) + int(session_meta.get("lines_removed", 0) or 0)

    if lines_changed and tool_errors:
        outcome = "partial"
    elif lines_changed:
        outcome = "implemented"
    elif tool_errors:
        outcome = "blocked"
    elif session_meta.get("uses_web_search") or session_meta.get("uses_web_fetch"):
        outcome = "researched"
    else:
        outcome = "unknown"

    if tool_errors > 1:
        satisfaction = "low"
    elif tool_errors == 0:
        satisfaction = "high"
    else:
        satisfaction = "medium"

    friction_points = []
    for category, count in Counter(session_meta.get("tool_error_categories", {})).most_common(3):
        if count > 0:
            friction_points.append(str(category).lower())
    if int(session_meta.get("user_interruptions", 0) or 0) > 0:
        friction_points.append("user interruptions")

    top_tools = ", ".join(Counter(session_meta.get("tools", {})).keys()) or "conversation"
    return {
        "underlying_goal": f"Sessão focada em {', '.join(goal_categories)}",
        "goal_categories": goal_categories,
        "outcome": outcome,
        "satisfaction": satisfaction,
        "friction_points": friction_points[:5],
        "primary_success": truncate(f"Transcript analisada com foco em {top_tools}", 160),
        "brief_summary": truncate(transcript, 320),
    }


def narrative(payload):
    """Return synthetic narrative from aggregate report data."""
    summary = payload.get("summary", {}) or {}
    facet_summary = payload.get("facet_summary", {}) or {}
    top_skills = Counter(payload.get("top_skills", {}))
    top_tools = Counter(payload.get("top_tools", {}))
    top_agents = Counter(payload.get("top_agents", {}))

    top_goal = next(iter(Counter(facet_summary.get("goal_categories", {})).keys()), "general")
    top_skill = next(iter(top_skills.keys()), "n/a")
    top_tool = next(iter(top_tools.keys()), "n/a")
    top_agent = next(iter(top_agents.keys()), "n/a")

    return {
        "at_a_glance": (
            f"{summary.get('total_sessions', 0)} sessões principais, "
            f"{summary.get('total_tool_errors', 0)} erros de tool e "
            f"{summary.get('total_branches_deduped', 0)} branches deduplicadas."
        ),
        "project_areas": f"Área dominante observada: {top_goal}.",
        "interaction_style": (
            f"Skill mais frequente: {top_skill}. "
            f"Tempo médio de resposta: {summary.get('avg_user_response_seconds', 0)}s."
        ),
        "what_works": f"Ferramenta mais recorrente: {top_tool}. Agent mais acionado: {top_agent}.",
        "friction_analysis": (
            f"Fricções principais: "
            f"{', '.join(Counter(facet_summary.get('friction_points', {})).keys()) or 'sem fricções relevantes'}."
        ),
        "suggestions": (
            "Usar esta narrativa apenas para validar o caminho de integração. "
            "Para análise real, troque o adapter por um backend com modelo."
        ),
        "on_the_horizon": (
            "O próximo passo é conectar esse report a um backend real de narrativa "
            "e enriquecer oportunidades futuras com exemplos concretos."
        ),
        "fun_ending": "Até o mock já mostra um padrão claro de operação contínua.",
    }


def insight_sections(payload):
    """Return a structured multi-section payload closer to Claude /insights."""
    summary = payload.get("summary", {}) or {}
    top_skills = Counter(payload.get("top_skills", {}))
    top_tools = Counter(payload.get("top_tools", {}))
    top_agents = Counter(payload.get("top_agents", {}))
    top_projects = payload.get("top_projects", []) or []
    facet_summary = payload.get("facet_summary", {}) or {}
    friction_labels = list(Counter(facet_summary.get("friction_points", {})).keys())

    project_area_items = []
    for project in top_projects[:4]:
        project_area_items.append(
            {
                "name": project.get("name", "Projeto"),
                "session_count": int(project.get("sessions", 0) or 0),
                "description": (
                    f"{project.get('sessions', 0)} sessões, "
                    f"{project.get('input_tokens', 0)}/{project.get('output_tokens', 0)} tokens "
                    f"e +{project.get('lines_added', 0)}/-{project.get('lines_removed', 0)} linhas."
                ),
            }
        )

    what_works_items = [
        {
            "title": "Execução consistente",
            "description": (
                f"Você manteve trabalho real em sessões com {summary.get('total_tool_errors', 0)} erros de tool "
                f"para {summary.get('total_lines_added', 0)} linhas adicionadas."
            ),
        },
        {
            "title": "Uso recorrente de workflow",
            "description": (
                f"Skills dominantes: {', '.join(list(top_skills.keys())[:3]) or 'n/a'}. "
                f"Tools dominantes: {', '.join(list(top_tools.keys())[:3]) or 'n/a'}."
            ),
        },
        {
            "title": "Adoção de agents",
            "description": f"Agents mais frequentes: {', '.join(list(top_agents.keys())[:3]) or 'n/a'}.",
        },
    ]

    friction_categories = [
        {
            "category": "Erros recorrentes",
            "description": "O histórico ainda mostra categorias de falha repetidas que poderiam ser capturadas em regras persistentes.",
            "examples": [label for label in friction_labels[:2]] or ["sem exemplos suficientes"],
        }
    ]

    return {
        "at_a_glance_sections": {
            "whats_working": "Você já opera com volume e sinais reais de execução, não só com exploração superficial.",
            "whats_hindering": "Os principais atritos ainda se repetem em categorias conhecidas, o que sugere falta de persistência operacional.",
            "quick_wins": "Transformar instruções recorrentes em CLAUDE.md, hooks e skills tende a reduzir retrabalho.",
            "ambitious_workflows": "As frentes com mais agents, scripts e edição real já são candidatas para loops mais autônomos.",
        },
        "project_area_items": project_area_items,
        "interaction_style": (
            f"Você usa Claude Code como sistema de execução contínua. "
            f"O padrão dominante combina {next(iter(top_skills.keys()), 'skills')} com {next(iter(top_tools.keys()), 'tools')}."
        ),
        "what_works_items": what_works_items,
        "friction_categories": friction_categories,
        "claude_md_additions": [
            {
                "addition": "Registrar convenções repetidas de merge, formato e validação.",
                "why": "O histórico mostra atritos repetidos que poderiam virar regra persistente.",
                "prompt_scaffold": "Adicionar em `CLAUDE.md` sob `## Regras Operacionais`.",
            }
        ],
        "features_to_try": [
            {
                "feature": "Custom Skills",
                "one_liner": "Empacotar workflows recorrentes.",
                "why_for_you": "Seu histórico já mostra skills suficientemente estáveis para isso.",
                "example_code": "Criar `.claude/skills/commit/SKILL.md` para o fluxo de commit.",
            }
        ],
        "usage_patterns": [
            {
                "title": "Persistir padrões repetidos",
                "suggestion": "Mover instruções recorrentes para assets persistentes.",
                "detail": "Isso reduz a dependência de correção manual sessão a sessão.",
                "copyable_prompt": "Analise minhas instruções repetidas e proponha CLAUDE.md + skills + hooks.",
            }
        ],
        "on_the_horizon": "Há espaço para workflows mais autônomos e paralelos nas frentes já dominadas.",
        "horizon_opportunities": [
            {
                "title": "Loop autônomo de validação",
                "whats_possible": "A rotina mais repetida do histórico pode virar um ciclo fechado com validação e correção automática.",
                "how_to_try": "Comece pela área com mais erros de tool e mais linhas alteradas.",
                "copyable_prompt": "Desenhe um loop autônomo para a minha rotina mais repetida.",
            }
        ],
        "fun_ending_card": {
            "headline": "Até o mock mostra uma operação com assinatura forte.",
            "detail": "O padrão dominante é execução contínua com sinais reais de adoção e fricção.",
        },
    }


def main():
    """Dispatch adapter modes from stdin JSON."""
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(json.dumps({"error": f"invalid_json: {exc}"}))
        raise SystemExit(1) from exc

    mode = str(payload.get("mode", "") or "").strip()
    if mode == "summarize_chunk":
        response = summarize_chunk(payload)
    elif mode == "facet":
        response = facet(payload)
    elif mode == "insight_sections":
        response = insight_sections(payload)
    elif mode == "narrative":
        response = narrative(payload)
    else:
        print(json.dumps({"error": f"unsupported_mode: {mode}"}))
        raise SystemExit(2)

    print(json.dumps(response, ensure_ascii=False))


if __name__ == "__main__":
    main()

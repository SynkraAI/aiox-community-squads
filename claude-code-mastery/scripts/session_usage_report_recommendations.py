#!/usr/bin/env python3
"""
Deterministic workflow recommendations for the session usage report.
"""
from collections import Counter


IMPACT_WEIGHTS = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
EFFORT_WEIGHTS = {"Quick": 3, "Medium": 2, "Investment": 1}


def safe_div(numerator, denominator):
    """Divide safely for heuristic scoring."""
    return float(numerator) / float(denominator) if denominator else 0.0


def make_recommendation(
    rec_id,
    title,
    description,
    impact,
    effort,
    category,
    phase,
    rationale,
    implementation_steps,
    estimated_minutes_saved_per_week,
    scope="global",
    project=None,
):
    """Canonical recommendation object used across report outputs."""
    return {
        "id": rec_id,
        "scope": scope,
        "project": project,
        "title": title,
        "description": description,
        "impact": impact,
        "effort": effort,
        "category": category,
        "phase": phase,
        "rationale": rationale,
        "implementation_steps": implementation_steps,
        "estimated_minutes_saved_per_week": estimated_minutes_saved_per_week,
        "priority_score": IMPACT_WEIGHTS.get(impact, 0) * 10 + EFFORT_WEIGHTS.get(effort, 0),
    }


def sort_recommendations(recommendations):
    """Sort recommendations by priority, then benefit, then title."""
    return sorted(
        recommendations,
        key=lambda rec: (
            -rec.get("priority_score", 0),
            -rec.get("estimated_minutes_saved_per_week", 0),
            rec.get("title", ""),
        ),
    )


def build_project_recommendations(project_name, project_data):
    """Deterministic workflow recommendations derived from one project's session metrics."""
    recommendations = []
    total_sessions = project_data.get("interactive", 0) + project_data.get("headless", 0)
    total_lines_changed = project_data.get("lines_added", 0) + project_data.get("lines_removed", 0)
    error_rate = safe_div(project_data.get("tool_errors", 0), max(total_sessions, 1))
    branch_pressure = project_data.get("branches_deduped", 0)
    response_seconds = project_data.get("avg_user_response_seconds", 0)
    web_sessions = project_data.get("sessions_with_web_search", 0) + project_data.get("sessions_with_web_fetch", 0)

    if project_data.get("tool_errors", 0) >= 2 or error_rate >= 0.5:
        impact = "HIGH" if project_data.get("tool_errors", 0) >= 3 else "MEDIUM"
        recommendations.append(make_recommendation(
            rec_id=f"{project_name}-permission-friction",
            scope="project",
            project=project_name,
            title="Revisar estratégia de permissões para reduzir falhas recorrentes",
            description="Há erros de tool suficientes para justificar uma revisão de allows seguros, prompts recorrentes e regras de edição.",
            impact=impact,
            effort="Quick",
            category="permissions",
            phase="Phase 3: Optimize Permission Strategy",
            rationale=(
                f"{project_data.get('tool_errors', 0)} erros de tool em {total_sessions} sessões principais "
                f"(taxa {round(error_rate * 100)}%)."
            ),
            implementation_steps=[
                "Listar as categorias de erro mais comuns e os comandos/paths envolvidos.",
                "Adicionar allows seguros para build, lint, testes e git read-only que hoje geram atrito.",
                "Promover padrões de correção repetidos para skills ou regras direcionadas.",
            ],
            estimated_minutes_saved_per_week=35 if impact == "HIGH" else 18,
        ))

    if branch_pressure >= 2:
        recommendations.append(make_recommendation(
            rec_id=f"{project_name}-context-checkpoints",
            scope="project",
            project=project_name,
            title="Inserir checkpoints de contexto e plano para sessões ramificadas",
            description="A quantidade de branches deduplicadas indica drift ou retomadas sucessivas do mesmo problema.",
            impact="HIGH" if branch_pressure >= 4 else "MEDIUM",
            effort="Quick",
            category="context",
            phase="Phase 2: Identify Bottlenecks",
            rationale=f"{branch_pressure} branches deduplicadas no período.",
            implementation_steps=[
                "Definir checkpoint explícito a cada mudança de abordagem maior.",
                "Compactar contexto ao fim de cada bloco de implementação ou investigação.",
                "Mover instruções permanentes para `CLAUDE.md`/regras e deixar a sessão com estado mínimo.",
            ],
            estimated_minutes_saved_per_week=28 if branch_pressure >= 4 else 15,
        ))

    if total_lines_changed >= 120 and project_data.get("sessions_with_task_agent", 0) == 0:
        recommendations.append(make_recommendation(
            rec_id=f"{project_name}-subagent-adoption",
            scope="project",
            project=project_name,
            title="Introduzir decomposição com subagents nas tarefas longas",
            description="O volume de alteração sugere trabalho suficiente para paralelizar exploração, implementação e verificação.",
            impact="HIGH",
            effort="Medium",
            category="orchestration",
            phase="Phase 1: Analyze Usage Patterns",
            rationale=f"{total_lines_changed} linhas alteradas sem uso de task agents no período.",
            implementation_steps=[
                "Separar exploração, implementação e revisão em subtarefas com ownership claro.",
                "Usar subagents para sidecars independentes e manter o agente principal no caminho crítico.",
                "Registrar padrões de decomposição efetivos em skill ou comando do time.",
            ],
            estimated_minutes_saved_per_week=32,
        ))

    if web_sessions >= 3 and project_data.get("sessions_with_mcp", 0) == 0:
        recommendations.append(make_recommendation(
            rec_id=f"{project_name}-research-stack",
            scope="project",
            project=project_name,
            title="Converter pesquisa recorrente em stack persistente de conhecimento",
            description="Há sessões de pesquisa suficientes para justificar MCP, memória de projeto ou skill de pesquisa dedicada.",
            impact="MEDIUM",
            effort="Medium",
            category="knowledge",
            phase="Phase 5: Configure Auto-Memory",
            rationale=f"{web_sessions} sessões com WebSearch/WebFetch e nenhuma sessão com MCP.",
            implementation_steps=[
                "Criar memória curta para findings confirmados e preferências recorrentes.",
                "Avaliar MCP ou skill de pesquisa para reduzir busca repetitiva no mesmo domínio.",
                "Salvar consultas e fontes de alta frequência em artefato auditável.",
            ],
            estimated_minutes_saved_per_week=22,
        ))

    if response_seconds >= 45 or project_data.get("user_interruptions", 0) >= 2:
        recommendations.append(make_recommendation(
            rec_id=f"{project_name}-shortcuts-and-automation",
            scope="project",
            project=project_name,
            title="Padronizar atalhos e automações para reduzir espera manual",
            description="A sessão mostra latência humana ou interrupções suficientes para justificar teclas rápidas, hooks leves e comandos compostos.",
            impact="MEDIUM",
            effort="Quick",
            category="shortcuts",
            phase="Phase 4: Set Up Keyboard Shortcuts",
            rationale=(
                f"Tempo médio de resposta {response_seconds}s e "
                f"{project_data.get('user_interruptions', 0)} interrupções."
            ),
            implementation_steps=[
                "Configurar atalhos para cancelar, compactar e reexecutar testes/validação.",
                "Encapsular fluxos repetitivos em comandos slash ou skills locais.",
                "Usar hooks leves para tarefas determinísticas de pré/pós execução.",
            ],
            estimated_minutes_saved_per_week=14,
        ))

    return sort_recommendations(recommendations)


def build_global_recommendations(summary, facet_summary):
    """Deterministic workflow recommendations derived from whole-period aggregates."""
    recommendations = []
    total_sessions = summary.get("total_sessions", 0)
    total_lines_changed = summary.get("total_lines_added", 0) + summary.get("total_lines_removed", 0)
    web_sessions = summary.get("sessions_with_web_search", 0) + summary.get("sessions_with_web_fetch", 0)

    if summary.get("total_tool_errors", 0) >= max(3, total_sessions // 4):
        recommendations.append(make_recommendation(
            rec_id="global-permission-baseline",
            title="Criar baseline de permissões seguras para os comandos mais frequentes",
            description="O volume agregado de erros indica que o workflow ainda está pagando custo excessivo em prompts ou tentativas falhas.",
            impact="HIGH",
            effort="Medium",
            category="permissions",
            phase="Phase 3: Optimize Permission Strategy",
            rationale=f"{summary.get('total_tool_errors', 0)} erros de tool em {total_sessions} sessões.",
            implementation_steps=[
                "Derivar um conjunto padrão de allows seguros a partir dos comandos e tools mais recorrentes.",
                "Publicar esse baseline em settings/rules reutilizáveis por projeto.",
                "Comparar prompts esperados antes/depois após nova coleta do report.",
            ],
            estimated_minutes_saved_per_week=45,
        ))

    if summary.get("total_branches_deduped", 0) >= max(4, total_sessions // 3):
        recommendations.append(make_recommendation(
            rec_id="global-context-discipline",
            title="Adotar disciplina operacional de compaction e checkpoints de plano",
            description="A taxa de branches deduplicadas mostra retrabalho de contexto suficiente para justificar uma política explícita de checkpoint.",
            impact="HIGH",
            effort="Quick",
            category="context",
            phase="Phase 2: Identify Bottlenecks",
            rationale=(
                f"{summary.get('total_branches_deduped', 0)} branches deduplicadas em {total_sessions} sessões."
            ),
            implementation_steps=[
                "Definir gatilhos de compaction por mudança de abordagem, tamanho de diff e duração da sessão.",
                "Exigir resumo curto de estado ao finalizar cada bloco significativo.",
                "Extrair instruções permanentes para `CLAUDE.md`, regras ou memória.",
            ],
            estimated_minutes_saved_per_week=38,
        ))

    if total_lines_changed >= 400 and summary.get("sessions_with_task_agent", 0) <= max(1, total_sessions // 6):
        recommendations.append(make_recommendation(
            rec_id="global-subagent-playbook",
            title="Formalizar playbook de decomposição multiagente para tarefas extensas",
            description="O volume de alteração já justifica uma prática padrão de subagents para exploração, implementação e verificação.",
            impact="HIGH",
            effort="Investment",
            category="orchestration",
            phase="Phase 1: Analyze Usage Patterns",
            rationale=(
                f"{total_lines_changed} linhas alteradas com apenas {summary.get('sessions_with_task_agent', 0)} sessões usando task agents."
            ),
            implementation_steps=[
                "Definir heurística de quando spawnar subagents por tamanho/risco da tarefa.",
                "Criar exemplos prontos de ownership por arquivo ou módulo.",
                "Treinar o time para usar paralelismo apenas em sidecars independentes.",
            ],
            estimated_minutes_saved_per_week=55,
        ))

    if web_sessions >= max(4, summary.get("sessions_with_mcp", 0) * 2 + 1):
        recommendations.append(make_recommendation(
            rec_id="global-research-memory",
            title="Transformar pesquisa repetitiva em memória e conectores persistentes",
            description="O perfil agregado mostra dependência de pesquisa web acima do necessário para um stack maduro.",
            impact="MEDIUM",
            effort="Medium",
            category="knowledge",
            phase="Phase 5: Configure Auto-Memory",
            rationale=f"{web_sessions} sessões com pesquisa web versus {summary.get('sessions_with_mcp', 0)} com MCP.",
            implementation_steps=[
                "Capturar findings confirmados em memória ou knowledge base curta.",
                "Avaliar MCPs e skills para domínios pesquisados com maior frequência.",
                "Promover queries repetidas e fontes confiáveis para workflow padrão.",
            ],
            estimated_minutes_saved_per_week=27,
        ))

    if facet_summary.get("friction_points", Counter()).get("user interruptions", 0) >= 2:
        recommendations.append(make_recommendation(
            rec_id="global-fast-lane",
            title="Criar fast lane operacional para cancelamento, validação e retomada",
            description="Interrupções recorrentes sugerem custo alto de navegação e mudança de contexto.",
            impact="MEDIUM",
            effort="Quick",
            category="shortcuts",
            phase="Phase 4: Set Up Keyboard Shortcuts",
            rationale=(
                f"{facet_summary.get('friction_points', Counter()).get('user interruptions', 0)} sessões com friction point de interrupção."
            ),
            implementation_steps=[
                "Padronizar atalhos para cancelar execução, aceitar prompt seguro e compactar contexto.",
                "Criar comandos compostos para testes, lint e checkpoint.",
                "Reduzir passos manuais entre investigação e execução.",
            ],
            estimated_minutes_saved_per_week=16,
        ))

    return sort_recommendations(recommendations)


def generate_workflow_recommendations(data):
    """Produce actionable optimization recommendations from the report dataset."""
    by_project = {}
    all_project_recommendations = []
    for project_name, project_data in data.get("projects", {}).items():
        project_recommendations = build_project_recommendations(project_name, project_data)
        by_project[project_name] = project_recommendations
        all_project_recommendations.extend(project_recommendations)

    global_recommendations = build_global_recommendations(
        data.get("summary", {}),
        data.get("facet_summary", {}),
    )
    all_recommendations = sort_recommendations(global_recommendations + all_project_recommendations)

    return {
        "summary": {
            "total_recommendations": len(all_recommendations),
            "high_impact": sum(1 for rec in all_recommendations if rec.get("impact") == "HIGH"),
            "medium_impact": sum(1 for rec in all_recommendations if rec.get("impact") == "MEDIUM"),
            "low_impact": sum(1 for rec in all_recommendations if rec.get("impact") == "LOW"),
            "quick_wins": sum(1 for rec in all_recommendations if rec.get("effort") == "Quick"),
            "estimated_minutes_saved_per_week": sum(
                rec.get("estimated_minutes_saved_per_week", 0)
                for rec in all_recommendations
            ),
        },
        "global": global_recommendations,
        "by_project": by_project,
        "top_recommendations": all_recommendations[:8],
    }

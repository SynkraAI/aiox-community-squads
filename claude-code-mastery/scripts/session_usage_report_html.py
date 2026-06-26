#!/usr/bin/env python3
"""
HTML renderer for Claude Code session usage reports.

Keeps presentation concerns out of the main analysis script.
"""
import html
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


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

MODULE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = MODULE_DIR.parent / "templates"
HTML_TEMPLATE_PATH = TEMPLATES_DIR / "session-usage-report-page.html"
CSS_TEMPLATE_PATH = TEMPLATES_DIR / "session-usage-report-page.css"


def normalize_skill_name(key):
    """Normalize slash commands and Skill tool names into a common form."""
    return str(key or "").lstrip("/")


def build_skill_rollup(data):
    """Merge Skill tool and slash command counts into a single normalized view."""
    combined = Counter()
    combined_interactive = Counter()
    combined_headless = Counter()
    combined_projects = defaultdict(set)

    for key, value in data.get("skills", Counter()).items():
        normalized = normalize_skill_name(key)
        combined[normalized] += value
        combined_interactive[normalized] += value
    for key, value in data.get("headless_skills", Counter()).items():
        normalized = normalize_skill_name(key)
        combined[normalized] += value
        combined_headless[normalized] += value
    for key, projects in data.get("skill_projects", {}).items():
        normalized = normalize_skill_name(key)
        combined_projects[normalized].update(projects)

    return {
        "combined": combined,
        "interactive": combined_interactive,
        "headless": combined_headless,
        "projects": combined_projects,
    }


def top_counter_items(counter, limit):
    """Return the most common items from a counter-like object."""
    return Counter(counter or {}).most_common(limit)


def format_counter_overview(counter, limit=5):
    """Short textual summary for counter distributions."""
    items = top_counter_items(counter, limit)
    return ", ".join(f"{name} ({format_number(count)})" for name, count in items) if items else "n/a"


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


def top_usage_entries(data, bucket, key="top_by_usage", limit=8):
    """Return compact usage inventory entries for executive tables."""
    usage_inventory = data.get("usage_inventory", {})
    entries = usage_inventory.get(bucket, {}).get(key, []) or []
    return entries[:limit]


def render_html_table(headers, rows, table_class="data-table"):
    """Render a simple HTML table."""
    head_html = "".join(f"<th>{html.escape(str(header))}</th>" for header in headers)
    body_rows = [
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        for row in rows
    ]
    return (
        f'<table class="{table_class}">'
        f"<thead><tr>{head_html}</tr></thead>"
        f"<tbody>{''.join(body_rows)}</tbody>"
        "</table>"
    )


def render_html_stat_cards(items):
    """Render a grid of executive stat cards."""
    cards = []
    for label, value, tone in items:
        cards.append(
            f'<article class="stat-card tone-{html.escape(tone)}">'
            f'<div class="stat-label">{html.escape(str(label))}</div>'
            f'<div class="stat-value">{html.escape(str(value))}</div>'
            "</article>"
        )
    return f'<div class="stats-grid">{"".join(cards)}</div>'


def render_html_section(title, body, subtitle=""):
    """Wrap report blocks in a consistent HTML section shell."""
    subtitle_html = f'<p class="section-subtitle">{html.escape(subtitle)}</p>' if subtitle else ""
    return (
        '<section class="report-section">'
        f'<div class="section-header"><h2>{html.escape(title)}</h2>{subtitle_html}</div>'
        f'<div class="section-body">{body}</div>'
        "</section>"
    )


def render_html_kv_grid(items):
    """Render a definition-style grid."""
    entries = []
    for label, value in items:
        entries.append(
            '<div class="kv-item">'
            f'<div class="kv-label">{html.escape(str(label))}</div>'
            f'<div class="kv-value">{html.escape(str(value))}</div>'
            "</div>"
        )
    return f'<div class="kv-grid">{"".join(entries)}</div>'


def load_asset(path):
    """Load a text asset from disk."""
    return path.read_text(encoding="utf-8")


def fill_template(template_text, replacements):
    """Replace `{{TOKEN}}` placeholders in a template string."""
    result = template_text
    for key, value in replacements.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result


REPORT_SCRIPT = """
function copyDataText(button) {
  const text = button.dataset.copyText || '';
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {
    const original = button.textContent;
    button.textContent = 'Copiado';
    button.classList.add('copied');
    window.setTimeout(() => {
      button.textContent = original;
      button.classList.remove('copied');
    }, 1400);
  });
}

function copyChecked(selector, button) {
  const items = Array.from(document.querySelectorAll(selector))
    .filter((input) => input.checked)
    .map((input) => input.dataset.copyText || '')
    .filter(Boolean);
  if (!items.length) return;
  navigator.clipboard.writeText(items.join('\\n\\n')).then(() => {
    const original = button.textContent;
    button.textContent = 'Copiado';
    button.classList.add('copied');
    window.setTimeout(() => {
      button.textContent = original;
      button.classList.remove('copied');
    }, 1400);
  });
}

function toggleCollapsible(header) {
  const content = header.nextElementSibling;
  if (!content) return;
  const isOpen = content.classList.toggle('open');
  header.classList.toggle('open', isOpen);
}
"""


def render_nav_toc(items):
    """Render the narrative navigation anchors."""
    links = [
        f'<a href="#{html.escape(anchor)}">{html.escape(label)}</a>'
        for anchor, label in items
    ]
    return f'<nav class="nav-toc">{"".join(links)}</nav>'


def render_bar_rows(items, color):
    """Render simple horizontal bar rows."""
    if not items:
        return '<p class="muted">Sem dados suficientes.</p>'
    max_value = max(value for _, value in items) or 1
    rows = []
    for label, value in items:
        pct = (value / max_value) * 100 if max_value else 0
        rows.append(
            '<div class="bar-row">'
            f'<div class="bar-label">{html.escape(str(label))}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct}%;background:{html.escape(color)}"></div></div>'
            f'<div class="bar-value">{html.escape(format_number(value))}</div>'
            '</div>'
        )
    return "".join(rows)


def bucket_message_hours(message_hours):
    """Group message timestamps into broad day periods."""
    buckets = [
        ("Manhã", range(6, 12)),
        ("Tarde", range(12, 18)),
        ("Noite", range(18, 24)),
        ("Madrugada", range(0, 6)),
    ]
    hour_counts = Counter(message_hours or [])
    return [
        (label, sum(hour_counts.get(hour, 0) for hour in hours))
        for label, hours in buckets
    ]


def render_chart_card(title, items, color):
    """Render a small chart card."""
    return (
        '<article class="chart-card">'
        f'<div class="chart-title">{html.escape(title)}</div>'
        f'{render_bar_rows(items, color)}'
        '</article>'
    )


def render_copyable_code(text, button_label="Copy", row_class="prompt-row", code_class="prompt-code"):
    """Render copyable prompt/code blocks."""
    clean = str(text or "").strip()
    if not clean:
        return ""
    escaped_attr = html.escape(clean, quote=True)
    return (
        f'<div class="{row_class}">'
        f'<code class="{code_class}">{html.escape(clean)}</code>'
        f'<button class="copy-btn" data-copy-text="{escaped_attr}" onclick="copyDataText(this)">{html.escape(button_label)}</button>'
        '</div>'
    )


def render_at_a_glance(narrative):
    """Render the 4-part executive glance section."""
    sections = narrative.get("at_a_glance_sections", {}) or {}
    labels = {
        "whats_working": ("O que está funcionando", "section-wins"),
        "whats_hindering": ("O que está atrapalhando", "section-friction"),
        "quick_wins": ("Quick wins", "section-features"),
        "ambitious_workflows": ("Workflows ambiciosos", "section-horizon"),
    }
    cards = []
    for key, (label, target) in labels.items():
        text = str(sections.get(key, "")).strip()
        if not text:
            continue
        cards.append(
            '<article class="glance-card">'
            f'<div class="glance-label">{html.escape(label)}</div>'
            f'<p>{html.escape(text)}</p>'
            f'<a class="see-more" href="#{html.escape(target)}">Ver seção →</a>'
            '</article>'
        )
    if not cards:
        fallback = str(narrative.get("at_a_glance", "")).strip()
        if not fallback:
            return ""
        cards.append(
            '<article class="glance-card full">'
            '<div class="glance-label">Resumo</div>'
            f'<p>{html.escape(fallback)}</p>'
            '</article>'
        )
    return (
        '<div class="at-a-glance">'
        '<div class="glance-title">At a Glance</div>'
        f'<div class="glance-grid">{"".join(cards)}</div>'
        '</div>'
    )


def format_html(data, days, project_roots=None, discover_inventory_fn=None, get_recent_commits_fn=None):
    """Render the report as a standalone executive HTML page."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    summary = data.get("summary", {})
    facet_summary = data.get("facet_summary", {})
    narrative = data.get("narrative", {})
    recommendations = data.get("recommendations", {})
    skill_rollup = build_skill_rollup(data)

    project_rows = []
    for name, project in sorted(
        data.get("projects", {}).items(),
        key=lambda item: -(item[1].get("interactive", 0) + item[1].get("headless", 0) + item[1].get("subagents", 0)),
    ):
        project_rows.append([
            f"<strong>{html.escape(name)}</strong>",
            html.escape(format_number(project.get("interactive", 0))),
            html.escape(format_number(project.get("headless", 0))),
            html.escape(format_number(project.get("subagents", 0))),
            html.escape(project.get("date_range", "unknown")),
            html.escape(format_number(project.get("input_tokens", 0))),
            html.escape(format_number(project.get("output_tokens", 0))),
            html.escape(format_number(project.get("tool_errors", 0))),
        ])
    if not project_rows:
        project_rows.append([
            "<em>Nenhum projeto no período</em>",
            "0", "0", "0", "unknown", "0", "0", "0",
        ])

    metrics_grid = render_html_kv_grid([
        ("Arquivos de sessão", format_number(summary.get("total_session_files", 0))),
        ("Sessões escaneadas", format_number(summary.get("total_sessions_scanned", summary.get("total_session_files", 0)))),
        ("Meta-sessões excluídas", format_number(summary.get("excluded_meta_sessions", 0))),
        ("Não substantivas excluídas", format_number(summary.get("excluded_non_substantive_sessions", 0))),
        ("Warmup/minimal excluídas", format_number(summary.get("excluded_minimal_facet_sessions", 0))),
        ("Branches deduplicadas", format_number(summary.get("total_branches_deduped", 0))),
        ("Mensagens do usuário", format_number(summary.get("total_user_messages", 0))),
        ("Mensagens do assistant", format_number(summary.get("total_assistant_messages", 0))),
        ("Input tokens", format_number(summary.get("total_input_tokens", 0))),
        ("Output tokens", format_number(summary.get("total_output_tokens", 0))),
        ("Tool errors", format_number(summary.get("total_tool_errors", 0))),
        ("Interrupções", format_number(summary.get("total_user_interruptions", 0))),
        ("Tempo médio de resposta (s)", format_number(summary.get("avg_user_response_seconds", 0))),
        ("Linhas adicionadas", format_number(summary.get("total_lines_added", 0))),
        ("Linhas removidas", format_number(summary.get("total_lines_removed", 0))),
        ("Arquivos modificados", format_number(summary.get("total_unique_files_modified", 0))),
        ("Sessões com MCP", format_number(summary.get("sessions_with_mcp", 0))),
        ("Sessões com task agent", format_number(summary.get("sessions_with_task_agent", 0))),
        ("Cache meta hit/miss", f"{format_number(summary.get('session_meta_cache_hits', 0))}/{format_number(summary.get('session_meta_cache_misses', 0))}"),
        ("Cache facets hit/miss", f"{format_number(summary.get('facets_cache_hits', 0))}/{format_number(summary.get('facets_cache_misses', 0))}"),
    ])

    top_skills_rows = [
        [
            f"<code>{html.escape(skill)}</code>",
            html.escape(format_number(skill_rollup["interactive"].get(skill, 0))),
            html.escape(format_number(skill_rollup["headless"].get(skill, 0))),
            html.escape(", ".join(sorted(skill_rollup["projects"].get(skill, set()))) or "n/a"),
        ]
        for skill, _ in skill_rollup["combined"].most_common(15)
    ] or [["<em>Sem dados</em>", "0", "0", "n/a"]]

    top_tools_rows = [
        [
            f"<code>{html.escape(tool_name)}</code>",
            html.escape(format_number(count)),
            html.escape(", ".join(sorted(data.get("tool_projects", {}).get(tool_name, set()))) or "n/a"),
        ]
        for tool_name, count in top_counter_items(data.get("tools", Counter()), 15)
    ] or [["<em>Sem dados</em>", "0", "n/a"]]

    top_agents_rows = [
        [
            f"<code>{html.escape(agent)}</code>",
            html.escape(format_number(count)),
            html.escape(", ".join(sorted(data.get("agent_projects", {}).get(agent, set()))) or "n/a"),
        ]
        for agent, count in top_counter_items(data.get("agents", Counter()), 15)
    ] or [["<em>Sem dados</em>", "0", "n/a"]]

    top_runners_rows = [
        [f"<code>{html.escape(runner)}</code>", html.escape(format_number(count))]
        for runner, count in top_counter_items(data.get("runners", Counter()), 12)
    ] or [["<em>Sem dados</em>", "0"]]

    usage_inventory = data.get("usage_inventory", {})
    usage_summary = usage_inventory.get("summary", {})
    usage_sections_html = ""
    context_cost_html = ""
    operational_friction_html = ""
    if usage_summary:
        normalized_usage_rows = [
            [
                f"<code>{html.escape(entry['name'])}</code>",
                html.escape(format_number(entry["invocations"])),
                html.escape(format_number(entry["sessions"])),
                html.escape(format_number(entry["projects_count"])),
                html.escape(format_number(entry["associated_lines_changed"])),
                html.escape(f"{format_number(entry['error_session_rate'] * 100)}%"),
            ]
            for entry in top_usage_entries(data, "normalized_skills", "top_by_usage")
        ] or [["<em>Sem dados</em>", "0", "0", "0", "0", "0%"]]

        slash_usage_rows = [
            [
                f"<code>{html.escape(entry['name'])}</code>",
                html.escape(format_number(entry["invocations"])),
                html.escape(format_number(entry["sessions"])),
                html.escape(format_number(entry["interactive_invocations"])),
                html.escape(format_number(entry["headless_invocations"])),
                html.escape(format_number(entry["subagent_invocations"])),
            ]
            for entry in top_usage_entries(data, "slash_commands", "top_by_usage")
        ] or [["<em>Sem dados</em>", "0", "0", "0", "0", "0"]]

        agent_impact_rows = [
            [
                f"<code>{html.escape(entry['name'])}</code>",
                html.escape(format_number(entry["invocations"])),
                html.escape(format_number(entry["sessions"])),
                html.escape(format_number(entry["associated_lines_changed"])),
                html.escape(format_number(entry["associated_files_modified"])),
                html.escape(f"{format_number(entry['error_session_rate'] * 100)}%"),
            ]
            for entry in top_usage_entries(data, "agents", "top_by_impact")
        ] or [["<em>Sem dados</em>", "0", "0", "0", "0", "0%"]]

        context_cost_skill_rows = [
            [
                f"<code>{html.escape(entry['name'])}</code>",
                html.escape(format_number(entry["associated_tokens"])),
                html.escape(format_number(entry.get("avg_associated_tokens_per_session", 0))),
                html.escape(format_number(entry["sessions"])),
                html.escape(format_number(entry["associated_lines_changed"])),
            ]
            for entry in top_usage_entries(data, "normalized_skills", "top_by_context_cost")
        ] or [["<em>Sem dados</em>", "0", "0", "0", "0"]]

        context_cost_tool_rows = [
            [
                f"<code>{html.escape(entry['name'])}</code>",
                html.escape(format_number(entry["associated_tokens"])),
                html.escape(format_number(entry.get("avg_associated_tokens_per_session", 0))),
                html.escape(format_number(entry["sessions"])),
                html.escape(format_number(entry["invocations"])),
            ]
            for entry in top_usage_entries(data, "tools", "top_by_context_cost")
        ] or [["<em>Sem dados</em>", "0", "0", "0", "0"]]

        friction_skill_rows = [
            [
                f"<code>{html.escape(entry['name'])}</code>",
                html.escape(format_number(entry["sessions_with_errors"])),
                html.escape(f"{format_number(entry['error_session_rate'] * 100)}%"),
                html.escape(format_number(entry["sessions"])),
                html.escape(format_number(entry["associated_tokens"])),
            ]
            for entry in top_usage_entries(data, "normalized_skills", "top_by_friction")
        ] or [["<em>Sem dados</em>", "0", "0%", "0", "0"]]

        tool_friction_rows = [
            [
                f"<code>{html.escape(entry['name'])}</code>",
                html.escape(format_number(entry["sessions_with_errors"])),
                html.escape(f"{format_number(entry['error_session_rate'] * 100)}%"),
                html.escape(format_number(entry["invocations"])),
                html.escape(format_number(entry["sessions"])),
                html.escape(format_number(entry["associated_tokens"])),
            ]
            for entry in top_usage_entries(data, "tools", "top_by_friction")
        ] or [["<em>Sem dados</em>", "0", "0%", "0", "0", "0"]]

        usage_sections_html = render_html_section(
            "Inventário Operacional",
            render_html_kv_grid([
                ("Skills normalizadas", format_number(usage_summary.get("normalized_skills", 0))),
                ("Slash commands cruos", format_number(usage_summary.get("slash_commands", 0))),
                ("Skill tool cruos", format_number(usage_summary.get("skill_tools", 0))),
                ("Agents", format_number(usage_summary.get("agents", 0))),
                ("Tools", format_number(usage_summary.get("tools", 0))),
                ("Runners", format_number(usage_summary.get("runners", 0))),
            ])
            + render_html_table(
                ["Skill", "Invocações", "Sessões", "Projetos", "Linhas +/-", "Erro"],
                normalized_usage_rows,
                table_class="compact-table",
            )
            + render_html_table(
                ["Slash", "Invocações", "Sessões", "Interativas", "Headless", "Subagents"],
                slash_usage_rows,
                table_class="compact-table",
            )
            + render_html_table(
                ["Agent", "Invocações", "Sessões", "Linhas +/-", "Arquivos", "Erro"],
                agent_impact_rows,
                table_class="compact-table",
            )
            ,
            subtitle="Camada determinística de adoção e impacto observado por entidade.",
        )

        context_cost_html = render_html_section(
            "Custo de Contexto",
            render_html_table(
                ["Skill", "Tokens assoc.", "Média tokens/sessão", "Sessões", "Linhas +/-"],
                context_cost_skill_rows,
                table_class="compact-table",
            )
            + render_html_table(
                ["Tool", "Tokens assoc.", "Média tokens/sessão", "Sessões", "Invocações"],
                context_cost_tool_rows,
                table_class="compact-table",
            ),
            subtitle="Leitura de custo baseada em tokens associados, não em valor econômico inferido.",
        )

        operational_friction_html = render_html_section(
            "Fricção Operacional",
            render_html_table(
                ["Skill", "Sessões c/ erro", "Erro", "Sessões", "Tokens assoc."],
                friction_skill_rows,
                table_class="compact-table",
            )
            + render_html_table(
                ["Tool", "Sessões c/ erro", "Erro", "Invocações", "Sessões", "Tokens assoc."],
                tool_friction_rows,
                table_class="compact-table",
            ),
            subtitle="Leitura de fricção baseada em erro observado e custo contextual associado.",
        )

    facets_body = render_html_kv_grid([
        ("Fontes", format_counter_overview(facet_summary.get("sources", Counter()))),
        ("Goal Categories", format_counter_overview(facet_summary.get("goal_categories", Counter()))),
        ("Outcomes", format_counter_overview(facet_summary.get("outcomes", Counter()))),
        ("Satisfaction", format_counter_overview(facet_summary.get("satisfaction", Counter()))),
        ("Friction Points", format_counter_overview(facet_summary.get("friction_points", Counter()))),
    ])

    insight_stats_html = (
        '<div class="stats-row">'
        f'<div class="stat"><div class="stat-value">{html.escape(format_number(summary.get("total_sessions", 0)))}</div><div class="stat-label">Sessões</div></div>'
        f'<div class="stat"><div class="stat-value">{html.escape(format_number(summary.get("days_active", 0)))}</div><div class="stat-label">Dias ativos</div></div>'
        f'<div class="stat"><div class="stat-value">{html.escape(format_number(summary.get("messages_per_day", 0)))}</div><div class="stat-label">Msgs/dia</div></div>'
        f'<div class="stat"><div class="stat-value">{html.escape(format_number(summary.get("git_commits", 0)))}</div><div class="stat-label">Git commits</div></div>'
        f'<div class="stat"><div class="stat-value">{html.escape(format_number(summary.get("git_pushes", 0)))}</div><div class="stat-label">Git pushes</div></div>'
        '</div>'
    )

    project_area_items = narrative.get("project_area_items", []) or []
    project_areas_html = ""
    if project_area_items:
        cards = []
        for area in project_area_items:
            cards.append(
                '<article class="project-area">'
                '<div class="area-header">'
                f'<span class="area-name">{html.escape(area.get("name", ""))}</span>'
                f'<span class="area-count">~{html.escape(format_number(area.get("session_count", 0)))} sessões</span>'
                '</div>'
                f'<div class="area-desc">{html.escape(area.get("description", ""))}</div>'
                '</article>'
            )
        project_areas_html = (
            '<div id="section-work" class="insight-block">'
            '<h3>What You Work On</h3>'
            f'<div class="project-areas">{"".join(cards)}</div>'
            '</div>'
        )

    chart_cards = [
        render_chart_card(
            "Goal Categories",
            Counter(facet_summary.get("goal_categories", {})).most_common(6),
            "#0d6c74",
        ),
        render_chart_card(
            "Top Tools",
            Counter(data.get("tools", Counter())).most_common(6),
            "#b06c1d",
        ),
        render_chart_card(
            "Hora do Dia",
            bucket_message_hours(summary.get("message_hours", [])),
            "#9c4325",
        ),
        render_chart_card(
            "Linguagens",
            Counter(summary.get("languages", {})).most_common(6),
            "#355070",
        ),
    ]
    charts_html = f'<div class="charts-row">{"".join(chart_cards)}</div>'

    interaction_html = ""
    interaction_text = str(narrative.get("interaction_style", "")).strip()
    if interaction_text:
        interaction_html = (
            '<div id="section-usage" class="insight-block">'
            '<h3>How You Use Claude Code</h3>'
            f'<div class="narrative prose-block"><p>{html.escape(interaction_text)}</p></div>'
            '</div>'
        )

    what_works_html = ""
    what_works_items = narrative.get("what_works_items", []) or []
    if what_works_items or str(narrative.get("what_works", "")).strip():
        cards = []
        for item in what_works_items:
            cards.append(
                '<article class="big-win">'
                f'<div class="big-win-title">{html.escape(item.get("title", ""))}</div>'
                f'<div class="big-win-desc">{html.escape(item.get("description", ""))}</div>'
                '</article>'
            )
        if not cards:
            cards.append(
                '<article class="big-win">'
                '<div class="big-win-title">O Que Está Funcionando</div>'
                f'<div class="big-win-desc">{html.escape(str(narrative.get("what_works", "")))}</div>'
                '</article>'
            )
        what_works_html = (
            '<div id="section-wins" class="insight-block">'
            '<h3>O Que Está Funcionando</h3>'
            f'<div class="big-wins">{"".join(cards)}</div>'
            '</div>'
        )

    friction_cards = []
    for category in narrative.get("friction_categories", []) or []:
        examples = category.get("examples", []) or []
        friction_cards.append(
            '<article class="friction-category">'
            f'<div class="friction-title">{html.escape(category.get("category", ""))}</div>'
            f'<div class="friction-desc">{html.escape(category.get("description", ""))}</div>'
            + (
                f'<ul class="friction-examples">{"".join(f"<li>{html.escape(example)}</li>" for example in examples)}</ul>'
                if examples else ""
            )
            + '</article>'
        )
    if not friction_cards and str(narrative.get("friction_analysis", "")).strip():
        friction_cards.append(
            '<article class="friction-category">'
            '<div class="friction-title">Análise de Fricção</div>'
            f'<div class="friction-desc">{html.escape(str(narrative.get("friction_analysis", "")))}</div>'
            '</article>'
        )
    friction_story_html = ""
    if friction_cards:
        friction_story_html = (
            '<div id="section-friction" class="insight-block">'
            '<h3>Where Things Go Wrong</h3>'
            f'<div class="friction-categories">{"".join(friction_cards)}</div>'
            '</div>'
        )

    features_html = ""
    claude_md_items = narrative.get("claude_md_additions", []) or []
    features_to_try = narrative.get("features_to_try", []) or []
    usage_patterns = narrative.get("usage_patterns", []) or []
    if claude_md_items or features_to_try or usage_patterns:
        blocks = []
        if claude_md_items:
            md_rows = []
            for index, item in enumerate(claude_md_items):
                scaffold = item.get("prompt_scaffold") or "Adicionar em CLAUDE.md"
                copy_text = f"{scaffold}\n\n{item.get('addition', '')}".strip()
                md_rows.append(
                    '<div class="claude-md-item">'
                    f'<input class="claude-md-checkbox" type="checkbox" checked data-copy-text="{html.escape(copy_text, quote=True)}" id="claude-md-{index}">'
                    f'<label for="claude-md-{index}" class="claude-md-label"><code>{html.escape(item.get("addition", ""))}</code></label>'
                    f'<button class="copy-btn" data-copy-text="{html.escape(copy_text, quote=True)}" onclick="copyDataText(this)">Copy</button>'
                    f'<div class="cmd-why">{html.escape(item.get("why", ""))}</div>'
                    '</div>'
                )
            blocks.append(
                '<div class="claude-md-section">'
                '<div class="subsection-header">'
                '<h4>Sugestões de CLAUDE.md</h4>'
                '<button class="copy-all-btn" onclick="copyChecked(\'.claude-md-checkbox\', this)">Copy All Checked</button>'
                '</div>'
                f'{"".join(md_rows)}'
                '</div>'
            )
        if features_to_try:
            feature_cards = []
            for item in features_to_try:
                feature_cards.append(
                    '<article class="feature-card">'
                    f'<div class="feature-title">{html.escape(item.get("feature", ""))}</div>'
                    f'<div class="feature-oneliner">{html.escape(item.get("one_liner", ""))}</div>'
                    f'<div class="feature-why">{html.escape(item.get("why_for_you", ""))}</div>'
                    f'{render_copyable_code(item.get("example_code", ""))}'
                    '</article>'
                )
            blocks.append(f'<div class="features-section">{"".join(feature_cards)}</div>')
        patterns_html = ""
        if usage_patterns:
            pattern_cards = []
            for item in usage_patterns:
                pattern_cards.append(
                    '<article class="pattern-card">'
                    f'<div class="pattern-title">{html.escape(item.get("title", ""))}</div>'
                    f'<div class="pattern-summary">{html.escape(item.get("suggestion", ""))}</div>'
                    f'<div class="pattern-detail">{html.escape(item.get("detail", ""))}</div>'
                    f'{render_copyable_code(item.get("copyable_prompt", ""))}'
                    '</article>'
                )
            patterns_html = f'<div id="section-patterns" class="insight-block"><h3>New Ways to Use Claude Code</h3><div class="patterns-section">{"".join(pattern_cards)}</div></div>'

        features_html = (
            '<div id="section-features" class="insight-block">'
            '<h3>Existing CC Features to Try</h3>'
            f'{"".join(blocks)}'
            '</div>'
            + patterns_html
        )

    horizon_html = ""
    horizon_cards = []
    for item in narrative.get("horizon_opportunities", []) or []:
        horizon_cards.append(
            '<article class="horizon-card">'
            f'<div class="horizon-title">{html.escape(item.get("title", ""))}</div>'
            f'<div class="horizon-possible">{html.escape(item.get("whats_possible", ""))}</div>'
            f'<div class="horizon-tip">{html.escape(item.get("how_to_try", ""))}</div>'
            f'{render_copyable_code(item.get("copyable_prompt", ""))}'
            '</article>'
        )
    if not horizon_cards and str(narrative.get("on_the_horizon", "")).strip():
        horizon_cards.append(
            '<article class="horizon-card">'
            '<div class="horizon-title">No Horizonte</div>'
            f'<div class="horizon-possible">{html.escape(str(narrative.get("on_the_horizon", "")))}</div>'
            '</article>'
        )
    if horizon_cards:
        horizon_html = (
            '<div id="section-horizon" class="insight-block">'
            '<h3>On the Horizon</h3>'
            f'<div class="horizon-section">{"".join(horizon_cards)}</div>'
            '</div>'
        )

    feedback_cards = []
    feedback = narrative.get("feedback", {}) or {}
    cc_feedback = feedback.get("cc_team_improvements", []) or []
    model_feedback = feedback.get("model_behavior_improvements", []) or []
    if cc_feedback:
        cards = "".join(
            '<article class="feedback-card team-card">'
            f'<div class="feedback-title">{html.escape(item.get("title", ""))}</div>'
            f'<div class="feedback-detail">{html.escape(item.get("detail", ""))}</div>'
            f'<div class="feedback-evidence">{html.escape(item.get("evidence", ""))}</div>'
            '</article>'
            for item in cc_feedback
        )
        feedback_cards.append(
            '<div class="collapsible-section">'
            '<div class="collapsible-header" onclick="toggleCollapsible(this)"><span class="collapsible-arrow">▶</span><h4>Feedback para produto</h4></div>'
            f'<div class="collapsible-content">{cards}</div>'
            '</div>'
        )
    if model_feedback:
        cards = "".join(
            '<article class="feedback-card model-card">'
            f'<div class="feedback-title">{html.escape(item.get("title", ""))}</div>'
            f'<div class="feedback-detail">{html.escape(item.get("detail", ""))}</div>'
            f'<div class="feedback-evidence">{html.escape(item.get("evidence", ""))}</div>'
            '</article>'
            for item in model_feedback
        )
        feedback_cards.append(
            '<div class="collapsible-section">'
            '<div class="collapsible-header" onclick="toggleCollapsible(this)"><span class="collapsible-arrow">▶</span><h4>Feedback para comportamento de modelo</h4></div>'
            f'<div class="collapsible-content">{cards}</div>'
            '</div>'
        )
    feedback_html = ""
    if feedback_cards:
        feedback_html = (
            '<div id="section-feedback" class="insight-block">'
            '<h3>Closing the Loop</h3>'
            f'{"".join(feedback_cards)}'
            '</div>'
        )

    fun_ending_card = narrative.get("fun_ending_card", {}) or {}
    fun_ending_html = ""
    if fun_ending_card.get("headline") or narrative.get("fun_ending"):
        fun_ending_html = (
            '<div class="insight-block">'
            '<h3>Fechamento</h3>'
            '<div class="fun-ending">'
            f'<div class="fun-headline">{html.escape(fun_ending_card.get("headline") or narrative.get("fun_ending", ""))}</div>'
            f'<div class="fun-detail">{html.escape(fun_ending_card.get("detail", ""))}</div>'
            '</div></div>'
        )

    insights_nav = render_nav_toc([
        ("section-work", "What You Work On"),
        ("section-usage", "How You Use CC"),
        ("section-wins", "O Que Está Funcionando"),
        ("section-friction", "Where Things Go Wrong"),
        ("section-features", "Features to Try"),
        ("section-patterns", "New Usage Patterns"),
        ("section-horizon", "On the Horizon"),
        ("section-feedback", "Feedback"),
        ("section-operations", "Inventário Operacional"),
    ])

    insights_body = (
        render_at_a_glance(narrative)
        + insights_nav
        + insight_stats_html
        + project_areas_html
        + charts_html
        + interaction_html
        + what_works_html
        + friction_story_html
        + features_html
        + horizon_html
        + feedback_html
        + fun_ending_html
    )

    recommendation_cards = []
    for recommendation in recommendations.get("top_recommendations", []):
        scope_label = recommendation.get("project") or "global"
        recommendation_cards.append(
            '<article class="narrative-card recommendation-card">'
            f'<div class="rec-meta"><span class="rec-badge">{html.escape(recommendation.get("impact", ""))}</span>'
            f'<span class="rec-scope">{html.escape(scope_label)}</span></div>'
            f'<h3>{html.escape(recommendation.get("title", ""))}</h3>'
            f'<p>{html.escape(recommendation.get("description", ""))}</p>'
            f'<p class="rec-detail"><strong>Fase:</strong> {html.escape(recommendation.get("phase", ""))}</p>'
            f'<p class="rec-detail"><strong>Ganho estimado:</strong> {html.escape(format_number(recommendation.get("estimated_minutes_saved_per_week", 0)))} min/semana</p>'
            f'<p class="rec-detail"><strong>Passos:</strong> {html.escape("; ".join(recommendation.get("implementation_steps", [])))}</p>'
            "</article>"
        )
    recommendations_html = (
        f'<div class="narrative-grid">{"".join(recommendation_cards)}</div>'
        if recommendation_cards else '<p class="muted">Sem recomendações calculadas.</p>'
    )

    project_recommendation_rows = [
        [
            f"<strong>{html.escape(project_name)}</strong>",
            html.escape(format_number(len(items))),
            html.escape(items[0]["title"] if items else "n/a"),
        ]
        for project_name, items in sorted(
            recommendations.get("by_project", {}).items(),
            key=lambda item: -len(item[1]),
        )
    ] or [["<em>Sem recomendações por projeto</em>", "0", "n/a"]]

    inventory_sections = []
    if project_roots and discover_inventory_fn and get_recent_commits_fn:
        for root_label, root_path in project_roots.items():
            inventory = discover_inventory_fn(root_path)
            all_used = set()
            for key in skill_rollup["combined"]:
                clean = normalize_skill_name(key).split(":")[0]
                all_used.add(clean)
                all_used.add(normalize_skill_name(key))

            unused_skills = [skill for skill in inventory["skills"] if skill not in all_used][:20]
            used_agent_types = set(data.get("agents", Counter()).keys())
            unused_agents = [agent for agent in inventory["agents"] if agent not in used_agent_types][:20]
            commit_rows = [
                [html.escape(area), html.escape(format_number(count))]
                for area, count in sorted(get_recent_commits_fn(root_path, days).items(), key=lambda item: -item[1])[:10]
            ]

            inventory_body = render_html_kv_grid([
                ("Skills nunca usados", ", ".join(unused_skills) or "n/a"),
                ("Agents nunca usados", ", ".join(unused_agents) or "n/a"),
            ])
            if commit_rows:
                inventory_body += render_html_table(["Área", "Commits"], commit_rows, table_class="compact-table")
            inventory_sections.append(
                render_html_section(
                    f"Inventário e Commits: {root_label}",
                    inventory_body,
                    subtitle="Resumo executivo do inventário local e sinais de git.",
                )
            )

    sections = [
        render_html_section(
            "Panorama",
            render_html_stat_cards([
                ("Sessões", format_number(summary.get("total_sessions", 0)), "ink"),
                ("Subagents", format_number(summary.get("total_subagents", 0)), "teal"),
                ("Tokens", f"{format_number(summary.get('total_input_tokens', 0))}/{format_number(summary.get('total_output_tokens', 0))}", "amber"),
                ("Tool Errors", format_number(summary.get("total_tool_errors", 0)), "rust"),
            ]),
            subtitle=f"Últimos {days} dias, gerado em {now}.",
        ),
        render_html_section(
            "Insights Narrativos",
            insights_body or '<p class="muted">Sem narrativa disponível.</p>',
            subtitle=f"Camada qualitativa com fonte {html.escape(str(narrative.get('source', 'deterministic')))}.",
        ),
        render_html_section(
            "Projetos",
            render_html_table(
                ["Projeto", "Interativas", "Headless", "Subagents", "Date Range", "Tokens In", "Tokens Out", "Tool Errors"],
                project_rows,
            ),
            subtitle="Visão consolidada por projeto.",
        ),
        render_html_section(
            "Métricas de Sessão",
            metrics_grid,
            subtitle="KPIs determinísticos extraídos das transcripts.",
        ),
        render_html_section(
            "Top Skills",
            render_html_table(["Skill/Command", "Interativas", "Headless", "Projetos"], top_skills_rows),
            subtitle="Normalização de slash commands + Skill tool.",
        ),
        render_html_section(
            "Top Tools",
            render_html_table(["Tool", "Invocações", "Projetos"], top_tools_rows),
            subtitle="Ferramentas mais frequentes no período.",
        ),
        (
            usage_sections_html.replace(
                '<section class="report-section">',
                '<section id="section-operations" class="report-section">',
                1,
            )
            if usage_sections_html else ""
        ),
        context_cost_html,
        operational_friction_html,
        render_html_section(
            "Top Agents e Runners",
            render_html_table(["Agent", "Invocações", "Projetos"], top_agents_rows)
            + render_html_table(["Runner", "Invocações"], top_runners_rows, table_class="compact-table"),
            subtitle="Subagents e scripts shell mais recorrentes.",
        ),
        render_html_section(
            "Facets",
            facets_body,
            subtitle=f"Fonte predominante: {html.escape(str(narrative.get('source', 'deterministic')))}.",
        ),
        render_html_section(
            "Recomendações Acionáveis",
            render_html_stat_cards([
                ("Total", recommendations.get("summary", {}).get("total_recommendations", 0), "ink"),
                ("Alto impacto", format_number(recommendations.get("summary", {}).get("high_impact", 0)), "rust"),
                ("Quick Wins", format_number(recommendations.get("summary", {}).get("quick_wins", 0)), "teal"),
                (
                    "Ganho semanal",
                    f"{format_number(recommendations.get('summary', {}).get('estimated_minutes_saved_per_week', 0))} min",
                    "amber",
                ),
            ]) + recommendations_html + render_html_table(
                ["Projeto", "Recomendações", "Top Item"],
                project_recommendation_rows,
                table_class="compact-table",
            ),
            subtitle="Itens priorizados para o workflow optimize-workflow consumir diretamente.",
        ),
    ]
    sections = [section for section in sections if section]
    sections.extend(inventory_sections)

    return fill_template(load_asset(HTML_TEMPLATE_PATH), {
        "TITLE": "Claude Code Session Usage Report",
        "STYLES": load_asset(CSS_TEMPLATE_PATH),
        "SCRIPT": REPORT_SCRIPT,
        "DAYS": html.escape(str(days)),
        "GENERATED_AT": html.escape(now),
        "NARRATIVE_SOURCE": html.escape(str(narrative.get("source", "deterministic"))),
        "SECTIONS": "".join(sections),
    })

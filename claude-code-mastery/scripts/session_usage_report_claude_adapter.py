#!/usr/bin/env python3
"""
Claude-backed insights adapter for session-usage-report.py.

Reads JSON from stdin and returns JSON to stdout. Uses `claude -p` with
structured output schemas so the report can generate real LLM-driven sections.
"""
import argparse
import json
import subprocess
import sys


SUMMARY_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
    },
    "required": ["summary"],
    "additionalProperties": False,
}

FACET_SCHEMA = {
    "type": "object",
    "properties": {
        "underlying_goal": {"type": "string"},
        "goal_categories": {"type": "array", "items": {"type": "string"}},
        "outcome": {"type": "string"},
        "satisfaction": {"type": "string"},
        "friction_points": {"type": "array", "items": {"type": "string"}},
        "primary_success": {"type": "string"},
        "brief_summary": {"type": "string"},
    },
    "required": [
        "underlying_goal",
        "goal_categories",
        "outcome",
        "satisfaction",
        "friction_points",
        "primary_success",
        "brief_summary",
    ],
    "additionalProperties": False,
}

INSIGHT_SECTIONS_SCHEMA = {
    "type": "object",
    "properties": {
        "at_a_glance_sections": {
            "type": "object",
            "properties": {
                "whats_working": {"type": "string"},
                "whats_hindering": {"type": "string"},
                "quick_wins": {"type": "string"},
                "ambitious_workflows": {"type": "string"},
            },
            "required": [
                "whats_working",
                "whats_hindering",
                "quick_wins",
                "ambitious_workflows",
            ],
            "additionalProperties": False,
        },
        "project_area_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "session_count": {"type": "integer"},
                    "description": {"type": "string"},
                },
                "required": ["name", "session_count", "description"],
                "additionalProperties": False,
            },
        },
        "interaction_style": {"type": "string"},
        "what_works_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["title", "description"],
                "additionalProperties": False,
            },
        },
        "friction_categories": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "description": {"type": "string"},
                    "examples": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["category", "description", "examples"],
                "additionalProperties": False,
            },
        },
        "claude_md_additions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "addition": {"type": "string"},
                    "why": {"type": "string"},
                    "prompt_scaffold": {"type": "string"},
                },
                "required": ["addition", "why", "prompt_scaffold"],
                "additionalProperties": False,
            },
        },
        "features_to_try": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "feature": {"type": "string"},
                    "one_liner": {"type": "string"},
                    "why_for_you": {"type": "string"},
                    "example_code": {"type": "string"},
                },
                "required": ["feature", "one_liner", "why_for_you", "example_code"],
                "additionalProperties": False,
            },
        },
        "usage_patterns": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "suggestion": {"type": "string"},
                    "detail": {"type": "string"},
                    "copyable_prompt": {"type": "string"},
                },
                "required": ["title", "suggestion", "detail", "copyable_prompt"],
                "additionalProperties": False,
            },
        },
        "on_the_horizon": {"type": "string"},
        "horizon_opportunities": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "whats_possible": {"type": "string"},
                    "how_to_try": {"type": "string"},
                    "copyable_prompt": {"type": "string"},
                },
                "required": ["title", "whats_possible", "how_to_try", "copyable_prompt"],
                "additionalProperties": False,
            },
        },
        "feedback": {
            "type": "object",
            "properties": {
                "cc_team_improvements": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "detail": {"type": "string"},
                            "evidence": {"type": "string"},
                        },
                        "required": ["title", "detail", "evidence"],
                        "additionalProperties": False,
                    },
                },
                "model_behavior_improvements": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "detail": {"type": "string"},
                            "evidence": {"type": "string"},
                        },
                        "required": ["title", "detail", "evidence"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["cc_team_improvements", "model_behavior_improvements"],
            "additionalProperties": False,
        },
        "fun_ending_card": {
            "type": "object",
            "properties": {
                "headline": {"type": "string"},
                "detail": {"type": "string"},
            },
            "required": ["headline", "detail"],
            "additionalProperties": False,
        },
    },
    "required": [
        "at_a_glance_sections",
        "project_area_items",
        "interaction_style",
        "what_works_items",
        "friction_categories",
        "claude_md_additions",
        "features_to_try",
        "usage_patterns",
        "on_the_horizon",
        "horizon_opportunities",
        "feedback",
        "fun_ending_card",
    ],
    "additionalProperties": False,
}


def parse_args():
    """Parse CLI args for the adapter."""
    parser = argparse.ArgumentParser(description="Claude-backed insights adapter")
    parser.add_argument("--claude-bin", default="claude", help="Claude CLI binary")
    parser.add_argument("--model", default="sonnet", help="Model alias/name passed to Claude CLI")
    parser.add_argument("--effort", default="medium", choices=["low", "medium", "high", "max"], help="Claude effort level")
    parser.add_argument("--max-budget-usd", default="", help="Optional max budget passed through to Claude CLI")
    parser.add_argument("--append-system-prompt", default="", help="Optional system prompt suffix")
    return parser.parse_args()


def parse_json_object(text):
    """Parse JSON even if the model wraps it in incidental text."""
    stripped = str(text or "").strip()
    if not stripped:
        return {}
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(stripped[start:end + 1])
        raise


def run_claude(claude_bin, model, effort, prompt, schema, max_budget_usd="", append_system_prompt=""):
    """Invoke `claude -p` with structured output."""
    command = [
        claude_bin,
        "-p",
        "--model",
        model,
        "--effort",
        effort,
        "--tools",
        "",
        "--permission-mode",
        "dontAsk",
        "--no-session-persistence",
        "--json-schema",
        json.dumps(schema, ensure_ascii=False),
    ]
    if max_budget_usd:
        command.extend(["--max-budget-usd", str(max_budget_usd)])
    if append_system_prompt:
        command.extend(["--append-system-prompt", append_system_prompt])
    command.append(prompt)
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        stderr_text = (completed.stderr or completed.stdout or "").strip()
        raise RuntimeError(stderr_text or f"Claude command failed with exit code {completed.returncode}")
    return parse_json_object(completed.stdout)


def build_summarize_chunk_prompt(payload):
    """Create a token-light chunk summary prompt."""
    return (
        "Resuma este chunk de transcript de Claude Code em no máximo 8 bullets curtos. "
        "Priorize intenção do usuário, tools relevantes, erros e resultado parcial. "
        "Não invente nada.\n\nCHUNK:\n"
        + str(payload.get("transcript_chunk", "") or "")
    )


def build_facet_prompt(payload):
    """Create a per-session facet prompt."""
    return (
        "Analise esta sessão de Claude Code e extraia facets operacionais. "
        "Seja fiel ao transcript. Use rótulos curtos em goal_categories e friction_points. "
        "Resuma em PT-BR.\n\nPROJECT:\n"
        + str(payload.get("project_name", "") or "unknown")
        + "\n\nSESSION_META:\n"
        + json.dumps(payload.get("session_meta", {}), ensure_ascii=False, indent=2)
        + "\n\nTRANSCRIPT:\n"
        + str(payload.get("transcript", "") or "")
    )


def build_insight_sections_prompt(payload):
    """Create a one-shot prompt for the executive sections."""
    return (
        "Você está gerando um relatório executivo de uso do Claude Code. "
        "Use segunda pessoa quando fizer sentido, mas mantenha tom pragmático. "
        "Não invente números nem fatos ausentes. "
        "Seu objetivo é produzir insights únicos e acionáveis, sem perder o foco operacional.\n\n"
        "Regras importantes:\n"
        "- at_a_glance_sections precisa ter 4 blocos curtos e densos.\n"
        "- project_area_items deve listar 4-5 frentes concretas de trabalho.\n"
        "- what_works_items deve destacar 3 workflows realmente fortes.\n"
        "- friction_categories deve trazer 3 categorias com exemplos concretos.\n"
        "- claude_md_additions deve priorizar instruções que parecem repetidas.\n"
        "- features_to_try deve ser específica para o histórico analisado.\n"
        "- usage_patterns deve trazer prompts/copiable flows que aproveitem o padrão observado.\n"
        "- horizon_opportunities deve ser ambicioso, mas plausível.\n"
        "- feedback pode ficar vazio se a evidência não for forte.\n\n"
        "DATA:\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )


def main():
    """Dispatch adapter modes from stdin JSON."""
    args = parse_args()
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(json.dumps({"error": f"invalid_json: {exc}"}))
        raise SystemExit(1) from exc

    mode = str(payload.get("mode", "") or "").strip()
    if mode == "summarize_chunk":
        response = run_claude(
            args.claude_bin,
            args.model,
            args.effort,
            build_summarize_chunk_prompt(payload),
            SUMMARY_SCHEMA,
            max_budget_usd=args.max_budget_usd,
            append_system_prompt=args.append_system_prompt,
        )
    elif mode == "facet":
        response = run_claude(
            args.claude_bin,
            args.model,
            args.effort,
            build_facet_prompt(payload),
            FACET_SCHEMA,
            max_budget_usd=args.max_budget_usd,
            append_system_prompt=args.append_system_prompt,
        )
    elif mode == "insight_sections":
        response = run_claude(
            args.claude_bin,
            args.model,
            args.effort,
            build_insight_sections_prompt(payload),
            INSIGHT_SECTIONS_SCHEMA,
            max_budget_usd=args.max_budget_usd,
            append_system_prompt=args.append_system_prompt,
        )
    else:
        print(json.dumps({"error": f"unsupported_mode: {mode}"}))
        raise SystemExit(2)

    print(json.dumps(response, ensure_ascii=False))


if __name__ == "__main__":
    main()

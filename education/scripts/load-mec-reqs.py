#!/usr/bin/env python3
"""
MEC Requirements Loader
Replaces LLM-based load-mec-requirements.md task with deterministic file compilation.

Usage:
  python squads/education/scripts/load-mec-reqs.py \
    --category livre \
    --domain "python-fundamentals" \
    --output minds/python-fundamentals/mec-requirements.md
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# MEC Category → Checklist File Mapping
# ─────────────────────────────────────────────────────────────────────────────

SQUAD_ROOT = Path(__file__).parent.parent  # squads/education/

CATEGORY_MAP = {
    "livre": {
        "label": "Curso Livre",
        "checklist": "checklists/mec-curso-livre-check.md",
        "description": "Cursos livres não requerem autorização MEC, mas devem seguir boas práticas.",
    },
    "fic": {
        "label": "Formação Inicial e Continuada (FIC)",
        "checklist": "checklists/mec-curso-livre-check.md",  # FIC uses livre rules + extras
        "description": "Cursos FIC de curta duração (160h+), regidos pela LDB Art. 39-42.",
    },
    "tecnico": {
        "label": "Curso Técnico",
        "checklist": "checklists/mec-curso-tecnico-check.md",
        "description": "Cursos técnicos de nível médio, catalogados no CNCT.",
    },
    "graduacao": {
        "label": "Graduação",
        "checklist": "checklists/mec-graduacao-check.md",
        "description": "Cursos de graduação (bacharelado, licenciatura, tecnólogo).",
    },
    "pos": {
        "label": "Pós-Graduação Lato Sensu",
        "checklist": "checklists/mec-pos-lato-sensu-check.md",
        "description": "Cursos de especialização (360h mínimas).",
    },
    "ead": {
        "label": "Educação a Distância",
        "checklist": "checklists/mec-ead-check.md",
        "description": "Modalidade EaD — aplica-se em conjunto com a categoria do curso.",
    },
}

# Regulated professions that require additional authorization
REGULATED_PROFESSIONS = {
    "medicina": "CFM + MEC",
    "direito": "OAB + MEC",
    "engenharia": "CREA + MEC",
    "psicologia": "CRP + MEC",
    "enfermagem": "COFEN + MEC",
    "odontologia": "CRO + MEC",
    "farmacia": "CRF + MEC",
    "contabilidade": "CRC + MEC",
    "arquitetura": "CAU + MEC",
    "nutricao": "CRN + MEC",
    "veterinaria": "CRMV + MEC",
    "fisioterapia": "CREFITO + MEC",
}


def load_checklist(checklist_path: Path) -> str:
    """Load checklist file content."""
    if not checklist_path.exists():
        return f"*Checklist not found: {checklist_path}*"
    return checklist_path.read_text(encoding="utf-8")


def detect_regulated(domain: str) -> str | None:
    """Check if domain is a regulated profession."""
    domain_lower = domain.lower()
    for profession, authority in REGULATED_PROFESSIONS.items():
        if profession in domain_lower:
            return f"**{profession.title()}** — Requires authorization from: {authority}"
    return None


def render_markdown(
    domain: str,
    category: str,
    cat_info: dict,
    checklist_content: str,
    regulated_info: str | None,
    ead_checklist: str | None,
) -> str:
    """Render the MEC requirements document."""
    lines = [
        f"# MEC Requirements: {domain}",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Category:** {cat_info['label']} (`{category}`)",
        f"**Domain:** {domain}",
        "",
        "---",
        "",
        "## Category Description",
        "",
        cat_info["description"],
        "",
        "---",
        "",
        "## Mandatory Requirements",
        "",
        checklist_content,
        "",
    ]

    if ead_checklist:
        lines += [
            "---",
            "",
            "## EaD Additional Requirements",
            "",
            "*Applies because this course includes distance education modality.*",
            "",
            ead_checklist,
            "",
        ]

    if regulated_info:
        lines += [
            "---",
            "",
            "## Domain-Specific Requirements (Regulated Profession)",
            "",
            regulated_info,
            "",
            "**Additional steps:**",
            "- [ ] Verify institutional authorization with professional council",
            "- [ ] Confirm curriculum meets council-specific guidelines",
            "- [ ] Include council-approved internship requirements",
            "",
        ]
    else:
        lines += [
            "---",
            "",
            "## Domain-Specific Requirements",
            "",
            "No regulated profession detected for this domain.",
            "",
        ]

    # Required documentation per category
    doc_reqs = {
        "livre": [
            "Programa do curso (ementa, carga horária, objetivos)",
            "Material didático",
            "Certificado de conclusão (sem selo MEC)",
        ],
        "fic": [
            "Programa do curso (ementa, carga horária, objetivos)",
            "Material didático",
            "Certificado de qualificação profissional",
        ],
        "tecnico": [
            "PPC (Projeto Pedagógico de Curso)",
            "Autorização institucional",
            "Catálogo CNCT alignment",
            "Corpo docente qualificado",
            "Infraestrutura laboratorial",
            "Diploma de técnico",
        ],
        "graduacao": [
            "PPC (Projeto Pedagógico de Curso)",
            "PDI (Plano de Desenvolvimento Institucional)",
            "Credenciamento MEC",
            "Corpo docente (33% mestres/doutores)",
            "Infraestrutura (biblioteca, laboratórios)",
            "Registro e-MEC",
            "Auto-avaliação SINAES",
        ],
        "pos": [
            "PPC (Projeto Pedagógico de Curso)",
            "Corpo docente (30% mestres/doutores)",
            "Certificado de especialista",
            "Trabalho de conclusão / monografia",
        ],
        "ead": [
            "Credenciamento EaD",
            "Polo presencial (se aplicável)",
            "AVA (Ambiente Virtual de Aprendizagem)",
            "Avaliações presenciais",
        ],
    }

    docs = doc_reqs.get(category, doc_reqs["livre"])
    lines += [
        "---",
        "",
        "## Required Documentation",
        "",
    ]
    for doc in docs:
        lines.append(f"- [ ] {doc}")

    lines += [
        "",
        "---",
        "",
        "## Compliance Checklist (Summary)",
        "",
        "Use this checklist to track compliance before submission:",
        "",
        "- [ ] All mandatory requirements met",
        "- [ ] Domain-specific requirements addressed",
        "- [ ] Required documentation assembled",
        "- [ ] Validation report clean (no FAIL items)",
        f"- [ ] Category-specific checklist passed (`{cat_info['checklist']}`)",
    ]

    if ead_checklist:
        lines.append("- [ ] EaD requirements met (if applicable)")

    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="MEC Requirements Loader — deterministic requirement compilation"
    )
    parser.add_argument(
        "--category",
        required=True,
        choices=list(CATEGORY_MAP.keys()),
        help="MEC course category",
    )
    parser.add_argument("--domain", required=True, help="Course domain name")
    parser.add_argument("--ead", action="store_true", help="Include EaD requirements overlay")
    parser.add_argument("--output", default=None, help="Output path (default: minds/{domain}/mec-requirements.md)")

    args = parser.parse_args()

    cat_info = CATEGORY_MAP[args.category]

    # Load main checklist
    checklist_path = SQUAD_ROOT / cat_info["checklist"]
    checklist_content = load_checklist(checklist_path)
    print(f"Loaded checklist: {checklist_path}")

    # Load EaD overlay if requested
    ead_content = None
    if args.ead and args.category != "ead":
        ead_path = SQUAD_ROOT / "checklists/mec-ead-check.md"
        ead_content = load_checklist(ead_path)
        print(f"Loaded EaD overlay: {ead_path}")

    # Check for regulated profession
    regulated = detect_regulated(args.domain)
    if regulated:
        print(f"Regulated profession detected: {regulated}")

    # Render
    md = render_markdown(
        args.domain, args.category, cat_info, checklist_content, regulated, ead_content
    )

    # Write output
    output_path = args.output or f"minds/{args.domain}/mec-requirements.md"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"MEC requirements written to: {output_path}")


if __name__ == "__main__":
    main()

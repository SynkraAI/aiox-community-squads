# Task: Brand Activation

## Metadata

```yaml
id: brand-activation
name: Brand Activation Operating System
executor: miller-sticky-brand
elicit: true
estimated_duration: "40-90 min"
```

**Responsible Executor:** Agent (@miller-sticky-brand)  
**Dependencies:** depends_on: `[load-workspace-context, positioning-narrative]` · enables: `[wf-brand-activation-system]` · workflow: `wf-brand-activation-system`

## Prerequisites

- **Context Gate (mandatory):** Brand workspace context and positioning must be loaded. If positioning-narrative has not run, HALT and suggest running it first.

## Objective

Transformar estratégia em execução com sistema de identidade, cultura e plano de rollout.

---

## Inputs

- Positioning & Narrative report
- Prioridades de canal
- Equipes envolvidas e prazo

---

## Output

| Artifact | Location | Description |
|---|---|---|
| `activation-30-60-90.md` | `workspace/businesses/{brand_name}/L2-tactical/brand/activation/activation-30-60-90.md` | Plano de ativacao com owners e marcos por janela |
| `activation-system-report.md` | `workspace/businesses/{brand_name}/L2-tactical/brand/activation/activation-system-report.md` | Consolidado de implementacao (identidade + cultura + GTM) |
| `logo-concept.yaml` | `workspace/businesses/{brand_name}/L2-tactical/brand/logo-concept.yaml` | Conceito simbolico inicial alinhado ao posicionamento |

## Veto Conditions

- [ ] Plano 30/60/90 sem owners, prazos e checkpoints claros
- [ ] Ausencia de alinhamento entre identidade externa e rituais internos
- [ ] KPIs sem ligacao com objetivos de awareness/consideration/conversion/retention
- [ ] Recomendacoes sem segmentacao minima (DTC/startup vs SMB/B2B)

## Steps

1. **Wheeler:** desenhar blueprint de identidade e governança.
2. **Yohn (FUSION):** alinhar promessa externa com cultura interna.
3. **Heyward:** plano de marca para aquisição/retensão em startup/DTC.
4. **Miller:** simplificar diferenciação para contexto PME/B2B.
5. Produzir plano 30/60/90 dias com owners e rituais.

---

## Output

```markdown
## Brand Activation Plan

### Identity System
- Guidelines essenciais: {itens}
- Governance: {responsáveis}

### Culture Alignment
- Gaps internos: {itens}
- Rituais e comportamentos: {itens}

### GTM by Segment
- DTC/Startup: {ações}
- SMB/B2B: {ações}

### 30/60/90 Plan
- 30 dias: {ações}
- 60 dias: {ações}
- 90 dias: {ações}

### KPIs
- Awareness: {kpi}
- Consideration: {kpi}
- Conversion: {kpi}
- Retention: {kpi}
```

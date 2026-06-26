# Task: Brand Diagnosis

## Metadata

```yaml
id: brand-diagnosis
name: Brand Foundations Diagnosis
executor: keller-brand-equity
elicit: true
estimated_duration: "30-60 min"
```

**Responsible Executor:** Agent (@keller-brand-equity)  
**Dependencies:** depends_on: `[load-workspace-context]` · enables: `[wf-brand-foundations]` · workflow: `wf-brand-foundations`

## Objective

Construir baseline estratégico de marca usando CBBE (Keller), Brand Vision (Aaker) e Growth lens (Byron Sharp).

---

## Inputs

- `business_context` (contexto de negocio)
- `category` (segmento e frame competitivo principal)
- `target_market` (brasil, latam ou global)
- Evidencias disponiveis (NPS, awareness, retencao, share, etc.)

---

## Output

| Artifact | Location | Description |
|---|---|---|
| `cbbe-report.md` | `workspace/businesses/{brand_name}/L2-tactical/brand/foundations/cbbe-report.md` | Diagnostico CBBE com baseline de equity |
| `foundations-report.md` | `workspace/businesses/{brand_name}/L2-tactical/brand/foundations/foundations-report.md` | Consolidado de fundamentos para handoff das proximas fases |
| `brandbook.yaml` | `workspace/businesses/{brand_name}/L2-tactical/brand/brandbook.yaml` | Estrutura base de identidade e diretrizes estrategicas |

## Veto Conditions

- [ ] Dados insuficientes para pontuar as 6 camadas CBBE com minimo de evidencias
- [ ] Ausencia total de contexto competitivo da categoria
- [ ] Nao foi possivel identificar ao menos 3 gaps prioritarios acionaveis
- [ ] Diagnostico sem recomendacoes para a proxima fase do workflow

## Steps

1. **Keller (CBBE):** avaliar salience, performance, imagery, judgments, feelings e resonance.
2. **Aaker:** definir identidade core/extended e proposta de valor.
3. **Sharp:** mapear mental e physical availability atual.
4. Consolidar gaps e hipóteses estratégicas para próxima fase.

---

## Output

```markdown
## Brand Foundations Report

### CBBE Baseline
- Salience: {score}
- Performance: {score}
- Imagery: {score}
- Judgments: {score}
- Feelings: {score}
- Resonance: {score}

### Brand Vision (Aaker)
- Core identity: {texto}
- Extended identity: {texto}
- Value proposition: {texto}

### Growth Lens (Sharp)
- Mental availability: {status}
- Physical availability: {status}

### Priority Gaps (Top 3)
1. {gap_1}
2. {gap_2}
3. {gap_3}
```

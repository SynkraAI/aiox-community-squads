# Task: Positioning & Narrative

## Metadata

```yaml
id: positioning-narrative
name: Positioning + Messaging System
executor: storybrand-narrator
elicit: true
estimated_duration: "30-70 min"
```

**Responsible Executor:** Agent (@storybrand-narrator)  
**Dependencies:** depends_on: `[load-workspace-context, brand-diagnosis]` · enables: `[wf-brand-positioning-narrative]` · workflow: `wf-brand-positioning-narrative`

## Prerequisites

- **Context Gate (mandatory):** Brand workspace context must be loaded. Run `load-workspace-context` first. If brand foundations (diagnosis) do not exist, HALT and run `brand-diagnosis` first.
- **Vocabulary:** Consult `data/brand-mappings.yaml` for canonical positioning terminology.

## Prerequisites

- **Context Gate (mandatory):** Brand workspace context must be loaded. If brand-diagnosis has not run, HALT and suggest running brand-diagnosis first.
- **Vocabulary:** Consult `data/brand-mappings.yaml` for canonical positioning terminology.

## Objective

Definir território competitivo e sistema de mensagem usando Ries, Neumeier, Archetypes e StoryBrand.

---

## Inputs

- Foundations report (`brand-diagnosis`)
- Público prioritário
- Oferta principal e diferenciais

---

## Output

| Artifact | Location | Description |
|---|---|---|
| `messaging-framework.md` | `workspace/businesses/{brand_name}/L2-tactical/brand/narrative/messaging-framework.md` | Sistema de mensagem consolidado (SB7 + claims + provas) |
| `strategic-positioning.yaml` | `workspace/businesses/{brand_name}/L2-tactical/brand/strategic-positioning.yaml` | Posicionamento estruturado para governanca de marca |
| `positioning-narrative-report.md` | `workspace/businesses/{brand_name}/L2-tactical/brand/positioning/positioning-narrative-report.md` | Relatorio consolidado de posicionamento + narrativa |

## Veto Conditions

- [ ] Posicionamento sem territorio competitivo defendavel
- [ ] Onlyness sem diferenca verificavel frente aos concorrentes
- [ ] Narrativa SB7 sem CTA claro ou sem prova de sustentacao
- [ ] Arquétipo escolhido contradiz o posicionamento definido

## Steps

1. **Ries:** mapear categoria, frame competitivo e posição defendável.
2. **Neumeier:** construir `Onlyness Statement`.
3. **Archetype:** definir arquétipo principal e suporte.
4. **StoryBrand SB7:** estruturar mensagem comercial clara.
5. Consolidar narrativa mestra com claims e provas.

---

## Output

```markdown
## Positioning & Narrative Report

### Positioning Statement
{texto}

### Onlyness Statement
{texto}

### Archetype System
- Principal: {arquétipo}
- Secundário: {arquétipo}

### StoryBrand Core
- Hero: {quem}
- Problem: {problema}
- Guide: {marca}
- Plan: {plano}
- CTA: {cta}
- Success: {resultado}
- Failure avoided: {risco}

### Messaging Pillars
1. {pillar_1}
2. {pillar_2}
3. {pillar_3}
```

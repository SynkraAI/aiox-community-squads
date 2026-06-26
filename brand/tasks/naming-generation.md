# Task: Naming Generation

## Metadata

```yaml
id: naming-generation
name: Generate Strategic Names (SNP)
executor: naming-strategist
elicit: true
estimated_duration: "20-40 min"
```

**Responsible Executor:** Agent (@naming-strategist)  
**Dependencies:** depends_on: `[load-workspace-context]` · enables: `[domain-check]` · workflow: `wf-naming-to-domain`

## Prerequisites

- **Context Gate (mandatory):** Brand workspace context must be loaded before execution. Run `load-workspace-context` first. If `workspace/businesses/{brand_name}/L2-tactical/brand/` does not exist, HALT and suggest workspace setup.
- **Vocabulary:** Consult `data/brand-mappings.yaml` for canonical naming terminology.

## Objective

Gerar shortlist de nomes com metodologia SNP (Igor Pinterich), aplicando validação estrutural para mercado brasileiro e filtros complementares quando necessário.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| context_type | enum | yes | produto, empresa, serviço |
| business_context | string | yes | contexto de negócio: o que é, para quem e em qual categoria |
| target_market | enum | yes | brasil, latam, global |
| constraints | string | no | palavras proibidas/restrições |
| existing_name | string | no | nome atual para validação |

---

## Output

| Artifact | Location | Description |
|---|---|---|
| `naming-shortlist.md` | `workspace/businesses/{brand_name}/L2-tactical/brand/naming/naming-shortlist.md` | Top candidatos priorizados pelo funil SNP com score e rationale |

## Execution Steps (SNP)

### Step 1: Estratégia
- Definir posicionamento, público e concorrência.
- Validar arquitetura de marca (monolítica/endossada/casa de marcas).

### Step 2: Critérios
- Eliminatórios: pronúncia BR, conotação negativa, risco legal básico.
- Pontuação: memorabilidade, distintividade, expressividade, adaptabilidade, longevidade.

### Step 3: Geração
- Meta de volume: 100-300 candidatos brutos.
- Técnicas principais SNP: combinação, truncamento, metáfora, neologismo.
- Complemento (se necessário): `20 Approaches` de Rob Meyerson.

### Step 4: Triagem em funil
- 300 -> 50 (filtro eliminatório)
- 50 -> 15 (score estratégico)
- 15 -> 5 (pré-validação legal e digital)

### Step 5: Validação complementar
- Aplicar SMILE/SCRATCH em top 5 (Alexandra Watkins).
- Aplicar Sound Symbolism (Placek) apenas se target incluir mercado global.

### Step 6: Recomendação
- Entregar top 3 para checagem de domínio e INPI aprofundada com `@domain-scout`.

---

## Output Template

```markdown
## Naming Shortlist (SNP)

### Contexto
- Tipo: {context_type}
- Mercado: {target_market}
- Posicionamento: {posicionamento}

### Top 5 Candidatos
| Nome | Score (/60) | SMILE | SCRATCH | Observação |
|---|---:|---:|---:|---|
| {nome_1} | {score_1} | {smile_1} | {scratch_1} | {obs_1} |
| {nome_2} | {score_2} | {smile_2} | {scratch_2} | {obs_2} |
| {nome_3} | {score_3} | {smile_3} | {scratch_3} | {obs_3} |
| {nome_4} | {score_4} | {smile_4} | {scratch_4} | {obs_4} |
| {nome_5} | {score_5} | {smile_5} | {scratch_5} | {obs_5} |

### Recomendação para domínio/INPI
1. {nome_1}
2. {nome_2}
3. {nome_3}
```

---

## Veto Conditions

- [ ] Nenhum candidato com score >= 36/60
- [ ] Todos os candidatos com risco legal alto em pré-checagem
- [ ] Todos com conflito semântico/cultural forte em PT-BR

---

## Handoff

```yaml
to: domain-scout
pass:
  - top_3_names: ["{nome_1}", "{nome_2}", "{nome_3}"]
  - target_market: "{target_market}"
  - check_inpi: true
  - priority_tlds: [".com.br", ".com", ".io"]
```

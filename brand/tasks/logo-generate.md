# Task: Logo Generation (Cross-Squad Bridge)

## Metadata

```yaml
id: logo-generate
name: Execute Logo Generation Batch
executor: nano-banana-generator
elicit: false
estimated_duration: "10-30 min"
cross_squad: true
source_squad: brand
target_squad: design
```

**Responsible Executor:** Agent (@nano-banana-generator) from Design Squad
**Dependencies:** depends_on: `[logo-prompt-engineering]` · enables: `[logo-curate]` · workflow: `wf-logo-brainstorm`

## Objective

Executar a geração de logos a partir do `logo-prompt-brief.yaml` criado pelo Brand Squad. Esta task é uma bridge cross-squad: o Brand Squad define O QUE gerar (prompts estratégicos), o Design Squad executa COMO gerar (via Nano Banana).

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| prompt_brief | file | yes | `logo-prompt-brief.yaml` com todos os prompts SCDS |
| output_dir | string | yes | Diretório de output para as gerações |
| guidelines | file | yes | `gemini-logo-guidelines.yaml` para referência |

---

## Output

| Artifact | Location | Description |
|---|---|---|
| Generated images | `{{output_dir}}/` | Imagens PNG geradas por prompt |
| Generation log | `{{output_dir}}/generation-log.yaml` | Log completo de todas as gerações |

## Execution Steps

### Step 1: Load Prompt Brief

- Ler `logo-prompt-brief.yaml` completamente
- Validar estrutura: todas as direções têm prompts, todos os prompts têm SCDS completo
- Ler `gemini-logo-guidelines.yaml` para quality checklist
- Criar diretório de output: `mkdir -p {{output_dir}}`

### Step 2: Validate Environment

- Verificar `GEMINI_API_KEY` em `.env` (primary)
- Se não encontrada, verificar `OPENROUTER_API_KEY` (fallback)
- Se nenhuma encontrada → abort
- Validar modelo disponível (flash ou pro conforme recomendação do brief)
- Confirmar aspect ratios suportados pelo provider selecionado

### Step 3: Execute Generation (Round-Robin)

Seguindo a batch_strategy do prompt brief:

1. Para cada rodada (round-robin por direção):
   - Selecionar 1 prompt de cada direção
   - Para cada prompt:
     - Construir request body com SCDS completo
     - Incluir negative prompt
     - Chamar `image-generate` task
     - Salvar como `{{output_dir}}/{{direction_id}}-{{prompt_id}}.png`
     - Pausar 5s entre gerações
   - Log de progresso: "Generated {n}/{total}"

2. Repetir até todos os prompts executados

### Step 4: Create Generation Log

```yaml
# Generation Log — {{brand_name}}
generation_session:
  id: "{{session_id}}"
  timestamp: "{{ISO-8601}}"
  brand_name: "{{brand_name}}"
  source_brief: "{{prompt_brief_path}}"
  model_used: "{{model}}"
  total_planned: {{n}}
  total_generated: {{n}}
  total_failed: {{n}}

generations:
  - id: "{{gen_id}}"
    direction: "{{direction_id}}"
    concept: "{{concept_name}}"
    prompt_id: "{{prompt_id}}"
    logo_type: "{{type}}"
    aspect_ratio: "{{ratio}}"
    resolution: "{{resolution}}"
    prompt_full: "{{full_scds_prompt}}"
    negative_prompt: "{{negative}}"
    output_file: "{{filename}}.png"
    file_size_kb: {{size}}
    status: "success|failed"
    error: "{{error_if_any}}"
    timestamp: "{{ISO-8601}}"
```

### Step 5: Present Summary

- Total gerado vs. total planejado
- Agrupar por direção conceitual
- Listar falhas (se houver) com causa
- Path do diretório de gerações

---

## Failure Handling

- **GEMINI_API_KEY missing:** Fall back para OpenRouter se disponível, senão abort
- **Model unavailable:** Fall back para modelo alternativo (flash ↔ pro)
- **Partial failure (>70% success):** Continuar, documentar falhas
- **Partial failure (<70% success):** Pausar, diagnosticar, tentar modelo alternativo
- **Rate limit:** Aumentar pausa para 15s, continuar

## Veto Conditions

- [ ] Nenhuma API key encontrada (`GEMINI_API_KEY` nem `OPENROUTER_API_KEY`)
- [ ] `logo-prompt-brief.yaml` inválido ou vazio
- [ ] Nenhuma imagem gerada com sucesso

---

## Handoff

```yaml
to: wheeler-brand-design
task: logo-curate
squad: brand
protocol: cross-squad-return
pass:
  - generations_dir: "{{output_dir}}/"
  - generation_log: "{{output_dir}}/generation-log.yaml"
  - brand_name: "{{brand_name}}"
  - total_generated: {{n}}
```

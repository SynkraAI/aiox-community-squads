# Criação de Deck de Slides AIOX

| Field              | Value                                        |
|--------------------|----------------------------------------------|
| **SOP ID**         | SOP-SLIDES-001                               |
| **Version**        | 1.2.0                                        |
| **Effective Date** | 2026-03-16                                   |
| **Department**     | Design System / Frontend                     |
| **Author**         | Gerber (SOP Creator Agent)                   |
| **Reviewer**       | Design System Maintainer                     |
| **Approver**       | Tech Lead                                    |
| **Next Review**    | 2026-09-16                                   |
| **Classification** | Internal                                     |
| **Status**         | DRAFT                                        |

> **Base normativa:** AIOX Slide Design Manual v2.1 (com correções validadas por pesquisa). Este documento segue padrões FDA/GMP de documentação controlada. Alterações requerem revisão formal e re-aprovação.

---

## 1. Purpose

Este SOP existe para garantir que todo deck de slides criado no Design System AIOX seja produzido de forma consistente, acessível e alinhada aos padrões visuais e técnicos da marca. Ele elimina variação de qualidade entre diferentes desenvolvedores, assegurando que qualquer dev frontend consiga produzir um deck completo seguindo um processo repetível — do briefing à entrega final — sem depender de conhecimento tácito ou decisões ad hoc.

---

## 2. Scope

**In Scope:**
- Criação end-to-end de decks de slides em React/TSX usando o Design System AIOX
- Seleção de modo de apresentação (Palco, Live, Async)
- Composição de sequência narrativa usando a taxonomia de 11 tipos de slide
- Aplicação de design tokens responsivos (cores, tipografia, espaçamento)
- Implementação de animações com Framer Motion
- Validação de acessibilidade (WCAG 2.2 AA mínimo)
- Checklist pré-entrega por slide e por deck

**Out of Scope:**
- Criação de conteúdo narrativo/textual (responsabilidade do autor do conteúdo)
- Manutenção do Design System em si (tokens, componentes base)
- Exportação para formatos não-web (PDF, PowerPoint) — coberto por SOP separado
- Design de novos tipos de slide não presentes na taxonomia

**Applicability:**
Desenvolvedores frontend que implementam slides em `slides-page.tsx` usando React, TypeScript e Framer Motion dentro do ecossistema AIOX.

---

## 3. Definitions & Abbreviations

| Termo / Abreviação | Definição |
|---------------------|-----------|
| **Aspect Ratio** | Proporção entre largura e altura do slide (ex: 16:9 = 1920×1080) |
| **Build progressivo** | Técnica de revelar conteúdo em etapas no mesmo slide, usando animação |
| **clamp()** | Função CSS que define valor mínimo, preferido e máximo para tamanho responsivo |
| **Design Token** | Variável de design (cor, tamanho, espaçamento) que serve como fonte única de verdade |
| **DS** | Design System |
| **svh** | Small Viewport Height — unidade CSS que mede a altura com o chrome do browser visível. Garante que o slide cabe na tela em qualquer estado. Preferida sobre `dvh` (dynamic, causa layout shifts) e `lvh` (large, similar ao `vh` legado) |
| **Framer Motion** | Biblioteca de animação para React |
| **Full-bleed** | Imagem ou elemento que ocupa 100% do slide sem margens |
| **Killer Item** | Item de checklist cuja falha impede a aprovação do slide (conceito de Gawande) |
| **Modo (Palco/Live/Async)** | Contexto de exibição que determina restrições de layout, densidade e interação |
| **PEAT** | Photosensitive Epilepsy Analysis Tool — ferramenta para validar animações contra riscos de convulsão |
| **RACI** | Responsible, Accountable, Consulted, Informed — matriz de responsabilidades |
| **Safe Area** | Zona segura do slide onde conteúdo pode ser posicionado sem risco de corte |
| **Section Break** | Slide divisor entre blocos temáticos de uma apresentação |
| **Stagger** | Delay incremental entre animações de elementos em sequência |
| **Stranger Test** | Teste de validação: um profissional qualificado que nunca viu o processo consegue executá-lo sem perguntas |
| **TSX** | TypeScript com JSX — formato de arquivo React com tipagem estática |
| **WCAG** | Web Content Accessibility Guidelines — diretrizes de acessibilidade web (versão 2.2) |
| **White Space** | Área vazia intencional no slide, usada para direcionar foco |

---

## 4. Roles & Responsibilities (RACI)

| Atividade | Dev Frontend | Designer/Autor | Tech Lead | QA |
|-----------|-------------|----------------|-----------|-----|
| Receber briefing e definir modo | R | C | I | — |
| Planejar sequência de slides | R | A | C | — |
| Implementar slides em TSX | R/A | I | C | — |
| Aplicar design tokens | R/A | — | I | — |
| Implementar animações | R/A | C | — | — |
| Validar acessibilidade | R | — | — | A |
| Executar checklist pré-entrega | R | — | A | C |
| Aprovar deck final | I | C | A | C |

**Escalation:** Tech Lead → Design System Maintainer → @aiox-master

---

## 5. Prerequisites & Materials

### 5.1 Ferramentas & Software

| Item | Especificação | Obrigatório |
|------|---------------|-------------|
| Node.js | v18+ | Sim |
| React | v18+ | Sim |
| TypeScript | v5+ | Sim |
| Framer Motion | v10+ | Sim |
| Fonte Geist Sans | Instalada no projeto | Sim |
| Fonte Geist Mono | Instalada no projeto | Sim |
| Ferramenta de contraste WCAG | Qualquer calculadora (ex: WebAIM Contrast Checker) | Sim |
| PEAT | Photosensitive Epilepsy Analysis Tool | Recomendado (obrigatório se houver animações com flash) |

### 5.2 Acesso & Permissões

| Sistema | Permissão | Como solicitar |
|---------|-----------|----------------|
| Repositório do projeto | Write access | Via Tech Lead |
| Design tokens (arquivo de variáveis) | Read access | Disponível no repositório |
| Figma (se houver mockups) | View access | Via Designer |

### 5.3 Treinamento Requerido

| Módulo | Pré-requisito |
|--------|---------------|
| AIOX Slide Design Manual v2.1 | Leitura completa antes da primeira execução |
| React + TypeScript básico | Proficiência funcional |
| Framer Motion fundamentals | Conhecimento de `motion`, `variants`, `AnimatePresence` |

### 5.4 Precondições

- [ ] Design tokens carregados no projeto (variáveis CSS disponíveis)
- [ ] Fontes Geist Sans e Geist Mono importadas e funcionais
- [ ] Briefing recebido com: tema, público-alvo, duração estimada e conteúdo-fonte
- [ ] Ambiente de desenvolvimento rodando (`npm run dev` funcional)
- [ ] Componentes base disponíveis: `SlideLayout`, `CornerMarks`, `WatermarkNumber`, `MetaBar`, `TechFrame`, `PageFooter`, `SectionTag`

---

## 6. Procedure (Step-by-Step)

> **INSTRUÇÃO:** Execute os passos sequencialmente. Cada passo representa uma ação. Não pule passos. Marque [x] ao completar.

---

### 6.1 Receber Briefing e Definir Modo

**Performer:** Dev Frontend
**Input:** Briefing do autor/designer

1. Receba o briefing contendo: tema da apresentação, público-alvo, duração estimada e conteúdo-fonte (texto, dados, imagens).

2. **[DECISION]** Determine o modo de apresentação com base no contexto de exibição:

   | Se o contexto é... | Então o modo é... |
   |---------------------|-------------------|
   | Conferência, keynote, workshop presencial | **Palco** |
   | YouTube, Twitch, call com screenshare | **Live** |
   | Deck pós-evento, material de curso, onboarding | **Async** |

3. Registre o modo escolhido. Todas as regras subsequentes derivam deste modo.

4. Registre as restrições do modo:

   | Restrição | Palco | Live | Async |
   |-----------|-------|------|-------|
   | Palavras por slide (máx) | 15 | 15 | 30 |
   | Fonte mínima corpo | 2.2vw (≈42px @1920) | 2.2vw | 1.6vw (≈30px @1920) |
   | Speaker notes obrigatórias | Sim | Sim | Não |
   | White space mínimo | 50% | 45% | 40% |
   | Animações | Sim | Moderação | Não |
   | Zona segura | Margens padrão | Evitar 20% inferior-direita (câmera) e lateral direita (chat) | Margens padrão |

5. **[CRITICAL]** Antes de confirmar o modo, consulte as regras por formato de apresentação (passo 6.1.1). O formato define overrides específicos.

**Expected Result:** Modo e formato definidos com restrições documentadas.

---

#### 6.1.1 Determinar Formato de Apresentação

**[DECISION]** Identifique o formato e aplique overrides:

| Formato | Slides | Texto | Bullets | Background | Autoexplicativo |
|---------|--------|-------|---------|------------|-----------------|
| TED/Keynote | 40–90 | Mínimo (0-1 frase) | **NUNCA** | Escuro | Nunca |
| Pitch Deck (VC) | 10–15 | Moderado | Raro | Neutro | Sim (leave-behind) |
| Sales Deck (B2B) | 8–25 | Moderado | Permitido | Neutro | Sim (champion) |
| Técnico/Conferência | 20–40 | Moderado+ | Permitido | Neutro/Escuro | Parcial (backup) |
| Zoom/Call Virtual | Variável | Reduzido | Com cautela | Escuro ou claro | Depende do modo |
| Carrossel/Stories | 5–10 | Mínimo (max 15 palavras) | **NUNCA** | Tema da marca | Sempre |

**Overrides por formato:**

- **TED/Keynote**: Bullets proibidos. Slide apoia o narrador — se funciona sozinho, está roubando atenção. Tipos dominantes: STATEMENT, IMAGE, METRIC. Arco: gancho → tensão → resolução → CTA.
- **Pitch Deck**: Estrutura Sequoia (Purpose→Problem→Solution→Why Now→Market→Competition→Product→Model→Team→Financials) ou YC. Mínimo 2 versões: live + leave-behind (Async com mais texto). Anti-pattern fatal: "We have no competition".
- **Sales Deck**: Framework SCR (Situation→Complication→Resolution). Personalizar por ICP. Leave-behind para champion vender internamente. O deck deve funcionar como vendedor autônomo.
- **Técnico**: Tipo CODE é legítimo. Código pode ir a 20pt (mono é mais largo). 5–10 backup slides para Q&A. Teste: "Recue 2m do monitor. Consegue ler?"
- **Zoom/Virtual**: Modo Live obrigatório. Slide é foco principal (sem linguagem corporal visível). 2+ movimentos visuais/minuto. Placeholder de interação a cada 3–5 min.
- **Carrossel/Stories**: Modo Async. Ratio 9:16 ou 1:1. Primeiro slide = hook visual. Último = CTA ("Salve", "Compartilhe"). Fonte extra-grande (scroll rápido a ~30cm).

**Expected Result:** Formato identificado com overrides registrados.

---

### 6.2 Selecionar Aspect Ratio

**Performer:** Dev Frontend

1. **[DECISION]** Selecione o aspect ratio com base no canal de exibição:

   | Canal | Aspect Ratio | Resolução de referência |
   |-------|-------------|------------------------|
   | Projetor, monitor, stream | **16:9** | 1920×1080 |
   | Projetores Mac, apresentação MacBook | **16:10** | 1920×1200 |
   | Stories, Reels, conteúdo vertical | **9:16** | 1080×1920 |
   | Carrossel Instagram, posts quadrados | **1:1** | 1080×1080 |

2. Configure o container do slide com o aspect ratio selecionado.

3. **[CRITICAL]** Use `100svh` em vez de `100vh` para containers de slide em contextos mobile. A unidade `svh` (small viewport height) mede a altura com o chrome do browser visível, garantindo que o slide cabe na tela em qualquer estado. Evitar `dvh` (dynamic — causa layout shifts percebidos como "glitch") e `lvh` (large — similar ao `vh` legado).

**Expected Result:** Aspect ratio configurado no `SlideLayout`.

---

### 6.3 Planejar Sequência de Slides

**Performer:** Dev Frontend + Autor/Designer (consultado)

1. Estime a quantidade de slides com base na duração:

   | Formato | Duração | Slides recomendados | Ritmo |
   |---------|---------|---------------------|-------|
   | Pitch/demo | 5–15 min | 8–15 | 1 slide/min |
   | Keynote | 30–60 min | 40–90 | 1 slide/30–40s |
   | Workshop | 1–4h | Módulos de 10–15 | Intercalado com exercícios |
   | Live/stream | Variável | Sob demanda | Ditado pela interação |

2. **[CRITICAL]** Nenhum slide deve permanecer na tela por mais de 2 minutos. Se o conteúdo exige mais tempo, divida em 2+ slides.

3. Monte a estrutura de sequência usando OBRIGATORIAMENTE:
   - Primeiro slide: tipo **TITLE**
   - Último slide: tipo **CLOSING**
   - Divisores entre blocos temáticos: tipo **SECTION-BREAK**

4. Distribua os slides de conteúdo entre as seções usando os 11 tipos da taxonomia:
   `TITLE` | `SECTION-BREAK` | `STATEMENT` | `CONTENT` | `COMPARISON` | `METRIC` | `DATA-VIZ` | `IMAGE` | `BUILD` | `CODE` | `CLOSING`

5. **[VERIFY]** Valide a sequência contra os patterns de ritmo:

   | Sequência | Efeito narrativo |
   |-----------|-----------------|
   | STATEMENT → CONTENT → CONTENT | Impacto → detalhe → detalhe |
   | METRIC → DATA-VIZ → CONTENT | Número → contexto → explicação |
   | IMAGE → STATEMENT | Visual → mensagem emocional |
   | BUILD (3 steps) | Progressão narrativa |
   | COMPARISON → STATEMENT | Contraste → conclusão |

6. **[CRITICAL]** Nunca mais de 3 slides consecutivos do mesmo tipo. Inserir mudanças de ritmo (SECTION-BREAK, IMAGE, STATEMENT) no meio de sequências longas para resetar a atenção da audiência.

7. Consulte a duração estimada por tipo para validar a duração total:

   | Tipo de slide | Tempo na tela |
   |--------------|--------------|
   | TITLE | 10–15s |
   | SECTION-BREAK | 3–5s |
   | STATEMENT | 5–10s |
   | CONTENT | 20–40s |
   | COMPARISON | 20–40s |
   | METRIC | 10–20s |
   | DATA-VIZ | 30–60s |
   | IMAGE | 5–15s |
   | BUILD | 15–30s por step |
   | CODE | 30–60s |
   | CLOSING | 10–20s |

**Expected Result:** Lista ordenada de slides com tipo definido para cada um.

---

### 6.4 Configurar Ambiente e Tokens

**Performer:** Dev Frontend

1. Verifique que os design tokens estão carregados no projeto. Os tokens OBRIGATÓRIOS são:

   **Cores:**
   | Token | Valor |
   |-------|-------|
   | `--bb-dark` | `#050505` |
   | `--bb-lime` | `#D1FF00` |
   | `--bb-cream` | `#FFFDD0` |
   | `--bb-dim` | **Deve ser ≥ `#777777`** (compliance WCAG AA). Para AAA, usar ≥ `#999999` |
   | `--bb-surface` | Definido no tema — usado para cards e painéis internos |

   **Ratios de contraste reais (v2.1 corrigidos):**
   | Combinação | Ratio real |
   |------------|-----------|
   | `--bb-cream` sobre `--bb-dark` | 19.62:1 (AAA) |
   | `--bb-lime` sobre `--bb-dark` | 17.48:1 (AAA) |
   | `--bb-dark` sobre `--bb-lime` | 17.48:1 (AAA) |
   | `--bb-dim` ≥ `#777777` sobre `--bb-dark` | ≥ 4.55:1 (AA) |
   | `--bb-dim` ≥ `#999999` sobre `--bb-dark` | ≥ 7.15:1 (AAA) |

2. Verifique que a escala tipográfica responsiva está definida:

   ```css
   :root {
     --slide-title-xl:   clamp(48px, 6.8vw, 130px);
     --slide-title-lg:   clamp(40px, 3.3vw, 64px);
     --slide-title-md:   clamp(32px, 2.5vw, 48px);
     --slide-body:       clamp(24px, 1.9vw, 36px);
     --slide-caption:    clamp(16px, 1.5vw, 28px);
     --slide-label:      clamp(13px, 0.7vw, 14px);  /* v2.1: piso elevado de 11px para 13px */
   }
   ```

   **[CRITICAL]** Nota sobre `--slide-label` em modo Palco: labels devem renderizar a ≥ 16px efetivos para legibilidade a distância. O valor de `0.7vw` em 1920px resulta em ~13.4px — validar que o contexto final não renderiza abaixo do piso.

   **Piso absoluto**: Nenhum texto em slides deve ser menor que 13px renderizado em qualquer viewport.

3. Verifique que os tokens de espaçamento estão definidos:

   ```css
   :root {
     --slide-space-xs:   clamp(4px, 0.4vw, 8px);
     --slide-space-sm:   clamp(8px, 0.8vw, 16px);
     --slide-space-md:   clamp(16px, 1.7vw, 32px);
     --slide-space-lg:   clamp(32px, 3.3vw, 64px);
     --slide-space-xl:   clamp(64px, 5vw, 96px);
   }
   ```

4. Verifique as margens de safe area:

   ```css
   :root {
     --slide-margin-x:      clamp(48px, 7.3vw, 200px);
     --slide-margin-top:    clamp(40px, 5vw, 136px);
     --slide-margin-bottom: clamp(24px, 2.1vw, 40px);
   }
   ```

5. **[DECISION]** Se o modo é **Live**, aplicar adicionalmente:

   ```css
   .mode-live {
     --slide-safe-right:  20%;
     --slide-safe-bottom: 15%;
   }
   ```

6. **[CRITICAL]** Nenhum valor de tamanho, espaçamento ou posição em `px` hardcoded. Sempre via token ou `clamp()`.

**Expected Result:** Todos os tokens carregados e validados. Ambiente de desenvolvimento funcional.

---

### 6.5 Criar Cada Slide

**Performer:** Dev Frontend

Para cada slide na sequência planejada (passo 6.3), execute o sub-procedimento correspondente ao tipo. Todo slide DEVE estar dentro de um `SlideLayout` com background `--bb-dark` e fonte Geist Sans como padrão.

**Regras gerais de background** (aplicam-se a todos os tipos):
- Grid pattern: máx 3% opacity. Radial glow: máx 6% opacity. Imagem de fundo: máx 15% com overlay `--bb-dark`.
- **Teste de subtração**: Remova o background. Se o slide funciona igual, o background é decorativo e aceitável. Se o slide perde informação, o background está carregando conteúdo e deve ser promovido a elemento visual principal.

---

#### 6.5.1 Tipo TITLE (Abertura)

1. Defina o título com `--slide-title-xl`, peso Black, máximo 5 palavras.
2. Defina o subtítulo com `--slide-title-md`, peso Medium, máximo 10 palavras.
3. Defina speaker com `--slide-caption`, peso Medium.
4. Defina data com `--slide-label`, fonte Geist Mono.
5. Adicione `CornerMarks` (máx 2 por deck section) e `MetaBar` se desejado.
6. Background: `--bb-dark` ou imagem a 10% opacity com overlay.
7. Layout: full center ou left-aligned com visual à direita.
8. **[CRITICAL]** Aplique `style={FONT_SANS}` inline em todo elemento com fonte custom.

---

#### 6.5.2 Tipo SECTION-BREAK (Divisor)

1. Defina `WatermarkNumber` gigante com opacity 4%.
2. Defina título com `--slide-title-lg`, peso Black, máximo 3 palavras.
3. Layout: full center, conteúdo mínimo.
4. Background: `--bb-dark` ou `--bb-lime` (accent).
5. Se background lime: texto em `--bb-dark`, peso Black.
6. **NÃO** adicione `PageFooter`.
7. Duração esperada: 3–5 segundos na tela.

---

#### 6.5.3 Tipo STATEMENT (Impacto)

1. Defina texto com `--slide-title-xl` ou `--slide-title-lg`, peso Black.
2. Atribuição opcional com `--slide-caption`, peso Medium.
3. Máximo 10 palavras no total do slide.
4. Layout: full center.
5. Máximo 2 palavras destacadas com inline highlight `--bb-lime`:
   ```tsx
   <span style={{
     background: "var(--bb-lime)",
     color: "var(--bb-dark)",
     padding: "0.05em 0.2em"
   }}>PALAVRA</span>
   ```
6. Background: `--bb-dark` exclusivo.
7. White space: ≥ 60%.
8. **Nota**: Citações de terceiros (com `attribution` preenchido) podem exigir tratamento visual distinto — aspas visuais, peso tipográfico diferente do manifesto próprio. Considerar separação futura em tipo QUOTE se o padrão recorrer em 3+ decks.

---

#### 6.5.4 Tipo CONTENT (Conteúdo Padrão)

1. Adicione `SectionTag` com número e label.
2. Defina título com `--slide-title-lg`, peso Black.
3. Defina 3–4 keywords/fragmentos com `--slide-body` (nunca frases completas).
4. Adicione `PageFooter` editorial: `Section — line — number — line — AIOX SQUAD.`
5. Layout: left-aligned.
6. White space: ≥ 50%.
7. **[CRITICAL]** Keywords, não frases:
   - ❌ "Nosso sistema coordena múltiplos agentes especializados"
   - ✅ "10+ agentes especializados"

---

#### 6.5.5 Tipo COMPARISON (Lado a Lado)

1. Defina lado esquerdo: título + 2–3 items.
2. Defina lado direito: título + 2–3 items.
3. Split: 50/50 ou 60/40.
4. Diferenciação visual: cor de ênfase OU opacidade — nunca apenas cor isolada (acessibilidade para daltônicos).
5. Layout 16:9: split horizontal. Layout 9:16: stack vertical.

---

#### 6.5.6 Tipo METRIC (Números de Impacto)

1. Defina 1–3 métricas com `{ value, label, unit? }`.
2. Valor: `--slide-title-xl`, peso Black, `font-bb-mono`.
3. Label: `--slide-caption`, peso Medium.
4. Layout: grid 1×1 (full center), 1×2 ou 1×3.
5. Animação: `scaleIn` com stagger de 0.15s (exceto modo Async).

---

#### 6.5.7 Tipo DATA-VIZ (Gráfico)

1. Defina título com `--slide-title-md`, peso Bold. **[CRITICAL]** O título é a CONCLUSÃO, não a descrição (ex: "Receita cresceu 40%", não "Gráfico de receita").
2. **[CRITICAL]** O dado deve ser legível a **3 metros de distância** (modo Palco).
3. Chart ocupa ≥ 60% da área do slide.
4. Source com `--slide-label`, Geist Mono, no canto inferior.
5. Cores do gráfico:
   - Série primária: `--bb-lime`
   - Série secundária: `--bb-cream` a 60% opacity
   - Série terciária: `--bb-dim`
   - Grid lines: `--bb-dim` a 20% opacity
   - Labels de eixo: `--bb-dim`, Geist Mono, `--slide-label`
5. **[CRITICAL]** Máximo 3 séries por gráfico.
6. **[CRITICAL]** Nunca diferenciar séries apenas por cor — sempre adicionar padrão (sólido, tracejado, pontilhado) ou label direto na série.
7. Tipos permitidos:
   - Bar vertical (máx 6 barras)
   - Bar horizontal (máx 8 barras)
   - Line chart (máx 12 pontos, 2 linhas)
   - Donut/pie (máx 4 fatias)
   - Big number + sparkline
   - Tabela simplificada (máx 4 colunas × 5 linhas)
8. **NÃO** usar: scatter plots, heatmaps, treemaps, sankey.
9. Labels em gráficos — tamanhos mínimos por elemento:

   | Elemento | Tamanho mínimo | Fonte |
   |----------|---------------|-------|
   | Valor nas barras/pontos | `--slide-caption` | Mono, Bold |
   | Eixo X/Y labels | `--slide-label` | Mono, Medium |
   | Legenda | `--slide-label` | Sans, Medium |
   | Título do gráfico | `--slide-title-md` | Sans, Bold |
   | Fonte/source | `--slide-label` | Mono, Regular |

---

#### 6.5.8 Tipo IMAGE (Imagem Dominante)

1. Imagem ocupa ≥ 60% do slide.
2. Caption com `--slide-caption`, máximo 8 palavras.
3. Layout: full-bleed, split 60/40, ou centered com padding.
4. Se texto sobrepõe imagem: gradiente de `--bb-dark` com opacity 60–80%. O texto deve manter contraste ≥ 4.5:1 sobre a parte mais clara da imagem.
5. Resolução mínima: 1920px de largura para full-bleed.
6. Screenshots: sempre com `TechFrame` (máx 2 por slide) ou borda sutil de 1px `--bb-surface`.
7. Imagens com fundo claro: DEVEM ter borda/frame ou cantos arredondados para não "flutuar" sobre `--bb-dark`. Imagens com fundo escuro podem ir full-bleed.
8. Performance: WebP preferido, máx 500KB por imagem. Decks com muitas imagens: lazy loading por slide visível.
9. **Mídia além de imagens estáticas:**
   - Vídeo embed (MP4): apenas modo Palco, máx 30s, autoplay sem som.
   - GIF / Lottie: máx 5s de loop, nunca como conteúdo principal isolado.
   - Ilustração / Ícone: SVG preferido, usar cores dos tokens, nunca cores externas.
10. **[CRITICAL]** Anti-patterns proibidos:
    - Stock photo genérica
    - Screenshot sem seta/highlight de contexto
    - Imagem pixelada ou esticada
    - Marca d'água visível
    - Imagem decorativa sem relação ao argumento (distração sem valor)

---

#### 6.5.9 Tipo BUILD (Progressivo)

1. Defina 2–5 etapas.
2. Passos futuros: 15% opacity. Passo atual: 100% opacity.
3. Layout: horizontal (timeline) ou vertical (lista progressiva).
4. **[DECISION]** Em modo Async: todos os passos visíveis simultaneamente, sem progressão.

---

#### 6.5.10 Tipo CODE (Código/Terminal)

1. Fonte: Geist Mono, tamanho mínimo `--slide-body`.
2. Label de linguagem no topo com `--slide-label`.
3. Highlight de linhas: `--bb-lime` a 15% opacity como fundo.
4. **[CRITICAL]** Máximo 12 linhas visíveis. Se exceder, dividir em 2 slides.
5. Layout: centered com padding generoso ou split com explicação.
6. **[CRITICAL]** Nunca usar screenshot de código — sempre texto renderizado.

---

#### 6.5.11 Tipo CLOSING (Final)

1. Mensagem com `--slide-title-lg`, peso Black, máximo 5 palavras.
2. Contato com `--slide-caption` (links, redes).
3. `CornerMarks` permitidos.
4. Layout: full center.
5. **[CRITICAL]** CTA apenas em texto. Sem botões clicáveis — o contexto é palco, não web.

---

### 6.6 Implementar Animações

**Performer:** Dev Frontend

1. **[DECISION]** Se o modo é **Async**: PULE este passo inteiro. Animações não se aplicam a export estático.

2. Selecione animações dos presets disponíveis:

   | Preset | Uso | Delay base |
   |--------|-----|------------|
   | `fadeUp` | Títulos, blocos de texto | 0.1–0.3s |
   | `fadeIn` | Backgrounds, elementos sutis | 0.0–0.2s |
   | `slideRight` | Conteúdo entrando da esquerda | 0.1–0.4s |
   | `slideLeft` | Conteúdo entrando da direita | 0.3–0.6s |
   | `scaleIn` | Cards, métricas, grids | 0.3–0.5s |
   | `growWidth` | Linhas horizontais, progress bars | 0.5–0.8s |
   | `growHeight` | Linhas verticais, barras de gráfico | 0.3–0.7s |

3. Para listas e grids, aplique stagger: `stagger(i, 0.3)` → `0.3 + i * 0.08`.

4. **[CRITICAL]** Restrições obrigatórias:
   - Máximo 3 tipos de animação por slide.
   - Delay total nunca maior que 1.5s.
   - Em modo Live: reduzir delays em 30%.

5. **[CRITICAL]** Anime APENAS quando controlar atenção temporal:
   - ✅ Sequência temporal (steps, timeline)
   - ✅ Revelar dado de impacto (big number)
   - ✅ Build progressivo
   - ✅ Gráficos com dados comparativos
   - ❌ Elementos decorativos (backgrounds, grids)
   - ❌ Título do slide (deve ser imediato)

6. Heurística: se remover a animação não muda a compreensão, não anime.

**Expected Result:** Animações implementadas respeitando as restrições do modo.

---

### 6.7 Validar Acessibilidade

**Performer:** Dev Frontend

1. **[CRITICAL]** Valide contraste de cada combinação texto/fundo:
   - ≥ 4.5:1 para texto em `--slide-body` ou menor
   - ≥ 3:1 para texto em `--slide-title-lg` ou maior (texto grande WCAG)
   - **[CRITICAL]** Valide especificamente `--bb-dim` sobre `--bb-dark` — ponto de maior risco do sistema. O valor de `--bb-dim` DEVE ser ≥ `#777777`.

2. Verifique daltonismo:
   - Nenhuma informação é diferenciada APENAS por cor.
   - Gráficos: cor + padrão (sólido, tracejado, pontilhado).
   - Comparações: cor + label textual.
   - Teste combinação `--bb-dim` vs `--bb-lime` para tritanopia.

3. Verifique estrutura semântica (obrigatório para modo Async):
   - Headings hierárquicos (`h1` > `h2` > `h3`).
   - Alt text em todas as imagens (decorativas: `alt=""`).
   - Labels em gráficos via `aria-label` ou texto alternativo.
   - Ordem de leitura do DOM = ordem visual.
   - **[CRITICAL]** Títulos de slide DEVEM ser únicos para navegação por screen reader (v2.1).

4. Verifique motion:
   - Implemente `@media (prefers-reduced-motion: reduce)` desabilitando todas as animações:
     ```css
     @media (prefers-reduced-motion: reduce) {
       *, *::before, *::after {
         animation-duration: 0.01ms !important;
         animation-iteration-count: 1 !important;
         transition-duration: 0.01ms !important;
         scroll-behavior: auto !important;
       }
     }
     ```
   - Em Framer Motion, verificar via hook:
     ```tsx
     import { useReducedMotion } from "framer-motion";
     const shouldReduceMotion = useReducedMotion();
     // Se true, desabilitar todas as variants animadas
     ```
   - **[CRITICAL]** Nenhum flash > 3 vezes em qualquer período de 1 segundo (≤ 3 é o limite WCAG 2.3.1, não < 3).
   - Se houver animações com flash, valide com PEAT (Photosensitive Epilepsy Analysis Tool). Nota: a versão atual do PEAT (2017) tem limitações com formatos de vídeo modernos — a função de captura nem sempre funciona, e formatos novos precisam ser convertidos para .AVI.

5. **[VERIFY]** Checklist de acessibilidade para export (obrigatório para modo Async/PDF):
   - [ ] Todos os slides têm títulos únicos para navegação por screen reader
   - [ ] Ordem de leitura do DOM verificada (usar Accessibility Inspector do browser)
   - [ ] Alt text em todas as imagens
   - [ ] Contraste de `--bb-dim` validado (≥ AA)
   - [ ] Animações removidas ou desabilitadas no export estático

**Expected Result:** Deck 100% compliant WCAG 2.2 AA (AAA preferido).

---

### 6.8 Executar Checklist Pré-Slide (Por Slide)

**Performer:** Dev Frontend

Para **cada** slide no deck, verifique:

**Todo slide:**
- [ ] Uma única ideia?
- [ ] Compreensível em 3 segundos?
- [ ] Tipo de slide definido (da taxonomia seção 4 do manual)?
- [ ] Tokens responsivos (zero `px` hardcoded)?
- [ ] White space ≥ limite do modo? (Teste: se não consegue apontar para uma área vazia ≥ 25% do slide de uma vez, está cheio demais)
- [ ] Zero parágrafos (exceto Async com restrição)?
- [ ] Zero botões/CTAs web?
- [ ] `prefers-reduced-motion` respeitado?
- [ ] Alt text em imagens?
- [ ] `style={FONT_SANS}` ou `style={FONT_MONO}` inline presente?

**Slides com texto:**
- [ ] Texto ≤ 6 palavras por linha?
- [ ] Máximo 4 linhas/bullets (Palco/Live) ou 6 (Async)?
- [ ] Fonte ≥ mínimo do modo?
- [ ] Hierarquia tipográfica clara (título > sub > body)?
- [ ] Keywords, não frases completas?

**Slides com dados:**
- [ ] Título = conclusão, não descrição?
- [ ] Máx 3 séries no gráfico?
- [ ] Diferenciação não depende só de cor?
- [ ] Labels legíveis no tamanho mínimo?
- [ ] Fonte do dado creditada?

**Slides com imagem:**
- [ ] Resolução ≥ 1920px para full-bleed?
- [ ] Contraste mantido se texto sobrepõe imagem?
- [ ] Não é stock genérica?
- [ ] Screenshot tem frame/borda?

**[CRITICAL — Killer Items]** Se qualquer item abaixo falhar, o slide NÃO pode ser aprovado:
1. Contraste < WCAG AA (4.5:1 corpo / 3:1 título)
2. Valor em `px` hardcoded
3. Mais de 15 palavras em modo Palco/Live
4. Parágrafo em modo Palco/Live
5. Screenshot de código (em vez de texto renderizado)

**Expected Result:** Cada slide com checklist completo aprovado.

---

### 6.9 Executar Checklist de Sequência (Deck Completo)

**Performer:** Dev Frontend

- [ ] Modo definido (Palco, Live, Async)?
- [ ] Aspect ratio definido e configurado?
- [ ] Section breaks entre blocos temáticos?
- [ ] Nenhum slide fica > 2 minutos na tela?
- [ ] Primeiro slide = TITLE?
- [ ] Último slide = CLOSING?
- [ ] Nunca mais de 3 slides consecutivos do mesmo tipo?
- [ ] Duração total compatível com o formato planejado?
- [ ] Todas as imagens em WebP e ≤ 500KB?
- [ ] Componentes base importados corretamente (`SlideLayout`, decorativos)?

**Expected Result:** Deck completo validado como unidade coerente.

---

### 6.10 Review e Entrega

**Performer:** Dev Frontend → Tech Lead (aprovação)

1. Execute `npm run lint` e `npm run typecheck`. Corrija erros.
2. Visualize o deck completo no browser em resolução de referência do aspect ratio escolhido.
3. Teste responsividade redimensionando o viewport.
4. Se modo Palco: projete em tela externa e valide legibilidade a distância.
5. Se modo Live: teste com overlay de câmera e chat simulado.
6. Submeta para review do Tech Lead.
7. **[VERIFY]** Tech Lead aprova ou solicita correções.
8. Se correções solicitadas: volte ao passo correspondente e re-execute.

**Expected Result:** Deck aprovado e pronto para uso.

---

## 7. Error Handling & Troubleshooting

### 7.1 Falhas Conhecidas

| # | Sintoma | Causa provável | Ação imediata | Escalation |
|---|---------|----------------|---------------|------------|
| 1 | Texto ilegível no projetor | Fonte abaixo do mínimo ou contraste insuficiente | Verificar token e ratio WCAG. Corrigir para o mínimo do modo | Dev → Tech Lead |
| 2 | Layout quebrado em viewport diferente | Valor em `px` hardcoded | Substituir por token ou `clamp()` | Dev auto-corrige |
| 3 | Animação travando em stream | Delay excessivo ou complexidade alta | Reduzir delays em 30% (regra Live). Simplificar animação | Dev auto-corrige |
| 4 | Slide não se encaixa em nenhum tipo | Conteúdo complexo demais para 1 slide | Decompor em 2+ slides de tipos existentes | Dev → Designer |
| 5 | Imagem pixelada ao escalar | Resolução < 1920px | Obter imagem em resolução maior ou reduzir área de exibição | Dev → Designer |
| 6 | `--bb-dim` falha contraste WCAG | Valor hex abaixo de `#777777` | Elevar para `#777777` (AA) ou `#999999` (AAA) | Dev auto-corrige |
| 7 | `prefers-reduced-motion` não funciona | Media query ausente | Adicionar CSS conforme passo 6.7.4 | Dev auto-corrige |
| 8 | Fontes não carregam no slide | `style={FONT_SANS}` inline ausente | Adicionar reforço inline em todo elemento com fonte custom | Dev auto-corrige |

### 7.2 Procedimento de Desvio

1. **PARE** — Interrompa a implementação no passo atual.
2. **DOCUMENTE** — Registre o desvio (slide afetado, problema, impacto).
3. **AVALIE** — Determine se é bloqueante (killer item) ou não-bloqueante.
4. **NOTIFIQUE** — Se bloqueante, notifique o Tech Lead.
5. **NÃO PROSSIGA** em killer items até resolução.

### 7.3 Rollback

Se o deck precisa ser revertido após entrega:
1. Reverta via `git revert` para o commit anterior ao deck.
2. Documente o motivo do rollback.
3. Re-execute o SOP a partir do passo que originou o problema.

---

## 8. Quality Controls & Metrics

### 8.1 Critérios de Aceitação

| Checkpoint | Critério | Método | Threshold | Verificador |
|------------|----------|--------|-----------|-------------|
| Contraste WCAG | Toda combinação texto/fundo ≥ AA | Calculadora WCAG | 4.5:1 corpo / 3:1 título | Dev + QA |
| Zero px hardcoded | Nenhum valor absoluto fora de tokens | Grep por `\d+px` no código do slide | 0 ocorrências | Dev |
| White space | ≥ limite do modo por slide | Inspeção visual | 50%/45%/40% conforme modo | Tech Lead |
| Responsividade | Layout funcional em todas as resoluções do ratio | Teste em viewport 50%, 100%, 150% | Sem overflow ou truncamento | Dev |
| Checklist por slide | Todos os items aprovados | Checklist 6.8 | 100% items marcados | Dev |
| Checklist de sequência | Todos os items aprovados | Checklist 6.9 | 100% items marcados | Dev |
| Lint + Typecheck | Zero erros | `npm run lint && npm run typecheck` | 0 errors | Dev |

### 8.2 Decisão de Aceitação

- **TODOS** os checkpoints PASS: Deck aprovado para entrega.
- **QUALQUER** killer item FAIL: Deck bloqueado. Voltar à seção 7.

---

## 9. References & Related Documents

| Documento | Relação |
|-----------|---------|
| AIOX Slide Design Manual v2.1 | Manual de referência primário (tokens, taxonomia, regras) |
| WCAG 2.2 — Web Content Accessibility Guidelines | Padrão de acessibilidade referenciado |
| Framer Motion Documentation | Biblioteca de animação utilizada |
| Geist Font Family Documentation | Fontes tipográficas do sistema |
| Atomic Design — Brad Frost | Arquitetura do sistema de design |
| The E-Myth Revisited — Michael Gerber | Filosofia de sistematização |
| The Checklist Manifesto — Atul Gawande | Princípios de checklists (killer items, pause points) |
| Presentation Zen Design — Garr Reynolds | Princípios de design de apresentações |
| TED — Speaker Guide & Slide Guidelines | Regras de slides para TED talks |
| Duarte — Resonate & Virtual Presentation Design | Design de apresentações virtuais |
| Y Combinator — Seed Deck Template | Estrutura de pitch deck |
| Sequoia Capital — Pitch Deck Framework | Framework de pitch para investidores |
| MIT CommLab — Technical Presentation Guidelines | Guidelines para apresentações técnicas |
| DocSend — Startup Fundraising Report | Dados de performance de pitch decks |
| Peter Kazanjy — Sales Decks for Founders | Framework de sales deck |

**Retenção:** Este SOP é retido enquanto o Design System AIOX estiver em uso. Armazenamento de referência: repositório do projeto em `squads/aiox-sop/outputs/`. Publicação canônica atual: SOPs markdown em `docs/sops/`; SOPs machine-readable por business em `workspace/businesses/{business}/sops/`.

---

## 10. Revision History

| Version | Date | Author | Change Description | Approved By |
|---------|------|--------|--------------------|-------------|
| 1.2.0 | 2026-03-16 | Gerber (SOP Creator Agent) | Auditoria v2.1 final: svh (não dvh) para viewport mobile, Seção 14 Guia por Formato de Apresentação (TED/Pitch/Sales/Técnico/Zoom/Carrossel), cross-ref formato→modo, PEAT limitations note, fontes bibliográficas novas. | Pending |
| 1.1.0 | 2026-03-16 | Gerber (SOP Creator Agent) | Auditoria de cobertura 100% contra manual v2.1. 24 gaps corrigidos: zona segura Live, --bb-surface, piso 13px standalone, limites decorativos, teste de subtração, nota QUOTE, layouts IMAGE, regras vídeo/GIF, tratamento imagens bg claro/escuro, lazy loading, 5o anti-pattern, legibilidade 3m, label sizes data-viz, hook useReducedMotion, scroll-behavior, teste 25% white space, tabela responsividade layout, checklist export, anotação título acessível, 2 anti-patterns v2.1, reset de ritmo, duração por tipo, gráficos na lista de animar. | Pending |
| 1.0.0 | 2026-03-16 | Gerber (SOP Creator Agent) | Versão inicial. Incorpora correções v2.1 do manual: ratios de contraste reais, piso de --bb-dim ≥ #777777, piso de --slide-label de 11px→13px, dvh vs vh, flash ≤ 3/s, títulos únicos obrigatórios, media query prefers-reduced-motion. | Pending |

**Ciclo de revisão:** A cada 6 meses ou quando o Design Manual receber atualização de versão major.

---

## Appendix A: Estrutura de Camadas do Slide

```
SlideLayout (container responsivo, bg: --bb-dark, font: Geist Sans)
+-- [1] Background layer
|   +-- Pattern / glow (opacity <= 6%)
+-- [2] Decorative layer
|   +-- CornerMarks, WatermarkNumber (contextual)
+-- [3] MetaBar (opcional, top)
+-- [4] Content (dentro de safe area)
|   +-- SectionTag
|   +-- Titulo (OBRIGATORIO e UNICO para acessibilidade)
|   +-- Keywords / bullets
|   +-- Elemento visual (chart, imagem, grid, codigo)
+-- [5] PageFooter (opcional, bottom)
+-- [6] Brand watermark (bottom-right, opacity minima)
```

## Appendix B: Anti-Patterns (Lista Rápida)

| Proibido | Motivo |
|----------|--------|
| Parágrafos de texto | Slides não são documentos |
| Fonte < `--slide-body` em Palco | Ilegível no projetor |
| Mais de 4 bullets (Palco/Live) | Sobrecarga cognitiva |
| Botões/CTAs clicáveis | Não existe interação no palco |
| Hover effects | Não existe mouse no palco |
| Preencher todo o espaço | White space = foco |
| Mais de 3 cores num slide | Poluição visual |
| Animações > 1.5s total | Audiência perde paciência |
| Valores em `px` hardcoded | Quebra responsividade |
| Screenshot de código | Inacessível, pixela ao escalar |
| Stock photo genérica | Destrói credibilidade |
| Mais de 1 gráfico por slide | Competição visual |
| Diferenciar dados apenas por cor | Inacessível para daltônicos |
| Slide sem título acessível | Invisível para screen readers |
| `--bb-dim` abaixo de `#777777` | Falha WCAG AA |
| Slide autoexplicativo em modo Palco | Se dispensa narrador, é documento |
| Slide dependente de narrador em modo Async | Se depende da voz, falta info |

## Appendix C: Mapa de Layout por Tipo de Slide

| Layout | Tipos compatíveis |
|--------|-------------------|
| Full center | STATEMENT, SECTION-BREAK, METRIC (1), CLOSING |
| Left-aligned | CONTENT, BUILD |
| Split 50/50 | COMPARISON, IMAGE |
| Split 60/40 | IMAGE, DATA-VIZ |
| Grid 1x2 | METRIC (2) |
| Grid 1x3 | METRIC (3), CONTENT (3 colunas) |

## Appendix D: Responsividade de Layout por Aspect Ratio

| Layout original (16:9) | Em 9:16 (vertical) | Em 1:1 (quadrado) |
|------------------------|--------------------|--------------------|
| Split 50/50 horizontal | Stack vertical 50/50 | Stack vertical 60/40 |
| Split 60/40 horizontal | Stack vertical, imagem topo | Imagem topo 50%, texto baixo |
| Grid 1×3 horizontal | Stack vertical 3×1 | Grid 1×3 com items menores |
| Full center | Full center (mesma lógica) | Full center |
| Left-aligned | Left-aligned | Left-aligned, margin reduzida |

**Regra**: O tipo de slide define a INTENÇÃO. O layout adapta a FORMA ao viewport sem mudar a hierarquia de informação.

---

*Este documento é controlado. Cópias não autorizadas não são válidas. Verifique a versão vigente antes de usar.*
*End of SOP-SLIDES-001 v1.2.0*
*Template: sop-human-tmpl.md | SOP Factory | Synkra AIOX*

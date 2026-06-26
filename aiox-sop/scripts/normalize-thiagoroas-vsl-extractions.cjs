#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..', '..');
const DOCS_SOPS_ROOT = path.join(ROOT, 'docs', 'sops');
const AUXILIARY_OUTPUT_ROOT = path.join(ROOT, 'outputs', 'aiox-sop', 'extractions');
const TODAY = new Date().toISOString().slice(0, 10);
const REVIEW_DATE = new Date(Date.UTC(2026, 5, 11)).toISOString().slice(0, 10);

const PROVENANCE_NOTE = [
  'DRAFT - EXTRACTED',
  'Normalized into the canonical SOP Factory extraction package.',
  'Original research drafts remain under squads/copy/data/sops/ as source material only.',
].join(' ');

const PACKAGES = [
  {
    slug: 'vsl-funnel-architecture',
    title: 'Funil VSL Perpetuo - Arquitetura Completa',
    sopId: 'SOP-COPY-VSL-ARCH-001',
    version: '0.1',
    classification: 'MAJOR',
    level: 'STRATEGIC',
    processId: 'vsl-funnel-architecture',
    sourcePath: 'squads/copy/data/sops/vsl-funnel-architecture-sop.md',
    sourceMaterial: [
      'Palestra ao vivo + slides de Thiago Roas',
      'Podcast "Segredos da Escala #122" (YouTube ID: qj04cUeaRAw)',
      'thiagoroas-vsl-funnel-and-traffic-framework.yaml',
    ],
    purpose:
      'To define the strategic architecture decisions that must be locked before a cold-traffic VSL funnel is written, recorded, or launched.',
    scopeIn: [
      'Niche qualification and funnel-fit screening for cold traffic',
      'Front-end pricing, upsell, downsell, and order-bump architecture',
      'Benchmark definitions for VSL structure, metrics, and creative coherence',
    ],
    scopeOut: [
      'Writing the VSL script itself',
      'Operating paid-media accounts or campaign setup',
    ],
    applicability:
      'Copy Chief, Strategist, Funnel Architect, and downstream planning agents that need a canonical pre-copy funnel architecture reference.',
    standards: [
      ['SOP Factory extract-sop', 'squads/aiox-sop/tasks/extract-sop.md'],
      ['ISO 9001:2015', 'Process approach and documented information'],
      ['Deming/Juran', 'PDCA, quality planning, and review-before-release discipline'],
    ],
    definitions: [
      ['VSL', 'Video Sales Letter used to convert cold traffic into direct sales.'],
      ['Front-end', 'Primary product offer shown in the first purchase step.'],
      ['Upsell', 'Immediate post-purchase offer used to increase ticket medio.'],
      ['Downsell', 'Reduced follow-up offer shown after the upsell decline.'],
      ['Play rate', 'Percentage of page visitors who start the VSL.'],
      ['Awareness level', 'Prospect sophistication state based on Schwartz-style demand awareness.'],
    ],
    roles: ['Copy Chief', 'Strategist', 'Funnel Architect', 'Performance Analyst'],
    raci: [
      ['Qualify niche and funnel fit', 'C', 'A', 'R', 'I'],
      ['Approve pricing architecture', 'A', 'R', 'C', 'I'],
      ['Define funnel stages and post-purchase path', 'C', 'R', 'A', 'I'],
      ['Set benchmark metrics and guardrails', 'C', 'C', 'R', 'A'],
      ['Approve creative-to-VSL coherence rules', 'A', 'R', 'C', 'C'],
    ],
    materials: [
      ['Thiago Roas source draft', 'Markdown source', '1', 'Primary extraction reference'],
      ['Reference YAMLs', 'Traffic + copy analysis files', '2+', 'Support provenance and benchmark checks'],
      ['Planning worksheet', 'Architecture decision log', '1', 'Used to capture final decisions'],
    ],
    systems: [
      ['Repository workspace', 'Read access', 'Project maintainer'],
      ['Planning sheet / brief', 'Edit access', 'Copy Chief'],
    ],
    training: [
      ['Cold-traffic VSL taxonomy review', 'Internal', 'Current'],
      ['Awareness and mechanism review', 'Internal', 'Current'],
    ],
    conditions: [
      'The offer is intended for cold-traffic acquisition rather than authority-driven selling.',
      'The team can measure play rate, retention, checkout, and ticket economics after launch.',
      'A niche brief and initial offer hypothesis exist before architecture starts.',
    ],
    trigger: {
      type: 'manual',
      description: 'Use before writing or recording a new cold-traffic VSL funnel.',
      source: 'Copy Chief or Funnel Architect',
    },
    phases: [
      {
        title: 'Qualify Niche',
        performer: 'Strategist',
        duration: 'PT45M',
        durationLabel: '45 minutes',
        actions: [
          'Estimate the addressable market and classify it as big, medium, or professional. [DOC]',
          'Verify whether the offer can convert cold traffic without depending on authority effects. [DOC]',
          'Stop and route to a different funnel model if the niche cannot sustain cold-traffic VSL economics. [INF]',
        ],
        expected:
          'A recorded funnel-fit verdict with niche size, awareness level, and go/no-go rationale.',
        source:
          'thiagoroas-vsl-funnel-architecture-sop.md -> Fase 1; funnel_taxonomy; brown_enrichment',
      },
      {
        title: 'Define Pricing Architecture',
        performer: 'Copy Chief',
        duration: 'PT30M',
        durationLabel: '30 minutes',
        actions: [
          'Set the front-end around the proven R$297 benchmark unless the team has stronger direct evidence. [DOC]',
          'Model card mix, upsell price, downsell path, and order-bump economics before media starts. [DOC]',
          'Flag any front-end price above the proven benchmark for dedicated validation before launch. [INF]',
        ],
        expected: 'A pricing stack with explicit rationale and exception flags.',
        source:
          'thiagoroas-vsl-funnel-architecture-sop.md -> Fase 2; vsl_funnel.front; pix_cartao_matematica_escala',
      },
      {
        title: 'Map Funnel Structure',
        performer: 'Funnel Architect',
        duration: 'PT45M',
        durationLabel: '45 minutes',
        actions: [
          'Define the front, checkout, upsell, downsell, and recovery sequence as one system. [DOC]',
          'Use a clean checkout as baseline and introduce order bumps only with explicit test intent. [DOC]',
          'Require visible decline paths on upsell and downsell pages to protect post-purchase flow. [DOC]',
        ],
        expected: 'A documented funnel path with baseline post-purchase rules.',
        source:
          'thiagoroas-vsl-funnel-architecture-sop.md -> Fase 3; vsl_funnel; funnel_health_metrics',
      },
      {
        title: 'Specify VSL Form Factor',
        performer: 'Funnel Architect',
        duration: 'PT30M',
        durationLabel: '30 minutes',
        actions: [
          'Set VSL length near the proven 20-30 minute range for a R$297 offer. [DOC]',
          'Require at least five micro-videos and at least three lead variants for testing. [DOC]',
          'Separate format choices from copy choices so retention problems can be diagnosed correctly later. [DOC]',
        ],
        expected: 'A VSL production brief with duration, segmentation, and lead rules.',
        source:
          'thiagoroas-vsl-funnel-architecture-sop.md -> Fase 4; vsl_retention.recording_rules; vsl_sizing',
      },
      {
        title: 'Define Metrics and Economic Guardrails',
        performer: 'Performance Analyst',
        duration: 'PT30M',
        durationLabel: '30 minutes',
        actions: [
          'Publish the baseline benchmarks for play rate, retention, checkout, upsell, downsell, and ticket medio. [DOC]',
          'Use custo de checkout and ticket medio as the primary economics guardrails instead of front-ticket ROAS alone. [DOC]',
          'Apply the 731 view and the 20% budget-increase rule only after statistical signal exists. [DOC]',
        ],
        expected: 'A benchmark table and traffic guardrail set ready for launch and diagnosis.',
        source:
          'thiagoroas-vsl-funnel-architecture-sop.md -> Fase 5; funnel_health_metrics; regra_20_percent',
      },
      {
        title: 'Align Creative and VSL Coherence',
        performer: 'Copy Chief',
        duration: 'PT25M',
        durationLabel: '25 minutes',
        actions: [
          'Map the awareness level of each creative angle to the lead style required by the VSL. [INF]',
          'Prefer video creative and a 70/30 mix between proven and new variations. [DOC]',
          'Treat creative refresh as a structural anti-fatigue rule, not optional polish. [DOC]',
        ],
        expected: 'A creative-to-VSL coherence rule set attached to the architecture brief.',
        source:
          'thiagoroas-vsl-funnel-architecture-sop.md -> Fase 6; creative_mix_rule; creative_as_awareness_filter',
      },
    ],
    decisionPoints: [
      {
        title: 'Niche Fit Decision',
        if: 'The niche is big enough and the offer can convert cold traffic without authority dependency.',
        then: 'Proceed to pricing and funnel architecture for a VSL-led system.',
        elseIf: 'The niche is medium or professional and requires another monetization path.',
        altAction: 'Route to low-ticket or launch-based architecture and stop this SOP.',
        escalate: 'Copy Chief',
      },
      {
        title: 'Pricing Exception Decision',
        if: 'The front-end remains within the proven benchmark range.',
        then: 'Proceed with the standard VSL specification.',
        elseIf: 'The team proposes a materially higher front-end price.',
        altAction: 'Open a validation branch and gather additional proof before launch.',
        escalate: 'Strategist',
      },
    ],
    dependencies: {
      sequential: [
        'Qualify Niche -> Define Pricing Architecture',
        'Define Pricing Architecture -> Map Funnel Structure',
        'Map Funnel Structure -> Specify VSL Form Factor',
        'Specify VSL Form Factor -> Define Metrics and Economic Guardrails',
        'Define Metrics and Economic Guardrails -> Align Creative and VSL Coherence',
      ],
      parallel: ['Metrics benchmark assembly can run in parallel with creative-coherence mapping after funnel structure exists.'],
      waitStates: ['Hold final release until pricing, funnel path, and measurement rules are all approved.'],
      loops: ['Return from launch diagnosis to this SOP if market, pricing, or funnel architecture proves invalid.'],
      criticalPath:
        'Niche qualification -> pricing architecture -> funnel structure -> VSL specification -> guardrails',
    },
    ml: {
      domain: 'copy',
      category: 'funnel_architecture',
      risk: 'high',
      input: [
        ['source_draft', 'file', true, 'Original Thiago Roas architecture draft'],
        ['offer_brief', 'object', true, 'Offer hypothesis with niche and pricing context'],
        ['traffic_assumptions', 'object', false, 'Cold-traffic planning assumptions'],
      ],
    },
    references: [
      'squads/copy/data/sops/vsl-funnel-architecture-sop.md',
      'squads/traffic-masters/data/references/thiagoroas-vsl-funnel-and-traffic-framework.yaml',
    ],
    headings: {
      confidence: '## Tabela de Resumo de Confianca',
      gaps: '## GAPs e Verificacoes Necessarias',
      sources: null,
    },
    fallbacks: {
      confidence: 'See the source draft confidence table in the original architecture extraction.',
      gaps: 'See the original architecture draft for unresolved niche-sizing and pricing exceptions.',
    },
  },
  {
    slug: 'vsl-script-creation',
    title: 'VSL Script - Do Diagnostico ao Script Final',
    sopId: 'SOP-COPY-VSL-SCRIPT-001',
    version: '0.1',
    classification: 'MAJOR',
    level: 'OPERATIONAL',
    processId: 'vsl-script-creation',
    sourcePath: 'squads/copy/data/sops/vsl-script-creation-sop.md',
    sourceMaterial: [
      'Palestra ao vivo + podcast de Thiago Roas',
      'thiagoroas-copy-analysis.yaml',
      'thiagoroas-vsl-funnel-and-traffic-framework.yaml',
    ],
    purpose:
      'To turn a validated VSL architecture into a script that graduates cold prospects from awareness to purchase readiness.',
    scopeIn: [
      'Awareness diagnosis and belief sequencing for a new VSL',
      'Lead selection, mechanism framing, format choice, and core script assembly',
      'Human plus AI production workflow up to a script ready for recording',
    ],
    scopeOut: [
      'Diagnosing an already-running VSL with live metrics',
      'Traffic account setup or campaign deployment',
    ],
    applicability:
      'Copy Chief, mechanism strategist, script operator, reviewer, and downstream copy agents that need a canonical VSL-writing SOP.',
    standards: [
      ['SOP Factory extract-sop', 'squads/aiox-sop/tasks/extract-sop.md'],
      ['Deming/Juran', 'Structured planning, control, and review before release'],
      ['Schwartz/Benson/Kennedy', 'Awareness progression, structure, and direct-response discipline'],
    ],
    definitions: [
      ['Lead', 'Opening segment that validates pain and earns the next minutes of attention.'],
      ['Mechanism', 'The explanatory frame that makes the offer feel uniquely solvable.'],
      ['Awareness level', 'Prospect state from problem-aware to most-aware.'],
      ['Format', 'Visual and performance style of the VSL separate from the words themselves.'],
      ['Micro-video', 'Distinct segment inside the VSL used to reset attention and retention.'],
      ['Post-pitch page', 'Page section and supporting elements shown after the offer reveal.'],
    ],
    roles: ['Copy Chief', 'Mechanism Strategist', 'Script Operator', 'Reviewer'],
    raci: [
      ['Diagnose awareness and sophistication', 'A', 'R', 'I', 'C'],
      ['Define lead and mechanism path', 'A', 'R', 'C', 'I'],
      ['Assemble script structure and body', 'C', 'C', 'A', 'R'],
      ['Run AI-assisted production pass', 'C', 'C', 'A', 'R'],
      ['Approve script before recording', 'A', 'C', 'R', 'C'],
    ],
    materials: [
      ['Thiago Roas source draft', 'Markdown source', '1', 'Primary extraction reference'],
      ['Persona and offer brief', 'Working document', '1', 'Required before writing'],
      ['Reference VSL set', 'Prior winning VSL examples', '1+', 'Used to seed structure and AI passes'],
    ],
    systems: [
      ['Repository workspace', 'Read access', 'Project maintainer'],
      ['Writing environment', 'Edit access', 'Copy Chief'],
      ['AI drafting tool', 'Operator access', 'Copy Chief'],
    ],
    training: [
      ['Awareness progression review', 'Internal', 'Current'],
      ['Mechanism and objection sequencing review', 'Internal', 'Current'],
    ],
    conditions: [
      'The funnel architecture and front-end offer are already defined.',
      'The team has persona, objections, and benchmark context before writing.',
      'The script will target a new VSL rather than a repair of an existing live VSL.',
    ],
    trigger: {
      type: 'manual',
      description: 'Use when writing a new VSL from zero after architecture is approved.',
      source: 'Copy Chief',
    },
    phases: [
      {
        title: 'Diagnose Awareness and Market Sophistication',
        performer: 'Mechanism Strategist',
        duration: 'PT45M',
        durationLabel: '45 minutes',
        actions: [
          'Define the awareness level of the traffic entering the VSL, defaulting to level 2-3 for cold R$297 traffic. [DOC]',
          'Map the awareness graduation the VSL must complete before the pitch. [DOC]',
          'Set the sophistication stage and record any assumptions that were inferred rather than stated. [REP]',
        ],
        expected: 'A written awareness map that governs lead, mechanism, and proof order.',
        source:
          'vsl-script-creation-sop.md -> Fase 1; schwartz_analysis; schwartz_enrichment',
      },
      {
        title: 'Map Beliefs to Create and Beliefs to Break',
        performer: 'Copy Chief',
        duration: 'PT30M',
        durationLabel: '30 minutes',
        actions: [
          'List the beliefs that must be created at each awareness transition. [DOC]',
          'List the blocking beliefs and objections that must be broken before the next transition. [DOC]',
          'Sequence those beliefs so each acceptance makes the next conclusion easier. [REP]',
        ],
        expected: 'A belief ladder connected to the awareness map.',
        source:
          'vsl-script-creation-sop.md -> 1.4; thiagoroas-copy-analysis.yaml',
      },
      {
        title: 'Select Lead and Mechanism',
        performer: 'Mechanism Strategist',
        duration: 'PT35M',
        durationLabel: '35 minutes',
        actions: [
          'Choose the lead style that matches the awareness level brought by the creative. [DOC]',
          'Define the mechanism that explains why the prospect has not solved the problem yet. [REP]',
          'Prepare at least three lead variants before choosing the production candidate. [DOC]',
        ],
        expected: 'A lead pack and mechanism statement ready for script assembly.',
        source:
          'vsl-script-creation-sop.md -> 1.1 to 1.4; brown_analysis; benson_analysis',
      },
      {
        title: 'Design Structure and Format',
        performer: 'Script Operator',
        duration: 'PT40M',
        durationLabel: '40 minutes',
        actions: [
          'Lay out the VSL in at least five micro-videos with explicit segment intent. [DOC]',
          'Choose the format based on retention logic before rewriting copy. [DOC]',
          'Lock the target duration near the proven 20-30 minute range for the benchmark offer. [DOC]',
        ],
        expected: 'A structural outline with format notes and timing targets.',
        source:
          'vsl-script-creation-sop.md -> Benson structure and format phases; vsl_sizing',
      },
      {
        title: 'Write the Core Argument',
        performer: 'Script Operator',
        duration: 'PT2H',
        durationLabel: '2 hours',
        actions: [
          'Draft the body so problem agitation, mechanism, proof, and offer escalate in the planned order. [REP]',
          'Interleave create-belief and break-belief moves through the body rather than batching them blindly. [INF]',
          'Preserve direct-response clarity and action pressure through the pitch and CTA. [DOC]',
        ],
        expected: 'A full long-form body draft with argument flow and CTA path.',
        source:
          'vsl-script-creation-sop.md -> Fases 3, 4, and 5; kennedy_analysis',
      },
      {
        title: 'Run AI-Assisted Production',
        performer: 'Script Operator',
        duration: 'PT90M',
        durationLabel: '90 minutes',
        actions: [
          'Feed the structure and references into the preferred AI workflow, keeping the human strategy layer in control. [DOC]',
          'Use prior winning VSLs as structural context rather than copying their surface language. [REP]',
          'Flag any unsupported AI-generated claims as assumptions for manual review. [ASM]',
        ],
        expected: 'A production-ready draft with explicit review flags.',
        source:
          'vsl-script-creation-sop.md -> Fase 6; Manus AI workflow reference',
      },
      {
        title: 'Validate the Script',
        performer: 'Reviewer',
        duration: 'PT45M',
        durationLabel: '45 minutes',
        actions: [
          'Check whether the awareness journey is complete by the time the pitch arrives. [DOC]',
          'Verify that format, lead, and offer logic are coherent before requesting copy rewrites. [DOC]',
          'Record any low-confidence areas that require A/B testing or practitioner verification. [DOC]',
        ],
        expected: 'A validated draft with review notes and unresolved assumptions clearly marked.',
        source:
          'vsl-script-creation-sop.md -> Fase 7; confidence table and gaps',
      },
      {
        title: 'Prepare Post-Pitch Support',
        performer: 'Copy Chief',
        duration: 'PT30M',
        durationLabel: '30 minutes',
        actions: [
          'Align the post-pitch page and supporting elements with the VSL promise. [DOC]',
          'Prepare the downsell and follow-up logic without introducing unsupported new mechanics. [DOC]',
          'Document any ticket or niche exceptions that require a later diagnostic loop. [INF]',
        ],
        expected: 'A final script package ready for recording and funnel-page assembly.',
        source:
          'vsl-script-creation-sop.md -> Fase 8; page and downsell notes',
      },
    ],
    decisionPoints: [
      {
        title: 'Awareness Entry Decision',
        if: 'Creative input indicates level 2-3 awareness.',
        then: 'Use the standard cold-traffic graduation path through mechanism and proof.',
        elseIf: 'Traffic enters at a materially different awareness level.',
        altAction: 'Rebuild the lead and belief path before drafting the body.',
        escalate: 'Copy Chief',
      },
      {
        title: 'Format Before Copy Decision',
        if: 'Retention logic points to a format problem.',
        then: 'Change format assumptions before rewriting the copy body.',
        elseIf: 'Format is sound and conversion logic is weak.',
        altAction: 'Revise the argument and belief sequencing while preserving the format.',
        escalate: 'Reviewer',
      },
    ],
    dependencies: {
      sequential: [
        'Diagnose Awareness -> Map Beliefs',
        'Map Beliefs -> Select Lead and Mechanism',
        'Select Lead and Mechanism -> Design Structure and Format',
        'Design Structure and Format -> Write the Core Argument',
        'Write the Core Argument -> Run AI-Assisted Production',
        'Run AI-Assisted Production -> Validate the Script',
        'Validate the Script -> Prepare Post-Pitch Support',
      ],
      parallel: ['Lead exploration and mechanism exploration can run in parallel before the final outline is locked.'],
      waitStates: ['Do not release for recording until review flags and unsupported claims are resolved or explicitly accepted.'],
      loops: ['If live retention fails after launch, route to the diagnostic SOP and return here only after the root cause is clear.'],
      criticalPath:
        'Awareness diagnosis -> belief map -> lead/mechanism -> structure -> core argument -> validation',
    },
    ml: {
      domain: 'copy',
      category: 'script_creation',
      risk: 'high',
      input: [
        ['source_draft', 'file', true, 'Original Thiago Roas script-creation draft'],
        ['persona_brief', 'object', true, 'Audience pains, desires, and objections'],
        ['offer_brief', 'object', true, 'Offer, ticket, and mechanism context'],
      ],
    },
    references: [
      'squads/copy/data/sops/vsl-script-creation-sop.md',
      'squads/copy/data/references/thiagoroas-copy-analysis.yaml',
      'squads/traffic-masters/data/references/thiagoroas-vsl-funnel-and-traffic-framework.yaml',
    ],
    headings: {
      confidence: '## Tabela de Confianca por Fase',
      gaps: '## Gaps e Itens para Verificacao',
      sources: '## Referencias das Fontes',
    },
    fallbacks: {
      confidence: 'See the original script-creation draft for phase-level confidence notes.',
      gaps: 'See the original script-creation draft for unresolved AI, ticket, and sequencing questions.',
    },
  },
  {
    slug: 'vsl-diagnostic-optimization',
    title: 'VSL Diagnostico e Otimizacao - Protocolo de Correcao',
    sopId: 'SOP-COPY-VSL-DIAG-001',
    version: '0.1',
    classification: 'MAJOR',
    level: 'OPERATIONAL',
    processId: 'vsl-diagnostic-optimization',
    sourcePath: 'squads/copy/data/sops/vsl-diagnostic-optimization-sop.md',
    sourceMaterial: [
      'Palestra ao vivo + podcast de Thiago Roas',
      'thiagoroas-vsl-funnel-and-traffic-framework.yaml',
      'thiagoroas-copy-analysis.yaml',
    ],
    purpose:
      'To diagnose and correct a live VSL funnel by isolating the first failing micro-funnel and applying the right fix in the right order.',
    scopeIn: [
      'Metric collection and benchmark comparison for live VSL funnels',
      'Micro-funnel isolation, 2x2 matrix diagnosis, and prioritized fix selection',
      'Recovery, scaling, and kill decisions using the 731 model and funnel economics',
    ],
    scopeOut: [
      'Writing a net-new VSL from zero',
      'Campaign build or media buying execution details',
    ],
    applicability:
      'Copy Chief, Performance Analyst, Creative Analyst, Operator, and downstream diagnostic agents working on a live VSL funnel.',
    standards: [
      ['SOP Factory extract-sop', 'squads/aiox-sop/tasks/extract-sop.md'],
      ['Deming/Juran', 'Check-then-act loop for continual improvement'],
      ['Thiago Roas diagnostic matrix', 'Retention/conversion root-cause routing'],
    ],
    definitions: [
      ['Micro-funnel', 'A single stage of the funnel isolated for diagnosis.'],
      ['Pitch retention', 'Percentage of viewers still watching when the offer is presented.'],
      ['Modelo 731', 'Decision frame using 7-day, 3-day, and current-day views.'],
      ['Custo de checkout', 'Primary cost metric for VSL traffic efficiency.'],
      ['Order bump', 'Checkout add-on offer tested after baseline checkout clarity is known.'],
      ['Recovery webinar', 'Post-upsell recovery mechanism for front buyers who decline the upsell.'],
    ],
    roles: ['Copy Chief', 'Performance Analyst', 'Creative Analyst', 'Operator'],
    raci: [
      ['Collect benchmark metrics', 'C', 'R', 'I', 'A'],
      ['Map micro-funnel health', 'C', 'R', 'I', 'A'],
      ['Apply diagnostic matrix and root-cause verdict', 'A', 'C', 'R', 'I'],
      ['Approve fix order and implementation path', 'A', 'C', 'C', 'R'],
      ['Approve scale, hold, or kill decision', 'C', 'A', 'C', 'R'],
    ],
    materials: [
      ['Live VSL analytics', 'Retention + conversion data', '1 set', 'Required before diagnosis starts'],
      ['Thiago Roas source draft', 'Markdown source', '1', 'Primary extraction reference'],
      ['Traffic and revenue dashboard', '7d / 3d / today views', '1', 'Used for 731 decisions'],
    ],
    systems: [
      ['Analytics platform', 'Read access', 'Performance Analyst'],
      ['Ad platform dashboard', 'Read access', 'Performance Analyst'],
      ['Repository workspace', 'Read access', 'Project maintainer'],
    ],
    training: [
      ['VSL diagnostic matrix review', 'Internal', 'Current'],
      ['731 model review', 'Internal', 'Current'],
    ],
    conditions: [
      'The VSL has been live long enough to gather meaningful data.',
      'The team can isolate page, VSL, checkout, upsell, and recovery metrics.',
      'The operator will not skip directly to copy rewrites before the matrix diagnosis is complete.',
    ],
    trigger: {
      type: 'manual',
      description: 'Use when a VSL funnel is live and underperforming or scaling unstably.',
      source: 'Performance Analyst or Copy Chief',
    },
    phases: [
      {
        title: 'Collect Metrics',
        performer: 'Performance Analyst',
        duration: 'PT45M',
        durationLabel: '45 minutes',
        actions: [
          'Pull retention, play rate, checkout, upsell, downsell, and ticket metrics into one table. [DOC]',
          'Record the known benchmark next to each actual metric before judging performance. [DOC]',
          'Reject diagnosis if the data window is too thin to support a real decision. [INF]',
        ],
        expected: 'A benchmarked metrics table with all primary signals captured.',
        source:
          'vsl-diagnostic-optimization-sop.md -> Phase 1; funnel_health_metrics; vsl_retention.benchmarks',
      },
      {
        title: 'Separate Micro-Funnels',
        performer: 'Performance Analyst',
        duration: 'PT30M',
        durationLabel: '30 minutes',
        actions: [
          'Break the funnel into traffic, page, VSL, checkout, upsell, and recovery stages. [DOC]',
          'Mark each stage as healthy, at risk, or failing. [DOC]',
          'Identify the first failing stage in sequence before proposing any fix. [DOC]',
        ],
        expected: 'A micro-funnel health map with the earliest failure point identified.',
        source:
          'vsl-diagnostic-optimization-sop.md -> Phase 2; vsl_micro_funnels.principle',
      },
      {
        title: 'Apply the 2x2 Diagnostic Matrix',
        performer: 'Copy Chief',
        duration: 'PT15M',
        durationLabel: '15 minutes',
        actions: [
          'Classify the VSL into the retention/conversion quadrant defined by the matrix. [DOC]',
          'Route the case to scale, format change, copy rewrite, or new VSL according to the quadrant. [DOC]',
          'Record the verdict before any tactical edits start. [DOC]',
        ],
        expected: 'A root-cause verdict tied to the matrix quadrant.',
        source:
          'vsl-diagnostic-optimization-sop.md -> Phase 3; vsl_diagnostic_matrix',
      },
      {
        title: 'Diagnose the Specific Symptom',
        performer: 'Creative Analyst',
        duration: 'PT35M',
        durationLabel: '35 minutes',
        actions: [
          'Inspect the exact symptom inside the failing stage, such as low play rate, weak lead, or offer drop shape. [DOC]',
          'Confirm whether the issue is format, copy, page, checkout, or post-purchase logic. [DOC]',
          'Flag any explanation that depends on inference rather than direct evidence. [INF]',
        ],
        expected: 'A symptom-level diagnosis attached to the matrix verdict.',
        source:
          'vsl-diagnostic-optimization-sop.md -> Phases 4 and 5; source provenance',
      },
      {
        title: 'Execute the Fix in Priority Order',
        performer: 'Operator',
        duration: 'PT2H',
        durationLabel: '2 hours',
        actions: [
          'Apply the fix at the earliest failing stage instead of patching downstream symptoms first. [DOC]',
          'Change format before copy when retention says format is the problem. [DOC]',
          'Keep a clean baseline and reintroduce optional elements such as bumps only after the core path is healthy. [DOC]',
        ],
        expected: 'A prioritized fix log with clear before/after state for the first failing stage.',
        source:
          'vsl-diagnostic-optimization-sop.md -> Phases 4 to 7; funnel_health_metrics',
      },
      {
        title: 'Run Scale or Kill Logic',
        performer: 'Performance Analyst',
        duration: 'PT30M',
        durationLabel: '30 minutes',
        actions: [
          'Review 7-day, 3-day, and current-day performance before changing budgets. [DOC]',
          'Increase spend only within the proven 20% guardrail when the system is stable. [DOC]',
          'Kill the asset or branch when repeated negative evidence persists instead of rationalizing the loss. [DOC]',
        ],
        expected: 'A documented hold, scale, or kill decision with 731 evidence.',
        source:
          'vsl-diagnostic-optimization-sop.md -> Phase 6 and Phase 8; Modelo 731',
      },
      {
        title: 'Document Recovery and Learning',
        performer: 'Copy Chief',
        duration: 'PT20M',
        durationLabel: '20 minutes',
        actions: [
          'Record whether recovery webinar or post-purchase changes are justified by the diagnosis. [DOC]',
          'Capture unresolved technical questions as review items rather than hiding them inside the SOP. [REP]',
          'Route format or script rebuilds back to the creation SOP only after the root cause is confirmed. [DOC]',
        ],
        expected: 'A final diagnostic report with next-step routing and unresolved questions surfaced.',
        source:
          'vsl-diagnostic-optimization-sop.md -> Phase 7 onward; source provenance',
      },
    ],
    decisionPoints: [
      {
        title: 'Matrix Verdict Decision',
        if: 'Retention is high and conversion is high.',
        then: 'Scale according to the traffic guardrails.',
        elseIf: 'The matrix points to copy, format, or a full new VSL.',
        altAction: 'Execute only the fix class specified by the matrix before changing anything else.',
        escalate: 'Copy Chief',
      },
      {
        title: 'Scale vs Kill Decision',
        if: 'The 731 view shows stable positive signal.',
        then: 'Scale inside the budget guardrails.',
        elseIf: 'The 731 view stays negative after the fix window.',
        altAction: 'Kill or replace the asset instead of forcing more spend.',
        escalate: 'Performance Analyst',
      },
    ],
    dependencies: {
      sequential: [
        'Collect Metrics -> Separate Micro-Funnels',
        'Separate Micro-Funnels -> Apply the 2x2 Diagnostic Matrix',
        'Apply the 2x2 Diagnostic Matrix -> Diagnose the Specific Symptom',
        'Diagnose the Specific Symptom -> Execute the Fix in Priority Order',
        'Execute the Fix in Priority Order -> Run Scale or Kill Logic',
        'Run Scale or Kill Logic -> Document Recovery and Learning',
      ],
      parallel: ['Creative symptom analysis can proceed in parallel with post-purchase path inspection after the failing stage is known.'],
      waitStates: ['Hold scale decisions until benchmarked metrics and the matrix verdict are both complete.'],
      loops: ['Repeat the collect -> isolate -> diagnose cycle after each significant fix until the first failing stage changes or disappears.'],
      criticalPath:
        'Metric collection -> micro-funnel isolation -> matrix verdict -> targeted fix -> 731 decision',
    },
    ml: {
      domain: 'copy',
      category: 'diagnostic_optimization',
      risk: 'high',
      input: [
        ['source_draft', 'file', true, 'Original Thiago Roas diagnostic draft'],
        ['analytics_snapshot', 'object', true, 'Retention, checkout, and post-purchase metrics'],
        ['traffic_snapshot', 'object', true, '7d / 3d / today media data'],
      ],
    },
    references: [
      'squads/copy/data/sops/vsl-diagnostic-optimization-sop.md',
      'squads/traffic-masters/data/references/thiagoroas-vsl-funnel-and-traffic-framework.yaml',
      'squads/copy/data/references/thiagoroas-copy-analysis.yaml',
    ],
    headings: {
      confidence: '## 9. Confidence Summary Table',
      gaps: '## 10. Gaps & Verification Needed',
      sources: '## 12. Source Provenance',
    },
    fallbacks: {
      confidence: 'See the original diagnostic draft for phase-by-phase confidence signals.',
      gaps: 'See the original diagnostic draft for unresolved fix-order, recovery, and benchmark questions.',
    },
  },
];

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function readRelative(relativePath) {
  return fs.readFileSync(path.join(ROOT, relativePath), 'utf8');
}

function writeRelative(relativePath, content) {
  const absolutePath = path.join(ROOT, relativePath);
  ensureDir(path.dirname(absolutePath));
  fs.writeFileSync(absolutePath, content, 'utf8');
}

function parseArgs(argv) {
  const args = {
    business: null,
  };

  for (const raw of argv) {
    if (raw.startsWith('--business=')) {
      args.business = raw.slice('--business='.length).trim() || null;
    }
  }

  return args;
}

function buildMlRoot(args) {
  if (args.business) {
    return path.join('workspace', 'businesses', args.business, 'sops');
  }

  return path.join('squads', 'aiox-sop', 'docs', 'sops');
}

function normalizeText(value) {
  return value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/\r\n/g, '\n');
}

function extractSection(text, heading) {
  if (!heading) {
    return '';
  }
  const normalized = text.replace(/\r\n/g, '\n');
  const lines = normalized.split('\n');
  const target = normalizeText(heading.trim());
  let startLine = -1;
  for (let index = 0; index < lines.length; index += 1) {
    if (normalizeText(lines[index].trim()) === target) {
      startLine = index;
      break;
    }
  }
  if (startLine === -1) {
    return '';
  }
  let endLine = lines.length;
  for (let index = startLine + 1; index < lines.length; index += 1) {
    if (/^##\s+/.test(lines[index])) {
      endLine = index;
      break;
    }
  }
  return lines.slice(startLine, endLine).join('\n').trim();
}

function parseMarkdownTable(section) {
  if (!section) {
    return [];
  }
  const lines = section
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.startsWith('|'));
  if (lines.length < 3) {
    return [];
  }
  const headers = lines[0]
    .split('|')
    .slice(1, -1)
    .map((cell) => cell.trim());
  const rows = [];
  for (const line of lines.slice(2)) {
    const cells = line
      .split('|')
      .slice(1, -1)
      .map((cell) => cell.trim());
    if (!cells.some(Boolean)) {
      continue;
    }
    const row = {};
    headers.forEach((header, index) => {
      row[header] = cells[index] || '';
      row[normalizeText(header)] = cells[index] || '';
    });
    rows.push(row);
  }
  return rows;
}

function valueFromRow(row, keys) {
  for (const key of keys) {
    if (row[key]) {
      return row[key];
    }
    const normalizedKey = normalizeText(key);
    if (row[normalizedKey]) {
      return row[normalizedKey];
    }
  }
  return '';
}

function normalizePriority(value, confidence) {
  const lower = `${value} ${confidence}`.toLowerCase();
  if (lower.includes('alta') || lower.includes('high') || lower.includes('0.3') || lower.includes('[asm]')) {
    return 'HIGH';
  }
  if (lower.includes('0.5') || lower.includes('[inf]')) {
    return 'HIGH';
  }
  if (lower.includes('media') || lower.includes('medium')) {
    return 'MEDIUM';
  }
  return 'REVIEW';
}

function normalizeGaps(pkg, sourceText) {
  const rawSection = extractSection(sourceText, pkg.headings.gaps);
  const rows = parseMarkdownTable(rawSection);
  if (!rows.length) {
    return [
      {
        id: `${pkg.slug.toUpperCase().replace(/-/g, '_')}-GAP-01`,
        item: 'Source gap extraction unavailable',
        confidence: 'REVIEW',
        description: pkg.fallbacks.gaps,
        verification: 'Review the source draft manually before using this SOP operationally.',
        priority: 'HIGH',
      },
    ];
  }
  return rows.map((row, index) => {
    const description =
      valueFromRow(row, ['Gap Description', 'Razao', 'Detalhe', 'Description']) || 'See source draft for details.';
    const rawItem = valueFromRow(row, ['Item', 'Gap', 'Gap ID']) || `Gap ${index + 1}`;
    const item = /^(gap\b|gap-\d+|\d+)$/i.test(rawItem)
      ? description.replace(/\.$/, '').slice(0, 96)
      : rawItem;
    const confidence = valueFromRow(row, ['Current Confidence', 'Confiança']) || 'REVIEW';
    const verification =
      valueFromRow(row, ['Verification Needed', 'Como verificar']) ||
      'Obtain direct practitioner validation and update the extraction package.';
    const priority = normalizePriority(valueFromRow(row, ['Prioridade']), confidence);
    const id = valueFromRow(row, ['Gap ID']) || `${pkg.sopId}-GAP-${String(index + 1).padStart(2, '0')}`;
    return { id, item, confidence, description, verification, priority };
  });
}

function summarizeLowConfidence(section) {
  if (!section) {
    return [];
  }
  return section
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.startsWith('|'))
    .filter((line) => /\[INF|\[ASM|0\.3|0\.5/.test(line))
    .map((line) => line.split('|')[1].trim())
    .filter(Boolean);
}

function summarizeAssumptions(sourceText) {
  return sourceText
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.includes('[ASM]'))
    .slice(0, 5);
}

function renderTable(headers, rows) {
  const headerLine = `| ${headers.join(' | ')} |`;
  const separator = `| ${headers.map(() => '---').join(' | ')} |`;
  const body = rows.map((row) => `| ${row.join(' | ')} |`).join('\n');
  return [headerLine, separator, body].filter(Boolean).join('\n');
}

function renderHumanDraft(pkg, sourceText, confidenceSection, normalizedGaps) {
  const gapRows = normalizedGaps.map((gap) => [
    gap.id,
    gap.item,
    gap.confidence,
    gap.description,
    gap.verification,
    gap.priority,
  ]);

  const definitions = renderTable(
    ['Term / Abbreviation', 'Definition'],
    pkg.definitions.map(([term, definition]) => [term, definition])
  );
  const standards = renderTable(
    ['Standard', 'Reference'],
    pkg.standards.map(([name, ref]) => [name, ref])
  );
  const raci = renderTable(
    ['Activity', ...pkg.roles],
    pkg.raci.map(([activity, ...cells]) => [activity, ...cells])
  );
  const materials = renderTable(
    ['Item', 'Specification', 'Quantity', 'Notes'],
    pkg.materials.map(([item, spec, quantity, notes]) => [item, spec, quantity, notes])
  );
  const systems = renderTable(
    ['System', 'Permission Level', 'How to Request'],
    pkg.systems.map(([system, permission, request]) => [system, permission, request])
  );
  const training = renderTable(
    ['Training Module', 'Certification ID', 'Validity Period'],
    pkg.training.map(([module, certification, validity]) => [module, certification, validity])
  );

  const procedureBlocks = pkg.phases
    .map((phase, index) => {
      const stepNumber = `5.${index + 1}`;
      const actions = phase.actions.map((action, actionIndex) => `${actionIndex + 1}. ${action}`).join('\n');
      return [
        `### ${stepNumber} ${phase.title}`,
        '',
        `**Performer:** ${phase.performer}`,
        `**Estimated Time:** ${phase.durationLabel}`,
        '',
        actions,
        '',
        `**Expected Result:** ${phase.expected}`,
        `**Source Basis:** ${phase.source}`,
      ].join('\n');
    })
    .join('\n\n---\n\n');

  const decisionBlocks = pkg.decisionPoints
    .map((decision, index) =>
      [
        `### 5.${pkg.phases.length + index + 1} Decision Point: ${decision.title}`,
        '',
        `**IF** ${decision.if}:`,
        `- ${decision.then}`,
        '',
        `**ELSE IF** ${decision.elseIf}:`,
        `- ${decision.altAction}`,
        '',
        '**ELSE:**',
        `- STOP and escalate to ${decision.escalate}.`,
      ].join('\n')
    )
    .join('\n\n---\n\n');

  const dependencyTable = renderTable(
    ['Dependency Type', 'Details'],
    [
      ['Sequential', pkg.dependencies.sequential.join('<br>')],
      ['Parallel', pkg.dependencies.parallel.join('<br>')],
      ['Wait States', pkg.dependencies.waitStates.join('<br>')],
      ['Loops', pkg.dependencies.loops.join('<br>')],
      ['Critical Path', pkg.dependencies.criticalPath],
    ]
  );

  const confidenceBody = confidenceSection
    ? confidenceSection.replace(/^##[^\n]*\n?/, '').trim()
    : pkg.fallbacks.confidence;

  const sourcesTable = renderTable(
    ['Source Type', 'Location', 'Usage'],
    [
      ['Primary draft', pkg.sourcePath, 'Original research extraction preserved as source material'],
      ...pkg.references.slice(1).map((ref) => ['Supporting reference', ref, 'Supporting provenance and benchmark validation']),
    ]
  );

  return [
    `# ${pkg.title}`,
    '',
    renderTable(
      ['Field', 'Value'],
      [
        ['**SOP ID**', pkg.sopId],
        ['**Version**', `${pkg.version}-draft`],
        ['**Effective Date**', TODAY],
        ['**Author**', 'Ohno (SOP Extractor) / SOP Factory Squad'],
        ['**Approver**', 'SOP Chief (pending)'],
        ['**Next Review**', REVIEW_DATE],
        ['**Classification**', pkg.classification],
        ['**Status**', 'DRAFT - EXTRACTED'],
        ['**Process ID**', pkg.processId],
        ['**Executor**', pkg.roles.join(', ')],
        ['**Level**', pkg.level],
      ]
    ),
    '',
    `> **Provenance:** ${PROVENANCE_NOTE}`,
    `> **Source Material:** ${pkg.sourceMaterial.join('; ')}`,
    '',
    '---',
    '',
    '## 1. Purpose & Scope',
    '',
    '### 1.1 Purpose',
    '',
    pkg.purpose,
    '',
    '### 1.2 Scope',
    '',
    '**In Scope:**',
    ...pkg.scopeIn.map((item) => `- ${item}`),
    '',
    '**Out of Scope:**',
    ...pkg.scopeOut.map((item) => `- ${item}`),
    '',
    '### 1.3 Applicability',
    '',
    pkg.applicability,
    '',
    '### 1.4 Applicable Standards',
    '',
    standards,
    '',
    '---',
    '',
    '## 2. Definitions & Abbreviations',
    '',
    definitions,
    '',
    '---',
    '',
    '## 3. Roles & Responsibilities (RACI)',
    '',
    raci,
    '',
    '---',
    '',
    '## 4. Prerequisites',
    '',
    '### 4.1 Materials & Equipment',
    '',
    materials,
    '',
    '### 4.2 System Access & Permissions',
    '',
    systems,
    '',
    '### 4.3 Required Training',
    '',
    training,
    '',
    '### 4.4 Environmental Conditions / Preconditions',
    '',
    ...pkg.conditions.map((condition) => `- [ ] ${condition}`),
    '',
    '---',
    '',
    '## 5. Procedure',
    '',
    '> **INSTRUCTION:** Execute steps sequentially unless a decision point routes the work elsewhere. Do not skip the validation and review stages.',
    '',
    procedureBlocks,
    '',
    decisionBlocks,
    '',
    '---',
    '',
    '## 6. Dependency Map',
    '',
    dependencyTable,
    '',
    '---',
    '',
    '## 7. Confidence Summary',
    '',
    confidenceBody,
    '',
    '---',
    '',
    '## 8. Gaps & Review Items',
    '',
    renderTable(
      ['Gap ID', 'Item', 'Current Confidence', 'Gap Description', 'Verification Needed', 'Priority'],
      gapRows
    ),
    '',
    '---',
    '',
    '## 9. Teach-Back Validation',
    '',
    '1. Hand this draft to a reviewer who did not perform the extraction.',
    '2. Ask the reviewer to explain the process back, step by step, without using the source draft.',
    '3. Record where the reviewer hesitates, asks questions, skips a dependency, or misstates a decision rule.',
    '4. Update the SOP, gap report, and ML artifact before operational use.',
    '',
    '**Teach-Back Pass Criteria:**',
    '- All critical steps can be restated without external prompting.',
    '- All decision points route cleanly to one next action.',
    '- All unresolved assumptions remain visible in the gap report.',
    '',
    '---',
    '',
    '## 10. Sources',
    '',
    sourcesTable,
    '',
    `Detailed source draft: \`${pkg.sourcePath}\``,
  ].join('\n');
}

function renderGapReport(pkg, gaps) {
  const rows = gaps.map((gap) => [
    gap.id,
    gap.item,
    gap.confidence,
    gap.description,
    gap.verification,
    `What direct evidence or practitioner confirmation resolves "${gap.item}"?`,
  ]);

  return [
    `# Gap Report - ${pkg.title}`,
    '',
    `Source draft: \`${pkg.sourcePath}\``,
    `Generated: ${TODAY}`,
    '',
    renderTable(
      ['Gap ID', 'Item', 'Current Confidence', 'Description', 'Verification Needed', 'Interview Question'],
      rows
    ),
  ].join('\n');
}

function renderConfidenceReport(pkg, confidenceSection, lowConfidenceItems) {
  return [
    `# Confidence Report - ${pkg.title}`,
    '',
    `Source draft: \`${pkg.sourcePath}\``,
    `Generated: ${TODAY}`,
    '',
    '## Source Confidence Extract',
    '',
    confidenceSection
      ? confidenceSection.replace(/^##[^\n]*\n?/, '').trim()
      : pkg.fallbacks.confidence,
    '',
    '## Low-Confidence Items (< 0.7 or explicitly inferred/assumed)',
    '',
    ...(lowConfidenceItems.length
      ? lowConfidenceItems.map((item) => `- ${item}`)
      : ['- No explicit low-confidence row could be parsed automatically; review the gap report manually.']),
  ].join('\n');
}

function renderReviewSummary(pkg, gaps, lowConfidenceItems, assumptions) {
  return [
    `# Review Summary - ${pkg.title}`,
    '',
    `Generated: ${TODAY}`,
    '',
    '## Critical Gaps',
    '',
    ...(gaps.length ? gaps.map((gap) => `- ${gap.id}: ${gap.item} (${gap.priority})`) : ['- None']),
    '',
    '## Low-Confidence Items',
    '',
    ...(lowConfidenceItems.length
      ? lowConfidenceItems.map((item) => `- ${item}`)
      : ['- None parsed from the confidence table']),
    '',
    '## Assumptions Found',
    '',
    ...(assumptions.length ? assumptions.map((line) => `- ${line}`) : ['- None detected automatically']),
    '',
    '## Release Guidance',
    '',
    '- Do not treat this draft as audited or certified.',
    '- Resolve high-priority gaps before production use.',
    '- Run teach-back before routing the SOP into autonomous execution.',
  ].join('\n');
}

function renderTeachbackPlan(pkg) {
  return [
    `# Teach-Back Plan - ${pkg.title}`,
    '',
    `Generated: ${TODAY}`,
    '',
    '## Objective',
    '',
    'Validate whether a fresh operator or agent can restate the process accurately without relying on tribal knowledge.',
    '',
    '## Method',
    '',
    '1. Give the normalized draft SOP to a reviewer who did not participate in the extraction.',
    '2. Ask the reviewer to narrate the process back from trigger to expected result.',
    '3. Capture confusion around prerequisites, decision points, dependencies, and low-confidence steps.',
    '4. Update the draft, gap report, and ML artifact with the findings.',
    '',
    '## Focus Areas',
    '',
    '- Can the reviewer identify the trigger and stopping conditions?',
    '- Can the reviewer follow the dependency map without outside help?',
    '- Can the reviewer explain every decision point and escalation path?',
    '- Does the reviewer surface the same assumptions already marked in the gap report?',
    '',
    '## Exit Criteria',
    '',
    '- No missing prerequisite blocks execution.',
    '- Decision routing is understood without extra prompting.',
    '- Remaining gaps are explicit and acceptable for draft status.',
  ].join('\n');
}

function renderMlYaml(pkg, gaps) {
  const stepLines = pkg.phases
    .map((phase, index) => {
      const stepId = `S${String(index + 1).padStart(3, '0')}`;
      const nextStep = index === pkg.phases.length - 1 ? 'END' : `S${String(index + 2).padStart(3, '0')}`;
      const toolId = index < 2 ? 'source_reader' : 'manual_workspace';
      return [
        `    - id: "${stepId}"`,
        `      name: "${phase.title}"`,
        `      action: "${phase.title.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '')}"`,
        `      description: "${phase.expected}"`,
        `      performer: "${phase.performer}"`,
        `      critical: ${index < 2 ? 'true' : 'false'}`,
        `      estimated_duration: "${phase.duration}"`,
        '',
        '      tool:',
        `        id: "${toolId}"`,
        `        command: "follow normalized draft step ${stepId}"`,
        '        timeout: "PT30M"',
        '',
        '      input:',
        '        - name: "source_draft"',
        '          type: "file"',
        '          source: "system"',
        `          value: "${pkg.sourcePath}"`,
        '          required: true',
        '',
        '      output:',
        '        - name: "step_result"',
        '          type: "object"',
        `          store_as: "${phase.title.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '')}_result"`,
        '',
        '      validation:',
        '        type: "assertion"',
        '        rules:',
        '          - field: "step_result"',
        '            operator: "exists"',
        '            expected: "true"',
        `            message: "${phase.title} must produce a result object."`,
        '',
        `      on_success: "${nextStep}"`,
        '      on_failure: "EH001"',
        '      decision_point: null',
      ].join('\n');
    })
    .join('\n\n');

  const gapTags = gaps.map((gap) => `      - "${gap.id}"`).join('\n');
  const inputLines = pkg.ml.input
    .map(
      ([name, type, required, description]) =>
        [
          `      - name: "${name}"`,
          `        type: "${type}"`,
          `        required: ${required ? 'true' : 'false'}`,
          `        description: "${description}"`,
        ].join('\n')
    )
    .join('\n');

  return [
    'sop:',
    `  id: "${pkg.sopId}"`,
    `  version: "${pkg.version}.0"`,
    `  title: "${pkg.title}"`,
    `  purpose: "${pkg.purpose}"`,
    '',
    '  classification:',
    `    domain: "${pkg.ml.domain}"`,
    `    category: "${pkg.ml.category}"`,
    `    risk_level: "${pkg.ml.risk}"`,
    '    compliance_tags:',
    '      - "SOP-FACTORY-EXTRACT"',
    '      - "DRAFT-EXTRACTED"',
    `  status: "DRAFT"`,
    `  effective_date: "${TODAY}"`,
    `  review_date: "${REVIEW_DATE}"`,
    '',
    '  trigger:',
    `    type: "${pkg.trigger.type}"`,
    `    description: "${pkg.trigger.description}"`,
    '    event: ""',
    '    schedule: ""',
    `    source: "${pkg.trigger.source}"`,
    '    conditions:',
    '      - field: "source_draft"',
    '        operator: "exists"',
    '        value: "true"',
    '',
    '  context:',
    '    tools:',
    '      - id: "source_reader"',
    '        name: "Repository Draft Reader"',
    '        type: "cli"',
    '        version: "1.0"',
    '        required: true',
    '      - id: "manual_workspace"',
    '        name: "Operator Workspace"',
    '        type: "manual"',
    '        version: "1.0"',
    '        required: true',
    '',
    '    permissions:',
    '      - resource: "repository-files"',
    '        action: "read"',
    '        scope: "source drafts and published outputs"',
    '        justification: "Required to consume the extracted SOP package safely."',
    '',
    '    environment:',
    '      - key: "AIOX_RUNTIME_MODE"',
    '        description: "Current SOP Factory runtime mode"',
    '        required: true',
    '        sensitive: false',
    '',
    '    input:',
    inputLines,
    '',
    '  steps:',
    stepLines,
    '',
    '  error_handling:',
    '    handlers:',
    '      - id: "EH001"',
    '        name: "Escalate review failure"',
    '        trigger_on:',
    '          - error_type: "validation"',
    '        action: "Stop execution, update gap report, and request human review."',
    '',
    '  success_criteria:',
    '    - "All procedure steps produce an output object."',
    '    - "Teach-back is completed before autonomous use."',
    '    - "High-priority gaps are visible in companion reports."',
    '',
    '  review_flags:',
    gapTags || '      - "NO_GAPS_PARSED"',
  ].join('\n');
}

function renderIndex(packages, args) {
  const rows = packages.map((pkg) => [
    pkg.title,
    `draft-${pkg.slug}-sop-v0.1.md`,
    `draft-${pkg.slug}-sop-v0.1.yaml`,
    `gaps-${pkg.slug}-${TODAY}.md`,
    `confidence-${pkg.slug}-${TODAY}.md`,
    `review-items-${pkg.slug}-${TODAY}.md`,
    `teachback-${pkg.slug}-${TODAY}.md`,
  ]);
  return [
    '# Thiago Roas VSL Extraction Package',
    '',
    `Generated: ${TODAY}`,
    '',
    'Canonical markdown publish root: `docs/sops/`',
    `Canonical machine-readable publish root: \`${buildMlRoot(args)}/\``,
    'Auxiliary extraction reports root: `outputs/aiox-sop/extractions/`',
    '',
    renderTable(
      ['Process', 'Human Draft', 'ML Draft', 'Gap Report', 'Confidence Report', 'Review Summary', 'Teach-Back'],
      rows
    ),
    '',
    'Source drafts remain in `squads/copy/data/sops/` and are not the canonical publish surface.',
  ].join('\n');
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const mlRoot = buildMlRoot(args);

  ensureDir(DOCS_SOPS_ROOT);
  ensureDir(path.join(ROOT, mlRoot));
  ensureDir(AUXILIARY_OUTPUT_ROOT);
  for (const pkg of PACKAGES) {
    const sourceText = readRelative(pkg.sourcePath);
    const confidenceSection = extractSection(sourceText, pkg.headings.confidence);
    const gaps = normalizeGaps(pkg, sourceText);
    const lowConfidenceItems = summarizeLowConfidence(confidenceSection);
    const assumptions = summarizeAssumptions(sourceText);

    writeRelative(
      path.join('docs', 'sops', `draft-${pkg.slug}-sop-v0.1.md`),
      `${renderHumanDraft(pkg, sourceText, confidenceSection, gaps)}\n`
    );
    writeRelative(
      path.join(mlRoot, `draft-${pkg.slug}-sop-v0.1.yaml`),
      `${renderMlYaml(pkg, gaps)}\n`
    );
    writeRelative(
      path.join('outputs', 'aiox-sop', 'extractions', `gaps-${pkg.slug}-${TODAY}.md`),
      `${renderGapReport(pkg, gaps)}\n`
    );
    writeRelative(
      path.join('outputs', 'aiox-sop', 'extractions', `confidence-${pkg.slug}-${TODAY}.md`),
      `${renderConfidenceReport(pkg, confidenceSection, lowConfidenceItems)}\n`
    );
    writeRelative(
      path.join('outputs', 'aiox-sop', 'extractions', `review-items-${pkg.slug}-${TODAY}.md`),
      `${renderReviewSummary(pkg, gaps, lowConfidenceItems, assumptions)}\n`
    );
    writeRelative(
      path.join('outputs', 'aiox-sop', 'extractions', `teachback-${pkg.slug}-${TODAY}.md`),
      `${renderTeachbackPlan(pkg)}\n`
    );
  }

  writeRelative(
    path.join('outputs', 'aiox-sop', 'extractions', 'thiagoroas-vsl-package-index.md'),
    `${renderIndex(PACKAGES, args)}\n`
  );

  console.log(
    `PASS: normalized ${PACKAGES.length} Thiago Roas extraction packages into docs/sops/ and ${mlRoot}/`
  );
}

main();

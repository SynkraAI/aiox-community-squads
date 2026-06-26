#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const { buildOutput } = require('./load-context.cjs');
const runtimePaths = require('./runtime-paths.cjs');

const ROOT = process.cwd();
const DEFAULT_CONFIG_PATH = path.join(ROOT, 'squads', 'hormozi', 'config.yaml');
const DEFAULT_COMMANDS = [
  '*show-context',
  '*route [topic]',
  '*diagnose [business]',
  '*offers',
  '*pricing',
  '*audit [asset]',
];
const DEFAULT_SESSION_COMMAND = 'node squads/hormozi/scripts/set-active-context.cjs --business=aiox --product=<slug>';

function loadYamlFile(filePath) {
  return yaml.load(fs.readFileSync(filePath, 'utf8')) || {};
}

function formatCommandList(commands, maxItems) {
  return (commands || []).slice(0, maxItems).map((item) => `- \`${item}\``).join('\n');
}

function formatPathList(paths, maxItems) {
  return (paths || []).slice(0, maxItems).map((item) => `  - \`${item}\``).join('\n');
}

function buildContextSection(context, settings) {
  if (settings.activation?.show_context_report === false) {
    return '';
  }

  const lines = [
    '## Active Product Context',
    '',
    `- Business: \`${context.business_slug}\``,
    `- Product: \`${context.product_slug}\``,
    `- Readiness: \`${context.readiness.status}\``,
  ];

  if (context.workstream) {
    lines.push(`- Workstream: \`${context.workstream}\``);
  }

  if ((context.readiness.reasons || []).length > 0) {
    lines.push(`- Notes: ${(context.readiness.reasons || []).join(' | ')}`);
  }

  if (settings.activation?.show_preload_report !== false) {
    lines.push('');
    lines.push('## Preloaded References');
    lines.push('');
    lines.push(`- Session context: \`${context.session_context_path}\``);
    if (context.company_offerbook_index) {
      lines.push(`- Company offerbook index: \`${context.company_offerbook_index}\``);
    }
    if ((context.resolved_paths.shared_files || []).length > 0) {
      lines.push('- Shared files:');
      lines.push(formatPathList(context.resolved_paths.shared_files, settings.preload?.max_shared_files || 3));
    }
    if ((context.resolved_paths.product_files || []).length > 0) {
      lines.push('- Product files:');
      lines.push(formatPathList(context.resolved_paths.product_files, settings.preload?.max_product_files || 4));
    }
  }

  if ((context.readiness.missing_required || []).length > 0) {
    lines.push('');
    lines.push('## Blockers');
    lines.push('');
    lines.push(...context.readiness.missing_required.map((item) => `- \`${item.id}\`: \`${item.path || 'missing'}\``));
  }

  return lines.join('\n');
}

function generateGreeting() {
  const config = loadYamlFile(DEFAULT_CONFIG_PATH);
  const settings = config.settings || {};
  const sessionPath = runtimePaths.getHormoziSessionContextPath();
  let context = null;
  let contextError = null;

  if (fs.existsSync(sessionPath)) {
    try {
      context = buildOutput({ task: 'hormozi-chief', format: 'json' });
    } catch (error) {
      contextError = error.message;
    }
  }

  const intro = context
    ? 'Hormozi Chief ativo. Contexto de produto carregado do runtime da sessao.'
    : [
        'Hormozi Chief ativo. Nenhum contexto de produto foi inicializado nesta sessao.',
        '',
        '## Session Bootstrap',
        '',
        `- Inicialize com: \`${DEFAULT_SESSION_COMMAND}\``,
        '- Depois rode `*show-context` para conferir o readiness do COO e as fontes canônicas.',
        `- Runtime path: \`${runtimePaths.toWorkspaceRelative(sessionPath)}\``,
        contextError ? `- Observação: \`${contextError}\`` : null,
      ]
        .filter(Boolean)
        .join('\n');

  const parts = [
    intro,
    context ? buildContextSection(context, settings) : null,
    '## Starter Commands\n\n' + formatCommandList(DEFAULT_COMMANDS, settings.activation?.quick_commands_limit || 6),
  ];

  return `${parts.filter(Boolean).join('\n\n')}\n`;
}

function main() {
  process.stdout.write(generateGreeting());
}

if (require.main === module) {
  main();
}

module.exports = {
  generateGreeting,
};

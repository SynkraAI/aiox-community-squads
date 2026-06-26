#!/usr/bin/env node

/**
 * validate-setup.js
 * Runtime-aware validation of Claude Code setup in a project.
 *
 * Usage:
 *   node squads/claude-code-mastery/scripts/validate-setup.js [project-path]
 *   node squads/claude-code-mastery/scripts/validate-setup.js [project-path] --json
 */

const fs = require('fs');
const os = require('os');
const path = require('path');

const args = process.argv.slice(2);
const jsonOutput = args.includes('--json');
const projectPath = path.resolve(
  args.find((arg) => !arg.startsWith('--')) || process.cwd()
);

const SUPPORTED_PERMISSION_MODES = new Set([
  'default',
  'acceptEdits',
  'dontAsk',
  'bypassPermissions',
  'plan',
  'auto',
]);
const LEGACY_PERMISSION_MODES = new Set(['askAlways', 'autoApprove']);
const KEYBINDING_CONTEXTS = new Set([
  'Global',
  'Chat',
  'Autocomplete',
  'Confirmation',
  'Help',
]);
const MEMORY_ENTRYPOINT_MAX_LINES = 200;
const MEMORY_ENTRYPOINT_MAX_BYTES = 25_000;
const PASS_THRESHOLD = 70;

function getManagedSettingsPath() {
  switch (process.platform) {
    case 'darwin':
      return '/Library/Application Support/ClaudeCode/managed-settings.json';
    case 'win32':
      return 'C:\\Program Files\\ClaudeCode\\managed-settings.json';
    default:
      return '/etc/claude-code/managed-settings.json';
  }
}

function getManagedMcpPath() {
  return path.join(path.dirname(getManagedSettingsPath()), 'managed-mcp.json');
}

function readJsonFile(filePath) {
  if (!fs.existsSync(filePath)) {
    return { path: filePath, exists: false, data: null, error: null };
  }

  try {
    return {
      path: filePath,
      exists: true,
      data: JSON.parse(fs.readFileSync(filePath, 'utf8')),
      error: null,
    };
  } catch (error) {
    return {
      path: filePath,
      exists: true,
      data: null,
      error: error instanceof Error ? error.message : String(error),
    };
  }
}

function countLines(content) {
  return content.split('\n').length;
}

function extractRulePattern(rule) {
  if (typeof rule === 'string') return rule;
  if (rule && typeof rule === 'object' && typeof rule.pattern === 'string') {
    return rule.pattern;
  }
  return null;
}

function flattenPermissionRules(surfaces, field) {
  return surfaces.flatMap((surface) => {
    const rules = surface.data?.permissions?.[field];
    if (!Array.isArray(rules)) return [];
    return rules
      .map((rule) => ({
        surface: surface.name,
        pattern: extractRulePattern(rule),
      }))
      .filter((entry) => typeof entry.pattern === 'string');
  });
}

function hasMatchingRule(rules, matcher) {
  return rules.some(({ pattern }) => matcher(pattern));
}

function findFirstExistingPath(candidates) {
  return candidates.find((candidate) => fs.existsSync(candidate)) || null;
}

function summarizeFile(filePath) {
  if (!filePath) return null;
  const content = fs.readFileSync(filePath, 'utf8');
  return {
    path: filePath,
    lines: countLines(content),
    bytes: Buffer.byteLength(content, 'utf8'),
  };
}

function validateKeybindings(filePath) {
  if (!fs.existsSync(filePath)) {
    return {
      passed: true,
      details: 'Nenhum keybindings.json configurado',
      findings: [],
    };
  }

  let parsed;
  try {
    parsed = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (error) {
    return {
      passed: false,
      details: `Falha ao parsear keybindings.json: ${error.message}`,
      findings: [
        {
          severity: 'high',
          message: 'keybindings.json existe, mas não é um JSON válido',
          recommendation: 'Corrija o JSON ou remova o arquivo até definir um formato válido',
        },
      ],
    };
  }

  if (!parsed || typeof parsed !== 'object' || !('bindings' in parsed)) {
    return {
      passed: false,
      details: 'Formato inválido: esperado objeto com chave "bindings"',
      findings: [
        {
          severity: 'high',
          message: 'keybindings.json não segue o formato carregado pelo runtime',
          recommendation:
            'Use o formato { "bindings": [ { "context": "...", "bindings": { ... } } ] }',
        },
      ],
    };
  }

  if (!Array.isArray(parsed.bindings)) {
    return {
      passed: false,
      details: '"bindings" existe, mas não é um array',
      findings: [
        {
          severity: 'high',
          message: 'keybindings.json precisa ter "bindings" como array',
          recommendation: 'Converta "bindings" para array de blocos válidos',
        },
      ],
    };
  }

  const invalidContexts = [];
  const invalidBlocks = [];
  for (const block of parsed.bindings) {
    if (!block || typeof block !== 'object') {
      invalidBlocks.push('Bloco não é objeto');
      continue;
    }
    if (typeof block.context !== 'string') {
      invalidBlocks.push('Bloco sem context string');
      continue;
    }
    if (!KEYBINDING_CONTEXTS.has(block.context)) {
      invalidContexts.push(block.context);
    }
    if (!block.bindings || typeof block.bindings !== 'object') {
      invalidBlocks.push(`Bloco ${block.context} sem objeto bindings`);
    }
  }

  if (invalidBlocks.length > 0 || invalidContexts.length > 0) {
    return {
      passed: false,
      details:
        invalidContexts.length > 0
          ? `Contextos inválidos: ${invalidContexts.join(', ')}`
          : invalidBlocks.join('; '),
      findings: [
        {
          severity: 'medium',
          message: 'keybindings.json contém blocos ou contextos inválidos',
          recommendation:
            'Use apenas contextos Global, Chat, Autocomplete, Confirmation e Help, e garanta que cada bloco tenha um objeto bindings',
        },
      ],
    };
  }

  return {
    passed: true,
    details: `keybindings.json válido com ${parsed.bindings.length} bloco(s)`,
    findings: [],
  };
}

function countMcpServers(configData) {
  if (!configData || typeof configData !== 'object') return 0;
  if (configData.mcpServers && typeof configData.mcpServers === 'object') {
    return Object.keys(configData.mcpServers).length;
  }
  return 0;
}

const claudeDirPath = path.join(projectPath, '.claude');
const claudeMdPath = findFirstExistingPath([
  path.join(projectPath, '.claude', 'CLAUDE.md'),
  path.join(projectPath, 'CLAUDE.md'),
]);
const memoryMdPath = findFirstExistingPath([
  path.join(projectPath, '.claude', 'MEMORY.md'),
  path.join(projectPath, 'MEMORY.md'),
]);
const rulesDirPath = path.join(projectPath, '.claude', 'rules');
const projectMcpPath = path.join(projectPath, '.mcp.json');
const keybindingsPath = path.join(os.homedir(), '.claude', 'keybindings.json');

const settingSurfaces = [
  {
    name: 'managed',
    ...readJsonFile(getManagedSettingsPath()),
  },
  {
    name: 'local',
    ...readJsonFile(path.join(projectPath, '.claude', 'settings.local.json')),
  },
  {
    name: 'shared',
    ...readJsonFile(path.join(projectPath, '.claude', 'settings.json')),
  },
  {
    name: 'user',
    ...readJsonFile(path.join(os.homedir(), '.claude', 'settings.json')),
  },
];

const parsedSettingSurfaces = settingSurfaces.filter(
  (surface) => surface.exists && surface.data
);
const settingParseErrors = settingSurfaces.filter(
  (surface) => surface.exists && surface.error
);

const effectiveDefaultMode = (() => {
  for (const surface of settingSurfaces) {
    const mode = surface.data?.permissions?.defaultMode;
    if (typeof mode === 'string') {
      return { mode, surface: surface.name, implicit: false };
    }
  }
  return { mode: 'default', surface: 'implicit runtime default', implicit: true };
})();

const legacyModeHits = settingSurfaces.flatMap((surface) => {
  const mode = surface.data?.permissions?.defaultMode;
  if (typeof mode === 'string' && LEGACY_PERMISSION_MODES.has(mode)) {
    return [{ surface: surface.name, mode }];
  }
  return [];
});

const mergedDenyRules = flattenPermissionRules(parsedSettingSurfaces, 'deny');
const hooksCount = parsedSettingSurfaces.reduce((total, surface) => {
  const hooks = surface.data?.hooks;
  return hooks && typeof hooks === 'object'
    ? total + Object.keys(hooks).length
    : total;
}, 0);

const projectMcp = readJsonFile(projectMcpPath);
const managedMcp = readJsonFile(getManagedMcpPath());
const totalMcpServers =
  parsedSettingSurfaces.reduce(
    (total, surface) => total + countMcpServers(surface.data),
    0
  ) +
  countMcpServers(projectMcp.data) +
  countMcpServers(managedMcp.data);

const rulesFileCount = fs.existsSync(rulesDirPath)
  ? fs.readdirSync(rulesDirPath).filter((file) => file.endsWith('.md')).length
  : 0;

const claudeMdSummary = summarizeFile(claudeMdPath);
const memoryMdSummary = summarizeFile(memoryMdPath);
const keybindingsValidation = validateKeybindings(keybindingsPath);

const checks = [
  {
    name: '.claude/ directory exists',
    weight: 8,
    severity: 'critical',
    evaluate: () => ({
      passed: fs.existsSync(claudeDirPath),
      details: fs.existsSync(claudeDirPath)
        ? `.claude encontrado em ${claudeDirPath}`
        : 'Diretório .claude ausente',
      recommendation: 'Crie a superfície .claude/ para settings, rules e artefatos de setup',
    }),
  },
  {
    name: 'Primary instruction file exists',
    weight: 10,
    severity: 'critical',
    evaluate: () => ({
      passed: Boolean(claudeMdPath),
      details: claudeMdPath
        ? `Arquivo principal detectado em ${claudeMdPath}`
        : 'Nenhum CLAUDE.md encontrado no projeto',
      recommendation: 'Crie CLAUDE.md ou .claude/CLAUDE.md como instrução primária do projeto',
    }),
  },
  {
    name: 'Settings surfaces parse successfully',
    weight: 15,
    severity: 'critical',
    evaluate: () => ({
      passed: settingParseErrors.length === 0 && parsedSettingSurfaces.length > 0,
      details:
        settingParseErrors.length > 0
          ? settingParseErrors
              .map((surface) => `${surface.name}: ${surface.error}`)
              .join(' | ')
          : `Superfícies válidas: ${parsedSettingSurfaces.map((surface) => surface.name).join(', ') || 'nenhuma'}`,
      recommendation:
        'Garanta ao menos uma settings surface válida e corrija qualquer JSON inválido antes de prosseguir',
    }),
  },
  {
    name: 'Permission mode uses current runtime names',
    weight: 15,
    severity: 'critical',
    evaluate: () => {
      if (legacyModeHits.length > 0) {
        return {
          passed: false,
          details: legacyModeHits
            .map((hit) => `${hit.surface}: ${hit.mode}`)
            .join(', '),
          recommendation:
            'Substitua askAlways por default. Não migre autoApprove automaticamente: escolha dontAsk (fail-closed) ou bypassPermissions (gated)',
        };
      }

      return {
        passed: SUPPORTED_PERMISSION_MODES.has(effectiveDefaultMode.mode),
        details: effectiveDefaultMode.implicit
          ? 'Nenhum defaultMode explícito; runtime cai para default'
          : `Modo efetivo: ${effectiveDefaultMode.mode} (${effectiveDefaultMode.surface})`,
        recommendation:
          'Use apenas default, acceptEdits, dontAsk, bypassPermissions, plan e auto (quando feature-gated)',
      };
    },
  },
  {
    name: 'settings.json has deny rules',
    weight: 10,
    severity: 'high',
    evaluate: () => ({
      passed: mergedDenyRules.length > 0,
      details: `deny rules detectadas: ${mergedDenyRules.length}`,
      recommendation: 'Adote estratégia deny-first com proteção explícita para superfícies sensíveis',
    }),
  },
  {
    name: '.env is covered by deny rules',
    weight: 10,
    severity: 'high',
    evaluate: () => ({
      passed: hasMatchingRule(
        mergedDenyRules,
        (pattern) => pattern.includes('.env')
      ),
      details: hasMatchingRule(
        mergedDenyRules,
        (pattern) => pattern.includes('.env')
      )
        ? 'Cobertura de .env encontrada'
        : 'Nenhuma regra deny cobre .env/.env.*',
      recommendation:
        'Inclua deny para .env, .env.* e demais superfícies com segredos antes de ampliar permissões',
    }),
  },
  {
    name: '.claude/rules/ has at least one rule file',
    weight: 8,
    severity: 'medium',
    evaluate: () => ({
      passed: rulesFileCount > 0,
      details: `Arquivos .md em .claude/rules/: ${rulesFileCount}`,
      recommendation:
        'Crie ao menos um rule file quando o projeto tiver convenções específicas ou contexto extenso',
    }),
  },
  {
    name: 'CLAUDE.md stays within guidance budget',
    weight: 8,
    severity: 'medium',
    evaluate: () => ({
      passed: !claudeMdSummary || claudeMdSummary.lines <= 200,
      details: claudeMdSummary
        ? `${claudeMdSummary.lines} linha(s) em ${claudeMdSummary.path}`
        : 'Sem CLAUDE.md para medir',
      recommendation:
        'Mantenha CLAUDE.md enxuto e mova contexto grande para rules/ e imports',
    }),
  },
  {
    name: 'MEMORY.md respects runtime caps if present',
    weight: 6,
    severity: 'medium',
    evaluate: () => ({
      passed:
        !memoryMdSummary ||
        (memoryMdSummary.lines <= MEMORY_ENTRYPOINT_MAX_LINES &&
          memoryMdSummary.bytes <= MEMORY_ENTRYPOINT_MAX_BYTES),
      details: memoryMdSummary
        ? `${memoryMdSummary.lines} linha(s), ${memoryMdSummary.bytes} byte(s) em ${memoryMdSummary.path}`
        : 'Nenhum MEMORY.md no projeto',
      recommendation:
        'Se usar MEMORY.md no projeto, mantenha-o abaixo de 200 linhas e 25 KB',
    }),
  },
  {
    name: 'Keybindings config is valid if present',
    weight: 4,
    severity: 'medium',
    evaluate: () => ({
      passed: keybindingsValidation.passed,
      details: keybindingsValidation.details,
      recommendation:
        'Se houver keybindings.json, use o formato { "bindings": [ ... ] } com contextos válidos do runtime',
    }),
  },
  {
    name: 'MCP configuration surfaces parse if present',
    weight: 4,
    severity: 'medium',
    evaluate: () => ({
      passed:
        !(projectMcp.exists && projectMcp.error) &&
        !(managedMcp.exists && managedMcp.error),
      details:
        projectMcp.error || managedMcp.error
          ? [projectMcp.error && `.mcp.json: ${projectMcp.error}`, managedMcp.error && `managed-mcp.json: ${managedMcp.error}`]
              .filter(Boolean)
              .join(' | ')
          : `MCP server(s) detectados: ${totalMcpServers}`,
      recommendation:
        'Valide .mcp.json e managed-mcp.json como JSON válido e trate enterprise MCP como superfície exclusiva quando presente',
    }),
  },
  {
    name: 'Hook surface is known',
    weight: 2,
    severity: 'low',
    evaluate: () => ({
      passed: true,
      details:
        hooksCount > 0
          ? `Hooks configurados: ${hooksCount}`
          : 'Nenhum hook configurado (aceitável, mas sem automação de enforcement)',
      recommendation:
        'Adicione hooks quando precisar de guard rails automáticos, auto-lint ou observabilidade',
    }),
  },
];

const results = checks.map((check) => {
  const evaluation = check.evaluate();
  return {
    ...check,
    ...evaluation,
    score: evaluation.passed ? check.weight : 0,
  };
});

const findings = results
  .filter((result) => !result.passed)
  .map((result) => ({
    severity: result.severity,
    message: result.name,
    details: result.details,
    recommendation: result.recommendation,
  }))
  .concat(
    keybindingsValidation.findings,
    effectiveDefaultMode.mode === 'bypassPermissions'
      ? [
          {
            severity: 'medium',
            message: 'defaultMode usa bypassPermissions',
            details:
              'bypassPermissions continua sujeito a safety checks e depende de launch-time gate',
            recommendation:
              'Prefira default ou acceptEdits como baseline; use bypassPermissions apenas em sandbox isolado e conscientemente',
          },
        ]
      : []
  );

const totalScore = results.reduce((total, result) => total + result.score, 0);
const maxScore = results.reduce((total, result) => total + result.weight, 0);
const percentage = Math.round((totalScore / maxScore) * 100);
const grade =
  percentage >= 90
    ? 'A'
    : percentage >= 80
      ? 'B'
      : percentage >= 70
        ? 'C'
        : percentage >= 60
          ? 'D'
          : 'F';

const criticalFindings = findings.filter(
  (finding) => finding.severity === 'critical'
);
const pass = percentage >= PASS_THRESHOLD && criticalFindings.length === 0;

const report = {
  project: projectPath,
  score: {
    total: totalScore,
    max: maxScore,
    percentage,
    grade,
    pass,
  },
  effectiveDefaultMode,
  checks: results.map((result) => ({
    name: result.name,
    passed: result.passed,
    weight: result.weight,
    score: result.score,
    details: result.details,
  })),
  findings,
};

if (jsonOutput) {
  console.log(JSON.stringify(report, null, 2));
  process.exit(pass ? 0 : 1);
}

console.log('\nClaude Code Setup Validation');
console.log(`Project: ${projectPath}`);
console.log(`${'='.repeat(60)}\n`);

for (const result of results) {
  const icon = result.passed ? 'PASS' : 'FAIL';
  console.log(`  [${icon}] ${result.name} (${result.score}/${result.weight})`);
  console.log(`        ${result.details}`);
}

if (findings.length > 0) {
  console.log(`\nFindings (${findings.length})`);
  console.log('-'.repeat(60));
  for (const finding of findings) {
    console.log(
      `  [${finding.severity.toUpperCase()}] ${finding.message}: ${finding.details}`
    );
    console.log(`        Recommendation: ${finding.recommendation}`);
  }
}

console.log(`\n${'='.repeat(60)}`);
console.log(`  Score: ${totalScore}/${maxScore} (${percentage}%)`);
console.log(`  Grade: ${grade}`);
console.log(`  Verdict: ${pass ? 'PASS' : 'FAIL'}`);
console.log(`${'='.repeat(60)}\n`);

process.exit(pass ? 0 : 1);

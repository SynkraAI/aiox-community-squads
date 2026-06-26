#!/usr/bin/env node
/**
 * CCM Output Schema Injector
 * Story: STORY-CCM-INT.1 T2
 *
 * Adds `output_schema: <schema-ref>` to the Contrato SINKRA block
 * in all 31 task .md files in squads/claude-code-mastery/tasks/.
 *
 * Usage:
 *   node inject-output-schemas.js            # apply changes
 *   node inject-output-schemas.js --dry-run   # preview only
 */

const fs = require('fs');
const path = require('path');

const TASKS_DIR = path.resolve(__dirname, '../tasks');
const DRY_RUN = process.argv.includes('--dry-run');

// Task → output_schema mapping from STORY-CCM-INT.1 T2
const OUTPUT_SCHEMA_MAP = {
  'audit-setup': 'audit-report-yaml',
  'audit-settings': 'config-score-yaml',
  'audit-integration': 'integration-report-yaml',
  'hook-designer': 'hook-implementation',
  'mcp-workflow': 'mcp-config',
  'mcp-integration-plan': 'mcp-integration-report-yaml',
  'configure-claude-code': 'claude-settings-plan-json',
  'create-rules': 'rules-directory',
  'create-agent-definition': 'agent-definition-md',
  'create-team-topology': 'team-topology-yaml',
  'claude-md-engineer': 'claude-md-file',
  'integrate-project': 'integration-plan-yaml',
  'setup-repository': 'setup-report-yaml',
  'setup-wizard': 'setup-report-yaml',
  'brownfield-setup': 'brownfield-report-yaml',
  'multi-project-setup': 'multi-project-plan-yaml',
  'sandbox-setup': 'sandbox-config-yaml',
  'ci-cd-setup': 'ci-pipeline-yaml',
  'diagnose': 'diagnosis-report-yaml',
  'optimize-context': 'context-optimization-yaml',
  'optimize-workflow': 'workflow-optimization-yaml',
  'parallel-decomposition': 'decomposition-plan-yaml',
  'worktree-strategy': 'worktree-plan-yaml',
  'permission-strategy': 'permission-matrix-yaml',
  'context-rot-audit': 'rot-report-yaml',
  'enterprise-config': 'enterprise-config-yaml',
  'delete-claude-code-mastery': 'deletion-confirmation',
  'update-claude-code-mastery': 'update-report-yaml',
  'align-memory-context': 'memory-alignment-yaml',
  'rebuild-runtime-validator': 'validator-script',
  'refresh-runtime-contract': 'contract-update-yaml',
};

function processFile(filepath) {
  const content = fs.readFileSync(filepath, 'utf8');
  const basename = path.basename(filepath);
  const taskSlug = path.basename(filepath, '.md');

  // Skip if already has output_schema
  if (content.includes('output_schema:')) {
    return { file: basename, status: 'skipped', reason: 'already exists' };
  }

  // Check for Contrato SINKRA section
  if (!content.includes('## Contrato SINKRA')) {
    return { file: basename, status: 'skipped', reason: 'no Contrato SINKRA section' };
  }

  const schema = OUTPUT_SCHEMA_MAP[taskSlug];
  if (!schema) {
    return { file: basename, status: 'error', reason: `no schema mapping for ${taskSlug}` };
  }

  // Insert output_schema after the Output: block
  // The Output: field is followed by lines starting with - (list items)
  // We need to insert after the last list item under Output:
  const outputPattern = /^(Output:\n(?:- .+\n)+)/m;
  const match = content.match(outputPattern);

  if (!match) {
    return { file: basename, status: 'error', reason: 'no Output: block found' };
  }

  const newContent = content.replace(
    outputPattern,
    `$1output_schema: ${schema}\n`
  );

  if (newContent === content) {
    return { file: basename, status: 'no-change' };
  }

  if (!DRY_RUN) {
    fs.writeFileSync(filepath, newContent, 'utf8');
  }

  return { file: basename, status: DRY_RUN ? 'would-update' : 'updated', schema };
}

// Main
const taskFiles = fs.readdirSync(TASKS_DIR)
  .filter(f => f.endsWith('.md'))
  .map(f => path.join(TASKS_DIR, f))
  .sort();

console.log(`Found ${taskFiles.length} task .md files`);
if (DRY_RUN) console.log('DRY RUN MODE — no files will be modified\n');

let updated = 0;
let skipped = 0;
let errors = 0;

for (const file of taskFiles) {
  const result = processFile(file);
  if (result.status === 'updated' || result.status === 'would-update') {
    updated++;
    console.log(`  ✅ ${result.file} → ${result.schema}`);
  } else if (result.status === 'skipped') {
    skipped++;
    console.log(`  ⏭️  ${result.file} (${result.reason})`);
  } else if (result.status === 'error') {
    errors++;
    console.log(`  ❌ ${result.file} (${result.reason})`);
  }
}

console.log(`\nSummary: ${updated} ${DRY_RUN ? 'would-update' : 'updated'}, ${skipped} skipped, ${errors} errors`);
console.log(`Total: ${taskFiles.length} files`);

if (errors > 0) process.exit(1);

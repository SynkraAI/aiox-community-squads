#!/usr/bin/env node
/**
 * CCM Accountability Token Injector
 * Story: STORY-CCM-INT.1 T1
 *
 * Adds `accountability_token: TK-CCM-ACC-001` to the Contrato SINKRA block
 * in all 31 task .md files in squads/claude-code-mastery/tasks/.
 *
 * All CCM tasks map to the single accountability token TK-CCM-ACC-001.
 *
 * Usage:
 *   node inject-accountability-tokens.js            # apply changes
 *   node inject-accountability-tokens.js --dry-run   # preview only
 */

const fs = require('fs');
const path = require('path');

const TASKS_DIR = path.resolve(__dirname, '../tasks');
const DRY_RUN = process.argv.includes('--dry-run');
const TOKEN = 'TK-CCM-ACC-001';

function processFile(filepath) {
  const content = fs.readFileSync(filepath, 'utf8');
  const basename = path.basename(filepath);

  // Skip if already has accountability_token
  if (content.includes('accountability_token:')) {
    return { file: basename, status: 'skipped', reason: 'already exists' };
  }

  // Check for Contrato SINKRA section
  if (!content.includes('## Contrato SINKRA')) {
    return { file: basename, status: 'skipped', reason: 'no Contrato SINKRA section' };
  }

  // Insert accountability_token after the Domain: line
  const domainPattern = /^(Domain: .+)$/m;
  const match = content.match(domainPattern);

  if (!match) {
    return { file: basename, status: 'error', reason: 'no Domain: line found' };
  }

  const newContent = content.replace(
    domainPattern,
    `$1\naccountability_token: ${TOKEN}`
  );

  if (newContent === content) {
    return { file: basename, status: 'no-change' };
  }

  if (!DRY_RUN) {
    fs.writeFileSync(filepath, newContent, 'utf8');
  }

  return { file: basename, status: DRY_RUN ? 'would-update' : 'updated', token: TOKEN };
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
    console.log(`  ✅ ${result.file} → ${result.token}`);
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

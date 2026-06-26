#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const { buildWorkspaceContext } = require('./load-workspace-context.cjs');

const ROOT = path.resolve(__dirname, '..', '..', '..');

function assert(condition, message, details = {}) {
  if (!condition) {
    const error = new Error(message);
    error.details = details;
    throw error;
  }
}

function listDirectories(directoryPath) {
  if (!fs.existsSync(directoryPath)) {
    return [];
  }

  return fs.readdirSync(directoryPath, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && !entry.name.startsWith('.'))
    .map((entry) => entry.name)
    .sort((left, right) => left.localeCompare(right));
}

async function findReadyBusinessFixture() {
  const businessesRoot = path.join(ROOT, 'workspace', 'businesses');

  for (const business of listDirectories(businessesRoot)) {
    const payload = await buildWorkspaceContext({
      business,
      includeRaw: false,
    });

    if (
      payload.workspace_context.coo_readiness_status === 'ready' &&
      payload.workspace_context.runtime_mode === 'full_workspace_mode' &&
      payload.workspace_context.source_of_truth === 'workspace_canonical' &&
      payload.workspace_context.blockers.length === 0 &&
      Boolean(payload.workspace_context.business_summary.company_name) &&
      payload.workspace_context.loaded_sources.operations.some(
        (item) => item.id === 'operations_team_structure' && item.exists
      )
    ) {
      return {
        business,
        payload,
      };
    }
  }

  throw new Error('No ready business fixture found for aiox-sop workspace context tests.');
}

async function main() {
  const { business, payload: ready } = await findReadyBusinessFixture();

  assert(ready.workspace_context.coo_readiness_status === 'ready', 'AIOX business should be ready for operations context', ready);
  assert(ready.workspace_context.runtime_mode === 'full_workspace_mode', 'Explicit business should switch aiox-sop to full_workspace_mode', ready);
  assert(ready.workspace_context.source_of_truth === 'workspace_canonical', 'Business-aware context should use workspace_canonical source of truth', ready);
  assert(ready.workspace_context.business_slug === business, 'Resolved business slug should match the chosen fixture', ready);
  assert(Boolean(ready.workspace_context.business_summary.company_name), 'Company summary should expose a company name', ready);
  assert(
    ready.workspace_context.loaded_sources.company.some((item) => item.id === 'company_profile' && item.exists),
    'Company profile must be loaded as a canonical source',
    ready
  );
  assert(
    ready.workspace_context.loaded_sources.operations.some((item) => item.id === 'operations_team_structure' && item.exists),
    'Operations team structure must be loaded as a canonical source',
    ready
  );
  assert(
    ready.workspace_context.loaded_sources.templates.length > 0,
    'Operations template inventory must be exposed',
    ready
  );

  const blocked = await buildWorkspaceContext({
    business: 'business-that-does-not-exist',
    includeRaw: false,
  });

  assert(blocked.workspace_context.blockers.length > 0, 'Missing business should produce blockers', blocked);
  assert(blocked.workspace_context.coo_readiness_status === 'blocked', 'Missing business should be blocked by COO readiness', blocked);

  console.log('PASS: aiox-sop workspace context loader tests passed');
}

main().catch((error) => {
  console.error('ERROR: aiox-sop workspace context loader tests failed');
  console.error(error.message);
  if (error.details) {
    console.error(JSON.stringify(error.details, null, 2));
  }
  process.exit(1);
});

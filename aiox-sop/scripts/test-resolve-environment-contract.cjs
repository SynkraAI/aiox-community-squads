#!/usr/bin/env node

const fs = require('fs');
const os = require('os');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..', '..');
const {
  DEFAULT_PROJECTION_PATH,
  resolveEnvironmentContract,
} = require('./resolve-environment-contract.cjs');

function assert(condition, message, details = {}) {
  if (!condition) {
    const error = new Error(message);
    error.details = details;
    throw error;
  }
}

function writeFile(root, relativePath, content) {
  const absolutePath = path.join(root, relativePath);
  fs.mkdirSync(path.dirname(absolutePath), { recursive: true });
  fs.writeFileSync(absolutePath, content, 'utf8');
}

function createFixtureRoot() {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'aiox-sop-env-'));
  writeFile(
    fixtureRoot,
    'squads/squad-creator-pro/config.yaml',
    'version: 9.9.9\nmetadata:\n  version: 9.9.9\n'
  );
  fs.mkdirSync(path.join(fixtureRoot, 'squads', 'squad-creator-pro', 'agents'), { recursive: true });
  fs.mkdirSync(path.join(fixtureRoot, 'squads', 'squad-creator-pro', 'tasks'), { recursive: true });
  fs.mkdirSync(path.join(fixtureRoot, 'squads', 'squad-creator-pro', 'workflows'), { recursive: true });
  writeFile(
    fixtureRoot,
    DEFAULT_PROJECTION_PATH,
    [
      'projection_freshness:',
      '  status: current',
      '  updated_at: "2026-03-10"',
      '',
    ].join('\n')
  );
  return fixtureRoot;
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

async function findReadyBusinessContract() {
  const businessesRoot = path.join(ROOT, 'workspace', 'businesses');

  for (const business of listDirectories(businessesRoot)) {
    const contract = await resolveEnvironmentContract({
      business,
      projectionPath: DEFAULT_PROJECTION_PATH,
    });

    if (
      contract.runtime_mode === 'full_workspace_mode' &&
      contract.source_of_truth === 'workspace_canonical'
    ) {
      return {
        business,
        contract,
      };
    }
  }

  throw new Error('No ready business fixture found for aiox-sop environment contract tests.');
}

async function main() {
  const fallback = await resolveEnvironmentContract({
    projectionPath: DEFAULT_PROJECTION_PATH,
  });
  assert(fallback.access_tier === 'pro', 'Fallback tier should resolve to pro in this repo', fallback);
  assert(
    fallback.runtime_mode === 'portable_docs_mode',
    'aiox-sop should stay in portable docs mode without explicit business context',
    fallback
  );
  assert(fallback.source_of_truth === 'docs_projection', 'Fallback source of truth should be docs projection', fallback);
  assert(fallback.projection_freshness === 'current', 'Projection freshness should be surfaced from the operational projection', fallback);

  const { contract: workspaceReady } = await findReadyBusinessContract();
  assert(workspaceReady.access_tier === 'pro', 'Explicit business context should keep pro tier in this repo', workspaceReady);
  assert(
    workspaceReady.runtime_mode === 'full_workspace_mode',
    'aiox-sop should enter full workspace mode when COO operations readiness is ready',
    workspaceReady
  );
  assert(
    workspaceReady.source_of_truth === 'workspace_canonical',
    'full workspace mode should switch source of truth to workspace_canonical',
    workspaceReady
  );

  const fixtureRoot = createFixtureRoot();
  writeFile(
    fixtureRoot,
    'workspace/license/enterprise-runtime.capability.yaml',
    [
      'enterprise_runtime_capability:',
      '  enabled: true',
      '  issued_by: "aiox"',
      '  scope: "private_runtime"',
      '  access_tier: "enterprise"',
      '  allow_full_workspace_mode: true',
      '  allowed_surfaces:',
      '    - workspace_canonical',
      '    - private_projection_generation',
      '  issued_at: "2026-03-10"',
      '',
    ].join('\n')
  );

  try {
    const enterpriseContract = await resolveEnvironmentContract({
      root: fixtureRoot,
      projectionPath: DEFAULT_PROJECTION_PATH,
    });
    assert(enterpriseContract.access_tier === 'enterprise', 'Canonical enterprise marker should resolve to enterprise', enterpriseContract);
    assert(
      enterpriseContract.runtime_mode === 'portable_docs_mode',
      'Enterprise marker must not bypass missing readiness support for aiox-sop',
      enterpriseContract
    );
    assert(
      enterpriseContract.projection_freshness === 'current',
      'Projection freshness should still be reported in portable mode',
      enterpriseContract
    );
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }

  console.log('PASS: aiox-sop environment contract tests passed');
}

main().catch((error) => {
  console.error('ERROR: aiox-sop environment contract tests failed');
  console.error(error.message);
  if (error.details) {
    console.error(JSON.stringify(error.details, null, 2));
  }
  process.exit(1);
});

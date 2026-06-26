#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const CANDIDATE_PATHS = [
  '../../workspace/scripts/resolve-squad-workspace-readiness.cjs',
  '../../c-level/scripts/resolve-squad-workspace-readiness.cjs',
];

function loadResolver() {
  for (const candidate of CANDIDATE_PATHS) {
    const absolutePath = path.resolve(__dirname, candidate);
    if (!fs.existsSync(absolutePath)) {
      continue;
    }

    const mod = require(absolutePath);
    if (typeof mod.resolveSquadWorkspaceReadiness === 'function') {
      return {
        resolveSquadWorkspaceReadiness: mod.resolveSquadWorkspaceReadiness,
        sourcePath: absolutePath,
      };
    }
  }

  const inspected = CANDIDATE_PATHS.map((candidate) => path.resolve(__dirname, candidate));
  const error = new Error(
    `Workspace readiness resolver not found. Checked: ${inspected.join(', ')}`
  );
  error.code = 'READINESS_RESOLVER_NOT_FOUND';
  error.checkedPaths = inspected;
  throw error;
}

function resolveSquadWorkspaceReadiness(input) {
  const { resolveSquadWorkspaceReadiness: resolver } = loadResolver();
  return resolver(input);
}

module.exports = {
  CANDIDATE_PATHS,
  loadResolver,
  resolveSquadWorkspaceReadiness,
};

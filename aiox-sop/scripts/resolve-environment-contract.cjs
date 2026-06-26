#!/usr/bin/env node

const path = require('path');
const yaml = require('js-yaml');

const ROOT = path.resolve(__dirname, '..', '..', '..');
const DEFAULT_SQUAD = 'aiox-sop';
const DEFAULT_PROJECTION_PATH = 'docs/squad/aiox-sop/operational-projection.yaml';

const {
  detectEnvironmentContract,
} = require(path.join(ROOT, 'squads', 'squad-creator', 'scripts', 'detect-environment-contract.cjs'));

function parseArgs(argv) {
  const args = {
    root: ROOT,
    squad: DEFAULT_SQUAD,
    business: null,
    product: null,
    app: null,
    contextType: null,
    format: 'json',
    projectionPath: DEFAULT_PROJECTION_PATH,
  };

  for (const raw of argv) {
    if (raw.startsWith('--squad=')) {
      args.squad = raw.slice('--squad='.length).trim() || DEFAULT_SQUAD;
      continue;
    }
    if (raw.startsWith('--business=')) {
      args.business = raw.slice('--business='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--product=')) {
      args.product = raw.slice('--product='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--app=')) {
      args.app = raw.slice('--app='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--context-type=')) {
      args.contextType = raw.slice('--context-type='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--format=')) {
      args.format = raw.slice('--format='.length).trim() || 'json';
      continue;
    }
    if (raw.startsWith('--projection-path=')) {
      args.projectionPath = raw.slice('--projection-path='.length).trim() || DEFAULT_PROJECTION_PATH;
    }
  }

  return args;
}

async function resolveEnvironmentContract(inputArgs = {}) {
  const args = {
    ...parseArgs([]),
    ...inputArgs,
  };

  const contract = await detectEnvironmentContract({
    root: args.root,
    squad: args.squad,
    business: args.business,
    product: args.product,
    app: args.app,
    contextType: args.contextType,
    projectionPath: args.projectionPath,
  });

  return {
    squad: args.squad,
    ...contract,
  };
}

function printOutput(output, format) {
  if (format === 'yaml') {
    process.stdout.write(yaml.dump(output, { lineWidth: 120, noRefs: true, sortKeys: false }));
    return;
  }

  process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const output = await resolveEnvironmentContract(args);
  printOutput(output, args.format);
}

if (require.main === module) {
  main().catch((error) => {
    console.error(`ERROR: ${error.message}`);
    process.exit(1);
  });
}

module.exports = {
  DEFAULT_PROJECTION_PATH,
  parseArgs,
  resolveEnvironmentContract,
};

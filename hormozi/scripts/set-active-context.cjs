#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const runtimePaths = require('./runtime-paths.cjs');
const { resolveSquadWorkspaceReadiness } = require('./resolve-readiness.cjs');

function fail(message) {
  console.error(`ERROR: ${message}`);
  process.exit(1);
}

function parseArgs(argv) {
  const args = {
    business: 'aiox',
    product: null,
    workstream: null,
    reason: 'manual',
    format: 'json',
  };

  for (const raw of argv) {
    if (raw.startsWith('--business=')) {
      args.business = raw.slice('--business='.length).trim() || 'aiox';
      continue;
    }
    if (raw.startsWith('--product=')) {
      args.product = raw.slice('--product='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--workstream=')) {
      args.workstream = raw.slice('--workstream='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--reason=')) {
      args.reason = raw.slice('--reason='.length).trim() || 'manual';
      continue;
    }
    if (raw.startsWith('--format=')) {
      args.format = raw.slice('--format='.length).trim() || 'json';
    }
  }

  return args;
}

function writeYaml(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, yaml.dump(data, { lineWidth: 120, noRefs: true, sortKeys: false }), 'utf8');
}

function printOutput(output, format) {
  if (format === 'yaml') {
    process.stdout.write(yaml.dump(output, { lineWidth: 120, noRefs: true, sortKeys: false }));
    return;
  }
  process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.product) {
    fail('Provide --product=<slug>');
  }

  let readiness;
  try {
    readiness = resolveSquadWorkspaceReadiness({
      squad: 'hormozi',
      business: args.business,
      product: args.product,
      contextType: 'product',
    });
  } catch (error) {
    fail(error.message);
  }

  const sessionPath = runtimePaths.getHormoziSessionContextPath();
  const payload = {
    active_context: {
      business_slug: args.business,
      product_slug: args.product,
      workstream: args.workstream,
      readiness_status: readiness.status,
      updated_at: new Date().toISOString(),
      reason: args.reason,
    },
  };

  writeYaml(sessionPath, payload);
  printOutput(
    {
      session_context_path: runtimePaths.toWorkspaceRelative(sessionPath),
      ...payload,
    },
    args.format
  );
}

if (require.main === module) {
  main();
}

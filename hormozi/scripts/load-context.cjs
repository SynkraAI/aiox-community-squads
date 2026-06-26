#!/usr/bin/env node

const fs = require('fs');
const yaml = require('js-yaml');

const runtimePaths = require('./runtime-paths.cjs');
const { resolveSquadWorkspaceReadiness } = require('./resolve-readiness.cjs');

function fail(message) {
  console.error(`ERROR: ${message}`);
  process.exit(1);
}

function parseArgs(argv) {
  const args = {
    business: null,
    product: null,
    task: null,
    format: 'json',
  };

  for (const raw of argv) {
    if (raw.startsWith('--business=')) {
      args.business = raw.slice('--business='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--product=')) {
      args.product = raw.slice('--product='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--task=')) {
      args.task = raw.slice('--task='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--format=')) {
      args.format = raw.slice('--format='.length).trim() || 'json';
    }
  }

  return args;
}

function readSessionContext() {
  const sessionPath = runtimePaths.getHormoziSessionContextPath();
  if (!fs.existsSync(sessionPath)) {
    fail(`Hormozi session context not found: ${runtimePaths.toWorkspaceRelative(sessionPath)}. Run node squads/hormozi/scripts/set-active-context.cjs --product=<slug>.`);
  }

  const payload = yaml.load(fs.readFileSync(sessionPath, 'utf8')) || {};
  const active = payload.active_context || {};
  if (!active.business_slug || !active.product_slug) {
    fail(`Invalid hormozi session context: missing active_context.business_slug or active_context.product_slug in ${runtimePaths.toWorkspaceRelative(sessionPath)}`);
  }

  return {
    sessionPath,
    businessSlug: String(active.business_slug).trim(),
    productSlug: String(active.product_slug).trim(),
    workstream: typeof active.workstream === 'string' && active.workstream.trim() !== '' ? active.workstream.trim() : null,
  };
}

function buildOutput(args) {
  const session = readSessionContext();
  const business = args.business || session.businessSlug;
  const product = args.product || session.productSlug;
  const cooReadiness = resolveSquadWorkspaceReadiness({
    squad: 'hormozi',
    business,
    product,
    contextType: 'product',
  });
  const readiness = cooReadiness.readiness_payload;

  const sharedFiles = readiness.requirements.filter((item) =>
    ['brand', 'positioning'].includes(item.id) && item.exists
  );
  const productFiles = readiness.requirements.filter((item) =>
    !['brand', 'positioning', 'pricing', 'product_structure'].includes(item.id) && item.exists
  );

  return {
    task: args.task || null,
    consumer: 'hormozi',
    business_slug: business,
    product_slug: product,
    workstream: session.workstream,
    coo_readiness: {
      owner: cooReadiness.owner,
      status: cooReadiness.status,
      reason: cooReadiness.reason,
      canonical_config_paths: cooReadiness.canonical_config_paths,
    },
    readiness: {
      status: readiness.status,
      reasons: readiness.reasons,
      missing_required: readiness.missing_required.map((item) => ({
        id: item.id,
        path: item.path,
      })),
      compliance_audit: readiness.compliance_audit,
    },
    session_context_path: runtimePaths.toWorkspaceRelative(session.sessionPath),
    company_offerbook_index: readiness.company_offerbook_index,
    resolved_paths: {
      shared_files: sharedFiles.map((item) => item.path),
      product_files: productFiles.map((item) => item.path),
      structure_source: readiness.requirements.find((item) => item.id === 'product_structure' && item.exists)?.path || null,
      pricing_source: readiness.requirements.find((item) => item.id === 'pricing' && item.exists)?.path || null,
    },
  };
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
  let output;
  try {
    output = buildOutput(args);
  } catch (error) {
    fail(error.message);
  }
  printOutput(output, args.format);
}

if (require.main === module) {
  main();
}

module.exports = {
  buildOutput,
};

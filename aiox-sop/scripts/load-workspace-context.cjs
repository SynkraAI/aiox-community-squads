#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const ROOT = path.resolve(__dirname, '..', '..', '..');

const {
  resolveSquadWorkspaceReadiness,
} = require(path.join(ROOT, 'workspace', 'scripts', 'resolve-squad-workspace-readiness.cjs'));

const {
  resolveEnvironmentContract,
} = require(path.join(ROOT, 'squads', 'aiox-sop', 'scripts', 'resolve-environment-contract.cjs'));

function parseArgs(argv) {
  const args = {
    business: null,
    format: 'json',
    includeRaw: false,
  };

  for (const raw of argv) {
    if (raw.startsWith('--business=')) {
      args.business = raw.slice('--business='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--bu=')) {
      args.business = raw.slice('--bu='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--format=')) {
      args.format = raw.slice('--format='.length).trim() || 'json';
      continue;
    }
    if (raw === '--include-raw') {
      args.includeRaw = true;
    }
  }

  return args;
}

function relativePath(targetPath) {
  return path.relative(ROOT, targetPath).split(path.sep).join('/');
}

function exists(relative) {
  return fs.existsSync(path.join(ROOT, relative));
}

function readYaml(relative) {
  return yaml.load(fs.readFileSync(path.join(ROOT, relative), 'utf8')) || {};
}

function describeSource(id, relative, required, includeRaw) {
  const available = exists(relative);
  return {
    id,
    path: relative,
    required,
    exists: available,
    data: available && includeRaw ? readYaml(relative) : undefined,
  };
}

function buildBusinessSummary(companyProfile, teamStructure) {
  return {
    company_name:
      companyProfile?.metadata?.company_name ||
      companyProfile?.company_essence?.trade_name ||
      companyProfile?.company_essence?.legal_name ||
      null,
    one_liner: companyProfile?.company_essence?.one_liner || null,
    mission: companyProfile?.mission?.statement || null,
    operations_framework:
      teamStructure?.metadata?.framework ||
      teamStructure?.current_team?.philosophy ||
      null,
    current_headcount: teamStructure?.current_team?.total_headcount || null,
  };
}

function listOperationTemplates() {
  const templateRoot = path.join(ROOT, 'workspace', '_templates', 'business-template', 'L1-strategy');
  if (!fs.existsSync(templateRoot)) {
    return [];
  }

  return fs.readdirSync(templateRoot)
    .sort()
    .map((name) => relativePath(path.join(templateRoot, name)));
}

async function buildWorkspaceContext(inputArgs) {
  const args = {
    format: 'json',
    includeRaw: false,
    ...inputArgs,
  };

  if (!args.business) {
    throw new Error('load-workspace-context requires --business=<slug>');
  }

  const readiness = resolveSquadWorkspaceReadiness({
    squad: 'aiox-sop',
    business: args.business,
    contextType: 'operations',
    format: 'json',
  });

  const environment = await resolveEnvironmentContract({
    business: args.business,
  });

  const companySources = {
    company_profile: describeSource(
      'company_profile',
      `workspace/businesses/${args.business}/L0-identity/company-dna.yaml`,
      true,
      args.includeRaw
    ),
    icp: describeSource(
      'company_icp',
      `workspace/businesses/${args.business}/L1-strategy/icp.yaml`,
      true,
      args.includeRaw
    ),
    brand: describeSource(
      'company_brand',
      `workspace/businesses/${args.business}/L2-tactical/brand/brandbook.yaml`,
      true,
      args.includeRaw
    ),
    offerbook: describeSource(
      'company_offerbook',
      `workspace/businesses/${args.business}/L1-strategy/offerbook.yaml`,
      false,
      args.includeRaw
    ),
  };

  const operationsSources = {
    team_structure: describeSource(
      'operations_team_structure',
      `workspace/businesses/${args.business}/L1-strategy/team-structure.yaml`,
      true,
      args.includeRaw
    ),
    pricing_strategy: describeSource(
      'operations_pricing_strategy',
      `workspace/businesses/${args.business}/L1-strategy/pricing-strategy.yaml`,
      true,
      args.includeRaw
    ),
    kpi_scorecards: describeSource(
      'operations_kpi_scorecards',
      `workspace/businesses/${args.business}/L1-strategy/kpi-scorecards.yaml`,
      true,
      args.includeRaw
    ),
    funnel_vsl_reference: describeSource(
      'operations_funnel_vsl_reference',
      `workspace/businesses/${args.business}/L1-strategy/funnel-vsl-reference.yaml`,
      false,
      args.includeRaw
    ),
    commission_design: describeSource(
      'operations_commission_design',
      `workspace/businesses/${args.business}/L1-strategy/commission-design.yaml`,
      false,
      args.includeRaw
    ),
  };

  const missingRequired = [
    ...Object.values(companySources),
    ...Object.values(operationsSources),
  ]
    .filter((item) => item.required && !item.exists)
    .map((item) => ({
      id: item.id,
      path: item.path,
      required: true,
    }));

  const blockers = [];
  if (readiness.status !== 'ready') {
    blockers.push(`COO readiness blocked: ${readiness.reason}`);
  }
  if (environment.runtime_mode !== 'full_workspace_mode') {
    blockers.push(`Environment runtime_mode is ${environment.runtime_mode}, expected full_workspace_mode`);
  }
  if (environment.source_of_truth !== 'workspace_canonical') {
    blockers.push(`Environment source_of_truth is ${environment.source_of_truth}, expected workspace_canonical`);
  }
  if (missingRequired.length > 0) {
    blockers.push('Required canonical business sources are missing.');
  }

  const companyProfile = companySources.company_profile.exists ? readYaml(companySources.company_profile.path) : null;
  const teamStructure = operationsSources.team_structure.exists ? readYaml(operationsSources.team_structure.path) : null;

  return {
    workspace_context: {
      generated_at: new Date().toISOString(),
      business_slug: args.business,
      coo_readiness_status: readiness.status,
      runtime_mode: environment.runtime_mode,
      source_of_truth: environment.source_of_truth,
      access_tier: environment.access_tier,
      blockers,
      readiness_reason: readiness.reason,
      business_summary: buildBusinessSummary(companyProfile, teamStructure),
      loaded_sources: {
        workspace: readiness.required_sources_loaded,
        company: Object.values(companySources).map(({ id, path: filePath, required, exists: sourceExists }) => ({
          id,
          path: filePath,
          required,
          exists: sourceExists,
        })),
        operations: Object.values(operationsSources).map(({ id, path: filePath, required, exists: sourceExists }) => ({
          id,
          path: filePath,
          required,
          exists: sourceExists,
        })),
        templates: listOperationTemplates(),
      },
      missing_required_sources: missingRequired,
      environment_contract: {
        access_tier: environment.access_tier,
        runtime_mode: environment.runtime_mode,
        source_of_truth: environment.source_of_truth,
        reason: environment.reason,
        evidence_paths: environment.evidence_paths,
      },
      company: args.includeRaw ? Object.fromEntries(
        Object.entries(companySources).map(([key, value]) => [key, value.data || null])
      ) : undefined,
      operations: args.includeRaw ? Object.fromEntries(
        Object.entries(operationsSources).map(([key, value]) => [key, value.data || null])
      ) : undefined,
    },
  };
}

async function loadWorkspaceContext(inputArgs) {
  const context = await buildWorkspaceContext(inputArgs);
  if (context.workspace_context.blockers.length > 0) {
    const error = new Error('Workspace context is not available for aiox-sop.');
    error.details = context;
    throw error;
  }
  return context;
}

function printOutput(payload, format) {
  if (format === 'yaml') {
    process.stdout.write(yaml.dump(payload, { lineWidth: 120, noRefs: true, sortKeys: false }));
    return;
  }

  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  try {
    const payload = await loadWorkspaceContext(args);
    printOutput(payload, args.format);
  } catch (error) {
    if (error.details) {
      printOutput(error.details, args.format);
    } else {
      console.error(`ERROR: ${error.message}`);
    }
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch((error) => {
    console.error(`ERROR: ${error.message}`);
    process.exit(1);
  });
}

module.exports = {
  buildWorkspaceContext,
  loadWorkspaceContext,
  parseArgs,
};

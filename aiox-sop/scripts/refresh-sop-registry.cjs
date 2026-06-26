#!/usr/bin/env node
/**
 * refresh-sop-registry.cjs
 *
 * Scans workspace/businesses/{name}/sops/{file}.yaml and docs/sops/{file}.md
 * to populate squads/aiox-sop/data/sop-registry.yaml deterministically.
 *
 * Usage:
 *   node squads/aiox-sop/scripts/refresh-sop-registry.cjs           # dry-run (stdout)
 *   node squads/aiox-sop/scripts/refresh-sop-registry.cjs --write   # write to disk
 *
 * Zero LLM involvement. Pure filesystem scan.
 */

'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..', '..');
const REGISTRY_PATH = path.join(ROOT, 'squads', 'aiox-sop', 'data', 'sop-registry.yaml');
const BUSINESSES_DIR = path.join(ROOT, 'workspace', 'businesses');
const SHARED_SOPS_DIR = path.join(ROOT, 'docs', 'sops');

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function listDirs(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);
}

function listFiles(dir, ext) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true })
    .filter(f => f.isFile() && f.name.endsWith(ext))
    .map(f => f.name);
}

/** Minimal YAML front-matter parser: extracts key: value from sop.metadata */
function extractSopMetadata(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const meta = {};

  // Extract sop_id
  const idMatch = content.match(/sop_id:\s*["']?([^"'\n]+)["']?/);
  if (idMatch) meta.sop_id = idMatch[1].trim();

  // Extract status
  const statusMatch = content.match(/status:\s*["']?(\w+)["']?/);
  if (statusMatch) meta.status = statusMatch[1].trim();

  // Extract process
  const processMatch = content.match(/process:\s*["']?([^"'\n]+)["']?/);
  if (processMatch) meta.process = processMatch[1].trim();

  // Extract business
  const bizMatch = content.match(/business:\s*["']?([^"'\n]+)["']?/);
  if (bizMatch) meta.business = bizMatch[1].trim();

  // Extract owner
  const ownerMatch = content.match(/owner:\s*["']?([^"'\n]+)["']?/);
  if (ownerMatch) meta.owner = ownerMatch[1].trim();

  // Extract objective (for tags heuristic)
  const objMatch = content.match(/objective:\s*["']?([^"'\n]+)["']?/);
  if (objMatch) meta.objective = objMatch[1].trim();

  return meta;
}

/** Derive process name from filename: atendimento-cliente.yaml -> atendimento-cliente */
function processFromFilename(filename) {
  return filename.replace(/\.yaml$/, '').replace(/\.yml$/, '').replace(/\.md$/, '');
}

/** Simple tag inference from process name */
function inferTags(processName) {
  const tags = [];
  const lower = processName.toLowerCase();
  if (lower.includes('atendimento') || lower.includes('customer') || lower.includes('onboarding')) tags.push('customer-success');
  if (lower.includes('venda') || lower.includes('sales') || lower.includes('prospecting')) tags.push('sales');
  if (lower.includes('trafego') || lower.includes('traffic') || lower.includes('ads')) tags.push('traffic');
  if (lower.includes('contratacao') || lower.includes('hiring') || lower.includes('ramp')) tags.push('hiring');
  if (lower.includes('financeiro') || lower.includes('finance') || lower.includes('commission')) tags.push('finance');
  if (lower.includes('conteudo') || lower.includes('content') || lower.includes('editorial')) tags.push('content');
  if (tags.length === 0) tags.push('operations');
  return tags;
}

// ---------------------------------------------------------------------------
// Scan
// ---------------------------------------------------------------------------

function scanBusinessSops() {
  const businesses = {};
  const businessDirs = listDirs(BUSINESSES_DIR);

  for (const biz of businessDirs) {
    const sopsDir = path.join(BUSINESSES_DIR, biz, 'sops');
    const yamlFiles = listFiles(sopsDir, '.yaml').concat(listFiles(sopsDir, '.yml'));

    if (yamlFiles.length === 0) continue;

    const sops = [];
    for (const file of yamlFiles) {
      if (file === 'README.md') continue;
      const filePath = path.join(sopsDir, file);
      const meta = extractSopMetadata(filePath);
      const processName = meta.process || processFromFilename(file);
      const sopId = meta.sop_id || `${biz}-${processName}-sop`;

      sops.push({
        sop_id: sopId,
        process: processName,
        file: `workspace/businesses/${biz}/sops/${file}`,
        status: meta.status || 'draft',
        squad_consumer: null,
        automatable: false,
        tags: inferTags(processName),
        human_doc: null,
      });
    }

    if (sops.length > 0) {
      businesses[biz] = { sops };
    }
  }

  return businesses;
}

function scanSharedSops() {
  const mdFiles = listFiles(SHARED_SOPS_DIR, '.md').filter(f => f !== 'README.md');
  return mdFiles.map(file => {
    const processName = processFromFilename(file).replace(/-sop-v[\d.]+$/, '').replace(/-sop$/, '');
    return {
      sop_id: `shared-${processName}-sop`,
      process: processName,
      file: `docs/sops/${file}`,
      status: 'active',
      tags: inferTags(processName),
    };
  });
}

/** Try to match shared markdown SOPs to business SOPs by process name */
function linkHumanDocs(businesses, sharedSops) {
  const sharedByProcess = {};
  for (const s of sharedSops) {
    sharedByProcess[s.process] = s.file;
  }

  for (const biz of Object.values(businesses)) {
    for (const sop of biz.sops) {
      if (sharedByProcess[sop.process]) {
        sop.human_doc = sharedByProcess[sop.process];
      }
    }
  }
}

function computeStats(businesses, sharedSops) {
  const stats = {
    by_status: { draft: 0, active: 0, deprecated: 0 },
    by_automatable: { true: 0, false: 0 },
    unmapped_sops: 0,
    mapped_sops: 0,
  };

  const allSops = Object.values(businesses).flatMap(b => b.sops);
  for (const sop of allSops) {
    const status = sop.status || 'draft';
    if (stats.by_status[status] !== undefined) stats.by_status[status]++;
    if (sop.automatable) stats.by_automatable.true++;
    else stats.by_automatable.false++;
    if (sop.squad_consumer) stats.mapped_sops++;
    else stats.unmapped_sops++;
  }

  return stats;
}

// ---------------------------------------------------------------------------
// YAML serializer (minimal, no dependency)
// ---------------------------------------------------------------------------

function toYamlValue(val) {
  if (val === null || val === undefined) return 'null';
  if (typeof val === 'boolean') return val ? 'true' : 'false';
  if (typeof val === 'number') return String(val);
  if (Array.isArray(val) && val.length === 0) return '[]';
  if (typeof val === 'string') {
    if (val.includes(':') || val.includes('#') || val.includes('"') || val.includes("'")) {
      return `"${val.replace(/"/g, '\\"')}"`;
    }
    return val;
  }
  return String(val);
}

function serializeSopEntry(sop, indent) {
  const pad = ' '.repeat(indent);
  const lines = [];
  lines.push(`${pad}- sop_id: ${toYamlValue(sop.sop_id)}`);
  lines.push(`${pad}  process: ${toYamlValue(sop.process)}`);
  lines.push(`${pad}  file: ${toYamlValue(sop.file)}`);
  lines.push(`${pad}  status: ${toYamlValue(sop.status)}`);
  lines.push(`${pad}  squad_consumer: ${toYamlValue(sop.squad_consumer)}`);
  lines.push(`${pad}  automatable: ${toYamlValue(sop.automatable)}`);
  lines.push(`${pad}  tags: [${sop.tags.join(', ')}]`);
  if (sop.human_doc) {
    lines.push(`${pad}  human_doc: ${toYamlValue(sop.human_doc)}`);
  }
  return lines.join('\n');
}

function generateRegistryYaml(businesses, sharedSops, stats, totalSops) {
  const now = new Date().toISOString().split('T')[0];
  const lines = [];

  lines.push('# ============================================================================');
  lines.push('# SOP-REGISTRY.YAML — Registro central de SOPs por business');
  lines.push('# ============================================================================');
  lines.push('# Generated by: node squads/aiox-sop/scripts/refresh-sop-registry.cjs --write');
  lines.push(`# Last refresh: ${now}`);
  lines.push('# Maintainer: aiox-sop');
  lines.push('#');
  lines.push('# PRINCIPIO TASK-FIRST:');
  lines.push('#   SOPs definem O QUE o negocio precisa executar.');
  lines.push('#   Tasks definem COMO um squad resolve o SOP.');
  lines.push('#   Agents sao os EXECUTORES das tasks.');
  lines.push('#   Fluxo: SOPs (business) -> Tasks (squad) -> Agents (executores)');
  lines.push('#');
  lines.push('# PATHS CANONICOS:');
  lines.push('#   SOPs machine-readable: workspace/businesses/{business}/sops/');
  lines.push('#   SOPs humanos (markdown): docs/sops/');
  lines.push('#   Template: workspace/_templates/sops/sop.yaml');
  lines.push('# ============================================================================');
  lines.push('');
  lines.push('schema_version: "1.0.0"');
  lines.push(`last_updated: "${now}"`);
  lines.push(`total_sops: ${totalSops}`);
  lines.push('maintainer: aiox-sop');
  lines.push('');

  // Businesses
  lines.push('businesses:');
  const bizNames = Object.keys(businesses).sort();
  if (bizNames.length === 0) {
    lines.push('  {}');
  } else {
    for (const biz of bizNames) {
      lines.push(`  ${biz}:`);
      lines.push('    sops:');
      for (const sop of businesses[biz].sops) {
        lines.push(serializeSopEntry(sop, 6));
      }
    }
  }
  lines.push('');

  // process_to_squad_map (preserved as empty -- populated manually or by squad-creator)
  lines.push('process_to_squad_map: {}');
  lines.push('');

  // Shared SOPs
  lines.push('shared_sops:');
  if (sharedSops.length === 0) {
    lines.push('  []');
  } else {
    for (const sop of sharedSops) {
      lines.push(`  - sop_id: ${toYamlValue(sop.sop_id)}`);
      lines.push(`    process: ${toYamlValue(sop.process)}`);
      lines.push(`    file: ${toYamlValue(sop.file)}`);
      lines.push(`    status: ${toYamlValue(sop.status)}`);
      lines.push(`    tags: [${sop.tags.join(', ')}]`);
    }
  }
  lines.push('');

  // Stats
  lines.push('stats:');
  lines.push('  by_status:');
  lines.push(`    draft: ${stats.by_status.draft}`);
  lines.push(`    active: ${stats.by_status.active}`);
  lines.push(`    deprecated: ${stats.by_status.deprecated}`);
  lines.push('  by_automatable:');
  lines.push(`    "true": ${stats.by_automatable.true}`);
  lines.push(`    "false": ${stats.by_automatable.false}`);
  lines.push(`  unmapped_sops: ${stats.unmapped_sops}`);
  lines.push(`  mapped_sops: ${stats.mapped_sops}`);
  lines.push('');

  return lines.join('\n');
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
  const writeMode = process.argv.includes('--write');

  const businesses = scanBusinessSops();
  const sharedSops = scanSharedSops();
  linkHumanDocs(businesses, sharedSops);

  const totalBizSops = Object.values(businesses).reduce((sum, b) => sum + b.sops.length, 0);
  const totalSops = totalBizSops + sharedSops.length;
  const stats = computeStats(businesses, sharedSops);

  const yaml = generateRegistryYaml(businesses, sharedSops, stats, totalSops);

  if (writeMode) {
    fs.writeFileSync(REGISTRY_PATH, yaml, 'utf8');
    console.log(`[refresh-sop-registry] Written ${REGISTRY_PATH}`);
    console.log(`  Businesses: ${Object.keys(businesses).length}`);
    console.log(`  Business SOPs: ${totalBizSops}`);
    console.log(`  Shared SOPs: ${sharedSops.length}`);
    console.log(`  Total: ${totalSops}`);
  } else {
    console.log(yaml);
    console.log(`# --- DRY RUN --- pass --write to save to ${REGISTRY_PATH}`);
  }
}

main();

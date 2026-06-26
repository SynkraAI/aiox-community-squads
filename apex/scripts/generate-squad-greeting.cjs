#!/usr/bin/env node

/**
 * generate-squad-greeting.js
 *
 * Generates a formatted greeting for Squad Apex agents.
 * Used during agent activation to display consistent, context-aware greetings.
 *
 * Usage:
 *   node scripts/generate-squad-greeting.js [agent-id]
 *   node scripts/generate-squad-greeting.js apex-lead
 *   node scripts/generate-squad-greeting.js --all
 *
 * Output: Formatted greeting string to stdout
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SQUAD_ROOT = path.resolve(__dirname, '..');
const AGENTS_DIR = path.join(SQUAD_ROOT, 'agents');
const REGISTRY_PATH = path.join(SQUAD_ROOT, 'data', 'agent-registry.yaml');

// Agent metadata (fallback if registry unavailable)
const AGENT_META = {
  'apex-lead':      { icon: '⚡', name: 'Emil',     role: 'Design Engineering Lead', tier: 'Orchestrator' },
  'frontend-arch':  { icon: '🏗️', name: 'Arch',     role: 'Frontend Architect',       tier: 'T1' },
  'interaction-dsgn':{ icon: '🎯', name: 'Ahmad',   role: 'Interaction Designer',     tier: 'T2' },
  'design-sys-eng': { icon: '💎', name: 'Diana',    role: 'Design System Engineer',   tier: 'T2' },
  'css-eng':        { icon: '🎭', name: 'Josh',     role: 'CSS Specialist',           tier: 'T3' },
  'react-eng':      { icon: '⚛️', name: 'Kent',     role: 'React Specialist',         tier: 'T3' },
  'mobile-eng':     { icon: '📱', name: 'Krzysztof', role: 'Mobile Engineer',          tier: 'T3' },
  'cross-plat-eng': { icon: '🔄', name: 'Fernando', role: 'Cross-Platform Engineer',  tier: 'T3' },
  'spatial-eng':    { icon: '🌐', name: 'Paul',      role: 'Spatial Engineer',         tier: 'T3' },
  'motion-eng':     { icon: '✨', name: 'Matt',     role: 'Motion Specialist',        tier: 'T4' },
  'a11y-eng':       { icon: '♿', name: 'Sara',     role: 'Accessibility Specialist', tier: 'T4' },
  'perf-eng':       { icon: '🚀', name: 'Addy',     role: 'Performance Specialist',   tier: 'T4' },
  'qa-visual':      { icon: '👁️', name: 'Andy',     role: 'Visual QA',                tier: 'T5' },
  'qa-xplatform':   { icon: '🔍', name: 'Michal',   role: 'Cross-Platform QA',        tier: 'T5' },
  'web-intel':      { icon: '🕸️', name: 'Kilian',   role: 'Web Intelligence',         tier: 'T2' },
};

function getGitContext() {
  try {
    const branch = execSync('git branch --show-current', { encoding: 'utf8' }).trim();
    const lastCommit = execSync('git log --oneline -1', { encoding: 'utf8' }).trim();
    const status = execSync('git status --porcelain -u', { encoding: 'utf8' }).trim();
    const modifiedCount = status ? status.split('\n').length : 0;

    return { branch, lastCommit, modifiedCount };
  } catch {
    return { branch: 'unknown', lastCommit: 'no commits', modifiedCount: 0 };
  }
}

function detectProfile() {
  try {
    const pkgPath = path.resolve(SQUAD_ROOT, '../../package.json');
    if (!fs.existsSync(pkgPath)) return 'minimal';

    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
    const deps = { ...pkg.dependencies, ...pkg.devDependencies };

    if (deps['react-native'] || deps['expo']) return 'full';
    if (deps['next']) return 'web-next';
    if (deps['react'] && deps['vite']) return 'web-spa';
    return 'minimal';
  } catch {
    return 'minimal';
  }
}

function generateGreeting(agentId) {
  const meta = AGENT_META[agentId];
  if (!meta) {
    console.error(`Unknown agent: ${agentId}`);
    process.exit(1);
  }

  const git = getGitContext();
  const profile = detectProfile();
  const activeAgentCount = {
    full: 15, 'web-next': 11, 'web-spa': 9, minimal: 4
  }[profile] || 4;

  const lines = [];

  // Line 1: Icon + name + role
  lines.push(`${meta.icon} **${meta.name}** — ${meta.role}`);
  lines.push('');

  // Line 2: Context
  lines.push(`Branch: \`${git.branch}\` | ${git.modifiedCount} files modified`);

  // Line 3: Profile
  lines.push(`Profile: **${profile}** (${activeAgentCount} agents active)`);
  lines.push('');

  // Line 4: Last commit
  lines.push(`Last commit: ${git.lastCommit}`);
  lines.push('');

  // Line 5: Ready message
  if (agentId === 'apex-lead') {
    lines.push('Every pixel is a decision. What are we crafting today?');
  } else {
    lines.push(`${meta.name} ready. What do you need?`);
  }

  return lines.join('\n');
}

function generateAllGreetings() {
  const lines = ['# Squad Apex — Agent Greetings\n'];

  for (const [id, meta] of Object.entries(AGENT_META)) {
    lines.push(`## ${meta.icon} ${meta.name} (${id})`);
    lines.push('```');
    lines.push(generateGreeting(id));
    lines.push('```');
    lines.push('');
  }

  return lines.join('\n');
}

// CLI
const args = process.argv.slice(2);

if (args.length === 0 || args[0] === '--help') {
  console.log('Usage: node generate-squad-greeting.js [agent-id|--all]');
  console.log('');
  console.log('Available agents:');
  for (const [id, meta] of Object.entries(AGENT_META)) {
    console.log(`  ${meta.icon} ${id} — ${meta.name} (${meta.role})`);
  }
  process.exit(0);
}

if (args[0] === '--all') {
  console.log(generateAllGreetings());
} else {
  console.log(generateGreeting(args[0]));
}

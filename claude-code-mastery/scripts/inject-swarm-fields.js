const fs = require('fs');
const path = require('path');

const squadsToProcess = [
  'sinkra-squad', 'claude-code-mastery', 'copy', 'infra-ops',
  'domain-decoder', 'hormozi', 'data', 'kaizen', 'backlog-ops',
  'etl-ops', 'aiox-sop', 'slides-creator', 'aiox-copy', 'aiox-design',
  'aiox-ads', 'books', 'brand', 'c-level',
  'clickup-ops-squad', 'deep-research', 'design-system', 'edital',
  'google-workspace-squad', 'innerlens', 'ip-shield-squad',
  'mega-brain', 'mmos', 'movement', 'process-excellence-squad',
  'project-ops', 'skill-creator-ops', 'spy', 'squad-creator',
  'squad-creator-pro', 'storytelling', 'team-ops-squad',
  'tools-squad', 'visual-knowledge-squad', 'agent-autonomy',
];

let updatedCount = 0;
let skippedCount = 0;

for (const squad of squadsToProcess) {
  const agentsDir = path.join(process.cwd(), 'squads', squad, 'agents');
  
  if (!fs.existsSync(agentsDir)) {
    console.log(`Squad directory not found: ${agentsDir}`);
    continue;
  }
  
  const files = fs.readdirSync(agentsDir).filter(f => f.endsWith('.md'));

  for (const file of files) {
    const filePath = path.join(agentsDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Safety check - skip if swarm already injected
    if (content.includes('\nswarm:\n')) {
      console.log(`[SKIPPED] ${squad}/${file} - Already has swarm block.`);
      skippedCount++;
      continue;
    }
    
    // Identify if the agent is a Chief based on naming
    const isChief = file.includes('chief') || file.includes('orchestrator');
    
    // CC hybrid coordinator: orchestrates + reads for synthesis (BR-COORD-004 + BR-COORD-009)
    const chiefYaml = `
swarm:
  role: leader
  allowed_tools:
    - Agent
    - TaskStop
    - SendMessage
    - SyntheticOutput
    - Read
    - Grep
    - Glob
  max_turns: 200
  memory_scope: shared
`;
    // CC async agent allowlist (BR-AGENT-007) + extras for AIOX workers
    const workerYaml = `
swarm:
  role: worker
  allowed_tools:
    - Read
    - Edit
    - Write
    - Grep
    - Glob
    - Bash
    - WebSearch
    - WebFetch
    - Skill
    - NotebookEdit
  max_turns: 50
  memory_scope: project
`;

    const swarmyaml = isChief ? chiefYaml : workerYaml;

    // Inject just before 'persona:' boundary
    if (content.includes('\npersona:\n')) {
        content = content.replace(/\npersona:\n/, swarmyaml + '\npersona:\n');
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`[INJECTED] ${squad}/${file} -> role: ${isChief ? 'leader' : 'worker'}`);
        updatedCount++;
    } else {
        console.warn(`[WARNING] Could not find 'persona:' boundary in ${squad}/${file}`);
    }
  }
}

console.log(`\nSwarm injection complete: ${updatedCount} agents updated, ${skippedCount} skipped.`);

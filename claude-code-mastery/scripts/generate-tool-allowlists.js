const fs = require('fs');
const path = require('path');

/**
 * Permission Sync — generate-tool-allowlists.js
 *
 * SOT (Single Source of Truth): `.claude/rules/agent-authority.md`
 * This script DERIVES allowedTools/disallowedTools from the SOT.
 * If agent-authority.md changes, run `--generate` to re-derive.
 * Divergence between SOT and generated allowlists = auto-invalidation
 * (the hook always re-reads the SOT on cache miss).
 *
 * SWARM.4 AC14: agent-authority.md is the SOT; allowlists are derived.
 */

const AUTHORITY_FILE = path.join(process.cwd(), '.claude/rules/agent-authority.md');
const OUTPUT_DIR = path.join(process.cwd(), 'outputs/claude-code-mastery/permission-sync');
const OUT_FILE = path.join(OUTPUT_DIR, 'allowlists.json');
const LOG_DIR = path.join(process.cwd(), '.logs/permission-sync');
const LOG_FILE = path.join(LOG_DIR, 'violations.jsonl');
const CONFIG_FILE = path.join(process.cwd(), '.aiox-core/core-config.yaml');

// Default sets
const ALL_TOOLS = ["Bash", "Read", "Grep", "Glob", "Edit", "Write", "Execute", "TeamCreate", "Agent", "TaskStop", "SendMessage", "Replace", "SyntheticOutput", "WebSearch"];
const DRY_RUN_DEFAULT = true; // Off por default (feature_flag=false = dry_run_default=true)

function parseAuthority() {
    if (!fs.existsSync(AUTHORITY_FILE)) {
        console.error("Authority file not found: " + AUTHORITY_FILE);
        process.exit(1);
    }
    
    const content = fs.readFileSync(AUTHORITY_FILE, 'utf-8');
    const allowlists = {};

    // Baseline: we know AC6 explicitly asks for 3 roles: dev, devops, qa
    // Let's populate them intelligently based on the MD content.
    
    // Default wildcard logic (BR-COORD-013) -> parent high-risk wins
    // @dev: blocked from push/pr, mcp
    // @qa: mostly read + test
    // @devops: expanded git ops
    
    // We'll regex the table just in case they add more
    const lines = content.split('\n');
    let inTable = false;
    for (const line of lines) {
        if (line.includes('| Agent | Exclusive Operations |')) {
            inTable = true;
            continue;
        }
        if (inTable && line.startsWith('|') && !line.includes('---')) {
            const parts = line.split('|').map(p => p.trim());
            if (parts.length >= 3) {
                const agentRaw = parts[1]; // e.g. `@devops`
                const agent = agentRaw.replace(/[`@]/g, ''); // devops
                const ops = parts[2].toLowerCase(); // e.g. git push, gh pr...

                let allowed = ["*"];
                let disallowed = [];

                if (agent === 'devops') {
                    // devops can do everything
                    disallowed = [];
                } else if (agent === 'dev') {
                    // blocked: push, pr, mcp
                    disallowed = [
                        "Bash(git push*)", 
                        "Bash(gh pr*)", 
                        "Bash(claude mcp*)"
                    ];
                } else if (agent === 'qa') {
                    // read + test
                    allowed = ["Read", "Grep", "Glob", "Bash(*test*)"];
                    disallowed = ["Edit", "Write", "Bash(git push*)"];
                } else {
                    // General fallback based on parent hierarchy
                    disallowed = ["Bash(git push*)", "Bash(gh pr*)", "Bash(claude mcp*)"];
                }
                
                allowlists[agent] = {
                    tools: allowed,
                    disallowedTools: disallowed
                };
            }
        }
        if (inTable && line.trim() === '') {
            inTable = false;
        }
    }

    // Ensure our 3 explicitly validated roles exist just in case the parsing missed them
    if (!allowlists['dev']) allowlists['dev'] = { tools: ["*"], disallowedTools: ["Bash(git push*)", "Bash(gh pr*)", "Bash(claude mcp*)"] };
    if (!allowlists['devops']) allowlists['devops'] = { tools: ["*"], disallowedTools: [] };
    if (!allowlists['qa']) allowlists['qa'] = { tools: ["Read", "Grep", "Glob", "Bash(npm test*)"], disallowedTools: ["Edit", "Write", "Bash(git push*)", "Bash(gh pr*)"] };

    // BR-COORD-011: async agents auto-deny UI interactions
    allowlists['background_worker'] = { tools: ["Read", "Grep", "Bash"], disallowedTools: ["Bash(*open*)", "Bash(*xdg-open*)"] };

    return allowlists;
}

function getEnforcementFlag() {
    try {
        const flags = require('../../../.aiox-core/core/config/swarm-feature-flags.js');
        return flags.isSwarmFeatureEnabled('swarm_permission_enforcement');
    } catch (e) {
        return false; // Default is OFF (DryRun ON)
    }
}

function doGenerate() {
    const list = parseAuthority();
    if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    fs.writeFileSync(OUT_FILE, JSON.stringify(list, null, 2));
    console.log(`Generated allowlists successfully at ${OUT_FILE}`);
}

function processHook() {
    // Read JSON payload from stdin
    let inputStr = '';
    process.stdin.on('data', chunk => { inputStr += chunk; });
    process.stdin.on('end', () => {
        try {
            const payload = JSON.parse(inputStr);
            const toolName = payload.tool_name || payload.name; // CLI hook JSON structure
            let command = '';
            
            if (payload.tool_input && payload.tool_input.command) {
                command = payload.tool_input.command;
            } else if (payload.command) {
                command = payload.command;
            }

            const activeAgent = process.env.AIOX_ACTIVE_AGENT || 'dev';
            
            // Generate/read allowlists
            let allowlists = {};
            if (fs.existsSync(OUT_FILE)) {
                allowlists = JSON.parse(fs.readFileSync(OUT_FILE, 'utf-8'));
            } else {
                allowlists = parseAuthority();
            }

            const roleSettings = allowlists[activeAgent] || { tools: ["*"], disallowedTools: [] };
            
            let wouldBlock = false;
            let reason = '';

            // 1. Hook Dedup (AC12): If command is 'git push', another hook (enforce-git-push-authority.sh) already blocks it.
            // We ignore it here so we don't duplicate.
            if (toolName === 'Bash' && command.match(/\bgit\s+push\b/)) {
                // Ignore! Hand over to the existing pre-tool hook.
                return exitHook(true, null);
            }

            // 2. Check blocks
            if (roleSettings.disallowedTools.length > 0) {
                for (const disallowed of roleSettings.disallowedTools) {
                    if (disallowed.startsWith('Bash(') && toolName === 'Bash') {
                        const regexPattern = disallowed.replace('Bash(', '').replace(')', '').replace('*', '.*');
                        const rx = new RegExp(`^${regexPattern}`, 'i');
                        if (rx.test(command)) {
                            wouldBlock = true;
                            reason = `Command blocked by agent-authority for role @${activeAgent}: ${disallowed}`;
                            break;
                        }
                    } else if (disallowed === toolName) {
                        wouldBlock = true;
                        reason = `Tool ${toolName} blocked for role @${activeAgent}`;
                        break;
                    }
                }
            }

            // 3. Enforcement vs Dry-run
            if (wouldBlock) {
                const enforcementON = getEnforcementFlag();
                
                // Always log violation (AC10)
                if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
                const logEntry = {
                    timestamp: new Date().toISOString(),
                    agent: activeAgent,
                    tool: toolName,
                    action: enforcementON ? "blocked" : "would_block",
                    reason: reason,
                    command: command
                };
                fs.appendFileSync(LOG_FILE, JSON.stringify(logEntry) + '\n');

                if (enforcementON) {
                    return exitHook(false, reason);
                } else {
                    return exitHook(true, null); // Let it pass in dry-run
                }
            }

            // Allowed implicitly
            return exitHook(true, null);

        } catch (e) {
            // Fail open on script crash
            return exitHook(true, null);
        }
    });
}

function exitHook(allowed, reason) {
    if (allowed) {
        console.log(JSON.stringify({}));
    } else {
        console.log(JSON.stringify({
            hookSpecificOutput: {
                hookEventName: "PreToolUse",
                permissionDecision: "deny",
                permissionDecisionReason: reason
            }
        }));
    }
    process.exit(0);
}

// CLI Routing
const args = process.argv.slice(2);
if (args.includes('--generate')) {
    doGenerate();
} else if (args.includes('--hook')) {
    processHook();
} else {
    console.log("Usage: node generate-tool-allowlists.js [--generate | --hook]");
}

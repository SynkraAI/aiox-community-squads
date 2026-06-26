#!/usr/bin/env node

const yaml = require('js-yaml');
const { buildOutput } = require('./load-context.cjs');

function main() {
  let output;
  try {
    output = buildOutput({
      task: 'hormozi-chief',
      format: 'json',
    });
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    process.exit(1);
  }
  process.stdout.write(yaml.dump(output, { lineWidth: 120, noRefs: true, sortKeys: false }));
}

if (require.main === module) {
  main();
}

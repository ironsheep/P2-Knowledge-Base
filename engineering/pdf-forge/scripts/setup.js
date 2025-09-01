#!/usr/bin/env node
/**
 * Doc Forge Setup Script
 * Initializes the PDF generation environment
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');

const DIRECTORIES = [
  'inbox/processed',
  'outbox/archive',
  'output',
  'logs',
  'config',
  'templates'
];

const CONFIG_FILES = {
  'config/pdf-settings.json': {
    format: 'A4',
    margin: {
      top: '1in',
      bottom: '1in',
      left: '1in',
      right: '1in'
    },
    quality: 'high',
    timeout: 30000,
    concurrent: 2
  },
  'config/templates.json': {
    default: 'admin-manual',
    templates: {
      'admin-manual': {
        file: 'admin-manual.latex',
        description: 'Professional administrator documentation'
      },
      'user-guide': {
        file: 'user-guide.latex', 
        description: 'End-user documentation and guides'
      }
    }
  }
};

async function setup() {
  console.log(chalk.blue('🔧 Setting up Doc Forge environment...'));
  console.log('');

  // Create directories
  for (const dir of DIRECTORIES) {
    await fs.ensureDir(dir);
    console.log(chalk.green('✓') + ` Created directory: ${dir}`);
  }

  // Create config files
  for (const [filePath, content] of Object.entries(CONFIG_FILES)) {
    await fs.outputJSON(filePath, content, { spaces: 2 });
    console.log(chalk.green('✓') + ` Created config: ${filePath}`);
  }

  // Create gitkeep files for empty directories
  const gitkeepDirs = ['inbox', 'outbox', 'output', 'logs'];
  for (const dir of gitkeepDirs) {
    const gitkeepPath = path.join(dir, '.gitkeep');
    if (!await fs.pathExists(gitkeepPath)) {
      await fs.writeFile(gitkeepPath, '');
      console.log(chalk.green('✓') + ` Created ${gitkeepPath}`);
    }
  }

  // Create sample request template
  const sampleRequest = {
    documents: [
      {
        input: 'sample-document.md',
        output: 'sample-document.pdf',
        template: 'admin-manual',
        variables: {
          version: '1.0.0',
          date: new Date().toLocaleDateString()
        }
      }
    ],
    options: {
      cleanup: true,
      archive: true
    }
  };

  await fs.outputJSON('inbox/sample-request.json', sampleRequest, { spaces: 2 });
  console.log(chalk.green('✓') + ' Created sample request template');

  console.log('');
  console.log(chalk.green('✅ Setup complete!'));
  console.log('');
  console.log('Next steps:');
  console.log('  1. Place markdown files in inbox/');
  console.log('  2. Create or modify inbox/request.json');
  console.log('  3. Run: make process');
}

setup().catch(error => {
  console.error(chalk.red('❌ Setup failed:'), error.message);
  process.exit(1);
});
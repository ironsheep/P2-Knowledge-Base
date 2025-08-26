#!/usr/bin/env node
/**
 * Doc Forge Default Request Creator
 * Creates a default request.json when none exists
 */

const fs = require('fs-extra');
const chalk = require('chalk');
const path = require('path');

async function createDefaultRequest() {
  console.log(chalk.blue('📝 Creating default request...'));
  
  try {
    const inboxDir = 'inbox';
    
    // Find any .md files in inbox
    const files = await fs.readdir(inboxDir);
    const markdownFiles = files.filter(file => 
      path.extname(file) === '.md' && file !== 'README.md'
    );
    
    if (markdownFiles.length === 0) {
      // Create a sample markdown file
      const sampleMd = `# Sample Document

This is a sample document for PDF generation.

## Features

- Professional PDF output
- LaTeX templates
- Automatic formatting

## Usage

1. Replace this content with your own
2. Update the request.json file
3. Run \`make process\`

Your PDF will be generated in the outbox/ directory.
`;
      
      await fs.writeFile(path.join(inboxDir, 'sample-document.md'), sampleMd);
      markdownFiles.push('sample-document.md');
      console.log(chalk.green('✓') + ' Created sample-document.md');
    }
    
    // Create default request for found files
    const documents = markdownFiles.map(file => ({
      input: file,
      output: file.replace('.md', '.pdf'),
      template: 'admin-manual',
      variables: {
        version: '1.0.0',
        date: new Date().toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long', 
          day: 'numeric'
        })
      }
    }));
    
    const defaultRequest = {
      documents: documents,
      options: {
        cleanup: true,
        archive: true,
        optimize: false
      }
    };
    
    const requestPath = path.join(inboxDir, 'request.json');
    await fs.outputJSON(requestPath, defaultRequest, { spaces: 2 });
    
    console.log(chalk.green('✓') + ' Created default request.json');
    console.log(`Found ${markdownFiles.length} markdown file(s):`);
    
    markdownFiles.forEach(file => {
      console.log(chalk.gray(`  - ${file} → ${file.replace('.md', '.pdf')}`));
    });
    
    console.log('');
    console.log(chalk.blue('ℹ Next steps:'));
    console.log('  1. Edit inbox/request.json if needed');
    console.log('  2. Run: make process');
    
    return true;
    
  } catch (error) {
    console.log('');
    console.log(chalk.red('❌ Failed to create default request:'));
    console.log(chalk.red(`   ${error.message}`));
    return false;
  }
}

// CLI usage
if (require.main === module) {
  createDefaultRequest()
    .then(success => process.exit(success ? 0 : 1))
    .catch(error => {
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    });
}

module.exports = { createDefaultRequest };
#!/usr/bin/env node
/**
 * Doc Forge Template Builder
 * Processes and validates LaTeX templates
 */

const fs = require('fs-extra');
const chalk = require('chalk');
const path = require('path');

async function buildTemplates() {
  console.log(chalk.blue('🔨 Building templates...'));
  
  try {
    const templatesDir = 'templates';
    
    // Ensure templates directory exists
    await fs.ensureDir(templatesDir);
    
    // Find all .latex files
    const files = await fs.readdir(templatesDir);
    const latexFiles = files.filter(file => path.extname(file) === '.latex');
    
    if (latexFiles.length === 0) {
      console.log(chalk.yellow('⚠ No .latex template files found'));
      return false;
    }
    
    console.log(`Found ${latexFiles.length} template(s)`);
    
    // Process each template
    const templates = {};
    for (const file of latexFiles) {
      const templateName = path.basename(file, '.latex');
      const templatePath = path.join(templatesDir, file);
      
      console.log(chalk.gray(`  Processing: ${file}`));
      
      // Read template content
      const content = await fs.readFile(templatePath, 'utf8');
      
      // Basic validation - check for required pandoc variables
      const requiredVars = ['$body$'];
      const optionalVars = ['$version$', '$date$', '$title$', '$author$'];
      
      for (const varName of requiredVars) {
        if (!content.includes(varName)) {
          throw new Error(`Template ${file}: Missing required variable ${varName}`);
        }
      }
      
      // Extract template metadata from comments
      const metadata = {
        name: templateName,
        file: file,
        description: extractDescription(content),
        variables: extractVariables(content),
        packages: extractPackages(content)
      };
      
      templates[templateName] = metadata;
      console.log(chalk.green('✓') + ` ${templateName}: ${metadata.description || 'No description'}`);
    }
    
    // Write template registry
    const registryPath = 'config/templates.json';
    await fs.outputJSON(registryPath, {
      built: new Date().toISOString(),
      templates: templates
    }, { spaces: 2 });
    
    console.log('');
    console.log(chalk.green('✅ Templates built successfully!'));
    console.log(`Registry saved to: ${registryPath}`);
    return true;
    
  } catch (error) {
    console.log('');
    console.log(chalk.red('❌ Template build failed:'));
    console.log(chalk.red(`   ${error.message}`));
    return false;
  }
}

function extractDescription(content) {
  // Look for description in comment
  const match = content.match(/% (.+(?:Template|template).+)/);
  return match ? match[1] : null;
}

function extractVariables(content) {
  // Find all $variable$ patterns
  const matches = content.match(/\$\w+\$/g) || [];
  return [...new Set(matches)].sort();
}

function extractPackages(content) {
  // Find all \usepackage{} declarations
  const matches = content.match(/\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}/g) || [];
  return matches.map(match => {
    const pkg = match.match(/\{([^}]+)\}/)[1];
    return pkg;
  });
}

// CLI usage
if (require.main === module) {
  buildTemplates()
    .then(success => process.exit(success ? 0 : 1))
    .catch(error => {
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    });
}

module.exports = { buildTemplates };
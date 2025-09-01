#!/usr/bin/env node
/**
 * Doc Forge Request Validator
 * Validates request.json files for PDF generation
 */

const fs = require('fs-extra');
const chalk = require('chalk');
const path = require('path');

const REQUIRED_FIELDS = ['documents'];
const DOCUMENT_REQUIRED_FIELDS = ['input', 'output'];

async function validateRequest(requestFile = 'inbox/request.json') {
  console.log(chalk.blue('🔍 Validating request...'));
  
  try {
    // Check if request file exists
    if (!await fs.pathExists(requestFile)) {
      throw new Error(`Request file not found: ${requestFile}`);
    }

    // Parse JSON
    const request = await fs.readJSON(requestFile);
    console.log(chalk.green('✓') + ' JSON format is valid');

    // Validate required fields
    for (const field of REQUIRED_FIELDS) {
      if (!request[field]) {
        throw new Error(`Missing required field: ${field}`);
      }
    }
    console.log(chalk.green('✓') + ' Required fields present');

    // Validate documents array
    if (!Array.isArray(request.documents)) {
      throw new Error('Documents must be an array');
    }

    if (request.documents.length === 0) {
      throw new Error('Documents array cannot be empty');
    }

    // Validate each document
    for (let i = 0; i < request.documents.length; i++) {
      const doc = request.documents[i];
      console.log(chalk.gray(`  Validating document ${i + 1}...`));

      // Check required document fields
      for (const field of DOCUMENT_REQUIRED_FIELDS) {
        if (!doc[field]) {
          throw new Error(`Document ${i + 1}: Missing required field '${field}'`);
        }
      }

      // Check if input file exists
      const inputPath = path.join('inbox', doc.input);
      if (!await fs.pathExists(inputPath)) {
        throw new Error(`Document ${i + 1}: Input file not found: ${doc.input}`);
      }

      // Check template if specified
      if (doc.template) {
        const templatePath = `templates/${doc.template}.latex`;
        if (!await fs.pathExists(templatePath)) {
          console.log(chalk.yellow('⚠') + ` Template not found: ${doc.template}, will use default`);
        }
      }

      console.log(chalk.green('✓') + ` Document ${i + 1} is valid`);
    }

    console.log('');
    console.log(chalk.green('✅ Request validation successful!'));
    console.log(`Found ${request.documents.length} document(s) to process`);
    return true;

  } catch (error) {
    console.log('');
    console.log(chalk.red('❌ Validation failed:'));
    console.log(chalk.red(`   ${error.message}`));
    return false;
  }
}

// CLI usage
if (require.main === module) {
  const requestFile = process.argv[2] || 'inbox/request.json';
  
  validateRequest(requestFile)
    .then(isValid => process.exit(isValid ? 0 : 1))
    .catch(error => {
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    });
}

module.exports = { validateRequest };
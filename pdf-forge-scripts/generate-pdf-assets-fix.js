#!/usr/bin/env node
/**
 * Doc Forge PDF Generator - ASSET-AWARE VERSION
 * Fixes image loading by setting correct resource path
 * 
 * CRITICAL FIX:
 * - Adds --resource-path=inbox to pandoc command
 * - This tells pandoc to look for assets relative to inbox/
 * - Supports assets/ subfolder for images
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const { execSync } = require('child_process');

async function generatePDF(
  inputFile,
  outputFile,
  template = 'admin-manual',
  variables = {},
  pandocArgs = [],
  metadata = {}
) {
  const texOutputFile = outputFile.replace(/\.pdf$/, '.tex');
  console.log(chalk.blue('📄 Generating PDF...'));
  console.log(`  Input:  ${inputFile}`);
  console.log(`  Output: ${outputFile}`);
  console.log(`  DBG Tex: ${texOutputFile}`);
  console.log(`  Template: ${template}`);
  
  if (pandocArgs.length > 0) {
    console.log(`  Pandoc Args: ${pandocArgs.join(' ')}`);
  }

  // Check if input file exists
  if (!(await fs.pathExists(inputFile))) {
    throw new Error(`Input file not found: ${inputFile}`);
  }

  // Check if template exists
  const templatePath = `templates/${template}.latex`;
  if (!(await fs.pathExists(templatePath))) {
    throw new Error(`Template not found: ${templatePath}`);
  }

  // Check if assets folder exists (for documents with images)
  const inputDir = path.dirname(inputFile);
  const assetsPath = path.join(inputDir, 'assets');
  if (await fs.pathExists(assetsPath)) {
    console.log(chalk.yellow(`  📷 Assets folder found: ${assetsPath}`));
  }

  // Merge metadata and variables (metadata takes precedence)
  const allVariables = { ...variables, ...metadata };
  
  // Prepare variables for pandoc
  const varArgs = Object.entries(allVariables)
    .map(([key, value]) => {
      // Handle boolean values
      if (typeof value === 'boolean') {
        return value ? `--variable ${key}` : '';
      }
      // Handle other values
      return `--variable ${key}="${value}"`;
    })
    .filter(arg => arg !== '')
    .join(' ');

  // Join pandoc_args array into string
  const customPandocArgs = pandocArgs.join(' ');

  // CRITICAL FIX: Add --resource-path to tell pandoc where to find images
  // This makes assets/image.png resolve relative to the markdown file's directory
  const resourcePath = `--resource-path="${inputDir}"`;

  // First, create the .tex file (for debugging)
  const texCommand = [
    'pandoc',
    `"${inputFile}"`,
    '-o',
    `"${texOutputFile}"`,
    '--template',
    `"${templatePath}"`,
    '--listings',
    resourcePath,        // CRITICAL: Tell pandoc where to find resources
    customPandocArgs,
    varArgs,
  ].filter(arg => arg !== '').join(' ');

  try {
    console.log(chalk.gray('Generating .tex for debugging...'));
    console.log(chalk.gray(`Command: ${texCommand}`));
    execSync(texCommand, { stdio: 'pipe' });
    console.log(chalk.green('✅ TEX generated successfully!'));
  } catch (error) {
    console.error(chalk.red('❌ TEX generation failed:'));
    console.error(error.message);
  }

  // Build pandoc command for PDF
  const command = [
    'pandoc',
    `"${inputFile}"`,
    '-o',
    `"${outputFile}"`,
    '--template',
    `"${templatePath}"`,
    '--pdf-engine=xelatex',
    '--listings',
    resourcePath,        // CRITICAL: Tell pandoc where to find resources
    customPandocArgs,
    varArgs,
  ].filter(arg => arg !== '').join(' ');

  try {
    console.log(chalk.gray('Running pandoc for PDF...'));
    console.log(chalk.gray(`Command: ${command}`));
    execSync(command, { stdio: 'pipe' });
    console.log(chalk.green('✅ PDF generated successfully!'));
    return true;
  } catch (error) {
    console.error(chalk.red('❌ PDF generation failed:'));
    console.error(error.message);
    return false;
  }
}

async function validateRequest(request) {
  console.log(chalk.blue('🔍 Validating request...'));
  
  // Check JSON structure
  if (!request) {
    throw new Error('Request is empty or invalid JSON');
  }
  
  console.log(chalk.green('✓ JSON format is valid'));
  
  // Check for required fields
  if (!request.documents || !Array.isArray(request.documents)) {
    throw new Error('Missing required field: documents (must be an array)');
  }
  
  console.log(chalk.green('✓ Required fields present'));
  
  // Validate each document
  for (let i = 0; i < request.documents.length; i++) {
    const doc = request.documents[i];
    console.log(chalk.gray(`  Validating document ${i + 1}...`));
    
    if (!doc.input) {
      throw new Error(`Document ${i + 1}: missing required field 'input'`);
    }
    if (!doc.output) {
      throw new Error(`Document ${i + 1}: missing required field 'output'`);
    }
    
    // Check if input file exists
    const inputPath = `inbox/${doc.input}`;
    if (!(await fs.pathExists(inputPath))) {
      throw new Error(`Document ${i + 1}: input file not found: ${inputPath}`);
    }
    
    console.log(chalk.green(`✓ Document ${i + 1} is valid`));
  }
  
  console.log(chalk.green('\n✅ Request validation successful!'));
  return true;
}

async function processRequest(requestFile = null) {
  try {
    console.log(chalk.cyan('Starting PDF generation process'));
    
    // Determine request path
    let requestPath;
    if (requestFile) {
      // If a specific request file is provided
      requestPath = requestFile;
      console.log(chalk.blue(`📋 Using request file: ${requestPath}`));
    } else {
      // Default to inbox/request.json
      requestPath = 'inbox/request.json';
    }
    
    // Check if request file exists
    if (!(await fs.pathExists(requestPath))) {
      throw new Error(`Request file not found: ${requestPath}`);
    }

    console.log(chalk.blue('📋 Validating request...'));
    const request = await fs.readJSON(requestPath);
    
    // Validate the request
    await validateRequest(request);

    console.log(
      chalk.blue(`Found ${request.documents.length} document(s) to process`)
    );
    console.log(chalk.blue('📄 Processing documents...'));

    // Ensure output directory exists
    await fs.ensureDir('output');
    await fs.ensureDir('outbox');

    let totalSuccess = 0;

    // Process each document
    for (let i = 0; i < request.documents.length; i++) {
      const doc = request.documents[i];
      console.log(
        chalk.blue(
          `\n📄 Processing document ${i + 1}/${request.documents.length}`
        )
      );

      const inputPath = `inbox/${doc.input}`;
      const outputPath = `output/${doc.output}`;

      // Use enhanced generatePDF with asset support
      const success = await generatePDF(
        inputPath,
        outputPath,
        doc.template || 'admin-manual',
        doc.variables || {},
        doc.pandoc_args || [],
        doc.metadata || {}
      );

      if (success) {
        totalSuccess++;
        // Copy to outbox
        await fs.copy(outputPath, `outbox/${doc.output}`);
      }
    }

    console.log(
      chalk.green(
        `\n✅ Successfully processed ${totalSuccess}/${request.documents.length} documents`
      )
    );

    // Create generation log
    const logContent = `PDF Generation Log
Generated: ${new Date().toISOString()}
Documents processed: ${totalSuccess}/${request.documents.length}
Success rate: ${Math.round((totalSuccess / request.documents.length) * 100)}%

${request.documents
  .map((doc, i) => `${i + 1}. ${doc.input} → ${doc.output} (${doc.template})`)
  .join('\n')}
`;
    await fs.writeFile('output/generation.log', logContent);

    return totalSuccess === request.documents.length;
  } catch (error) {
    console.error(chalk.red('❌ Request processing failed:'));
    console.error(error.message);
    return false;
  }
}

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    // No arguments - process inbox/request.json
    processRequest()
      .then((success) => process.exit(success ? 0 : 1))
      .catch((error) => {
        console.error(chalk.red('Error:'), error.message);
        process.exit(1);
      });
  } else if (args[0].endsWith('.json')) {
    // First argument is a request file
    processRequest(args[0])
      .then((success) => process.exit(success ? 0 : 1))
      .catch((error) => {
        console.error(chalk.red('Error:'), error.message);
        process.exit(1);
      });
  } else if (args.length >= 2) {
    // Arguments provided - direct mode
    const [inputFile, outputFile, template] = args;
    const variables = {};

    // Parse additional variables (key=value format)
    for (let i = 3; i < args.length; i++) {
      const [key, value] = args[i].split('=');
      if (key && value) {
        variables[key] = value;
      }
    }

    generatePDF(inputFile, outputFile, template, variables)
      .then((success) => process.exit(success ? 0 : 1))
      .catch((error) => {
        console.error(chalk.red('Error:'), error.message);
        process.exit(1);
      });
  } else {
    console.log(
      'Usage: node generate-pdf.js [<input.md> <output.pdf> [template] [variables...]]'
    );
    console.log('       node generate-pdf.js <request.json>');
    console.log('       node generate-pdf.js (processes inbox/request.json)');
    process.exit(1);
  }
}

module.exports = { generatePDF };
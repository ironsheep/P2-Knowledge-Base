#!/usr/bin/env node
/**
 * PRODUCTION DOCUMENT GENERATION SYSTEM
 * Doc Forge PDF Generator - ENHANCED for P2 Knowledge Base
 * 
 * ==========================================
 * AI DECISION GUIDANCE - READ THIS FIRST!
 * ==========================================
 * 
 * PURPOSE: Generate final deliverable PDFs for distribution and publication
 * FORMAT: document_generation (format_type: "document_generation")
 * WORKFLOW: Production document creation with specific output requirements
 * 
 * USE WHEN:
 * - User says: "generate the manual", "create deliverables", "make production PDFs"
 * - User says: "create the final document", "generate for publication"
 * - User says: "build the PDF", "export to PDF", "create release documents"
 * - Need specific output filenames (Manual-v1.pdf, Guide-v2.pdf, etc.)
 * - Multiple different documents with different templates in one job
 * - Final deliverable creation for end users
 * - Production workflow with quality requirements
 * 
 * DO NOT USE FOR:
 * - Template testing or development (use watch-shared-workspace.js)
 * - Template validation (use watch-shared-workspace.js)
 * - Testing template behavior against multiple inputs (use watch-shared-workspace.js)
 * - Development/debugging workflows (use watch-shared-workspace.js)
 * 
 * FORMAT STRUCTURE:
 * {
 *   "format_type": "document_generation",
 *   "documents": [
 *     {
 *       "input": "document.md",
 *       "output": "Final-Document.pdf", 
 *       "template": "template-name",
 *       "metadata": {...},
 *       "pandoc_args": [...],
 *       "lua_filters": [...]
 *     }
 *   ]
 * }
 * 
 * TECHNICAL ENHANCEMENTS:
 * - Supports pandoc_args from request.json
 * - Supports metadata field (preferred over variables)
 * - Maintains backward compatibility with variables
 * - ASSET SUPPORT: Handles images in assets/ subfolder (2025-08-25)
 * - RELIABILITY: Fail-fast behavior with timeouts and clear error messages
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
  pandocArgs = [],  // NEW: Accept pandoc_args
  metadata = {}     // NEW: Accept metadata (preferred over variables)
) {
  const texOutputFile = outputFile.replace(/\.pdf$/, '.tex');
  console.log(chalk.blue('📄 Generating PDF...'));
  console.log(`  Input:  ${inputFile}`);
  console.log(`  Output: ${outputFile}`);
  console.log(`  DBG Tex: ${texOutputFile}`);
  console.log(`  Template: ${template}`);
  
  // NEW: Show pandoc_args if present
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

  // NEW: Join pandoc_args array into string
  const customPandocArgs = pandocArgs.join(' ');

  // ASSET SUPPORT: Add --resource-path to tell pandoc where to find images
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
    resourcePath,      // ASSET SUPPORT: Tell pandoc where to find resources
    customPandocArgs,  // NEW: Include custom pandoc args
    varArgs,
  ].filter(arg => arg !== '').join(' ');

  try {
    console.log(chalk.gray('Generating .tex for debugging...'));
    console.log(chalk.gray(`Command: ${texCommand}`));
    // Set TEXINPUTS to include templates directory for .sty files
    const envWithTexInputs = {
      ...process.env,
      TEXINPUTS: `./templates//:${process.env.TEXINPUTS || ''}`
    };
    execSync(texCommand, { stdio: 'pipe', env: envWithTexInputs, timeout: 300000 }); // 5 minute timeout
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
    resourcePath,      // ASSET SUPPORT: Tell pandoc where to find resources
    customPandocArgs,  // NEW: Include custom pandoc args
    varArgs,
  ].filter(arg => arg !== '').join(' ');

  try {
    console.log(chalk.gray('Running pandoc for PDF...'));
    console.log(chalk.gray(`Command: ${command}`));
    // Set TEXINPUTS to include templates directory for .sty files
    const envWithTexInputs = {
      ...process.env,
      TEXINPUTS: `./templates//:${process.env.TEXINPUTS || ''}`
    };
    execSync(command, { stdio: 'pipe', env: envWithTexInputs, timeout: 600000 }); // 10 minute timeout
    console.log(chalk.green('✅ PDF generated successfully!'));
    return true;
  } catch (error) {
    console.error(chalk.red('❌ PDF generation failed:'));
    console.error(error.message);
    return false;
  }
}

async function processRequest() {
  try {
    // Read request.json
    const requestPath = 'inbox/request.json';
    if (!(await fs.pathExists(requestPath))) {
      console.error(chalk.red('❌ FATAL: No request.json found in inbox/'));
      process.exit(1);
    }

    let request;
    try {
      request = await fs.readJSON(requestPath);
    } catch (jsonError) {
      console.error(chalk.red('❌ FATAL: Failed to parse request.json:'));
      console.error(chalk.red(`   ${jsonError.message}`));
      process.exit(1);
    }

    if (!request.documents || !Array.isArray(request.documents)) {
      console.error(chalk.red('❌ FATAL: Invalid request.json format:'));
      console.error(chalk.red('   Expected: documents array'));
      console.error(chalk.red(`   Found: ${typeof request.documents}`));
      process.exit(1);
    }

    console.log(
      chalk.blue(`Found ${request.documents.length} document(s) to process`)
    );

    // Ensure output directory exists
    try {
      await fs.ensureDir('output');
      await fs.ensureDir('outbox');
    } catch (dirError) {
      console.error(chalk.red('❌ FATAL: Cannot create output directories:'));
      console.error(chalk.red(`   ${dirError.message}`));
      process.exit(1);
    }

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

      // Handle lua_filters array - convert to pandoc_args format
      let processedPandocArgs = doc.pandoc_args || [];
      if (doc.lua_filters && Array.isArray(doc.lua_filters)) {
        const luaFilterArgs = doc.lua_filters.map(filter => {
          const filterName = filter.endsWith('.lua') ? filter : `${filter}.lua`;
          return `--lua-filter=filters/${filterName}`;
        });
        // Prepend lua filters to other pandoc_args
        processedPandocArgs = [...luaFilterArgs, ...processedPandocArgs];
      }

      // NEW: Use enhanced generatePDF with pandoc_args and metadata support
      const success = await generatePDF(
        inputPath,
        outputPath,
        doc.template || 'admin-manual',
        doc.variables || {},      // Backward compatibility
        processedPandocArgs,       // Includes lua_filters
        doc.metadata || {}         // NEW: Pass metadata
      );

      if (success) {
        totalSuccess++;
        // Copy to outbox with timeout protection
        try {
          await fs.copy(outputPath, `outbox/${doc.output}`);
        } catch (copyError) {
          console.error(chalk.red(`❌ WARNING: Failed to copy ${doc.output} to outbox:`));
          console.error(chalk.red(`   ${copyError.message}`));
          // Don't exit here - PDF was generated successfully, copy failure is not fatal
        }
      }
    }

    console.log(
      chalk.green(
        `\n✅ Successfully processed ${totalSuccess}/${request.documents.length} documents`
      )
    );

    // Create generation log for shell script compatibility
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
    // No arguments - process request.json
    processRequest()
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
    console.log('       node generate-pdf.js (processes inbox/request.json)');
    process.exit(1);
  }
}

module.exports = { generatePDF };
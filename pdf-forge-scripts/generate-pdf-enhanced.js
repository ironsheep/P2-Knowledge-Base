#!/usr/bin/env node
/**
 * Doc Forge PDF Generator - ENHANCED v2 for P2 Knowledge Base
 * Converts markdown to PDF using templates with full pandoc_args support
 * 
 * ENHANCEMENTS v2:
 * - Filters work like templates (just name, no path/extension)
 * - Supports pandoc_args from request.json
 * - Supports metadata field (preferred over variables)
 * - Maintains backward compatibility with variables
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const { execSync } = require('child_process');

/**
 * Process pandoc arguments to handle filters consistently with templates
 * Transforms filter names to full paths automatically
 */
function processPandocArgs(pandocArgs) {
  return pandocArgs.map(arg => {
    // Check if this is a lua-filter argument
    if (arg.startsWith('--lua-filter=')) {
      const filterName = arg.substring('--lua-filter='.length);
      
      // If it already has a path or extension, leave it alone (backward compatibility)
      if (filterName.includes('/') || filterName.includes('.lua')) {
        return arg;
      }
      
      // Otherwise, add filters/ prefix and .lua extension
      const filterPath = `filters/${filterName}.lua`;
      console.log(chalk.gray(`  Filter: ${filterName} → ${filterPath}`));
      return `--lua-filter=${filterPath}`;
    }
    
    // Return other arguments unchanged
    return arg;
  });
}

async function generatePDF(
  inputFile,
  outputFile,
  template = 'admin-manual',
  variables = {},
  pandocArgs = [],  // Accept pandoc_args
  metadata = {}     // Accept metadata (preferred over variables)
) {
  const texOutputFile = outputFile.replace(/\.pdf$/, '.tex');
  console.log(chalk.blue('📄 Generating PDF...'));
  console.log(`  Input:  ${inputFile}`);
  console.log(`  Output: ${outputFile}`);
  console.log(`  DBG Tex: ${texOutputFile}`);
  console.log(`  Template: ${template}`);
  
  // Process pandoc args to handle filters consistently
  const processedArgs = processPandocArgs(pandocArgs);
  
  if (processedArgs.length > 0) {
    console.log(`  Pandoc Args: ${processedArgs.join(' ')}`);
  }

  // Check if input file exists
  if (!(await fs.pathExists(inputFile))) {
    throw new Error(`Input file not found: ${inputFile}`);
  }

  // Check if template exists (with automatic path/extension)
  const templatePath = `templates/${template}.latex`;
  if (!(await fs.pathExists(templatePath))) {
    throw new Error(`Template not found: ${templatePath}`);
  }

  // Check if filters exist
  for (const arg of processedArgs) {
    if (arg.startsWith('--lua-filter=')) {
      const filterPath = arg.substring('--lua-filter='.length);
      if (!(await fs.pathExists(filterPath))) {
        throw new Error(`Filter not found: ${filterPath}`);
      }
    }
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

  // Join processed pandoc_args array into string
  const customPandocArgs = processedArgs.join(' ');

  // First, create the .tex file (for debugging)
  const texCommand = [
    'pandoc',
    `"${inputFile}"`,
    '-o',
    `"${texOutputFile}"`,
    '--template',
    `"${templatePath}"`,
    '--listings',
    customPandocArgs,  // Include processed pandoc args
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
    customPandocArgs,  // Include processed pandoc args
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

async function processRequest() {
  try {
    // Read request.json
    const requestPath = 'inbox/request.json';
    if (!(await fs.pathExists(requestPath))) {
      throw new Error('No request.json found in inbox/');
    }

    const request = await fs.readJSON(requestPath);

    if (!request.documents || !Array.isArray(request.documents)) {
      throw new Error('Invalid request.json: documents array missing');
    }

    console.log(
      chalk.blue(`Found ${request.documents.length} document(s) to process`)
    );

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

      // Use enhanced generatePDF with processed pandoc_args
      const success = await generatePDF(
        inputPath,
        outputPath,
        doc.template || 'admin-manual',
        doc.variables || {},      // Backward compatibility
        doc.pandoc_args || [],     // Pass pandoc_args
        doc.metadata || {}         // Pass metadata
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
    processRequest()
      .then((success) => {
        if (success) {
          console.log(chalk.green('✨ All done!'));
          process.exit(0);
        } else {
          console.log(chalk.yellow('⚠️ Some documents failed'));
          process.exit(1);
        }
      })
      .catch((error) => {
        console.error(chalk.red('Fatal error:'), error.message);
        process.exit(1);
      });
  } else if (args.length === 3) {
    // Direct CLI usage: node generate-pdf.js input.md output.pdf template
    generatePDF(`inbox/${args[0]}`, `output/${args[1]}`, args[2])
      .then((success) => {
        process.exit(success ? 0 : 1);
      })
      .catch((error) => {
        console.error(chalk.red('Fatal error:'), error.message);
        process.exit(1);
      });
  } else {
    console.log('Usage: node generate-pdf.js');
    console.log('       node generate-pdf.js input.md output.pdf template');
    process.exit(1);
  }
}

module.exports = { generatePDF, processRequest };
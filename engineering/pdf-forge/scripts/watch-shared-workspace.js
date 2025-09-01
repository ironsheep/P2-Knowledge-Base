#!/usr/bin/env node
/**
 * TEMPLATE TESTING SYSTEM
 * PDF Forge Shared Workspace Monitor - Template Development & Validation
 *
 * ==========================================
 * AI DECISION GUIDANCE - READ THIS FIRST!
 * ==========================================
 * 
 * PURPOSE: Test template behavior and validate template development
 * FORMAT: template_testing (format_type: "template_testing")
 * WORKFLOW: Template testing, development validation, single-template focus
 * 
 * USE WHEN:
 * - User says: "test this template", "validate template behavior"
 * - User says: "test the template", "debug template issues"
 * - User says: "check if template works", "validate template design"
 * - User says: "test template against multiple inputs"
 * - Focus on ONE template's behavior against various test scenarios
 * - Development/debugging workflow for templates
 * - Template validation before production use
 * - Interactive template development and iteration
 * 
 * DO NOT USE FOR:
 * - Production document generation (use generate-pdf.js)
 * - Creating final deliverable PDFs (use generate-pdf.js)
 * - Multiple different documents/templates in one job (use generate-pdf.js)
 * - Publishing workflow (use generate-pdf.js)
 * 
 * FORMAT STRUCTURE:
 * {
 *   "format_type": "template_testing",
 *   "template": "template-name.latex",
 *   "metadata": {
 *     "title": "Default title for all tests",
 *     "author": "Default author"
 *   },
 *   "tests": [
 *     {
 *       "name": "test-case-name",
 *       "input": "test-input.md",
 *       "metadata": {...},
 *       "pandoc_args": [...],
 *       "lua_filters": [...],
 *       "variables": {...}
 *     }
 *   ]
 * }
 * 
 * SYSTEM FEATURES:
 * - Monitors /workspace/shared/ for test requests automatically
 * - Provides intelligent error analysis and auto-fix capabilities
 * - Generates .tex files for debugging template issues
 * - Creates comprehensive test result reports
 * - RELIABILITY: Fail-fast behavior with timeouts and clear error messages
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const chokidar = require('chokidar');
const { execSync } = require('child_process');

const SHARED_PATH = '/workspace/shared';
const REQUESTS_PATH = path.join(SHARED_PATH, 'test-requests');
const RESULTS_PATH = path.join(SHARED_PATH, 'test-results');
const TEMPLATES_PATH = path.join(SHARED_PATH, 'templates');
const TEST_DOCS_PATH = path.join(SHARED_PATH, 'test-documents');
const OUTPUT_PDFS_PATH = path.join(SHARED_PATH, 'output-pdfs');
const STATUS_PATH = path.join(SHARED_PATH, 'status');

class SharedWorkspaceMonitor {
  constructor() {
    this.isProcessing = false;
    this.setupEnvironment();
    this.setupWatchers();
    this.logActivity('🚀 PDF Forge Shared Workspace Monitor started');
    this.signalReady();
  }

  async setupEnvironment() {
    // Ensure all directories exist with proper error handling
    try {
      await fs.ensureDir(REQUESTS_PATH);
      await fs.ensureDir(RESULTS_PATH);
      await fs.ensureDir(TEMPLATES_PATH);
      await fs.ensureDir(TEST_DOCS_PATH);
      await fs.ensureDir(OUTPUT_PDFS_PATH);
      await fs.ensureDir(STATUS_PATH);
      await fs.ensureDir(path.join(REQUESTS_PATH, 'processed'));
    } catch (dirError) {
      console.error(chalk.red('❌ FATAL: Cannot create required directories:'));
      console.error(chalk.red(`   ${dirError.message}`));
      process.exit(1);
    }
  }

  setupWatchers() {
    // Watch for new test requests
    const requestWatcher = chokidar.watch(path.join(REQUESTS_PATH, '*.json'), {
      ignored: /processed/,
      persistent: true,
      awaitWriteFinish: {
        stabilityThreshold: 1000,
        pollInterval: 100,
      },
    });

    requestWatcher
      .on('add', (filePath) => this.onNewRequest(filePath))
      .on('change', (filePath) => this.onRequestModified(filePath))
      .on('error', (error) => this.logError('Request watcher error:', error));

    // Watch for template changes
    const templateWatcher = chokidar.watch(
      path.join(TEMPLATES_PATH, '*.latex')
    );
    templateWatcher
      .on('change', (filePath) => this.onTemplateChanged(filePath))
      .on('error', (error) => this.logError('Template watcher error:', error));

    this.logActivity('📡 File watchers initialized');
  }

  async onNewRequest(requestPath) {
    if (this.isProcessing) {
      this.logActivity(
        `⏳ Request queued, processing in progress...${path.basename(requestPath)}`
      );
      return;
    }

    try {
      this.isProcessing = true;
      const requestFile = path.basename(requestPath);
      this.logActivity(`📋 New test request: ${requestFile}`);

      const request = await this.parseRequest(requestPath);
      const results = await this.processTestRequest(request);

      await this.writeResults(request, results);
      await this.archiveRequest(requestPath);

      this.logActivity(`✅ Test request completed: ${request.request_id}`);
    } catch (error) {
      this.logError(
        `💥 CRITICAL ERROR processing ${path.basename(requestPath)}:`,
        error
      );
      await this.writeErrorResult(requestPath, error);

      // For parsing errors, make it very obvious and consider halting
      if (error.message.includes('Failed to parse request')) {
        console.error(chalk.red.bold('❌ TEST REJECTED ❌'));
        console.error(chalk.red.bold(`REASON: ${error.message}`));
        console.error(chalk.red(`FILE: ${path.basename(requestPath)}`));
        console.error(
          chalk.yellow(
            'EXPECTED FORMAT: {"template": "name.latex", "tests": [...]}'
          )
        );
        console.error('');

        // Optionally exit on parse failures (uncomment to enable)
        // console.error(chalk.red('🛑 Exiting due to parse failure...'));
        // process.exit(1);
      }
    } finally {
      this.isProcessing = false;
    }
  }

  async parseRequest(requestPath) {
    this.logActivity(`⏳ Parse...${path.basename(requestPath)}`);
    if (!(await fs.pathExists(requestPath))) {
      this.logError(`📁 Request file not found: ${path.basename(requestPath)}`);
      console.error(chalk.red('❌ FATAL: Test request file missing'));
      process.exit(1);
    }
    try {
      let content;
      try {
        content = await fs.readFile(requestPath, 'utf8');
      } catch (readError) {
        console.error(chalk.red(`❌ FATAL: Cannot read request file: ${readError.message}`));
        process.exit(1);
      }
      
      let request;
      try {
        request = JSON.parse(content);
      } catch (parseError) {
        console.error(chalk.red(`❌ FATAL: Invalid JSON in request file: ${parseError.message}`));
        process.exit(1);
      }

      // Enhanced validation with detailed error messages
      if (!request.template) {
        const availableFields = Object.keys(request).join(', ');
        console.error(chalk.red('❌ FATAL: Invalid request format - missing template field'));
        console.error(chalk.red(`   Found fields: [${availableFields}]`));
        console.error(chalk.red('   Expected format: {"template": "name.latex", "tests": [...]}'));
        process.exit(1);
      }

      if (!request.tests) {
        console.error(chalk.red('❌ FATAL: Invalid request format - missing tests field'));
        console.error(chalk.red('   Expected format: {"template": "name.latex", "tests": [{"name": "test-name", "input": "file.md"}]}'));
        process.exit(1);
      }

      // Set defaults
      request.request_id =
        request.request_id || path.basename(requestPath, '.json');
      request.timestamp = request.timestamp || new Date().toISOString();
      request.options = request.options || {};
      request.tests = request.tests || [
        { name: 'default', input: 'minimal.md' },
      ];

      // Log successful parse
      this.logActivity(
        `✓ Request parsed: template=${request.template}, tests=${request.tests.length}`
      );

      return request;
    } catch (error) {
      if (error instanceof SyntaxError) {
        throw new Error(
          `Failed to parse request: Invalid JSON syntax - ${error.message}`
        );
      }
      throw new Error(`Failed to parse request: ${error.message}`);
    }
  }

  async processTestRequest(request) {
    this.logActivity(`⏳ Process Request...${request.request_id}`);
    const startTime = Date.now();
    const results = {
      request_id: request.request_id,
      status: 'in_progress',
      timestamp: new Date().toISOString(),
      forge_version: 'Enhanced by Claude v1.0',
      template: request.template,
      test_results: [],
      performance: {},
      overall_result: 'unknown',
    };

    try {
      // Validate template exists
      const templatePath = path.join(TEMPLATES_PATH, request.template);
      if (!(await fs.pathExists(templatePath))) {
        throw new Error(`Template not found: ${request.template}`);
      }

      this.logActivity(`🔧 Testing template: ${request.template}`);

      // Process each test
      for (const test of request.tests) {
        this.logActivity(`   Testing: ${test.name}`);
        const testResult = await this.runSingleTest(
          templatePath,
          test,
          request.options,
          request.metadata || {}
        );
        results.test_results.push(testResult);
      }

      // Determine overall result
      const failures = results.test_results.filter((t) =>
        t.status.includes('FAIL')
      );
      results.overall_result =
        failures.length === 0 ? 'success' : 'partial_failure';
      results.status = 'completed';

      // Performance metrics
      results.performance = {
        total_duration_ms: Date.now() - startTime,
        tests_run: request.tests.length,
        failures: failures.length,
      };

      this.logActivity(
        `📊 Overall result: ${results.overall_result} (${failures.length} failures)`
      );
    } catch (error) {
      results.status = 'failed';
      results.error = error.message;
      results.overall_result = 'error';
      this.logError('Test processing failed:', error);
    }

    return results;
  }

  async runSingleTest(templatePath, test, options, requestMetadata = {}) {
    const testStartTime = Date.now();
    const testResult = {
      name: test.name,
      status: 'unknown',
      duration_ms: 0,
      error: null,
      pdf_path: null,
      auto_fix_attempted: false,
    };

    try {
      // Validate test input file exists
      const testDocPath = path.join(TEST_DOCS_PATH, test.input);
      if (!(await fs.pathExists(testDocPath))) {
        throw new Error(`Test input file not found: ${test.input}`);
      }

      // Generate unique output name
      const outputName = `${test.name}-${Date.now()}`;
      const outputPdf = path.join(OUTPUT_PDFS_PATH, `${outputName}.pdf`);
      const outputTex = path.join(OUTPUT_PDFS_PATH, `${outputName}.tex`);
      const resultTex = path.join(RESULTS_PATH, `${outputName}.tex`);

      // Setup enhanced working directory with .sty file support
      const workingEnv = await this.setupWorkingDirectory(
        templatePath,
        test.name
      );

      // Build pandoc command with working directory, lua_filters, and metadata
      const pandocCmd = this.buildPandocCommand(
        testDocPath,
        outputPdf,
        workingEnv.templatePath,
        test,
        options,
        workingEnv.workDir,
        requestMetadata
      );

      this.logActivity(`     Running: pandoc for ${test.name}`);

      // Execute pandoc
      try {
        // Generate .tex for debugging
        const texCmd = pandocCmd
          .replace(`-o "${outputPdf}"`, `-o "${outputTex}"`)
          .replace('--pdf-engine=xelatex', '');

        let texGenerated = false;
        try {
          execSync(texCmd, { stdio: 'pipe', cwd: workingEnv.workDir, timeout: 300000 }); // 5 minute timeout

          // Copy .tex file to results directory for debugging access
          if (await fs.pathExists(outputTex)) {
            try {
              await fs.copy(outputTex, resultTex);
            } catch (copyError) {
              this.logError(`Failed to copy .tex file: ${copyError.message}`);
              // Continue - this is not fatal
            }
            testResult.tex_path = `${path.basename(resultTex)}`;
            testResult.tex_available = true;
            texGenerated = true;
            this.logActivity(
              `       📄 .tex file available: ${path.basename(resultTex)}`
            );
          }
        } catch (texError) {
          testResult.tex_available = false;
          testResult.tex_error = texError.stderr
            ? texError.stderr.toString()
            : texError.message;
          this.logActivity(
            `       ❌ .tex generation failed: ${testResult.tex_error.split('\n')[0]}`
          );
        }

        // Generate PDF
        execSync(pandocCmd, { stdio: 'pipe', cwd: workingEnv.workDir, timeout: 600000 }); // 10 minute timeout

        testResult.status = '✅ PASS';
        testResult.pdf_path = `output-pdfs/${outputName}.pdf`;

        // Validate output
        if (await fs.pathExists(outputPdf)) {
          const stats = await fs.stat(outputPdf);
          testResult.pdf_size_bytes = stats.size;
        }
      } catch (pandocError) {
        // Always cleanup working directory
        if (workingEnv.workDir) {
          await fs.remove(workingEnv.workDir).catch(() => {});
        }
        const errorOutput = pandocError.stderr
          ? pandocError.stderr.toString()
          : pandocError.message;
        testResult.status = '❌ FAIL';
        testResult.error = errorOutput;

        // Ensure tex availability is noted even on failure
        if (!testResult.hasOwnProperty('tex_available')) {
          testResult.tex_available = false;
          testResult.tex_error =
            'PDF generation failed before .tex could be generated';
        }

        // Attempt auto-fix if requested
        if (options.auto_fix_attempt) {
          const fixResult = await this.attemptAutoFix(
            templatePath,
            errorOutput,
            test
          );
          if (fixResult.success) {
            testResult.auto_fix_attempted = true;
            testResult.auto_fix_result = fixResult;
            testResult.status = '🔧 FIXED';
          }
        }

        // Analyze error for better reporting
        testResult.error_analysis = this.analyzeError(errorOutput);
      }
    } catch (error) {
      testResult.status = '❌ ERROR';
      testResult.error = error.message;
    }

    testResult.duration_ms = Date.now() - testStartTime;
    return testResult;
  }

  /**
   * Enhanced working directory setup with .sty file management
   * Solves LaTeX \usepackage dependency issues for layered templates
   */
  async setupWorkingDirectory(templatePath, testName) {
    try {
      // Create unique working directory
      const workDir = path.join(
        '/tmp',
        `pandoc-work-${testName}-${Date.now()}`
      );
      await fs.ensureDir(workDir);

      // Copy template to working directory
      const templateName = path.basename(templatePath);
      const workTemplatePath = path.join(workDir, templateName);
      await fs.copy(templatePath, workTemplatePath);

      this.logActivity(`       🔧 Working directory: ${workDir}`);
      this.logActivity(`       📄 Template copied: ${templateName}`);

      // Find and copy ALL .sty files from templates directory
      let templatesDirFiles;
      try {
        templatesDirFiles = await fs.readdir(TEMPLATES_PATH);
      } catch (readdirError) {
        this.logError('Failed to read templates directory:', readdirError);
        throw new Error(`Templates directory read failed: ${readdirError.message}`);
      }
      const styFiles = templatesDirFiles.filter((file) =>
        file.endsWith('.sty')
      );

      if (styFiles.length > 0) {
        this.logActivity(
          `       🎨 Copying ${styFiles.length} style files: ${styFiles.join(', ')}`
        );

        for (const styFile of styFiles) {
          const srcPath = path.join(TEMPLATES_PATH, styFile);
          const dstPath = path.join(workDir, styFile);
          try {
            await fs.copy(srcPath, dstPath);
          } catch (styError) {
            this.logError(`Failed to copy .sty file ${styFile}: ${styError.message}`);
            // Continue - missing .sty files might not be fatal
          }
        }
      }

      return {
        workDir: workDir,
        templatePath: workTemplatePath,
      };
    } catch (error) {
      this.logError('Failed to setup working directory:', error);
      throw new Error(`Working directory setup failed: ${error.message}`);
    }
  }

  buildPandocCommand(
    inputPath,
    outputPath,
    templatePath,
    test,
    options,
    workDir = null,
    requestMetadata = {}
  ) {
    // Start with base pandoc command
    let pandocCmd = `pandoc "${inputPath}" --template "${templatePath}"`;

    // NEW: Process lua_filters array if present
    if (test.lua_filters && Array.isArray(test.lua_filters)) {
      const filtersPath = path.join(SHARED_PATH, 'filters');
      for (const filter of test.lua_filters) {
        // Add .lua extension if not present
        const filterName = filter.endsWith('.lua') ? filter : `${filter}.lua`;
        const filterPath = path.join(filtersPath, filterName);
        pandocCmd += ` --lua-filter="${filterPath}"`;
      }
    }

    // Process pandoc_args if present
    if (test.pandoc_args && Array.isArray(test.pandoc_args)) {
      pandocCmd += ' ' + test.pandoc_args.join(' ');
    }

    // Add standard options
    pandocCmd += ` --pdf-engine=xelatex`;
    pandocCmd += ` --listings`;
    pandocCmd += ` --resource-path="/workspace/shared${workDir ? ':' + workDir : ''}"`;

    // Process metadata hierarchy: test.metadata > request.metadata > defaults
    const defaultMetadata = {
      title: 'Test Document',
      author: 'PDF Forge Test',
      date: '2025',
      toc: true,
      'toc-depth': '3',
      documentclass: 'book',
      fontsize: '11pt',
      papersize: 'a4paper',
      mainfont: 'Latin Modern Roman',
      monofont: 'Latin Modern Mono',
    };

    // Merge metadata from request level and test level
    const testMetadata = test.metadata || {};
    const variables = { ...defaultMetadata, ...requestMetadata, ...testMetadata, ...(test.variables || {}) };

    for (const [key, value] of Object.entries(variables)) {
      if (typeof value === 'boolean') {
        if (value) pandocCmd += ` --variable ${key}`;
      } else {
        pandocCmd += ` --variable ${key}="${value}"`;
      }
    }

    pandocCmd += ` -o "${outputPath}"`;

    return pandocCmd;
  }

  analyzeError(errorText) {
    const errorPatterns = [
      {
        pattern: /Missing number, treated as zero/,
        cause: 'Missing \\real{} command for table column calculations',
        solution: 'Add \\newcommand*{\\real}[1]{#1} to template',
        confidence: 0.95,
      },
      {
        pattern: /Paragraph ended before \\lstset@ was complete/,
        cause: 'Unclosed lstset block in template',
        solution: 'Add closing } to lstset configuration',
        confidence: 0.9,
      },
      {
        pattern: /Undefined control sequence.*tightlist/,
        cause: 'Missing \\tightlist command definition',
        solution: 'Add \\providecommand{\\tightlist}{...} to template',
        confidence: 0.85,
      },
    ];

    for (const errorPattern of errorPatterns) {
      if (errorPattern.pattern.test(errorText)) {
        return {
          recognized: true,
          cause: errorPattern.cause,
          solution: errorPattern.solution,
          confidence: errorPattern.confidence,
          auto_fixable: errorPattern.confidence > 0.8,
        };
      }
    }

    return {
      recognized: false,
      cause: 'Unknown error pattern',
      solution: 'Manual investigation required',
      confidence: 0.0,
      auto_fixable: false,
    };
  }

  async attemptAutoFix(templatePath, errorText, test) {
    // This would implement automatic fixes for known issues
    // For now, return placeholder
    return {
      success: false,
      attempted: true,
      reason: 'Auto-fix engine not yet implemented',
    };
  }

  async writeResults(request, results) {
    this.logActivity(`📝 Write Results: ${request.request_id}`);
    const resultPath = path.join(
      RESULTS_PATH,
      `${request.request_id}-result.json`
    );
    await fs.writeFile(resultPath, JSON.stringify(results, null, 2));

    // Write notification file if requested
    if (request.notification && request.notification.status_file) {
      const statusFile = path.join(
        STATUS_PATH,
        request.notification.status_file
      );
      await fs.writeFile(
        statusFile,
        `Test completed: ${results.overall_result}\nTimestamp: ${results.timestamp}`
      );
    }
  }

  async writeErrorResult(requestPath, error) {
    const errorResult = {
      request_id: path.basename(requestPath, '.json'),
      status: 'error',
      timestamp: new Date().toISOString(),
      error: error.message,
      overall_result: 'system_error',
    };

    const resultPath = path.join(
      RESULTS_PATH,
      `${errorResult.request_id}-error.json`
    );
    await fs.writeFile(resultPath, JSON.stringify(errorResult, null, 2));
  }

  async archiveRequest(requestPath) {
    this.logActivity(`📝 Archive Request: ${path.basename(requestPath)}`);
    const processedPath = path.join(
      REQUESTS_PATH,
      'processed',
      path.basename(requestPath)
    );
    await fs.move(requestPath, processedPath);
  }

  async onRequestModified(requestPath) {
    this.logActivity(`📝 Request modified: ${path.basename(requestPath)}`);
  }

  async onTemplateChanged(templatePath) {
    const templateName = path.basename(templatePath);
    this.logActivity(`🔧 Template changed: ${templateName}`);

    // Could trigger automatic re-testing of affected templates
  }

  async signalReady() {
    const readyFile = path.join(STATUS_PATH, 'forge-ready.txt');
    await fs.writeFile(
      readyFile,
      `PDF Forge ready at ${new Date().toISOString()}\nMonitoring: ${REQUESTS_PATH}`
    );
  }

  logActivity(message) {
    const timestamp = new Date().toISOString();
    console.log(chalk.blue(`[${timestamp}]`) + ' ' + message);

    // Also log to file
    const logFile = path.join(STATUS_PATH, 'activity.log');
    fs.appendFile(logFile, `[${timestamp}] ${message}\n`).catch(() => {});
  }

  logError(message, error) {
    const timestamp = new Date().toISOString();
    const errorMsg = error ? ` - ${error.message}` : '';
    console.error(chalk.red(`[${timestamp}] ERROR: ${message}${errorMsg}`));

    // Also log to file
    const logFile = path.join(STATUS_PATH, 'errors.log');
    fs.appendFile(
      logFile,
      `[${timestamp}] ERROR: ${message}${errorMsg}\n`
    ).catch(() => {});
  }
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log(chalk.yellow('\n🛑 Shutting down PDF Forge Monitor...'));
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log(chalk.yellow('\n🛑 Shutting down PDF Forge Monitor...'));
  process.exit(0);
});

// Start the monitor
console.log(chalk.green('🚀 Starting PDF Forge Shared Workspace Monitor...'));
new SharedWorkspaceMonitor();

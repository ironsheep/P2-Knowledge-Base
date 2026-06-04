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
 * - Request queue ensures no requests are lost (FIFO processing)
 * - Hierarchical output structure (test-runs/{request}_{ts}/{test}/)
 * - Per-test result files with complete file manifests
 * - PNG thumbnails for visual verification
 * - Startup cleanup of orphaned temp directories and old runs
 * - Recovers pending requests on restart
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const crypto = require('crypto');
const chokidar = require('chokidar');
const { execSync } = require('child_process');

// Configuration
const CONFIG = {
  RETENTION_DAYS: parseInt(process.env.FORGE_RETENTION_DAYS) || 7,
  CLEANUP_ON_STARTUP: process.env.FORGE_CLEANUP_ON_STARTUP !== 'false',
  MAX_QUEUE_SIZE: parseInt(process.env.FORGE_MAX_QUEUE) || 100,
  TEX_TIMEOUT_MS: 300000,    // 5 minutes
  PDF_TIMEOUT_MS: 600000,    // 10 minutes
  THUMBNAIL_TIMEOUT_MS: 30000, // 30 seconds
};

const SHARED_PATH = '/workspace/shared';
const REQUESTS_PATH = path.join(SHARED_PATH, 'test-requests');
const TEST_RUNS_PATH = path.join(SHARED_PATH, 'test-runs');
const TEMPLATES_PATH = path.join(SHARED_PATH, 'templates');
const FILTERS_PATH = path.join(SHARED_PATH, 'filters');
const TEST_DOCS_PATH = path.join(SHARED_PATH, 'test-documents');
const STATUS_PATH = path.join(SHARED_PATH, 'status');

/**
 * Custom error class for validation errors (recoverable)
 */
class ValidationError extends Error {
  constructor(message, details = {}) {
    super(message);
    this.name = 'ValidationError';
    this.details = details;
  }
}

/**
 * Main monitor class
 */
class SharedWorkspaceMonitor {
  constructor() {
    this.requestQueue = [];
    this.queueTimes = new Map();
    this.isProcessing = false;
    this.currentRequestId = null;
    this.currentRequestStartTime = null;
    this.recentCompleted = [];
  }

  async startup() {
    this.logActivity('🚀 PDF Forge starting...');

    // 1. Setup directories
    await this.setupEnvironment();

    // 2. Cleanup orphaned temp directories (always safe)
    if (CONFIG.CLEANUP_ON_STARTUP) {
      await this.cleanupTempDirectories();
      await this.cleanupOldRuns();
      await this.markIncompleteRuns();
    }

    // 3. Recover pending requests
    await this.recoverPendingRequests();

    // 4. Setup watchers
    this.setupWatchers();

    // 5. Signal ready
    await this.signalReady();

    // 6. Start processing queue
    this.processNextInQueue();

    this.logActivity('✅ PDF Forge ready');
  }

  async setupEnvironment() {
    try {
      await fs.ensureDir(REQUESTS_PATH);
      await fs.ensureDir(path.join(REQUESTS_PATH, 'processed'));
      await fs.ensureDir(TEST_RUNS_PATH);
      await fs.ensureDir(TEMPLATES_PATH);
      await fs.ensureDir(FILTERS_PATH);
      await fs.ensureDir(TEST_DOCS_PATH);
      await fs.ensureDir(STATUS_PATH);
    } catch (dirError) {
      console.error(chalk.red('❌ FATAL: Cannot create required directories:'));
      console.error(chalk.red(`   ${dirError.message}`));
      process.exit(1);
    }
  }

  /**
   * Cleanup orphaned temp directories from previous runs
   */
  async cleanupTempDirectories() {
    try {
      const tmpDir = '/tmp';
      const entries = await fs.readdir(tmpDir);
      const orphaned = entries.filter(e => e.startsWith('pandoc-work-'));

      if (orphaned.length > 0) {
        this.logActivity(`🧹 Cleaning ${orphaned.length} orphaned temp directories`);
        for (const dir of orphaned) {
          await fs.remove(path.join(tmpDir, dir)).catch(() => {});
        }
      }
    } catch (err) {
      this.logActivity(`⚠️ Temp cleanup skipped: ${err.message}`);
    }
  }

  /**
   * Cleanup old test runs based on retention policy
   */
  async cleanupOldRuns() {
    try {
      const cutoff = Date.now() - (CONFIG.RETENTION_DAYS * 24 * 60 * 60 * 1000);
      const runs = await fs.readdir(TEST_RUNS_PATH).catch(() => []);
      let cleaned = 0;

      for (const run of runs) {
        const runPath = path.join(TEST_RUNS_PATH, run);
        const stats = await fs.stat(runPath).catch(() => null);

        if (stats && stats.mtimeMs < cutoff) {
          await fs.remove(runPath);
          cleaned++;
        }
      }

      if (cleaned > 0) {
        this.logActivity(`🧹 Cleaned ${cleaned} test runs older than ${CONFIG.RETENTION_DAYS} days`);
      }
    } catch (err) {
      this.logActivity(`⚠️ Old runs cleanup skipped: ${err.message}`);
    }
  }

  /**
   * Mark incomplete runs from previous sessions
   */
  async markIncompleteRuns() {
    try {
      const runs = await fs.readdir(TEST_RUNS_PATH).catch(() => []);

      for (const run of runs) {
        const runPath = path.join(TEST_RUNS_PATH, run);
        const summaryPath = path.join(runPath, 'summary.json');

        const isDir = (await fs.stat(runPath).catch(() => null))?.isDirectory();
        if (isDir && !(await fs.pathExists(summaryPath))) {
          this.logActivity(`⚠️ Marking incomplete run: ${run}`);

          await fs.writeFile(summaryPath, JSON.stringify({
            request_id: run,
            status: 'incomplete',
            error: 'Daemon terminated before completion',
            marked_incomplete_at: new Date().toISOString()
          }, null, 2));
        }
      }
    } catch (err) {
      this.logActivity(`⚠️ Incomplete runs check skipped: ${err.message}`);
    }
  }

  /**
   * Recover pending requests from previous session
   */
  async recoverPendingRequests() {
    try {
      const files = await fs.readdir(REQUESTS_PATH).catch(() => []);
      const pending = files
        .filter(f => f.endsWith('.json') && !f.includes('.processed'))
        .sort();

      if (pending.length > 0) {
        this.logActivity(`📋 Recovering ${pending.length} pending request(s)`);
        for (const file of pending) {
          await this.queueRequest(path.join(REQUESTS_PATH, file));
        }
      }
    } catch (err) {
      this.logActivity(`⚠️ Request recovery skipped: ${err.message}`);
    }
  }

  setupWatchers() {
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
      .on('error', (error) => this.logError('Request watcher error:', error));

    const templateWatcher = chokidar.watch(path.join(TEMPLATES_PATH, '*.latex'));
    templateWatcher
      .on('change', (filePath) => this.onTemplateChanged(filePath))
      .on('error', (error) => this.logError('Template watcher error:', error));

    this.logActivity('📡 File watchers initialized');
  }

  /**
   * Queue a request for processing
   */
  async queueRequest(requestPath) {
    if (this.requestQueue.length >= CONFIG.MAX_QUEUE_SIZE) {
      this.logError(`Queue full (${CONFIG.MAX_QUEUE_SIZE}), rejecting request`);
      await this.writeRequestStatus(requestPath, 'rejected', {
        error: 'Queue full, try again later'
      });
      return;
    }

    const position = this.requestQueue.length + 1;
    this.requestQueue.push(requestPath);
    this.queueTimes.set(requestPath, new Date().toISOString());

    await this.updateQueueStatus();
    this.logActivity(`📥 Request queued: ${path.basename(requestPath)} (position: ${position})`);

    await this.writeRequestStatus(requestPath, 'queued', { position });
  }

  /**
   * Process next request in queue
   */
  async processNextInQueue() {
    if (this.isProcessing || this.requestQueue.length === 0) {
      return;
    }

    this.isProcessing = true;
    const requestPath = this.requestQueue.shift();
    this.queueTimes.delete(requestPath);

    try {
      await this.updateQueueStatus();
      await this.processRequest(requestPath);
    } finally {
      this.isProcessing = false;
      setImmediate(() => this.processNextInQueue());
    }
  }

  async onNewRequest(requestPath) {
    // Check if already in queue (recovery scenario)
    if (this.requestQueue.includes(requestPath)) {
      return;
    }

    await this.queueRequest(requestPath);
    this.processNextInQueue();
  }

  /**
   * Process a single request
   */
  async processRequest(requestPath) {
    const requestFile = path.basename(requestPath);
    this.logActivity(`📋 Processing: ${requestFile}`);

    try {
      await this.writeRequestStatus(requestPath, 'processing');

      const request = await this.parseRequest(requestPath);
      this.currentRequestId = request.request_id;
      this.currentRequestStartTime = new Date().toISOString();

      await this.updateQueueStatus();

      const runResult = await this.executeTestRun(request);

      // Track completed
      this.recentCompleted.push({
        request_id: request.request_id,
        result: runResult.overall_result,
        completed_at: new Date().toISOString()
      });
      if (this.recentCompleted.length > 10) {
        this.recentCompleted.shift();
      }

      await this.archiveRequest(requestPath);
      this.logActivity(`✅ Request completed: ${request.request_id}`);

    } catch (error) {
      this.logError(`Error processing ${requestFile}:`, error);
      await this.writeErrorResult(requestPath, error);
      await this.archiveRequest(requestPath);
    } finally {
      this.currentRequestId = null;
      this.currentRequestStartTime = null;
      await this.updateQueueStatus();
    }
  }

  /**
   * Parse and validate request file
   */
  async parseRequest(requestPath) {
    const filename = path.basename(requestPath);
    this.logActivity(`⏳ Parsing: ${filename}`);

    if (!(await fs.pathExists(requestPath))) {
      throw new ValidationError(`Request file not found: ${filename}`);
    }

    let content;
    try {
      content = await fs.readFile(requestPath, 'utf8');
    } catch (readError) {
      throw new ValidationError(`Cannot read request file: ${readError.message}`);
    }

    let request;
    try {
      request = JSON.parse(content);
    } catch (parseError) {
      throw new ValidationError(`Invalid JSON: ${parseError.message}`);
    }

    // Validate required fields
    if (!request.template) {
      throw new ValidationError('Missing required field: template', {
        found_fields: Object.keys(request),
        expected: '{"template": "name.latex", "tests": [...]}'
      });
    }

    if (!request.tests || !Array.isArray(request.tests) || request.tests.length === 0) {
      throw new ValidationError('Missing or empty tests array', {
        expected: '{"template": "...", "tests": [{"name": "test-name", "input": "file.md"}]}'
      });
    }

    // Validate each test has required fields
    for (let i = 0; i < request.tests.length; i++) {
      const test = request.tests[i];
      if (!test.name) {
        throw new ValidationError(`Test ${i + 1}: missing 'name' field`);
      }
      if (!test.input) {
        throw new ValidationError(`Test ${i + 1} (${test.name}): missing 'input' field`);
      }
    }

    // Set defaults
    request.request_id = request.request_id || path.basename(requestPath, '.json');
    request.timestamp = request.timestamp || new Date().toISOString();
    request.options = request.options || {};
    request.metadata = request.metadata || {};

    this.logActivity(`✓ Parsed: template=${request.template}, tests=${request.tests.length}`);
    return request;
  }

  /**
   * Execute a complete test run
   */
  async executeTestRun(request) {
    const startTime = Date.now();
    const timestamp = Date.now();
    const runId = `${request.request_id}_${timestamp}`;
    const runPath = path.join(TEST_RUNS_PATH, runId);

    // Create run directory
    await fs.ensureDir(runPath);

    // Copy original request for reference
    await fs.writeFile(
      path.join(runPath, 'request.json'),
      JSON.stringify(request, null, 2)
    );

    const summary = {
      request_id: request.request_id,
      run_id: runId,
      run_path: runPath,
      status: 'in_progress',
      started_at: new Date().toISOString(),
      completed_at: null,
      template: request.template,
      tests: {},
      overall_result: 'unknown',
      pass_count: 0,
      fail_count: 0,
      total_duration_ms: 0
    };

    try {
      // Validate template exists
      const templatePath = path.join(TEMPLATES_PATH, request.template);
      if (!(await fs.pathExists(templatePath))) {
        throw new ValidationError(`Template not found: ${request.template}`);
      }

      this.logActivity(`🔧 Testing template: ${request.template}`);

      // Process each test
      for (const test of request.tests) {
        this.logActivity(`   Running test: ${test.name}`);

        const testResult = await this.runSingleTest(
          runPath,
          templatePath,
          test,
          request.options,
          request.metadata
        );

        // Update summary
        summary.tests[test.name] = {
          result: testResult.result,
          result_file: `${test.name}/result.json`,
          has_pdf: testResult.generated_files.pdf.exists,
          has_thumbnail: testResult.generated_files.thumbnail?.exists || false,
          duration_ms: testResult.duration_ms
        };

        if (testResult.result.includes('PASS')) {
          summary.pass_count++;
        } else {
          summary.fail_count++;
        }
      }

      // Determine overall result
      if (summary.fail_count === 0) {
        summary.overall_result = 'success';
      } else if (summary.pass_count === 0) {
        summary.overall_result = 'failure';
      } else {
        summary.overall_result = 'partial_failure';
      }

      summary.status = 'completed';

    } catch (error) {
      summary.status = 'error';
      summary.overall_result = 'error';
      summary.error = error.message;
      this.logError('Test run failed:', error);
    }

    summary.completed_at = new Date().toISOString();
    summary.total_duration_ms = Date.now() - startTime;

    // Write summary
    await fs.writeFile(
      path.join(runPath, 'summary.json'),
      JSON.stringify(summary, null, 2)
    );

    this.logActivity(`📊 Run complete: ${summary.overall_result} (${summary.pass_count}/${request.tests.length} passed)`);

    return summary;
  }

  /**
   * Run a single test within a test run
   */
  async runSingleTest(runPath, templatePath, test, options, requestMetadata) {
    const testStartTime = Date.now();
    const testPath = path.join(runPath, test.name);
    await fs.ensureDir(testPath);

    const result = {
      request_id: path.basename(path.dirname(testPath)),
      test_name: test.name,
      status: 'in_progress',
      result: 'unknown',
      started_at: new Date().toISOString(),
      completed_at: null,
      duration_ms: 0,
      template: path.basename(templatePath),
      input_file: test.input,
      lua_filters: test.lua_filters || [],
      pandoc_args: test.pandoc_args || [],
      generated_files: {
        pdf: { path: null, relative_path: null, size_bytes: null, exists: false },
        tex: { path: null, relative_path: null, exists: false },
        thumbnail: { path: null, relative_path: null, exists: false }
      },
      error: null,
      error_analysis: null
    };

    let workingEnv = null;

    try {
      // Validate test input file exists
      const testDocPath = path.join(TEST_DOCS_PATH, test.input);
      if (!(await fs.pathExists(testDocPath))) {
        throw new ValidationError(`Test input file not found: ${test.input}`);
      }

      // Output paths (simple names since they're in unique directory)
      const outputPdf = path.join(testPath, 'output.pdf');
      const outputTex = path.join(testPath, 'output.tex');
      const thumbnailPath = path.join(testPath, 'thumbnail.png');

      // Setup working directory with .sty files
      workingEnv = await this.setupWorkingDirectory(templatePath, test.name);

      // Build pandoc command
      const pandocCmd = this.buildPandocCommand(
        testDocPath,
        outputPdf,
        workingEnv.templatePath,
        test,
        options,
        workingEnv.workDir,
        requestMetadata
      );

      // Generate .tex first (for debugging even if PDF fails)
      const texCmd = pandocCmd
        .replace(`-o "${outputPdf}"`, `-o "${outputTex}"`)
        .replace('--pdf-engine=xelatex', '');

      try {
        const envWithTexInputs = this.buildTexEnvironment(workingEnv.workDir);
        execSync(texCmd, {
          stdio: 'pipe',
          cwd: workingEnv.workDir,
          env: envWithTexInputs,
          timeout: CONFIG.TEX_TIMEOUT_MS
        });

        result.generated_files.tex = {
          path: outputTex,
          relative_path: `${test.name}/output.tex`,
          exists: true
        };
        this.logActivity(`       📄 .tex generated`);
      } catch (texError) {
        result.generated_files.tex.exists = false;
        this.logActivity(`       ⚠️ .tex generation failed`);
      }

      // Generate PDF. --verbose echoes the full xelatex transcript so recoverable
      // LaTeX errors (e.g. "Float(s) lost") that still exit 0 are captured, not lost.
      const envWithTexInputs = this.buildTexEnvironment(workingEnv.workDir);
      const pdfCmd = `${pandocCmd} --verbose`;
      const compileLogPath = path.join(testPath, 'output.compile.log');
      let compileOutput = '';
      try {
        // 2>&1 folds stderr into stdout; maxBuffer raised for the large --verbose log.
        compileOutput = execSync(`${pdfCmd} 2>&1`, {
          stdio: 'pipe',
          cwd: workingEnv.workDir,
          env: envWithTexInputs,
          timeout: CONFIG.PDF_TIMEOUT_MS,
          maxBuffer: 64 * 1024 * 1024
        }).toString();
      } catch (pdfError) {
        compileOutput = (pdfError.stdout ? pdfError.stdout.toString() : '')
                      + (pdfError.stderr ? pdfError.stderr.toString() : '')
                      + `\n[watch] ${pdfError.message}\n`;
        await fs.writeFile(compileLogPath, compileOutput).catch(() => {});
        result.generated_files.compile_log = {
          path: compileLogPath,
          relative_path: `${test.name}/output.compile.log`,
          exists: true
        };
        pdfError.stderr = compileOutput; // hand the outer handler the full transcript
        throw pdfError;
      }

      // Always persist the transcript on success too — recoverable LaTeX errors only
      // show here (xelatex exits 0 even when it silently drops floats/content).
      await fs.writeFile(compileLogPath, compileOutput || '(no output captured)\n').catch(() => {});
      result.generated_files.compile_log = {
        path: compileLogPath,
        relative_path: `${test.name}/output.compile.log`,
        exists: true
      };
      const DIAG_SIGNATURES = ['Float(s) lost', 'Not in outer par mode', '! LaTeX Error', '! Undefined control sequence', '! Emergency stop'];
      const diagHits = DIAG_SIGNATURES.filter(s => compileOutput.includes(s));
      if (diagHits.length > 0) {
        result.latex_warnings = diagHits;
        this.logActivity(`       ⚠️ LaTeX diagnostics (content may be MISSING): ${diagHits.join(', ')}`);
      }

      // PDF generated successfully
      const pdfStats = await fs.stat(outputPdf);
      result.generated_files.pdf = {
        path: outputPdf,
        relative_path: `${test.name}/output.pdf`,
        size_bytes: pdfStats.size,
        exists: true
      };

      result.result = '✅ PASS';
      result.status = 'completed';
      this.logActivity(`       ✅ PDF generated (${this.formatBytes(pdfStats.size)})`);

      // Generate thumbnail
      try {
        await this.generateThumbnail(outputPdf, thumbnailPath);
        result.generated_files.thumbnail = {
          path: thumbnailPath,
          relative_path: `${test.name}/thumbnail.png`,
          exists: true
        };
        this.logActivity(`       🖼️ Thumbnail generated`);
      } catch (thumbError) {
        this.logActivity(`       ⚠️ Thumbnail skipped: ${thumbError.message}`);
      }

      // Get PDF metadata
      try {
        result.pdf_info = await this.getPdfInfo(outputPdf);
      } catch (infoError) {
        // Non-fatal
      }

    } catch (error) {
      const errorOutput = error.stderr ? error.stderr.toString() : error.message;
      result.result = '❌ FAIL';
      result.status = 'completed';
      result.error = errorOutput;
      result.error_analysis = this.analyzeError(errorOutput);

      this.logActivity(`       ❌ Test failed: ${error.message.split('\n')[0]}`);
    } finally {
      // Always cleanup working directory
      if (workingEnv?.workDir) {
        await fs.remove(workingEnv.workDir).catch(() => {});
      }
    }

    result.completed_at = new Date().toISOString();
    result.duration_ms = Date.now() - testStartTime;

    // Write per-test result file
    await fs.writeFile(
      path.join(testPath, 'result.json'),
      JSON.stringify(result, null, 2)
    );

    return result;
  }

  /**
   * Setup isolated working directory with template and .sty files
   */
  async setupWorkingDirectory(templatePath, testName) {
    const uniqueId = crypto.randomBytes(4).toString('hex');
    const workDir = path.join('/tmp', `pandoc-work-${testName}-${Date.now()}-${uniqueId}`);
    await fs.ensureDir(workDir);

    // Copy template
    const templateName = path.basename(templatePath);
    const workTemplatePath = path.join(workDir, templateName);
    await fs.copy(templatePath, workTemplatePath);

    // Copy all .sty files
    try {
      const files = await fs.readdir(TEMPLATES_PATH);
      const styFiles = files.filter(f => f.endsWith('.sty'));

      for (const styFile of styFiles) {
        await fs.copy(
          path.join(TEMPLATES_PATH, styFile),
          path.join(workDir, styFile)
        ).catch(() => {});
      }
    } catch (err) {
      // Non-fatal
    }

    return {
      workDir,
      templatePath: workTemplatePath
    };
  }

  buildTexEnvironment(workDir) {
    return {
      ...process.env,
      TEXINPUTS: `${SHARED_PATH}//:${workDir}//:${process.env.TEXINPUTS || ''}`
    };
  }

  buildPandocCommand(inputPath, outputPath, templatePath, test, options, workDir, requestMetadata) {
    let cmd = `pandoc "${inputPath}" --template "${templatePath}"`;

    // Lua filters
    if (test.lua_filters && Array.isArray(test.lua_filters)) {
      for (const filter of test.lua_filters) {
        const filterName = filter.endsWith('.lua') ? filter : `${filter}.lua`;
        const filterPath = path.join(FILTERS_PATH, filterName);
        cmd += ` --lua-filter="${filterPath}"`;
      }
    }

    // Custom pandoc args
    if (test.pandoc_args && Array.isArray(test.pandoc_args)) {
      cmd += ' ' + test.pandoc_args.join(' ');
    }

    // Standard options
    cmd += ' --pdf-engine=xelatex';
    cmd += ' --listings';
    cmd += ` --resource-path="${SHARED_PATH}:${workDir}"`;

    // Metadata hierarchy: test > request > defaults
    const defaultMetadata = {
      title: 'Test Document',
      author: 'PDF Forge Test',
      date: new Date().getFullYear().toString(),
      documentclass: 'book',
      fontsize: '11pt',
      papersize: 'a4paper'
    };

    const testMetadata = test.metadata || {};
    const variables = {
      ...defaultMetadata,
      ...requestMetadata,
      ...testMetadata,
      ...(test.variables || {})
    };

    for (const [key, value] of Object.entries(variables)) {
      if (typeof value === 'boolean') {
        if (value) cmd += ` --variable ${key}`;
      } else if (value !== null && value !== undefined) {
        // Escape double quotes in values
        const escaped = String(value).replace(/"/g, '\\"');
        cmd += ` --variable ${key}="${escaped}"`;
      }
    }

    cmd += ` -o "${outputPath}"`;
    return cmd;
  }

  /**
   * Generate PNG thumbnail of first page
   */
  async generateThumbnail(pdfPath, thumbnailPath) {
    // Try pdftoppm first (usually faster)
    try {
      const basePath = thumbnailPath.replace('.png', '');
      execSync(
        `pdftoppm -png -f 1 -l 1 -scale-to 800 "${pdfPath}" "${basePath}"`,
        { stdio: 'pipe', timeout: CONFIG.THUMBNAIL_TIMEOUT_MS }
      );
      // pdftoppm adds -1.png suffix
      const generatedPath = `${basePath}-1.png`;
      if (await fs.pathExists(generatedPath)) {
        await fs.move(generatedPath, thumbnailPath, { overwrite: true });
        return;
      }
    } catch (err) {
      // Fall through to ghostscript
    }

    // Fallback to ghostscript
    execSync(
      `gs -dNOPAUSE -dBATCH -sDEVICE=png16m -r150 -dFirstPage=1 -dLastPage=1 -sOutputFile="${thumbnailPath}" "${pdfPath}"`,
      { stdio: 'pipe', timeout: CONFIG.THUMBNAIL_TIMEOUT_MS }
    );
  }

  /**
   * Get PDF metadata using pdfinfo
   */
  async getPdfInfo(pdfPath) {
    try {
      const output = execSync(`pdfinfo "${pdfPath}"`, {
        encoding: 'utf8',
        timeout: 10000
      });

      const info = {};
      for (const line of output.split('\n')) {
        const match = line.match(/^([^:]+):\s*(.+)$/);
        if (match) {
          const key = match[1].trim().toLowerCase().replace(/\s+/g, '_');
          info[key] = match[2].trim();
        }
      }
      return info;
    } catch (err) {
      return null;
    }
  }

  analyzeError(errorText) {
    const errorPatterns = [
      {
        pattern: /Missing number, treated as zero/,
        cause: 'Missing \\real{} command for table column calculations',
        solution: 'Add \\newcommand*{\\real}[1]{#1} to template',
        confidence: 0.95
      },
      {
        pattern: /Paragraph ended before \\lstset@ was complete/,
        cause: 'Unclosed lstset block in template',
        solution: 'Add closing } to lstset configuration',
        confidence: 0.9
      },
      {
        pattern: /Undefined control sequence.*tightlist/,
        cause: 'Missing \\tightlist command definition',
        solution: 'Add \\providecommand{\\tightlist}{...} to template',
        confidence: 0.85
      },
      {
        pattern: /File .* not found/,
        cause: 'Missing file reference (image, style, or include)',
        solution: 'Check that all referenced files exist in the correct location',
        confidence: 0.8
      },
      {
        pattern: /LaTeX Error: Environment .* undefined/,
        cause: 'Missing environment definition',
        solution: 'Define the environment or include the package that provides it',
        confidence: 0.85
      },
      {
        pattern: /! LaTeX Error: Missing \\begin{document}/,
        cause: 'Template structure error - document body not started',
        solution: 'Ensure template has \\begin{document} before $body$',
        confidence: 0.95
      }
    ];

    for (const ep of errorPatterns) {
      if (ep.pattern.test(errorText)) {
        return {
          recognized: true,
          cause: ep.cause,
          solution: ep.solution,
          confidence: ep.confidence,
          auto_fixable: ep.confidence > 0.8
        };
      }
    }

    return {
      recognized: false,
      cause: 'Unknown error pattern',
      solution: 'Manual investigation required - check the .tex file for details',
      confidence: 0.0,
      auto_fixable: false
    };
  }

  /**
   * Write per-request status file
   */
  async writeRequestStatus(requestPath, status, details = {}) {
    const requestId = path.basename(requestPath, '.json');
    const statusFile = path.join(STATUS_PATH, `request-${requestId}.status.json`);

    await fs.writeFile(statusFile, JSON.stringify({
      request_id: requestId,
      status: status,
      updated_at: new Date().toISOString(),
      ...details
    }, null, 2));
  }

  /**
   * Update queue status file
   */
  async updateQueueStatus() {
    const status = {
      daemon_status: 'running',
      updated_at: new Date().toISOString(),
      current_request: this.currentRequestId,
      current_request_started: this.currentRequestStartTime,
      queue_depth: this.requestQueue.length,
      queued_requests: this.requestQueue.map((p, i) => ({
        position: i + 1,
        request_id: path.basename(p, '.json'),
        queued_at: this.queueTimes.get(p)
      })),
      recent_completed: this.recentCompleted.slice(-5)
    };

    await fs.writeFile(
      path.join(STATUS_PATH, 'queue-status.json'),
      JSON.stringify(status, null, 2)
    );
  }

  async writeErrorResult(requestPath, error) {
    const requestId = path.basename(requestPath, '.json');
    const timestamp = Date.now();
    const runId = `${requestId}_${timestamp}`;
    const runPath = path.join(TEST_RUNS_PATH, runId);

    await fs.ensureDir(runPath);

    const summary = {
      request_id: requestId,
      run_id: runId,
      run_path: runPath,
      status: 'error',
      error: error.message,
      error_details: error.details || null,
      overall_result: 'system_error',
      started_at: new Date().toISOString(),
      completed_at: new Date().toISOString()
    };

    await fs.writeFile(
      path.join(runPath, 'summary.json'),
      JSON.stringify(summary, null, 2)
    );
  }

  async archiveRequest(requestPath, retries = 3) {
    const filename = path.basename(requestPath);
    const processedPath = path.join(REQUESTS_PATH, 'processed', filename);

    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        await fs.move(requestPath, processedPath, { overwrite: true });
        this.logActivity(`📦 Archived: ${filename}`);
        return;
      } catch (err) {
        if (attempt === retries) {
          this.logError(`Failed to archive after ${retries} attempts`, err);
          // Last resort: mark as processed in place
          try {
            await fs.writeFile(requestPath + '.processed', new Date().toISOString());
          } catch {}
        } else {
          await new Promise(r => setTimeout(r, 500 * attempt));
        }
      }
    }
  }

  async onTemplateChanged(templatePath) {
    const templateName = path.basename(templatePath);
    this.logActivity(`🔧 Template changed: ${templateName}`);
  }

  async signalReady() {
    const readyFile = path.join(STATUS_PATH, 'forge-ready.txt');
    await fs.writeFile(
      readyFile,
      `PDF Forge ready at ${new Date().toISOString()}\nMonitoring: ${REQUESTS_PATH}\nRetention: ${CONFIG.RETENTION_DAYS} days`
    );
  }

  formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }

  logActivity(message) {
    const timestamp = new Date().toISOString();
    console.log(chalk.blue(`[${timestamp}]`) + ' ' + message);

    const logFile = path.join(STATUS_PATH, 'activity.log');
    fs.appendFile(logFile, `[${timestamp}] ${message}\n`).catch(() => {});
  }

  logError(message, error) {
    const timestamp = new Date().toISOString();
    const errorMsg = error ? ` - ${error.message}` : '';
    console.error(chalk.red(`[${timestamp}] ERROR: ${message}${errorMsg}`));

    const logFile = path.join(STATUS_PATH, 'errors.log');
    fs.appendFile(logFile, `[${timestamp}] ERROR: ${message}${errorMsg}\n`).catch(() => {});
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

// Handle uncaught errors (keep daemon alive)
process.on('uncaughtException', (error) => {
  console.error(chalk.red(`[${new Date().toISOString()}] UNCAUGHT EXCEPTION: ${error.message}`));
  console.error(error.stack);
  // Don't exit - try to keep running
});

process.on('unhandledRejection', (reason, promise) => {
  console.error(chalk.red(`[${new Date().toISOString()}] UNHANDLED REJECTION: ${reason}`));
  // Don't exit - try to keep running
});

// Start the monitor
console.log(chalk.green('🚀 Starting PDF Forge Shared Workspace Monitor...'));
const monitor = new SharedWorkspaceMonitor();
monitor.startup().catch((error) => {
  console.error(chalk.red('Failed to start monitor:'), error);
  process.exit(1);
});

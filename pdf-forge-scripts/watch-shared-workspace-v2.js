#!/usr/bin/env node
/**
 * PDF Forge Shared Workspace Monitor v2.0
 * Enhanced archiving with timestamp-based folders to prevent overwrites
 * 
 * CHANGES:
 * - Archives use YYMMDD_HHMM format instead of YYYYMMDD
 * - Keeps metadata about each archive
 * - Automatic cleanup of old archives (configurable retention)
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

// Archive configuration
const ARCHIVE_KEEP_COUNT = 10; // Keep last 10 archives
const ARCHIVE_METADATA = true; // Create metadata file for each archive

class SharedWorkspaceMonitor {
  constructor() {
    this.isProcessing = false;
    this.setupEnvironment();
    this.setupWatchers();
    this.logActivity('🚀 PDF Forge Shared Workspace Monitor v2.0 started');
    this.logActivity(`📁 Archive retention: ${ARCHIVE_KEEP_COUNT} versions`);
    this.signalReady();
  }

  async setupEnvironment() {
    // Ensure all directories exist
    await fs.ensureDir(REQUESTS_PATH);
    await fs.ensureDir(RESULTS_PATH);
    await fs.ensureDir(TEMPLATES_PATH);
    await fs.ensureDir(TEST_DOCS_PATH);
    await fs.ensureDir(OUTPUT_PDFS_PATH);
    await fs.ensureDir(STATUS_PATH);
    await fs.ensureDir(path.join(REQUESTS_PATH, 'processed'));
  }

  setupWatchers() {
    // Watch for new test requests
    const requestWatcher = chokidar.watch(path.join(REQUESTS_PATH, '*.json'), {
      ignored: /processed/,
      persistent: true,
      awaitWriteFinish: {
        stabilityThreshold: 1000,
        pollInterval: 100
      }
    });

    requestWatcher
      .on('add', (filePath) => this.onNewRequest(filePath))
      .on('change', (filePath) => this.onRequestModified(filePath))
      .on('error', (error) => this.logError('Request watcher error:', error));

    // Watch for template changes  
    const templateWatcher = chokidar.watch(path.join(TEMPLATES_PATH, '*.latex'));
    templateWatcher
      .on('change', (filePath) => this.onTemplateChanged(filePath))
      .on('error', (error) => this.logError('Template watcher error:', error));

    this.logActivity('📡 File watchers initialized');
  }

  async onNewRequest(requestPath) {
    if (this.isProcessing) {
      this.logActivity('⏳ Request queued, processing in progress...');
      return;
    }

    try {
      this.isProcessing = true;
      const requestFile = path.basename(requestPath);
      this.logActivity(`📋 New test request: ${requestFile}`);

      const request = await this.parseRequest(requestPath);
      const results = await this.processTestRequest(request);
      
      await this.writeResults(request, results);
      await this.archiveRequestV2(requestPath, results);
      
      this.logActivity(`✅ Test request completed: ${request.request_id}`);
      
    } catch (error) {
      this.logError(`💥 CRITICAL ERROR processing ${path.basename(requestPath)}:`, error);
      await this.writeErrorResult(requestPath, error);
      
      // For parsing errors, make it very obvious and consider halting
      if (error.message.includes('Failed to parse request')) {
        console.error(chalk.red.bold('❌ TEST REJECTED ❌'));
        console.error(chalk.red.bold(`REASON: ${error.message}`));
        console.error(chalk.red(`FILE: ${path.basename(requestPath)}`));
        console.error(chalk.yellow('EXPECTED FORMAT: {"template": "name.latex", "tests": [...]}'));
        console.error('');
      }
    } finally {
      this.isProcessing = false;
    }
  }

  /**
   * Enhanced archive function with timestamp-based folders
   * Prevents overwrites and maintains metadata
   */
  async archiveRequestV2(requestPath, results) {
    try {
      // Create timestamp-based archive folder (YYMMDD_HHMM)
      const now = new Date();
      const timestamp = now.toISOString()
        .replace(/^20(\d{2})-(\d{2})-(\d{2})T(\d{2}):(\d{2}).*/, '$1$2$3_$4$5');
      
      const archivePath = path.join(REQUESTS_PATH, 'processed', timestamp);
      await fs.ensureDir(archivePath);
      
      // Move request file
      const requestName = path.basename(requestPath);
      const archivedRequestPath = path.join(archivePath, requestName);
      await fs.move(requestPath, archivedRequestPath);
      
      // Archive related test documents
      if (results && results.test_results) {
        for (const test of results.test_results) {
          if (test.document) {
            const docPath = path.join(TEST_DOCS_PATH, test.document);
            if (await fs.pathExists(docPath)) {
              const archivedDocPath = path.join(archivePath, test.document);
              await fs.copy(docPath, archivedDocPath);
            }
          }
        }
      }
      
      // Create metadata file if enabled
      if (ARCHIVE_METADATA) {
        const metadata = {
          archived_at: now.toISOString(),
          timestamp_folder: timestamp,
          request_id: results?.request_id || 'unknown',
          overall_result: results?.overall_result || 'unknown',
          tests_run: results?.test_results?.length || 0,
          failures: results?.test_results?.filter(t => t.status.includes('FAIL')).length || 0,
          performance: results?.performance || {},
          files_archived: [
            requestName,
            ...(results?.test_results?.map(t => t.document).filter(Boolean) || [])
          ]
        };
        
        const metadataPath = path.join(archivePath, 'archive_metadata.json');
        await fs.writeJSON(metadataPath, metadata, { spaces: 2 });
        
        // Also create human-readable info file
        const infoPath = path.join(archivePath, 'archive_info.txt');
        const infoContent = `Archive Information
===================
Created: ${now.toISOString()}
Folder: ${timestamp}
Request ID: ${metadata.request_id}
Result: ${metadata.overall_result}
Tests Run: ${metadata.tests_run}
Failures: ${metadata.failures}
Duration: ${metadata.performance.total_duration_ms || 0}ms

Files Archived:
${metadata.files_archived.map(f => `  - ${f}`).join('\n')}
`;
        await fs.writeFile(infoPath, infoContent);
      }
      
      this.logActivity(`📁 Archived to: processed/${timestamp}`);
      
      // Cleanup old archives
      await this.cleanupOldArchives();
      
    } catch (error) {
      this.logError('Archive v2 failed:', error);
      // Fall back to simple move
      const fallbackPath = path.join(REQUESTS_PATH, 'processed', path.basename(requestPath));
      await fs.move(requestPath, fallbackPath).catch(() => {});
    }
  }

  /**
   * Clean up old archives, keeping only ARCHIVE_KEEP_COUNT most recent
   */
  async cleanupOldArchives() {
    try {
      const processedPath = path.join(REQUESTS_PATH, 'processed');
      const entries = await fs.readdir(processedPath);
      
      // Filter and sort archives (newer format YYMMDD_HHMM sorts naturally)
      const archives = entries
        .filter(name => /^\d{6}_\d{4}$/.test(name) || /^\d{8}$/.test(name))
        .sort()
        .reverse(); // Most recent first
      
      if (archives.length > ARCHIVE_KEEP_COUNT) {
        const toRemove = archives.slice(ARCHIVE_KEEP_COUNT);
        
        for (const archive of toRemove) {
          const archivePath = path.join(processedPath, archive);
          await fs.remove(archivePath);
          this.logActivity(`🧹 Removed old archive: ${archive}`);
        }
        
        this.logActivity(`📊 Archive cleanup: kept ${ARCHIVE_KEEP_COUNT}, removed ${toRemove.length}`);
      }
    } catch (error) {
      this.logError('Archive cleanup failed (non-critical):', error);
    }
  }

  async parseRequest(requestPath) {
    try {
      const content = await fs.readFile(requestPath, 'utf8');
      const request = JSON.parse(content);
      
      // Enhanced validation with detailed error messages
      if (!request.template) {
        const availableFields = Object.keys(request).join(', ');
        throw new Error(`Missing required field: template. Found fields: [${availableFields}]. Expected format: {"template": "name.latex", "tests": [...]}`);
      }
      
      if (!request.tests && !request.documents) {
        throw new Error(`Missing required field: tests (or legacy documents array). Expected format: {"template": "name.latex", "tests": [{"name": "test-name", "document": "file.md"}]}`);
      }
      
      // Set defaults
      request.request_id = request.request_id || path.basename(requestPath, '.json');
      request.timestamp = request.timestamp || new Date().toISOString();
      request.options = request.options || {};
      request.tests = request.tests || [{ name: 'default', document: 'minimal.md' }];
      
      // Log successful parse
      this.logActivity(`✓ Request parsed: template=${request.template}, tests=${request.tests.length}`);
      
      return request;
    } catch (error) {
      if (error instanceof SyntaxError) {
        throw new Error(`Failed to parse request: Invalid JSON syntax - ${error.message}`);
      }
      throw new Error(`Failed to parse request: ${error.message}`);
    }
  }

  async processTestRequest(request) {
    const startTime = Date.now();
    const results = {
      request_id: request.request_id,
      status: 'in_progress',
      timestamp: new Date().toISOString(),
      forge_version: 'Enhanced v2.0 with Archive System',
      template: request.template,
      test_results: [],
      performance: {},
      overall_result: 'unknown'
    };

    try {
      // Validate template exists
      const templatePath = path.join(TEMPLATES_PATH, request.template);
      if (!await fs.pathExists(templatePath)) {
        throw new Error(`Template not found: ${request.template}`);
      }

      this.logActivity(`🔧 Testing template: ${request.template}`);

      // Process each test
      for (const test of request.tests) {
        this.logActivity(`   Testing: ${test.name}`);
        const testResult = await this.runSingleTest(templatePath, test, request.options);
        results.test_results.push(testResult);
      }

      // Determine overall result
      const failures = results.test_results.filter(t => t.status.includes('FAIL'));
      results.overall_result = failures.length === 0 ? 'success' : 'partial_failure';
      results.status = 'completed';

      // Performance metrics
      results.performance = {
        total_duration_ms: Date.now() - startTime,
        tests_run: request.tests.length,
        failures: failures.length
      };

      this.logActivity(`📊 Overall result: ${results.overall_result} (${failures.length} failures)`);

    } catch (error) {
      results.status = 'failed';
      results.error = error.message;
      results.overall_result = 'error';
      this.logError('Test processing failed:', error);
    }

    return results;
  }

  async runSingleTest(templatePath, test, options) {
    const testStartTime = Date.now();
    const testResult = {
      name: test.name,
      document: test.document, // Store for archiving
      status: 'unknown',
      duration_ms: 0,
      error: null,
      pdf_path: null,
      auto_fix_attempted: false
    };

    try {
      // Validate test document exists
      const testDocPath = path.join(TEST_DOCS_PATH, test.document);
      if (!await fs.pathExists(testDocPath)) {
        throw new Error(`Test document not found: ${test.document}`);
      }

      // Generate unique output name
      const outputName = `${test.name}-${Date.now()}`;
      const outputPdf = path.join(OUTPUT_PDFS_PATH, `${outputName}.pdf`);
      const outputTex = path.join(OUTPUT_PDFS_PATH, `${outputName}.tex`);
      const resultTex = path.join(RESULTS_PATH, `${outputName}.tex`);

      // Setup enhanced working directory with .sty file support
      const workingEnv = await this.setupWorkingDirectory(templatePath, test.name);

      // Build pandoc command with working directory and lua_filters
      const pandocCmd = this.buildPandocCommand(testDocPath, outputPdf, workingEnv.templatePath, test, options, workingEnv.workDir);
      
      this.logActivity(`     Running: pandoc for ${test.name}`);
      
      // Execute pandoc
      try {
        // Generate .tex for debugging
        const texCmd = pandocCmd.replace(`-o "${outputPdf}"`, `-o "${outputTex}"`).replace('--pdf-engine=xelatex', '');
        
        let texGenerated = false;
        try {
          execSync(texCmd, { stdio: 'pipe', cwd: workingEnv.workDir });
          
          // Copy .tex file to results directory for debugging access
          if (await fs.pathExists(outputTex)) {
            await fs.copy(outputTex, resultTex);
            testResult.tex_path = `${path.basename(resultTex)}`;
            testResult.tex_available = true;
            texGenerated = true;
            this.logActivity(`       📄 .tex file available: ${path.basename(resultTex)}`);
          }
        } catch (texError) {
          testResult.tex_available = false;
          testResult.tex_error = texError.stderr ? texError.stderr.toString() : texError.message;
          this.logActivity(`       ❌ .tex generation failed: ${testResult.tex_error.split('\n')[0]}`);
        }
        
        // Generate PDF
        execSync(pandocCmd, { stdio: 'pipe', cwd: workingEnv.workDir });
        
        testResult.status = '✅ PASS';
        testResult.pdf_path = `output-pdfs/${outputName}.pdf`;
        
        // Validate output
        if (await fs.pathExists(outputPdf)) {
          const stats = await fs.stat(outputPdf);
          testResult.pdf_size_bytes = stats.size;
        }
        
      } catch (pandocError) {
        const errorOutput = pandocError.stderr ? pandocError.stderr.toString() : pandocError.message;
        testResult.status = '❌ FAIL';
        testResult.error = errorOutput;
        
        // Attempt auto-fix if requested
        if (options.auto_fix_attempt) {
          const fixResult = await this.attemptAutoFix(templatePath, errorOutput, test);
          if (fixResult.success) {
            testResult.auto_fix_attempted = true;
            testResult.auto_fix_result = fixResult;
            testResult.status = '🔧 FIXED';
          }
        }
        
        // Analyze error for better reporting
        testResult.error_analysis = this.analyzeError(errorOutput);
      } finally {
        // Always cleanup working directory
        if (workingEnv.workDir) {
          await fs.remove(workingEnv.workDir).catch(() => {});
        }
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
   */
  async setupWorkingDirectory(templatePath, testName) {
    try {
      // Create unique working directory
      const workDir = path.join('/tmp', `pandoc-work-${testName}-${Date.now()}`);
      await fs.ensureDir(workDir);
      
      // Copy template to working directory
      const templateName = path.basename(templatePath);
      const workTemplatePath = path.join(workDir, templateName);
      await fs.copy(templatePath, workTemplatePath);
      
      this.logActivity(`       🔧 Working directory: ${workDir}`);
      this.logActivity(`       📄 Template copied: ${templateName}`);
      
      // Find and copy ALL .sty files from templates directory
      const templatesDirFiles = await fs.readdir(TEMPLATES_PATH);
      const styFiles = templatesDirFiles.filter(file => file.endsWith('.sty'));
      
      if (styFiles.length > 0) {
        this.logActivity(`       🎨 Copying ${styFiles.length} style files: ${styFiles.join(', ')}`);
        
        for (const styFile of styFiles) {
          const srcPath = path.join(TEMPLATES_PATH, styFile);
          const dstPath = path.join(workDir, styFile);
          await fs.copy(srcPath, dstPath);
        }
      }
      
      return {
        workDir: workDir,
        templatePath: workTemplatePath
      };
      
    } catch (error) {
      this.logError('Failed to setup working directory:', error);
      throw new Error(`Working directory setup failed: ${error.message}`);
    }
  }

  buildPandocCommand(inputPath, outputPath, templatePath, test, options, workDir = null) {
    // Start with base pandoc command
    let pandocCmd = `pandoc "${inputPath}" --template "${templatePath}"`;
    
    // Process lua_filters array if present
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
    
    // Add variables
    const variables = test.variables || {
      title: 'Test Document',
      author: 'PDF Forge Test',
      date: '2025',
      toc: true,
      'toc-depth': '3',
      documentclass: 'book',
      fontsize: '11pt',
      papersize: 'a4paper',
      mainfont: 'Latin Modern Roman',
      monofont: 'Latin Modern Mono'
    };
    
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
        confidence: 0.95
      },
      {
        pattern: /Paragraph ended before \\lstset@ was complete/,
        cause: 'Unclosed lstset block in template',
        solution: 'Add closing } to lstset configuration',
        confidence: 0.90
      },
      {
        pattern: /Undefined control sequence.*tightlist/,
        cause: 'Missing \\tightlist command definition',
        solution: 'Add \\providecommand{\\tightlist}{...} to template',
        confidence: 0.85
      }
    ];

    for (const errorPattern of errorPatterns) {
      if (errorPattern.pattern.test(errorText)) {
        return {
          recognized: true,
          cause: errorPattern.cause,
          solution: errorPattern.solution,
          confidence: errorPattern.confidence,
          auto_fixable: errorPattern.confidence > 0.8
        };
      }
    }

    return {
      recognized: false,
      cause: 'Unknown error pattern',
      solution: 'Manual investigation required',
      confidence: 0.0,
      auto_fixable: false
    };
  }

  async attemptAutoFix(templatePath, errorText, test) {
    // Placeholder for auto-fix implementation
    return {
      success: false,
      attempted: true,
      reason: 'Auto-fix engine not yet implemented'
    };
  }

  async writeResults(request, results) {
    const resultPath = path.join(RESULTS_PATH, `${request.request_id}-result.json`);
    await fs.writeFile(resultPath, JSON.stringify(results, null, 2));
    
    // Write notification file if requested
    if (request.notification && request.notification.status_file) {
      const statusFile = path.join(STATUS_PATH, request.notification.status_file);
      await fs.writeFile(statusFile, `Test completed: ${results.overall_result}\nTimestamp: ${results.timestamp}`);
    }
  }

  async writeErrorResult(requestPath, error) {
    const errorResult = {
      request_id: path.basename(requestPath, '.json'),
      status: 'error',
      timestamp: new Date().toISOString(),
      error: error.message,
      overall_result: 'system_error'
    };
    
    const resultPath = path.join(RESULTS_PATH, `${errorResult.request_id}-error.json`);
    await fs.writeFile(resultPath, JSON.stringify(errorResult, null, 2));
  }

  async onRequestModified(requestPath) {
    this.logActivity(`📝 Request modified: ${path.basename(requestPath)}`);
  }

  async onTemplateChanged(templatePath) {
    const templateName = path.basename(templatePath);
    this.logActivity(`🔧 Template changed: ${templateName}`);
  }

  async signalReady() {
    const readyFile = path.join(STATUS_PATH, 'forge-ready.txt');
    const content = `PDF Forge ready at ${new Date().toISOString()}
Monitoring: ${REQUESTS_PATH}
Archive System: v2.0 (${ARCHIVE_KEEP_COUNT} version retention)
Archive Format: YYMMDD_HHMM`;
    await fs.writeFile(readyFile, content);
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
    fs.appendFile(logFile, `[${timestamp}] ERROR: ${message}${errorMsg}\n`).catch(() => {});
  }
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log(chalk.yellow('\n🛑 Shutting down PDF Forge Monitor v2.0...'));
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log(chalk.yellow('\n🛑 Shutting down PDF Forge Monitor v2.0...'));
  process.exit(0);
});

// Start the monitor
console.log(chalk.green('🚀 Starting PDF Forge Shared Workspace Monitor v2.0...'));
console.log(chalk.green(`📁 Archive system: timestamped folders with ${ARCHIVE_KEEP_COUNT} version retention`));
new SharedWorkspaceMonitor();
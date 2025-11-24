# Doc Forge Makefile
# Professional PDF generation from Markdown + Enhanced Template Development

.PHONY: help setup process watch clean preview test shared-start shared-stop shared-status shared-monitor shared-test

# PID file for daemon management
SHARED_DAEMON_PID = /tmp/pdf-forge-shared-daemon.pid

# Default target - show help
help:
	@echo "╔══════════════════════════════════════════════════════════╗"
	@echo "║                   Doc Forge Commands                      ║"
	@echo "╚══════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "  Standard Workflow:"
	@echo "    make setup    - Initial environment setup"
	@echo "    make process  - Generate PDFs from inbox/"
	@echo "    make watch    - Auto-process on file changes"
	@echo "    make preview  - Start web server for PDF preview"
	@echo "    make clean    - Remove generated files"
	@echo "    make test     - Run validation tests"
	@echo ""
	@echo "  Enhanced Template Development (SystemD-like):"
	@echo "    make shared-start   - Start monitoring daemon (background)"
	@echo "    make shared-stop    - Stop monitoring daemon"
	@echo "    make shared-status  - Show daemon status and recent results"
	@echo "    make shared-monitor - Live view of daemon activity"
	@echo "    make shared-test    - Run template compatibility test"
	@echo ""
	@echo "  make help     - Show this help message"
	@echo ""
	@echo "Standard workflow:"
	@echo "  1. Place .md files in inbox/"
	@echo "  2. Create inbox/request.json"
	@echo "  3. Run 'make process'"
	@echo "  4. Find PDFs in outbox/"
	@echo ""
	@echo "Template development workflow:"
	@echo "  1. make shared-start    (start daemon)"
	@echo "  2. make shared-test     (run tests anytime)"
	@echo "  3. make shared-monitor  (watch activity)"
	@echo "  4. make shared-stop     (when done)"

# Setup environment
setup:
	@echo "🔧 Setting up Doc Forge environment..."
	@mkdir -p inbox outbox output logs templates scripts config
	@mkdir -p inbox/processed outbox/archive
	@touch inbox/.gitkeep outbox/.gitkeep
	@npm install --silent
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Place markdown files in inbox/"
	@echo "  2. Run 'make process' to generate PDFs"

# Start shared workspace monitoring daemon
shared-start:
	@echo "🚀 Starting PDF Forge shared workspace daemon..."
	@if [ -f "$(SHARED_DAEMON_PID)" ] && kill -0 $$(cat $(SHARED_DAEMON_PID)) 2>/dev/null; then \
		echo "⚠️  Daemon already running (PID: $$(cat $(SHARED_DAEMON_PID)))"; \
		exit 1; \
	fi
	@if [ ! -f "scripts/watch-shared-workspace.js" ]; then \
		echo "❌ Enhanced monitoring script not found!"; \
		echo "   Standard 'make watch' still available"; \
		exit 1; \
	fi
	@if [ ! -d "/workspace/shared" ]; then \
		echo "❌ Shared workspace not mounted!"; \
		echo "   Standard 'make watch' still available"; \
		exit 1; \
	fi
	@echo "📡 Starting background monitoring..."
	@nohup node scripts/watch-shared-workspace.js > /workspace/shared/status/daemon.log 2>&1 & echo $$! > $(SHARED_DAEMON_PID)
	@sleep 1
	@if kill -0 $$(cat $(SHARED_DAEMON_PID)) 2>/dev/null; then \
		echo "✅ Daemon started successfully (PID: $$(cat $(SHARED_DAEMON_PID)))"; \
		echo "   Monitor with: make shared-monitor"; \
		echo "   Test with: make shared-test"; \
	else \
		echo "❌ Failed to start daemon"; \
		rm -f $(SHARED_DAEMON_PID); \
		exit 1; \
	fi

# Stop shared workspace monitoring daemon
shared-stop:
	@echo "🛑 Stopping PDF Forge shared workspace daemon..."
	@if [ ! -f "$(SHARED_DAEMON_PID)" ]; then \
		echo "⚠️  No daemon PID file found"; \
		exit 0; \
	fi
	@PID=$$(cat $(SHARED_DAEMON_PID)) && \
	if kill -0 $$PID 2>/dev/null; then \
		kill $$PID && \
		echo "✅ Daemon stopped (PID: $$PID)"; \
	else \
		echo "⚠️  Daemon not running"; \
	fi
	@rm -f $(SHARED_DAEMON_PID)

# Show shared workspace daemon status
shared-status:
	@echo "📊 PDF Forge Shared Workspace Status"
	@echo "══════════════════════════════════════"
	@if [ -f "$(SHARED_DAEMON_PID)" ] && kill -0 $$(cat $(SHARED_DAEMON_PID)) 2>/dev/null; then \
		echo "Daemon: ✅ Running (PID: $$(cat $(SHARED_DAEMON_PID)))"; \
		echo "Uptime: $$(ps -o etime= -p $$(cat $(SHARED_DAEMON_PID)) | tr -d ' ')"; \
	else \
		echo "Daemon: ❌ Not running"; \
		rm -f $(SHARED_DAEMON_PID) 2>/dev/null; \
	fi
	@echo ""
	@if [ -d "/workspace/shared" ]; then \
		echo "Shared workspace: ✅ Available"; \
		echo "Templates: $$(ls -1 /workspace/shared/templates/*.latex 2>/dev/null | wc -l | tr -d ' ') available"; \
		echo "Pending requests: $$(ls -1 /workspace/shared/test-requests/*.json 2>/dev/null | wc -l | tr -d ' ')"; \
		echo "Completed results: $$(ls -1 /workspace/shared/test-results/*.json 2>/dev/null | wc -l | tr -d ' ')"; \
		echo "Generated PDFs: $$(ls -1 /workspace/shared/output-pdfs/*.pdf 2>/dev/null | wc -l | tr -d ' ')"; \
	else \
		echo "Shared workspace: ❌ Not available"; \
	fi
	@echo ""
	@if [ -f "/workspace/shared/status/activity.log" ]; then \
		echo "Recent activity (last 5 lines):"; \
		tail -5 /workspace/shared/status/activity.log 2>/dev/null || echo "  No recent activity"; \
	else \
		echo "Activity log: Not available"; \
	fi

# Monitor shared workspace daemon activity
shared-monitor:
	@echo "👁️  Monitoring shared workspace daemon activity..."
	@echo "   Press Ctrl+C to stop monitoring"
	@echo "════════════════════════════════════════"
	@if [ ! -f "/workspace/shared/status/activity.log" ]; then \
		echo "⚠️  Activity log not found"; \
		echo "   Start daemon first: make shared-start"; \
		exit 1; \
	fi
	@tail -f /workspace/shared/status/activity.log

# Run template compatibility tests  
shared-test:
	@echo "🧪 Running template compatibility test..."
	@if [ ! -d "/workspace/shared" ]; then \
		echo "❌ Shared workspace not available, falling back to standard tests"; \
		make test; \
		exit 0; \
	fi
	@echo "📋 Creating template test request..."
	@mkdir -p /workspace/shared/test-requests /workspace/shared/test-documents
	@echo "# Smart Pins Template Test\n\nTesting Smart Pins template with Pandoc 2.17.1.1 compatibility.\n\n## Code Example\n\n\`\`\`spin2\nPUB main()\n  wrpin(##P_HIGH_FAST, 16)\n  waitms(1000)\n\`\`\`\n\n## Table Test (\\real{} command)\n\n| Pin | Mode | Description |\n|-----|------|-------------|\n| P0  | Smart| General I/O |\n| P16 | Smart| Status LED  |" > /workspace/shared/test-documents/smart-pins-test.md
	@TIMESTAMP=$$(date +%s) && \
	echo "{\n  \"request_id\": \"smart-pins-$$TIMESTAMP\",\n  \"action\": \"test-template\",\n  \"template\": \"p2kb-smart-pins.latex\",\n  \"tests\": [\"smart-pins-test\"],\n  \"options\": {\n    \"generate_pdf\": true,\n    \"capture_tex_output\": true,\n    \"error_analysis\": true\n  }\n}" > /workspace/shared/test-requests/smart-pins-$$TIMESTAMP.json
	@echo "✅ Smart Pins test request created!"
	@if [ -f "$(SHARED_DAEMON_PID)" ] && kill -0 $$(cat $(SHARED_DAEMON_PID)) 2>/dev/null; then \
		echo "   Daemon will process automatically"; \
		echo "   Monitor: make shared-monitor"; \
	else \
		echo "   Start daemon: make shared-start"; \
	fi

# Process all documents in inbox
process:
	@echo "📄 Processing documents..."
	@echo "══════════════════════════════════════"
	@if [ ! -f "inbox/request.json" ]; then \
		echo "⚠️  No request.json found in inbox/"; \
		echo "   Creating default request..."; \
		node scripts/create-default-request.js; \
	fi
	@bash scripts/process-inbox.sh
	@echo "══════════════════════════════════════"
	@echo "✅ Processing complete!"
	@ls -la outbox/*.pdf 2>/dev/null || echo "No PDFs generated"

# Watch for changes and auto-process
watch:
	@echo "👁️  Watching inbox/ for changes..."
	@echo "   Press Ctrl+C to stop"
	@npm run watch

# Start preview server
preview:
	@echo "🌐 Starting preview server..."
	@echo "   Open http://localhost:8080"
	@npm run preview

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	@rm -rf output/*.pdf output/*.log
	@rm -rf outbox/*.pdf outbox/*.log
	@if [ -d "/workspace/shared" ]; then \
		rm -rf /workspace/shared/test-results/*.json 2>/dev/null || true; \
		rm -rf /workspace/shared/output-pdfs/*.pdf 2>/dev/null || true; \
	fi
	@echo "✅ Clean complete"

# Clean everything including dependencies
clean-all: clean
	@echo "🧹 Deep cleaning..."
	@rm -rf node_modules
	@rm -rf inbox/processed/*
	@if [ -d "/workspace/shared" ]; then \
		rm -rf /workspace/shared/test-requests/processed/* 2>/dev/null || true; \
	fi
	@make shared-stop 2>/dev/null || true
	@echo "✅ Deep clean complete"

# Run tests
test:
	@echo "🧪 Running tests..."
	@npm test
	@npm run lint
	@echo "✅ Tests complete"

# Install/update dependencies
deps:
	@echo "📦 Updating dependencies..."
	@npm update
	@echo "✅ Dependencies updated"

# Show current status (legacy - use shared-status for enhanced features)
status:
	@echo "📊 Doc Forge Status"
	@echo "══════════════════════════════════════"
	@echo "Standard Workflow:"
	@echo "  Inbox files:"
	@ls -la inbox/*.md 2>/dev/null || echo "    No markdown files"
	@echo "  Outbox files:"
	@ls -la outbox/*.pdf 2>/dev/null || echo "    No PDF files"
	@echo ""
	@echo "Environment:"
	@echo "  Node version: $$(node --version)"
	@echo "  Pandoc version: $$(pandoc --version | head -1)"
	@echo ""
	@echo "💡 Use 'make shared-status' for enhanced template development status"

# Generate sample documents for testing
sample:
	@echo "📝 Generating sample documents..."
	@node scripts/generate-samples.js
	@echo "✅ Sample documents created in inbox/"

# Archive old PDFs
archive:
	@echo "📦 Archiving old PDFs..."
	@mkdir -p outbox/archive/$$(date +%Y%m%d)
	@mv outbox/*.pdf outbox/archive/$$(date +%Y%m%d)/ 2>/dev/null || echo "No PDFs to archive"
	@echo "✅ Archive complete"
#!/bin/bash

# Doc Forge - Main Processing Script
# Processes markdown files from inbox/ to create PDFs in outbox/

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INBOX_DIR="${PDF_INPUT_DIR:-./inbox}"
OUTBOX_DIR="${PDF_OUTPUT_DIR:-./outbox}"
OUTPUT_DIR="./output"
TEMPLATES_DIR="./templates"
LOGS_DIR="./logs"

# Create log file
LOG_FILE="$LOGS_DIR/process_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$LOGS_DIR"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Print colored message
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Header
print_message "$BLUE" "╔══════════════════════════════════════════╗"
print_message "$BLUE" "║         Doc Forge PDF Generator          ║"
print_message "$BLUE" "╚══════════════════════════════════════════╝"
echo

log "Starting PDF generation process"

# Check for request file
if [ ! -f "$INBOX_DIR/request.json" ]; then
    print_message "$YELLOW" "⚠️  No request.json found in $INBOX_DIR/"
    log "No request.json found, creating default"

    # Create default request for all .md files
    node scripts/create-default-request.js

    if [ ! -f "$INBOX_DIR/request.json" ]; then
        print_message "$RED" "❌ Failed to create default request"
        exit 1
    fi
fi

# Validate request
print_message "$BLUE" "📋 Validating request..."
node scripts/validate-request.js
if [ $? -ne 0 ]; then
    print_message "$RED" "❌ Request validation failed"
    exit 1
fi

# Process documents
print_message "$BLUE" "📄 Processing documents..."
node scripts/generate-pdf.js

# Check results
if [ -f "$OUTPUT_DIR/generation.log" ]; then
    # Move PDFs to outbox
    print_message "$BLUE" "📦 Moving PDFs to outbox..."
    mv $OUTPUT_DIR/*.pdf "$OUTBOX_DIR/" 2>/dev/null || true

    # Copy generation log
    cp "$OUTPUT_DIR/generation.log" "$OUTBOX_DIR/"

    # Show results
    print_message "$GREEN" "✅ Generation complete!"
    echo
    print_message "$BLUE" "Generated files:"
    ls -lh "$OUTBOX_DIR"/*.pdf 2>/dev/null || print_message "$YELLOW" "No PDFs generated"

    # Archive processed files (optional)
    read -p "Archive processed files? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        mkdir -p "$INBOX_DIR/processed/$(date +%Y%m%d)"
        mv "$INBOX_DIR"/*.md "$INBOX_DIR/processed/$(date +%Y%m%d)/" 2>/dev/null || true
        mv "$INBOX_DIR/request.json" "$INBOX_DIR/processed/$(date +%Y%m%d)/"
        print_message "$GREEN" "✅ Files archived"
    fi
else
    print_message "$RED" "❌ Generation failed - check logs"
    exit 1
fi

log "Process completed successfully"
print_message "$GREEN" "🎉 All done!"

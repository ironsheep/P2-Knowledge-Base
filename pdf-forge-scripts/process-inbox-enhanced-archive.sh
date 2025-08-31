#!/bin/bash

# Doc Forge - Main Processing Script with Enhanced Archiving
# ENHANCED: Timestamp-based archiving to prevent overwrites
# Keeps multiple versions per day with automatic cleanup of old archives

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
ARCHIVE_KEEP_COUNT=10  # Keep last 10 archives (adjustable)

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

# Clean up old archives (keep only ARCHIVE_KEEP_COUNT most recent)
cleanup_old_archives() {
    local archive_dir="$INBOX_DIR/processed"
    if [ -d "$archive_dir" ]; then
        # Count total archives
        local total_archives=$(find "$archive_dir" -mindepth 1 -maxdepth 1 -type d | wc -l)
        
        if [ "$total_archives" -gt "$ARCHIVE_KEEP_COUNT" ]; then
            local remove_count=$((total_archives - ARCHIVE_KEEP_COUNT))
            print_message "$YELLOW" "🧹 Cleaning up old archives (removing $remove_count oldest)..."
            
            # Find and remove oldest directories
            find "$archive_dir" -mindepth 1 -maxdepth 1 -type d -print0 | \
                xargs -0 ls -dt | \
                tail -n "$remove_count" | \
                while read dir; do
                    log "Removing old archive: $dir"
                    rm -rf "$dir"
                done
        fi
    fi
}

# Header
print_message "$BLUE" "╔══════════════════════════════════════════╗"
print_message "$BLUE" "║         Doc Forge PDF Generator          ║"
print_message "$BLUE" "║      Enhanced Archive System v2.0         ║"
print_message "$BLUE" "╚══════════════════════════════════════════╝"
echo

log "Starting PDF generation process (Enhanced Archive)"

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

    # Archive processed files (enhanced with timestamp)
    read -p "Archive processed files? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Create timestamped archive directory
        # Format: YYMMDD_HHMM for better sorting and uniqueness
        ARCHIVE_DIR="$INBOX_DIR/processed/$(date +%y%m%d_%H%M)"
        mkdir -p "$ARCHIVE_DIR"
        
        # Calculate file sizes for logging
        TOTAL_SIZE=$(du -sh "$INBOX_DIR"/*.md 2>/dev/null | cut -f1 | tail -1)
        
        # Create archive metadata
        cat > "$ARCHIVE_DIR/archive_info.txt" <<EOF
Archive Created: $(date '+%Y-%m-%d %H:%M:%S')
Total Files: $(ls -1 "$INBOX_DIR"/*.md 2>/dev/null | wc -l)
Total Size: ${TOTAL_SIZE:-0}
PDF Generated: $(ls -1 "$OUTBOX_DIR"/*.pdf 2>/dev/null | wc -l) files

Files Archived:
$(ls -la "$INBOX_DIR"/*.md 2>/dev/null)
EOF
        
        # Move files to archive
        mv "$INBOX_DIR"/*.md "$ARCHIVE_DIR/" 2>/dev/null || true
        mv "$INBOX_DIR/request.json" "$ARCHIVE_DIR/"
        
        # Copy any templates used (for reference)
        if [ -d "$INBOX_DIR/templates" ]; then
            cp -r "$INBOX_DIR/templates" "$ARCHIVE_DIR/"
        fi
        
        # Copy any assets used (for completeness)
        if [ -d "$INBOX_DIR/assets" ]; then
            cp -r "$INBOX_DIR/assets" "$ARCHIVE_DIR/"
        fi
        
        print_message "$GREEN" "✅ Files archived to: $ARCHIVE_DIR"
        
        # Show archive info
        print_message "$BLUE" "📁 Archive contains:"
        ls -lh "$ARCHIVE_DIR"/*.md 2>/dev/null | head -5
        
        # Clean up old archives
        cleanup_old_archives
        
        # Show current archive status
        ARCHIVE_COUNT=$(find "$INBOX_DIR/processed" -mindepth 1 -maxdepth 1 -type d | wc -l)
        print_message "$BLUE" "📊 Archive status: $ARCHIVE_COUNT versions kept (max: $ARCHIVE_KEEP_COUNT)"
    fi
else
    print_message "$RED" "❌ Generation failed - check logs"
    exit 1
fi

log "Process completed successfully"
print_message "$GREEN" "🎉 All done!"
#!/bin/bash
# OBEX Download Helper Script v2.0
# Automatically retrieves YAML metadata and downloads OBEX object
# Usage: bash download-helper.sh <object_id>

set -e  # Exit on any error

# Parameter
OBJECT_ID=$1

# Validate parameter
if [ -z "$OBJECT_ID" ]; then
    echo "Usage: bash download-helper.sh <object_id>"
    echo "Example: bash download-helper.sh 2817"
    exit 1
fi

echo "🔍 OBEX Download Helper v2.0"
echo "📦 Object ID: $OBJECT_ID"

# Check if fetch script exists
if [ ! -f ".p2kb-cache/fetch-kb-file.sh" ]; then
    echo "❌ Error: fetch-kb-file.sh not found in .p2kb-cache/"
    echo "Please run the P2 Knowledge Base setup first."
    exit 1
fi

# Step 1: Fetch the object's YAML and capture its contents
echo "📄 Fetching object metadata..."
YAML_PATH="engineering/knowledge-base/P2/community/obex/objects/${OBJECT_ID}.yaml"
YAML_CONTENT=$(bash .p2kb-cache/fetch-kb-file.sh "$YAML_PATH" 2>/dev/null)

if [ -z "$YAML_CONTENT" ]; then
    echo "❌ Error: Could not fetch YAML for object ${OBJECT_ID}"
    echo "Please verify the object ID is correct."
    exit 1
fi

# Step 2: Parse title from the captured YAML content
TITLE=$(echo "$YAML_CONTENT" | grep "^  title:" | cut -d: -f2- | xargs)

if [ -z "$TITLE" ]; then
    echo "❌ Error: Could not parse title from YAML"
    exit 1
fi

echo "📝 Title: $TITLE"

# Step 3: Generate slug from title  
TITLE_SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-\|-$//g')
echo "📁 Directory slug: $TITLE_SLUG"

# Step 4: Get download URL from YAML (or construct it)
DOWNLOAD_URL=$(echo "$YAML_CONTENT" | grep "download_direct:" | sed 's/.*download_direct: *//')
if [ -z "$DOWNLOAD_URL" ]; then
    # Fallback: construct URL
    DOWNLOAD_URL="https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB${OBJECT_ID}"
fi

# Step 5: Create directory and download
echo "📁 Creating directory: OBEX/${TITLE_SLUG}/"
mkdir -p "OBEX/${TITLE_SLUG}"
cd "OBEX/${TITLE_SLUG}"

# Download the ZIP file
ZIP_FILE="OB${OBJECT_ID}.zip"
echo "⬇️  Downloading from OBEX..."
if command -v curl &>/dev/null; then
    curl -L -o "$ZIP_FILE" "$DOWNLOAD_URL"
elif command -v wget &>/dev/null; then
    wget -O "$ZIP_FILE" "$DOWNLOAD_URL"
else
    echo "❌ Error: Neither curl nor wget found"
    exit 1
fi

# Check if download was successful
if [ ! -f "$ZIP_FILE" ] || [ ! -s "$ZIP_FILE" ]; then
    echo "❌ Error: Download failed or file is empty"
    exit 1
fi

echo "✅ Downloaded: ${ZIP_FILE} ($(ls -lh ${ZIP_FILE} | awk '{print $5}'))"

# Extract the ZIP file
echo "📦 Extracting ${ZIP_FILE}..."
unzip -q "$ZIP_FILE"

# Check for nested ZIPs (common in OBEX)
NESTED_ZIPS=$(find . -name "*.zip" -not -name "$ZIP_FILE" 2>/dev/null || true)
if [ ! -z "$NESTED_ZIPS" ]; then
    echo "📦 Found nested ZIP files, extracting..."
    for nested in $NESTED_ZIPS; do
        echo "   Extracting: $(basename $nested)"
        unzip -q "$nested" -d "$(basename $nested .zip)"
    done
fi

# List extracted contents
echo ""
echo "📋 Extracted contents:"
ls -la

echo ""
echo "✅ OBEX object ${OBJECT_ID} successfully downloaded and extracted"
echo "📍 Location: $(pwd)"
echo "📝 Object: $TITLE"
echo ""
echo "🛑 STOPPING HERE - Ready for user inspection"

# Output the final path to stdout for Claude to capture
echo "$(pwd)"
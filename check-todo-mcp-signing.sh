#!/bin/bash

# Script to check code signing status of todo-mcp executables
# Iterates through all found todo-mcp binaries and checks their signing

echo "Checking code signing for todo-mcp executables..."
echo "================================================="

# Array of all todo-mcp executable paths
files=(
    "/Users/stephen/container-tools/opt/todo-mcp/bin/todo-mcp"
    "/Users/stephen/container-tools-PRIOR0/opt/todo-mcp/bin/todo-mcp"
    "/Users/stephen/container-tools-PRIOR1/opt/todo-mcp/bin/todo-mcp"
    "/Users/stephen/container-tools-PRIOR2/opt/todo-mcp/bin/todo-mcp"
    "/Users/stephen/container-tools/opt/todo-mcp/bin/platforms/todo-mcp-v0.6.8.2-darwin-amd64"
    "/Users/stephen/container-tools/opt/todo-mcp/bin/platforms/todo-mcp-v0.6.8.2-darwin-arm64"
    "/Users/stephen/container-tools-PRIOR0/opt/todo-mcp/bin/platforms/todo-mcp-darwin-amd64"
    "/Users/stephen/container-tools-PRIOR0/opt/todo-mcp/bin/platforms/todo-mcp-darwin-arm64"
    "/Users/stephen/container-tools-PRIOR1/opt/todo-mcp/bin/platforms/todo-mcp-v0.6.8-darwin-amd64"
    "/Users/stephen/container-tools-PRIOR1/opt/todo-mcp/bin/platforms/todo-mcp-v0.6.8-darwin-arm64"
    "/Users/stephen/container-tools-PRIOR2/opt/todo-mcp/bin/platforms/todo-mcp-v0.6.8.1-darwin-arm64"
    "/Users/stephen/container-tools-PRIOR2/opt/todo-mcp/bin/platforms/todo-mcp-v0.6.8.1-darwin-amd64"
)

# Iterate through each file and check signing
for file in "${files[@]}"; do
    echo
    echo "Checking: $file"
    echo "----------------------------------------"
    
    # Check if file exists
    if [[ ! -f "$file" ]]; then
        echo "❌ File not found"
        continue
    fi
    
    # Check code signing
    codesign -dv --verbose=4 "$file" 2>&1 | head -10
    
    # Check signing status more concisely
    if codesign -v "$file" 2>/dev/null; then
        echo "✅ SIGNED"
    else
        echo "❌ NOT SIGNED or INVALID SIGNATURE"
    fi
done

echo
echo "================================================="
echo "Code signing check complete."
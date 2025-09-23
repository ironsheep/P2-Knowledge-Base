#!/usr/bin/env bash
# Manifest Linkage Verification Script for P2 Knowledge Base
#
# This script runs the Python linkage verifier and can be used:
# - As a pre-commit hook
# - In CI/CD pipelines
# - For manual verification before releases
#
# Usage:
#   ./verify-manifest-linkages.sh [--verbose] [--ci]
#
# Exit codes:
#   0 - All linkages valid
#   1 - Broken linkages found
#   2 - Script error

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Find the repository root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

# Change to repo root
cd "$REPO_ROOT"

echo "============================================"
echo "P2 Knowledge Base - Linkage Verification"
echo "Repository: $REPO_ROOT"
echo "============================================"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed${NC}"
    exit 2
fi

# Check if PyYAML is installed
if ! python3 -c "import yaml" 2>/dev/null; then
    echo -e "${YELLOW}Warning: PyYAML not installed. Installing...${NC}"
    pip3 install pyyaml || {
        echo -e "${RED}Error: Failed to install PyYAML${NC}"
        echo "Please install manually: pip3 install pyyaml"
        exit 2
    }
fi

# Run the verification script
python3 "$SCRIPT_DIR/verify-manifest-linkages.py" "$@"
RESULT=$?

# Handle results
if [ $RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ Linkage verification passed!${NC}"
elif [ $RESULT -eq 1 ]; then
    echo -e "${RED}✗ Linkage verification failed - broken links found${NC}"
    echo "Please fix the issues before committing/releasing"
else
    echo -e "${RED}✗ Verification script error${NC}"
fi

exit $RESULT
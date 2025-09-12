#!/bin/bash
# Enhanced OBEX discovery script with P2 focus

echo "🔍 Checking Python dependencies..."
python3 -c "import requests, bs4, yaml; print('Dependencies OK')" || {
    echo "❌ Missing dependencies. Install with: pip3 install requests beautifulsoup4 pyyaml"
    exit 1
}

echo "🚀 Starting OBEX discovery..."
echo "📋 Categories: spin2 pasm2 propeller-2"

# Enhanced discovery with additional P2 categories and Stephen M Moraco author search
python3 obex_discovery.py --categories spin2 pasm2 propeller-2 --delay ${1:-1.5}
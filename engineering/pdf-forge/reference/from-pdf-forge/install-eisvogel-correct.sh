#!/bin/bash
# Correct Eisvogel installation script
# The file extension changed from .tex to .latex!

echo "=== Installing Eisvogel (with CORRECT URL) ==="
echo ""

# Method 1: Try the raw GitHub URL with correct extension
echo "Method 1: Trying raw GitHub URL..."
wget https://raw.githubusercontent.com/Wandmalfarbe/pandoc-latex-template/master/eisvogel.latex -O /workspace/templates/eisvogel.latex

if [ -f /workspace/templates/eisvogel.latex ]; then
    echo "✅ Eisvogel downloaded successfully!"
    echo "   Size: $(wc -l /workspace/templates/eisvogel.latex | cut -d' ' -f1) lines"
    
    # Try to copy to Pandoc directory (might need sudo)
    cp /workspace/templates/eisvogel.latex /home/node/.local/share/pandoc/templates/ 2>/dev/null && \
        echo "✅ Copied to Pandoc user directory" || \
        echo "⚠️  Couldn't copy to Pandoc directory, but template is in /workspace/templates/"
else
    echo "❌ Method 1 failed, trying release download..."
    
    # Method 2: Download from releases page
    echo ""
    echo "Method 2: Downloading from latest release..."
    
    # Get latest release
    wget https://github.com/Wandmalfarbe/pandoc-latex-template/releases/latest/download/Eisvogel.tar.gz -O /tmp/eisvogel.tar.gz
    
    if [ -f /tmp/eisvogel.tar.gz ]; then
        echo "✅ Release archive downloaded"
        
        # Extract
        cd /tmp
        tar -xzf eisvogel.tar.gz
        
        # Find and copy the template
        find /tmp -name "eisvogel.latex" -type f -exec cp {} /workspace/templates/ \;
        
        if [ -f /workspace/templates/eisvogel.latex ]; then
            echo "✅ Eisvogel extracted and installed!"
        else
            echo "❌ Couldn't find eisvogel.latex in archive"
        fi
        
        # Cleanup
        rm -rf /tmp/eisvogel.tar.gz /tmp/Eisvogel*
    else
        echo "❌ Couldn't download from releases either"
    fi
fi

echo ""
echo "=== Testing Eisvogel ==="
if [ -f /workspace/templates/eisvogel.latex ]; then
    echo "Creating test document..."
    cat > /workspace/test-eisvogel.md << 'EOF'
---
title: "Eisvogel Test"
author: "PDFForge"
titlepage: true
titlepage-color: "1F4788"
titlepage-text-color: "FFFFFF"
toc: true
book: true
---

# Chapter 1

This should start on a new page with Eisvogel.

# Chapter 2

This should also start on a new page.
EOF

    echo "Generating PDF with Eisvogel..."
    pandoc /workspace/test-eisvogel.md \
        --template=/workspace/templates/eisvogel.latex \
        --pdf-engine=xelatex \
        -o /workspace/test-eisvogel.pdf 2>&1
    
    if [ -f /workspace/test-eisvogel.pdf ]; then
        echo "✅ Eisvogel works! PDF generated successfully"
        echo "   Size: $(ls -lh /workspace/test-eisvogel.pdf | awk '{print $5}')"
    else
        echo "❌ PDF generation with Eisvogel failed"
    fi
else
    echo "❌ Eisvogel template not found, cannot test"
fi

echo ""
echo "=== Summary ==="
ls -la /workspace/templates/*.latex 2>/dev/null || echo "No templates found"
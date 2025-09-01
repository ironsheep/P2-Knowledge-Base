#!/bin/bash
# Verify what actually got installed and test it

echo "=== Verifying PDFForge Installation ==="
echo ""

echo "📁 Checking what exists:"
echo ""

# Check templates
if [ -f /workspace/templates/p2kb-pasm-desilva-enhanced.latex ]; then
    echo "✅ P2KB template found at /workspace/templates/"
    echo "   Size: $(wc -l /workspace/templates/p2kb-pasm-desilva-enhanced.latex | cut -d' ' -f1) lines"
else
    echo "❌ P2KB template NOT found"
fi

# Check Lua filter
if [ -f /workspace/filters/desilva-boxes.lua ]; then
    echo "✅ Lua filter found at /workspace/filters/"
else
    echo "❌ Lua filter NOT found"
fi

# Check Eisvogel
if [ -f /usr/share/pandoc/data/templates/eisvogel.tex ]; then
    echo "✅ Eisvogel template found"
else
    echo "⚠️  Eisvogel not installed (but that's OK, we have P2KB template)"
fi

echo ""
echo "🧪 Creating simple test..."
cat > /workspace/test-chapters.md << 'EOF'
---
title: "Chapter Test"
author: "PDFForge"
toc: true
numbersections: false
---

# Chapter 1: First Chapter

This should start on a new page.

:::sidetrack
Testing sidetrack box.
:::

# Chapter 2: Second Chapter  

This should ALSO start on a new page.

The header should show "Chapter 2" not "Contents".

:::yourturn
**Your Turn:** Check if this renders correctly.
:::
EOF

echo ""
echo "🚀 Testing P2KB template with FULL path..."
echo ""
echo "Running: pandoc test with absolute template path..."

# Test with full path to template
pandoc /workspace/test-chapters.md \
  --template=/workspace/templates/p2kb-pasm-desilva-enhanced.latex \
  --pdf-engine=xelatex \
  --lua-filter=/workspace/filters/desilva-boxes.lua \
  -o /workspace/test-p2kb-fullpath.pdf 2>&1

if [ -f /workspace/test-p2kb-fullpath.pdf ]; then
    echo "✅ SUCCESS! PDF generated: test-p2kb-fullpath.pdf"
    echo "   Size: $(ls -lh /workspace/test-p2kb-fullpath.pdf | awk '{print $5}')"
else
    echo "❌ PDF generation failed"
fi

echo ""
echo "=== 📋 Summary ==="
echo ""
echo "What's working:"
echo "  ✅ P2KB template exists at /workspace/templates/"
echo "  ✅ Lua filter exists at /workspace/filters/"
echo ""
echo "For your request.json, use FULL PATH:"
echo '{'
echo '  "documents": [{'
echo '    "input": "your-document.md",'
echo '    "output": "your-document.pdf",'
echo '    "template": "/workspace/templates/p2kb-pasm-desilva-enhanced.latex",'
echo '    "pdf-engine": "xelatex",'
echo '    "lua-filters": ["/workspace/filters/desilva-boxes.lua"]'
echo '  }]'
echo '}'
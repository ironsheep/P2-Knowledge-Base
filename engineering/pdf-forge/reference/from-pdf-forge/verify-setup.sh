#!/bin/bash
# Verify Enhanced PDFForge Setup
# Run AFTER manual-install-now.sh to confirm everything works

echo "=== PDFForge Enhancement Verification ==="
echo ""

# Check what's installed
echo "📋 Checking installations..."
echo ""

echo "1. Eisvogel template:"
if [ -f /usr/share/pandoc/data/templates/eisvogel.tex ]; then
    echo "   ✅ Eisvogel installed"
else
    echo "   ❌ Eisvogel NOT found"
fi

echo "2. De Silva template:"
if [ -f /usr/share/pandoc/data/templates/desilva.tex ]; then
    echo "   ✅ De Silva template installed"
else
    echo "   ❌ De Silva template NOT found"
fi

echo "3. Lua filter:"
if [ -f /workspace/filters/desilva-boxes.lua ]; then
    echo "   ✅ Lua filter installed"
else
    echo "   ❌ Lua filter NOT found"
fi

echo "4. Python filters:"
echo -n "   pandoc-latex-environment: "
if pip3 show pandoc-latex-environment > /dev/null 2>&1; then
    echo "✅"
else
    echo "❌ CRITICAL - this is needed for :::boxes!"
fi

echo -n "   pandoc-xnos: "
if pip3 show pandoc-xnos > /dev/null 2>&1; then
    echo "✅"
else
    echo "⚠️  Optional but recommended"
fi

echo ""
echo "📝 Creating test markdown..."
cat > /workspace/test-verify.md << 'EOF'
---
title: "PDFForge Enhancement Test"
author: "Verification Script"
date: "2025-08-23"
toc: true
numbersections: false
---

# Chapter 1: Testing Features

This chapter should start on a new page.

## Code Test

```pasm2
    mov     x, #42
    add     x, #1
```

:::sidetrack
This is a sidetrack box. Gray with dashed border.
:::

:::yourturn
**Your Turn:** Make x equal to 100
:::

# Chapter 2: Verification

This should also start on a new page.

The header should say "Chapter 2" not "Contents".

:::missing
CORDIC operations documentation needed here.
:::

Chapter numbering should be correct (not 0.4).
EOF

echo ""
echo "🧪 Running generation tests..."
echo ""

# Test 1: Basic Pandoc (should work even without enhancements)
echo "Test 1: Basic Pandoc..."
pandoc /workspace/test-verify.md \
    --pdf-engine=xelatex \
    -o /workspace/test1-basic.pdf 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ Basic PDF generation works"
else
    echo "   ❌ Basic PDF generation failed"
fi

# Test 2: Eisvogel template
echo "Test 2: Eisvogel template..."
pandoc /workspace/test-verify.md \
    --template=eisvogel \
    --pdf-engine=xelatex \
    --variable=book:true \
    -o /workspace/test2-eisvogel.pdf 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ Eisvogel template works"
else
    echo "   ❌ Eisvogel template failed"
fi

# Test 3: De Silva template with Lua filter
echo "Test 3: De Silva custom template..."
pandoc /workspace/test-verify.md \
    --template=desilva \
    --pdf-engine=xelatex \
    --lua-filter=/workspace/filters/desilva-boxes.lua \
    -o /workspace/test3-desilva.pdf 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ De Silva template works"
else
    echo "   ❌ De Silva template failed"
fi

# Test 4: With pandoc-latex-environment filter
echo "Test 4: With pandoc-latex-environment..."
pandoc /workspace/test-verify.md \
    --template=eisvogel \
    --pdf-engine=xelatex \
    --filter=pandoc-latex-environment \
    -o /workspace/test4-filter.pdf 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ pandoc-latex-environment filter works"
else
    echo "   ⚠️  pandoc-latex-environment not working (may not be installed)"
fi

echo ""
echo "=== Verification Complete ==="
echo ""
echo "📊 Summary:"
ls -lh /workspace/test*.pdf 2>/dev/null | awk '{print "   " $9 " (" $5 ")"}'
echo ""
echo "🎯 For your De Silva manual, use:"
echo "   • Template: eisvogel (with book:true)"
echo "   • Or: desilva (custom template)"
echo "   • Filter: pandoc-latex-environment or Lua filter"
echo "   • Engine: xelatex (already your default)"
echo ""
echo "📝 Your request.json should work if it uses:"
echo '   "template": "eisvogel" or "template": "desilva"'
echo '   "pdf-engine": "xelatex"'
echo '   "filters": ["pandoc-latex-environment"]'
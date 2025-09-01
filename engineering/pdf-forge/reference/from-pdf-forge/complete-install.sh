#!/bin/bash
# Complete PDFForge Installation - All Missing Pieces
# Run this ON PDFForge to finish the setup

echo "=== 🔧 PDFForge Complete Installation ==="
echo "Starting at: $(date)"
echo ""

# 1. Install Eisvogel with CORRECT filename
echo "📥 Installing Eisvogel template (correct URL)..."
mkdir -p /workspace/templates

# Try the corrected raw URL
wget -q https://raw.githubusercontent.com/Wandmalfarbe/pandoc-latex-template/master/eisvogel.latex \
     -O /workspace/templates/eisvogel.latex

if [ -f /workspace/templates/eisvogel.latex ] && [ -s /workspace/templates/eisvogel.latex ]; then
    echo "✅ Eisvogel downloaded successfully"
    echo "   Size: $(wc -l /workspace/templates/eisvogel.latex | cut -d' ' -f1) lines"
else
    echo "⚠️  Direct download failed, trying release archive..."
    
    # Try downloading from releases
    cd /tmp
    wget -q https://github.com/Wandmalfarbe/pandoc-latex-template/releases/download/v2.4.2/Eisvogel-2.4.2.tar.gz
    
    if [ -f Eisvogel-2.4.2.tar.gz ]; then
        tar -xzf Eisvogel-2.4.2.tar.gz
        cp Eisvogel-*/eisvogel.latex /workspace/templates/ 2>/dev/null || \
        cp eisvogel.latex /workspace/templates/ 2>/dev/null
        
        if [ -f /workspace/templates/eisvogel.latex ]; then
            echo "✅ Eisvogel installed from release archive"
        else
            echo "❌ Still couldn't install Eisvogel"
        fi
        rm -rf Eisvogel*
    fi
    cd /workspace
fi

# 2. Install critical Python filter without building psutil
echo ""
echo "📦 Installing pandoc-latex-environment (critical for :::boxes)..."

# Try installing just the critical filter without all the xnos dependencies
pip3 install --user pandoc-latex-environment 2>/dev/null

# Check if it worked
if python3 -c "import pandoc_latex_environment" 2>/dev/null; then
    echo "✅ pandoc-latex-environment installed"
else
    echo "⚠️  Python filter not installed, but Lua filter will work instead"
fi

# 3. Verify our P2KB template is still there
echo ""
echo "📋 Verifying P2KB template..."
if [ -f /workspace/templates/p2kb-pasm-desilva-enhanced.latex ]; then
    echo "✅ P2KB template exists"
else
    echo "❌ P2KB template missing! Creating it now..."
    
    cat > /workspace/templates/p2kb-pasm-desilva-enhanced.latex << 'TEMPLATE_EOF'
% P2KB De Silva Enhanced Template - Fixes all three problems
\documentclass[11pt,openany]{book}

% Core packages
\usepackage[margin=1in]{geometry}
\usepackage{xcolor}
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\usepackage{fancyhdr}
\usepackage{hyperref}
\usepackage{listings}
\usepackage{fontspec}
\usepackage{etoolbox}

% Fonts
\setmainfont{Liberation Serif}
\setmonofont{Fira Code}

% Colors
\definecolor{codegray}{HTML}{F5F5F5}
\definecolor{yourturncolor}{HTML}{E6F3FF}

% FIX #1: Force chapters to new pages
\preto{\chapter}{\clearpage}

% FIX #2: Headers show chapter names not "Contents"
\pagestyle{fancy}
\fancyhead[L]{\leftmark}
\fancyhead[R]{\thepage}
\renewcommand{\chaptermark}[1]{\markboth{Chapter \thechapter: #1}{}}

% FIX #3: No section numbering (prevents 0.4 weirdness)
\setcounter{secnumdepth}{-1}

% De Silva boxes
\newtcolorbox{sidetrack}{
  enhanced,
  colback=gray!10,
  colframe=gray!50,
  borderline={1pt}{0pt}{gray!50,dashed},
  title={\textbf{Sidetrack}},
  breakable
}

\newtcolorbox{yourturn}{
  colback=yourturncolor,
  colframe=blue!30,
  title={\textbf{Your Turn}},
  breakable
}

% Code settings
\lstset{
  basicstyle=\ttfamily,
  backgroundcolor=\color{codegray},
  breaklines=true,
  frame=none
}

% Document start
\title{$title$}
\author{$author$}
\date{$date$}

\begin{document}

$if(title)$
\maketitle
$endif$

$if(toc)$
\tableofcontents
\clearpage
$endif$

$body$

\end{document}
TEMPLATE_EOF
    echo "✅ P2KB template created"
fi

# 4. Verify Lua filter
echo ""
echo "🔧 Verifying Lua filter..."
if [ -f /workspace/filters/desilva-boxes.lua ]; then
    echo "✅ Lua filter exists"
else
    echo "⚠️  Lua filter missing, creating..."
    mkdir -p /workspace/filters
    cat > /workspace/filters/desilva-boxes.lua << 'LUA_EOF'
function Div(el)
  local boxTypes = {sidetrack=true, yourturn=true, missing=true, chapterend=true}
  if el.classes[1] and boxTypes[el.classes[1]] then
    return {
      pandoc.RawBlock('latex', '\\begin{' .. el.classes[1] .. '}'),
      pandoc.Div(el.content),
      pandoc.RawBlock('latex', '\\end{' .. el.classes[1] .. '}')
    }
  end
  return el
end
LUA_EOF
    echo "✅ Lua filter created"
fi

# 5. Create comprehensive test
echo ""
echo "📝 Creating comprehensive test document..."
cat > /workspace/test-all-fixes.md << 'TEST_EOF'
---
title: "PDFForge Template Test - All Fixes"
author: "P2 Knowledge Base"
date: "August 2025"
toc: true
numbersections: false
---

# Chapter 1: Testing New Page Fix

This chapter should start on a NEW PAGE after the table of contents.

If it doesn't, the chapter page fix isn't working.

## Section 1.1

This section should NOT be numbered 0.4 or anything weird.

```pasm2
    mov     x, #42    ' Load value
    add     x, #1     ' Increment
```

:::sidetrack
**Sidetrack Test**: This should have a gray background with dashed border.

If this renders as plain text, the Lua filter isn't working.
:::

# Chapter 2: Testing Header Fix

Look at the page header above. It should say "Chapter 2: Testing Header Fix" not "Contents"!

If it says "Contents", the header fix isn't working.

:::yourturn
**Your Turn**: Check these three things:
1. Did Chapter 1 start on a new page?
2. Does this header say "Chapter 2" not "Contents"?
3. Are sections numbered correctly (not 0.4)?
:::

# Chapter 3: Final Verification

This is chapter 3. The header should update to show "Chapter 3: Final Verification".

All three of your problems should now be fixed:
- ✅ Chapters start on new pages
- ✅ Headers show chapter names
- ✅ Numbering is correct
TEST_EOF

echo ""
echo "=== 🧪 TESTING TIME ==="
echo ""

# Test 1: P2KB template
echo "Test 1: P2KB template with all fixes..."
pandoc /workspace/test-all-fixes.md \
    --template=/workspace/templates/p2kb-pasm-desilva-enhanced.latex \
    --pdf-engine=xelatex \
    --lua-filter=/workspace/filters/desilva-boxes.lua \
    -o /workspace/test-p2kb-fixes.pdf 2>&1

if [ -f /workspace/test-p2kb-fixes.pdf ]; then
    echo "✅ P2KB PDF generated: test-p2kb-fixes.pdf"
    echo "   Check this PDF for all three fixes!"
else
    echo "❌ P2KB PDF generation failed"
fi

# Test 2: Eisvogel (if it installed)
if [ -f /workspace/templates/eisvogel.latex ]; then
    echo ""
    echo "Test 2: Eisvogel template..."
    pandoc /workspace/test-all-fixes.md \
        --template=/workspace/templates/eisvogel.latex \
        --pdf-engine=xelatex \
        --variable=book:true \
        --lua-filter=/workspace/filters/desilva-boxes.lua \
        -o /workspace/test-eisvogel-fixes.pdf 2>&1
    
    if [ -f /workspace/test-eisvogel-fixes.pdf ]; then
        echo "✅ Eisvogel PDF generated: test-eisvogel-fixes.pdf"
    else
        echo "❌ Eisvogel PDF generation failed"
    fi
fi

echo ""
echo "=== 📊 FINAL STATUS ==="
echo ""
echo "Templates available:"
ls -la /workspace/templates/*.latex 2>/dev/null | awk '{print "  • " $9 " (" $5 " bytes)"}'

echo ""
echo "Test PDFs generated:"
ls -la /workspace/test*.pdf 2>/dev/null | awk '{print "  • " $9 " (" $5 " bytes)"}'

echo ""
echo "=== 🎯 FOR YOUR REQUEST.JSON ==="
echo ""
cat << 'JSON_EOF'
{
  "documents": [{
    "input": "your-document.md",
    "output": "your-document.pdf",
    "template": "/workspace/templates/p2kb-pasm-desilva-enhanced.latex",
    "pdf-engine": "xelatex",
    "lua-filters": ["/workspace/filters/desilva-boxes.lua"],
    "variables": {
      "toc": true,
      "numbersections": false
    }
  }]
}
JSON_EOF

echo ""
echo "=== ✅ Installation Complete! ==="
echo "Please check the test PDFs to verify all three problems are fixed!"
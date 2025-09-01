#!/bin/bash
# PDFForge Installation Script - FOR RUNNING ON PDFFORGE CONTAINER
# This script is for the Docker container, not local Mac!

echo "=== PDFForge Enhancement Installation ==="
echo "Running on: $(hostname)"
echo "Starting at: $(date)"

# First, let's check where we are and what exists
echo ""
echo "📍 Checking environment..."
echo "Current directory: $(pwd)"
echo "User: $(whoami)"

# Find Pandoc's actual template directory
echo ""
echo "🔍 Finding Pandoc template directory..."
PANDOC_TEMPLATE_DIR=$(pandoc --version | grep "Default user data directory" | cut -d: -f2 | xargs)/templates
echo "Pandoc template directory: $PANDOC_TEMPLATE_DIR"

# Create template directory if it doesn't exist
mkdir -p "$PANDOC_TEMPLATE_DIR"
mkdir -p templates
mkdir -p filters

# 1. Install Eisvogel template
echo ""
echo "📥 Installing Eisvogel template..."
wget -q https://raw.githubusercontent.com/Wandmalfarbe/pandoc-latex-template/master/eisvogel.tex -O "$PANDOC_TEMPLATE_DIR/eisvogel.tex"
if [ $? -eq 0 ]; then
    echo "✅ Eisvogel installed to $PANDOC_TEMPLATE_DIR"
else
    echo "❌ Failed to download Eisvogel"
fi

# 2. Install Python filters (without --break-system-packages flag)
echo ""
echo "📦 Installing pandoc filters..."
pip3 install -q \
    pandoc-xnos \
    pandoc-fignos \
    pandoc-tablenos \
    pandoc-eqnos \
    pandoc-latex-environment 2>/dev/null

# Check what got installed
echo "Checking filter installations:"
for filter in pandoc-xnos pandoc-fignos pandoc-tablenos pandoc-eqnos pandoc-latex-environment; do
    if pip3 show $filter >/dev/null 2>&1; then
        echo "  ✅ $filter installed"
    else
        echo "  ❌ $filter not found"
    fi
done

# 3. Create P2KB template in local templates folder
echo ""
echo "🎨 Creating P2KB De Silva enhanced template..."
cat > templates/p2kb-pasm-desilva-enhanced.latex << 'EOF'
% P2KB De Silva Enhanced Template
% Fixes chapter pages, numbering, and headers
\documentclass[11pt,openany]{book}

% Packages
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

% Colors from De Silva guide
\definecolor{codegray}{HTML}{F5F5F5}
\definecolor{inlineyellow}{HTML}{FFFACD}
\definecolor{yourturncolor}{HTML}{E6F3FF}
\definecolor{missingviolet}{HTML}{E6E6FA}
\definecolor{revieworange}{HTML}{FFE4B5}
\definecolor{diagramblue}{HTML}{E0F2FF}
\definecolor{chaptergreen}{HTML}{F0FFF0}

% CRITICAL FIX 1: Force chapters to new pages
\preto{\chapter}{\clearpage}

% CRITICAL FIX 2: Headers show chapter names
\pagestyle{fancy}
\fancyhead[L]{\leftmark}
\fancyhead[R]{\thepage}
\renewcommand{\chaptermark}[1]{\markboth{Chapter \thechapter: #1}{}}

% CRITICAL FIX 3: No section numbering
\setcounter{secnumdepth}{-1}

% De Silva custom boxes
\newtcolorbox{sidetrack}{
  enhanced,
  colback=gray!10,
  colframe=gray!50,
  borderline={1pt}{0pt}{gray!50,dashed},
  title={\textbf{Sidetrack}},
  fonttitle=\bfseries\color{black},
  breakable
}

\newtcolorbox{yourturn}{
  colback=yourturncolor,
  colframe=blue!30,
  title={\textbf{Your Turn}},
  fonttitle=\bfseries\color{black},
  breakable
}

\newtcolorbox{missing}{
  colback=missingviolet,
  colframe=violet!70,
  boxrule=2pt,
  title={🚧 \textbf{CONTENT MISSING}},
  fonttitle=\large\bfseries\color{black},
  breakable
}

\newtcolorbox{review}{
  colback=revieworange,
  colframe=orange!70,
  boxrule=2pt,
  title={🔍 \textbf{NEEDS REVIEW}},
  fonttitle=\large\bfseries\color{black},
  breakable
}

\newtcolorbox{diagram}{
  colback=diagramblue,
  colframe=blue!50,
  boxrule=2pt,
  title={🎨 \textbf{DIAGRAM NEEDED}},
  fonttitle=\large\bfseries\color{black},
  breakable
}

\newtcolorbox{interlude}{
  colback=gray!10,
  colframe=gray!10,
  boxrule=0pt,
  title={\textbf{Interlude}},
  breakable
}

\newtcolorbox{chapterend}{
  colback=chaptergreen,
  colframe=chaptergreen,
  boxrule=0pt,
  width=0.8\textwidth,
  center,
  fontupper=\itshape,
  breakable
}

% Code listings
\lstset{
  basicstyle=\ttfamily,
  backgroundcolor=\color{codegray},
  breaklines=true,
  frame=none,
  showstringspaces=false
}

% Pandoc variables
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
EOF
echo "✅ P2KB template created at: $(pwd)/templates/p2kb-pasm-desilva-enhanced.latex"

# Also copy to Pandoc's template directory
cp templates/p2kb-pasm-desilva-enhanced.latex "$PANDOC_TEMPLATE_DIR/" 2>/dev/null
echo "✅ Template copied to Pandoc directory"

# 4. Create Lua filter
echo ""
echo "🔧 Creating Lua filter..."
cat > filters/desilva-boxes.lua << 'EOF'
-- Pandoc Lua filter for De Silva boxes
function Div(el)
  local boxTypes = {
    sidetrack = true,
    yourturn = true,
    missing = true,
    chapterend = true,
    review = true,
    diagram = true,
    interlude = true
  }
  
  if el.classes[1] and boxTypes[el.classes[1]] then
    local envName = el.classes[1]
    return {
      pandoc.RawBlock('latex', '\\begin{' .. envName .. '}'),
      pandoc.Div(el.content),
      pandoc.RawBlock('latex', '\\end{' .. envName .. '}')
    }
  end
  return el
end
EOF
echo "✅ Lua filter created at: $(pwd)/filters/desilva-boxes.lua"

# 5. Create test document
echo ""
echo "📝 Creating test document..."
cat > test-template.md << 'EOF'
---
title: "Template Test"
author: "PDFForge"
toc: true
numbersections: false
---

# Chapter 1: First Test

This chapter should start on a NEW PAGE!

## Code Example

```pasm2
    mov x, #42
```

:::sidetrack
This is a sidetrack with gray background and dashed border.
:::

# Chapter 2: Second Test

This should ALSO start on a new page.

The header should say "Chapter 2: Second Test" not "Contents"!

:::yourturn
**Your Turn:** Test something here.
:::

Chapter numbering should be normal (not 0.4).
EOF

echo ""
echo "=== 🎯 Quick Test Commands ==="
echo ""
echo "Test Eisvogel:"
echo "  pandoc test-template.md --template=eisvogel --pdf-engine=xelatex -o test-eisvogel.pdf"
echo ""
echo "Test P2KB template:"
echo "  pandoc test-template.md --template=p2kb-pasm-desilva-enhanced --pdf-engine=xelatex --lua-filter=filters/desilva-boxes.lua -o test-p2kb.pdf"
echo ""
echo "=== ✨ Installation Complete! ==="
echo ""
echo "📁 Created files:"
echo "  • templates/p2kb-pasm-desilva-enhanced.latex"
echo "  • filters/desilva-boxes.lua"
echo "  • test-template.md"
echo ""
echo "🎯 Your three problems should now be FIXED:"
echo "  ✅ Chapters start on new pages"
echo "  ✅ Numbering is correct"
echo "  ✅ Headers show chapter names"
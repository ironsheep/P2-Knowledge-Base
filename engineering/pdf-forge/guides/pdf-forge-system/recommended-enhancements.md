# PDFForge Recommended Enhancements

## Priority 1: Essential Templates & Tools

### Eisvogel Template (Most Important)
```bash
# The most popular Pandoc LaTeX template
cd /usr/share/pandoc/data/templates
wget https://github.com/Wandmalfarbe/pandoc-latex-template/releases/latest/download/eisvogel.latex

# Also get the examples for reference
cd /workspace/templates
git clone https://github.com/Wandmalfarbe/pandoc-latex-template eisvogel-examples
```

**Why**: Professional output out-of-the-box, extensive customization via YAML

### Cross-Reference Filters
```bash
pip3 install --break-system-packages \
  pandoc-xnos \
  pandoc-fignos \
  pandoc-tablenos \
  pandoc-eqnos \
  pandoc-secnos
```

**Why**: Professional numbered figures, tables, equations with references like "See Figure 2.3"

## Priority 2: Enhanced Functionality

### Better Code Blocks & Environments
```bash
pip3 install --break-system-packages \
  pandoc-latex-environment \
  pandocfilters \
  pandoc-include-code
```

**Why**: 
- Create custom styled environments from markdown divs
- Include code from external files with syntax highlighting
- Better control over code formatting

### Diagram Support
```bash
# Already have these in Dockerfile, but verify:
apt-get install -y \
  plantuml \
  graphviz \
  ditaa

pip3 install --break-system-packages \
  pandoc-plantuml-filter \
  pandoc-mermaid-filter
```

**Why**: Generate diagrams from text descriptions in markdown

## Document-Specific Templates

### 1. Technical Manuals (P2-style)
**Built-in class**: `scrbook` (KOMA-Script)
```latex
\documentclass[11pt,twoside,openright]{scrbook}
\usepackage{scrlayer-scrpage}  % Better headers/footers
```

### 2. Professional Reports
**Use**: Eisvogel template with customization
```yaml
---
documentclass: scrreprt
titlepage: true
toc-own-page: true
listings: true
---
```

### 3. Academic Papers
**Built-in class**: `article` with packages
```latex
\documentclass[11pt]{article}
\usepackage{authblk}  % Author affiliations
\usepackage{natbib}   % Citations
```

### 4. Marketing/Brochures
**Built-in class**: `memoir` with custom layout
```latex
\documentclass[10pt,twoside]{memoir}
\usepackage{multicol}
\setlrmarginsandblock{2cm}{2cm}{*}
```

## Template Organization Structure

```
/workspace/templates/
├── eisvogel/              # Eisvogel and examples
├── p2-manuals/            # Your P2 custom templates
│   ├── p2kb-pasm-desilva.latex
│   └── p2kb-technical.latex
├── parallax-official/     # Templates from Parallax
├── professional/          # Generic professional templates
│   ├── report.latex
│   ├── manual.latex
│   └── whitepaper.latex
└── academic/              # Academic templates
    ├── ieee.latex
    └── paper.latex
```

## Quick Setup Script

Create `/workspace/scripts/enhance-pdfforge.sh`:

```bash
#!/bin/bash
# PDFForge Enhancement Script

echo "Installing Eisvogel template..."
cd /usr/share/pandoc/data/templates
wget -q https://github.com/Wandmalfarbe/pandoc-latex-template/releases/latest/download/eisvogel.latex

echo "Installing pandoc filters..."
pip3 install --break-system-packages -q \
  pandoc-xnos \
  pandoc-fignos \
  pandoc-tablenos \
  pandoc-eqnos \
  pandoc-latex-environment

echo "Creating template structure..."
mkdir -p /workspace/templates/{eisvogel,p2-manuals,parallax-official,professional,academic}

echo "Fetching Eisvogel examples..."
cd /workspace/templates
git clone -q https://github.com/Wandmalfarbe/pandoc-latex-template eisvogel

echo "Enhancement complete!"
```

## Usage Examples

### Example 1: Professional Report with Eisvogel
```json
{
  "template": "eisvogel",
  "pdf-engine": "xelatex",
  "variables": {
    "titlepage": true,
    "titlepage-color": "1F4788",
    "titlepage-text-color": "FFFFFF",
    "logo": "logo.png",
    "toc-own-page": true,
    "listings": true
  }
}
```

### Example 2: Technical Manual with Cross-References
```bash
pandoc manual.md \
  --template=scrbook \
  --filter=pandoc-xnos \
  --pdf-engine=xelatex \
  -o manual.pdf
```

### Example 3: Quick Professional Output
```bash
# Just add to any markdown:
---
documentclass: scrartcl
classoption: [11pt, a4paper]
geometry: margin=1in
---

# Your content here
```

## Testing Templates

Create `/workspace/test/template-test.md`:
```markdown
---
title: Template Test
author: Your Name
date: \today
documentclass: scrartcl
---

# Testing Professional Output

This tests our template setup.

## Features to Test

- Code blocks
- Tables  
- Cross-references
- Typography
```

Then test each template:
```bash
pandoc template-test.md --template=eisvogel -o test-eisvogel.pdf
pandoc template-test.md --template=default -o test-default.pdf
```

## Notes

- With `texlive-full`, you have ALL LaTeX packages - no missing package errors!
- XeLaTeX as default means you can use system fonts directly
- The Python filters add significant functionality
- Eisvogel alone will cover 80% of professional document needs

## Next Steps

1. Install Eisvogel (Priority 1)
2. Add cross-reference filters
3. Test with your actual content
4. Customize as needed
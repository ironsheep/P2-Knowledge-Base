# PDFForge Analysis & Recommendations

Generated: 2025-08-23

## ✅ What You Have (Excellent Foundation!)

### Core Tools
- **Pandoc 2.17.1.1** - Good recent version with citeproc built-in
- **XeLaTeX** - Default PDF engine, perfect for custom fonts
- **LuaLaTeX** - Available as alternative
- **texlive-full** - ALL LaTeX packages installed!

### Fonts Available
- **Fira Code** ✅ - Perfect for code blocks
- **Liberation Serif/Sans** ✅ - Excellent readable fonts
- **Latin Modern** ✅ - Professional LaTeX fonts
- **Noto family** ✅ - Comprehensive international support
- **Charter** ❌ - NOT in the list (but we can work around this!)

### Python Filters Installed
- ✅ pandoc-include (include external files)
- ✅ pandoc-plantuml-filter (diagrams from text)
- ✅ pandoc-mustache (template variables)
- ✅ panflute (custom filter framework)

## 🔴 Critical Fixes for De Silva Manual

### Fix 1: Charter Font Alternative
Since Charter isn't available, use **Liberation Serif** or **TeX Gyre Schola**:
```yaml
mainfont: "Liberation Serif"  # Close to Charter, very readable
# OR
mainfont: "TeX Gyre Schola"   # Palatino-like, elegant
monofont: "Fira Code"          # You have this!
```

### Fix 2: Missing Critical Filters
```bash
# MUST INSTALL for professional documents:
pip3 install --break-system-packages \
  pandoc-xnos \
  pandoc-fignos \
  pandoc-tablenos \
  pandoc-latex-environment  # This one is CRITICAL for your :::boxes
```

The `pandoc-latex-environment` filter is what will convert your `:::sidetrack` patterns to LaTeX environments!

## 📦 Immediate Installation Script

Create `/workspace/scripts/enhance-pdfforge-now.sh`:

```bash
#!/bin/bash
echo "=== PDFForge Critical Enhancements ==="

# 1. Get Eisvogel template (just one file!)
echo "Installing Eisvogel template..."
cd /usr/share/pandoc/data/templates
wget -q https://raw.githubusercontent.com/Wandmalfarbe/pandoc-latex-template/master/eisvogel.tex
echo "✅ Eisvogel installed"

# 2. Install critical Python filters
echo "Installing pandoc filters..."
pip3 install --break-system-packages -q \
  pandoc-xnos \
  pandoc-fignos \
  pandoc-tablenos \
  pandoc-latex-environment
echo "✅ Filters installed"

# 3. Create De Silva hybrid template
echo "Creating De Silva template..."
cat > /usr/share/pandoc/data/templates/desilva.tex << 'EOF'
% Based on Eisvogel with De Silva customizations
\input{eisvogel.tex}

% De Silva custom environments
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}

% Sidetrack box
\newenvironment{sidetrack}{%
  \begin{tcolorbox}[
    enhanced,
    colback=gray!10,
    colframe=gray!50,
    borderline={1pt}{0pt}{gray!50,dashed},
    title={\textbf{Sidetrack}},
    fonttitle=\bfseries\color{black}
  ]
}{\end{tcolorbox}}

% Your Turn box
\newenvironment{yourturn}{%
  \begin{tcolorbox}[
    colback=yellow!10,
    colframe=blue!30,
    title={\textbf{Your Turn}},
    fonttitle=\bfseries\color{black}
  ]
}{\end{tcolorbox}}

% Add other boxes as needed...
EOF
echo "✅ De Silva template created"

echo "=== Enhancement Complete! ==="
```

## 🎯 How to Fix Your Three Chapter Issues

### Solution for All Three Problems:

In your `request.json`:
```json
{
  "template": "eisvogel",
  "pdf-engine": "xelatex",
  "variables": {
    "documentclass": "book",
    "classoption": ["11pt", "openany"],
    "book": true,
    "toc": true,
    "toc-own-page": true,
    "numbersections": false,
    "mainfont": "Liberation Serif",
    "monofont": "Fira Code"
  },
  "filters": [
    "pandoc-latex-environment"
  ]
}
```

This will:
1. ✅ **Force chapters to new pages** (book class + openany)
2. ✅ **Fix numbering** (numbersections: false, proper reset)
3. ✅ **Fix headers** (Eisvogel handles this correctly)

## 📝 Simple Pandoc Filter for Your Boxes

Create `/workspace/scripts/desilva-boxes.lua`:

```lua
-- Pandoc filter to convert :::boxtype to LaTeX environments
function Div(el)
  if el.classes[1] == "sidetrack" then
    return {
      pandoc.RawBlock('latex', '\\begin{sidetrack}'),
      el,
      pandoc.RawBlock('latex', '\\end{sidetrack}')
    }
  elseif el.classes[1] == "yourturn" then
    return {
      pandoc.RawBlock('latex', '\\begin{yourturn}'),
      el,
      pandoc.RawBlock('latex', '\\end{yourturn}')
    }
  -- Add other box types...
  end
end
```

Then use with:
```bash
pandoc input.md \
  --template=desilva \
  --lua-filter=/workspace/scripts/desilva-boxes.lua \
  -o output.pdf
```

## 🚀 Next Steps

1. **Run the enhancement script** to install Eisvogel and filters
2. **Test with a simple chapter** to verify fixes work
3. **Refine the De Silva template** with all your box types
4. **Process your manual** with confidence!

## 💡 Why This Will Work

- **Eisvogel** is battle-tested with thousands of users
- **XeLaTeX** + system fonts = no more font package issues
- **Pandoc filters** = clean separation of content and style
- **Book class** = proper chapter handling built-in

Your De Silva manual will look professional with FAR less LaTeX wrestling!
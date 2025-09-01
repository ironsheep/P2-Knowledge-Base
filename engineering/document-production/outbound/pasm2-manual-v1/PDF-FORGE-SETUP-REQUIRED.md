# PDF Forge Setup Requirements

## PDF Forge Directory Structure (2025-08-23)

**Repository Root Structure**:
```
/                           # PDF Forge repo root
├── templates/             # LaTeX templates (.latex files)
├── filters/               # Pandoc Lua filters (.lua files) - NEW!
├── scripts/               # Processing scripts
├── inbox/                 # Where files are placed for processing
├── outbox/                # Where generated PDFs are output
├── config/                # Configuration files
└── output/                # Working directory for processing
```

### Lua Filters Setup

**Location**: `/filters/` at PDF Forge repo root

**Current Filters**:
- `div-to-environment.lua` - Converts Pandoc div syntax to LaTeX environments

**Usage in request.json**:
```json
"pandoc_args": ["--lua-filter=filters/div-to-environment.lua"]
```

**Note**: Filters are referenced relative to repo root where scripts run.

---

## CRITICAL TEMPLATE INSTALLATION FIX (2025-08-23)

**Problem**: Cascading templates fail with "eisvogel.latex not found"
**Cause**: Eisvogel only in /templates/, not in Pandoc's search path
**Solution**: Install Eisvogel in BOTH locations

### Required Installation Steps:

```bash
# In PDF Forge Docker container:

# 1. Verify Pandoc's template directory exists
ls /usr/share/pandoc/data/templates/

# 2. Copy Eisvogel to Pandoc's template directory
cp /templates/eisvogel.latex /usr/share/pandoc/data/templates/

# 3. Verify installation
ls -la /usr/share/pandoc/data/templates/eisvogel.latex
```

### Why This Works:
- Custom templates in `/templates/` can use `\input{eisvogel.latex}`
- Pandoc searches `/usr/share/pandoc/data/templates/` for includes
- Enables template cascading/inheritance

### Template Locations After Fix:
- **Base templates** (Eisvogel, etc.): `/usr/share/pandoc/data/templates/`
- **Custom templates**: `/templates/`
- **Result**: Cascading works via `\input{}`

---

# PDF Forge Setup Requirements

**Created**: 2025-08-20  
**Purpose**: Installation requirements for P2 Manual PDF generation  
**Status**: ⏳ AWAITING INSTALLATION

## 🔧 Required Installations on PDF Forge Machine

### 1. LaTeX Font Packages
```bash
# Run these commands on the PDF Forge system:
sudo apt-get update
sudo apt-get install texlive-fonts-extra
sudo apt-get install texlive-xetex
```

**Why needed**:
- `texlive-fonts-extra`: Provides Charter and Palatino fonts for better readability
- `texlive-xetex`: Better font support and modern typography features

### 2. LaTeX Style Packages
```bash
sudo apt-get install texlive-latex-extra
sudo apt-get install texlive-plain-generic  # For soul.sty
```

**Why needed**:
- `texlive-latex-extra`: Provides `tcolorbox` for boxes and `mdframed` for backgrounds
- `texlive-plain-generic`: Provides `soul` for inline highlighting

### 3. Verify Installations
After installation, verify these packages are available:
```bash
# Check if packages installed correctly:
kpsewhich tcolorbox.sty
kpsewhich mdframed.sty
kpsewhich charter.sty
```

**Note**: If `soul.sty` is missing, that's OK! We can use `xcolor` for inline highlighting instead:

```latex
% Instead of soul package:
% \usepackage{soul}
% \hl{text}

% Use xcolor (already installed):
\usepackage{xcolor}
\newcommand{\inlinecode}[1]{%
  \colorbox{yellow!20}{\texttt{#1}}%
}
```

## 📦 Complete Installation Command
For convenience, here's everything in one command:
```bash
sudo apt-get update && \
sudo apt-get install -y \
  texlive-fonts-extra \
  texlive-xetex \
  texlive-latex-extra \
  texlive-plain-generic
```

## ✅ Installation Checklist
- [ ] texlive-fonts-extra installed
- [ ] texlive-xetex installed  
- [ ] texlive-latex-extra installed
- [ ] All packages verified with kpsewhich
- [ ] Test PDF generation with new template

## 🎯 What This Enables

Once installed, the PDF will have:
1. **Better typography** - Charter/Palatino fonts instead of default Computer Modern
2. **Colored backgrounds** - Yellow for inline code, gray for sidetracks, violet for TBDs
3. **Dotted borders** - Visual distinction for optional content
4. **Improved readability** - Better line spacing and font choices

## 📝 Notes

- These are standard Debian/Ubuntu packages
- Installation requires sudo privileges
- Total download size approximately 200-300MB
- Installation takes 5-10 minutes depending on connection

## 🔄 Status Updates

**Installation Complete!**

Installation Date: 2025-08-20
Installed By: User
Packages Verified:
- ✅ texlive-fonts-extra (charter.sty found)
- ✅ texlive-xetex (installed)
- ✅ texlive-latex-extra (tcolorbox.sty, mdframed.sty found)
- ✅ texlive-plain-generic (soul.sty found)

All kpsewhich checks: ✅ PASS
Ready for PDF generation: YES

---

**Next Steps After Installation**:
1. Run test PDF generation with P2 manual
2. Verify fonts render correctly
3. Check colored backgrounds work
4. Confirm dotted borders appear

---

*Please notify Claude when installation is complete so we can proceed with PDF generation.*
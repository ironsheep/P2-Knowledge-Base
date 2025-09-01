#!/bin/bash
# PDFForge Discovery Script
# Purpose: Gather complete information about PDFForge capabilities
# Output: pdfforge-capabilities.txt

OUTPUT_FILE="pdfforge-capabilities.txt"

echo "PDFForge Capability Discovery Report" > $OUTPUT_FILE
echo "====================================" >> $OUTPUT_FILE
echo "Generated: $(date)" >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

echo "=== SYSTEM INFORMATION ===" >> $OUTPUT_FILE
uname -a >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

echo "=== PANDOC VERSION ===" >> $OUTPUT_FILE
pandoc --version >> $OUTPUT_FILE 2>&1
echo "" >> $OUTPUT_FILE

echo "=== PANDOC EXTENSIONS ===" >> $OUTPUT_FILE
pandoc --list-extensions >> $OUTPUT_FILE 2>&1
echo "" >> $OUTPUT_FILE

echo "=== PANDOC INPUT FORMATS ===" >> $OUTPUT_FILE
pandoc --list-input-formats >> $OUTPUT_FILE 2>&1
echo "" >> $OUTPUT_FILE

echo "=== PANDOC OUTPUT FORMATS ===" >> $OUTPUT_FILE
pandoc --list-output-formats >> $OUTPUT_FILE 2>&1
echo "" >> $OUTPUT_FILE

echo "=== PANDOC HIGHLIGHT LANGUAGES ===" >> $OUTPUT_FILE
pandoc --list-highlight-languages >> $OUTPUT_FILE 2>&1
echo "" >> $OUTPUT_FILE

echo "=== PANDOC HIGHLIGHT STYLES ===" >> $OUTPUT_FILE
pandoc --list-highlight-styles >> $OUTPUT_FILE 2>&1
echo "" >> $OUTPUT_FILE

echo "=== PANDOC DATA DIRECTORY ===" >> $OUTPUT_FILE
pandoc --version | grep "Default user data directory" >> $OUTPUT_FILE 2>&1
echo "" >> $OUTPUT_FILE

echo "=== LATEX VERSION ===" >> $OUTPUT_FILE
pdflatex --version >> $OUTPUT_FILE 2>&1
echo "" >> $OUTPUT_FILE

echo "=== XELATEX VERSION ===" >> $OUTPUT_FILE
xelatex --version 2>&1 | head -5 >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

echo "=== LUALATEX VERSION ===" >> $OUTPUT_FILE
lualatex --version 2>&1 | head -5 >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

echo "=== TEX PACKAGES INSTALLED (via tlmgr) ===" >> $OUTPUT_FILE
if command -v tlmgr &> /dev/null; then
    tlmgr list --installed --only-installed >> $OUTPUT_FILE 2>&1
else
    echo "tlmgr not found - checking dpkg for texlive packages:" >> $OUTPUT_FILE
    dpkg -l | grep texlive >> $OUTPUT_FILE 2>&1
fi
echo "" >> $OUTPUT_FILE

echo "=== CHECKING KEY LATEX PACKAGES ===" >> $OUTPUT_FILE
for package in tcolorbox mdframed soul fancyhdr titlesec xcolor listings hyperref graphicx array calc longtable booktabs multicol makeidx needspace fancyvrb tikz; do
    echo -n "Checking $package.sty: " >> $OUTPUT_FILE
    if kpsewhich ${package}.sty > /dev/null 2>&1; then
        echo "FOUND" >> $OUTPUT_FILE
    else
        echo "NOT FOUND" >> $OUTPUT_FILE
    fi
done
echo "" >> $OUTPUT_FILE

echo "=== SYSTEM FONTS (for XeLaTeX/LuaLaTeX) ===" >> $OUTPUT_FILE
fc-list : family | sort | uniq >> $OUTPUT_FILE 2>&1
echo "" >> $OUTPUT_FILE

echo "=== PANDOC FILTERS AVAILABLE ===" >> $OUTPUT_FILE
echo "Checking for pandoc filters in PATH:" >> $OUTPUT_FILE
ls -la /usr/bin/pandoc-* 2>/dev/null >> $OUTPUT_FILE
ls -la /usr/local/bin/pandoc-* 2>/dev/null >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

echo "Checking specific filters:" >> $OUTPUT_FILE
for filter in pandoc-crossref pandoc-citeproc pandoc-include pandoc-latex-environment; do
    echo -n "$filter: " >> $OUTPUT_FILE
    if command -v $filter &> /dev/null; then
        echo "FOUND at $(which $filter)" >> $OUTPUT_FILE
    else
        echo "NOT FOUND" >> $OUTPUT_FILE
    fi
done
echo "" >> $OUTPUT_FILE

echo "=== PYTHON VERSION (for Pandoc filters) ===" >> $OUTPUT_FILE
python3 --version >> $OUTPUT_FILE 2>&1
echo "" >> $OUTPUT_FILE

echo "=== PYTHON PANDOC PACKAGES ===" >> $OUTPUT_FILE
pip3 list 2>/dev/null | grep -i pandoc >> $OUTPUT_FILE 2>&1
echo "" >> $OUTPUT_FILE

echo "=== IMAGEMAGICK/GRAPHICSMAGICK (for image conversion) ===" >> $OUTPUT_FILE
convert --version 2>&1 | head -3 >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

echo "=== GHOSTSCRIPT (for PDF manipulation) ===" >> $OUTPUT_FILE
gs --version >> $OUTPUT_FILE 2>&1
echo "" >> $OUTPUT_FILE

echo "=== INKSCAPE (for SVG to PDF conversion) ===" >> $OUTPUT_FILE
inkscape --version >> $OUTPUT_FILE 2>&1
echo "" >> $OUTPUT_FILE

echo "=== LIBRSVG (for SVG handling) ===" >> $OUTPUT_FILE
rsvg-convert --version >> $OUTPUT_FILE 2>&1
echo "" >> $OUTPUT_FILE

echo "=== DOCKERFILE CONTENTS ===" >> $OUTPUT_FILE
if [ -f Dockerfile ]; then
    echo "Dockerfile found, contents:" >> $OUTPUT_FILE
    cat Dockerfile >> $OUTPUT_FILE
else
    echo "No Dockerfile in current directory" >> $OUTPUT_FILE
fi
echo "" >> $OUTPUT_FILE

echo "=== MAKEFILE CONTENTS (if exists) ===" >> $OUTPUT_FILE
if [ -f Makefile ]; then
    echo "Makefile found, contents:" >> $OUTPUT_FILE
    cat Makefile >> $OUTPUT_FILE
else
    echo "No Makefile in current directory" >> $OUTPUT_FILE
fi
echo "" >> $OUTPUT_FILE

echo "=== PANDOC DEFAULT TEMPLATES ===" >> $OUTPUT_FILE
echo "LaTeX template location:" >> $OUTPUT_FILE
pandoc -D latex 2>/dev/null | head -50 >> $OUTPUT_FILE
echo "... (first 50 lines shown)" >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

echo "=== DISCOVERY COMPLETE ===" >> $OUTPUT_FILE
echo "Report generated successfully!" >> $OUTPUT_FILE
echo "File size: $(du -h $OUTPUT_FILE | cut -f1)" >> $OUTPUT_FILE

echo ""
echo "Discovery complete! Results saved to: $OUTPUT_FILE"
echo "File size: $(du -h $OUTPUT_FILE | cut -f1)"
echo ""
echo "Please copy this file back to your local system."
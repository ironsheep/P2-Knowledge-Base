# PDF Templates Master Library

**Last Updated**: 2025-08-20  
**Source**: PDF Forge production templates

## Available Templates

### 1. p2kb-pasm-desilva.latex
**Purpose**: deSilva pedagogical style for P2 tutorials  
**Features**:
- Colored boxes for different content types (missing, review, diagram needed)
- Sidetracks with dotted borders
- Interludes without borders
- Chapter-end celebration boxes
- Draft watermarking support
- Fixed: Chapter numbering starts from 1
- Fixed: Page headers show chapter names
- Fixed: No duplicate environment definitions

### 2. p2kb-pasm2-manual.latex
**Purpose**: Parallax official documentation style  
**Features**:
- Parallax branding and colors
- Professional technical documentation layout
- Compatible with instruction reference format
- Single-page article class
- Company header/footer styling

### 3. p2kb-pasm2-minimal.latex
**Purpose**: Minimal reliable template based on proven admin template  
**Features**:
- Book class for multi-chapter documents
- Crimson font for readability
- Two-sided printing support
- Proven pandoc compatibility
- Clean, simple formatting

### 4. p2kb-presentation.latex
**Purpose**: Professional presentation and sponsor materials  
**Features**:
- Modern blue/gray color scheme
- Info/warning/success callout boxes
- Professional section formatting
- Enhanced list formatting
- Clean title page design

## Template Workflow

1. **FROM PDF Forge**: Templates arrive in `/exports/pdf-generation/inbound/pdf-templates/`
2. **TO Master**: Copied here for permanent reference
3. **NEW Templates**: Created in document's `/exports/pdf-generation/outbound/[doc-name]/` folder
4. **Signal to User**: Template in outbound = needs deployment to Forge
5. **Confirmation**: Template disappears from outbound = deployed

## Package Requirements (Available on PDF Forge)

All templates assume these packages are installed:
- texlive-fonts-extra (Charter, Palatino)
- texlive-xetex (XeLaTeX engine)
- texlive-latex-extra (tcolorbox, mdframed)
- texlive-plain-generic (soul.sty)

## Usage Notes

- Template names follow pattern: `p2kb-[purpose].latex`
- No version numbers in filenames (e.g., NOT p2kb-manual-v2.latex)
- Variables are passed via pandoc -V flags
- All templates include pandoc compatibility fixes

## Common Variables

All templates support:
- `$title$` - Document title
- `$author$` - Author name
- `$date$` - Publication date
- `$version$` - Version string
- `$company$` - Company name
- `$footer$` - Footer text

Additional template-specific variables documented in each template header.
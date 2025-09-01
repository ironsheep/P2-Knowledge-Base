# PDF Generation Test Checklist

## 📦 Ready for Testing: P2 Smart Pins Complete Reference

### Pre-Deployment Verification ✅

**All files present in `/exports/pdf-generation/outbound/P2-Smart-Pins-Reference/`:**
- ✅ `P2-Smart-Pins-Complete-Reference.md` (83KB - LaTeX escaped)
- ✅ `p2-smart-pins-reference.latex` (6KB template)
- ✅ `request.json` (1KB configuration)
- ✅ `assets/` folder with 21 PNG images
- ✅ `last-deployed/` backup folder

### 🚀 Deployment Steps

1. **Copy entire folder to PDF Forge:**
   ```bash
   # On your local machine (copy entire folder including assets)
   scp -r P2-Smart-Pins-Reference/ [user]@[pdf-forge]:[path]/inbox/
   ```

2. **On PDF Forge, move template:**
   ```bash
   cd [pdf-forge-root]
   mv inbox/P2-Smart-Pins-Reference/p2-smart-pins-reference.latex templates/
   ```

3. **Generate PDF:**
   ```bash
   cd [pdf-forge-root]
   node scripts/generate-pdf.js inbox/P2-Smart-Pins-Reference/request.json
   ```

4. **Check output:**
   ```bash
   ls -la outbox/P2-Smart-Pins-Complete-Reference-v1.0.pdf
   ```

### 🔍 What to Check in PDF Output

#### Title Page
- [ ] "DRAFT - TECHNICAL REVIEW ONLY" appears in red
- [ ] Technical Review Notice box is present
- [ ] Document Statistics box shows correct numbers
- [ ] Title and subtitle are correct

#### Table of Contents
- [ ] All chapters listed
- [ ] Executive Summary present
- [ ] Quick Start Guide present
- [ ] Page numbers align

#### Content Verification
- [ ] Images appear (14 diagrams should be visible)
- [ ] Code blocks have syntax highlighting
- [ ] Tables format correctly (especially comparison matrix)
- [ ] Headers and footers show correctly

#### Specific Sections to Check
- [ ] Page ~5: Executive Summary renders correctly
- [ ] Page ~8: Quick Start Guide code examples work
- [ ] Page ~50: First Smart Pin diagram appears
- [ ] Page ~400: Index is present

### ⚠️ Potential Issues and Fixes

**If images don't appear:**
- Check image paths are relative: `assets/filename.png`
- Verify all PNGs copied to PDF Forge

**If LaTeX errors occur:**
- Check for unescaped special characters
- Verify template syntax is valid

**If formatting looks wrong:**
- Template may need XeLaTeX packages
- Check PDF Forge has required fonts

### 📊 Expected Results

- **File Size**: ~5-10 MB PDF
- **Page Count**: ~400 pages
- **Generation Time**: 1-3 minutes
- **Images**: All 14 should be embedded
- **Code Examples**: 156 with highlighting

### 🎯 Success Criteria

The PDF is ready for technical review if:
1. ✅ Generates without errors
2. ✅ All content is present
3. ✅ Images display correctly
4. ✅ Code has syntax highlighting
5. ✅ Technical review header is prominent
6. ✅ Navigation (TOC, page numbers) works

---

## Test Command Summary

```bash
# Quick test command sequence:
cd [pdf-forge-root]
mv inbox/P2-Smart-Pins-Reference/p2-smart-pins-reference.latex templates/
node scripts/generate-pdf.js inbox/P2-Smart-Pins-Reference/request.json
ls -la outbox/*.pdf
```

---

*Ready for test generation!*  
*The current template is clean, simple, and should work well.*
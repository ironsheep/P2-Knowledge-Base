# Build Instructions - P2 Debugger Manual v1.0 Draft 1

**Date**: August 15, 2025  
**Document**: P2 Single-Step Debugger User's Manual  
**Voice**: Stephen/IronSheep (The Bridge)  
**Status**: Ready for PDF generation (no images yet)

## Files in This Package

```
v1.0-draft1/
├── BUILD-INSTRUCTIONS.md           # This file
├── debugger-manual-v1.0.docx      # Word format for Pages import
├── debugger-manual-source.md       # Original Markdown source
└── template-setup-guide.md         # How to create the Pages template
```

## Step-by-Step PDF Creation

### Step 1: Create Pages Template (First Time Only)
1. Open Apple Pages
2. Create new document from blank template
3. Follow the template specifications in `template-setup-guide.md`
4. Save as template: File → Save as Template → ".P2-User-Manual.template"

### Step 2: Import Content
1. Open Apple Pages
2. File → Open → Select `debugger-manual-v1.0.docx`
3. Pages will import the Word document with formatting
4. Apply your `.P2-User-Manual.template` styling

### Step 3: Format and Style
1. **Apply template styles** to match the professional design
2. **Verify code formatting** - should be monospace, gray background
3. **Check heading hierarchy** - consistent sizing and spacing
4. **Add page breaks** where logical (between major sections)
5. **Format table of contents** - auto-generate if needed

### Step 4: Export PDF
1. File → Export To → PDF
2. Settings:
   - **Quality**: Best
   - **Include**: Table of Contents (if created)
   - **Security**: None needed
3. Save as: `p2-debugger-manual-v1.0-draft1.pdf`

## Expected Results

### Document Structure
- **Total Pages**: ~15-20 pages
- **Sections**: 8 major sections with subsections
- **Code Examples**: ~12 SPIN2 code blocks
- **Features**: Complete debugger workflow coverage

### Content Summary
- Introduction and quick start
- Core debugging features (PASM-level, Multi-COG)
- DEBUG SCOPE displays and triggers  
- Advanced workflows (performance, hardware interface)
- Error handling and diagnostics
- Real-world debugging scenarios
- Troubleshooting guide
- Version history appendix

## Feedback Needed

When you've generated the PDF, please provide feedback on:

1. **Overall Layout**: Professional appearance, readability
2. **Typography**: Font choices, sizing, hierarchy clarity
3. **Code Formatting**: Monospace display, background styling
4. **Spacing**: Section breaks, white space, margins
5. **Navigation**: Easy to find information, logical flow
6. **Missing Elements**: What would improve usability?

## Next Iteration

Based on your feedback, I will:
1. **Resume MCP task #535**
2. **Adjust template design** per your suggestions
3. **Modify content formatting** as needed
4. **Create v1.0-draft2** with improvements
5. **Pause task again** for your next review

## Notes

- **No images yet**: This draft uses text placeholders for screenshots
- **Voice consistency**: Maintained Stephen/IronSheep practical tone throughout
- **Complete content**: All major debugger features covered
- **Code tested**: All SPIN2 examples are syntactically correct

**Ready for your PDF generation and feedback!**
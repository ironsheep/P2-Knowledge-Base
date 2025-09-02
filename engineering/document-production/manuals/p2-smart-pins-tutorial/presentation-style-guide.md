# P2 Smart Pins Complete Reference - Presentation Style Guide

## Overall Design Philosophy
**"Technical Elegance Through Clarity"**
- Clean, modern technical documentation aesthetic
- High information density without clutter
- Quick visual scanning capability
- Professional without being sterile

## Recommended Layout Style

### Page Layout
- **Format**: US Letter (8.5" × 11") for easy printing
- **Margins**: 0.75" all sides (maximizes content area)
- **Columns**: Single column for code readability
- **Headers**: Mode name on left, Mode binary on right
- **Footers**: Page number centered, section name discrete

### Typography Hierarchy
```
TITLE: Source Sans Pro Bold, 24pt (Mode Headers)
SECTION: Source Sans Pro Semibold, 14pt (Specifications, Configuration, etc.)
BODY: Source Serif Pro, 11pt (Readable technical content)
CODE: Fira Code, 10pt (Monospace with ligatures)
CAPTIONS: Source Sans Pro, 9pt (Image/table captions)
```

### Color Palette
- **Primary Text**: #1a1a1a (Softer than pure black)
- **Headers**: #004B87 (Professional blue, not Parallax blue)
- **Code Background**: #f8f9fa (Subtle gray)
- **Syntax Highlighting**: 
  - Keywords: #0066cc (blue)
  - Numbers: #098658 (green)
  - Comments: #6a737d (gray)
- **Accent Elements**: #ff6b00 (Iron Sheep orange, sparingly)

### Visual Structure Per Mode

```
┌─────────────────────────────────────────────────────────┐
│ Mode %00010 — DAC 124Ω, 3.3V Output          [Header]   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│ ▪ Specifications                              [Section]  │
│   Clean bullet-point layout with aligned values          │
│                                                           │
│ ┌───────────────────────────────────────────┐           │
│ │ [Register Bit Diagram - Clean Vector Art]  │           │
│ └───────────────────────────────────────────┘           │
│                                                           │
│ ▪ Configuration                                          │
│   Register details in structured format                  │
│                                                           │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ // Spin2 Implementation                              │ │
│ │ [Syntax-highlighted code in subtle background]       │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                           │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ ' PASM2 Implementation                               │ │
│ │ [Syntax-highlighted code in subtle background]       │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                           │
│ ▪ Applications                                           │
│   Practical uses with performance notes                  │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## Distinctive Elements

### Mode Headers
- Large, bold mode number with binary representation
- Clear mode name
- Thin horizontal rule separator
- NO decorative elements

### Code Blocks
- Subtle background shading (#f8f9fa)
- Thin left border in language color (Spin2 = blue, PASM2 = green)
- Clear language label in top-right corner
- Line numbers only if referenced in text

### Visual Aids
- **Timing Diagrams**: Clean, vector-style waveforms
- **Register Diagrams**: Bit-field boxes with labels
- **Pin Connections**: Simple line diagrams
- **Tables**: Minimal borders, alternating row shading

### Information Boxes
Three types only:
```
📌 NOTE: Important information (blue border)
⚠️ WARNING: Critical limitations (orange border)
💡 TIP: Optimization suggestions (green border)
```

## Professional Touches

### Front Matter
```
Title Page:
- Clean title typography
- "Professional Reference" clearly stated
- Version and date
- NO company logos on front

Copyright Page:
- Standard copyright notice
- Disclaimer
- Small "Produced by Iron Sheep Productions" with logo
```

### Back Matter
```
Appendices:
- Quick reference cards
- Index
- About Iron Sheep Productions (½ page)
- Logo and website
- "Initial Edition - Version 1.0"
```

## What Makes This Style Optimal

### For Developers
- **Scannable**: Can find any mode in seconds
- **Readable**: Code stands out clearly
- **Printable**: Works in B&W if needed
- **Professional**: Looks credible on any desk

### For Learning
- **Consistent**: Same structure for all 32 modes
- **Complete**: Everything on 4-5 pages per mode
- **Clear**: No ambiguity in presentation

### For Production
- **Eisvogel Compatible**: Works with the template
- **Markdown Friendly**: Simple to generate
- **Version Control**: Text-based source
- **Maintainable**: Easy to update

## Branding Strategy

### Subtle but Professional
- **Front**: No branding, pure technical content
- **Footer**: Tiny "Iron Sheep Productions" on copyright page
- **Back**: Professional "About" section with logo
- **Throughout**: Quality speaks for itself

### Example Back Page Section
```
─────────────────────────────────────────────────
About This Reference

This P2 Smart Pins Complete Reference represents 
the comprehensive documentation effort to make all 
32 Smart Pin modes accessible to developers.

Initial Edition
Version 1.0 - August 2025

Produced by Iron Sheep Productions, LLC
[Small logo here]
www.ironsheepproductions.com

Special thanks to Jon Titus for the original 
Smart Pins documentation and the Parallax 
community for validation and feedback.
─────────────────────────────────────────────────
```

## Implementation with Eisvogel

### Template Customization
```yaml
# In eisvogel template header
titlepage: true
titlepage-text-color: "1a1a1a"
titlepage-rule-color: "004B87"
titlepage-background: "none"  # Clean white
toc: true
toc-depth: 2
highlight-style: github
code-block-font-size: \small
listings-no-page-break: true
```

### Production Commands
```bash
pandoc smart-pins-reference.md \
  -o smart-pins-reference.pdf \
  --template=eisvogel \
  --listings \
  --toc \
  --number-sections \
  --highlight-style=github
```

## Summary

This presentation style delivers:
- **Maximum Clarity**: Information-first design
- **Professional Appearance**: Credible technical document
- **Practical Usability**: Developer-friendly layout
- **Subtle Branding**: Iron Sheep quality without intrusion
- **Production Ready**: Works with existing tools

The result will be a reference document that looks like it belongs on every P2 developer's desk - clean, professional, and immediately useful.
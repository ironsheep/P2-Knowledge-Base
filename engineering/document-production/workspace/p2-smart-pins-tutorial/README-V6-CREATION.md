# P2 Smart Pins Tutorial - Version 6 Creation

## Why V6 Was Created (2025-09-02)

V6 was created from V5 to accomplish a complete image refresh using cleaned, properly-named images from the ingestion source.

### Problems V6 Solves:

1. **Missing Image Assets** - V5 referenced images that didn't exist in any assets folder
2. **Incorrect Image Matching** - Many images were incorrectly matched to content (e.g., quadrature encoder image used for sync serial)
3. **Unorganized Image Sources** - Images needed to be consolidated from the cleaned ingestion source
4. **Poor Image Naming** - Original extraction had mode-specific naming that wasn't being utilized

### What V6 Provides:

- **Clean Master Document** - `P2-Smart-Pins-Green-Book-Tutorial-v6.md` (read-only)
- **Matched Assets Folder** - `v6-assets/` containing 22 properly-named images
- **Correct Image Mappings** - All mode-specific images correctly matched to their content
- **Smart Pin Block Diagram** - Added the missing `smart-pins-master-trimmed.png`
- **Placeholder Markers** - Missing conceptual diagrams marked as `needs-diagram`

### Image Sources:

- **Primary Source**: `/engineering/ingestion/sources/smart-pins/assets/images-smartpins-20250901/`
  - 21 mode-specific images extracted from P2 SmartPins-220809.pdf
  - Named with mode numbers for easy identification (e.g., mode00011_page13)

- **Independent Image**: `smart-pins-master-trimmed.png`
  - From `/engineering/ingestion/visual-assets-catalog/`
  - Not part of the original PDF but essential for the tutorial

### Version Protection:

V6 and its assets are protected as a matched set:
- `P2-Smart-Pins-Green-Book-Tutorial-v6.md` - Read-only master
- `v6-assets/` - Version-specific image folder
- Both committed together to maintain consistency

### Working Process:

When starting new work:
1. Copy v6 → working document
2. Copy v6-assets → assets
3. Make edits to working copies
4. Preserve v6 as reference baseline

### Key Fixes in V6:

- ✅ Chapter 0 timing diagrams correctly matched
- ✅ PWM Sawtooth/Triangle images unswapped  
- ✅ Sync Serial using correct serial timing image
- ✅ Quadrature encoder using correct mode image
- ✅ All mode-specific images verified against catalog
- ✅ Missing conceptual images marked for future creation

---

*V6 represents a clean, verified baseline with all available images correctly matched and organized.*
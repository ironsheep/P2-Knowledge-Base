# AI Reference Documentation

## Document Processing Strategy

Each source document is analyzed independently, with results archived separately before synthesis.

## File Structure

### `/extractions/` - Raw Document Extractions
Independent analysis of each source document, preserved as-is:
- `spreadsheet-pasm2-instructions.md` - P2 Instructions v35 CSV analysis
- `pdf-silicon-document.md` - P2 Documentation v35 PDF analysis (pending)

### Root Level - Synthesized Knowledge
- `pasm2-knowledge-synthesis.md` - Combined understanding from all sources

## Source Documents

**Official P2 documentation from [Parallax.com](https://www.parallax.com):**
- **P2 Instructions v35 - Rev B/C Silicon** (spreadsheet)
- **P2 Documentation v35 - Rev B/C Silicon** (PDF)

*These authoritative documents by Chip Gracey are publicly available from Parallax. 
Local copies in `/import/p2/` are for processing only and are not versioned in this repository.*

## Process
1. Each document analyzed independently
2. Extraction saved to `/extractions/`
3. Questions generated from gaps in understanding
4. Synthesis combines all extractions
5. Questions answered by cross-referencing documents

## Current Status
- ✅ Spreadsheet extraction complete (2025-08-14)
- ⏳ PDF extraction pending
- ⏳ Synthesis pending PDF completion
# P2 Streamer Programming Guide - Workspace

## Purpose

This workspace is for developing and refining the P2 Streamer Programming Guide before PDF generation.

## Source Document

The primary source document is located at:
```
../manuals/p2-streamer-programming-guide/P2-Streamer-Programming-Guide.md
```

## Workflow

1. **Edit** the source markdown in the manuals folder
2. **Stage** files for PDF generation in this workspace
3. **Deploy** to outbound for PDF Forge processing

## Document Status

| Item | Status |
|------|--------|
| Source compilation | Complete |
| Technical review | Pending |
| PDF template selection | Pending |
| LaTeX escaping | Pending |

## Content Coverage

The guide covers:
- Streamer architecture and NCO operation
- All 8 mode categories with encoding tables
- Complete symbol/constant reference
- DAC channel configuration
- Pin selection and control
- DDS/Goertzel frequency analysis
- Video output (VGA, HDMI, composite)
- Programming examples from real code

## Sources Used

- Silicon Documentation v35
- Spin2 Documentation v51
- Flash Loader source code
- Quick Bytes Goertzel example
- OBEX video driver examples

## Next Steps

1. Select appropriate PDF template
2. Add diagrams/figures if needed
3. Run LaTeX escape script
4. Stage to outbound for PDF Forge

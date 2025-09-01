# Sources Directory

## Purpose
This directory contains all source materials, extractions, and analysis documents that feed into the public-facing documentation. This is the working area where raw materials are processed and refined before becoming part of the official documentation.

## Directory Structure

### `/originals/`
Original source documents from Parallax and the community:
- PDFs from Parallax
- Spreadsheets with instruction sets
- Text extractions from PDFs
- Community-contributed documents

### `/extractions/`
Machine-processed extractions from original sources:
- Structured data extracted from spreadsheets
- Text content extracted from PDFs
- Parsed technical specifications

### `/analysis/`
Analysis and gap-identification documents:
- Knowledge gaps identified during processing
- Questions for Chip Gracey and Parallax team
- Missing content requests
- Documentation audit results

### `/working/`
Temporary working documents during processing:
- Draft extractions
- In-progress analysis
- Notes and scratch files

## Workflow

1. **Import**: Original documents go into `/originals/`
2. **Extract**: Process originals to create structured extractions in `/extractions/`
3. **Analyze**: Identify gaps and create analysis documents in `/analysis/`
4. **Generate**: Use extractions and analysis to create public documentation in parent directories
5. **Clean**: Move completed work from `/working/` to appropriate locations

## Important Notes

- This directory is for internal processing only
- Public-facing documentation lives in the parent directories (`/ai-reference/`, `/learning-paths/`, etc.)
- All files here maintain clear provenance back to original sources
- Version control tracks the evolution from source to final documentation

## Current Status

See `EXTRACTION-INDEX.md` for detailed status of all document processing.
# P2 Knowledge Base Central Repository

## Overview
This is the central repository for all P2 (Propeller 2) microcontroller knowledge, organized as structured YAML files with comprehensive metadata and cross-references.

## Purpose
- **Single Source of Truth**: Aggregates knowledge from multiple authoritative sources
- **Machine-Readable**: YAML format enables automated document generation and AI consumption
- **Quality-Tracked**: Every entry has completeness scores and audit trails
- **Version-Controlled**: Git-based tracking of all changes and updates

## Directory Structure

### Core Content Directories
- `instructions/` - All P2 instruction definitions (PASM2 and Spin2)
- `architecture/` - P2 architectural components and systems
- `hardware/` - P2 boards, modules, and physical specifications
- `components/` - Subsystems like Smart Pins, CORDIC, streamers
- `examples/` - Code examples linked to instructions and features

### Metadata and Tracking
- `quality-audits/` - Completeness scores and extraction coverage
- `update-tracking/` - Change logs and version history

## Naming Conventions
- **Files**: lowercase, hyphens for spaces, `.yaml` extension
  - Example: `add-instruction.yaml`, `smart-pin-mode-7.yaml`
- **Directories**: lowercase, hyphens for spaces
  - Example: `smart-pins/`, `cross-references/`

## Completeness Scoring
Each entry is scored 0-8 based on data layers present:
1. Basic definition (P2 Instruction Set CSV)
2. Timing data (P2 Datasheet)
3. Rich narratives (Silicon Doc)
4. Clarifications (Chip's forum posts)
5. Code examples
6. Cross-references
7. Usage patterns
8. Meta-knowledge

## Contributing
See `repository-structure.md` for detailed documentation on:
- YAML schema specifications
- Extraction methodologies
- Quality requirements
- Update procedures

## Status
- **Version**: 1.0 (Initial Structure)
- **Coverage**: Building toward 500+ instructions
- **Quality Target**: 80% entries at score 6+
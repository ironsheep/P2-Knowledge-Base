# Engineering Tools

*Comprehensive toolkit for P2 Knowledge Base development and maintenance*

## Overview

This directory contains all tools and scripts used in the P2 Knowledge Base engineering workflow. Tools are organized by function to support ingestion, conversion, validation, and automation tasks.

## Directory Structure

```
tools/
├── extraction/        # Content extraction and mining tools
├── conversion/        # Format converters and transformers
├── validation/        # Code validators and syntax checkers
├── automation/        # Workflow automation scripts
└── documentation/     # Tool usage guides and documentation
```

## Tool Categories

### 📥 Extraction Tools (`extraction/`)

Tools for extracting content from various sources including PDFs, code files, and documentation.

| Tool | Language | Purpose |
|------|----------|---------|
| `extract-manual-examples.py` | Python | Extract code examples from manuals |
| `find-images-in-code.py` | Python | Locate image references in source code |
| `pdf_image_extractor.py` | Python | Extract images from PDF documents |
| `source-code-extractor.py` | Python | Extract and catalog source code from documents |
| `generate-smartpin-diagrams.py` | Python | Generate Smart Pin configuration diagrams |

### 🔄 Conversion Tools (`conversion/`)

Tools for converting between formats and preparing content for processing.

| Tool | Language | Purpose |
|------|----------|---------|
| `latex-escape-all.sh` | Shell | Escape LaTeX special characters in markdown |
| `apply-coloring.sh` | Shell | Apply syntax coloring to code blocks |
| `convert-to-div-blocks.sh` | Shell | Convert markdown to div block syntax |
| `format-pasm-instructions.py` | Python | Format PASM2 instruction documentation |
| `uppercase-instructions.py` | Python | Convert instructions to uppercase format |
| `uppercase-instructions-latex.py` | Python | Convert instructions to uppercase for LaTeX |
| `latex_escape_processor.py` | Python | Advanced LaTeX character escaping processor |

### ✅ Validation Tools (`validation/`)

Tools for validating code syntax and document structure.

| Tool | Language | Purpose |
|------|----------|---------|
| `validate-pasm-code.sh` | Shell | Validate PASM2 code using pnut_ts compiler |

### 🤖 Automation Tools (`automation/`)

Scripts for automating repetitive tasks and workflows.

| Tool | Language | Purpose |
|------|----------|---------|
| `create-request-json.sh` | Shell | Generate PDF request JSON files |

### 📚 Documentation (`documentation/`)

Guides and documentation for tool usage and development.

| Document | Purpose |
|----------|---------|
| `pnut_ts-usage-guide.md` | Complete guide for P2 compiler usage |
| `claude-p2-development-environment.md` | P2 development environment setup for Claude |
| `TOOL-REGRESSION-PATTERN.md` | Pattern documentation for tool regression testing |

## Test Files

The `conversion/test-files/` directory contains test cases and validation files for the conversion tools, particularly for LaTeX escaping:

- LaTeX escaping test cases and gold standards
- Test markdown files with various P2 code patterns
- Regression test files for validation

## Usage Examples

### Extract Images from PDF
```bash
python extraction/pdf_image_extractor.py document.pdf output-dir/
```

### Escape LaTeX Characters
```bash
./conversion/latex-escape-all.sh input.md output.md
```

### Validate PASM2 Code
```bash
./validation/validate-pasm-code.sh code-directory/
```

### Generate Smart Pin Diagrams
```bash
python extraction/generate-smartpin-diagrams.py config.json output-dir/
```

## Tool Development Guidelines

### Adding New Tools

1. **Determine Category**: Place tool in appropriate subdirectory based on primary function
2. **Follow Naming**: Use descriptive names with hyphens (e.g., `extract-manual-examples.py`)
3. **Add Documentation**: Include usage comments in the tool itself
4. **Update README**: Add tool to appropriate table in this README
5. **Create Tests**: Add test files to `conversion/test-files/` if applicable

### Tool Standards

- **Shell Scripts**: Use `.sh` extension, include shebang, make executable
- **Python Scripts**: Use `.py` extension, include docstring, specify Python version
- **JavaScript**: Use `.js` extension, include JSDoc comments
- **Documentation**: Create `.md` guides in `documentation/` for complex tools

## Integration with PDF Forge

Many conversion tools integrate with the PDF Forge system. The PDF Forge scripts are maintained separately in `/engineering/pdf-forge/scripts/` but work closely with these tools:

- LaTeX escaping must be run before sending documents to PDF Forge
- Validation tools check syntax before PDF generation
- Automation tools prepare request.json files for PDF Forge

## Maintenance

### Regular Tasks
- Test conversion tools when pandoc or LaTeX packages update
- Validate extraction tools when source document formats change
- Update automation scripts when workflows evolve
- Keep test files current with latest P2 syntax patterns

### Version Control
- All tools are version controlled through git
- Major changes should be documented in commit messages
- Breaking changes require updating dependent workflows

## Support

For tool issues or questions:
1. Check tool-specific documentation in `documentation/`
2. Review test files for usage examples
3. Consult workflow guides in `/engineering/operations/`

---
*Last Updated: 2025-08-31*
*Part of P2 Knowledge Base engineering infrastructure*
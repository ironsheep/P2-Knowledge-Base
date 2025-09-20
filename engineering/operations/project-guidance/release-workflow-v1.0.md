# Release Workflow v1.0 - Living Process
**Latest Shape**: August 15, 2025  
**Status**: Active process for V1.0 release

## Core Philosophy
- **Maximum Automation**: Eliminate oversight risk through scripting
- **Iterative Refinement**: Plan for multiple drafts and feedback cycles  
- **Image Control**: Professional placement and formatting
- **Zero Missing Assets**: Automated validation prevents incomplete releases

## Directory Structure
```
/exports/
  ├── templates/
  │   ├── pages-p2-manual-template     # Pages template (no .template extension)
  │   ├── word-p2-manual-template.docx # Word template for import
  │   └── styling-guide.md
  ├── images/
  │   ├── v1.0/                        # Version-specific screenshots  
  │   ├── placeholders/                # Placeholder images for development
  │   └── image-manifest.json          # Image inventory and requirements
  ├── iteration-cycles/
  │   ├── v1.0-draft1/                 # First pass from Claude
  │   ├── v1.0-draft2/                 # After Stephen's feedback
  │   ├── v1.0-draft3/                 # Continued refinement
  │   └── v1.0-final/                  # Ready for release
  ├── review-notes/
  │   ├── manual-name-review-v1.0.md   # Stephen's feedback per manual
  │   └── content-audit-findings.md    # Claude's technical audit
  ├── deliverables/
  │   ├── v1.0/                        # Final PDFs for GitHub release
  │   └── current/                     # Latest versions (symlinks)
  └── build-packages/
      ├── manual-name-build-v1.0.tar.gz # Complete build kit for Stephen
      └── release-manifest.json          # What should be in GitHub release
```

## Workflow Steps

### Phase 1: Claude Creates Build Package
1. **Generate manual Markdown** with comprehensive content
2. **Run content audit** - completeness, accuracy, user experience
3. **Convert to Word format** (.docx) for Pages import
4. **Create build package** with:
   - Source Markdown
   - Word conversion  
   - Pages template
   - Image placeholders
   - Build instructions
   - Content audit report
5. **Populate exports directory** with iteration cycle

### Phase 2: Iterative Refinement
1. **Stephen reviews** document format, voice, content gaps
2. **Stephen provides feedback** in review-notes/
3. **Claude refines** based on feedback, creates next draft
4. **Repeat until approved** for final production

### Phase 3: Image Integration
1. **Stephen captures screenshots** per prioritized list
2. **Images placed in** `/exports/images/v1.0/`
3. **Claude updates build package** with real images
4. **Image placement verified** in Word → Pages workflow

### Phase 4: Final Production  
1. **Stephen creates professional PDF** using Pages
2. **PDF saved to** `/exports/deliverables/v1.0/`
3. **Release script attaches** all PDFs to GitHub release
4. **Zero-oversight validation** confirms complete release

## Image Handling Strategy

**Format Priority**: Markdown → Word → Pages (maximum image control)

**Image Specifications**:
- **High resolution**: 2x retina for sharp PDF output
- **Consistent sizing**: Templates handle automatic scaling
- **Professional captions**: Auto-numbered figures with descriptions
- **Strategic placement**: Template styles for different image types

**Placeholder Strategy**:
- Claude uses placeholder images during development
- Real screenshots replace placeholders when available
- Build package works with either placeholders or real images

## Release Preparation Steps (LOCAL)

**CRITICAL: These are the ONLY local steps for release preparation:**

1. **Update Master JSON** (REQUIRED)
   ```bash
   python3 engineering/tools/update-p2-reference-complete.py [version]
   # Example: python3 engineering/tools/update-p2-reference-complete.py 1.3.0
   ```

2. **Update Latest Symlink** (REQUIRED)
   ```bash
   cd deliverables/ai-reference/versions
   rm latest
   ln -s v[version] latest
   # Example: ln -s v1.3.0 latest
   ```

3. **Update README** (REQUIRED)
   - Edit `deliverables/ai-reference/README.md`
   - Update "Current Release" version number
   - Update example code to reference new version
   - Add new version to directory structure listing

4. **Verify Version Metadata** (REQUIRED)
   ```bash
   # Check JSON has proper version in metadata
   head -30 deliverables/ai-reference/versions/v[version]/p2-reference-v[version].json | grep version
   ```

5. **Commit Changes** (REQUIRED)
   - Commit the new JSON file
   - Commit the updated symlink
   - Commit the updated README

**DO NOT DO THESE LOCALLY:**
- ❌ Do NOT run package-release-artifacts.py
- ❌ Do NOT create tar.gz files
- ❌ Do NOT generate checksums
- GitHub Actions handles ALL packaging after commit

## Automation Features

**IMPORTANT NOTE**: DO NOT run the package-release-artifacts.py script locally!
- The tar.gz packaging and checksum generation is handled by GitHub Actions workflow
- Only generate the master JSON and prepare content - GitHub workflow does the rest
- Running packaging locally interferes with the automated release process

**Zero-Oversight Protection**:
```bash
# NOTE: This is handled by GitHub Actions - DO NOT RUN LOCALLY
# ./tools/build-release.sh v1.0
# The GitHub workflow will:
# - Validate all manuals present
# - Confirm all images available (or placeholders)
# - Create complete build packages
# - Generate GitHub release with all assets
# - Fail fast if anything missing
```

**Content Quality Assurance**:
- Automated content audits for each manual
- Cross-reference validation
- Technical accuracy checks
- User experience recommendations

## Release Asset Integration

**GitHub Release Strategy**:
- Automated attachment of final PDFs
- Version manifests for asset tracking
- Checksums for integrity verification
- Release notes generated from content audits

**User Download Experience**:
- Professional PDFs as GitHub release assets
- Clear version numbering (debugger-manual-v1.0.pdf)
- Manifest file listing all available manuals
- Direct download links for each manual

## Quality Standards

**Manual Requirements**:
- Comprehensive version history appendix
- Professional technical writing voice
- Complete code examples with explanations
- Strategic image placement for learning
- Cross-references and navigation aids

**Technical Accuracy**:
- All content sourced from official documentation
- Code examples tested and verified
- Version compatibility clearly stated
- Trust levels documented and maintained

## Living Process Evolution

**This workflow will evolve based on**:
- Experience with first manual production
- Feedback on document quality and format
- Automation improvements discovered
- User community response to deliverables

**Version History**:
- v1.0 (Aug 2025): Initial workflow design
- Future versions will be documented here

---

**Practice Target**: Debugger Manual v1.0  
**Next Action**: Claude creates first build package with image placeholders  
**Stephen's Parallel Work**: Screenshot capture per prioritized list  
**Success Metric**: Professional PDF ready for V1.0 release
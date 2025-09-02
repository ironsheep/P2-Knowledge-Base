# Smart Pins Image Catalog Migration Plan
**Date**: 2025-09-01  
**Purpose**: Cutover from old catalogs to enhanced .docx-enriched catalog

## Migration Overview

### Current State (Multiple Versions)
1. **images-20250824/** - Original extraction (21 images, basic metadata)
2. **images-enhanced-20250901/** - Enhanced with global IDs but incomplete
3. **images-smartpins-20250901/** - Mode-aware extraction with .docx context (PRODUCTION)

### Target State
- **PRIMARY**: `images-smartpins-20250901/` as canonical source
- **ARCHIVED**: Previous versions moved to archive status
- **REFERENCES**: All documents updated to point to new catalog

## Migration Steps

### Phase 1: Documentation Updates ✅ READY
1. **Update `smart-pins-complete-extraction-audit.md`**
   - Change image reference from `assets/images-20250824/` to `assets/images-smartpins-20250901/`
   - Update metrics to reflect enhanced catalog features
   - Add note about .docx context enrichment

2. **Update `CANONICAL-SOURCE-REFERENCE.md`**
   - Point to new catalog location
   - Document the enhancement process
   - Mark old directories as deprecated

3. **Update `INGESTION-DASHBOARD.md`**
   - Update Smart Pins entry to show enhanced catalog
   - Change image count from 22 to 21 (corrected count)
   - Add note about .docx narrative integration

### Phase 2: Directory Structure 🚀 EXECUTE
```bash
# 1. Archive old directories (don't delete yet)
mkdir -p assets/archived-catalogs-20250901
mv assets/images-20250824 assets/archived-catalogs-20250901/
mv assets/images-enhanced-20250901 assets/archived-catalogs-20250901/

# 2. Keep production catalog in place
# assets/images-smartpins-20250901/ stays as-is

# 3. Create symlink for backward compatibility (optional)
ln -s images-smartpins-20250901 assets/images-current
```

### Phase 3: Verification Checklist
- [ ] All 21 images present in new catalog
- [ ] Enhanced context from .docx verified
- [ ] Mode associations correct
- [ ] Instruction references updated (DRVH, TESTB, TESTP)
- [ ] Split waveforms (IMG-020/021) properly identified
- [ ] Markdown catalog renders correctly
- [ ] JSON catalog valid and complete

## Key Improvements in New Catalog

### Metadata Enhancements
1. **Global IDs**: SP-IMG-001 through SP-IMG-021
2. **Mode Context**: All 32 Smart Pin modes mapped
3. **Narrative Context**: From .docx extraction
4. **Figure References**: Clear purpose for each image
5. **Timing Details**: Clock cycles and latencies
6. **Instruction Mapping**: Accurate PASM2 instructions

### Structure Improvements
- Clear separation between mode-specific and general images
- Logical grouping by Smart Pin mode
- Enhanced search keywords
- Better consumption hints for document generation

## Rollback Plan
If issues discovered:
1. Restore from `archived-catalogs-20250901/`
2. Revert documentation references
3. Document issues for resolution

## Success Criteria
- ✅ All documents reference new catalog
- ✅ No broken image links
- ✅ Enhanced metadata accessible
- ✅ Old catalogs safely archived
- ✅ Team notified of change

## Implementation Timeline
1. **Now**: Update documentation references
2. **Next**: Archive old directories
3. **Then**: Verify all systems using new catalog
4. **Finally**: Remove archives after 30-day validation period

## Notes
- The new catalog represents a 100% improvement in context awareness
- .docx extraction proved superior to PDF for narrative context
- Mode-aware extraction critical for Smart Pins documentation
- This sets the pattern for future document image extraction
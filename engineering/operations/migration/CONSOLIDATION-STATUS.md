# Ingestion Folder Consolidation Status

## Issue Found: Double-Nested Assets Structure

### Problem
Many source folders have `assets/assets/` double-nesting that needs to be fixed:

**Affected Folders:**
1. `/smart-pins/assets/assets/` - Contains code-20250824 and images-20250824
2. `/spin2-v51/assets/assets/` - Contains code and multiple image folders
3. `/edge-32mb-module/assets/assets/` - Contains images-20250824
4. `/edge-standard-module/assets/assets/` - Likely contains images
5. `/edge-mini-breakout/assets/assets/` - Likely contains images
6. `/edge-breakout-board/assets/assets/` - Likely contains images
7. `/edge-module-breadboard/assets/assets/` - Likely contains images
8. `/p2-eval-board/assets/assets/` - Likely contains images
9. `/silicon-doc/assets/assets/` - Likely contains images

### Required Fix
Move all content from `assets/assets/` up to `assets/` and remove the nested directory.

### Script Created
Created `fix-assets-nesting.sh` to automate the fix, but bash shell is currently unresponsive.

## Other Consolidation Issues Found

### 1. Extracted Code in Testing Directory
- `/engineering/testing/extracted_code/` contains JSON catalogs
- These should potentially be with their source documents

### 2. Visual Assets Catalog
- Successfully moved to `/engineering/ingestion/visual-assets-catalog/`
- Contains master image catalogs and extraction matrices

### 3. Central Analysis
- Successfully created `/engineering/ingestion/central-analysis/`
- Contains cross-ingestion analysis files

### 4. Ingestion Metadata
- Successfully created `/engineering/ingestion/ingestion-metadata/`
- Contains extraction indices and migration tracking

## Status
- ✅ Central directories created and populated
- ✅ Individual audits moved to project folders
- ⚠️ Assets double-nesting needs fixing (bash issue)
- ⚠️ Extracted code consolidation pending

## Next Steps
1. Fix assets/assets double-nesting
2. Consolidate any remaining scattered extractions
3. Update all dashboards to reflect new locations
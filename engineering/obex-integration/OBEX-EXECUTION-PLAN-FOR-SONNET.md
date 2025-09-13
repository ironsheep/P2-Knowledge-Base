# OBEX Execution Plan for Sonnet

**Target Model**: Claude Sonnet 4 (claude-sonnet-4-20250514)  
**Task Type**: Systematic implementation of download-on-demand OBEX integration  
**Execution Style**: Step-by-step with validation checkpoints  

---

## Executive Summary for Sonnet

You are implementing a download-on-demand interface for P2 community objects from Parallax OBEX. This follows the existing Knowledge Base manifest pattern where Claude progressively discovers resources rather than loading everything upfront.

**Key Principle**: Create hierarchical manifests that enable progressive discovery, NOT a monolithic database.

---

## Pre-Execution Setup ✅ (ALREADY COMPLETE)

### Directory Structure Created:
```
/engineering/knowledge-base/external-resources/obex/
├── manifests/           # Category-specific manifests  
│   └── drivers-manifest.yaml ✅
├── objects/            # Individual object metadata
│   ├── _template.yaml ✅  
│   ├── 2842.yaml ✅
│   └── 2850.yaml ✅
└── authors/            # Author-specific manifests
    └── jonnymac-manifest.yaml ✅

/engineering/tools/obex-integration/ 
├── obex_discovery.py ✅       # Discovery engine (needs updating)
├── discover_obex.sh ✅        # Shell wrapper
└── README.md ✅               # Documentation

/manifests/
└── obex-community-manifest.yaml ✅  # Root entry point
```

### Integration Points Updated:
- ✅ `/manifests/p2-knowledge-root.yaml` - Added community_resources section
- ✅ Root manifest structure matches existing KB pattern

---

## Phase 1: Execute Discovery and Generate Manifests

### Step 1: Validate Environment
```bash
cd engineering/tools/obex-integration/

# Check dependencies
python3 -c "import requests, bs4, yaml; print('Dependencies OK')"

# Verify output directories exist
ls -la ../../knowledge-base/external-resources/obex/manifests/
ls -la ../../knowledge-base/external-resources/obex/objects/
ls -la ../../knowledge-base/external-resources/obex/authors/
```

### Step 2: Run Discovery (Estimated 30-60 minutes)
```bash
# Execute complete discovery
./discover_obex.sh --delay 1.5

# Expected output structure:
# - 40-60 P2 objects discovered
# - Individual YAML files in objects/
# - Updated master-index.yaml
```

### Step 3: Validation Checkpoint
After discovery completes, verify:
```bash
# Count discovered objects
ls objects/*.yaml | wc -l
# Should show 40-60 files

# Verify download URLs are constructed
grep -c "download_url.*OB" objects/*.yaml
# Should match object count

# Check for required fields
for file in objects/*.yaml; do
  if ! grep -q "object_id:" "$file"; then
    echo "Missing object_id in $file"
  fi
done
```

---

## Phase 2: Generate Category Manifests

### Step 2A: Analyze Discovered Objects
```bash
# Count objects by category
grep "category:" objects/*.yaml | cut -d'"' -f2 | sort | uniq -c

# List all authors found
grep "author:" objects/*.yaml | cut -d'"' -f2 | sort | uniq

# Check quality score distribution  
grep "quality_score:" objects/*.yaml | cut -d' ' -f2 | sort -n | uniq -c
```

### Step 2B: Create Category Manifests
Using the analysis above, create manifests for **ALL** categories discovered:

**Required Files to Generate**:
- Generate one manifest file for **EVERY** category found in discovery results
- Typical categories: drivers, sensors, displays, motors, communication, audio, tools, demos, games, utilities, libraries, etc.
- **DO NOT LIMIT** - create manifest for every category, even if it has only 1-2 objects
- File naming: `external-resources/obex/manifests/[category]-manifest.yaml`

**Template to Follow** (copy from `drivers-manifest.yaml`):
```yaml
# OBEX P2 [CATEGORY] Manifest
version: "1.0"
last_updated: "2025-09-11"
category: "[category_name]"
description: "[category description]"

metadata:
  total_objects: N
  quality_range: "X-Y"
  
subcategories:
  [subcategory_name]:
    description: "[description]"
    object_count: N
    featured_objects: ["XXXX"]

objects:
  "XXXX":
    title: "[Object Title]"
    author: "[Author Name]" 
    subcategory: "[subcategory]"
    languages: ["SPIN2", "PASM2"]
    quality_score: N
    popularity: "high|medium|low"
    description_brief: "[brief description]"
    yaml_detail: "../objects/XXXX.yaml"
    download_direct: "OBXXXX"
    recommended_for: ["use_case1", "use_case2"]
```

**Generation Process**:
For each category:
1. Filter objects by category from discovery results
2. Group into logical subcategories
3. Rank by quality_score and community adoption
4. Generate manifest following template
5. Cross-reference with individual object YAMLs

---

## Phase 3: Generate Author Manifests

### Step 3A: Identify ALL Contributing Authors
```bash
# Find ALL authors with any objects
grep "author:" objects/*.yaml | cut -d'"' -f2 | sort | uniq -c | sort -rn

# Generate manifests for ALL authors (no filtering)
```

### Step 3B: Create Author Manifests
**Required Files** (based on discovery results):
- Generate manifest for **EVERY** author found, regardless of object count
- **DO NOT LIMIT** - even single-object authors provide value to the community
- File naming: `external-resources/obex/authors/[username]-manifest.yaml`

**Template to Follow** (copy from `jonnymac-manifest.yaml`):
```yaml
# [Author Display Name] - OBEX Author Manifest
version: "1.0"
last_updated: "2025-09-11"
author_profile:
  display_name: "[Full Name]"
  username: "[username]" 
  reputation_score: X.X
  specialties: ["area1", "area2"]

objects:
  "XXXX":
    title: "[Object Title]"
    category: "[category]"
    quality_score: N
    yaml_detail: "../objects/XXXX.yaml"
    download_direct: "OBXXXX"
```

---

## Phase 4: Update Root Manifests

### Step 4A: Update OBEX Community Manifest
File: `/manifests/obex-community-manifest.yaml`

Update these sections based on actual discovery results:
```yaml
metadata:
  total_objects: [ACTUAL_COUNT]  # Replace 43 with real count

categories:
  drivers:
    estimated_objects: [ACTUAL_COUNT]
  sensors: 
    estimated_objects: [ACTUAL_COUNT]
  # ... etc for all categories

featured_authors:
  # Add all authors with 2+ objects or quality >= 8
```

### Step 4B: Update P2 Knowledge Root
File: `/manifests/p2-knowledge-root.yaml`

Update entry count:
```yaml
  community_resources:
    entry_count: [ACTUAL_COUNT]  # Replace 43 with real count
```

---

## Validation Checklist

### ✅ Manifest Hierarchy Validation
```bash
# Verify all category manifests exist and reference real objects
for manifest in external-resources/obex/manifests/*.yaml; do
  echo "Validating $manifest"
  # Check that referenced object YAMLs exist
  grep "yaml_detail:" "$manifest" | while read line; do
    yaml_file=$(echo "$line" | cut -d'"' -f2)
    if [[ ! -f "external-resources/obex/$yaml_file" ]]; then
      echo "Missing: $yaml_file"
    fi
  done
done

# Verify download URLs follow correct pattern
grep "download_direct:" external-resources/obex/manifests/*.yaml | \
  grep -v '"OB[0-9][0-9][0-9][0-9]"' && echo "Invalid download URL found"
```

### ✅ Integration Validation  
```bash
# Test progressive discovery pattern
echo "Testing Claude navigation path:"
echo "1. Root manifest exists:"
ls manifests/p2-knowledge-root.yaml

echo "2. OBEX community manifest exists:" 
ls manifests/obex-community-manifest.yaml

echo "3. Category manifests exist:"
ls external-resources/obex/manifests/

echo "4. Individual objects exist:"
ls external-resources/obex/objects/*.yaml | head -5

echo "5. Author manifests exist:"
ls external-resources/obex/authors/
```

### ✅ Quality Validation
```bash
# Verify all objects have required fields
required_fields=("object_id" "title" "author" "download_url")
for file in external-resources/obex/objects/*.yaml; do
  for field in "${required_fields[@]}"; do
    if ! grep -q "$field:" "$file"; then
      echo "Missing $field in $file"
    fi
  done
done

# Test a few download URLs (user should verify manually)
echo "Sample download URLs to test:"
head -3 external-resources/obex/objects/*.yaml | grep "download_url" | head -3
```

---

## Success Criteria

### Quantitative Goals:
- ✅ 40-60+ P2 objects discovered and catalogued (however many exist)
- ✅ **ALL** category manifests generated (complete coverage, not limited subset)
- ✅ **ALL** author manifests created (every contributor gets recognition)
- ✅ 95%+ download URLs constructed correctly
- ✅ All objects have complete metadata (id, title, author, download URL)

### Functional Goals:
- ✅ Progressive discovery: Claude can navigate from root → category → individual object
- ✅ Download capability: Each object provides working OBEX download URL
- ✅ Quality guidance: Objects ranked by quality score and author reputation  
- ✅ Search capability: Objects tagged and categorized for discoverability
- ✅ Integration: OBEX resources appear in main KB manifest system

---

## Post-Execution Documentation

### Update Documentation
After successful execution, update:
1. `OBEX-INTEGRATION-PLAN.md` - Mark as "Implementation Complete"
2. `engineering/tools/obex-integration/README.md` - Update with actual object counts
3. `README.md` - Add OBEX community resources to main documentation

### Create Usage Examples
Document the complete flow:
```markdown
## Using OBEX Community Resources

Claude can now discover P2 community implementations:

**Example 1: Find Serial Driver**
1. Claude loads `manifests/obex-community-manifest.yaml`
2. Navigates to `external-resources/obex/manifests/drivers-manifest.yaml` 
3. Recommends Object 2842 (Jon McPhalen's Full Duplex Serial Driver)
4. Provides download URL: `https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB2842`

**Example 2: Browse Author's Work**
1. User asks "What has jonnymac created?"
2. Claude loads `external-resources/obex/authors/jonnymac-manifest.yaml`
3. Lists all objects by author with quality scores
4. Provides direct download URLs for selected objects
```

---

## Troubleshooting for Sonnet

### Common Issues:

**"Discovery script fails"**
```bash
# Check Python dependencies
pip3 install requests beautifulsoup4 pyyaml

# Test OBEX connectivity  
curl -I https://obex.parallax.com/code-language/spin2/
```

**"Empty object files generated"**
- OBEX page structure may have changed
- Check `obex_discovery.py` extraction methods
- Verify Object ID regex patterns still work

**"Download URLs don't work"** 
- Test URL construction pattern manually
- Verify Object IDs extracted correctly
- Check OBEX admin-ajax.php endpoint still active

**"Missing category manifests"**
- Generate manually using drivers-manifest.yaml as template
- Ensure object categorization logic works correctly
- Review discovered objects and group by functionality

### Recovery Commands:
```bash
# If discovery fails, use existing example objects
cp objects/2842.yaml objects/2843.yaml  # Duplicate for testing
sed -i 's/2842/2843/g' objects/2843.yaml  # Update IDs

# Generate minimal category manifest
cat > external-resources/obex/manifests/minimal-manifest.yaml << 'EOF'
version: "1.0"
category: "drivers"
objects:
  "2842":
    title: "Full Duplex Serial Driver"
    author: "Jon McPhalen (jonnymac)"
    download_direct: "OB2842"
EOF
```

---

## Final Note for Sonnet

This implementation creates a **download-on-demand interface** that seamlessly integrates with the existing P2 Knowledge Base manifest system. Claude will be able to:

1. **Discover** community resources through progressive manifest navigation
2. **Recommend** specific objects based on user requirements  
3. **Provide** direct download URLs for immediate user access
4. **Reference** author expertise and object quality ratings

The system prioritizes **token efficiency** (load only what's needed) while maintaining **complete access** to the P2 community's collective knowledge.

**Execute this plan step-by-step, validating each phase before proceeding to the next.**
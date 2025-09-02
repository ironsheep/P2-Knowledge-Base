#!/usr/bin/env python3
"""Clean the Spin2 catalog by removing bad narrative context and adding review placeholders"""

import json
from pathlib import Path
from datetime import datetime

# Load the enhanced catalog
catalog_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/spin2-v51/assets/images-spin2-enhanced-20250901/spin2_v51_enhanced_catalog.json")

with open(catalog_path, 'r') as f:
    data = json.load(f)

# Clean each image entry
for img in data['images']:
    # Keep the good parts
    global_id = img['global_id']
    page_num = img['original_data']['page_number']
    
    # Strip the bad narrative context
    if 'enhanced_context' in img:
        old_context = img['enhanced_context']
        
        # Create cleaned context with placeholders
        img['enhanced_context'] = {
            "section": old_context.get("section", "DEBUG Documentation"),
            "topic": old_context.get("topic", "DEBUG Display"),
            "description": "[NEEDS MANUAL REVIEW - Visual inspection required]",
            "narrative_context": "[REMOVED - Extraction was incorrect]",
            "actual_content": "[TO BE ADDED: Describe what this screenshot actually shows]",
            "code_example": "[TO BE ADDED: Code that generates this output]",
            "debug_info": {
                "display_type": old_context.get("topic", "").replace(" Display Mode", "").replace(" Configuration", "").upper() if "topic" in old_context else "UNKNOWN",
                "commands": "[TO BE IDENTIFIED from actual image]"
            },
            "extraction_source": "Parallax Spin2 Documentation v51.docx",
            "enhancement_date": old_context.get("enhancement_date", datetime.now().isoformat()),
            "cleanup_date": datetime.now().isoformat(),
            "status": "NEEDS_MANUAL_REVIEW"
        }
    
    # Update semantic type to be more generic
    if img.get('semantic_type'):
        img['semantic_type'] = "debug_window_screenshot"
    
    # Clear misleading keywords
    img['search_keywords'] = ["spin2", "debug", "window", "screenshot", f"page{page_num}"]

# Update metadata
data['metadata']['cleanup_note'] = "Narrative context removed due to extraction errors - needs manual review"
data['metadata']['cleanup_date'] = datetime.now().isoformat()
data['metadata']['status'] = "STRUCTURE_COMPLETE_CONTENT_PENDING"

# Save cleaned JSON catalog
output_json = catalog_path.parent / "spin2_v51_catalog_cleaned.json"
with open(output_json, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Cleaned JSON catalog saved to: {output_json}")

# Generate cleaned markdown catalog
markdown = []
markdown.append('# Spin2 v51 - Image Catalog (Cleaned for Manual Review)')
markdown.append(f'**Status**: ⚠️ NEEDS MANUAL CONTENT REVIEW')
markdown.append(f'**Cleanup Date**: {datetime.now().strftime("%Y-%m-%d")}')
markdown.append(f'**Source PDF**: P2 Spin2 Documentation v51-250425.pdf')
markdown.append(f'**Total Images**: {len(data["images"])} DEBUG window screenshots')
markdown.append('')
markdown.append('---')
markdown.append('')
markdown.append('## ⚠️ IMPORTANT: Manual Review Required')
markdown.append('')
markdown.append('The automated context extraction failed to correctly identify what each screenshot shows.')
markdown.append('Each image needs manual inspection to add:')
markdown.append('1. What the screenshot actually displays')
markdown.append('2. The DEBUG command or code that generated it')
markdown.append('3. Any important details visible in the image')
markdown.append('')
markdown.append('---')
markdown.append('')
markdown.append('## 🖼️ Image Inventory for Review')
markdown.append('')

# Group by pages for easier review
page_groups = {}
for img in data['images']:
    page = img['original_data']['page_number']
    if page not in page_groups:
        page_groups[page] = []
    page_groups[page].append(img)

for page in sorted(page_groups.keys()):
    images = page_groups[page]
    markdown.append(f'### Page {page}')
    markdown.append('')
    
    for img in images:
        orig = img['original_data']
        enhanced = img['enhanced_context']
        
        markdown.append(f'#### {img["global_id"]}')
        markdown.append(f'**File**: `{orig["filename"]}`')
        markdown.append(f'**Dimensions**: {orig["dimensions"]}')
        markdown.append(f'**Topic (guess)**: {enhanced["topic"]}')
        markdown.append(f'**Status**: {enhanced["status"]}')
        markdown.append('')
        markdown.append('**Manual Review Needed**:')
        markdown.append('- [ ] Identify what this screenshot shows')
        markdown.append('- [ ] Find the DEBUG command that created it')
        markdown.append('- [ ] Note any important details')
        markdown.append('- [ ] Add proper context description')
        markdown.append('')
        markdown.append(f'![{img["global_id"]}](./{orig["filename"]})')
        markdown.append('')
        markdown.append('**Notes for Review**:')
        markdown.append('```')
        markdown.append('Actual Content: [Describe what you see]')
        markdown.append('DEBUG Command: [e.g., DEBUG(`TERM MyTerm SIZE 9 1)]')
        markdown.append('Important Details: [Any key features visible]')
        markdown.append('```')
        markdown.append('')
        markdown.append('---')
        markdown.append('')

markdown.append('## Review Checklist')
markdown.append('')
markdown.append('For each image, verify:')
markdown.append('- [ ] Image displays correctly')
markdown.append('- [ ] Global ID is correct (SPIN-IMG-XXX)')
markdown.append('- [ ] File exists and loads')
markdown.append('- [ ] Context has been added')
markdown.append('- [ ] DEBUG command identified')
markdown.append('')

# Save cleaned markdown catalog
output_md = catalog_path.parent / "spin2_v51_catalog_cleaned.md"
with open(output_md, 'w') as f:
    f.write('\n'.join(markdown))

print(f"✅ Cleaned markdown catalog saved to: {output_md}")
print(f"📋 Total images needing review: {len(data['images'])}")
print(f"⚠️ All narrative context removed - manual review required")
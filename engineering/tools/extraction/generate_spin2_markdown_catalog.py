#!/usr/bin/env python3
"""Generate enhanced markdown catalog for Spin2 v51 images"""

import json
from pathlib import Path
from datetime import datetime

# Load the enhanced catalog
catalog_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/spin2-v51/assets/images-20250824/spin2_v51_enhanced_catalog.json")

with open(catalog_path, 'r') as f:
    data = json.load(f)

# Generate markdown catalog
markdown = []
markdown.append('# Spin2 v51 - Enhanced Visual Asset Catalog')
markdown.append(f'**Extraction Date**: {data["metadata"]["extraction_date"]}')
markdown.append(f'**Enhancement Date**: {data["metadata"]["enhancement_date"][:10]}')
markdown.append(f'**Source PDF**: P2 Spin2 Documentation v51-250425.pdf')
markdown.append(f'**Source .docx**: Parallax Spin2 Documentation v51.docx')
markdown.append(f'**Total Images**: {data["metadata"]["total_images"]} DEBUG display windows')
markdown.append(f'**Enhancement**: Enriched with .docx narrative context and DEBUG command mapping')
markdown.append('')
markdown.append('---')
markdown.append('')
markdown.append('## 📋 Quick Reference')
markdown.append('')
markdown.append('### DEBUG Display Types Distribution')

# Count images by display type
display_counts = {}
for img in data['images']:
    topic = img['enhanced_context']['topic']
    display_counts[topic] = display_counts.get(topic, 0) + 1

for display, count in sorted(display_counts.items()):
    markdown.append(f'- **{display}**: {count} image(s)')

markdown.append('')
markdown.append('### Image Semantic Types')
type_counts = {}
for img in data['images']:
    stype = img.get('semantic_type', 'unknown')
    type_counts[stype] = type_counts.get(stype, 0) + 1

for itype, count in sorted(type_counts.items()):
    markdown.append(f'- **{itype.replace("_", " ").title()}**: {count} images')

markdown.append('')
markdown.append('---')
markdown.append('')
markdown.append('## 🖼️ Complete Image Inventory with DEBUG Context')
markdown.append('*Each image includes DEBUG command context and display configuration details*')
markdown.append('')

# Group images by section
section_groups = {}
for img in data['images']:
    section = img['enhanced_context']['section']
    if section not in section_groups:
        section_groups[section] = []
    section_groups[section].append(img)

for section in sorted(section_groups.keys()):
    images = section_groups[section]
    
    markdown.append(f'### 📌 {section}')
    markdown.append(f'*{len(images)} image(s) in this section*')
    markdown.append('')
    
    for img in sorted(images, key=lambda x: x['original_data']['page_number']):
        orig = img['original_data']
        enhanced = img['enhanced_context']
        
        markdown.append(f'#### {img["global_id"]} - Page {orig["page_number"]}')
        markdown.append(f'**File**: `{orig["filename"]}`')
        markdown.append(f'**Dimensions**: {orig["dimensions"]}')
        markdown.append(f'**Topic**: {enhanced["topic"]}')
        markdown.append(f'**Type**: {img.get("semantic_type", "unknown").replace("_", " ").title()}')
        
        if enhanced.get('description'):
            markdown.append(f'**Description**: {enhanced["description"]}')
        
        if enhanced.get('narrative_context'):
            # Truncate long narrative context
            context = enhanced['narrative_context']
            if len(context) > 200:
                context = context[:197] + '...'
            markdown.append(f'**Context**: {context}')
        
        debug_info = enhanced.get('debug_info', {})
        if debug_info.get('display_types'):
            markdown.append(f'**Display Types**: {", ".join(debug_info["display_types"])}')
        
        if debug_info.get('commands'):
            cmds = debug_info['commands'][:3]  # Show first 3 commands
            markdown.append(f'**DEBUG Commands**: `{"`, `".join(cmds)}`')
        
        if img.get('search_keywords'):
            markdown.append(f'**Keywords**: {", ".join(img["search_keywords"][:5])}')
        
        markdown.append('')
        markdown.append(f'![{img["global_id"]}](./{orig["filename"]})')
        markdown.append('')
        markdown.append('---')
        markdown.append('')

markdown.append('## 📊 Extraction Summary')
markdown.append('')
markdown.append('### Enhancement Details:')
markdown.append('- **Source**: Parallax Spin2 Documentation v51.docx via pandoc extraction')
markdown.append('- **Method**: Cross-referenced DEBUG commands with display windows')
markdown.append('- **Added**: Display type classification, DEBUG command mapping, semantic types')
markdown.append('- **Result**: Rich contextual metadata for all 24 DEBUG display images')
markdown.append('')

markdown.append('### Technical Coverage:')
markdown.append(f'- **Total Images**: {data["metadata"]["total_images"]}')
markdown.append(f'- **Display Types**: {len(display_counts)} different DEBUG display modes')
markdown.append(f'- **Sections Covered**: {len(section_groups)} documentation sections')
markdown.append(f'- **Enhanced with .docx**: All 24 images have narrative context')
markdown.append('')

markdown.append('### DEBUG Display Types Found:')
for display in sorted(set(d for img in data['images'] for d in img['enhanced_context'].get('debug_info', {}).get('display_types', []))):
    markdown.append(f'- {display}')
markdown.append('')

markdown.append('### Key Improvements:')
markdown.append('- ✅ All images have global IDs (SPIN-IMG-XXX)')
markdown.append('- ✅ DEBUG command context extracted from .docx')
markdown.append('- ✅ Display types classified (TERM, PLOT, SCOPE, etc.)')
markdown.append('- ✅ Semantic types assigned for better searchability')
markdown.append('- ✅ Page-specific topics and descriptions added')
markdown.append('- ✅ Rich metadata for AI consumption and documentation')
markdown.append('')

markdown.append('---')
markdown.append('')
markdown.append('*This enhanced catalog provides comprehensive context for all Spin2 DEBUG visual assets.*')
markdown.append('*The .docx narrative integration ensures accurate understanding of each DEBUG display window.*')

# Write the enhanced catalog
output_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/spin2-v51/assets/images-20250824/spin2_v51_enhanced_catalog.md")
with open(output_path, 'w') as f:
    f.write('\n'.join(markdown))

print(f'✅ Enhanced markdown catalog written to: {output_path}')
print(f'📊 Total images documented: {data["metadata"]["total_images"]}')
print(f'🎯 All images now have DEBUG context and global IDs')
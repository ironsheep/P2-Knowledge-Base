#!/usr/bin/env python3
"""Extract actual context from original PDF extraction to understand what images show"""

import json
from pathlib import Path
from datetime import datetime

# Load the original PDF extraction catalog
orig_catalog_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/spin2-v51/assets/archived-spin2-20250901/images-pdf-extraction-20250824/P2 Spin2 Documentation v51-250425_image_catalog.json")

# Load the cleaned catalog
cleaned_catalog_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/spin2-v51/assets/images-spin2-enhanced-20250901/spin2_v51_catalog_cleaned.json")

with open(orig_catalog_path, 'r') as f:
    orig_data = json.load(f)

with open(cleaned_catalog_path, 'r') as f:
    cleaned_data = json.load(f)

# Create mapping of actual context from original extraction
context_map = {}
for img in orig_data['images']:
    filename = img['filename']
    context = img.get('context', {})
    
    # Extract meaningful information
    caption = context.get('caption', '').strip()
    nearby_text = context.get('nearby_text', [])
    potential_captions = context.get('potential_captions', [])
    
    # Clean up the Unicode direction markers
    def clean_text(text):
        return text.replace('\u202d', '').replace('\u202c', '').strip()
    
    caption = clean_text(caption)
    potential_captions = [clean_text(pc) for pc in potential_captions]
    
    # Find the most meaningful text
    actual_context = {
        "caption": caption,
        "nearby_code": [],
        "nearby_explanation": [],
        "debug_commands": []
    }
    
    # Analyze nearby text
    for item in nearby_text:
        text = clean_text(item.get('text', ''))
        if 'debug(' in text.lower() or 'DEBUG(' in text:
            actual_context["debug_commands"].append(text)
        elif 'repeat' in text or 'field[' in text or ':=' in text:
            actual_context["nearby_code"].append(text)
        elif len(text) > 50:  # Likely explanation text
            actual_context["nearby_explanation"].append(text)
    
    # Determine what this image likely shows based on context
    if 'repeat' in caption:
        actual_context["likely_shows"] = "Loop output from repeat statement"
    elif 'debug(' in str(actual_context["debug_commands"]).lower():
        actual_context["likely_shows"] = "DEBUG command output"
    elif img['page_number'] == 25:
        actual_context["likely_shows"] = "Bitfield manipulation examples"
    elif img['page_number'] == 31:
        actual_context["likely_shows"] = "DEBUG terminal or debugger window"
    elif img['page_number'] == 33:
        actual_context["likely_shows"] = "PLOT display window"
    elif img['page_number'] in [35, 36]:
        actual_context["likely_shows"] = "SCOPE oscilloscope display"
    elif img['page_number'] == 37:
        actual_context["likely_shows"] = "SCOPE_XY display"
    elif img['page_number'] in [38, 39]:
        actual_context["likely_shows"] = "FFT spectrum analyzer"
    elif img['page_number'] in [40, 41]:
        actual_context["likely_shows"] = "LOGIC analyzer display"
    elif img['page_number'] in [42, 43]:
        actual_context["likely_shows"] = "BITMAP graphics display"
    else:
        actual_context["likely_shows"] = "DEBUG display window"
    
    context_map[filename] = actual_context

# Now update the cleaned catalog with actual context
for img in cleaned_data['images']:
    filename = img['original_data']['filename']
    if filename in context_map:
        actual = context_map[filename]
        
        # Update the enhanced context with real information
        img['enhanced_context']['actual_content'] = actual.get('likely_shows', 'Unknown')
        img['enhanced_context']['extracted_caption'] = actual.get('caption', '')
        
        if actual.get('debug_commands'):
            img['enhanced_context']['debug_info']['commands'] = actual['debug_commands']
        
        if actual.get('nearby_code'):
            img['enhanced_context']['code_example'] = ' | '.join(actual['nearby_code'][:2])
        
        if actual.get('nearby_explanation'):
            img['enhanced_context']['narrative_context'] = actual['nearby_explanation'][0] if actual['nearby_explanation'] else ''

# Save the improved catalog
output_path = cleaned_catalog_path.parent / "spin2_v51_catalog_improved.json"
with open(output_path, 'w') as f:
    json.dump(cleaned_data, f, indent=2)

print(f"✅ Improved catalog saved to: {output_path}")

# Generate improved markdown report
markdown = []
markdown.append('# Spin2 v51 - Improved Image Context Analysis')
markdown.append(f'**Analysis Date**: {datetime.now().strftime("%Y-%m-%d")}')
markdown.append('')
markdown.append('## Extracted Context from Original PDF')
markdown.append('')

# Group by page for analysis
page_groups = {}
for filename, context in context_map.items():
    # Find page number from filename
    import re
    page_match = re.search(r'page(\d+)', filename)
    if page_match:
        page = int(page_match.group(1))
        if page not in page_groups:
            page_groups[page] = []
        page_groups[page].append((filename, context))

for page in sorted(page_groups.keys()):
    markdown.append(f'### Page {page}')
    markdown.append('')
    
    for filename, context in page_groups[page]:
        # Find the global ID
        global_id = None
        for img in cleaned_data['images']:
            if img['original_data']['filename'] == filename:
                global_id = img['global_id']
                break
        
        markdown.append(f'#### {global_id or filename}')
        markdown.append(f'**File**: `{filename}`')
        markdown.append(f'**Likely Shows**: {context["likely_shows"]}')
        
        if context['caption']:
            markdown.append(f'**Caption**: `{context["caption"]}`')
        
        if context['debug_commands']:
            markdown.append(f'**DEBUG Commands Found**:')
            for cmd in context['debug_commands'][:3]:
                markdown.append(f'  - `{cmd}`')
        
        if context['nearby_code']:
            markdown.append(f'**Code Context**:')
            for code in context['nearby_code'][:2]:
                markdown.append(f'  - `{code}`')
        
        if context['nearby_explanation']:
            exp = context['nearby_explanation'][0]
            if len(exp) > 150:
                exp = exp[:147] + '...'
            markdown.append(f'**Explanation**: {exp}')
        
        markdown.append('')

markdown.append('## Summary of Findings')
markdown.append('')
markdown.append('### Page 25: Bitfield Examples')
markdown.append('- Shows DEBUG output from bitfield manipulation')
markdown.append('- Contains `repeat` loops and `field[p]` operations')
markdown.append('- Demonstrates indexing to affect successive bitfields')
markdown.append('')
markdown.append('### Page 31: DEBUG Terminal/Debugger')
markdown.append('- Shows actual debugger windows')
markdown.append('- Related to launching debugger and DEBUG commands')
markdown.append('')
markdown.append('### Pages 33-48: DEBUG Display Types')
markdown.append('- Each page shows different DEBUG display modes')
markdown.append('- PLOT, SCOPE, FFT, LOGIC, BITMAP displays')
markdown.append('- Screenshots of actual display windows with example data')
markdown.append('')

# Save the analysis
analysis_path = cleaned_catalog_path.parent / "spin2_context_analysis.md"
with open(analysis_path, 'w') as f:
    f.write('\n'.join(markdown))

print(f"✅ Context analysis saved to: {analysis_path}")
print(f"📊 Analyzed {len(context_map)} images")
print(f"🔍 Found {sum(1 for c in context_map.values() if c['debug_commands'])} images with DEBUG commands")
print(f"📝 Found {sum(1 for c in context_map.values() if c['caption'])} images with captions")
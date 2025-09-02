#!/usr/bin/env python3
"""
Correct Smart Pins image metadata for split waveform diagrams.
SP-IMG-020 and SP-IMG-021 are left and right halves of a waveform.
"""

import json
import os
from datetime import datetime

def correct_split_waveforms():
    """Fix classification of split waveform images."""
    
    catalog_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/smart-pins/assets/images-smartpins-20250901/P2 SmartPins-220809_smartpins_catalog_corrected.json"
    
    # Load corrected catalog
    with open(catalog_path, 'r') as f:
        catalog = json.load(f)
    
    # Define corrections for the split waveform
    corrections = {
        "SP-IMG-020": {
            "semantic_type": "async_serial_waveform",  # Was marked as "corrupted_image"
            "specific_type": "waveform_left_half",
            "correction_note": "Left half of async serial transmission waveform - narrowed to show important details",
            "needs_re_extraction": False,  # Not corrupted!
            "verified": True,
            "related_image": "SP-IMG-021",
            "waveform_part": "left",
            "description": "Shows start bit and beginning of async serial transmission"
        },
        "SP-IMG-021": {
            "semantic_type": "async_serial_waveform",  # Was marked as "corrupted_image"
            "specific_type": "waveform_right_half",
            "correction_note": "Right half of async serial transmission waveform - narrowed to show important details",
            "needs_re_extraction": False,  # Not corrupted!
            "verified": True,
            "related_image": "SP-IMG-020",
            "waveform_part": "right",
            "description": "Shows end of async serial transmission and stop bit"
        }
    }
    
    # Apply corrections
    corrected_count = 0
    
    for img in catalog['images']:
        global_id = img['global_id']
        
        if global_id in corrections:
            # Update all fields from corrections
            for key, value in corrections[global_id].items():
                if key not in ['correction_note']:
                    img[key] = value
            
            # Update or add correction metadata
            if 'metadata_correction' not in img:
                img['metadata_correction'] = {}
            
            img['metadata_correction'].update({
                'corrected_on': datetime.now().isoformat(),
                'correction_note': corrections[global_id]['correction_note'],
                'correction_type': 'split_waveform_recognition',
                'original_classification': 'corrupted_image'
            })
            
            # Remove corruption flags
            if 'needs_re_extraction' in img:
                img['needs_re_extraction'] = False
            
            corrected_count += 1
            print(f"✅ Corrected {global_id}: {corrections[global_id]['correction_note']}")
    
    # Update catalog metadata
    if 'metadata' not in catalog:
        catalog['metadata'] = {}
    
    catalog['metadata']['split_waveform_correction'] = {
        'date': datetime.now().isoformat(),
        'corrected_images': corrected_count,
        'note': 'Identified SP-IMG-020 and SP-IMG-021 as intentional split waveform halves'
    }
    
    # Save updated catalog
    output_path = catalog_path.replace('_corrected.json', '_final.json')
    with open(output_path, 'w') as f:
        json.dump(catalog, f, indent=2)
    
    print(f"\n📊 Split Waveform Correction Summary:")
    print(f"  - Corrected: {corrected_count} images")
    print(f"  - SP-IMG-020: Left half of async serial waveform")
    print(f"  - SP-IMG-021: Right half of async serial waveform")
    print(f"  - These are NOT corrupted - they're intentionally split for clarity")
    print(f"  - Saved to: {output_path}")
    
    # Update the re-extraction list to remove these images
    re_extract_path = catalog_path.replace('_corrected.json', '_re_extract_list.json')
    if os.path.exists(re_extract_path):
        with open(re_extract_path, 'r') as f:
            re_extract_data = json.load(f)
        
        # Filter out SP-IMG-020 and SP-IMG-021
        updated_list = [
            img for img in re_extract_data.get('images_needing_re_extraction', [])
            if img['global_id'] not in ['SP-IMG-020', 'SP-IMG-021']
        ]
        
        if len(updated_list) != len(re_extract_data.get('images_needing_re_extraction', [])):
            re_extract_data['images_needing_re_extraction'] = updated_list
            re_extract_data['total'] = len(updated_list)
            re_extract_data['updated'] = datetime.now().isoformat()
            re_extract_data['note'] = 'SP-IMG-020 and SP-IMG-021 removed - they are split waveform halves, not corrupted'
            
            with open(re_extract_path, 'w') as f:
                json.dump(re_extract_data, f, indent=2)
            
            print(f"\n✅ Updated re-extraction list - removed split waveform images")
            print(f"  Remaining images needing re-extraction: {len(updated_list)}")

if __name__ == "__main__":
    correct_split_waveforms()
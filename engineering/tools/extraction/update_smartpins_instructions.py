#!/usr/bin/env python3
"""
Update Smart Pins catalog with corrected instruction references for images 1-3.
Based on user corrections:
- IMG-001: the delay for a DRVH instruction
- IMG-002: the timing for the TESTB INA,#0 operation  
- IMG-003: the timing for a TESTP instruction
"""

import json
import os
from datetime import datetime

def update_instruction_references():
    """Update the instruction references based on user corrections."""
    
    # Load the final catalog
    catalog_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/smart-pins/assets/images-smartpins-20250901/P2 SmartPins-220809_smartpins_catalog_final.json"
    
    if not os.path.exists(catalog_path):
        # Try the original catalog
        catalog_path = catalog_path.replace('_final.json', '.json')
    
    with open(catalog_path, 'r') as f:
        catalog = json.load(f)
    
    # Define corrections for each image
    corrections = {
        "SP-IMG-001": {
            "instructions": ["DRVH"],
            "description": "Shows the delay for a DRVH instruction",
            "subject": "DRVH instruction timing - 3-clock delay from instruction to pin state change",
            "technical_detail": "When DRVH instruction executes, there is a 3 system-clock cycle delay before the pin transitions to its new state",
            "semantic_type": "instruction_timing_diagram"
        },
        "SP-IMG-002": {
            "instructions": ["TESTB", "INA"],
            "description": "Shows the timing for the TESTB INA,#0 operation",
            "subject": "TESTB instruction timing - reading IN register with 3-clock latency",
            "technical_detail": "When TESTB reads the INA register, it receives the pin state from 3 system-clock cycles before the instruction start",
            "semantic_type": "instruction_timing_diagram"
        },
        "SP-IMG-003": {
            "instructions": ["TESTP"],
            "description": "Shows the timing for a TESTP instruction",
            "subject": "TESTP instruction timing - direct pin test with 2-clock latency",
            "technical_detail": "TESTP reads pin state from 2 system-clock cycles before instruction start, providing fresher data than IN register reads",
            "semantic_type": "instruction_timing_diagram"
        }
    }
    
    # Update the images in the catalog
    updated_count = 0
    for img in catalog.get('images', []):
        global_id = img.get('global_id')
        
        if global_id in corrections:
            corr = corrections[global_id]
            
            # Update instruction references
            if 'smart_pin_context' in img:
                img['smart_pin_context']['instructions'] = corr['instructions']
                img['smart_pin_context']['description'] = corr['description']
                img['smart_pin_context']['technical_detail'] = corr['technical_detail']
            
            # Update semantic type
            img['semantic_type'] = corr['semantic_type']
            
            # Add or update description fields
            img['description'] = corr['description']
            img['subject'] = corr['subject']
            img['technical_detail'] = corr['technical_detail']
            
            # Update caption to be more accurate
            if global_id == "SP-IMG-001":
                img['caption'] = "DRVH instruction timing showing 3-clock delay"
            elif global_id == "SP-IMG-002":
                img['caption'] = "TESTB INA,#0 timing showing 3-clock latency"
            elif global_id == "SP-IMG-003":
                img['caption'] = "TESTP instruction timing showing 2-clock latency"
            
            # Mark as corrected
            if 'metadata_correction' not in img:
                img['metadata_correction'] = {}
            
            img['metadata_correction'].update({
                'instruction_correction': {
                    'date': datetime.now().isoformat(),
                    'source': 'user_visual_verification',
                    'corrected_instructions': corr['instructions'],
                    'note': 'Corrected based on visual inspection of actual diagram content'
                }
            })
            
            updated_count += 1
            print(f"✅ Updated {global_id}:")
            print(f"   Instructions: {corr['instructions']}")
            print(f"   Description: {corr['description']}")
    
    # Update catalog metadata
    if 'metadata' not in catalog:
        catalog['metadata'] = {}
    
    catalog['metadata']['instruction_corrections'] = {
        'date': datetime.now().isoformat(),
        'images_corrected': updated_count,
        'correction_source': 'User visual verification',
        'corrections_applied': list(corrections.keys())
    }
    
    # Save the corrected catalog
    output_path = catalog_path.replace('.json', '_instructions_corrected.json')
    with open(output_path, 'w') as f:
        json.dump(catalog, f, indent=2)
    
    print(f"\n📊 Instruction Correction Summary:")
    print(f"  - Corrected: {updated_count} images")
    print(f"  - SP-IMG-001: DRVH instruction (3-clock delay)")
    print(f"  - SP-IMG-002: TESTB INA,#0 (3-clock latency)")
    print(f"  - SP-IMG-003: TESTP instruction (2-clock latency)")
    print(f"  - Saved to: {output_path}")
    
    return output_path

if __name__ == "__main__":
    update_instruction_references()
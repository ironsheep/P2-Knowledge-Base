#!/usr/bin/env python3
"""
Correct Smart Pins image metadata based on visual review.
"""

import json
import os
from datetime import datetime

def correct_metadata():
    """Apply corrections to Smart Pins catalog based on visual review."""
    
    catalog_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/smart-pins/assets/images-smartpins-20250901/P2 SmartPins-220809_smartpins_catalog.json"
    
    # Load existing catalog
    with open(catalog_path, 'r') as f:
        catalog = json.load(f)
    
    corrections = {
        "SP-IMG-018": {
            "semantic_type": "serial_timing",  # Was "pin_configuration"
            "correction_note": "Shows serial data transmission timing from LSB to MSB",
            "verified": True
        },
        "SP-IMG-020": {
            "semantic_type": "corrupted_image",  # Was "mode_11110_diagram"
            "correction_note": "Image appears corrupted/incomplete - needs re-extraction",
            "needs_re_extraction": True,
            "verified": False
        },
        "SP-IMG-021": {
            "semantic_type": "corrupted_image",  # Was "register_layout"
            "correction_note": "Image appears corrupted/incomplete - needs re-extraction",
            "needs_re_extraction": True,
            "verified": False
        }
    }
    
    # Additional classifications that are actually correct but could be more specific
    confirmations = {
        "SP-IMG-001": {
            "semantic_type": "timing_diagram",
            "specific_type": "instruction_timing",
            "correction_note": "Correctly classified - shows DRVH instruction timing",
            "verified": True
        },
        "SP-IMG-002": {
            "semantic_type": "timing_diagram", 
            "specific_type": "instruction_timing",
            "correction_note": "Correctly classified - shows TESTB instruction timing",
            "verified": True
        },
        "SP-IMG-003": {
            "semantic_type": "timing_waveform",
            "specific_type": "instruction_timing", 
            "correction_note": "Correctly classified - shows TESTP instruction timing",
            "verified": True
        },
        "SP-IMG-004": {
            "semantic_type": "timing_diagram",
            "specific_type": "pwm_dac_timing",
            "correction_note": "Correctly classified - shows PWM period for DAC dithering",
            "verified": True
        }
    }
    
    # Apply corrections
    corrected_count = 0
    confirmed_count = 0
    
    for img in catalog['images']:
        global_id = img['global_id']
        
        # Apply corrections
        if global_id in corrections:
            for key, value in corrections[global_id].items():
                if key == "semantic_type":
                    img['semantic_type'] = value
                elif key not in ['correction_note']:
                    img[key] = value
            
            # Add correction metadata
            img['metadata_correction'] = {
                'corrected_on': datetime.now().isoformat(),
                'correction_note': corrections[global_id]['correction_note'],
                'original_semantic_type': img.get('original_semantic_type', img['semantic_type'])
            }
            corrected_count += 1
            print(f"✅ Corrected {global_id}: {corrections[global_id]['correction_note']}")
        
        # Apply confirmations (add specific type but keep semantic type)
        elif global_id in confirmations:
            conf = confirmations[global_id]
            img['specific_type'] = conf.get('specific_type', '')
            img['verified'] = conf.get('verified', False)
            img['verification_note'] = conf.get('correction_note', '')
            confirmed_count += 1
            print(f"✓ Confirmed {global_id}: {conf['correction_note']}")
    
    # Add correction metadata to catalog
    catalog['metadata']['corrections_applied'] = {
        'date': datetime.now().isoformat(),
        'corrected_images': corrected_count,
        'confirmed_images': confirmed_count,
        'total_reviewed': corrected_count + confirmed_count
    }
    
    # Save corrected catalog
    output_path = catalog_path.replace('.json', '_corrected.json')
    with open(output_path, 'w') as f:
        json.dump(catalog, f, indent=2)
    
    print(f"\n📊 Correction Summary:")
    print(f"  - Corrected: {corrected_count} images")
    print(f"  - Confirmed: {confirmed_count} images")
    print(f"  - Saved to: {output_path}")
    
    # Generate re-extraction list
    re_extract = []
    for img in catalog['images']:
        if img.get('needs_re_extraction'):
            re_extract.append({
                'global_id': img['global_id'],
                'page': img['page_number'],
                'filename': img['filename'],
                'issue': img.get('correction_note', 'Needs re-extraction')
            })
    
    if re_extract:
        re_extract_path = catalog_path.replace('.json', '_re_extract_list.json')
        with open(re_extract_path, 'w') as f:
            json.dump({
                'images_needing_re_extraction': re_extract,
                'total': len(re_extract),
                'generated': datetime.now().isoformat()
            }, f, indent=2)
        print(f"\n⚠️  {len(re_extract)} images need re-extraction")
        print(f"  List saved to: {re_extract_path}")

if __name__ == "__main__":
    correct_metadata()
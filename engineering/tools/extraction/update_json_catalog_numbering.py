#!/usr/bin/env python3
"""
Add sequential numbering to JSON catalog images array.
"""

import json

def add_sequential_numbering(json_path, prefix="P2DS"):
    """Add sequential numbering to JSON catalog"""
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Add sequential numbering to each image
    for i, image in enumerate(data['images'], 1):
        image['sequential_id'] = f"{prefix}-{i:03d}"
        image['document_prefix'] = prefix
        image['sequence_number'] = i
    
    # Update metadata
    if 'metadata' not in data:
        data['metadata'] = {}
    
    data['metadata']['numbering_system'] = {
        'document_prefix': prefix,
        'sequential_format': f"{prefix}-###",
        'total_images': len(data['images']),
        'range': f"{prefix}-001 through {prefix}-{len(data['images']):03d}"
    }
    
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Added sequential numbering to {len(data['images'])} images")
    print(f"   Range: {prefix}-001 through {prefix}-{len(data['images']):03d}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 update_json_catalog_numbering.py <json_path> [prefix]")
        sys.exit(1)
    
    json_path = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) > 2 else "P2DS"
    
    add_sequential_numbering(json_path, prefix)
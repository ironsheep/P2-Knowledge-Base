#!/usr/bin/env python3
"""
Convert OrderedDict-serialized YAML files to clean YAML format.
"""

import yaml
import sys
from collections import OrderedDict

def ordereddict_to_dict(obj):
    """Recursively convert OrderedDict to regular dict."""
    if isinstance(obj, OrderedDict):
        return {k: ordereddict_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [ordereddict_to_dict(item) for item in obj]
    else:
        return obj

def convert_file(filepath):
    """Convert a single OrderedDict YAML file to clean YAML."""
    print(f"Converting {filepath}...")
    
    # Read the OrderedDict YAML using UnsafeLoader (handles Python objects)
    with open(filepath, 'r') as f:
        data = yaml.load(f, Loader=yaml.UnsafeLoader)
    
    # Convert OrderedDict to regular dict recursively
    clean_data = ordereddict_to_dict(data)
    
    # Write back as clean YAML
    with open(filepath, 'w') as f:
        yaml.dump(clean_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"  ✅ Converted successfully")

if __name__ == "__main__":
    files = [
        "engineering/ingestion/sources/pasm2-manual/updated-yamls/callpa.yaml",
        "engineering/ingestion/sources/pasm2-manual/updated-yamls/callpb.yaml",
        "engineering/ingestion/sources/pasm2-manual/updated-yamls/nop.yaml",
    ]
    
    for filepath in files:
        convert_file(filepath)
    
    print("\n✅ All 3 files converted to clean YAML")

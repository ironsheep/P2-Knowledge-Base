#!/usr/bin/env python3
"""
Fix OBEX Manifest Relative Paths
Implements base_path pattern to eliminate ../ paths for clean external access
"""

import os
import yaml
import sys
from pathlib import Path

def fix_yaml_path(yaml_path):
    """Convert ../../../engineering/... path to just objects/[id].yaml"""
    if yaml_path and '../' in yaml_path:
        # Extract just the final part: objects/XXXX.yaml
        parts = yaml_path.split('/')
        if 'objects' in parts:
            idx = parts.index('objects')
            return '/'.join(parts[idx:])
    return yaml_path

def add_base_path_to_manifest(filepath, is_category=True):
    """Add base_path field and fix all yaml_path entries"""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
        data = yaml.safe_load(content)
    
    fixed = False
    
    # Add base_path if not present
    if 'base_path' not in data:
        data['base_path'] = 'engineering/knowledge-base/P2/community/obex/'
        fixed = True
        print(f"  Added base_path: {data['base_path']}")
    
    # Add path construction note if not present
    if 'path_construction_note' not in data:
        data['path_construction_note'] = """TO ACCESS ANY FILE IN THIS MANIFEST:
Combine: raw_base_url (from root) + base_path (above) + yaml_path (from entries)

Example:
https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/ +
engineering/knowledge-base/P2/community/obex/ +
objects/2817.yaml
= Full URL to the YAML file"""
        fixed = True
        print(f"  Added path_construction_note")
    
    # Fix objects with yaml_path
    if 'objects' in data:
        for obj in data['objects']:
            if 'yaml_path' in obj:
                old_path = obj['yaml_path']
                new_path = fix_yaml_path(old_path)
                if old_path != new_path:
                    obj['yaml_path'] = new_path
                    fixed = True
                    print(f"  Fixed: {old_path} → {new_path}")
    
    if fixed:
        # Write with proper ordering
        ordered_data = {}
        
        # Put metadata fields first
        if 'manifest_metadata' in data:
            ordered_data['manifest_metadata'] = data['manifest_metadata']
        
        # Add base_path and construction note early
        ordered_data['base_path'] = data.get('base_path', 'engineering/knowledge-base/P2/community/obex/')
        ordered_data['path_construction_note'] = data.get('path_construction_note', '')
        
        # Add other fields
        for key, value in data.items():
            if key not in ['manifest_metadata', 'base_path', 'path_construction_note']:
                ordered_data[key] = value
        
        with open(filepath, 'w') as f:
            yaml.dump(ordered_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        print(f"  ✓ Updated {filepath}")
    else:
        print(f"  - No changes needed")
    
    return fixed

def fix_root_manifest(filepath):
    """Fix the OBEX root manifest specifically"""
    print(f"Processing root manifest: {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
        data = yaml.safe_load(content)
    
    fixed = False
    
    # Update access_patterns if needed
    if 'access_patterns' in data:
        if 'individual_objects' in data['access_patterns']:
            old_path = data['access_patterns']['individual_objects'].get('path', '')
            if '../' in old_path:
                data['access_patterns']['individual_objects']['path'] = 'objects/'
                data['access_patterns']['individual_objects']['note'] = 'Relative to base_path in sub-manifests'
                fixed = True
                print(f"  Fixed access pattern path")
    
    # Add base_path for OBEX
    if 'base_path' not in data:
        data['base_path'] = 'engineering/knowledge-base/P2/community/obex/'
        fixed = True
        print(f"  Added base_path")
    
    if fixed:
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        print(f"  ✓ Updated root manifest")
    
    return fixed

def main():
    # Get repository root
    repo_root = Path(__file__).resolve().parents[2]
    obex_manifest_dir = repo_root / 'manifests' / 'obex'
    
    print("Fixing OBEX Manifest Paths - Using Base Path Pattern")
    print("=" * 60)
    print("Goal: Eliminate ../ paths by using base_path + relative paths")
    print()
    
    total_fixed = 0
    
    # Fix root manifest first
    root_manifest = obex_manifest_dir / 'obex-root.yaml'
    if root_manifest.exists():
        if fix_root_manifest(root_manifest):
            total_fixed += 1
    
    # Process all manifest files in categories/
    categories_dir = obex_manifest_dir / 'categories'
    if categories_dir.exists():
        print("\nProcessing category manifests...")
        for manifest in sorted(categories_dir.glob('*.yaml')):
            if add_base_path_to_manifest(manifest, is_category=True):
                total_fixed += 1
    
    # Process all manifest files in authors/
    authors_dir = obex_manifest_dir / 'authors'
    if authors_dir.exists():
        print("\nProcessing author manifests...")
        for manifest in sorted(authors_dir.glob('*.yaml')):
            if add_base_path_to_manifest(manifest, is_category=False):
                total_fixed += 1
    
    print("\n" + "=" * 60)
    print(f"Total manifests fixed: {total_fixed}")
    print("\n✓ Path fixing complete!")
    print("\nPattern implemented:")
    print("- Each manifest has a base_path field")
    print("- All yaml_path entries are relative DOWN from base_path")
    print("- No ../ paths needed for clean URL construction")
    print("\nNext steps:")
    print("1. Run the enhanced validation script")
    print("2. Test external URL construction")
    print("3. Commit the changes")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
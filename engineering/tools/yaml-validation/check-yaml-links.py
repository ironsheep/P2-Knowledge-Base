#!/usr/bin/env python3
"""
Check P2 Knowledge Base YAML tree for orphaned files.
Traces from root manifest to find all linked files and identifies orphans.
"""

import os
import yaml
from pathlib import Path

KB_BASE = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2")

def find_all_yaml_files():
    """Find all YAML files in the knowledge base."""
    yaml_files = set()
    for root, dirs, files in os.walk(KB_BASE):
        for file in files:
            if file.endswith('.yaml'):
                full_path = Path(root) / file
                rel_path = full_path.relative_to(KB_BASE)
                yaml_files.add(str(rel_path))
    return yaml_files

def trace_manifest_links():
    """Trace all links from root manifest."""
    linked_files = set()
    to_process = ['root_manifest.yaml']
    processed = set()
    
    while to_process:
        current = to_process.pop(0)
        if current in processed:
            continue
        processed.add(current)
        linked_files.add(current)
        
        current_path = KB_BASE / current
        if not current_path.exists():
            print(f"WARNING: Referenced file missing: {current}")
            continue
            
        try:
            with open(current_path, 'r') as f:
                data = yaml.safe_load(f)
                if data:
                    # Extract all YAML references from the data
                    extract_yaml_refs(data, current_path.parent, linked_files, to_process)
        except Exception as e:
            print(f"ERROR reading {current}: {e}")
    
    return linked_files

def extract_yaml_refs(data, base_path, linked_files, to_process):
    """Recursively extract YAML file references from data structure."""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and value.endswith('.yaml'):
                # Convert to relative path from KB root
                if value.startswith('/'):
                    rel_path = value[1:]
                else:
                    # Resolve relative to current file's directory
                    resolved = (base_path / value).resolve()
                    if resolved.exists():
                        rel_path = resolved.relative_to(KB_BASE)
                    else:
                        rel_path = value
                
                rel_path_str = str(rel_path)
                if rel_path_str not in linked_files:
                    linked_files.add(rel_path_str)
                    to_process.append(rel_path_str)
                    
            elif isinstance(value, (dict, list)):
                extract_yaml_refs(value, base_path, linked_files, to_process)
                
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, str) and item.endswith('.yaml'):
                # Convert to relative path from KB root
                if item.startswith('/'):
                    rel_path = item[1:]
                else:
                    # Resolve relative to current file's directory
                    resolved = (base_path / item).resolve()
                    if resolved.exists():
                        rel_path = resolved.relative_to(KB_BASE)
                    else:
                        rel_path = item
                        
                rel_path_str = str(rel_path)
                if rel_path_str not in linked_files:
                    linked_files.add(rel_path_str)
                    to_process.append(rel_path_str)
                    
            elif isinstance(item, (dict, list)):
                extract_yaml_refs(item, base_path, linked_files, to_process)

def check_special_directories():
    """Check for YAML files in directories that should have manifests/indexes."""
    special_dirs = {
        'language/pasm2': 'instruction files',
        'language/pasm2/groups': 'instruction groups',
        'language/spin2': 'method files',
        'language/spin2/methods': 'Spin2 methods',
        'hardware': 'board definitions',
        'architecture/smart-pins': 'smart pin modes',
        'architecture/system-registers': 'system registers'
    }
    
    dir_contents = {}
    for dir_path, description in special_dirs.items():
        full_path = KB_BASE / dir_path
        if full_path.exists():
            yaml_files = list(full_path.glob('*.yaml'))
            if yaml_files:
                dir_contents[dir_path] = {
                    'description': description,
                    'count': len(yaml_files),
                    'files': [f.name for f in yaml_files[:5]]  # First 5 as sample
                }
    
    return dir_contents

def main():
    print("=== P2 Knowledge Base YAML Link Checker ===\n")
    
    # Find all YAML files
    all_yaml_files = find_all_yaml_files()
    print(f"Total YAML files found: {len(all_yaml_files)}")
    
    # Trace linked files from root manifest
    linked_files = trace_manifest_links()
    print(f"Files linked from root manifest: {len(linked_files)}")
    
    # Find orphans
    orphaned_files = all_yaml_files - linked_files
    print(f"\nORPHANED FILES: {len(orphaned_files)}")
    
    # Check special directories
    special_dirs = check_special_directories()
    
    # Group orphans by directory
    orphans_by_dir = {}
    for orphan in sorted(orphaned_files):
        dir_name = str(Path(orphan).parent)
        if dir_name not in orphans_by_dir:
            orphans_by_dir[dir_name] = []
        orphans_by_dir[dir_name].append(Path(orphan).name)
    
    # Report findings
    print("\n=== ORPHANED FILES BY DIRECTORY ===")
    for dir_name in sorted(orphans_by_dir.keys()):
        files = orphans_by_dir[dir_name]
        print(f"\n{dir_name}/ ({len(files)} files)")
        
        # Check if this is a special directory
        if dir_name in special_dirs:
            info = special_dirs[dir_name]
            print(f"  TYPE: {info['description']}")
            print(f"  EXPECTED: Should have manifest/index linking these files")
        
        # Show first 10 files as examples
        for file in files[:10]:
            print(f"  - {file}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more")
    
    # Summary recommendations
    print("\n=== RECOMMENDATIONS ===")
    
    missing_manifests = []
    if 'language/pasm2' in orphans_by_dir:
        missing_manifests.append("- Create language/pasm2/instruction_manifest.yaml")
    if 'language/pasm2/groups' in orphans_by_dir:
        missing_manifests.append("- Create or link language/pasm2/groups manifests")
    if 'language/spin2' in orphans_by_dir or 'language/spin2/methods' in orphans_by_dir:
        missing_manifests.append("- Create language/spin2/method_manifest.yaml")
    if 'hardware' in orphans_by_dir:
        missing_manifests.append("- Create hardware/board_manifest.yaml")
    if 'architecture/smart-pins' in orphans_by_dir:
        missing_manifests.append("- Create architecture/smart-pins/smartpin_manifest.yaml")
        
    if missing_manifests:
        print("\nMissing manifest files that need to be created:")
        for manifest in missing_manifests:
            print(manifest)
    
    # Check for directories with many YAML files but no manifest
    print("\n=== STATISTICS BY DIRECTORY ===")
    for dir_name in sorted(orphans_by_dir.keys()):
        count = len(orphans_by_dir[dir_name])
        if count > 10:
            print(f"{dir_name}: {count} orphaned files (NEEDS MANIFEST)")

if __name__ == "__main__":
    main()
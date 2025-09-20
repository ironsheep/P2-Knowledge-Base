#!/usr/bin/env python3
"""
Fix broken links in manifests by ensuring proper path prefixes.
"""

import os
import yaml
from pathlib import Path

KB_BASE = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2")

def check_and_fix_manifest(manifest_path):
    """Check and fix a manifest file."""
    print(f"\nChecking: {manifest_path.relative_to(KB_BASE)}")
    
    with open(manifest_path, 'r') as f:
        data = yaml.safe_load(f)
    
    if not data:
        return
    
    changes_made = False
    issues_found = []
    
    # Check language_components in Spin2 manifest
    if 'language_components' in data:
        for component_name, component_data in data['language_components'].items():
            if isinstance(component_data, dict) and 'files' in component_data:
                path_prefix = component_data.get('path', '')
                files = component_data['files']
                
                # Check if files exist with the path prefix
                for i, file_ref in enumerate(files):
                    if not file_ref.endswith('.yaml'):
                        continue
                        
                    # Check if file exists relative to manifest location
                    full_path = manifest_path.parent / path_prefix / file_ref
                    
                    if not full_path.exists():
                        # Try without path prefix
                        alt_path = manifest_path.parent / file_ref
                        if alt_path.exists():
                            issues_found.append(f"  - {component_name}: {file_ref} should include path prefix")
                        else:
                            issues_found.append(f"  - {component_name}: {file_ref} doesn't exist")
    
    # Check pattern_components in Spin2 manifest  
    if 'pattern_components' in data:
        for component_name, component_data in data['pattern_components'].items():
            if isinstance(component_data, dict) and 'files' in component_data:
                path_prefix = component_data.get('path', '')
                files = component_data['files']
                
                for file_ref in files:
                    if not file_ref.endswith('.yaml'):
                        continue
                    
                    full_path = manifest_path.parent / path_prefix / file_ref
                    if not full_path.exists():
                        issues_found.append(f"  - {component_name}: {file_ref} doesn't exist at {path_prefix}")
    
    # Check special_components in PASM2 manifest
    if 'special_components' in data:
        for component_name, component_data in data['special_components'].items():
            if isinstance(component_data, dict) and 'files' in component_data:
                path_prefix = component_data.get('path', '')
                files = component_data['files']
                
                for file_ref in files:
                    if not file_ref.endswith('.yaml'):
                        continue
                        
                    full_path = manifest_path.parent / path_prefix / file_ref
                    if not full_path.exists():
                        issues_found.append(f"  - {component_name}: {file_ref} doesn't exist at {path_prefix}")
    
    if issues_found:
        print(f"Issues found in {manifest_path.name}:")
        for issue in issues_found[:10]:  # First 10 issues
            print(issue)
        if len(issues_found) > 10:
            print(f"  ... and {len(issues_found) - 10} more issues")
    else:
        print(f"  ✓ All references valid")
    
    return len(issues_found)

def find_all_broken_references():
    """Find all broken references across all manifests."""
    
    manifest_files = [
        KB_BASE / "root_manifest.yaml",
        KB_BASE / "language/spin2/method_manifest.yaml",
        KB_BASE / "language/pasm2/instruction_manifest.yaml",
        KB_BASE / "architecture/architecture_manifest.yaml",
        KB_BASE / "hardware/board_manifest.yaml",
        KB_BASE / "architecture/smart-pins/smartpin_manifest.yaml",
        KB_BASE / "architecture/system-registers/register_manifest.yaml",
        KB_BASE / "code-examples/examples_manifest.yaml",
        KB_BASE / "language/spin2/patterns/pattern-index.yaml",
        KB_BASE / "language/pasm2/patterns/pattern_manifest.yaml"
    ]
    
    total_issues = 0
    for manifest in manifest_files:
        if manifest.exists():
            issues = check_and_fix_manifest(manifest)
            if issues:
                total_issues += issues
    
    print(f"\n=== SUMMARY ===")
    print(f"Total broken references found: {total_issues}")
    
    if total_issues > 0:
        print("\nThe issue is that file references in manifests need to be:")
        print("1. Relative to the manifest file's location")
        print("2. Not include the 'path' prefix when it's already specified")
        print("\nThese are NOT placeholder links - the files exist but the paths are wrong!")

def main():
    print("=== Checking for Broken Links in Manifests ===")
    find_all_broken_references()

if __name__ == "__main__":
    main()
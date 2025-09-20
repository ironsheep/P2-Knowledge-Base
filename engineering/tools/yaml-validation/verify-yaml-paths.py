#!/usr/bin/env python3
"""
Verify all linked YAML files are within the KB_BASE directory.
Check for any external references or files outside the knowledge base.
"""

import os
import yaml
from pathlib import Path

KB_BASE = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2")
PROJECT_ROOT = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base")

def check_yaml_references():
    """Check all YAML files for external references."""
    external_refs = []
    missing_refs = []
    valid_internal = []
    
    # Find all YAML files in KB_BASE
    for yaml_file in KB_BASE.rglob("*.yaml"):
        try:
            with open(yaml_file, 'r') as f:
                content = yaml.safe_load(f)
                if content:
                    check_references(content, yaml_file, external_refs, missing_refs, valid_internal)
        except Exception as e:
            print(f"Error reading {yaml_file.relative_to(KB_BASE)}: {e}")
    
    return external_refs, missing_refs, valid_internal

def check_references(data, source_file, external_refs, missing_refs, valid_internal):
    """Recursively check data for YAML file references."""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and value.endswith('.yaml'):
                check_single_reference(value, source_file, external_refs, missing_refs, valid_internal)
            elif isinstance(value, (dict, list)):
                check_references(value, source_file, external_refs, missing_refs, valid_internal)
                
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, str) and item.endswith('.yaml'):
                check_single_reference(item, source_file, external_refs, missing_refs, valid_internal)
            elif isinstance(item, (dict, list)):
                check_references(item, source_file, external_refs, missing_refs, valid_internal)

def check_single_reference(ref_path, source_file, external_refs, missing_refs, valid_internal):
    """Check a single YAML reference."""
    source_rel = source_file.relative_to(KB_BASE)
    
    # Handle absolute paths
    if ref_path.startswith('/'):
        # Absolute path from system root - definitely external
        external_refs.append({
            'source': str(source_rel),
            'reference': ref_path,
            'type': 'absolute_system_path'
        })
        return
    
    # Check if path tries to go outside KB_BASE
    if '../' in ref_path:
        # Could be trying to reference outside KB_BASE
        resolved = (source_file.parent / ref_path).resolve()
        if not str(resolved).startswith(str(KB_BASE)):
            external_refs.append({
                'source': str(source_rel),
                'reference': ref_path,
                'type': 'relative_outside_kb',
                'resolves_to': str(resolved)
            })
            return
    
    # Check if file exists in KB_BASE
    if ref_path.startswith('language/') or ref_path.startswith('architecture/') or ref_path.startswith('hardware/'):
        # Direct reference from KB_BASE
        target = KB_BASE / ref_path
    else:
        # Relative to source file's directory
        target = (source_file.parent / ref_path).resolve()
    
    if target.exists():
        if str(target).startswith(str(KB_BASE)):
            valid_internal.append({
                'source': str(source_rel),
                'reference': ref_path
            })
        else:
            external_refs.append({
                'source': str(source_rel),
                'reference': ref_path,
                'type': 'exists_outside_kb',
                'actual_path': str(target)
            })
    else:
        missing_refs.append({
            'source': str(source_rel),
            'reference': ref_path,
            'expected_path': str(target.relative_to(KB_BASE)) if str(target).startswith(str(KB_BASE)) else str(target)
        })

def check_for_external_yaml_files():
    """Check if there are YAML files outside KB_BASE that should be inside."""
    external_yaml = []
    
    # Check engineering/ingestion directory
    ingestion_path = PROJECT_ROOT / "engineering/ingestion"
    if ingestion_path.exists():
        for yaml_file in ingestion_path.glob("*.yaml"):
            if "pattern" in yaml_file.name or "idiom" in yaml_file.name:
                external_yaml.append({
                    'file': str(yaml_file.relative_to(PROJECT_ROOT)),
                    'type': 'pattern/idiom file outside KB',
                    'size': yaml_file.stat().st_size
                })
    
    # Check other engineering directories
    for subdir in ['document-production', 'pdf-forge', 'operations']:
        dir_path = PROJECT_ROOT / f"engineering/{subdir}"
        if dir_path.exists():
            for yaml_file in dir_path.rglob("*.yaml"):
                if "manifest" in yaml_file.name.lower() or "pattern" in yaml_file.name.lower():
                    external_yaml.append({
                        'file': str(yaml_file.relative_to(PROJECT_ROOT)),
                        'type': 'potential KB file outside KB',
                        'size': yaml_file.stat().st_size
                    })
    
    return external_yaml

def main():
    print("=== Verifying YAML References are Within KB_BASE ===\n")
    print(f"KB_BASE: {KB_BASE}")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}\n")
    
    # Check references in YAML files
    external_refs, missing_refs, valid_internal = check_yaml_references()
    
    print(f"Total references checked: {len(external_refs) + len(missing_refs) + len(valid_internal)}")
    print(f"Valid internal references: {len(valid_internal)}")
    print(f"Missing references: {len(missing_refs)}")
    print(f"External references: {len(external_refs)}\n")
    
    if external_refs:
        print("=== ⚠️  EXTERNAL REFERENCES FOUND ===")
        print("These files reference YAMLs outside the KB_BASE:\n")
        for ref in external_refs:
            print(f"Source: {ref['source']}")
            print(f"  References: {ref['reference']}")
            print(f"  Type: {ref['type']}")
            if 'resolves_to' in ref:
                print(f"  Resolves to: {ref['resolves_to']}")
            if 'actual_path' in ref:
                print(f"  Actual path: {ref['actual_path']}")
            print()
    
    if missing_refs:
        print(f"=== MISSING REFERENCES (First 20 of {len(missing_refs)}) ===")
        for ref in missing_refs[:20]:
            print(f"Source: {ref['source']}")
            print(f"  Missing: {ref['reference']}")
            print()
    
    # Check for external YAML files
    external_yaml = check_for_external_yaml_files()
    if external_yaml:
        print("=== YAML FILES OUTSIDE KB_BASE ===")
        print("These YAML files exist outside the knowledge base:\n")
        for file_info in external_yaml:
            print(f"File: {file_info['file']}")
            print(f"  Type: {file_info['type']}")
            print(f"  Size: {file_info['size']} bytes")
            print()
    
    # Summary
    print("=== SUMMARY ===")
    if external_refs:
        print(f"⚠️  PROBLEM: {len(external_refs)} references point outside KB_BASE")
        print("   These need to be fixed to ensure remote AI only accesses KB content")
    else:
        print("✅ GOOD: All references are within KB_BASE")
    
    if external_yaml:
        print(f"\n📁 NOTE: {len(external_yaml)} YAML files exist outside KB_BASE")
        print("   Review these to determine if any should be moved into KB")

if __name__ == "__main__":
    main()
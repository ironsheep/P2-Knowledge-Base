#!/usr/bin/env python3
"""
Apply extracted manual documentation to YAML files.
This merges the extracted content with existing YAMLs, preserving technical fields
while adding the rich documentation from the manual.
"""

import yaml
from pathlib import Path
import shutil
from datetime import datetime
import json

# Paths
PASM2_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2")
EXTRACTION_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/extracted-documentation")
BACKUP_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2-backup")

# Fields to preserve from existing YAMLs (technical/compiler data)
PRESERVE_FIELDS = [
    'instruction',
    'syntax',
    'encoding', 
    'timing',
    'compiler_syntax',
    'compiler_encoding',
    'compiler_category',
    'compiler_effects',
    'compiler_operand_format',
    'enhancement_source',
    'syntax_variants'
]

# Fields to merge (combine existing + manual)
MERGE_FIELDS = [
    'related',
    'examples',
    'notes'
]

def merge_yaml_data(existing, manual_extracted):
    """Intelligently merge manual documentation with existing YAML data."""
    merged = existing.copy()
    
    # Preserve technical fields
    for field in PRESERVE_FIELDS:
        if field in existing:
            merged[field] = existing[field]
    
    # Update documentation fields from manual
    if manual_extracted.get('brief_description'):
        merged['brief_description'] = manual_extracted['brief_description']
    
    if manual_extracted.get('category'):
        # Don't override if we have a group already
        if not merged.get('group'):
            merged['group'] = manual_extracted['category']
    
    # Use manual description if it's longer/better
    manual_desc = manual_extracted.get('description', '')
    existing_desc = existing.get('description', '')
    
    if manual_desc and len(manual_desc) > len(existing_desc):
        merged['description'] = manual_desc
    elif not existing_desc and manual_desc:
        merged['description'] = manual_desc
    
    # Add result description if not present
    if manual_extracted.get('result_description'):
        merged['result_description'] = manual_extracted['result_description']
    
    # Update parameters with manual content
    if manual_extracted.get('parameters'):
        # If existing has no parameters or they're minimal, use manual
        if not existing.get('parameters') or len(str(existing.get('parameters', ''))) < 100:
            merged['parameters'] = manual_extracted['parameters']
    
    # Merge related instructions
    if manual_extracted.get('related'):
        existing_related = existing.get('related', [])
        manual_related = manual_extracted['related']
        # Combine and deduplicate
        all_related = list(set(existing_related + manual_related))
        if all_related:
            merged['related'] = sorted(all_related)
    
    # Add usage notes
    if manual_extracted.get('usage_notes'):
        # Combine with existing if present
        existing_notes = existing.get('usage_notes', '')
        manual_notes = manual_extracted['usage_notes']
        if existing_notes and manual_notes and existing_notes != manual_notes:
            merged['usage_notes'] = existing_notes + '\n\n' + manual_notes
        elif manual_notes:
            merged['usage_notes'] = manual_notes
    
    # Add warnings
    if manual_extracted.get('warnings'):
        merged['warnings'] = manual_extracted['warnings']
    
    # Merge examples
    if manual_extracted.get('examples'):
        existing_examples = existing.get('examples', [])
        manual_examples = manual_extracted['examples']
        
        # Deduplicate based on code content
        existing_codes = {ex.get('code', '') for ex in existing_examples if isinstance(ex, dict)}
        
        for ex in manual_examples:
            if isinstance(ex, dict) and ex.get('code') not in existing_codes:
                existing_examples.append(ex)
        
        if existing_examples:
            merged['examples'] = existing_examples
    
    # Update documentation metadata
    merged['documentation_source'] = 'PASM2 Manual 2022/11/01 Pages 31-147'
    merged['documentation_level'] = 'comprehensive'
    merged['manual_extraction_complete'] = True
    merged['last_updated'] = datetime.now().isoformat()
    
    return merged

def apply_updates(dry_run=False):
    """Apply the extracted manual updates to YAMLs."""
    
    # Create backup directory
    if not dry_run:
        BACKUP_PATH.mkdir(exist_ok=True)
        print(f"Creating backups in: {BACKUP_PATH}")
    
    # Load extracted data
    extraction_file = EXTRACTION_PATH / "complete_manual_extraction.json"
    if not extraction_file.exists():
        print("ERROR: No extraction file found. Run extract-full-manual-documentation.py first!")
        return
    
    with open(extraction_file, 'r') as f:
        extracted_data = json.load(f)
    
    print(f"Loaded documentation for {len(extracted_data)} instructions")
    
    # Process each instruction
    updated_count = 0
    created_count = 0
    unchanged_count = 0
    
    for inst_name, manual_data in extracted_data.items():
        yaml_path = PASM2_PATH / f"{inst_name.lower()}.yaml"
        
        if yaml_path.exists():
            # Load existing YAML
            with open(yaml_path, 'r') as f:
                existing_data = yaml.safe_load(f) or {}
            
            # Merge with manual data
            merged_data = merge_yaml_data(existing_data, manual_data)
            
            # Check if anything changed
            if merged_data != existing_data:
                if not dry_run:
                    # Backup original
                    backup_file = BACKUP_PATH / f"{inst_name.lower()}.yaml"
                    shutil.copy(yaml_path, backup_file)
                    
                    # Write merged data
                    with open(yaml_path, 'w') as f:
                        yaml.dump(merged_data, f, default_flow_style=False, sort_keys=False)
                
                updated_count += 1
                print(f"  Updated: {inst_name}")
                
                # Show what changed
                added_fields = set(merged_data.keys()) - set(existing_data.keys())
                if added_fields:
                    print(f"    Added fields: {', '.join(added_fields)}")
                
                # Check description improvement
                old_desc_len = len(existing_data.get('description', ''))
                new_desc_len = len(merged_data.get('description', ''))
                if new_desc_len > old_desc_len:
                    print(f"    Description: {old_desc_len} -> {new_desc_len} chars")
            else:
                unchanged_count += 1
        else:
            # Create new YAML
            yaml_data = {
                'instruction': inst_name,
                'description': manual_data.get('description', ''),
                'brief_description': manual_data.get('brief_description', ''),
                'category': manual_data.get('category', ''),
                'result_description': manual_data.get('result_description', ''),
                'parameters': manual_data.get('parameters', []),
                'related': manual_data.get('related', []),
                'usage_notes': manual_data.get('usage_notes', ''),
                'examples': manual_data.get('examples', []),
                'documentation_source': 'PASM2 Manual 2022/11/01 Pages 31-147',
                'documentation_level': 'comprehensive',
                'manual_extraction_complete': True,
                'last_updated': datetime.now().isoformat()
            }
            
            if not dry_run:
                with open(yaml_path, 'w') as f:
                    yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)
            
            created_count += 1
            print(f"  Created: {inst_name}")
    
    # Summary
    print("\n" + "="*60)
    print("UPDATE SUMMARY")
    print("="*60)
    print(f"Updated: {updated_count} YAMLs")
    print(f"Created: {created_count} new YAMLs")
    print(f"Unchanged: {unchanged_count} YAMLs")
    
    if dry_run:
        print("\nDRY RUN - No files were modified")
        print("Run with --apply to actually update the YAMLs")
    else:
        print(f"\nOriginal YAMLs backed up to: {BACKUP_PATH}")
        print("Run analyze_instruction_coverage.py to see the improvement!")

if __name__ == "__main__":
    import sys
    
    dry_run = True
    if "--apply" in sys.argv:
        dry_run = False
        print("APPLYING UPDATES - This will modify YAML files!")
    else:
        print("DRY RUN MODE - No files will be modified")
    
    apply_updates(dry_run=dry_run)
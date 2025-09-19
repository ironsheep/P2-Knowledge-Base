#!/usr/bin/env python3
"""
Apply extracted documentation from pages 31-147 to the YAML knowledge base.
This script merges the extracted content with existing YAMLs, preserving technical fields.
"""

import yaml
from pathlib import Path
import shutil
from datetime import datetime

# Paths
UPDATES_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/extracted-documentation/yaml_updates_pages_31_147")
PASM2_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2")
DIRECTIVES_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2/assembly-directives")
BACKUP_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/yaml-backups")

# Create backup directory
backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = BACKUP_PATH / f"backup_{backup_timestamp}"
backup_dir.mkdir(exist_ok=True, parents=True)

print("="*60)
print("APPLYING EXTRACTED DOCUMENTATION TO YAML KNOWLEDGE BASE")
print("="*60)
print(f"\nBackup directory: {backup_dir}")

# Get all update files
update_files = list(UPDATES_PATH.glob("*.yaml"))
print(f"\nFound {len(update_files)} YAML updates to apply")

# Statistics
stats = {
    'instructions_updated': 0,
    'directives_updated': 0,
    'new_instructions': 0,
    'new_directives': 0,
    'fields_added': 0,
    'fields_updated': 0,
    'errors': []
}

# Directives list
KNOWN_DIRECTIVES = {'alignl', 'alignw', 'org', 'orgf', 'orgh', 'res', 'fit', 'byte', 'word', 'long', 'file'}

def merge_yaml_content(existing, update):
    """Merge update content into existing YAML, preserving technical fields."""
    merged = existing.copy()
    fields_changed = []
    
    # Fields to update (overwrite if present in update)
    update_fields = [
        'brief_description',
        'category', 
        'description',
        'result',
        'syntax',
        'syntax_variants',
        'parameters',
        'encoding',
        'timing',
        'flags_affected',
        'related',
        'usage_notes',
        'examples',
        'documentation_source',
        'documentation_level',
        'manual_extraction_date'
    ]
    
    for field in update_fields:
        if field in update:
            # Check if field is new or changed
            if field not in existing:
                fields_changed.append(f"added:{field}")
                merged[field] = update[field]
            elif existing.get(field) != update.get(field):
                # Special handling for description - append if significantly different
                if field == 'description' and existing.get(field):
                    # Check if update adds significant new content
                    if len(update[field]) > len(existing[field]) * 1.5:
                        merged[field] = update[field]
                        fields_changed.append(f"expanded:{field}")
                else:
                    merged[field] = update[field]
                    fields_changed.append(f"updated:{field}")
    
    # Preserve technical fields not in update
    preserve_fields = [
        'instruction',
        'directive',
        'type',
        'group',
        'compiler_operand_format',
        'compiler_encoding',
        'enhancement_source',
        'group_membership',
        'has_group_documentation',
        'specifics',
        'last_updated'
    ]
    
    for field in preserve_fields:
        if field in existing and field not in merged:
            merged[field] = existing[field]
    
    # Update last_updated timestamp
    merged['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    
    return merged, fields_changed

# Process each update file
for update_file in update_files:
    instruction_name = update_file.stem
    
    # Load update content
    with open(update_file, 'r') as f:
        update_content = yaml.safe_load(f) or {}
    
    # Determine if instruction or directive
    is_directive = instruction_name.lower() in KNOWN_DIRECTIVES
    
    if is_directive:
        target_path = DIRECTIVES_PATH / f"{instruction_name}.yaml"
        item_type = "directive"
    else:
        target_path = PASM2_PATH / f"{instruction_name}.yaml"
        item_type = "instruction"
    
    try:
        # Backup existing file if it exists
        if target_path.exists():
            backup_file = backup_dir / f"{instruction_name}.yaml"
            shutil.copy2(target_path, backup_file)
            
            # Load existing content
            with open(target_path, 'r') as f:
                existing_content = yaml.safe_load(f) or {}
            
            # Merge content
            merged_content, changes = merge_yaml_content(existing_content, update_content)
            
            # Write merged content
            with open(target_path, 'w') as f:
                yaml.dump(merged_content, f, default_flow_style=False, sort_keys=False, width=100)
            
            if is_directive:
                stats['directives_updated'] += 1
            else:
                stats['instructions_updated'] += 1
            
            stats['fields_added'] += len([c for c in changes if c.startswith('added:')])
            stats['fields_updated'] += len([c for c in changes if c.startswith('updated:') or c.startswith('expanded:')])
            
            if changes:
                print(f"  Updated {instruction_name} ({item_type}): {', '.join(changes[:3])}")
        else:
            # New file - write directly
            with open(target_path, 'w') as f:
                yaml.dump(update_content, f, default_flow_style=False, sort_keys=False, width=100)
            
            if is_directive:
                stats['new_directives'] += 1
            else:
                stats['new_instructions'] += 1
            
            print(f"  Created new {instruction_name} ({item_type})")
            
    except Exception as e:
        stats['errors'].append(f"{instruction_name}: {str(e)}")
        print(f"  ERROR processing {instruction_name}: {e}")

# Print summary
print("\n" + "="*60)
print("APPLICATION COMPLETE")
print("="*60)
print("\nStatistics:")
print(f"  Instructions updated: {stats['instructions_updated']}")
print(f"  Directives updated: {stats['directives_updated']}")
print(f"  New instructions added: {stats['new_instructions']}")
print(f"  New directives added: {stats['new_directives']}")
print(f"  Total fields added: {stats['fields_added']}")
print(f"  Total fields updated: {stats['fields_updated']}")

if stats['errors']:
    print(f"\nErrors ({len(stats['errors'])}):")
    for error in stats['errors'][:5]:
        print(f"  - {error}")

print(f"\nBackup saved to: {backup_dir}")
print("\nTo verify changes:")
print("  1. Check a few updated YAMLs to ensure quality")
print("  2. Run instruction_analysis.yaml to see improved scores")
print("  3. Generate new heat maps to visualize improvement")
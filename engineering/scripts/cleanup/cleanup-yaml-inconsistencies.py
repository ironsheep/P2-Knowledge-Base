#!/usr/bin/env python3
"""
Comprehensive cleanup of YAML inconsistencies in PASM2 instruction documentation.
Fixes data type issues, removes obsolete fields, and ensures grouped instructions are fully synchronized.
"""

import yaml
from pathlib import Path
from collections import defaultdict
import re
from datetime import datetime

# Paths
PASM2_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2")
DIRECTIVES_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2/assembly-directives")

# Load instruction analysis to find grouped instructions
print("Loading instruction analysis...")
data = yaml.safe_load(open('instruction_analysis.yaml'))
yaml_items = data['yaml_items']

# Find all grouped instructions
grouped_instructions = defaultdict(list)
for name, info in yaml_items.items():
    if info.get('is_grouped_in_manual'):
        group_key = tuple(sorted(info['manual_group_members']))
        grouped_instructions[group_key].append(name)

print(f"Found {len(grouped_instructions)} instruction groups")

# Track changes
changes_made = defaultdict(list)

def fix_yaml_file(filepath, is_directive=False):
    """Fix a single YAML file."""
    filename = filepath.name
    instruction_name = filepath.stem.upper()
    
    with open(filepath, 'r') as f:
        content = f.read()
        data = yaml.safe_load(content)
    
    if not data:
        return False
    
    original_data = dict(data)
    local_changes = []
    
    # 1. Fix timing.cycles data type - should be integer
    if 'timing' in data and isinstance(data['timing'], dict):
        if 'cycles' in data['timing']:
            cycles = data['timing']['cycles']
            if isinstance(cycles, str) and cycles.isdigit():
                data['timing']['cycles'] = int(cycles)
                local_changes.append(f"Fixed timing.cycles: '{cycles}' -> {int(cycles)}")
            elif isinstance(cycles, str):
                # Handle ranges like "2-13"
                if '-' in cycles:
                    # Keep as string for ranges
                    pass
                else:
                    try:
                        data['timing']['cycles'] = int(cycles)
                        local_changes.append(f"Fixed timing.cycles: '{cycles}' -> {int(cycles)}")
                    except:
                        pass
    
    # 2. Remove obsolete fields
    obsolete_fields = ['needs_documentation', 'update_note']
    for field in obsolete_fields:
        if field in data:
            del data[field]
            local_changes.append(f"Removed obsolete field: {field}")
    
    # 3. Ensure documentation_level is set properly if documentation exists
    if 'description' in data and data['description']:
        desc_len = len(data['description'])
        if desc_len > 200 and data.get('documentation_level') != 'comprehensive':
            data['documentation_level'] = 'comprehensive'
            local_changes.append("Set documentation_level to comprehensive")
        elif desc_len > 100 and data.get('documentation_level') == 'minimal':
            data['documentation_level'] = 'enhanced'
            local_changes.append("Updated documentation_level from minimal to enhanced")
    
    # 4. Standardize field names
    field_renames = {
        'category': 'group',  # Use group consistently
        'flags': 'flags_affected',  # Standardize flag field name
    }
    
    for old_field, new_field in field_renames.items():
        if old_field in data and new_field not in data:
            data[new_field] = data[old_field]
            del data[old_field]
            local_changes.append(f"Renamed field: {old_field} -> {new_field}")
        elif old_field in data and new_field in data:
            # Both exist, keep the one with more content
            if isinstance(data[old_field], str) and isinstance(data[new_field], str):
                if len(data[old_field]) > len(data[new_field]):
                    data[new_field] = data[old_field]
            del data[old_field]
            local_changes.append(f"Merged {old_field} into {new_field}")
    
    # 5. Ensure compiler fields have consistent structure
    if 'compiler_operand_format' in data:
        cof = data['compiler_operand_format']
        if isinstance(cof, dict):
            # Ensure valueType is integer if it exists
            if 'valueType' in cof and isinstance(cof['valueType'], str):
                try:
                    cof['valueType'] = int(cof['valueType'])
                    local_changes.append("Fixed compiler_operand_format.valueType to integer")
                except:
                    pass
    
    if 'compiler_encoding' in data:
        ce = data['compiler_encoding']
        if isinstance(ce, dict):
            # Ensure operandFormat is integer if it exists
            if 'operandFormat' in ce and isinstance(ce['operandFormat'], str):
                try:
                    ce['operandFormat'] = int(ce['operandFormat'])
                    local_changes.append("Fixed compiler_encoding.operandFormat to integer")
                except:
                    pass
    
    # Save if changes were made
    if local_changes:
        data['last_updated'] = datetime.now().isoformat()
        
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        
        changes_made[instruction_name] = local_changes
        return True
    
    return False

def synchronize_grouped_instructions():
    """Ensure grouped instructions have identical documentation fields."""
    print("\n" + "="*60)
    print("Synchronizing grouped instructions...")
    print("="*60)
    
    synced_count = 0
    
    for group_members, instructions in grouped_instructions.items():
        if len(instructions) < 2:
            continue
        
        # Load all YAMLs for this group
        group_data = {}
        for inst in instructions:
            filepath = PASM2_PATH / f"{inst.lower()}.yaml"
            if filepath.exists():
                with open(filepath, 'r') as f:
                    group_data[inst] = yaml.safe_load(f)
        
        if len(group_data) < 2:
            continue
        
        # Find the best-documented member (highest score)
        best_inst = None
        best_score = -1
        for inst in instructions:
            score = yaml_items.get(inst, {}).get('score', 0)
            if score > best_score:
                best_score = score
                best_inst = inst
        
        if not best_inst or best_inst not in group_data:
            continue
        
        best_data = group_data[best_inst]
        
        # Fields that should be synchronized across grouped instructions
        sync_fields = [
            'description', 'category', 'group', 'parameters', 'flags_affected',
            'documentation_source', 'documentation_level', 'timing',
            'compiler_operand_format', 'compiler_encoding', 'enhancement_source'
        ]
        
        # Synchronize other members with the best one
        for inst in instructions:
            if inst == best_inst:
                continue
            
            if inst not in group_data:
                continue
            
            inst_data = group_data[inst]
            inst_changes = []
            
            for field in sync_fields:
                if field in best_data:
                    if field == 'timing':
                        # Special handling for timing to ensure consistency
                        if field not in inst_data or inst_data[field] != best_data[field]:
                            inst_data[field] = best_data[field]
                            inst_changes.append(f"Synchronized {field}")
                    elif field not in inst_data or inst_data[field] != best_data[field]:
                        inst_data[field] = best_data[field]
                        inst_changes.append(f"Synchronized {field}")
            
            # Save if changes were made
            if inst_changes:
                inst_data['last_updated'] = datetime.now().isoformat()
                filepath = PASM2_PATH / f"{inst.lower()}.yaml"
                
                with open(filepath, 'w') as f:
                    yaml.dump(inst_data, f, default_flow_style=False, sort_keys=False)
                
                changes_made[inst].extend(inst_changes)
                synced_count += 1
                print(f"  Synchronized {inst} with {best_inst}")
    
    print(f"\nSynchronized {synced_count} instructions")
    return synced_count

# Process all PASM2 instruction files
print("\nProcessing PASM2 instruction YAMLs...")
pasm2_files = list(PASM2_PATH.glob("*.yaml"))
fixed_pasm2 = 0

for filepath in pasm2_files:
    if filepath.stem in ['concepts', 'patterns', 'idioms']:
        continue
    
    if fix_yaml_file(filepath, is_directive=False):
        fixed_pasm2 += 1

print(f"Fixed {fixed_pasm2} PASM2 instruction files")

# Process all directive files
print("\nProcessing assembly directive YAMLs...")
directive_files = list(DIRECTIVES_PATH.glob("*.yaml"))
fixed_directives = 0

for filepath in directive_files:
    if fix_yaml_file(filepath, is_directive=True):
        fixed_directives += 1

print(f"Fixed {fixed_directives} directive files")

# Synchronize grouped instructions
sync_count = synchronize_grouped_instructions()

# Report all changes
print("\n" + "="*60)
print("CLEANUP SUMMARY")
print("="*60)

total_changes = len(changes_made)
print(f"\nTotal files modified: {total_changes}")

if total_changes > 0:
    print("\nChanges by instruction (first 20):")
    for inst, changes in list(changes_made.items())[:20]:
        print(f"\n{inst}:")
        for change in changes[:3]:  # Show first 3 changes per instruction
            print(f"  - {change}")
        if len(changes) > 3:
            print(f"  ... and {len(changes) - 3} more changes")

    # Summary of change types
    change_types = defaultdict(int)
    for changes in changes_made.values():
        for change in changes:
            if "Fixed timing.cycles" in change:
                change_types["timing_fixes"] += 1
            elif "Removed obsolete" in change:
                change_types["obsolete_removed"] += 1
            elif "documentation_level" in change:
                change_types["doc_level_fixed"] += 1
            elif "Renamed field" in change:
                change_types["field_renamed"] += 1
            elif "Synchronized" in change:
                change_types["synchronized"] += 1
            elif "Fixed compiler" in change:
                change_types["compiler_fixed"] += 1
    
    print("\nChange type summary:")
    for change_type, count in change_types.items():
        print(f"  {change_type}: {count}")

print("\n✅ Cleanup complete!")
print("Run 'python3 analyze_instruction_coverage.py' to verify the improvements")
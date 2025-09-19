#!/usr/bin/env python3
"""
Fix grouped instructions by copying documentation from the better-documented
member to the less-documented members of each group.
"""

import yaml
from pathlib import Path
import shutil
from datetime import datetime

# Paths
PASM2_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2")

# Load the analysis data
print("Loading instruction analysis...")
data = yaml.safe_load(open('instruction_analysis.yaml'))
yaml_items = data['yaml_items']

# Find all grouped instructions with mismatched scores
grouped_pairs = {}
for name, info in yaml_items.items():
    if info.get('is_grouped_in_manual'):
        group = tuple(sorted(info['manual_group_members']))
        if group not in grouped_pairs:
            grouped_pairs[group] = []
        grouped_pairs[group].append((name, info['score']))

# Find groups with mismatched scores
mismatched_groups = []
for group, members in sorted(grouped_pairs.items()):
    scores = [score for _, score in members]
    if len(set(scores)) > 1:  # Different scores in the group
        # Find the best-documented member
        best_member = max(members, key=lambda x: x[1])
        worst_member = min(members, key=lambda x: x[1])
        score_diff = best_member[1] - worst_member[1]
        
        if score_diff >= 10:  # Significant difference
            mismatched_groups.append({
                'group': group,
                'members': members,
                'best': best_member,
                'worst': worst_member,
                'diff': score_diff
            })

print(f"\nFound {len(mismatched_groups)} groups with significant mismatches (>= 10 points)")

# Sort by score difference
mismatched_groups.sort(key=lambda x: x['diff'], reverse=True)

# Show what will be fixed
print("\nGroups to fix (sorted by score difference):")
print("=" * 60)
for group_info in mismatched_groups[:10]:  # Show top 10
    print(f"\n{' / '.join(group_info['group'])}: diff={group_info['diff']}")
    for name, score in group_info['members']:
        status = "✓ BEST" if (name, score) == group_info['best'] else "  FIX"
        print(f"  {status} {name}: {score}")

# Show what will be done
total_fixes = sum(len(g['members'])-1 for g in mismatched_groups)
print(f"\nWill update {total_fixes} YAML files")
print("Creating backups with .backup extension")
print("Starting fixes...")
print("=" * 60)

# Fix the mismatched groups
fixed_count = 0
for group_info in mismatched_groups:
    best_name, best_score = group_info['best']
    best_file = PASM2_PATH / f"{best_name.lower()}.yaml"
    
    # Load the best documentation
    with open(best_file, 'r') as f:
        best_data = yaml.safe_load(f)
    
    # Key fields to copy from the best-documented instruction
    fields_to_copy = [
        'description',
        'category', 
        'parameters',
        'flags_affected',
        'documentation_source',
        'documentation_level'
    ]
    
    # Update other members of the group
    for member_name, member_score in group_info['members']:
        if (member_name, member_score) == group_info['best']:
            continue  # Skip the best one
        
        member_file = PASM2_PATH / f"{member_name.lower()}.yaml"
        
        # Backup original
        backup_file = member_file.with_suffix('.yaml.backup')
        shutil.copy(member_file, backup_file)
        
        # Load member data
        with open(member_file, 'r') as f:
            member_data = yaml.safe_load(f)
        
        # Copy documentation fields from best to member
        for field in fields_to_copy:
            if field in best_data:
                # Special handling for description to keep instruction-specific parts
                if field == 'description':
                    # Replace member's description with the group description
                    member_data[field] = best_data[field]
                else:
                    member_data[field] = best_data[field]
        
        # Mark as updated
        member_data['last_updated'] = datetime.now().isoformat()
        member_data['update_note'] = f'Documentation synchronized with {best_name} (grouped instruction)'
        
        # Save updated YAML
        with open(member_file, 'w') as f:
            yaml.dump(member_data, f, default_flow_style=False, sort_keys=False)
        
        fixed_count += 1
        print(f"Fixed {member_name} (copied from {best_name})")

print(f"\n✅ Fixed {fixed_count} YAML files")
print("\nBackup files created with .backup extension")
print("Run 'python3 analyze_instruction_coverage.py' to verify the fixes")
#!/usr/bin/env python3
"""
Fix PASM2 instruction files - minimal changes only:
1. Clean up group/category duplication
2. Extract oneliner from the embedded descriptions
"""

import os
import yaml
import re
from pathlib import Path

# Path to PASM2 instruction files
pasm2_dir = Path("engineering/knowledge-base/P2/language/pasm2")

# Native P2 categories (normalized)
VALID_CATEGORIES = {
    'arithmetic', 'logic', 'bit_manipulation', 'memory_hub', 'memory_cog',
    'control_flow', 'pin_control', 'timing_events', 'cordic', 'streamer',
    'colorspace', 'interrupts', 'cog_control', 'stack_ops', 'special_ops',
    'misc_ops', 'indirection'  # Adding indirection based on what we saw
}

def extract_category_and_oneliner(text):
    """
    Extract clean category and oneliner from malformed text like:
    "Math Instruction - Add two unsigned values."
    """
    if not text:
        return None, None
    
    text = str(text).strip()
    
    # Common patterns we've seen:
    # "Category Type - Description"
    # "Category_Type - Description" 
    # "Category Type"
    
    # Split on ' - ' first
    if ' - ' in text:
        category_part, desc_part = text.split(' - ', 1)
        oneliner = desc_part.strip().rstrip('.')
    else:
        category_part = text
        oneliner = None
    
    # Clean up the category part
    # Remove "Instruction" suffix
    category_part = category_part.replace(' Instruction', '').replace('_Instruction', '')
    category_part = category_part.replace('_', ' ')
    
    # Map to standard categories
    category_lower = category_part.lower().strip()
    
    # Try to match to our valid categories
    if 'math' in category_lower or 'arithmetic' in category_lower:
        category = 'arithmetic'
    elif 'logic' in category_lower:
        category = 'logic'
    elif 'bit' in category_lower:
        category = 'bit_manipulation'
    elif 'memory' in category_lower and 'hub' in category_lower:
        category = 'memory_hub'
    elif 'memory' in category_lower and ('cog' in category_lower or 'lut' in category_lower):
        category = 'memory_cog'
    elif 'control' in category_lower or 'jump' in category_lower or 'call' in category_lower or 'branch' in category_lower:
        category = 'control_flow'
    elif 'pin' in category_lower or 'smart' in category_lower:
        category = 'pin_control'
    elif 'timing' in category_lower or 'event' in category_lower or 'wait' in category_lower:
        category = 'timing_events'
    elif 'cordic' in category_lower:
        category = 'cordic'
    elif 'stream' in category_lower:
        category = 'streamer'
    elif 'color' in category_lower or 'pixel' in category_lower:
        category = 'colorspace'
    elif 'interrupt' in category_lower:
        category = 'interrupts'
    elif 'cog' in category_lower:
        category = 'cog_control'
    elif 'stack' in category_lower or 'push' in category_lower or 'pop' in category_lower:
        category = 'stack_ops'
    elif 'indirect' in category_lower or 'alter' in category_lower or 'alt' in category_lower:
        category = 'indirection'
    elif 'special' in category_lower:
        category = 'special_ops'
    else:
        # Default to misc if we can't categorize
        category = 'misc_ops'
    
    return category, oneliner

def fix_file(yaml_file):
    """Fix a single PASM2 file"""
    changes = []
    
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        
        if not data:
            return None
        
        original_data = dict(data)  # Keep original for comparison
        
        # Priority 1: Fix group/category mess
        if 'group' in data and 'category' in data:
            # Both exist - need to extract oneliner from one of them
            # Usually 'category' has the more detailed text
            category, oneliner = extract_category_and_oneliner(data['category'])
            if not oneliner and data['group']:
                # Try group if category didn't have a description
                category2, oneliner = extract_category_and_oneliner(data['group'])
                if not category:
                    category = category2
            
            data['category'] = category
            if oneliner:
                data['oneliner'] = oneliner
            del data['group']
            changes.append(f"Fixed duplicate group/category -> category: {category}, oneliner: {oneliner}")
            
        elif 'group' in data and 'category' not in data:
            # Only group exists - convert to category
            category, oneliner = extract_category_and_oneliner(data['group'])
            data['category'] = category
            if oneliner:
                data['oneliner'] = oneliner
            del data['group']
            changes.append(f"Converted group -> category: {category}, oneliner: {oneliner}")
            
        elif 'category' in data and 'group' not in data:
            # Only category exists - extract oneliner if needed
            if ' - ' in str(data['category']) or '_' in str(data['category']):
                category, oneliner = extract_category_and_oneliner(data['category'])
                data['category'] = category
                if oneliner:
                    data['oneliner'] = oneliner
                changes.append(f"Cleaned category: {category}, oneliner: {oneliner}")
        
        # Priority 2: If no oneliner yet, try to get from brief_description
        if 'oneliner' not in data and 'brief_description' in data:
            data['oneliner'] = str(data['brief_description']).strip()
            changes.append(f"Used brief_description as oneliner")
        
        # Only write if we made changes
        if changes:
            with open(yaml_file, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False, width=120)
            return changes
        
    except Exception as e:
        print(f"Error processing {yaml_file.name}: {e}")
        return None
    
    return None

# Process all files
yaml_files = sorted(list(pasm2_dir.glob("*.yaml")))
print(f"Processing {len(yaml_files)} PASM2 instruction files...\n")

total_fixed = 0
categories_found = set()

for yaml_file in yaml_files:
    changes = fix_file(yaml_file)
    if changes:
        total_fixed += 1
        print(f"Fixed {yaml_file.name}:")
        for change in changes:
            print(f"  - {change}")
        
        # Track what categories we're using
        try:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)
                if data and 'category' in data:
                    categories_found.add(data['category'])
        except:
            pass

print(f"\n{'='*60}")
print(f"SUMMARY: Fixed {total_fixed} of {len(yaml_files)} files")
print(f"\nCategories in use: {sorted(categories_found)}")

# Check how many still need oneliners
missing_oneliner = 0
for yaml_file in yaml_files:
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
            if data and 'oneliner' not in data:
                missing_oneliner += 1
    except:
        pass

if missing_oneliner > 0:
    print(f"\nWARNING: {missing_oneliner} files still missing oneliner field")
    print("These will need manual review or extraction from description field")
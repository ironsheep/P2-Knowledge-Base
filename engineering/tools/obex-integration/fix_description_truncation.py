#!/usr/bin/env python3
"""
Fix description_short truncation issues in object YAML files
"""

import os
import yaml
from pathlib import Path
import time

class DescriptionTruncationFixer:
    def __init__(self, objects_dir):
        self.objects_dir = Path(objects_dir)
        self.truncation_issues = []
        
    def find_truncation_issues(self):
        """Find all objects with truncated description_short fields"""
        print("Analyzing description_short truncation issues...")
        
        for yaml_file in sorted(self.objects_dir.glob("*.yaml")):
            if yaml_file.name == "_template.yaml":
                continue
                
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                obj_id = data['object_metadata']['object_id']
                title = data['object_metadata']['title']
                desc_full = data['object_metadata']['functionality'].get('description_full', '')
                desc_short = data['object_metadata']['functionality'].get('description_short', '')
                
                # Check for potential truncation issues
                is_truncated = False
                truncation_type = ""
                
                # Pattern 1: description_short appears to be cut off mid-word
                if desc_short and not desc_short.endswith(('.', '!', '?', ')', ']', '}', '"', "'")):
                    # Check if it ends with an incomplete word
                    last_word = desc_short.split()[-1] if desc_short.split() else ""
                    if len(last_word) < 4 and last_word.isalpha():
                        is_truncated = True
                        truncation_type = "mid_word"
                
                # Pattern 2: description_short is exactly 200 characters (common truncation length)
                if len(desc_short) == 200:
                    is_truncated = True
                    truncation_type = "200_char_limit"
                
                # Pattern 3: description_full contains more text that could complete description_short
                if desc_short and desc_full and desc_full.startswith(desc_short):
                    remaining_text = desc_full[len(desc_short):]
                    if remaining_text and len(remaining_text) < 50:  # Short completion
                        is_truncated = True
                        truncation_type = "incomplete_from_full"
                
                if is_truncated:
                    # Try to create a better description_short from description_full
                    better_desc_short = self.create_better_description_short(desc_full, desc_short)
                    
                    issue = {
                        'object_id': obj_id,
                        'title': title,
                        'file_path': yaml_file,
                        'current_desc_short': desc_short,
                        'desc_full': desc_full,
                        'better_desc_short': better_desc_short,
                        'truncation_type': truncation_type
                    }
                    self.truncation_issues.append(issue)
                    
                    print(f"❌ {obj_id}: {truncation_type} truncation")
                    print(f"   Current: {desc_short[:100]}...")
                    print(f"   Better:  {better_desc_short[:100]}...")
                    print()
                    
            except Exception as e:
                print(f"Error processing {yaml_file}: {e}")
        
        print(f"Found {len(self.truncation_issues)} objects with description truncation issues")
        return self.truncation_issues
    
    def create_better_description_short(self, desc_full, current_short):
        """Create a better description_short from description_full"""
        if not desc_full:
            return current_short
        
        # Clean up the full description - remove HTML artifacts
        clean_full = desc_full
        
        # Remove HTML-style tags and artifacts
        import re
        clean_full = re.sub(r'<[^>]+>', '', clean_full)  # Remove HTML tags
        clean_full = re.sub(r'&[a-zA-Z]+;', '', clean_full)  # Remove HTML entities
        clean_full = re.sub(r'\s+', ' ', clean_full)  # Normalize whitespace
        clean_full = clean_full.strip()
        
        # If the current short description appears to be a prefix of the full description
        if clean_full.startswith(current_short):
            remaining = clean_full[len(current_short):]
            
            # Look for a good breaking point within the next 50 characters
            for i, char in enumerate(remaining[:50]):
                if char in '.!?':
                    return current_short + remaining[:i+1]
                elif char in ')]}"' and i > 5:
                    return current_short + remaining[:i+1]
            
            # If no good break point, look for word boundary
            words = remaining.split()
            if words:
                # Add words until we hit a reasonable length or natural break
                result = current_short
                for word in words[:5]:  # Max 5 additional words
                    result += word
                    if len(result) > 250:  # Don't make it too long
                        break
                    if word.endswith(('.', '!', '?', ')', ']', '}')):
                        break
                    result += ' '
                return result.strip()
        
        # Fallback: create new description_short from first sentence of clean_full
        sentences = re.split(r'[.!?]+', clean_full)
        if sentences and len(sentences[0]) > 20:
            first_sentence = sentences[0].strip()
            if len(first_sentence) < 300:
                return first_sentence + '.'
        
        # Final fallback: return first 200 characters with word boundary
        if len(clean_full) > 200:
            truncated = clean_full[:200]
            last_space = truncated.rfind(' ')
            if last_space > 150:
                return truncated[:last_space] + '...'
        
        return clean_full if len(clean_full) < 300 else current_short
    
    def fix_truncation_issues(self):
        """Fix all identified truncation issues"""
        if not self.truncation_issues:
            print("No truncation issues to fix.")
            return 0
        
        print(f"Fixing {len(self.truncation_issues)} description truncation issues...")
        
        fixed_count = 0
        for issue in self.truncation_issues:
            try:
                with open(issue['file_path'], 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                # Update the description_short
                old_desc = data['object_metadata']['functionality']['description_short']
                data['object_metadata']['functionality']['description_short'] = issue['better_desc_short']
                
                # Update metadata
                current_time = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                if 'metadata' not in data['object_metadata']:
                    data['object_metadata']['metadata'] = {}
                
                data['object_metadata']['metadata']['last_description_fix'] = current_time
                
                # Write back to file
                with open(issue['file_path'], 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
                
                print(f"✓ Fixed {issue['object_id']}: {issue['title']}")
                print(f"   Old: {old_desc[:80]}...")
                print(f"   New: {issue['better_desc_short'][:80]}...")
                print()
                
                fixed_count += 1
                
            except Exception as e:
                print(f"✗ Error fixing {issue['object_id']}: {e}")
        
        print(f"✓ Fixed {fixed_count}/{len(self.truncation_issues)} description truncation issues")
        return fixed_count

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    fixer = DescriptionTruncationFixer(objects_dir)
    
    print("DESCRIPTION TRUNCATION ANALYSIS AND FIX")
    print("=" * 60)
    
    # Find all truncation issues
    issues = fixer.find_truncation_issues()
    
    if issues:
        print(f"\n🔧 FIXING TRUNCATION ISSUES:")
        print("-" * 40)
        
        # Fix the issues
        fixed_count = fixer.fix_truncation_issues()
        
        print(f"\n✅ DESCRIPTION FIX COMPLETE:")
        print(f"   Issues found: {len(issues)}")
        print(f"   Issues fixed: {fixed_count}")
        
        if fixed_count > 0:
            print(f"\n📝 Next step: Regenerate manifests to pick up the fixed descriptions")
    else:
        print("\n✅ No description truncation issues found!")

if __name__ == "__main__":
    main()
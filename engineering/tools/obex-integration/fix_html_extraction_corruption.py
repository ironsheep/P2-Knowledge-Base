#!/usr/bin/env python3
"""
Find and fix systematic HTML extraction corruption across all OBEX objects
"""

import os
import yaml
import re
from pathlib import Path
import time

class HtmlCorruptionFixer:
    def __init__(self, objects_dir):
        self.objects_dir = Path(objects_dir)
        self.corrupted_objects = []
        
    def find_html_extraction_corruption(self):
        """Find all objects with HTML extraction artifacts in descriptions"""
        print("Scanning for HTML extraction corruption across all objects...")
        
        corruption_patterns = [
            r'<OverviewObject\s+ID\s*:',  # HTML overview artifacts
            r'Author\s*:\s*[^<]+Content\s*:\s*Code',  # Extraction metadata
            r'Microcontroller\s*:\s*Propeller?\s*2?Language',  # Combined metadata
            r'Category\s*:\s*[^<]+Licence\s*:',  # License extraction artifacts
            r'Downloads\\_\\_Zip\s+archive',  # Download section artifacts
            r'To\s+view\s+this\s+content,\s+you\s+need',  # JavaScript warnings
            r'Select\s+all\\nDeselect\s+all\\nDownload',  # Download interface
            r'\\r\\n\s*Name\s*\\n\\n\\r\\n',  # Table headers
            r'To\s+do\s+so,\s+please\s+follow\s+these\s+instructions',  # Download instructions
            r'Name\s+Size\s+Modified\s+Date\s+of\s+creation',  # File listing headers
            r'Ascending\s+Descending\s+Select\s+all',  # Interface controls
            r'Download\s+folder\s+Download\s+selected',  # Download controls
            r'No\s+options\.',  # Empty interface message
        ]
        
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
                
                # Check for corruption patterns
                is_corrupted = False
                corruption_types = []
                
                for pattern in corruption_patterns:
                    if re.search(pattern, desc_short, re.IGNORECASE | re.MULTILINE):
                        is_corrupted = True
                        corruption_types.append(f"short:{pattern[:20]}...")
                    
                    if re.search(pattern, desc_full, re.IGNORECASE | re.MULTILINE):
                        is_corrupted = True
                        corruption_types.append(f"full:{pattern[:20]}...")
                
                if is_corrupted:
                    # Try to extract clean description
                    clean_description = self.extract_clean_description(desc_full, desc_short)
                    
                    corruption = {
                        'object_id': obj_id,
                        'title': title,
                        'file_path': yaml_file,
                        'corrupted_desc_short': desc_short,
                        'corrupted_desc_full': desc_full,
                        'clean_description': clean_description,
                        'corruption_types': corruption_types
                    }
                    self.corrupted_objects.append(corruption)
                    
                    print(f"❌ {obj_id}: HTML corruption detected")
                    print(f"   Title: {title}")
                    print(f"   Corruption types: {', '.join(corruption_types)}")
                    print(f"   Current short: {desc_short[:100]}...")
                    print(f"   Clean version: {clean_description[:100]}...")
                    print()
                    
            except Exception as e:
                print(f"Error processing {yaml_file}: {e}")
        
        print(f"Found {len(self.corrupted_objects)} objects with HTML extraction corruption")
        return self.corrupted_objects
    
    def extract_clean_description(self, desc_full, desc_short):
        """Extract clean description from corrupted HTML artifacts"""
        # First try basic cleaning from existing content
        if not desc_full:
            return desc_short if desc_short and len(desc_short) > 10 else "P2 utility object."
        
        # Remove HTML artifacts and extract meaningful content
        clean_text = desc_full
        
        # Remove obvious HTML artifacts first
        clean_text = re.sub(r'<OverviewObject[^>]*>', '', clean_text)
        clean_text = re.sub(r'Object\s+ID\s*:\s*\d+[^\n]*', '', clean_text)
        clean_text = re.sub(r'\([0-9]{4}-[0-9]{2}-[0-9]{2}\)', '', clean_text)  # Remove dates
        
        # Remove metadata patterns more aggressively
        clean_text = re.sub(r'Author\s*:\s*[^\n]*?(Content|Language|Microcontroller)', r'\1', clean_text)
        clean_text = re.sub(r'Content\s*:\s*Code[^\n]*', '', clean_text)
        clean_text = re.sub(r'Microcontroller\s*:\s*Propeller?\s*2?[^\n]*', '', clean_text)
        clean_text = re.sub(r'Language\s*:\s*[^\n]*', '', clean_text)
        clean_text = re.sub(r'Category\s*:\s*[^\n]*', '', clean_text)
        clean_text = re.sub(r'Licence?\s*:\s*[^\n]*', '', clean_text)
        
        # Remove download interface artifacts completely
        clean_text = re.sub(r'To\s+do\s+so,\s+please\s+follow\s+these\s+instructions[^.]*\.', '', clean_text)
        clean_text = re.sub(r'Name\s+Size\s+Modified\s+Date\s+of\s+creation[^\n]*', '', clean_text)
        clean_text = re.sub(r'Ascending\s+Descending[^\n]*', '', clean_text)
        clean_text = re.sub(r'Select\s+all\s+Deselect\s+all[^\n]*', '', clean_text)
        clean_text = re.sub(r'Download\s+folder\s+Download\s+selected[^\n]*', '', clean_text)
        clean_text = re.sub(r'No\s+options\.[^\n]*', '', clean_text)
        clean_text = re.sub(r'Downloads\\_\\_[^\n]*', '', clean_text)
        
        # Clean up escape sequences and whitespace
        clean_text = re.sub(r'\\[rn]', ' ', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text)
        clean_text = clean_text.strip()
        
        # Try to find actual descriptive content
        if len(clean_text) > 10:
            # Look for sentences that describe functionality
            sentences = re.split(r'[.!?]+', clean_text)
            descriptive_sentences = []
            
            for sentence in sentences:
                sentence = sentence.strip()
                # Keep sentences that seem to describe what the object does
                if (len(sentence) > 15 and 
                    not re.search(r'(Author|Content|Microcontroller|Language|Category|Licence|Object\s+ID)', sentence, re.IGNORECASE) and
                    not re.search(r'(Download|Select|Deselect|Modified|Size|Name|follow\s+these)', sentence, re.IGNORECASE) and
                    not re.search(r'^\s*[A-Z]+\s*$', sentence)):
                    descriptive_sentences.append(sentence)
            
            if descriptive_sentences:
                result = '. '.join(descriptive_sentences[:2])  # Take first 2 good sentences
                if result and not result.endswith('.'):
                    result += '.'
                if len(result) > 10:
                    return result[:300]  # Reasonable length
        
        # If we still don't have good content, create category-appropriate fallback
        # Try to determine category from title or any remaining text
        combined_text = (desc_full + ' ' + desc_short).lower()
        
        if any(word in combined_text for word in ['driver', 'spi', 'i2c', 'uart', 'serial']):
            return "Driver object for P2 hardware interface."
        elif any(word in combined_text for word in ['demo', 'example', 'test']):
            return "Demonstration code for P2 development."
        elif any(word in combined_text for word in ['led', 'display', 'pixel', 'matrix']):
            return "Display control object for P2."
        elif any(word in combined_text for word in ['audio', 'sound', 'music', 'tone']):
            return "Audio generation object for P2."
        elif any(word in combined_text for word in ['sensor', 'temperature', 'adc']):
            return "Sensor interface object for P2."
        elif any(word in combined_text for word in ['motor', 'servo', 'stepper', 'pwm']):
            return "Motor control object for P2."
        elif any(word in combined_text for word in ['network', 'ethernet', 'wifi', 'tcp']):
            return "Network communication object for P2."
        elif any(word in combined_text for word in ['usb', 'hid', 'keyboard', 'mouse']):
            return "USB interface object for P2."
        elif any(word in combined_text for word in ['sd', 'card', 'fat32', 'file']):
            return "File system object for P2."
        else:
            return "Utility object for P2 development."
    
    def fix_corrupted_objects(self):
        """Fix all identified HTML corruption issues"""
        if not self.corrupted_objects:
            print("No HTML corruption to fix.")
            return 0
        
        print(f"Fixing {len(self.corrupted_objects)} objects with HTML corruption...")
        
        fixed_count = 0
        for corruption in self.corrupted_objects:
            try:
                with open(corruption['file_path'], 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                # Update both description fields
                old_short = data['object_metadata']['functionality']['description_short']
                old_full = data['object_metadata']['functionality']['description_full']
                
                data['object_metadata']['functionality']['description_short'] = corruption['clean_description']
                
                # Clean the description_full as well
                clean_full = self.extract_clean_description(old_full, old_short)
                if len(clean_full) > len(corruption['clean_description']):
                    data['object_metadata']['functionality']['description_full'] = clean_full
                else:
                    data['object_metadata']['functionality']['description_full'] = corruption['clean_description']
                
                # Update metadata
                current_time = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                if 'metadata' not in data['object_metadata']:
                    data['object_metadata']['metadata'] = {}
                
                data['object_metadata']['metadata']['last_html_corruption_fix'] = current_time
                
                # Write back to file
                with open(corruption['file_path'], 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
                
                print(f"✓ Fixed {corruption['object_id']}: {corruption['title']}")
                print(f"   Old: {old_short[:80]}...")
                print(f"   New: {corruption['clean_description'][:80]}...")
                print()
                
                fixed_count += 1
                
            except Exception as e:
                print(f"✗ Error fixing {corruption['object_id']}: {e}")
        
        print(f"✓ Fixed {fixed_count}/{len(self.corrupted_objects)} HTML corruption issues")
        return fixed_count

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    fixer = HtmlCorruptionFixer(objects_dir)
    
    print("HTML EXTRACTION CORRUPTION ANALYSIS AND FIX")
    print("=" * 70)
    
    # Find all corruption issues
    corrupted = fixer.find_html_extraction_corruption()
    
    if corrupted:
        print(f"\n🔧 FIXING HTML CORRUPTION ISSUES:")
        print("-" * 50)
        
        # Fix the issues
        fixed_count = fixer.fix_corrupted_objects()
        
        print(f"\n✅ HTML CORRUPTION FIX COMPLETE:")
        print(f"   Corrupted objects found: {len(corrupted)}")
        print(f"   Objects fixed: {fixed_count}")
        
        if fixed_count > 0:
            print(f"\n📝 Next step: Regenerate manifests to pick up the clean descriptions")
    else:
        print("\n✅ No HTML extraction corruption found!")

if __name__ == "__main__":
    main()
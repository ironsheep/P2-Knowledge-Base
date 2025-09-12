#!/usr/bin/env python3
"""
Complete OBEX Author Extraction Tool
Enhanced parsing to extract ALL authors from the rich OBEX page data we already collected
"""

import yaml
import os
import re
from collections import defaultdict, Counter
from pathlib import Path
from datetime import datetime

class CompleteAuthorExtractor:
    def __init__(self, objects_dir: str):
        self.objects_dir = Path(objects_dir)
        self.stats = {
            'processed': 0,
            'authors_updated': 0,
            'authors_found': defaultdict(list),
            'parsing_methods': Counter()
        }
        
        # Enhanced author extraction patterns
        self.author_patterns = [
            # Pattern 1: "Author : Name" format
            (r'Author\s*:\s*([^\\n\\r<]+?)(?:Content|Language|Microcontroller)', 'colon_format'),
            
            # Pattern 2: "By Name" format  
            (r'(?:By|Created by|Submitted by)\s*:\s*([^\\n\\r<]+)', 'by_format'),
            
            # Pattern 3: Username format like "jonnymac"
            (r'Tags\s*:[^\\n]*?([a-z][a-z0-9_-]{3,15})(?:,|\s|\\n)', 'username_tag'),
            
            # Pattern 4: Email or username in content
            (r'(?:Contact|Email|Author).*?([a-zA-Z][a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+)', 'email'),
            
            # Pattern 5: GitHub/forum style username
            (r'(?:github\.com/|forums\.parallax\.com/.*?/)([a-zA-Z][a-zA-Z0-9_-]{2,20})', 'social_username'),
        ]
        
        # Known author mappings for cleanup
        self.author_mappings = {
            'jonnymac': 'Jon McPhalen (jonnymac)',
            'jon mcphalen': 'Jon McPhalen (jonnymac)',
            'chip gracey': 'Chip Gracey',
            'cgracey': 'Chip Gracey',
            'kwabena w. agyeman': 'Kwabena W. Agyeman',
            'kwabena agyeman': 'Kwabena W. Agyeman',
            'stephen moraco': 'Stephen M Moraco',
            'stephen m moraco': 'Stephen M Moraco',
            'stephen m. moraco': 'Stephen M Moraco',
        }

    def extract_author_from_content(self, obj_id: str, title: str, description: str) -> tuple:
        """Extract author using multiple parsing strategies"""
        
        # Strategy 1: ISP prefix = Stephen M Moraco
        if title.startswith('ISP '):
            return 'Stephen M Moraco', 'isp_prefix'
        
        # Strategy 2: Try all regex patterns
        for pattern, method in self.author_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                candidate = match.strip()
                
                # Clean up the candidate
                candidate = re.sub(r'[<>"\']', '', candidate)  # Remove HTML/quotes
                candidate = re.sub(r'\s+', ' ', candidate)     # Normalize spaces
                candidate = candidate.strip()
                
                # Validate candidate
                if self._is_valid_author(candidate):
                    # Apply mappings
                    author_clean = self._normalize_author(candidate)
                    if author_clean:
                        return author_clean, method
        
        # Strategy 3: Look for common P2 author names even without perfect patterns
        known_authors = ['chip gracey', 'jon mcphalen', 'jonnymac', 'kwabena', 'stephen moraco', 'borri']
        desc_lower = description.lower()
        
        for known in known_authors:
            if known in desc_lower:
                return self._normalize_author(known), 'known_name_search'
        
        return None, 'not_found'

    def _is_valid_author(self, candidate: str) -> bool:
        """Validate if a candidate string looks like an author name"""
        if not candidate or len(candidate) < 2:
            return False
        if len(candidate) > 50:
            return False
        
        # Reject obvious non-names
        reject_patterns = [
            r'^(content|code|microcontroller|language|category|licence|tags?)$',
            r'^(propeller|spin2?|pasm2?)$',
            r'^(download|zip|archive|file)s?$',
            r'^[0-9\-\s]+$',
            r'^\w{1}$',
        ]
        
        for reject in reject_patterns:
            if re.match(reject, candidate, re.IGNORECASE):
                return False
        
        # Must contain at least some letters
        if not re.search(r'[a-zA-Z]', candidate):
            return False
            
        return True

    def _normalize_author(self, author: str) -> str:
        """Normalize and map author names to canonical forms"""
        author_lower = author.lower().strip()
        
        # Direct mappings
        if author_lower in self.author_mappings:
            return self.author_mappings[author_lower]
        
        # Pattern-based normalization
        if 'mcphalen' in author_lower or author_lower == 'jonnymac':
            return 'Jon McPhalen (jonnymac)'
        elif 'gracey' in author_lower:
            return 'Chip Gracey'
        elif 'agyeman' in author_lower:
            return 'Kwabena W. Agyeman'
        elif 'moraco' in author_lower and 'stephen' in author_lower:
            return 'Stephen M Moraco'
        elif 'borri' in author_lower:
            return 'm.k. borri'
        
        # Title case for unknown authors
        return author.title()

    def extract_enhanced_metadata(self, description: str) -> dict:
        """Extract additional metadata from the rich description"""
        metadata = {
            'creation_date': '',
            'object_id_confirmed': '',
            'license': '',
            'tags_extracted': [],
            'language_confirmed': []
        }
        
        # Extract creation date
        date_match = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', description)
        if date_match:
            metadata['creation_date'] = date_match.group(1)
        
        # Extract Object ID
        id_match = re.search(r'Object\s+ID\s*:\s*(\d+)', description)
        if id_match:
            metadata['object_id_confirmed'] = id_match.group(1)
        
        # Extract License
        license_match = re.search(r'Licence\s*:\s*([A-Z][A-Za-z\s]+)', description)
        if license_match:
            metadata['license'] = license_match.group(1).strip()
        
        # Extract Tags
        tags_match = re.search(r'Tags\s*:\s*([^\\n]+)', description)
        if tags_match:
            tags_raw = tags_match.group(1)
            tags = [t.strip() for t in tags_raw.split(',') if t.strip()]
            metadata['tags_extracted'] = tags[:10]  # Limit tags
        
        # Confirm Language
        if 'Language : SPIN2' in description:
            metadata['language_confirmed'].append('SPIN2')
        if 'Language : PASM2' in description:
            metadata['language_confirmed'].append('PASM2')
        if 'SPIN2 PASM2' in description:
            metadata['language_confirmed'] = ['SPIN2', 'PASM2']
            
        return metadata

    def process_all_objects(self):
        """Process all object files to complete author extraction"""
        print("🚀 Starting complete author extraction...")
        
        object_files = list(self.objects_dir.glob("*.yaml"))
        object_files = [f for f in object_files if f.name != '_template.yaml']
        
        print(f"📦 Processing {len(object_files)} objects...")
        
        for i, object_file in enumerate(object_files, 1):
            obj_id = object_file.stem
            
            try:
                # Load existing object
                with open(object_file, 'r') as f:
                    data = yaml.safe_load(f)
                
                obj = data['object_metadata']
                title = obj['title']
                description = obj['functionality'].get('description_full', '')
                current_author = obj.get('author', '').strip()
                
                # Extract author and metadata
                author, method = self.extract_author_from_content(obj_id, title, description)
                enhanced_meta = self.extract_enhanced_metadata(description)
                
                # Update object if we found better information
                updated = False
                
                if author and (not current_author or current_author == '' or len(author) > len(current_author)):
                    obj['author'] = author
                    self.stats['authors_found'][author].append(obj_id)
                    self.stats['parsing_methods'][method] += 1
                    updated = True
                    print(f"  ✅ {obj_id}: {author} ({method})")
                elif current_author:
                    # Keep existing author
                    normalized = self._normalize_author(current_author)
                    if normalized != current_author:
                        obj['author'] = normalized
                        updated = True
                    self.stats['authors_found'][normalized or current_author].append(obj_id)
                    print(f"  📋 {obj_id}: {normalized or current_author} (existing)")
                else:
                    self.stats['authors_found']['Unknown'].append(obj_id)
                    print(f"  ❓ {obj_id}: Unknown")
                
                # Update enhanced metadata
                if enhanced_meta['creation_date'] and not obj['metadata'].get('created_date'):
                    obj['metadata']['created_date'] = enhanced_meta['creation_date']
                    updated = True
                
                if enhanced_meta['license']:
                    obj['metadata']['license'] = enhanced_meta['license']
                    updated = True
                
                if enhanced_meta['tags_extracted']:
                    existing_tags = set(obj['functionality'].get('tags', []))
                    new_tags = set(enhanced_meta['tags_extracted'])
                    combined = list(existing_tags.union(new_tags))
                    if len(combined) > len(existing_tags):
                        obj['functionality']['tags'] = combined
                        updated = True
                
                if enhanced_meta['language_confirmed']:
                    obj['technical_details']['languages_confirmed'] = enhanced_meta['language_confirmed']
                    updated = True
                
                # Save if updated
                if updated:
                    obj['metadata']['last_complete_extraction'] = datetime.now().isoformat()
                    obj['metadata']['extraction_status'] = 'complete'
                    
                    with open(object_file, 'w') as f:
                        yaml.dump(data, f, default_flow_style=False, indent=2)
                    
                    self.stats['authors_updated'] += 1
                
                self.stats['processed'] += 1
                
            except Exception as e:
                print(f"  ❌ Error processing {obj_id}: {e}")
        
        # Print final statistics
        print(f"\n{'='*60}")
        print("🎯 COMPLETE AUTHOR EXTRACTION FINISHED")
        print(f"{'='*60}")
        print(f"📦 Objects processed: {self.stats['processed']}")
        print(f"✅ Objects updated: {self.stats['authors_updated']}")
        
        print(f"\n📊 PARSING METHODS:")
        for method, count in self.stats['parsing_methods'].most_common():
            print(f"  {method}: {count}")
        
        print(f"\n👥 FINAL AUTHOR DISTRIBUTION:")
        for author, objects in sorted(self.stats['authors_found'].items(), key=lambda x: len(x[1]), reverse=True):
            count = len(objects)
            print(f"  {author}: {count} objects")
            if count <= 5:
                print(f"    Objects: {', '.join(objects)}")

if __name__ == '__main__':
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    extractor = CompleteAuthorExtractor(objects_dir)
    extractor.process_all_objects()
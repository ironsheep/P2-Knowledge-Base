#!/usr/bin/env python3
"""
Final OBEX Author Cleanup
Fix all remaining author extraction issues with precise parsing
"""

import yaml
import os
import re
from collections import defaultdict, Counter
from pathlib import Path
from datetime import datetime

class FinalAuthorCleanup:
    def __init__(self, objects_dir: str):
        self.objects_dir = Path(objects_dir)
        self.stats = {
            'processed': 0,
            'fixed': 0,
            'final_authors': defaultdict(list)
        }
        
        # Author name mappings
        self.author_mappings = {
            'jon mcphalen': 'Jon McPhalen (jonnymac)',
            'jonnymac': 'Jon McPhalen (jonnymac)', 
            'chip gracey': 'Chip Gracey',
            'cgracey': 'Chip Gracey',
            'm.k. borri': 'm.k. borri',
            'kwabena w. agyeman': 'Kwabena W. Agyeman',
            'kwabena agyeman': 'Kwabena W. Agyeman',
            'ray allen': 'Ray Allen',
            'eric smith': 'Eric Smith',
            'greg lapolla': 'Greg LaPolla'
        }

    def extract_author_precisely(self, title: str, description: str) -> str:
        """Extract author with very precise patterns"""
        
        # ISP objects = Stephen M Moraco
        if title.startswith('ISP '):
            return 'Stephen M Moraco'
        
        # Primary pattern: "Author : Name" in the description
        author_match = re.search(r'Author\s*:\s*([^\\\\]+?)(?:Content|Language|Microcontroller|\\\n)', description)
        if author_match:
            author = author_match.group(1).strip()
            # Clean up the author name
            author = re.sub(r'[\\\\n\\\\r<>"]', '', author).strip()
            return self._normalize_author(author)
        
        # Secondary patterns
        patterns = [
            r'(?:By|Created by|Submitted by)\s*:\s*([^\\\\n]+?)(?:\s|\\\\n|$)',
            r'(?:Contact|Email):\s*([a-zA-Z\s.]+?)(?:\s|\\\\n|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                candidate = match.group(1).strip()
                if self._is_valid_author(candidate):
                    return self._normalize_author(candidate)
        
        return 'Unknown'

    def _normalize_author(self, author: str) -> str:
        """Normalize author names"""
        if not author:
            return 'Unknown'
            
        author_clean = author.lower().strip()
        
        # Direct mapping
        if author_clean in self.author_mappings:
            return self.author_mappings[author_clean]
        
        # Pattern-based cleanup
        if 'mcphalen' in author_clean or 'jonnymac' in author_clean:
            return 'Jon McPhalen (jonnymac)'
        elif 'gracey' in author_clean:
            return 'Chip Gracey'
        elif 'agyeman' in author_clean:
            return 'Kwabena W. Agyeman'
        elif 'moraco' in author_clean:
            return 'Stephen M Moraco'
        elif 'borri' in author_clean:
            return 'm.k. borri'
        elif 'lapolla' in author_clean:
            return 'Greg LaPolla'
        elif 'allen' in author_clean and 'ray' in author_clean:
            return 'Ray Allen'
        elif 'smith' in author_clean and 'eric' in author_clean:
            return 'Eric Smith'
        
        # Return title case for unknown but valid authors
        if self._is_valid_author(author):
            return author.title()
        
        return 'Unknown'

    def _is_valid_author(self, author: str) -> bool:
        """Check if author name looks valid"""
        if not author or len(author) < 2 or len(author) > 50:
            return False
        
        # Reject obvious non-names
        reject_words = [
            'content', 'code', 'microcontroller', 'language', 'category', 'licence', 
            'tags', 'propeller', 'spin2', 'pasm2', 'download', 'zip', 'archive',
            'temperature', 'click', 'applications', 'extension', 'header'
        ]
        
        author_lower = author.lower()
        for reject in reject_words:
            if reject == author_lower:
                return False
        
        # Must contain letters
        if not re.search(r'[a-zA-Z]', author):
            return False
        
        # Reject if mostly punctuation
        if len(re.sub(r'[a-zA-Z0-9\s]', '', author)) > len(author) // 2:
            return False
            
        return True

    def cleanup_all_authors(self):
        """Fix author information for all objects"""
        print("🔧 Starting final author cleanup...")
        
        object_files = list(self.objects_dir.glob("*.yaml"))
        object_files = [f for f in object_files if f.name != '_template.yaml']
        
        for object_file in object_files:
            obj_id = object_file.stem
            
            try:
                with open(object_file, 'r') as f:
                    data = yaml.safe_load(f)
                
                obj = data['object_metadata']
                title = obj['title']
                description = obj['functionality'].get('description_full', '')
                current_author = obj.get('author', '').strip()
                
                # Extract correct author
                correct_author = self.extract_author_precisely(title, description)
                
                # Check if we need to update
                needs_update = (
                    not current_author or
                    current_author == 'Unknown' or
                    not self._is_valid_author(current_author) or
                    len(correct_author) > len(current_author)
                )
                
                if needs_update and correct_author != 'Unknown':
                    obj['author'] = correct_author
                    obj['metadata']['last_author_cleanup'] = datetime.now().isoformat()
                    
                    with open(object_file, 'w') as f:
                        yaml.dump(data, f, default_flow_style=False, indent=2)
                    
                    print(f"  ✅ {obj_id}: {current_author or 'None'} → {correct_author}")
                    self.stats['fixed'] += 1
                else:
                    final_author = current_author if current_author and self._is_valid_author(current_author) else correct_author
                    print(f"  📋 {obj_id}: {final_author}")
                
                # Track final author distribution
                final_author = obj.get('author', 'Unknown')
                if not self._is_valid_author(final_author):
                    final_author = 'Unknown'
                    
                self.stats['final_authors'][final_author].append(obj_id)
                self.stats['processed'] += 1
                
            except Exception as e:
                print(f"  ❌ Error processing {obj_id}: {e}")
        
        # Print final results
        print(f"\n{'='*60}")
        print("🎯 FINAL AUTHOR CLEANUP COMPLETE")
        print(f"{'='*60}")
        print(f"📦 Objects processed: {self.stats['processed']}")
        print(f"🔧 Authors fixed: {self.stats['fixed']}")
        
        print(f"\n👥 FINAL AUTHOR DISTRIBUTION:")
        sorted_authors = sorted(self.stats['final_authors'].items(), key=lambda x: len(x[1]), reverse=True)
        
        for author, objects in sorted_authors:
            count = len(objects)
            print(f"  {author}: {count} objects")
            if count <= 5:
                print(f"    IDs: {', '.join(objects)}")

if __name__ == '__main__':
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    cleanup = FinalAuthorCleanup(objects_dir)
    cleanup.cleanup_all_authors()
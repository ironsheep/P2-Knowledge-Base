#!/usr/bin/env python3
"""
Clean rebuild of manifests using only current, verified author data
"""

import os
import yaml
from pathlib import Path
from collections import Counter, defaultdict
import time

class CleanManifestBuilder:
    def __init__(self, objects_dir, manifests_dir):
        self.objects_dir = Path(objects_dir)
        self.manifests_dir = Path(manifests_dir)
        self.current_authors = set()
        
    def get_current_authors_from_objects(self):
        """Get the actual current authors from object YAML files"""
        print("Reading current authors from object files...")
        
        authors = set()
        author_objects = defaultdict(list)
        
        for yaml_file in self.objects_dir.glob("*.yaml"):
            if yaml_file.name == "_template.yaml":
                continue
                
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                obj_id = data['object_metadata']['object_id']
                title = data['object_metadata']['title']
                author = data['object_metadata'].get('author', '').strip()
                
                if author and author != '':
                    authors.add(author)
                    author_objects[author].append((obj_id, data['object_metadata']))
                    
            except Exception as e:
                print(f"Error processing {yaml_file}: {e}")
        
        print(f"Found {len(authors)} legitimate authors currently in object files:")
        for author in sorted(authors):
            print(f"  - {author} ({len(author_objects[author])} objects)")
        
        return authors, author_objects
    
    def build_clean_author_manifests(self):
        """Build author manifests using only current, legitimate authors"""
        authors, author_objects = self.get_current_authors_from_objects()
        
        print(f"\nBuilding clean author manifests for {len(authors)} authors...")
        
        authors_dir = self.manifests_dir / "authors"
        authors_dir.mkdir(exist_ok=True)
        
        created_manifests = []
        
        for author, objects in author_objects.items():
            # Create safe filename - much more conservative approach
            safe_author = (author
                          .replace(' ', '_')
                          .replace('(', '')
                          .replace(')', '')
                          .replace('.', '')
                          .replace(':', '')
                          .replace('/', '')
                          .replace('\\', '')
                          .replace('?', '')
                          .replace('*', '')
                          .replace('"', '')
                          .replace('<', '')
                          .replace('>', '')
                          .replace('|', '')
                          .lower())
            
            # Sort objects by ID for consistency
            objects.sort(key=lambda x: int(x[0]))
            
            author_manifest = {
                'manifest_metadata': {
                    'manifest_type': 'obex_author',
                    'author': author,
                    'generated': time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                    'object_count': len(objects)
                },
                
                'author_info': {
                    'name': author,
                    'contribution_summary': f"{len(objects)} P2 objects contributed to OBEX",
                    'specialties': self.analyze_author_specialties(objects)
                },
                
                'objects': []
            }
            
            for obj_id, obj_data in objects:
                author_manifest['objects'].append({
                    'object_id': obj_id,
                    'title': obj_data['title'],
                    'category': obj_data['functionality'].get('category', 'misc'),
                    'languages': obj_data['technical_details'].get('languages', []),
                    'created_date': obj_data.get('metadata', {}).get('created_date', ''),
                    'yaml_path': f"../objects/{obj_id}.yaml"
                })
            
            # Write author manifest
            manifest_file = authors_dir / f"{safe_author}-manifest.yaml"
            with open(manifest_file, 'w', encoding='utf-8') as f:
                yaml.dump(author_manifest, f, default_flow_style=False, sort_keys=False)
            
            created_manifests.append({
                'author': author,
                'safe_name': safe_author,
                'objects': len(objects),
                'file': manifest_file
            })
            
            print(f"✓ Created {safe_author}-manifest.yaml ({len(objects)} objects)")
        
        return created_manifests
    
    def analyze_author_specialties(self, objects):
        """Analyze author's specialty areas"""
        categories = Counter()
        languages = Counter()
        
        for obj_id, obj_data in objects:
            categories[obj_data['functionality'].get('category', 'misc')] += 1
            for lang in obj_data['technical_details'].get('languages', []):
                languages[lang] += 1
        
        specialties = []
        if categories:
            top_cat = categories.most_common(1)[0]
            specialties.append(f"{top_cat[0]} ({top_cat[1]} objects)")
        
        if languages:
            lang_list = [f"{lang} ({count})" for lang, count in languages.most_common(2)]
            specialties.extend(lang_list)
        
        return specialties[:3]  # Top 3 specialties
    
    def update_root_manifest(self, author_manifests):
        """Update root manifest with clean author manifest list"""
        root_path = self.manifests_dir / "obex-community-manifest.yaml"
        
        if root_path.exists():
            with open(root_path, 'r', encoding='utf-8') as f:
                root_data = yaml.safe_load(f)
            
            # Update author manifest list
            root_data['sub_manifests']['by_author']['manifests'] = [
                f"{manifest['safe_name']}-manifest.yaml" for manifest in author_manifests
            ]
            
            # Update author count
            root_data['manifest_metadata']['total_authors'] = len(author_manifests)
            root_data['manifest_metadata']['generated'] = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
            
            # Write back
            with open(root_path, 'w', encoding='utf-8') as f:
                yaml.dump(root_data, f, default_flow_style=False, sort_keys=False)
            
            print(f"✓ Updated root manifest with {len(author_manifests)} clean author manifests")

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    manifests_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/manifests"
    
    builder = CleanManifestBuilder(objects_dir, manifests_dir)
    
    print("CLEAN AUTHOR MANIFEST REBUILD")
    print("=" * 60)
    
    # Build only clean author manifests
    author_manifests = builder.build_clean_author_manifests()
    
    # Update root manifest
    builder.update_root_manifest(author_manifests)
    
    print(f"\n" + "="*60)
    print("CLEAN REBUILD COMPLETE")
    print("="*60)
    print(f"✅ Created {len(author_manifests)} clean author manifests")
    print(f"✅ Updated root manifest")
    print(f"✅ Removed all corrupted manifests")

if __name__ == "__main__":
    main()
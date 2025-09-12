#!/usr/bin/env python3
"""
Rebuild complete OBEX manifest hierarchy with accurate data
"""

import os
import yaml
from pathlib import Path
from collections import Counter, defaultdict
import time

class ManifestBuilder:
    def __init__(self, objects_dir, manifests_dir):
        self.objects_dir = Path(objects_dir)
        self.manifests_dir = Path(manifests_dir)
        self.objects_data = {}
        self.category_stats = Counter()
        self.author_stats = Counter()
        self.language_stats = Counter()
        
    def load_all_objects(self):
        """Load all object data for analysis"""
        print("Loading all OBEX object data...")
        
        for yaml_file in self.objects_dir.glob("*.yaml"):
            if yaml_file.name == "_template.yaml":
                continue
                
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                obj_id = data['object_metadata']['object_id']
                self.objects_data[obj_id] = data['object_metadata']
                
                # Collect statistics
                category = data['object_metadata']['functionality'].get('category', 'misc')
                author = data['object_metadata'].get('author', 'Unknown').strip()
                languages = data['object_metadata']['technical_details'].get('languages', [])
                
                self.category_stats[category] += 1
                if author and author != 'Unknown':
                    self.author_stats[author] += 1
                
                for lang in languages:
                    self.language_stats[lang] += 1
                    
            except Exception as e:
                print(f"Error loading {yaml_file}: {e}")
        
        print(f"Loaded {len(self.objects_data)} objects")
        return self.objects_data
    
    def build_root_manifest(self):
        """Build the root OBEX community manifest"""
        print("Building root OBEX community manifest...")
        
        # Calculate totals
        total_objects = len(self.objects_data)
        total_authors = len([a for a in self.author_stats.keys() if a and a != 'Unknown'])
        
        root_manifest = {
            'manifest_metadata': {
                'manifest_type': 'obex_community_root',
                'version': '2.0',
                'generated': time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                'total_objects': total_objects,
                'total_authors': total_authors,
                'coverage_status': 'complete',
                'quality_metrics': {
                    'author_coverage': f"{total_authors}/{total_objects} ({total_authors/total_objects*100:.1f}%)",
                    'p1_p2_separation': 'complete',
                    'reference_filtering': 'complete'
                }
            },
            
            'community_overview': {
                'description': 'P2 (Propeller 2) community code objects from Parallax OBEX',
                'source_url': 'https://obex.parallax.com/microcontroller/propeller-2/',
                'extraction_methodology': 'Comprehensive discovery across 13 pages with P1/P2 filtering',
                'last_extraction': time.strftime('%Y-%m-%d'),
                'object_types': 'executable_code_only',
                'filtering_applied': [
                    'P1_objects_removed',
                    'reference_materials_removed', 
                    'P2_PASM2_SPIN2_only'
                ]
            },
            
            'statistics': {
                'by_category': dict(self.category_stats.most_common()),
                'by_language': dict(self.language_stats.most_common()),
                'top_contributors': dict(self.author_stats.most_common(10))
            },
            
            'sub_manifests': {
                'by_category': {
                    'path': 'categories/',
                    'manifests': [f"{cat}-manifest.yaml" for cat in self.category_stats.keys()]
                },
                'by_author': {
                    'path': 'authors/',
                    'manifests': [f"{author.replace(' ', '_').replace('(', '').replace(')', '').lower()}-manifest.yaml" 
                                for author in self.author_stats.keys() if author and author != 'Unknown']
                }
            },
            
            'access_patterns': {
                'individual_objects': {
                    'path': '../objects/',
                    'format': '{object_id}.yaml',
                    'example': '5281.yaml'
                },
                'download_on_demand': {
                    'enabled': True,
                    'base_url': 'https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB',
                    'format': '{base_url}{object_id}'
                }
            }
        }
        
        # Write root manifest
        root_path = self.manifests_dir / "obex-community-manifest.yaml"
        with open(root_path, 'w', encoding='utf-8') as f:
            yaml.dump(root_manifest, f, default_flow_style=False, sort_keys=False)
        
        print(f"✓ Created root manifest: {root_path}")
        return root_manifest
    
    def build_category_manifests(self):
        """Build category-specific manifests"""
        print("Building category manifests...")
        
        categories_dir = self.manifests_dir / "categories"
        categories_dir.mkdir(exist_ok=True)
        
        # Group objects by category
        category_objects = defaultdict(list)
        for obj_id, obj_data in self.objects_data.items():
            category = obj_data['functionality'].get('category', 'misc')
            category_objects[category].append((obj_id, obj_data))
        
        category_manifests = {}
        
        for category, objects in category_objects.items():
            # Sort objects by ID for consistency
            objects.sort(key=lambda x: int(x[0]))
            
            category_manifest = {
                'manifest_metadata': {
                    'manifest_type': 'obex_category',
                    'category': category,
                    'generated': time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                    'object_count': len(objects)
                },
                
                'category_info': {
                    'name': category,
                    'description': self.get_category_description(category),
                    'common_use_cases': self.get_category_use_cases(category)
                },
                
                'objects': []
            }
            
            for obj_id, obj_data in objects:
                category_manifest['objects'].append({
                    'object_id': obj_id,
                    'title': obj_data['title'],
                    'author': obj_data.get('author', 'Unknown'),
                    'languages': obj_data['technical_details'].get('languages', []),
                    'description_short': obj_data['functionality'].get('description_short', ''),
                    'yaml_path': f"../objects/{obj_id}.yaml"
                })
            
            # Write category manifest
            manifest_file = categories_dir / f"{category}-manifest.yaml"
            with open(manifest_file, 'w', encoding='utf-8') as f:
                yaml.dump(category_manifest, f, default_flow_style=False, sort_keys=False)
            
            category_manifests[category] = manifest_file
            print(f"✓ Created {category} manifest: {len(objects)} objects")
        
        return category_manifests
    
    def build_author_manifests(self):
        """Build author-specific manifests"""
        print("Building author manifests...")
        
        authors_dir = self.manifests_dir / "authors"
        authors_dir.mkdir(exist_ok=True)
        
        # Group objects by author
        author_objects = defaultdict(list)
        for obj_id, obj_data in self.objects_data.items():
            author = obj_data.get('author', 'Unknown').strip()
            if author and author != 'Unknown':
                author_objects[author].append((obj_id, obj_data))
        
        author_manifests = {}
        
        for author, objects in author_objects.items():
            # Sort objects by ID for consistency
            objects.sort(key=lambda x: int(x[0]))
            
            # Create safe filename
            safe_author = author.replace(' ', '_').replace('(', '').replace(')', '').replace('.', '').lower()
            
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
            
            author_manifests[author] = manifest_file
            print(f"✓ Created {author} manifest: {len(objects)} objects")
        
        return author_manifests
    
    def get_category_description(self, category):
        """Get description for category"""
        descriptions = {
            'drivers': 'Hardware interface and peripheral drivers for sensors, displays, and communication modules',
            'demos': 'Demonstration and example code showcasing P2 capabilities and techniques',
            'misc': 'Miscellaneous utilities and general-purpose code objects',
            'motors': 'Motor control, servo control, and motion system drivers',
            'tools': 'Development tools, utilities, and helper objects for P2 programming',
            'communication': 'Communication protocols, networking, and data exchange objects',
            'audio': 'Audio processing, sound generation, and audio interface drivers',
            'sensors': 'Sensor interface drivers and data acquisition objects'
        }
        return descriptions.get(category, f'Objects in the {category} category')
    
    def get_category_use_cases(self, category):
        """Get common use cases for category"""
        use_cases = {
            'drivers': ['Hardware interfacing', 'Sensor integration', 'Peripheral control'],
            'demos': ['Learning P2 programming', 'Feature exploration', 'Proof of concept'],
            'misc': ['General utilities', 'Helper functions', 'Common algorithms'],
            'motors': ['Robot control', 'Automation systems', 'Motion control'],
            'tools': ['Development workflow', 'Debugging', 'Code generation'],
            'communication': ['IoT connectivity', 'Data exchange', 'Protocol implementation'],
            'audio': ['Sound synthesis', 'Audio processing', 'Music applications'],
            'sensors': ['Data collection', 'Environmental monitoring', 'Measurement systems']
        }
        return use_cases.get(category, ['General purpose applications'])
    
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
    
    def validate_manifest_connectivity(self):
        """Validate that all manifests connect properly"""
        print("Validating manifest connectivity...")
        
        issues = []
        
        # Check root manifest exists
        root_path = self.manifests_dir / "obex-community-manifest.yaml"
        if not root_path.exists():
            issues.append("Root manifest missing")
            return issues
        
        # Load root manifest
        with open(root_path, 'r', encoding='utf-8') as f:
            root_data = yaml.safe_load(f)
        
        # Check category manifests
        categories_dir = self.manifests_dir / "categories"
        for category in self.category_stats.keys():
            manifest_file = categories_dir / f"{category}-manifest.yaml"
            if not manifest_file.exists():
                issues.append(f"Category manifest missing: {category}")
            else:
                # Validate content
                try:
                    with open(manifest_file, 'r', encoding='utf-8') as f:
                        cat_data = yaml.safe_load(f)
                    
                    expected_count = self.category_stats[category]
                    actual_count = len(cat_data['objects'])
                    if expected_count != actual_count:
                        issues.append(f"Category {category}: expected {expected_count}, got {actual_count}")
                        
                except Exception as e:
                    issues.append(f"Category {category} manifest error: {e}")
        
        # Check author manifests
        authors_dir = self.manifests_dir / "authors"
        for author in self.author_stats.keys():
            if author and author != 'Unknown':
                safe_author = author.replace(' ', '_').replace('(', '').replace(')', '').replace('.', '').lower()
                manifest_file = authors_dir / f"{safe_author}-manifest.yaml"
                if not manifest_file.exists():
                    issues.append(f"Author manifest missing: {author}")
        
        if issues:
            print("VALIDATION ISSUES FOUND:")
            for issue in issues:
                print(f"  ❌ {issue}")
        else:
            print("✅ All manifest connectivity validated successfully")
        
        return issues

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    manifests_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/manifests"
    
    builder = ManifestBuilder(objects_dir, manifests_dir)
    
    # Load all data
    builder.load_all_objects()
    
    print("\n" + "="*80)
    print("REBUILDING COMPLETE OBEX MANIFEST HIERARCHY")
    print("="*80)
    
    # Build manifests
    root_manifest = builder.build_root_manifest()
    category_manifests = builder.build_category_manifests()
    author_manifests = builder.build_author_manifests()
    
    # Validate connectivity
    issues = builder.validate_manifest_connectivity()
    
    print(f"\n" + "="*80)
    print("MANIFEST REBUILD COMPLETE")
    print("="*80)
    print(f"✅ Root manifest: 1 created")
    print(f"✅ Category manifests: {len(category_manifests)} created")
    print(f"✅ Author manifests: {len(author_manifests)} created")
    print(f"✅ Total objects: {len(builder.objects_data)}")
    print(f"✅ Connectivity validation: {'PASSED' if not issues else 'FAILED'}")
    
    if not issues:
        print(f"\n🎉 OBEX integration ready for commit and publishing!")

if __name__ == "__main__":
    main()
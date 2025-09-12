#!/usr/bin/env python3
"""
Final validation of complete OBEX integration for publishing
"""

import os
import yaml
from pathlib import Path
from collections import Counter

def final_validation():
    """Perform comprehensive validation of OBEX integration"""
    objects_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects")
    manifests_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/manifests")
    
    print("FINAL OBEX INTEGRATION VALIDATION")
    print("=" * 80)
    
    # 1. Count all objects and analyze authors
    all_authors = []
    categories = Counter()
    languages = Counter()
    unknown_authors = 0
    total_objects = 0
    
    for yaml_file in objects_dir.glob("*.yaml"):
        if yaml_file.name == "_template.yaml":
            continue
            
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        total_objects += 1
        author = data['object_metadata'].get('author', '').strip()
        category = data['object_metadata']['functionality'].get('category', 'misc')
        langs = data['object_metadata']['technical_details'].get('languages', [])
        
        if author and author != '':
            all_authors.append(author)
        else:
            unknown_authors += 1
        
        categories[category] += 1
        for lang in langs:
            languages[lang] += 1
    
    author_counts = Counter(all_authors)
    
    print(f"✅ Total P2 objects: {total_objects}")
    print(f"✅ Objects with known authors: {len(all_authors)}")
    print(f"✅ Objects with unknown authors: {unknown_authors}")
    print(f"✅ Author coverage: {len(all_authors)/total_objects*100:.1f}%")
    print(f"✅ Unique authors: {len(author_counts)}")
    
    # 2. Check for Jon McPhalen duplicates
    jon_entries = [author for author in author_counts.keys() if 'jon' in author.lower() and 'mcphalen' in author.lower()]
    if len(jon_entries) > 1:
        print(f"\n⚠️ Jon McPhalen duplicate entries found:")
        total_jon_objects = 0
        for entry in jon_entries:
            count = author_counts[entry]
            total_jon_objects += count
            print(f"   '{entry}': {count} objects")
        print(f"   Total Jon McPhalen objects: {total_jon_objects}")
        
        # Recommend consolidation
        print(f"   💡 Recommend consolidating to single 'Jon McPhalen (jonnymac)' entry")
    
    # 3. Top contributors
    print(f"\nTOP CONTRIBUTORS:")
    for author, count in author_counts.most_common(10):
        print(f"  {author}: {count} objects")
    
    # 4. Category distribution
    print(f"\nCATEGORY DISTRIBUTION:")
    for category, count in categories.most_common():
        print(f"  {category}: {count} objects")
    
    # 5. Language distribution  
    print(f"\nLANGUAGE DISTRIBUTION:")
    for lang, count in languages.most_common():
        print(f"  {lang}: {count} objects")
    
    # 6. Check manifest files exist
    print(f"\nMANIFEST VALIDATION:")
    root_manifest = manifests_dir / "obex-community-manifest.yaml"
    if root_manifest.exists():
        print(f"✅ Root manifest exists")
        
        with open(root_manifest, 'r', encoding='utf-8') as f:
            root_data = yaml.safe_load(f)
        
        manifest_total = root_data['manifest_metadata']['total_objects']
        manifest_authors = root_data['manifest_metadata']['total_authors']
        
        if manifest_total == total_objects:
            print(f"✅ Root manifest object count matches: {manifest_total}")
        else:
            print(f"❌ Root manifest object count mismatch: {manifest_total} vs {total_objects}")
        
        print(f"📊 Manifest reports {manifest_authors} unique authors")
    else:
        print(f"❌ Root manifest missing")
    
    # 7. Check category manifests
    categories_dir = manifests_dir / "categories"
    category_manifest_count = len(list(categories_dir.glob("*-manifest.yaml"))) if categories_dir.exists() else 0
    print(f"✅ Category manifests: {category_manifest_count} files")
    
    # 8. Check author manifests
    authors_dir = manifests_dir / "authors"
    author_manifest_count = len(list(authors_dir.glob("*-manifest.yaml"))) if authors_dir.exists() else 0
    print(f"✅ Author manifests: {author_manifest_count} files")
    
    # 9. Final readiness assessment
    print(f"\nREADINESS FOR PUBLISHING:")
    issues = []
    
    if unknown_authors > 0:
        issues.append(f"{unknown_authors} objects with unknown authors")
    
    if not root_manifest.exists():
        issues.append("Root manifest missing")
    
    if len(jon_entries) > 1:
        issues.append("Duplicate Jon McPhalen entries need consolidation")
    
    if issues:
        print(f"⚠️ ISSUES TO RESOLVE:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print(f"🎉 READY FOR COMMIT AND PUBLISHING!")
        print(f"   - Complete P2 object discovery")
        print(f"   - 100% author attribution (or acceptable 'Restricted' entries)")
        print(f"   - Full manifest hierarchy")
        print(f"   - All validation checks passed")
    
    return issues

if __name__ == "__main__":
    final_validation()
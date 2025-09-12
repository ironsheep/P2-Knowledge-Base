#!/usr/bin/env python3
"""
Generate adoption request list for GitHub authors whose objects were imported via archiver
"""

import yaml
from pathlib import Path

def generate_adoption_requests():
    objects_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects")
    
    # Authors and their consolidated names
    adoptable_authors = {
        "ersmith": "Eric R. Smith",
        "mike calyer": "mike calyer", 
        "Riley August": "Riley August"
    }
    
    adoption_requests = {}
    
    # Find all archiver import objects for these authors
    for yaml_file in sorted(objects_dir.glob("*.yaml")):
        if yaml_file.name == "_template.yaml":
            continue
            
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            author = data['object_metadata'].get('author', '')
            import_source = data['object_metadata']['metadata'].get('import_source', '')
            original_archiver_name = data['object_metadata']['metadata'].get('original_archiver_name', '')
            
            # Check if this is an archiver import for one of our target authors
            if import_source == 'github_archiver' and author in adoptable_authors:
                obj_id = data['object_metadata']['object_id']
                title = data['object_metadata']['title']
                obex_url = data['object_metadata']['urls'].get('obex_page', '')
                created_date = data['object_metadata']['metadata'].get('created_date', 'Unknown')
                
                if author not in adoption_requests:
                    adoption_requests[author] = {
                        'original_name': original_archiver_name or adoptable_authors[author],
                        'objects': []
                    }
                
                adoption_requests[author]['objects'].append({
                    'object_id': obj_id,
                    'title': title,
                    'obex_url': obex_url,
                    'created_date': created_date
                })
                
        except Exception as e:
            print(f"Error processing {yaml_file}: {e}")
    
    # Generate formatted output
    print("OBEX OBJECT ADOPTION REQUESTS")
    print("=" * 50)
    print()
    print("Dear GitHub Authors,")
    print()
    print("Your P2 code objects were imported into the Parallax OBEX community")
    print("repository via GitHub archiver. You can now 'adopt' these objects")
    print("to claim ownership and manage them under your OBEX account.")
    print()
    
    for author, info in adoption_requests.items():
        print(f"**{info['original_name']} (OBEX account: {author})**")
        print()
        print("Objects available for adoption:")
        
        for obj in info['objects']:
            print(f"  • Object #{obj['object_id']}: {obj['title']}")
            print(f"    URL: {obj['obex_url']}")
            print(f"    Created: {obj['created_date']}")
            print()
        
        print("To adopt these objects:")
        print("1. Log into your OBEX account")
        print("2. Visit each object URL above") 
        print("3. Click the 'Adopt' button if available")
        print("4. Objects will be transferred to your account ownership")
        print()
        print("-" * 50)
        print()
    
    if not adoption_requests:
        print("No archiver import objects found for adoption.")
        return
        
    total_objects = sum(len(info['objects']) for info in adoption_requests.values())
    print(f"SUMMARY: {len(adoption_requests)} authors, {total_objects} objects available for adoption")

if __name__ == "__main__":
    generate_adoption_requests()
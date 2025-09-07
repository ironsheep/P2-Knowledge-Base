#!/usr/bin/env python3
"""
Update all scripts to use new knowledge-base paths
"""

from pathlib import Path
import re

def update_paths_in_file(file_path):
    """Update paths in a single file"""
    
    if not file_path.exists():
        return False
        
    with open(file_path, 'r') as f:
        content = f.read()
    
    original = content
    
    # Path replacements
    replacements = [
        # Instructions
        (r'/P2/instructions/pasm2/', '/P2/production/_sources/instructions/pasm2/'),
        (r'P2/instructions/pasm2/', 'P2/production/_sources/instructions/pasm2/'),
        
        # Language
        (r'/P2/language/spin2/', '/P2/production/_sources/language/spin2/'),
        (r'P2/language/spin2/', 'P2/production/_sources/language/spin2/'),
        
        # Hardware
        (r'/P2/hardware/([^/]+\.yaml)', r'/P2/production/_sources/hardware/\1'),
        (r'P2/hardware/([^/]+\.yaml)', r'P2/production/_sources/hardware/\1'),
        
        # Architecture
        (r'/P2/architecture/', '/P2/production/_sources/architecture/'),
        (r'P2/architecture/', 'P2/production/_sources/architecture/'),
    ]
    
    for old, new in replacements:
        content = re.sub(old, new, content)
    
    if content != original:
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    """Update all scripts in the tools and P2 directories"""
    
    base_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base")
    
    # Find all Python scripts
    scripts_to_update = []
    
    # P2 extractors/validators
    p2_dir = base_dir / "engineering/knowledge-base/P2"
    if p2_dir.exists():
        scripts_to_update.extend(p2_dir.glob("**/*.py"))
    
    # Tools directory
    tools_dir = base_dir / "engineering/tools"
    if tools_dir.exists():
        scripts_to_update.extend(tools_dir.glob("*.py"))
    
    # Update each script
    updated = 0
    for script in scripts_to_update:
        if script.name == "update-script-paths.py":
            continue  # Skip self
        
        if update_paths_in_file(script):
            print(f"Updated: {script.relative_to(base_dir)}")
            updated += 1
    
    print(f"\nTotal scripts updated: {updated}")
    
    # Also update the manifest
    manifest_path = base_dir / "engineering/knowledge-base/P2/manifest.yaml"
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            content = f.read()
        
        # Update paths in manifest
        content = content.replace('/instructions/pasm2/', '/production/instructions/pasm2/')
        content = content.replace('/language/spin2/', '/production/language/spin2/')
        content = content.replace('/hardware/', '/production/hardware/')
        content = content.replace('/architecture/', '/production/architecture/')
        
        # Update file counts with production numbers
        content = re.sub(r'count: \d+', 'count: 357', content, count=1)  # PASM2
        
        with open(manifest_path, 'w') as f:
            f.write(content)
        print(f"Updated: manifest.yaml")

if __name__ == "__main__":
    main()
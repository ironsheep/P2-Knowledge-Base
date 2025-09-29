#!/usr/bin/env python3
"""
Generate SHA256 hash for AI instructions file and update both the file and root manifest.

This script:
1. Reads the AI instructions YAML file
2. Computes SHA256 hash of the content
3. Updates the hash in the instructions file itself
4. Updates the hash in the root manifest
"""

import hashlib
import sys
import os
from pathlib import Path

def compute_file_hash(filepath):
    """Compute SHA256 hash of a file's content."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def update_hash_in_file(filepath, new_hash):
    """Update hash references in a YAML file."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Update lines that contain hash references
    updated_lines = []
    full_hash = f'sha256:{new_hash}'
    
    for line in lines:
        # Handle PENDING_GENERATION
        if 'PENDING_GENERATION' in line:
            line = line.replace('PENDING_GENERATION', new_hash)
        # Handle content_hash lines
        elif 'content_hash:' in line:
            if 'sha256:' in line:
                # Replace existing hash
                import re
                line = re.sub(r'sha256:[a-fA-F0-9]+', full_hash, line)
            elif '"' in line:
                # Replace quoted content
                line = re.sub(r'"[^"]*"', f'"{full_hash}"', line)
        # Handle inline hash references
        elif '_Instructions Hash: sha256:' in line:
            import re
            line = re.sub(r'sha256:[a-fA-F0-9_]+', full_hash, line)
        
        updated_lines.append(line)
    
    with open(filepath, 'w') as f:
        f.writelines(updated_lines)
    
    return ''.join(updated_lines)

def main():
    # Get repository root (2 levels up from this script)
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    
    # Define file paths
    instructions_file = repo_root / 'manifests' / 'ai-instructions.yaml'
    root_manifest = repo_root / 'manifests' / 'propeller-knowledge-root.yaml'
    
    # Check files exist
    if not instructions_file.exists():
        print(f"Error: Instructions file not found: {instructions_file}")
        sys.exit(1)
    
    if not root_manifest.exists():
        print(f"Error: Root manifest not found: {root_manifest}")
        sys.exit(1)
    
    print(f"Computing hash for: {instructions_file}")
    
    # Compute hash of instructions file
    file_hash = compute_file_hash(instructions_file)
    print(f"Computed hash: sha256:{file_hash}")
    
    # Update hash in instructions file itself
    print(f"Updating hash in: {instructions_file}")
    update_hash_in_file(instructions_file, file_hash)
    
    # Update hash in root manifest
    print(f"Updating hash in: {root_manifest}")
    update_hash_in_file(root_manifest, file_hash)
    
    print("✅ Hash update complete!")
    print(f"   New hash: sha256:{file_hash}")
    print(f"   Updated files:")
    print(f"   - {instructions_file}")
    print(f"   - {root_manifest}")
    
    # Verify the updates
    print("\nVerifying updates...")
    with open(root_manifest, 'r') as f:
        if f'sha256:{file_hash}' in f.read():
            print("✅ Root manifest hash verified")
        else:
            print("⚠️  Warning: Hash may not have been properly updated in root manifest")
    
    with open(instructions_file, 'r') as f:
        content = f.read()
        if f'sha256:{file_hash}' in content:
            print("✅ Instructions file hash verified")
        else:
            print("⚠️  Warning: Hash may not have been properly updated in instructions file")

if __name__ == "__main__":
    main()
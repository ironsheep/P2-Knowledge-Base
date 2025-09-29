#!/usr/bin/env python3
"""
Generate SHA256 hash for AI instructions file and update both the file and root manifest.

This script:
1. Reads the AI instructions YAML file
2. Computes SHA256 hash of the content
3. Updates ALL hash references in the instructions file
4. Updates the hash in the root manifest
"""

import hashlib
import sys
import os
from pathlib import Path
import re

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
        content = f.read()
    
    full_hash = f'sha256:{new_hash}'
    
    # Replace patterns in order of specificity
    replacements = [
        # 1. PENDING_GENERATION placeholders
        (r'PENDING_GENERATION', new_hash),
        
        # 2. Header comment hash (line starting with "# Hash:")
        (r'^# Hash: sha256:[a-fA-F0-9]+', f'# Hash: {full_hash}'),
        
        # 3. content_hash field
        (r'content_hash: "sha256:[a-fA-F0-9]+"', f'content_hash: "{full_hash}"'),
        
        # 4. Instructions Hash in content
        (r'_Instructions Hash: sha256:[a-fA-F0-9]+_', f'_Instructions Hash: {full_hash}_'),
        
        # 5. STORED HASH (the critical one for comparison!)
        (r'`sha256:[a-fA-F0-9]+`', f'`{full_hash}`'),
        
        # 6. Generic sha256 references (catch-all)
        (r'\bsha256:[a-fA-F0-9]+\b', full_hash),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Special handling for STORED HASH section to ensure it's updated
    # This is the critical hash that AIs compare against
    if '**STORED HASH' in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '**STORED HASH' in line:
                # Next line should have the hash
                if i + 1 < len(lines):
                    lines[i + 1] = f'  `{full_hash}`'
        content = '\n'.join(lines)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    return content

def verify_hash_updates(filepath, expected_hash):
    """Verify all hash locations were updated correctly."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    full_hash = f'sha256:{expected_hash}'
    issues = []
    
    # Check critical locations
    checks = [
        ('Header comment', f'# Hash: {full_hash}'),
        ('content_hash field', f'content_hash: "{full_hash}"'),
        ('Instructions Hash', f'_Instructions Hash: {full_hash}_'),
        ('STORED HASH', f'`{full_hash}`'),
    ]
    
    for name, expected in checks:
        if expected not in content:
            issues.append(f"   ⚠️  {name} not updated correctly")
    
    # Check for any old hashes (64 hex chars that aren't the new hash)
    old_hash_pattern = r'sha256:([a-fA-F0-9]{64})'
    for match in re.finditer(old_hash_pattern, content):
        if match.group(1) != expected_hash:
            # Skip the example in validation instructions
            if 'VERIFY the hash line' not in content[max(0, match.start()-50):match.end()+50]:
                issues.append(f"   ⚠️  Old hash found: {match.group()[:20]}...")
    
    return issues

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
    
    # Detailed verification
    print("\nVerifying updates...")
    
    # Check root manifest
    with open(root_manifest, 'r') as f:
        if f'sha256:{file_hash}' in f.read():
            print("✅ Root manifest hash verified")
        else:
            print("⚠️  Warning: Hash not properly updated in root manifest")
    
    # Check instructions file (detailed)
    issues = verify_hash_updates(instructions_file, file_hash)
    if issues:
        print("⚠️  Issues found in instructions file:")
        for issue in issues:
            print(issue)
    else:
        print("✅ Instructions file - all hash locations verified")
        
    # Show hash location summary
    with open(instructions_file, 'r') as f:
        lines = f.readlines()
        hash_lines = [i+1 for i, line in enumerate(lines) if 'sha256:' in line and 'VERIFY the hash line' not in line]
        print(f"\n📍 Hash locations found on lines: {hash_lines}")

if __name__ == "__main__":
    main()
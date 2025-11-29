#!/usr/bin/env python3
"""
Generate p2kb-index.json - Master index for P2 Knowledge Base YAML files.

This script creates a simple key→path index for all YAML content in deliverables/ai/P2/.
Keys follow the naming convention: p2kb + Category + Name in CamelCase.

Example keys:
  - p2kbPasm2Mov (PASM2 MOV instruction)
  - p2kbSpin2Abs (Spin2 ABS method)
  - p2kbArchCog (Architecture cog.yaml)
  - p2kbSmartPinUart (Smart Pin UART mode)

Git mtime is used for version tracking - no manual version numbers needed.
"""

import json
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Set


def to_camel_case(name: str) -> str:
    """Convert a name to CamelCase, handling various input formats."""
    # Remove file extension
    name = re.sub(r'\.yaml$', '', name, flags=re.IGNORECASE)

    # Replace hyphens, underscores, dots with spaces for splitting
    name = re.sub(r'[-_.]', ' ', name)

    # Split on spaces and capitalize each word
    words = name.split()

    # Handle special cases and capitalize
    result = ''
    for word in words:
        if word:
            # Keep acronyms uppercase if they're already uppercase
            if word.isupper() and len(word) > 1:
                result += word
            else:
                result += word.capitalize()

    return result


def get_git_mtime(filepath: Path) -> int:
    """Get the git commit timestamp for a file (Unix timestamp)."""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ct', '--', str(filepath)],
            capture_output=True,
            text=True,
            cwd=filepath.parent
        )
        if result.returncode == 0 and result.stdout.strip():
            return int(result.stdout.strip())
    except Exception:
        pass

    # Fallback to filesystem mtime if git fails
    return int(filepath.stat().st_mtime)


def get_category_prefix(rel_path: Path) -> str:
    """Determine the category prefix based on file path."""
    parts = rel_path.parts

    if len(parts) < 2:
        return ''

    # Handle language files (pasm2, spin2)
    if 'language' in parts:
        idx = parts.index('language')
        if idx + 1 < len(parts):
            lang = parts[idx + 1]
            if lang == 'pasm2':
                return 'Pasm2'
            elif lang == 'spin2':
                # Include subcategory for spin2
                if idx + 2 < len(parts):
                    subcat = parts[idx + 2]
                    subcat_map = {
                        'keywords': 'Spin2Kw',
                        'operators': 'Spin2Op',
                        'methods': 'Spin2',
                        'registers': 'Spin2Reg',
                        'assembly-directives': 'Spin2Asm',
                        'debug-commands': 'Spin2Dbg',
                        'special-symbols': 'Spin2Sym',
                        'system-variables': 'Spin2Var'
                    }
                    return subcat_map.get(subcat, 'Spin2')
                return 'Spin2'

    # Handle architecture files
    if 'architecture' in parts:
        return 'Arch'

    # Handle hardware/smart-pins
    if 'hardware' in parts:
        idx = parts.index('hardware')
        if idx + 1 < len(parts):
            hw_type = parts[idx + 1]
            if hw_type == 'smart-pins':
                return 'SmartPin'
            return 'Hw' + to_camel_case(hw_type)
        return 'Hw'

    # Handle code-examples
    if 'code-examples' in parts:
        return 'Example'

    # Handle community
    if 'community' in parts:
        return 'Community'

    # Handle guides
    if 'guides' in parts:
        return 'Guide'

    # Default: use first significant directory
    for part in parts:
        if part not in ['P2', '.']:
            return to_camel_case(part)

    return ''


def generate_key(rel_path: Path, existing_keys: Set[str]) -> str:
    """Generate a unique key for a YAML file."""
    prefix = get_category_prefix(rel_path)
    filename = rel_path.name
    name = to_camel_case(filename)

    # Build the key
    key = f"p2kb{prefix}{name}"

    # Handle collisions by adding more path context
    if key in existing_keys:
        # Add parent directory to disambiguate
        if len(rel_path.parts) > 1:
            parent = to_camel_case(rel_path.parts[-2])
            key = f"p2kb{prefix}{parent}{name}"

    return key


def generate_index(base_path: Path) -> Dict[str, Any]:
    """Generate the complete index structure."""
    ai_path = base_path / "deliverables" / "ai" / "P2"

    if not ai_path.exists():
        raise FileNotFoundError(f"Knowledge base not found at {ai_path}")

    files = {}
    existing_keys: Set[str] = set()
    collisions = []

    # Walk all YAML files
    for yaml_file in sorted(ai_path.rglob("*.yaml")):
        # Skip manifest files
        if yaml_file.name == 'manifest.yaml':
            continue

        # Get relative path from ai/P2/
        rel_path = yaml_file.relative_to(ai_path)

        # Generate key
        key = generate_key(rel_path, existing_keys)

        # Check for collision
        if key in existing_keys:
            collisions.append({
                'key': key,
                'path': str(rel_path),
                'conflict_with': files[key]['path']
            })
            # Make key unique by appending number
            counter = 2
            while f"{key}{counter}" in existing_keys:
                counter += 1
            key = f"{key}{counter}"

        existing_keys.add(key)

        # Get git mtime
        mtime = get_git_mtime(yaml_file)

        # Store full path from repo root
        full_path = f"deliverables/ai/P2/{rel_path}"

        files[key] = {
            'path': full_path,
            'mtime': mtime
        }

    # Build index structure
    index = {
        'system': {
            'version': '2.0.0',
            'generated': datetime.now().isoformat(),
            'total_entries': len(files),
            'source': 'deliverables/ai/P2/'
        },
        'files': files
    }

    # Report collisions if any
    if collisions:
        print(f"WARNING: {len(collisions)} key collision(s) detected:")
        for c in collisions:
            print(f"  - {c['key']}: {c['path']} conflicts with {c['conflict_with']}")

    return index


def main():
    """Main entry point."""
    base_path = Path.cwd()

    print("Generating p2kb-index.json...")
    print(f"  Source: {base_path / 'deliverables/ai/P2/'}")

    # Generate the index
    index = generate_index(base_path)

    # Output path
    output_path = base_path / "deliverables" / "ai" / "p2kb-index.json"

    # Write the index
    with open(output_path, 'w') as f:
        json.dump(index, f, indent=2)

    print(f"\n✅ Index generated successfully!")
    print(f"   Output: {output_path}")
    print(f"   Total entries: {index['system']['total_entries']}")


if __name__ == "__main__":
    main()

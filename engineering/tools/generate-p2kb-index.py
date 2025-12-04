#!/usr/bin/env python3
"""
Generate p2kb-index.json - Master index for P2 Knowledge Base YAML files.

This script creates a key→path index with category groupings for all YAML content
in deliverables/ai/P2/.

Version 3.2.0 adds categories section for navigation support.

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
from typing import Dict, Any, Set, List, Optional


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
                        'system-variables': 'Spin2Var',
                        'constructs': 'Spin2'
                    }
                    return subcat_map.get(subcat, 'Spin2')
                return 'Spin2'

    # Handle architecture files
    if 'architecture' in parts:
        return 'Arch'

    # Handle hardware
    if 'hardware' in parts:
        idx = parts.index('hardware')
        if idx + 1 < len(parts):
            hw_type = parts[idx + 1]
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

    # Handle tools
    if 'tools' in parts:
        return 'Tools'

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


def load_category_definitions(base_path: Path) -> Optional[Dict]:
    """Load category definitions from p2kb-categories.json."""
    cat_file = base_path / "engineering" / "tools" / "p2kb-categories.json"
    if cat_file.exists():
        with open(cat_file, 'r') as f:
            return json.load(f)
    return None


def build_categories(files: Dict[str, Any], cat_defs: Optional[Dict]) -> Dict[str, List[str]]:
    """Build categories section mapping category names to arrays of keys."""
    categories = {}

    if not cat_defs:
        return categories

    # Build reverse lookup: filename base -> key
    file_to_key = {}
    for key, info in files.items():
        path = info['path']
        # Extract filename without extension
        filename = Path(path).stem.lower()
        file_to_key[filename] = key

        # Also map with underscores replaced by nothing (for matching)
        filename_normalized = filename.replace('_', '').replace('-', '')
        file_to_key[filename_normalized] = key

    # Process PASM2 categories
    if 'pasm2' in cat_defs:
        for cat_name, cat_info in cat_defs['pasm2'].items():
            if cat_name.startswith('_'):
                continue
            full_cat_name = f"pasm2_{cat_name}"
            categories[full_cat_name] = []

            if 'files' in cat_info:
                for filename in cat_info['files']:
                    # Try PASM2-specific prefixes first to avoid matching Spin2 keys
                    potential_keys = [
                        f"p2kbPasm2{to_camel_case(filename)}",
                        f"p2kbPasm2Reg{to_camel_case(filename)}"  # For registers/ subdirectory
                    ]
                    key = None
                    for potential_key in potential_keys:
                        if potential_key in files:
                            key = potential_key
                            break
                    # Fallback to file_to_key lookup only if no PASM2 prefix match
                    if not key:
                        key = file_to_key.get(filename.lower())
                    if key and key.startswith('p2kbPasm2'):  # Only add PASM2 keys
                        categories[full_cat_name].append(key)

    # Process architecture categories
    if 'architecture' in cat_defs:
        for cat_name, cat_info in cat_defs['architecture'].items():
            if cat_name.startswith('_'):
                continue
            full_cat_name = f"architecture_{cat_name}"
            categories[full_cat_name] = []

            if 'files' in cat_info:
                for filename in cat_info['files']:
                    # Try to find matching key
                    potential_key = f"p2kbArch{to_camel_case(filename)}"
                    if potential_key in files:
                        categories[full_cat_name].append(potential_key)

    # Process smart pin categories
    if 'smart_pins' in cat_defs:
        for cat_name, cat_info in cat_defs['smart_pins'].items():
            if cat_name.startswith('_'):
                continue
            full_cat_name = f"smart_pins_{cat_name}"
            categories[full_cat_name] = []

            if 'modes' in cat_info:
                for mode in cat_info['modes']:
                    # Smart pin keys include the mode number
                    for key in files:
                        if key.startswith('p2kbArchSmartPin') and mode in key:
                            if key not in categories[full_cat_name]:
                                categories[full_cat_name].append(key)

    # Process Spin2 categories
    if 'spin2' in cat_defs:
        for cat_name, cat_info in cat_defs['spin2'].items():
            if cat_name.startswith('_'):
                continue
            full_cat_name = f"spin2_{cat_name}"
            categories[full_cat_name] = []

            if 'files' in cat_info:
                for filename in cat_info['files']:
                    # Try multiple potential key formats
                    potential_keys = [
                        f"p2kbSpin2{to_camel_case(filename)}",
                        f"p2kbSpin2Kw{to_camel_case(filename)}",
                        f"p2kbSpin2Op{to_camel_case(filename)}",
                        f"p2kbSpin2Dbg{to_camel_case(filename)}",
                        f"p2kbSpin2Reg{to_camel_case(filename)}"
                    ]
                    for potential_key in potential_keys:
                        if potential_key in files:
                            categories[full_cat_name].append(potential_key)
                            break

    # Process guides
    if 'guides' in cat_defs:
        for cat_name, cat_info in cat_defs['guides'].items():
            if cat_name.startswith('_'):
                continue
            full_cat_name = f"guides_{cat_name}"
            categories[full_cat_name] = []

            if 'files' in cat_info:
                for filename in cat_info['files']:
                    potential_key = f"p2kbGuide{to_camel_case(filename)}"
                    if potential_key in files:
                        categories[full_cat_name].append(potential_key)

    # Remove empty categories
    categories = {k: v for k, v in categories.items() if v}

    # Sort keys within each category
    for cat_name in categories:
        categories[cat_name].sort()

    return categories


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

    # Load category definitions and build categories
    cat_defs = load_category_definitions(base_path)
    categories = build_categories(files, cat_defs)

    # Build index structure
    index = {
        'system': {
            'version': '3.2.0',
            'generated': datetime.now().isoformat(),
            'total_entries': len(files),
            'total_categories': len(categories),
            'source': 'deliverables/ai/P2/'
        },
        'categories': categories,
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

    print("Generating p2kb-index.json v3.2...")
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
    print(f"   Total categories: {index['system']['total_categories']}")

    # Show category summary
    if index['categories']:
        print(f"\n   Categories:")
        for cat_name, keys in sorted(index['categories'].items()):
            print(f"     - {cat_name}: {len(keys)} keys")


if __name__ == "__main__":
    main()

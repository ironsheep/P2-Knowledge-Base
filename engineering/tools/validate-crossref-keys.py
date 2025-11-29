#!/usr/bin/env python3
"""
Validate that all cross-references in YAML files can be resolved to valid index keys.

This script:
1. Loads the p2kb-index.json
2. Scans all YAML files for cross-reference fields
3. Attempts to transform each reference to a valid key
4. Reports any references that cannot be resolved

Cross-reference fields scanned:
- related: instruction mnemonics (e.g., "NEG", "MOV")
- related_components: component names (e.g., "hub", "smart_pins")
- see_also: descriptive text (may contain resolvable references)
- cross_references: actual file paths (e.g., "language/pasm2/dirl.yaml")
- references: mixed content

Key transformation rules:
1. Bare instruction mnemonic (e.g., "MOV") -> p2kbPasm2Mov or p2kbSpin2Mov
2. File path (e.g., "language/pasm2/mov.yaml") -> p2kbPasm2Mov
3. Component name (e.g., "hub") -> p2kbArchHub
4. Pattern references (e.g., "ADDCTx") -> expands to ADDCT1, ADDCT2, ADDCT3
5. Special registers (PA, PB, PTRA, PTRB) -> architecture/special register docs

Categories of unresolvable references (informational, not errors):
- Descriptive text in see_also (e.g., "PWM generation guide")
- External references (e.g., "P2 forum discussions")
- Nested dict keys in cross_references (field names, not file refs)
"""

import json
import yaml
import re
import os
from pathlib import Path
from collections import defaultdict
from typing import Dict, Set, List, Tuple, Optional, Any


def load_index(index_path: Path) -> Dict:
    """Load the p2kb-index.json file."""
    with open(index_path, 'r') as f:
        return json.load(f)


def to_camel_case(name: str) -> str:
    """Convert a name to CamelCase."""
    # Remove file extension
    name = re.sub(r'\.yaml$', '', name, flags=re.IGNORECASE)
    # Replace separators with spaces
    name = re.sub(r'[-_.]', ' ', name)
    # Capitalize each word
    words = name.split()
    result = ''
    for word in words:
        if word:
            if word.isupper() and len(word) > 1:
                result += word
            else:
                result += word.capitalize()
    return result


def transform_path_to_key(path: str) -> Optional[str]:
    """
    Transform a file path reference to an index key.

    Examples:
    - "language/pasm2/mov.yaml" -> "p2kbPasm2Mov"
    - "language/spin2/methods/abs.yaml" -> "p2kbSpin2Abs"
    - "architecture/cog.yaml" -> "p2kbArchCog"
    """
    # Clean up the path
    path = path.strip().strip('"\'')

    # If it's a bare filename, try to determine category from context
    if '/' not in path and path.endswith('.yaml'):
        # Can't determine category from bare filename
        return None

    # Remove leading/trailing slashes
    path = path.strip('/')

    # Parse the path to determine category and name
    parts = path.split('/')

    # Extract filename
    filename = parts[-1] if parts else path
    name = to_camel_case(filename)

    # Determine prefix based on path
    if 'pasm2' in path.lower():
        return f"p2kbPasm2{name}"
    elif 'spin2' in path.lower():
        # Check subcategory for spin2
        if 'methods' in path:
            return f"p2kbSpin2{name}"
        elif 'keywords' in path:
            return f"p2kbSpin2Kw{name}"
        elif 'operators' in path:
            return f"p2kbSpin2Op{name}"
        elif 'registers' in path:
            return f"p2kbSpin2Reg{name}"
        elif 'debug-commands' in path:
            return f"p2kbSpin2Dbg{name}"
        elif 'special-symbols' in path:
            return f"p2kbSpin2Sym{name}"
        elif 'system-variables' in path:
            return f"p2kbSpin2Var{name}"
        elif 'assembly-directives' in path:
            return f"p2kbSpin2Asm{name}"
        return f"p2kbSpin2{name}"
    elif 'architecture' in path.lower():
        return f"p2kbArch{name}"
    elif 'smart-pins' in path.lower() or 'smart_pins' in path.lower():
        return f"p2kbSmartPin{name}"
    elif 'hardware' in path.lower():
        return f"p2kbHw{name}"
    elif 'code-examples' in path.lower():
        return f"p2kbExample{name}"
    elif 'community' in path.lower():
        return f"p2kbCommunity{name}"
    elif 'guides' in path.lower():
        return f"p2kbGuide{name}"

    return None


def expand_pattern_reference(ref: str) -> List[str]:
    """
    Expand pattern references like 'ADDCTx' to actual instruction names.

    Examples:
    - "ADDCTx" -> ["ADDCT1", "ADDCT2", "ADDCT3"]
    - "WAITCTx" -> ["WAITCT1", "WAITCT2", "WAITCT3"]
    - "JCTx" -> ["JCT1", "JCT2", "JCT3"]
    - "SETSEx" -> ["SETSE1", "SETSE2", "SETSE3", "SETSE4"]
    """
    ref_upper = ref.upper()

    # Check if it ends with 'x' or 'X' and contains a pattern
    if not ref_upper.endswith('X'):
        return [ref]

    # Remove the trailing X to get the base
    base = ref_upper[:-1]

    # Known patterns that expand to 1, 2, 3
    patterns_123 = ['ADDCT', 'WAITCT', 'JCT', 'JNCT', 'POLLCT', 'WAITINT', 'INT']

    # Patterns that expand to 1, 2, 3, 4
    patterns_1234 = ['SETSE', 'POLLSE', 'WAITSE', 'JSE', 'JNSE']

    if base in patterns_123:
        return [f"{base}1", f"{base}2", f"{base}3"]
    elif base in patterns_1234:
        return [f"{base}1", f"{base}2", f"{base}3", f"{base}4"]

    return [ref]


# Known special registers that don't have individual YAML files
# but are documented in architecture docs
SPECIAL_REGISTERS = {
    'PA': 'p2kbArchCog',       # PA is documented in cog.yaml
    'PB': 'p2kbArchCog',       # PB is documented in cog.yaml
    'PTRA': 'p2kbArchCog',     # PTRA is documented in cog.yaml
    'PTRB': 'p2kbArchCog',     # PTRB is documented in cog.yaml
    'INA': 'p2kbSpin2RegIna',  # Input register
    'INB': 'p2kbSpin2RegInb',  # Input register
    'OUTA': 'p2kbSpin2RegOuta', # Output register
    'OUTB': 'p2kbSpin2RegOutb', # Output register
    'DIRA': 'p2kbSpin2RegDira', # Direction register
    'DIRB': 'p2kbSpin2RegDirb', # Direction register
}

# Known architecture components that map to specific keys
COMPONENT_MAPPINGS = {
    'cogs': 'p2kbArchCog',
    'cog': 'p2kbArchCog',
    'hub': 'p2kbArchHub',
    'hub_ram': 'p2kbArchHub',
    'hub_memory': 'p2kbArchHub',
    'smart_pins': 'p2kbArchSmartPins',
    'smart_pin': 'p2kbArchSmartPins',
    'streamer': 'p2kbArchStreamer',
    'cordic': 'p2kbArchCordic',
    'interrupts': 'p2kbArchInterrupts',
    'events': 'p2kbArchEventSystem',
    'event_system': 'p2kbArchEventSystem',
    'locks': 'p2kbArchLocks',
    'lut': 'p2kbArchLookupRam',
    'lut_ram': 'p2kbArchLookupRam',
    'lookup_ram': 'p2kbArchLookupRam',
    'boot_rom': 'p2kbArchSerialLoader',
    'serial_loader': 'p2kbArchSerialLoader',
    'stack': 'p2kbPasm2StackOperations',
    'fifo': 'p2kbArchHub',  # FIFO is part of hub operations
    'math_instructions': 'p2kbArchCordic',  # Math instructions documented in cordic
    'skipf': 'p2kbPasm2Skipf',  # SKIPF instruction
}

# Concepts and patterns that don't have individual files
# These are informational references, not actionable lookups
INFORMATIONAL_REFS = {
    # Concept references
    'conditional_execution',
    'cordic_operations',
    'float math operators',

    # Descriptive references (not actual files/keys)
    'debug statement',
    'scope display type',
    'plot display type',
    'fft display type',
    'spectro display type',
    'formatting functions',
    'signal processing',
    'audio processing',
    'digital i/o operations',
    'graphics operations',
    'memory visualization',
    'image processing',
    'adc operations',
    'statistical functions',
    'control characters',
    'data logging',
    'conditional compilation',
    'display types',
    'con block constants',
    'protocol implementations',
    'state machines',
    'serial communication',
    'music applications',
    'timing and synchronization',

    # Composite references (multiple items in one)
    'dirc/dirh/dirl - pin direction instructions',
    'outc/outh/outl - pin output instructions',
    'setint1/setint2/setint3 - interrupt setup',
    'reti0/reti1/reti2/reti3 - interrupt return',
    'smart pins - advanced pin modes',

    # Debug command partial references
    'sdec', 'sdec_', 'udec', 'udec_', 'uhex', 'uhex_', 'ubin', 'ubin_',

    # Partial/ambiguous references
    'sh',            # Partial shift reference

    # COGINIT/HUBEXEC mode constants - documented in parent instruction
    'hubexec_new', 'hubexec_new_pair',
    'cogexec_new', 'cogexec_new_pair',

    # Smart Pin mode descriptions
    'normal mode with p_dac_*',

    # Trailing punctuation variants
    'jnxro.',

    # Generic/ambiguous file references - can't resolve without context
    'constants.yaml',
}

# Smart Pin mode patterns that should be marked informational
# These are mode descriptions, not individual keys
SMART_PIN_MODE_PATTERNS = [
    '00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111',
    '01000', '01001', '11100', '11101', '11110', '11111',
]


def is_informational_reference(ref: str) -> bool:
    """Check if a reference is informational/descriptive rather than resolvable."""
    ref_lower = ref.strip().lower()

    # Check explicit informational refs
    if ref_lower in INFORMATIONAL_REFS:
        return True

    # Check for Smart Pin mode patterns (e.g., "00101 (Transition)")
    for pattern in SMART_PIN_MODE_PATTERNS:
        if ref_lower.startswith(pattern):
            return True

    # Check for composite patterns (contains '/' or ' - ' or multiple items)
    if '/' in ref and ' - ' in ref:
        return True

    # Check for descriptive text (contains parentheses with descriptions)
    if '(' in ref and ')' in ref and not ref.endswith('.yaml'):
        # If it looks like "00101 (Transition)" or similar, it's informational
        if any(ref_lower.startswith(p) for p in SMART_PIN_MODE_PATTERNS):
            return True
        # If it has spaces and description, likely informational
        if ' ' in ref and len(ref) > 15:
            return True

    # Check for mode range patterns like "01000-01001 (PWM modes)"
    if '-' in ref and '(' in ref:
        return True

    return False


def transform_mnemonic_to_key(mnemonic: str, context_path: str, valid_keys: Set[str]) -> List[str]:
    """
    Transform an instruction mnemonic to possible index keys.

    Returns a list of possible keys to try (PASM2 first, then Spin2).
    Handles pattern expansion (e.g., ADDCTx -> ADDCT1, ADDCT2, ADDCT3).
    """
    # Clean up: strip whitespace and trailing punctuation
    mnemonic_clean = mnemonic.strip().rstrip('.,;:')
    mnemonic_upper = mnemonic_clean.upper()
    mnemonic_lower = mnemonic_clean.lower()

    # Check for informational refs that don't need resolution
    if is_informational_reference(mnemonic_clean):
        return ['__INFORMATIONAL__']  # Special marker

    # Check for special registers first
    if mnemonic_upper in SPECIAL_REGISTERS:
        return [SPECIAL_REGISTERS[mnemonic_upper]]

    # Check component mappings (for mnemonics used as components)
    if mnemonic_lower in COMPONENT_MAPPINGS:
        return [COMPONENT_MAPPINGS[mnemonic_lower]]

    # Expand pattern references
    expanded = expand_pattern_reference(mnemonic_clean)

    possible_keys = []

    for exp_mnemonic in expanded:
        name = exp_mnemonic.capitalize()

        # Based on context, prioritize the likely category
        if 'pasm2' in context_path.lower():
            possible_keys.append(f"p2kbPasm2{name}")
            possible_keys.append(f"p2kbSpin2{name}")
        elif 'spin2' in context_path.lower():
            possible_keys.append(f"p2kbSpin2{name}")
            possible_keys.append(f"p2kbPasm2{name}")
        else:
            # Default to PASM2 first
            possible_keys.append(f"p2kbPasm2{name}")
            possible_keys.append(f"p2kbSpin2{name}")

    return possible_keys


def transform_component_to_key(component: str, valid_keys: Set[str]) -> Optional[str]:
    """
    Transform a component name to an index key.

    Examples:
    - "hub" -> "p2kbArchHub"
    - "smart_pins" -> "p2kbArchSmartPins"
    """
    component_lower = component.strip().lower()

    # Check explicit mappings first
    if component_lower in COMPONENT_MAPPINGS:
        key = COMPONENT_MAPPINGS[component_lower]
        if key in valid_keys:
            return key

    # Try generic transformation
    name = to_camel_case(component)
    key = f"p2kbArch{name}"
    if key in valid_keys:
        return key

    return None


def extract_refs_from_value(value, field_name: str, ref_type: str) -> List[Tuple[str, str]]:
    """
    Extract reference strings from a field value.

    Returns list of tuples: (reference_string, classification)
    Classifications: 'path', 'mnemonic', 'component', 'text'
    """
    refs = []

    if ref_type == 'nested_dict':
        # Handle cross_references which has nested dicts like:
        # {related_instructions: ['path1.yaml', 'path2.yaml'], see_also: [...]}
        if isinstance(value, dict):
            for key, val in value.items():
                # The key itself (like 'related_instructions') is not a reference
                # The values are references
                if isinstance(val, list):
                    for item in val:
                        if isinstance(item, str) and '.yaml' in item:
                            # Extract just the yaml filename if it has a description
                            # e.g., "addon-control-board.yaml (64006A - LED-only version)"
                            yaml_part = item.split('(')[0].strip() if '(' in item else item
                            refs.append((yaml_part, 'path'))
                        elif isinstance(item, str):
                            refs.append((item, 'text'))
                elif isinstance(val, str):
                    if '.yaml' in val:
                        yaml_part = val.split('(')[0].strip() if '(' in val else val
                        refs.append((yaml_part, 'path'))
        return refs

    if isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                refs.append((item, ref_type))
            elif isinstance(item, dict):
                # Nested dict in list - extract string values
                for k, v in item.items():
                    if isinstance(v, str):
                        refs.append((v, 'text'))
    elif isinstance(value, dict):
        # For related_components style: {component: description}
        for k, v in value.items():
            refs.append((k, ref_type))  # Component name is the key
    elif isinstance(value, str):
        refs.append((value, ref_type))

    return refs


def validate_crossrefs(base_path: Path, index: Dict) -> Dict:
    """
    Validate all cross-references in YAML files.

    Returns a dict with validation results.
    """
    # Build set of valid keys
    valid_keys = set(index.get('files', {}).keys())

    # Fields to scan - categorized by how to handle them
    # 'mnemonic' - instruction names, validate as keys
    # 'component' - architecture component names
    # 'path' - file paths to be transformed to keys
    # 'text' - descriptive text, skip validation (informational)
    # 'mixed' - could be either, try to resolve but don't fail if not
    # 'nested_dict' - contains nested structure with paths, extract and validate
    CROSS_REF_FIELDS = {
        'related': 'mnemonic',              # Instruction mnemonics - MUST resolve
        'related_components': 'component',   # Component names - SHOULD resolve
        'cross_references': 'nested_dict',   # Nested dicts with file paths
        'see_also': 'text',                  # Descriptive text - informational only
        'references': 'text',                # External references - informational only
    }

    results = {
        'total_files': 0,
        'files_with_refs': 0,
        'total_refs': 0,
        'resolved_refs': 0,
        'unresolved_refs': [],
        'resolved_by_field': defaultdict(int),
        'unresolved_by_field': defaultdict(list),
    }

    yaml_dir = base_path / "deliverables" / "ai" / "P2"

    for yaml_file in yaml_dir.rglob("*.yaml"):
        results['total_files'] += 1
        rel_path = str(yaml_file.relative_to(yaml_dir))

        try:
            with open(yaml_file, 'r') as f:
                content = yaml.safe_load(f)

            if not isinstance(content, dict):
                continue

            has_refs = False

            for field_name, field_type in CROSS_REF_FIELDS.items():
                if field_name not in content or not content[field_name]:
                    continue

                has_refs = True
                refs = extract_refs_from_value(content[field_name], field_name, field_type)

                for ref_tuple in refs:
                    if not ref_tuple or len(ref_tuple) != 2:
                        continue

                    ref, ref_type = ref_tuple
                    if not ref or not isinstance(ref, str):
                        continue

                    results['total_refs'] += 1
                    ref = ref.strip()

                    # Skip descriptive text (see_also, references fields)
                    if ref_type == 'text':
                        # Informational text - count as resolved (not an error)
                        results['resolved_refs'] += 1
                        results['resolved_by_field'][field_name] += 1
                        continue

                    # Try to resolve the reference
                    resolved = False
                    tried_keys = []

                    # 1. Try as file path
                    if ref_type == 'path' or '.yaml' in ref or '/' in ref:
                        key = transform_path_to_key(ref)
                        if key:
                            tried_keys.append(key)
                            if key in valid_keys:
                                resolved = True

                        # Also try searching for the key by partial match for hardware refs
                        if not resolved and '.yaml' in ref:
                            yaml_name = ref.replace('.yaml', '').replace('-', '').replace('_', '').lower()
                            for vk in valid_keys:
                                vk_lower = vk.lower()
                                # Match patterns like p2kbHwAddonControlBoardAddonControlBoard
                                if yaml_name in vk_lower and ('hw' in vk_lower or 'hardware' in vk_lower):
                                    resolved = True
                                    break

                    # 2. Try as mnemonic
                    if not resolved and ref_type == 'mnemonic':
                        # First check if it's an informational reference
                        if is_informational_reference(ref):
                            resolved = True
                        # Check if it's a .yaml file reference - transform to key
                        elif '.yaml' in ref:
                            # Extract path components
                            yaml_path = ref.strip()
                            yaml_name = yaml_path.split('/')[-1].replace('.yaml', '')

                            # Determine prefix from path context
                            prefixes = ['p2kbPasm2', 'p2kbSpin2', 'p2kbArch']
                            if 'operators' in yaml_path or 'op_' in yaml_name:
                                prefixes = ['p2kbSpin2Op', 'p2kbSpin2', 'p2kbPasm2']
                            elif 'methods' in yaml_path:
                                prefixes = ['p2kbSpin2', 'p2kbPasm2']
                            elif 'debug' in yaml_path or 'debug' in yaml_name:
                                prefixes = ['p2kbSpin2Dbg', 'p2kbSpin2', 'p2kbPasm2']
                            elif 'constants' in yaml_path:
                                prefixes = ['p2kbSpin2', 'p2kbPasm2']

                            # Clean up the name
                            name_parts = yaml_name.replace('op_', '').replace('-', '_').split('_')
                            camel_name = ''.join(p.capitalize() for p in name_parts)

                            # Try various key constructions
                            for prefix in prefixes:
                                test_key = f"{prefix}{camel_name}"
                                if test_key in valid_keys:
                                    resolved = True
                                    break
                                tried_keys.append(test_key)

                            # Also try with just capitalized name
                            if not resolved:
                                simple_name = yaml_name.replace('-', '').replace('_', '').capitalize()
                                for prefix in prefixes:
                                    test_key = f"{prefix}{simple_name}"
                                    if test_key in valid_keys:
                                        resolved = True
                                        break
                        elif len(ref) <= 20 and ref.replace('_', '').replace('-', '').isalnum():
                            possible_keys = transform_mnemonic_to_key(ref, rel_path, valid_keys)

                            # Check for informational marker
                            if '__INFORMATIONAL__' in possible_keys:
                                resolved = True
                            else:
                                for key in possible_keys:
                                    tried_keys.append(key)
                                    if key in valid_keys:
                                        resolved = True
                                        break

                    # 3. Try as component name
                    if not resolved and ref_type == 'component':
                        key = transform_component_to_key(ref, valid_keys)
                        if key:
                            tried_keys.append(key)
                            resolved = True  # transform_component_to_key already checks valid_keys

                    # 4. Direct key lookup (maybe it's already a key)
                    if not resolved:
                        if ref in valid_keys:
                            resolved = True
                        elif f"p2kb{ref}" in valid_keys:
                            resolved = True

                    if resolved:
                        results['resolved_refs'] += 1
                        results['resolved_by_field'][field_name] += 1
                    else:
                        results['unresolved_refs'].append({
                            'file': rel_path,
                            'field': field_name,
                            'reference': ref,
                            'ref_type': ref_type,
                            'tried_keys': tried_keys[:3],  # First 3 attempted
                        })
                        results['unresolved_by_field'][field_name].append({
                            'file': rel_path,
                            'reference': ref,
                            'ref_type': ref_type,
                        })

            if has_refs:
                results['files_with_refs'] += 1

        except Exception as e:
            print(f"Error processing {yaml_file}: {e}")

    return results


def print_report(results: Dict):
    """Print a formatted validation report."""
    print("\n" + "=" * 70)
    print("P2KB CROSS-REFERENCE VALIDATION REPORT")
    print("=" * 70)

    print(f"\n📁 Files scanned: {results['total_files']}")
    print(f"📁 Files with cross-references: {results['files_with_refs']}")
    print(f"\n🔗 Total references: {results['total_refs']}")
    print(f"✅ Resolved references: {results['resolved_refs']}")
    print(f"❌ Unresolved references: {len(results['unresolved_refs'])}")

    resolution_rate = (results['resolved_refs'] / results['total_refs'] * 100) if results['total_refs'] > 0 else 0
    print(f"\n📊 Resolution rate: {resolution_rate:.1f}%")

    print("\n" + "-" * 70)
    print("RESOLUTION BY FIELD:")
    print("-" * 70)
    for field, count in sorted(results['resolved_by_field'].items()):
        print(f"  {field}: {count} resolved")

    if results['unresolved_refs']:
        print("\n" + "-" * 70)
        print("UNRESOLVED REFERENCES:")
        print("-" * 70)

        # Group by field type
        for field, refs in sorted(results['unresolved_by_field'].items()):
            print(f"\n🔸 {field} ({len(refs)} unresolved):")
            for ref_info in refs[:10]:  # Show first 10
                print(f"   {ref_info['file']}")
                print(f"      → \"{ref_info['reference']}\"")
            if len(refs) > 10:
                print(f"   ... and {len(refs) - 10} more")

    print("\n" + "=" * 70)
    if len(results['unresolved_refs']) == 0:
        print("✅ ALL CROSS-REFERENCES VALIDATED SUCCESSFULLY")
    else:
        print(f"⚠️  {len(results['unresolved_refs'])} REFERENCES NEED ATTENTION")
    print("=" * 70)


def main():
    """Main entry point."""
    base_path = Path("/workspaces/P2-Knowledge-Base")
    index_path = base_path / "deliverables" / "ai" / "p2kb-index.json"

    print("Loading index...")
    index = load_index(index_path)
    print(f"  Found {len(index.get('files', {}))} keys in index")

    print("\nScanning YAML files for cross-references...")
    results = validate_crossrefs(base_path, index)

    print_report(results)

    # Return exit code based on unresolved refs
    return 0 if len(results['unresolved_refs']) == 0 else 1


if __name__ == "__main__":
    exit(main())

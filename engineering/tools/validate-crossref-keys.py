#!/usr/bin/env python3
"""
Validate that all cross-references in YAML files can be resolved to valid index keys.

SCOPE (F-340 / F-373, 2026-09-13): the release gate is that EVERY reference an agent
can follow resolves. So this validator reads the whole document, not the top level:
  * every string value, at every depth, is scanned for KB path tokens (`*.yaml`);
    each must be a KB-root-relative path to a file that exists (`engineering/...`
    tokens must exist in the repo; `_index.yaml` files may list siblings by bare name);
  * every reference field (`related*`, `see_also`, `references`, `cross_references`,
    `combines_with`, `grouped_with`, `prerequisites`, `next_steps`,
    `knowledge_progression`, `canonical_entries`) is walked at every depth, and its
    non-path entries in must-resolve fields must resolve to an index key, alias, or a
    symbol defined somewhere in the KB (`symbol_name:`);
  * `--negative-control` plants one defect of every kind and proves each is caught.
Nothing is reported as "not checked": there is no scope caveat left to print.

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


PATH_TOKEN = re.compile(r'(?<![\w@/.-])(/?(?:\.{1,2}/)?(?:[\w.-]+/)*[\w.-]+\.ya?ml)(?![\w-])')
REF_FIELD_RE = re.compile(r'^(related(_[a-z0-9_]+)?|see_also|references|prerequisites|next_steps|'
                          r'knowledge_progression|canonical_entries|cross_references|combines_with|grouped_with)$')

# How each KNOWN reference field's non-path entries are handled. Path-shaped
# entries are checked for every field by the path-token pass, whatever the type.
CROSS_REF_FIELDS = {
    'related': 'mnemonic',
    'related_components': 'component',
    'cross_references': 'nested_dict',
    'see_also': 'text',
    'references': 'text',
    'related_documentation': 'mnemonic',
    'related_concepts': 'text',
    'related_constructs': 'mnemonic',
    'related_operators': 'mnemonic',
    'related_pasm': 'mnemonic',
    'related_methods': 'mnemonic',
    'related_instructions': 'mnemonic',
    'combines_with': 'mnemonic',
    'grouped_with': 'mnemonic',
    'related_symbols': 'mnemonic',
}


def is_schema_descriptor(value) -> bool:
    """A JSON-schema-style field descriptor ({type: array, items: ...}) documents a
    field; it is not a reference list. Schema-definition files carry these."""
    return (isinstance(value, dict) and 'type' in value
            and any(k in value for k in ('items', 'description', 'required', 'properties')))


def iter_strings(node, path=()):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from iter_strings(v, path + (str(k),))
    elif isinstance(node, list):
        for i, x in enumerate(node):
            yield from iter_strings(x, path + (f'[{i}]',))
    elif isinstance(node, str):
        yield '.'.join(path), node


def iter_ref_fields(node, path=()):
    """Every reference field at every depth. Does not descend into a reference
    field's own value (its strings are covered by the path-token pass)."""
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(k, str) and (k in CROSS_REF_FIELDS or REF_FIELD_RE.match(k)):
                yield '.'.join(path + (k,)), k, v
            else:
                yield from iter_ref_fields(v, path + (str(k),))
    elif isinstance(node, list):
        for i, x in enumerate(node):
            yield from iter_ref_fields(x, path + (f'[{i}]',))


class CrossRefChecker:
    def __init__(self, base_path: Path, index: Dict):
        self.repo_root = base_path
        self.yaml_dir = base_path / "deliverables" / "ai" / "P2"
        self.valid_keys = set(index.get('files', {}).keys())
        self.aliases = index.get('aliases', {})
        self.defined_symbols: Set[str] = set()
        self.by_basename = defaultdict(list)
        self.results = {
            'total_files': 0, 'files_with_refs': 0,
            'path_tokens': 0, 'path_ok': 0,
            'name_refs': 0, 'name_ok': 0, 'informational': 0,
            'schema_descriptors_skipped': 0,
            'issues': [],
            'resolved_by_field': defaultdict(int),
            'unlisted_fields': defaultdict(int),
        }

    # -- setup ---------------------------------------------------------------
    def load_corpus(self):
        docs = []
        for yaml_file in sorted(self.yaml_dir.rglob("*.yaml")):
            rel = str(yaml_file.relative_to(self.yaml_dir))
            self.by_basename[yaml_file.name].append(rel)
            try:
                with open(yaml_file, 'r') as f:
                    content = yaml.safe_load(f)
            except Exception as e:
                self.issue(rel, '', '', 'parse_error', str(e)[:200])
                continue
            docs.append((rel, content))
            self._collect_symbols(content)
        return docs

    def _collect_symbols(self, node):
        if isinstance(node, dict):
            name = node.get('symbol_name')
            if isinstance(name, str):
                self.defined_symbols.add(name)
            for v in node.values():
                self._collect_symbols(v)
        elif isinstance(node, list):
            for x in node:
                self._collect_symbols(x)

    def issue(self, rel, keypath, ref, kind, detail=''):
        self.results['issues'].append({'file': rel, 'where': keypath, 'reference': ref,
                                       'kind': kind, 'detail': detail})

    # -- path tokens -----------------------------------------------------------
    def check_path_token(self, rel, keypath, tok):
        r = self.results
        r['path_tokens'] += 1
        if tok.startswith('/') or 'deliverables/ai/P2/' in tok:
            return self.issue(rel, keypath, tok, 'root_prefixed',
                              'write KB-root-relative: ' + tok.split('deliverables/ai/P2/')[-1].lstrip('/'))
        if tok.startswith('./') or tok.startswith('../'):
            return self.issue(rel, keypath, tok, 'relative_path', self._suggest(rel, tok))
        if tok.startswith('engineering/'):
            if (self.repo_root / tok).is_file():
                r['path_ok'] += 1
                return
            return self.issue(rel, keypath, tok, 'missing_repo_file')
        if (self.yaml_dir / tok).is_file():
            r['path_ok'] += 1
            return
        if Path(rel).name == '_index.yaml' and (self.yaml_dir / Path(rel).parent / tok).is_file():
            r['path_ok'] += 1   # a directory index may list its own files by bare name
            return
        sugg = self._suggest(rel, tok)
        self.issue(rel, keypath, tok, 'not_full_path' if sugg else 'missing', sugg)

    def _suggest(self, rel, tok):
        cand = os.path.normpath(str(Path(rel).parent / tok))
        if (self.yaml_dir / cand).is_file():
            return cand
        hits = self.by_basename.get(Path(tok).name, [])
        if len(hits) == 1:
            return hits[0]
        if len(hits) > 1:
            return 'ambiguous: ' + ', '.join(hits)
        return ''

    # -- names -------------------------------------------------------------------
    def resolve_name(self, ref, ref_type, rel):
        aliases, valid_keys = self.aliases, self.valid_keys
        if ref in self.defined_symbols:
            return True
        for cand in (ref, ref.upper(), ref.lower()):
            targets = aliases.get(cand)
            if isinstance(targets, list) and any(t in valid_keys for t in targets):
                return True
            if isinstance(targets, str) and targets in valid_keys:
                return True
        if ref_type == 'mnemonic':
            if is_informational_reference(ref):
                return True
            if len(ref) <= 20 and ref.replace('_', '').replace('-', '').isalnum():
                keys = transform_mnemonic_to_key(ref, rel, valid_keys)
                if '__INFORMATIONAL__' in keys or any(k in valid_keys for k in keys):
                    return True
        if ref_type == 'component' and transform_component_to_key(ref, valid_keys):
            return True
        return ref in valid_keys or f"p2kb{ref}" in valid_keys

    # -- per document --------------------------------------------------------------
    def check_document(self, rel, content):
        r = self.results
        r['total_files'] += 1
        if content is None:
            return
        for keypath, s in iter_strings(content):
            for m in PATH_TOKEN.finditer(s):
                self.check_path_token(rel, keypath, m.group(1))
        has_refs = False
        for keypath, field, value in iter_ref_fields(content):
            if not value:
                continue
            if is_schema_descriptor(value):
                r['schema_descriptors_skipped'] += 1
                continue
            has_refs = True
            ftype = CROSS_REF_FIELDS.get(field)
            if ftype is None:
                r['unlisted_fields'][field] += 1
                ftype = 'text'
            for ref, rtype in extract_refs_from_value(value, field, ftype):
                if not isinstance(ref, str) or not ref.strip():
                    continue
                ref = ref.strip()
                if PATH_TOKEN.search(ref):
                    continue            # validated by the path-token pass
                if rtype in ('text', 'path'):
                    r['informational'] += 1
                    continue
                r['name_refs'] += 1
                if self.resolve_name(ref, rtype, rel):
                    r['name_ok'] += 1
                    r['resolved_by_field'][field] += 1
                else:
                    self.issue(rel, keypath, ref, 'unresolved_name', f'field {field} ({rtype})')
        if has_refs:
            r['files_with_refs'] += 1


def validate_crossrefs(base_path: Path, index: Dict) -> Dict:
    checker = CrossRefChecker(base_path, index)
    for rel, content in checker.load_corpus():
        checker.check_document(rel, content)
    return checker.results


def run_negative_control(base_path: Path, index: Dict) -> int:
    """Plant one defect of every kind the gate claims to catch, plus a positive
    control that must stay clean. A gate that cannot fail on these proves nothing."""
    checker = CrossRefChecker(base_path, index)
    checker.load_corpus()                       # symbols + basenames from the real KB
    checker.results['issues'] = []
    cases = [
        ('nc/nested_related_missing.yaml', {'s': {'related': ['language/pasm2/no_such_file.yaml']}}, 'missing'),
        ('nc/nested_symbol_bogus.yaml', {'items': [{'related_symbols': ['NOT_A_REAL_SYMBOL_XYZ']}]}, 'unresolved_name'),
        ('nc/see_also_missing.yaml', {'see_also': ['architecture/no_such_file.yaml']}, 'missing'),
        ('nc/root_prefixed.yaml', {'next_steps': ['/deliverables/ai/P2/architecture/cog.yaml - read first']}, 'root_prefixed'),
        ('nc/unlisted_field_missing.yaml', {'a': {'related_patterns': ['language/spin2/nope.yaml']}}, 'missing'),
        ('nc/prose_in_related.yaml', {'documentation': {'related': ['Some Vendor Datasheet Title']}}, 'unresolved_name'),
        ('nc/bare_in_prose.yaml', {'note': 'see cog.yaml for details'}, 'not_full_path'),
        ('nc/relative_path.yaml', {'related': ['../pasm2/mov.yaml']}, 'relative_path'),
        ('nc/positive_control.yaml', {
            'related': ['language/pasm2/mov.yaml', 'MOV'],
            'x': {'related_symbols': ['EVENT_CT1']},
            'see_also': ['architecture/cog.yaml', 'free prose is informational'],
            'schema': {'related_symbols': {'type': 'array', 'items': {'type': 'string'}}},
            'next_steps': ['architecture/hub.yaml - the hub'],
        }, None),
    ]
    ok = True
    print("NEGATIVE CONTROL — each planted defect must be caught; the positive control must stay clean")
    for rel, doc, expect in cases:
        before = len(checker.results['issues'])
        checker.check_document(rel, doc)
        got = [i['kind'] for i in checker.results['issues'][before:]]
        passed = (expect in got) if expect else (got == [])
        ok &= passed
        print(f"  {'PASS' if passed else 'FAIL'}  {rel:38s} expect={expect or 'clean'} got={got or 'clean'}")
    print("NEGATIVE CONTROL: " + ("PASS" if ok else "FAIL — the gate cannot see a defect it claims to catch"))
    return 0 if ok else 1


def print_report(results: Dict):
    print("\n" + "=" * 70)
    print("P2KB CROSS-REFERENCE VALIDATION REPORT")
    print("=" * 70)
    r = results
    issues = r['issues']
    checked = r['path_tokens'] + r['name_refs']
    ok = r['path_ok'] + r['name_ok']
    print(f"\n📁 Files scanned: {r['total_files']}   (files with reference fields: {r['files_with_refs']})")
    print(f"🔗 KB path tokens checked (every string, every depth): {r['path_tokens']}  — resolved {r['path_ok']}")
    print(f"🔗 Named references checked (reference fields, every depth): {r['name_refs']}  — resolved {r['name_ok']}")
    print(f"   informational entries (prose in text-typed fields): {r['informational']}")
    print(f"   schema field descriptors skipped: {r['schema_descriptors_skipped']}")
    if r['unlisted_fields']:
        print("   reference-shaped fields with no declared type (paths checked, prose informational): "
              + ', '.join(f"{k}={v}" for k, v in sorted(r['unlisted_fields'].items())))
    rate = (ok / checked * 100) if checked else 0
    print(f"\n📊 Resolution rate: {rate:.1f}%")
    if issues:
        print("\n" + "-" * 70)
        print(f"REFERENCES THAT DO NOT RESOLVE — COMPLETE LIST ({len(issues)})")
        print("-" * 70)
        by_kind = defaultdict(list)
        for i in issues:
            by_kind[i['kind']].append(i)
        for kind in sorted(by_kind):
            print(f"\n🔸 {kind} ({len(by_kind[kind])}):")
            for i in by_kind[kind]:
                print(f"   {i['file']}  [{i['where']}]")
                print(f"      → \"{i['reference']}\"" + (f"   ({i['detail']})" if i['detail'] else ''))
    print("\n" + "=" * 70)
    if not issues and checked:
        print(f"✅ ALL CROSS-REFERENCES RESOLVE — {checked} checked, every field, every depth")
    else:
        print(f"❌ {len(issues)} REFERENCE(S) DO NOT RESOLVE")
    print("=" * 70)


def main():
    import sys
    base_path = Path.cwd()
    index_path = base_path / "deliverables" / "ai" / "p2kb-index.json"
    print("Loading index...")
    index = load_index(index_path)
    print(f"  Found {len(index.get('files', {}))} keys in index")
    if '--negative-control' in sys.argv:
        return run_negative_control(base_path, index)
    print("\nScanning YAML files for cross-references...")
    results = validate_crossrefs(base_path, index)
    print_report(results)
    return 0 if not results['issues'] and (results['path_tokens'] + results['name_refs']) else 1


if __name__ == "__main__":
    exit(main())

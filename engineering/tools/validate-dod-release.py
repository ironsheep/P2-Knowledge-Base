#!/usr/bin/env python3
"""
P2 Knowledge Base DOD (Download-On-Demand) Release Validator v1.1

Comprehensive validation suite for DOD v3.0 releases.
Run this before pushing any changes to the knowledge base.

Usage:
    python3 engineering/tools/validate-dod-release.py [--verbose] [--incremental]

Options:
    --verbose, -v     Show detailed output
    --incremental     Only validate YAMLs changed since last run
    --full            Force full validation (ignore history)
    --post-commit     Run after the content commit (release step 6c): the index
                      freshness limb treats a dirty deliverables/ai/P2 tree as an error
    --help, -h        Show this help

Exit codes:
    0 = All validations passed
    1 = Validation failures found
"""

import hashlib
import json
import os
import re
import tempfile
import sys
import gzip
import subprocess
import yaml
from pathlib import Path
from collections import Counter
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set

# Configuration
INDEX_PATH = Path("deliverables/ai/p2kb-index.json")
INDEX_GZ_PATH = Path("deliverables/ai/p2kb-index.json.gz")
YAML_BASE = Path("deliverables/ai/P2")
HISTORY_FILE = Path("engineering/tools/.dod-validation-history.json")

# The delivery filter's rule is read from the GENERATED INDEX -- the artifact every
# receiver reads -- never from a copy held here. A copy per receiver is what let the
# MCP server ship a stale filter (F-439). generate-p2kb-index.py's DELIVERY_FILTER
# is the single source; contract MCP-DELIVERY-FILTER-HANDOFF.md §3 (format 1).
_FIELD_NAME_RE = re.compile(r'^[A-Za-z0-9_]+$')
_INDEX_RULE = None


def index_filter_rule() -> Tuple[Optional[Dict], str]:
    """(rule, problem) from the index's `delivery_filter`, validated as strictly as a
    format-1 receiver must (agreement §3). rule is None when it is absent or invalid,
    and problem says why -- the release fails on either (agreement §8.1)."""
    global _INDEX_RULE
    if _INDEX_RULE is None:
        with open(INDEX_PATH) as f:
            rule = json.load(f).get('delivery_filter')
        problem = ''
        if rule is None:
            problem = 'the index carries no delivery_filter block'
        elif not isinstance(rule, dict) or set(rule) != {'format', 'remove_fields', 'remove_column0_comments'}:
            problem = 'delivery_filter must have exactly format / remove_fields / remove_column0_comments'
        elif type(rule['format']) is not int or rule['format'] != 1:
            problem = f"delivery_filter.format is {rule['format']!r}, not the integer 1"
        elif type(rule['remove_column0_comments']) is not bool:
            problem = 'delivery_filter.remove_column0_comments is not a boolean'
        elif (not isinstance(rule['remove_fields'], list) or not rule['remove_fields']
              or not all(isinstance(n, str) and _FIELD_NAME_RE.match(n) for n in rule['remove_fields'])
              or len(set(rule['remove_fields'])) != len(rule['remove_fields'])):
            problem = 'delivery_filter.remove_fields must be a non-empty list of unique literal names'
        _INDEX_RULE = (None if problem else rule, problem)
    return _INDEX_RULE


def filter_rule_id(rule: Dict) -> str:
    """rule_id per agreement §3.1 -- what every receiver computes for this rule."""
    text = (f"p2kb-delivery-filter\nformat={rule['format']}\n"
            f"remove_fields={','.join(rule['remove_fields'])}\n"
            f"remove_column0_comments={'true' if rule['remove_column0_comments'] else 'false'}\n")
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _rule_fields() -> Set[str]:
    rule, _ = index_filter_rule()
    return set(rule['remove_fields']) if rule else set()


# =============================================================================
# VALIDATION HISTORY MANAGEMENT
# =============================================================================

def load_validation_history() -> Dict:
    """Load previous validation run history."""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE) as f:
                return json.load(f)
        except:
            pass
    return {
        'last_run': None,
        'last_run_passed': None,
        'yaml_checksums': {},
        'runs': []
    }


def save_validation_history(history: Dict):
    """Save validation run history."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)


def get_yaml_checksum(path: Path) -> str:
    """Get a simple checksum for a YAML file (mtime + size)."""
    stat = path.stat()
    return f"{stat.st_mtime}:{stat.st_size}"


def get_changed_yamls(history: Dict) -> Tuple[Set[Path], Set[Path], Set[Path]]:
    """
    Compare current YAMLs against history.
    Returns: (new_files, modified_files, deleted_files)
    """
    old_checksums = history.get('yaml_checksums', {})

    current_files = {}
    for yaml_file in YAML_BASE.rglob("*.yaml"):
        if yaml_file.name == 'manifest.yaml':
            continue
        rel_path = str(yaml_file.relative_to(YAML_BASE))
        current_files[rel_path] = get_yaml_checksum(yaml_file)

    new_files = set()
    modified_files = set()
    deleted_files = set()

    # Find new and modified
    for rel_path, checksum in current_files.items():
        full_path = YAML_BASE / rel_path
        if rel_path not in old_checksums:
            new_files.add(full_path)
        elif old_checksums[rel_path] != checksum:
            modified_files.add(full_path)

    # Find deleted
    for rel_path in old_checksums:
        if rel_path not in current_files:
            deleted_files.add(YAML_BASE / rel_path)

    return new_files, modified_files, deleted_files


def update_history_checksums(history: Dict):
    """Update checksums in history for all current YAMLs."""
    checksums = {}
    for yaml_file in YAML_BASE.rglob("*.yaml"):
        if yaml_file.name == 'manifest.yaml':
            continue
        rel_path = str(yaml_file.relative_to(YAML_BASE))
        checksums[rel_path] = get_yaml_checksum(yaml_file)
    history['yaml_checksums'] = checksums


# =============================================================================
# VALIDATION RESULT CONTAINER
# =============================================================================

class ValidationResult:
    """Container for validation results."""
    def __init__(self, name: str):
        self.name = name
        self.passed = True
        self.messages: List[str] = []
        self.warnings: List[str] = []

    def fail(self, msg: str):
        self.passed = False
        self.messages.append(f"❌ {msg}")

    def warn(self, msg: str):
        self.warnings.append(f"⚠️  {msg}")

    def ok(self, msg: str):
        self.messages.append(f"✅ {msg}")

    def info(self, msg: str):
        self.messages.append(f"   {msg}")


def validate_index_structure(verbose: bool = False) -> ValidationResult:
    """Validate index JSON structure and contents."""
    result = ValidationResult("Index Structure")

    # Check index exists
    if not INDEX_PATH.exists():
        result.fail(f"Index not found: {INDEX_PATH}")
        return result

    # Parse JSON
    try:
        with open(INDEX_PATH) as f:
            idx = json.load(f)
    except json.JSONDecodeError as e:
        result.fail(f"Invalid JSON: {e}")
        return result

    result.ok("Index is valid JSON")

    # Check required fields
    if 'system' not in idx:
        result.fail("Missing 'system' section")
    else:
        sys_info = idx['system']
        result.info(f"Version: {sys_info.get('version', 'MISSING')}")
        result.info(f"Entries: {sys_info.get('total_entries', 'MISSING')}")
        result.info(f"Generated: {sys_info.get('generated', 'MISSING')}")

    if 'files' not in idx:
        result.fail("Missing 'files' section")
        return result

    # Validate entry count matches
    actual_count = len(idx['files'])
    declared_count = idx.get('system', {}).get('total_entries', 0)
    if actual_count != declared_count:
        result.fail(f"Entry count mismatch: declared={declared_count}, actual={actual_count}")
    else:
        result.ok(f"Entry count verified: {actual_count}")

    return result


def validate_gzip_compression(verbose: bool = False) -> ValidationResult:
    """Validate gzip file exists and decompresses correctly."""
    result = ValidationResult("Gzip Compression")

    if not INDEX_GZ_PATH.exists():
        result.fail(f"Compressed index not found: {INDEX_GZ_PATH}")
        return result

    # Check file sizes
    json_size = INDEX_PATH.stat().st_size
    gz_size = INDEX_GZ_PATH.stat().st_size
    ratio = (1 - gz_size / json_size) * 100
    result.info(f"JSON size: {json_size:,} bytes")
    result.info(f"Gzip size: {gz_size:,} bytes ({ratio:.1f}% compression)")

    # Verify decompression
    try:
        with gzip.open(INDEX_GZ_PATH, 'rt') as f:
            gz_content = f.read()
        with open(INDEX_PATH) as f:
            json_content = f.read()

        if gz_content == json_content:
            result.ok("Gzip decompresses to identical content")
        else:
            result.fail("Gzip content does not match JSON file")
    except Exception as e:
        result.fail(f"Decompression failed: {e}")

    return result


def validate_file_paths(verbose: bool = False) -> ValidationResult:
    """Validate all index paths point to existing files."""
    result = ValidationResult("File Paths")

    with open(INDEX_PATH) as f:
        idx = json.load(f)

    missing = []
    for key, entry in idx['files'].items():
        path = Path(entry['path'])
        if not path.exists():
            missing.append((key, entry['path']))

    if missing:
        result.fail(f"{len(missing)} paths point to non-existent files")
        for key, path in missing[:5]:
            result.info(f"  {key}: {path}")
        if len(missing) > 5:
            result.info(f"  ... and {len(missing) - 5} more")
    else:
        result.ok(f"All {len(idx['files'])} paths exist")

    return result


def validate_orphaned_files(verbose: bool = False) -> ValidationResult:
    """Check for YAML files not in the index."""
    result = ValidationResult("Orphaned Files")

    with open(INDEX_PATH) as f:
        idx = json.load(f)

    indexed_paths = set(entry['path'] for entry in idx['files'].values())

    orphaned = []
    for yaml_file in YAML_BASE.rglob("*.yaml"):
        if yaml_file.name == 'manifest.yaml':
            continue
        rel_path = f"deliverables/ai/P2/{yaml_file.relative_to(YAML_BASE)}"
        if rel_path not in indexed_paths:
            orphaned.append(rel_path)

    if orphaned:
        result.fail(f"{len(orphaned)} YAML files not in index")
        for path in orphaned[:5]:
            result.info(f"  {path}")
    else:
        result.ok(f"No orphaned YAML files")

    return result


def validate_key_naming(verbose: bool = False) -> ValidationResult:
    """Validate key naming conventions."""
    result = ValidationResult("Key Naming")

    with open(INDEX_PATH) as f:
        idx = json.load(f)

    issues = []
    special_char_keys = []

    for key, entry in idx['files'].items():
        # Skip synthetic alias entries promoted from the aliases section by
        # generate-p2kb-index.py's promote_aliases_to_files (see that function's
        # docstring). When that workaround is removed, this skip can go too.
        if isinstance(entry, dict) and 'alias_of' in entry:
            continue
        if not key.startswith('p2kb'):
            issues.append(f"Missing p2kb prefix: {key}")
        else:
            clean_part = key[4:]
            if not clean_part.replace('_', '').isalnum():
                special_char_keys.append(key)

    if issues:
        result.fail(f"{len(issues)} keys have naming issues")
        for issue in issues[:5]:
            result.info(f"  {issue}")
    else:
        result.ok("All keys follow p2kb prefix convention")

    if special_char_keys:
        result.warn(f"{len(special_char_keys)} keys contain special characters (valid Spin2 symbols)")
        if verbose:
            for key in special_char_keys:
                result.info(f"  {repr(key)}")

    return result


def validate_timestamps(verbose: bool = False) -> ValidationResult:
    """Validate all timestamps are reasonable."""
    result = ValidationResult("Timestamps")

    with open(INDEX_PATH) as f:
        idx = json.load(f)

    now = datetime.now().timestamp()
    one_year_ago = now - (365 * 24 * 60 * 60)

    issues = []
    for key, entry in idx['files'].items():
        mtime = entry.get('mtime', 0)
        if mtime == 0:
            issues.append((key, "Missing timestamp"))
        elif mtime > now + 86400:
            issues.append((key, "Future timestamp"))

    if issues:
        result.warn(f"{len(issues)} timestamp issues")
        for key, issue in issues[:5]:
            result.info(f"  {key}: {issue}")
    else:
        result.ok(f"All timestamps valid")

    return result


def _find_filter_induced_nulls(original_obj, filtered_obj, path: str = "") -> List[str]:
    """Walk the FILTERED payload (the artifact, not the declaration) and report
    any key whose value collapsed to None as a side effect of line-filtering.

    Line-based filtering removes a `key:` line without regard for whether that
    key had siblings. When every child of a mapping key was itself a filtered
    field, the parent key survives with nothing under it — `yaml.safe_load`
    reads that as `key: null`, and a consumer sees a live key holding no data.
    Diffing REMOVED LINES against an expected-field list never catches this:
    every removed line IS an expected field. Only re-parsing the delivered
    payload and comparing it back to the source catches the collapse.
    """
    bad: List[str] = []
    if isinstance(filtered_obj, dict):
        if not isinstance(original_obj, dict):
            return bad
        for k, fv in filtered_obj.items():
            new_path = f"{path}.{k}" if path else str(k)
            ov = original_obj.get(k, None)
            if fv is None and isinstance(ov, (dict, list)) and ov:
                bad.append(new_path)
            else:
                bad.extend(_find_filter_induced_nulls(ov, fv, new_path))
    elif isinstance(filtered_obj, list) and isinstance(original_obj, list):
        for i, (ov, fv) in enumerate(zip(original_obj, filtered_obj)):
            bad.extend(_find_filter_induced_nulls(ov, fv, f"{path}[{i}]"))
    return bad


def _strip_provenance_keys(obj):
    """The structural reading of the filter's intent: the same field names,
    removed as YAML KEYS (what YAML itself says is a key), not as lines."""
    if isinstance(obj, dict):
        return {k: _strip_provenance_keys(v) for k, v in obj.items()
                if str(k) not in _rule_fields()}
    if isinstance(obj, list):
        return [_strip_provenance_keys(x) for x in obj]
    return obj


def _find_filter_eaten_content(expected_obj, filtered_obj, path: str = "") -> List[str]:
    """Content the line filter deleted although YAML reads it as content.

    The line rule drops any line that STARTS WITH a provenance field name, so a
    wrapped prose line inside a block scalar that happens to begin `sources: ...`
    is deleted from the delivered text (2026-10-04: the P60/P61 boot-pin swap
    in both Edge module notes was shipped with that line missing). Comparing the
    filter to a prediction of the same line rule cannot see it; comparing it to
    YAML's own reading can. Direction matters: the filter KEEPING a content key
    that happens to share a field name (a flow mapping `{source: "cog
    registers"}`, a list item `- source: "CON"`) is correct and is not reported.
    """
    eaten: List[str] = []
    if isinstance(expected_obj, dict) and isinstance(filtered_obj, dict):
        for k, ev in expected_obj.items():
            new_path = f"{path}.{k}" if path else str(k)
            if k not in filtered_obj:
                eaten.append(f"{new_path} (key missing)")
            else:
                eaten.extend(_find_filter_eaten_content(ev, filtered_obj[k], new_path))
    elif isinstance(expected_obj, list) and isinstance(filtered_obj, list):
        if len(expected_obj) != len(filtered_obj):
            eaten.append(f"{path} (list length {len(expected_obj)} -> {len(filtered_obj)})")
        for i, (ev, fv) in enumerate(zip(expected_obj, filtered_obj)):
            eaten.extend(_find_filter_eaten_content(ev, fv, f"{path}[{i}]"))
    elif isinstance(expected_obj, str) and isinstance(filtered_obj, str):
        kept = {ln.strip() for ln in filtered_obj.split('\n')}
        lost = [ln.strip() for ln in expected_obj.split('\n')
                if ln.strip() and ln.strip() not in kept]
        if lost:
            eaten.append(f"{path} (line lost: {lost[0][:70]!r})")
    return eaten


def _predicted_filtered(original: str) -> str:
    """An INDEPENDENT prediction of what the shipped filter should produce.

    This is deliberately a second implementation of the same rule, and it is NOT
    used to build the payload -- `_apply_shipped_filter` does that, by running the
    real thing. This one exists so the two can be COMPARED: agreement between two
    independent readings is evidence, and a disagreement is a finding about one of
    them. What it must never become again is the single source of the answer, which
    is what let the Python line-model and the shipped filter drift apart.

    It is a transcription of the agreement's format-1 text (MCP-DELIVERY-FILTER-HANDOFF.md
    §4), applied with the rule read from the index -- not of the awk.
    """
    rule, _ = index_filter_rule()
    if rule is None:
        return original
    if original == '':
        return ''
    ws = ' \t\n\v\f\r'                       # POSIX [[:space:]], as the agreement says
    fields = set(rule['remove_fields'])
    col0 = rule['remove_column0_comments']
    kept = []
    dropping = False
    drop_indent = 0
    for line in original.split('\n'):
        if dropping:
            body = line.lstrip(ws)
            if body == '' or body.startswith('#'):     # blank or comment: span continues
                continue
            if len(line) - len(body) > drop_indent:    # deeper: still the field
                continue
            dropping = False                           # span ended; test this line
        if col0 and line.startswith('#'):
            continue
        indent = len(line) - len(line.lstrip(ws))
        rest = line[indent:]
        colon = rest.find(':')
        if colon > 0 and rest[:colon] in fields:
            drop_indent, dropping = indent, True
            continue
        kept.append(line)
    return '\n'.join(kept)


def _apply_shipped_filter(paths):
    """Run the SHIPPED filter -- fetch-kb-file.sh's own `filter_metadata` -- over
    every path, in ONE subprocess, and return {path: filtered_text}.

    WHY THIS SHELLS OUT (2026-09-19). This check used to re-implement the filter
    in Python as a line regex (`FILTER_PATTERN.match`). That was a MODEL of the
    filter, and on 2026-09-19 the model and the artifact diverged: the shipped
    filter became indentation-aware so it could strip block scalars, and the
    Python line-model kept reporting 50 files broken that the real filter handles
    correctly. A gate must read the produced artifact, never a declaration of it
    -- and a gate that models the thing it checks will eventually check the model.

    The rule it applies is the INDEX's (passed as RULE_FIELDS / RULE_COL0, exactly
    as fetch-kb-file.sh's load_filter_rule sets them), so the payload checked is
    the payload a receiver of this index would deliver.
    """
    sh = Path("engineering/tools/p2kb/fetch-kb-file.sh").read_text()
    start = sh.index("filter_metadata() {")
    end = sh.index("\n}\n", start) + 3
    delim = "@@P2KB-FILTER-DELIM@@"
    driver = sh[start:end] + f'\nfor f in "$@"; do echo "{delim}$f"; filter_metadata < "$f"; done\n'
    rule, _ = index_filter_rule()
    env = dict(os.environ)
    if rule is not None:
        env['RULE_FIELDS'] = ','.join(rule['remove_fields'])
        env['RULE_COL0'] = 'true' if rule['remove_column0_comments'] else 'false'
    proc = subprocess.run(["bash", "-c", driver, "bash"] + [str(x) for x in paths],
                          capture_output=True, text=True, env=env)
    if proc.returncode != 0:
        raise RuntimeError(f"shipped filter failed: {proc.stderr[:200]}")
    out, cur, buf = {}, None, []
    for line in proc.stdout.split("\n"):
        if line.startswith(delim):
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur, buf = line[len(delim):], []
        else:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


_SHIPPED_PAYLOAD = None


def _shipped_payload():
    """(live index entries, {path: shipped payload}) -- computed once per run.

    Two validators read the payload; the shipped filter is one bash pass over
    every file, so it runs once and both share the result.
    """
    global _SHIPPED_PAYLOAD
    if _SHIPPED_PAYLOAD is None:
        with open(INDEX_PATH) as f:
            idx = json.load(f)
        live = [(key, Path(entry['path'])) for key, entry in idx['files'].items()
                if Path(entry['path']).exists()]
        _SHIPPED_PAYLOAD = (live, _apply_shipped_filter([p for _, p in live]))
    return _SHIPPED_PAYLOAD


def validate_metadata_filter(verbose: bool = False) -> ValidationResult:
    """Comprehensive audit of metadata filtering."""
    result = ValidationResult("Metadata Filter")

    total_files = 0
    files_with_changes = 0
    field_removals = Counter()
    unexpected_changes = []
    structural_failures = []

    rule, problem = index_filter_rule()
    if rule is None:
        result.fail(f"No usable delivery filter rule: {problem} -- every receiver reads "
                    f"the rule from the index (MCP-DELIVERY-FILTER-HANDOFF.md §8.1)")
        return result
    result.info(f"Rule from the index: rule_id {filter_rule_id(rule)}")
    fields = set(rule['remove_fields'])

    live, shipped = _shipped_payload()

    for key, path in live:
        total_files += 1

        with open(path) as f:
            original = f.read()

        # The payload the consumer actually receives, produced by the shipped
        # filter itself rather than a Python model of it.
        filtered = shipped[str(path)]

        # Did the shipped filter remove exactly what the published rule says? Compared
        # against an independent prediction on EVERY file -- including those the
        # shipped filter left unchanged, or a filter that silently removed nothing
        # would never be compared at all.
        if filtered.rstrip('\n') != _predicted_filtered(original).rstrip('\n'):
            unexpected_changes.append(
                (key, 'shipped filter and the expected rule disagree on this file'))

        if original != filtered:
            files_with_changes += 1

            for line in original.split('\n'):
                if rule['remove_column0_comments'] and line.startswith('#'):
                    field_removals['#column-0 comment'] += 1
                    continue
                name = line.strip().split(':', 1)[0]
                if ':' in line and name in fields:
                    field_removals[name] += 1

            # Read the ARTIFACT, not the declaration: does the payload the
            # consumer actually receives still parse, and did filtering
            # collapse any key to null?
            try:
                original_obj = yaml.safe_load(original)
                filtered_obj = yaml.safe_load(filtered)
            except yaml.YAMLError as e:
                structural_failures.append((key, f"filtered payload does not parse: {e}"))
                continue
            for bad_path in _find_filter_induced_nulls(original_obj, filtered_obj):
                structural_failures.append(
                    (key, f"key '{bad_path}' became null — every child was a filtered field"))
            for eaten in _find_filter_eaten_content(_strip_provenance_keys(original_obj), filtered_obj):
                structural_failures.append(
                    (key, f"filter deleted content YAML reads as content: {eaten}"))

    result.info(f"Files analyzed: {total_files}")
    result.info(f"Files with metadata: {files_with_changes}")

    if verbose:
        for field, count in sorted(field_removals.items()):
            result.info(f"  {field}: {count} removals")

    if unexpected_changes:
        result.fail(f"{len(unexpected_changes)} file(s) where the shipped filter "
                    f"and the expected rule disagree")
        for key, line in unexpected_changes[:5]:
            result.info(f"  {key}: {line}")
    else:
        result.ok("Shipped filter agrees with the expected rule on every file")

    if structural_failures:
        result.fail(f"{len(structural_failures)} file(s) deliver a structurally "
                    f"broken payload after filtering")
        for key, msg in structural_failures:      # every hit: a capped list reads like a clean one
            result.info(f"  {key}: {msg}")
    else:
        result.ok("Filtered payload re-parses cleanly with no filter-induced null keys and no deleted content")

    return result


# CP-NNN (compile proofs) and E-NNN (SOURCE-ERRATA) added 2026-10-09 («#414»): both
# registers are internal provenance, exactly like EF/XF.
INTERNAL_ID_PATTERN = re.compile(r'\b(?:EF|XF|F|CP|E)-\d{3}\b|\bVO-[A-Z]-\d{3}\b')

# Repo locators a consumer cannot open (F-523, 2026-10-03): a path into this repo,
# a document file cited by line (`silicon-doc-text.txt:2726`, `pasm2-manual-text :2087`),
# or a bare line cite (`(:834`, `doc :3269`). The bare form excludes a colon that
# follows a word, digit, `$`, `%`, `#`, `:` or `/` -- times, hex, URLs, labels.
REPO_LOCATOR_PATTERN = re.compile(
    r'\b(?:engineering|deliverables)/[\w./-]+'
    r'|\b[\w.-]+\.(?:txt|md|ya?ml|spin2|lst|pas|pdf|docx|html|json|py|sh)\s*:\s*\d+'
    r'|\b[\w-]+-text\s*:\s*\d+'
    r'|(?<![\w$#%:/]):\d{2,5}(?:[-,]\d+)?\b'
    r'|\bv\d{2}\s*:\s*\d{2,5}\b'               # `v55:1718` -- the F-400 shorthand
    r'|\(order \d+(?:,\s*\d+)*\)'              # `(order 154)` -- an instruction-sheet row number (F-557)
    r'|\b(?:SOURCE-ERRATA|P2KB-CORRECTION-FINDINGS|P2-EMPIRICAL-FINDINGS|'
    r'EXTERNAL-HARDWARE-FINDINGS|KNOWLEDGE-GAPS|APP-NOTE-DESIGN-DECISIONS)\.md\b')


def validate_internal_ids(verbose: bool = False) -> ValidationResult:
    """No internal identifier or repo locator reaches a consumer (F-519, F-523, 2026-10-03).

    F-523 widened it to repo locators: a repo path or a document `file:line` cite
    is provenance the consumer cannot open. Both belong in a stripped field
    (`source:` / `sources:`), where `audit-yaml-claim-sourcing.py` still reads them.

    Ledger ids (EF-/XF-NNN), finding ids (F-NNN) and verification-opportunity ids
    (VO-X-NNN) are provenance: this repo's gates and auditors resolve them, a
    consuming agent cannot. They may live in the fields the delivery filter strips
    (source, sources, ...) and in its provenance comments -- that is where
    provenance belongs. The bench audit of 2026-10-03 found 179 lines in 99 files
    carrying them in content that ships, because nothing checked the payload.
    So this reads the PAYLOAD: the shipped filter's own output, never the source
    tree, and every hit is printed (a capped list reads like a clean one).
    """
    result = ValidationResult("Internal IDs in Shipped Content")
    live, shipped = _shipped_payload()

    hits = []
    for _, path in live:
        for n, line in enumerate(shipped[str(path)].split('\n'), 1):
            for m in INTERNAL_ID_PATTERN.finditer(line):
                hits.append(f"{path} (payload line {n}): {m.group(0)} -- {line.strip()[:90]}")
            for m in REPO_LOCATOR_PATTERN.finditer(line):
                hits.append(f"{path} (payload line {n}): {m.group(0)} -- {line.strip()[:90]}")

    result.info(f"Files checked (shipped payload): {len(live)}")
    if hits:
        result.fail(f"{len(hits)} internal id(s) or repo locator(s) in shipped content -- "
                    f"move each to a stripped field (source:/sources:); state the fact only")
        for h in hits:
            result.info(f"  {h}")
    else:
        result.ok("No EF/XF/F/CP/E/VO identifier, repo path or file:line cite reaches a consumer")
    return result


# Register ids that are NEVER served, in ANY value -- source fields included (#422,
# 2026-10-10). EF-/XF-/CP- are citable records (the claim-sourcing gate resolves them
# and a reader can be told "EF-024"); F- (finding), E- (source erratum), S- (study
# decision) and VO- (verification opportunity) are our own bookkeeping and name nothing
# a reader or a citation may rest on. validate_internal_ids reads the delivery-filtered
# PAYLOAD, where source fields are already stripped, so it cannot see these; this reads
# the parsed source file's string VALUES (comments are not values).
REGISTER_ID_PATTERN = re.compile(r'(?<![A-Za-z0-9])(?:[FES]-\d{3}|VO-[A-Z]-\d{3})\b')

REGISTER_ID_CONTROL = [
    # (text, must_fire)
    ("Hardware-verified on P2 silicon (Rev C): hardware-verification ledger EF-024 (F-202).", True),
    ("Parallax Propeller 2 Documentation v35, SMART PINS; erratum E-007.", True),
    ("Study decision S-393 applies.", True),
    ("Opportunity VO-B-014 covers it.", True),
    # Citable records and ordinary text -- MUST NOT fire.
    ("Hardware-verified on P2 silicon (EF-024).", False),
    ("Compiler-proved (CP-001); measured on silicon (XF-001).", False),
    ("RS-232 and RS-485 line drivers.", False),
    ("The ATN-100 filter has a 3 dB corner.", False),
    ("DIV-007 is not a register id.", False),
]


def register_id_negative_control():
    """Return the control cases that misbehave (empty list == control passes)."""
    return [(text, want) for text, want in REGISTER_ID_CONTROL
            if bool(REGISTER_ID_PATTERN.search(text)) != want]


def validate_register_ids_in_values(verbose: bool = False) -> ValidationResult:
    """No F-/E-/S-/VO- register id in any shipped YAML value, source fields included.
    The negative control runs first: a check that cannot fire is not run."""
    result = ValidationResult("Register Ids in YAML Values (source fields included)")
    bad_control = register_id_negative_control()
    if bad_control:
        result.fail(f"negative control FAILED on {len(bad_control)} case(s) -- do not trust this run")
        for text, want in bad_control:
            result.info(f"  must_fire={want}: {text}")
        return result
    result.ok(f"Negative control: {sum(w for _, w in REGISTER_ID_CONTROL)} register-id shapes fire, "
              f"{sum(not w for _, w in REGISTER_ID_CONTROL)} citable or ordinary strings do not")

    live, _ = _shipped_payload()
    hits = []
    for _, path in live:
        try:
            doc = yaml.safe_load(Path(path).read_text(encoding='utf-8'))
        except (yaml.YAMLError, OSError):
            continue                    # an unparseable file is Metadata Filter's finding
        for key, value in _walk_string_values(doc):
            for m in REGISTER_ID_PATTERN.finditer(value):
                hits.append(f"{path} [{key}] {m.group(0)} -- {value.strip()[:90]!r}")

    result.info(f"Files checked (parsed source values): {len(live)}")
    if hits:
        result.fail(f"{len(hits)} F-/E-/S-/VO- register id(s) in YAML values -- remove them; "
                    f"EF-/XF-/CP- are the only ids a value may carry")
        for h in hits:
            result.info(f"  {h}")
    else:
        result.ok("No F-/E-/S-/VO- register id in any YAML value")
    return result


# Change-history phrasing (#422, 2026-10-10): the shipped entry states the FACT, never
# the story of its own edits -- "a prior form of this entry said...", "was fabricated",
# "until now", "added 2026-08-25". That story is provenance; it belongs in the
# register entry (F-NNN) or a YAML comment, both of which the consumer never sees.
# Every pattern is written against the SHAPE of an edit note, and the negative
# control below proves each one fires while ordinary technical prose that shares a
# word ("the previously configured mode", "added to the accumulator") does not.
HISTORY_PROSE_PATTERNS = [
    ("prior-form", re.compile(r"\ba prior (?:form|version|revision) of\b", re.I)),
    ("earlier-form", re.compile(r"\ban earlier (?:form|version|revision) of this\b", re.I)),
    ("previously-said", re.compile(
        r"\bpreviously (?:stood|said|stated|carried|claimed|asserted|read|listed|gave)\b", re.I)),
    ("this-was-previously", re.compile(
        r"\b(?:this|the) (?:file|entry|page|block|section) was previously\b", re.I)),
    ("fabricated", re.compile(r"\bwas fabricat", re.I)),
    ("until-now", re.compile(r"\buntil now\b", re.I)),
    ("not-restored", re.compile(
        r"\b(?:claim|figure|statement|sentence|entry|value|text|row) is not restored\b", re.I)),
    ("dated-edit", re.compile(
        r"\b(?:added|removed|corrected|changed|fixed|rewritten|deleted|demoted|retired|"
        r"replaced)\b[^.\n]{0,40}?\b20\d\d-\d\d-\d\d\b", re.I)),
]


def history_prose_hits(text):
    """The (pattern name, match) pairs of change-history phrasing in one string."""
    return [(name, m.group(0)) for name, rx in HISTORY_PROSE_PATTERNS
            for m in rx.finditer(text)]


def _walk_string_values(node, path=""):
    """Yield (key path, string) for every string VALUE in a parsed YAML tree.
    Parsing is what excludes comments: a YAML comment never reaches a consumer."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from _walk_string_values(v, f"{path}.{k}" if path else str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _walk_string_values(v, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


HISTORY_PROSE_CONTROL = [
    # (text, must_fire)
    ("A prior form of this entry gave 150 mA per pin.", True),
    ("An earlier version of this page listed six modes.", True),
    ("The table previously stated a 3 ns rise time.", True),
    ("This file was previously a parallel description of inline PASM2.", True),
    ("The drive ladder was fabricated and has been removed.", True),
    ("Until now the KB carried no write-side figure.", True),
    ("The 300 mA figure is not restored here.", True),
    ("Added 2026-08-25 from the bench run.", True),
    ("It has been demoted to a stub on 2026-04-29.", True),
    # Ordinary technical prose sharing a word -- MUST NOT fire.
    ("Restores the previously configured mode on exit.", False),
    ("The carry is added to the accumulator each cycle.", False),
    ("Continue a task that was previously halted with TASKHALT.", False),
    ("Z is set if Z was previously set and the result is zero.", False),
    ("The clock stays stopped until the next reset.", False),
    ("The C flag is not restored by RETI.", False),
    ("An earlier version of PNut accepted this form.", False),
    ("Released 2026-05-07 as v55.", False),
]


def history_prose_negative_control():
    """Return the control cases that misbehave (empty list == control passes)."""
    return [(text, want) for text, want in HISTORY_PROSE_CONTROL
            if bool(history_prose_hits(text)) != want]


def validate_history_prose(verbose: bool = False) -> ValidationResult:
    """No change-history prose in shipped YAML values (#422, 2026-10-10).

    Reads the PAYLOAD the consumer receives (the shipped filter's own output), parses
    it, and tests every string value -- comments are excluded because a parsed tree
    has none. Its negative control runs first: a check that cannot fire is not run."""
    result = ValidationResult("Change-History Prose in Shipped Content")
    bad_control = history_prose_negative_control()
    if bad_control:
        result.fail(f"negative control FAILED on {len(bad_control)} case(s) -- do not trust this run")
        for text, want in bad_control:
            result.info(f"  must_fire={want}: {text}")
        return result
    result.ok(f"Negative control: {sum(w for _, w in HISTORY_PROSE_CONTROL)} edit-note shapes fire, "
              f"{sum(not w for _, w in HISTORY_PROSE_CONTROL)} ordinary sentences do not")

    live, shipped = _shipped_payload()
    hits = []
    for _, path in live:
        try:
            doc = yaml.safe_load(shipped[str(path)])
        except yaml.YAMLError:
            continue                    # a payload that does not parse is Metadata Filter's finding
        for key, value in _walk_string_values(doc):
            for name, text in history_prose_hits(value):
                hits.append(f"{path} [{key}] {name}: {text!r}")

    result.info(f"Files checked (shipped payload): {len(live)}")
    if hits:
        result.fail(f"{len(hits)} change-history phrase(s) in shipped content -- state the fact; "
                    f"the edit history belongs in the register entry or a YAML comment")
        for h in hits:
            result.info(f"  {h}")
    else:
        result.ok("No change-history prose reaches a consumer")
    return result


LEDGERS = [
    Path("engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md"),
    Path("engineering/ingestion/external-sources/hardware-verification/EXTERNAL-HARDWARE-FINDINGS.md"),
    # «#412» (Q12): the compile-proof register is the second self-created citation
    # the sourcing gate accepts, so its `### CP-NNN` entries carry the same
    # `*KB:*` home line and are checked the same way.
    Path("engineering/ingestion/external-sources/compiler-verification/COMPILE-PROOFS.md"),
]
LEDGER_ENTRY = re.compile(r'^### ((?:EF|XF|CP)-\d{3})\b')
NOT_A_KB_FACT = re.compile(r'not a KB fact\s*[—-]\s*\S')


def validate_ledger_kb_home(verbose: bool = False) -> ValidationResult:
    """Every bench entry says where its fact lives in the KB (2026-10-03, «#375»).

    The bench audit of 2026-10-03 found that the ledger could not answer "did this
    reach the KB?" for two-thirds of its entries: only 28 of 84 named a YAML in
    their Grounds line, and the answer had to be rebuilt by reading the whole KB.
    So the line directly under each `### EF-NNN` / `### XF-NNN` heading is
    `*KB:*` followed by the YAML path(s) (in backticks, relative to
    deliverables/ai/P2/) or `not a KB fact — <reason>`. This fails on an entry
    without one and on a named path that does not exist. A new bench result is not
    finished until this line names where it was written.
    """
    result = ValidationResult("Bench Ledger + Compile Proofs -> KB Home")
    problems, entries = [], 0
    for ledger in LEDGERS:
        lines = ledger.read_text(encoding="utf-8").split("\n")
        for i, line in enumerate(lines):
            m = LEDGER_ENTRY.match(line)
            if not m:
                continue
            entries += 1
            where = f"{ledger.name}:{i + 1} {m.group(1)}"
            nxt = next((l for l in lines[i + 1:] if l.strip()), "")
            if not nxt.startswith("*KB:*"):
                problems.append(f"{where}: no `*KB:*` line under the heading")
                continue
            body = nxt[len("*KB:*"):].strip()
            if body.startswith("not a KB fact"):
                if not NOT_A_KB_FACT.match(body):
                    problems.append(f"{where}: 'not a KB fact' needs '— <reason>'")
                continue
            paths = re.findall(r'`([^`]+\.yaml)`', body)
            if not paths:
                problems.append(f"{where}: `*KB:*` names no YAML path")
            problems += [f"{where}: {p} does not exist" for p in paths
                         if not (YAML_BASE / p).is_file()]
    result.info(f"Ledger entries checked: {entries}")
    if problems:
        result.fail(f"{len(problems)} ledger entr(y/ies) without a valid KB home")
        for p in problems:
            result.info(f"  {p}")
    else:
        result.ok("Every bench and compile-proof entry names where its fact lives "
                  "(or why it is not a KB fact)")
    return result


def validate_cross_references(verbose: bool = False) -> ValidationResult:
    """Run cross-reference validation script."""
    result = ValidationResult("Cross-References")

    script_path = Path("engineering/tools/validate-crossref-keys.py")
    if not script_path.exists():
        result.fail(f"Validation script not found: {script_path}")
        return result

    try:
        proc = subprocess.run(
            ['python3', str(script_path)],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Parse output for resolution rate. A MISSING rate line is a failure,
        # not a pass: a validator that printed no measurement audited nothing,
        # and "nothing audited" reading as green is the digit-density lesson.
        rate_seen = False
        for line in proc.stdout.split('\n'):
            if 'Resolution rate' in line:
                rate_seen = True
                result.info(line.strip())
                if '100.0%' in line:
                    # F-340/F-373 closed 2026-09-13: the validator now reads every
                    # string (KB path tokens) and every reference field at every
                    # depth, so 100% is a statement about ALL references.
                    result.ok("All cross-references resolve (every string, every reference field, every depth)")
                else:
                    result.fail("Some cross-references failed to resolve")
                break
            if 'SCOPE:' in line:
                result.info(line.strip())
        if not rate_seen:
            result.fail("Cross-reference validator printed no resolution rate — "
                        "nothing audited, which is not a pass")

        # A gate must be shown able to fail: plant one defect of every kind it
        # claims to catch, and require each to be caught.
        nc = subprocess.run(['python3', str(script_path), '--negative-control'],
                            capture_output=True, text=True, timeout=120)
        if nc.returncode == 0 and 'NEGATIVE CONTROL: PASS' in nc.stdout:
            result.ok("Cross-reference negative control: every planted defect caught")
        else:
            result.fail("Cross-reference negative control FAILED — the gate cannot see a defect it claims to catch")
            for line in nc.stdout.split('\n'):
                if 'FAIL' in line:
                    result.info(line.strip())

        if proc.returncode != 0 and 'Resolution rate: 100.0%' not in proc.stdout:
            result.fail("Cross-reference validation failed")
            if verbose:
                for line in proc.stdout.split('\n')[-10:]:
                    if line.strip():
                        result.info(line)
    except subprocess.TimeoutExpired:
        result.fail("Validation script timed out")
    except Exception as e:
        result.fail(f"Failed to run validation: {e}")

    return result


def _run_gate(result: ValidationResult, script: Path, args: List[str],
              label: str, verbose: bool, timeout: int = 300) -> None:
    """Run one instrument and let its EXIT STATUS decide the release.

    Three outcomes, and the third is the one that has to be spelled out:
      0  -> pass
      1  -> Tier 1 violations; the release FAILS
      2+ -> the tool could not audit (no truth table, KB tree missing, crash).
            THAT ALSO FAILS. "Nothing audited" is never a pass -- the standing
            lesson from the digit-density gate, which shipped able to exit 0
            having measured nothing at all. A gate must read the artifact.
    """
    if not script.exists():
        result.fail(f"{label}: instrument not found at {script}")
        return
    try:
        proc = subprocess.run(['python3', str(script)] + args,
                              capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        result.fail(f"{label}: timed out — nothing audited, which is not a pass")
        return
    except Exception as e:                                   # noqa: BLE001
        result.fail(f"{label}: failed to run ({e}) — nothing audited, not a pass")
        return

    tail = [ln for ln in proc.stdout.strip().split('\n') if ln.strip()]
    # The VERDICT line, not the last line. Both instruments print a scope note
    # after their verdict — deliberately, so a green never reads as a guarantee —
    # and reporting the last line would surface the note's final sentence as the
    # gate's result. A summary must quote the measurement, not whatever printed
    # most recently.
    verdict = next((ln.strip() for ln in reversed(tail)
                    if ln.strip().startswith(("PASS", "FAIL", "ERROR",
                                              "Negative control"))), None)
    if proc.returncode == 0:
        result.ok(f"{label}: {verdict or 'exit 0'}")
        if verbose:
            for ln in tail[-6:]:
                result.info(ln.strip())
        return

    if proc.returncode == 1:
        result.fail(f"{label}: {verdict or 'exit 1'}")
    else:
        result.fail(f"{label}: exited {proc.returncode} — the instrument could "
                    f"not audit. Nothing audited is never a pass.")
    for ln in tail[-15:]:
        result.info(ln.strip())
    if proc.stderr.strip():
        for ln in proc.stderr.strip().split('\n')[-5:]:
            result.info(ln.strip())


def validate_constant_fidelity(verbose: bool = False) -> ValidationResult:
    """BLOCKING. Does the KB's description of a named constant match the source's?

    No grandfathered baseline and no tolerance value: the purge removed the
    existing population first, so there is nothing to tolerate. A Tier 1
    violation fails the release, on the first one.

    The `--negative-control` run is part of the gate, not a nicety. A check that
    cannot fail has not been verified, it has been RUN -- so the release proves
    the instrument still discriminates before it trusts the instrument's pass.
    """
    result = ValidationResult("Constant Fidelity (P_* named constants)")
    script = Path("engineering/tools/validation/audit-constant-fidelity.py")
    _run_gate(result, script, ['--negative-control'], "negative control", verbose)
    _run_gate(result, script, [], "audit", verbose)
    result.info("Scope: NAMED CONSTANTS only. Prose that describes a behaviour "
                "without naming one passes untouched.")
    return result


def validate_claim_sourcing(verbose: bool = False) -> ValidationResult:
    """BLOCKING. Does a quantitative claim in the shipped KB say where it came from?

    Tier 1 only — a block carrying physical quantities inside a file that
    demonstrably knows the citing convention, so the file's own other sections
    are the control. Tier 2 (a file that cites nothing anywhere) stays advisory
    and does NOT block; its population is not zero and the tool prints it.
    """
    result = ValidationResult("Claim Sourcing (quantitative claims)")
    script = Path("engineering/tools/validation/audit-yaml-claim-sourcing.py")
    _run_gate(result, script, ['--negative-control'], "negative control", verbose)
    _run_gate(result, script, [], "audit", verbose)
    result.info("Scope: QUANTITATIVE CLAIMS only, and only that a citation is "
                "PRESENT — nothing here reads the cited document.")
    return result


def validate_kb_code_compiles(verbose: bool = False) -> ValidationResult:
    """BLOCKING (ENH-03). Does every code block in the shipped KB compile in its
    declared context?

    Every candidate block carries a reviewed class in the sidecar manifest
    (`kb-compile-manifest/`): program, fragment, never (asserted to FAIL at its
    line) or not-code (with a reason). A block that fails its class, an
    unclassified block, a stale fingerprint or an orphan entry all fail the
    release. A failing block that names its finding is still a failure: the
    finding is reported, it never changes the verdict.

    Timeout: a full sweep measured 27 s wall on 24 cores (about 520 s of CPU),
    2026-10-09, «#404». 900 s covers a single-core run of that CPU time with
    headroom; the inherited 300 s would not.
    """
    result = ValidationResult("KB Code Compiles (ENH-03 compile gate)")
    script = Path("engineering/tools/validation/audit-kb-code-compiles.py")
    _run_gate(result, script, ['--negative-control'], "negative control", verbose)
    _run_gate(result, script, [], "audit", verbose, timeout=900)
    result.info("Scope: LEGALITY ONLY. A pass means pnut-ts accepts each block in "
                "its declared context — not that the code does what its text says, "
                "and not that any P2 fact in it is right.")
    return result


def validate_source_lock(verbose: bool = False) -> ValidationResult:
    """ADVISORY (ratchet). Is every claim-bearing shipped YAML locked to a source
    that can still be FOLLOWED — and has that lock got worse since the baseline?

    This is the companion to the claim-sourcing gate above, and it exists because
    that gate answers a deliberately narrow question: is a citation PRESENT on a
    quantitative block. Presence is not correctness. `source: enhanced` satisfies
    presence while naming no document, which is how F-348's pin-current limit —
    five times the datasheet's absolute maximum — survived two purges wearing a
    citation.

    So this gate tiers provenance by how far it can be followed (RESOLVABLE /
    NAMED / WEAK / ABSENT) and runs as a RATCHET against a recorded baseline: it
    blocks a REGRESSION, not the standing backlog. A gate that is permanently red
    over ~44% of the set would be a gate people learn to scroll past, and the
    backlog is the study's job to shrink, not this gate's job to shout about.
    """
    result = ValidationResult("Golden-source lock (ratchet vs baseline)")
    script = Path("engineering/tools/validation/audit-yaml-source-lock.py")
    baseline = Path("engineering/tools/validation/baselines/yaml-source-lock.json")
    if baseline.exists():
        _run_gate(result, script, ['--baseline', str(baseline)], "regression gate", verbose)
    else:
        result.info(f"no baseline at {baseline} — reporting only; "
                    f"record one with --write-baseline to arm the ratchet")
        _run_gate(result, script, [], "report", verbose)
    result.info("Scope: can the citation be FOLLOWED. Complements claim-sourcing, "
                "which asks only whether one is PRESENT.")
    return result


def validate_duplicate_keys(verbose: bool = False) -> ValidationResult:
    """BLOCKING. Does any shipped YAML mapping carry the same key twice?

    `yaml.safe_load` keeps the LAST occurrence of a duplicate key and discards
    the first silently — no parse error, no warning. F-360 lost a corrective
    sentence to exactly this on 2026-08-25 while every other gate stayed
    green. This walks the composed node tree, not the loaded object, because
    by the time you have a dict the evidence is already gone.
    """
    result = ValidationResult("Duplicate YAML Keys")
    script = Path("engineering/tools/validation/audit-yaml-duplicate-keys.py")
    _run_gate(result, script, ['--negative-control'], "negative control", verbose)
    _run_gate(result, script, [], "audit", verbose)
    result.info("Scope: DUPLICATE MAPPING KEYS only. A file free of them can "
                "still be wrong in every other way.")
    return result


def validate_adc_encoding(verbose: bool = False) -> ValidationResult:
    """BLOCKING. Does the shipped ADC X[5:4] sub-mode map still match silicon?

    F-170: this four-row map was inverted for 6.5 months because no checklist
    read it, and the defect survived a downstream-only fix. The instrument
    existed from 2026-06-28 and nothing in the repo ever ran it — it was the
    only gate `audit-gate-arming.py` reported UNWIRED — so a re-inversion today
    would have turned nothing red. Wired here «#346», 2026-09-21.

    Its `--negative-control` mutates a scratch copy per limb and asserts each
    verdict, including the case that must stay GREEN: mode 11010's X[1:0]
    filter select uses the same `%NN` notation and is not an ADC sub-mode.
    """
    result = ValidationResult("ADC X[5:4] Sub-mode Encoding (F-170)")
    script = Path("engineering/tools/validation/audit-adc-encoding.py")
    _run_gate(result, script, ['--negative-control'], "negative control", verbose)
    _run_gate(result, script, [], "audit", verbose)
    result.info("Scope: the X[5:4] sub-mode map in the three published ADC "
                "YAMLs, against the Silicon Doc row. Nothing here reads the "
                "ingestion tree — that donor limb retired with the superseded "
                "smart-pins-catalog (see the instrument's header).")
    return result


def _two_phase_gate(title: str, script_name: str, scope: str, verbose: bool,
                    audit_args: List[str] = (), timeout: int = 120) -> ValidationResult:
    """Run a gate's --negative-control, then its audit, and record its scope note."""
    result = ValidationResult(title)
    script = Path("engineering/tools/validation") / script_name
    _run_gate(result, script, ['--negative-control'], "negative control", verbose, timeout=timeout)
    _run_gate(result, script, list(audit_args), "audit", verbose, timeout=timeout)
    result.info(scope)
    return result


def validate_plain_scalar_comment(verbose: bool = False) -> ValidationResult:
    """BLOCKING. Is any YAML plain scalar silently cut short by a same-line ` #` comment?

    S-200 / S-183: `- MOV reg, #42` is served as the scalar `MOV reg,` with the
    comment `#42`. Every other gate reads the parsed value, which looks fine. This
    reads the composed node tree and the source line. Measured 2.5 s wall on the
    1,129-file tree (2026-10-09, «#410»), so the 120 s timeout is ample.
    """
    return _two_phase_gate(
        "YAML Plain Scalar Cut By Comment (S-200)", "audit-yaml-plain-scalar-comment.py",
        "Scope: PLAIN scalars cut by a ` #` comment only. A quoted scalar "
        "that lost text, a flow `[a, b #c]` collection, or a `#` with no "
        "whitespace before it are outside the rule.", verbose)


def validate_index_integrity(verbose: bool = False) -> ValidationResult:
    """BLOCKING. Does the index agree with what is committed (F-441 / F-405)?

    sha256 limb: every entry's sha256 equals SHA-256 of `git show HEAD:<path>`; no
    HEAD-tracked YAML is missing from the index. fresh limb: the index equals a
    fresh regeneration at HEAD (clean tree only; with --post-commit a dirty tree
    is an error). gz limb: the .gz decompresses to the index's bytes.

    Timeout: the fresh limb clones the repo and runs the generator. Measured 22 s
    wall for the fresh limb alone on 2026-10-09 («#410»); 600 s is generous.
    """
    return _two_phase_gate(
        "Index Integrity vs Committed Blobs (F-441/F-405)", "audit-index-integrity.py",
        "Scope: the index's sha256/freshness/.gz against git. Not the "
        "CONTENT of any entry, not the published tree, not findability.", verbose,
        audit_args=['--post-commit'] if '--post-commit' in sys.argv else [], timeout=600)


def validate_hardware_revision_scope(verbose: bool = False) -> ValidationResult:
    """BLOCKING. Is a rating in a revision-declaring hardware YAML stated with its board revision?

    F-454 / S-386: a correct current-revision number stripped of the scope that
    made it correct (Rev A/B VIN max 5.5 V; Rev C+ 16 V). The gate cannot judge
    the number; it enforces that the decision is made and recorded.
    """
    return _two_phase_gate(
        "Hardware Revision Scope (F-454)", "audit-hardware-revision-scope.py",
        "Scope: that a scope decision is recorded and ratings are "
        "qualified; NOT that any rating is right for its revision.", verbose)


def validate_index_findability(verbose: bool = False) -> ValidationResult:
    """BLOCKING. Does a directory's own name reach all of its files, or only some (F-389)?

    Reads the regenerated index (key + aliases + category names). A partial-reach
    directory not in the reviewed baseline fails. Reached-by-none directories are
    advisory (structural).
    """
    return _two_phase_gate(
        "Index Findability by Directory Term (F-389)", "audit-index-findability.py",
        "Scope: path-term reachability only; a vocabulary gap (a query "
        "no alias answers) is invisible to it.", verbose)


def validate_fetch_script_parity(verbose: bool = False) -> ValidationResult:
    """Verify bash and PowerShell scripts have matching behavior."""
    result = ValidationResult("Fetch Script Parity")

    bash_path = Path("engineering/tools/p2kb/fetch-kb-file.sh")
    ps_path = Path("engineering/tools/p2kb/fetch-kb-file.ps1")

    if not bash_path.exists():
        result.fail(f"Bash script not found: {bash_path}")
        return result
    if not ps_path.exists():
        result.fail(f"PowerShell script not found: {ps_path}")
        return result

    with open(bash_path) as f:
        bash_content = f.read()
    with open(ps_path) as f:
        ps_content = f.read()

    # Check version numbers match
    bash_version = re.search(r'v(\d+\.\d+)', bash_content)
    ps_version = re.search(r'v(\d+\.\d+)', ps_content)

    if bash_version and ps_version:
        if bash_version.group(1) == ps_version.group(1):
            result.ok(f"Version match: v{bash_version.group(1)}")
        else:
            result.fail(f"Version mismatch: bash={bash_version.group(1)}, ps={ps_version.group(1)}")

    # The scripts' BUILT-IN rule (used without jq, or when the index has no usable
    # block) must be the published rule exactly -- read from the script by running
    # it, never by spotting field names in its text.
    rule, problem = index_filter_rule()
    if rule is None:
        result.fail(f"Cannot compare built-in rules: {problem}")
    else:
        sh = bash_content[bash_content.index("filter_metadata() {"):]
        sh = sh[:sh.index("\n}\n") + 3]
        proc = subprocess.run(["bash", "-c", sh + "\nfilter_metadata --builtin-fields"],
                              capture_output=True, text=True)
        builtin = proc.stdout.split(',') if proc.returncode == 0 else []
        if builtin == rule['remove_fields'] and rule['remove_column0_comments'] is True:
            result.ok(f"bash built-in rule equals the index rule ({len(builtin)} fields, column-0 comments)")
        else:
            result.fail(f"bash built-in rule {builtin} differs from the index rule {rule['remove_fields']}")
        # PowerShell cannot run here; its built-in list sits between fixed markers.
        block = re.search(r'# BEGIN BUILTIN-RULE(.*?)# END BUILTIN-RULE', ps_content, re.S)
        ps_builtin = re.findall(r'"([^"]+)"', block.group(1)) if block else []
        ps_col0 = bool(re.search(r'Column0 = \$true', ps_content))
        if ps_builtin == rule['remove_fields'] and ps_col0 and rule['remove_column0_comments'] is True:
            result.ok(f"PowerShell built-in rule equals the index rule ({len(ps_builtin)} fields)")
        else:
            result.fail(f"PowerShell built-in rule {ps_builtin} differs from the index rule")

    # Check same base URL
    if 'ironsheep/P2-Knowledge-Base' in bash_content and \
       'ironsheep/P2-Knowledge-Base' in ps_content:
        result.ok("Base URLs match")
    else:
        result.fail("Base URLs do not match")

    # Check same cache age
    if '86400' in bash_content and '86400' in ps_content:
        result.ok("Cache max age matches (86400s)")
    else:
        result.warn("Cache max age may differ")

    return result


FETCH_SH = Path("engineering/tools/p2kb/fetch-kb-file.sh")


def _fetch_sh_functions(*names: str) -> str:
    """The named top-level functions of fetch-kb-file.sh, as shell text, so a gate
    runs the script's own code rather than a model of it."""
    sh = FETCH_SH.read_text()
    out = []
    for name in names:
        start = sh.index(f"\n{name}() {{") + 1
        end = sh.index("\n}\n", start) + 3
        out.append(sh[start:end])
    return "\n".join(out)


def validate_filter_rule_readback(verbose: bool = False) -> ValidationResult:
    """fetch-kb-file.sh reads the published rule back out of the generated index.

    Agreement §8.3: the KB's own scripts must be able to read the rule it publishes.
    Runs the script's load_filter_rule and filter_rule_id (with jq) against the
    generated index and requires the same fields, flag and rule_id this validator
    computes. Without jq the script uses its built-in rule; the parity gate checks
    that one.
    """
    result = ValidationResult("Filter Rule Read-Back (fetch-kb-file.sh)")
    rule, problem = index_filter_rule()
    if rule is None:
        result.fail(problem)
        return result
    if subprocess.run(["bash", "-c", "command -v jq"], capture_output=True).returncode != 0:
        result.fail("jq is not installed here -- the read-back runs the script's jq path")
        return result
    driver = ("log() { :; }\nINDEX_FILE=\"$1\"\n"
              + _fetch_sh_functions("load_filter_rule", "sha256_hex", "filter_rule_id", "filter_metadata")
              + '\nload_filter_rule\nprintf "%s|%s|%s\\n" "$RULE_FIELDS" "$RULE_COL0" "$(filter_rule_id)"\n')
    proc = subprocess.run(["bash", "-c", driver, "bash", str(INDEX_PATH)],
                          capture_output=True, text=True)
    want = (f"{','.join(rule['remove_fields'])}|"
            f"{'true' if rule['remove_column0_comments'] else 'false'}|{filter_rule_id(rule)}")
    got = proc.stdout.strip()
    if got == want:
        result.ok(f"Script reads the index rule back: rule_id {filter_rule_id(rule)}")
    else:
        result.fail(f"Script read {got!r}; the index says {want!r}")
    return result


def validate_nojq_lookup(verbose: bool = False) -> ValidationResult:
    """Without jq, fetch-kb-file.sh resolves every key and alias as json.load does.

    jq is optional on users' machines; the script's no-jq reader depends on the
    layout the generator writes. A layout change that breaks it would otherwise
    fail only on machines without jq, silently. Runs the script's own lookup_key /
    lookup_alias with jq hidden from PATH (a directory of every PATH tool but jq),
    over every key and every alias of the generated index.
    """
    result = ValidationResult("No-jq Key/Alias Lookup (fetch-kb-file.sh)")
    with open(INDEX_PATH) as f:
        idx = json.load(f)
    keys, aliases = list(idx['files']), list(idx['aliases'])

    def expected_alias(a):                     # exact, then UPPER, then lower
        for v in (a, a.upper(), a.lower()):
            if v in idx['aliases']:
                return ','.join(idx['aliases'][v])
        return ''

    driver = ("log() { :; }\nerror() { :; }\nINDEX_FILE=\"$1\"\n"
              + _fetch_sh_functions("nojq_index", "json_escape", "to_upper", "to_lower",
                                    "lookup_key", "lookup_alias")
              + '\nwhile IFS= read -r n; do\n'
                '  if [[ $2 == key ]]; then printf "%s\\t%s\\n" "$n" "$(lookup_key "$n")"\n'
                '  else printf "%s\\t%s\\n" "$n" "$(lookup_alias "$n" | paste -sd, -)"; fi\n'
                'done\n')
    with tempfile.TemporaryDirectory() as bindir:
        for d in os.environ.get('PATH', '').split(':'):
            if not os.path.isdir(d):
                continue
            for name in os.listdir(d):
                target = os.path.join(bindir, name)
                if name != 'jq' and not os.path.exists(target):
                    os.symlink(os.path.join(d, name), target)
        env = dict(os.environ, PATH=bindir, LC_ALL='C.UTF-8', LANG='C.UTF-8')
        if subprocess.run(["bash", "-c", "command -v jq"], capture_output=True, env=env).returncode == 0:
            result.fail("could not hide jq from PATH for this check")
            return result
        problems = []
        for mode, names, want in (("key", keys, lambda k: idx['files'][k]['path']),
                                  ("alias", aliases, expected_alias)):
            proc = subprocess.run(["bash", "-c", driver, "bash", str(INDEX_PATH), mode],
                                  input="\n".join(names) + "\n", capture_output=True,
                                  text=True, env=env)
            got = dict(line.split("\t", 1) for line in proc.stdout.rstrip("\n").split("\n") if "\t" in line)
            problems += [f"{mode} {n!r}: got {got.get(n)!r}, want {want(n)!r}"
                         for n in names if got.get(n) != want(n)]
    result.info(f"Checked without jq: {len(keys)} keys, {len(aliases)} aliases")
    if problems:
        result.fail(f"{len(problems)} lookup(s) differ from json.load without jq")
        for p in problems:                         # every hit: a capped list reads like a clean one
            result.info(f"  {p}")
    else:
        result.ok("Every key and alias resolves without jq exactly as json.load reads it")
    return result


PS1_RECORD = Path("engineering/tools/p2kb/PS1-VERIFIED.md")
PS1_SCRIPTS = [Path("engineering/tools/p2kb/fetch-kb-file.ps1"),
               Path("engineering/tools/p2kb/refresh-kb.ps1")]


def validate_ps1_verified(verbose: bool = False) -> ValidationResult:
    """The PowerShell scripts as they stand were verified on Windows.

    They cannot run in this container (Stephen, 2026-10-07: one Windows run, as little
    as possible). verify-ps1-filter.ps1 prints each script's SHA-256 over its
    LF-normalized content; PS1-VERIFIED.md records them with the result. A .ps1 edited
    since its recorded PASS fails here until the check is run again. A rule change does
    not -- the rule comes from the index.
    """
    result = ValidationResult("PowerShell Filter Verified")
    record = PS1_RECORD.read_text() if PS1_RECORD.exists() else ""
    if not re.search(r'^result: PASS\s*$', record, re.M):
        result.fail(f"{PS1_RECORD} records no PASS -- run verify-ps1-filter.ps1 on Windows and record it")
    for script in PS1_SCRIPTS:
        actual = hashlib.sha256(script.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        m = re.search(rf'^{re.escape(script.name)}: ([0-9a-f]{{64}})\s*$', record, re.M)
        if not m:
            result.fail(f"{script.name}: no verified hash recorded (current {actual})")
        elif m.group(1) != actual:
            result.fail(f"{script.name} changed since its Windows verification "
                        f"(recorded {m.group(1)[:12]}..., now {actual[:12]}...) -- re-run the check")
        else:
            result.ok(f"{script.name} is the version verified on Windows")
    return result


def run_all_validations(verbose: bool = False, incremental: bool = False) -> bool:
    """Run all validations and return overall pass/fail."""
    history = load_validation_history()

    print("=" * 70)
    print("P2 KNOWLEDGE BASE DOD RELEASE VALIDATION")
    print(f"Timestamp: {datetime.now().isoformat()}")

    # Show history info
    if history['last_run']:
        print(f"Last run: {history['last_run']} ({'PASSED' if history['last_run_passed'] else 'FAILED'})")

    # Check for changes if incremental mode
    if incremental and history['yaml_checksums']:
        new_files, modified_files, deleted_files = get_changed_yamls(history)
        total_changes = len(new_files) + len(modified_files) + len(deleted_files)

        if total_changes == 0:
            print("=" * 70)
            print("\n📋 INCREMENTAL MODE: No YAML changes detected since last run")
            print("   Use --full to force complete validation")
            print("\n✅ NO CHANGES - VALIDATION SKIPPED")
            print("=" * 70)
            return True

        print(f"\n📋 INCREMENTAL MODE: {total_changes} YAML change(s) detected")
        if new_files:
            print(f"   New files: {len(new_files)}")
            if verbose:
                for f in sorted(new_files)[:5]:
                    print(f"      + {f.name}")
        if modified_files:
            print(f"   Modified files: {len(modified_files)}")
            if verbose:
                for f in sorted(modified_files)[:5]:
                    print(f"      ~ {f.name}")
        if deleted_files:
            print(f"   Deleted files: {len(deleted_files)}")
            if verbose:
                for f in sorted(deleted_files)[:5]:
                    print(f"      - {f.name}")

    print("=" * 70)

    validations = [
        validate_index_structure,
        validate_gzip_compression,
        validate_file_paths,
        validate_orphaned_files,
        validate_key_naming,
        validate_timestamps,
        validate_metadata_filter,
        validate_internal_ids,
        validate_register_ids_in_values,
        validate_history_prose,
        validate_ledger_kb_home,
        validate_cross_references,
        validate_constant_fidelity,
        validate_claim_sourcing,
        validate_kb_code_compiles,
        validate_source_lock,
        validate_duplicate_keys,
        validate_adc_encoding,
        validate_plain_scalar_comment,
        validate_index_integrity,
        validate_hardware_revision_scope,
        validate_index_findability,
        validate_fetch_script_parity,
        validate_filter_rule_readback,
        validate_nojq_lookup,
        validate_ps1_verified,
    ]

    all_passed = True

    for validate_fn in validations:
        print(f"\n{'─' * 50}")
        result = validate_fn(verbose)

        # Print header with pass/fail
        status = "PASS" if result.passed else "FAIL"
        status_symbol = "✅" if result.passed else "❌"
        print(f"{status_symbol} {result.name}: {status}")

        # Print messages
        for msg in result.messages:
            print(f"   {msg}")
        for warn in result.warnings:
            print(f"   {warn}")

        if not result.passed:
            all_passed = False

    print(f"\n{'=' * 70}")
    if all_passed:
        print("✅ ALL VALIDATIONS PASSED - READY FOR RELEASE")
    else:
        print("❌ VALIDATION FAILURES - DO NOT RELEASE")
    print("=" * 70)

    # Update history
    history['last_run'] = datetime.now().isoformat()
    history['last_run_passed'] = all_passed
    update_history_checksums(history)

    # Keep last 10 runs in history
    history['runs'].append({
        'timestamp': history['last_run'],
        'passed': all_passed,
        'yaml_count': len(history['yaml_checksums'])
    })
    history['runs'] = history['runs'][-10:]

    save_validation_history(history)
    print(f"\n📝 Validation history saved to {HISTORY_FILE}")

    return all_passed


def main():
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    incremental = '--incremental' in sys.argv
    force_full = '--full' in sys.argv

    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    # --full overrides --incremental
    if force_full:
        incremental = False

    passed = run_all_validations(verbose, incremental)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()

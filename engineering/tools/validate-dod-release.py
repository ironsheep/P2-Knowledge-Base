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
    --help, -h        Show this help

Exit codes:
    0 = All validations passed
    1 = Validation failures found
"""

import json
import re
import sys
import gzip
import subprocess
from pathlib import Path
from collections import Counter
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set

# Configuration
INDEX_PATH = Path("deliverables/ai/p2kb-index.json")
INDEX_GZ_PATH = Path("deliverables/ai/p2kb-index.json.gz")
YAML_BASE = Path("deliverables/ai/P2")
HISTORY_FILE = Path("engineering/tools/.dod-validation-history.json")

# Metadata filter pattern (must match fetch scripts exactly)
# Update this if fetch scripts change!
FILTER_PATTERN = re.compile(
    r'^\s*(last_updated|enhancement_source|documentation_source|documentation_level|manual_extraction_date):'
)

# Expected metadata fields that get filtered
EXPECTED_FILTER_FIELDS = {
    'last_updated',
    'enhancement_source',
    'documentation_source',
    'documentation_level',
    'manual_extraction_date'
}


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

    for key in idx['files'].keys():
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


def validate_metadata_filter(verbose: bool = False) -> ValidationResult:
    """Comprehensive audit of metadata filtering."""
    result = ValidationResult("Metadata Filter")

    with open(INDEX_PATH) as f:
        idx = json.load(f)

    total_files = 0
    files_with_changes = 0
    field_removals = Counter()
    unexpected_changes = []

    for key, entry in idx['files'].items():
        path = Path(entry['path'])
        if not path.exists():
            continue

        total_files += 1

        with open(path) as f:
            original = f.read()

        # Apply filter
        lines = original.split('\n')
        filtered_lines = [l for l in lines if not FILTER_PATTERN.match(l)]
        filtered = '\n'.join(filtered_lines)

        if original != filtered:
            files_with_changes += 1

            original_lines = set(original.split('\n'))
            filtered_lines_set = set(filtered.split('\n'))
            removed_lines = original_lines - filtered_lines_set

            for line in removed_lines:
                line_stripped = line.strip()
                matched = False
                for field in EXPECTED_FILTER_FIELDS:
                    if line_stripped.startswith(f'{field}:'):
                        field_removals[field] += 1
                        matched = True
                        break
                if not matched:
                    unexpected_changes.append((key, line))

    result.info(f"Files analyzed: {total_files}")
    result.info(f"Files with metadata: {files_with_changes}")

    if verbose:
        for field, count in sorted(field_removals.items()):
            result.info(f"  {field}: {count} removals")

    if unexpected_changes:
        result.fail(f"{len(unexpected_changes)} unexpected line removals")
        for key, line in unexpected_changes[:5]:
            result.info(f"  {key}: {repr(line[:50])}")
    else:
        result.ok("All filtered lines are expected metadata fields")

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

        # Parse output for resolution rate
        for line in proc.stdout.split('\n'):
            if 'Resolution rate' in line:
                result.info(line.strip())
                if '100.0%' in line:
                    result.ok("All cross-references resolve")
                else:
                    result.fail("Some cross-references failed to resolve")
                break

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

    # Check same metadata fields filtered (must include all 5 fields)
    expected_fields = ['last_updated', 'enhancement_source', 'documentation_source',
                       'documentation_level', 'manual_extraction_date']

    bash_has_all = all(field in bash_content for field in expected_fields)
    ps_has_all = all(field in ps_content for field in expected_fields)

    if bash_has_all and ps_has_all:
        result.ok(f"Metadata filter patterns match ({len(expected_fields)} fields)")
    elif bash_has_all != ps_has_all:
        result.fail("Metadata filter fields differ between scripts")
    else:
        result.warn("Could not verify filter pattern match")

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
        validate_cross_references,
        validate_fetch_script_parity,
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

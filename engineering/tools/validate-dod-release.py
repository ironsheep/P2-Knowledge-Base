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

# Metadata filter pattern (must match fetch scripts exactly)
# Update this if fetch scripts change!
FILTER_PATTERN = re.compile(
    r'^\s*(last_updated|enhancement_source|documentation_source|documentation_level|'
    r'manual_extraction_date|source|sources|source_reference|verified_against):'
)

# Provenance written as a comment -- stripped by the same filter, for the same
# reason, and classified here so an expected removal is not reported as a surprise.
COMMENT_PROVENANCE_PATTERN = re.compile(r'^#\s*(Source|Sources|Extracted from|Verified against)')

# Expected metadata fields that get filtered
EXPECTED_FILTER_FIELDS = {
    'last_updated',
    'enhancement_source',
    'documentation_source',
    'documentation_level',
    'manual_extraction_date',
    # Added 2026-09-19: provenance is for this project's gates and auditors, never
    # for the consuming agent. `source` is the one that was actually reaching
    # consumers -- 177 files, 91 of them citing `engineering/` paths no consumer
    # has. Public citations go too: an agent cannot open the Silicon Doc either.
    'source',
    'sources',
    'source_reference',
    'verified_against',
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


def _predicted_filtered(original: str) -> str:
    """An INDEPENDENT prediction of what the shipped filter should produce.

    This is deliberately a second implementation of the same rule, and it is NOT
    used to build the payload -- `_apply_shipped_filter` does that, by running the
    real thing. This one exists so the two can be COMPARED: agreement between two
    independent readings is evidence, and a disagreement is a finding about one of
    them. What it must never become again is the single source of the answer, which
    is what let the Python line-model and the shipped filter drift apart.
    """
    lines = original.split('\n')
    kept = []
    dropping = False
    drop_indent = 0
    comment_drop = False
    for line in lines:
        if comment_drop:
            if re.match(r'^#\s+', line):
                continue
            comment_drop = False
        if dropping:
            if line.strip() == '':
                continue
            indent = len(line) - len(line.lstrip())
            if indent > drop_indent:
                continue
            dropping = False
        if COMMENT_PROVENANCE_PATTERN.match(line):
            comment_drop = True
            continue
        if FILTER_PATTERN.match(line):
            drop_indent = len(line) - len(line.lstrip())
            dropping = True
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
    `FILTER_PATTERN` is retained only to classify WHICH field a removed line
    belonged to, never to decide what gets removed.
    """
    sh = Path("engineering/tools/p2kb/fetch-kb-file.sh").read_text()
    start = sh.index("filter_metadata() {")
    end = sh.index("\n}\n", start) + 3
    delim = "@@P2KB-FILTER-DELIM@@"
    driver = sh[start:end] + f'\nfor f in "$@"; do echo "{delim}$f"; filter_metadata < "$f"; done\n'
    proc = subprocess.run(["bash", "-c", driver, "bash"] + [str(x) for x in paths],
                          capture_output=True, text=True)
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


def validate_metadata_filter(verbose: bool = False) -> ValidationResult:
    """Comprehensive audit of metadata filtering."""
    result = ValidationResult("Metadata Filter")

    with open(INDEX_PATH) as f:
        idx = json.load(f)

    total_files = 0
    files_with_changes = 0
    field_removals = Counter()
    unexpected_changes = []
    structural_failures = []

    live = [(key, Path(entry['path'])) for key, entry in idx['files'].items()
            if Path(entry['path']).exists()]
    shipped = _apply_shipped_filter([p for _, p in live])

    for key, path in live:
        total_files += 1

        with open(path) as f:
            original = f.read()

        # The payload the consumer actually receives, produced by the shipped
        # filter itself rather than a Python model of it.
        filtered = shipped[str(path)]

        if original != filtered:
            files_with_changes += 1

            # Did the shipped filter remove exactly what this project intends it
            # to remove? Compared against an independent prediction, not against a
            # line-by-line heuristic -- a block scalar's continuation lines are a
            # legitimate removal and a per-line classifier calls them a surprise.
            if filtered.rstrip('\n') != _predicted_filtered(original).rstrip('\n'):
                unexpected_changes.append(
                    (key, 'shipped filter and the expected rule disagree on this file'))

            for line in original.split('\n'):
                line_stripped = line.strip()
                if COMMENT_PROVENANCE_PATTERN.match(line):
                    field_removals['#provenance-comment'] += 1
                    continue
                for field in EXPECTED_FILTER_FIELDS:
                    if line_stripped.startswith(f'{field}:'):
                        field_removals[field] += 1
                        break

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
        for key, msg in structural_failures[:10]:
            result.info(f"  {key}: {msg}")
    else:
        result.ok("Filtered payload re-parses cleanly with no filter-induced null keys")

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
              label: str, verbose: bool) -> None:
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
                              capture_output=True, text=True, timeout=300)
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
    expected_fields = sorted(EXPECTED_FILTER_FIELDS)

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
        validate_constant_fidelity,
        validate_claim_sourcing,
        validate_duplicate_keys,
        validate_adc_encoding,
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

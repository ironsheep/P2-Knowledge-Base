#!/usr/bin/env python3
"""
Manifest Linkage Verification Tool for P2 Knowledge Base - Version 2.0

Enhanced validation with proper error classification and intelligent orphan detection.

Major improvements:
- Uses instruction_count/entry_count fields instead of directory file counts
- Validates category sums match totals
- Detects duplicate entries across categories
- Classifies orphans as ERRORS (real content) vs warnings (misplaced/obsolete)
- Better detection of what files actually are

Version: 2.0.0
Last Updated: 2025-09-26
"""

import os
import sys
import yaml
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Set

class Colors:
    """Terminal color codes for output formatting."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class EnhancedManifestVerifier:
    """Enhanced verifier with intelligent content classification."""
    
    def __init__(self, base_path: str, verbose: bool = False):
        self.base_path = Path(base_path)
        self.verbose = verbose
        self.errors = []  # Critical issues that MUST be fixed
        self.warnings = []  # Issues that should be addressed
        self.info = []  # Informational messages
        self.checked_count = 0
        self.manifest_count = 0
        self.referenced_files = set()
        self.orphaned_errors = []  # Real content not in manifests
        self.orphaned_warnings = []  # Misplaced or obsolete files
        self.category_totals = {}  # Track instruction counts per category
        self.duplicate_entries = []  # Files referenced in multiple categories
        
    def verify_all(self) -> bool:
        """Run complete verification suite."""
        print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}P2 KNOWLEDGE BASE - ENHANCED MANIFEST VERIFICATION v2.0{Colors.RESET}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 70}\n")
        
        # Define all manifests to check
        manifests = [
            ("Root Manifest", "manifests/p2-knowledge-root.yaml"),
            ("PASM2 Instructions", "manifests/pasm2-manifest.yaml"),
            ("Spin2 Language", "manifests/spin2-manifest.yaml"),
            ("Architecture", "manifests/architecture-manifest.yaml"),
            ("Smart Pins", "manifests/smart-pins-manifest.yaml"),
            ("Patterns", "manifests/patterns-manifest.yaml"),
            ("Hardware", "manifests/hardware-manifest.yaml"),
        ]
        
        # Verify each manifest
        for name, path in manifests:
            self._verify_manifest(name, path)
        
        # Special validation for hierarchical manifests
        self._validate_pasm2_hierarchy()
        self._validate_spin2_completeness()
        
        # Check for orphaned files with intelligent classification
        self._check_orphaned_files_smart()
        
        # Check for duplicates across categories
        self._check_for_duplicates()
        
        # Print summary
        self._print_summary()
        
        return len(self.errors) == 0
    
    def _verify_manifest(self, name: str, path: str, indent: int = 0) -> None:
        """Verify a single manifest file with enhanced checks."""
        self.manifest_count += 1
        indent_str = "  " * indent
        
        full_path = self.base_path / path
        
        if not full_path.exists():
            self.errors.append(f"Manifest not found: {path}")
            print(f"{indent_str}{Colors.RED}✗ {name}: Manifest not found{Colors.RESET}")
            return
            
        try:
            with open(full_path, 'r') as f:
                content = f.read()
                manifest = yaml.safe_load(content)
            
            base_path = manifest.get('base_path', '')
            
            # Handle hierarchical manifests (like PASM2)
            if manifest.get('structure') == 'hierarchical':
                self._process_hierarchical_manifest(name, path, manifest, indent)
                return
            
            # Find all file references
            file_refs = self._extract_file_references(content, manifest)
            
            if not file_refs:
                if self.verbose:
                    print(f"{indent_str}{Colors.YELLOW}⚠ {name}: No file references found{Colors.RESET}")
                return
            
            # Check files exist
            missing = []
            checked = 0
            
            for file_ref in file_refs:
                checked += 1
                self.checked_count += 1
                
                # Resolve file path
                if base_path:
                    expected = Path(base_path) / file_ref
                else:
                    expected = Path(file_ref)
                resolved = self.base_path / expected
                
                # Track referenced files
                if resolved.exists():
                    self.referenced_files.add(str(resolved.relative_to(self.base_path)))
                else:
                    missing.append(str(expected))
            
            # Report results
            if missing:
                self.errors.extend([f"{path}: Missing {f}" for f in missing])
                print(f"{indent_str}{Colors.RED}✗ {name}: {len(missing)} missing files{Colors.RESET}")
                for f in missing[:5]:
                    print(f"{indent_str}  {Colors.RED}  - {f}{Colors.RESET}")
            else:
                print(f"{indent_str}{Colors.GREEN}✓ {name}: All {checked} references valid{Colors.RESET}")
                
        except Exception as e:
            self.errors.append(f"{path}: Error - {e}")
            print(f"{indent_str}{Colors.RED}✗ {name}: Error - {e}{Colors.RESET}")
    
    def _process_hierarchical_manifest(self, name: str, path: str, manifest: dict, indent: int) -> None:
        """Process hierarchical manifest like PASM2 with category validation."""
        indent_str = "  " * indent
        categories = manifest.get('categories', {})
        total_claimed = manifest.get('total_instructions', 0) or manifest.get('total_entries', 0)
        
        print(f"{indent_str}{Colors.CYAN}Processing hierarchical: {name}{Colors.RESET}")
        
        category_sum = 0
        all_instructions = set()
        
        for cat_name, cat_data in categories.items():
            sub_manifest_path = cat_data.get('manifest', '')
            items = cat_data.get('items', [])
            expected_count = cat_data.get('count', 0)
            
            # Handle categories with 'items' (directives, constants, special_registers)
            if items:
                item_count = len(items)
                base_path = manifest.get('base_path', 'engineering/knowledge-base/P2/language/pasm2/')
                
                # Track referenced files from items
                for item in items:
                    if isinstance(item, dict) and 'file' in item:
                        file_path = Path(base_path) / item['file']
                        resolved = self.base_path / file_path
                        if resolved.exists():
                            self.referenced_files.add(str(resolved.relative_to(self.base_path)))
                        else:
                            self.errors.append(f"{cat_name}: Missing {item['file']}")
                
                print(f"{indent_str}  ✓ {cat_name}: {item_count} items")
                # Don't add to category_sum as these aren't instructions
                continue
            
            if sub_manifest_path:
                # Load and verify sub-manifest
                full_sub_path = self.base_path / 'manifests' / sub_manifest_path
                
                if full_sub_path.exists():
                    with open(full_sub_path, 'r') as f:
                        sub_content = f.read()
                        sub_manifest = yaml.safe_load(sub_content)
                    
                    # Get instruction count
                    instruction_count = sub_manifest.get('instruction_count', 0)
                    base_path = sub_manifest.get('base_path', '')
                    
                    # Count actual instructions listed
                    file_refs = self._extract_file_references(sub_content, sub_manifest)
                    actual_listed = len(file_refs)
                    
                    # Track for duplicates
                    for ref in file_refs:
                        full_ref = (Path(base_path) / ref) if base_path else Path(ref)
                        if str(full_ref) in all_instructions:
                            self.duplicate_entries.append({
                                'file': str(full_ref),
                                'category': cat_name,
                                'manifest': sub_manifest_path
                            })
                        all_instructions.add(str(full_ref))
                    
                    # Track files for orphan detection
                    for ref in file_refs:
                        if base_path:
                            full_path = self.base_path / base_path / ref
                            if full_path.exists():
                                self.referenced_files.add(str(full_path.relative_to(self.base_path)))
                    
                    # Validate counts
                    if instruction_count != expected_count:
                        self.warnings.append(
                            f"{sub_manifest_path}: Claims {instruction_count} but parent expects {expected_count}"
                        )
                    
                    if actual_listed != instruction_count:
                        self.warnings.append(
                            f"{sub_manifest_path}: Claims {instruction_count} but lists {actual_listed}"
                        )
                    
                    category_sum += instruction_count
                    self.category_totals[cat_name] = instruction_count
                    
                    print(f"{indent_str}  ✓ {cat_name}: {actual_listed}/{instruction_count} instructions")
                else:
                    self.errors.append(f"Sub-manifest not found: {sub_manifest_path}")
                    print(f"{indent_str}  {Colors.RED}✗ {cat_name}: Manifest not found{Colors.RESET}")
        
        # Validate total
        if category_sum != total_claimed:
            self.errors.append(
                f"{name}: Category sum ({category_sum}) doesn't match total ({total_claimed})"
            )
            print(f"{indent_str}{Colors.RED}✗ Sum mismatch: {category_sum} != {total_claimed}{Colors.RESET}")
        else:
            print(f"{indent_str}{Colors.GREEN}✓ Category sum correct: {category_sum}{Colors.RESET}")
    
    def _validate_pasm2_hierarchy(self) -> None:
        """Validate PASM2 instruction completeness and organization."""
        print(f"\n{Colors.CYAN}PASM2 Hierarchy Validation:{Colors.RESET}")
        
        # Load main PASM2 manifest
        pasm2_path = self.base_path / "manifests/pasm2-manifest.yaml"
        with open(pasm2_path) as f:
            pasm2_manifest = yaml.safe_load(f)
        
        total_instructions = pasm2_manifest.get('total_instructions', 0)
        
        # Sum categories
        category_sum = sum(self.category_totals.values())
        
        if category_sum == total_instructions:
            print(f"  {Colors.GREEN}✓ All {total_instructions} instructions accounted for{Colors.RESET}")
        else:
            diff = total_instructions - category_sum
            self.errors.append(f"PASM2: {diff} instructions not in any category")
            print(f"  {Colors.RED}✗ {diff} instructions missing from categories{Colors.RESET}")
        
        # Check for duplicates
        if self.duplicate_entries:
            print(f"  {Colors.RED}✗ {len(self.duplicate_entries)} duplicate entries found{Colors.RESET}")
            for dup in self.duplicate_entries[:3]:
                print(f"    - {dup['file']} in {dup['category']}")
    
    def _validate_spin2_completeness(self) -> None:
        """Validate Spin2 method and operator completeness."""
        print(f"\n{Colors.CYAN}Spin2 Completeness Check:{Colors.RESET}")
        
        spin2_path = self.base_path / "manifests/spin2-manifest.yaml"
        with open(spin2_path) as f:
            spin2_manifest = yaml.safe_load(f)
        
        total_entries = spin2_manifest.get('total_entries', 0)
        print(f"  Spin2 claims {total_entries} total entries")
    
    def _check_orphaned_files_smart(self) -> None:
        """Intelligently classify orphaned files as errors or warnings."""
        
        # Known instruction patterns
        pasm_instruction_pattern = re.compile(r'^[a-z]+[0-9]*$')  # abs, add, mov, etc
        spin_method_pattern = re.compile(r'^[a-z_]+$')  # strsize, bytemove, etc
        operator_pattern = re.compile(r'^op_')  # op_add, op_sub, etc
        
        directories = {
            "engineering/knowledge-base/P2/language/pasm2": "pasm",
            "engineering/knowledge-base/P2/language/spin2/methods": "method",
            "engineering/knowledge-base/P2/language/spin2/operators": "operator",
            "engineering/knowledge-base/P2/language/spin2/debug-commands": "debug",
            "engineering/knowledge-base/P2/architecture": "architecture",
            "engineering/knowledge-base/P2/architecture/smart-pins": "smartpin",
        }
        
        for dir_path, dir_type in directories.items():
            full_dir = self.base_path / dir_path
            if not full_dir.exists():
                continue
            
            yaml_files = list(full_dir.glob("*.yaml"))
            
            for yaml_file in yaml_files:
                relative_path = yaml_file.relative_to(self.base_path)
                if str(relative_path) not in self.referenced_files:
                    filename = yaml_file.stem  # without .yaml
                    
                    # Skip known non-content files
                    if filename in ['index', 'README', '_template', 'manifest']:
                        continue
                    
                    # Try to classify the file
                    is_error = False
                    classification = "unknown"
                    
                    # Read first few lines to determine content type
                    try:
                        with open(yaml_file, 'r') as f:
                            content = f.read(500)  # Read first 500 chars
                            
                        if dir_type == "pasm":
                            if 'instruction:' in content or 'opcode:' in content:
                                is_error = True
                                classification = "PASM instruction"
                            elif 'formatter' in content.lower():
                                classification = "Misplaced debug formatter"
                                
                        elif dir_type == "method":
                            if 'method:' in content or 'returns:' in content:
                                is_error = True
                                classification = "Spin2 method"
                                
                        elif dir_type == "operator":
                            if 'operator:' in content or 'precedence:' in content:
                                is_error = True
                                classification = "Spin2 operator"
                                
                        elif dir_type == "debug":
                            if 'formatter' in content or 'DEBUG' in content:
                                is_error = True
                                classification = "Debug formatter"
                                
                    except:
                        pass
                    
                    # Add to appropriate list
                    orphan_info = {
                        'path': str(relative_path),
                        'name': filename,
                        'type': classification
                    }
                    
                    if is_error:
                        self.orphaned_errors.append(orphan_info)
                    else:
                        self.orphaned_warnings.append(orphan_info)
    
    def _check_for_duplicates(self) -> None:
        """Check for entries that appear in multiple manifests."""
        # This is handled in _process_hierarchical_manifest
        pass
    
    def _extract_file_references(self, content: str, manifest: dict) -> List[str]:
        """Extract all file references from a manifest."""
        files = []
        
        # Parse YAML properly to avoid regex issues with quotes
        # Use yaml parsing for structured data
        def extract_from_dict(d):
            if isinstance(d, dict):
                for k, v in d.items():
                    if k == 'file' and isinstance(v, str):
                        files.append(v)
                    elif k == 'yaml_path' and isinstance(v, str):
                        files.append(v)
                    else:
                        extract_from_dict(v)
            elif isinstance(d, list):
                for item in d:
                    extract_from_dict(item)
        
        extract_from_dict(manifest)
        
        # Also use regex as fallback for non-structured content
        # But clean up any quotes that get included
        patterns = [
            re.compile(r'file:\s*["\']?([^"\',\s]+\.yaml)["\']?'),  # Handles quotes or no quotes
            re.compile(r'yaml_path:\s*["\']?([^"\',\s]+)["\']?'),  # yaml_path with optional quotes
        ]
        
        for pattern in patterns:
            matches = pattern.findall(content)
            for match in matches:
                # Clean any remaining quotes
                clean_match = match.strip('"\'')
                if clean_match not in files:
                    files.append(clean_match)
        
        return list(set(files))
    
    def _print_summary(self) -> None:
        """Print enhanced verification summary."""
        print(f"\n{'=' * 70}")
        print(f"{Colors.BOLD}VERIFICATION SUMMARY{Colors.RESET}")
        print(f"{'=' * 70}")
        
        print(f"Manifests checked: {self.manifest_count}")
        print(f"File references checked: {self.checked_count}")
        
        # Category totals
        if self.category_totals:
            print(f"\n{Colors.CYAN}PASM2 Category Breakdown:{Colors.RESET}")
            total = 0
            for cat, count in sorted(self.category_totals.items()):
                print(f"  {cat:20} : {count:3} instructions")
                total += count
            print(f"  {'TOTAL':20} : {total:3} instructions")
        
        # Duplicate entries
        if self.duplicate_entries:
            print(f"\n{Colors.RED}DUPLICATE ENTRIES ({len(self.duplicate_entries)}):{Colors.RESET}")
            print(f"{Colors.RED}Files referenced in multiple categories:{Colors.RESET}")
            for dup in self.duplicate_entries[:5]:
                print(f"  {Colors.RED}✗ {dup['file']} appears in {dup['category']}{Colors.RESET}")
        
        # Orphaned files - ERRORS (real content)
        if self.orphaned_errors:
            print(f"\n{Colors.RED}CRITICAL: ORPHANED CONTENT ({len(self.orphaned_errors)}):{Colors.RESET}")
            print(f"{Colors.RED}Real instructions/methods not in manifests:{Colors.RESET}")
            
            by_type = {}
            for orphan in self.orphaned_errors:
                t = orphan['type']
                if t not in by_type:
                    by_type[t] = []
                by_type[t].append(orphan['name'])
            
            for content_type, files in by_type.items():
                print(f"  {Colors.RED}{content_type} ({len(files)} files):{Colors.RESET}")
                for f in files[:5]:
                    print(f"    - {f}")
                if len(files) > 5:
                    print(f"    ... and {len(files)-5} more")
        
        # Orphaned files - WARNINGS (misplaced/unknown)
        if self.orphaned_warnings:
            print(f"\n{Colors.YELLOW}WARNING: QUESTIONABLE FILES ({len(self.orphaned_warnings)}):{Colors.RESET}")
            print(f"{Colors.YELLOW}Possibly misplaced or obsolete:{Colors.RESET}")
            for orphan in self.orphaned_warnings[:10]:
                print(f"  {Colors.YELLOW}⚠ {orphan['name']} - {orphan['type']}{Colors.RESET}")
        
        # Other errors
        if self.errors:
            print(f"\n{Colors.RED}ERRORS ({len(self.errors)}):{Colors.RESET}")
            for error in self.errors[:10]:
                print(f"  {Colors.RED}✗ {error}{Colors.RESET}")
        
        # Final verdict
        if self.errors or self.orphaned_errors:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ VERIFICATION FAILED - CRITICAL ISSUES{Colors.RESET}")
            print(f"{Colors.RED}Must fix all errors before release:{Colors.RESET}")
            if self.orphaned_errors:
                print(f"  - {len(self.orphaned_errors)} legitimate files not in manifests")
            if self.errors:
                print(f"  - {len(self.errors)} other critical errors")
        elif self.warnings or self.orphaned_warnings:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  VERIFICATION PASSED WITH WARNINGS{Colors.RESET}")
            print(f"{Colors.YELLOW}Should investigate warnings:{Colors.RESET}")
            if self.orphaned_warnings:
                print(f"  - {len(self.orphaned_warnings)} questionable files")
            if self.warnings:
                print(f"  - {len(self.warnings)} other warnings")
        else:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ PERFECT - ALL VALIDATIONS PASSED{Colors.RESET}")
            print(f"{Colors.GREEN}Knowledge base is complete and properly organized!{Colors.RESET}")
        
        print(f"\n{'=' * 70}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Enhanced manifest verification for P2 Knowledge Base'
    )
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed output')
    parser.add_argument('--ci', action='store_true',
                       help='CI mode - exit with error code')
    
    args = parser.parse_args()
    
    # Determine base path
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent.parent
    
    # Change to base directory
    os.chdir(base_path)
    
    # Run verification
    verifier = EnhancedManifestVerifier(base_path, verbose=args.verbose)
    
    try:
        success = verifier.verify_all()
        
        if args.ci:
            sys.exit(0 if success else 1)
            
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(2)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Manifest Linkage Verification Tool for P2 Knowledge Base

This script verifies all manifest linkages in the P2 Knowledge Base to ensure
referential integrity before releases. It checks that all files referenced in
manifests actually exist and reports any broken linkages.

Usage:
    python3 verify-manifest-linkages.py [--verbose] [--ci]
    
Options:
    --verbose  Show all checked files, not just errors
    --ci       Exit with error code if issues found (for CI/CD pipelines)
    
Exit codes:
    0 - All linkages valid
    1 - Broken linkages found
    2 - Script error

Author: P2 Knowledge Base Team
Version: 1.3.0
Last Updated: 2025-09-23
Changelog:
  1.3.0 - Added hierarchical manifest support
  1.2.0 - Added orphaned file detection (files not in manifests)
  1.1.0 - Added incomplete manifest detection (total_entries vs actual)
"""

import os
import sys
import yaml
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

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

class ManifestVerifier:
    """Verifies linkages in P2 Knowledge Base manifests."""
    
    def __init__(self, base_path: str, verbose: bool = False):
        """
        Initialize the verifier.
        
        Args:
            base_path: Root directory of the P2 Knowledge Base
            verbose: Show all checks, not just errors
        """
        self.base_path = Path(base_path)
        self.verbose = verbose
        self.issues = []
        self.warnings = []
        self.checked_count = 0
        self.manifest_count = 0
        self.incomplete_manifests = []
        self.referenced_files = set()  # Track all referenced files
        self.orphaned_files = []
        
    def verify_all(self) -> bool:
        """
        Verify all manifests in the knowledge base.
        
        Returns:
            True if all linkages are valid, False otherwise
        """
        print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}P2 KNOWLEDGE BASE - MANIFEST LINKAGE VERIFICATION{Colors.RESET}")
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
            ("Quick Queries", "manifests/quick-queries-manifest.yaml"),
            ("Obex Root", "manifests/obex/obex-root.yaml"),
        ]
        
        # Also check Obex category and author manifests
        obex_categories = self._find_obex_manifests("manifests/obex/categories")
        obex_authors = self._find_obex_manifests("manifests/obex/authors")
        
        # Verify each manifest
        for name, path in manifests:
            self._verify_manifest(name, path)
            
        # Verify Obex sub-manifests
        if obex_categories:
            print(f"\n{Colors.CYAN}Obex Category Manifests:{Colors.RESET}")
            for manifest in obex_categories:
                name = Path(manifest).stem
                self._verify_manifest(f"  {name}", manifest, indent=2)
                
        if obex_authors:
            print(f"\n{Colors.CYAN}Obex Author Manifests:{Colors.RESET}")
            # Sample check - don't check all 24 authors unless verbose
            sample_size = len(obex_authors) if self.verbose else min(3, len(obex_authors))
            for manifest in obex_authors[:sample_size]:
                name = Path(manifest).stem
                self._verify_manifest(f"  {name}", manifest, indent=2)
            if not self.verbose and len(obex_authors) > 3:
                print(f"  {Colors.WHITE}(Checked {sample_size} of {len(obex_authors)} author manifests){Colors.RESET}")
        
        # Check for orphaned files
        self._check_orphaned_files()
        
        # Print summary
        self._print_summary()
        
        return len(self.issues) == 0
    
    def _check_orphaned_files(self) -> None:
        """Check for YAML files that exist but aren't referenced in any manifest."""
        # Define directories to check for orphaned files
        directories_to_check = [
            "engineering/knowledge-base/P2/language/pasm2",
            "engineering/knowledge-base/P2/language/spin2/methods",
            "engineering/knowledge-base/P2/language/spin2/constructs",
            "engineering/knowledge-base/P2/language/spin2/operators",
            "engineering/knowledge-base/P2/architecture/smart-pins",
            "engineering/knowledge-base/P2/architecture",
            "engineering/knowledge-base/P2/hardware",
            "engineering/knowledge-base/P2/community/obex/objects"
        ]
        
        for dir_path in directories_to_check:
            full_dir = self.base_path / dir_path
            if not full_dir.exists():
                continue
                
            # Find all YAML files in directory
            yaml_files = list(full_dir.glob("*.yaml"))
            
            for yaml_file in yaml_files:
                relative_path = yaml_file.relative_to(self.base_path)
                if str(relative_path) not in self.referenced_files:
                    # Check if it's a special file we should ignore
                    filename = yaml_file.name
                    if filename in ['pattern-index.yaml', 'README.yaml', 'index.yaml']:
                        continue
                    
                    self.orphaned_files.append({
                        'path': str(relative_path),
                        'dir': dir_path,
                        'name': filename
                    })
    
    def _verify_manifest(self, name: str, path: str, indent: int = 0) -> None:
        """
        Verify a single manifest file.
        
        Args:
            name: Display name for the manifest
            path: Path to the manifest file
            indent: Indentation level for output
        """
        self.manifest_count += 1
        indent_str = "  " * indent
        
        full_path = self.base_path / path
        
        if not full_path.exists():
            self.issues.append(f"Manifest not found: {path}")
            print(f"{indent_str}{Colors.RED}✗ {name}: Manifest not found{Colors.RESET}")
            return
            
        try:
            with open(full_path, 'r') as f:
                content = f.read()
                manifest = yaml.safe_load(content)
            
            # Extract base path if specified
            base_path = manifest.get('base_path', '')
            
            # Check if this is a hierarchical manifest
            if manifest.get('structure') == 'hierarchical':
                # Process hierarchical manifest
                categories = manifest.get('categories', {})
                for cat_name, cat_data in categories.items():
                    sub_manifest_path = cat_data.get('manifest', '')
                    if sub_manifest_path:
                        # Verify sub-manifest
                        full_sub_path = Path('manifests') / sub_manifest_path
                        sub_name = f"{name}/{cat_name}"
                        self._verify_manifest(sub_name, str(full_sub_path), indent=indent+1)
                return
            
            # Find all file references
            file_refs = self._extract_file_references(content, manifest)
            
            if not file_refs:
                if self.verbose:
                    print(f"{indent_str}{Colors.YELLOW}⚠ {name}: No file references found{Colors.RESET}")
                return
            
            # Check for incomplete manifest (total_entries mismatch)
            if 'total_entries' in manifest:
                claimed_total = manifest.get('total_entries', 0)
                actual_refs = len(file_refs)
                if claimed_total > 0 and actual_refs < claimed_total * 0.5:  # Less than 50% listed
                    self.incomplete_manifests.append({
                        'path': path,
                        'name': name,
                        'claimed': claimed_total,
                        'actual': actual_refs,
                        'coverage': f"{(actual_refs/claimed_total*100):.1f}%"
                    })
            
            # Check for base_path directory existence
            if 'base_path' in manifest:
                base_dir = self.base_path / manifest['base_path']
                if base_dir.exists() and base_dir.is_dir():
                    # Count actual files in directory
                    actual_files = list(base_dir.glob('*.yaml'))
                    if len(actual_files) > len(file_refs) * 1.5:  # Many more files than referenced
                        if path not in [im['path'] for im in self.incomplete_manifests]:
                            self.incomplete_manifests.append({
                                'path': path,
                                'name': name,
                                'claimed': len(actual_files),
                                'actual': len(file_refs),
                                'coverage': f"{(len(file_refs)/len(actual_files)*100):.1f}%"
                            })
            
            # Check files
            missing = []
            checked = 0
            
            for file_ref in file_refs:
                checked += 1
                self.checked_count += 1
                
                # Resolve the file path
                if file_ref.startswith('../'):
                    # Relative to manifest location
                    resolved = (full_path.parent / file_ref).resolve()
                    expected = resolved.relative_to(self.base_path)
                else:
                    # Relative to base_path
                    expected = Path(base_path) / file_ref if base_path else Path(file_ref)
                    resolved = self.base_path / expected
                
                # Track referenced files for orphan detection
                if resolved.exists():
                    self.referenced_files.add(str(resolved.relative_to(self.base_path)))
                else:
                    missing.append(str(expected))
                    
            # Report results
            if missing:
                self.issues.extend([f"{path}: Missing {f}" for f in missing])
                print(f"{indent_str}{Colors.RED}✗ {name}: {len(missing)} missing files{Colors.RESET}")
                if self.verbose or len(missing) <= 5:
                    for f in missing[:5]:
                        print(f"{indent_str}  {Colors.RED}  - {f}{Colors.RESET}")
                    if len(missing) > 5:
                        print(f"{indent_str}  {Colors.RED}  ... and {len(missing)-5} more{Colors.RESET}")
            else:
                print(f"{indent_str}{Colors.GREEN}✓ {name}: All {checked} references valid{Colors.RESET}")
                
        except yaml.YAMLError as e:
            self.issues.append(f"{path}: YAML parse error - {e}")
            print(f"{indent_str}{Colors.RED}✗ {name}: YAML parse error{Colors.RESET}")
        except Exception as e:
            self.issues.append(f"{path}: Error - {e}")
            print(f"{indent_str}{Colors.RED}✗ {name}: Error - {e}{Colors.RESET}")
    
    def _extract_file_references(self, content: str, manifest: dict) -> List[str]:
        """
        Extract all file references from a manifest.
        
        Args:
            content: Raw manifest content
            manifest: Parsed manifest dictionary
            
        Returns:
            List of file paths referenced in the manifest
        """
        files = []
        
        # Method 1: Regex search for file: "..." patterns (with quotes)
        file_pattern = re.compile(r'file:\s*"([^"]+)"')
        files.extend(file_pattern.findall(content))
        
        # Method 1b: Regex search for file: ... patterns (without quotes)
        file_pattern_no_quotes = re.compile(r'file:\s+([\w.-]+\.yaml)')
        files.extend(file_pattern_no_quotes.findall(content))
        
        # Method 2: Look for yaml_path in Obex manifests
        yaml_path_pattern = re.compile(r'yaml_path:\s*([^\s]+)')
        files.extend(yaml_path_pattern.findall(content))
        
        # Method 3: Check specific manifest structures
        # This handles manifests that might have different formats
        if 'url' in manifest and isinstance(manifest['url'], str):
            # Don't add URLs as file references
            pass
            
        return list(set(files))  # Remove duplicates
    
    def _find_obex_manifests(self, directory: str) -> List[str]:
        """
        Find all YAML manifests in an Obex directory.
        
        Args:
            directory: Directory to search
            
        Returns:
            List of manifest file paths
        """
        dir_path = self.base_path / directory
        if not dir_path.exists():
            return []
            
        return [str(f.relative_to(self.base_path)) 
                for f in dir_path.glob("*.yaml")]
    
    def _print_summary(self) -> None:
        """Print verification summary."""
        print(f"\n{'=' * 70}")
        print(f"{Colors.BOLD}VERIFICATION SUMMARY{Colors.RESET}")
        print(f"{'=' * 70}")
        
        print(f"Manifests checked: {self.manifest_count}")
        print(f"File references checked: {self.checked_count}")
        
        if self.incomplete_manifests:
            print(f"\n{Colors.YELLOW}Incomplete Manifests ({len(self.incomplete_manifests)}):{Colors.RESET}")
            for im in self.incomplete_manifests:
                print(f"  ⚠ {im['name']}: Only {im['actual']} of {im['claimed']} entries listed ({im['coverage']})")
                print(f"    Path: {im['path']}")
                if self.verbose:
                    print(f"    This may prevent AI from discovering unlisted content")
        
        if self.orphaned_files:
            # Group orphaned files by directory
            by_dir = {}
            for of in self.orphaned_files:
                dir_name = of['dir']
                if dir_name not in by_dir:
                    by_dir[dir_name] = []
                by_dir[dir_name].append(of['name'])
            
            print(f"\n{Colors.YELLOW}Orphaned Files ({len(self.orphaned_files)}):{Colors.RESET}")
            print(f"{Colors.YELLOW}Files that exist but aren't referenced in any manifest:{Colors.RESET}")
            for dir_name, files in by_dir.items():
                print(f"  {dir_name}:")
                for f in files[:5]:  # Show first 5 per directory
                    print(f"    - {f}")
                if len(files) > 5:
                    print(f"    ... and {len(files) - 5} more")
        
        if self.warnings:
            print(f"\n{Colors.YELLOW}Warnings ({len(self.warnings)}):{Colors.RESET}")
            for warning in self.warnings[:10]:
                print(f"  ⚠ {warning}")
                
        if self.issues:
            print(f"\n{Colors.RED}Issues Found ({len(self.issues)}):{Colors.RESET}")
            for issue in self.issues[:20]:
                print(f"  ✗ {issue}")
            if len(self.issues) > 20:
                print(f"  ... and {len(self.issues) - 20} more issues")
                
            print(f"\n{Colors.RED}{Colors.BOLD}❌ VERIFICATION FAILED{Colors.RESET}")
            print(f"{Colors.YELLOW}Please fix the above issues before release.{Colors.RESET}")
        elif self.incomplete_manifests or self.orphaned_files:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  VERIFICATION PASSED WITH WARNINGS{Colors.RESET}")
            if self.incomplete_manifests:
                print(f"{Colors.YELLOW}Some manifests are incomplete - AI may not discover all content.{Colors.RESET}")
            if self.orphaned_files:
                print(f"{Colors.YELLOW}Some files exist but aren't referenced - AI cannot discover them.{Colors.RESET}")
        else:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ ALL MANIFEST LINKAGES VERIFIED SUCCESSFULLY!{Colors.RESET}")
            print(f"{Colors.GREEN}The knowledge base is ready for release.{Colors.RESET}")
        
        print(f"\n{'=' * 70}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Verify manifest linkages in P2 Knowledge Base'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show all checked files, not just errors'
    )
    parser.add_argument(
        '--ci',
        action='store_true',
        help='CI mode - exit with error code if issues found'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    args = parser.parse_args()
    
    # Disable colors if requested
    if args.no_color:
        for attr in dir(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')
    
    # Determine base path (script is in engineering/tools/)
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent.parent  # Go up to repo root
    
    # Change to base directory
    os.chdir(base_path)
    
    # Run verification
    verifier = ManifestVerifier(base_path, verbose=args.verbose)
    
    try:
        success = verifier.verify_all()
        
        if args.ci:
            sys.exit(0 if success else 1)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Verification interrupted by user{Colors.RESET}")
        sys.exit(2)
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {e}{Colors.RESET}")
        sys.exit(2)

if __name__ == '__main__':
    main()
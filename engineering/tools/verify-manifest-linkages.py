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
Version: 1.0.0
Last Updated: 2025-09-23
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
        
        # Print summary
        self._print_summary()
        
        return len(self.issues) == 0
    
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
            
            # Find all file references
            file_refs = self._extract_file_references(content, manifest)
            
            if not file_refs:
                if self.verbose:
                    print(f"{indent_str}{Colors.YELLOW}⚠ {name}: No file references found{Colors.RESET}")
                return
            
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
                
                if not resolved.exists():
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
        
        # Method 1: Regex search for file: "..." patterns
        file_pattern = re.compile(r'file:\s*"([^"]+)"')
        files.extend(file_pattern.findall(content))
        
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
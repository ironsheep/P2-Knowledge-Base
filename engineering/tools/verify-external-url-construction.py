#!/usr/bin/env python3
"""
External URL Construction Verification Tool

Validates that all manifest paths can be properly constructed into valid GitHub URLs
for external access. This ensures external Claude instances can traverse the entire
manifest hierarchy without encountering 404 errors.

Tests:
1. All manifests use proper path construction (no ../ paths)
2. base_path + file combinations create valid URLs
3. All referenced files are accessible via constructed URLs
4. No path traversal issues that would break external access
"""

import os
import sys
import yaml
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
import urllib.parse

class Colors:
    """Terminal color codes for output formatting."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class URLValidator:
    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.verbose = verbose
        self.base_url = "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/"
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.validated_urls: Set[str] = set()
        self.file_cache: Dict[str, bool] = {}  # Cache file existence checks
        
    def log_error(self, message: str):
        """Log an error message."""
        self.errors.append(message)
        print(f"{Colors.RED}✗{Colors.RESET} {message}")
        
    def log_warning(self, message: str):
        """Log a warning message."""
        self.warnings.append(message)
        print(f"{Colors.YELLOW}⚠{Colors.RESET} {message}")
        
    def log_success(self, message: str):
        """Log a success message."""
        if self.verbose:
            print(f"{Colors.GREEN}✓{Colors.RESET} {message}")
            
    def log_info(self, message: str):
        """Log an info message."""
        if self.verbose:
            print(f"{Colors.CYAN}ℹ{Colors.RESET} {message}")

    def validate_no_parent_traversal(self, path: str, context: str) -> bool:
        """Check that a path doesn't contain parent directory traversal."""
        if '../' in path or path.startswith('..'):
            self.log_error(f"{context}: Path contains parent traversal: {path}")
            return False
        return True

    def construct_url(self, base_path: str, file_path: str) -> str:
        """Construct a full URL from base_path and file_path."""
        # Clean up paths
        if base_path and not base_path.endswith('/'):
            base_path += '/'
        if file_path.startswith('/'):
            file_path = file_path[1:]
            
        full_url = self.base_url + base_path + file_path
        return full_url

    def validate_local_file_exists(self, relative_path: str) -> bool:
        """Check if a file exists locally (as a proxy for GitHub availability)."""
        if relative_path in self.file_cache:
            return self.file_cache[relative_path]
            
        full_path = self.repo_root / relative_path
        exists = full_path.exists()
        self.file_cache[relative_path] = exists
        return exists

    def validate_manifest_urls(self, manifest_path: Path) -> Tuple[int, int]:
        """Validate all URLs that would be constructed from a manifest."""
        valid_count = 0
        error_count = 0
        
        rel_path = manifest_path.relative_to(self.repo_root)
        self.log_info(f"Checking manifest: {rel_path}")
        
        try:
            with open(manifest_path, 'r') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            self.log_error(f"Failed to load manifest {rel_path}: {e}")
            return 0, 1
            
        # Extract base_path if present
        base_path = data.get('base_path', '')
        
        # Check for path_construction_note (good practice)
        if 'path_construction_note' in data:
            self.log_success(f"{rel_path} has path construction instructions")
        
        # Process different manifest structures
        
        # OBEX manifests with objects
        if 'objects' in data:
            for obj in data['objects']:
                if 'yaml_path' in obj:
                    yaml_path = obj['yaml_path']
                    object_id = obj.get('object_id', 'unknown')
                    
                    # Check for parent traversal
                    if not self.validate_no_parent_traversal(yaml_path, f"Object {object_id} in {rel_path}"):
                        error_count += 1
                        continue
                    
                    # Construct full URL
                    if base_path:
                        full_url = self.construct_url(base_path, yaml_path)
                        local_path = base_path + yaml_path
                    else:
                        # Without base_path, paths should be repo-relative
                        full_url = self.base_url + yaml_path
                        local_path = yaml_path
                    
                    # Validate file exists
                    if self.validate_local_file_exists(local_path):
                        self.log_success(f"Object {object_id}: {full_url}")
                        self.validated_urls.add(full_url)
                        valid_count += 1
                    else:
                        self.log_error(f"Object {object_id} file not found: {local_path}")
                        error_count += 1
        
        # Spin2/PASM2 manifests with by_category entries
        if 'by_category' in data:
            for category, items in data['by_category'].items():
                if isinstance(items, list):
                    for item in items:
                        if 'file' in item:
                            file_path = item['file']
                            name = item.get('name', 'unknown')
                            
                            if not self.validate_no_parent_traversal(file_path, f"Item {name} in {rel_path}"):
                                error_count += 1
                                continue
                            
                            if base_path:
                                full_url = self.construct_url(base_path, file_path)
                                local_path = base_path + file_path
                            else:
                                full_url = self.base_url + file_path
                                local_path = file_path
                            
                            if self.validate_local_file_exists(local_path):
                                self.log_success(f"Item {name}: {full_url}")
                                self.validated_urls.add(full_url)
                                valid_count += 1
                            else:
                                self.log_error(f"Item {name} file not found: {local_path}")
                                error_count += 1
                elif isinstance(items, dict):
                    # Handle nested structures
                    for subcategory, subitems in items.items():
                        if isinstance(subitems, list):
                            for item in subitems:
                                if 'file' in item:
                                    file_path = item['file']
                                    name = item.get('name', 'unknown')
                                    
                                    if not self.validate_no_parent_traversal(file_path, f"Item {name} in {rel_path}"):
                                        error_count += 1
                                        continue
                                    
                                    if base_path:
                                        full_url = self.construct_url(base_path, file_path)
                                        local_path = base_path + file_path
                                    else:
                                        full_url = self.base_url + file_path
                                        local_path = file_path
                                    
                                    if self.validate_local_file_exists(local_path):
                                        self.log_success(f"Item {name}: {full_url}")
                                        self.validated_urls.add(full_url)
                                        valid_count += 1
                                    else:
                                        self.log_error(f"Item {name} file not found: {local_path}")
                                        error_count += 1
        
        # Check sub-manifests references
        if 'sub_manifests' in data:
            sub = data['sub_manifests']
            if 'by_category' in sub and 'manifests' in sub['by_category']:
                for manifest_file in sub['by_category']['manifests']:
                    manifest_path_in_sub = sub['by_category'].get('path', '') + manifest_file
                    if not self.validate_no_parent_traversal(manifest_path_in_sub, f"Sub-manifest in {rel_path}"):
                        error_count += 1
                    else:
                        self.log_success(f"Sub-manifest reference OK: {manifest_path_in_sub}")
                        valid_count += 1
                        
            if 'by_author' in sub and 'manifests' in sub['by_author']:
                for manifest_file in sub['by_author']['manifests']:
                    manifest_path_in_sub = sub['by_author'].get('path', '') + manifest_file
                    if not self.validate_no_parent_traversal(manifest_path_in_sub, f"Sub-manifest in {rel_path}"):
                        error_count += 1
                    else:
                        self.log_success(f"Sub-manifest reference OK: {manifest_path_in_sub}")
                        valid_count += 1
        
        # Check categories with manifest references (like in pasm2-manifest.yaml)
        if 'categories' in data:
            for cat_name, cat_data in data['categories'].items():
                if isinstance(cat_data, dict) and 'manifest' in cat_data:
                    manifest_ref = cat_data['manifest']
                    if not self.validate_no_parent_traversal(manifest_ref, f"Category {cat_name} in {rel_path}"):
                        error_count += 1
                    else:
                        self.log_success(f"Category manifest reference OK: {manifest_ref}")
                        valid_count += 1
        
        return valid_count, error_count

    def validate_all_manifests(self) -> bool:
        """Validate URL construction for all manifests in the repository."""
        manifests_dir = self.repo_root / 'manifests'
        
        print(f"\n{Colors.BOLD}Validating External URL Construction{Colors.RESET}")
        print("=" * 60)
        print(f"Repository root: {self.repo_root}")
        print(f"Base URL: {self.base_url}")
        print("=" * 60 + "\n")
        
        # Find all manifest files
        manifest_files = []
        for yaml_file in manifests_dir.rglob('*.yaml'):
            # Skip backup files
            if '.backup' in str(yaml_file):
                continue
            manifest_files.append(yaml_file)
        
        manifest_files.sort()
        
        total_valid = 0
        total_errors = 0
        
        # Process root manifest first
        root_manifest = manifests_dir / 'p2-knowledge-root.yaml'
        if root_manifest.exists():
            print(f"{Colors.BOLD}Root Manifest:{Colors.RESET}")
            valid, errors = self.validate_manifest_urls(root_manifest)
            total_valid += valid
            total_errors += errors
            print()
        
        # Process other manifests
        print(f"{Colors.BOLD}Sub-Manifests:{Colors.RESET}")
        for manifest_path in manifest_files:
            if manifest_path == root_manifest:
                continue
            valid, errors = self.validate_manifest_urls(manifest_path)
            total_valid += valid
            total_errors += errors
            
        # Summary
        print("\n" + "=" * 60)
        print(f"{Colors.BOLD}VALIDATION SUMMARY{Colors.RESET}")
        print("=" * 60)
        
        print(f"Total manifests checked: {len(manifest_files)}")
        print(f"Total URLs validated: {len(self.validated_urls)}")
        print(f"Valid path constructions: {Colors.GREEN}{total_valid}{Colors.RESET}")
        
        if total_errors > 0:
            print(f"Path construction errors: {Colors.RED}{total_errors}{Colors.RESET}")
            print(f"\n{Colors.RED}✗ VALIDATION FAILED{Colors.RESET}")
            print("\nErrors found:")
            for error in self.errors[:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more errors")
        else:
            print(f"\n{Colors.GREEN}✓ ALL URL CONSTRUCTIONS VALID{Colors.RESET}")
            print("External systems should be able to traverse all manifests successfully.")
        
        if self.warnings:
            print(f"\n{Colors.YELLOW}Warnings:{Colors.RESET}")
            for warning in self.warnings[:5]:
                print(f"  - {warning}")
                
        return total_errors == 0

def main():
    parser = argparse.ArgumentParser(description='Validate manifest URL construction for external access')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show all validated URLs')
    parser.add_argument('--ci', action='store_true', help='Exit with error code for CI/CD')
    
    args = parser.parse_args()
    
    # Get repository root
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[2]  # Go up from engineering/tools to repo root
    
    # Run validation
    validator = URLValidator(repo_root, verbose=args.verbose)
    success = validator.validate_all_manifests()
    
    # Exit with appropriate code
    if args.ci:
        sys.exit(0 if success else 1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
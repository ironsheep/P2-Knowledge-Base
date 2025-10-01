#!/usr/bin/env python3
"""
Verify manifest linkages in the P2 Knowledge Base
Validates that all manifests and content files are properly connected
Uses the 4-key path standard for resolution

Version: 3.0.0
Date: 2025-09-28
Changes:
  - v3.0.0: Complete rewrite for 4-key path standard
            Understands manifest_base and content_base
            Ignores informational sections (related_manifests, notes, etc.)
            Precise path construction with no ambiguity
  - v2.4.0: Previous version with various path resolution attempts
"""

import os
import sys
import yaml
from pathlib import Path
from collections import defaultdict
from typing import Set, Dict, List, Tuple, Optional

# ANSI color codes for output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Files to ignore during validation
IGNORED_FILES = {
    '_template.yaml',  # Template files should never be referenced
}

# Sections to ignore during validation (informational only)
IGNORED_SECTIONS = {
    'related_manifests',
    'notes', 
    'comments',
    'description',
    'metadata',
    'search_terms',
    # 'keywords',  # DON'T ignore - this contains actual content references!
    'missing_files',  # These are documented as missing
    'planned_files',  # These are documented as not yet created
    'planned_but_not_created',  # These are documented as not created
    'cross_references',  # No standard yet for cross-references
}

class ManifestValidator:
    def __init__(self, root_path: Path):
        self.root = root_path
        self.errors = []
        self.warnings = []
        self.referenced_files = set()
        self.referenced_manifests = set()
        self.obex_category_refs = defaultdict(set)
        self.obex_author_refs = defaultdict(set)
        
    def resolve_path(self, base: Optional[str], reference: str) -> str:
        """Resolve a path using the 4-key standard"""
        if base:
            # Simple concatenation - the standard!
            return f"{base}/{reference}".replace('//', '/')
        else:
            # No base means reference should be complete
            return reference
            
    def load_manifest(self, manifest_path: Path) -> Optional[Dict]:
        """Load a manifest file and extract its bases"""
        if not manifest_path.exists():
            return None
            
        try:
            with open(manifest_path, 'r') as f:
                data = yaml.safe_load(f)
                return data
        except Exception as e:
            self.errors.append(f"Error loading {manifest_path}: {e}")
            return None
    
    def process_manifest(self, manifest_path: Path, depth: int = 0) -> None:
        """Process a manifest using the 4-key standard"""
        if depth > 10:  # Prevent infinite recursion
            return
            
        # Track this manifest as processed
        relative_path = manifest_path.relative_to(self.root)
        self.referenced_manifests.add(str(relative_path))
        
        # Load the manifest
        data = self.load_manifest(manifest_path)
        if not data:
            return
            
        # Extract the base paths from the 4-key standard
        manifest_base = data.get('manifest_base', '')
        content_base = data.get('content_base', '')
        
        # Track OBEX references for dual-organization validation
        # Note: unified index serves as the "category" organization
        is_obex_category = 'obex/categories' in str(manifest_path) or 'obex-unified-index.yaml' in str(manifest_path)
        is_obex_author = 'obex/authors' in str(manifest_path)
        
        # Process the manifest data recursively
        self._process_data(data, manifest_path, manifest_base, content_base,
                          is_obex_category, is_obex_author, depth)
    
    def _process_data(self, data, manifest_path: Path, 
                     manifest_base: str, content_base: str,
                     is_obex_category: bool, is_obex_author: bool, 
                     depth: int) -> None:
        """Process any data structure looking for manifest and content references"""
        
        if isinstance(data, dict):
            for key, value in data.items():
                # Skip ignored sections
                if key in IGNORED_SECTIONS:
                    continue
                    
                # Skip the base definitions themselves
                if key in ('manifest_base', 'content_base'):
                    continue
                    
                # Process based on key type
                if key == 'manifest' and isinstance(value, str):
                    # This is a manifest reference
                    full_path = self.resolve_path(manifest_base, value)
                    self._process_manifest_ref(full_path, depth)
                    
                elif key == 'content' and isinstance(value, str):
                    # This is a content reference
                    full_path = self.resolve_path(content_base, value)
                    self._track_content_ref(full_path, is_obex_category, is_obex_author, 
                                          manifest_path, value)
                    
                # Handle OBEX-style sub_manifests
                elif key == 'sub_manifests' and isinstance(value, dict):
                    for section_name, section_data in value.items():
                        if isinstance(section_data, dict):
                            sub_path = section_data.get('path', '')
                            manifests = section_data.get('manifests', [])
                            if sub_path and manifests:
                                for manifest_file in manifests:
                                    full_path = self.resolve_path(manifest_base, f"{sub_path}{manifest_file}")
                                    self._process_manifest_ref(full_path, depth)
                    
                else:
                    # Recurse into the value
                    self._process_data(value, manifest_path, manifest_base, content_base,
                                     is_obex_category, is_obex_author, depth)
                    
        elif isinstance(data, list):
            for item in data:
                self._process_data(item, manifest_path, manifest_base, content_base,
                                 is_obex_category, is_obex_author, depth)
    
    def _process_manifest_ref(self, manifest_ref: str, depth: int) -> None:
        """Process a manifest reference"""
        # Remove leading slash if present
        if manifest_ref.startswith('/'):
            manifest_ref = manifest_ref[1:]
            
        # Build full path
        full_path = self.root / manifest_ref
        
        # Check if it exists and process it
        if full_path.exists():
            self.process_manifest(full_path, depth + 1)
        else:
            self.errors.append(f"Referenced manifest not found: {manifest_ref}")
    
    def _track_content_ref(self, content_ref: str, is_obex_category: bool, 
                          is_obex_author: bool, manifest_path: Path, 
                          original_ref: str) -> None:
        """Track a content file reference"""
        # Remove leading slash if present  
        if content_ref.startswith('/'):
            content_ref = content_ref[1:]
            
        # Track the reference
        self.referenced_files.add(content_ref)
        
        # Track OBEX dual-organization
        if is_obex_category and 'objects/' in original_ref:
            category = manifest_path.stem.replace('-manifest', '')
            self.obex_category_refs[original_ref].add(category)
        elif is_obex_author and 'objects/' in original_ref:
            author = manifest_path.stem.replace('-manifest', '')
            self.obex_author_refs[original_ref].add(author)
    
    def validate_root_manifest(self) -> Dict:
        """Load and validate the root manifest"""
        root_manifest_path = self.root / "manifests" / "propeller-knowledge-root.yaml"
        
        if not root_manifest_path.exists():
            self.errors.append(f"Root manifest not found: {root_manifest_path}")
            return {}
            
        return self.load_manifest(root_manifest_path)
    
    def process_manifest_hierarchy(self) -> None:
        """Process the entire manifest hierarchy starting from the root"""
        # Start with the root manifest
        root_path = self.root / "manifests" / "propeller-knowledge-root.yaml"
        if root_path.exists():
            self.process_manifest(root_path)
            
        # Also process P2 root if it exists
        p2_root = self.root / "manifests" / "P2" / "p2-root.yaml"
        if p2_root.exists():
            # Process manifest_registry if present
            data = self.load_manifest(p2_root)
            if data and 'manifest_registry' in data:
                for name, entry in data['manifest_registry'].items():
                    if isinstance(entry, dict) and 'path' in entry:
                        manifest_path = entry['path']
                        if manifest_path.startswith('/'):
                            manifest_path = manifest_path[1:]
                        full_path = self.root / manifest_path
                        if full_path.exists():
                            self.process_manifest(full_path, depth=1)
    
    def find_orphaned_files(self) -> Tuple[Set[str], Set[str]]:
        """Find files that exist but aren't referenced"""
        orphaned_manifests = set()
        orphaned_content = set()
        
        # Check all content files in knowledge base (P2 directory only, not P2-support)
        kb_path = self.root / "engineering" / "knowledge-base" / "P2"
        if kb_path.exists():
            for yaml_file in kb_path.rglob("*.yaml"):
                if yaml_file.name in IGNORED_FILES:
                    continue
                    
                relative_path = yaml_file.relative_to(self.root)
                path_str = str(relative_path)
                
                if path_str not in self.referenced_files:
                    orphaned_content.add(path_str)
        
        # Check all manifest files
        manifest_path = self.root / "manifests"
        if manifest_path.exists():
            for yaml_file in manifest_path.rglob("*.yaml"):
                # Skip root manifest
                if yaml_file.name == "propeller-knowledge-root.yaml":
                    continue
                    
                relative_path = yaml_file.relative_to(self.root)
                path_str = str(relative_path)
                
                if path_str not in self.referenced_manifests:
                    orphaned_manifests.add(path_str)
        
        return orphaned_manifests, orphaned_content
    
    def validate_obex_dual_organization(self) -> Tuple[List[str], List[str]]:
        """Validate that OBEX objects are referenced in both category and author manifests"""
        errors = []
        warnings = []
        
        # Get all OBEX object references
        all_obex_objects = set(self.obex_category_refs.keys()) | set(self.obex_author_refs.keys())
        
        for obj_ref in sorted(all_obex_objects):
            categories = self.obex_category_refs.get(obj_ref, set())
            authors = self.obex_author_refs.get(obj_ref, set())
            
            if not categories:
                errors.append(f"OBEX object {obj_ref} MISSING from category manifests")
            if not authors:
                errors.append(f"OBEX object {obj_ref} MISSING from author manifests")
        
        # Check for orphaned OBEX files
        obex_dir = self.root / "engineering" / "knowledge-base" / "P2" / "community" / "obex" / "objects"
        if obex_dir.exists():
            for yaml_file in obex_dir.glob("*.yaml"):
                if yaml_file.name in IGNORED_FILES:
                    continue
                    
                obj_ref = f"objects/{yaml_file.name}"
                if obj_ref not in all_obex_objects:
                    errors.append(f"OBEX object {yaml_file.name} is ORPHANED (not in ANY manifest)")
        
        return errors, warnings
    
    def print_summary(self, baseline_counts=None) -> None:
        """Print validation summary"""
        print("\n" + "=" * 70)
        print(f"{BOLD}VERIFICATION SUMMARY{RESET}")
        print("=" * 70)
        
        # Basic stats
        manifests_processed = len(self.referenced_manifests)
        files_referenced = len(self.referenced_files)
        
        if baseline_counts:
            manifest_coverage = (manifests_processed / baseline_counts['manifests'] * 100) if baseline_counts['manifests'] > 0 else 0
            content_coverage = (files_referenced / baseline_counts['content'] * 100) if baseline_counts['content'] > 0 else 0
            
            print(f"Manifests processed: {manifests_processed} / {baseline_counts['manifests']} ({manifest_coverage:.1f}% coverage)")
            print(f"Content files referenced: {files_referenced} / {baseline_counts['content']} ({content_coverage:.1f}% coverage)")
        else:
            print(f"Manifests processed: {manifests_processed}")
            print(f"Content files referenced: {files_referenced}")
        
        # OBEX validation
        obex_errors, obex_warnings = self.validate_obex_dual_organization()
        
        if obex_errors:
            print(f"\n{RED}OBEX Dual-Organization Errors ({len(obex_errors)}):{RESET}")
            for error in obex_errors[:5]:
                print(f"  ❌ {error}")
            if len(obex_errors) > 5:
                print(f"  ... and {len(obex_errors) - 5} more errors")
        else:
            obex_count = len(set(self.obex_category_refs.keys()) | set(self.obex_author_refs.keys()))
            if obex_count > 0:
                print(f"\n{GREEN}✓ OBEX Dual-Organization Valid:{RESET}")
                print(f"  All {obex_count} objects referenced in both category AND author manifests")
        
        # Find orphaned files
        orphaned_manifests, orphaned_content = self.find_orphaned_files()
        
        # Report orphaned files
        if orphaned_manifests:
            print(f"\n{YELLOW}Orphaned Manifests ({len(orphaned_manifests)}):{RESET}")
            for manifest in sorted(orphaned_manifests)[:5]:
                print(f"  {manifest}")
            if len(orphaned_manifests) > 5:
                print(f"  ... and {len(orphaned_manifests) - 5} more")
        
        if orphaned_content:
            print(f"\n{YELLOW}Orphaned Content Files ({len(orphaned_content)}):{RESET}")
            # Group by directory
            by_dir = defaultdict(list)
            for orphan in orphaned_content:
                dir_path = str(Path(orphan).parent)
                by_dir[dir_path].append(orphan)
            
            for dir_path in sorted(by_dir.keys())[:10]:
                count = len(by_dir[dir_path])
                print(f"  {dir_path}: {count} files")
            
            if len(by_dir) > 10:
                print(f"  ... and {len(by_dir) - 10} more directories")
        
        # Final status
        print()
        if self.errors:
            print(f"{RED}{BOLD}❌ VERIFICATION FAILED{RESET}")
            for error in self.errors[:5]:
                print(f"{RED}  {error}{RESET}")
            if len(self.errors) > 5:
                print(f"{RED}  ... and {len(self.errors) - 5} more errors{RESET}")
        elif orphaned_content or orphaned_manifests:
            print(f"{YELLOW}{BOLD}⚠️  VERIFICATION PASSED WITH WARNINGS{RESET}")
            total_orphans = len(orphaned_content) + len(orphaned_manifests)
            print(f"{YELLOW}  {total_orphans} orphaned files found{RESET}")
        else:
            print(f"{GREEN}{BOLD}✅ VERIFICATION PASSED{RESET}")
            print(f"{GREEN}  All manifests and content files are properly connected!{RESET}")
        
        print("\n" + "=" * 70)

def main():
    # Get repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent  # Go up two levels from engineering/tools
    
    print(f"Validating manifest linkages in: {repo_root}")
    print(f"Using 4-key path standard (v3.0.0)")
    
    # Generate baseline counts
    print("\n" + "=" * 50)
    print(f"{BOLD}BASELINE FILE COUNTS{RESET}")
    print("=" * 50)
    
    # Count files for baseline
    manifests_dir = repo_root / "manifests"
    manifest_files = list(manifests_dir.rglob("*.yaml")) if manifests_dir.exists() else []
    manifest_count = len(manifest_files)
    
    # Count only P2 knowledge base files (excluding P2-support and ignored files)
    kb_dir = repo_root / "engineering" / "knowledge-base" / "P2"
    content_files = [f for f in kb_dir.rglob("*.yaml") if f.name not in IGNORED_FILES] if kb_dir.exists() else []
    content_count = len(content_files)
    
    print(f"Manifest files in manifests/ tree: {manifest_count}")
    print(f"Content files in engineering/knowledge-base/: {content_count}")
    print(f"Total relevant YAML files: {manifest_count + content_count}")
    
    print(f"\n{CYAN}Expected processing targets:{RESET}")
    print(f"  • Manifests to validate: {manifest_count}")
    print(f"  • Content files to reference: {content_count}")
    print("\n" + "=" * 50)
    
    # Create validator and run
    validator = ManifestValidator(repo_root)
    
    # Process the manifest hierarchy
    validator.process_manifest_hierarchy()
    
    # Prepare baseline counts for summary
    baseline_counts = {
        'manifests': manifest_count,
        'content': content_count
    }
    
    # Print results
    validator.print_summary(baseline_counts)
    
    # Exit with appropriate code
    if validator.errors:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
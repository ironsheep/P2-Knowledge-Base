#!/usr/bin/env python3
"""
Verify manifest linkages in the P2 Knowledge Base
Validates that all manifests and content files are properly connected

Version: 2.4.0
Date: 2025-09-27
Changes:
  - v2.4.0: CRITICAL FIX - Eliminated absolute paths from manifest tracking
            All paths now properly relative to repository root
            Fixed path resolution to never use .resolve() which creates absolute paths
            Added validation to catch and report absolute path errors
  - v2.3.0: Added support for path + manifests pattern
            Handles sub_manifests with path field and manifests list
            Properly combines path with manifest filenames
  - v2.2.0: Added support for manifest_registry pattern
            Registry allows name-based manifest references
            Processes manifests listed in registry with paths
  - v2.1.0: Made fully data-driven - no hardcoded section names
            Recursive processing of any manifest structure
            Preserved OBEX dual-organization validation
  - v2.0.0: Complete rewrite with unified path construction
            Fixed OBEX dual-organization validation
            Limited scope to P2 knowledge base only
            Support for all manifest patterns (lists, dicts, categories)
  - v1.0.0: Initial version
"""

import os
import sys
import yaml
from pathlib import Path
from collections import defaultdict, Counter
from typing import Set, Dict, List, Tuple

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

class ManifestValidator:
    def __init__(self, root_path: Path):
        self.root = root_path
        self.errors = []
        self.warnings = []
        self.referenced_files = set()
        self.referenced_manifests = set()
        self.obex_category_refs = defaultdict(set)  # Track OBEX refs by category
        self.obex_author_refs = defaultdict(set)    # Track OBEX refs by author
    
    def build_path(self, *parts, relative: bool = False) -> Path:
        """Build a path from parts, optionally returning relative path"""
        # Filter out empty parts and join
        clean_parts = [p for p in parts if p]
        
        # Handle absolute paths that start with /
        if clean_parts and clean_parts[0].startswith('/'):
            clean_parts[0] = clean_parts[0].lstrip('/')
        
        # Build the full path
        full_path = self.root
        for part in clean_parts:
            full_path = full_path / part
        
        # Return relative if requested
        if relative and full_path.is_relative_to(self.root):
            return full_path.relative_to(self.root)
        elif relative:
            # If can't make relative, return as is
            return full_path
        return full_path
        
    def validate_root_manifest(self) -> Dict:
        """Load and validate the root manifest"""
        root_manifest_path = self.build_path("manifests", "propeller-knowledge-root.yaml")

        if not root_manifest_path.exists():
            self.errors.append(f"Root manifest not found: {root_manifest_path}")
            return {}

        try:
            with open(root_manifest_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.errors.append(f"Error loading root manifest: {e}")
            return {}

    def process_manifest_registry(self, root_data: Dict) -> None:
        """Process the manifest_registry section in P2 root manifest
        This is a new pattern where manifests are registered by name with paths
        """
        # Check for P2 root manifest (has manifest_registry)
        p2_root_path = self.build_path("manifests", "P2", "p2-root.yaml")
        if not p2_root_path.exists():
            return

        try:
            with open(p2_root_path, 'r') as f:
                p2_data = yaml.safe_load(f)

            # Process manifest_registry if present
            if 'manifest_registry' in p2_data:
                registry = p2_data.get('manifest_registry', {})
                for name, entry in registry.items():
                    if isinstance(entry, dict) and 'path' in entry:
                        # This is a registry entry with a path
                        manifest_path = entry['path']
                        # Add to referenced manifests
                        self.referenced_manifests.add(manifest_path)

                        # Process the referenced manifest
                        full_path = self.build_path(manifest_path)
                        if full_path.exists():
                            try:
                                with open(full_path, 'r') as mf:
                                    manifest_data = yaml.safe_load(mf)
                                    if manifest_data:
                                        # Process this manifest hierarchy
                                        self.process_manifest_hierarchy(manifest_data, full_path, depth=1)
                            except Exception as e:
                                self.errors.append(f"Error loading registry manifest {manifest_path}: {e}")
                        else:
                            self.errors.append(f"Registry manifest not found: {manifest_path}")

        except Exception as e:
            # Silent fail if p2-root doesn't have registry - that's ok
            pass
    
    def process_manifest_hierarchy(self, manifest_data: Dict, manifest_path: Path, depth: int = 0) -> None:
        """Process manifest hierarchy - purely shape-driven approach"""
        # Prevent deep recursion
        if depth > 10:
            return

        # Get base_path if specified at manifest level
        base_path = manifest_data.get('base_path', '')

        # Track OBEX references for dual-organization validation
        is_obex_category = 'obex/categories' in str(manifest_path)
        is_obex_author = 'obex/authors' in str(manifest_path)
        
        # Process all sections recursively based on shape only
        self._process_any_structure(manifest_data, manifest_path, base_path, 
                                   is_obex_category, is_obex_author, depth)
    
    def _process_any_structure(self, data, manifest_path: Path, base_path: str,
                              is_obex_category: bool, is_obex_author: bool, depth: int = 0) -> None:
        """Process any YAML structure based purely on shape - no hardcoded field names"""
        if depth > 5:  # Prevent infinite recursion
            return
            
        if isinstance(data, dict):
            # Check if this dict has base_path to override
            current_base = data.get('base_path', base_path)
            
            for key, value in data.items():
                # Skip base_path since we handled it above
                if key == 'base_path':
                    continue
                    
                if isinstance(value, str):
                    # Handle based on key context
                    if key == 'manifest':
                        # This is definitely a manifest reference
                        # Use the directory of the current manifest, not its parent
                        manifest_dir = manifest_path.parent if manifest_path.is_file() else manifest_path
                        self.process_sub_manifest(value, manifest_dir, 0)
                    elif key == 'content':
                        # This is definitely a content file reference
                        content_path = self.build_path(current_base, value, relative=True)
                        self.referenced_files.add(str(content_path))
                        # Debug output removed for production
                        
                        # Track OBEX references
                        if is_obex_category and 'objects/' in value:
                            category = manifest_path.stem.replace('-manifest', '')
                            self.obex_category_refs[value].add(category)
                        elif is_obex_author and 'objects/' in value:
                            author = manifest_path.stem.replace('-manifest', '')
                            self.obex_author_refs[value].add(author)
                    elif key != 'pattern' and (value.endswith('.yaml') or value.endswith('.yml')):
                        # Only treat as manifest if it's not clearly a content file
                        # and contains path separators (manifest paths typically have directories)
                        # Also skip 'pattern' fields which are glob patterns, not actual files
                        if ('/' in value or '-manifest' in value) and '*' not in value:
                            # Use the directory of the current manifest, not its parent
                            manifest_dir = manifest_path.parent if manifest_path.is_file() else manifest_path
                            self.process_sub_manifest(value, manifest_dir, 0)
                            
                elif isinstance(value, list):
                    # Special handling for 'manifests' list when there's a 'path' field
                    if key == 'manifests' and 'path' in data:
                        # This is the path + manifests pattern
                        base_manifest_path = data['path']  # e.g., 'obex/categories/'
                        for manifest_file in value:
                            if isinstance(manifest_file, str) and manifest_file.endswith('.yaml'):
                                # Combine the path with manifest filename
                                full_manifest_path = base_manifest_path + manifest_file
                                # Use the directory of the current manifest, not its parent
                                manifest_dir = manifest_path.parent if manifest_path.is_file() else manifest_path
                                self.process_sub_manifest(full_manifest_path, manifest_dir, depth)
                    else:
                        # Process lists recursively as normal
                        self._process_any_structure(value, manifest_path, current_base, 
                                                  is_obex_category, is_obex_author, depth + 1)
                    
                elif isinstance(value, dict):
                    # Process nested dictionaries recursively
                    self._process_any_structure(value, manifest_path, current_base,
                                              is_obex_category, is_obex_author, depth + 1)
                    
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    # Check for content field in list items
                    if 'content' in item and isinstance(item['content'], str):
                        content_path = self.build_path(base_path, item['content'], relative=True)
                        self.referenced_files.add(str(content_path))
                        # Debug output removed for production
                            
                        # Track OBEX references
                        if is_obex_category and 'objects/' in item['content']:
                            category = manifest_path.stem.replace('-manifest', '')
                            self.obex_category_refs[item['content']].add(category)
                        elif is_obex_author and 'objects/' in item['content']:
                            author = manifest_path.stem.replace('-manifest', '')
                            self.obex_author_refs[item['content']].add(author)
                    
                    # Check for manifest field in list items
                    if 'manifest' in item and isinstance(item['manifest'], str):
                        # Use the directory of the current manifest, not its parent
                        manifest_dir = manifest_path.parent if manifest_path.is_file() else manifest_path
                        self.process_sub_manifest(item['manifest'], manifest_dir, 0)
                    
                    # Recurse into the item
                    self._process_any_structure(item, manifest_path, base_path,
                                              is_obex_category, is_obex_author, depth + 1)
                elif isinstance(item, str):
                    # String items - check for manifest references
                    # Only treat as manifest if it contains 'manifest' in the name or has directory separators
                    if (item.endswith('.yaml') or item.endswith('.yml')) and ('-manifest' in item or '/' in item):
                        # Use the directory of the current manifest, not its parent
                        manifest_dir = manifest_path.parent if manifest_path.is_file() else manifest_path
                        self.process_sub_manifest(item, manifest_dir, 0)
                else:
                    # Recurse into other types
                    self._process_any_structure(item, manifest_path, base_path,
                                              is_obex_category, is_obex_author, depth + 1)
    
    # Old methods removed - now using shape-driven approach
    

    
    def process_sub_manifest(self, manifest_ref, parent_dir: Path, depth: int = 0) -> None:
        """Process a sub-manifest reference"""
        # Handle case where manifest_ref might be a list
        if isinstance(manifest_ref, list):
            # Process each manifest in the list
            for ref in manifest_ref:
                self.process_sub_manifest(ref, parent_dir, depth)
            return
        
        # Ensure manifest_ref is a string
        if not isinstance(manifest_ref, str):
            return
            
        # Prevent deep recursion
        if depth > 10:
            return
        
        # Resolve manifest path
        if manifest_ref.startswith('/') or manifest_ref.startswith('manifests/'):
            manifest_path = self.build_path(manifest_ref)
        else:
            manifest_path = parent_dir / manifest_ref

        # Normalize path but keep it relative to root
        # DO NOT use resolve() as it creates absolute paths!
        if not manifest_path.is_absolute():
            manifest_path = self.root / manifest_path
        
        # Make sure we store relative paths for tracking
        if manifest_path.is_relative_to(self.root):
            relative_path = manifest_path.relative_to(self.root)
        else:
            # This should never happen - it's a critical error
            self.errors.append(f"CRITICAL: Absolute path detected: {manifest_path}")
            return
        
        path_str = str(relative_path)
        
        if path_str in self.referenced_manifests:
            return  # Already processed
        
        # Track this manifest as referenced
        self.referenced_manifests.add(path_str)
        
        # Debug output removed for production
        
        # Load and process the sub-manifest
        if manifest_path.exists():
            try:
                with open(manifest_path, 'r') as f:
                    sub_data = yaml.safe_load(f)
                    if sub_data:
                        self.process_manifest_hierarchy(sub_data, manifest_path, depth + 1)
            except Exception as e:
                self.errors.append(f"Error loading manifest {manifest_path}: {e}")
        else:
            # Always report relative paths in errors
            error_path = str(relative_path) if 'relative_path' in locals() else str(manifest_path)
            if error_path.startswith('/'):
                # Try to make it relative
                try:
                    error_path = str(Path(error_path).relative_to(self.root))
                except:
                    pass  # Keep as is if can't make relative
            self.errors.append(f"Referenced manifest not found: {error_path}")
    
    # resolve_content_path method is no longer needed - using build_path instead
    
    def find_orphaned_files(self) -> Tuple[Set[str], Set[str]]:
        """Find files that exist but aren't referenced"""
        orphaned_manifests = set()
        orphaned_content = set()

        # ONLY check P2 knowledge base files (not P2-support or P1)
        kb_path = self.build_path("engineering", "knowledge-base", "P2")
        if kb_path.exists():
            for yaml_file in kb_path.rglob("*.yaml"):
                relative_path = yaml_file.relative_to(self.root)
                path_str = str(relative_path)

                # Skip if referenced
                if path_str in self.referenced_files:
                    continue

                # Skip template files
                if yaml_file.name == '_template.yaml':
                    continue

                orphaned_content.add(path_str)
        
        # Check all manifest files
        manifest_path = self.build_path("manifests")
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
        """Validate that OBEX objects are referenced in both category and author manifests
        Returns: (errors, warnings)
        """
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

        # Also check if any OBEX object files exist but aren't referenced
        obex_dir = self.build_path("engineering", "knowledge-base", "P2", "community", "obex", "objects")
        if obex_dir.exists():
            for yaml_file in obex_dir.glob("*.yaml"):
                if yaml_file.name == '_template.yaml':
                    continue

                obj_ref = f"objects/{yaml_file.name}"
                if obj_ref not in all_obex_objects:
                    errors.append(f"OBEX object {yaml_file.name} is ORPHANED (not in ANY manifest)")

        return errors, warnings
    
    def check_incomplete_manifests(self) -> Dict[str, float]:
        """Check for manifests with incomplete references"""
        incomplete = {}
        
        # Check specific known manifests
        queries_manifest = self.build_path("manifests", "P2", "language", "spin2", "queries", "quick-queries-manifest.yaml")
        if queries_manifest.exists():
            try:
                with open(queries_manifest, 'r') as f:
                    data = yaml.safe_load(f)
                    if data and 'queries' in data:
                        total = len(data['queries'])
                        with_content = sum(1 for q in data['queries'] if 'content' in q)
                        if with_content < total:
                            incomplete['Quick Queries'] = (with_content, total)
            except:
                pass
                
        return incomplete
    
    def print_summary(self, baseline_counts=None) -> None:
        """Print validation summary with baseline comparison"""
        print("\n" + "=" * 70)
        print(f"{BOLD}VERIFICATION SUMMARY{RESET}")
        print("=" * 70)
        
        # Basic stats with baseline comparison if available
        manifests_processed = len(self.referenced_manifests) + 1  # +1 for root
        files_referenced = len(self.referenced_files)
        
        if baseline_counts:
            manifest_coverage = (manifests_processed / baseline_counts['manifests'] * 100) if baseline_counts['manifests'] > 0 else 0
            content_coverage = (files_referenced / baseline_counts['content'] * 100) if baseline_counts['content'] > 0 else 0
            
            print(f"Manifests processed: {manifests_processed} / {baseline_counts['manifests']} ({manifest_coverage:.1f}% coverage)")
            print(f"Content files referenced: {files_referenced} / {baseline_counts['content']} ({content_coverage:.1f}% coverage)")
        else:
            print(f"Manifests checked: {manifests_processed}")
            print(f"File references checked: {files_referenced}")
        
        # Check for incomplete manifests
        incomplete = self.check_incomplete_manifests()
        if incomplete:
            print(f"\n{YELLOW}Incomplete Manifests ({len(incomplete)}):{RESET}")
            for name, (complete, total) in incomplete.items():
                pct = (complete / total * 100) if total > 0 else 0
                print(f"  ⚠ {name}: Only {complete} of {total} entries ({pct:.1f}%)")
        
        # Find orphaned files
        orphaned_manifests, orphaned_content = self.find_orphaned_files()
        
        # Special handling for OBEX - don't count them as orphaned if they're properly dual-referenced
        obex_errors, obex_warnings = self.validate_obex_dual_organization()

        # Add OBEX errors to main errors list
        if obex_errors:
            self.errors.extend(obex_errors)
        
        # Remove properly referenced OBEX files from orphaned list
        all_obex_refs = set(self.obex_category_refs.keys()) | set(self.obex_author_refs.keys())
        filtered_orphaned = set()
        for orphan in orphaned_content:
            # Check if this is an OBEX object that's actually referenced
            if 'obex/objects/' in orphan:
                filename = orphan.split('/')[-1]
                if f"objects/{filename}" not in all_obex_refs:
                    filtered_orphaned.add(orphan)
            else:
                filtered_orphaned.add(orphan)
        
        # Report OBEX validation
        if obex_errors:
            print(f"\n{RED}OBEX Dual-Organization Errors ({len(obex_errors)}):{RESET}")
            for error in obex_errors[:10]:  # Show first 10
                print(f"  ❌ {error}")
            if len(obex_errors) > 10:
                print(f"  ... and {len(obex_errors) - 10} more errors")
        else:
            print(f"\n{GREEN}✓ OBEX Dual-Organization Valid:{RESET}")
            obex_count = len([o for o in all_obex_refs if o.startswith('objects/')])
            print(f"  All {obex_count} objects referenced in both category AND author manifests")
        
        # Report orphaned files
        if orphaned_manifests:
            print(f"\n{YELLOW}Orphaned Manifests ({len(orphaned_manifests)}):{RESET}")
            for manifest in sorted(orphaned_manifests)[:5]:
                print(f"  {manifest}")
            if len(orphaned_manifests) > 5:
                print(f"  ... and {len(orphaned_manifests) - 5} more")
        
        if filtered_orphaned:
            print(f"\n{YELLOW}Orphaned Files ({len(filtered_orphaned)}):{RESET}")
            # Group by directory
            by_dir = defaultdict(list)
            for orphan in filtered_orphaned:
                dir_path = str(Path(orphan).parent)
                by_dir[dir_path].append(orphan)
            
            # Show summary by directory
            for dir_path in sorted(by_dir.keys())[:10]:
                count = len(by_dir[dir_path])
                print(f"  {dir_path}: {count} files")
            
            if len(by_dir) > 10:
                remaining_dirs = len(by_dir) - 10
                remaining_files = sum(len(files) for dir, files in list(by_dir.items())[10:])
                print(f"  ... and {remaining_dirs} more directories")
        
        # Final status
        print()
        if self.errors:
            print(f"{RED}{BOLD}❌ VERIFICATION FAILED{RESET}")
            for error in self.errors[:5]:
                print(f"{RED}  {error}{RESET}")
        elif filtered_orphaned or orphaned_manifests:
            print(f"{YELLOW}{BOLD}⚠️  VERIFICATION PASSED WITH WARNINGS{RESET}")
            print(f"{YELLOW}{len(filtered_orphaned)} files exist but aren't referenced.{RESET}")
        else:
            print(f"{GREEN}{BOLD}✅ VERIFICATION PASSED{RESET}")
            print(f"{GREEN}All manifests and content files are properly connected!{RESET}")
        
        print("\n" + "=" * 70)

def main():
    # Get repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent  # Go up two levels from engineering/tools
    
    print(f"Validating manifest linkages in: {repo_root}")
    
    # Generate baseline file counts for comparison
    print("\n" + "=" * 50)
    print(f"{BOLD}BASELINE FILE COUNTS{RESET}")
    print("=" * 50)
    
    # Count manifest files in manifests/ tree
    manifests_dir = repo_root / "manifests"
    manifest_files = list(manifests_dir.rglob("*.yaml")) if manifests_dir.exists() else []
    manifest_count = len(manifest_files)
    print(f"Manifest files in manifests/ tree: {manifest_count}")
    
    # Count content files in engineering/knowledge-base/ tree
    kb_dir = repo_root / "engineering" / "knowledge-base"
    content_files = list(kb_dir.rglob("*.yaml")) if kb_dir.exists() else []
    content_count = len(content_files)
    print(f"Content files in engineering/knowledge-base/: {content_count}")
    
    # Total relevant files
    total_relevant = manifest_count + content_count
    print(f"Total relevant YAML files: {total_relevant}")
    
    print(f"\n{CYAN}Expected processing targets:{RESET}")
    print(f"  • Manifests to validate: {manifest_count}")
    print(f"  • Content files to reference: {content_count}")
    print("\n" + "=" * 50)
    
    # Create validator and run
    validator = ManifestValidator(repo_root)

    # Load and process root manifest
    root_data = validator.validate_root_manifest()
    if root_data:
        # Start with root manifest processing
        root_path = repo_root / "manifests" / "propeller-knowledge-root.yaml"
        validator.process_manifest_hierarchy(root_data, root_path)

    # Process manifest_registry pattern (new in v2.2)
    # This handles the new registry-based manifest references
    validator.process_manifest_registry(root_data)
    
    # Debug output
    if False:  # Set to True for debugging
        print(f"\nDEBUG: Referenced manifests ({len(validator.referenced_manifests)}):")
        # Group by pattern
        patterns = {}
        for m in validator.referenced_manifests:
            if m.startswith('Users/'):
                patterns.setdefault('absolute', []).append(m)
            elif m.startswith('manifests/'):
                patterns.setdefault('manifests/', []).append(m)
            elif m.startswith('obex/'):
                patterns.setdefault('obex/', []).append(m)
            else:
                patterns.setdefault('other', []).append(m)
        
        for pattern, items in patterns.items():
            print(f"\n  Pattern '{pattern}': {len(items)} items")
            for item in sorted(items)[:3]:
                print(f"    {item}")
    
    # Prepare baseline counts for summary
    baseline_counts = {
        'manifests': manifest_count,
        'content': content_count,
        'total_relevant': total_relevant
    }
    
    # Print results
    validator.print_summary(baseline_counts)
    
    # Exit with appropriate code
    if validator.errors:
        sys.exit(1)
    elif validator.find_orphaned_files()[1]:  # If there are orphaned content files
        sys.exit(0)  # Warnings but not failure
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
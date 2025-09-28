#!/usr/bin/env python3
"""
Check for obsolete keys in manifest files according to the 4-key path standard.
These keys should no longer exist in any manifest files.
"""

import os
import sys
import yaml
from pathlib import Path
from collections import defaultdict

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Obsolete keys that should NOT appear in manifests
OBSOLETE_KEYS = {
    'base_path': 'Use manifest_base and content_base instead',
    'file': 'Use content: instead', 
    'path': 'Use manifest: or content: with proper base',
    'location': 'Use content: with content_base',
    'yaml_path': 'Use content: with content_base',
    'url': 'Not used in local manifests',
    'manifest_path': 'Use manifest: with manifest_base',
    'content_path': 'Use content: with content_base',
    'reference': 'Use manifest: or content: instead',
    'yaml': 'Use content: instead',
}

# Keys that might be obsolete but need context
POSSIBLY_OBSOLETE = {
    'files': 'Should use content: for individual references',
    'manifests': 'Should use manifest: for individual references',
    'items': 'May be valid in some contexts, check usage',
}

def check_for_obsolete_keys(data, path="", file_path=""):
    """Recursively check for obsolete keys in data structure"""
    issues = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            
            # Check if this key is obsolete
            if key in OBSOLETE_KEYS:
                issues.append({
                    'file': file_path,
                    'path': current_path,
                    'key': key,
                    'reason': OBSOLETE_KEYS[key],
                    'severity': 'error'
                })
            elif key in POSSIBLY_OBSOLETE:
                # Only flag if not in an ignored section
                if not any(ignored in path for ignored in ['notes', 'description', 'metadata']):
                    issues.append({
                        'file': file_path,
                        'path': current_path,
                        'key': key,
                        'reason': POSSIBLY_OBSOLETE[key],
                        'severity': 'warning'
                    })
            
            # Recurse into the value
            if isinstance(value, (dict, list)):
                issues.extend(check_for_obsolete_keys(value, current_path, file_path))
                
    elif isinstance(data, list):
        for i, item in enumerate(data):
            current_path = f"{path}[{i}]"
            if isinstance(item, (dict, list)):
                issues.extend(check_for_obsolete_keys(item, current_path, file_path))
    
    return issues

def check_manifest_file(manifest_path):
    """Check a single manifest file for obsolete keys"""
    try:
        with open(manifest_path, 'r') as f:
            data = yaml.safe_load(f)
            if data:
                return check_for_obsolete_keys(data, "", str(manifest_path))
    except Exception as e:
        print(f"{RED}Error loading {manifest_path}: {e}{RESET}")
    return []

def main():
    # Get repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    
    print(f"{BOLD}{'='*70}{RESET}")
    print(f"{BOLD}OBSOLETE KEY CHECKER - 4-KEY PATH STANDARD{RESET}")
    print(f"{BOLD}{'='*70}{RESET}")
    
    # Find all manifest files
    manifest_dir = repo_root / "manifests"
    manifest_files = list(manifest_dir.rglob("*.yaml"))
    
    print(f"\nChecking {len(manifest_files)} manifest files for obsolete keys...")
    print(f"According to: {CYAN}MANIFEST-PATH-STANDARD.md{RESET}\n")
    
    all_issues = []
    files_with_issues = set()
    
    # Check each manifest
    for manifest_path in sorted(manifest_files):
        issues = check_manifest_file(manifest_path)
        if issues:
            all_issues.extend(issues)
            files_with_issues.add(str(manifest_path))
    
    # Group issues by severity
    errors = [i for i in all_issues if i['severity'] == 'error']
    warnings = [i for i in all_issues if i['severity'] == 'warning']
    
    # Report results
    if errors:
        print(f"{RED}{BOLD}ERRORS FOUND ({len(errors)}):{RESET}")
        print(f"{RED}These keys MUST be removed:{RESET}\n")
        
        # Group by key
        by_key = defaultdict(list)
        for issue in errors:
            by_key[issue['key']].append(issue)
        
        for key in sorted(by_key.keys()):
            issues = by_key[key]
            print(f"  {RED}❌ '{key}'{RESET} - {issues[0]['reason']}")
            for issue in issues[:3]:
                rel_path = Path(issue['file']).relative_to(repo_root)
                print(f"      {rel_path} at {issue['path']}")
            if len(issues) > 3:
                print(f"      ... and {len(issues) - 3} more occurrences")
            print()
    
    if warnings:
        print(f"{YELLOW}{BOLD}WARNINGS ({len(warnings)}):{RESET}")
        print(f"{YELLOW}These keys might need attention:{RESET}\n")
        
        # Group by key
        by_key = defaultdict(list)
        for issue in warnings:
            by_key[issue['key']].append(issue)
        
        for key in sorted(by_key.keys()):
            issues = by_key[key]
            print(f"  {YELLOW}⚠️  '{key}'{RESET} - {issues[0]['reason']}")
            for issue in issues[:2]:
                rel_path = Path(issue['file']).relative_to(repo_root)
                print(f"      {rel_path} at {issue['path']}")
            if len(issues) > 2:
                print(f"      ... and {len(issues) - 2} more occurrences")
            print()
    
    # Summary
    print(f"{BOLD}{'='*70}{RESET}")
    print(f"{BOLD}SUMMARY{RESET}")
    print(f"{BOLD}{'='*70}{RESET}")
    
    print(f"Files checked: {len(manifest_files)}")
    print(f"Files with issues: {len(files_with_issues)}")
    print(f"Total errors: {len(errors)}")
    print(f"Total warnings: {len(warnings)}")
    
    if errors:
        print(f"\n{RED}{BOLD}❌ OBSOLETE KEYS FOUND{RESET}")
        print(f"{RED}Fix these before proceeding with manifest validation.{RESET}")
        
        # Provide fix command
        print(f"\n{CYAN}To automatically fix some of these:{RESET}")
        print(f"  python3 engineering/tools/update-manifests-to-standard.py")
        
        sys.exit(1)
    elif warnings:
        print(f"\n{YELLOW}{BOLD}⚠️  CHECK COMPLETE WITH WARNINGS{RESET}")
        print(f"{YELLOW}Review the warnings above for potential improvements.{RESET}")
    else:
        print(f"\n{GREEN}{BOLD}✅ ALL MANIFESTS CLEAN{RESET}")
        print(f"{GREEN}No obsolete keys found!{RESET}")
    
    print()

if __name__ == "__main__":
    main()
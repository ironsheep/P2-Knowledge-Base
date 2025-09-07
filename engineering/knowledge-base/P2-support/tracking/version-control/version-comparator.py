#!/usr/bin/env python3
"""
P2 Knowledge Base Version Comparison Tool
Compares repository versions and generates migration guides
Version: 1.0.0
"""

import yaml
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict
import difflib

class VersionComparator:
    """Compare different versions of the repository"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.current_version = self.get_current_version()
        
    def get_current_version(self) -> str:
        """Get current repository version from git"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()[:8]
        except:
            return "unknown"
            
    def get_version_at_commit(self, commit: str) -> Dict[str, Any]:
        """Get repository state at a specific commit"""
        version_data = {
            'commit': commit,
            'entries': {},
            'statistics': {}
        }
        
        try:
            # Get list of YAML files at that commit
            result = subprocess.run(
                ['git', 'ls-tree', '-r', '--name-only', commit],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            yaml_files = [f for f in result.stdout.splitlines() 
                         if f.endswith('.yaml') and ('instructions/' in f or 
                            'components/' in f or 'architecture/' in f)]
            
            # Get content of each file at that commit
            for file_path in yaml_files:
                try:
                    result = subprocess.run(
                        ['git', 'show', f'{commit}:{file_path}'],
                        cwd=self.repo_path,
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        data = yaml.safe_load(result.stdout)
                        if data and 'id' in data:
                            version_data['entries'][data['id']] = {
                                'path': file_path,
                                'data': data
                            }
                except:
                    pass
                    
            # Calculate statistics
            version_data['statistics'] = self.calculate_statistics(version_data['entries'])
            
        except Exception as e:
            print(f"Error getting version at {commit}: {e}")
            
        return version_data
        
    def calculate_statistics(self, entries: Dict) -> Dict[str, Any]:
        """Calculate statistics for a version"""
        stats = {
            'total_entries': len(entries),
            'by_category': defaultdict(int),
            'by_completeness': defaultdict(int),
            'average_completeness': 0,
            'total_examples': 0,
            'total_cross_refs': 0
        }
        
        completeness_scores = []
        
        for entry_id, entry_info in entries.items():
            data = entry_info['data']
            
            # Category stats
            if 'category' in data:
                stats['by_category'][data['category']] += 1
                
            # Completeness stats
            if 'completeness_score' in data:
                score = data['completeness_score']
                stats['by_completeness'][score] += 1
                completeness_scores.append(score)
                
            # Count examples
            if 'examples' in data:
                stats['total_examples'] += len(data['examples'])
                
            # Count cross-references
            if 'related_instructions' in data:
                stats['total_cross_refs'] += len(data['related_instructions'])
                
        # Calculate average completeness
        if completeness_scores:
            stats['average_completeness'] = sum(completeness_scores) / len(completeness_scores)
            
        return stats
        
    def compare_versions(self, version1: str, version2: str) -> Dict[str, Any]:
        """Compare two versions of the repository"""
        print(f"Comparing versions {version1} and {version2}...")
        
        # Get data for both versions
        v1_data = self.get_version_at_commit(version1)
        v2_data = self.get_version_at_commit(version2)
        
        comparison = {
            'version1': version1,
            'version2': version2,
            'timestamp': datetime.now().isoformat(),
            'entries': {
                'added': [],
                'removed': [],
                'modified': []
            },
            'statistics': {
                'v1': v1_data['statistics'],
                'v2': v2_data['statistics']
            },
            'field_changes': defaultdict(lambda: defaultdict(int))
        }
        
        v1_ids = set(v1_data['entries'].keys())
        v2_ids = set(v2_data['entries'].keys())
        
        # Find added entries
        for entry_id in v2_ids - v1_ids:
            comparison['entries']['added'].append({
                'id': entry_id,
                'path': v2_data['entries'][entry_id]['path'],
                'category': v2_data['entries'][entry_id]['data'].get('category', 'unknown'),
                'completeness': v2_data['entries'][entry_id]['data'].get('completeness_score', 0)
            })
            
        # Find removed entries
        for entry_id in v1_ids - v2_ids:
            comparison['entries']['removed'].append({
                'id': entry_id,
                'path': v1_data['entries'][entry_id]['path'],
                'category': v1_data['entries'][entry_id]['data'].get('category', 'unknown')
            })
            
        # Find modified entries
        for entry_id in v1_ids & v2_ids:
            v1_entry = v1_data['entries'][entry_id]['data']
            v2_entry = v2_data['entries'][entry_id]['data']
            
            changes = self.compare_entries(v1_entry, v2_entry)
            
            if changes:
                comparison['entries']['modified'].append({
                    'id': entry_id,
                    'path': v2_data['entries'][entry_id]['path'],
                    'changes': changes
                })
                
                # Track field-level changes
                for change in changes:
                    comparison['field_changes'][change['field']][change['type']] += 1
                    
        return comparison
        
    def compare_entries(self, entry1: Dict, entry2: Dict) -> List[Dict]:
        """Compare two versions of an entry"""
        changes = []
        
        # Check all fields in entry2
        for field, value2 in entry2.items():
            if field in ['last_updated', 'update_history']:
                continue  # Skip metadata fields
                
            if field not in entry1:
                changes.append({
                    'field': field,
                    'type': 'added',
                    'new_value': str(value2)[:100] if not isinstance(value2, (dict, list)) else f"[{type(value2).__name__}]"
                })
            elif entry1[field] != value2:
                changes.append({
                    'field': field,
                    'type': 'modified',
                    'old_value': str(entry1[field])[:100] if not isinstance(entry1[field], (dict, list)) else f"[{type(entry1[field]).__name__}]",
                    'new_value': str(value2)[:100] if not isinstance(value2, (dict, list)) else f"[{type(value2).__name__}]"
                })
                
        # Check for removed fields
        for field in entry1:
            if field not in entry2 and field not in ['last_updated', 'update_history']:
                changes.append({
                    'field': field,
                    'type': 'removed',
                    'old_value': str(entry1[field])[:100] if not isinstance(entry1[field], (dict, list)) else f"[{type(entry1[field]).__name__}]"
                })
                
        return changes
        
    def generate_migration_guide(self, comparison: Dict) -> str:
        """Generate migration guide for downstream consumers"""
        guide = f"""# P2 Knowledge Base Migration Guide
From Version: {comparison['version1']}
To Version: {comparison['version2']}
Generated: {comparison['timestamp']}

## Overview
This guide helps downstream consumers migrate from version {comparison['version1'][:8]} to {comparison['version2'][:8]} of the P2 Knowledge Base.

## Summary of Changes

### Entry Changes
- **Added**: {len(comparison['entries']['added'])} new entries
- **Removed**: {len(comparison['entries']['removed'])} entries
- **Modified**: {len(comparison['entries']['modified'])} entries

### Statistical Changes
"""
        
        # Compare statistics
        v1_stats = comparison['statistics']['v1']
        v2_stats = comparison['statistics']['v2']
        
        guide += f"""- **Total Entries**: {v1_stats['total_entries']} → {v2_stats['total_entries']} ({v2_stats['total_entries'] - v1_stats['total_entries']:+d})
- **Average Completeness**: {v1_stats['average_completeness']:.1f} → {v2_stats['average_completeness']:.1f} ({v2_stats['average_completeness'] - v1_stats['average_completeness']:+.1f})
- **Total Examples**: {v1_stats['total_examples']} → {v2_stats['total_examples']} ({v2_stats['total_examples'] - v1_stats['total_examples']:+d})
- **Total Cross-References**: {v1_stats['total_cross_refs']} → {v2_stats['total_cross_refs']} ({v2_stats['total_cross_refs'] - v1_stats['total_cross_refs']:+d})

## Breaking Changes
"""
        
        # Identify breaking changes
        breaking_changes = []
        
        if comparison['entries']['removed']:
            breaking_changes.append("### Removed Entries")
            breaking_changes.append("The following entries have been removed and will cause lookup failures:")
            for entry in comparison['entries']['removed'][:10]:
                breaking_changes.append(f"- `{entry['id']}` ({entry['category']})")
                
        if any(c['type'] == 'removed' for m in comparison['entries']['modified'] for c in m['changes']):
            breaking_changes.append("\n### Removed Fields")
            breaking_changes.append("The following fields have been removed from entries:")
            field_removals = defaultdict(list)
            for modified in comparison['entries']['modified']:
                for change in modified['changes']:
                    if change['type'] == 'removed':
                        field_removals[change['field']].append(modified['id'])
            for field, entries in list(field_removals.items())[:5]:
                guide += f"- `{field}` removed from {len(entries)} entries\n"
                
        if breaking_changes:
            guide += "\n".join(breaking_changes)
        else:
            guide += "No breaking changes detected.\n"
            
        # Add new features section
        guide += """
## New Features
"""
        
        if comparison['entries']['added']:
            guide += f"\n### New Entries ({len(comparison['entries']['added'])} total)\n"
            for entry in comparison['entries']['added'][:10]:
                guide += f"- `{entry['id']}` - {entry['category']} (completeness: {entry['completeness']})\n"
            if len(comparison['entries']['added']) > 10:
                guide += f"- ... and {len(comparison['entries']['added']) - 10} more\n"
                
        # Add field changes summary
        if comparison['field_changes']:
            guide += "\n### Field-Level Changes\n"
            for field, changes in list(comparison['field_changes'].items())[:10]:
                total = sum(changes.values())
                guide += f"- `{field}`: {total} changes "
                details = []
                if changes['added']:
                    details.append(f"{changes['added']} added")
                if changes['modified']:
                    details.append(f"{changes['modified']} modified")
                if changes['removed']:
                    details.append(f"{changes['removed']} removed")
                guide += f"({', '.join(details)})\n"
                
        # Add migration steps
        guide += """
## Migration Steps

### 1. Update Entry Lookups
Review your code for references to removed entries and update accordingly.

### 2. Handle Field Changes
Update any code that accesses removed or modified fields.

### 3. Leverage New Features
Consider using newly added entries and fields to enhance functionality.

### 4. Revalidate Integration
Run your test suite to ensure compatibility with the new version.

## API Compatibility

### Recommended Approach
```python
# Check for field existence before access
if 'field_name' in entry_data:
    value = entry_data['field_name']
else:
    # Use default or handle missing field
    value = default_value
```

### Version Detection
```python
# Check repository version
with open('update-tracking/repository-stats.json') as f:
    stats = json.load(f)
    commit = stats.get('commit', 'unknown')
```

## Support
For questions or issues with migration, please refer to the repository documentation or create an issue.
"""
        
        return guide
        
    def generate_diff_report(self, comparison: Dict) -> str:
        """Generate detailed diff report"""
        report = f"""# Detailed Version Diff Report
{comparison['version1'][:8]} → {comparison['version2'][:8]}
Generated: {comparison['timestamp']}

## Modified Entries ({len(comparison['entries']['modified'])} total)
"""
        
        for entry in comparison['entries']['modified'][:20]:  # Limit to 20
            report += f"\n### {entry['id']}\n"
            report += f"Path: `{entry['path']}`\n\n"
            
            for change in entry['changes'][:10]:  # Limit changes per entry
                if change['type'] == 'added':
                    report += f"- ➕ **{change['field']}**: {change['new_value']}\n"
                elif change['type'] == 'removed':
                    report += f"- ➖ **{change['field']}**: ~~{change['old_value']}~~\n"
                elif change['type'] == 'modified':
                    report += f"- 📝 **{change['field']}**: {change['old_value']} → {change['new_value']}\n"
                    
        if len(comparison['entries']['modified']) > 20:
            report += f"\n... and {len(comparison['entries']['modified']) - 20} more modified entries\n"
            
        return report
        
    def compare_with_tag(self, tag: str) -> Dict[str, Any]:
        """Compare current version with a tagged version"""
        try:
            # Get commit hash for tag
            result = subprocess.run(
                ['git', 'rev-list', '-n', '1', tag],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                tag_commit = result.stdout.strip()
                current_commit = subprocess.run(
                    ['git', 'rev-parse', 'HEAD'],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                ).stdout.strip()
                
                return self.compare_versions(tag_commit, current_commit)
            else:
                print(f"Tag {tag} not found")
                return {}
                
        except Exception as e:
            print(f"Error comparing with tag: {e}")
            return {}
            

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="P2 Knowledge Base Version Comparison")
    parser.add_argument('--repo-path', default='.', help='Repository root path')
    parser.add_argument('--from-version', help='From version (commit hash or tag)')
    parser.add_argument('--to-version', help='To version (commit hash or tag)')
    parser.add_argument('--from-tag', help='Compare from tag to current')
    parser.add_argument('--output', help='Output file for migration guide')
    
    args = parser.parse_args()
    
    comparator = VersionComparator(args.repo_path)
    
    if args.from_tag:
        # Compare tag with current
        comparison = comparator.compare_with_tag(args.from_tag)
    elif args.from_version and args.to_version:
        # Compare two specific versions
        comparison = comparator.compare_versions(args.from_version, args.to_version)
    else:
        print("Please specify versions to compare")
        exit(1)
        
    if comparison:
        # Generate migration guide
        guide = comparator.generate_migration_guide(comparison)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(guide)
            print(f"Migration guide saved to {args.output}")
        else:
            print(guide)
            
        # Also generate diff report
        diff_report = comparator.generate_diff_report(comparison)
        diff_file = Path(args.output).with_suffix('.diff.md') if args.output else Path('version-diff.md')
        with open(diff_file, 'w') as f:
            f.write(diff_report)
        print(f"Diff report saved to {diff_file}")
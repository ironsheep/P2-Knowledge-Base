#!/usr/bin/env python3
"""
P2 Knowledge Base Update Propagation System
Propagates changes from source documents to repository entries
Version: 1.0.0
"""

import yaml
import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Any
from collections import defaultdict
import subprocess

class UpdatePropagator:
    """Propagates updates through the repository"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.trigger_dir = self.repo_path / "update-tracking" / "extraction-triggers"
        self.backup_dir = self.repo_path / "update-tracking" / "backups"
        self.conflict_dir = self.repo_path / "update-tracking" / "conflicts"
        self.propagation_log = []
        
    def load_extraction_triggers(self) -> List[Dict]:
        """Load pending extraction triggers"""
        triggers = []
        
        if self.trigger_dir.exists():
            for trigger_file in self.trigger_dir.glob("extract-*.yaml"):
                with open(trigger_file, 'r') as f:
                    trigger_data = yaml.safe_load(f)
                    trigger_data['trigger_file'] = trigger_file
                    triggers.append(trigger_data)
                    
        # Sort by timestamp
        triggers.sort(key=lambda x: x.get('trigger_time', ''))
        return triggers
        
    def backup_entry(self, entry_path: Path) -> Path:
        """Create backup of entry before modification"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / entry_path.parent.name / \
                     f"{entry_path.stem}_backup_{timestamp}.yaml"
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(entry_path, backup_path)
        return backup_path
        
    def merge_entry_data(self, existing_data: Dict, new_data: Dict, 
                        source: str) -> Tuple[Dict, List[str]]:
        """Merge new data into existing entry, tracking conflicts"""
        merged = existing_data.copy()
        conflicts = []
        
        # Layer-based merging strategy
        layer_priority = {
            'P2-Instruction-Set.csv': 1,
            'P2-Datasheet': 2,
            'Silicon-Doc': 3,
            'Forum': 4
        }
        
        source_priority = 2  # Default priority
        for key, priority in layer_priority.items():
            if key in source:
                source_priority = priority
                break
                
        # Merge fields based on priority
        for field, new_value in new_data.items():
            if field in ['id', 'mnemonic', 'category']:
                # These fields should not change
                if field in existing_data and existing_data[field] != new_value:
                    conflicts.append({
                        'field': field,
                        'existing': existing_data[field],
                        'new': new_value,
                        'source': source
                    })
                    continue
                    
            elif field == 'completeness_score':
                # Recalculate based on new data
                merged[field] = self.calculate_completeness_score(merged)
                
            elif field == 'source_layers':
                # Merge source layer flags
                if field not in merged:
                    merged[field] = {}
                merged[field].update(new_value)
                
            elif field == 'examples':
                # Append new examples, avoiding duplicates
                if field not in merged:
                    merged[field] = []
                existing_codes = {ex.get('code', '') for ex in merged[field]}
                for example in new_value:
                    if example.get('code', '') not in existing_codes:
                        merged[field].append(example)
                        
            elif field == 'related_instructions':
                # Merge lists, avoiding duplicates
                if field not in merged:
                    merged[field] = []
                merged[field] = list(set(merged[field] + new_value))
                
            elif field in ['timing', 'encoding']:
                # Higher priority sources override
                if source_priority >= 2:  # Datasheet or higher
                    merged[field] = new_value
                elif field not in merged:
                    merged[field] = new_value
                    
            else:
                # Default: newer data wins for most fields
                if field not in merged or source_priority >= 3:
                    merged[field] = new_value
                    
        # Update metadata
        merged['last_updated'] = datetime.now().isoformat()
        if 'update_history' not in merged:
            merged['update_history'] = []
        merged['update_history'].append({
            'date': datetime.now().isoformat(),
            'source': source,
            'changes': f"Updated from {source}"
        })
        
        return merged, conflicts
        
    def calculate_completeness_score(self, entry_data: Dict) -> int:
        """Calculate completeness score for an entry"""
        score = 0
        
        # Check each layer
        if entry_data.get('source_layers', {}).get('csv'):
            score += 1
        if entry_data.get('source_layers', {}).get('datasheet'):
            score += 1
        if entry_data.get('source_layers', {}).get('silicon_doc'):
            score += 1
        if entry_data.get('source_layers', {}).get('forum_clarification'):
            score += 1
            
        # Check for examples
        if entry_data.get('examples') and len(entry_data['examples']) > 0:
            score += 1
            
        # Check for cross-references
        if entry_data.get('related_instructions') or entry_data.get('see_also'):
            score += 1
            
        # Check for usage notes
        if entry_data.get('usage_notes'):
            score += 1
            
        # Check for meta-knowledge
        if entry_data.get('special_cases') or entry_data.get('optimization_tips'):
            score += 1
            
        return min(score, 8)
        
    def resolve_conflicts(self, entry_path: Path, conflicts: List[Dict]) -> None:
        """Save conflicts for manual resolution"""
        if not conflicts:
            return
            
        conflict_file = self.conflict_dir / f"{entry_path.stem}_conflicts.yaml"
        conflict_file.parent.mkdir(parents=True, exist_ok=True)
        
        conflict_data = {
            'entry': str(entry_path),
            'timestamp': datetime.now().isoformat(),
            'conflicts': conflicts,
            'resolution_status': 'pending'
        }
        
        with open(conflict_file, 'w') as f:
            yaml.dump(conflict_data, f, default_flow_style=False)
            
        self.propagation_log.append({
            'type': 'conflict',
            'entry': str(entry_path),
            'conflict_count': len(conflicts)
        })
        
    def propagate_update(self, trigger: Dict) -> Dict[str, Any]:
        """Propagate updates from a trigger"""
        results = {
            'processed': 0,
            'updated': 0,
            'conflicts': 0,
            'errors': 0,
            'entries': []
        }
        
        source_file = trigger['source_file']
        affected_entries = trigger.get('affected_entries', [])
        
        print(f"  Processing {len(affected_entries)} affected entries...")
        
        for entry_path_str in affected_entries:
            entry_path = self.repo_path / entry_path_str
            results['processed'] += 1
            
            if not entry_path.exists():
                results['errors'] += 1
                self.propagation_log.append({
                    'type': 'error',
                    'entry': entry_path_str,
                    'error': 'Entry file not found'
                })
                continue
                
            try:
                # Load existing entry
                with open(entry_path, 'r') as f:
                    existing_data = yaml.safe_load(f) or {}
                    
                # Simulate extraction (in production, would call actual extractor)
                # For now, we'll just update metadata
                new_data = {
                    'source_layers': existing_data.get('source_layers', {})
                }
                
                # Mark which source was updated
                if 'CSV' in source_file or 'csv' in source_file:
                    new_data['source_layers']['csv'] = True
                elif 'Datasheet' in source_file or 'datasheet' in source_file:
                    new_data['source_layers']['datasheet'] = True
                elif 'Silicon' in source_file or 'silicon' in source_file:
                    new_data['source_layers']['silicon_doc'] = True
                    
                # Backup before modification
                backup_path = self.backup_entry(entry_path)
                
                # Merge data
                merged_data, conflicts = self.merge_entry_data(
                    existing_data, new_data, source_file
                )
                
                # Save merged data
                with open(entry_path, 'w') as f:
                    yaml.dump(merged_data, f, default_flow_style=False, sort_keys=False)
                    
                results['updated'] += 1
                results['entries'].append({
                    'path': entry_path_str,
                    'backup': str(backup_path),
                    'conflicts': len(conflicts)
                })
                
                # Handle conflicts
                if conflicts:
                    results['conflicts'] += 1
                    self.resolve_conflicts(entry_path, conflicts)
                    
                self.propagation_log.append({
                    'type': 'update',
                    'entry': entry_path_str,
                    'source': source_file,
                    'backup': str(backup_path)
                })
                
            except Exception as e:
                results['errors'] += 1
                self.propagation_log.append({
                    'type': 'error',
                    'entry': entry_path_str,
                    'error': str(e)
                })
                
        return results
        
    def process_all_triggers(self) -> Dict[str, Any]:
        """Process all pending extraction triggers"""
        triggers = self.load_extraction_triggers()
        
        if not triggers:
            print("No pending extraction triggers found.")
            return {'triggers_processed': 0}
            
        print(f"Found {len(triggers)} extraction triggers to process")
        
        all_results = {
            'triggers_processed': 0,
            'total_entries_processed': 0,
            'total_updated': 0,
            'total_conflicts': 0,
            'total_errors': 0,
            'triggers': []
        }
        
        for trigger in triggers:
            print(f"\nProcessing trigger: {trigger['source_file']}")
            results = self.propagate_update(trigger)
            
            all_results['triggers_processed'] += 1
            all_results['total_entries_processed'] += results['processed']
            all_results['total_updated'] += results['updated']
            all_results['total_conflicts'] += results['conflicts']
            all_results['total_errors'] += results['errors']
            
            all_results['triggers'].append({
                'source': trigger['source_file'],
                'results': results
            })
            
            # Archive processed trigger
            if 'trigger_file' in trigger:
                archive_dir = self.trigger_dir / "processed"
                archive_dir.mkdir(exist_ok=True)
                trigger['trigger_file'].rename(
                    archive_dir / trigger['trigger_file'].name
                )
                
        return all_results
        
    def generate_propagation_report(self, results: Dict[str, Any]) -> str:
        """Generate propagation report"""
        report = f"""# Update Propagation Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Triggers Processed**: {results['triggers_processed']}
- **Entries Processed**: {results['total_entries_processed']}
- **Entries Updated**: {results['total_updated']}
- **Conflicts Found**: {results['total_conflicts']}
- **Errors**: {results['total_errors']}

## Trigger Details
"""
        
        for trigger_result in results.get('triggers', []):
            source = trigger_result['source']
            res = trigger_result['results']
            report += f"""
### Source: `{source}`
- Entries Processed: {res['processed']}
- Updated: {res['updated']}
- Conflicts: {res['conflicts']}
- Errors: {res['errors']}
"""
            
        # Add propagation log
        if self.propagation_log:
            report += "\n## Detailed Log\n"
            for log_entry in self.propagation_log[:50]:  # Limit to 50 entries
                if log_entry['type'] == 'update':
                    report += f"- ✅ Updated: `{log_entry['entry']}`\n"
                elif log_entry['type'] == 'conflict':
                    report += f"- ⚠️ Conflict: `{log_entry['entry']}` ({log_entry['conflict_count']} conflicts)\n"
                elif log_entry['type'] == 'error':
                    report += f"- ❌ Error: `{log_entry['entry']}` - {log_entry['error']}\n"
                    
        # Add action items
        if results['total_conflicts'] > 0:
            report += f"""
## Action Required
- **Resolve {results['total_conflicts']} conflicts** in `update-tracking/conflicts/`
"""
        
        if results['total_errors'] > 0:
            report += f"- **Review {results['total_errors']} errors** and retry failed updates\n"
            
        return report
        
    def run(self) -> None:
        """Run the update propagation process"""
        print("🔄 Starting update propagation...")
        
        # Process all triggers
        results = self.process_all_triggers()
        
        if results['triggers_processed'] > 0:
            # Generate report
            report = self.generate_propagation_report(results)
            
            # Save report
            report_file = self.repo_path / "update-tracking" / "reports" / \
                         f"propagation-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            report_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(report_file, 'w') as f:
                f.write(report)
                
            print(f"\n📄 Report saved: {report_file.name}")
            
            # Print summary
            print("\n📊 Propagation Summary:")
            print(f"  Triggers: {results['triggers_processed']}")
            print(f"  Updated: {results['total_updated']}/{results['total_entries_processed']}")
            if results['total_conflicts'] > 0:
                print(f"  ⚠️ Conflicts: {results['total_conflicts']}")
            if results['total_errors'] > 0:
                print(f"  ❌ Errors: {results['total_errors']}")
                

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="P2 Knowledge Base Update Propagation")
    parser.add_argument('--repo-path', default='.', help='Repository root path')
    parser.add_argument('--dry-run', action='store_true', help='Simulate without making changes')
    args = parser.parse_args()
    
    propagator = UpdatePropagator(args.repo_path)
    propagator.run()
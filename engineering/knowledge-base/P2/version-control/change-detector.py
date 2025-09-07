#!/usr/bin/env python3
"""
P2 Knowledge Base Change Detection System
Identifies changes in source documents and affected repository entries
Version: 1.0.0
"""

import os
import yaml
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict

class ChangeDetector:
    """Detects changes in source documents and repository entries"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.source_hashes_file = self.repo_path / "update-tracking" / "source-hashes.json"
        self.entry_hashes_file = self.repo_path / "update-tracking" / "entry-hashes.json"
        self.changes = {
            'sources': [],
            'entries': [],
            'dependencies': []
        }
        
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file"""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"Error hashing {file_path}: {e}")
            return ""
            
    def load_previous_hashes(self, hash_file: Path) -> Dict[str, str]:
        """Load previously stored file hashes"""
        if hash_file.exists():
            with open(hash_file, 'r') as f:
                return json.load(f)
        return {}
        
    def save_hashes(self, hashes: Dict[str, str], hash_file: Path) -> None:
        """Save current file hashes"""
        hash_file.parent.mkdir(parents=True, exist_ok=True)
        with open(hash_file, 'w') as f:
            json.dump(hashes, f, indent=2)
            
    def detect_source_changes(self) -> List[Dict]:
        """Detect changes in source documents"""
        source_patterns = [
            "sources/**/*.csv",
            "sources/**/*.md",
            "external-inputs/**/*.docx",
            "external-inputs/**/*.xlsx"
        ]
        
        current_hashes = {}
        changed_sources = []
        
        # Calculate current hashes
        for pattern in source_patterns:
            for file_path in self.repo_path.glob(pattern):
                rel_path = str(file_path.relative_to(self.repo_path))
                current_hashes[rel_path] = self.calculate_file_hash(file_path)
                
        # Load previous hashes
        previous_hashes = self.load_previous_hashes(self.source_hashes_file)
        
        # Compare hashes
        for file_path, current_hash in current_hashes.items():
            if file_path not in previous_hashes:
                changed_sources.append({
                    'file': file_path,
                    'change_type': 'added',
                    'hash': current_hash
                })
            elif previous_hashes[file_path] != current_hash:
                changed_sources.append({
                    'file': file_path,
                    'change_type': 'modified',
                    'old_hash': previous_hashes[file_path],
                    'new_hash': current_hash
                })
                
        # Check for deleted files
        for file_path in previous_hashes:
            if file_path not in current_hashes:
                changed_sources.append({
                    'file': file_path,
                    'change_type': 'deleted',
                    'old_hash': previous_hashes[file_path]
                })
                
        # Save current hashes for next run
        self.save_hashes(current_hashes, self.source_hashes_file)
        
        self.changes['sources'] = changed_sources
        return changed_sources
        
    def detect_entry_changes(self) -> List[Dict]:
        """Detect changes in repository entries"""
        entry_patterns = [
            "instructions/**/*.yaml",
            "components/**/*.yaml",
            "architecture/*.yaml",
            "hardware/*.yaml"
        ]
        
        current_hashes = {}
        changed_entries = []
        
        # Calculate current hashes
        for pattern in entry_patterns:
            for file_path in self.repo_path.glob(pattern):
                rel_path = str(file_path.relative_to(self.repo_path))
                current_hashes[rel_path] = self.calculate_file_hash(file_path)
                
        # Load previous hashes
        previous_hashes = self.load_previous_hashes(self.entry_hashes_file)
        
        # Compare hashes
        for file_path, current_hash in current_hashes.items():
            if file_path not in previous_hashes:
                changed_entries.append({
                    'file': file_path,
                    'change_type': 'added',
                    'hash': current_hash,
                    'needs_audit': True
                })
            elif previous_hashes[file_path] != current_hash:
                # Load the entry to check what changed
                full_path = self.repo_path / file_path
                with open(full_path, 'r') as f:
                    entry_data = yaml.safe_load(f)
                    
                changed_entries.append({
                    'file': file_path,
                    'change_type': 'modified',
                    'old_hash': previous_hashes[file_path],
                    'new_hash': current_hash,
                    'completeness_score': entry_data.get('completeness_score', 0),
                    'needs_audit': True
                })
                
        # Check for deleted files
        for file_path in previous_hashes:
            if file_path not in current_hashes:
                changed_entries.append({
                    'file': file_path,
                    'change_type': 'deleted',
                    'old_hash': previous_hashes[file_path]
                })
                
        # Save current hashes for next run
        self.save_hashes(current_hashes, self.entry_hashes_file)
        
        self.changes['entries'] = changed_entries
        return changed_entries
        
    def map_sources_to_entries(self) -> Dict[str, List[str]]:
        """Map source documents to affected repository entries"""
        source_mapping = {
            'P2-Instruction-Set.csv': 'instructions/pasm2/',
            'P2-Datasheet': 'instructions/',
            'Silicon-Doc': 'instructions/',
            'Spin2': 'instructions/spin2/',
            'Smart-Pins': 'components/smart-pins/',
            'P2-EVAL': 'hardware/'
        }
        
        affected_entries = defaultdict(list)
        
        for source_change in self.changes['sources']:
            source_file = source_change['file']
            
            # Find matching patterns
            for pattern, entry_dir in source_mapping.items():
                if pattern.lower() in source_file.lower():
                    # Find all entries in that directory
                    entry_path = self.repo_path / entry_dir
                    if entry_path.exists():
                        for entry_file in entry_path.glob("**/*.yaml"):
                            rel_path = str(entry_file.relative_to(self.repo_path))
                            affected_entries[source_file].append(rel_path)
                            
        return dict(affected_entries)
        
    def identify_dependencies(self) -> List[Dict]:
        """Identify entries that depend on changed entries"""
        dependencies = []
        changed_entry_ids = set()
        
        # Get IDs of changed entries
        for entry_change in self.changes['entries']:
            if entry_change['change_type'] != 'deleted':
                file_path = self.repo_path / entry_change['file']
                try:
                    with open(file_path, 'r') as f:
                        data = yaml.safe_load(f)
                        if data and 'id' in data:
                            changed_entry_ids.add(data['id'])
                except:
                    pass
                    
        # Check all entries for dependencies on changed entries
        for pattern in ["instructions/**/*.yaml", "components/**/*.yaml"]:
            for file_path in self.repo_path.glob(pattern):
                try:
                    with open(file_path, 'r') as f:
                        data = yaml.safe_load(f)
                        if data:
                            entry_id = data.get('id', '')
                            
                            # Check related instructions
                            if 'related_instructions' in data:
                                for related in data['related_instructions']:
                                    related_id = f"{related.lower()}-instruction"
                                    if related_id in changed_entry_ids:
                                        dependencies.append({
                                            'entry': entry_id,
                                            'depends_on': related_id,
                                            'field': 'related_instructions',
                                            'file': str(file_path.relative_to(self.repo_path))
                                        })
                                        
                            # Check see_also references
                            if 'see_also' in data:
                                for ref in data['see_also']:
                                    if ref in changed_entry_ids:
                                        dependencies.append({
                                            'entry': entry_id,
                                            'depends_on': ref,
                                            'field': 'see_also',
                                            'file': str(file_path.relative_to(self.repo_path))
                                        })
                except:
                    pass
                    
        self.changes['dependencies'] = dependencies
        return dependencies
        
    def generate_update_report(self) -> str:
        """Generate a comprehensive update report"""
        report = f"""# P2 Knowledge Base Update Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Source Document Changes
"""
        
        if self.changes['sources']:
            for change in self.changes['sources']:
                icon = {'added': '🆕', 'modified': '📝', 'deleted': '🗑️'}.get(
                    change['change_type'], '❓'
                )
                report += f"- {icon} **{change['change_type'].title()}**: `{change['file']}`\n"
        else:
            report += "No source document changes detected.\n"
            
        report += f"""
## Repository Entry Changes
"""
        
        if self.changes['entries']:
            # Group by change type
            by_type = defaultdict(list)
            for change in self.changes['entries']:
                by_type[change['change_type']].append(change)
                
            for change_type, entries in by_type.items():
                report += f"\n### {change_type.title()} ({len(entries)} entries)\n"
                for entry in entries[:10]:  # Limit to first 10
                    report += f"- `{entry['file']}`"
                    if 'completeness_score' in entry:
                        report += f" (score: {entry['completeness_score']})"
                    report += "\n"
                if len(entries) > 10:
                    report += f"- ... and {len(entries) - 10} more\n"
        else:
            report += "No repository entry changes detected.\n"
            
        report += f"""
## Affected Dependencies
"""
        
        if self.changes['dependencies']:
            report += f"Found {len(self.changes['dependencies'])} entries with dependencies on changed entries:\n\n"
            for dep in self.changes['dependencies'][:10]:
                report += f"- `{dep['entry']}` depends on `{dep['depends_on']}` (via {dep['field']})\n"
            if len(self.changes['dependencies']) > 10:
                report += f"- ... and {len(self.changes['dependencies']) - 10} more\n"
        else:
            report += "No dependent entries affected.\n"
            
        # Add action items
        report += """
## Recommended Actions

"""
        
        if self.changes['sources']:
            report += "1. **Re-extraction needed** for updated source documents\n"
            
        if self.changes['entries']:
            needs_audit = sum(1 for e in self.changes['entries'] 
                            if e.get('needs_audit', False))
            if needs_audit > 0:
                report += f"2. **Audit required** for {needs_audit} modified entries\n"
                
        if self.changes['dependencies']:
            report += f"3. **Review dependencies** for {len(self.changes['dependencies'])} affected entries\n"
            
        return report
        
    def generate_extraction_triggers(self) -> None:
        """Generate extraction trigger files for changed sources"""
        if not self.changes['sources']:
            return
            
        trigger_dir = self.repo_path / "update-tracking" / "extraction-triggers"
        trigger_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for source_change in self.changes['sources']:
            if source_change['change_type'] != 'deleted':
                # Create trigger file
                source_name = Path(source_change['file']).stem
                trigger_file = trigger_dir / f"extract-{source_name}-{timestamp}.yaml"
                
                trigger_data = {
                    'trigger_time': datetime.now().isoformat(),
                    'source_file': source_change['file'],
                    'change_type': source_change['change_type'],
                    'new_hash': source_change.get('new_hash', ''),
                    'affected_entries': []
                }
                
                # Add affected entries
                mapping = self.map_sources_to_entries()
                if source_change['file'] in mapping:
                    trigger_data['affected_entries'] = mapping[source_change['file']]
                    
                with open(trigger_file, 'w') as f:
                    yaml.dump(trigger_data, f, default_flow_style=False)
                    
                print(f"Created extraction trigger: {trigger_file.name}")
                
    def run_full_detection(self) -> Dict:
        """Run complete change detection process"""
        print("🔍 Running change detection...")
        
        # Detect changes
        print("  Checking source documents...")
        self.detect_source_changes()
        
        print("  Checking repository entries...")
        self.detect_entry_changes()
        
        print("  Identifying dependencies...")
        self.identify_dependencies()
        
        # Generate outputs
        print("  Generating update report...")
        report = self.generate_update_report()
        
        # Save report
        report_file = self.repo_path / "update-tracking" / "reports" / \
                     f"update-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w') as f:
            f.write(report)
            
        print(f"  Report saved: {report_file.name}")
        
        # Generate extraction triggers
        if self.changes['sources']:
            print("  Generating extraction triggers...")
            self.generate_extraction_triggers()
            
        # Summary
        print("\n📊 Change Detection Summary:")
        print(f"  Source changes: {len(self.changes['sources'])}")
        print(f"  Entry changes: {len(self.changes['entries'])}")
        print(f"  Affected dependencies: {len(self.changes['dependencies'])}")
        
        return self.changes
        

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="P2 Knowledge Base Change Detection")
    parser.add_argument('--repo-path', default='.', help='Repository root path')
    parser.add_argument('--watch', action='store_true', help='Watch for changes continuously')
    args = parser.parse_args()
    
    detector = ChangeDetector(args.repo_path)
    
    if args.watch:
        import time
        print("👁️ Watching for changes (Ctrl+C to stop)...")
        while True:
            detector.run_full_detection()
            print("\nWaiting 60 seconds before next check...")
            time.sleep(60)
    else:
        detector.run_full_detection()
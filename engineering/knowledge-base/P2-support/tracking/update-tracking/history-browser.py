#!/usr/bin/env python3
"""
P2 Knowledge Base History Browser
Explores and visualizes the evolution of repository entries over time
Version: 1.0.0
"""

import os
import yaml
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import seaborn as sns

class HistoryBrowser:
    """Browse and visualize entry evolution history"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.entries = {}
        self.global_timeline = []
        
    def load_entry_history(self, entry_file: Path) -> Dict[str, Any]:
        """Load historical tracking data from an entry YAML file"""
        with open(entry_file, 'r') as f:
            data = yaml.safe_load(f)
        
        # Extract historical tracking if present
        if 'historical_tracking' in data:
            return data['historical_tracking']
        
        # Fall back to basic metadata if enhanced tracking not present
        return self._extract_basic_history(data)
    
    def _extract_basic_history(self, data: Dict) -> Dict[str, Any]:
        """Extract basic history from existing metadata structure"""
        basic_history = {
            'entry_id': data.get('metadata', {}).get('id', 'unknown'),
            'version_history': [],
            'source_attribution': {},
            'quality_progression': {'completeness_history': []}
        }
        
        # Extract layer information as version history
        layers = ['layer1_csv', 'layer2_datasheet', 'layer3_silicon_doc', 'layer4_clarifications']
        for i, layer in enumerate(layers):
            if layer in data:
                layer_data = data[layer]
                if 'extraction_date' in layer_data:
                    basic_history['version_history'].append({
                        'version_number': f"1.{i}.0",
                        'timestamp': layer_data['extraction_date'],
                        'change_type': 'enhancement',
                        'trigger_source': f"{layer} integration",
                        'updated_by': 'extraction-pipeline'
                    })
        
        return basic_history
    
    def scan_repository(self) -> None:
        """Scan repository for all entries and load their histories"""
        print("Scanning repository for entries...")
        
        # Scan instruction files
        for yaml_file in self.repo_path.glob("instructions/**/*.yaml"):
            try:
                history = self.load_entry_history(yaml_file)
                self.entries[history['entry_id']] = history
            except Exception as e:
                print(f"Error loading {yaml_file}: {e}")
        
        # Scan component files
        for yaml_file in self.repo_path.glob("components/**/*.yaml"):
            try:
                history = self.load_entry_history(yaml_file)
                self.entries[history['entry_id']] = history
            except Exception as e:
                print(f"Error loading {yaml_file}: {e}")
                
        print(f"Loaded {len(self.entries)} entries")
    
    def build_global_timeline(self) -> None:
        """Build chronological timeline of all changes across repository"""
        timeline_events = []
        
        for entry_id, entry_data in self.entries.items():
            version_history = entry_data.get('version_history', [])
            
            for version in version_history:
                timeline_events.append({
                    'timestamp': version.get('timestamp'),
                    'entry_id': entry_id,
                    'version': version.get('version_number'),
                    'change_type': version.get('change_type'),
                    'trigger_source': version.get('trigger_source'),
                    'completeness_change': self._get_completeness_change(entry_data, version.get('timestamp'))
                })
        
        # Sort by timestamp
        timeline_events.sort(key=lambda x: x['timestamp'] if x['timestamp'] else '')
        self.global_timeline = timeline_events
    
    def _get_completeness_change(self, entry_data: Dict, timestamp: str) -> Tuple[int, int]:
        """Get completeness score change at a given timestamp"""
        completeness_history = entry_data.get('quality_progression', {}).get('completeness_history', [])
        
        for i, record in enumerate(completeness_history):
            if record.get('date') == timestamp:
                old_score = 0
                if i > 0:
                    old_score = completeness_history[i-1].get('score', 0)
                return (old_score, record.get('score', 0))
        
        return (0, 0)
    
    def show_entry_evolution(self, entry_id: str) -> None:
        """Display detailed evolution of a specific entry"""
        if entry_id not in self.entries:
            print(f"Entry '{entry_id}' not found")
            return
            
        entry = self.entries[entry_id]
        print(f"\n=== Evolution of {entry_id} ===\n")
        
        version_history = entry.get('version_history', [])
        for version in version_history:
            print(f"Version: {version.get('version_number')}")
            print(f"Date: {version.get('timestamp')}")
            print(f"Change Type: {version.get('change_type')}")
            print(f"Trigger: {version.get('trigger_source')}")
            print(f"Updated By: {version.get('updated_by')}")
            
            changes = version.get('changes_made', [])
            if changes:
                print("Changes:")
                for change in changes:
                    print(f"  • {change.get('field')}: {change.get('change_type')}")
                    if change.get('rationale'):
                        print(f"    Rationale: {change.get('rationale')}")
            
            progression = version.get('completeness_progression', {})
            if progression:
                print(f"Completeness: {progression.get('old_score', 0)} → {progression.get('new_score', 0)}")
                
            print("-" * 50)
    
    def visualize_quality_progression(self, entry_id: str) -> None:
        """Create visualization of quality progression over time"""
        if entry_id not in self.entries:
            print(f"Entry '{entry_id}' not found")
            return
            
        entry = self.entries[entry_id]
        completeness_history = entry.get('quality_progression', {}).get('completeness_history', [])
        
        if not completeness_history:
            print(f"No quality progression data for {entry_id}")
            return
        
        dates = []
        scores = []
        
        for record in completeness_history:
            try:
                date = datetime.fromisoformat(record['date'].replace('Z', '+00:00'))
                dates.append(date)
                scores.append(record['score'])
            except:
                continue
                
        if not dates:
            print(f"No valid date data for {entry_id}")
            return
        
        plt.figure(figsize=(12, 6))
        plt.plot(dates, scores, 'o-', linewidth=2, markersize=8)
        plt.title(f"Quality Progression: {entry_id}")
        plt.xlabel("Date")
        plt.ylabel("Completeness Score")
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 10)
        
        # Add annotations for major changes
        for i, (date, score) in enumerate(zip(dates, scores)):
            if i > 0 and scores[i] - scores[i-1] >= 2:
                plt.annotate(f"Score: {score}", (date, score), 
                           xytext=(10, 10), textcoords='offset points',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        
        plt.tight_layout()
        plt.show()
    
    def repository_overview_dashboard(self) -> None:
        """Create dashboard showing repository-wide evolution metrics"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Updates over time
        if self.global_timeline:
            dates = []
            for event in self.global_timeline:
                try:
                    date = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                    dates.append(date)
                except:
                    continue
            
            if dates:
                # Group by month
                monthly_counts = defaultdict(int)
                for date in dates:
                    month_key = date.replace(day=1)
                    monthly_counts[month_key] += 1
                
                months = sorted(monthly_counts.keys())
                counts = [monthly_counts[month] for month in months]
                
                ax1.bar(months, counts)
                ax1.set_title("Updates Over Time")
                ax1.set_xlabel("Month")
                ax1.set_ylabel("Number of Updates")
                ax1.tick_params(axis='x', rotation=45)
        
        # 2. Change type distribution
        change_types = defaultdict(int)
        for event in self.global_timeline:
            change_types[event.get('change_type', 'unknown')] += 1
        
        if change_types:
            ax2.pie(change_types.values(), labels=change_types.keys(), autopct='%1.1f%%')
            ax2.set_title("Change Type Distribution")
        
        # 3. Completeness score distribution
        current_scores = []
        for entry in self.entries.values():
            completeness_history = entry.get('quality_progression', {}).get('completeness_history', [])
            if completeness_history:
                current_scores.append(completeness_history[-1].get('score', 0))
        
        if current_scores:
            ax3.hist(current_scores, bins=range(11), edgecolor='black')
            ax3.set_title("Current Completeness Score Distribution")
            ax3.set_xlabel("Completeness Score")
            ax3.set_ylabel("Number of Entries")
            ax3.set_xticks(range(10))
        
        # 4. Source contribution analysis
        source_contributions = defaultdict(int)
        for event in self.global_timeline:
            trigger = event.get('trigger_source', 'unknown')
            if 'CSV' in trigger or 'csv' in trigger:
                source_contributions['CSV'] += 1
            elif 'Datasheet' in trigger or 'datasheet' in trigger:
                source_contributions['Datasheet'] += 1
            elif 'Silicon Doc' in trigger or 'silicon' in trigger:
                source_contributions['Silicon Doc'] += 1
            elif 'Chip' in trigger or 'clarification' in trigger:
                source_contributions['Chip Clarifications'] += 1
            else:
                source_contributions['Other'] += 1
        
        if source_contributions:
            ax4.bar(source_contributions.keys(), source_contributions.values())
            ax4.set_title("Source Contribution Analysis")
            ax4.set_xlabel("Source Type")
            ax4.set_ylabel("Number of Contributions")
            ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def find_entries_by_criteria(self, **criteria) -> List[str]:
        """Find entries matching specific criteria"""
        matching_entries = []
        
        for entry_id, entry_data in self.entries.items():
            match = True
            
            # Check completeness score
            if 'min_completeness' in criteria:
                completeness_history = entry_data.get('quality_progression', {}).get('completeness_history', [])
                if completeness_history:
                    current_score = completeness_history[-1].get('score', 0)
                    if current_score < criteria['min_completeness']:
                        match = False
                else:
                    match = False
            
            # Check last update date
            if 'updated_since' in criteria:
                version_history = entry_data.get('version_history', [])
                if version_history:
                    try:
                        last_update = datetime.fromisoformat(version_history[-1]['timestamp'].replace('Z', '+00:00'))
                        since_date = datetime.fromisoformat(criteria['updated_since'])
                        if last_update < since_date:
                            match = False
                    except:
                        match = False
                else:
                    match = False
            
            # Check source attribution
            if 'has_source' in criteria:
                source_attribution = entry_data.get('source_attribution', {})
                if criteria['has_source'] not in str(source_attribution):
                    match = False
            
            if match:
                matching_entries.append(entry_id)
        
        return matching_entries
    
    def generate_evolution_report(self, output_file: str = None) -> None:
        """Generate comprehensive evolution report"""
        report = []
        report.append("# P2 Knowledge Base Evolution Report")
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append(f"Total Entries: {len(self.entries)}")
        report.append(f"Total Updates: {len(self.global_timeline)}")
        report.append("")
        
        # Repository statistics
        report.append("## Repository Statistics")
        report.append("")
        
        # Completeness distribution
        score_distribution = defaultdict(int)
        for entry in self.entries.values():
            completeness_history = entry.get('quality_progression', {}).get('completeness_history', [])
            if completeness_history:
                score = completeness_history[-1].get('score', 0)
                score_distribution[score] += 1
        
        report.append("### Completeness Score Distribution")
        for score in sorted(score_distribution.keys()):
            count = score_distribution[score]
            percentage = (count / len(self.entries)) * 100
            report.append(f"Score {score}: {count} entries ({percentage:.1f}%)")
        report.append("")
        
        # Recent activity
        report.append("### Recent Activity (Last 30 Days)")
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_updates = []
        
        for event in self.global_timeline:
            try:
                event_date = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                if event_date > thirty_days_ago:
                    recent_updates.append(event)
            except:
                continue
        
        report.append(f"Total recent updates: {len(recent_updates)}")
        
        # Group by change type
        recent_by_type = defaultdict(int)
        for event in recent_updates:
            recent_by_type[event.get('change_type', 'unknown')] += 1
        
        for change_type, count in recent_by_type.items():
            report.append(f"- {change_type}: {count}")
        report.append("")
        
        # Top evolving entries
        report.append("### Most Actively Updated Entries")
        entry_update_counts = defaultdict(int)
        for event in self.global_timeline:
            entry_update_counts[event['entry_id']] += 1
        
        top_entries = sorted(entry_update_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        for entry_id, count in top_entries:
            report.append(f"- {entry_id}: {count} updates")
        report.append("")
        
        # Source contribution summary
        report.append("### Source Contributions")
        source_stats = defaultdict(int)
        for event in self.global_timeline:
            trigger = event.get('trigger_source', 'unknown')
            if 'CSV' in trigger or 'csv' in trigger:
                source_stats['CSV Extractions'] += 1
            elif 'Datasheet' in trigger or 'datasheet' in trigger:
                source_stats['Datasheet Enhancements'] += 1
            elif 'Silicon Doc' in trigger or 'silicon' in trigger:
                source_stats['Silicon Doc Integrations'] += 1
            elif 'Chip' in trigger or 'clarification' in trigger:
                source_stats['Chip Clarifications'] += 1
            elif 'meta-knowledge' in trigger.lower():
                source_stats['Meta-knowledge Additions'] += 1
            else:
                source_stats['Other Updates'] += 1
        
        for source_type, count in sorted(source_stats.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(self.global_timeline)) * 100
            report.append(f"- {source_type}: {count} ({percentage:.1f}%)")
        
        report_text = "\n".join(report)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
            print(f"Evolution report written to: {output_file}")
        else:
            print(report_text)

def main():
    """Main function for interactive history browser"""
    repo_path = "/path/to/P2-Knowledge-Base/engineering/knowledge-base/P2"
    browser = HistoryBrowser(repo_path)
    
    print("P2 Knowledge Base History Browser")
    print("=" * 40)
    
    # Load repository data
    browser.scan_repository()
    browser.build_global_timeline()
    
    while True:
        print("\nOptions:")
        print("1. View entry evolution")
        print("2. Visualize quality progression")
        print("3. Repository overview dashboard")
        print("4. Find entries by criteria")
        print("5. Generate evolution report")
        print("6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            entry_id = input("Enter entry ID: ").strip()
            browser.show_entry_evolution(entry_id)
            
        elif choice == "2":
            entry_id = input("Enter entry ID: ").strip()
            browser.visualize_quality_progression(entry_id)
            
        elif choice == "3":
            browser.repository_overview_dashboard()
            
        elif choice == "4":
            min_score = input("Minimum completeness score (or Enter to skip): ").strip()
            criteria = {}
            if min_score:
                criteria['min_completeness'] = int(min_score)
            
            matching = browser.find_entries_by_criteria(**criteria)
            print(f"Found {len(matching)} matching entries:")
            for entry_id in matching[:20]:  # Show first 20
                print(f"- {entry_id}")
                
        elif choice == "5":
            output_file = input("Output file (or Enter for console): ").strip()
            browser.generate_evolution_report(output_file if output_file else None)
            
        elif choice == "6":
            break
            
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
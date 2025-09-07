#!/usr/bin/env python3
"""
P2 Knowledge Base Conflict Detector
Automatically detects conflicts between sources, versions, and extraction runs
Version: 1.0.0
"""

import os
import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict
import re

class ConflictDetector:
    """Detect conflicts between sources and versions"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.conflicts = []
        self.conflict_id_counter = 1
        self.authority_hierarchy = {
            'ABSOLUTE': 4,
            'SILICON_DOC_VERIFIED': 3,
            'DATASHEET_CONFIRMED': 2,
            'CSV_EXTRACTED': 1
        }
        
    def generate_conflict_id(self) -> str:
        """Generate unique conflict identifier"""
        today = datetime.now().strftime('%Y-%m-%d')
        conflict_id = f"CONF-{today}-{self.conflict_id_counter:03d}"
        self.conflict_id_counter += 1
        return conflict_id
    
    def load_entry(self, entry_file: Path) -> Dict[str, Any]:
        """Load entry YAML file"""
        try:
            with open(entry_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading {entry_file}: {e}")
            return {}
    
    def extract_field_sources(self, entry_data: Dict) -> Dict[str, Dict[str, Any]]:
        """Extract fields by source layer with authority levels"""
        field_sources = {}
        
        # Layer 1: CSV
        if 'layer1_csv' in entry_data:
            layer_data = entry_data['layer1_csv']
            for field, value in layer_data.items():
                if field != 'extraction_date':
                    field_sources[field] = field_sources.get(field, {})
                    field_sources[field]['CSV_EXTRACTED'] = {
                        'value': value,
                        'source': 'layer1_csv',
                        'authority': 1,
                        'date': layer_data.get('extraction_date', '')
                    }
        
        # Layer 2: Datasheet
        if 'layer2_datasheet' in entry_data:
            layer_data = entry_data['layer2_datasheet']
            for field, value in layer_data.items():
                if field not in ['extraction_date', 'source']:
                    field_sources[field] = field_sources.get(field, {})
                    field_sources[field]['DATASHEET_CONFIRMED'] = {
                        'value': value,
                        'source': 'layer2_datasheet',
                        'authority': 2,
                        'date': layer_data.get('extraction_date', '')
                    }
        
        # Layer 3: Silicon Doc
        if 'layer3_silicon_doc' in entry_data:
            layer_data = entry_data['layer3_silicon_doc']
            for field, value in layer_data.items():
                if field not in ['extraction_date', 'source', 'parts_used']:
                    field_sources[field] = field_sources.get(field, {})
                    field_sources[field]['SILICON_DOC_VERIFIED'] = {
                        'value': value,
                        'source': 'layer3_silicon_doc',
                        'authority': 3,
                        'date': layer_data.get('extraction_date', '')
                    }
        
        # Layer 4: Chip Clarifications
        if 'layer4_clarifications' in entry_data:
            layer_data = entry_data['layer4_clarifications']
            for field, value in layer_data.items():
                if field not in ['extraction_date', 'source_posts', 'authority_level']:
                    field_sources[field] = field_sources.get(field, {})
                    field_sources[field]['ABSOLUTE'] = {
                        'value': value,
                        'source': 'layer4_clarifications',
                        'authority': 4,
                        'date': layer_data.get('extraction_date', '')
                    }
        
        return field_sources
    
    def detect_direct_contradictions(self, entry_id: str, field_sources: Dict) -> List[Dict]:
        """Detect direct contradictions between sources"""
        conflicts = []
        
        for field, sources in field_sources.items():
            if len(sources) < 2:
                continue
                
            # Compare all pairs of sources
            source_items = list(sources.items())
            for i in range(len(source_items)):
                for j in range(i + 1, len(source_items)):
                    source1_name, source1_data = source_items[i]
                    source2_name, source2_data = source_items[j]
                    
                    value1 = source1_data['value']
                    value2 = source2_data['value']
                    
                    # Check for contradiction
                    if self._values_conflict(value1, value2):
                        severity = self._assess_conflict_severity(field, value1, value2)
                        
                        conflict = {
                            'conflict_id': self.generate_conflict_id(),
                            'entry_id': entry_id,
                            'conflict_type': 'direct_contradiction',
                            'field': field,
                            'severity': severity,
                            'conflicting_sources': [
                                {
                                    'source': source1_name,
                                    'authority': source1_data['authority'],
                                    'value': value1,
                                    'date': source1_data['date']
                                },
                                {
                                    'source': source2_name,
                                    'authority': source2_data['authority'],
                                    'value': value2,
                                    'date': source2_data['date']
                                }
                            ],
                            'detected_date': datetime.now().isoformat(),
                            'detection_method': 'automated'
                        }
                        conflicts.append(conflict)
        
        return conflicts
    
    def _values_conflict(self, value1: Any, value2: Any) -> bool:
        """Determine if two values represent a conflict"""
        # Handle None values
        if value1 is None or value2 is None:
            return False
        
        # Convert to strings for comparison
        str1 = str(value1).strip().lower()
        str2 = str(value2).strip().lower()
        
        # Same values don't conflict
        if str1 == str2:
            return False
        
        # Check for numeric conflicts
        if self._is_numeric_conflict(str1, str2):
            return True
        
        # Check for boolean conflicts
        if self._is_boolean_conflict(str1, str2):
            return True
        
        # Check for semantic conflicts in descriptions
        if self._is_semantic_conflict(str1, str2):
            return True
        
        return False
    
    def _is_numeric_conflict(self, str1: str, str2: str) -> bool:
        """Check for numeric value conflicts"""
        # Extract numbers from strings
        nums1 = re.findall(r'\d+(?:\.\d+)?', str1)
        nums2 = re.findall(r'\d+(?:\.\d+)?', str2)
        
        if not nums1 or not nums2:
            return False
        
        # Simple case: single numbers that are different
        if len(nums1) == 1 and len(nums2) == 1:
            try:
                n1 = float(nums1[0])
                n2 = float(nums2[0])
                # Different numbers conflict unless one is a range containing the other
                if n1 != n2:
                    # Check if one might be a more precise version
                    return not self._is_precision_refinement(str1, str2, n1, n2)
            except ValueError:
                pass
        
        return False
    
    def _is_precision_refinement(self, str1: str, str2: str, n1: float, n2: float) -> bool:
        """Check if one value is a precision refinement of another"""
        # Common patterns: "2 cycles" vs "2-9 cycles"
        if '-' in str1 or '-' in str2:
            # One is a range, check if the other is within range
            range_str = str1 if '-' in str1 else str2
            single_str = str2 if '-' in str1 else str1
            
            range_nums = re.findall(r'\d+(?:\.\d+)?', range_str)
            if len(range_nums) >= 2:
                try:
                    range_min = float(range_nums[0])
                    range_max = float(range_nums[1])
                    single_val = n1 if '-' not in str1 else n2
                    
                    # If single value is within range, it's refinement not conflict
                    return range_min <= single_val <= range_max
                except ValueError:
                    pass
        
        return False
    
    def _is_boolean_conflict(self, str1: str, str2: str) -> bool:
        """Check for boolean conflicts"""
        bool_patterns = {
            'true': ['true', 'yes', 'enabled', 'set'],
            'false': ['false', 'no', 'disabled', 'clear', 'unset']
        }
        
        bool1 = None
        bool2 = None
        
        for bool_val, patterns in bool_patterns.items():
            if any(pattern in str1 for pattern in patterns):
                bool1 = bool_val
            if any(pattern in str2 for pattern in patterns):
                bool2 = bool_val
        
        # If both are boolean and different, it's a conflict
        return bool1 is not None and bool2 is not None and bool1 != bool2
    
    def _is_semantic_conflict(self, str1: str, str2: str) -> bool:
        """Check for semantic conflicts in descriptions"""
        # Look for contradictory keywords
        contradictory_pairs = [
            (['enable', 'set', 'turn on'], ['disable', 'clear', 'turn off']),
            (['increase', 'increment', 'raise'], ['decrease', 'decrement', 'lower']),
            (['fast', 'quick', 'rapid'], ['slow', 'delayed']),
            (['required', 'mandatory', 'must'], ['optional', 'may', 'can']),
        ]
        
        for positive_words, negative_words in contradictory_pairs:
            has_positive1 = any(word in str1 for word in positive_words)
            has_negative1 = any(word in str1 for word in negative_words)
            has_positive2 = any(word in str2 for word in positive_words)
            has_negative2 = any(word in str2 for word in negative_words)
            
            # If one has positive and other has negative for same concept
            if (has_positive1 and has_negative2) or (has_negative1 and has_positive2):
                return True
        
        return False
    
    def _assess_conflict_severity(self, field: str, value1: Any, value2: Any) -> str:
        """Assess severity of detected conflict"""
        # Critical fields that affect fundamental operation
        critical_fields = ['encoding', 'mnemonic', 'operation', 'basic_operation']
        if field in critical_fields:
            return 'critical'
        
        # High priority fields affecting behavior
        high_fields = ['timing', 'flags_affected', 'description', 'syntax']
        if field in high_fields:
            return 'high'
        
        # Medium priority fields affecting understanding
        medium_fields = ['usage_notes', 'examples', 'related_instructions']
        if field in medium_fields:
            return 'medium'
        
        # Low priority presentation differences
        return 'low'
    
    def detect_completeness_conflicts(self, entry_id: str, field_sources: Dict) -> List[Dict]:
        """Detect completeness conflicts (information presence/absence)"""
        conflicts = []
        
        # Look for cases where higher authority source lacks info from lower authority
        for field, sources in field_sources.items():
            if len(sources) < 2:
                continue
            
            # Find highest and lowest authority sources with data
            max_authority = max(src_data['authority'] for src_data in sources.values())
            min_authority = min(src_data['authority'] for src_data in sources.values())
            
            if max_authority == min_authority:
                continue
            
            # Check if lower authority has more detailed information
            max_auth_sources = [src for src, data in sources.items() if data['authority'] == max_authority]
            min_auth_sources = [src for src, data in sources.items() if data['authority'] == min_authority]
            
            for max_src in max_auth_sources:
                for min_src in min_auth_sources:
                    max_value = sources[max_src]['value']
                    min_value = sources[min_src]['value']
                    
                    # Check if lower authority source has more detail
                    if self._is_more_detailed(min_value, max_value):
                        conflict = {
                            'conflict_id': self.generate_conflict_id(),
                            'entry_id': entry_id,
                            'conflict_type': 'completeness_conflict',
                            'field': field,
                            'severity': 'medium',
                            'description': f"Lower authority source has more detailed information",
                            'higher_authority_source': max_src,
                            'lower_authority_source': min_src,
                            'detected_date': datetime.now().isoformat(),
                            'detection_method': 'automated'
                        }
                        conflicts.append(conflict)
        
        return conflicts
    
    def _is_more_detailed(self, detailed_value: Any, basic_value: Any) -> bool:
        """Check if one value is more detailed than another"""
        if detailed_value is None or basic_value is None:
            return False
        
        detailed_str = str(detailed_value)
        basic_str = str(basic_value)
        
        # More detailed if significantly longer and contains the basic info
        if len(detailed_str) > len(basic_str) * 1.5:
            # Check if basic info is contained in detailed
            basic_words = set(basic_str.lower().split())
            detailed_words = set(detailed_str.lower().split())
            
            # If basic words are mostly contained in detailed
            overlap = len(basic_words & detailed_words)
            if overlap / len(basic_words) > 0.7:
                return True
        
        return False
    
    def scan_repository_for_conflicts(self) -> List[Dict]:
        """Scan entire repository for conflicts"""
        print("Scanning repository for conflicts...")
        all_conflicts = []
        
        # Scan instruction files
        instruction_files = list(self.repo_path.glob("instructions/**/*.yaml"))
        print(f"Scanning {len(instruction_files)} instruction files...")
        
        for yaml_file in instruction_files:
            entry_data = self.load_entry(yaml_file)
            if not entry_data:
                continue
            
            entry_id = entry_data.get('metadata', {}).get('id', yaml_file.stem)
            field_sources = self.extract_field_sources(entry_data)
            
            # Detect different types of conflicts
            direct_conflicts = self.detect_direct_contradictions(entry_id, field_sources)
            completeness_conflicts = self.detect_completeness_conflicts(entry_id, field_sources)
            
            all_conflicts.extend(direct_conflicts)
            all_conflicts.extend(completeness_conflicts)
        
        self.conflicts = all_conflicts
        print(f"Detected {len(all_conflicts)} conflicts total")
        
        # Group by severity
        severity_counts = defaultdict(int)
        for conflict in all_conflicts:
            severity_counts[conflict.get('severity', 'unknown')] += 1
        
        print("Conflict breakdown by severity:")
        for severity, count in severity_counts.items():
            print(f"  {severity}: {count}")
        
        return all_conflicts
    
    def save_conflict_log(self, output_file: str = None) -> None:
        """Save detected conflicts to log file"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            output_file = f"conflict-log-{timestamp}.yaml"
        
        conflict_log = {
            'conflict_detection_run': {
                'timestamp': datetime.now().isoformat(),
                'total_conflicts': len(self.conflicts),
                'conflicts': self.conflicts
            }
        }
        
        output_path = self.repo_path / "update-tracking" / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            yaml.dump(conflict_log, f, default_flow_style=False, indent=2)
        
        print(f"Conflict log saved to: {output_path}")
    
    def generate_conflict_report(self) -> str:
        """Generate human-readable conflict report"""
        if not self.conflicts:
            return "No conflicts detected."
        
        report = []
        report.append("# P2 Knowledge Base Conflict Detection Report")
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append(f"Total Conflicts: {len(self.conflicts)}")
        report.append("")
        
        # Group by severity
        severity_groups = defaultdict(list)
        for conflict in self.conflicts:
            severity_groups[conflict.get('severity', 'unknown')].append(conflict)
        
        for severity in ['critical', 'high', 'medium', 'low', 'unknown']:
            if severity not in severity_groups:
                continue
            
            conflicts = severity_groups[severity]
            report.append(f"## {severity.upper()} Conflicts ({len(conflicts)})")
            report.append("")
            
            for conflict in conflicts:
                report.append(f"### {conflict['conflict_id']}")
                report.append(f"**Entry**: {conflict['entry_id']}")
                report.append(f"**Field**: {conflict['field']}")
                report.append(f"**Type**: {conflict['conflict_type']}")
                
                if conflict['conflict_type'] == 'direct_contradiction':
                    report.append("**Conflicting Values**:")
                    for source in conflict['conflicting_sources']:
                        report.append(f"- {source['source']} (authority {source['authority']}): {source['value']}")
                
                report.append("")
        
        return "\n".join(report)

def main():
    """Main function for conflict detection"""
    repo_path = "/path/to/P2-Knowledge-Base/engineering/knowledge-base/P2"
    detector = ConflictDetector(repo_path)
    
    print("P2 Knowledge Base Conflict Detector")
    print("=" * 40)
    
    # Run conflict detection
    conflicts = detector.scan_repository_for_conflicts()
    
    if conflicts:
        # Save conflict log
        detector.save_conflict_log()
        
        # Generate and display report
        report = detector.generate_conflict_report()
        print("\n" + report)
        
        # Offer to save report
        save_report = input("\nSave conflict report to file? (y/n): ").strip().lower()
        if save_report == 'y':
            report_file = input("Report filename (or Enter for default): ").strip()
            if not report_file:
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                report_file = f"conflict-report-{timestamp}.md"
            
            report_path = detector.repo_path / "update-tracking" / report_file
            with open(report_path, 'w') as f:
                f.write(report)
            print(f"Report saved to: {report_path}")
    
    else:
        print("\n✅ No conflicts detected - repository is consistent!")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
P2 Knowledge Base Conflict Resolver
Automatically resolves conflicts using defined resolution strategies
Version: 1.0.0
"""

import os
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import shutil

class ConflictResolver:
    """Resolve conflicts using systematic strategies"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.resolution_log = []
        self.authority_hierarchy = {
            'ABSOLUTE': 4,
            'SILICON_DOC_VERIFIED': 3,
            'DATASHEET_CONFIRMED': 2,
            'CSV_EXTRACTED': 1
        }
        
        # Load conflict resolution rules
        self.resolution_rules = self.load_resolution_rules()
    
    def load_resolution_rules(self) -> Dict[str, Any]:
        """Load conflict resolution system configuration"""
        rules_file = self.repo_path / "update-tracking" / "conflict-resolution-system.yaml"
        if rules_file.exists():
            with open(rules_file, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def load_conflict_log(self, conflict_file: str) -> List[Dict]:
        """Load conflicts from detection log"""
        conflict_path = self.repo_path / "update-tracking" / conflict_file
        if not conflict_path.exists():
            print(f"Conflict file not found: {conflict_path}")
            return []
        
        with open(conflict_path, 'r') as f:
            conflict_data = yaml.safe_load(f)
        
        return conflict_data.get('conflict_detection_run', {}).get('conflicts', [])
    
    def resolve_authority_hierarchy_conflict(self, conflict: Dict) -> Dict[str, Any]:
        """Resolve conflict using authority hierarchy"""
        conflicting_sources = conflict['conflicting_sources']
        
        # Find source with highest authority
        highest_authority = 0
        winning_source = None
        
        for source in conflicting_sources:
            if source['authority'] > highest_authority:
                highest_authority = source['authority']
                winning_source = source
        
        resolution = {
            'resolution_strategy': 'authority_hierarchy_primary',
            'winning_source': winning_source,
            'resolution_rationale': f"Applied authority hierarchy - {winning_source['source']} (authority {highest_authority}) overrides lower authority sources",
            'confidence_level': 'high',
            'automated': True,
            'resolved_value': winning_source['value']
        }
        
        return resolution
    
    def resolve_additive_enhancement_conflict(self, conflict: Dict) -> Dict[str, Any]:
        """Resolve conflict by merging additive information"""
        conflicting_sources = conflict['conflicting_sources']
        
        # Check if information is truly additive
        values = [source['value'] for source in conflicting_sources]
        if self._is_additive_compatible(values):
            # Merge information from all sources
            merged_value = self._merge_additive_values(values, conflicting_sources)
            
            resolution = {
                'resolution_strategy': 'additive_enhancement',
                'merged_sources': [src['source'] for src in conflicting_sources],
                'resolution_rationale': 'Information is compatible and additive - merged all sources',
                'confidence_level': 'high',
                'automated': True,
                'resolved_value': merged_value
            }
        else:
            # Escalate to manual review
            resolution = {
                'resolution_strategy': 'escalate_to_manual',
                'escalation_reason': 'Information appears additive but contains contradictions',
                'confidence_level': 'low',
                'automated': False
            }
        
        return resolution
    
    def resolve_precision_enhancement_conflict(self, conflict: Dict) -> Dict[str, Any]:
        """Resolve conflict by using more precise information"""
        conflicting_sources = conflict['conflicting_sources']
        
        # Find most precise source
        most_precise_source = None
        highest_precision_score = 0
        
        for source in conflicting_sources:
            precision_score = self._calculate_precision_score(source['value'])
            if precision_score > highest_precision_score:
                highest_precision_score = precision_score
                most_precise_source = source
        
        if most_precise_source and self._precision_contains_less_precise(
            most_precise_source['value'], 
            [src['value'] for src in conflicting_sources if src != most_precise_source]
        ):
            resolution = {
                'resolution_strategy': 'precision_enhancement',
                'winning_source': most_precise_source,
                'resolution_rationale': f"More precise information from {most_precise_source['source']} contains less precise versions",
                'confidence_level': 'high',
                'automated': True,
                'resolved_value': most_precise_source['value']
            }
        else:
            # Escalate if precision relationships unclear
            resolution = {
                'resolution_strategy': 'escalate_to_manual',
                'escalation_reason': 'Precision relationships unclear - requires human analysis',
                'confidence_level': 'low',
                'automated': False
            }
        
        return resolution
    
    def _is_additive_compatible(self, values: List[Any]) -> bool:
        """Check if values can be additively combined"""
        # Convert to strings for analysis
        str_values = [str(v) for v in values]
        
        # Check for obvious contradictions
        for i in range(len(str_values)):
            for j in range(i + 1, len(str_values)):
                if self._contains_contradiction(str_values[i], str_values[j]):
                    return False
        
        return True
    
    def _contains_contradiction(self, value1: str, value2: str) -> bool:
        """Check if two string values contain contradictions"""
        v1_lower = value1.lower()
        v2_lower = value2.lower()
        
        # Look for contradictory boolean statements
        bool_contradictions = [
            (['true', 'yes', 'enable'], ['false', 'no', 'disable']),
            (['set', 'high'], ['clear', 'low']),
            (['required', 'must'], ['optional', 'may'])
        ]
        
        for positive, negative in bool_contradictions:
            has_pos_1 = any(word in v1_lower for word in positive)
            has_neg_1 = any(word in v1_lower for word in negative)
            has_pos_2 = any(word in v2_lower for word in positive)
            has_neg_2 = any(word in v2_lower for word in negative)
            
            if (has_pos_1 and has_neg_2) or (has_neg_1 and has_pos_2):
                return True
        
        return False
    
    def _merge_additive_values(self, values: List[Any], sources: List[Dict]) -> str:
        """Merge additive values from multiple sources"""
        merged_parts = []
        source_attribution = []
        
        for i, value in enumerate(values):
            source_name = sources[i]['source']
            authority = sources[i]['authority']
            
            merged_parts.append(str(value))
            source_attribution.append(f"[{source_name}]")
        
        # Create merged value with source attribution
        merged_value = ". ".join(merged_parts)
        attribution = " + ".join(source_attribution)
        
        return f"{merged_value} ({attribution})"
    
    def _calculate_precision_score(self, value: Any) -> int:
        """Calculate precision score for a value"""
        if value is None:
            return 0
        
        value_str = str(value)
        score = 0
        
        # Length contributes to precision
        score += len(value_str) // 10
        
        # Numbers and ranges indicate precision
        if '-' in value_str:  # Range like "2-9"
            score += 10
        
        # Technical terms indicate precision
        technical_terms = ['sync', 'dependent', 'window', 'alignment', 'cycles', 'clocks']
        score += sum(2 for term in technical_terms if term in value_str.lower())
        
        # Parenthetical explanations indicate precision
        if '(' in value_str and ')' in value_str:
            score += 5
        
        return score
    
    def _precision_contains_less_precise(self, precise_value: Any, other_values: List[Any]) -> bool:
        """Check if precise value logically contains less precise values"""
        precise_str = str(precise_value).lower()
        
        for other_value in other_values:
            other_str = str(other_value).lower()
            
            # Check if key terms from less precise version appear in more precise
            other_words = set(other_str.split())
            precise_words = set(precise_str.split())
            
            # If most words from other appear in precise, it's contained
            overlap = len(other_words & precise_words)
            if overlap / len(other_words) < 0.6:  # Less than 60% overlap
                return False
        
        return True
    
    def apply_resolution(self, conflict: Dict, resolution: Dict, entry_file: Path) -> bool:
        """Apply resolution to the actual entry file"""
        try:
            # Load entry
            with open(entry_file, 'r') as f:
                entry_data = yaml.safe_load(f)
            
            if not resolution.get('automated', False):
                return False  # Don't apply manual resolutions automatically
            
            # Create backup
            backup_file = entry_file.with_suffix('.yaml.backup')
            shutil.copy2(entry_file, backup_file)
            
            # Apply resolution based on strategy
            field = conflict['field']
            resolved_value = resolution.get('resolved_value')
            
            if resolution['resolution_strategy'] == 'authority_hierarchy_primary':
                self._apply_authority_resolution(entry_data, field, resolution)
                
            elif resolution['resolution_strategy'] == 'additive_enhancement':
                self._apply_additive_resolution(entry_data, field, resolution)
                
            elif resolution['resolution_strategy'] == 'precision_enhancement':
                self._apply_precision_resolution(entry_data, field, resolution)
            
            # Add resolution tracking to entry
            if 'conflict_resolutions' not in entry_data:
                entry_data['conflict_resolutions'] = []
            
            entry_data['conflict_resolutions'].append({
                'conflict_id': conflict['conflict_id'],
                'resolution_date': datetime.now().isoformat(),
                'resolution_strategy': resolution['resolution_strategy'],
                'resolved_by': 'conflict-resolver-automated',
                'resolution_rationale': resolution['resolution_rationale']
            })
            
            # Save updated entry
            with open(entry_file, 'w') as f:
                yaml.dump(entry_data, f, default_flow_style=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error applying resolution to {entry_file}: {e}")
            return False
    
    def _apply_authority_resolution(self, entry_data: Dict, field: str, resolution: Dict) -> None:
        """Apply authority hierarchy resolution to entry"""
        winning_source = resolution['winning_source']
        source_layer = winning_source['source']
        resolved_value = resolution['resolved_value']
        
        # Update the appropriate layer with winning value
        if source_layer in entry_data:
            entry_data[source_layer][field] = resolved_value
            
        # Mark other layers as overridden
        layers = ['layer1_csv', 'layer2_datasheet', 'layer3_silicon_doc', 'layer4_clarifications']
        for layer in layers:
            if layer != source_layer and layer in entry_data and field in entry_data[layer]:
                # Keep original value but mark as overridden
                entry_data[layer][f"{field}_overridden_by"] = source_layer
    
    def _apply_additive_resolution(self, entry_data: Dict, field: str, resolution: Dict) -> None:
        """Apply additive enhancement resolution to entry"""
        merged_value = resolution['resolved_value']
        
        # Create merged field in a resolution section
        if 'merged_resolutions' not in entry_data:
            entry_data['merged_resolutions'] = {}
        
        entry_data['merged_resolutions'][field] = {
            'merged_value': merged_value,
            'source_layers': resolution['merged_sources'],
            'resolution_type': 'additive_enhancement'
        }
    
    def _apply_precision_resolution(self, entry_data: Dict, field: str, resolution: Dict) -> None:
        """Apply precision enhancement resolution to entry"""
        winning_source = resolution['winning_source']
        source_layer = winning_source['source']
        resolved_value = resolution['resolved_value']
        
        # Similar to authority resolution but with precision rationale
        if source_layer in entry_data:
            entry_data[source_layer][field] = resolved_value
            entry_data[source_layer][f"{field}_precision_enhanced"] = True
    
    def resolve_conflicts_batch(self, conflict_file: str) -> Dict[str, Any]:
        """Resolve all conflicts in a batch"""
        conflicts = self.load_conflict_log(conflict_file)
        
        if not conflicts:
            return {'total_conflicts': 0, 'resolved': 0, 'escalated': 0}
        
        resolved_count = 0
        escalated_count = 0
        resolution_log = []
        
        print(f"Processing {len(conflicts)} conflicts...")
        
        for conflict in conflicts:
            print(f"Resolving {conflict['conflict_id']}...")
            
            # Determine resolution strategy
            resolution = self._determine_resolution_strategy(conflict)
            
            # Try to apply resolution if automated
            if resolution.get('automated', False):
                entry_file = self._find_entry_file(conflict['entry_id'])
                if entry_file and self.apply_resolution(conflict, resolution, entry_file):
                    resolved_count += 1
                    print(f"  ✅ Resolved automatically")
                else:
                    escalated_count += 1
                    print(f"  ⚠️ Failed to apply - escalated")
            else:
                escalated_count += 1
                print(f"  📋 Escalated for manual review")
            
            # Log resolution attempt
            resolution_entry = {
                'conflict_id': conflict['conflict_id'],
                'entry_id': conflict['entry_id'],
                'resolution_date': datetime.now().isoformat(),
                'resolution': resolution,
                'status': 'resolved' if resolution.get('automated', False) else 'escalated'
            }
            resolution_log.append(resolution_entry)
        
        # Save resolution log
        self._save_resolution_log(resolution_log)
        
        print(f"\nBatch resolution complete:")
        print(f"  Total conflicts: {len(conflicts)}")
        print(f"  Resolved automatically: {resolved_count}")
        print(f"  Escalated for manual review: {escalated_count}")
        
        return {
            'total_conflicts': len(conflicts),
            'resolved': resolved_count,
            'escalated': escalated_count,
            'resolution_log': resolution_log
        }
    
    def _determine_resolution_strategy(self, conflict: Dict) -> Dict[str, Any]:
        """Determine appropriate resolution strategy for conflict"""
        conflict_type = conflict['conflict_type']
        
        if conflict_type == 'direct_contradiction':
            # Check severity and authority differences
            conflicting_sources = conflict['conflicting_sources']
            authorities = [src['authority'] for src in conflicting_sources]
            
            # If clear authority difference, use hierarchy
            if max(authorities) > min(authorities):
                return self.resolve_authority_hierarchy_conflict(conflict)
            else:
                # Same authority - need manual review
                return {
                    'resolution_strategy': 'escalate_to_manual',
                    'escalation_reason': 'Same authority level sources with direct contradiction',
                    'automated': False
                }
        
        elif conflict_type == 'completeness_conflict':
            return self.resolve_additive_enhancement_conflict(conflict)
        
        elif conflict_type == 'precision_conflict':
            return self.resolve_precision_enhancement_conflict(conflict)
        
        else:
            # Unknown conflict type - escalate
            return {
                'resolution_strategy': 'escalate_to_manual',
                'escalation_reason': f'Unknown conflict type: {conflict_type}',
                'automated': False
            }
    
    def _find_entry_file(self, entry_id: str) -> Optional[Path]:
        """Find the YAML file for an entry ID"""
        # Search in instructions directory
        for yaml_file in self.repo_path.glob("instructions/**/*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                
                if data.get('metadata', {}).get('id') == entry_id:
                    return yaml_file
            except:
                continue
        
        return None
    
    def _save_resolution_log(self, resolution_log: List[Dict]) -> None:
        """Save resolution log to file"""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file = self.repo_path / "update-tracking" / f"resolution-log-{timestamp}.yaml"
        
        log_data = {
            'resolution_run': {
                'timestamp': datetime.now().isoformat(),
                'total_resolutions': len(resolution_log),
                'resolutions': resolution_log
            }
        }
        
        with open(log_file, 'w') as f:
            yaml.dump(log_data, f, default_flow_style=False, indent=2)
        
        print(f"Resolution log saved to: {log_file}")
    
    def generate_escalation_queue(self, resolution_log: List[Dict]) -> str:
        """Generate manual review queue from escalated conflicts"""
        escalated = [res for res in resolution_log if res['status'] == 'escalated']
        
        if not escalated:
            return "No conflicts require manual review."
        
        queue = []
        queue.append("# Manual Review Queue")
        queue.append(f"Generated: {datetime.now().isoformat()}")
        queue.append(f"Conflicts requiring manual review: {len(escalated)}")
        queue.append("")
        
        # Sort by severity (if available)
        for resolution in escalated:
            conflict_id = resolution['conflict_id']
            entry_id = resolution['entry_id']
            escalation_reason = resolution['resolution']['escalation_reason']
            
            queue.append(f"## {conflict_id}")
            queue.append(f"**Entry**: {entry_id}")
            queue.append(f"**Reason**: {escalation_reason}")
            queue.append(f"**Review Deadline**: {(datetime.now()).strftime('%Y-%m-%d')} + 1 week")
            queue.append("")
            queue.append("**Required Actions**:")
            queue.append("- [ ] Analyze conflicting information")
            queue.append("- [ ] Research additional context if needed")
            queue.append("- [ ] Make resolution decision")
            queue.append("- [ ] Document rationale")
            queue.append("- [ ] Update entry")
            queue.append("- [ ] Close conflict")
            queue.append("")
        
        return "\n".join(queue)

def main():
    """Main function for conflict resolution"""
    repo_path = "/path/to/P2-Knowledge-Base/engineering/knowledge-base/P2"
    resolver = ConflictResolver(repo_path)
    
    print("P2 Knowledge Base Conflict Resolver")
    print("=" * 40)
    
    # List available conflict logs
    conflict_logs = list(resolver.repo_path.glob("update-tracking/conflict-log-*.yaml"))
    
    if not conflict_logs:
        print("No conflict logs found. Run conflict-detector.py first.")
        return
    
    print("Available conflict logs:")
    for i, log_file in enumerate(conflict_logs):
        print(f"{i + 1}. {log_file.name}")
    
    try:
        choice = int(input("\nSelect conflict log to resolve (number): ")) - 1
        if choice < 0 or choice >= len(conflict_logs):
            print("Invalid selection")
            return
        
        selected_log = conflict_logs[choice].name
        print(f"Resolving conflicts from: {selected_log}")
        
        # Resolve conflicts
        results = resolver.resolve_conflicts_batch(selected_log)
        
        # Generate escalation queue if needed
        if results['escalated'] > 0:
            resolution_log = results['resolution_log']
            queue = resolver.generate_escalation_queue(resolution_log)
            
            queue_file = resolver.repo_path / "update-tracking" / "manual-review-queue.md"
            with open(queue_file, 'w') as f:
                f.write(queue)
            
            print(f"\nManual review queue generated: {queue_file}")
    
    except (ValueError, IndexError):
        print("Invalid selection")

if __name__ == "__main__":
    main()
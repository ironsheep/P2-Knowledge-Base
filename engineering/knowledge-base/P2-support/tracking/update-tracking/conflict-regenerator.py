#!/usr/bin/env python3
"""
P2 Knowledge Base - Conflict Regeneration and Rollback System

Provides capability to re-evaluate past conflict decisions and roll back
resolutions when new information becomes available or when review reveals
incorrect resolution choices.

This enables the knowledge base to evolve its understanding while maintaining
complete audit trail of decision changes.
"""

import os
import sys
import json
import yaml
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ConflictSnapshot:
    """Captures complete state of conflict and its resolution"""
    conflict_id: str
    original_conflict: Dict
    resolution_used: str
    resolution_result: Dict
    resolved_timestamp: str
    resolver_info: Dict
    entry_state_before: Dict
    entry_state_after: Dict
    confidence_level: float
    
class ConflictRegenerator:
    """Handles re-evaluation and rollback of conflict resolutions"""
    
    def __init__(self, knowledge_base_path: str):
        self.kb_path = Path(knowledge_base_path)
        self.snapshots_dir = self.kb_path / "P2" / "update-tracking" / "conflict-snapshots"
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        self.rollback_log = self.kb_path / "P2" / "update-tracking" / "rollback-log.yaml"
        
    def create_conflict_snapshot(self, conflict: Dict, resolution: Dict, 
                               entry_before: Dict, entry_after: Dict) -> str:
        """Create snapshot before applying conflict resolution"""
        conflict_id = self._generate_conflict_id(conflict)
        
        snapshot = ConflictSnapshot(
            conflict_id=conflict_id,
            original_conflict=conflict.copy(),
            resolution_used=resolution.get('strategy', 'unknown'),
            resolution_result=resolution.copy(),
            resolved_timestamp=datetime.now().isoformat(),
            resolver_info={
                'resolver_version': '1.0.0',
                'authority_hierarchy': resolution.get('authority_used', 'unknown'),
                'manual_review_required': resolution.get('requires_manual_review', False)
            },
            entry_state_before=entry_before.copy(),
            entry_state_after=entry_after.copy(),
            confidence_level=resolution.get('confidence_level', 0.5)
        )
        
        # Save snapshot
        snapshot_file = self.snapshots_dir / f"{conflict_id}.yaml"
        with open(snapshot_file, 'w') as f:
            yaml.dump(snapshot.__dict__, f, default_flow_style=False, sort_keys=False)
            
        return conflict_id
        
    def evaluate_regeneration_triggers(self) -> List[Dict]:
        """Identify conflicts that should be re-evaluated"""
        triggers = []
        
        # Check for various regeneration triggers
        triggers.extend(self._find_low_confidence_resolutions())
        triggers.extend(self._find_outdated_authority_resolutions())
        triggers.extend(self._find_manual_review_completions())
        triggers.extend(self._find_new_source_impacts())
        
        return triggers
        
    def _find_low_confidence_resolutions(self) -> List[Dict]:
        """Find resolutions that had low confidence levels"""
        low_confidence = []
        
        for snapshot_file in self.snapshots_dir.glob("*.yaml"):
            with open(snapshot_file) as f:
                snapshot = yaml.safe_load(f)
                
            if snapshot.get('confidence_level', 1.0) < 0.7:
                low_confidence.append({
                    'conflict_id': snapshot['conflict_id'],
                    'trigger': 'low_confidence',
                    'confidence': snapshot['confidence_level'],
                    'reason': f"Confidence {snapshot['confidence_level']} below 0.7 threshold"
                })
                
        return low_confidence
        
    def _find_outdated_authority_resolutions(self) -> List[Dict]:
        """Find resolutions that used lower authority when higher is now available"""
        outdated = []
        
        for snapshot_file in self.snapshots_dir.glob("*.yaml"):
            with open(snapshot_file) as f:
                snapshot = yaml.safe_load(f)
                
            # Check if higher authority sources are now available
            original_authority = snapshot.get('resolver_info', {}).get('authority_hierarchy', 'CSV_EXTRACTED')
            entry_id = snapshot['original_conflict']['entry_id']
            
            # This would check current entry state vs snapshot state
            # If higher authority source now exists, trigger regeneration
            if self._has_higher_authority_available(entry_id, original_authority):
                outdated.append({
                    'conflict_id': snapshot['conflict_id'],
                    'trigger': 'higher_authority_available',
                    'original_authority': original_authority,
                    'reason': "Higher authority source now available"
                })
                
        return outdated
        
    def _find_manual_review_completions(self) -> List[Dict]:
        """Find manual reviews that have been completed"""
        completed_reviews = []
        
        for snapshot_file in self.snapshots_dir.glob("*.yaml"):
            with open(snapshot_file) as f:
                snapshot = yaml.safe_load(f)
                
            if snapshot.get('resolver_info', {}).get('manual_review_required', False):
                # Check if manual review has been completed
                review_id = snapshot['conflict_id']
                if self._is_manual_review_complete(review_id):
                    completed_reviews.append({
                        'conflict_id': snapshot['conflict_id'],
                        'trigger': 'manual_review_complete',
                        'review_decision': self._get_manual_review_decision(review_id),
                        'reason': "Manual review decision available"
                    })
                    
        return completed_reviews
        
    def _find_new_source_impacts(self) -> List[Dict]:
        """Find conflicts affected by new source additions"""
        new_impacts = []
        
        # This would analyze recent source additions and their impact
        # on previously resolved conflicts
        recent_sources = self._get_recent_source_additions()
        
        for source_info in recent_sources:
            affected_conflicts = self._find_conflicts_affected_by_source(source_info)
            for conflict_id in affected_conflicts:
                new_impacts.append({
                    'conflict_id': conflict_id,
                    'trigger': 'new_source_impact',
                    'new_source': source_info['source_name'],
                    'reason': f"New source {source_info['source_name']} may change resolution"
                })
                
        return new_impacts
        
    def regenerate_conflict_resolution(self, conflict_id: str, 
                                     regeneration_reason: str) -> Dict:
        """Re-evaluate a specific conflict with current knowledge"""
        
        # Load original conflict snapshot
        snapshot_file = self.snapshots_dir / f"{conflict_id}.yaml"
        if not snapshot_file.exists():
            return {'error': f'Snapshot not found for conflict {conflict_id}'}
            
        with open(snapshot_file) as f:
            original_snapshot = yaml.safe_load(f)
            
        # Re-run conflict detection and resolution with current state
        from .conflict_detector import ConflictDetector
        from .conflict_resolver import ConflictResolver
        
        detector = ConflictDetector(str(self.kb_path))
        resolver = ConflictResolver(str(self.kb_path))
        
        # Get current entry state
        entry_id = original_snapshot['original_conflict']['entry_id']
        current_entry_state = self._get_current_entry_state(entry_id)
        
        # Re-detect conflicts on current entry
        current_conflicts = detector.detect_entry_conflicts(entry_id)
        
        # Find the equivalent conflict (may have evolved)
        equivalent_conflict = self._find_equivalent_conflict(
            original_snapshot['original_conflict'], 
            current_conflicts
        )
        
        if not equivalent_conflict:
            return {
                'status': 'conflict_no_longer_exists',
                'reason': 'Original conflict no longer present in current state'
            }
            
        # Re-resolve with current resolution strategies
        new_resolution = resolver.resolve_conflict(equivalent_conflict)
        
        # Compare resolutions
        comparison = self._compare_resolutions(
            original_snapshot['resolution_result'],
            new_resolution
        )
        
        return {
            'status': 'regenerated',
            'conflict_id': conflict_id,
            'regeneration_reason': regeneration_reason,
            'original_resolution': original_snapshot['resolution_result'],
            'new_resolution': new_resolution,
            'resolution_changed': comparison['changed'],
            'changes_summary': comparison['changes'],
            'confidence_improvement': new_resolution.get('confidence_level', 0.5) - 
                                    original_snapshot.get('confidence_level', 0.5)
        }
        
    def rollback_conflict_resolution(self, conflict_id: str, 
                                   rollback_reason: str) -> Dict:
        """Roll back a conflict resolution to its pre-resolution state"""
        
        # Load conflict snapshot
        snapshot_file = self.snapshots_dir / f"{conflict_id}.yaml"
        if not snapshot_file.exists():
            return {'error': f'Snapshot not found for conflict {conflict_id}'}
            
        with open(snapshot_file) as f:
            snapshot = yaml.safe_load(f)
            
        # Restore entry to pre-resolution state
        entry_id = snapshot['original_conflict']['entry_id']
        pre_resolution_state = snapshot['entry_state_before']
        
        rollback_success = self._restore_entry_state(entry_id, pre_resolution_state)
        
        if rollback_success:
            # Log the rollback
            self._log_rollback(conflict_id, rollback_reason, snapshot)
            
            return {
                'status': 'rolled_back',
                'conflict_id': conflict_id,
                'entry_id': entry_id,
                'rollback_reason': rollback_reason,
                'restored_state': pre_resolution_state
            }
        else:
            return {
                'status': 'rollback_failed',
                'conflict_id': conflict_id,
                'error': 'Could not restore entry to previous state'
            }
            
    def _generate_conflict_id(self, conflict: Dict) -> str:
        """Generate unique ID for conflict"""
        conflict_str = json.dumps(conflict, sort_keys=True)
        return hashlib.md5(conflict_str.encode()).hexdigest()[:12]
        
    def _has_higher_authority_available(self, entry_id: str, current_authority: str) -> bool:
        """Check if higher authority sources are now available"""
        # This would check current entry sources vs original resolution authority
        # Implementation depends on entry storage format
        return False  # Placeholder
        
    def _is_manual_review_complete(self, review_id: str) -> bool:
        """Check if manual review has been completed"""
        # This would check manual review queue/database
        return False  # Placeholder
        
    def _get_manual_review_decision(self, review_id: str) -> Dict:
        """Get the decision from completed manual review"""
        # This would fetch the review decision
        return {}  # Placeholder
        
    def _get_recent_source_additions(self) -> List[Dict]:
        """Get list of recently added sources"""
        # This would check git log or source tracking for recent additions
        return []  # Placeholder
        
    def _find_conflicts_affected_by_source(self, source_info: Dict) -> List[str]:
        """Find conflict IDs that might be affected by new source"""
        # This would analyze which conflicts could be impacted
        return []  # Placeholder
        
    def _get_current_entry_state(self, entry_id: str) -> Dict:
        """Get current state of knowledge base entry"""
        # This would load current entry from knowledge base
        return {}  # Placeholder
        
    def _find_equivalent_conflict(self, original_conflict: Dict, 
                                current_conflicts: List[Dict]) -> Optional[Dict]:
        """Find current conflict equivalent to original"""
        # This would match conflicts based on field and entry
        return None  # Placeholder
        
    def _compare_resolutions(self, original: Dict, new: Dict) -> Dict:
        """Compare two conflict resolutions"""
        changes = []
        
        # Compare key resolution fields
        for key in ['chosen_value', 'authority_used', 'strategy']:
            if original.get(key) != new.get(key):
                changes.append({
                    'field': key,
                    'old_value': original.get(key),
                    'new_value': new.get(key)
                })
                
        return {
            'changed': len(changes) > 0,
            'changes': changes
        }
        
    def _restore_entry_state(self, entry_id: str, target_state: Dict) -> bool:
        """Restore entry to specific state"""
        # This would update the knowledge base entry
        return False  # Placeholder - requires KB write access
        
    def _log_rollback(self, conflict_id: str, reason: str, snapshot: Dict):
        """Log rollback action for audit trail"""
        rollback_entry = {
            'timestamp': datetime.now().isoformat(),
            'conflict_id': conflict_id,
            'rollback_reason': reason,
            'original_resolution_timestamp': snapshot['resolved_timestamp'],
            'entry_id': snapshot['original_conflict']['entry_id']
        }
        
        # Append to rollback log
        rollback_log = []
        if self.rollback_log.exists():
            with open(self.rollback_log) as f:
                rollback_log = yaml.safe_load(f) or []
                
        rollback_log.append(rollback_entry)
        
        with open(self.rollback_log, 'w') as f:
            yaml.dump(rollback_log, f, default_flow_style=False)

def main():
    """CLI interface for conflict regeneration"""
    if len(sys.argv) < 2:
        print("Usage: python conflict_regenerator.py <command> [args]")
        print("Commands:")
        print("  check-triggers     - Find conflicts that need re-evaluation")
        print("  regenerate <id>    - Re-evaluate specific conflict")
        print("  rollback <id>      - Roll back specific conflict resolution")
        sys.exit(1)
        
    kb_path = os.path.dirname(os.path.dirname(__file__))
    regenerator = ConflictRegenerator(kb_path)
    
    command = sys.argv[1]
    
    if command == "check-triggers":
        triggers = regenerator.evaluate_regeneration_triggers()
        print(f"Found {len(triggers)} conflicts that need re-evaluation:")
        for trigger in triggers:
            print(f"  {trigger['conflict_id']}: {trigger['reason']}")
            
    elif command == "regenerate" and len(sys.argv) > 2:
        conflict_id = sys.argv[2]
        result = regenerator.regenerate_conflict_resolution(
            conflict_id, 
            "Manual regeneration request"
        )
        print(f"Regeneration result: {result}")
        
    elif command == "rollback" and len(sys.argv) > 2:
        conflict_id = sys.argv[2]
        result = regenerator.rollback_conflict_resolution(
            conflict_id,
            "Manual rollback request"
        )
        print(f"Rollback result: {result}")
        
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
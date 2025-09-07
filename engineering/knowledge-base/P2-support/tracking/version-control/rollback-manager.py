#!/usr/bin/env python3
"""
P2 Knowledge Base Rollback Manager
Manages rollback of problematic updates and recovery from backups
Version: 1.0.0
"""

import yaml
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

class RollbackManager:
    """Manages rollback operations for the repository"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.backup_dir = self.repo_path / "update-tracking" / "backups"
        self.rollback_log = self.repo_path / "update-tracking" / "rollback-log.yaml"
        self.rollback_history = []
        
    def list_available_backups(self, entry_path: Optional[str] = None) -> List[Dict]:
        """List available backups for an entry or all entries"""
        backups = []
        
        if entry_path:
            # Get backups for specific entry
            entry_name = Path(entry_path).stem
            pattern = f"{entry_name}_backup_*.yaml"
        else:
            # Get all backups
            pattern = "*_backup_*.yaml"
            
        for backup_file in self.backup_dir.rglob(pattern):
            # Extract timestamp from filename
            parts = backup_file.stem.split('_backup_')
            if len(parts) == 2:
                try:
                    timestamp_str = parts[1]
                    timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    
                    # Get original file path
                    original_name = parts[0]
                    category = backup_file.parent.name
                    original_path = f"instructions/{category}/{original_name}.yaml"
                    
                    backups.append({
                        'backup_file': backup_file,
                        'original_path': original_path,
                        'timestamp': timestamp,
                        'age_days': (datetime.now() - timestamp).days,
                        'size': backup_file.stat().st_size
                    })
                except:
                    continue
                    
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x['timestamp'], reverse=True)
        return backups
        
    def get_backup_for_commit(self, commit: str) -> List[Dict]:
        """Find backups created around the time of a specific commit"""
        backups = []
        
        try:
            # Get commit timestamp
            result = subprocess.run(
                ['git', 'show', '-s', '--format=%ci', commit],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                commit_time = datetime.strptime(
                    result.stdout.strip()[:19], '%Y-%m-%d %H:%M:%S'
                )
                
                # Find backups within 5 minutes of commit
                all_backups = self.list_available_backups()
                for backup in all_backups:
                    time_diff = abs((backup['timestamp'] - commit_time).total_seconds())
                    if time_diff < 300:  # Within 5 minutes
                        backup['commit'] = commit
                        backup['time_diff_seconds'] = time_diff
                        backups.append(backup)
                        
        except Exception as e:
            print(f"Error finding backups for commit {commit}: {e}")
            
        return backups
        
    def rollback_entry(self, entry_path: str, backup_file: Optional[Path] = None,
                      reason: str = "") -> bool:
        """Rollback a single entry to a backup version"""
        entry_path = self.repo_path / entry_path
        
        if not entry_path.exists():
            print(f"Error: Entry {entry_path} not found")
            return False
            
        # Find backup if not specified
        if not backup_file:
            backups = self.list_available_backups(str(entry_path))
            if not backups:
                print(f"No backups found for {entry_path}")
                return False
            backup_file = backups[0]['backup_file']  # Use most recent
            
        if not backup_file.exists():
            print(f"Error: Backup file {backup_file} not found")
            return False
            
        try:
            # Create a safety backup of current version
            safety_backup = self.backup_dir / "rollback-safety" / \
                          f"{entry_path.stem}_safety_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
            safety_backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(entry_path, safety_backup)
            
            # Perform rollback
            shutil.copy2(backup_file, entry_path)
            
            # Log the rollback
            self.rollback_history.append({
                'timestamp': datetime.now().isoformat(),
                'entry': str(entry_path),
                'backup_used': str(backup_file),
                'safety_backup': str(safety_backup),
                'reason': reason
            })
            
            print(f"✅ Rolled back {entry_path.name} to backup from {backup_file.stem}")
            return True
            
        except Exception as e:
            print(f"Error during rollback: {e}")
            return False
            
    def rollback_commit(self, commit: str, reason: str = "") -> Dict[str, Any]:
        """Rollback all changes from a specific commit"""
        results = {
            'commit': commit,
            'timestamp': datetime.now().isoformat(),
            'rolled_back': [],
            'failed': [],
            'reason': reason
        }
        
        try:
            # Get list of files changed in commit
            result = subprocess.run(
                ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"Error: Could not get files for commit {commit}")
                return results
                
            changed_files = result.stdout.strip().split('\n')
            yaml_files = [f for f in changed_files if f.endswith('.yaml')]
            
            print(f"Rolling back {len(yaml_files)} files from commit {commit}")
            
            # Find and apply backups
            backups = self.get_backup_for_commit(commit)
            backup_map = {b['original_path']: b['backup_file'] for b in backups}
            
            for file_path in yaml_files:
                if file_path in backup_map:
                    if self.rollback_entry(file_path, backup_map[file_path], reason):
                        results['rolled_back'].append(file_path)
                    else:
                        results['failed'].append(file_path)
                else:
                    # Try to restore from git
                    if self.rollback_from_git(file_path, f"{commit}~1"):
                        results['rolled_back'].append(file_path)
                    else:
                        results['failed'].append(file_path)
                        
        except Exception as e:
            print(f"Error during commit rollback: {e}")
            
        # Save rollback history
        self.save_rollback_log(results)
        
        return results
        
    def rollback_from_git(self, file_path: str, commit: str) -> bool:
        """Rollback a file using git history"""
        try:
            # Get file content from git
            result = subprocess.run(
                ['git', 'show', f'{commit}:{file_path}'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Save current version as backup
                current_path = self.repo_path / file_path
                if current_path.exists():
                    backup_path = self.backup_dir / "git-rollback" / \
                                f"{current_path.stem}_git_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(current_path, backup_path)
                    
                # Write git version
                current_path.parent.mkdir(parents=True, exist_ok=True)
                with open(current_path, 'w') as f:
                    f.write(result.stdout)
                    
                print(f"✅ Restored {file_path} from git commit {commit}")
                return True
                
        except Exception as e:
            print(f"Error restoring from git: {e}")
            
        return False
        
    def rollback_time_range(self, hours: int, reason: str = "") -> Dict[str, Any]:
        """Rollback all changes within the last N hours"""
        results = {
            'time_range': f"last {hours} hours",
            'timestamp': datetime.now().isoformat(),
            'rolled_back': [],
            'failed': [],
            'reason': reason
        }
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Find all backups after cutoff time
        all_backups = self.list_available_backups()
        recent_backups = [b for b in all_backups if b['timestamp'] > cutoff_time]
        
        # Group by original path
        by_path = defaultdict(list)
        for backup in recent_backups:
            by_path[backup['original_path']].append(backup)
            
        print(f"Found {len(by_path)} entries modified in the last {hours} hours")
        
        # Rollback each entry to pre-cutoff state
        for entry_path, backups in by_path.items():
            # Find the last backup before cutoff
            pre_cutoff = [b for b in self.list_available_backups(entry_path) 
                         if b['timestamp'] <= cutoff_time]
                         
            if pre_cutoff:
                if self.rollback_entry(entry_path, pre_cutoff[0]['backup_file'], reason):
                    results['rolled_back'].append(entry_path)
                else:
                    results['failed'].append(entry_path)
            else:
                print(f"No pre-cutoff backup found for {entry_path}")
                results['failed'].append(entry_path)
                
        # Save rollback history
        self.save_rollback_log(results)
        
        return results
        
    def create_restore_point(self, name: str, description: str = "") -> bool:
        """Create a named restore point of the current state"""
        restore_point_dir = self.backup_dir / "restore-points" / name
        
        if restore_point_dir.exists():
            print(f"Restore point {name} already exists")
            return False
            
        try:
            restore_point_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy all current YAML files
            patterns = [
                "instructions/**/*.yaml",
                "components/**/*.yaml",
                "architecture/*.yaml",
                "hardware/*.yaml"
            ]
            
            file_count = 0
            for pattern in patterns:
                for file_path in self.repo_path.glob(pattern):
                    rel_path = file_path.relative_to(self.repo_path)
                    dest_path = restore_point_dir / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, dest_path)
                    file_count += 1
                    
            # Save metadata
            metadata = {
                'name': name,
                'description': description,
                'timestamp': datetime.now().isoformat(),
                'file_count': file_count,
                'git_commit': self.get_current_commit()
            }
            
            with open(restore_point_dir / 'metadata.yaml', 'w') as f:
                yaml.dump(metadata, f, default_flow_style=False)
                
            print(f"✅ Created restore point '{name}' with {file_count} files")
            return True
            
        except Exception as e:
            print(f"Error creating restore point: {e}")
            return False
            
    def restore_from_point(self, name: str) -> Dict[str, Any]:
        """Restore repository to a named restore point"""
        restore_point_dir = self.backup_dir / "restore-points" / name
        results = {
            'restore_point': name,
            'timestamp': datetime.now().isoformat(),
            'restored': [],
            'failed': []
        }
        
        if not restore_point_dir.exists():
            print(f"Restore point {name} not found")
            return results
            
        try:
            # Load metadata
            with open(restore_point_dir / 'metadata.yaml', 'r') as f:
                metadata = yaml.safe_load(f)
                
            print(f"Restoring from point '{name}' created at {metadata['timestamp']}")
            
            # Create safety backup first
            self.create_restore_point(
                f"auto-safety-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                f"Safety backup before restoring to {name}"
            )
            
            # Restore files
            for source_file in restore_point_dir.glob("**/*.yaml"):
                if source_file.name == 'metadata.yaml':
                    continue
                    
                rel_path = source_file.relative_to(restore_point_dir)
                dest_path = self.repo_path / rel_path
                
                try:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, dest_path)
                    results['restored'].append(str(rel_path))
                except Exception as e:
                    print(f"Failed to restore {rel_path}: {e}")
                    results['failed'].append(str(rel_path))
                    
        except Exception as e:
            print(f"Error during restore: {e}")
            
        # Save rollback history
        self.save_rollback_log(results)
        
        return results
        
    def get_current_commit(self) -> str:
        """Get current git commit hash"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except:
            return "unknown"
            
    def save_rollback_log(self, results: Dict) -> None:
        """Save rollback operation to log"""
        self.rollback_log.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing log
        if self.rollback_log.exists():
            with open(self.rollback_log, 'r') as f:
                log_data = yaml.safe_load(f) or []
        else:
            log_data = []
            
        # Add new entry
        log_data.append(results)
        
        # Save updated log
        with open(self.rollback_log, 'w') as f:
            yaml.dump(log_data, f, default_flow_style=False)
            
    def cleanup_old_backups(self, days: int = 30) -> Dict[str, int]:
        """Clean up backups older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        results = {
            'deleted': 0,
            'kept': 0,
            'space_freed': 0
        }
        
        all_backups = self.list_available_backups()
        
        for backup in all_backups:
            if backup['timestamp'] < cutoff_date:
                try:
                    results['space_freed'] += backup['size']
                    backup['backup_file'].unlink()
                    results['deleted'] += 1
                except:
                    pass
            else:
                results['kept'] += 1
                
        print(f"Cleaned up {results['deleted']} old backups")
        print(f"Kept {results['kept']} recent backups")
        print(f"Freed {results['space_freed'] / 1024:.1f} KB")
        
        return results
        

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="P2 Knowledge Base Rollback Manager")
    parser.add_argument('--repo-path', default='.', help='Repository root path')
    parser.add_argument('--rollback-entry', help='Rollback specific entry')
    parser.add_argument('--rollback-commit', help='Rollback entire commit')
    parser.add_argument('--rollback-hours', type=int, help='Rollback last N hours')
    parser.add_argument('--create-restore-point', help='Create named restore point')
    parser.add_argument('--restore-from', help='Restore from named point')
    parser.add_argument('--cleanup-days', type=int, help='Clean backups older than N days')
    parser.add_argument('--reason', default='', help='Reason for rollback')
    
    args = parser.parse_args()
    
    manager = RollbackManager(args.repo_path)
    
    if args.rollback_entry:
        manager.rollback_entry(args.rollback_entry, reason=args.reason)
    elif args.rollback_commit:
        results = manager.rollback_commit(args.rollback_commit, reason=args.reason)
        print(f"Rolled back: {len(results['rolled_back'])} files")
        print(f"Failed: {len(results['failed'])} files")
    elif args.rollback_hours:
        results = manager.rollback_time_range(args.rollback_hours, reason=args.reason)
        print(f"Rolled back: {len(results['rolled_back'])} entries")
    elif args.create_restore_point:
        manager.create_restore_point(args.create_restore_point, args.reason)
    elif args.restore_from:
        results = manager.restore_from_point(args.restore_from)
        print(f"Restored: {len(results['restored'])} files")
    elif args.cleanup_days:
        manager.cleanup_old_backups(args.cleanup_days)
    else:
        # List available backups
        backups = manager.list_available_backups()
        print(f"Found {len(backups)} backups")
        for backup in backups[:10]:
            print(f"  - {backup['original_path']}: {backup['age_days']} days old")
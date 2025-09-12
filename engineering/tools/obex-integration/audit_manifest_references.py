#!/usr/bin/env python3
"""
CRITICAL: Audit manifest yaml_path references vs actual Object IDs
"""

import os
import yaml
from pathlib import Path

class ManifestReferenceAuditor:
    def __init__(self, manifests_dir, objects_dir):
        self.manifests_dir = Path(manifests_dir)
        self.objects_dir = Path(objects_dir)
        self.reference_errors = []
        
    def audit_manifest_references(self):
        """Check all manifest references to object files"""
        print("CRITICAL AUDIT: Manifest References vs Object Files")
        print("=" * 80)
        
        total_references = 0
        broken_references = 0
        id_mismatches = 0
        
        # Check root manifest
        root_manifest = self.manifests_dir / "obex-community-manifest.yaml"
        if root_manifest.exists():
            print("Checking root manifest references...")
            # Root manifest doesn't contain direct object references, skip for now
        
        # Check category manifests
        categories_dir = self.manifests_dir / "categories"
        if categories_dir.exists():
            print("Checking category manifest references...")
            for manifest_file in categories_dir.glob("*-manifest.yaml"):
                errors = self.check_manifest_file(manifest_file, "category")
                broken_references += len([e for e in errors if e['type'] == 'missing_file'])
                id_mismatches += len([e for e in errors if e['type'] == 'id_mismatch'])
                total_references += len(errors) + len([e for e in errors if e['type'] == 'valid'])
        
        # Check author manifests  
        authors_dir = self.manifests_dir / "authors"
        if authors_dir.exists():
            print("Checking author manifest references...")
            for manifest_file in authors_dir.glob("*-manifest.yaml"):
                errors = self.check_manifest_file(manifest_file, "author")
                broken_references += len([e for e in errors if e['type'] == 'missing_file'])
                id_mismatches += len([e for e in errors if e['type'] == 'id_mismatch'])
                total_references += sum(1 for error in errors if 'objects_checked' in error for _ in range(error.get('objects_checked', 0)))
        
        print(f"\nAUDIT RESULTS:")
        print(f"Total object references checked: {total_references}")
        print(f"Broken file references: {broken_references}")
        print(f"Object ID mismatches: {id_mismatches}")
        print(f"Reference integrity: {((total_references - broken_references - id_mismatches)/total_references)*100:.1f}%" if total_references > 0 else "N/A")
        
        return self.reference_errors
    
    def check_manifest_file(self, manifest_file, manifest_type):
        """Check references in a specific manifest file"""
        errors = []
        objects_checked = 0
        
        try:
            with open(manifest_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            manifest_name = manifest_file.name
            objects = data.get('objects', [])
            
            print(f"  Checking {manifest_name}: {len(objects)} object references")
            
            for obj_ref in objects:
                objects_checked += 1
                manifest_obj_id = obj_ref.get('object_id', '')
                yaml_path = obj_ref.get('yaml_path', '')
                title = obj_ref.get('title', 'NO TITLE')
                
                if not yaml_path:
                    error = {
                        'type': 'missing_path',
                        'manifest_file': manifest_name,
                        'manifest_type': manifest_type,
                        'object_id': manifest_obj_id,
                        'title': title,
                        'issue': 'No yaml_path specified'
                    }
                    errors.append(error)
                    self.reference_errors.append(error)
                    print(f"    ❌ {manifest_obj_id}: No yaml_path")
                    continue
                
                # Resolve the path relative to manifests directory
                if yaml_path.startswith('../objects/'):
                    actual_file_path = self.objects_dir / yaml_path.replace('../objects/', '')
                else:
                    actual_file_path = self.manifests_dir / yaml_path
                
                if not actual_file_path.exists():
                    error = {
                        'type': 'missing_file',
                        'manifest_file': manifest_name,
                        'manifest_type': manifest_type,
                        'object_id': manifest_obj_id,
                        'yaml_path': yaml_path,
                        'resolved_path': str(actual_file_path),
                        'title': title,
                        'issue': f'File does not exist: {actual_file_path}'
                    }
                    errors.append(error)
                    self.reference_errors.append(error)
                    print(f"    ❌ {manifest_obj_id}: File missing - {yaml_path}")
                    continue
                
                # Check if the Object ID in the file matches the manifest reference
                try:
                    with open(actual_file_path, 'r', encoding='utf-8') as f:
                        file_data = yaml.safe_load(f)
                    
                    file_obj_id = file_data['object_metadata'].get('object_id', '')
                    
                    if manifest_obj_id != file_obj_id:
                        error = {
                            'type': 'id_mismatch',
                            'manifest_file': manifest_name,
                            'manifest_type': manifest_type,
                            'manifest_object_id': manifest_obj_id,
                            'file_object_id': file_obj_id,
                            'yaml_path': yaml_path,
                            'title': title,
                            'issue': f'Object ID mismatch: manifest says {manifest_obj_id}, file contains {file_obj_id}'
                        }
                        errors.append(error)
                        self.reference_errors.append(error)
                        print(f"    ❌ {manifest_obj_id}: ID mismatch - file contains {file_obj_id}")
                    else:
                        print(f"    ✅ {manifest_obj_id}: Valid reference")
                        
                except Exception as e:
                    error = {
                        'type': 'file_error',
                        'manifest_file': manifest_name,
                        'manifest_type': manifest_type,
                        'object_id': manifest_obj_id,
                        'yaml_path': yaml_path,
                        'title': title,
                        'issue': f'Error reading file: {e}'
                    }
                    errors.append(error)
                    self.reference_errors.append(error)
                    print(f"    ❌ {manifest_obj_id}: File read error - {e}")
        
        except Exception as e:
            print(f"  ❌ Error reading manifest {manifest_file}: {e}")
        
        # Add objects_checked to the first error for counting purposes
        if errors and objects_checked > 0:
            errors[0]['objects_checked'] = objects_checked
        elif objects_checked > 0:
            errors.append({'type': 'valid', 'objects_checked': objects_checked})
            
        return errors
    
    def generate_error_report(self):
        """Generate detailed error report"""
        if not self.reference_errors:
            print("\n✅ All manifest references are valid!")
            return
        
        print(f"\n🚨 FOUND {len(self.reference_errors)} REFERENCE ERRORS:")
        print("=" * 80)
        
        # Group errors by type
        error_types = {}
        for error in self.reference_errors:
            error_type = error['type']
            if error_type not in error_types:
                error_types[error_type] = []
            error_types[error_type].append(error)
        
        for error_type, errors in error_types.items():
            print(f"\n{error_type.upper().replace('_', ' ')} ERRORS ({len(errors)}):")
            print("-" * 40)
            
            for error in errors:
                print(f"📁 {error['manifest_file']} ({error.get('manifest_type', 'unknown')})")
                print(f"   Object ID: {error.get('object_id', error.get('manifest_object_id', 'N/A'))}")
                print(f"   Title: {error.get('title', 'N/A')}")
                print(f"   Issue: {error['issue']}")
                if 'yaml_path' in error:
                    print(f"   Path: {error['yaml_path']}")
                print()
        
        return error_types

def main():
    manifests_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/manifests"
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    auditor = ManifestReferenceAuditor(manifests_dir, objects_dir)
    
    # Perform comprehensive reference audit
    errors = auditor.audit_manifest_references()
    
    # Generate error report
    error_types = auditor.generate_error_report()
    
    return errors, error_types

if __name__ == "__main__":
    main()
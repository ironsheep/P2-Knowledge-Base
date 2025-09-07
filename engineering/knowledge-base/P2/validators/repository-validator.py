#!/usr/bin/env python3
"""
P2 Knowledge Base Repository Validator
Comprehensive validation for YAML entries, cross-references, and data consistency
Version: 1.0.0
"""

import yaml
import json
import re
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional
from datetime import datetime
from collections import defaultdict
import networkx as nx

class RepositoryValidator:
    """Main validation framework for P2 Knowledge Base"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.errors = []
        self.warnings = []
        self.info = []
        self.entries = {}
        self.cross_refs = defaultdict(set)
        self.dependency_graph = nx.DiGraph()
        
        # Load schemas
        self.instruction_schema = self._load_schema('instruction-schema.yaml')
        self.audit_schema = self._load_schema('quality-audit-schema.yaml')
        
    def _load_schema(self, schema_file: str) -> Dict:
        """Load a schema definition file"""
        schema_path = self.repo_path / schema_file
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
        
    def validate_all(self) -> Dict[str, Any]:
        """Run all validation checks"""
        print("Starting comprehensive repository validation...")
        
        # Load all entries
        self._load_entries()
        
        # Run validation suites
        results = {
            'timestamp': datetime.now().isoformat(),
            'schema_validation': self._validate_schemas(),
            'cross_references': self._validate_cross_references(),
            'encoding_validation': self._validate_encodings(),
            'timing_validation': self._validate_timing(),
            'circular_references': self._detect_circular_references(),
            'coverage_gaps': self._identify_coverage_gaps(),
            'consistency_checks': self._check_consistency(),
            'statistics': self._calculate_statistics()
        }
        
        # Compile issues
        results['errors'] = self.errors
        results['warnings'] = self.warnings
        results['info'] = self.info
        results['summary'] = {
            'total_entries': len(self.entries),
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
            'validation_passed': len(self.errors) == 0
        }
        
        return results
        
    def _load_entries(self) -> None:
        """Load all YAML entries from repository"""
        patterns = [
            'instructions/pasm2/*.yaml',
            'instructions/spin2/*.yaml',
            'components/**/*.yaml',
            'architecture/*.yaml',
            'hardware/*.yaml'
        ]
        
        for pattern in patterns:
            for file_path in self.repo_path.glob(pattern):
                try:
                    with open(file_path, 'r') as f:
                        data = yaml.safe_load(f)
                        if data:
                            entry_id = data.get('id', file_path.stem)
                            self.entries[entry_id] = {
                                'path': file_path,
                                'data': data
                            }
                except Exception as e:
                    self.errors.append({
                        'type': 'load_error',
                        'file': str(file_path),
                        'error': str(e)
                    })
                    
    def _validate_schemas(self) -> Dict[str, Any]:
        """Validate all entries against their schemas"""
        results = {
            'validated': 0,
            'failed': 0,
            'schema_errors': []
        }
        
        for entry_id, entry in self.entries.items():
            data = entry['data']
            
            # Determine schema type
            if 'instructions' in str(entry['path']):
                schema = self.instruction_schema
            else:
                continue  # Skip non-instruction entries for now
                
            # Validate required fields
            if 'required_fields' in schema:
                for field, field_spec in schema['required_fields'].items():
                    if field not in data:
                        self.errors.append({
                            'type': 'missing_required_field',
                            'entry': entry_id,
                            'field': field
                        })
                        results['failed'] += 1
                    else:
                        # Validate field type and pattern
                        if not self._validate_field(data[field], field_spec):
                            self.errors.append({
                                'type': 'field_validation_failed',
                                'entry': entry_id,
                                'field': field,
                                'value': str(data[field])[:100]
                            })
                            results['failed'] += 1
                            
            results['validated'] += 1
            
        return results
        
    def _validate_field(self, value: Any, spec: Dict) -> bool:
        """Validate a field against its specification"""
        # Type check
        if 'type' in spec:
            expected_type = spec['type']
            if expected_type == 'string' and not isinstance(value, str):
                return False
            elif expected_type == 'integer' and not isinstance(value, int):
                return False
            elif expected_type == 'boolean' and not isinstance(value, bool):
                return False
                
        # Pattern check
        if 'pattern' in spec and isinstance(value, str):
            pattern = spec['pattern']
            if not re.match(pattern, value):
                return False
                
        # Enum check
        if 'enum' in spec:
            if value not in spec['enum']:
                return False
                
        return True
        
    def _validate_cross_references(self) -> Dict[str, Any]:
        """Validate all cross-references between entries"""
        results = {
            'total_refs': 0,
            'valid_refs': 0,
            'broken_refs': [],
            'orphaned_entries': []
        }
        
        # Build reference map
        for entry_id, entry in self.entries.items():
            data = entry['data']
            
            # Check related_instructions
            if 'related_instructions' in data:
                for ref in data['related_instructions']:
                    results['total_refs'] += 1
                    self.cross_refs[entry_id].add(ref)
                    
                    # Check if reference exists
                    ref_id = f"{ref.lower()}-instruction"
                    if ref_id not in self.entries:
                        self.errors.append({
                            'type': 'broken_reference',
                            'entry': entry_id,
                            'reference': ref,
                            'field': 'related_instructions'
                        })
                        results['broken_refs'].append((entry_id, ref))
                    else:
                        results['valid_refs'] += 1
                        self.dependency_graph.add_edge(entry_id, ref_id)
                        
            # Check see_also references
            if 'see_also' in data:
                for ref in data['see_also']:
                    results['total_refs'] += 1
                    # These might be concepts, not just instructions
                    self.warnings.append({
                        'type': 'unverified_reference',
                        'entry': entry_id,
                        'reference': ref,
                        'field': 'see_also'
                    })
                    
        # Find orphaned entries (no incoming or outgoing refs)
        for entry_id in self.entries:
            if entry_id not in self.cross_refs and not any(
                entry_id in refs for refs in self.cross_refs.values()
            ):
                results['orphaned_entries'].append(entry_id)
                self.info.append({
                    'type': 'orphaned_entry',
                    'entry': entry_id
                })
                
        return results
        
    def _validate_encodings(self) -> Dict[str, Any]:
        """Validate instruction encoding formats"""
        results = {
            'validated': 0,
            'invalid_encodings': []
        }
        
        encoding_pattern = re.compile(r'^[01ECZI\s]+$')
        
        for entry_id, entry in self.entries.items():
            data = entry['data']
            
            if 'encoding' in data:
                encoding = data['encoding'].replace('D', '').replace('S', '')
                encoding = encoding.replace(' ', '')
                
                # Check if 32 bits
                bit_count = len(encoding.replace('E', '0').replace('C', '0')
                              .replace('Z', '0').replace('I', '0'))
                              
                if bit_count != 32:
                    self.errors.append({
                        'type': 'invalid_encoding_length',
                        'entry': entry_id,
                        'length': bit_count,
                        'expected': 32
                    })
                    results['invalid_encodings'].append(entry_id)
                    
                results['validated'] += 1
                
        return results
        
    def _validate_timing(self) -> Dict[str, Any]:
        """Validate timing specifications"""
        results = {
            'validated': 0,
            'invalid_timing': []
        }
        
        for entry_id, entry in self.entries.items():
            data = entry['data']
            
            if 'timing' in data:
                timing = data['timing']
                
                if 'cycles' in timing:
                    cycles = timing['cycles']
                    
                    # Validate cycle format
                    if isinstance(cycles, str):
                        # Check for range format "2-9"
                        if '-' in cycles:
                            parts = cycles.split('-')
                            try:
                                min_cycles = int(parts[0])
                                max_cycles = int(parts[1])
                                if min_cycles > max_cycles:
                                    self.errors.append({
                                        'type': 'invalid_timing_range',
                                        'entry': entry_id,
                                        'timing': cycles
                                    })
                                    results['invalid_timing'].append(entry_id)
                            except ValueError:
                                self.errors.append({
                                    'type': 'invalid_timing_format',
                                    'entry': entry_id,
                                    'timing': cycles
                                })
                                results['invalid_timing'].append(entry_id)
                                
                results['validated'] += 1
                
        return results
        
    def _detect_circular_references(self) -> Dict[str, Any]:
        """Detect circular reference chains"""
        results = {
            'circular_chains': [],
            'checked_nodes': 0
        }
        
        try:
            # Find all simple cycles
            cycles = list(nx.simple_cycles(self.dependency_graph))
            
            for cycle in cycles:
                self.warnings.append({
                    'type': 'circular_reference',
                    'cycle': cycle
                })
                results['circular_chains'].append(cycle)
                
            results['checked_nodes'] = self.dependency_graph.number_of_nodes()
            
        except Exception as e:
            self.errors.append({
                'type': 'circular_detection_error',
                'error': str(e)
            })
            
        return results
        
    def _identify_coverage_gaps(self) -> Dict[str, Any]:
        """Identify systematic coverage gaps"""
        results = {
            'missing_fields': defaultdict(int),
            'incomplete_categories': defaultdict(list),
            'coverage_summary': {}
        }
        
        # Track field presence across entries
        field_presence = defaultdict(int)
        total_entries = len(self.entries)
        
        for entry_id, entry in self.entries.items():
            data = entry['data']
            
            # Check common fields
            common_fields = [
                'description', 'examples', 'timing', 'usage_notes',
                'related_instructions', 'affects_flags', 'source_layers'
            ]
            
            for field in common_fields:
                if field in data:
                    field_presence[field] += 1
                else:
                    results['missing_fields'][field] += 1
                    
            # Check completeness score
            if 'completeness_score' in data:
                score = data['completeness_score']
                if score < 6:
                    category = str(entry['path'].parent.name)
                    results['incomplete_categories'][category].append({
                        'entry': entry_id,
                        'score': score
                    })
                    
        # Calculate coverage percentages
        for field, count in field_presence.items():
            results['coverage_summary'][field] = {
                'present': count,
                'missing': total_entries - count,
                'percentage': (count / total_entries * 100) if total_entries > 0 else 0
            }
            
        return results
        
    def _check_consistency(self) -> Dict[str, Any]:
        """Check data consistency across related entries"""
        results = {
            'inconsistencies': [],
            'bidirectional_check': {
                'valid': 0,
                'invalid': []
            }
        }
        
        # Check bidirectional relationships
        for entry_id, refs in self.cross_refs.items():
            for ref_id in refs:
                if ref_id in self.entries:
                    ref_data = self.entries[ref_id]['data']
                    
                    # Check if reverse reference exists
                    if 'related_instructions' in ref_data:
                        reverse_refs = ref_data['related_instructions']
                        expected_reverse = entry_id.replace('-instruction', '').upper()
                        
                        if expected_reverse not in reverse_refs:
                            self.warnings.append({
                                'type': 'missing_bidirectional_reference',
                                'from': entry_id,
                                'to': ref_id,
                                'expected': expected_reverse
                            })
                            results['bidirectional_check']['invalid'].append(
                                (entry_id, ref_id)
                            )
                        else:
                            results['bidirectional_check']['valid'] += 1
                            
        # Check category consistency
        categories = defaultdict(list)
        for entry_id, entry in self.entries.items():
            if 'category' in entry['data']:
                category = entry['data']['category']
                categories[category].append(entry_id)
                
        # Verify related instructions are in compatible categories
        compatible_categories = {
            'math': ['math', 'logic'],
            'branch': ['branch', 'special'],
            'memory': ['memory', 'system'],
            'smart-pin': ['smart-pin', 'system']
        }
        
        for entry_id, entry in self.entries.items():
            if 'category' in entry['data'] and 'related_instructions' in entry['data']:
                entry_category = entry['data']['category']
                
                for ref in entry['data']['related_instructions']:
                    ref_id = f"{ref.lower()}-instruction"
                    if ref_id in self.entries and 'category' in self.entries[ref_id]['data']:
                        ref_category = self.entries[ref_id]['data']['category']
                        
                        # Check compatibility
                        if entry_category in compatible_categories:
                            if ref_category not in compatible_categories[entry_category]:
                                self.info.append({
                                    'type': 'cross_category_reference',
                                    'from': f"{entry_id} ({entry_category})",
                                    'to': f"{ref_id} ({ref_category})"
                                })
                                
        return results
        
    def _calculate_statistics(self) -> Dict[str, Any]:
        """Calculate repository statistics"""
        stats = {
            'total_entries': len(self.entries),
            'by_category': defaultdict(int),
            'by_completeness': defaultdict(int),
            'average_completeness': 0,
            'field_coverage': {}
        }
        
        completeness_scores = []
        
        for entry_id, entry in self.entries.items():
            data = entry['data']
            
            # Category stats
            if 'category' in data:
                stats['by_category'][data['category']] += 1
                
            # Completeness stats
            if 'completeness_score' in data:
                score = data['completeness_score']
                stats['by_completeness'][score] += 1
                completeness_scores.append(score)
                
        # Calculate averages
        if completeness_scores:
            stats['average_completeness'] = sum(completeness_scores) / len(completeness_scores)
            
        return stats
        
    def generate_report(self, results: Dict[str, Any], output_path: str) -> None:
        """Generate validation report"""
        report = f"""# P2 Knowledge Base Validation Report
Generated: {results['timestamp']}

## Summary
- **Total Entries**: {results['summary']['total_entries']}
- **Errors Found**: {results['summary']['error_count']}
- **Warnings**: {results['summary']['warning_count']}
- **Validation Status**: {'✅ PASSED' if results['summary']['validation_passed'] else '❌ FAILED'}

## Schema Validation
- Validated: {results['schema_validation']['validated']}
- Failed: {results['schema_validation']['failed']}

## Cross-Reference Validation
- Total References: {results['cross_references']['total_refs']}
- Valid References: {results['cross_references']['valid_refs']}
- Broken References: {len(results['cross_references']['broken_refs'])}
- Orphaned Entries: {len(results['cross_references']['orphaned_entries'])}

## Circular References
- Circular Chains Found: {len(results['circular_references']['circular_chains'])}

## Coverage Analysis
"""
        
        # Add coverage details
        for field, coverage in results['coverage_gaps']['coverage_summary'].items():
            report += f"- **{field}**: {coverage['percentage']:.1f}% coverage\n"
            
        # Add errors section
        if results['errors']:
            report += "\n## Errors (Must Fix)\n"
            for error in results['errors'][:20]:  # Limit to first 20
                report += f"- [{error['type']}] {error.get('entry', 'N/A')}: "
                report += f"{error.get('field', '')} {error.get('error', '')}\n"
                
        # Add warnings section
        if results['warnings']:
            report += "\n## Warnings (Should Fix)\n"
            for warning in results['warnings'][:20]:  # Limit to first 20
                report += f"- [{warning['type']}] {warning.get('entry', 'N/A')}: "
                report += f"{warning.get('field', '')} {warning.get('reference', '')}\n"
                
        # Save report
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(report)
            
        # Also save JSON results
        json_file = output_file.with_suffix('.json')
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
            
        print(f"Validation report saved to: {output_file}")
        print(f"JSON results saved to: {json_file}")
        

if __name__ == "__main__":
    # Run validation
    validator = RepositoryValidator(".")
    results = validator.validate_all()
    
    # Generate report
    validator.generate_report(results, "validation-reports/validation-report.md")
    
    # Print summary
    print("\nValidation Summary:")
    print(f"  Errors: {results['summary']['error_count']}")
    print(f"  Warnings: {results['summary']['warning_count']}")
    print(f"  Status: {'✅ PASSED' if results['summary']['validation_passed'] else '❌ FAILED'}")
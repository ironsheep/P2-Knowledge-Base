#!/usr/bin/env python3
"""
Unified merge of PASM2 manual extractions with existing YAML files.
Creates single source of truth for each field with Option A flag structure.

This script implements the unified field strategy with:
- Single comprehensive description
- Nested flag structure
- Clear documentation source tracking
"""

import yaml
import re
import json
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

class UnifiedMerger:
    def __init__(self, yaml_dir: str, extract_dir: str, output_dir: str):
        self.yaml_dir = Path(yaml_dir)
        self.extract_dir = Path(extract_dir)
        self.output_dir = Path(output_dir)
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Track comprehensive statistics
        self.stats = {
            'total_processed': 0,
            'enriched_from_manual': 0,
            'kept_minimal': 0,
            'errors': [],
            'missing_documentation': [],
            'field_statistics': {
                'descriptions_unified': 0,
                'flags_structured': 0,
                'parameters_added': 0,
                'related_added': 0
            }
        }
        
        self.report = []
        
    def clean_text(self, text: str) -> str:
        """Clean up text from manual extraction"""
        if not text:
            return text
            
        # Fix common ligatures
        text = text.replace('ﬂ', 'fl')
        text = text.replace('ﬁ', 'fi')
        text = text.replace('ﬀ', 'ff')
        
        # Remove page numbers and copyright notices
        text = re.sub(r'Copyright © Parallax Inc\..*?Page \d+', '', text)
        text = re.sub(r'▪ Propeller 2 Assembly Language Manual.*?▪\s*Page \d+', '', text)
        
        # Clean up excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
        
    def unify_description(self, original: Dict, extracted: Dict) -> str:
        """Create unified description from all available sources"""
        
        parts = []
        
        # Start with detailed explanation if available
        if extracted and 'detailed_explanation' in extracted:
            explanation = self.clean_text(extracted['detailed_explanation'])
            if explanation and len(explanation) > 20:
                parts.append(explanation)
        
        # Add operation result if different from explanation
        if extracted and 'result' in extracted:
            result = self.clean_text(extracted['result'])
            if result and result not in parts[0] if parts else True:
                if parts:
                    parts.append(f"Result: {result}")
                else:
                    parts.append(result)
        
        # Add formula from original if not already included
        if 'description' in original:
            orig_desc = original['description'].strip()
            # Extract formula like "D = D + S"
            formula_match = re.search(r'[A-Z]\s*=\s*[^.]+', orig_desc)
            if formula_match and not any(formula_match.group() in p for p in parts):
                parts.append(formula_match.group().strip() + '.')
        
        # If we still don't have much, use original description
        if not parts and 'description' in original:
            parts.append(original['description'].strip())
        
        # Join parts into comprehensive description
        description = ' '.join(parts)
        
        # Ensure it ends with period
        if description and not description.endswith('.'):
            description += '.'
            
        return description
        
    def structure_flags(self, original: Dict, extracted: Dict) -> Dict:
        """Create structured flag documentation"""
        
        flags = {}
        
        # Start with original flag formulas
        if 'flags_affected' in original:
            for flag, formula in original['flags_affected'].items():
                if flag in ['C', 'Z']:
                    flags[flag] = {'formula': formula}
        
        # Add descriptions from extraction
        if extracted:
            if 'c_flag_effect' in extracted and extracted['c_flag_effect']:
                if 'C' not in flags:
                    flags['C'] = {}
                flags['C']['when'] = self.clean_text(extracted['c_flag_effect'])
                
            if 'z_flag_effect' in extracted and extracted['z_flag_effect']:
                if 'Z' not in flags:
                    flags['Z'] = {}
                flags['Z']['when'] = self.clean_text(extracted['z_flag_effect'])
        
        # If we have the nested structure, track it
        if flags and any('when' in v for v in flags.values() if isinstance(v, dict)):
            self.stats['field_statistics']['flags_structured'] += 1
            
        return flags if flags else None
        
    def clean_parameters(self, extracted: Dict) -> List[str]:
        """Clean and structure parameter documentation"""
        
        if not extracted or 'parameters' not in extracted:
            return None
            
        params = []
        for param in extracted['parameters']:
            cleaned = self.clean_text(param)
            if cleaned and len(cleaned) > 10:
                # Make sure it starts with the parameter name
                if not cleaned[0].isupper():
                    cleaned = cleaned[0].upper() + cleaned[1:]
                params.append(cleaned)
                
        return params if params else None
        
    def merge_instruction(self, name: str) -> Dict:
        """Unified merge of a single instruction"""
        
        # Load original YAML
        yaml_path = self.yaml_dir / f"{name.lower()}.yaml"
        if not yaml_path.exists():
            self.report.append(f"ERROR: {name} - YAML file not found")
            return None
            
        try:
            with open(yaml_path, 'r') as f:
                original = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.report.append(f"ERROR: {name} - YAML parse error: {e}")
            self.stats['errors'].append(f"{name}: YAML parse error")
            return None
            
        # Check for extracted content
        extract_path = self.extract_dir / f"{name.lower()}_extracted.yaml"
        extracted = None
        if extract_path.exists():
            try:
                with open(extract_path, 'r') as f:
                    extracted = yaml.safe_load(f)
            except:
                extracted = None
        
        # Build unified structure
        unified = {
            'instruction': name
        }
        
        # Copy critical technical fields that must be preserved
        for field in ['syntax', 'encoding', 'timing', 'group']:
            if field in original:
                unified[field] = original[field]
        
        # Create unified description
        unified['description'] = self.unify_description(original, extracted)
        if extracted:
            self.stats['field_statistics']['descriptions_unified'] += 1
        
        # Add category information
        if extracted and 'category' in extracted:
            unified['category'] = self.clean_text(extracted['category'])
        elif 'group' in original:
            unified['category'] = original['group']
            
        # Structure flags
        flags = self.structure_flags(original, extracted)
        if flags:
            unified['flags_affected'] = flags
            
        # Add parameters if available
        params = self.clean_parameters(extracted) if extracted else None
        if params:
            unified['parameters'] = params
            self.stats['field_statistics']['parameters_added'] += 1
            
        # Add related instructions
        if extracted and 'related_instructions' in extracted:
            unified['related'] = extracted['related_instructions']
            self.stats['field_statistics']['related_added'] += 1
            
        # Mark documentation source
        if extracted:
            unified['documentation_source'] = "PASM2 Manual 2022/11/01"
            unified['documentation_level'] = "comprehensive"
            self.stats['enriched_from_manual'] += 1
            self.report.append(f"ENRICHED: {name} - Full documentation from manual")
        else:
            unified['documentation_source'] = "original"
            unified['documentation_level'] = "minimal"
            unified['needs_documentation'] = True
            self.stats['kept_minimal'] += 1
            self.stats['missing_documentation'].append(name)
            self.report.append(f"MINIMAL: {name} - Needs documentation")
            
        return unified
        
    def process_all_instructions(self):
        """Process all PASM2 instructions"""
        
        # Get all YAML files
        yaml_files = list(self.yaml_dir.glob("*.yaml"))
        
        # Filter out concept files
        instructions = [f.stem.upper() for f in yaml_files 
                       if not f.stem.startswith('concepts')]
        
        print(f"Processing {len(instructions)} total instructions...")
        print(f"Output directory: {self.output_dir}\n")
        
        for instr in sorted(instructions):
            self.stats['total_processed'] += 1
            
            unified = self.merge_instruction(instr)
            
            if unified:
                # Save unified file
                output_path = self.output_dir / f"{instr.lower()}.yaml"
                with open(output_path, 'w') as f:
                    yaml.dump(unified, f, default_flow_style=False, 
                            sort_keys=False, width=100, allow_unicode=True)
                    
                # Progress indicator
                if self.stats['total_processed'] % 20 == 0:
                    print(f"  Processed {self.stats['total_processed']} instructions...")
                    
    def generate_report(self):
        """Generate comprehensive merge report"""
        
        report_path = self.output_dir / "MERGE_REPORT.md"
        
        with open(report_path, 'w') as f:
            f.write("# PASM2 Unified Merge Report\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            f.write("## Summary Statistics\n\n")
            f.write(f"- **Total Instructions Processed**: {self.stats['total_processed']}\n")
            f.write(f"- **Enriched from Manual**: {self.stats['enriched_from_manual']}\n")
            f.write(f"- **Kept Minimal**: {self.stats['kept_minimal']}\n")
            f.write(f"- **Errors**: {len(self.stats['errors'])}\n\n")
            
            f.write("## Field Enhancement Statistics\n\n")
            f.write(f"- **Descriptions Unified**: {self.stats['field_statistics']['descriptions_unified']}\n")
            f.write(f"- **Flags Structured**: {self.stats['field_statistics']['flags_structured']}\n")
            f.write(f"- **Parameters Added**: {self.stats['field_statistics']['parameters_added']}\n")
            f.write(f"- **Related Instructions Added**: {self.stats['field_statistics']['related_added']}\n\n")
            
            f.write("## Instructions Needing Documentation\n\n")
            f.write(f"Total: {len(self.stats['missing_documentation'])} instructions\n\n")
            
            # Group missing by first letter
            grouped = {}
            for instr in sorted(self.stats['missing_documentation']):
                first = instr[0]
                if first not in grouped:
                    grouped[first] = []
                grouped[first].append(instr)
                
            for letter, instrs in sorted(grouped.items()):
                f.write(f"### {letter}\n")
                f.write(', '.join(instrs) + '\n\n')
                
            if self.stats['errors']:
                f.write("## Errors\n\n")
                for error in self.stats['errors']:
                    f.write(f"- {error}\n")
                f.write("\n")
                
            f.write("## Processing Log\n\n")
            f.write("```\n")
            for entry in self.report[-50:]:  # Last 50 entries
                f.write(f"{entry}\n")
            if len(self.report) > 50:
                f.write(f"... and {len(self.report) - 50} more entries\n")
            f.write("```\n")
            
        # Also save JSON statistics
        stats_path = self.output_dir / "merge_statistics.json"
        with open(stats_path, 'w') as f:
            json.dump(self.stats, f, indent=2)
            
        print(f"\n📊 Report saved to: {report_path}")
        print(f"📈 Statistics saved to: {stats_path}")
        

def main():
    print("="*70)
    print("PASM2 UNIFIED MERGE - FINAL PRODUCTION RUN")
    print("="*70)
    
    # First, run full extraction
    print("\n" + "="*70)
    print("PHASE 1: FULL EXTRACTION FROM MANUAL")
    print("="*70)
    
    import subprocess
    result = subprocess.run([
        'python3', 
        'engineering/tools/extract-manual-content-v3.py'
    ], capture_output=True, text=True)
    
    # Paths
    yaml_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2"
    extract_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/tools/manual-extractions"
    output_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/tools/unified-output"
    
    print("\n" + "="*70)
    print("PHASE 2: UNIFIED MERGE")
    print("="*70)
    
    merger = UnifiedMerger(yaml_dir, extract_dir, output_dir)
    merger.process_all_instructions()
    
    print("\n" + "="*70)
    print("PHASE 3: GENERATING REPORT")
    print("="*70)
    
    merger.generate_report()
    
    print("\n" + "="*70)
    print("MERGE COMPLETE")
    print("="*70)
    print(f"\n✅ Successfully processed {merger.stats['total_processed']} instructions")
    print(f"📚 Enriched: {merger.stats['enriched_from_manual']} instructions")
    print(f"📝 Need documentation: {merger.stats['kept_minimal']} instructions")
    print(f"\n📁 Output: {output_dir}")
    print(f"📊 Report: {output_dir}/MERGE_REPORT.md")
    print("\n" + "="*70)
    

if __name__ == "__main__":
    main()
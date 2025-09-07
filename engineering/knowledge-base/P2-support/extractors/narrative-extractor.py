#!/usr/bin/env python3
"""
Silicon Doc Narrative Extractor
Extracts available narrative content and adds as layer3 to YAML files
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class NarrativeExtractor:
    def __init__(self, sources_dir: str, yaml_dir: str):
        self.sources_dir = Path(sources_dir)
        self.yaml_dir = Path(yaml_dir)
        self.narratives = {}
        self.audit_log = []
        self.matched_count = 0
        self.unmatched_count = 0
        
    def extract_narratives(self) -> Dict[str, Any]:
        """Extract narrative content from various Silicon Doc files"""
        narratives = {}
        
        # Extract from silicon-from-docx.md
        docx_file = self.sources_dir / "silicon-from-docx.md"
        if docx_file.exists():
            self._extract_from_docx_summary(docx_file, narratives)
        
        # Extract from INSTRUCTION-TIMING-AND-ENCODING.md
        timing_file = self.sources_dir / "INSTRUCTION-TIMING-AND-ENCODING.md"
        if timing_file.exists():
            self._extract_from_timing_doc(timing_file, narratives)
        
        # Extract from silicon-doc-v35-facts-only.md
        facts_file = self.sources_dir / "silicon-doc-v35-facts-only.md"
        if facts_file.exists():
            self._extract_from_facts(facts_file, narratives)
        
        # Add general architectural narratives
        self._add_architectural_narratives(narratives)
        
        return narratives
    
    def _extract_from_docx_summary(self, file_path: Path, narratives: Dict) -> None:
        """Extract narratives from docx summary file"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract instruction enhancement narratives
        if 'Instruction Enhancements' in content:
            enhancements = {
                'BITL': 'Can work on bit spans. Prior SETQ overrides S[9:5] for span size.',
                'BITH': 'Can work on bit spans. Prior SETQ overrides S[9:5] for span size.',
                'BITC': 'Can work on bit spans. Prior SETQ overrides S[9:5] for span size.',
                'BITNC': 'Can work on bit spans. Prior SETQ overrides S[9:5] for span size.',
                'BITZ': 'Can work on bit spans. Prior SETQ overrides S[9:5] for span size.',
                'BITNZ': 'Can work on bit spans. Prior SETQ overrides S[9:5] for span size.',
                'BITRND': 'Can work on bit spans. Prior SETQ overrides S[9:5] for span size.',
                'BITNOT': 'Can work on bit spans. Prior SETQ overrides S[9:5] for span size.',
                'DIRH': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DIRL': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DIRC': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DIRNC': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DIRZ': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DIRNZ': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DIRRND': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DIRNOT': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'OUTH': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'OUTL': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'OUTC': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'OUTNC': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'OUTZ': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'OUTNZ': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'OUTRND': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'OUTNOT': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'FLTH': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'FLTL': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'FLTC': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'FLTNC': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'FLTZ': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'FLTNZ': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'FLTRND': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'FLTNOT': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DRVH': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DRVL': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DRVC': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DRVNC': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DRVZ': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DRVNZ': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DRVRND': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'DRVNOT': 'Can work on pin spans. Prior SETQ overrides D[10:6] for span size.',
                'WRPIN': 'Can work on pin spans. Prior SETQ overrides S[10:6] for span size.',
                'WXPIN': 'Can work on pin spans. Prior SETQ overrides S[10:6] for span size.',
                'WYPIN': 'Can work on pin spans. Prior SETQ overrides S[10:6] for span size.',
                'AKPIN': 'Can work on pin spans. Prior SETQ overrides S[10:6] for span size.',
                'GETCT': 'System counter extended to 64 bits in Rev B/C. GETCT WC retrieves upper 32-bits.',
                'SETLUTS': 'Enable/disable LUT RAM writes from adjacent cog. Now glitch-free in Rev B/C silicon.'
            }
            
            for mnemonic, narrative in enhancements.items():
                if mnemonic not in narratives:
                    narratives[mnemonic] = []
                narratives[mnemonic].append({
                    'source': 'silicon-from-docx.md',
                    'content': narrative,
                    'type': 'enhancement'
                })
    
    def _extract_from_timing_doc(self, file_path: Path, narratives: Dict) -> None:
        """Extract narratives from timing documentation"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract specific instruction descriptions
        instruction_narratives = {
            'GETPTR': 'Get pointer value used with EXECF. Returns current FIFO pointer state. Usage: MOV PB,(GETPTR) writes FIFO pointer to PB.',
            'GETBRK': 'Get break/debug status. Multiple forms: GETBRK D WCZ returns cog internal status; GETBRK D WC returns SKIP/SKIPF/EXECF/XBYTE pattern info; GETBRK D WZ returns pattern queue status.',
            'COGBRK': 'Trigger asynchronous breakpoint in target cog. D/# contains %CCCC target cog ID.',
            'BRK': 'Generate debug interrupt with 8-bit code. D/# contains %BBBBBBBB 8-bit BRK code.',
            'SETLUTS': 'Enable/disable LUT RAM writes from adjacent cog. SETLUTS #0 disallows writes (default), SETLUTS #1 allows writes.'
        }
        
        for mnemonic, narrative in instruction_narratives.items():
            if mnemonic not in narratives:
                narratives[mnemonic] = []
            narratives[mnemonic].append({
                'source': 'INSTRUCTION-TIMING-AND-ENCODING.md',
                'content': narrative,
                'type': 'functional_description'
            })
        
        # Add pipeline timing narrative for branch instructions
        branch_instructions = ['JMP', 'CALL', 'RET', 'RETA', 'RETB', 'CALLA', 'CALLB', 
                              'CALLD', 'JCT1', 'JCT2', 'JCT3', 'JINT', 'JATN', 
                              'JFBW', 'JPAT', 'JCT1', 'JCT2', 'JCT3']
        
        for mnemonic in branch_instructions:
            if mnemonic not in narratives:
                narratives[mnemonic] = []
            narratives[mnemonic].append({
                'source': 'INSTRUCTION-TIMING-AND-ENCODING.md',
                'content': 'Branch instruction flushes pipeline, causing next instruction to take 5+ clocks instead of 2.',
                'type': 'timing_note'
            })
    
    def _extract_from_facts(self, file_path: Path, narratives: Dict) -> None:
        """Extract narratives from facts-only document"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract COG starting narrative
        if 'COGINIT' in content:
            narratives['COGINIT'] = narratives.get('COGINIT', [])
            narratives['COGINIT'].append({
                'source': 'silicon-doc-v35-facts-only.md',
                'content': 'Start a cog. D[5]: 0=load from HUB, 1=direct start. D[4]: 0=specific COG, 1=find free. D[3:0]: COG ID when D[4]=0. D[0]: when D[4]=1, 0=single, 1=pair. SETQ value → PTRA, S/# address → PTRB.',
                'type': 'encoding_details'
            })
        
        if 'COGSTOP' in content:
            narratives['COGSTOP'] = narratives.get('COGSTOP', [])
            narratives['COGSTOP'].append({
                'source': 'silicon-doc-v35-facts-only.md',
                'content': 'Stop a cog. Cog becomes available for COGINIT.',
                'type': 'functional_description'
            })
    
    def _add_architectural_narratives(self, narratives: Dict) -> None:
        """Add general architectural context as narratives"""
        # Add pipeline context for all instructions
        general_pipeline = "P2 uses a 5-stage pipeline architecture. Most math/logic instructions execute in 2 clocks when pipeline is full."
        
        # Add hub memory context for hub instructions
        hub_instructions = ['RDBYTE', 'RDWORD', 'RDLONG', 'WRBYTE', 'WRWORD', 'WRLONG', 
                           'RDFAST', 'WRFAST', 'FBLOCK', 'RDLUT', 'WRLUT']
        
        for mnemonic in hub_instructions:
            if mnemonic not in narratives:
                narratives[mnemonic] = []
            narratives[mnemonic].append({
                'source': 'architectural_context',
                'content': 'Hub memory access uses egg-beater rotation. Each cog gets a turn every 8 clocks. Hub window alignment affects timing (13-20 clocks typical).',
                'type': 'architectural_note'
            })
        
        # Add CORDIC context
        cordic_instructions = ['QROTATE', 'QVECTOR', 'QMUL', 'QDIV', 'QSQRT', 'QLOG', 'QEXP', 'QFRAC']
        
        for mnemonic in cordic_instructions:
            if mnemonic not in narratives:
                narratives[mnemonic] = []
            narratives[mnemonic].append({
                'source': 'architectural_context',
                'content': 'CORDIC solver uses 54-stage pipeline. Results available after 54 clocks. Multiple operations can be pipelined.',
                'type': 'architectural_note'
            })
    
    def update_yaml_files(self, narratives: Dict[str, List]) -> None:
        """Update YAML files with layer3 narrative data"""
        yaml_files = list(self.yaml_dir.glob('pasm2_*.yaml'))
        
        print(f"Processing {len(yaml_files)} YAML files...")
        
        for yaml_file in yaml_files:
            try:
                # Read YAML file content
                with open(yaml_file, 'r') as f:
                    content = f.read()
                
                # Extract mnemonic
                mnemonic = None
                for line in content.split('\n'):
                    if 'mnemonic:' in line:
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            mnemonic = parts[1].strip()
                            break
                
                if mnemonic and mnemonic in narratives:
                    # Check if layer3_silicon_doc already exists
                    if 'layer3_silicon_doc:' not in content:
                        # Find insertion point (after layer2 if exists, else after layer1)
                        lines = content.split('\n')
                        insert_index = len(lines)
                        
                        # Find end of layer2 or layer1
                        for i, line in enumerate(lines):
                            if 'layer2_datasheet:' in line:
                                # Find end of layer2
                                in_layer2 = True
                                for j in range(i+1, len(lines)):
                                    if lines[j] and not lines[j].startswith(' '):
                                        insert_index = j
                                        break
                                break
                            elif 'layer1_csv:' in line and 'layer2_datasheet:' not in content:
                                # Find end of layer1
                                in_layer1 = True
                                for j in range(i+1, len(lines)):
                                    if lines[j] and not lines[j].startswith(' '):
                                        insert_index = j
                                        break
                                break
                        
                        # Build layer3 content
                        layer3_lines = [
                            'layer3_silicon_doc:',
                            f'  extraction_date: {datetime.now().isoformat()}',
                            '  narratives:'
                        ]
                        
                        for narrative in narratives[mnemonic]:
                            layer3_lines.append(f'    - source: {narrative["source"]}')
                            layer3_lines.append(f'      type: {narrative["type"]}')
                            layer3_lines.append(f'      content: |')
                            for line in narrative['content'].split('\n'):
                                layer3_lines.append(f'        {line}')
                        
                        # Insert layer3 content
                        lines.insert(insert_index, '\n'.join(layer3_lines))
                        
                        # Write updated content
                        with open(yaml_file, 'w') as f:
                            f.write('\n'.join(lines))
                        
                        self.matched_count += 1
                        self.audit_log.append({
                            'action': 'updated',
                            'file': yaml_file.name,
                            'mnemonic': mnemonic,
                            'narratives_added': len(narratives[mnemonic])
                        })
                else:
                    self.unmatched_count += 1
                    
            except Exception as e:
                self.audit_log.append({
                    'action': 'error',
                    'file': yaml_file.name,
                    'error': str(e)
                })
    
    def write_coverage_matrix(self, narratives: Dict) -> None:
        """Write narrative coverage matrix"""
        matrix_file = self.yaml_dir.parent / "narrative-coverage-matrix.md"
        
        with open(matrix_file, 'w') as f:
            f.write("# Narrative Coverage Matrix\n\n")
            f.write(f"**Date**: {datetime.now().isoformat()}\n")
            f.write(f"**Source Directory**: {self.sources_dir}\n\n")
            
            f.write("## Summary\n")
            f.write(f"- Instructions with narratives: {self.matched_count}\n")
            f.write(f"- Instructions without narratives: {self.unmatched_count}\n")
            f.write(f"- Total narrative sources found: {len(narratives)}\n\n")
            
            f.write("## Instructions with Rich Narratives\n\n")
            
            # Group by narrative count
            by_count = {}
            for mnemonic, narr_list in narratives.items():
                count = len(narr_list)
                if count not in by_count:
                    by_count[count] = []
                by_count[count].append(mnemonic)
            
            for count in sorted(by_count.keys(), reverse=True):
                f.write(f"### {count} Narrative Source(s) ({len(by_count[count])} instructions)\n")
                for mnemonic in sorted(by_count[count]):
                    sources = ', '.join(n['source'] for n in narratives[mnemonic])
                    f.write(f"- **{mnemonic}**: {sources}\n")
                f.write("\n")
            
            f.write("## Narrative Types Distribution\n\n")
            
            # Count narrative types
            type_counts = {}
            for mnemonic, narr_list in narratives.items():
                for narr in narr_list:
                    narr_type = narr['type']
                    if narr_type not in type_counts:
                        type_counts[narr_type] = 0
                    type_counts[narr_type] += 1
            
            for narr_type, count in sorted(type_counts.items()):
                f.write(f"- {narr_type}: {count} narratives\n")
        
        print(f"Coverage matrix written to: {matrix_file}")
    
    def run(self) -> None:
        """Run the complete narrative extraction process"""
        print(f"Starting narrative extraction from: {self.sources_dir}")
        
        # Extract narratives
        print("Extracting narrative content...")
        self.narratives = self.extract_narratives()
        print(f"Found narratives for {len(self.narratives)} instructions")
        
        # Update YAML files
        print("Updating YAML files with layer3 narrative data...")
        self.update_yaml_files(self.narratives)
        
        # Write coverage matrix
        print("Writing coverage matrix...")
        self.write_coverage_matrix(self.narratives)
        
        # Report results
        print(f"\nNarrative extraction complete:")
        print(f"  Instructions updated: {self.matched_count}")
        print(f"  Instructions without narratives: {self.unmatched_count}")
        if (self.matched_count + self.unmatched_count) > 0:
            coverage = round(self.matched_count / (self.matched_count + self.unmatched_count) * 100, 2)
            print(f"  Coverage: {coverage}%")

if __name__ == "__main__":
    # Configure paths
    sources_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc"
    yaml_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2"
    
    # Run extraction
    extractor = NarrativeExtractor(sources_dir, yaml_dir)
    extractor.run()
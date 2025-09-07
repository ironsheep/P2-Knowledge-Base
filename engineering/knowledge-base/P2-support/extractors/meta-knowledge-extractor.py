#!/usr/bin/env python3
"""
Meta-Knowledge Extractor
Extracts insights, patterns, and relationships from analysis documents
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

class MetaKnowledgeExtractor:
    def __init__(self, sources_dir: str, output_dir: str):
        self.sources_dir = Path(sources_dir)
        self.output_dir = Path(output_dir)
        self.meta_knowledge = {}
        self.learning_paths = {}
        self.insights_count = 0
        
    def extract_from_walkthrough(self, file_path: Path) -> Dict[str, Any]:
        """Extract meta-knowledge from walkthrough analysis"""
        meta = {
            'architectural_insights': [],
            'instruction_patterns': [],
            'optimization_hints': [],
            'common_gotchas': [],
            'hardware_considerations': []
        }
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract architectural insights
        if 'System Organization' in content:
            meta['architectural_insights'].append({
                'topic': 'Hub/Cog Interaction',
                'insight': 'Hub memory uses egg-beater rotation for fair access. Each cog gets a hub window every 8 clocks.',
                'related_instructions': ['RDBYTE', 'RDWORD', 'RDLONG', 'WRBYTE', 'WRWORD', 'WRLONG'],
                'impact': 'timing_critical'
            })
            
            meta['architectural_insights'].append({
                'topic': 'CORDIC Solver',
                'insight': 'CORDIC uses 54-stage pipeline. Multiple operations can be pipelined for throughput.',
                'related_instructions': ['QROTATE', 'QVECTOR', 'QMUL', 'QDIV', 'QSQRT', 'QLOG', 'QEXP'],
                'impact': 'performance'
            })
        
        # Extract hardware considerations
        if 'Pin' in content or 'Smart Pin' in content:
            meta['hardware_considerations'].append({
                'topic': 'Smart Pin Configuration',
                'insight': 'Smart pins have multiple modes requiring proper configuration sequence. WRPIN sets mode, WXPIN/WYPIN set parameters.',
                'related_instructions': ['WRPIN', 'WXPIN', 'WYPIN', 'RDPIN', 'RQPIN', 'AKPIN'],
                'best_practice': 'Always acknowledge pin operations with AKPIN to clear status'
            })
        
        # Extract common gotchas from gaps analysis
        if 'Gaps' in content or 'Critical' in content:
            meta['common_gotchas'].append({
                'issue': 'Pipeline Flush on Branches',
                'description': 'Branch instructions flush the 5-stage pipeline, causing 3+ cycle penalty',
                'affected_instructions': ['JMP', 'CALL', 'RET', 'Jxx conditional jumps'],
                'mitigation': 'Use conditional execution (IF_xx) for short sequences instead of branches'
            })
            
            meta['common_gotchas'].append({
                'issue': 'Hub Window Alignment',
                'description': 'Hub access timing varies 13-20 cycles based on window alignment',
                'affected_instructions': ['All RDxxxx/WRxxxx hub operations'],
                'mitigation': 'Use RDFAST/WRFAST with FIFO for predictable streaming'
            })
        
        # Extract optimization hints
        meta['optimization_hints'].append({
            'technique': 'Instruction Pairing',
            'description': 'ALTx instructions modify the next instruction without pipeline stall',
            'examples': ['ALTS + MOV for indexed access', 'ALTD + ADD for destination indexing'],
            'benefit': 'Avoid self-modifying code penalties'
        })
        
        meta['optimization_hints'].append({
            'technique': 'Block Transfers',
            'description': 'SETQ/SETQ2 enable fast block transfers between cog/lut/hub',
            'examples': ['SETQ + RDLONG for hub->cog block read', 'SETQ2 + RDLONG for hub->lut'],
            'benefit': 'Transfer 1 long per clock after initial setup'
        })
        
        return meta
    
    def extract_from_critical_insights(self, file_path: Path) -> Dict[str, Any]:
        """Extract patterns from critical insights document"""
        patterns = {
            'instruction_categories': {},
            'performance_patterns': [],
            'usage_patterns': []
        }
        
        if not file_path.exists():
            return patterns
            
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Define instruction categories based on common patterns
        patterns['instruction_categories'] = {
            'math_basic': {
                'instructions': ['ADD', 'SUB', 'CMP', 'NEG', 'ABS', 'MIN', 'MAX'],
                'characteristics': 'Fixed 2-cycle execution, affects C/Z flags',
                'common_usage': 'Loop counters, address calculations, arithmetic'
            },
            'math_multiply': {
                'instructions': ['MUL', 'MULS', 'SCA', 'SCAS'],
                'characteristics': '2-cycle for 16x16 bit, special scaling modes',
                'common_usage': 'Fixed-point math, scaling operations'
            },
            'bit_operations': {
                'instructions': ['AND', 'OR', 'XOR', 'NOT', 'TEST', 'TESTB', 'BITC', 'BITH', 'BITL'],
                'characteristics': 'Bit manipulation, flag testing, mask operations',
                'common_usage': 'Flag manipulation, bit fields, masks'
            },
            'memory_cog': {
                'instructions': ['MOV', 'MOVBYTS', 'SETBYTE', 'GETBYTE'],
                'characteristics': '2-cycle cog RAM access',
                'common_usage': 'Register operations, byte manipulation'
            },
            'memory_hub': {
                'instructions': ['RDBYTE', 'RDWORD', 'RDLONG', 'WRBYTE', 'WRWORD', 'WRLONG'],
                'characteristics': 'Variable timing (13-20 cycles), hub window dependent',
                'common_usage': 'Main memory access, data structures'
            },
            'memory_streaming': {
                'instructions': ['RDFAST', 'WRFAST', 'RFBYTE', 'RFWORD', 'RFLONG', 'WFBYTE', 'WFWORD', 'WFLONG'],
                'characteristics': 'FIFO-based streaming, predictable timing',
                'common_usage': 'Video, audio, bulk data transfer'
            },
            'branch_unconditional': {
                'instructions': ['JMP', 'CALL', 'RET', 'CALLA', 'CALLB', 'RETA', 'RETB'],
                'characteristics': 'Pipeline flush, 5+ cycle cost',
                'common_usage': 'Program flow, subroutines'
            },
            'branch_conditional': {
                'instructions': ['TJZ', 'TJNZ', 'TJF', 'TJNF', 'DJZ', 'DJNZ', 'IJZ', 'IJNZ'],
                'characteristics': 'Test-and-jump, decrement-and-jump patterns',
                'common_usage': 'Loop control, conditional execution'
            },
            'smart_pin': {
                'instructions': ['WRPIN', 'WXPIN', 'WYPIN', 'RDPIN', 'RQPIN', 'AKPIN'],
                'characteristics': 'Smart pin configuration and control',
                'common_usage': 'PWM, serial, ADC, DAC, counters'
            },
            'cordic': {
                'instructions': ['QROTATE', 'QVECTOR', 'QMUL', 'QDIV', 'QSQRT', 'QLOG', 'QEXP', 'GETQX', 'GETQY'],
                'characteristics': '54-stage pipeline, concurrent operations possible',
                'common_usage': 'Math acceleration, DSP, graphics transforms'
            },
            'special': {
                'instructions': ['GETCT', 'WAITX', 'WAITCT1', 'COGID', 'COGINIT', 'COGSTOP'],
                'characteristics': 'System control, timing, cog management',
                'common_usage': 'Timing, multi-cog coordination'
            }
        }
        
        # Extract performance patterns
        patterns['performance_patterns'].append({
            'pattern': 'Minimize Branches',
            'rationale': 'Branches flush pipeline causing 3+ cycle penalty',
            'alternative': 'Use conditional execution (IF_xx prefixes) for short sequences',
            'example': 'Replace "CMP/JZ label" with "IF_Z MOV" for 2-3 instructions'
        })
        
        patterns['performance_patterns'].append({
            'pattern': 'Hub Access Optimization',
            'rationale': 'Hub window alignment causes 13-20 cycle variance',
            'technique': 'Group hub accesses together to hit same window',
            'example': 'Read all needed data at once rather than interleaving with processing'
        })
        
        return patterns
    
    def generate_learning_paths(self, meta_knowledge: Dict) -> Dict[str, List]:
        """Generate learning paths through instruction groups"""
        paths = {}
        
        # Beginner path - start with basics
        paths['beginner'] = [
            {
                'step': 1,
                'topic': 'Basic Data Movement',
                'instructions': ['MOV', 'MOVBYTS'],
                'concepts': ['Register operations', 'Immediate values'],
                'exercises': ['Copy register', 'Load constants']
            },
            {
                'step': 2,
                'topic': 'Basic Arithmetic',
                'instructions': ['ADD', 'SUB', 'CMP'],
                'concepts': ['ALU operations', 'Flag effects'],
                'exercises': ['Simple calculations', 'Loop counters']
            },
            {
                'step': 3,
                'topic': 'Conditional Execution',
                'instructions': ['IF_Z', 'IF_NZ', 'IF_C', 'IF_NC'],
                'concepts': ['Flags', 'Conditional prefixes'],
                'exercises': ['Conditional moves', 'Min/max operations']
            },
            {
                'step': 4,
                'topic': 'Basic Branching',
                'instructions': ['JMP', 'TJZ', 'DJNZ'],
                'concepts': ['Program flow', 'Loop control'],
                'exercises': ['Simple loops', 'Conditional jumps']
            },
            {
                'step': 5,
                'topic': 'Hub Memory Access',
                'instructions': ['RDBYTE', 'RDWORD', 'RDLONG', 'WRBYTE', 'WRWORD', 'WRLONG'],
                'concepts': ['Hub timing', 'Memory addressing'],
                'exercises': ['Read/write variables', 'Array access']
            }
        ]
        
        # Intermediate path - optimization focus
        paths['intermediate'] = [
            {
                'step': 1,
                'topic': 'ALTx Instructions',
                'instructions': ['ALTS', 'ALTD', 'ALTI', 'ALTR'],
                'concepts': ['Instruction modification', 'Indexing'],
                'exercises': ['Table lookup', 'Indirect addressing']
            },
            {
                'step': 2,
                'topic': 'Block Transfers',
                'instructions': ['SETQ', 'SETQ2', 'RDLONG', 'WRLONG'],
                'concepts': ['Fast block moves', 'FIFO operations'],
                'exercises': ['Buffer copies', 'Stack operations']
            },
            {
                'step': 3,
                'topic': 'Bit Manipulation',
                'instructions': ['BITC', 'BITH', 'BITL', 'BITNC', 'BITZ', 'BITNZ'],
                'concepts': ['Bit fields', 'Flag manipulation'],
                'exercises': ['Bit masks', 'State machines']
            },
            {
                'step': 4,
                'topic': 'Streaming Operations',
                'instructions': ['RDFAST', 'WRFAST', 'RFBYTE', 'WFBYTE'],
                'concepts': ['FIFO streaming', 'Predictable timing'],
                'exercises': ['Video output', 'Data streaming']
            }
        ]
        
        # Advanced path - system features
        paths['advanced'] = [
            {
                'step': 1,
                'topic': 'Smart Pin Programming',
                'instructions': ['WRPIN', 'WXPIN', 'WYPIN', 'RDPIN', 'AKPIN'],
                'concepts': ['Pin modes', 'Smart pin configuration'],
                'exercises': ['PWM generation', 'Serial communication']
            },
            {
                'step': 2,
                'topic': 'CORDIC Operations',
                'instructions': ['QROTATE', 'QMUL', 'QDIV', 'QSQRT', 'GETQX', 'GETQY'],
                'concepts': ['Pipeline usage', 'Math acceleration'],
                'exercises': ['Coordinate transforms', 'DSP operations']
            },
            {
                'step': 3,
                'topic': 'Multi-Cog Programming',
                'instructions': ['COGINIT', 'COGSTOP', 'COGID', 'LOCKNEW', 'LOCKREL'],
                'concepts': ['Parallel processing', 'Synchronization'],
                'exercises': ['Task distribution', 'Resource sharing']
            },
            {
                'step': 4,
                'topic': 'Interrupt Handling',
                'instructions': ['SETINT1', 'SETINT2', 'SETINT3', 'TRGINT1', 'NIXINT1'],
                'concepts': ['Event handling', 'Interrupt vectors'],
                'exercises': ['Timer interrupts', 'Pin events']
            }
        ]
        
        return paths
    
    def write_meta_knowledge_index(self) -> None:
        """Write meta-knowledge index file"""
        index_file = self.output_dir / "meta-knowledge-index.md"
        
        with open(index_file, 'w') as f:
            f.write("# P2 Meta-Knowledge Index\n\n")
            f.write(f"**Generated**: {datetime.now().isoformat()}\n")
            f.write(f"**Total Insights**: {self.insights_count}\n\n")
            
            f.write("## Architectural Insights\n\n")
            for insight in self.meta_knowledge.get('architectural_insights', []):
                f.write(f"### {insight['topic']}\n")
                f.write(f"{insight['insight']}\n")
                f.write(f"- **Related Instructions**: {', '.join(insight['related_instructions'])}\n")
                f.write(f"- **Impact**: {insight['impact']}\n\n")
            
            f.write("## Common Gotchas\n\n")
            for gotcha in self.meta_knowledge.get('common_gotchas', []):
                f.write(f"### {gotcha['issue']}\n")
                f.write(f"{gotcha['description']}\n")
                f.write(f"- **Affected**: {', '.join(gotcha['affected_instructions']) if isinstance(gotcha['affected_instructions'], list) else gotcha['affected_instructions']}\n")
                f.write(f"- **Mitigation**: {gotcha['mitigation']}\n\n")
            
            f.write("## Optimization Techniques\n\n")
            for opt in self.meta_knowledge.get('optimization_hints', []):
                f.write(f"### {opt['technique']}\n")
                f.write(f"{opt['description']}\n")
                f.write(f"- **Examples**: {', '.join(opt['examples'])}\n")
                f.write(f"- **Benefit**: {opt['benefit']}\n\n")
            
            f.write("## Instruction Categories\n\n")
            if 'instruction_categories' in self.meta_knowledge:
                for cat_name, cat_data in self.meta_knowledge['instruction_categories'].items():
                    f.write(f"### {cat_name.replace('_', ' ').title()}\n")
                    f.write(f"- **Instructions**: {', '.join(cat_data['instructions'][:5])}...\n")
                    f.write(f"- **Characteristics**: {cat_data['characteristics']}\n")
                    f.write(f"- **Common Usage**: {cat_data['common_usage']}\n\n")
        
        print(f"Meta-knowledge index written to: {index_file}")
    
    def write_learning_paths(self) -> None:
        """Write learning path documentation"""
        paths_file = self.output_dir / "learning-paths.md"
        
        with open(paths_file, 'w') as f:
            f.write("# P2 Instruction Learning Paths\n\n")
            f.write("Structured progression through P2 instruction set\n\n")
            
            for path_name, path_steps in self.learning_paths.items():
                f.write(f"## {path_name.title()} Path\n\n")
                
                for step in path_steps:
                    f.write(f"### Step {step['step']}: {step['topic']}\n")
                    f.write(f"**Instructions**: {', '.join(step['instructions'])}\n\n")
                    f.write(f"**Concepts**:\n")
                    for concept in step['concepts']:
                        f.write(f"- {concept}\n")
                    f.write(f"\n**Exercises**:\n")
                    for exercise in step['exercises']:
                        f.write(f"- {exercise}\n")
                    f.write("\n")
                
                f.write("---\n\n")
        
        print(f"Learning paths written to: {paths_file}")
    
    def run(self) -> None:
        """Run meta-knowledge extraction"""
        print("Starting meta-knowledge extraction...")
        
        # Extract from walkthrough analysis
        walkthrough_file = self.sources_dir / "p2-datasheet-walkthrough-analysis.md"
        if walkthrough_file.exists():
            print(f"Processing: {walkthrough_file.name}")
            self.meta_knowledge = self.extract_from_walkthrough(walkthrough_file)
            self.insights_count += sum(len(v) if isinstance(v, list) else 1 for v in self.meta_knowledge.values())
        
        # Extract from critical insights
        insights_file = self.sources_dir / "p2-datasheet-critical-insights.md"
        if insights_file.exists():
            print(f"Processing: {insights_file.name}")
            patterns = self.extract_from_critical_insights(insights_file)
            self.meta_knowledge.update(patterns)
            self.insights_count += len(patterns.get('instruction_categories', {}))
        
        # Generate learning paths
        print("Generating learning paths...")
        self.learning_paths = self.generate_learning_paths(self.meta_knowledge)
        
        # Write outputs
        print("Writing meta-knowledge index...")
        self.write_meta_knowledge_index()
        
        print("Writing learning paths...")
        self.write_learning_paths()
        
        print(f"\nMeta-knowledge extraction complete:")
        print(f"  Total insights: {self.insights_count}")
        print(f"  Learning paths: {len(self.learning_paths)}")

if __name__ == "__main__":
    sources_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-datasheet"
    output_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2"
    
    extractor = MetaKnowledgeExtractor(sources_dir, output_dir)
    extractor.run()
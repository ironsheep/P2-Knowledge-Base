#!/usr/bin/env python3
"""
Generate AI Reference deliverables from YAML source files.
This creates the packaged, versioned content for AI consumption.
"""

import json
import yaml
import os
from pathlib import Path
from datetime import datetime
import shutil
from typing import Dict, List, Any

class AIReferenceGenerator:
    def __init__(self, version: str):
        self.version = version
        self.timestamp = datetime.now().isoformat()
        self.base_path = Path.cwd()
        self.kb_path = self.base_path / "engineering/knowledge-base/P2"
        self.output_path = self.base_path / "deliverables/ai-reference" / f"v{version}"
        self.stats = {
            "instructions": 0,
            "keywords": 0,
            "operators": 0,
            "methods": 0,
            "registers": 0,
            "assembly_directives": 0,
            "debug_commands": 0,
            "special_symbols": 0,
            "system_variables": 0,
            "total_elements": 0
        }
        
    def load_yaml(self, file_path: Path) -> Dict:
        """Load and parse a YAML file."""
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    
    def collect_spin2_elements(self) -> Dict[str, List[Dict]]:
        """Collect all SPIN2 language elements from YAML files."""
        spin2_path = self.kb_path / "language/spin2"
        elements = {
            "keywords": [],
            "operators": [],
            "methods": [],
            "registers": [],
            "assembly_directives": [],
            "debug_commands": [],
            "special_symbols": [],
            "system_variables": []
        }
        
        for category in elements.keys():
            category_path = spin2_path / category.replace("_", "-")
            if category_path.exists():
                for yaml_file in category_path.glob("*.yaml"):
                    if yaml_file.name != "manifest.yaml":
                        try:
                            data = self.load_yaml(yaml_file)
                            if data:
                                elements[category].append(data)
                                self.stats[category] += 1
                        except Exception as e:
                            print(f"Error loading {yaml_file}: {e}")
        
        return elements
    
    def collect_instructions(self) -> List[Dict]:
        """Collect PASM2 instructions from deliverables (until we have YAMLs)."""
        # For now, we'll collect from the existing deliverables
        # In future, this should read from engineering/knowledge-base/P2/instructions/
        instructions = []
        pasm_path = self.base_path / "deliverables/ai-reference/p2-claude-knowledge/instruction-knowledge"
        
        if pasm_path.exists():
            for yaml_file in pasm_path.glob("*.yaml"):
                try:
                    data = self.load_yaml(yaml_file)
                    if data:
                        instructions.append(data)
                        self.stats["instructions"] += 1
                except Exception as e:
                    print(f"Error loading {yaml_file}: {e}")
        
        return instructions
    
    def generate_manifest(self, elements: Dict) -> Dict:
        """Generate a manifest of all elements."""
        manifest = {
            "version": self.version,
            "generated": self.timestamp,
            "statistics": self.stats,
            "categories": {}
        }
        
        for category, items in elements.items():
            if items:
                manifest["categories"][category] = {
                    "count": len(items),
                    "elements": [self.get_element_summary(item) for item in items]
                }
        
        self.stats["total_elements"] = sum(self.stats.values())
        manifest["statistics"]["total_elements"] = self.stats["total_elements"]
        
        return manifest
    
    def get_element_summary(self, element: Dict) -> Dict:
        """Extract summary information from an element."""
        # Adapt based on element structure
        summary = {}
        
        # Common fields across different element types
        if "name" in element:
            summary["name"] = element["name"]
        elif "keyword" in element:
            summary["name"] = element["keyword"]
        elif "operator" in element:
            summary["name"] = element["operator"]
        elif "method" in element:
            summary["name"] = element["method"]
        elif "register" in element:
            summary["name"] = element["register"]
        elif "directive" in element:
            summary["name"] = element["directive"]
        elif "command" in element:
            summary["name"] = element["command"]
        elif "symbol" in element:
            summary["name"] = element["symbol"]
        elif "variable" in element:
            summary["name"] = element["variable"]
            
        if "description" in element:
            summary["description"] = element["description"][:100] + "..." if len(element.get("description", "")) > 100 else element.get("description", "")
            
        if "category" in element:
            summary["category"] = element["category"]
            
        return summary
    
    def generate_coverage_report(self) -> Dict:
        """Generate a coverage report."""
        return {
            "version": self.version,
            "generated": self.timestamp,
            "coverage": {
                "pasm2_instructions": {
                    "documented": self.stats["instructions"],
                    "estimated_total": 350,  # Approximate
                    "percentage": round(self.stats["instructions"] / 350 * 100, 1)
                },
                "spin2_elements": {
                    "documented": sum([self.stats[k] for k in self.stats if k != "instructions" and k != "total_elements"]),
                    "categories": {
                        "keywords": self.stats["keywords"],
                        "operators": self.stats["operators"],
                        "methods": self.stats["methods"],
                        "registers": self.stats["registers"],
                        "assembly_directives": self.stats["assembly_directives"],
                        "debug_commands": self.stats["debug_commands"],
                        "special_symbols": self.stats["special_symbols"],
                        "system_variables": self.stats["system_variables"]
                    }
                },
                "total_elements": self.stats["total_elements"]
            }
        }
    
    def create_output_structure(self):
        """Create the output directory structure."""
        self.output_path.mkdir(parents=True, exist_ok=True)
        (self.output_path / "instructions" / "PASM2").mkdir(parents=True, exist_ok=True)
        (self.output_path / "language" / "spin2").mkdir(parents=True, exist_ok=True)
        (self.output_path / "manifests").mkdir(parents=True, exist_ok=True)
        (self.output_path / "schemas").mkdir(parents=True, exist_ok=True)
    
    def copy_yaml_files(self, elements: Dict):
        """Copy YAML files to output structure."""
        spin2_path = self.kb_path / "language/spin2"
        output_spin2 = self.output_path / "language/spin2"
        
        for category in elements.keys():
            category_path = spin2_path / category.replace("_", "-")
            if category_path.exists():
                output_category = output_spin2 / category.replace("_", "-")
                output_category.mkdir(parents=True, exist_ok=True)
                
                for yaml_file in category_path.glob("*.yaml"):
                    if yaml_file.name != "manifest.yaml":
                        shutil.copy2(yaml_file, output_category / yaml_file.name)
    
    def write_version_file(self):
        """Write version information."""
        version_info = {
            "version": self.version,
            "generated": self.timestamp,
            "source": "engineering/knowledge-base/P2",
            "generator": "generate-ai-reference-from-yaml.py"
        }
        
        with open(self.output_path / "VERSION", 'w') as f:
            f.write(f"{self.version}\n")
            
        with open(self.output_path / "version.json", 'w') as f:
            json.dump(version_info, f, indent=2)
    
    def write_readme(self):
        """Write README for the release."""
        readme = f"""# P2 AI Reference v{self.version}

Generated: {self.timestamp}

## Contents

This release contains {self.stats['total_elements']} documented elements:

- PASM2 Instructions: {self.stats['instructions']}
- SPIN2 Keywords: {self.stats['keywords']}
- SPIN2 Operators: {self.stats['operators']}
- SPIN2 Methods: {self.stats['methods']}
- Registers: {self.stats['registers']}
- Assembly Directives: {self.stats['assembly_directives']}
- Debug Commands: {self.stats['debug_commands']}
- Special Symbols: {self.stats['special_symbols']}
- System Variables: {self.stats['system_variables']}

## Usage

### For AI Systems
1. Load the manifest files from `manifests/` for element discovery
2. Load individual YAML files as needed from their respective directories
3. Use schemas from `schemas/` for validation

### For Developers
- All elements are in YAML format for easy parsing
- Each element follows a consistent schema
- Manifests provide quick lookup without parsing all files

## Source
Generated from: engineering/knowledge-base/P2/
Repository: https://github.com/ironsheep/P2-Knowledge-Base
"""
        
        with open(self.output_path / "README.md", 'w') as f:
            f.write(readme)
    
    def generate(self):
        """Main generation process."""
        print(f"Generating AI Reference v{self.version}...")
        
        # Create output structure
        self.create_output_structure()
        
        # Collect all elements
        print("Collecting SPIN2 elements...")
        spin2_elements = self.collect_spin2_elements()
        
        print("Collecting PASM2 instructions...")
        instructions = self.collect_instructions()
        
        # Generate manifest
        print("Generating manifest...")
        all_elements = {"instructions": instructions, **spin2_elements}
        manifest = self.generate_manifest(all_elements)
        
        with open(self.output_path / "manifests" / "complete-manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        # Generate coverage report
        print("Generating coverage report...")
        coverage = self.generate_coverage_report()
        
        with open(self.output_path / "manifests" / "coverage-report.json", 'w') as f:
            json.dump(coverage, f, indent=2)
        
        # Copy YAML files
        print("Copying YAML files...")
        self.copy_yaml_files(spin2_elements)
        
        # Copy instruction YAMLs (temporary until we have them in kb)
        pasm_source = self.base_path / "deliverables/ai-reference/p2-claude-knowledge/instruction-knowledge"
        pasm_dest = self.output_path / "instructions/PASM2"
        if pasm_source.exists():
            for yaml_file in pasm_source.glob("*.yaml"):
                shutil.copy2(yaml_file, pasm_dest / yaml_file.name)
        
        # Write metadata files
        self.write_version_file()
        self.write_readme()
        
        print(f"\nGeneration complete!")
        print(f"Output: {self.output_path}")
        print(f"Total elements: {self.stats['total_elements']}")
        
        return self.stats


if __name__ == "__main__":
    import sys
    
    version = sys.argv[1] if len(sys.argv) > 1 else "2.0.0"
    
    generator = AIReferenceGenerator(version)
    stats = generator.generate()
    
    print("\nGeneration Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
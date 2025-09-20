#!/usr/bin/env python3
"""
Update the P2 reference JSON with BOTH PASM2 and SPIN2 from YAML sources.
Uses engineering/knowledge-base/P2/ as the single source of truth.
"""

import json
import yaml
import os
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Any

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle datetime objects."""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

class P2CompleteReferenceUpdater:
    def __init__(self, version: str = "1.3.0"):
        self.version = version
        self.timestamp = datetime.now().isoformat()
        self.base_path = Path.cwd()
        self.kb_path = self.base_path / "engineering/knowledge-base/P2"
        
        # Start with existing JSON structure
        self.existing_json_path = self.base_path / "deliverables/ai-reference/versions/v0.1.0/p2-reference-v0.1.0.json"
        with open(self.existing_json_path, 'r') as f:
            self.reference = json.load(f)
            
        self.stats = {
            "pasm2_instructions": 0,
            "spin2_keywords": 0,
            "spin2_operators": 0,
            "spin2_methods": 0,
            "spin2_registers": 0,
            "spin2_assembly_directives": 0,
            "spin2_debug_commands": 0,
            "spin2_special_symbols": 0,
            "spin2_system_variables": 0
        }
    
    def load_yaml(self, file_path: Path) -> Dict:
        """Load and parse a YAML file."""
        try:
            with open(file_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None
    
    def collect_pasm2_instructions(self) -> Dict[str, Dict]:
        """Collect all PASM2 instructions from YAML files."""
        instructions = {}
        pasm2_path = self.kb_path / "language/pasm2"
        
        if pasm2_path.exists():
            for yaml_file in pasm2_path.glob("*.yaml"):
                if yaml_file.is_file():
                    data = self.load_yaml(yaml_file)
                    if data and "instruction" in data:
                        name = data["instruction"]
                        instructions[name] = data
                        self.stats["pasm2_instructions"] += 1
        
        return instructions
    
    def build_pasm2_section(self) -> Dict:
        """Build complete PASM2 instructions section with full details."""
        print("Collecting PASM2 instructions...")
        instructions = self.collect_pasm2_instructions()
        
        # Group instructions by category
        categories = {}
        for name, inst in instructions.items():
            category = inst.get("category", inst.get("group", "Uncategorized"))
            if category not in categories:
                categories[category] = {
                    "count": 0,
                    "description": category,
                    "instructions": {}
                }
            
            categories[category]["instructions"][name] = {
                "mnemonic": name,
                "syntax": inst.get("syntax", ""),
                "encoding": inst.get("encoding", ""),
                "description": inst.get("description", ""),
                "timing": inst.get("timing", {}),
                "flags_affected": inst.get("flags_affected", {}),
                "parameters": inst.get("parameters", []),
                "related": inst.get("related", []),
                "compiler_info": {
                    "syntax": inst.get("compiler_syntax", ""),
                    "encoding": inst.get("compiler_encoding", {}),
                    "category": inst.get("compiler_category", ""),
                    "effects": inst.get("compiler_effects", []),
                    "operand_format": inst.get("compiler_operand_format", {})
                },
                "documentation_source": inst.get("documentation_source", ""),
                "documentation_level": inst.get("documentation_level", "")
            }
            categories[category]["count"] += 1
        
        return {
            "total_count": self.stats["pasm2_instructions"],
            "source": "engineering/knowledge-base/P2/language/pasm2/",
            "extraction_date": self.timestamp,
            "categories": categories
        }
    
    def collect_spin2_category(self, category: str) -> List[Dict]:
        """Collect all elements from a SPIN2 category."""
        elements = []
        category_path = self.kb_path / "language/spin2" / category.replace("_", "-")
        
        if category_path.exists():
            for yaml_file in category_path.glob("*.yaml"):
                if yaml_file.name not in ["manifest.yaml", "unknown.yaml"]:
                    data = self.load_yaml(yaml_file)
                    if data:
                        elements.append(data)
                        self.stats[f"spin2_{category}"] += 1
        
        return elements
    
    def build_spin2_section(self) -> Dict:
        """Build complete SPIN2 language section."""
        print("Collecting SPIN2 elements...")
        spin2 = {
            "version": "1.51.5",
            "source": "engineering/knowledge-base/P2/language/spin2/",
            "extraction_date": self.timestamp,
            "categories": {}
        }
        
        # Process each SPIN2 category
        categories_to_process = [
            "keywords", "operators", "methods", "registers",
            "assembly_directives", "debug_commands", 
            "special_symbols", "system_variables"
        ]
        
        for category in categories_to_process:
            elements = self.collect_spin2_category(category)
            if elements:
                spin2["categories"][category] = {
                    "count": len(elements),
                    "elements": {}
                }
                
                for elem in elements:
                    # Get the element name based on category
                    if category == "keywords":
                        name = elem.get("keyword", "unknown")
                    elif category == "operators":
                        name = elem.get("operator", "unknown")
                    elif category == "methods":
                        name = elem.get("method", "unknown")
                    elif category == "registers":
                        name = elem.get("register", "unknown")
                    elif category == "assembly_directives":
                        name = elem.get("name", elem.get("directive", "unknown"))
                    elif category == "debug_commands":
                        name = elem.get("command", "unknown")
                    elif category == "special_symbols":
                        name = elem.get("symbol", "unknown")
                    elif category == "system_variables":
                        name = elem.get("variable", "unknown")
                    
                    # Store full element data
                    spin2["categories"][category]["elements"][name] = elem
        
        # Add statistics
        total_spin2 = sum(v for k, v in self.stats.items() if k.startswith("spin2_"))
        spin2["statistics"] = {
            "total_elements": total_spin2,
            "by_category": {k.replace("spin2_", ""): v for k, v in self.stats.items() if k.startswith("spin2_")}
        }
        
        return spin2
    
    def update_meta_section(self):
        """Update metadata for new version."""
        self.reference["meta"]["version"] = self.version
        self.reference["meta"]["release_date"] = datetime.now().strftime("%Y-%m-%d")
        self.reference["meta"]["completeness"] = 0.95  # Updated from 0.85
        self.reference["meta"]["last_updated"] = self.timestamp
        self.reference["meta"]["sources"]["pasm2"] = "engineering/knowledge-base/P2/language/pasm2/"
        self.reference["meta"]["sources"]["spin2"] = "engineering/knowledge-base/P2/language/spin2/ (PNUT-TS v1.51.5)"
        
    def save_updated_reference(self):
        """Save the updated reference JSON."""
        output_dir = self.base_path / "deliverables/ai-reference/versions" / f"v{self.version}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"p2-reference-v{self.version}.json"
        
        with open(output_file, 'w') as f:
            json.dump(self.reference, f, indent=2, cls=DateTimeEncoder)
        
        return output_file
    
    def generate_summary(self):
        """Generate summary of what was included."""
        summary = f"""
P2 Reference v{self.version} - Complete Update Summary
========================================================

PASM2 Instructions: {self.stats['pasm2_instructions']} (from YAMLs)
  - Full instruction details
  - Timing, encoding, flags
  - Compiler metadata
  
SPIN2 Elements: {sum(v for k, v in self.stats.items() if k.startswith('spin2_'))}
  - Keywords: {self.stats['spin2_keywords']}
  - Operators: {self.stats['spin2_operators']}
  - Methods: {self.stats['spin2_methods']}
  - Registers: {self.stats['spin2_registers']}
  - Assembly Directives: {self.stats['spin2_assembly_directives']}
  - Debug Commands: {self.stats['spin2_debug_commands']}
  - Special Symbols: {self.stats['spin2_special_symbols']}
  - System Variables: {self.stats['spin2_system_variables']}

Total Elements: {sum(self.stats.values())}

Source: engineering/knowledge-base/P2/
"""
        return summary
    
    def update(self):
        """Main update process."""
        print(f"Updating P2 Reference to v{self.version} with COMPLETE data...")
        
        # Build PASM2 section from YAMLs
        print("Building PASM2 instructions section...")
        pasm2_section = self.build_pasm2_section()
        self.reference["instructions"] = pasm2_section
        
        # Build SPIN2 section from YAMLs
        print("Building SPIN2 language section...")
        spin2_section = self.build_spin2_section()
        self.reference["spin2"] = spin2_section
        
        # Update metadata
        print("Updating metadata...")
        self.update_meta_section()
        
        # Save updated reference
        print("Saving updated reference...")
        output_file = self.save_updated_reference()
        
        # Print summary
        summary = self.generate_summary()
        print(summary)
        
        print(f"✅ Update complete!")
        print(f"   Output: {output_file}")
        
        return self.stats


if __name__ == "__main__":
    import sys
    version = sys.argv[1] if len(sys.argv) > 1 else "1.3.0"
    updater = P2CompleteReferenceUpdater(version=version)
    stats = updater.update()
#!/usr/bin/env python3
"""
Package P2 Knowledge Base into two release artifacts:
1. P2 Reference JSON Package - Single JSON with schemas
2. P2 Knowledge YAMLs Package - Modular YAMLs with manifests
"""

import json
import yaml
import os
import shutil
import tarfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class P2ReleasePackager:
    def __init__(self, version: str = "1.3.0"):
        self.version = version
        self.timestamp = datetime.now().isoformat()
        self.base_path = Path.cwd()
        self.kb_path = self.base_path / "engineering/knowledge-base/P2"
        self.release_path = self.base_path / "releases" / f"v{version}"
        
        # Create release directory
        self.release_path.mkdir(parents=True, exist_ok=True)
        
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
            print(f"Warning: Could not load {file_path}: {e}")
            return None
    
    def create_root_manifest(self) -> Dict:
        """Create the root manifest that serves as the main entry point."""
        return {
            "manifest_version": "1.0.0",
            "knowledge_base_version": self.version,
            "generated": self.timestamp,
            "structure": {
                "architecture": {
                    "description": "P2 Hardware Architecture Components",
                    "manifest": "manifests/architecture-manifest.json",
                    "directory": "architecture/",
                    "count": self.stats.get("architecture", 0)
                },
                "hardware": {
                    "description": "P2 Hardware Specifications and Pinouts",
                    "manifest": "manifests/hardware-manifest.json",
                    "directory": "hardware/",
                    "count": self.stats.get("hardware", 0)
                },
                "code-examples": {
                    "description": "P2 Code Examples and Patterns",
                    "manifest": "manifests/code-examples-manifest.json",
                    "directory": "code-examples/",
                    "count": self.stats.get("code_examples", 0)
                },
                "pasm2": {
                    "description": "PASM2 Assembly Language Instructions",
                    "manifest": "manifests/pasm2-manifest.json",
                    "directory": "language/pasm2/",
                    "count": self.stats["pasm2_instructions"]
                },
                "spin2": {
                    "description": "SPIN2 High-Level Language Elements",
                    "manifest": "manifests/spin2-manifest.json",
                    "categories": {
                        "keywords": {
                            "manifest": "manifests/spin2-keywords-manifest.json",
                            "directory": "spin2/keywords/",
                            "count": self.stats["spin2_keywords"]
                        },
                        "operators": {
                            "manifest": "manifests/spin2-operators-manifest.json",
                            "directory": "spin2/operators/",
                            "count": self.stats["spin2_operators"]
                        },
                        "methods": {
                            "manifest": "manifests/spin2-methods-manifest.json",
                            "directory": "spin2/methods/",
                            "count": self.stats["spin2_methods"]
                        },
                        "registers": {
                            "manifest": "manifests/spin2-registers-manifest.json",
                            "directory": "spin2/registers/",
                            "count": self.stats["spin2_registers"]
                        },
                        "assembly_directives": {
                            "manifest": "manifests/spin2-assembly-directives-manifest.json",
                            "directory": "spin2/assembly-directives/",
                            "count": self.stats["spin2_assembly_directives"]
                        },
                        "debug_commands": {
                            "manifest": "manifests/spin2-debug-commands-manifest.json",
                            "directory": "spin2/debug-commands/",
                            "count": self.stats["spin2_debug_commands"]
                        },
                        "special_symbols": {
                            "manifest": "manifests/spin2-special-symbols-manifest.json",
                            "directory": "spin2/special-symbols/",
                            "count": self.stats["spin2_special_symbols"]
                        },
                        "system_variables": {
                            "manifest": "manifests/spin2-system-variables-manifest.json",
                            "directory": "spin2/system-variables/",
                            "count": self.stats["spin2_system_variables"]
                        }
                    }
                }
            },
            "total_elements": sum(self.stats.values()),
            "sources": {
                "repository": "https://github.com/ironsheep/P2-Knowledge-Base",
                "path": "engineering/knowledge-base/P2/",
                "extraction_date": self.timestamp
            }
        }
    
    def create_pasm2_manifest(self) -> Dict:
        """Create manifest for PASM2 instructions."""
        instructions = []
        pasm2_path = self.kb_path / "language/pasm2"
        
        if pasm2_path.exists():
            for yaml_file in sorted(pasm2_path.glob("*.yaml")):
                if yaml_file.is_file():
                    data = self.load_yaml(yaml_file)
                    if data and "instruction" in data:
                        instructions.append({
                            "name": data["instruction"],
                            "file": f"pasm2/{yaml_file.name}",
                            "category": data.get("category", data.get("group", "Uncategorized")),
                            "syntax": data.get("syntax", ""),
                            "description": data.get("description", "")[:100] + "..."
                                         if len(data.get("description", "")) > 100 
                                         else data.get("description", "")
                        })
                        self.stats["pasm2_instructions"] += 1
        
        return {
            "type": "pasm2_instructions",
            "version": self.version,
            "count": len(instructions),
            "instructions": instructions
        }
    
    def create_spin2_category_manifest(self, category: str) -> Dict:
        """Create manifest for a SPIN2 category."""
        elements = []
        category_path = self.kb_path / "language/spin2" / category.replace("_", "-")
        
        if category_path.exists():
            for yaml_file in sorted(category_path.glob("*.yaml")):
                if yaml_file.name not in ["manifest.yaml", "unknown.yaml"]:
                    data = self.load_yaml(yaml_file)
                    if data:
                        # Get element name based on category
                        name_field = {
                            "keywords": "keyword",
                            "operators": "operator",
                            "methods": "method",
                            "registers": "register",
                            "assembly_directives": "directive",
                            "debug_commands": "command",
                            "special_symbols": "symbol",
                            "system_variables": "variable"
                        }.get(category, "name")
                        
                        name = data.get(name_field, data.get("name", "unknown"))
                        
                        elements.append({
                            "name": name,
                            "file": f"spin2/{category.replace('_', '-')}/{yaml_file.name}",
                            "type": data.get("type", category),
                            "category": data.get("category", ""),
                            "description": data.get("description", "")[:100] + "..."
                                         if len(data.get("description", "")) > 100
                                         else data.get("description", "")
                        })
                        self.stats[f"spin2_{category}"] += 1
        
        return {
            "type": f"spin2_{category}",
            "version": self.version,
            "count": len(elements),
            "elements": elements
        }
    
    def create_spin2_complete_manifest(self) -> Dict:
        """Create complete SPIN2 manifest."""
        return {
            "type": "spin2_complete",
            "version": self.version,
            "categories": {
                "keywords": {
                    "count": self.stats["spin2_keywords"],
                    "manifest": "manifests/spin2-keywords-manifest.json"
                },
                "operators": {
                    "count": self.stats["spin2_operators"],
                    "manifest": "manifests/spin2-operators-manifest.json"
                },
                "methods": {
                    "count": self.stats["spin2_methods"],
                    "manifest": "manifests/spin2-methods-manifest.json"
                },
                "registers": {
                    "count": self.stats["spin2_registers"],
                    "manifest": "manifests/spin2-registers-manifest.json"
                },
                "assembly_directives": {
                    "count": self.stats["spin2_assembly_directives"],
                    "manifest": "manifests/spin2-assembly-directives-manifest.json"
                },
                "debug_commands": {
                    "count": self.stats["spin2_debug_commands"],
                    "manifest": "manifests/spin2-debug-commands-manifest.json"
                },
                "special_symbols": {
                    "count": self.stats["spin2_special_symbols"],
                    "manifest": "manifests/spin2-special-symbols-manifest.json"
                },
                "system_variables": {
                    "count": self.stats["spin2_system_variables"],
                    "manifest": "manifests/spin2-system-variables-manifest.json"
                }
            },
            "total_elements": sum(v for k, v in self.stats.items() if k.startswith("spin2_"))
        }
    
    def package_json_artifact(self):
        """Package the JSON reference artifact."""
        print("Packaging JSON Reference artifact...")
        
        json_dir = self.release_path / f"p2-reference-v{self.version}"
        json_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy main JSON
        source_json = self.base_path / f"deliverables/ai-reference/versions/v{self.version}/p2-reference-v{self.version}.json"
        if source_json.exists():
            shutil.copy2(source_json, json_dir / f"p2-reference-v{self.version}.json")
        
        # Create schemas directory
        schemas_dir = json_dir / "schemas"
        schemas_dir.mkdir(exist_ok=True)
        
        # Create basic schemas
        self.create_json_schemas(schemas_dir)
        
        # Copy changelog and release notes
        source_dir = self.base_path / f"deliverables/ai-reference/versions/v{self.version}"
        for file in ["CHANGELOG.md", "RELEASE-NOTES.md"]:
            if (source_dir / file).exists():
                shutil.copy2(source_dir / file, json_dir / file)
        
        # Create README
        self.create_json_readme(json_dir)
        
        # Create tarball
        tarball = self.release_path / f"p2-reference-v{self.version}.tar.gz"
        with tarfile.open(tarball, "w:gz") as tar:
            tar.add(json_dir, arcname=f"p2-reference-v{self.version}")
        
        print(f"  Created: {tarball}")
        return tarball
    
    def package_yaml_artifact(self):
        """Package the YAML knowledge base artifact."""
        print("Packaging YAML Knowledge Base artifact...")
        
        yaml_dir = self.release_path / f"p2-knowledge-yamls-v{self.version}"
        yaml_dir.mkdir(parents=True, exist_ok=True)
        
        # Create manifests directory
        manifests_dir = yaml_dir / "manifests"
        manifests_dir.mkdir(exist_ok=True)
        
        # Generate PASM2 manifest
        pasm2_manifest = self.create_pasm2_manifest()
        with open(manifests_dir / "pasm2-manifest.json", 'w') as f:
            json.dump(pasm2_manifest, f, indent=2)
        
        # Generate SPIN2 category manifests
        spin2_categories = [
            "keywords", "operators", "methods", "registers",
            "assembly_directives", "debug_commands", 
            "special_symbols", "system_variables"
        ]
        
        for category in spin2_categories:
            manifest = self.create_spin2_category_manifest(category)
            manifest_file = manifests_dir / f"spin2-{category.replace('_', '-')}-manifest.json"
            with open(manifest_file, 'w') as f:
                json.dump(manifest, f, indent=2)
        
        # Generate complete SPIN2 manifest
        spin2_manifest = self.create_spin2_complete_manifest()
        with open(manifests_dir / "spin2-manifest.json", 'w') as f:
            json.dump(spin2_manifest, f, indent=2)
        
        # Generate root manifest (MUST BE LAST - needs stats)
        root_manifest = self.create_root_manifest()
        with open(yaml_dir / "MANIFEST.json", 'w') as f:
            json.dump(root_manifest, f, indent=2)
        
        # Copy YAML files
        self.copy_yaml_files(yaml_dir)
        
        # Create README
        self.create_yaml_readme(yaml_dir)
        
        # Create tarball
        tarball = self.release_path / f"p2-knowledge-yamls-v{self.version}.tar.gz"
        with tarfile.open(tarball, "w:gz") as tar:
            tar.add(yaml_dir, arcname=f"p2-knowledge-yamls-v{self.version}")
        
        print(f"  Created: {tarball}")
        return tarball
    
    def copy_yaml_files(self, target_dir: Path):
        """Copy all YAML files to the target directory."""
        # Copy PASM2 YAMLs
        pasm2_source = self.kb_path / "language/pasm2"
        pasm2_target = target_dir / "pasm2"
        pasm2_target.mkdir(exist_ok=True)
        
        if pasm2_source.exists():
            for yaml_file in pasm2_source.glob("*.yaml"):
                if yaml_file.is_file():
                    shutil.copy2(yaml_file, pasm2_target / yaml_file.name)
        
        # Copy SPIN2 YAMLs
        spin2_source = self.kb_path / "language/spin2"
        spin2_target = target_dir / "spin2"
        
        for category in ["keywords", "operators", "methods", "registers",
                        "assembly-directives", "debug-commands",
                        "special-symbols", "system-variables"]:
            source_dir = spin2_source / category
            if source_dir.exists():
                target_category = spin2_target / category
                target_category.mkdir(parents=True, exist_ok=True)
                
                for yaml_file in source_dir.glob("*.yaml"):
                    if yaml_file.name not in ["manifest.yaml", "unknown.yaml"]:
                        shutil.copy2(yaml_file, target_category / yaml_file.name)
    
    def create_json_schemas(self, schemas_dir: Path):
        """Create JSON schemas for the reference."""
        # Instruction schema
        instruction_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "PASM2 Instruction Schema",
            "type": "object",
            "required": ["mnemonic", "syntax", "description"],
            "properties": {
                "mnemonic": {"type": "string"},
                "syntax": {"type": "string"},
                "encoding": {"type": "string"},
                "description": {"type": "string"},
                "timing": {"type": "object"},
                "flags_affected": {"type": "object"},
                "parameters": {"type": "array"},
                "related": {"type": "array"},
                "compiler_info": {"type": "object"}
            }
        }
        
        with open(schemas_dir / "instruction-schema.json", 'w') as f:
            json.dump(instruction_schema, f, indent=2)
        
        # SPIN2 element schema
        spin2_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "SPIN2 Element Schema",
            "type": "object",
            "required": ["type", "description"],
            "properties": {
                "type": {"type": "string"},
                "category": {"type": "string"},
                "description": {"type": "string"},
                "syntax": {"type": ["string", "array"]},
                "examples": {"type": "array"},
                "parameters": {"type": "array"},
                "returns": {"type": ["string", "object"]}
            }
        }
        
        with open(schemas_dir / "spin2-schema.json", 'w') as f:
            json.dump(spin2_schema, f, indent=2)
    
    def create_json_readme(self, json_dir: Path):
        """Create README for JSON package."""
        readme = f"""# P2 Reference JSON v{self.version}

Complete P2 microcontroller reference for AI code generation.

## Contents
- `p2-reference-v{self.version}.json` - Complete reference (708KB)
- `schemas/` - JSON schemas for validation
- `CHANGELOG.md` - Version changes
- `RELEASE-NOTES.md` - Release information

## Usage

### JavaScript/Node.js
```javascript
const p2ref = require('./p2-reference-v{self.version}.json');
console.log(p2ref.instructions.total_count); // 352
console.log(p2ref.spin2.statistics.total_elements); // 268
```

### Python
```python
import json
with open('p2-reference-v{self.version}.json') as f:
    p2ref = json.load(f)
```

## Structure
- `instructions` - 352 PASM2 instructions with full details
- `spin2` - 268 SPIN2 language elements in 8 categories
- `architecture` - P2 hardware architecture
- `memory_model` - Memory organization
- `code_generation_guidance` - AI code generation hints

## Repository
https://github.com/ironsheep/P2-Knowledge-Base
"""
        
        with open(json_dir / "README.md", 'w') as f:
            f.write(readme)
    
    def create_yaml_readme(self, yaml_dir: Path):
        """Create README for YAML package."""
        readme = f"""# P2 Knowledge YAMLs v{self.version}

Modular P2 knowledge base with individual YAML files and manifests.

## Structure
```
MANIFEST.json                    # Root manifest - START HERE
manifests/                       # Category-specific manifests
├── pasm2-manifest.json         # All PASM2 instructions
├── spin2-manifest.json         # All SPIN2 elements
└── spin2-*-manifest.json       # Individual SPIN2 categories
pasm2/                          # {self.stats['pasm2_instructions']} instruction YAMLs
spin2/                          # {sum(v for k,v in self.stats.items() if k.startswith('spin2_'))} element YAMLs
├── keywords/
├── operators/
├── methods/
├── registers/
├── assembly-directives/
├── debug-commands/
├── special-symbols/
└── system-variables/
```

## Usage

### 1. Start with Root Manifest
```python
import json
with open('MANIFEST.json') as f:
    manifest = json.load(f)
print(f"Total elements: {{manifest['total_elements']}}")
```

### 2. Navigate to Category
```python
# Get PASM2 manifest
with open(manifest['structure']['pasm2']['manifest']) as f:
    pasm2 = json.load(f)
```

### 3. Load Individual Elements
```python
import yaml
for instruction in pasm2['instructions']:
    with open(instruction['file']) as f:
        data = yaml.safe_load(f)
```

## Statistics
- PASM2 Instructions: {self.stats['pasm2_instructions']}
- SPIN2 Elements: {sum(v for k,v in self.stats.items() if k.startswith('spin2_'))}
- Total: {sum(self.stats.values())}

## Repository
https://github.com/ironsheep/P2-Knowledge-Base
"""
        
        with open(yaml_dir / "README.md", 'w') as f:
            f.write(readme)
    
    def package(self):
        """Main packaging process."""
        print(f"\n📦 Packaging P2 Knowledge Base v{self.version}")
        print("=" * 50)
        
        # Package both artifacts
        json_package = self.package_json_artifact()
        yaml_package = self.package_yaml_artifact()
        
        # Create checksums
        self.create_checksums([json_package, yaml_package])
        
        print("\n✅ Packaging complete!")
        print(f"   Release directory: {self.release_path}")
        print(f"   Total elements: {sum(self.stats.values())}")
        
        return self.stats
    
    def create_checksums(self, packages: List[Path]):
        """Create checksums file for packages."""
        import hashlib
        
        checksums_file = self.release_path / f"checksums-v{self.version}.txt"
        
        with open(checksums_file, 'w') as f:
            for package in packages:
                if package.exists():
                    sha256 = hashlib.sha256()
                    with open(package, 'rb') as pf:
                        sha256.update(pf.read())
                    
                    f.write(f"SHA256 ({package.name}) = {sha256.hexdigest()}\n")
        
        print(f"\n  Created: {checksums_file}")


if __name__ == "__main__":
    import sys
    
    version = sys.argv[1] if len(sys.argv) > 1 else "1.3.0"
    
    packager = P2ReleasePackager(version)
    stats = packager.package()
    
    print("\n📊 Packaging Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
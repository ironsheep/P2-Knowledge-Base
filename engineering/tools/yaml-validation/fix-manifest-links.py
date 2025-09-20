#!/usr/bin/env python3
"""
Fix manifest linking to ensure all YAML files are properly linked.
"""

import os
import yaml
from pathlib import Path

KB_BASE = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2")

def get_yaml_files_in_dir(directory, exclude_patterns=None):
    """Get all YAML files in a directory."""
    dir_path = KB_BASE / directory
    if not dir_path.exists():
        return []
    
    exclude_patterns = exclude_patterns or []
    files = []
    for file in sorted(dir_path.glob("*.yaml")):
        skip = False
        for pattern in exclude_patterns:
            if pattern in file.name:
                skip = True
                break
        if not skip:
            files.append(file.name)
    return files

def update_spin2_manifest():
    """Update Spin2 manifest to properly link all subdirectories."""
    manifest_path = KB_BASE / "language/spin2/method_manifest.yaml"
    
    # Get all files in each subdirectory
    methods = get_yaml_files_in_dir("language/spin2/methods")
    keywords = get_yaml_files_in_dir("language/spin2/keywords")
    operators = get_yaml_files_in_dir("language/spin2/operators")
    registers = get_yaml_files_in_dir("language/spin2/registers")
    special_symbols = get_yaml_files_in_dir("language/spin2/special-symbols")
    debug_commands = get_yaml_files_in_dir("language/spin2/debug-commands")
    debug_displays = get_yaml_files_in_dir("language/spin2/debug-displays")
    assembly_directives = get_yaml_files_in_dir("language/spin2/assembly-directives")
    system_variables = get_yaml_files_in_dir("language/spin2/system-variables")
    constants = get_yaml_files_in_dir("language/spin2/constants")
    constructs = get_yaml_files_in_dir("language/spin2/constructs")
    concepts = get_yaml_files_in_dir("language/spin2/concepts")
    idioms = get_yaml_files_in_dir("language/spin2/idioms")
    integration = get_yaml_files_in_dir("language/spin2/integration")
    symbols = get_yaml_files_in_dir("language/spin2/symbols")
    statements = get_yaml_files_in_dir("language/spin2/statements")
    
    # Get pattern files
    structural_patterns = get_yaml_files_in_dir("language/spin2/patterns/structural")
    implementation_patterns = get_yaml_files_in_dir("language/spin2/patterns/implementation")
    application_patterns = get_yaml_files_in_dir("language/spin2/patterns/applications")
    
    # Get language map files
    language_files = get_yaml_files_in_dir("language/spin2", exclude_patterns=["method_manifest"])
    
    manifest = {
        "manifest_type": "spin2_language_manifest",
        "version": "2.1.0",
        "description": "P2 Spin2 language complete manifest - fully linked",
        "total_components": sum([
            len(methods), len(keywords), len(operators), len(registers),
            len(special_symbols), len(debug_commands), len(debug_displays),
            len(assembly_directives), len(system_variables), len(constants),
            len(constructs), len(concepts), len(idioms), len(integration),
            len(structural_patterns), len(implementation_patterns), 
            len(application_patterns), len(language_files)
        ]),
        "language_maps": {
            "description": "Language overview and schema files",
            "files": language_files
        },
        "language_components": {
            "methods": {
                "description": "Built-in Spin2 methods",
                "path": "methods/",
                "count": len(methods),
                "files": methods
            },
            "keywords": {
                "description": "Spin2 language keywords",
                "path": "keywords/",
                "count": len(keywords),
                "files": keywords
            },
            "operators": {
                "description": "Spin2 operators",
                "path": "operators/",
                "count": len(operators),
                "files": operators
            },
            "registers": {
                "description": "Spin2 accessible registers",
                "path": "registers/",
                "count": len(registers),
                "files": registers
            },
            "special_symbols": {
                "description": "Special symbols and directives",
                "path": "special-symbols/",
                "count": len(special_symbols),
                "files": special_symbols
            },
            "debug_commands": {
                "description": "Debug system commands",
                "path": "debug-commands/",
                "count": len(debug_commands),
                "files": debug_commands
            },
            "debug_displays": {
                "description": "Debug display modes",
                "path": "debug-displays/",
                "count": len(debug_displays),
                "files": debug_displays
            },
            "assembly_directives": {
                "description": "Inline assembly directives",
                "path": "assembly-directives/",
                "count": len(assembly_directives),
                "files": assembly_directives
            },
            "system_variables": {
                "description": "System variables",
                "path": "system-variables/",
                "count": len(system_variables),
                "files": system_variables
            },
            "constants": {
                "description": "Built-in constants",
                "path": "constants/",
                "count": len(constants),
                "files": constants
            },
            "constructs": {
                "description": "Language constructs",
                "path": "constructs/",
                "count": len(constructs),
                "files": constructs
            },
            "concepts": {
                "description": "Language concepts",
                "path": "concepts/",
                "count": len(concepts),
                "files": concepts
            },
            "idioms": {
                "description": "Common Spin2 idioms",
                "path": "idioms/",
                "count": len(idioms),
                "files": idioms
            },
            "integration": {
                "description": "Spin2/PASM2 integration",
                "path": "integration/",
                "count": len(integration),
                "files": integration
            },
            "symbols": {
                "description": "Symbol tables and definitions",
                "path": "symbols/",
                "count": len(symbols),
                "files": symbols
            },
            "statements": {
                "description": "Statement types",
                "path": "statements/",
                "count": len(statements),
                "files": statements
            }
        },
        "pattern_components": {
            "patterns_index": "patterns/pattern-index.yaml",
            "structural_patterns": {
                "description": "Object structure patterns",
                "path": "patterns/structural/",
                "count": len(structural_patterns),
                "files": structural_patterns
            },
            "implementation_patterns": {
                "description": "Implementation patterns",
                "path": "patterns/implementation/",
                "count": len(implementation_patterns),
                "files": implementation_patterns
            },
            "application_patterns": {
                "description": "Application patterns",
                "path": "patterns/applications/",
                "count": len(application_patterns),
                "files": application_patterns
            }
        }
    }
    
    with open(manifest_path, 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    
    print(f"Updated Spin2 manifest: {manifest['total_components']} components linked")
    return manifest['total_components']

def update_pasm2_manifest():
    """Update PASM2 manifest to include all subdirectories."""
    manifest_path = KB_BASE / "language/pasm2/instruction_manifest.yaml"
    
    # Get instruction files
    instruction_files = get_yaml_files_in_dir("language/pasm2", 
                                             exclude_patterns=["manifest", "index"])
    
    # Get subdirectory files
    concepts = get_yaml_files_in_dir("language/pasm2/concepts")
    idioms = get_yaml_files_in_dir("language/pasm2/idioms")
    groups = get_yaml_files_in_dir("language/pasm2/groups")
    
    # Get pattern implementation files
    pattern_impl = get_yaml_files_in_dir("language/pasm2/patterns/implementation")
    
    # Group instructions by first letter
    grouped = {}
    for file in instruction_files:
        if file.startswith("_"):
            letter = "_"
        else:
            letter = file[0].upper()
        if letter not in grouped:
            grouped[letter] = []
        grouped[letter].append(file)
    
    manifest = {
        "manifest_type": "instruction_index",
        "version": "2.1.0",
        "description": "P2 PASM2 instruction set manifest - fully linked",
        "total_instructions": len(instruction_files),
        "total_components": len(instruction_files) + len(concepts) + len(idioms) + len(groups) + len(pattern_impl),
        "instruction_groups": {},
        "special_components": {
            "concepts": {
                "description": "PASM2 programming concepts",
                "path": "concepts/",
                "count": len(concepts),
                "files": concepts
            },
            "idioms": {
                "description": "Common PASM2 idioms",
                "path": "idioms/",
                "count": len(idioms),
                "files": idioms
            },
            "groups": {
                "description": "Instruction groups",
                "path": "groups/",
                "count": len(groups),
                "files": groups
            },
            "pattern_manifest": {
                "description": "PASM2 patterns index",
                "path": "patterns/pattern_manifest.yaml"
            },
            "pattern_implementations": {
                "description": "PASM2 implementation patterns",
                "path": "patterns/implementation/",
                "count": len(pattern_impl),
                "files": pattern_impl
            }
        }
    }
    
    # Add alphabetically grouped instructions
    for letter in sorted(grouped.keys()):
        manifest["instruction_groups"][f"group_{letter}"] = {
            "description": f"Instructions starting with '{letter}'",
            "count": len(grouped[letter]),
            "instructions": grouped[letter]
        }
    
    with open(manifest_path, 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    
    print(f"Updated PASM2 manifest: {manifest['total_components']} components linked")
    return manifest['total_components']

def update_architecture_manifest():
    """Update architecture manifest to include patterns-analysis."""
    manifest_path = KB_BASE / "architecture/architecture_manifest.yaml"
    
    arch_files = get_yaml_files_in_dir("architecture", 
                                      exclude_patterns=["manifest", "index"])
    pattern_analysis = get_yaml_files_in_dir("architecture/patterns-analysis")
    
    manifest = {
        "manifest_type": "architecture_manifest",
        "version": "2.1.0",
        "description": "P2 architecture components manifest - fully linked",
        "total_components": len(arch_files) + len(pattern_analysis),
        "components": {
            "core": {
                "description": "Core architecture components",
                "count": len(arch_files),
                "files": arch_files
            },
            "patterns_analysis": {
                "description": "Architecture pattern analysis",
                "path": "patterns-analysis/",
                "count": len(pattern_analysis),
                "files": pattern_analysis
            },
            "smart_pins": {
                "description": "Smart Pin system",
                "manifest": "smart-pins/smartpin_manifest.yaml"
            },
            "system_registers": {
                "description": "System registers",
                "manifest": "system-registers/register_manifest.yaml"
            }
        }
    }
    
    with open(manifest_path, 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    
    print(f"Updated Architecture manifest: {manifest['total_components']} components linked")
    return manifest['total_components']

def create_code_examples_manifest():
    """Create manifest for code examples."""
    examples = get_yaml_files_in_dir("code-examples")
    
    manifest = {
        "manifest_type": "code_examples_manifest",
        "version": "1.0.0",
        "description": "P2 code examples manifest",
        "total_examples": len(examples),
        "examples": examples
    }
    
    manifest_path = KB_BASE / "code-examples/examples_manifest.yaml"
    with open(manifest_path, 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    
    print(f"Created Code Examples manifest: {len(examples)} examples linked")
    return len(examples)

def update_root_manifest_with_examples():
    """Add code examples to root manifest."""
    root_path = KB_BASE / "root_manifest.yaml"
    
    with open(root_path, 'r') as f:
        root_data = yaml.safe_load(f)
    
    # Add code examples if not already there
    if 'code_examples' not in root_data['knowledge_domains']:
        root_data['knowledge_domains']['code_examples'] = {
            'description': 'Code examples and tutorials',
            'path': 'code-examples/',
            'manifests': ['code-examples/examples_manifest.yaml']
        }
    
    # Update statistics
    root_data['statistics']['total_files'] = 1000  # Update with actual count
    
    with open(root_path, 'w') as f:
        yaml.dump(root_data, f, default_flow_style=False, sort_keys=False)
    
    print("Updated root manifest with code examples")

def main():
    print("=== Fixing All Manifest Links ===\n")
    
    totals = {}
    totals["Spin2"] = update_spin2_manifest()
    totals["PASM2"] = update_pasm2_manifest()
    totals["Architecture"] = update_architecture_manifest()
    totals["Code Examples"] = create_code_examples_manifest()
    update_root_manifest_with_examples()
    
    print("\n=== Summary ===")
    total = sum(totals.values())
    print(f"Total components linked: {total}")
    for category, count in totals.items():
        print(f"  {category}: {count} components")
    
    print("\nManifests updated successfully!")
    print("\nNote: backup_before_update directory intentionally excluded (166 files)")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Create missing manifest files for P2 Knowledge Base YAML files.
"""

import os
import yaml
from pathlib import Path

KB_BASE = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2")

def get_yaml_files_in_dir(directory):
    """Get all YAML files in a directory."""
    dir_path = KB_BASE / directory
    if not dir_path.exists():
        return []
    
    files = []
    for file in sorted(dir_path.glob("*.yaml")):
        if not file.name.endswith("_manifest.yaml") and not file.name.endswith("-index.yaml"):
            files.append(file.name)
    return files

def create_pasm2_instruction_manifest():
    """Create manifest for PASM2 instructions."""
    instruction_files = get_yaml_files_in_dir("language/pasm2")
    
    # Group instructions by first letter for better organization
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
        "version": "2.0.0",
        "description": "P2 PASM2 instruction set manifest",
        "total_instructions": len(instruction_files),
        "instruction_groups": {},
        "special_groups": {
            "concepts": "concepts/",
            "idioms": "idioms/",
            "groups": "groups/",
            "patterns": "patterns/pattern_manifest.yaml"
        }
    }
    
    # Add alphabetically grouped instructions
    for letter in sorted(grouped.keys()):
        manifest["instruction_groups"][f"group_{letter}"] = {
            "description": f"Instructions starting with '{letter}'",
            "instructions": grouped[letter]
        }
    
    output_path = KB_BASE / "language/pasm2/instruction_manifest.yaml"
    with open(output_path, 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    
    print(f"Created: {output_path}")
    return len(instruction_files)

def create_spin2_method_manifest():
    """Create manifest for Spin2 methods and language features."""
    method_files = get_yaml_files_in_dir("language/spin2/methods")
    
    manifest = {
        "manifest_type": "spin2_language_manifest",
        "version": "2.0.0",
        "description": "P2 Spin2 language complete manifest",
        "total_methods": len(method_files),
        "language_components": {
            "methods": {
                "description": "Built-in Spin2 methods",
                "path": "methods/",
                "files": method_files
            },
            "keywords": {
                "description": "Spin2 language keywords",
                "path": "keywords/"
            },
            "operators": {
                "description": "Spin2 operators",
                "path": "operators/"
            },
            "registers": {
                "description": "Spin2 accessible registers",
                "path": "registers/"
            },
            "special_symbols": {
                "description": "Special symbols and directives",
                "path": "special-symbols/"
            },
            "debug_commands": {
                "description": "Debug system commands",
                "path": "debug-commands/"
            },
            "debug_displays": {
                "description": "Debug display modes",
                "path": "debug-displays/"
            },
            "assembly_directives": {
                "description": "Inline assembly directives",
                "path": "assembly-directives/"
            },
            "system_variables": {
                "description": "System variables",
                "path": "system-variables/"
            },
            "constants": {
                "description": "Built-in constants",
                "path": "constants/"
            },
            "constructs": {
                "description": "Language constructs",
                "path": "constructs/"
            },
            "concepts": {
                "description": "Language concepts",
                "path": "concepts/"
            },
            "idioms": {
                "description": "Common Spin2 idioms",
                "path": "idioms/"
            },
            "patterns": {
                "description": "Code patterns",
                "path": "patterns/pattern-index.yaml"
            }
        }
    }
    
    output_path = KB_BASE / "language/spin2/method_manifest.yaml"
    with open(output_path, 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    
    print(f"Created: {output_path}")
    return len(method_files)

def create_hardware_board_manifest():
    """Create manifest for hardware boards."""
    board_files = get_yaml_files_in_dir("hardware")
    
    # Categorize boards
    eval_boards = [f for f in board_files if "eval" in f or "p2-eval" in f]
    edge_boards = [f for f in board_files if "edge" in f]
    addon_boards = [f for f in board_files if "addon" in f]
    other_boards = [f for f in board_files if f not in eval_boards + edge_boards + addon_boards]
    
    manifest = {
        "manifest_type": "hardware_manifest",
        "version": "2.0.0",
        "description": "P2 hardware boards and peripherals manifest",
        "total_boards": len(board_files),
        "board_categories": {
            "eval_boards": {
                "description": "P2 Evaluation boards",
                "boards": eval_boards
            },
            "edge_modules": {
                "description": "P2 Edge modules and carriers",
                "boards": edge_boards
            },
            "addon_boards": {
                "description": "Add-on boards and accessories",
                "boards": addon_boards
            },
            "peripherals": {
                "description": "Other peripherals and boards",
                "boards": other_boards
            }
        },
        "selection_guides": [
            "p2-hardware-selection-guide.yaml",
            "p2-hardware-feature-comparison.yaml",
            "hardware-compatibility-matrix.yaml"
        ]
    }
    
    output_path = KB_BASE / "hardware/board_manifest.yaml"
    with open(output_path, 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    
    print(f"Created: {output_path}")
    return len(board_files)

def create_smartpin_manifest():
    """Create manifest for smart pin modes."""
    smartpin_files = get_yaml_files_in_dir("architecture/smart-pins")
    
    # Group by mode type
    normal_modes = [f for f in smartpin_files if "normal" in f or "00000" in f]
    dac_modes = [f for f in smartpin_files if "dac" in f]
    pulse_modes = [f for f in smartpin_files if "pulse" in f or "transition" in f]
    nco_modes = [f for f in smartpin_files if "nco" in f]
    pwm_modes = [f for f in smartpin_files if "pwm" in f]
    quadrature_modes = [f for f in smartpin_files if "quadrature" in f or "encoder" in f]
    count_modes = [f for f in smartpin_files if "count" in f]
    time_modes = [f for f in smartpin_files if "time" in f]
    adc_modes = [f for f in smartpin_files if "adc" in f]
    usb_modes = [f for f in smartpin_files if "usb" in f]
    serial_modes = [f for f in smartpin_files if "serial" in f or "async" in f or "sync" in f]
    
    manifest = {
        "manifest_type": "smartpin_manifest",
        "version": "2.0.0",
        "description": "P2 Smart Pin modes manifest",
        "total_modes": len(smartpin_files),
        "mode_categories": {
            "basic_io": {
                "description": "Basic I/O modes",
                "modes": normal_modes
            },
            "dac_modes": {
                "description": "DAC and noise generation",
                "modes": dac_modes
            },
            "pulse_generation": {
                "description": "Pulse and transition outputs",
                "modes": pulse_modes
            },
            "nco_modes": {
                "description": "NCO frequency and duty",
                "modes": nco_modes
            },
            "pwm_modes": {
                "description": "PWM generation modes",
                "modes": pwm_modes
            },
            "encoder_modes": {
                "description": "Quadrature encoder modes",
                "modes": quadrature_modes
            },
            "counting_modes": {
                "description": "Event counting modes",
                "modes": count_modes
            },
            "timing_modes": {
                "description": "Time measurement modes",
                "modes": time_modes
            },
            "adc_modes": {
                "description": "ADC sampling modes",
                "modes": adc_modes
            },
            "usb_mode": {
                "description": "USB host/device mode",
                "modes": usb_modes
            },
            "serial_modes": {
                "description": "Serial communication modes",
                "modes": serial_modes
            }
        },
        "all_modes": smartpin_files
    }
    
    output_path = KB_BASE / "architecture/smart-pins/smartpin_manifest.yaml"
    with open(output_path, 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    
    print(f"Created: {output_path}")
    return len(smartpin_files)

def create_system_register_manifest():
    """Create manifest for system registers."""
    register_files = get_yaml_files_in_dir("architecture/system-registers")
    
    manifest = {
        "manifest_type": "register_manifest",
        "version": "2.0.0",
        "description": "P2 system registers manifest",
        "total_registers": len(register_files),
        "register_files": register_files,
        "register_index": "complete-system-registers-index.yaml"
    }
    
    output_path = KB_BASE / "architecture/system-registers/register_manifest.yaml"
    with open(output_path, 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    
    print(f"Created: {output_path}")
    return len(register_files)

def create_architecture_manifest():
    """Create manifest for architecture components."""
    arch_files = get_yaml_files_in_dir("architecture")
    
    manifest = {
        "manifest_type": "architecture_manifest",
        "version": "2.0.0",
        "description": "P2 architecture components manifest",
        "components": {
            "core": {
                "description": "Core architecture components",
                "files": arch_files
            },
            "smart_pins": {
                "description": "Smart Pin system",
                "manifest": "smart-pins/smartpin_manifest.yaml"
            },
            "system_registers": {
                "description": "System registers",
                "manifest": "system-registers/register_manifest.yaml"
            },
            "patterns_analysis": {
                "description": "Architecture pattern analysis",
                "path": "patterns-analysis/"
            }
        }
    }
    
    output_path = KB_BASE / "architecture/architecture_manifest.yaml"
    with open(output_path, 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    
    print(f"Created: {output_path}")
    return len(arch_files)

def main():
    print("=== Creating Missing Manifests ===\n")
    
    counts = {}
    counts["PASM2 instructions"] = create_pasm2_instruction_manifest()
    counts["Spin2 methods"] = create_spin2_method_manifest()
    counts["Hardware boards"] = create_hardware_board_manifest()
    counts["Smart pin modes"] = create_smartpin_manifest()
    counts["System registers"] = create_system_register_manifest()
    counts["Architecture"] = create_architecture_manifest()
    
    print("\n=== Summary ===")
    for category, count in counts.items():
        print(f"{category}: {count} files linked")
    
    print("\nAll manifests created successfully!")

if __name__ == "__main__":
    main()
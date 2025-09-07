#!/usr/bin/env python3
"""
Final validation to ensure all extractions are complete and accurate
"""

from pathlib import Path

def final_validation():
    """Run comprehensive validation of all extracted content"""
    
    # Paths
    kb_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2")
    
    print("=" * 60)
    print("P2 KNOWLEDGE BASE - FINAL VALIDATION")
    print("=" * 60)
    
    # 1. Validate PASM2 Instructions
    print("\n1. PASM2 INSTRUCTIONS")
    print("-" * 40)
    
    pasm2_dir = kb_dir / "instructions" / "pasm2"
    pasm2_files = list(pasm2_dir.glob("*.yaml")) if pasm2_dir.exists() else []
    
    print(f"  Total instruction files: {len(pasm2_files)}")
    
    # Check for expected instructions
    expected_count = 440  # After deduplication
    if len(pasm2_files) == expected_count:
        print(f"  ✅ Count matches expected ({expected_count})")
    else:
        print(f"  ⚠️ Count mismatch: {len(pasm2_files)} vs {expected_count} expected")
    
    # Check layer coverage
    layer_coverage = {
        'layer1_csv': 0,
        'layer2_datasheet': 0,
        'layer3_narrative': 0,
        'layer4_chip': 0
    }
    
    for filepath in pasm2_files:
        with open(filepath, 'r') as f:
            content = f.read()
            for layer in layer_coverage:
                if layer in content:
                    layer_coverage[layer] += 1
    
    print("\n  Layer Coverage:")
    for layer, count in layer_coverage.items():
        percent = (count / len(pasm2_files)) * 100 if pasm2_files else 0
        status = "✅" if percent > 90 else "⚠️" if percent > 10 else "❌"
        print(f"    {status} {layer}: {count}/{len(pasm2_files)} ({percent:.1f}%)")
    
    # 2. Validate Spin2 Language
    print("\n2. SPIN2 LANGUAGE")
    print("-" * 40)
    
    spin2_dir = kb_dir / "language" / "spin2"
    spin2_files = list(spin2_dir.glob("*.yaml")) if spin2_dir.exists() else []
    
    methods = [f for f in spin2_files if 'spin2_op_' not in f.name]
    operators = [f for f in spin2_files if 'spin2_op_' in f.name]
    
    print(f"  Methods: {len(methods)}")
    print(f"  Operators: {len(operators)}")
    print(f"  Total: {len(spin2_files)}")
    
    if len(methods) >= 70:
        print(f"  ✅ Good method coverage ({len(methods)})")
    else:
        print(f"  ⚠️ Low method count ({len(methods)})")
    
    # 3. Validate Hardware Specifications
    print("\n3. HARDWARE SPECIFICATIONS")
    print("-" * 40)
    
    hw_dir = kb_dir / "hardware"
    hw_files = list(hw_dir.glob("*.yaml")) if hw_dir.exists() else []
    
    print(f"  Total hardware specs: {len(hw_files)}")
    
    # Check for key boards
    key_boards = ['p2_eval_board', 'p2_edge_module', 'control_board', '7_segment_display']
    found_boards = []
    for board in key_boards:
        if any(board in f.name for f in hw_files):
            found_boards.append(board)
            print(f"  ✅ Found: {board}")
        else:
            print(f"  ❌ Missing: {board}")
    
    # 4. Validate Architecture Components
    print("\n4. ARCHITECTURE COMPONENTS")
    print("-" * 40)
    
    arch_dir = kb_dir / "architecture"
    arch_files = list(arch_dir.glob("*.yaml")) if arch_dir.exists() else []
    
    print(f"  Total components: {len(arch_files)}")
    
    # Check for key components
    key_components = ['cog', 'hub', 'cordic', 'smart_pins', 'streamer', 'event_system']
    found_components = []
    for component in key_components:
        if any(component in f.name.lower() for f in arch_files):
            found_components.append(component)
            print(f"  ✅ Found: {component}")
        else:
            print(f"  ❌ Missing: {component}")
    
    # 5. Check Manifest
    print("\n5. MANIFEST FILE")
    print("-" * 40)
    
    manifest_path = kb_dir / "manifest.yaml"
    if manifest_path.exists():
        print("  ✅ manifest.yaml exists")
        with open(manifest_path, 'r') as f:
            content = f.read()
            if 'version: 1.0.0' in content:
                print("  ✅ Version 1.0.0 set")
            if 'statistics:' in content:
                print("  ✅ Statistics section present")
            if 'layers:' in content:
                print("  ✅ Layers section present")
    else:
        print("  ❌ manifest.yaml missing")
    
    # 6. Check Quality Report
    print("\n6. QUALITY REPORT")
    print("-" * 40)
    
    quality_report_path = kb_dir / "baseline-quality-report-v1.0.md"
    if quality_report_path.exists():
        print("  ✅ baseline-quality-report-v1.0.md exists")
    else:
        print("  ❌ baseline-quality-report-v1.0.md missing")
    
    # 7. Overall Statistics
    print("\n7. OVERALL STATISTICS")
    print("-" * 40)
    
    total_files = len(pasm2_files) + len(spin2_files) + len(hw_files) + len(arch_files)
    print(f"  Total YAML files: {total_files}")
    print(f"  PASM2 instructions: {len(pasm2_files)}")
    print(f"  Spin2 elements: {len(spin2_files)}")
    print(f"  Hardware specs: {len(hw_files)}")
    print(f"  Architecture components: {len(arch_files)}")
    
    # Final Assessment
    print("\n" + "=" * 60)
    print("FINAL ASSESSMENT")
    print("=" * 60)
    
    issues = []
    
    # Check critical metrics
    if len(pasm2_files) < 400:
        issues.append("Low PASM2 instruction count")
    if layer_coverage.get('layer1_csv', 0) < len(pasm2_files) * 0.9:
        issues.append("Incomplete Layer 1 coverage")
    if len(spin2_files) < 100:
        issues.append("Low Spin2 element count")
    if len(hw_files) < 10:
        issues.append("Low hardware specification count")
    if len(arch_files) < 5:
        issues.append("Low architecture component count")
    
    if not issues:
        print("✅ ALL VALIDATIONS PASSED")
        print("\n🎉 The P2 Knowledge Base v1.0 is ready for release!")
        print("\nNext steps:")
        print("  1. Create git tag v1.0.0")
        print("  2. Commit all changes")
        print("  3. Push to repository")
    else:
        print("⚠️ VALIDATION ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        print("\nRecommendation: Address issues before v1.0 release")
    
    return len(issues) == 0

if __name__ == "__main__":
    success = final_validation()
    exit(0 if success else 1)
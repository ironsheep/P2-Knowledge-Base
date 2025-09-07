#!/usr/bin/env python3
"""
Quality check - spot check 10% of files for extraction accuracy
"""

from pathlib import Path
import random
# import yaml - not available, using text parsing

def quality_check():
    """Spot check 10% of extracted files"""
    
    # Paths
    kb_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2")
    
    # Collect all YAML files
    all_files = []
    
    # PASM2 instructions
    pasm2_dir = kb_dir / "instructions" / "pasm2"
    if pasm2_dir.exists():
        pasm2_files = list(pasm2_dir.glob("*.yaml"))
        all_files.extend(pasm2_files)
    
    # Spin2 language
    spin2_dir = kb_dir / "language" / "spin2"
    if spin2_dir.exists():
        spin2_files = list(spin2_dir.glob("*.yaml"))
        all_files.extend(spin2_files)
    
    # Hardware
    hw_dir = kb_dir / "hardware"
    if hw_dir.exists():
        hw_files = list(hw_dir.glob("*.yaml"))
        all_files.extend(hw_files)
    
    # Architecture
    arch_dir = kb_dir / "architecture"
    if arch_dir.exists():
        arch_files = list(arch_dir.glob("*.yaml"))
        all_files.extend(arch_files)
    
    print(f"Total files found: {len(all_files)}")
    
    # Sample 10%
    sample_size = max(1, len(all_files) // 10)
    sample_files = random.sample(all_files, min(sample_size, len(all_files)))
    
    print(f"Sampling {len(sample_files)} files (10%)")
    print("-" * 60)
    
    # Check each sampled file
    issues = []
    checks_passed = 0
    
    for filepath in sample_files:
        file_issues = []
        
        # Read file
        try:
            with open(filepath, 'r') as f:
                content = f.read()
        except Exception as e:
            file_issues.append(f"Cannot read: {e}")
            issues.append((filepath.name, file_issues))
            continue
        
        # Parse YAML as text
        data = {}
        for line in content.split('\n'):
            if ':' in line and not line.strip().startswith('-'):
                key = line.split(':')[0].strip()
                value = line.split(':', 1)[1].strip()
                data[key] = value
        
        # Check based on file type
        if 'pasm2_' in filepath.name:
            # Check PASM2 instruction
            if 'layer1_csv' not in content:
                file_issues.append("Missing layer1_csv section")
            if 'mnemonic' not in content:
                file_issues.append("Missing mnemonic field")
            if 'encoding' not in content.lower():
                file_issues.append("Missing encoding field")
            
            # Verify mnemonic matches filename
            expected_mnemonic = filepath.stem.replace('pasm2_', '').upper()
            # Look for mnemonic in content
            for line in content.split('\n'):
                if 'mnemonic:' in line:
                    actual = line.split(':', 1)[1].strip()
                    if actual != expected_mnemonic:
                        file_issues.append(f"Mnemonic mismatch: {actual} != {expected_mnemonic}")
                    break
        
        elif 'spin2_' in filepath.name:
            # Check Spin2 element
            if 'name' not in data:
                file_issues.append("Missing 'name' field")
            if 'type' not in data:
                file_issues.append("Missing 'type' field")
            if 'source' not in data:
                file_issues.append("Missing 'source' field")
        
        elif 'hw_' in filepath.name:
            # Check hardware spec
            if 'name' not in data:
                file_issues.append("Missing 'name' field")
            if 'category' not in data:
                file_issues.append("Missing 'category' field")
            if 'description' not in data:
                file_issues.append("Missing 'description' field")
        
        elif 'arch_' in filepath.name:
            # Check architecture component
            if 'name' not in data:
                file_issues.append("Missing 'name' field")
            if 'category' not in data:
                file_issues.append("Missing 'category' field")
            if 'features' not in data:
                file_issues.append("Missing 'features' field")
        
        if file_issues:
            issues.append((filepath.name, file_issues))
        else:
            checks_passed += 1
            print(f"✅ {filepath.name}")
    
    # Summary
    print("-" * 60)
    print(f"\nQuality Check Results:")
    print(f"  Files checked: {len(sample_files)}")
    print(f"  Passed: {checks_passed}")
    print(f"  Issues found: {len(issues)}")
    
    if issues:
        print("\nIssues Detail:")
        for filename, file_issues in issues:
            print(f"\n  {filename}:")
            for issue in file_issues:
                print(f"    - {issue}")
    
    # Calculate quality score
    quality_score = (checks_passed / len(sample_files)) * 100
    print(f"\nQuality Score: {quality_score:.1f}%")
    
    if quality_score >= 95:
        print("✅ EXCELLENT - Quality check PASSED")
    elif quality_score >= 90:
        print("⚠️ GOOD - Minor issues found")
    else:
        print("❌ NEEDS ATTENTION - Significant issues found")

if __name__ == "__main__":
    quality_check()
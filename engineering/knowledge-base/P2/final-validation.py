#!/usr/bin/env python3
"""
Final validation of reorganized P2 knowledge base
"""

from pathlib import Path

def validate_knowledge_base():
    """Validate the complete knowledge base structure and content"""
    
    base_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2")
    
    print("=" * 60)
    print("P2 KNOWLEDGE BASE FINAL VALIDATION")
    print("=" * 60)
    
    # Check production structure
    checks = {
        "Production PASM2": base_dir / "production/instructions/pasm2",
        "Production Spin2 Methods": base_dir / "production/language/spin2/methods",
        "Production Spin2 Operators": base_dir / "production/language/spin2/operators",
        "Production Hardware": base_dir / "production/hardware",
        "Production Architecture": base_dir / "production/architecture",
        "Source PASM2": base_dir / "production/_sources/instructions/pasm2",
        "Source Spin2": base_dir / "production/_sources/language/spin2",
        "Source Hardware": base_dir / "production/_sources/hardware",
        "Source Architecture": base_dir / "production/_sources/architecture"
    }
    
    all_good = True
    file_counts = {}
    
    print("\n📁 Directory Structure:")
    for name, path in checks.items():
        if path.exists():
            count = len(list(path.glob("*.yaml")))
            file_counts[name] = count
            print(f"  ✅ {name:30} {count:4} files")
        else:
            print(f"  ❌ {name:30} MISSING")
            all_good = False
    
    # Verify counts
    print("\n📊 File Count Validation:")
    expected = {
        "Production PASM2": 357,
        "Production Spin2 Methods": 73,
        "Production Spin2 Operators": 46,
        "Production Hardware": 11,
        "Production Architecture": 8,
        "Source PASM2": 357
    }
    
    for name, expected_count in expected.items():
        if name in file_counts:
            actual = file_counts[name]
            if actual == expected_count:
                print(f"  ✅ {name}: {actual} (expected {expected_count})")
            else:
                print(f"  ⚠️  {name}: {actual} (expected {expected_count})")
                all_good = False
    
    # Check sample production files
    print("\n📄 Sample Production Files:")
    sample_files = [
        base_dir / "production/instructions/pasm2/add.yaml",
        base_dir / "production/instructions/pasm2/sub.yaml",
        base_dir / "production/language/spin2/methods/debug.yaml",
        base_dir / "production/hardware/p2_eval_board.yaml",
        base_dir / "production/architecture/cog.yaml"
    ]
    
    for file in sample_files:
        if file.exists():
            size = file.stat().st_size
            print(f"  ✅ {file.name:25} {size:6} bytes")
            
            # Check content structure
            with open(file, 'r') as f:
                content = f.read()
                if any(key in content for key in ['instruction:', 'method:', 'operator:', 'component:']):
                    pass  # Good
                else:
                    print(f"     ⚠️  Missing expected structure")
                    all_good = False
        else:
            print(f"  ❌ {file.name:25} MISSING")
            all_good = False
    
    # Check for unwanted files
    print("\n🚫 Checking for Removed Files:")
    bad_patterns = ['if_', 'c_and', 'nc_or', '_ret_', 'empty', 'clr']
    bad_files = []
    
    pasm2_dir = base_dir / "production/instructions/pasm2"
    if pasm2_dir.exists():
        for file in pasm2_dir.glob("*.yaml"):
            if any(pattern in file.stem for pattern in bad_patterns):
                bad_files.append(file.name)
    
    if bad_files:
        print(f"  ❌ Found {len(bad_files)} conditional/pseudo files that should be removed:")
        for bf in bad_files[:5]:
            print(f"     - {bf}")
    else:
        print("  ✅ No conditional/pseudo files found (correct)")
    
    # Check documentation
    print("\n📚 Documentation:")
    docs = [
        base_dir / "production/README.md",
        base_dir / "USAGE-GUIDE.md",
        base_dir / "manifest.yaml",
        base_dir / "timing-investigation-report.md"
    ]
    
    for doc in docs:
        if doc.exists():
            size = doc.stat().st_size
            print(f"  ✅ {doc.name:35} {size:6} bytes")
        else:
            print(f"  ⚠️  {doc.name:35} MISSING")
    
    # Final summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    total_production = sum([
        file_counts.get("Production PASM2", 0),
        file_counts.get("Production Spin2 Methods", 0),
        file_counts.get("Production Spin2 Operators", 0),
        file_counts.get("Production Hardware", 0),
        file_counts.get("Production Architecture", 0)
    ])
    
    total_source = sum([
        file_counts.get("Source PASM2", 0),
        file_counts.get("Source Spin2", 0),
        file_counts.get("Source Hardware", 0),
        file_counts.get("Source Architecture", 0)
    ])
    
    print(f"\n📈 Statistics:")
    print(f"  Total production files: {total_production}")
    print(f"  Total source files: {total_source}")
    print(f"  Total files: {total_production + total_source}")
    
    if all_good and not bad_files:
        print("\n✅ KNOWLEDGE BASE VALIDATION PASSED!")
        print("   Ready for production use")
    else:
        print("\n⚠️  VALIDATION FOUND ISSUES")
        print("   Please review warnings above")
    
    return all_good

if __name__ == "__main__":
    validate_knowledge_base()
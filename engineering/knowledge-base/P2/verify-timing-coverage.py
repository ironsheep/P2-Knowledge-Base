#!/usr/bin/env python3
"""
Verify timing data coverage in PASM2 instruction files
"""

from pathlib import Path

def verify_timing_coverage():
    """Check how many PASM2 files have timing data"""
    
    pasm2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    
    total_files = 0
    files_with_timing = 0
    files_without_timing = []
    timing_types = {}
    
    for yaml_file in pasm2_dir.glob("pasm2_*.yaml"):
        total_files += 1
        
        # Read file content
        with open(yaml_file, 'r') as f:
            content = f.read()
        
        # Check for layer2_datasheet section with timing
        if 'layer2_datasheet:' in content and 'timing:' in content:
            files_with_timing += 1
            
            # Extract timing type if present
            for line in content.split('\n'):
                if 'type:' in line and 'timing' in content[max(0, content.index(line)-200):content.index(line)]:
                    timing_type = line.split(':', 1)[1].strip()
                    timing_types[timing_type] = timing_types.get(timing_type, 0) + 1
                    break
        else:
            files_without_timing.append(yaml_file.stem.replace('pasm2_', '').upper())
    
    print(f"Timing Coverage Report:")
    print(f"=" * 60)
    print(f"Total PASM2 files: {total_files}")
    print(f"Files with timing data: {files_with_timing}")
    print(f"Files without timing data: {len(files_without_timing)}")
    print(f"Coverage: {(files_with_timing/total_files)*100:.1f}%")
    
    print(f"\nTiming Types Distribution:")
    for timing_type, count in sorted(timing_types.items()):
        print(f"  {timing_type}: {count}")
    
    if files_without_timing:
        print(f"\nInstructions without timing (first 20):")
        for inst in sorted(files_without_timing)[:20]:
            print(f"  - {inst}")
        
        if len(files_without_timing) > 20:
            print(f"  ... and {len(files_without_timing) - 20} more")
    
    # Sample check - look at a few files with timing to verify format
    print(f"\nSample files WITH timing:")
    sample_count = 0
    for yaml_file in pasm2_dir.glob("pasm2_*.yaml"):
        if sample_count >= 5:
            break
        with open(yaml_file, 'r') as f:
            content = f.read()
        if 'layer2_datasheet:' in content and 'timing:' in content:
            inst_name = yaml_file.stem.replace('pasm2_', '').upper()
            # Find the raw timing value
            for line in content.split('\n'):
                if 'raw:' in line and 'timing' in content[max(0, content.index(line)-100):content.index(line)]:
                    raw_value = line.split(':', 1)[1].strip()
                    print(f"  {inst_name}: {raw_value}")
                    sample_count += 1
                    break

if __name__ == "__main__":
    verify_timing_coverage()
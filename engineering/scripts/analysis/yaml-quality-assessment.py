#!/usr/bin/env python3
"""
Comprehensive YAML Quality Assessment Tool
Validates that instruction and directive YAMLs meet the highest quality standards.
"""

import yaml
from pathlib import Path
import re
from collections import defaultdict

# Paths
PASM2_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2")
DIRECTIVES_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2/assembly-directives")
MANUAL_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt")

print("="*60)
print("YAML QUALITY ASSESSMENT REPORT")
print("="*60)

# Define quality criteria
class QualityCriteria:
    """Define what makes a high-quality YAML."""
    
    # Required fields for instructions
    INSTRUCTION_REQUIRED = [
        'instruction',
        'syntax',
        'group',
        'description',
        'documentation_source'
    ]
    
    # Required fields for directives
    DIRECTIVE_REQUIRED = [
        'directive',
        'syntax',
        'description',
        'documentation_source'
    ]
    
    # Highly desirable fields
    HIGHLY_DESIRABLE = [
        'brief_description',
        'category',
        'parameters',
        'examples',
        'usage_notes',
        'encoding',
        'timing',
        'flags_affected',
        'related'
    ]
    
    # Quality thresholds
    MIN_DESCRIPTION_LENGTH = 100  # Characters
    MIN_BRIEF_DESC_LENGTH = 20
    MIN_PARAMETERS = 1  # At least one parameter documented
    MIN_EXAMPLES = 1    # At least one example
    
    @staticmethod
    def calculate_quality_score(data, is_directive=False):
        """Calculate a detailed quality score for a YAML."""
        score = 0
        max_score = 0
        issues = []
        strengths = []
        
        # Check required fields (40 points)
        required = QualityCriteria.DIRECTIVE_REQUIRED if is_directive else QualityCriteria.INSTRUCTION_REQUIRED
        for field in required:
            max_score += 8
            if field in data and data[field]:
                score += 8
                strengths.append(f"Has {field}")
            else:
                issues.append(f"Missing required field: {field}")
        
        # Check description quality (20 points)
        max_score += 20
        if 'description' in data:
            desc_len = len(data['description'] or '')
            if desc_len >= QualityCriteria.MIN_DESCRIPTION_LENGTH:
                score += 20
                strengths.append(f"Comprehensive description ({desc_len} chars)")
            elif desc_len > 50:
                score += 10
                issues.append(f"Description too short ({desc_len} chars, need {QualityCriteria.MIN_DESCRIPTION_LENGTH})")
            else:
                issues.append(f"Minimal description ({desc_len} chars)")
        
        # Check brief description (10 points)
        max_score += 10
        if 'brief_description' in data:
            brief_len = len(data['brief_description'] or '')
            if brief_len >= QualityCriteria.MIN_BRIEF_DESC_LENGTH:
                score += 10
                strengths.append("Has brief description")
            else:
                score += 5
                issues.append(f"Brief description too short ({brief_len} chars)")
        else:
            issues.append("Missing brief description")
        
        # Check parameters documentation (10 points)
        max_score += 10
        if 'parameters' in data and data['parameters']:
            param_count = len(data['parameters'])
            if param_count >= QualityCriteria.MIN_PARAMETERS:
                score += 10
                strengths.append(f"Parameters documented ({param_count})")
            else:
                score += 5
        else:
            issues.append("No parameters documented")
        
        # Check examples (10 points)
        max_score += 10
        if 'examples' in data and data['examples']:
            example_count = len(data['examples'])
            if example_count >= QualityCriteria.MIN_EXAMPLES:
                score += 10
                strengths.append(f"Has examples ({example_count})")
            else:
                score += 5
                issues.append(f"Only {example_count} example(s)")
        else:
            issues.append("No examples provided")
        
        # Check technical fields for instructions (10 points)
        if not is_directive:
            max_score += 10
            tech_score = 0
            if 'encoding' in data and data['encoding']:
                tech_score += 3
                strengths.append("Has encoding")
            else:
                issues.append("Missing encoding")
                
            if 'timing' in data and data['timing']:
                tech_score += 3
                strengths.append("Has timing")
            else:
                issues.append("Missing timing")
                
            if 'flags_affected' in data and data['flags_affected']:
                tech_score += 4
                strengths.append("Has flags documentation")
            else:
                issues.append("Missing flags documentation")
            
            score += tech_score
        
        return score, max_score, issues, strengths

def analyze_yaml_quality(yaml_path, is_directive=False):
    """Analyze a single YAML file for quality."""
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f) or {}
    
    score, max_score, issues, strengths = QualityCriteria.calculate_quality_score(data, is_directive)
    percentage = (score / max_score * 100) if max_score > 0 else 0
    
    # Categorize quality level
    if percentage >= 90:
        quality = "EXCELLENT"
    elif percentage >= 80:
        quality = "VERY GOOD"
    elif percentage >= 70:
        quality = "GOOD"
    elif percentage >= 60:
        quality = "ADEQUATE"
    elif percentage >= 50:
        quality = "NEEDS IMPROVEMENT"
    else:
        quality = "POOR"
    
    return {
        'name': yaml_path.stem,
        'score': score,
        'max_score': max_score,
        'percentage': percentage,
        'quality': quality,
        'issues': issues,
        'strengths': strengths,
        'has_manual_extraction': data.get('manual_extraction_date') == '2025-01-19'
    }

# Analyze all instructions
print("\n1. ANALYZING INSTRUCTIONS")
print("-"*40)

instruction_results = []
for yaml_file in sorted(PASM2_PATH.glob("*.yaml")):
    result = analyze_yaml_quality(yaml_file, is_directive=False)
    instruction_results.append(result)

# Sort by quality
instruction_results.sort(key=lambda x: x['percentage'], reverse=True)

# Show statistics
quality_dist = defaultdict(int)
for r in instruction_results:
    quality_dist[r['quality']] += 1

print(f"Total instructions analyzed: {len(instruction_results)}")
print("\nQuality Distribution:")
for quality in ["EXCELLENT", "VERY GOOD", "GOOD", "ADEQUATE", "NEEDS IMPROVEMENT", "POOR"]:
    count = quality_dist[quality]
    bar = "█" * (count // 5)
    print(f"  {quality:20} {count:3} {bar}")

# Show top 5 best
print("\nTop 5 Highest Quality Instructions:")
for i, result in enumerate(instruction_results[:5], 1):
    print(f"  {i}. {result['name'].upper():10} {result['percentage']:.1f}% - {result['quality']}")

# Show bottom 5 worst
print("\nBottom 5 Needing Most Work:")
for i, result in enumerate(instruction_results[-5:], 1):
    print(f"  {i}. {result['name'].upper():10} {result['percentage']:.1f}% - {result['quality']}")
    if result['issues'][:2]:
        for issue in result['issues'][:2]:
            print(f"     ⚠ {issue}")

# Analyze directives
print("\n2. ANALYZING DIRECTIVES")
print("-"*40)

directive_results = []
for yaml_file in sorted(DIRECTIVES_PATH.glob("*.yaml")):
    result = analyze_yaml_quality(yaml_file, is_directive=True)
    directive_results.append(result)

directive_results.sort(key=lambda x: x['percentage'], reverse=True)

print(f"Total directives analyzed: {len(directive_results)}")

# Show all directives with scores
print("\nDirective Quality Scores:")
for result in directive_results:
    status = "✅" if result['percentage'] >= 70 else "⚠️" if result['percentage'] >= 50 else "❌"
    print(f"  {status} {result['name'].upper():10} {result['percentage']:.1f}% - {result['quality']}")

# Check extraction coverage
print("\n3. MANUAL EXTRACTION COVERAGE")
print("-"*40)

extracted_instructions = sum(1 for r in instruction_results if r['has_manual_extraction'])
extracted_directives = sum(1 for r in directive_results if r['has_manual_extraction'])

print(f"Instructions with manual extraction: {extracted_instructions}/{len(instruction_results)} ({extracted_instructions/len(instruction_results)*100:.1f}%)")
print(f"Directives with manual extraction: {extracted_directives}/{len(directive_results)} ({extracted_directives/len(directive_results)*100:.1f}%)")

# Common issues analysis
print("\n4. MOST COMMON QUALITY ISSUES")
print("-"*40)

all_issues = defaultdict(int)
for result in instruction_results + directive_results:
    for issue in result['issues']:
        # Normalize issue types
        if 'Missing encoding' in issue:
            all_issues['Missing encoding'] += 1
        elif 'Missing timing' in issue:
            all_issues['Missing timing'] += 1
        elif 'Missing flags' in issue:
            all_issues['Missing flags documentation'] += 1
        elif 'No examples' in issue:
            all_issues['No examples provided'] += 1
        elif 'No parameters' in issue:
            all_issues['No parameters documented'] += 1
        elif 'Description too short' in issue:
            all_issues['Description too short'] += 1
        elif 'Missing brief' in issue:
            all_issues['Missing brief description'] += 1
        else:
            all_issues[issue] += 1

sorted_issues = sorted(all_issues.items(), key=lambda x: x[1], reverse=True)
for issue, count in sorted_issues[:10]:
    print(f"  • {issue}: {count} files")

# Validation against manual
print("\n5. MANUAL VALIDATION CHECK")
print("-"*40)

# Load manual to check for missing instructions
with open(MANUAL_PATH, 'r') as f:
    manual_text = f.read()

# Find instructions mentioned in manual
manual_instructions = set()
instruction_pattern = r'\b[A-Z][A-Z0-9]+\b'
for match in re.finditer(instruction_pattern, manual_text):
    word = match.group()
    # Filter to likely instructions (3-8 chars, common prefixes)
    if 3 <= len(word) <= 8 and any(word.startswith(p) for p in 
        ['ADD', 'SUB', 'MOV', 'JMP', 'CALL', 'TEST', 'CMP', 'AND', 'OR', 'XOR', 
         'RD', 'WR', 'GET', 'SET', 'POLL', 'WAIT', 'ALT', 'BIT', 'ROL', 'ROR']):
        manual_instructions.add(word)

# Check which manual instructions have YAMLs
yaml_instructions = {r['name'].upper() for r in instruction_results}
missing_from_yamls = manual_instructions - yaml_instructions

if missing_from_yamls:
    print(f"Instructions in manual but no YAML: {len(missing_from_yamls)}")
    for inst in sorted(list(missing_from_yamls)[:10]):
        print(f"  • {inst}")

# Overall quality assessment
print("\n6. OVERALL QUALITY ASSESSMENT")
print("-"*40)

avg_inst_score = sum(r['percentage'] for r in instruction_results) / len(instruction_results)
avg_dir_score = sum(r['percentage'] for r in directive_results) / len(directive_results) if directive_results else 0

print(f"Average instruction quality score: {avg_inst_score:.1f}%")
print(f"Average directive quality score: {avg_dir_score:.1f}%")
print(f"Overall knowledge base quality: {(avg_inst_score + avg_dir_score) / 2:.1f}%")

# Quality threshold analysis
high_quality = sum(1 for r in instruction_results if r['percentage'] >= 80)
adequate_quality = sum(1 for r in instruction_results if r['percentage'] >= 60)
needs_work = sum(1 for r in instruction_results if r['percentage'] < 60)

print(f"\nInstructions meeting quality thresholds:")
print(f"  High quality (80%+): {high_quality} ({high_quality/len(instruction_results)*100:.1f}%)")
print(f"  Adequate (60%+): {adequate_quality} ({adequate_quality/len(instruction_results)*100:.1f}%)")
print(f"  Needs work (<60%): {needs_work} ({needs_work/len(instruction_results)*100:.1f}%)")

# Recommendations
print("\n7. RECOMMENDATIONS FOR HIGHEST QUALITY")
print("-"*40)

if avg_inst_score < 90:
    print("To achieve highest quality (90%+ score), focus on:")
    
    top_improvements = sorted_issues[:5]
    for issue, count in top_improvements:
        if 'examples' in issue.lower():
            print(f"  1. Add code examples to {count} files - CRITICAL for AI code generation")
        elif 'encoding' in issue.lower():
            print(f"  2. Add encoding information to {count} instructions - needed for assembler")
        elif 'timing' in issue.lower():
            print(f"  3. Add timing information to {count} instructions - critical for optimization")
        elif 'flags' in issue.lower():
            print(f"  4. Document flag effects for {count} instructions - essential for correctness")
        elif 'parameters' in issue.lower():
            print(f"  5. Document parameters for {count} files - required for proper usage")

print("\nQuality validation complete!")
print("="*60)
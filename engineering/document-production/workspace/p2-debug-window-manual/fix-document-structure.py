#!/usr/bin/env python3
"""
Fix document structure for Debug Window Manual:
1. Separate "Next:" lines from chapter headings
2. Add Part divisions
3. Change chapters from # to ## for proper hierarchy with Parts
"""

import re
import sys

def fix_document_structure(content):
    """Fix the document structure issues."""
    
    # 1. Fix the concatenated chapter transitions
    # Pattern: *Next: Chapter X - Title*# Chapter X: Title
    content = re.sub(
        r'(\*Next: Chapter \d+ - [^*]+\*)(# Chapter \d+:)',
        r'\1\n\n\2',
        content
    )
    
    # 2. Insert Part headings before appropriate chapters
    # Based on TOC structure:
    # PART I: FOUNDATION (Chapters 1-3)
    content = content.replace(
        '# Chapter 1: Beyond Basic DEBUG - The Vision Gap',
        '# PART I: FOUNDATION\n\n## Chapter 1: Beyond Basic DEBUG - The Vision Gap'
    )
    
    # PART II: INTERACTIVE APPLICATIONS (Chapters 4-6)
    # First fix the line break if needed
    if '*Next: Chapter 4' in content:
        content = re.sub(
            r'(\*Next: Chapter 4[^*]+\*)\n\n(# Chapter 4:)',
            r'\1\n\n# PART II: INTERACTIVE APPLICATIONS\n\n\2',
            content
        )
    
    # PART III: DATA EFFICIENCY (Chapters 7-8)
    if '*Next: Chapter 7' in content:
        content = re.sub(
            r'(\*Next: Chapter 7[^*]+\*)\n\n(# Chapter 7:)',
            r'\1\n\n# PART III: DATA EFFICIENCY\n\n\2',
            content
        )
    
    # PART IV: ADVANCED ANALYSIS (Chapters 9-11)
    if '*Next: Chapter 9' in content:
        content = re.sub(
            r'(\*Next: Chapter 9[^*]+\*)\n\n(# Chapter 9:)',
            r'\1\n\n# PART IV: ADVANCED ANALYSIS\n\n\2',
            content
        )
    
    # PART V: INTEGRATION MASTERY (Chapters 12-14)
    if '*Next: Chapter 12' in content:
        content = re.sub(
            r'(\*Next: Chapter 12[^*]+\*)\n\n(# Chapter 12:)',
            r'\1\n\n# PART V: INTEGRATION MASTERY\n\n\2',
            content
        )
    
    # 3. Change all "# Chapter X:" to "## Chapter X:" for proper hierarchy
    # This makes chapters level 2 (under Parts which are level 1)
    content = re.sub(
        r'^# Chapter (\d+:)',
        r'## Chapter \1',
        content,
        flags=re.MULTILINE
    )
    
    # 4. Find and add APPENDICES part if there are appendices
    # Look for Appendix A
    if 'Appendix A:' in content:
        # Find the first appendix and add Part heading before it
        content = re.sub(
            r'(.*\n)(#+\s*Appendix A:)',
            r'\1\n# APPENDICES\n\n\2',
            content,
            count=1
        )
    
    # 5. Make sure ## level headings within chapters become ### (sections)
    # This is trickier - we need to identify what's a chapter-level section vs a chapter heading
    
    # First, let's fix the known problematic sections in Chapter 1
    # "The Debug Iceberg Effect" and "The Capability Discovery Journey" should be ### not ##
    lines = content.split('\n')
    in_chapter = False
    result = []
    
    for i, line in enumerate(lines):
        # Track when we're in a chapter
        if line.startswith('## Chapter '):
            in_chapter = True
            result.append(line)
        elif line.startswith('# PART ') or line.startswith('# APPENDICES'):
            in_chapter = False
            result.append(line)
        elif in_chapter and line.startswith('## ') and not line.startswith('## Chapter'):
            # This is a section within a chapter, should be ###
            result.append('##' + line)  # Add one more # to make it ###
        else:
            result.append(line)
    
    return '\n'.join(result)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 fix-document-structure.py input.md output.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Read input
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix structure
    fixed_content = fix_document_structure(content)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Document structure fixed and saved to {output_file}")
    print("\nChanges made:")
    print("1. Separated 'Next:' lines from chapter headings")
    print("2. Added PART divisions (I-V + APPENDICES)")
    print("3. Changed chapters from # to ## for proper hierarchy")
    print("4. Changed sections within chapters from ## to ###")
    print("\nWith --top-level-division=part:")
    print("  # PART → \\part{}")
    print("  ## Chapter → \\chapter{}")
    print("  ### Section → \\section{}")

if __name__ == "__main__":
    main()
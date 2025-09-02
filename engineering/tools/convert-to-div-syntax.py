#!/usr/bin/env python3
"""
Convert language-tagged code blocks to div-wrapped syntax for Smart Pins documentation.
Handles both grounded (at left edge) and inline (preceded by text) code blocks.

Usage: python3 convert-to-div-syntax.py input.md output.md
"""

import re
import sys
from pathlib import Path

class CodeBlockConverter:
    def __init__(self, use_three_colons=True):
        """
        Initialize converter.
        Args:
            use_three_colons: If True, use ::: (Pandoc standard). If False, use ::::
        """
        self.colon_count = ":::" if use_three_colons else "::::"
        self.stats = {
            'spin2_converted': 0,
            'pasm2_converted': 0,
            'antipattern_found': 0,
            'blank_lines_added': 0,
            'total_blocks': 0
        }
        
    def needs_blank_line(self, lines, block_start_idx):
        """
        Check if we need to insert a blank line before the div opener.
        Returns True if the line before the code block is not empty.
        """
        if block_start_idx == 0:
            return False
        
        prev_line = lines[block_start_idx - 1]
        return prev_line.strip() != ''
    
    def find_code_block_end(self, lines, start_idx):
        """
        Find the end of a code block starting at start_idx.
        Returns the index of the closing ``` line.
        """
        for i in range(start_idx + 1, len(lines)):
            if lines[i].strip() == '```':
                return i
        return -1
    
    def detect_antipattern(self, lines, start_idx, end_idx):
        """
        Check if this code block contains both WRONG and RIGHT patterns.
        Returns True if this should be split into antipattern blocks.
        """
        block_content = '\n'.join(lines[start_idx+1:end_idx])
        has_wrong = "' WRONG" in block_content or "' This won't work" in block_content
        has_right = "' RIGHT" in block_content or "' This works" in block_content
        return has_wrong and has_right
    
    def split_antipattern_block(self, lines, start_idx, end_idx, language):
        """
        Split a mixed antipattern block into separate WRONG and RIGHT blocks.
        Returns the new lines to replace the original block.
        """
        result = []
        wrong_lines = []
        right_lines = []
        
        in_wrong = False
        in_right = False
        
        for i in range(start_idx + 1, end_idx):
            line = lines[i]
            if "' WRONG" in line or "' This won't work" in line:
                in_wrong = True
                in_right = False
                wrong_lines.append(line)
            elif "' RIGHT" in line or "' This works" in line:
                in_right = True
                in_wrong = False
                right_lines.append(line)
            elif in_wrong:
                wrong_lines.append(line)
            elif in_right:
                right_lines.append(line)
        
        # Build the antipattern block (red)
        if wrong_lines:
            result.append(f"{self.colon_count} antipattern")
            result.append("```")
            result.extend(wrong_lines)
            result.append("```")
            result.append(self.colon_count)
            result.append("")  # Blank line between blocks
            self.stats['antipattern_found'] += 1
        
        # Build the correct pattern block (green for spin2)
        if right_lines:
            result.append(f"{self.colon_count} {language}")
            result.append("```")
            result.extend(right_lines)
            result.append("```")
            result.append(self.colon_count)
        
        return result
    
    def convert_code_block(self, lines, start_idx):
        """
        Convert a single code block to div syntax.
        Returns (new_lines, lines_to_skip).
        """
        # Extract language from the opening ```
        opening_line = lines[start_idx]
        match = re.match(r'^```(\w+)$', opening_line.strip())
        
        if not match:
            return None, 0
        
        language = match.group(1)
        
        # Only process spin2 and pasm2
        if language not in ['spin2', 'pasm2']:
            return None, 0
        
        # Find the end of this code block
        end_idx = self.find_code_block_end(lines, start_idx)
        if end_idx == -1:
            print(f"WARNING: Unclosed code block at line {start_idx + 1}")
            return None, 0
        
        self.stats['total_blocks'] += 1
        
        # Check if this is an antipattern block that needs splitting
        if language == 'spin2' and self.detect_antipattern(lines, start_idx, end_idx):
            new_lines = self.split_antipattern_block(lines, start_idx, end_idx, language)
            return new_lines, end_idx - start_idx + 1
        
        # Build the converted block
        result = []
        
        # Check if we need a blank line before the div
        if self.needs_blank_line(lines, start_idx):
            result.append("")
            self.stats['blank_lines_added'] += 1
        
        # Add div opener
        result.append(f"{self.colon_count} {language}")
        
        # Add the code block without language tag
        result.append("```")
        
        # Add the code content
        for i in range(start_idx + 1, end_idx):
            result.append(lines[i])
        
        # Add code block closer
        result.append("```")
        
        # Add div closer
        result.append(self.colon_count)
        
        # Update stats
        if language == 'spin2':
            self.stats['spin2_converted'] += 1
        elif language == 'pasm2':
            self.stats['pasm2_converted'] += 1
        
        return result, end_idx - start_idx + 1
    
    def convert_file(self, input_path, output_path):
        """
        Convert all code blocks in a file.
        """
        print(f"Converting {input_path} -> {output_path}")
        print(f"Using {len(self.colon_count)} colons for div syntax")
        print("-" * 50)
        
        # Read the input file
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Strip newlines but preserve them for output
        lines = [line.rstrip('\n') for line in lines]
        
        # Process the file
        output_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Check if this is a code block with language tag
            if re.match(r'^```(spin2|pasm2)$', line.strip()):
                new_lines, skip = self.convert_code_block(lines, i)
                
                if new_lines:
                    output_lines.extend(new_lines)
                    i += skip
                else:
                    output_lines.append(line)
                    i += 1
            else:
                output_lines.append(line)
                i += 1
        
        # Write the output file
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in output_lines:
                f.write(line + '\n')
        
        # Print statistics
        print("\nConversion Statistics:")
        print(f"  Total code blocks found: {self.stats['total_blocks']}")
        print(f"  Spin2 blocks converted: {self.stats['spin2_converted']}")
        print(f"  PASM2 blocks converted: {self.stats['pasm2_converted']}")
        print(f"  Antipattern blocks split: {self.stats['antipattern_found']}")
        print(f"  Blank lines added: {self.stats['blank_lines_added']}")
        print("\nConversion complete!")
        
        # Verification
        remaining = self.verify_conversion(output_path)
        if remaining == 0:
            print("✅ SUCCESS: No language-tagged blocks remain!")
        else:
            print(f"⚠️  WARNING: {remaining} language-tagged blocks still found")
    
    def verify_conversion(self, file_path):
        """
        Verify that no language-tagged blocks remain.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        spin2_count = len(re.findall(r'^```spin2', content, re.MULTILINE))
        pasm2_count = len(re.findall(r'^```pasm2', content, re.MULTILINE))
        
        return spin2_count + pasm2_count

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 convert-to-div-syntax.py input.md output.md")
        print("Optional: Add '3' or '4' as third argument for colon count (default: 3)")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    
    # Check if input file exists
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    # Determine colon count
    use_three = True
    if len(sys.argv) > 3:
        if sys.argv[3] == '4':
            use_three = False
    
    # Create converter and process file
    converter = CodeBlockConverter(use_three_colons=use_three)
    converter.convert_file(input_file, output_file)

if __name__ == "__main__":
    main()
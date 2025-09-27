#!/usr/bin/env python3
"""
YAML Syntax Validation Tool for P2 Knowledge Base

Checks all YAML files in the knowledge base for syntax errors.
Run this before generating the master JSON to catch issues early.

Version: 1.0.0
Created: 2025-09-26
"""

import os
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Tuple

class Colors:
    """Terminal color codes for output formatting."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class YAMLValidator:
    """Validates YAML syntax across the knowledge base."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.errors = []
        self.warnings = []
        self.files_checked = 0
        self.files_with_errors = 0
        
    def validate_directory(self, directory: Path) -> List[Tuple[Path, str]]:
        """Validate all YAML files in a directory recursively."""
        errors = []
        
        for yaml_file in sorted(directory.glob('**/*.yaml')):
            self.files_checked += 1
            error = self.validate_file(yaml_file)
            if error:
                errors.append((yaml_file, error))
                self.files_with_errors += 1
                
        return errors
    
    def validate_file(self, file_path: Path) -> str:
        """Validate a single YAML file. Returns error message or empty string."""
        try:
            with open(file_path, 'r') as f:
                content = yaml.safe_load(f)
                
            # Check for empty files
            if content is None:
                return "Empty YAML file (no content)"
                
            # Check for common issues
            if isinstance(content, str):
                return "File contains only a string, not a structured YAML document"
                
            return ""  # No error
            
        except yaml.YAMLError as e:
            # Extract the most relevant part of the error
            error_str = str(e)
            lines = error_str.split('\n')
            if len(lines) > 0:
                # Return first two lines for context
                return ' | '.join(lines[:2])
            return error_str
            
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def check_common_patterns(self, file_path: Path) -> List[str]:
        """Check for common YAML issues that might not be syntax errors."""
        warnings = []
        
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                # Check for tabs (YAML prefers spaces)
                if '\t' in line:
                    warnings.append(f"Line {i}: Contains tabs (use spaces instead)")
                
                # Check for improper indentation in code blocks
                if i > 1 and 'if_' in line and line[0] not in ' -':
                    # Might be an unindented conditional instruction
                    prev_line = lines[i-2] if i > 1 else ""
                    if not line.startswith(' '):
                        warnings.append(f"Line {i}: Possible unindented conditional instruction")
                        
        except Exception:
            pass  # Ignore errors in pattern checking
            
        return warnings
    
    def run_validation(self):
        """Run validation on all knowledge base directories."""
        print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}P2 KNOWLEDGE BASE - YAML SYNTAX VALIDATOR{Colors.RESET}")
        print(f"{'=' * 70}\n")
        
        # Directories to check
        directories = [
            self.base_path / "manifests",
            self.base_path / "engineering/knowledge-base/P2"
        ]
        
        all_errors = []
        
        for directory in directories:
            if not directory.exists():
                print(f"{Colors.YELLOW}⚠ Directory not found: {directory}{Colors.RESET}")
                continue
                
            print(f"{Colors.CYAN}Checking: {directory.relative_to(self.base_path)}{Colors.RESET}")
            errors = self.validate_directory(directory)
            
            if errors:
                all_errors.extend(errors)
                print(f"{Colors.RED}  ✗ Found {len(errors)} files with errors{Colors.RESET}")
                for file_path, error in errors[:5]:  # Show first 5 errors
                    rel_path = file_path.relative_to(self.base_path)
                    print(f"    {Colors.RED}• {rel_path}:{Colors.RESET}")
                    print(f"      {error[:100]}...")  # Truncate long errors
                if len(errors) > 5:
                    print(f"    ... and {len(errors) - 5} more")
            else:
                print(f"{Colors.GREEN}  ✓ All files valid{Colors.RESET}")
        
        # Summary
        print(f"\n{'=' * 70}")
        print(f"{Colors.BOLD}VALIDATION SUMMARY{Colors.RESET}")
        print(f"{'=' * 70}")
        print(f"Files checked: {self.files_checked}")
        print(f"Files with errors: {self.files_with_errors}")
        
        if self.files_with_errors == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ ALL YAML FILES ARE VALID!{Colors.RESET}")
            return True
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ YAML VALIDATION FAILED{Colors.RESET}")
            print(f"{Colors.RED}Fix the errors above before generating JSON.{Colors.RESET}")
            
            # Show all errors in detail
            print(f"\n{Colors.BOLD}DETAILED ERROR REPORT:{Colors.RESET}")
            for i, (file_path, error) in enumerate(all_errors, 1):
                rel_path = file_path.relative_to(self.base_path)
                print(f"\n{i}. {Colors.YELLOW}{rel_path}{Colors.RESET}")
                print(f"   {error}")
            
            return False

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate YAML syntax in P2 Knowledge Base')
    parser.add_argument('--path', default='.', help='Base path of the knowledge base')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    
    args = parser.parse_args()
    
    validator = YAMLValidator(args.path)
    success = validator.run_validation()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
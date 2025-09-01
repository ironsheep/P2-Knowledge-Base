#!/usr/bin/env python3
"""
LaTeX Escaping Processor for P2 Assembly Manual
Handles proper escaping of LaTeX special characters while preserving code blocks,
LaTeX environments, and markdown headers.
"""
import sys
import re


def process_latex_escaping(input_file, output_file):
    """Process file and escape LaTeX special characters with proper state tracking."""
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    output_lines = []
    in_code_block = False
    in_latex_env = False
    
    for line in lines:
        original_line = line
        line = line.rstrip('\n')
        
        # Track code blocks (```pasm2, ```markdown, etc.)
        # Check the stripped line to handle indented code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            output_lines.append(original_line)
            continue
            
        # Track ONLY standard LaTeX environments (preserve completely)
        # Template environments like sidetrack need content processed
        standard_latex_envs = ['equation', 'align', 'array', 'matrix', 'tabular', 'figure', 'table']
        
        if line.startswith('\\begin{'):
            # Extract environment name
            env_match = re.search(r'\\begin\{(\w+)\}', line)
            if env_match:
                env_name = env_match.group(1)
                if env_name in standard_latex_envs:
                    # Standard LaTeX environment - preserve completely
                    in_latex_env = True
            # Always output the \begin{} line itself
            output_lines.append(original_line)
            continue
        elif line.startswith('\\end{'):
            # Extract environment name
            env_match = re.search(r'\\end\{(\w+)\}', line)
            if env_match:
                env_name = env_match.group(1)
                if env_name in standard_latex_envs and in_latex_env:
                    # End of standard LaTeX environment
                    in_latex_env = False
            # Always output the \end{} line itself (for both standard and template)
            output_lines.append(original_line)
            continue
            
        # Skip processing if in protected blocks
        if in_code_block or in_latex_env:
            output_lines.append(original_line)
            continue
            
        # Handle markdown headers - keep structure but escape content
        header_match = re.match(r'^(#+\s+)(.*)', line)
        if header_match:
            header_prefix = header_match.group(1)  # "### " 
            header_content = header_match.group(2) # "Immediate Values (# characters)"
            
            # Escape the content part but keep header structure
            escaped_content = header_content
            escaped_content = escaped_content.replace('\\', '\\textbackslash{}')
            escaped_content = escaped_content.replace('^', '\\^{}')
            escaped_content = escaped_content.replace('\\^{}', 'XPROTECT_CARET_X')
            escaped_content = escaped_content.replace('{', '\\{')
            escaped_content = escaped_content.replace('}', '\\}')
            escaped_content = escaped_content.replace('XPROTECT_CARET_X', '\\^{}')
            escaped_content = escaped_content.replace('#', '\\#')
            escaped_content = escaped_content.replace('$', '\\$')
            escaped_content = escaped_content.replace('%', '\\%')
            escaped_content = escaped_content.replace('&', '\\&')
            escaped_content = escaped_content.replace('_', '\\_')
            # Don't escape tildes - Pandoc handles them fine in markdown
            # escaped_content = escaped_content.replace('~', '\\textasciitilde{}')
            
            output_lines.append(header_prefix + escaped_content + '\n')
            continue
            
        # Process normal text lines - escape LaTeX special characters
        # BUT preserve valid LaTeX commands like \textbf{}, \textit{}, etc.
        
        # PROTECT INLINE CODE FIRST (backticks)
        # Find and protect inline code `like this`
        protected_inline_code = []
        # Use negative lookbehind to avoid matching ``` code blocks
        inline_code_pattern = r'(?<!`)(`[^`\n]+`)'  # Match `text` but not ```
        for match in re.finditer(inline_code_pattern, line):
            placeholder = f'XPROTECTINLINECODE{len(protected_inline_code)}X'
            protected_inline_code.append(match.group(1))
            line = line.replace(match.group(1), placeholder, 1)
        
        # First, protect valid LaTeX commands by replacing them with placeholders
        protected_commands = []
        
        # Find and protect \textbf{...} commands
        while True:
            match = re.search(r'\\textbf\{([^}]*)\}', line)
            if not match:
                break
            placeholder = f'XPROTECTLATEXCMD{len(protected_commands)}X'
            protected_commands.append(match.group(0))
            line = line.replace(match.group(0), placeholder, 1)
        
        # Find and protect other LaTeX commands
        for pattern in [r'\\textit\{([^}]*)\}', r'\\texttt\{([^}]*)\}', r'\\emph\{([^}]*)\}', r'\\underline\{([^}]*)\}']:
            while True:
                match = re.search(pattern, line)
                if not match:
                    break
                placeholder = f'XPROTECTLATEXCMD{len(protected_commands)}X'
                protected_commands.append(match.group(0))
                line = line.replace(match.group(0), placeholder, 1)
        
        # Find and protect LaTeX list commands
        for pattern in [r'\\item\b', r'\\begin\{itemize\}', r'\\end\{itemize\}', 
                       r'\\begin\{enumerate\}', r'\\end\{enumerate\}',
                       r'\\begin\{description\}', r'\\end\{description\}']:
            while True:
                match = re.search(pattern, line)
                if not match:
                    break
                placeholder = f'XPROTECTLATEXCMD{len(protected_commands)}X'
                protected_commands.append(match.group(0))
                line = line.replace(match.group(0), placeholder, 1)
        
        # Find and protect LaTeX sectioning commands (but escape their content)
        for cmd in ['section', 'subsection', 'subsubsection', 'paragraph', 'chapter', 'part']:
            pattern = rf'\\{cmd}\{{([^}}]*)\}}'
            while True:
                match = re.search(pattern, line)
                if not match:
                    break
                # Escape the content inside the braces
                content = match.group(1)
                escaped_content = content
                escaped_content = escaped_content.replace('#', '\\#')
                escaped_content = escaped_content.replace('$', '\\$')
                escaped_content = escaped_content.replace('%', '\\%')
                escaped_content = escaped_content.replace('&', '\\&')
                escaped_content = escaped_content.replace('_', '\\_')
                escaped_content = escaped_content.replace('^', '\\^{}')
                # Don't escape tildes - Pandoc handles them fine
                # escaped_content = escaped_content.replace('~', '\\textasciitilde{}')
                
                # Reconstruct the command with escaped content
                escaped_cmd = f'\\{cmd}{{{escaped_content}}}'
                placeholder = f'XPROTECTLATEXCMD{len(protected_commands)}X'
                protected_commands.append(escaped_cmd)
                line = line.replace(match.group(0), placeholder, 1)
        
        # Find and protect LaTeX formatting commands (no arguments)
        for pattern in [r'\\par\b', r'\\newline\b', r'\\\\', r'\\noindent\b',
                       r'\\centering\b', r'\\raggedright\b', r'\\raggedleft\b',
                       r'\\small\b', r'\\large\b', r'\\Large\b', r'\\huge\b', r'\\Huge\b',
                       r'\\normalsize\b', r'\\footnotesize\b', r'\\scriptsize\b', r'\\tiny\b',
                       r'\\chapterseparator\b']:  # Custom command for chapter endings
            while True:
                match = re.search(pattern, line)
                if not match:
                    break
                placeholder = f'XPROTECTLATEXCMD{len(protected_commands)}X'
                protected_commands.append(match.group(0))
                line = line.replace(match.group(0), placeholder, 1)
        
        # Find and protect LaTeX spacing commands
        for pattern in [r'\\vspace\{([^}]*)\}', r'\\hspace\{([^}]*)\}',
                       r'\\quad\b', r'\\qquad\b', r'\\,', r'\\:', r'\\;', r'\\!',
                       r'\\bigskip\b', r'\\medskip\b', r'\\smallskip\b']:
            while True:
                match = re.search(pattern, line)
                if not match:
                    break
                placeholder = f'XPROTECTLATEXCMD{len(protected_commands)}X'
                protected_commands.append(match.group(0))
                line = line.replace(match.group(0), placeholder, 1)
        
        # Find and protect LaTeX reference commands
        for pattern in [r'\\ref\{([^}]*)\}', r'\\label\{([^}]*)\}', r'\\cite\{([^}]*)\}',
                       r'\\pageref\{([^}]*)\}', r'\\eqref\{([^}]*)\}']:
            while True:
                match = re.search(pattern, line)
                if not match:
                    break
                placeholder = f'XPROTECTLATEXCMD{len(protected_commands)}X'
                protected_commands.append(match.group(0))
                line = line.replace(match.group(0), placeholder, 1)
        
        # Find and protect LaTeX special characters and math delimiters
        for pattern in [r'\\ldots\b', r'\\dots\b', r'\\dag\b', r'\\ddag\b',
                       r'\\copyright\b', r'\\trademark\b',
                       r'\\\(', r'\\\)', r'\\\[', r'\\\]']:
            while True:
                match = re.search(pattern, line)
                if not match:
                    break
                placeholder = f'XPROTECTLATEXCMD{len(protected_commands)}X'
                protected_commands.append(match.group(0))
                line = line.replace(match.group(0), placeholder, 1)
        
        # Now escape special characters in the remaining text
        # 1. Escape backslashes (but not in protected commands)
        line = line.replace('\\', '\\textbackslash{}')
        
        # 2. Escape ^ before { } to create \^{} correctly
        line = line.replace('^', '\\^{}')
        
        # 3. Now protect our \^{} patterns and escape remaining { }
        line = line.replace('\\^{}', 'XPROTECT_CARET_X')
        line = line.replace('{', '\\{')
        line = line.replace('}', '\\}')
        line = line.replace('XPROTECT_CARET_X', '\\^{}')
        
        # 4. Escape other special characters
        line = line.replace('#', '\\#')
        line = line.replace('$', '\\$') 
        line = line.replace('%', '\\%')
        line = line.replace('&', '\\&')
        line = line.replace('_', '\\_')
        # Don't escape tildes - Pandoc handles them fine in markdown
        # line = line.replace('~', '\\textasciitilde{}')
        
        # 5. Restore protected LaTeX commands
        for i, cmd in enumerate(protected_commands):
            placeholder = f'XPROTECTLATEXCMD{i}X'
            line = line.replace(placeholder, cmd)
        
        # 6. Restore protected inline code (UNCHANGED - no escaping)
        for i, code in enumerate(protected_inline_code):
            placeholder = f'XPROTECTINLINECODE{i}X'
            line = line.replace(placeholder, code)
        
        output_lines.append(line + '\n')
    
    with open(output_file, 'w') as f:
        f.writelines(output_lines)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 latex_escape_processor.py input.md output.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_latex_escaping(input_file, output_file)
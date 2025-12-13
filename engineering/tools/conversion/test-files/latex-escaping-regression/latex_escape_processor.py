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
    in_raw_latex_block = False  # Track ```{=latex} blocks (need partial escaping)
    in_fenced_div = False  # Track ::: type fenced divs
    in_latex_env = False
    in_grid_table = False  # Track grid tables (NO escaping - breaks column alignment)

    # Code types that should be protected in fenced divs (no escaping inside)
    code_div_types = ['pasm2', 'spin2', 'cordic', 'multicog', 'antipattern', 'pasm', 'spin']

    for line in lines:
        original_line = line
        line = line.rstrip('\n')

        # Track code blocks (```pasm2, ```markdown, etc.) and raw LaTeX blocks
        # Check the stripped line to handle indented code blocks
        stripped = line.strip()
        if stripped.startswith('```'):
            # Check if this is a raw LaTeX block opening/closing
            if stripped == '```{=latex}' or stripped.startswith('```{=latex}'):
                in_raw_latex_block = not in_raw_latex_block
                output_lines.append(original_line)
                continue
            elif stripped == '```' and in_raw_latex_block:
                # Closing a raw LaTeX block
                in_raw_latex_block = False
                output_lines.append(original_line)
                continue
            else:
                # Regular code block
                in_code_block = not in_code_block
                output_lines.append(original_line)
                continue

        # Track grid tables (lines starting with + followed by - or =)
        # Grid tables MUST NOT be escaped because adding chars breaks column alignment
        # which causes Pandoc to misparse the table structure entirely
        if stripped.startswith('+') and (re.match(r'^\+[-=+]+\+$', stripped) or re.match(r'^\+[-=+]+$', stripped)):
            # This is a grid table border row (e.g., +------+------+ or +======+======+)
            in_grid_table = True
            output_lines.append(original_line)
            continue
        elif in_grid_table:
            # Check if we're still in the grid table
            # Grid table rows start with | (data row) or + (border row)
            if stripped.startswith('|') or (stripped.startswith('+') and '-' in stripped):
                # Still in grid table - output unchanged
                output_lines.append(original_line)
                continue
            else:
                # No longer in grid table
                in_grid_table = False
                # Fall through to process this line normally

        # Track fenced divs (::: pasm2, ::: spin2, etc.)
        # These are Pandoc fenced div syntax for code blocks
        stripped = line.strip()
        if stripped.startswith(':::'):
            # Check if this is a code-type div opening (e.g., "::: pasm2")
            div_match = re.match(r'^:::\s*(\w+)', stripped)
            if div_match:
                div_type = div_match.group(1).lower()
                if div_type in code_div_types:
                    in_fenced_div = True
            # Check if this is a closing ::: (just ":::" with optional whitespace)
            elif stripped == ':::' or re.match(r'^:::\s*$', stripped):
                in_fenced_div = False
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
        if in_code_block or in_latex_env or in_fenced_div:
            output_lines.append(original_line)
            continue

        # Special handling for raw LaTeX blocks (```{=latex})
        # Only escape underscores - other chars are valid LaTeX
        if in_raw_latex_block:
            # Escape underscores that are NOT already escaped
            # Use negative lookbehind to avoid double-escaping
            line = re.sub(r'(?<!\\)_', r'\\_', line)
            output_lines.append(line + '\n')
            continue
            
        # Handle markdown headers - keep structure but escape content
        # IMPORTANT: Preserve Pandoc anchor syntax {#anchor-id} at end of headers
        header_match = re.match(r'^(#+\s+)(.*)', line)
        if header_match:
            header_prefix = header_match.group(1)  # "### "
            header_content = header_match.group(2) # "INSTR {#instr}" or "Immediate Values (# characters)"

            # Check for Pandoc anchor at end: {#some-anchor-id}
            anchor_match = re.search(r'\s*(\{#[a-zA-Z0-9_-]+\})\s*$', header_content)
            anchor_suffix = ''
            if anchor_match:
                anchor_suffix = anchor_match.group(1)  # Preserve the anchor exactly
                header_content = header_content[:anchor_match.start()]  # Content before anchor

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

            # Reassemble: header prefix + escaped content + unescaped anchor
            if anchor_suffix:
                output_lines.append(header_prefix + escaped_content + ' ' + anchor_suffix + '\n')
            else:
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
        for pattern in [r'\\textit\{([^}]*)\}', r'\\texttt\{([^}]*)\}', r'\\emph\{([^}]*)\}', r'\\underline\{([^}]*)\}',
                        r'\\textsuperscript\{([^}]*)\}', r'\\textsubscript\{([^}]*)\}']:
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
        
        # Protect trailing backslash (Pandoc hard line break) BEFORE escaping
        # A single backslash at end of line is Pandoc's hard line break syntax
        trailing_backslash = False
        if line.rstrip().endswith('\\') and not line.rstrip().endswith('\\\\'):
            trailing_backslash = True
            line = line.rstrip()[:-1]  # Remove trailing backslash temporarily

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
                       r'\\pageref\{([^}]*)\}', r'\\eqref\{([^}]*)\}',
                       r'\\hypertarget\{([^}]*)\}\{([^}]*)\}']:  # Pandoc anchor targets
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
        
        # Protect PASM2 operand syntax {#} meaning "optional immediate"
        # This appears in instruction syntax like: ADD Dest, {#}Src
        # Must be protected BEFORE escaping { } and #
        line = line.replace('{#}', 'XPROTECT_OPTIONAL_IMM_X')

        # Protect PASM2 absolute address syntax #\Label and \Label
        # In PASM2, backslash prefix means absolute address (vs relative)
        # Pattern: #\ followed by identifier OR just \ followed by identifier at word boundary
        # Examples: #\Addr, #\DebugStatus, \helper
        # Store protected patterns to restore later
        # NOTE: Placeholder uses no underscores to avoid underscore escaping issues
        protected_pasm2_addr = []
        # Match #\identifier patterns (absolute immediate address)
        for match in re.finditer(r'#\\([A-Za-z_][A-Za-z0-9_]*)', line):
            placeholder = f'XPROTECTPASMABSADDR{len(protected_pasm2_addr)}X'
            protected_pasm2_addr.append(('\\#\\\\' + match.group(1), match.group(0)))
            line = line.replace(match.group(0), placeholder, 1)
        # Match standalone \identifier patterns (absolute address in jumps)
        for match in re.finditer(r'(?<![#A-Za-z0-9_])\\([A-Za-z_][A-Za-z0-9_]*)', line):
            placeholder = f'XPROTECTPASMABSADDR{len(protected_pasm2_addr)}X'
            protected_pasm2_addr.append(('\\\\' + match.group(1), match.group(0)))
            line = line.replace(match.group(0), placeholder, 1)

        # Now escape special characters in the remaining text
        # 1. Escape backslashes (but not in protected commands)
        # Use a placeholder that won't have its braces escaped
        line = line.replace('\\', 'XTEXTBACKSLASHX')

        # 2. Escape ^ before { } to create \^{} correctly
        line = line.replace('^', 'XCARETX')

        # 3. Escape braces
        line = line.replace('{', '\\{')
        line = line.replace('}', '\\}')

        # 4. Restore backslash and caret with proper LaTeX escapes
        # \textbackslash{} needs {} for proper spacing in LaTeX
        line = line.replace('XTEXTBACKSLASHX', '\\textbackslash{}')
        line = line.replace('XCARETX', '\\^{}')

        # 4. Escape other special characters
        line = line.replace('#', '\\#')

        # 5. Restore {#} optional immediate syntax
        line = line.replace('XPROTECT_OPTIONAL_IMM_X', '{\\#}')
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

        # 7. Restore protected PASM2 absolute address syntax
        # These use double backslash in output for LaTeX to render single backslash
        for i, (replacement, original) in enumerate(protected_pasm2_addr):
            placeholder = f'XPROTECTPASMABSADDR{i}X'
            line = line.replace(placeholder, replacement)

        # 8. Restore trailing backslash for Pandoc hard line breaks
        if trailing_backslash:
            output_lines.append(line + '\\\n')
        else:
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
#!/bin/bash
# Add the missing \tightlist definition to the template

echo "Adding \\tightlist fix to template..."

# Add this right after the \usepackage commands in your template
cat >> templates/p2kb-pasm-desilva-enhanced.latex << 'EOF'

% Fix for Pandoc's \tightlist command
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}

EOF

echo "✅ Added \\tightlist fix"
echo ""
echo "The template should now work! Try running the process again."
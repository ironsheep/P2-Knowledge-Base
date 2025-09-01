# Doc-Forge Integration Guide

**For repositories that generate documents for PDF processing**

This guide explains how to create content and templates that are compatible with the doc-forge PDF generation system.

---

## 🎯 Overview

Doc-forge uses **pandoc + LaTeX** to generate professional PDFs. If your repository generates documents or templates for PDF processing, follow these guidelines to ensure compatibility.

## 📋 Request Format

### request.json Structure
```json
{
  "documents": [
    {
      "input": "your-document.md",
      "output": "Professional_Document_v1.0.pdf", 
      "template": "admin-manual",
      "variables": {
        "title": "Your Document Title",
        "version": "1.0.0",
        "date": "2025-08-16",
        "author": "Your Organization",
        "company": "Your Company Name"
      }
    }
  ],
  "options": {
    "cleanup": true,
    "archive": true,
    "optimize": true
  }
}
```

### Available Templates
- `admin-manual` - Professional administrator documentation
- `user-guide` - Clean, accessible user documentation
- Custom templates (see Template Creation section)

## 📝 Markdown Compatibility

### ✅ Safe Markdown Patterns
```markdown
# Headers (all levels work)
## Subheaders
### etc.

**Bold text** and *italic text*

- Bullet lists
- Work perfectly
  - Including nested lists

1. Numbered lists
2. Also work well
   1. With sub-numbering

`Inline code` is safe

\```bash
# Code blocks work great
command --with --flags
\```

> Blockquotes are supported

| Tables | Also | Work |
|--------|------|------|
| Data   | Goes | Here |

[Links work](https://example.com)
```

### ⚠️ Potential Issues to Avoid

**Complex HTML**: Stick to standard markdown
```markdown
❌ <div class="custom">Complex HTML</div>
✅ **Use markdown formatting instead**
```

**Custom CSS**: Won't work in LaTeX
```markdown
❌ <style>css here</style>
✅ Let the template handle formatting
```

**Unsupported Extensions**: Avoid non-standard markdown
```markdown
❌ ~~strikethrough~~ (may not work)
✅ **emphasis** or *italic* instead
```

## 🎨 Template Creation

### Required LaTeX Compatibility Block

If you create custom LaTeX templates, **ALWAYS** include this compatibility block:

```latex
% Pandoc compatibility fixes (REQUIRED)
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\providecommand{\passthrough}[1]{#1}
\providecommand{\euro}{\texteuro}
\providecommand{\UrlFont}{\ttfamily}
\providecommand{\footnotesize}{}
\providecommand{\oldparagraph}{}
\providecommand{\oldsubparagraph}{}
\ifx\paragraph\undefined\else
  \let\oldparagraph\paragraph
  \renewcommand{\paragraph}[1]{\oldparagraph{#1}\mbox{}}
\fi
\ifx\subparagraph\undefined\else
  \let\oldsubparagraph\subparagraph
  \renewcommand{\subparagraph}[1]{\oldsubparagraph{#1}\mbox{}}
\fi
```

### Template Variables

Use these patterns for dynamic content:
```latex
% Document variables from request.json
\newcommand{\docTitle}{$title$}
\newcommand{\docVersion}{$version$}
\newcommand{\docDate}{$date$}
\newcommand{\docAuthor}{$author$}
\newcommand{\docCompany}{$company$}

% Use in document
{\Huge\bfseries \docTitle\par}
{\Large Version \docVersion\par}
{\large \docDate\par}
```

### Safe Image References

Images must exist or be optional:
```latex
% Safe approach - optional logo
\IfFileExists{logo.png}{
  \includegraphics[width=0.3\textwidth]{logo.png}
}{
  % Fallback or skip logo
}

% Or comment out if not provided
% \includegraphics[width=0.3\textwidth]{logo.png}
```

## 📁 Directory Structure

When generating documents for doc-forge processing:

```
your-repo/
├── documents-for-pdf/
│   ├── inbox/
│   │   ├── your-document.md      # Generated content
│   │   └── request.json          # Generated config
│   └── templates/                # Custom templates (optional)
│       └── your-template.latex   # With compatibility fixes
└── scripts/
    └── generate-pdf-request.js   # Your generation script
```

## 🔧 Generation Script Example

```javascript
// generate-pdf-request.js
const fs = require('fs-extra');

async function generatePDFRequest(content, metadata) {
  // Create the request
  const request = {
    documents: [{
      input: `${metadata.name}.md`,
      output: `${metadata.title}_v${metadata.version}.pdf`,
      template: metadata.template || 'admin-manual',
      variables: {
        title: metadata.title,
        version: metadata.version,
        date: new Date().toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long', 
          day: 'numeric'
        }),
        author: metadata.author,
        company: metadata.company
      }
    }],
    options: {
      cleanup: true,
      archive: true, 
      optimize: true
    }
  };

  // Write files
  await fs.outputFile(`documents-for-pdf/inbox/${metadata.name}.md`, content);
  await fs.outputJSON('documents-for-pdf/inbox/request.json', request, { spaces: 2 });
  
  console.log('✅ PDF request generated in documents-for-pdf/inbox/');
}
```

## 🚀 Workflow Integration

### 1. Generate Compatible Content
```bash
# In your repo
node scripts/generate-pdf-request.js
```

### 2. Copy to Doc-Forge
```bash
# Copy your generated content to doc-forge
cp documents-for-pdf/inbox/* /path/to/doc-forge/inbox/
```

### 3. Process in Doc-Forge
```bash
# In doc-forge container
make process
```

### 4. Retrieve PDFs
```bash
# Copy results back
cp /path/to/doc-forge/outbox/*.pdf ./generated-pdfs/
```

## ✅ Testing Your Integration

### Validation Checklist
- [ ] Markdown uses only standard syntax
- [ ] request.json follows the required format
- [ ] Custom templates include compatibility fixes
- [ ] Images are optional or guaranteed to exist
- [ ] Variables are properly defined
- [ ] Test with actual doc-forge processing

### Quick Test
```bash
# Validate your request.json
node /path/to/doc-forge/scripts/validate-request.js your-request.json
```

## 🔍 Troubleshooting

### Common Issues

**"Undefined control sequence" errors**:
- Add the compatibility fixes to your template
- Check for custom LaTeX commands without definitions

**"File not found" errors**:
- Make sure all referenced images exist
- Use optional image includes or comment out missing files

**"Invalid request.json"**:
- Validate JSON syntax
- Ensure all required fields are present
- Check that referenced files exist

### Getting Help

**Template Issues**: Check existing templates in `/templates/` for examples
**Request Format**: Use the validation script to check your request.json
**Markdown Problems**: Test with simple markdown first, then add complexity

---

## 📋 Quick Reference

### Minimal Working Example
```json
{
  "documents": [{
    "input": "simple-doc.md", 
    "output": "Simple_Document.pdf",
    "template": "admin-manual",
    "variables": {
      "title": "Simple Document",
      "version": "1.0",
      "date": "2025-08-16"
    }
  }],
  "options": { "cleanup": true }
}
```

### Required Template Header
```latex
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\providecommand{\passthrough}[1]{#1}
```

### Safe Markdown
- Standard headers, lists, code blocks, tables
- Avoid HTML, custom CSS, complex extensions
- Test with simple content first

---

*This guide ensures your repository generates content that works seamlessly with doc-forge PDF processing.*
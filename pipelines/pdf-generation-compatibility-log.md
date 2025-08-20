# PDF Generation Compatibility Log

**LaTeX Package Compatibility Issues and Solutions for Doc-Forge System**

---

## 🚨 CRITICAL COMPATIBILITY ISSUES

### ❌ **Packages That DON'T Work**

#### 1. `longtabu` Package
**Error**: `! LaTeX Error: File 'longtabu.sty' not found.`
**Cause**: Package not available in doc-forge TeX Live 2022 distribution
**Failed Template Version**: p2kb-pasm2-manual v1.0
**Solution**: Replace with standard `longtable` + `array` packages

#### 2. `titlesec` Package  
**Error**: `! Argument of \paragraph has an extra }.`
**Cause**: Conflicts with pandoc's paragraph handling
**Failed Template Versions**: p2kb-pasm2-manual v1.1, v1.2
**Solution**: Remove `titlesec` entirely, use basic LaTeX sectioning

---

## ✅ **Packages That DO Work**

### Safe Package List (Tested Working)
- `[utf8]{inputenc}` - Text encoding ✅
- `[T1]{fontenc}` - Font encoding ✅
- `lmodern` - Latin Modern fonts ✅
- `geometry` - Page layout ✅
- `fancyhdr` - Headers/footers ✅
- `xcolor` - Color support ✅
- `booktabs` - Professional tables ✅
- `longtable` - Multi-page tables ✅
- `array` - Enhanced arrays ✅
- `listings` - Code syntax highlighting ✅
- `graphicx` - Graphics inclusion ✅
- `hyperref` - PDF links ✅

---

## 🔧 **Working Solutions**

### Title Page Design
**Works**: Basic LaTeX formatting with `minipage` layout
```latex
\begin{minipage}[t]{0.3\textwidth}
  % Left content
\end{minipage}%
\hfill
\begin{minipage}[t]{0.65\textwidth}
  % Right content  
\end{minipage}
```

### Section Formatting
**Works**: Default LaTeX sectioning commands
- Use `\section{}`, `\subsection{}`, `\subsubsection{}` as-is
- Apply colors with `\textcolor{color}{text}`
- **Avoid**: Custom `\titleformat` modifications

### Table Formatting
**Works**: Standard `longtable` environment
```latex
\begin{longtable}{|p{width}|p{width}|...}
  \hline
  \rowcolor{color} Header & Content \\
  \hline
  \endhead
  % Content rows
  \hline
\end{longtable}
```
**Avoid**: `longtabu`, `tabu`, custom table packages

### Headers/Footers
**Works**: Standard `fancyhdr` package
```latex
\fancyhead[L]{\textcolor{color}{\textbf{$title$}}}
\fancyfoot[C]{\thepage}
```

---

## 📝 **Template Evolution History**

### Version 1.0 - Failed (longtabu issue)
- Used `longtabu` package for instruction tables
- Error: Package not found in TeX distribution
- **Lesson**: Stick to standard TeX Live packages

### Version 1.1 - Failed (longtabu fixed, titlesec issue)
- Fixed: Replaced `longtabu` with `longtable`
- New Error: `titlesec` paragraph conflicts
- **Lesson**: Package replacement successful, but introduced new conflict

### Version 1.2 - Failed (titlesec conflict persisted)
- Attempted: Added explicit `\paragraph` formatting
- Error: Still conflicted with pandoc paragraph handling
- **Lesson**: `titlesec` fundamentally incompatible with pandoc

### Version 1.3 - SUCCESS (simplified approach)
- Fixed: Removed `titlesec` entirely
- Used: Basic LaTeX sectioning with manual color formatting
- **Lesson**: Simple, standard LaTeX works best with pandoc

---

## 🎯 **Best Practices for Doc-Forge Templates**

### DO:
1. **Use standard TeX Live packages** - Check package availability first
2. **Test incrementally** - Add one package at a time
3. **Keep it simple** - Basic LaTeX is more reliable than advanced packages
4. **Follow pandoc conventions** - Work with pandoc, not against it
5. **Document failures** - Track what doesn't work for future reference

### DON'T:
1. **Assume package availability** - Doc-forge may have limited package set
2. **Override pandoc defaults** - Especially paragraph/sectioning handling
3. **Use cutting-edge packages** - Stick to well-established, standard packages
4. **Complex formatting** - Simple approaches are more reliable

---

## 🚀 **Template Development Workflow**

### 1. **Start Minimal**
Begin with absolute minimum packages and basic formatting

### 2. **Add Incrementally** 
Add one package/feature at a time, test each addition

### 3. **Test Early and Often**
Generate test PDFs after each change

### 4. **Document Failures**
Record exactly what fails and why for future reference

### 5. **Prefer Standard Solutions**
Choose standard LaTeX over custom packages when possible

---

## 📊 **Success Rate by Approach**

| Approach | Success Rate | Notes |
|----------|-------------|--------|
| Advanced packages (longtabu, titlesec) | ❌ 0% | Not available or conflicts |
| Standard packages (longtable, fancyhdr) | ✅ 100% | Reliable, well-supported |
| Basic LaTeX formatting | ✅ 100% | Always works |
| Custom commands/environments | ⚠️ Mixed | Test thoroughly |

---

**Key Insight**: Doc-forge + pandoc + LaTeX requires a conservative, standard-library approach. Advanced formatting packages often conflict or aren't available.

**Update Policy**: Add new compatibility findings to this log immediately after discovery.
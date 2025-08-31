\# LaTeX Escaping Test Cases for P2 Assembly Manual

This file contains all the problematic patterns found in real P2 content that must be escaped correctly.

\#\# Assembly Code Patterns

\#\#\# Immediate Values (\# characters)
- Basic immediate: `mov x, \#42`
- Double immediate: `waitx \#\#25\_000\_000`
- Hex immediate: `mov x, \#\$FF`
- Binary immediate: `mov x, \#\%1010\_0001`

\#\#\# Register References (\$ patterns)
- Hex values: `\$1\_0000\_0000 represents full circle`
- Hub addresses: `wrlong data, \#\#\$1000`
- Special registers: `rdlong pa, \#\$14`

\#\#\# Underscores in Code
- Numeric separators: `25\_000\_000`
- Hex with underscores: `\$FF\_AA\_BB\_CC`
- Variable names: `hub\_address`
- Labels: `main\_loop:`

\#\#\# Mathematical Expressions
- Powers: `2\^\{\}9 = 512`
- Exponents: `e\^\{\}2 = 7.389`
- Complex: `2\^\{\}32 addresses`

\#\#\# Special Characters in Context
- Pin ranges: `pins 16-47 are safe`
- Assembly comments: `' This is a comment`
- Bit operations: `value & mask`
- Percentages: `80\% complete`

\#\# Markdown Headers (Should NOT be escaped)
\# Chapter 1: Assembly Basics
\#\# Section 2.1: Memory Layout
\#\#\# Subsection 3.2.1: Register Usage

\#\# Code Blocks (Should NOT be escaped)
```pasm2
' Assembly code should remain unescaped
mov x, #42
waitx ##25_000_000
wrlong data, ##$1000
```

\#\# LaTeX Environments (Should NOT be escaped)
\begin{sidetrack}
\textbf{This LaTeX should remain untouched}
Including {braces} and $math$ and #symbols
\end{sidetrack}

\#\# Complex Mixed Content
The P2 can address 2\^\{\}9 = 512 locations with \#9-bit immediate values.
Hub memory starts at \$0000 and extends to \$7\_FFFF (512KB total).
Pin \#16 connects to LED with 220Ω resistor for \textasciitilde{}15mA current (3.3V / 220Ω).

\#\# Edge Cases
- Multiple patterns: `mov \#reg, \#\#\$FF\_AA & mask`
- Nested patterns: `2\^\{\}(n+1) where n=\#bits`
- Mixed quotes: "Use \#immediate" vs 'reg \#value'
- URL-like: `http://example.com\#anchor`
- Email-like: `user@domain.com`
- Temperature: `25°C & 77°F`

\#\# Tricky Boundaries
- Start of line \#immediate
- End of line immediate\#
- Mid-sentence like this\#value here
- Multiple in sequence: \#\#immediate \#\#values
- With punctuation: \#value, \#other; \#final.

\#\# Known Problem Patterns
Line that caused PDF error: "With 9 bits, you can address 2\^\{\}9 = 512 locations"
Assembly immediate in text: "The \#\#25\_000\_000 value equals 0.5 seconds"
Mixed hex and underscore: "\$1\_0000\_0000 represents the full circle value"

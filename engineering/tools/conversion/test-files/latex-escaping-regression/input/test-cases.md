# LaTeX Escaping Test Cases for P2 Assembly Manual

This file contains all the problematic patterns found in real P2 content that must be escaped correctly.

## Assembly Code Patterns

### Immediate Values (# characters)
- Basic immediate: `mov x, #42`
- Double immediate: `waitx ##25_000_000`
- Hex immediate: `mov x, #$FF`
- Binary immediate: `mov x, #%1010_0001`

### Register References ($ patterns)
- Hex values: `$1_0000_0000 represents full circle`
- Hub addresses: `wrlong data, ##$1000`
- Special registers: `rdlong pa, #$14`

### Underscores in Code
- Numeric separators: `25_000_000`
- Hex with underscores: `$FF_AA_BB_CC`
- Variable names: `hub_address`
- Labels: `main_loop:`

### Mathematical Expressions
- Powers: `2^9 = 512`
- Exponents: `e^2 = 7.389`
- Complex: `2^32 addresses`

### Special Characters in Context
- Pin ranges: `pins 16-47 are safe`
- Assembly comments: `' This is a comment`
- Bit operations: `value & mask`
- Percentages: `80% complete`

## Markdown Headers (Should NOT be escaped)
# Chapter 1: Assembly Basics
## Section 2.1: Memory Layout
### Subsection 3.2.1: Register Usage

## Code Blocks (Should NOT be escaped)
```pasm2
' Assembly code should remain unescaped
mov x, #42
waitx ##25_000_000
wrlong data, ##$1000
```

## LaTeX Environments (Template vs Standard)
\begin{sidetrack}
\textbf{This LaTeX should remain untouched}
Including {braces} and $math$ and #symbols
\end{sidetrack}

## Complex Mixed Content
The P2 can address 2^9 = 512 locations with #9-bit immediate values.
Hub memory starts at $0000 and extends to $7_FFFF (512KB total).
Pin #16 connects to LED with 220Ω resistor for ~15mA current (3.3V / 220Ω).

## Edge Cases
- Multiple patterns: `mov #reg, ##$FF_AA & mask`
- Nested patterns: `2^(n+1) where n=#bits`
- Mixed quotes: "Use #immediate" vs 'reg #value'
- URL-like: `http://example.com#anchor`
- Email-like: `user@domain.com`
- Temperature: `25°C & 77°F`

## Tricky Boundaries
- Start of line #immediate
- End of line immediate#
- Mid-sentence like this#value here
- Multiple in sequence: ##immediate ##values
- With punctuation: #value, #other; #final.

## Known Problem Patterns  
Line that caused PDF error: "With 9 bits, you can address 2^9 = 512 locations"
Assembly immediate in text: "The ##25_000_000 value equals 0.5 seconds"
Mixed hex and underscore: "$1_0000_0000 represents the full circle value"

## NEW Regression Cases (Found in Production)
Power expression in sidetrack: "With 9 bits, you can address 2^9 = 512 locations"
Addressing calculation: "2^32 total address space"
Bit calculation: "Use 2^n where n=bit_count"

## Template Environment Test (Process Content)
\begin{sidetrack}
\textbf{Why 512 Longs?}

The magic number 512 comes from addressing. With 9 bits, you can address 2^9 = 512 locations. This fits perfectly in P2 instruction encoding.
\end{sidetrack}

## LaTeX List Commands Test (Should NOT be escaped)
\begin{sidetrack}
\textbf{Key Points:}
\begin{itemize}
\item First point with #immediate value
\item Second point with $hex_value  
\item Third point with 2^8 = 256
\end{itemize}
\end{sidetrack}

## Comprehensive LaTeX Command Protection Test
\begin{sidetrack}
\section{Test Section with #special}
\subsection{Subsection with $values}

Formatting tests:
\par
New paragraph with \noindent no indent.
\centering
Centered text with 2^8 = 256.
\raggedright

Size commands: \small small text \large large text \normalsize normal.

Spacing: word\quad space\qquad bigger\,thin\:medium\;thick space.
\bigskip
After big skip with \vspace{1em} vertical space.

References: See \ref{fig:example} on page \pageref{fig:example}.
\label{test:label}

Special chars: \ldots and \copyright 2025.

Math delimiters: \(x^2 + y^2 = z^2\) inline and
\[
E = mc^2
\]
display math.

Line breaks: First line\\Second line\newline Third line.
\end{sidetrack}

\begin{interlude}
Hub memory layout: $0000 to $7_FFFF (512KB total).
Pin #16 connects to LED with 220Ω resistor for ~15mA current.
\end{interlude}

## Standard LaTeX Environment Test (Preserve Completely)
\begin{equation}
E = mc^2 where c = 3 × 10^8 m/s
\end{equation}

\begin{align}
F &= ma \\
E &= \frac{1}{2}mv^2
\end{align}

## Mixed Environment Patterns
Normal text with 2^9 = 512 locations.
\begin{sidetrack}
Inside template: Use #immediate with 2^8 = 256 values.
\end{sidetrack}
More normal text with $FF_AA patterns.
\begin{equation}
\sum_{i=1}^{n} x_i = n \cdot \bar{x}
\end{equation}
Final normal text with underscore_patterns.

## Table with Tilde Approximation Test
| Mode | Speed | Description |
|------|-------|--------------|
| Fast | ~3 clocks | Approximate timing |
| Slow | ~10 clocks | Variable delay |
| FIFO | ~2-3 clocks | Best case scenario |

## Indented Code Blocks Test (Bug Fix)
This tests code blocks that are indented (e.g., in lists).

1. **Reset Pin** (optional but recommended)
   ```pasm2
   dirl    #pin            ' Disable pin (Smart Pin OFF)
   ```

2. **Configure Mode**
   ```pasm2
   wrpin   mode_value, #pin ' Write mode configuration
   ```

3. **Set X Parameter** (mode-dependent)
   ```pasm2
   wxpin   x_value, #pin   ' Write X parameter
   ```

4. **Configuration Block with attribute**
   ```{.configuration}
   CON
     CONFIG_VALUE = $1234_5678    ' Hex with $ and underscore
   ```

## Inline Code Test (Bug Fix)
This tests inline code that should NOT be escaped.

1. **`P_TRANSITION`** - Selects transition output mode
2. **`P_OE`** - Enables output driver  
3. Use `wxpin x_value, #pin` to set X parameter
4. The `##25_000_000` value equals 0.5 seconds
5. Register `$FF_AA` contains the mask
6. Set `mode_value` with `P_PWM_SAWTOOTH`

Regular text outside backticks: P_TRANSITION and $FF_AA should be escaped here.
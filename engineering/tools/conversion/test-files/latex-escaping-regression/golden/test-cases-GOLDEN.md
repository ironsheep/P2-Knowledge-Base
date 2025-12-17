# LaTeX Escaping Test Cases for P2 Assembly Manual

This file contains all the problematic patterns found in real P2 content that must be escaped correctly.

## Assembly Code Patterns

### Immediate Values (\# characters)
- Basic immediate: `mov x, #42`
- Double immediate: `waitx ##25_000_000`
- Hex immediate: `mov x, #$FF`
- Binary immediate: `mov x, #%1010_0001`

### Register References (\$ patterns)
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
Including \{braces\} and \$math\$ and \#symbols
\end{sidetrack}

## Complex Mixed Content
The P2 can address 2\^{}9 = 512 locations with \#9-bit immediate values.
Hub memory starts at \$0000 and extends to \$7\_FFFF (512KB total).
Pin \#16 connects to LED with 220Ω resistor for ~15mA current (3.3V / 220Ω).

## Edge Cases
- Multiple patterns: `mov #reg, ##$FF_AA & mask`
- Nested patterns: `2^(n+1) where n=#bits`
- Mixed quotes: "Use \#immediate" vs 'reg \#value'
- URL-like: `http://example.com#anchor`
- Email-like: `user@domain.com`
- Temperature: `25°C & 77°F`

## Tricky Boundaries
- Start of line \#immediate
- End of line immediate\#
- Mid-sentence like this\#value here
- Multiple in sequence: \#\#immediate \#\#values
- With punctuation: \#value, \#other; \#final.

## Known Problem Patterns  
Line that caused PDF error: "With 9 bits, you can address 2\^{}9 = 512 locations"
Assembly immediate in text: "The \#\#25\_000\_000 value equals 0.5 seconds"
Mixed hex and underscore: "\$1\_0000\_0000 represents the full circle value"

## NEW Regression Cases (Found in Production)
Power expression in sidetrack: "With 9 bits, you can address 2\^{}9 = 512 locations"
Addressing calculation: "2\^{}32 total address space"
Bit calculation: "Use 2\^{}n where n=bit\_count"

## Template Environment Test (Process Content)
\begin{sidetrack}
\textbf{Why 512 Longs?}

The magic number 512 comes from addressing. With 9 bits, you can address 2\^{}9 = 512 locations. This fits perfectly in P2 instruction encoding.
\end{sidetrack}

## LaTeX List Commands Test (Should NOT be escaped)
\begin{sidetrack}
\textbf{Key Points:}
\begin{itemize}
\item First point with \#immediate value
\item Second point with \$hex\_value  
\item Third point with 2\^{}8 = 256
\end{itemize}
\end{sidetrack}

## Comprehensive LaTeX Command Protection Test
\begin{sidetrack}
\section{Test Section with \#special}
\subsection{Subsection with \$values}

Formatting tests:
\par
New paragraph with \noindent no indent.
\centering
Centered text with 2\^{}8 = 256.
\raggedright

Size commands: \small small text \large large text \normalsize normal.

Spacing: word\quad space\qquad bigger\,thin\:medium\;thick space.
\bigskip
After big skip with \vspace{1em} vertical space.

References: See \ref{fig:example} on page \pageref{fig:example}.
\label{test:label}

Special chars: \ldots and \copyright 2025.

Math delimiters: \(x\^{}2 + y\^{}2 = z\^{}2\) inline and
\[
E = mc\^{}2
\]
display math.

Line breaks: First line\\Second line\newline Third line.
\end{sidetrack}

\begin{interlude}
Hub memory layout: \$0000 to \$7\_FFFF (512KB total).
Pin \#16 connects to LED with 220Ω resistor for ~15mA current.
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
Normal text with 2\^{}9 = 512 locations.
\begin{sidetrack}
Inside template: Use \#immediate with 2\^{}8 = 256 values.
\end{sidetrack}
More normal text with \$FF\_AA patterns.
\begin{equation}
\sum_{i=1}^{n} x_i = n \cdot \bar{x}
\end{equation}
Final normal text with underscore\_patterns.

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

Regular text outside backticks: P\_TRANSITION and \$FF\_AA should be escaped here.

## Fenced Div Code Blocks Test (Bug Fix - Issue \#324)
This tests ::: fenced divs with code type labels (pasm2, spin2, etc.) that should NOT be escaped.

::: pasm2
        XINIT   mode, data         ' Start data transfer
        WYPIN   count, #clk_pin    ' Start clock generation
        WAITXFI                    ' Wait for completion
:::

::: spin2
    ' Spin2 code with underscores and $ values
    hub_address := $FF_AA_BB
    wait_time := ##25_000_000
:::

::: cordic
    ' CORDIC operations with special chars
    QROTATE x_val, #angle_deg
    GETQX   result_x
:::

Text between divs should have \#special and \$chars and \_underscores escaped.

::: antipattern
' WRONG: This antipattern code should NOT be escaped
    mov   x, #bad_value      ' Bad pattern with #immediate
    wrlong $bad_addr, data   ' Bad hex address
:::

Final regular text with \#hash and \$dollar and \_underscore should be escaped.

## Trailing Backslash Test (Pandoc Hard Line Breaks)
This tests trailing backslash preservation for Pandoc hard line breaks.

**TESTP**  *{\#}Dest*  WC/WZ\
**TESTPN**  *{\#}Dest*  WC/WZ

Multiple consecutive lines with trailing backslash:
**MOV**  *Dest*, *{\#}Src*\
**ADD**  *Dest*, *{\#}Src*\
**SUB**  *Dest*, *{\#}Src*

Mixed content with backslash and special chars:
Line with \#immediate and trailing backslash\
Line with \$hex\_value and trailing backslash\
Line with underscore\_pattern and trailing backslash\
Final line without trailing backslash

Regular text should still have \_underscores and \#hash escaped even near backslashes.

## Grid Table Alignment Test (Bug Fix - Grid Tables with \%)
This tests grid tables containing \% characters. The escape processor must NOT escape
\% inside grid tables because adding the backslash breaks column alignment and causes
Pandoc to misparse the table structure.

Grid table with \% in data cells:

+------+----------------+-------------+-------------------+-----------+
| Bits | SETQ D Pattern | LUT Base    | Index Calculation | Bytecodes |
+======+================+=============+===================+===========+
| 8    | %A0000000F     | %A00000000  | I = bytecode[7:0] | 256       |
+------+----------------+-------------+-------------------+-----------+
| 7    | %AAxx0010F     | %AA0000000  | I = bytecode[6:0] | 128       |
+------+----------------+-------------+-------------------+-----------+
| 4    | %AAAAA111F     | %AAAAA0000  | I = bytecode[7:4] | 16        |
+------+----------------+-------------+-------------------+-----------+

Grid table with multi-line cells and \%:

+----------------------------+------------------------------+------------------------------------------+
| Constant                   | Value                        | Description                              |
+============================+==============================+==========================================+
| X_1ADC8_0P_1DAC8_WFBYTE    | %1111_0000_0000_0010 << 16   | 1 ADC to 8-bit, 0 pins, 1 DAC,           |
|                            |                              | write byte                               |
+----------------------------+------------------------------+------------------------------------------+
| X_2ADC8_0P_2DAC8_WFWORD    | %1111_0000_0000_0100 << 16   | 2 ADCs to 8-bit, 0 pins, 2 DACs,         |
|                            |                              | write word                               |
+----------------------------+------------------------------+------------------------------------------+

Text after grid table should have \%percent escaped normally.

Pipe table with \% (should still be escaped since pipe tables don't have alignment issues):

| Mode | Value | Description |
|------|-------|-------------|
| Binary | \%1010 | Binary pattern |
| Hex | \$FF | Hex value |

## Hypertarget Anchor Commands Test (Bug Fix - Cross-reference anchors)
This tests \\hypertarget commands used for Pandoc cross-references. These LaTeX
commands must NOT be escaped - they create anchor points for internal links.

Single hypertarget:
\hypertarget{resi0}{}

Multiple hypertargets on one line (common for combined instruction groups):
\hypertarget{resi1}{}\hypertarget{resi2}{}\hypertarget{resi3}{}

Hypertargets for interrupt instructions:
\hypertarget{setint2}{}\hypertarget{setint3}{}

Hypertargets for counter instructions:
\hypertarget{addct2}{}\hypertarget{addct3}{}
\hypertarget{pollct2}{}\hypertarget{pollct3}{}
\hypertarget{waitct2}{}\hypertarget{waitct3}{}

Hypertargets for event instructions:
\hypertarget{jse2}{}\hypertarget{jse3}{}\hypertarget{jse4}{}\hypertarget{jnse1}{}\hypertarget{jnse2}{}\hypertarget{jnse3}{}\hypertarget{jnse4}{}

Text after hypertargets should have \#hash and \$dollar and \_underscore escaped normally.

## Pandoc Superscript Syntax Test (Bug Fix - Encoding table footnotes)
This tests Pandoc's `^text^` superscript syntax used for footnote markers in encoding tables.
The escape processor must NOT escape the caret characters in `^text^` patterns, because:
1. Pandoc converts `^text^` to `\textsuperscript{text}` in LaTeX
2. If we escape `^` to `\^{}`, Pandoc sees it as a literal caret
3. Pandoc then outputs `^{}` to LaTeX, which is invalid outside math mode
4. xelatex fails with "Missing \$ inserted" error

Simple superscript patterns (from encoding tables):
D^1^ should become D\textsuperscript{1}
D^2^ should become D\textsuperscript{2}
Result^1^ for footnote reference

Multiple superscripts in table-like context:
| Result | Clks |
|--------|------|
| D^1^ | 2 |
| S^2^ | 4 |

Superscript with multiple characters:
D^10^ for footnote 10
Result^note^ for text superscript

Mixed content with superscripts:
The value D^1^ is adjusted by Src[17:9]^2^ per the auto-indexer^3^.

Regular caret (NOT superscript) should still be escaped:
Power expression: 2\^{}9 = 512 (single caret, not paired)
Bitwise XOR: a \^{} b (spaces around caret)

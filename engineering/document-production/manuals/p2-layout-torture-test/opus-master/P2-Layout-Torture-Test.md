<!--
  P2 LAYOUT TORTURE TEST — engineered to reproduce every known layout defect on a small,
  fast-to-generate document built on the live (Streamer Tier-1 twin) stack. Each case carries
  a visible yellow EXPECT box (defined in p2kb-torture-content.sty) describing what to look for,
  and boundary-sensitive elements are forced near the page foot with \leavebottom so they must
  straddle. Annotations use single-line TORTURE comments; none are nested inside another comment.
-->

```{=latex}
% --- Torture-harness-only definitions, kept IN the document so it is self-contained ---
% (defined here, not in content.sty, so the harness never depends on which content.sty
%  the Forge happens to hold). tcolorbox is already loaded by the foundation layer.
\definecolor{torture-expect-bg}{HTML}{FFF8D0}
\definecolor{torture-expect-frame}{HTML}{B8860B}
% NOTE: ExpectBox is deliberately UNBREAKABLE. It is small (a few lines) and always
% fits, and keeping it unbreakable makes it contribute to \pagetotal synchronously —
% which \leavebottom below relies on to measure the page accurately (a breakable box
% defers and made \leavebottom overshoot, ejecting/dropping the demo).
\newtcolorbox{ExpectBox}{%
  enhanced, unbreakable,
  colback=torture-expect-bg, colframe=torture-expect-frame,
  boxrule=1pt, leftrule=5pt, arc=2pt,
  left=10pt, right=10pt, top=6pt, bottom=6pt,
  before skip=12pt, after skip=10pt,
  fontupper=\small,
  coltitle=black, fonttitle=\bfseries\small, colbacktitle=torture-expect-bg,
  title={EXPECT --- what this case should show}
}
% VerifiedBox (green): a case whose desired behavior is ALREADY IMPLEMENTED and has been
% validated (toggle + standard check). Renders correctly — NOT a defect. Same unbreakable
% shape as ExpectBox so \leavebottom measurement stays accurate.
\definecolor{torture-verified-bg}{HTML}{E6F4EA}
\definecolor{torture-verified-frame}{HTML}{2E7D32}
\newtcolorbox{VerifiedBox}{%
  enhanced, unbreakable,
  colback=torture-verified-bg, colframe=torture-verified-frame,
  boxrule=1pt, leftrule=5pt, arc=2pt,
  left=10pt, right=10pt, top=6pt, bottom=6pt,
  before skip=12pt, after skip=10pt,
  fontupper=\small,
  coltitle=black, fonttitle=\bfseries\small, colbacktitle=torture-verified-bg,
  title={$\checkmark$ VERIFIED --- renders correctly (already implemented)}
}
% ProcessBox (blue): a case whose standard is enforced at BUILD TIME and in the
% SOURCE, not by the template render. The template makes the condition VISIBLE
% (e.g. an over-long code line overflows rather than silently wrapping); a
% prepare-time audit flags it against a calibrated budget; the author fixes the
% source. So the render below deliberately shows the un-fixed condition --- it is
% the audit's test fixture, not a defect the template should paper over.
\definecolor{torture-process-bg}{HTML}{E8EDF5}
\definecolor{torture-process-frame}{HTML}{3F51B5}
\newtcolorbox{ProcessBox}{%
  enhanced, unbreakable,
  colback=torture-process-bg, colframe=torture-process-frame,
  boxrule=1pt, leftrule=5pt, arc=2pt,
  left=10pt, right=10pt, top=6pt, bottom=6pt,
  before skip=12pt, after skip=10pt,
  fontupper=\small,
  coltitle=black, fonttitle=\bfseries\small, colbacktitle=torture-process-bg,
  title={PROCESS --- enforced by the build audit + in source, not by the template}
}
% \leavebottom{X}: force the following demo toward the page foot so it must straddle the
% boundary (the whole point of the torture cases) — but SAFELY. The earlier version dropped
% content because it measured \pagetotal while the EXPECT box was still breakable (deferred),
% so the \vspace* overshot and pushed the demo off-page. Now the EXPECT box is unbreakable, so
% \pagetotal is accurate here. We push to leave X at the foot, but FLOOR the room left at
% 0.32\textheight so a figure's 0.30\textheight \needspace is always satisfiable and nothing is
% ejected/dropped. The floor (how much blank we tolerate to force a straddle) is the
% whitespace-tolerance knob from USER-PREFERENCES A1 vs C5/C7 — tune it here, centrally.
% #1 = floor (optional): minimum space left at the foot, protecting an unbreakable figure
%      from ejection. Default is SMALL so strand/split cases actually reach the page foot.
%      FIGURE/diagram cases pass a larger floor (>= figure height), e.g. [0.32\textheight].
% #2 = target space to leave at the foot.
% Root-cause fix 2026-06-05: the old hard-coded 0.32\textheight floor clamped EVERY case
%      ~2.9in above the foot, so short content never reached a boundary (systemic under-force).
\newcommand{\leavebottom}[2][0.04\textheight]{%
  \par\begingroup
  \dimen0=\dimexpr\textheight-\pagetotal-#2\relax
  \dimen2=\dimexpr\textheight-\pagetotal-#1\relax
  \ifdim\dimen0>\dimen2 \dimen0=\dimen2 \fi
  % NON-starred \vspace (breakable/discardable) — the page builder can break cleanly
  % instead of overflowing the custom \output routine (which drops the demo).
  \ifdim\dimen0>0pt \vspace{\dimen0}\fi
  \endgroup}

\begin{center}
\vspace*{0.5cm}
{\fontsize{36}{42}\selectfont\bfseries P2 Layout Torture Test\par}
\vspace{0.3cm}
{\Large\itshape Every Page-Break, Table, Code, and Figure Defect, On Purpose\par}
\vspace{0.6cm}
{\large June 2026\par}
\vspace{0.2cm}
{\large\color{blue}Version 0.3 (engineering harness)\par}

\vfill
\begin{tcolorbox}[
  colback=gray!5, colframe=gray!40, boxrule=1pt, width=0.88\textwidth, center,
  title={\bfseries\color{black} How to Read This Document},
  colbacktitle=gray!15, coltitle=black
]
This is not a real manual. It is a deliberate stress test for the PDF layout pipeline,
built on the live document stack. Before each case is a \textbf{yellow EXPECT box} stating,
in plain language, what that case is supposed to demonstrate and what the defect looks like.
Many elements are deliberately forced near the foot of a page so they must break across the
boundary. Read each EXPECT box, then look at what actually happened just below it.
\end{tcolorbox}
\vfill
\end{center}

\clearpage
```

# Part I: Page-Break and Keep-Together Torture

```{=latex}
\begin{VerifiedBox}
This Part has an introduction (the two paragraphs below). The first chapter heading
(``Chapter 1'') appears cleanly \emph{below} this intro text with normal spacing --- it does
not overlap the intro lines. Verified: the pinned-chapter spacing fix in the content layer.
\end{VerifiedBox}
```

This is a **Part introduction** — prose that belongs to the part as a whole, sitting between
the part title and the first chapter. Our house style keeps the first chapter on the part's
page rather than pushing it to a fresh page, and we want this intro to flow naturally into that
first chapter heading rather than colliding with it.

The introduction runs to a second paragraph so there is real text for the chapter heading to
collide with. The first chapter heading must appear *after* this text, never on top of it.

# Chapter 1: Headings and Their Content

This chapter stresses heading-to-content cohesion at page boundaries: stranded headings, blocks
that must stay together, and headings that must not detach from what they introduce.

```{=latex}
\clearpage
```

## 1.1 An Orphaned Heading

```{=latex}
\begin{VerifiedBox}
The heading below is forced to the page foot. It pulls its first body line with it onto the
same page --- the heading does not strand alone at the bottom. Verified: the foundation's
keep-with-next protection (needspace) holds the heading and its body together.
\end{VerifiedBox}
\leavebottom{0.75in}
```

### 1.1.1 This Subheading Should Keep Its Body

The paragraph beneath this subheading proves whether keep-with-next works. If the subheading
sits at the bottom of the page and this paragraph begins on the next, that is the orphaned-heading
defect. These are ballast words, but they must read as ordinary prose so the layout engine treats
them the way it treats real content, and there should be enough of them to clearly wrap onto the
following page.

```{=latex}
\clearpage
```

## 1.2 A Heading, Intro, Diagram, and Caption as One Block

```{=latex}
\begin{VerifiedBox}
The heading, its one-line intro, the diagram, and the caption below are ONE unit, forced to
the page foot. They stay together --- the diagram and caption do not detach from the
heading/intro; the whole block moves as a unit. Verified in the v6 render.
\end{VerifiedBox}
\leavebottom[0.32\textheight]{1.6in}
```

### 1.2.1 Read This Block as One Unit

This one-line intro belongs with the diagram below it and that diagram's caption.

```{=latex}
\DiagDataFlow
```

::: {.figurecaption #fig:dataflow}
The streamer data path from hub FIFO through the shifter to the pins — this caption must stay
welded to the diagram above it.
:::

```{=latex}
\clearpage
```

## 1.3 A Heading Immediately Followed by Code

```{=latex}
\begin{ExpectBox}
The code block below is forced near the page foot. It should stay with the heading above it.
THE DEFECT: the heading is left stranded at the bottom while the listing jumps to the next page.
\end{ExpectBox}
\leavebottom{1.0in}
```

```spin2
PUB main() | x
  pinstart(BASE_PIN, P_NCO_FREQ, FREQ_WORD, 0)
  repeat
    x := getrnd()
    wypin(BASE_PIN, x)
    waitms(10)
```

```{=latex}
\clearpage
```

## 1.4 Deep Nesting

```{=latex}
\begin{ExpectBox}
The subsection and sub-subsection below are forced toward the page foot. EXPECT: each nested
heading keeps at least its first body line on its own page. THE DEFECT: a deeply-nested heading
(\#\#\# or \#\#\#\#) strands alone at the bottom while its body begins on the next page.
\end{ExpectBox}
\leavebottom{1.1in}
```

Section text introduces the nested headings that follow.

### 1.4.1 A Subsection

Subsection body text, long enough to be ordinary content rather than a stub, so the heading above
it and the deeper heading below it both have real material to bind to.

#### 1.4.1.1 A Subsubsection

Subsubsection body text. The deepest heading level should still hold to its following text and
never strand at a page foot.

## 1.5 A Heading That Is Quite Long and Therefore Wraps Onto a Second Line in the Layout

```{=latex}
\begin{VerifiedBox}
The heading just above is long enough to wrap onto a second line. The wrapped heading keeps
consistent spacing above and below and binds to the paragraph beneath it --- no uneven
inter-line spacing, no detachment. Verified in the v6 render.
\end{VerifiedBox}
```

A heading that wraps to two lines must keep consistent spacing above and below and must still bind
to the paragraph beneath it, like this one.

# Chapter 2: Code Blocks at Boundaries

Code is the bulk of our real manuals, so it gets its own chapter: a listing that must split
across a page, a listing whose lines are wider than the box, and a short listing at a page foot.

```{=latex}
\clearpage
```

## 2.1 A Listing That Must Split Across a Page

```{=latex}
\begin{VerifiedBox}
The listing below is forced to begin near the page foot, so it spans onto the next page. The colored
code box breaks cleanly and signposts the span the way a continued table does --- a ``continues on
next page'' marker in the footer where it breaks and a ``continued from previous page'' marker in the
header where it resumes, with the box border and background intact on both parts. Verified in the v21
render: the breakable styled boxes now carry continuation markers (standard C10).
\end{VerifiedBox}
\leavebottom{1.5in}
```

```pasm2
        org     0
init    setxfrq ##FREQ              ' set NCO frequency for the streamer
        wrpin   ##P_NCO_FREQ, #BASE ' configure smart pin
        wxpin   ##1, #BASE
        dirh    #BASE
        rdfast  #0, ptra            ' point FIFO at the source buffer
        xinit   ##X_RFLONG_32P, #0  ' begin streaming, 32 pins per transfer
.loop   xcont   m_rf, #0            ' stream one block of data
        testb   ina, #STATUS  wc    ' sample a status pin into C
   if_c jmp     #.fault             ' branch out on fault
        djnz    count, #.loop       ' repeat until the block count is zero
        xstop                       ' halt the streamer
        ret
.fault  drvl    #BASE               ' drive the pin low on fault
        getct   timestamp           ' record the fault time
        wrlong  timestamp, ptrb     ' log it to hub
        jmp     #recover
recover mov     count, ##BLOCKS     ' reload the block counter
        rdfast  #0, ptra            ' re-point the FIFO
        xinit   ##X_RFLONG_32P, #0  ' restart the stream
        jmp     #.loop
```

```{=latex}
\clearpage
```

## 2.2 Code Lines Too Long for the Box (the column budget)

```{=latex}
\begin{ProcessBox}
Code boxes do NOT wrap. A typeset wrap cannot break a comment and re-indent it, nor insert the
language's line continuation for a split statement, so it would render wrong-looking code AND hide
the problem. Instead, the box has a column budget K --- the widest code line it holds. Read K off the
ruler below: it is the last column still inside the box before the text spills past the right edge.
K is recorded in each manual's creation-guide; the prepare-manual line-length audit flags any source
line longer than K; the author shortens it (break the comment and re-indent, or continue the
statement). The two demo lines further below are deliberately over-length --- they overflow here on
purpose, and double as the audit's self-test fixture.
\end{ProcessBox}
```

The column ruler (tens row, units row, then exact-length end markers). The box's right edge falls
between two of the labelled markers --- the largest marker still fully inside the box is K:

```pasm2
         1         2         3         4         5         6         7         8         9         0
1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
col 76 --------------------------------------------------------------------|
col 78 ----------------------------------------------------------------------|
col 80 ------------------------------------------------------------------------|
col 82 --------------------------------------------------------------------------|
col 84 ----------------------------------------------------------------------------|
col 86 ------------------------------------------------------------------------------|
col 88 --------------------------------------------------------------------------------|
col 90 ----------------------------------------------------------------------------------|
```

Deliberately over-length lines (these MUST overflow the box AND be flagged by the audit):

```pasm2
        rep     @.endrep, #16       ' this comment is deliberately extended well past the usual width to force the code line to exceed the printable text block and reveal how the code box handles overflow at the right edge
.endrep wrlong  value, ptra++       ' another very long trailing comment that keeps going and going so that the rendered line is unmistakably wider than the page text width and we can see exactly what happens
```

```{=latex}
\clearpage
```

## 2.3 A Code Block Pushed to the Page Foot

```{=latex}
\begin{VerifiedBox}
The short listing below is forced to the page foot. The whole code box stays together and moves
to the next page rather than being sheared by the boundary --- it is not split. Verified in the
v6/v8 render (the code box moved whole, intact).
\end{VerifiedBox}
\leavebottom{0.9in}
```

```spin2
PUB blink()
  repeat
    pintoggle(LED)
    waitms(250)
```

# Chapter 3: Lists, Quotes, and Boxed Content at Boundaries

## 3.1 A List That Must Split Across a Page

```{=latex}
\begin{VerifiedBox}
The numbered list below is forced to the page foot and splits across the boundary. It breaks
cleanly between items and continues with correct numbering on the next page --- no stranded item,
no restart, no mid-item break. Verified in the v6 render (items 1--5 then 6--10 across the break).
\end{VerifiedBox}
\leavebottom{1.2in}
```

1. Immediate modes drive the DACs directly from the command value.
2. RDFAST modes pull from the hub FIFO, paced by the NCO.
3. WRFAST modes capture pins back into the hub FIFO.
4. ADC modes sample analog inputs for scope and Goertzel work.
5. DDS and Goertzel modes drive a stimulus and accumulate a response.
6. The pass-through mode disables the streamer entirely.
7. Each mode is selected by a distinct command constant.
8. The NCO frequency sets the per-clock pacing for every mode.
9. Events let a cog resynchronise without polling.
10. The same command vocabulary covers output, input, and sampling.

```{=latex}
\clearpage
```

## 3.2 A Block Quote Forced to a Boundary

```{=latex}
\begin{ExpectBox}
The block quote below is forced near the page foot. EXPECT: the quote breaks cleanly between lines,
keeping its quote styling (indent / rule) consistent on both pages. THE DEFECT: the quote styling is
lost on the continuation, or a single quoted line strands alone at the boundary.
\end{ExpectBox}
\leavebottom{1.0in}
```

> The streamer is not a coprocessor and not an interrupt; it is a described transfer that the
> hardware carries out cycle-accurately while the cog moves on. Treat it as a contract: state the
> transfer once, then let the silicon keep time.

```{=latex}
\clearpage
```

## 3.3 A Boxed Formula Forced to a Boundary

```{=latex}
\begin{VerifiedBox}
The boxed formula below is forced to the page foot. The short box is kept whole --- pushed to the
next page rather than split, and it does not overrun the bottom margin. Verified in the v6/v8 render.
\end{VerifiedBox}
\leavebottom{0.7in}
```

```formula
NCO_phase(t+1) = (NCO_phase(t) + FREQ) mod 2^32
shift_trigger  = high_bits_of(NCO_phase)
```

# Chapter 4: Widows and Orphans in Prose

```{=latex}
\begin{VerifiedBox}
The paragraph below is forced to begin near the page foot so it must break across the boundary.
It keeps at least two lines on each side --- no single line is stranded (no orphan at the foot,
no widow at the top). Verified: the foundation now sets clubpenalty/widowpenalty = 10000.
\end{VerifiedBox}
\leavebottom{1.0in}
```

The streamer exists because the cog, fast as it is, cannot toggle pins quickly or regularly enough
for video timing or high-rate sampling on its own. A tight cog loop can move a datum every few
clocks, but the jitter from branch timing and the ceiling on loop speed both rule it out for a
250-megahertz pixel clock. The streamer removes the cog from the inner loop entirely: the cog
describes the transfer once, then the streamer carries it out cycle-accurately while the cog moves
on to other work. This is the same division of labour you see in a DMA controller, but specialised
for the rhythmic, pin-facing transfers a Propeller is built around. The final sentence is short.

# Part II: Table and Figure Torture

```{=latex}
\begin{VerifiedBox}
This second Part also has an introduction, confirming the part-intro fix works for EVERY part.
The ``Chapter 5'' heading sits cleanly below this intro --- no overlap, exactly as in Part I.
Verified.
\end{VerifiedBox}
```

This second part introduction confirms the part-intro-to-chapter flow works for *every* part, not
only the first. The chapters here stress table layout and figure placement.

# Chapter 5: Tables That Must Split

## 5.1 A Long Multi-Page Table

```{=latex}
\begin{VerifiedBox}
This table has 60+ rows --- far more than fit on one page. It breaks cleanly across pages, repeating
its header row at the top of each continuation page, so no rows are lost off the page bottom. Verified
in the v13 render: wide tables with many rows are now emitted as a breakable longtblr (with a repeating
header) instead of a non-breaking tblr.
\end{VerifiedBox}
```

| Mode | Command | Bits/Clock | Source | Destination | Notes |
|------|---------|-----------:|--------|-------------|-------|
| Immediate LUT | X_IMM_1X32_LUT | 32 | LUT | DAC/pins | one transfer per clock |
| Immediate 8b | X_IMM_8X1_1DAC8 | 1 | imm | DAC | fan-out |
| RFBYTE | X_RFBYTE_1P_1DAC8 | 8 | FIFO | DAC0 | paced by NCO |
| RFWORD | X_RFWORD_2P_2DAC8 | 16 | FIFO | DAC0–1 | dual channel |
| RFLONG | X_RFLONG_4P_4DAC8 | 32 | FIFO | DAC0–3 | quad channel |
| RFWORD RGB16 | X_RFWORD_RGB16 | 16 | FIFO | pins | 5-6-5 video |
| RFLONG RGB24 | X_RFLONG_RGB24 | 24 | FIFO | pins | 8-8-8 video |
| RFBYTE LUMA8 | X_RFBYTE_LUMA8 | 8 | FIFO | pins | luma only |
| WFBYTE | X_WRBYTE_1P | 8 | pins | FIFO | input capture |
| WFWORD | X_WRWORD_2P | 16 | pins | FIFO | dual input |
| WFLONG | X_WRLONG_4P | 32 | pins | FIFO | quad input |
| DDS/Goertzel | X_1P_1DAC1_WFBYTE | 1 | FIFO | DAC+ADC | sampling |
| ADC 8b | X_RFBYTE_1P_1ADC | 8 | ADC | FIFO | scope mode |
| Pins 1b | X_1ADC8_0P | 1 | ADC | FIFO | bit capture |
| Pins 2b | X_2ADC8_0P | 2 | ADC | FIFO | dual ADC |
| Pins 4b | X_4ADC8_0P | 4 | ADC | FIFO | quad ADC |
| RGB LUT8 | X_RFBYTE_RGBI8 | 8 | FIFO | pins | LUT palette |
| RGB LUT4 | X_RFBYTE_RGBI4 | 4 | FIFO | pins | 16-color |
| RGB LUT2 | X_RFBYTE_RGBI2 | 2 | FIFO | pins | 4-color |
| RGB LUT1 | X_RFBYTE_RGBI1 | 1 | FIFO | pins | mono |
| Immediate 16b | X_IMM_4X8_1DAC8 | 8 | imm | DAC | byte stream |
| Immediate 32b | X_IMM_2X16_2DAC8 | 16 | imm | DAC | word stream |
| RFBYTE 2DAC | X_RFBYTE_2P_2DAC8 | 8 | FIFO | DAC0–1 | stereo audio |
| RFWORD 4DAC | X_RFWORD_4P_4DAC8 | 16 | FIFO | DAC0–3 | four-channel |
| WFLONG 8P | X_WRLONG_8P | 32 | pins | FIFO | wide capture |
| RFLONG 16P | X_RFLONG_16P | 32 | FIFO | pins | wide output |
| RFLONG 32P | X_RFLONG_32P | 32 | FIFO | pins | full port |
| LUT RGB24 | X_LUT_RGB24 | 24 | LUT | pins | palette video |
| LUT RGB16 | X_LUT_RGB16 | 16 | LUT | pins | palette video |
| Pass-through | X_PINS_OFF | 0 | — | — | disabled |
| Immediate 1b | X_IMM_32X1_1DAC1 | 1 | imm | DAC | bit stream |
| Immediate 2b | X_IMM_16X2_2DAC1 | 2 | imm | DAC | pair stream |
| Immediate 4b | X_IMM_8X4_4DAC1 | 4 | imm | DAC | nibble stream |
| RFBYTE 4DAC | X_RFBYTE_4P_4DAC2 | 8 | FIFO | DAC0–3 | quad low-res |
| RFWORD LUMA | X_RFWORD_LUMA8 | 16 | FIFO | pins | wide luma |
| WFBYTE 2P | X_WRBYTE_2P | 8 | pins | FIFO | dual capture |
| WFWORD 4P | X_WRWORD_4P | 16 | pins | FIFO | quad capture |
| ADC 1x | X_1ADC8_1P | 8 | ADC | FIFO | single scope |
| ADC 2x | X_2ADC8_2P | 16 | ADC | FIFO | dual scope |
| ADC 4x | X_4ADC8_4P | 32 | ADC | FIFO | quad scope |
| DDS lo | X_1P_1DAC1_WFWORD | 1 | FIFO | DAC+ADC | low-rate DDS |
| DDS hi | X_1P_1DAC1_WFLONG | 1 | FIFO | DAC+ADC | high-rate DDS |
| RGB8 out | X_RFBYTE_RGB8 | 8 | FIFO | pins | 3-3-2 video |
| RGB4 out | X_RFBYTE_RGB4 | 4 | FIFO | pins | 16-color vid |
| LUMA4 out | X_RFBYTE_LUMA4 | 4 | FIFO | pins | low luma |
| LUMA2 out | X_RFBYTE_LUMA2 | 2 | FIFO | pins | 2-bit luma |
| LUMA1 out | X_RFBYTE_LUMA1 | 1 | FIFO | pins | mono luma |
| Imm DAC4 | X_IMM_4X8_4DAC8 | 32 | imm | DAC0–3 | quad imm |
| Imm DAC2 | X_IMM_8X4_2DAC8 | 16 | imm | DAC0–1 | dual imm |
| RF nibble | X_RFBYTE_RGBI4b | 4 | FIFO | pins | palette4 |
| RF crumb | X_RFBYTE_RGBI2b | 2 | FIFO | pins | palette2 |
| RF bit | X_RFBYTE_RGBI1b | 1 | FIFO | pins | palette1 |
| WF nibble | X_WRBYTE_4P | 8 | pins | FIFO | quad capture |
| WF crumb | X_WRBYTE_8P | 8 | pins | FIFO | octal capture |
| Scope 8 | X_RFBYTE_1P_1ADCb | 8 | ADC | FIFO | scope basic |
| Scope 16 | X_RFWORD_2P_2ADC | 16 | ADC | FIFO | scope wide |
| Scope 32 | X_RFLONG_4P_4ADC | 32 | ADC | FIFO | scope full |
| Goertzel 1 | X_1P_1DAC1_GOERTZEL | 1 | FIFO | DAC+ADC | tone detect |
| Goertzel 2 | X_2P_2DAC1_GOERTZEL | 2 | FIFO | DAC+ADC | dual tone |
| Pass A | X_PINS_OFF_A | 0 | — | — | disabled A |
| Pass B | X_PINS_OFF_B | 0 | — | — | disabled B |

```{=latex}
\clearpage
```

## 5.2 A Table Forced to a Boundary

```{=latex}
\begin{VerifiedBox}
The small table below is forced to the page foot. It is kept whole --- pushed to the next page
rather than split through the middle of a row, with its header intact. Verified in the v6/v8 render
(table moved whole to the next page).
\end{VerifiedBox}
\leavebottom{0.8in}
```

| Field | Width | Meaning |
|-------|------:|---------|
| EEEE | 4 | condition |
| Opcode | 7 | instruction |
| CZI | 3 | flag controls |
| D | 9 | destination |
| S | 9 | source |

```{=latex}
\clearpage
```

## 5.3 A Table With a Caption

```{=latex}
\begin{ExpectBox}
The captioned table below is forced near the page foot. EXPECT: the caption stays welded to its
table — both move together to the next page if they do not fit. THE DEFECT: the caption detaches
from the table, or lands on a different page from the rows it describes.
\end{ExpectBox}
\leavebottom{0.9in}
```

Table: Streamer event sources and the instructions that clear them.

| Event | Source | Cleared by |
|-------|--------|-----------|
| XFI | FIFO empty | RDFAST |
| XMT | block done | XCONT |
| XRL | accumulation | XINIT |

# Chapter 6: Tables That Overflow the Page Width

## 6.1 Many Wide Columns

```{=latex}
\begin{VerifiedBox}
This table has ten columns, several carrying wide text. It fits the page width: each column is given
a token-fit width and the whole table is shrunk to a small font, with the prose cells wrapping inside
their columns. No columns are written on top of each other. Verified in the v20 render: many-column
tables are now routed to the token-fit width allocator (with a small-font tier) instead of falling to
pandoc's narrow defaults.
\end{VerifiedBox}
```

| Mode | Mnemonic | Bits/Clk | DAC Channels | Pin Group | NCO Source | Event Raised | Typical Application | Companion Instruction | Reset Behavior |
|------|----------|---------|--------------|-----------|------------|--------------|---------------------|-----------------------|----------------|
| RGB24 video output | X_RFLONG_RGB24 | 24 | DAC0–DAC3 differential | pins 0–31 selectable | XFRQ accumulator high bits | XFI on buffer empty | HDMI and VGA framebuffer scan-out | SETXFRQ before XINIT | clears on XINIT reload |
| ADC scope sampling | X_RFBYTE_1P_1ADC | 8 | single DAC feedback | pins 8–15 group | XFRQ paced sample clock | XMT on block done | oscilloscope capture front-end | RDFAST to stage buffer | continues across XCONT |
| Goertzel tone detect | X_1P_1DAC1_WFBYTE | 1 | DAC0 stimulus only | pin 0 stimulus + sense | XFRQ sets bin frequency | XRL on accumulation | single-frequency lock-in detection | SETSE for sense routing | accumulators zeroed on reload |

## 6.2 Long Unbreakable Tokens in a Narrow Column

```{=latex}
\begin{VerifiedBox}
The left column is narrow; the symbols in it are long and have no spaces to wrap on. The column
widens to fit its longest symbol --- the symbol is never split, and it no longer runs out of its
column or overlaps the description to its right. Verified in the v20 render: the symbol/description
width allocator now sizes column 1 to its longest unbreakable token (capped so the description keeps
a readable half).
\end{VerifiedBox}
```

| Symbol | Description |
|--------|-------------|
| X_RFLONG_32P_4DAC8_DIFFERENTIAL | a deliberately long constant name with no natural break points |
| P_OE_FLOAT_LOW_1K5_PULLUP_FILTER | another long symbol that cannot wrap on spaces |
| EVENT_STREAMER_FIFO_EMPTY_INT1 | a long event-source symbol |

```{=latex}
\clearpage
```

## 6.3 An Oversized Tall Table

```{=latex}
\begin{VerifiedBox}
The tall table below is forced to the page foot. It moves whole to the next page rather than running
off the bottom margin --- one of the two acceptable outcomes (move-whole, or break with a repeated
header). Verified in the v6/v8 render (table moved whole to the next page).
\end{VerifiedBox}
\leavebottom{1.2in}
```

| Pin | Function | Default |
|----:|----------|---------|
| 0 | DAC0 / streamer out | input |
| 1 | DAC1 / streamer out | input |
| 2 | DAC2 / streamer out | input |
| 3 | DAC3 / streamer out | input |
| 4 | Smart pin A | input |
| 5 | Smart pin B | input |
| 6 | Serial TX | input |
| 7 | Serial RX | input |
| 8 | ADC0 | input |
| 9 | ADC1 | input |
| 10 | ADC2 | input |
| 11 | ADC3 | input |
| 12 | HDMI clk+ | input |
| 13 | HDMI clk- | input |
| 14 | HDMI d0+ | input |
| 15 | HDMI d0- | input |

# Chapter 7: Figures at Boundaries

## 7.1 A Diagram Forced to a Boundary

```{=latex}
\begin{VerifiedBox}
The diagram below is forced near the page foot. Because it is an unbreakable [H] figure that cannot
fit in the space left at the foot, the page breaks before it and the whole diagram --- with its
caption --- moves to the next page rather than overrunning the bottom margin. Verified in the v21
render (VGA timing diagram + caption together at the top of the following page, nothing off-page).
\end{VerifiedBox}
\leavebottom{1.5in}
```

```{=latex}
\DiagVgaTiming
```

::: {.figurecaption #fig:vga}
VGA timing relationships produced by the streamer and NCO.
:::

```{=latex}
\clearpage
```

## 7.2 A Figure With a Long Caption at a Boundary

```{=latex}
\begin{VerifiedBox}
The figure below is forced to the page foot and its caption is several lines long. The diagram and
its full caption stay welded together --- the caption does not detach and does not split across the
boundary. Verified in the v6 render (figure + multi-line caption together at the foot of the page).
\end{VerifiedBox}
\leavebottom[0.32\textheight]{1.8in}
```

```{=latex}
\DiagCommandWord
```

::: {.figurecaption #fig:cmdword}
The streamer command, field by field: the mode selector chooses the transfer class, the DAC and
pin-group fields route the data, and the size field sets how many bits move per clock. This caption
is deliberately long enough to wrap to several lines so we can confirm a multi-line caption stays
bound to its figure and does not detach across a page boundary.
:::

```{=latex}
\clearpage
```

## 7.3 Two Figures Competing for One Boundary

```{=latex}
\begin{VerifiedBox}
Two diagrams sit back to back, forced near a page foot. The first stays on this page and the
second moves to the next, each with its caption intact --- neither overruns the margin and no
caption detaches. Verified in the v6 render (first figure on this page, second on the next).
\end{VerifiedBox}
\leavebottom[0.32\textheight]{2.2in}
```

```{=latex}
\DiagNcoRollover
```

::: {.figurecaption #fig:nco}
NCO phase rollover and the shift trigger it generates.
:::

```{=latex}
\DiagRgbFormats
```

::: {.figurecaption #fig:rgb}
RGB packing formats for the video output modes.
:::

# Part III: Boxes, Whitespace, and Pagination

```{=latex}
\begin{VerifiedBox}
This third Part also has an introduction, so the part-intro-to-chapter flow (B4) and the
"first chapter shares the Part's page" rule (A2) are checked a third time. The ``Chapter 8''
heading sits cleanly below this intro, ON THIS PAGE --- no overlap, not pushed to a fresh page.
Verified (A2 + B4).
\end{VerifiedBox}
```

This third part stresses the styled-box family — colored callout boxes — plus the central
whitespace-tolerance trade-off and the chapter/part pagination rules themselves.

# Chapter 8: Callout Boxes at Boundaries

Our manuals lean on colored callout boxes (tip, antipattern, sidetrack). They are styled
`tcolorbox`es just like code blocks, so they face the same boundary problems: a long one must
span a page cleanly, and a short one must not be split needlessly.

## 8.1 A Long Callout That Must Span a Page

```{=latex}
\clearpage
\begin{VerifiedBox}
This colored callout is long and is forced to begin near the page foot, so it spans onto the next
page. It splits cleanly and signposts the span like a continued table --- a ``continues on next
page'' marker in the footer where it breaks and a ``continued from previous page'' marker in the
header where it resumes, the colored fill and border intact on both parts. Verified in the v21
render: callout boxes share the same continuation-marker standard as code boxes (C11 = C10 = C9).
\end{VerifiedBox}
\leavebottom{1.5in}
```

```{=latex}
\begin{AntipatternBlock}
```

**Antipattern — assuming the streamer survives a reconfiguration.** A common mistake is to treat
the streamer as a fire-and-forget engine that keeps running across changes to the NCO frequency,
the pin routing, or the command word. It does not. Any change to the transfer description must be
followed by a fresh command word, or the streamer continues with the *old* description and the
output silently diverges from what the code intends.

This callout is deliberately long so that, when forced toward the page foot, it cannot fit and must
span the boundary — exercising exactly the same continuation problem we have for code blocks and
tables. Watch the break: the box should carry a footer marker on the page where it breaks and a
header marker where it resumes, and the colored frame and background must be unbroken on both
pages. The reader must never be left guessing whether two coloured bands on facing pages are one
box or two.

A final paragraph of ballast so the box is unambiguously taller than the space left at the foot of
the page, guaranteeing the span occurs rather than the whole box simply moving to the next page.

```{=latex}
\end{AntipatternBlock}
```

## 8.2 A Short Callout Forced to a Boundary

```{=latex}
\clearpage
\begin{VerifiedBox}
This short callout is forced to the page foot. The short box is kept whole --- pushed to the next
page as a single unit rather than split through the middle. Verified in the v6/v8 render.
\end{VerifiedBox}
\leavebottom{0.8in}
```

```{=latex}
\begin{AntipatternBlock}
```

**Antipattern — forgetting to re-issue the command word.** After any reconfiguration, re-issue the
streamer command word before relying on the output. This box is deliberately short, so it should
move to the next page whole rather than split.

```{=latex}
\end{AntipatternBlock}
```

# Chapter 9: Whitespace Tolerance and Pagination Rules

```{=latex}
\begin{VerifiedBox}
This chapter began on a FRESH page --- normal chapters break to a new page (rule A3), and this
one did, cleanly, before the chapter title. (Contrast A2: only the FIRST chapter after a Part
shares the Part's page; every other chapter, including this one, starts fresh.) Verified.
\end{VerifiedBox}
```

This chapter isolates the trade-off the whole effort exists to resolve: how much blank space we
will tolerate at a page foot in order to avoid splitting a small logical unit (A1 vs C5/C7).

## 9.1 A Keep-Together Unit That Leaves a Tail Blank

```{=latex}
\clearpage
\begin{ExpectBox}
The unit below (a subheading, a short paragraph, and a small table) is forced toward the page foot.
It is kept together, so when it cannot fit it moves WHOLE to the next page — leaving a blank "tail"
at the foot of this page. EXPECT (A1 vs C5/C7): that tail blank must be WITHIN TOLERANCE — a small,
acceptable gap around the central whitespace knob — NOT a large wasteful empty band. THE DEFECT:
either the unit splits (keep-together failed, C5/C7) OR the tail blank is excessive (A1 violated).
This case exercises the whitespace-tolerance threshold directly; tune the knob until the tail is
acceptable.
\end{ExpectBox}
\leavebottom{0.5in}
```

### 9.1.1 A Small Keep-Together Unit

This subheading, this paragraph, and the small table below it form one logical unit that should not
be split. When forced near the page foot it should move to the next page as a whole, and the gap it
leaves behind must stay within the tolerated whitespace budget rather than yawning open.

| Phase | Action | Result |
|-------|--------|--------|
| setup | issue command word | streamer armed |
| run | XCONT per block | data moves |
| stop | XSTOP | streamer idle |

```{=latex}
\clearpage
\begin{ExpectBox}
End of the torture cases. Every case above is labeled with its own EXPECT box. Compare each box to
what actually rendered just below it; the goal is a version of this document where every EXPECT box
is satisfied. At that point the underlying rule changes are ready to port to the live manuals.
\end{ExpectBox}
```

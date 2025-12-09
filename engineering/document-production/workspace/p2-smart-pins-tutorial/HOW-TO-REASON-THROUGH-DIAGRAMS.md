# How to Reason Through Diagrams

**Purpose:** Reference guide for systematically analyzing and recreating timing diagrams and block diagrams in TikZ. Read this document before starting work on any new diagram.

**Document:** P2 Smart Pins Tutorial (Green Book)

---

## Core Principle

**Analyze completely before writing any code.** The goal is to reduce iteration cycles by catching errors at the specification stage rather than after rendering.

---

## Diagram Types and What to Look For

### Timing Diagrams (Waveforms)

Timing diagrams show signal relationships over time. Key aspects:

#### 1. Signal Characteristics (Per Signal Line)

For EACH signal line, systematically extract:

| Attribute | What to Check |
|-----------|---------------|
| **Label** | Exact text, position (usually left-aligned) |
| **Level indicators** | "1"/"0" markers near the signal |
| **Lead-in state** | What level does the signal START at? |
| **Lead-out state** | What level does the signal END at? (often dashed continuation) |
| **Shape** | Square wave, sawtooth, triangle, stepped/dashed counter |
| **Polarity** | HIGH-going pulses on LOW baseline, or LOW-going dips on HIGH baseline? |
| **Transition count** | Exact number of rising and falling edges |
| **Waveform details** | For counters: dashed steps vs solid lines |

#### 2. Phase Relationships (CRITICAL)

Edges are deeply important. Look for:

- Which edges on different signals are **vertically aligned/coincident**?
- What causes what? (e.g., threshold crossing causes output transition)
- Document each alignment explicitly: "Signal A rising edge coincident with Signal B falling edge"

#### 3. Vertical Reference Lines

Dotted/dashed vertical lines typically show:
- Causality between signals (edge on one signal causes change on another)
- Measurement points for timing annotations

Note: Which edges they connect, and in which direction they flow.

#### 4. Sawtooth/Counter Waveforms

Special considerations:
- **Stepped appearance:** Small horizontal dashes (not solid diagonal lines)
- **Vertical drops:** Some have them, some DON'T (visually disconnected frames)
- **Frame definition:** Valley-to-valley? Peak-to-peak? Document which.
- **Threshold crossings:** Where does the sawtooth cross a threshold line?

---

### Block Diagrams (Data Flow)

Block diagrams show functional relationships. Key aspects:

#### 1. Block Inventory

List every block with:
- Label text
- Approximate size/shape
- Position in diagram

#### 2. Connection Analysis (CRITICAL for Visual Balance)

For EACH block edge (top, bottom, left, right):
- How many arrows enter/exit this edge?
- Arrows on same edge must be **evenly spaced and centered**

**Rules:**
- 1 arrow on edge → centered on that edge
- 2 arrows on edge → evenly spaced, centered as a pair
- 3+ arrows → evenly distributed across edge

#### 3. Arrow Characteristics

- **Direction:** Which way does data flow?
- **Stem length:** Arrows need visible stems, not just arrowheads touching boxes
- **Whitespace:** Space between arrow and what it points to/from

---

## Annotations and Dimensions

### Dimension Lines (e.g., "5.1 usec")

- **Arrow direction:** Inward-pointing or outward-pointing?
- **Label position:** Inside the arrows, outside to left, outside to right?
- **Whitespace:** Gap between label and arrows, gap between arrows and measured edges

### Register/Value Annotations (e.g., "X[31:16] = $200")

- **Color coding:** Often register name in blue, value in black
- **Arrow direction:** Which way does annotation arrow point?
- **Position:** Left of target? Right of target? Above/below?
- **Whitespace:** Gaps between text, arrow, and target

### Threshold Lines

- Horizontal lines showing comparison levels
- Often dashed
- Label indicates register/value being compared

### Arrow Style Requirements

**Use thin-line solid arrowheads throughout:**
- TikZ style: `>=Stealth` with `thin` line weight
- NOT: thick arrows, hollow arrows, or latex default arrows
- Arrowheads should be small and unobtrusive

**Annotation arrows must be HORIZONTAL:**
- Arrows pointing from labels to waveform features (peaks, valleys, edges) must be horizontal
- Do NOT angle arrows diagonally to reach targets
- If vertical adjustment is needed, position the label at the correct Y-level first

**Arrow direction for annotations:**
- Label → Target: Arrow points FROM label TO the thing being referenced
- Verify: "X[31:16] = $200" arrow points toward the sawtooth peak, not away from it

---

## Visual Spacing and Proportions

### Vertical Spacing

Look at the reference image and note the relative vertical distances between:
- Signal baselines (0-levels)
- Different signal groups
- Annotation areas
- Time axis

**Match these proportions** - they affect readability.

### Left-Edge Alignment

Labels on the left side of timing diagrams are typically **right-aligned**:
- "IN" right edge
- "P20 Output" right edge
- "Y[15:0] = $0080" right edge

All should align to the same vertical position.

### Left Vertical Reference Line

Some diagrams have an explicit vertical line at the left edge:
- Note where it starts (mid-signal? top?)
- Note where it ends (below time axis?)
- Note what it intersects

---

## Pre-Generation Checklist

Before writing TikZ code, verify you can answer:

### For Each Signal:
- [ ] What is the exact label text?
- [ ] What is the lead-in state?
- [ ] What is the lead-out state?
- [ ] How many transitions occur?
- [ ] What is the waveform shape/style?

### For Phase Relationships:
- [ ] Which edges align with which other edges?
- [ ] What vertical reference lines exist?
- [ ] What do those reference lines connect?

### For Annotations:
- [ ] What dimension lines exist?
- [ ] What register/value annotations exist?
- [ ] What is the exact color coding?
- [ ] Where is whitespace required?

### For Layout:
- [ ] What are the vertical spacing proportions?
- [ ] What left-edge alignment is required?
- [ ] Does a left vertical reference line exist?

---

## Common Mistakes to Avoid

1. **Inverted polarity:** Mistaking HIGH baseline with LOW dips for LOW baseline with HIGH pulses
2. **Wrong transition count:** Missing edges or adding extras
3. **Misaligned phases:** Edges that should be coincident are offset
4. **Insufficient arrow stems:** Arrowheads touching boxes with no visible line
5. **Uncentered connections:** Multiple arrows on one block edge not evenly spaced
6. **Missing whitespace:** Annotations crowded against targets
7. **Wrong lead-in/lead-out:** Signal starts or ends at wrong level
8. **Solid vs dashed:** Using solid lines for counter waveforms that should be stepped
9. **Angled annotation arrows:** Reference arrows pointing to waveform features should be HORIZONTAL, not angled
10. **Label overlap with signal levels:** Signal name labels and 0/1 level indicators must not overlap - separate them clearly
11. **Missing baseline references:** Sawtooth/counter waveforms often need a horizontal baseline a few pixels below the waveform itself
12. **Text overlapping lines:** Labels must NEVER overlap with arrows, dimension lines, or axis lines - always clear separation
13. **Wrong arrow style:** Use thin-line solid arrowheads (Stealth), not thick/hollow arrow forms
14. **Compressed vertical space:** Waveforms need sufficient vertical height for clarity - especially sawtooth/counter waveforms
15. **Time axis too prominent:** Time axis label should be smaller/subordinate, not competing with diagram content

---

## Self-Review Before Human Review (MANDATORY)

**After generating any diagram, ALWAYS view the rendered thumbnail and check for issues BEFORE asking the human to review.**

### Visual Crowding Checklist

Inspect the rendered output for these problems:

1. **Label/element overlap** - Do any labels touch or overlap other elements?
2. **Insufficient whitespace** - Is there clear separation between all elements?
3. **Labels crowding edges** - Are signal labels too close to rising/falling edges?
4. **Annotation interference** - Do annotations (CW/CCW, dimension labels) overlap waveforms or other annotations?
5. **Arc/circle positioning** - Are curved arrows clear of nearby text and waveforms?

### Self-Correction Process

1. Submit test request to PDF Forge
2. **Wait for and view the thumbnail** - Do not proceed without visual inspection
3. Identify any crowding or overlap issues
4. Fix the issues in the template
5. Re-submit and re-check
6. Only present to human when the diagram is visually clean

**Do NOT ask the human to review a diagram that has obvious visual problems you can see and fix yourself.**

---

## Iteration Process

When feedback indicates problems:

1. **Identify the specific issue** (polarity? alignment? spacing?)
2. **Trace back to analysis** - was this captured correctly in pre-analysis?
3. **If analysis was wrong:** Correct understanding first, then fix code
4. **If analysis was right but code wrong:** Fix the TikZ implementation
5. **Update this document** if a new pattern/principle is discovered

---

## Technical Notes

### LaTeX Macro Naming

**CRITICAL:** LaTeX macro names can only contain letters. Numbers break parsing.

- ❌ `\pulse1rise` - LaTeX sees `\pulse` + `1rise`
- ❌ `\p20High` - LaTeX sees `\p` + `20High`
- ✅ `\pulseArise` - Use letters only
- ✅ `\outHigh` - Use descriptive letter-only names

### Consistent Endpoints

Define a single `\waveend` coordinate for where solid lines end and dashed continuations begin. Use this for:
- All signal waveforms
- Baseline horizontal lines
- Frame period arrow dotted continuation

This ensures visual consistency across the diagram.

### Vertical Reference Lines

**Left edge vertical line:**
- Typically starts at mid-height of a signal (e.g., P20 Output)
- Extends down past the time axis
- Marks the diagram's left boundary

**Dotted drop lines from signal edges:**
- Connect signal transitions to related features below
- May need to extend through multiple levels (crossing arrows, reaching valleys)
- Should stop just before touching the target (whitespace gap)

---

## Lessons Learned Log

### 2025-12-09: SawtoothPWMDiagram

**Iterations required:** 7 (v1-v7)

**Key issues encountered:**
1. LaTeX macro naming (numbers in names)
2. Arrow direction confusion (FROM label TO target, not reverse)
3. Label/level indicator overlap - need separate X positions
4. Angled arrows instead of horizontal
5. Missing baseline reference line
6. Vertical spacing too compressed initially
7. Text overlapping with dimension lines
8. Dotted reference lines not extending far enough

**What the pre-analysis missed:**
- Detailed vertical spacing proportions
- Exact extent of vertical reference lines
- Baseline requirement below sawtooth
- Arrow direction semantics (label→target)

### 2025-12-09: QuadEncoderDiagram (v1-v9)

**Iterations required:** 9

**Key issues encountered:**
1. **ALL FOUR WAVEFORMS POLARITY INVERTED** - Drew HIGH baseline with LOW dips instead of LOW baseline with HIGH pulses
2. Schematic: Only drew 2 pins instead of 3 (middle pin goes to ground)
3. Pulse timing: Drew evenly spaced pulses instead of paired pulses (2 close, gap, 1 isolated)
4. Label positioning: Labels should be at mid-height with LOW level BELOW the label baseline
5. Arc/label overlap: CW/CCW curved arrows not centered relative to their labels
6. Removed unnecessary up/down arrows annotation
7. Labels crowding rising edges - needed multiple iterations to shift labels left enough
8. CW/CCW arc positioning - needed to center arc radius on P32 baseline
9. CCW arrow direction was backwards initially
10. **Failed to self-review thumbnails** - made unnecessary iterations by not checking rendered output

**Critical lesson - POLARITY DETERMINATION:**
When analyzing a waveform, ask these questions IN ORDER:
1. **Where does the signal START?** (lead-in state)
2. **Where does the signal END?** (lead-out state)
3. **Where is the LABEL positioned vertically?** (usually at mid-height)
4. **Is the active portion ABOVE or BELOW the label?**

If lead-in is LOW and lead-out is LOW → LOW baseline, HIGH pulses going UP
If lead-in is HIGH and lead-out is HIGH → HIGH baseline, LOW dips going DOWN

**The reference image showed:**
- P32/P33 labels at mid-height
- Signals starting LOW, ending LOW
- Active pulses going UP above the label level
- Therefore: LOW baseline with HIGH pulses (NOT HIGH baseline with LOW dips)

**What the pre-analysis missed:**
- Systematic polarity determination method
- Detailed pulse timing pattern (2+1 grouping, not uniform)
- Third encoder pin for ground connection
- Label vertical positioning relative to signal levels

---

*Created: 2025-12-09*
*Updated: 2025-12-09 - Added lessons from QuadEncoderDiagram polarity errors*
*Purpose: Reduce diagram iteration cycles through systematic pre-analysis*

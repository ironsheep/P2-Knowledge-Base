# Manual Layout — User Preferences & Known Defects

**Status:** Authority document for our house style
**Companion to:** `manual-layout-standards-INPUTS.md` (external-agent suggestions)
**Purpose:** Capture what **we** deliberately want for the documents we produce — including
where we intentionally depart from print tradition — and the specific layout defects we see
today. When we analyze the external inputs, **this document is the authority.** External
"standards" get adopted only where they serve these preferences; where they conflict, our
preferences win.

**Core framing (from the user):** We want to *augment* our current style, not work against it.
Our documents are PDFs that users **scroll through quickly**, not printed books read page by
page. That changes some traditional rules — most notably, we do not want large blank/empty
page areas just to honor print pagination conventions.

---

## Governing principle — automatic by default, manual override as the exception

The single most important design constraint across everything below:

**We want placement decisions made automatically by general rules, not by hand-tuning
individual elements.** The system should put headings, logical blocks, figures, captions, and
tables in the right place by default — driven by rules encoded once (in the template / preamble /
filters) that apply to *every* element of that kind. Manual correction is allowed, but only as a
**sparing escape hatch for the specific instance the automatic rules get wrong** — never as the
normal workflow.

What this explicitly rejects:
- Hand-placing `\needspace` / `\newpage` / `\pagebreak` before specific figures, headings, or
  tables as the routine way to fix splits. That per-element babysitting is exactly what we are
  fighting against today.
- Any "solution" that requires the author to anticipate and annotate each element that might
  break badly.

What this requires:
- General, document-wide rules that fire automatically for all headings, blocks, and tables.
- A clean, **sparing** override syntax for the rare exception — used only when the automatic
  result is genuinely wrong, not as standard practice.

### The central tension this principle has to manage (automatically)

Two of our goals pull in opposite directions:
- **A#1** (minimize blank/empty page areas — because the PDF is scrolled quickly), versus
- **C#5 / C#7** (don't strand headings; keep logical blocks together).

The traditional fixes for stranding and block-splitting work *by pushing content to the next
page*, which can create exactly the blank areas A#1 wants to avoid. The hard design problem is
therefore **how much whitespace we will automatically tolerate to prevent a bad split** — and
that threshold must itself be a general, tunable rule, not a per-element judgment call. Resolving
this trade-off (rather than picking one side) is the core of the recommendation we will produce.

---

## A. Intentional current style — PRESERVE these

These are deliberate choices. They may contradict traditional hardcopy guidance; that is fine
and intended. Any external recommendation that would undo one of these is **rejected by default**
unless we explicitly decide otherwise.

1. **Minimize blank/empty page areas.** Because the PDF is scrolled quickly, we avoid leaving
   significant empty regions on a page. We do not insert blank pages or large gaps just to make
   the next element start on a "fresh" page in the print-tradition sense.

2. **First chapter after a Part shares the Part's page.** The first chapter following a Part
   heading **continues on the same page** as the part — we explicitly reject the tradition of a
   standalone Part page followed by the first chapter beginning on a separate later page.

3. **Chapters break to a new page — except after a Part.** Normal chapters start on a new page.
   The one exception is a chapter that immediately follows a Part heading (see #2), which stays
   on the part's page.

---

## B. Desired feature — want it; tried it; it broke

4. **Part introduction that flows into the first chapter heading — without overlap.**
   We want to support a **Part introduction** (one or more paragraphs after the Part heading),
   and then flow the **first chapter heading** after that introduction, on the same page when it
   fits (consistent with A#2/A#3).

   - **What broke:** when we attempted this, the **chapter heading overlapped the Part
     introduction paragraph** — the heading was placed on top of / colliding with the intro text.
     Because it rendered broken, we **reverted** it.
   - **Requirement:** the part-intro + first-chapter-heading must behave as a proper vertical
     flow with correct spacing and keep-together behavior — the heading must follow the intro
     text, never collide with it. If there isn't room for the heading plus some following body,
     it should move as a unit rather than overlap.

---

## C. Known defects — happening today, want fixed

5. **Orphaned titles at page bottom.** Headings are being left stranded at the bottom of a page
   with no (or insufficient) body text following them on the same page.

6. **Tables not splitting correctly / tables too large.** Some tables fail to split properly
   across pages; some simply grow too large to place well.

7. **Logical block splitting across pages.** A unit that should stay together —
   **heading → intro paragraph → diagram → caption** — sometimes fragments across a page
   boundary (e.g., diagram on one page, caption on the next; or heading separated from its
   following content).

8. **Table width overflow → overlapping, unreadable text.** When a table has columns that are
   too wide, or simply too many columns, it does not lay out cleanly across the page width.
   The failure mode is severe: **columns physically overlap and the rendered text is written on
   top of itself, becoming unreadable.** This is a hard correctness failure, not just an
   aesthetic one.

9. **No standard for table page-splitting (format + detection).** In at least one case we worked
   hard to split a long table correctly — repeating the header row on the continuation page and
   marking the prior page's table as "continued." But:
   - We have **no standard format** for how a continued/split table should look
     (repeated header, "(continued)" marker, where it goes).
   - We have **no standard detection** for *when* a table needs this treatment.
   We need both: a reusable, consistent split format **and** a reliable way to detect/trigger it.

10. **No standard for CODE-BLOCK page-spanning (format + detection).** The code-block analogue of
    C9. A listing too long for one page must be allowed to span — and when it does, the break must
    be **signposted the same way a continued table is**: a continuation marker in the **footer** of
    the breaking page ("listing continues…") and one in the **header** of the continuation
    ("…listing continued"), with the colored box border and background intact on both parts.
    **Today we do neither** — a long listing splits silently (no signpost) or breaks badly. We need
    the format AND the detection.

11. **Callout/admonition boxes — length policy + page-spanning.** Our manuals use colored callout
    boxes (tip / antipattern / sidetrack / note), which are styled `tcolorbox`es just like code.
    Two items:
    - **Policy (UNDECIDED):** do we **keep callouts short** so they never need to span a page, or
      do we **allow long callouts**? We have not made this call. It drives everything below.
    - **If long callouts are allowed**, they inherit the C10/C9 spanning requirement: split cleanly
      with footer/header continuation markers and intact styling. **If kept short**, the rule
      becomes "a callout that won't fit moves whole to the next page, never splits" — which needs
      its own detection (how short is short enough, and what happens when one exceeds it).

### One shared continuation-marker standard (C9 + C10 + C11)

Tables (C9), code blocks (C10), and callouts (C11) all describe the *same* underlying need: a
single, reusable **"block continues / block continued"** signpost applied wherever a styled block
spans a page, plus reliable detection of when to trigger it. The recommendation must define this
**once** and apply it across all three — not three ad-hoc treatments. (Tables already have a
partial version; code and callouts have none.)

---

## How this document is used

During analysis of `manual-layout-standards-INPUTS.md`, evaluate each external suggestion
against the items above:

- Does it **serve** a desired feature (B) or **fix** a known defect (C)? → candidate to adopt/adapt.
- Does it **conflict** with an intentional choice (A)? → reject, or adapt so it respects A.
- Is it **irrelevant** to our pipeline? → note and set aside.

The output of that analysis will be a clean recommendation doc, separate from both this file and
the raw inputs file.

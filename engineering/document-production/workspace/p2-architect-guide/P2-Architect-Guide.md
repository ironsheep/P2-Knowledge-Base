```{=latex}
% Banner image at top (full width) with drop shadow for visual balance
\begin{tcolorbox}[
  enhanced,
  boxrule=1.5pt,
  colframe=gray!60,
  colback=white,
  drop shadow southeast,
  shadow={3pt}{-3pt}{1mm}{black!15},
  left=0pt, right=0pt, top=0pt, bottom=0pt,
  width=\textwidth,
  arc=0pt,
  outer arc=0pt
]
\includegraphics[width=\linewidth]{inbox/assets/book-artwork.png}
\end{tcolorbox}

\begin{center}
\vspace{0.35cm}
{\fontsize{36}{42}\selectfont\bfseries The P2 Architect's Guide\par}
\vspace{0.3cm}
{\Large\itshape Thinking in Cogs, Pins, and Forces\par}
\vspace{0.35cm}
{\large June 2026\par}
\vspace{0.2cm}
{\large\color{blue}Version 0.1.0 — First Draft\par}
\end{center}

\clearpage
```

<!--
================================================================================
FRONT MATTER — SKELETON (scaffold §1 / task #93)

This file is a STRUCTURAL SKELETON only. The house-standard front matter is
authored in §2 / task #98 (AFTER the chapters, so the conventions block reflects
what the body actually uses). Per the sprint plan, §98 fills:

  - Title page (above — title/subtitle/version per charter D1; DONE in skeleton)
  - Organization / author panel  (charter D1 — Iron Sheep Productions, LLC)
  - Copyright page
  - How to use this guide = the FOUR reading paths
      (newcomer / P1-vet / working-dev / agent — charter §5 + creation-guide §3.5)
  - Conventions block
      (COG-not-CPU · code constants not arithmetic · the "P1 note:" sidebar ·
       the five-color code system)

Reference implementation to model against:
  ../../p2-streamer-programming-guide/opus-master/front-matter.md
House standard:
  engineering/document-production/standards/manual-front-matter-and-code-coloring-standard.md
================================================================================
-->

> **[Front matter — authored in §2 (task #98). Title page above is the scaffold seed; organization panel, copyright, the four reading paths, and the conventions block are added once the chapters fix the conventions they use.]**


<!--
================================================================================
THE P2 ARCHITECT'S GUIDE — BODY (single-file, per DD3)

This file is the canonical body source. It is assembled AFTER front-matter.md by
assemble-manual.sh into P2-Architect-Guide.md for PDF Forge.

SCAFFOLD STATE (task #93): headings + authoring contracts only. Chapters and back
matter are authored by the sprint tasks below — each section heading carries the
task that fills it and its golden sources. Do NOT author content during scaffold;
this skeleton exists so assemble-manual.sh has real structure to assemble and the
template stack can be round-tripped.

  Ch1  "Meet the Propeller 2"                  → task #94 (plan §3)
  Ch2  "Putting It to Work"                    → task #95 (plan §4)
  Ch3  "Thinking in P2 (Functional Decomp.)"  → task #96 (plan §5)
  Appendix A / B, Glossary, Where-to-Next      → task #97 (plan §6)

CONVENTIONS (fixed at scaffold; front matter §98 documents them):
  - "P1 note:" migration sidebars use a fenced div:   ::: p1note  …  :::
    (mapped by filters/p2kb-architect-local.lua → P1NoteBlock; DD1)
  - Code is fenced ```spin2 / ```pasm2 and pnut_ts-verified (never code-divisions)
  - Figures are deferred (DD5): mark intended locations as
    > **[Figure — <description>]**  and log them to PUNCH-LIST.md
================================================================================
-->

# Meet the Propeller 2

<!-- TASK #94 (plan §3). Warm, feature-first mental model. Concrete — NO spatial
abstraction yet (comfort-first gate). Quietly seed "each cog just keeps running,
independently" for Ch3. Land the accessible MCU<->FPGA hook here.
SOURCES: deliverables/ai/P2/architecture/ (p2-architecture-mental-model.yaml,
cog.yaml, hub.yaml, cordic.yaml, streamer/, event_system.yaml, interrupts.yaml,
clock_system.yaml, boot-rom/, locks.yaml, lookup_ram.yaml, fifo.yaml,
xbyte_engine.yaml); Silicon Doc v35; P2 datasheet.
PRIOR-ART (harmonize + link-out, never duplicate): PASM2 Manual Part I —
manuals/p2-assembly-language-manual/opus-master/part-i/chapter-01-execution-model.md,
chapter-04-timing.md, chapter-05-hardware.md.
Feature tour: 8 cogs · pins · hub · smart pins · CORDIC · streamer/FIFO · events ·
memory/boot · clock. Each "what it does + why it's nice", orient-then-link-out.
Weave ::: p1note sidebars (8 cogs, hub round-robin, locks). -->

> **[Chapter 1 — authored in task #94. Skeleton below shows the two load-bearing constructs (a P1 note sidebar and a Spin2 fence) so the template stack round-trips during scaffold verification.]**

::: p1note
**P1 note (scaffold exemplar — replaced in #94):** On the P1 you had eight cogs
sharing one round-robin hub. The P2 keeps the eight-cog feel but the hub is now an
"egg-beater" — this sidebar pattern is how every P1→P2 delta is woven into the
chapters.
:::

```spin2
' scaffold exemplar — replaced by pnut_ts-verified examples in #94
PUB main()
  repeat
    pinwrite(56, 1)
```

# Putting It to Work

<!-- TASK #95 (plan §4). USE the features; build comfort through doing. Still warm
comfort register. SOURCES: deliverables/ai/P2/guides/spin2-getting-started.yaml,
pasm2-getting-started.yaml; serial_loader.yaml / boot-rom/; deliverables/ai/P2/language/.
PRIOR-ART / link-out: PASM2 Part I chapter-01-execution-model.md, chapter-06-address-modes.md.
Launch a cog; drive a pin; the Spin2-vs-PASM2 DECISION (not a tutorial); object /
run-time model; hub sharing; boot/run. Short pnut_ts-verified examples; link out for
depth. Weave ::: p1note sidebars (hub egg-beater, clock setup, 64 pins). -->

> **[Chapter 2 — authored in task #95.]**

# Thinking in P2 (Functional Decomposition)

<!-- TASK #96 (plan §5). The EARNED capstone. Formal space-vs-time thesis as the
RATIONALE → the forces → the first-contact procedure → ONE worked derivation.
Warmth STAYS, rigor RISES, glibness → 0. LOAD-BEARING ANTI-PRESCRIPTION PRINCIPLE:
teaches the METHOD of deriving an architecture, NEVER prescribes an outcome. The
robot-dog derivation is a DEMONSTRATION explicitly framed as ONE machine's answer.
SOURCES (golden home — derives, never drifts): deliverables/ai/P2/architecture/
decomposition/ — all 12 entries. Any authoring-time theory improvement lands in the
YAML FIRST, then renders here. Weave ::: p1note sidebars where the new-in-P2 fabric
changes the decomposition. -->

> **[Chapter 3 — authored in task #96.]**

# Appendix A — Computing in Space and Time (Why We Borrow FPGA Language)

<!-- TASK #97 (plan §6). Temporal→spatial spectrum; honest WHAT-TRANSFERS /
WHAT-DOESN'T (coarse-grained, still software, no place-and-route); the
FPGA-terminology table (term · FPGA meaning · P2 mapping · where it's loose).
SOURCE: architecture/decomposition/spatial-computing.yaml.
ANTI-CASE: no sentence implies the P2 IS an FPGA. -->

> **[Appendix A — authored in task #97.]**

# Appendix B — Further Reading on Functional Decomposition

<!-- TASK #97 (plan §6). Two axes — logical (Parnas; Constantine & Yourdon;
Page-Jones) and physical/concurrent (Hoare CSP + transputer/Occam; optional Kung
systolic) — each with a one-line "why it's relevant to P2". Sources cited in
decomposition-method.yaml. EVERY author/title/year VERIFIED before publish; marked
NEEDS-VERIFICATION until checked. -->

> **[Appendix B — authored in task #97.]**

# Glossary

<!-- TASK #97 (plan §6). From decomposition-glossary.yaml; terms match the YAML. -->

> **[Glossary — authored in task #97.]**

# Where to Next

<!-- TASK #97 (plan §6). Map into the reference manuals (Spin2 v55, the PASM2
Manual, Smart Pins & Streamer guides, Debug manual). Every link resolves to a real
manual. -->

> **[Where-to-Next — authored in task #97.]**



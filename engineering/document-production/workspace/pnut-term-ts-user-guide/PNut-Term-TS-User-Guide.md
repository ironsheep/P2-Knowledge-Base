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
\vspace{0.6cm}
{\fontsize{36}{42}\selectfont\bfseries PNut-Term-TS User Guide\par}
\vspace{0.3cm}
{\Large\itshape The Cross-Platform Downloader, Terminal, and Debug Display for the Propeller 2\par}
\vspace{0.6cm}
{\large July 2026\par}
\vspace{0.2cm}
{\large\color{blue}Version 0.1.0 (draft)\par}

\vfill
\begin{tcolorbox}[
  colback=gray!5,
  colframe=gray!40,
  boxrule=1pt,
  width=0.85\textwidth,
  center,
  title={\bfseries\color{black} Guide Organization},
  colbacktitle=gray!15,
  coltitle=black
]
\textbf{A practical guide to operating PNut-Term-TS}

\vspace{0.3cm}
\begin{minipage}[t]{0.45\textwidth}
\textbf{Getting Started \& Core Features}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Introduction
\item Operating Modes
\item Quick Start
\item The Main Window
\item Menus \& Settings
\item Devices, Recording \& Monitoring
\item Logging
\end{itemize}
\end{minipage}%
\begin{minipage}[t]{0.45\textwidth}
\textbf{Debug Windows \& Reference}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Debug Windows Overview
\item Command-Line Reference
\item Keyboard Shortcuts
\item Troubleshooting
\item Tips \& Best Practices
\item Support \& Resources
\end{itemize}
\end{minipage}

\end{tcolorbox}
\vspace{0.5cm}

{\small Iron Sheep Productions, LLC\par}
{\small P2 Knowledge Base Project\par}
\end{center}

\clearpage
\pagestyle{fancy}

\tableofcontents
\clearpage
\listoffigures
\clearpage
```

# Copyright and License

Copyright © 2026 Iron Sheep Productions, LLC.

PNut-Term-TS is © 2024–2026 Iron Sheep Productions, LLC and is licensed under the MIT License.

This user guide is licensed under the Creative Commons Attribution–NonCommercial–NoDerivatives 4.0 International License (CC BY-NC-ND 4.0).

You are free to:

- **Share** — copy and redistribute the material in any medium or format

Under the following terms:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made (for example, formatting or excerpting).
- **NonCommercial** — You may not use the material for commercial purposes.
- **NoDerivatives** — If you remix, transform, translate, or build upon the material, you may not distribute the modified material.

**Commercial use:** For uses that may be commercial (including paid courses, kits, or redistribution with products), please contact Iron Sheep Productions, LLC (info@ironsheep.biz) for separate permission.

To view the full license, visit: https://creativecommons.org/licenses/by-nc-nd/4.0/

### Trademarks

Parallax, Propeller, Spin, and the Parallax logo are trademarks of Parallax Inc.

```{=latex}
\clearpage
```


<!--
  BODY — PNut-Term-TS User Guide
  ================================
  Content is drafted from the two feeds in ../REF-NO-COMMIT/ following
  ../voice-guide.md and the outline in ../PLANNING.md. The assemble script
  prepends ./front-matter.md to this file.

  doc_class: behavior — the PNut-Term-TS repo is ground truth; do not describe
  behavior from memory. Cross-reference (do NOT reproduce) the debug() directive
  spec, the P2 Debug Window Manual, and the P2 Single-Step Debugger Manual.

  DRAFTED SO FAR: Part 1 — Getting Oriented (the shared trunk / Book 0).
  Books A (GUI), B (Headless), and the reference tail are still to come.
-->

# Part 1: Getting Oriented

Whoever you are and however you plan to use PNut-Term-TS, start here. This short
part places the tool in the Propeller 2 workflow, shows you the three jobs it
does, introduces the two ways you can run it, and then points you to the part of
this guide written for *your* job. Everything after this part is split by how you
work — so spend a few minutes here first, and you will land in the right place.

# Chapter 1: Where PNut-Term-TS Fits

You have written a Propeller 2 program. You have compiled it. Now you want to put
it on the chip and *see what it does* — the numbers it prints, the waveforms it
draws, whether it behaves the way you expected. **PNut-Term-TS is the tool that
closes that loop.** It downloads your compiled program to the P2, then receives
and displays the `debug()` output the program sends back over a USB serial
connection.

## The tool it belongs to

PNut-Term-TS does not work alone. It is the runtime end of a small, coherent set
of tools for developing on the Propeller 2 — the set you reach for whether you
are working by hand or driving the whole thing from an AI coding assistant:

| Tool | Its job |
|------|---------|
| **P2KB MCP** | Serves the P2 knowledge base — instructions, the language, the silicon — to an assistant that is writing P2 code. |
| **`pnut_ts`** | The Spin2 / PASM2 compiler. Turns your source into a binary the P2 can run (and bakes in the debug settings). |
| **`pnut_term_ts`** | *This tool.* Downloads that binary to the P2 and shows you its `debug()` output. |
| Spin2 VS Code extension *(optional)* | Your editor, with Spin2 syntax and semantic highlighting. |

Think of the first three as compile, and run-and-observe. `pnut_ts` produces the
binary; **PNut-Term-TS is where you watch it come alive.**

If you are building an *agentic* P2 workflow — an assistant that writes code,
compiles it, runs it on real silicon, and reads back the result to decide what to
do next — this tool is the piece that lets the assistant *observe the hardware*.
That workflow is described in depth in **The P2 Architect's Guide, Part 3**; this
guide is the operating manual for the tool that makes it possible.

# Chapter 2: Three Tools in One

The quickest way to understand PNut-Term-TS is to know what it replaces. It folds
**three** jobs that used to need separate tools — or a specific operating system —
into one program that runs the same way everywhere.

## 1. A downloader

It loads your compiled program onto the P2 and starts it running — either into
**RAM** (fast, for the edit-run-edit loop of development) or into **flash** (so
the program sticks and runs on power-up). It handles resetting the P2 into its
loader for you.

## 2. A serial terminal — replacing Parallax Serial Terminal

Once your program is running, its `debug()` text and any other serial output
appear in a terminal window, and you can type back to the program. This is the
job Parallax Serial Terminal did — now built in, and on every platform.

## 3. A debug-window display — replacing PNut's, everywhere

The P2's `debug()` system can draw far more than text: oscilloscope traces, logic
timing, plots, bitmaps, spectra, and an interactive single-step debugger. PNut can
show these windows too — but only on Windows. **PNut-Term-TS renders the same
windows on Windows, macOS, and Linux**, and it is where you *produce* the saved
images and captures those windows can emit. This cross-platform reach is the whole
reason the tool exists in the form it does.

> **What the name tells you.** *PNut-Term-TS* reads as "PNut **Term**inal, written
> in **T**ype**S**cript." The *Terminal* is jobs 1 and 2; the *TypeScript* is why
> job 3 runs everywhere instead of on Windows alone. The name is a compact
> reminder of what the tool is.

The `debug()` display windows themselves — what each one shows and how to author
them from your Spin2 source — are the subject of the **P2 Debug Window Manual**,
and the interactive single-step debugger has its own **P2 Single-Step Debugger
Manual**. This guide is about the *tool that displays and produces them*; when you
need the windows in depth, those manuals are where to go.

# Chapter 3: Two Ways to Run — GUI and Headless

PNut-Term-TS runs in two fundamentally different ways, and knowing both up front
will save you a lot of confusion. You choose between them by *how you launch the
tool*.

## Headed — the interactive GUI

Launch it normally and you get the full graphical application: a main window with
a terminal, a toolbar to download and reset, and debug windows that pop open on
their own as your program draws to them. This is the mode you use **at your desk**,
watching a P2 and reacting to what you see.

```bash
pnut-term-ts -r myprogram.bin
```

## Headless — no windows, for automation

Launch it with `--headless` and there is **no graphical interface at all**. The
tool downloads your program, captures everything the P2 sends to a timestamped log
file, and exits on a signal you define. This is the mode built for **continuous
integration pipelines, containers, and AI coding assistants** running
hardware-in-the-loop tests — anywhere a program, not a person, is watching.

```bash
pnut-term-ts --headless -r test.bin --end-marker
```

In headless mode the **log file is the whole point** — it is how an automated
caller (or an assistant reading back its own program's behavior) sees what the P2
did. We return to that idea in depth in the headless part of this guide.

Between these two poles are a few in-between modes — downloading from the command
line but keeping the GUI, a headed "batch" run that exits when the program signals
it is done, and an IDE-integration mode. They are covered where they belong, in
the part for your workflow.

# Chapter 4: Which Path Is Yours

The rest of this guide is written twice — once for each way of working — because
the two jobs genuinely differ. Find yourself below and go there.

| If you are… | …you want | Go to |
|-------------|-----------|-------|
| At your desk, watching a P2 and reacting to what you see | The windows, the toolbar, recording a session, driving the single-step debugger by hand | **Part 2 — Using the GUI** |
| Automating P2 runs — CI, a container, or an AI assistant in the loop | Launching headless, ending a run cleanly, exit codes, and reading the log | **Part 3 — Headless and Automation** |

You do not have to read the other path. What both paths share — the full
command-line reference, keyboard shortcuts, the settings that shape either mode,
and troubleshooting — lives in **Part 4 — Reference**, and both paths point you
there when you need it.

If you are not sure yet, start with **Part 2**. The GUI shows you everything the
tool can do in a form you can see, and much of what you learn there carries
straight over to automating it later.

<!--
  ===========================================================================
  END OF DRAFTED CONTENT (Part 1 — Getting Oriented / the shared trunk).
  TO COME:
    Part 2 — Using the GUI (Book A): main window, downloading, serial terminal,
      debug windows + Automatic Window Placement, single-step debugger
      interaction, recording & playback, performance monitor, menus & settings.
    Part 3 — Headless and Automation (Book B): headless invocation, end-markers
      / timeouts, exit codes, the log as the feedback loop, USB traffic log,
      CI / agent recipe.
    Part 4 — Reference: full CLI reference, keyboard shortcuts, settings
      hierarchy, troubleshooting, support & resources.
  Trunk diagrams (TBD, not yet rendered): (1) tool-chain position; (2) the
  three-in-one identity. See PLANNING.md "Open items".
  ===========================================================================
-->



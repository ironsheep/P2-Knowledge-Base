<!--
  BODY — PNut-Term-TS User Guide
  ================================
  Content is drafted from the two feeds in ../REF-NO-COMMIT/ following
  ../voice-guide.md and the outline in ../PLANNING.md. The assemble script
  prepends ./front-matter.md to this file.

  doc_class: behavior — the PNut-Term-TS repo is ground truth; do not describe
  behavior from memory. Cross-reference (do NOT reproduce) the debug() directive
  spec, the P2 Debug Window Manual, and the P2 Single-Step Debugger Manual.

  COMPLETE as of v1.0.0 (2026-08-19): Parts 1-4, Chapters 1-19, all 9 figures.

  PLACEMENT RULE (agent material): Parts 1-2 teach a PERSON to operate the tool.
  AI agents, assistants, and P2KB MCP must not appear before Part 3 — the reader
  cannot act on them yet, and the log-as-return-path claim is FALSE for a person
  at the GUI, whose return path is the screen. The agentic tool-chain figure and
  the Architect Part-3 link live in Ch15, after the headless loop is in hand.
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
of tools for developing on the Propeller 2:

| Tool | Its job |
|------|---------|
| **`pnut-ts`** | The Spin2 / PASM2 compiler. Turns your source into a binary the P2 can run (and bakes in the debug settings). |
| **`pnut-term-ts`** | *This tool.* Downloads that binary to the P2 and shows you its `debug()` output. |
| Spin2 VS Code extension *(optional)* | Your editor, with Spin2 syntax and semantic highlighting. |

Think of the first two as compile, then run-and-observe. `pnut-ts` produces the
binary; **PNut-Term-TS is where you watch it come alive.**

```{=latex}
\begin{figure}[H]
\centering
\diagramscale{
\begin{tikzpicture}
\node[iospbox] (you) {You};
\node[iospbox, right=14mm of you] (compile) {\texttt{pnut-ts}\\compiler};
\node[iospkey, right=16mm of compile] (term) {\texttt{pnut-term-ts}\\download + observe};
\node[iospbox, right=26mm of term] (p2) {Propeller~2\\silicon};
\node[iospbox, below=15mm of term] (log) {the log file\\\texttt{./logs/}};
\node[iospsub, below=1.5mm of log] (logsub)
   {a timestamped record\\of the run};
\draw[iospflow] (you) -- node[above, font=\scriptsize]{Spin2} (compile);
\draw[iospflow] (compile) -- node[above, font=\scriptsize]{\texttt{.bin}} (term);
% The serial link is a TWO-WAY conversation, and both directions terminate at
% pnut-term-ts -- never at you. Drawn as a matched pair rather than one arrow,
% because the return leg is the whole point of the figure.
\draw[iospflow] ([yshift=2mm]term.east) --
   node[above, font=\scriptsize]{run} ([yshift=2mm]p2.west);
\draw[iospflow] ([yshift=-2mm]p2.west) --
   node[below, font=\scriptsize]{\texttt{debug()}} ([yshift=-2mm]term.east);
\draw[iospflow] (term) -- node[right, font=\scriptsize]{writes} (log);
% The return leg to the PERSON is the screen, not the log -- arced over the
% spine so it does not collide with the .bin arrow running beneath it.
\draw[iospflow] (term.north) to[out=90, in=90, looseness=0.55]
   node[pos=0.5, above, inner sep=2pt, font=\scriptsize]
   {terminal + debug windows} (you.north);
\end{tikzpicture}
}
\caption{Where PNut-Term-TS sits in the Propeller 2 workflow. \texttt{pnut-ts}
builds the binary; PNut-Term-TS downloads it, starts it, and shows you what the
chip sends back — as terminal text and as the debug windows your program draws
to — while writing the same output to a log file you can keep.}
\end{figure}
```

Follow how that loop closes. **Everything the P2 sends comes back to
PNut-Term-TS** — there is no second path off the chip. What arrives is shown to
you as it happens, in the terminal and in the debug windows your program draws
to, and the same output is written to a log file as it goes, so you have a record
of the run after the windows are closed. (Logs land next to the run, in `./logs/`
relative to the folder you launched from, so the evidence stays beside the
program that produced it. You can point them somewhere else if you would rather.)

# Chapter 2: Three Tools in One

To understand PNut-Term-TS, start from what it replaces. It folds
**three** jobs that used to need separate tools — or a specific operating system —
into one program that runs the same way everywhere.

## 1. A downloader

It loads your compiled program onto the P2 and starts it running — either into
**RAM** (fast, for the edit-run-edit loop of development) or into **flash** (so
the program sticks and runs on power-up). It handles resetting the P2 into its
loader for you.

**It will download a binary from any compiler.** Downloading is the P2's own boot
protocol, so what built the image does not come into it. PNut, `pnut-ts`, FlexSpin
and Spin Tools IDE all produce binaries this tool loads and starts, and so does
anything else that can build for the P2 — if your toolchain produces a binary that
downloads and runs, PNut-Term-TS can download and run it. You do not have to
change compilers to use this tool.

What comes *back* follows a single rule, and it is a rule about the bytes on the
wire rather than about your compiler:

| What the P2 sends | Where it appears |
|---|---|
| debug output formed as *Parallax Spin2 Documentation v55* specifies | the debug log, and the debug windows it addresses |
| anything else written to the serial port | the terminal |

Both halves matter. A program built **without** debug is not a lesser case — every
byte it writes still arrives and is shown in the terminal, exactly as any serial
terminal would show it. Build **with** debug and that output is recognised for
what it is and routed onward, to the log and to the windows the commands name.

Which means the way for any compiler to be fully supported here is written down
and public: emit what the Spin2 documentation specifies, and this tool will
receive it. The one thing that is not carried on the wire is the debug baud rate —
see Chapter 6, where compilers do differ.

## 2. A serial terminal — replacing Parallax Serial Terminal

Once your program is running, its `debug()` text and any other serial output
appear in a terminal window, and you can type back to the program. This is the
job Parallax Serial Terminal did — now built in, and on every platform.

## 3. A debug-window display — replacing PNut's, everywhere

The P2's `debug()` system can draw far more than text: oscilloscope traces, logic
timing, plots, bitmaps, spectra, and an interactive single-step debugger. PNut can
show these windows too — but only on Windows. **PNut-Term-TS renders the same
windows on Windows, macOS, and Linux**, and it is where you *produce* the saved
images and captures those windows can emit. That cross-platform reach is a large
part of why the tool takes the form it does.

> **What the name tells you.** *PNut-Term-TS* reads as "PNut **Term**inal, written
> in **T**ype**S**cript." The *Terminal* is jobs 1 and 2; the *TypeScript* is why
> job 3 runs everywhere instead of on Windows alone.

```{=latex}
\begin{figure}[H]
\centering
\diagramscale{
% These three lines are NOT traffic -- nothing flows along them. They say
% "this role is folded into that app," which is a statement about identity,
% not about data. Dashed keeps them from borrowing the solid-arrow vocabulary
% Figure 1.1 uses for the real serial/file path, where the arrows DO mean flow.
\begin{tikzpicture}[iospindicate/.style={iospflow, dashed,
                                         dash pattern=on 2.2pt off 1.8pt}]
\node[iospbox, align=center] (dl) at (0,1.9) {Downloader};
\node[iospbox, align=center] (term) at (0,0)
   {Serial terminal\\{\scriptsize replaces Parallax Serial Terminal}};
\node[iospbox, align=center] (dbg) at (0,-1.9)
   {Debug-window display\\{\scriptsize replaces PNut's --- now cross-platform}};
\node[iospkey, align=center, minimum height=15mm, minimum width=30mm] (one) at (7,0)
   {\textbf{PNut-Term-TS}};
\node[iospsub, below=1.5mm of one] {one app \textperiodcentered\ Windows \textperiodcentered\ macOS \textperiodcentered\ Linux};
\draw[iospindicate] (dl) -- (one);
\draw[iospindicate] (term) -- (one);
\draw[iospindicate] (dbg) -- (one);
\end{tikzpicture}
}
\caption{The three tools PNut-Term-TS folds into one.}
\end{figure}
```

The `debug()` display windows themselves — what each one shows and how to author
them from your Spin2 source — are the subject of the **P2 Debug Window Manual**,
and the interactive single-step debugger has its own **P2 Single-Step Debugger
Manual**. This guide is about the *tool that displays and produces them*; when you
need the windows in depth, those manuals are where to go.

# Chapter 3: Two Ways to Run — GUI and Headless

PNut-Term-TS runs in two fundamentally different ways, and the rest of this guide
is organized around the difference. You choose between them by *how you launch the
tool*.

## Headed — the interactive GUI

Launch it normally and you get the full graphical application: a main window with
a terminal, a toolbar to download and reset, and debug windows that pop open on
their own as your program draws to them. This is the mode you use **at your desk**,
watching a P2 and reacting to what you see. You can start it on its own and load a
program from the GUI, or name a program on the command line to download at once:

```command
pnut-term-ts                    # open the GUI, load a file from it
pnut-term-ts -r myprogram.bin   # open the GUI and download this file
```

## Headless — no windows, for automation

Launch it with `--headless` and there is **no graphical interface at all**. The
tool downloads your program, captures everything the P2 sends to a timestamped log
file, and exits on a signal you define. This is the mode built for **continuous
integration pipelines, containers, and scripted test runs** on real hardware —
anywhere a program, not a person, is watching.

```command
pnut-term-ts --headless -r test.bin --end-marker
```

With no windows, the log file is the only place the run can be seen: it is how
whatever launched the tool finds out what the P2 did. The headless part of this
guide covers it in depth.

Between these two poles are a few in-between modes — downloading from the command
line but keeping the GUI, a headed "batch" run that exits when the program signals
it is done, and an IDE-integration mode. They are covered where they belong, in
the part for your workflow.

Whichever way you launch it, the tool's help is built in: run `pnut-term-ts
--help` at any time for the full list of options.

# Chapter 4: Which Path Is Yours

The rest of this guide is written twice — once for each way of working — because
the two jobs genuinely differ. Find yourself below and go there.

| If you are… | …you want | Go to |
|-------------|-----------|-------|
| At your desk, watching a P2 and reacting to what you see | The windows, the toolbar, recording a session, driving the single-step debugger by hand | **Part 2 — Using the GUI** |
| Automating P2 runs — CI, a container, or a script driving the hardware | Launching headless, ending a run cleanly, exit codes, and reading the log | **Part 3 — Headless and Automation** |

You do not have to read the other path. What both paths share — the full
command-line reference, keyboard shortcuts, the settings that shape either mode,
and troubleshooting — lives in **Part 4 — Reference**, and both paths point you
there when you need it.

If you are not sure yet, start with **Part 2**. The GUI shows you everything the
tool can do in a form you can see, and much of what you learn there carries
straight over to automating it later.

# Part 2: Using the GUI

This part is for working **at your desk** — launching PNut-Term-TS as a graphical
application, downloading a program, and watching it run in the terminal and the
debug windows. If you are here to automate P2 runs instead, skip ahead to *Part 3
— Headless and Automation*; the two paths rejoin in *Part 4 — Reference*.

# Chapter 5: The Main Window

When you launch PNut-Term-TS, **two windows open**: the **main window** and the
**Debug Logger** (a separate window that captures the run's log). These are the
two windows the auto-layout keeps reserved spots for (Chapter 8); the other debug
windows — scopes, plots, and the rest — open on their own later, as your program
draws to them.

This chapter is about the main window: your home base for connecting,
downloading, and reading text output. It has five areas, top to bottom — a **menu
bar**, a **toolbar**, a **text-entry field**, the **terminal display**, and a
**status bar**.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=\linewidth]{inbox/assets/main-window-and-logger.png}
\caption{Startup opens two windows: the PNut-Term-TS main window (left) and the Debug Logger (right).}
\end{figure}
```

## The toolbar

Left to right:

- **Reset control line** — a button labeled with the active reset line (**DTR**
  or **RTS**) and a checkbox. Click it to assert a reset on the P2. Which line a
  device uses is set per device in PropPlug Management (Chapter 10); this button
  just shows and fires it.
- **RAM** / **FLASH** — download the loaded binary into the P2's RAM or its
  flash and run it. The small indicator beside them is green for the active
  download target.
- **Download** (the tray icon) — pick a binary file to load.
- **Record** / **Play** — start or stop a recording, and play one back, with a
  status label beside them ("Ready", "Recording…"). Recording is a further
  feature covered briefly in Chapter 11.

## The text-entry field

The field just below the toolbar sends a line of text to the running P2 when you
press **Enter** — this is how you type back to a program that reads input. (During
playback of a recording, a transport strip appears here instead — see Chapter 11.)

## The terminal display

The large central area shows the text your program sends: its `DEBUG()` output
and any other serial text. How it looks — terminal mode, color theme, font, and
whether each line is tagged with the cog that produced it — is yours to set;
Chapter 7 covers the terminal, and Chapter 10 the settings behind it.

## The status bar

The status bar carries the at-a-glance state of the connection. On the **left**:

- **Connection indicator** — green when connected to a P2, amber when not.
- **Active cogs** — which cogs are currently driving debug output.
- **Logging indicator** — lit while the debug log is being written. (Recording is
  a separate thing, shown by the toolbar's status label.)

On the **right**:

- **Echo** — a checkbox that suppresses characters the P2 echoes back, so text
  you type is not shown twice.
- **TX / RX** — flash during serial transmit and receive.
- **Port** — the connected device's path.
- **Baud** — the active debug baud rate.

The active reset line (DTR or RTS) lives on the *toolbar* button, not here.

# Chapter 6: Downloading and Running Your Program

The core loop at your desk is: hand PNut-Term-TS a compiled program, tell it
where to put it on the P2, and watch it run.

## Two ways to load a program

There are two ways to hand PNut-Term-TS your compiled `.bin`, and you can mix
them freely:

- **Interactively (standalone).** Launch PNut-Term-TS on its own, with no file —
  it opens ready and waiting. Click **Download** on the toolbar to choose a
  binary, then send it to the P2 with the **RAM** or **FLASH** button. Open the
  app once and load, and re-load, programs from the GUI as you work.
- **From the command line.** Name the binary when you launch, and PNut-Term-TS
  downloads and runs it straight away, keeping the GUI open:

```command
pnut-term-ts -r myprogram.bin      # download to RAM and run
pnut-term-ts -f myprogram.bin      # download to FLASH and run
```

## RAM or flash

Either way you load it, you choose *where* the program goes on the P2:

- **RAM** (`-r`, or the toolbar **RAM** button) — the program is loaded and run
  immediately, but does not survive a power cycle. This is the fast path for the
  edit-compile-run loop of development.
- **FLASH** (`-f`, or the toolbar **FLASH** button) — the program is written to
  the P2's flash, so it runs on its own every time the board powers up.

You use one or the other — `-r` and `-f` cannot be combined. PNut-Term-TS resets
the P2 into its loader at the right moment, downloads the program, and begins
capturing debug output.

## Resetting the P2 — and when it happens

To start your program cleanly, the P2 has to be reset. Whether that happens the
moment PNut-Term-TS connects is governed by one preference, **Reset P2 on App
Startup** (Chapter 10), and it reflects two different ways of working:

- **On** (the default) — reset on connect. Use this during development, so every
  run starts from a known state.
- **Off** — do not reset; attach to a program that is *already running*. Use this
  to monitor a board that is already doing its job.

The reset itself is asserted over one of two control lines — **DTR** or **RTS**.
Parallax PropPlugs and most FTDI adapters use **DTR**; some clones need **RTS**.
The line is remembered per device (Chapter 10), and you can override it for one
session with `--rts`.

## The debug baud rate — you should not need to set it

When you download a binary that PNut-Term-TS recognises, **it reads the debug baud
rate out of the image itself** and listens at exactly that rate. PNut and `pnut-ts`
write the value in — including when your source sets its own rate:

```spin2
CON  DEBUG_BAUD = 921600   ' picked up automatically
```

If your source says nothing, the P2 toolchain defaults to **2,000,000** bits per
second, and so does PNut-Term-TS. Either way, downloading a binary sets the rate
for you, with no flag from you.

This is the one place in the download path where toolchains differ, so it is worth
being plain about it. **PNut-Term-TS auto-detects a PNut or `pnut-ts` image** and
takes the debug baud rate from it, which is why downloading one settles the question
with no flag from you.

**A binary it does not recognise as PNut or `pnut-ts` downloads and runs exactly the
same way** — that half does not depend on your compiler at all. What it does not do
is hand over a rate. So if that program was built **with** debug, tell the tool the
rate yourself with `-b`; if it was built without debug, there is nothing to set and
its output simply appears in the terminal.

There is an override, `-b` (`--debugbaud`), for exactly the two cases the binary
cannot tell us about:

- **Attaching to a P2 that is already running** — no download, so there is no
  image to read a rate out of.
- **A debug build from any other toolchain** — the download works; only the rate
  has to come from you.

Either way you have two ways to say it: `-b` for one session, or the **Default
Baud Rate** preference (Chapter 10) if you would rather set it once and forget it.

If you pass `-b` and it disagrees with the binary you are downloading, PNut-Term-TS
warns you — the P2 will transmit at its own compiled rate regardless, and the
mismatch would make the output unreadable. When text comes out garbled, the first
thing to try is *dropping* `-b`.

# Chapter 7: The Serial Terminal

Once your program runs, its text appears in the terminal, and you can type back.
This is the job Parallax Serial Terminal used to do — now built in, and the same
on every platform.

## Reading output

Each line the P2 sends is shown as it arrives. If **Show Cog Prefixes** is on
(the default), each line is tagged with the cog that produced it, so you can tell
overlapping output apart. You can search what has scrolled past with **Find**
(`Ctrl+F`), and clear the display with **Clear Terminal**.

## Typing back

Type into the text-entry field and press **Enter** to send a line to the running
program. If the P2 echoes your characters back, tick the **Echo** box in the
status bar so they are not shown twice.

## Look and feel

The terminal's appearance is set in Preferences (Chapter 10); the choices that
shape day-to-day reading are:

| Setting | Choices | Default |
|---------|---------|---------|
| Terminal Mode | PST, ANSI | PST |
| Color Theme | Green / White / Amber on Black | Green on Black |
| Font Size | 10–24 | 14 |
| Font Family | Default, Parallax, IBM 3270 (+ Green / Amber) | Default |
| Show Cog Prefixes | on / off | on |
| Local Echo | on / off | off |

# Chapter 8: Debug Windows and Automatic Window Placement

The P2's `debug()` system draws far more than text. Ask for a scope trace, a
logic-timing view, a plot, a bitmap, and PNut-Term-TS opens a separate window for
each — an oscilloscope, a logic analyzer, and so on, live on Windows, macOS, and
Linux alike.

## Windows open themselves

There is **no menu command to open a debug window.** A window appears the moment
your program sends a `debug()` display directive for it, and it is the directive
that decides what the window shows. The window types are:

| Window | Shows |
|--------|-------|
| TERM | A text terminal |
| BITMAP | A pixel / image display |
| PLOT | General X/Y plotting, shapes, sprites |
| SCOPE | Oscilloscope-style waveforms |
| SCOPE_XY | X-versus-Y (Lissajous / vector) display |
| LOGIC | Logic-analyzer timing |
| FFT | Frequency spectrum |
| SPECTRO | Spectrogram / waterfall |
| MIDI | MIDI keyboard / messages |
| Cog logger | Per-cog debug message log |
| Debugger | The interactive single-step debugger (Chapter 9) |

> **Where to learn the windows themselves.** *What* each window displays and
> *how you author it* from your Spin2 source — the `debug()` display directives
> and their parameters — are the subject of the **P2 Debug Window Manual** and
> the Parallax P2 DEBUG documentation. This guide covers the windows only as the
> tool *presents* them; when you want a window in depth, that manual is where to
> go.

## Automatic Window Placement

A P2 program can name a screen position for each
window with a `POS` directive, but it does not have to. **A window with no `POS`
is placed for you automatically** — PNut-Term-TS lays the whole set out as a tidy
*dashboard* instead of stacking every window on the same spot. (Windows that *do*
carry a `POS` are put exactly where they ask.)

The dashboard is a grid **sized to your display**: the height sets how many rows,
the width how many columns. A typical 1920×1080 screen gives a **3×3** grid; a
2560×1440 or a 4K display gives more cells (5×3 or 5×4); an ultra-wide gives more
columns still, up to seven. There is always an odd number of columns, so a true
center column exists to build around.

Windows fill the grid in a fixed **center-out** order: the first window takes the
top-center cell, the next two flank it, and the arrangement widens outward and
works its way down, row by row, staying balanced left-to-right as it goes. If you
open more windows than the grid holds, the extras cascade from the top-left.

**The bottom row is not really yours.** The **main window** and the **debug
logger** live there, and both are wider than a single column — so each of them
also claims the cell beside it, which is what a window too wide for its cell
always does. Between them they take the rest of the bottom row; on a typical
screen they even overlap each other, as you can see in Figure 5.1. In practice
that leaves the far-left cell as the only bottom slot an auto-placed window can
land in.

```{=latex}
\begin{figure}[H]
\centering
\diagramscale{
\begin{tikzpicture}[x=1cm,y=1cm]
\def\cw{2.0}\def\ch{1.5}\def\gp{0.18}
\draw[draw=diagram-border, line width=1pt, rounded corners=3pt, fill=white]
   (-0.35,-0.35) rectangle (10.75,5.35);
\node[iospsub] at (5.2,5.62) {your screen};
% Auto-placed windows, labelled by fill order (Half-Moon Descending). Only the
% first TEN are drawn as ordinary cells: they fill the top two rows exactly.
% The bottom row is NOT three more free cells -- see below.
\foreach \lbl/\c/\r in {1/2/0, 2/1/0, 3/3/0, 4/2/1, 5/1/1, 6/3/1,
                        7/0/0, 8/4/0, 9/0/1, 10/4/1} {
  \pgfmathsetmacro\px{\c*(\cw+\gp)}
  \pgfmathsetmacro\py{(2-\r)*(\ch+\gp)}
  \draw[draw=diagram-border, fill=diagram-box, rounded corners=1.5pt]
     (\px,\py) rectangle ++(\cw,\ch);
  \draw[draw=diagram-border, fill=diagram-highlight, rounded corners=1.5pt]
     (\px,\py) ++(0,\ch-0.3) rectangle ++(\cw,0.3);
  \node[font=\large\bfseries, text=diagram-text] at (\px+\cw/2,\py+0.6) {\lbl};
}
% The 11th window: the one bottom cell the system windows leave alone.
\draw[draw=diagram-border, fill=diagram-box, rounded corners=1.5pt]
   (0,0) rectangle ++(\cw,\ch);
\draw[draw=diagram-border, fill=diagram-highlight, rounded corners=1.5pt]
   (0,\ch-0.3) rectangle ++(\cw,0.3);
\node[font=\large\bfseries, text=diagram-text] at (\cw/2,0.6) {11};
% THE BOTTOM ROW IS NOT A ROW OF CELLS. Both system windows are wider than one
% column, and a width-overflowing window reserves the cells beside it -- so
% between them they take the rest of the row. They are drawn here at real
% relative width, overlapping, which is what they actually do on screen.
\def\mwl{2.18}\def\mwr{7.70}\def\dll{6.95}\def\dlr{10.72}
\draw[draw=diagram-border!70, fill=diagram-border!12, rounded corners=1.5pt]
   (\mwl,0) rectangle (\mwr,\ch);
\node[font=\scriptsize\itshape, text=diagram-text, align=center]
   at ({(\mwl+\dll)/2},0.75) {Main\\Window};
% drawn second, so it sits ON TOP of the main window the way it really does
\draw[draw=diagram-border, fill=diagram-border!22, rounded corners=1.5pt]
   (\dll,0) rectangle (\dlr,\ch);
\node[font=\scriptsize\itshape, text=diagram-text, align=center]
   at ({(\dll+\dlr)/2},0.75) {Debug\\Logger};
\node[iospsub, align=center] at (6.6,-0.72)
   {both are wider than a column, and they overlap each other:\\
    no auto-placed window fits between them};
\end{tikzpicture}
}
\caption{Automatic Window Placement: unpositioned windows fill a screen-sized grid
center-out, top row first (numbers = open order; shown on the canonical 5-column
$\times$ 3-row layout). The bottom row belongs to the main window and the debug
logger --- both are wider than one column, so they take the cells beside them
too, leaving only the far-left cell for an eleventh window.}
\end{figure}
```

> **One thing to expect on a 1920-wide screen.** The fill *order* is defined
> against the five-column layout above, but the *pixel* positions are computed
> from the columns your display actually gets — and 1920 wide gives you three.
> The two outermost positions then fall off the right-hand edge of the work area
> and get clamped back to it, so those later windows stack near the right edge
> rather than tiling cleanly. It is a known constraint of the current placer, not
> something you have done wrong. Displays 2000 px and wider get five columns and
> lay out exactly as drawn. If you want a specific arrangement on a 1920-wide
> screen, that is a good moment to reach for `POS`.

The result is that you can throw a handful of `debug()` displays on screen and get
a readable dashboard with no `POS` directives at all. And when you *do* want to
pin a window to an exact spot, you do not have to guess coordinates: **drag a
display window and its title bar shows its live `x, y` position** as it moves —
read the numbers off and bake them into a `POS` directive in your source. (The cog
logger, the debugger, and the message-log windows do not show this readout; they
are placed by their own rules.)

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=\linewidth]{inbox/assets/multi-window-desktop.png}
\caption{Several debug windows auto-placed on a real desktop: SCOPE, a TERM status readout, and a Software-SPI LOGIC trace filling the top rows, with the main window and Debug Logger along the bottom in their reserved cells.}
\end{figure}
```

## Two more shared behaviors

- **SAVE** — a `debug()` `SAVE` (or `SAVE WINDOW`) directive writes a window's
  current image out to a bitmap file. This is how you *produce* the captures the
  debug windows can emit.
- **Input back to the P2** — a window can forward mouse and key input to the
  running program, when the program asked for it with the `PC_MOUSE` / `PC_KEY`
  mechanisms.

# Chapter 9: The Single-Step Debugger

One of the windows PNut-Term-TS can display is special: the **interactive
single-step debugger**. When your program is compiled with debugging enabled and
reaches a `DEBUG` statement, execution can pause and this window appears — showing
registers, memory, flags, and the program counter, and letting you step, run, set
breakpoints, and watch state as your PASM2 code executes.

PNut-Term-TS is what **renders that debugger window and carries your interaction
with it** — the keystrokes and clicks that step and break — to the P2 and back.
Bringing this interface to macOS and Linux, not just Windows, is a large part of
why the tool exists.

> **Using the debugger is its own subject.** How to turn on debugging, read each
> region of the debugger window, set breakpoints, and drive a debugging session
> is covered fully in the **P2 Single-Step Debugger Manual**. This guide's part
> is only that the window is *here*, cross-platform, and interactive.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=\linewidth]{inbox/assets/single-step-debugger.png}
\caption{The single-step debugger window, hosted by PNut-Term-TS (shown here on macOS).}
\end{figure}
```

# Chapter 10: Menus, Settings, and Devices

This chapter collects the GUI's configuration: the menus, the settings that shape
every run, and the management of the USB devices you connect through.

## Menus differ by platform

PNut-Term-TS uses the **native application menu on macOS** and an **in-window menu
bar on Windows and Linux** — and they are **not equivalent**. The macOS native
menu offers only the application, Edit, and Window menus; **File, Help, Find,
Clear Terminal, and the show/hide-windows items live only on the Windows/Linux
in-window menu bar**. Accelerators differ too: `Cmd` on macOS, `Ctrl` on
Windows/Linux.

| Menu | Items |
|------|-------|
| **File** *(Win/Linux bar)* | New / Open / Save Recording; Select PropPlug; Start Recording (`Ctrl+R`); Stop Recording; Playback Recording (`Ctrl+P`); Exit (`Ctrl+Q`) |
| **Edit** | Cut / Copy / Paste; Find… (`Ctrl+F`); Clear Terminal; Preferences… (`Ctrl+,`) |
| **Window** | Performance Monitor; Show All Windows; Hide All Windows |
| **Help** *(Win/Linux bar)* | Documentation (`F1`); About PNut-Term-TS |

On macOS, **Preferences…** is under the application menu (`Cmd+,`), along with the
standard Quit and Hide items.

## Settings and the hierarchy behind them

Open settings with **Edit → Preferences…** (`Ctrl+,`, or `Cmd+,` on macOS).
Settings resolve in priority order, most specific first:

1. **Project settings** — overrides scoped to the current project directory.
2. **User settings** — your per-machine defaults.
3. **Application defaults** — the built-in baseline.

The dialog has three tabs. The **User Settings** tab holds your machine-wide
defaults:

| Group | Setting | Default |
|-------|---------|---------|
| Terminal | Mode / Theme / Font size / Font family / Cog prefixes / Local echo | PST · Green on Black · 14 · Default · on · off |
| Serial Port | Default PropPlug / Default baud / Reset P2 on App Startup | Auto-detect · — · on |
| Logging | Log Directory / Auto-Save Debug Output / Enable USB Traffic Logging | `./logs/` · on · off |
| Recordings | Recordings Directory | `./recordings/` |
| Debug Logger | History Lines (100–10000) | 1000 |

A P2 reset always starts a **new** log file — that boundary is what makes a log
readable as a single run. Logs are not size-capped.

The **Project Settings** tab carries the same controls, each with an **override**
checkbox: only the boxes you tick override your user defaults for the current
project, and the rest show and inherit your global values.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=0.82\linewidth]{inbox/assets/preferences-user-settings.png}
\caption{Preferences --- the User Settings tab.}
\end{figure}
```

## PropPlug and device management

PNut-Term-TS remembers every USB serial device it has seen and lets you name it
and set its reset line. New devices are added automatically when they enumerate,
with the Parallax-standard **DTR** control line.

Open the **PropPlug Management** tab to manage them. The known-devices table shows
each device's serial number, friendly name, control line, and last-used time.
Select a row to give it a **Friendly Name** (e.g. "Workbench Plug"), choose its
**Control Line** (DTR or RTS), view its VID/PID, and **Save Changes** or **Delete
Device**.

When you have more than one device, which one a run uses is decided in this order:

1. A command-line `-p <device>` — an exact match, or a case-insensitive partial
   match on the path or serial number.
2. A project device override, if one is set.
3. Your user default.
4. Auto-detect — used when exactly one device is connected.
5. Otherwise, you are asked to choose (or the run errors if nothing matches).

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=0.82\linewidth]{inbox/assets/preferences-propplug.png}
\caption{Preferences --- the PropPlug Management tab.}
\end{figure}
```

# Chapter 11: Further Features

Two capabilities sit outside the everyday download-and-watch loop. They are
documented here — briefly, and deliberately out of the main flow — because one is
present but not yet exhaustively exercised, and the other is aimed at development
and diagnostics rather than routine use. Reach for them if they fit your need, but
do not build a workflow on them yet.

## Recording and playback

PNut-Term-TS can capture a whole debug session to a **`.p2rec`** file and replay
it later, timing and all — useful for regression testing, for sharing a
reproduction, or for studying a run offline. Start and stop a recording from
**File → Start Recording** (`Ctrl+R`) and **File → Stop Recording**; replay one
with **File → Open Recording…** (`Ctrl+P`), which reproduces the captured stream —
including its timing — driving the debug windows exactly as the live run did.
Recordings land in your Recordings Directory (default `./recordings/`).

> This feature has had only limited testing so far. Treat it as experimental:
> it is here if it helps you, but it is not yet a foundation to build on.

## Performance monitoring

**Window → Performance Monitor** opens a view of the serial-to-window data path —
throughput, buffer usage, queue depth, and message counts — so you can see
whether the tool is keeping up at high baud rates. It is primarily a
**developer and diagnostic** aid: reach for it if you suspect the pipeline is
falling behind (buffer usage climbing toward full), and otherwise you can leave
it closed.

# Part 3: Headless and Automation

This part is for running PNut-Term-TS where **no person is watching** — a
continuous-integration pipeline, a container, or an AI coding assistant running
programs on real P2 silicon and reading back the results. There is no graphical
interface here; the **log file is how the run is seen**. If you are working at
your desk, *Part 2 — Using the GUI* is your part; both rejoin in *Part 4 —
Reference*.

# Chapter 12: Running Headless

Add `--headless` and PNut-Term-TS runs with **no windows at all**. It downloads
your program, captures everything the P2 sends to a timestamped log file, and
runs until you tell it to stop.

```command
pnut-term-ts --headless -r test.bin -p P9cektn7
```

Everything you know about downloading from Part 2 still applies — `-r` versus
`-f`, the reset control line, the automatic debug baud — because the download
path is the same. What changes is that there are no debug windows and no
terminal: the program's output goes to the log instead of the screen.

Between the full GUI and fully headless sit two in-between modes you may reach for:

- **Headed batch** — a normal GUI run that *exits on its own* when the program
  signals it is done, draining any pending window SAVEs and logs first. Use it
  for scripted capture that still needs on-screen rendering:

  ```command
  pnut-term-ts -r gen.bin --exit-on-end-session -p P9cektn7
  ```

- **IDE integration** — a minimal UI meant to be driven by an editor such as the
  Spin2 VS Code extension:

  ```command
  pnut-term-ts --ide -p P9cektn7          # DTR reset
  pnut-term-ts --ide --rts -p P9cektn7    # RTS reset
  ```

# Chapter 13: Ending a Run Cleanly

A person closes the GUI when they are done. An automated run needs a defined way
to stop — and a way to tell success from failure without looking. PNut-Term-TS
gives you both.

## Three ways to stop

A headless run ends on any of:

- a **signal** — `Ctrl+C` or `SIGTERM`;
- a **timeout** — `--timeout <seconds>`, which stops the run after a fixed time;
- an **end marker** — `--end-marker`, which stops the run when a phrase appears in
  the output.

```command
pnut-term-ts --headless -r test.bin --end-marker    # stop on the marker
pnut-term-ts --headless -r test.bin --timeout 60    # stop after 60s
```

By default the end marker matches either `END_SESSION` or `DEBUG_END_SESSION`
(a case-sensitive match anywhere in the output), so a program that prints one of
those when it finishes will end the run by itself. Give `--end-marker "PHRASE"` to
match your own phrase instead. The same marker mechanism drives the headed-batch
`--exit-on-end-session` mode from Chapter 12.

## Exit codes — how a script reads the outcome

When PNut-Term-TS exits it returns a code, and **the codes are the same whether
you ran with the GUI or headless**, so a launching script can branch on `$?`
identically either way:

| Code | Meaning |
|------|---------|
| 0 | Clean exit — all SAVEs and logs flushed |
| 1 | Port / device error — the command was valid; the hardware was not there |
| 2 | Bad command line — nothing ran |
| 3 | Download failed |
| 124 | Headless `--timeout` expired |
| 125 | Shutdown drain exceeded its timeout — output may be incomplete |

One thing worth knowing about code 2: the command line is checked **before
anything runs**. If an option is wrong, PNut-Term-TS reports *every* problem with
it at once and exits — no device is touched, no download attempted, no window
opened.

# Chapter 14: The Log Is Your Feedback Loop

In headless mode the log file is not a side effect — **it is the whole point.** It
is how an automated caller, or an assistant reading back the behavior of code it
just wrote, sees what the P2 did. So it is worth understanding what the log holds
and what it deliberately keeps out.

## Program output stays clean

The log's first job is to carry your program's output — its `DEBUG()` text —
**complete and unpolluted**, because that text is what the automated reader is
there to see. PNut-Term-TS keeps that stream clean and adds only a thin layer of
run narrative alongside it: window-placement notices, download start / success /
failure, the baud and reset lines, and any directive errors or warnings (the ones
that help you fix a bad `debug()` directive). The tool's own internal
transport chatter is kept *out* of released builds entirely, so it can never
crowd out the output you came for.

## What a log is named, and what it records

Each run writes a timestamped file to the log directory (by default `./logs/`,
next to where you launched the run, so logs land beside the program that produced
them). The names are:

| Log | File name |
|-----|-----------|
| Debug log (headed runs) | `debug_YYMMDD-HHMMSS.log` |
| Headless log | `headless_YYMMDD-HHMMSS.log` |
| USB traffic log | `usb-traffic_YYMMDD-HHMMSS.log` |

Every log begins with a banner that records **which build produced it** —
`PNut-Term-TS: vX.Y.Z` — because a captured log is often kept as regression
evidence, and evidence has to say what version it came from. A P2 reset starts a
fresh log file, so each file reads as a single clean run.

## The USB traffic log

For the times you need to see the raw bytes on the wire, turn on the **USB traffic
log** with `-u` (`--log-usb-trfc`). It captures the runtime byte conversation —
everything exchanged once the P2 is running:

- the `DEBUG()` stream coming *from* the P2, and
- everything the host sends *back* — typed terminal input, `PC_KEY` / `PC_MOUSE`
  forwarding, and single-step-debugger responses.

Direction coverage depends on the mode, and this is by design: a **headed** run
captures both directions, while a **headless** run is **receive-only** — nothing
in the headless path sends bytes to the P2 after the download, so there is no
transmit side to record.

Two things the USB log deliberately does **not** contain: the reset and handshake
that *get* the program running, and the downloaded binary image itself — logging
the image would bury the interesting bytes under hundreds of kilobytes of hex.
One consequence is worth remembering: **an empty USB traffic log is meaningful.**
It means the P2 never produced any runtime traffic — most often because the
download failed and the program never started.

# Chapter 15: A Complete Automated Run

Putting Part 3 together, here is the shape of a hardware-in-the-loop run an
assistant or a CI job can drive end to end: **download, run, stop on a marker,
then read the log.**

Have your program print a known phrase when it finishes — for example a line
containing `DEBUG_END_SESSION` — so the run ends by itself. Then:

```command
pnut-term-ts --headless -r build/test.bin -p P9cektn7 --end-marker
```

When the marker appears, PNut-Term-TS flushes and exits. The caller then does two
things:

1. **Checks the exit code.** `0` means a clean finish; a non-zero code (Chapter
   13) says what went wrong — `3` for a failed download, `124` for a timeout, and
   so on — without any need to read the log.
2. **Reads the log.** The freshest `headless_*.log` in `./logs/` holds the
   program's `DEBUG()` output — the actual behavior of the code under test, ready
   to be parsed, compared against an expected result, or fed back to the
   assistant that wrote the program.

That download → run → marker → read cycle is the loop that lets a program, rather
than a person, develop and verify P2 code on real silicon.

## The agent in the loop

That cycle is what makes this tool the runtime end of an *agentic* P2 workflow —
an assistant that writes P2 code, compiles it, runs it on real silicon, and reads
the log back to decide what to do next. Seen that way, the tool chain of Chapter 1
gains one more member, because an assistant needs a source for what it is writing
about:

| Tool | Its job |
|------|---------|
| **P2KB MCP** | Serves the P2 knowledge base — the instruction set, the language, the silicon — to an assistant that is writing P2 code. |
| **`pnut-ts`** | The Spin2 / PASM2 compiler. Turns that source into a binary the P2 can run. |
| **`pnut-term-ts`** | *This tool.* Downloads the binary, runs it, and writes back what the P2 said. |

```{=latex}
\begin{figure}[H]
\centering
\diagramscale{
\begin{tikzpicture}
\node[iospbox] (agent) {your\\AI agent};
\node[iospbox, right=14mm of agent] (compile) {\texttt{pnut-ts}\\compiler};
\node[iospkey, right=16mm of compile] (term) {\texttt{pnut-term-ts}\\download + observe};
\node[iospbox, right=26mm of term] (p2) {Propeller~2\\silicon};
\node[iospbox, above=9mm of agent] (mcp) {P2KB MCP\\knowledge};
\node[iospbox, below=15mm of term] (log) {the log file\\\texttt{./logs/}};
\node[iospsub, below=1.5mm of log] (logsub)
   {\texttt{headless\_*.log}};
\draw[iospflow] (mcp) -- (agent);
\draw[iospflow] (agent) -- node[above, font=\scriptsize]{Spin2} (compile);
\draw[iospflow] (compile) -- node[above, font=\scriptsize]{\texttt{.bin}} (term);
% The serial link is a TWO-WAY conversation, and both directions terminate at
% pnut-term-ts -- never at the agent. Drawn as a matched pair rather than one
% arrow, because the return leg is the whole point of the figure.
\draw[iospflow] ([yshift=2mm]term.east) --
   node[above, font=\scriptsize]{run} ([yshift=2mm]p2.west);
\draw[iospflow] ([yshift=-2mm]p2.west) --
   node[below, font=\scriptsize]{\texttt{debug()}} ([yshift=-2mm]term.east);
\draw[iospflow] (term) -- node[right, font=\scriptsize]{writes} (log);
\draw[iospflow] (log.west) to[out=180, in=-90, looseness=0.7]
   node[pos=0.42, below, yshift=-2pt, inner sep=2pt, font=\scriptsize]
   {the agent reads the log} (agent.south);
\end{tikzpicture}
}
\caption{Where PNut-Term-TS sits in the P2 agentic tool chain. With no windows to
watch, the loop closes through the \emph{log file} rather than through a direct
line from the chip: everything the P2 sends comes back to PNut-Term-TS, which
writes it to a log, and it is that log the agent reads.}
\end{figure}
```

Follow how that loop closes, because the shape of it is the whole point. The agent
does not read the P2 directly. **Everything the P2 sends comes back to
PNut-Term-TS, which writes it to a log file in the `logs` folder — and it is that
file the agent reads.** At your desk that log sits alongside what you are already
watching on screen, a record you may never open. Here there is no screen, so the
log is not a convenience bolted on the side: it *is* the return path, and it is
the reason a program can take the place of the person who used to watch.

That agent-in-the-loop way of working is the subject of **The P2 Architect's
Guide, Part 3**, which names this very tool chain — `pnut-ts`, `pnut-term-ts`, and
the Knowledge Base — as what lets a hosted agent close the write-compile-run-read
loop on its own. This guide is the operating manual for the tool that makes it
possible.

# Part 4: Reference

The material both paths point into: the full command-line reference, the keyboard
shortcuts, troubleshooting, and where to go for more.

# Chapter 16: Command-Line Reference

This same list is built into the tool — run `pnut-term-ts --help` for it at any
time.

```command
pnut-term-ts [options]
```

| Option | Long form | Argument | Description |
|--------|-----------|----------|-------------|
| `-r` | `--ram` | file | Download the file to **RAM** and run |
| `-f` | `--flash` | file | Download the file to **FLASH** and run |
| `-p` | `--plug` | device | Use the device at `<device>` (path or serial; partial match OK). Auto-detects if exactly one is present |
| `-b` | `--debugbaud` | rate | **Override** the debug baud rate — normally unnecessary (Chapter 6) |
| `-n` | `--dvcnodes` | | List detected USB serial devices and exit |
| `-m` | `--match-vendor-only` | | With `-n`, list any FTDI device, not just PropPlugs |
| `-d` | `--debug` | | Emit detailed diagnostic messages |
| `-v` | `--verbose` | | Emit verbose messages |
| `-q` | `--quiet` | | Suppress the banner and non-error text |
| `-u` | `--log-usb-trfc` | | Write a timestamped USB-traffic log |
| | `--ide` | | IDE-integration mode (minimal UI) |
| | `--rts` | | Use RTS instead of DTR for reset (overrides the per-device setting) |
| | `--console-mode` | | Console output mode |
| | `--headless` | | Run with no GUI (file logging only) |
| | `--timeout` | seconds | Exit after N seconds (**headless only**) |
| | `--end-marker` | [phrase] | Exit when `phrase` appears; with no value, matches `END_SESSION` / `DEBUG_END_SESSION` |
| | `--exit-on-end-session` | | GUI batch: exit on the end-session marker, draining first |
| `-V` | `--version` | | Print the version |
| `-h` | `--help` | | Show help |

**Constraints.** `-r` and `-f` are mutually exclusive. `--timeout` requires
`--headless`. `--end-marker` requires `--headless` or `--exit-on-end-session`, and
its phrase cannot be empty. The command line is validated before anything runs;
any error is reported in full and the tool exits with code 2.

**Examples.**

```command
pnut-term-ts -n                                  # list devices
pnut-term-ts -r prog.bin -p P9cektn7             # RAM download (GUI)
pnut-term-ts -f prog.bin                         # FLASH download
pnut-term-ts -p P9cektn7 -u                      # enable USB logging
pnut-term-ts --ide --rts -p P9cektn7             # IDE mode, RTS reset
pnut-term-ts --headless -r test.bin --end-marker # headless, exit on marker
pnut-term-ts --headless -r test.bin --timeout 60 # headless, exit after 60s
```

# Chapter 17: Keyboard Shortcuts

Application-level shortcuts (use `Cmd` instead of `Ctrl` on macOS):

| Shortcut | Action |
|----------|--------|
| `Ctrl+R` | Start Recording |
| `Ctrl+P` | Playback Recording |
| `Ctrl+Q` | Exit |
| `Ctrl+,` | Preferences |
| `Ctrl+F` | Find in terminal |
| `F1` | Documentation |

Cut / Copy / Paste use your platform's standard keys in any text field. Inside a
debug window, mouse and key input may be forwarded to the running program when it
asked for them (`PC_MOUSE` / `PC_KEY`); dragging a display window shows its
position in the title bar (Chapter 8).

# Chapter 18: Troubleshooting

**The P2 is not detected.** Check the USB cable and that the P2 is powered. Run
`pnut-term-ts -n` to see whether it enumerates. Install FTDI drivers if needed and
try another port. On Linux and macOS, check serial-port permissions (below).

**Text is garbled or missing.** Almost always a baud mismatch, and which way to
fix it depends on where the binary came from. If you built with PNut or `pnut-ts`
and passed `-b`, **try dropping it** — those images are auto-detected and carry
their own debug baud (Chapter 6); watch for the warning that `-b` disagrees with
the binary. If you built with **any other toolchain**, or you are attaching to an
*already-running* P2, there is no rate for us to read, so it is the opposite move:
set the rate yourself with `-b` or the Default Baud Rate preference. Common
rates are 115200, 921600, and 2000000.

**The P2 does not reset or the program does not start.** The reset control line
may be wrong for your adapter. Set **DTR** or **RTS** for the device in PropPlug
Management, or pass `--rts` for the session. Parallax PropPlugs use DTR; some
clones use RTS.

**A window is blank or data is missing.** Confirm the program is actually running
and sending `debug()` output. Open the Performance Monitor; if buffer usage is
high, lower the data rate.

**Recording problems.** Check free disk space and write permission to the
recordings directory, and stop any recording in progress before starting a new
one.

**Platform notes.**

- **Windows** — if port access is denied, make sure no other program holds the COM
  port; confirm the COM number in Device Manager.
- **macOS** — grant serial access if prompted; devices appear as
  `/dev/tty.usbserial-*`.
- **Linux** — add your user to the `dialout` group
  (`sudo usermod -a -G dialout $USER`, then log back in); devices appear as
  `/dev/ttyUSB*`.

# Chapter 19: Support and Resources

- **Report an issue** — the PNut-Term-TS GitHub issue tracker.
- **The `debug()` display directives** — the official Parallax P2 DEBUG
  documentation, and the **P2 Debug Window Manual** for the display windows.
- **The single-step debugger** — the **P2 Single-Step Debugger Manual**.
- **Agentic P2 development** — **The P2 Architect's Guide, Part 3**, for the
  tool-chain workflow this guide's tool takes part in.
- **The Propeller 2** — the Parallax Propeller 2 documentation and the Parallax
  Forums.

<!--
  ===========================================================================
  FIGURES — 9 slots, all real (no placeholders).
  - 4 TikZ diagrams: workflow position, user-facing [Ch1], three-in-one identity
    [Ch2], Automatic Window Placement order [Ch8], agentic tool chain [Ch15].
    Ch1 and Ch15 are a deliberate PAIR on the same spine: same nodes, same
    left-to-right flow, different return leg — the screen for a person, the log
    for an agent. Keep them visually parallel; that parallel IS the teaching.
  - 5 screenshots (Stephen's captures, staged as inbox/assets/*.png):
    main-window-and-logger [Ch5] · multi-window-desktop [Ch8] ·
    single-step-debugger [Ch9] · preferences-user-settings [Ch10] ·
    preferences-propplug [Ch10].
  Recording/playback + performance monitoring are de-emphasized into Ch 11
  "Further Features" — no screenshots for those.
  ===========================================================================
-->

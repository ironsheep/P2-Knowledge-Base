# PNut-Term-TS User Guide Changelog

## v1.0.0 (2026-08-19): Initial public release

**Initial release.** The operating guide for **PNut-Term-TS** — the downloader, serial
terminal, and debug display for the Propeller 2, in one program that runs the same way on
every platform. It replaces Parallax Serial Terminal, hosts the `debug()` display windows
and the single-step debugger, and does all three without a specific operating system.

The guide forks by intent after a shared orientation: one opening places the tool in your
workflow, then the reading splits into the GUI path and the headless command-line path so
you follow only the half you work in. It states the tool's compiler independence outright
— downloading is the P2's own boot protocol, so a binary from any toolchain downloads and
runs — and is plain about the one place toolchains differ: PNut and `pnut-ts` images are
auto-detected and carry their own debug baud rate, and a debug build from anything else
needs `-b`.

**The opening teaches the loop you can actually see.** Chapter 1 places the tool in the
workflow as *you* operate it: you compile, PNut-Term-TS downloads and runs, and what the
P2 sends comes back to your terminal and debug windows, with a log written alongside as a
record. The automated form of that loop — where an agent stands in for the person, P2KB
MCP supplies what it knows about the P2, and the log becomes the only return path because
there is no longer a screen — is taught in Chapter 15, once the headless run, its exit
codes, and its log are in hand. The two chapters carry matching diagrams of one spine, and
the difference between them is the lesson: **who is watching decides what the return path
is.**

Ships with four TikZ diagrams and five screenshots. Co-released with the *P2 Single-Step
Debugger Manual*, which covers driving the debugger itself.

## v0.9.0 (2026-08-12): Tool developer review draft — compiler compatibility

**Not a public release.** This draft circulates only to the outside tool authors
whose products it now describes, and it carries four questions addressed to them
by name. It is not releasable as it stands, and a gate enforces that.

**New: the downloader's compiler independence is stated outright.** The guide had
only ever named `pnut-ts`, which left a reader to conclude this tool wants their
toolchain changed. It does not. Downloading is the P2's own boot protocol, so any
binary that downloads and runs will download and run here — **PNut**, **`pnut-ts`**,
**FlexSpin** and **Spin Tools IDE** are named, and anything else that builds for
the P2 is covered by the general rule rather than by a list we would have to
maintain.

**What comes back is now stated as one rule about the bytes, not about compilers**
(Chapter 2): debug output formed as *Parallax Spin2 Documentation v55* specifies is
routed to the debug log and the debug windows; anything else the program writes to
the serial port appears in the terminal. Both outcomes are given, so a program
built *without* debug reads as a supported case rather than an omission — its
output still arrives, in the terminal. This also tells another compiler author how
to become fully supported: the format is public, and emitting it is the whole
requirement.

**The one place compilers genuinely differ is now named** (Chapter 6). The guide
previously hedged — `-b` existed for "a toolchain we do not recognize" — which
named a limitation without telling anyone it was about them. PNut and `pnut-ts`
write the debug baud rate into the image; a FlexSpin binary does not carry a rate
this tool can read, so that user sets it with `-b` or the Default Baud Rate
preference. Chapter 18's garbled-text entry now routes both ways from the same
fact: drop `-b` if you built with PNut/`pnut-ts`, supply it if you built with
FlexSpin.

**Four questions to the tool authors**, in violet `tool-review` boxes, with a
roadmap page after the cover so each reviewer can find their own:
- **Ch.2** — *Marco Maccaferri*: confirm or correct our description of Spin Tools
  IDE as fully supported (debug windows and the debugger).
- **Ch.2** — *Eric Smith*: does FlexSpin's `debug()` output reach the display
  windows, or debug text only?
- **Ch.6** — *Eric Smith*: does a FlexSpin binary really carry no readable debug
  baud rate?
- **Ch.9** — *Eric Smith*: can FlexSpin compile in the debugger kernel that the
  single-step debugger needs? (Codegen, not stream format — the one capability a
  compiler cannot reach by emitting the right bytes.)

Where an answer spans both this guide and the *P2 Single-Step Debugger Manual*, it
will be written into both; the two co-release.

**Platform:** new `ToolReviewBlock` in `p2kb-platform-content.sty` (violet, square
corners, dashed border — deliberately unlike the rounded advisory family, so it
reads as scaffolding) and the `::: {.tool-review who="…"}` fence in
`p2kb-platform-code-coloring.lua`. There is **no draft switch that hides these**,
because a hidden question is one nobody answers; instead
`tools/validation/audit-review-scaffolding.py` **fails the release** while any box
survives. Render-verified on the Forge: box renders, title tracks the addressee,
lists/tables/code spans work inside it, compile clean.

## v0.1.0 (2026-07-21): Element seeded (no content yet)

Standing structure for a new user guide documenting **PNut-Term-TS**, the
cross-platform desktop debug terminal for the Propeller 2. This is a *tool* user
guide (`doc_class: behavior`), not a P2 silicon or language reference.

Seeded:
- Voice guide (adapted from the Single-Step Debugger Manual, its closest
  sibling, same host application, same "operate this tool" register).
- Creation guide, MANUAL-DESCRIPTOR, and PLANNING chapter outline.
- Front matter (title, subtitle, license) and this changelog.
- Two authoritative feeds copied into `REF-NO-COMMIT/` from the PNut-Term-TS
  repo (v0.10.3, 2026-07-20): `User-Guide-FEED.md` and
  `LOGGING-STANDARDS-FEED.md`.
- Workspace build scaffolding (assemble script, request descriptor) and the
  PUBLICATION-ROSTER entry (In progress · Type = guide).

**Design intent settled** the same day (see `creation-guide.md` / `PLANNING.md`):
- **Purpose = positioning** within the P2 agentic tool chain (P2KB MCP +
  `pnut_ts` + `pnut_term_ts`, optional Spin2 VS Code extension); delivers the
  agentic usability of **The P2 Architect's Guide, Part 3**.
- **Identity = three tools in one**: downloader · Parallax Serial Terminal
  replacement · PNut debug-window replacement/production (now cross-platform).
- **Pedagogy = shared orientation trunk → fork by intent** (GUI vs headless).
- **Automatic Window Placement** is a called-out GUI headline.
- **Subtitle:** *The Cross-Platform Downloader, Terminal, and Debug Display for
  the Propeller 2.*
- **Release gate:** co-releases with the P2 Single-Step Debugger Manual, timed to
  PNut-Term-TS v1.0.

No body chapters drafted. Next: draft Book 0 (orientation) from the two feeds
following the voice guide; first render pending Forge template wiring (TBD, see
PLANNING).

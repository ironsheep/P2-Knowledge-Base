# Planning — PNut-Term-TS User Guide

**Status:** SEED + design intent settled (2026-07-21). Standing structure
created; no content drafted.
**Slug:** `pnut-term-ts-user-guide` · **Type:** guide · **doc_class:** behavior

---

## Title block (decided with Stephen, 2026-07-21)

- **Title:** PNut-Term-TS User Guide
- **Subtitle:** The Cross-Platform Downloader, Terminal, and Debug Display for the Propeller 2
- **Author:** Iron Sheep Productions, LLC
- **Starting version:** v0.1.0 (draft)

The name is a feature-acronym — **PNut-Term-TS** = "PNut **Term**inal,
**T**ype**S**cript." The subtitle decodes the three-in-one identity on the cover;
the name is reused as a mnemonic for that scope in the orientation trunk.

## Purpose — tool-chain positioning

Primary job is **positioning**, not just operation (see `creation-guide.md` §0).
This tool is the *runtime/observation* leg of the P2 **agentic tool suite**:

- **P2KB MCP** + **`pnut_ts`** + **`pnut_term_ts`** (this tool), optional **Spin2
  VS Code extension**.
- Delivers the agentic usability described in **The P2 Architect's Guide,
  Part 3** (bidirectional cross-reference).

**Identity = three tools in one:** downloader · Parallax Serial Terminal
replacement · PNut debug-window replacement/production (now cross-platform).

## Sources

Two feeds, snapshotted from the PNut-Term-TS repo (v0.10.3, 2026-07-20), in
`./REF-NO-COMMIT/`:

- `User-Guide-FEED.md` — the structural backbone.
- `LOGGING-STANDARDS-FEED.md` — logging behavior, folded into the guide per
  Stephen's authoring note (not shipped as a standalone chapter).

See `creation-guide.md` §1 (grounding) and §4 (cross-references out — do not
reproduce the `debug()` directive spec, the Debug Window Manual's windows, or
the Single-Step Debugger Manual).

## Structure — shared trunk, then fork (three books in one)

Pedagogy: teach the conceptual model once, then fork by intent (GUI vs headless).
See `creation-guide.md` §2–§3.

### Book 0 — Orientation (everyone reads, before the fork)
1. Where this sits — the agentic tool suite; the Architect Part-3 link.
2. Three tools in one — downloader / PST replacement / debug-window engine;
   cross-platform; the name-as-mnemonic.
3. The two stances — **headed (GUI)** and **headless (automation)**, side by side,
   so the reader self-identifies (both are know-this-immediately facts).
4. **The fork** — explicit router: at your desk → Book A; automating P2 runs
   (CI / container / agent-in-the-loop) → Book B.
   *(Trunk diagrams: (1) tool-chain position; (2) three-in-one identity.)*

### Book A — GUI branch
5. The Main Window — toolbar, text-entry, terminal/log display, status bar.
6. Downloading & Running — RAM vs flash; reset control line (DTR/RTS); the
   "you should not need to set baud" behavior.
7. The Serial Terminal — sending input, echo, terminal modes/themes (PST vs ANSI).
8. Debug Windows + **Automatic Window Placement** — windows open automatically
   from `debug()`; auto-layout (no need to `POS` every window); drag to read
   coordinates and bake a `POS` back into source; SAVE; PC_KEY/PC_MOUSE.
   *(Cross-ref OUT: Debug Window Manual for what each window is / how to author.)*
9. The Single-Step Debugger interface — how this tool renders and drives it.
   *(Cross-ref OUT: Single-Step Debugger Manual for using the debugger.)*
10. Recording & Playback — `.p2rec`, capture, replay with timing.
11. Performance Monitoring — throughput / buffers / queue depth / message counts.
12. Menus & Settings (GUI) — macOS native vs Windows/Linux in-window (NOT
    equivalent); the 3-tier settings hierarchy; PropPlug / device management.

### Book B — Headless branch
13. Headless invocation — `--headless`, download, device selection.
14. Ending a run — `--end-marker` / `--timeout`; the end-session markers.
15. Exit codes — 0/1/2/3/124/125; branching on `$?` (identical GUI vs headless).
16. **The log as the automation feedback loop** — program output stays clean;
    canonical as-built filenames; version banners; reading the log as the agent's
    window into its own code.
17. USB traffic log — scope (runtime bytes both directions headed; RX-only
    headless); when an empty log is meaningful.
18. CI / agent-in-the-loop patterns — a complete *"your first automated run"*
    recipe (download → run → end-marker → read the log).

### Shared reference tail (both branches point in)
19. Command-Line Reference — full option table, examples, constraints.
20. Keyboard Shortcuts.
21. Settings hierarchy (full reference).
22. Troubleshooting — not detected / garbled / no reset / blank window /
    recording problems / platform notes.
23. Support & Resources.

*(Chapter grouping/numbering to firm up as drafting begins; the Book 0 → A/B →
tail spine is the fixed decision.)*

## Release gate

**Co-releases with the P2 Single-Step Debugger Manual, timed to PNut-Term-TS
v1.0** (Debug Window Manual already released). Draft-and-hold to v1.0: draft now
against v0.10.3, track the tool, **re-pull the feeds + re-verify at release.**

## Open items / decisions to finalize before first render

- **Forge template — BASELINE ESTABLISHED (2026-07-21).** `p2kb-pnut-term-ts.latex`
  (in `workspace/.../templates/`, based on the SSDB template's minimal
  platform-stack loader — loads only the three shared `p2kb-platform-*` layers,
  no manual-specific `.sty`). Proven by a clean `forge-test` round-trip of Book 0
  (`pnut-term-ts-test-v1`: 9pp, compile-log clean, all content present — cover,
  Part/Chapter promotion, platform tables, inline mono, fork router). Production
  `request.json` now points at it. *Open sub-decision:* whether a `# Part N`
  should get its own **part-divider page** — currently `\manualpart` renders the
  Part heading inline atop the first chapter (Part 1 + Chapter 1 share a page).
  Acceptable for now; revisit if we want divider pages.
- **Figure slots — PLACEHOLDERS IN PLACE (2026-07-21).** 10 `\placeholderfig`
  boxes carry capture/authoring notes + real captions (figure numbers + LoF
  entries reserved). Swap each `\placeholderfig` → `\screenshotfig{inbox/assets/…}`
  (or TikZ) as assets land.
  - **7 SCREENSHOTS (Stephen to capture):** (1) main window [Ch5], (2) several
    debug windows auto-placed on screen, one mid-drag showing x,y [Ch8],
    (3) single-step debugger window, macOS/Linux preferred [Ch9], (4) playback
    transport strip [Ch10], (5) Performance Monitor [Ch11], (6) Preferences ·
    User Settings tab [Ch12], (7) Preferences · PropPlug Management tab [Ch12].
    Land captures in `./screenshots/` → then `inbox/assets/` at build.
  - **3 DIAGRAMS (Claude to author, TikZ):** tool-chain position [Ch1],
    three-in-one identity [Ch2], Automatic Window Placement order [Ch8].
- **Examples** — command-line recipe snippets go under `./examples-library/`.
- **Re-pull check** — confirm the feeds still match the repo (v0.10.3+) before
  release.

## Status log

- **2026-07-21** — Element seeded (folders + guides + descriptor + front-matter +
  changelog + body stub; two feeds copied to `REF-NO-COMMIT/`; roster row +
  Freshness-ledger entry). **Design intent settled** same day: purpose =
  tool-chain positioning; three-in-one identity; shared-trunk→fork pedagogy;
  Architect Part-3 cross-reference; Automatic Window Placement as a GUI headline;
  subtitle #3; v1.0 co-release gate with the Single-Step Debugger Manual. No
  content drafted.

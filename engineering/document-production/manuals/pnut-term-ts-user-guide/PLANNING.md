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

- **P2KB MCP** + **`pnut-ts`** + **`pnut-term-ts`** (this tool), optional **Spin2
  VS Code extension**.
- Delivers the agentic usability described in **The P2 Architect's Guide,
  Part 3** (bidirectional cross-reference).

**But positioning ≠ positioning up front.** Per the `creation-guide.md` §0
placement rule, the agentic frame — agents, AI assistants, P2KB MCP, and the
Architect Part-3 link — is delivered **in Book B (headless), never in the
trunk**. The trunk's tool-chain diagram shows the chain **as a person operates
it**; Book B redraws the same spine with the agent added. See §0 for why: the
"loop closes through the log" claim is false for a person at the GUI.

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
1. Where this sits — the compile / run-and-observe chain **as you operate it**.
   Agent-free: no agents, no P2KB MCP, no Architect Part-3 link (§0 rule).
2. Three tools in one — downloader / PST replacement / debug-window engine;
   cross-platform; the name-as-mnemonic.
3. The two stances — **headed (GUI)** and **headless (automation)**, side by side,
   so the reader self-identifies (both are know-this-immediately facts).
4. **The fork** — explicit router: at your desk → Book A; automating P2 runs
   (CI / container / scripted hardware runs) → Book B.
   *(Trunk diagrams: (1) workflow position, user-facing; (2) three-in-one
   identity.)*

### Book A — GUI branch (Part 2) — AS BUILT
5. The Main Window — toolbar, text-entry, terminal display, status bar.
6. Downloading and Running — RAM vs flash; reset control line (DTR/RTS); the
   "you should not need to set baud" behavior.
7. The Serial Terminal — sending input, echo, terminal modes/themes (PST vs ANSI).
8. Debug Windows and **Automatic Window Placement** — windows open automatically
   from `debug()`; auto-layout; drag to read coordinates; SAVE; PC_KEY/PC_MOUSE.
   *(Cross-ref OUT: Debug Window Manual.)*
9. The Single-Step Debugger — how this tool renders/drives it.
   *(Cross-ref OUT: Single-Step Debugger Manual.)*
10. Menus, Settings, and Devices — macOS vs Windows/Linux menus; 3-tier settings;
    PropPlug / device management.
11. **Further Features** *(de-emphasized 2026-07-21, honest caveats)* — recording
    & playback (present but lightly tested — experimental) and performance
    monitoring (developer/diagnostic aid). Kept out of the main flow on purpose;
    UI references elsewhere point here. **Not illustrated.**

### Book B — Headless branch (Part 3) — AS BUILT
12. Running Headless — `--headless`, download, device selection; the in-between
    modes (headed batch `--exit-on-end-session`, IDE `--ide`).
13. Ending a Run Cleanly — `--end-marker` / `--timeout`; the exit codes
    (0/1/2/3/124/125), identical GUI vs headless.
14. The Log Is Your Feedback Loop — program output stays clean; canonical
    as-built filenames; version banners; the USB traffic log (direction by mode).
15. A Complete Automated Run — the download → run → marker → read recipe.

### Shared reference tail (Part 4) — AS BUILT
16. Command-Line Reference — full option table, examples, constraints, exit codes.
17. Keyboard Shortcuts.
18. Troubleshooting — not detected / garbled / no reset / blank window / platform.
19. Support and Resources.

*(19 chapters as built. The Book 0 → A/B →
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
  - **ALL 5 SCREENSHOTS WIRED (2026-07-21)** — Stephen's captures, canonical
    copies in `./screenshots/` + build copies in `workspace/.../assets/`,
    referenced as `inbox/assets/*.png`, all verified rendering (forge-test
    v6/v7/v8): (1) `main-window-and-logger` [Ch5, cropped — the two startup
    windows], (2) `multi-window-desktop` [Ch8 — several display windows
    auto-placed on a full desktop; main window + Debug Logger in the bottom
    reserved cells, matching the Ch8 diagram], (3) `single-step-debugger`
    [Ch9, macOS], (4) `preferences-user-settings` [Ch10], (5) `preferences-propplug`
    [Ch10]. **No placeholders remain — all 8 figures (3 diagrams + 5 screenshots)
    are real.**
    *(Transport-strip + Performance-Monitor shots dropped when recording/perf were
    de-emphasized into Ch 11.)*
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

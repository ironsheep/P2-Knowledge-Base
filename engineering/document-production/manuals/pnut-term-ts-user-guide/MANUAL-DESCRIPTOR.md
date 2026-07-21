---
manual_slug: pnut-term-ts-user-guide
doc_class: behavior                               # software-tool user guide — grounds against source-extraction (repo feeds), NOT language YAML
code_line_budget_K: 76                            # platform-inherited default (LM-Mono reference K); revisit if this guide adopts a different template
last_published_tag:                               # none yet — seed created 2026-07-21, not yet released
guide_paths:
  creation_guide: ./creation-guide.md
  voice_guide: ./voice-guide.md
  style_guide: ./voice-guide.md                   # no separate style-guide; voice-guide.md carries voice + style conformance
  planning: ./PLANNING.md
authoritative_sources: see ./creation-guide.md    # behavior-guide grounding; the two REF-NO-COMMIT feeds + the live PNut-Term-TS repo are the "Bible"
source_highlights:
  - ./REF-NO-COMMIT/User-Guide-FEED.md            # PRIMARY — operating modes, main window, menus, settings, device mgmt, recording, CLI reference, troubleshooting (← repo DOCs/USER-GUIDE.md, v0.10.3)
  - ./REF-NO-COMMIT/LOGGING-STANDARDS-FEED.md      # PRIMARY — logging principles, four content buckets, USB traffic log, canonical as-built filenames (← repo project-specific/LOGGING-STANDARDS.md)
  - ./REF-NO-COMMIT/WINDOW-LAYOUT-FEED.md          # PRIMARY — auto window-placement algorithm (adaptive grid; Half-Moon Descending center-out fill; reserved Main/Logger cells; cascade-when-full; Debugger + COG-grid strategies). Code-accurate from src/utils/windowPlacer.ts; currency v0.10.8
  - https://github.com/ironsheep/PNut-Term-TS      # source of truth if a feed is stale — re-pull the feeds, do not edit snapshots in place
high_risk_tables:
  - "Command-Line Reference options table (option / long form / argument / description) — many rows; verify each vs the tool's actual --help and validation"
  - "Exit codes table (0/1/2/3/124/125) — same codes GUI and headless; a launching script branches on these, so each meaning must be exact"
  - "Settings hierarchy tables (Terminal / Serial Port / Logging / Recordings / Debug Logger — option / options / default) across the three Preferences tabs"
  - "Menu tables — macOS native menu vs Windows/Linux in-window menu bar are NOT equivalent; File/Help/Find/Clear are Win/Linux-only; accelerators differ (Cmd vs Ctrl)"
fragile_areas:
  - "Debug baud — do NOT tell the reader to set -b routinely: on -r/-f download the rate is read from the binary. Precedence: -b flag -> binary's rate -> project -> global -> 2,000,000. -b is an override for attach-to-running / unknown-toolchain only."
  - "Log filenames — use ONLY the as-built canonical names (debug_/headless_/usb-traffic_ + YYMMDD-HHMMSS). The feed's {Prefix}_{Ctx}_{YYYYMMDD}_{HHMMSS} scheme is ASPIRATIONAL and UNIMPLEMENTED — never document it as current."
  - "USB traffic log direction differs by mode BY DESIGN: headed = bi-directional; headless = receive-only (no transmit path exists after download). An empty USB log is meaningful (P2 produced no runtime traffic — usually a failed download)."
  - "Reset control line — DTR (Parallax PropPlugs / most FTDI) vs RTS (some clones); stored per device; --rts overrides for a session. Not set in the Logging/Serial tabs — it's in PropPlug Management."
  - "Operating modes are five and distinct (interactive GUI / command-line download / headed batch --exit-on-end-session / IDE --ide / headless --headless); --timeout and --end-marker are headless/batch-gated. Don't conflate them."
  - "Names — application is PNut-Term-TS (invocation pnut-term-ts); compiler is pnut_ts; there is no 'PNut IDE' / pnut.exe. Debug display windows open automatically from debug() directives, never from a menu."
  - "Scope boundary — do NOT reproduce the debug() directive syntax (Parallax P2 DEBUG spec / Debug Window Manual) or teach the single-step debugger (its own manual). This tool DISPLAYS/PRODUCES what those manuals DESCRIBE. Cross-reference only."
  - "Positioning claims — the agentic tool suite (P2KB MCP + pnut_ts + pnut_term_ts, optional Spin2 VS Code extension) and the bidirectional link to The P2 Architect's Guide Part 3 are load-bearing framing; verify the suite membership + the Part-3 relationship stay accurate as those docs evolve."
---

# PNut-Term-TS User Guide — Descriptor

Thin per-manual overlay read by `document-audit` (and `prepare-manual` /
`release-manual` / `document-finalize`). Everything not listed in the front
matter is inherited from the central skill bodies + the guides referenced above.

**Grounding-model note:** `doc_class: behavior`. This guide documents a
**software tool**, not the P2 chip — there is no language YAML for the subject.
The source of truth is the **PNut-Term-TS repository**, captured as the two
point-in-time feeds in `./REF-NO-COMMIT/` (current as of **v0.10.3**,
2026-07-20). Factual dimensions verify against *those* documents (and a fresh
re-pull if the repo advanced), **not** `deliverables/ai/P2/language/`; the
`p2kb-mcp` currency caveat does not apply. Where the tool's behavior and any
prose disagree, **the tool is ground truth.**

**Type note:** roster `Type = guide` (a user guide for a tool), but unlike the
off-platform AI Privacy Guide this one is expected to ride the `p2kb-platform`
template stack (it ships code blocks and screenshots like the manual siblings).
The Forge template + platform-filter wiring is **TBD** — to be finalized at first
render (see `PLANNING.md`).

**Release gate:** **co-releases with the P2 Single-Step Debugger Manual, timed to
PNut-Term-TS v1.0** (the P2 Debug Window Manual is already released).
Draft-and-hold to v1.0 — draft now against the v0.10.3 feeds, then **re-pull the
feeds + re-verify at release**.

**Baseline note:** `last_published_tag` is empty — this is a fresh seed
(2026-07-21), never released. Set it at first public release.

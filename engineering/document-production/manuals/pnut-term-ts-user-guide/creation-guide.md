# Creation Guide — PNut-Term-TS User Guide

**Status:** DRAFT (seed + design intent) — 2026-07-21
**Slug:** `pnut-term-ts-user-guide`
**Type:** guide · **doc_class:** behavior

This guide defines *what the PNut-Term-TS User Guide is* — its purpose, subject,
sources, structure, and the grounding discipline that keeps it trustworthy. The
companion `voice-guide.md` defines *how it reads*; `PLANNING.md` carries the
working chapter outline.

---

## 0. Purpose — positioning within the P2 agentic tool chain

The guide's primary job is **positioning**, not just operation. It documents
**PNut-Term-TS**, the cross-platform desktop debug terminal for the Propeller 2,
and its central task is to place that tool inside the P2 **agentic tool chain**
and explain what it is.

**The agentic tool suite:**
- **P2KB MCP** — the P2 knowledge base, served to an agent.
- **`pnut_ts`** — the Spin2/PASM2 compiler.
- **`pnut_term_ts`** (this tool) — the downloader + terminal + debug-window
  runtime that closes the hardware-in-the-loop observation loop.
- *(optional)* the **Spin2 VS Code extension** — editor with syntax + semantic
  highlighting.

This tool is the *runtime/observation* leg. **The P2 Architect's Guide, Part 3**
("The Same Work, with an Agent") walks the P2 design workflow with an agent in
the loop, and — in its Chapter 12 — names *this very tool chain* (`pnut_ts`,
`pnut_term_ts`, and the Knowledge Base) as the hosted set that lets an agent
close the write-compile-run-read loop on real silicon by itself. This guide is
the operating manual for that runtime leg, so Part 3 is a first-class
bidirectional cross-reference (§4). (Scope note: Part 3's *depth* is the
agent-collaboration methodology; the closed tool-chain loop is one well-drawn
element of it, not its whole subject — cite it as "names/describes," not
"treats in depth.")

### Identity — three tools integrated into one

The whole frame of the document. Each leg maps to reader value and to what it
replaces:
1. **Downloader** — get a compiled program onto the P2 (RAM or flash).
2. **Parallax Serial Terminal replacement** — the serial terminal / `DEBUG()`
   text stream.
3. **PNut debug-window replacement + production mechanism** — the visualization
   windows *and* the single-step debugger interface, **now cross-platform**
   (PNut's version is Windows-only). This is the reason it exists in TypeScript.

The name itself encodes this: **PNut-Term-TS** = "PNut **Term**inal,
**T**ype**S**cript." Use the name as a mnemonic for the three-in-one scope in
the orientation trunk (§3, Book 0).

**Is not:**
- a P2 silicon or language reference (this documents a *tool*, not the chip);
- a `debug()` **directive** reference — that syntax is the Parallax P2 DEBUG
  specification, cross-referenced here, not reproduced;
- the **P2 Debug Window Manual** or the **P2 Single-Step Debugger Manual** — this
  tool *displays and produces* what those manuals *describe*; it points to them,
  it does not teach them.

## 1. Grounding model — `doc_class: behavior`

There is no P2 language YAML for this subject. The authority is the
**PNut-Term-TS repository** and the point-in-time **feeds** snapshotted from it.
Where the tool's behavior and any prose disagree, **the tool (its source /
shipping build) is ground truth.** Re-pull the feeds when the repo advances
rather than editing the snapshots in place.

### Authoritative sources (the "Bible")

| Source | Role |
|--------|------|
| `REF-NO-COMMIT/User-Guide-FEED.md` | PRIMARY — operating modes, main window, menus, settings hierarchy, PropPlug/device management, recording & playback, performance monitor, debug-windows overview, full CLI reference, troubleshooting. (← repo `DOCs/USER-GUIDE.md`, v0.10.3) |
| `REF-NO-COMMIT/LOGGING-STANDARDS-FEED.md` | PRIMARY — logging principles: the four content buckets, program-output-stays-clean, USB traffic log scope + direction-by-mode, version banners, canonical as-built filenames. (← repo `project-specific/LOGGING-STANDARDS.md`) |
| The live **PNut-Term-TS** repo | Source of truth if a feed is stale — `https://github.com/ironsheep/PNut-Term-TS` |

**Currency:** both feeds current as of **PNut-Term-TS v0.10.3 (2026-07-20)**,
captured immediately after the pre-1.0 documentation audit. Re-pull if the repo
has advanced before release.

### Stephen's authoring decisions carried from the feeds

- **Fold logging into the guide.** Where logging behavior is directly relevant
  to a reader (headless log as the automation feedback loop; the USB traffic log
  and when it's empty; version banners in captured logs), fold it into the
  user-facing content rather than shipping the logging spec as a standalone
  chapter. The standards doc remains the authority; the guide is where the reader
  meets the behavior.
- **As-built filenames only.** The logging feed carries an explicitly
  *aspirational, unimplemented* filename scheme. Document only the canonical
  as-built names (`debug_`/`headless_`/`usb-traffic_` + `YYMMDD-HHMMSS`).

## 2. Audience & pedagogy — shared trunk, then fork

Two first-class readers, and the source material flags the second as the
highest-value use:
- **the developer at the GUI** — watching a P2 at their desk;
- **the automation author** — CI / container / AI coding assistant driving the
  tool **headless**, where the log is the agent's feedback loop on code it wrote.

**Resolution: one manual, structured as a shared orientation trunk that forks by
intent.** The two audiences share the *conceptual model* (what the tool is, the
modes) but diverge on *tasks*. Teach the model once in the trunk; fork so each
reader skips the other's material. (Same instinct as the SSDB Ch3 "annotated map
then guided tour": orient globally, then go deep locally.)

Register per `voice-guide.md`: second person, mentor, introduce-before-use,
both-modes-in-view, as-built-not-aspirational.

### How best to show it (depth target)

**Code line budget** — **Max code columns (K): 76** (platform-inherited default;
LM-Mono reference width). Command-lines and code blocks must fit within K —
they do not wrap.

`doc_class: behavior` → **show behavior, don't just tabulate it.**
- Lead each capability with a **task**, then mechanize it.
- **Worked, runnable command-lines** are the connective tissue — especially one
  complete *"your first automated run"* recipe in the headless branch.
- **Two positioning diagrams** earn their place in the trunk: (1) the tool-chain
  diagram (MCP + `pnut_ts` + `pnut_term_ts` + optional VS Code ext, with the
  P2), and (2) the three-in-one identity diagram.
- **Annotated screenshots** carry the GUI branch (main window, toolbar, status
  bar, Preferences tabs, PropPlug Management, and **Automatic Window Placement**
  in action) — Stephen captures these externally.
- **Exhaustive enumeration** (every CLI option, setting, exit code) lives in the
  reference tail as tables, not narrative.
- **Depth verdict:** re-voice + fold logging + add the positioning frame +
  screenshots + the headless recipe — **not** a wholesale expansion. The feed is
  already near-complete on enumeration; our added value is positioning, the
  fork/pedagogy, the automation recipe, and the visuals.

## 3. Structure — three books bound as one

Working outline; see `PLANNING.md` for the chapter-level detail.

- **Book 0 — Orientation (everyone, before the fork).** Tool-chain position (the
  suite + the Architect Part-3 link); the **three-in-one identity** + the
  name-as-mnemonic; the **two stances** (headed GUI / headless automation)
  introduced side by side; then **the fork** — an explicit router ("at your desk
  → GUI part; automating P2 runs → Headless part").
- **Book A — GUI branch.** Main window; download; serial terminal; **debug
  windows + Automatic Window Placement** (a headline GUI advantage — no need to
  `POS` every window; drag to read coordinates and bake a `POS` back into
  source); single-step debugger interaction; recording & playback; performance
  monitor; settings.
- **Book B — Headless branch.** Headless invocation; end-markers / timeouts;
  exit codes; **the log as the automation feedback loop**; USB traffic log;
  CI / agent-in-the-loop patterns.
- **Shared reference tail (both branches point in).** Full CLI reference;
  keyboard shortcuts; settings hierarchy; troubleshooting; support & resources.

## 4. Cross-references out (do not reproduce)

- **The P2 Architect's Guide, Part 3 (agentic use)** — *bidirectional,
  positioning.* Part 3 says "use this tool chain"; this guide is the tool that
  delivers it.
- **P2 Debug Window Manual** — the nine display windows this tool *displays and
  produces*; that manual is *what they are and how to author them* (already
  released).
- **P2 Single-Step Debugger Manual** — the single-step debugger interface this
  tool *renders and drives*; that manual is *how to use the debugger*.
- **Parallax P2 DEBUG documentation** — the `debug()` display-directive syntax.
- **Suite-mates named in the trunk:** P2KB MCP, `pnut_ts`, the Spin2 VS Code
  extension.

## 5. Release gate

**Co-releases with the P2 Single-Step Debugger Manual, timed to PNut-Term-TS
v1.0** (the P2 Debug Window Manual is already released). Therefore
**draft-and-hold to v1.0**: draft now against v0.10.3, track the tool as it
moves toward 1.0, and **re-pull the feeds + re-verify** at release.

## 6. Verification sources at audit time

- The two feeds (and a fresh re-pull from the repo if it advanced).
- Command-line behavior claims verifiable against the tool's actual `--help` /
  option validation.
- Platform-specific claims (menu layout, device paths, groups) stated per the
  feed's platform notes — do not flatten to one platform.

## 7. Status

Seed + design intent settled 2026-07-21 (purpose, identity, fork pedagogy,
cross-references, release gate). No content chapters written yet. Next: draft
Book 0 from the feeds following the voice guide.

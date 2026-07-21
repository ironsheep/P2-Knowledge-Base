# PNut-Term-TS User Guide — Changelog

## v0.1.0 (2026-07-21) — Element seeded (no content yet)

Standing structure for a new user guide documenting **PNut-Term-TS**, the
cross-platform desktop debug terminal for the Propeller 2. This is a *tool* user
guide (`doc_class: behavior`) — not a P2 silicon or language reference.

Seeded:
- Voice guide (adapted from the Single-Step Debugger Manual — its closest
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
- **Identity = three tools in one** — downloader · Parallax Serial Terminal
  replacement · PNut debug-window replacement/production (now cross-platform).
- **Pedagogy = shared orientation trunk → fork by intent** (GUI vs headless).
- **Automatic Window Placement** is a called-out GUI headline.
- **Subtitle:** *The Cross-Platform Downloader, Terminal, and Debug Display for
  the Propeller 2.*
- **Release gate:** co-releases with the P2 Single-Step Debugger Manual, timed to
  PNut-Term-TS v1.0.

No body chapters drafted. Next: draft Book 0 (orientation) from the two feeds
following the voice guide; first render pending Forge template wiring (TBD — see
PLANNING).

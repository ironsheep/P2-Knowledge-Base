# P2 Streamer Programming Guide — Punch List

Outstanding work items for the Streamer Guide. Sweep completed items into a dated
archive section at closeout.

> **2026-06-19 — v1.0.1 content-fix cycle in progress** (grounding audit
> `audit/streamer-grounding-audit-2026-06-19.md`; plan
> `engineering/planning/streamer-grounding-audit-fix-plan-2026-06-19.md`). That cycle
> covers **content only** (code-compile sweep, pin/DAC table transposition, semantics,
> LOW polish) and a single Forge render to verify those fixes landed.
> **The visual review below — diagram render-audit, Tier-3 candidates, emoji
> render-watch — is DEFERRED PAST v1.0.1 as a separate visual pass (Stephen, 2026-06-19).**
> The "after next Forge build" trigger does NOT mean the v1.0.1 build.

---

## Tier-3 diagrams (candidates — awaiting per-item approval)

Proposed during the 2026-06-01 diagram pass; Tier 1+2 (7 diagrams) were built.
These three are nice-to-haves the user may approve a couple of after reviewing the
first diagram build. Build only the ones explicitly approved.

- [ ] **§12.1 Pin-group selection windows** — a 0–63 pin ruler showing the eight `%ppp` 32-pin windows, including the wrap-around cases (`%101`–`%111`). The wrap-around table is genuinely confusing; a picture fixes it. *(bit-ruler / range diagram)*
- [ ] **§11.1–11.2 DAC routing examples** — mono / stereo / differential channel-to-pin routing as small block diagrams illustrating the `%dddd` field. *(flow / block)*
- [ ] **§16.1 SPI streamer + smart-pin timing** — data bits (streamer) aligned to clock transitions (smart pin) with the `WAITXFI` sync point. *(wsig waveform)*

---

## Diagram audit (pending — after next Forge build)

The 7 Tier-1+2 diagrams (Figs 2.1, 2.2, 3.1, 4.1, 7.1, 10.1, 15.1) are first-draft
TikZ, not yet rendered-audited. After the next PDF build, audit each rendered figure
with the standard image-tools technique (alignment, label legibility, no overlap,
technical correctness):

- [ ] Fig 2.1 Streamer data path — check no node overlap; arrow routing to DAC/Goertzel
- [ ] Fig 2.2 Data-flow paths — source→route→destination edges legible
- [ ] Fig 3.1 NCO rollover — sawtooth + advance ticks align to the 2³¹ line
- [ ] Fig 4.1 Command word — field widths/labels; `$FFFF` perpetual note
- [ ] Fig 7.1 RGB formats — segment proportions match bit counts (8/2222/332/565/888)
- [ ] Fig 10.1 DDS/Goertzel — multiply-accumulate branch reads clearly
- [ ] Fig 15.1 VGA timing — HSYNC low only during the sync segment; segment labels

---

## Other open items (carried from the content audit)

- [x] **§15.1 VGA sync/blank technique — FIXED 2026-06-03.** Rewritten against the reference driver (Eric R. Smith / Total Spectrum Software, OBEX 2847, `vga_tile_driver.spin2`). Now: sync/porch/blank use **`$7F01_0000` = `X_IMM_1X32_4DAC8 | X_DACS_3_2_1_0`** (immediate DAC-level output; S = `#0` blank / `#1` hsync-active), **VSYNC is a separate `DRVNOT` pin toggle**, and the §15.1 prose/hardware were corrected from "composite sync" to separate H/V sync. The old `$F080_0000` (a capture mode) and the streamer-folded-sync model are gone. Driver source is local-only at `NO-COMMIT/OB2847/` (gitignored; Total Spectrum © 2019-2020).
- [x] **Emoji markers (⚠️ 💡 🔧)** — POLICY RESOLVED 2026-06-03: `voice-guide.md` §3 ("Enhancement Markers") explicitly prescribes these; they are by-design and family-consistent with the live PASM2 manual. Build-render watch remains: confirm they render on the Forge build; fallback = symbol mapping (`\warningmarker = \blacktriangle`) if they box.
- [x] **Upstream KB defects** — DONE: applied in **KB v1.6.2** (F-016…F-022; F-019 split, F-022 new). Manual synced to the corrected KB on 2026-06-03: DDS/Goertzel frequency → `$8000_0000` (2³¹) at §10.6/§17.1/§17.2, SINC2 amplitude → ±10, Goertzel bitstream sum → −3..+3, Appendix A + B completed to all 56 mode symbols.

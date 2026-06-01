# P2 Streamer Programming Guide — Punch List

Outstanding work items for the Streamer Guide. Sweep completed items into a dated
archive section at closeout.

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

- [ ] **§15.1 VGA `$F080_0000` sync mode-long** — unverified encoding (cited from OBEX); validate against the actual OBEX streamer VGA driver before it's treated as authoritative.
- [ ] **Emoji markers (⚠️ 💡 🔧)** — confirm acceptable rendering on the Forge build (family-consistent with the live PASM2 manual; fallback = a symbol mapping if they show as missing-glyph boxes).
- [ ] **8 upstream KB defects** (F-016…F-021 in `engineering/operations/P2KB-CORRECTION-FINDINGS.md`) — separate `yaml-knowledge-base-maintenance` pass.

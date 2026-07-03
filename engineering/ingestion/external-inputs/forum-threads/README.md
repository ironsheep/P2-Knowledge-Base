# Forum-Thread Ingestions — Index

Ingested Parallax P2 forum threads. Process, trust model, and placement convention:
**[FORUM-THREAD-INGESTION-POLICY.md](FORUM-THREAD-INGESTION-POLICY.md)**.
Trust rule in one line: **`cgracey` (Chip Gracey, P2 designer) = 🏆 authoritative;
every other poster individually qualified 🟢 domain-expert / 🟡 community =
cross-check (verify before use).**

## Batch 1 — 2026-07-01 (4 threads)

| Thread | ID | Pg | Posts | CG🏆 | Topic | Primary doc targets |
|--------|----|----|-------|------|-------|---------------------|
| [Reciprocal Counter Demo](ReciprocalCounterDemo/INGEST.md) | 170882 | 5 | ~118 | 8 | smart-pin reciprocal counting + clock/PLL accuracy | **IOSP Ch.14/15 · P2AN004** |
| [Problem: streamer Goertzel SINC2](ProblemGoertzelSINC2mode/INGEST.md) | 176065 | 1 | 3 | 2 | **confirmed silicon erratum** (SINC2 GETXACC) | **Streamer Guide · IOSP ADC** |
| [1024-point FFT in 79 longs](1024-point-FFTin79longs/INGEST.md) | 170948 | 4 | 110 | 22 | CORDIC FFT butterfly, pipelining | **P2AN002 · Streamer** |
| [Anti-aliased 24-bpp HDMI](HDMIAnti-aliased-24-bits-per-pixel/INGEST.md) | 175725 | 3 | 85 | 13 | HDMI/DVI streamer output, blanking, pixel-blend | **Streamer Guide · PASM2 YAML** |

Each folder holds `raw-capture.md` (verbatim evidence) + `INGEST.md` (digest).

**Capture caveats** (WebFetch summarizer limits — noted in each thread's Open
Questions): Reciprocal Counter's OP PASM was initially refused on copyright grounds
and load-bearing lines recovered individually; the FFT thread's large attachment-style
listings (Chip's ~500-line spectrographs, OBEX lib) were elided. Re-fetch specific
posts if full source is needed for authoring.

---

## Merged reconciliation queue

Findings to disposition in the **separate reconciliation pass** (audit each target
against these, per policy §5). 🏆 = Chip Gracey authoritative; 🟢 = credible-community
(verify); ⚠️ = flagged even at its tier (contested or relayed — must verify before publishing).

### → I/O & Smart Pins User Guide (IOSP)
| # | Finding | Section | Action | Trust |
|---|---------|---------|--------|-------|
| I1 | Reciprocal counter = 3 cells, modes `%10101/%10110/%10111` = `P_COUNTER_TICKS/HIGHS/PERIODS` | Ch.14/15 | verify present + correct; enrich | 🏆 |
| I2 | 64-bit intermediate math (QMUL→SETQ→QDIV) prevents overflow computing freq=periods·sysfreq/clocks | Ch.15 | verify example uses it | 🏆 |
| I3 | Counter terminology: "ticks/highs/periods"; duty = highs÷ticks ("density") | Ch.14/15 | align wording | 🏆 |
| I4 | Counter pins are NOT consumed — still usable as general I/O; 2-cell wireless measure via `P_MINUS2/3_A/B` (±3 pins, no jumper) | Ch.14 | verify + add technique | 🏆/🟢 |
| I5 | Smart-pin ADC self-biases to ~VIO/2 (mic input needs no divider) | ADC ch. | verify + note | 🏆 |
| I6 | Goertzel SINC2 sensitivity (noise every 30–60 ms) if iteration count varies | ADC/Goertzel ch. | add caveat + cross-ref Streamer | 🏆 |

### → P2AN004 (Frequency / Period / Pulse Measurement)
| # | Finding | Action | Trust |
|---|---------|--------|-------|
| A1 | Reciprocal modes + 64-bit compute (`muldiv64`) as the core method | fold into recipe | 🏆 |
| A2 | Reciprocal auto-scales any input; ceiling ≤ ~100 MHz @250 MHz sysclk | method-selection + range note | 🟢 ⚠️ (exact ceiling) |
| A3 | Reciprocal vs fixed-gate tradeoff; does NOT measure jitter | method-selection | 🟢 |
| A4 | Canonical Ariba Spin2 port `muldiv64(clkfreq, periods, ticks-1)` | example (compile-cert) | 🟢 ⚠️ (`ticks-1` rationale) |
| A5 | Crystal `%CC` cap modes shift ppm → duty aperture-walk; `%10/%11` pF value **contested** (Chip 7.5/15 vs jmg 15/30) | accuracy caveat | 🏆 ⚠️ (verify vs Silicon Doc) |
| A6 | TSL235R light-to-frequency Quick-Byte drivers as a related measure source | related-links | 🟢 |

**Status (2026-07-01) — RECONCILED into P2AN002/P2AN004 opus-masters.** A1 already present (reciprocal + `muldiv64` core; MULDIV64 prose ripple in commit 9f5473e7). A2/A3/A5 folded as method-selection & accuracy notes (range below ½ sysclk; averages so does not measure jitter; reading only as accurate as clkfreq — no contested pF/ceiling figures cited). A6 already in Resources. **A4 `ticks-1` NOT adopted** — the correction's rationale is unverified in-thread; our formula `MULDIV64(periods, clkfreq, ticks)` is the correct reciprocal form and stays. C1/C2/C3 folded into the "Going Further" FFT paragraph (butterfly = one QROTATE; pipelined; 79-long ~3 ms / hand-tuned ~700 µs @250 MHz). C4 folded as a library pointer (**OBEX #5361** SaucySoliton FFT/IFFT — real-input, windowing, radix-4 digit reversal) rather than a full DSP appendix, matching the note's pointer-altitude scope. Both notes remain v0.1.0 drafts (uncommitted at time of writing).

### → P2AN002 (CORDIC for Real Work)
| # | Finding | Action | Trust |
|---|---------|--------|-------|
| C1 | **Crown jewel:** one `SETQ`+`QROTATE` = a complete complex twiddle multiply = one FFT butterfly rotation | worked example | 🏆 |
| C2 | CORDIC pipelining (8-cycle cadence, unroll to hide latency): ~3 ms → ~700 µs @250 MHz for 1024-pt | throughput section | 🏆/🟢 |
| C3 | 10-pass FFT structure with skip-when-angle-0 optimization | structure | 🏆 |
| C4 | Real-input FFT, radix-4 digit reversal, windowing (SaucySoliton OBEX fft-ifft) | DSP appendix | 🟢 |

### → Streamer Programming Guide
| # | Finding | Action | Trust |
|---|---------|--------|-------|
| S1 | **Goertzel SINC2 requires constant iterations/cycle** — non-power-of-two `SETXFREQ` D corrupts current+next GETXACC sample. Workarounds: (1) power-of-two sysclk (256 MHz not 250 for 1 MHz), (2) use SINC1, (3) SINC2 with XZERO start + period < 20 ms | new subsection (erratum) | 🏆 |
| S2 | HDMI/DVI blanking is display-limited not analog-mandated; hblank floor ~16→68 px, multiple-of-8; vblank floor 8 lines | HDMI timing | 🏆/🟢 |
| S3 | HDMI audio (data-island) needs ~34 hblank pixel-periods vs ~16 video-only | HDMI audio | 🏆 ⚠️ (relayed from Wuerfel_21 — verify vs HDMI spec) |
| S4 | SETQ block RDLONG/WRLONG burst = 1 clock/long | FIFO/burst section | 🏆 |
| S5 | Streamer scope-mode MSPS capture feeding FFT | capture example | 🟢 |

**Status (2026-07-01) — RECONCILED into the Streamer Programming Guide; shipped in v1.0.3 (2026-07-03).** S1 folded as a §10.4 caution (SINC2 constant-iteration-count silicon limitation + 3 workarounds; Silicon-Doc note 2024.12.16) + an App-D checklist item. S2 + S3 folded into §15.2 (blanking display-limited 16–68 px / mult-of-8 / ~8-line vblank; audio ~34 px flagged **community-measured, verify vs data-island spec**). S5 folded as a §9.2 capture-to-spectrum pointer (→ P2AN002). **S4 DEFERRED** — "SETQ block RDLONG/WRLONG = 1 clk/long" is a hub-transfer fact, a *different* mechanism from the streamer's RDFAST/WRFAST FIFO; folding it into the FIFO discussion would be a technical conflation. Route to PASM2/hub docs, not this guide. **Y5 (SETPIV/BLNPIX)** → PASM2 YAML (yaml head), ⚠️ community-reverse-engineered — verify semantics before use. **D1 (8-bit sub-pixel model)** → DEBUG-window manual, not the Streamer guide.

### → YAML / Silicon-Doc reconciliation
| # | Finding | Target | Action | Trust |
|---|---------|--------|--------|-------|
| Y1 | Confirm the Silicon-Doc **2024.12.16 SINC2 note** is present in our ingested copy | Silicon Doc extract | verify presence | 🏆 |
| Y2 | `REP` blocks interrupts | rep.yaml | verify documented | 🏆 |
| Y3 | CORDIC auto-waitstate 8/16-clk spacing (explicit NOPs unnecessary) | cordic/qrotate YAML | cross-check | 🟢 |
| Y4 | QMUL/QDIV signed-word limitation | qmul/qdiv YAML | cross-check | 🟢 |
| Y5 | `SETPIV`(alpha=low 8 bits)+`BLNPIX` pixel-blend; `RGBSQZ`/`RGBEXP` for 16bpp; 32bpp/LUMA only | setpiv/blnpix/rgbsqz/rgbexp YAML | verify semantics | ⚠️ community-reverse-engineered |

**Status (2026-07-02) — RECONCILED into the served YAML (ships in a release-yamls patch).** **Y1** applied: added a `sinc2_constraint` field to `language/pasm2/getxacc.yaml` (register F-190) — attributed to Chip's designer report, since the released Silicon Doc still lacks the 2024.12.16 note (confirmed by Stephen). **Y2** verified already present — `pasm2/rep.yaml` states "Interrupts stalled during execution." **Y3** no change — `qrotate`/`qvector`/`cordic` already document the 8-clock hub-window spacing; the "no manual NOPs needed" corollary is derivable from that and only a 🟢 community claim (not shipped as new authoritative fact). **Y4** no change — `qmul`/`qdiv` already documented unsigned throughout (the "signed-word" note = the unsigned nature; digest itself flags it as possibly interpretation, not a hardware limit). **Y5** no change — `setpiv` ("blend factor to D[7:0]"), `blnpix`, `rgbsqz`, `rgbexp` already carry the correct semantics; the ⚠️ community reverse-engineering merely confirms them. (The F-188 overflow sweep also surfaced F-189 in `timing_operations.yaml` — fixed same pass.)

### → DEBUG display docs
| # | Finding | Action | Trust |
|---|---------|--------|-------|
| D1 | 8-bit sub-pixel (1/256 px) coordinate+diameter model behind DEBUG anti-aliased line draw | reference note | 🏆 |

---

*Next step: the reconciliation pass — audit each target doc/YAML against its rows,
promote confirmed 🏆 contradictions/extensions to `P2KB-CORRECTION-FINDINGS.md`, verify
🟢/⚠️ items before use. Ingestion (this batch) is finding + understanding only.*

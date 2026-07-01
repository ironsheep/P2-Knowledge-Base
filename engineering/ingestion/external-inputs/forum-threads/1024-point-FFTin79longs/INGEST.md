# Forum Thread Ingestion — 1024-point FFT in 79 longs

- **Source URL:** https://forums.parallax.com/discussion/170948/1024-point-fft-in-79-longs
- **Thread ID:** 170948
- **Pages:** 4
- **Post count:** 110 (P1: 33, P2: 29, P3: 29, P4: 19)
- **OP author + date:** cgracey — 2019-12-17
- **Fetched:** 2026-07-01
- **Topic class:** Algorithm / DSP technique — CORDIC-based FFT on P2; CORDIC pipelining, streamer capture, real-vs-complex FFT, bit/digit reversal, windowing, FFT fast-convolution filtering (SDR).

---

## Thread purpose

Chip Gracey posts a complete 1024-point FFT (converting 1024 signed word samples into 512
frequency powers) that fits in 79 longs and runs in ~3 ms at 250 MHz. The thread's core value
is Chip's realization that a **single CORDIC `SETQ`+`QROTATE` performs the entire FFT butterfly
rotation** — turning an FFT into "CORDIC rotates plus adds/subtracts." The discussion then
develops CORDIC-pipeline stuffing, streamer-based high-rate capture (SaucySoliton), real-input
FFT, radix-4 digit reversal, and a full DSP/SDR toolchain (bob_g4bby), culminating in a
published OBEX FFT/IFFT library.

---

## Participant trust classification

| User | Trust | Basis |
|------|-------|-------|
| cgracey | 🏆 | Chip Gracey — P2 chip designer; authoritative/trusted (ground truth). Authored the FFT + all CORDIC-usage claims. |
| SaucySoliton | 🟢 | Deep, correct DSP/FFT expertise; radix-4 digit reversal, real-FFT, MOPS derivations vs FFTW, published OBEX FFT/IFFT library. Clearly knows the domain. |
| TonyB_ | 🟢 | Precise P2-microarch reasoning (CORDIC 8-cycle issue cadence, SUBR, skip/`_ret_` tricks, LUT/FIFO timing). Consistently correct. |
| bob_g4bby | 🟢 | Working SDR/DSP engineer (LabView receiver, FFT fast-convolution filter design); credible inline-PASM CORDIC pipelining. Some open questions, but domain-expert. |
| evanh | 🟢 | Accurate P2 timing facts (16-cog 16-clock CORDIC cadence, ADC noise floor); self-corrected MOPS misread. |
| Wuerfel_21 | 🟢 | Correct authoritative statement on CORDIC auto-inserted waitstates (8-cycle spacing). |
| jmg | 🟡 | Reasonable ADC-performance figures (ES1 10–12 bit) but ES1-era, cross-check. |
| Rayman | 🟡 | Active integrator/experimenter (windowing suggestion, ADC-gain findings, VGA port); community. |
| lonesock | 🟡 | Correct FFT insight (last pass = trivial rotations); occasional contributor. |
| Christof Eb. | 🟡 | Good DSP references (Goertzel, FFT scaling/overflow); community. |
| avsa242 | 🟡 | Ported Heater P1 FFT; benchmark reports; community. |
| Reinhard | 🟡 | Enthusiast Q&A; general community. |
| Cluso99 | 🟡 | Long-time P2 community; here just a clarifying question. |
| Publison | 🟡 | Community/logistics (board offer, moderation). |
| Ariba | 🟡 | Provided a reference link. |
| msrobots | 🟡 | Off-hand comment. |

---

## Chip Gracey findings (trusted gold)

### CG-1 · A single CORDIC SETQ+QROTATE performs the entire FFT butterfly rotation
> "So, I substituted a single CORDIC operation for that whole sequence:
> ```
> 		setq	b2		'rotate (b1,b2) by angle
> 		qrotate	b1,angle
> 		getqx	b1
> 		getqy	b2
> ```
> AND IT WORKED!!!!! So, the CORDIC can really whip the core of the FFT problem. This just leaves some adds and subtracts in the inner loop."

Replaces the classic two-`QROTATE` + cross add/sub complex-rotation sequence. `SETQ` loads the
Y operand so `QROTATE b1,angle` rotates the vector (b1,b2) by `angle`; `GETQX`/`GETQY` retrieve
rotated X,Y. This is the standard way to rotate an (X,Y) pair by an angle on the P2 CORDIC.
- **Means:** The FFT butterfly's complex twiddle-factor multiply = one CORDIC vector rotation. `QROTATE` intrinsically supplies sin/cos and the 4 multiplies + 2 adds of a complex rotate.
- **Affects:** P2AN002 (CORDIC for Real Work) — canonical worked example of `SETQ`+`QROTATE` as a complex-rotate primitive; CORDIC instruction YAMLs (`qrotate`, `getqx`, `getqy`, `setq`).

### CG-2 · Complete simple butterfly inner loop (readable reference form)
> ```
> .loop3		setq	#2-1		'read (bx,by)
> 		rdlong	bx,ptrb
> 		setq	by		'rotate (bx,by) by angle
> 		qrotate	bx,angle
> 		setq	#2-1		'read (ax,ay)
> 		rdlong	ax,ptra
> 		getqx	bx		'get rotated (bx,by)
> 		getqy	by
> 		add	ax,bx		'(ax,ay) = (ax+bx,ay+by)
> 		add	ay,by
> 		shl	bx,#1		'(bx,by) = (ax-bx,ay-by)
> 		subr	bx,ax
> 		shl	by,#1
> 		subr	by,ay
> 		setq	#2-1		'write (ax,ay)
> 		wrlong	ax,ptra++
> 		setq	#2-1		'write (bx,by)
> 		wrlong	bx,ptrb++
> 		djnz	c2,#.loop3
> ```
- **Means:** A complete decimation-in-frequency butterfly: rotate B by twiddle angle, then A±B. Uses `SETQ`+`RDLONG`/`WRLONG` burst pairs (2-long block transfers), and `SHL #1`+`SUBR` to form (A−B) since A already had B added. Placing a `SETQ`+`RDLONG` between `QROTATE` and `GETQX` overlaps hub I/O with CORDIC latency and speeds it up (Rayman's suggestion, confirmed by Chip).
- **Affects:** P2AN002 worked example; Streamer/FIFO guide (burst `SETQ`+`RDLONG`/`WRLONG` idiom); CORDIC-latency-hiding pattern.

### CG-3 · CORDIC pipelining sets the achievable FFT speed
> "I think the simplest way to speed up this program would be to take bigger bites in the inner loop, so that we load/store more A's and B's and pipeline more CORDIC operations. Right now it's taking ~750,000 clocks to do 10,000 operations. That's 75 clocks per. We could probably get it down to 30 clocks."
> "We could read 16 pairs at a time and then stuff the CORDIC pipeline."
- **Means:** Throughput is limited by how full the CORDIC pipeline is kept; unrolling to 8–16 rotations per batch overlaps command issue with the 8-cycle CORDIC latency. ~3 ms initial → sub-1 ms target at 250 MHz.
- **Affects:** P2AN002 (CORDIC throughput/pipelining section); Streamer/CORDIC overlap patterns.

### CG-4 · FFT pass structure and twiddle-angle table
> "the FFT does the following-sized runs of rotations and adds/subs on contiguously-placed coordinate pairs: 512 x1, 256 x2, 128 x4, 64 x8, 32 x16, 16 x32, 8 x64, 4 x128, 2 x256, 1 x512"
> angle table (MSBS, 000/400/200 = 0/90/45 deg): first 512-span pass rotates nothing (angle 0), 256-span rotates only 90° in its last half; "In every inner loop, the rotation can be skipped when the angle is zero."
- **Means:** 10 passes (log2 of 1024) over contiguous coordinate pairs; angles span 0..just under 180°. Zero-angle rotations can be skipped (later exploited via `SKIPF`). Passes ≥16×32 run ~68 µs each — ~60% of the job in ~420 µs; the small final passes dominate remaining time.
- **Affects:** P2AN002 (FFT structure); optimization note (skip-when-angle-zero).

### CG-5 · Result / footprint / conversion
> "It takes a hair over 3ms at 250MHz. It converts 1024 signed word samples to 512 frequency powers." (79 longs)
> Later: "I had worked on a fast 1024-point FFT a few years ago and got it down to 700us at 250MHz. I hard-coded different parts of the butterfly to speed it up."
- **Means:** Baseline compact FFT = 79 longs, ~3 ms @250 MHz; a hardcoded/unrolled variant reaches 700 µs @250 MHz. Input signed 16-bit words, output 512 magnitude bins.
- **Affects:** P2AN002 performance framing; demonstrates P2 DSP capability.

### CG-6 · ADC self-biases to ~VIO/2 (mic via cap directly to a pin)
> "The ADC pulls it to its own center, which is the threshold of a particular inverter, and close to VIO/2."
- **Means:** Smart-pin ADC input self-centers near VIO/2 at an inverter threshold, so an AC-coupled mic (0.1 µF cap to pin) needs no external bias divider.
- **Affects:** Smart Pins / ADC docs (self-biasing behavior); IOSP ADC chapter cross-check.

### CG-7 · Cosine window; SINC2 14-bit ADC capture; REP caveat
> "I made a nice cosine-shaped window filter which actually cleaned up the output quite a bit."
> "We could use REP, but it wouldn't save much time. Also, it would block interrupts."
- **Means:** A cosine (Hann-family) window on the input reduces spectral leakage. `REP` in the inner loop is discouraged because it **blocks interrupts** for the duration. Mic captured with 14-bit SINC2 smart-pin ADC mode.
- **Affects:** DSP windowing note; `REP` instruction YAML caveat (blocks interrupts) — cross-check against existing YAML.

### CG-8 · Why P2 optimization is "chess not checkers"
> "because hardware optimizations exist in the P2 that enable software optimizations, you wind up playing chess instead of checkers ... if the hardware was simple, everyone's software efforts would result in the same solutions."
- **Means:** Design commentary — P2's CORDIC/streamer/FIFO create a large software-optimization space. Narrative color, not a technical spec.
- **Affects:** App-note voice / motivation prose only.

---

## Other credible technical contributions (qualified posters, community/cross-check)

- **TonyB_ 🟢 — CORDIC issue cadence:** "Is it possible to issue a new command every 8 cycles, with three 2-cycle instructions in between? Eight A's and B's in the inner loop look to be optimal." Also: `QMUL` best case one sample / 16 cycles; `RDLUT` is 3 cycles and can disrupt CORDIC pipelining; `SUBR` underused; changing an instruction's condition prefix (`always`↔`_ret_`) to synthesize subroutines. → Cross-check CORDIC-cadence + instruction-timing claims against silicon/YAML.
- **evanh 🟢 — Cadence on 16-cog part:** "For a 16-cog prop2 the tightest is every 16 clocks, with up to seven 2-cycle instructions between." (8-cog = every 8 clocks.) Also: x100 ADC gain noise floor ~10× worse than x10. → CORDIC command spacing is a function of cog count (hub/egg-beater slot).
- **Wuerfel_21 🟢 — CORDIC auto-waitstates:** "CORDIC ops automatically insert waitstates so they're spaced a multiple of 8 cycles apart" — so explicit `NOP`s between back-to-back `QVECTOR`s are unnecessary. → Authoritative-sounding; cross-check against CORDIC YAML/Silicon Doc, could confirm/clarify existing docs.
- **SaucySoliton 🟢 — optimization catalog:** FIFO background reads; instructions in hub-write wait interval; `SKIPF` to bypass CORDIC ops when angle=0; unrolled loop packs 4 points; real-input FFT (pack reals as complex of half size + post-process ≈ halves time; per FFTW formula 1024-real=25,600 ops=50% of 1024-complex); radix-4 **digit** reversal (2-bit digits, P2 `SPLITW`/`REV`/`ROL`/`MERGEW` shuffle in 3 extra instructions) cutting reversal 160 µs→50 µs; full 1024 transform 870 µs @160 MHz; IFFT = FFT with conjugated in/out; DIF-FFT (bit-reversal last) vs DIT. Published OBEX **fft-ifft** library (https://obex.parallax.com/obex/fft-ifft/). QROTATE = "sin(), cos(), 4 multiplies and 2 adds in as little as 8 clocks." → Strong secondary source; independent confirmation of CG-1/CG-3.
- **bob_g4bby 🟢 — inline-PASM CORDIC pipelining + SDR design:** `SETQ #31`+`RDLONG`/`WRLONG` moves 16 iq pairs at 1 clock/long; preload 8 CORDIC ops, interleave read-result/load-next → ~9 clocks per CORDIC result; `xytopol` (cartesian→polar via `QVECTOR`) 56.1 µs @320 MHz. FFT fast-convolution filter architecture for SDR (Youngblood "SDR for the Masses"); window applied to filter coefficients once, not the signal path; Blackman-Harris window in LUT RAM (symmetric, store half). Note: `QMUL`/`QDIV` don't handle signed words (does polar-domain math instead). → Cross-check the signed-word QMUL/QDIV claim against YAML.
- **lonesock 🟡 / Christof Eb. 🟡:** last FFT pass ≈ trivial 90°/180° rotations (special-case-able); Goertzel more efficient than FFT when only a few bins are needed; FFT scaling/overflow strategy (÷2 every 1–2 stages) to avoid the ~256× growth in a forward 1024-FFT.
- **jmg 🟡:** ES1-silicon internal ADC ~10–12 bit (varies with supply/pin/MHz); external isolated ADC ~78 kHz BW, 12–14 useful bits. ES1-era, verify against current smart-pin ADC characterization.

---

## Doc-impact targets (reconciliation queue)

| # | Finding | Target doc/section | Suggested action | Trust |
|---|---------|--------------------|------------------|-------|
| 1 | SETQ+QROTATE = one-instruction complex vector rotation (FFT butterfly) | P2AN002 CORDIC for Real Work — worked FFT example | Add as canonical CORDIC-rotate/FFT-butterfly example with CG-1/CG-2 code | 🏆 |
| 2 | CORDIC pipelining: 8-cycle issue cadence, unroll to keep pipeline full; hide latency by interleaving hub I/O | P2AN002 CORDIC throughput section; Streamer/CORDIC overlap | Document pipelining pattern + per-result clock budget (~9 clk/result achievable) | 🏆 (+🟢 TonyB_/evanh/bob) |
| 3 | CORDIC command spacing = 8 clk (8-cog) / 16 clk (16-cog); auto-inserted waitstates make inter-op NOPs unnecessary | CORDIC instruction YAMLs / Silicon-Doc CORDIC timing | Verify + state auto-waitstate spacing rule explicitly | 🏆-adjacent (🟢 evanh/Wuerfel_21) — cross-check |
| 4 | FFT pass structure (10 passes) + skip rotation when angle=0 (SKIPF) | P2AN002 FFT structure/optimization | Document pass table + zero-angle skip optimization | 🏆 |
| 5 | Smart-pin ADC self-biases to ~VIO/2 → AC-coupled mic needs no bias divider | Smart Pins / IOSP ADC chapter | Cross-check against existing ADC self-bias text; add if absent | 🏆 |
| 6 | `REP` blocks interrupts (loop caveat) | REP instruction YAML | Verify caveat present; add if missing | 🏆 |
| 7 | Real-input FFT (pack reals as half-size complex + post-process) ≈ halves runtime | P2AN002 advanced/real-FFT note | Add as technique reference (cite SaucySoliton OBEX lib) | 🟢 |
| 8 | Radix-4 digit reversal via SPLITW/REV/ROL/MERGEW; bit/digit-reversal cost | P2AN002 / DSP appendix | Reference technique; point to OBEX fft-ifft | 🟢 |
| 9 | SETQ block RDLONG/WRLONG = 1 clock/long burst transfer | Streamer/FIFO/hub block-transfer guide | Confirm block-transfer timing doc covers SETQ+RDLONG bursts | 🏆 (CG-2) +🟢 bob |
| 10 | Streamer scope-mode capture to megasamples/s feeding FFT (SaucySoliton 3.676 MSPS) | Streamer Programming Guide — capture-to-hub example | Note streamer→FFT pipeline + cogatn sync as use case | 🟢 |
| 11 | QMUL/QDIV do not handle signed words | CORDIC QMUL/QDIV YAML | Verify signed-operand behavior; document constraint | 🟢 — cross-check |
| 12 | Windowing (cosine/Hann, Blackman-Harris) for FFT input / applied to filter coeffs | P2AN002 / DSP appendix windowing note | Add windowing guidance (leakage reduction) | 🏆 (cosine) +🟢 |

---

## Open questions / unresolved

- **Zero-angle skip vs SKIPF interaction:** Chip notes rotation can be skipped when angle=0; SaucySoliton uses `SKIPF`. Exact skip-pattern encoding for the mixed pass sizes not fully spelled out here (see attached code, not captured verbatim).
- **QMUL/QDIV signed-word limitation (bob_g4bby):** Stated as fact but not confirmed by Chip — needs YAML/silicon verification (may be a scaling/interpretation issue rather than a hardware limit).
- **CORDIC 16-cog spacing (evanh):** "16 clocks for a 16-cog prop2" — the shipped P2 is 8-cog; confirm the general rule (spacing tied to hub rotation) and drop the hypothetical 16-cog framing.
- **ES1 ADC bit-depth (jmg):** 10–12 bit figures are ES1-era; reconcile with current smart-pin ADC characterization / hardware-verification ledger.
- **Large attachment code not captured verbatim:** Chip's full spectrograph programs (P2 posts ~500–600 lines) and SaucySoliton's OBEX library source are attachments/large code blocks elided by the fetcher — retrieve from Google Drive link / OBEX (fft-ifft) if the full listings are needed for P2AN002.
- **FFT scaling/overflow (Christof Eb.):** ÷2-per-stage strategy referenced from an external project; not yet a P2-specific documented recommendation.

# P2KB Correction Findings — ARCHIVE, swept 2026-10-05 (after the I/O & Smart Pins v1.0.11 release)

> **This is an archive of CLOSED findings. It is never re-edited.** Ask "what is
> outstanding?" of `engineering/operations/P2KB-CORRECTION-FINDINGS.md` alone — never
> re-derive completion state from here. If an archived finding must be reopened, it
> returns as a **new** active finding that references this file.
>
> Contains 4 findings carrying a `DONE` status token: F-533, F-534, F-535 and F-536, all released in
> the P2 I/O & Smart Pins User Guide v1.0.11 (tag `p2-io-and-smart-pins-user-guide-v1.0.11`) and
> verified on the released PDF on 2026-10-05. None was the only finding under its section heading, so
> no heading moves.
>
> Swept by rename-then-trim: the register was `git mv`'d here and copied back; this copy was cut to
> the 4 findings, and the live copy had the same text removed with the edit tools. Every line below is
> the pre-sweep text (commit f4bd3935), verbatim; `audit-register-hygiene.py --sweep-check f4bd3935`
> proves it.

---

### F-533 — I/O & Smart Pins: trigger-mode examples write Y before enable, and the generic sequence and PINSTART carry no caveat — `DONE` (released in IOSP v1.0.11, 2026-10-05, verified on the PDF: pages 86, 100, 105)
> **Applied** against `pinstart.yaml` (trigger list: %00100, %00101, %11110; %11100 primes in reset, EF-090).
> Appendix F pulse and transition quick examples: `PINH` before `WYPIN`. **Evidence-scoping:** the sweep found
> ten more WYPIN-before-enable quick examples in appendix F (DAC dither, counters, timers) — all value modes,
> correct either way, left; async TX (`PINLOW` then `WYPIN`) and sync TX already right. One caveat in §4.8 (after
> Step 5), one in §5.4 PINSTART (Yval lost; pass 0, WYPIN after), and the §5.x best-practice list item. The
> §5.x overhead line (:407) is a cycle count, not a procedure, and stays. Appendix E loopback rebuilt: bit
> period, both pins enabled with PINSTART, WYPIN after, `>> 24` read; compiled clean with `pnut-ts -d`.
D19 (EF-011: pulse and transition PASS-REQUIRED). `part-5-appendices/appendix-f-mode-reference.md:205-208`
(P_PULSE: `WYPIN(pin, 5)` then `PINH`) and `:238-241` (P_TRANSITION: `WYPIN(pin, 20)` then `PINH`) — the
count is lost. Generic: `chapter-04:369-392` ("Step 4 WYPIN / Step 5 Enable", no trigger caveat),
`chapter-05:291-308` (PINSTART "combines WRPIN, WXPIN, WYPIN, and enable"), `:407`, `:508`. Also
`appendix-e-troubleshooting.md:590-597`: the async loopback test never raises DIR at all, so nothing
transmits. ch07, ch11 and ch17:301-308 already do it right. **Fix:** appendix F examples WYPIN after
PINH; one caveat in ch04/ch05 (trigger and async TX: Y after enable; value modes either way; sync TX
primes in reset — F-526); loopback test enables both pins.

### F-534 — I/O & Smart Pins: "OUT=1 enables the ADC" in the DAC modes, without the TT bit 0 condition — `DONE` (released in IOSP v1.0.11, 2026-10-05, verified on the PDF: pages 158-161, 284, 290, 359-360)
> **Applied** against `smart_pins.yaml` out_needs_tt_bit0_to_run_adc and the %00001/%00010/%00011 YAMLs.
> §10.6 and §18.4 (the DAC-PRNG-dither readback) carry a Rev C silicon-note chip; the five table cells read
> "(if OUT=1, TT bit 0 set)"; the §10.6 example comment names `P_OE`. No pointer to P2 Errata, no E-number.
D7 (P2 Errata E6). `part-2-output-modes/chapter-10-dac-output.md:356-365` ("Enable ADC feedback (OUT=1)",
`PINWRITE(pin, 1)`), `part-4-special-modes/chapter-18-repository.md:252` ("When OUT is high, the pin's ADC
is enabled"), and the "(if OUT=1)" table cells at ch10:215, :263, ch18:544, appendix-f:127, :161. The
examples carry `P_OE`, so they work. **Fix:** "with TT bit 0 set (P_OE)" at each, pointing to the erratum.

### F-535 — I/O & Smart Pins: "WAITSE1 WC ... C and Z carry the same timeout result" — `DONE` (low; released in IOSP v1.0.11, 2026-10-05, verified on the PDF: page 94)
> **Applied** at §5.1: "`WCZ` writes the timeout result to both `C` and `Z`; with `WC` only `C` is written."
C39/D4. `chapter-05-working-with-smart-pins.md:81`: with `WC` only C is written. **Fix:** "(`WCZ` writes
both; with `WC` only `C` is written.)"

### F-536 — I/O & Smart Pins: an internal edge-mode inconsistency and a dead index pointer — `DONE` (released in IOSP v1.0.11, 2026-10-05, verified on the PDF: pages 211, 393)
> **Edge encoding: no defect.** Silicon Doc `silicon-doc-text.txt:4180-4184` gives Y[1:0] `%1x` = edge. ch13:251
> and appendix-f:694 say `%1x`; ch13's other table lists 3-bit Y values, where `%01x` is Y[2]=0, Y[1:0]=`%1x` —
> the same encoding. Its column header now reads `Y[2:0]` (was "Y Value"), which is what invited the misread.
> **Index:** `P_CHANNEL` repointed to Ch. 2, App. B (ch02:380, appendix-b:242).
Seen by the audit, not inventory facts. ch13:245-251 gives `%1x` as "any edge" while ch13:593-600 and
appendix-f:694 give `%01x`; `part-5-appendices/index.md:149` points P_CHANNEL at Chapter 10, which never
mentions it. **To do:** settle the edge encoding against the Silicon Doc, then fix the losing side;
repoint the index (P_CHANNEL is at ch02:380 and appendix-b:242).

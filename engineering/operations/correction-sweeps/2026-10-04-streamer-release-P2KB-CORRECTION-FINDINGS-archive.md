# P2KB Correction Findings — ARCHIVE, swept 2026-10-04 (after the Streamer Guide v1.1.3 release)

> **This is an archive of CLOSED findings. It is never re-edited.** Ask "what is
> outstanding?" of `engineering/operations/P2KB-CORRECTION-FINDINGS.md` alone — never
> re-derive completion state from here. If an archived finding must be reopened, it
> returns as a **new** active finding that references this file.
>
> Contains 2 findings carrying a `DONE` status token: F-539 and F-479, both released in the P2
> Streamer Programming Guide v1.1.3 (tag `p2-streamer-programming-guide-v1.1.3`) and verified on the
> released PDF on 2026-10-04. F-479 was the only finding under its section heading, so the heading
> comes here with it. The fourth sweep of the day, so it has its own file.
>
> Swept by rename-then-trim: the register was `git mv`'d here and copied back; this copy was cut to
> the 2 findings and the one emptied section heading, and the live copy had the same text removed
> with the edit tools. Every line below is the pre-sweep text (commit 7c318104), verbatim;
> `audit-register-hygiene.py --sweep-check 7c318104` proves it.

---

### F-539 — Streamer Guide ch16: streamer SPI data against a P_TRANSITION clock, taught as "matched rates", with no word on the losing start phase — `DONE` (released in Streamer v1.1.3, 2026-10-04, verified on the PDF: pages 72-73)
> **Applied.** Ch16 intro: the rates match because both run from one clock, and the starting phase is set by
> your code. §16.1 gains a caution after the bulk transfer: the `XINIT`-to-`WYPIN` spacing picks one of a few
> phases (one per sysclk of the half-period), exactly one loses silently, and a safe spacing at one SCK rate can
> lose at another, so check it at every rate. Source: `streamer_smartpin_control.yaml` alignment_pad.write_side.
> The partner's residue formula is not stated. The examples keep their back-to-back `XINIT`/`WYPIN`: no
> spacing is proven for their configuration, so the caution, not a number, is the fix.
D15 (partner bench XF-001, graded SCOPED). `streamer-body.md:1688-1747`: `wrpin P_TRANSITION`,
`xinit mode, data`, `wypin transitions` — only half-period-many start phases exist and exactly one silently
corrupts whole transfers; a pad safe at one SCK rate can lose at another. **Fix:** a caution in 16.1:
the XINIT-to-WYPIN phase matters, and the alignment must be verified at each SCK rate
(`streamer_smartpin_control.yaml` alignment_pad.write_side). Do not state the partner's residue formula.

## The Streamer Guide teaches GETXACC as capture-and-clear (2026-10-01, v1.22.0 impact survey) — F-479

### F-479 — the Streamer Guide says GETXACC "captures and clears" both accumulators; on silicon the clear acts only during a Goertzel burst, and a burst's last term lands in the next — `DONE` (released in Streamer v1.1.3, 2026-10-04, verified on the PDF: pages 43, 75)
> **2026-10-04 — hold lifted, applied.** Stephen: "yes E1-E7 approved". §10.6 and §17.1 now state the silicon
> behaviour as two Rev C silicon-note chips (E4: an idle read returns the running total and clears nothing;
> E5: a burst's last term joins the next Goertzel burst), keep the before/after difference rule, and give the
> zero-term burst (count 4, `S[15:12]` = 0, then `WAITXFI`) for an exact SINC1 sum. Source: `getxacc.yaml`
> silicon_errata + workaround (EF-069, EF-070, EF-076). No pointer to P2 Errata and no E-numbers in the text:
> the citation waits for the amended Silicon Doc. The demo's "get prior Goertzel acc's" quote was dropped (it
> described the holding-register model). Re-audit for an absolute read after a discrete burst: none — the only
> other read is the §17.1 `XCONT` loop, which reads inside the running command.
> **2026-10-02 — held, not applied.** The guide's text is the P2 Documentation's documented
> behaviour; the correction is errata E4/E5 content, and only E1 and E2 are ratified for
> publication (Stephen, 2026-10-02). A first application in «#352» was reverted before any push.
> Apply when E4/E5 are ratified. Done meanwhile (not errata): §17.1's claim that the XCONT loop
> "subtracts a baseline" (no such code) removed. Re-audit of the guide's Goertzel examples: the
> only other GETXACC site is the §10.6 read pattern (no absolute discrete read).

**Where:** `p2-streamer-programming-guide/opus-master/streamer-body.md` §10.6 *Reading Results* (:813)
and §17.1 *Reading the result: one GETXACC per command* (:1795-1799); its CHANGELOG v-entry (:96)
repeats it.
**Against:** EF-069 (Rev C): idle or in a non-Goertzel mode GETXACC clears nothing and returns the
running total; EF-070: a burst's last term is added to the NEXT Goertzel burst. Both are P2 Errata
E4/E5; KB v1.22.0 `getxacc.yaml` now states them. The guide's statements match the Silicon Doc's text
(:1604), which the silicon contradicts.
**What stays right:** read before and after and take the difference — the rule the guide gives — is
exactly what E4 requires; its "a second read returns the same numbers" holds when idle (for a
different reason).
**Correction:** rewrite both passages to the silicon behaviour (clear only during a Goertzel burst;
an idle read returns and keeps the running total), keep the difference rule with its reason, and
add the held last term (deliver it with a zero-term burst, or accept one term of carry) — pointing
to P2 Errata E4/E5 as the reader's reference. The CHANGELOG line is history and stays; the next
release's entry states the change. Re-audit the guide's Goertzel examples for an absolute read
after a discrete burst.

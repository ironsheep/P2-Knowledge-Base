# P2KB Correction Findings — ARCHIVE, swept 2026-10-05 (after the Assembly Reference v3.1.11 release)

> **This is an archive of CLOSED findings. It is never re-edited.** Ask "what is
> outstanding?" of `engineering/operations/P2KB-CORRECTION-FINDINGS.md` alone — never
> re-derive completion state from here. If an archived finding must be reopened, it
> returns as a **new** active finding that references this file.
>
> Contains 4 closed findings: F-528, F-530 and F-541 carry `DONE`, released in the P2 Assembly Language
> Reference v3.1.11 (tag `p2-assembly-language-manual-v3.1.11`) and verified on the released PDF on
> 2026-10-05 (F-530's DEBUG Window half shipped in v1.1.4); F-527 carries `RESOLVED-INVALID` — rejected
> on re-reading the sources, nothing applied. F-529 stays live until its deSilva half ships. None was the
> only finding under its section heading, so no heading moves.
>
> Swept by rename-then-trim: the register was `git mv`'d here and copied back; this copy was cut to
> the 4 findings, and the live copy had the same text removed with the edit tools. Every line below is
> the pre-sweep text (commit b6893a5a), verbatim; `audit-register-hygiene.py --sweep-check b6893a5a`
> proves it.

---

### F-527 — Assembly Reference: "13-20 clocks" for a taken hub-exec branch, at 87 lines, against its own correct rule — `RESOLVED-INVALID` (2026-10-05, «#385»)
> **Rejected on re-reading the sources.** The range is Parallax's own: the P2 Datasheet (2022/11/01)
> gives "4 / 13...20" on every branch row (`sources/p2-datasheet/p2-datasheet-text.txt:1725-1744`),
> the P2 Instructions v35 spreadsheet carries `13...20` on 63 rows, and the KB's per-instruction YAMLs
> state it in 54 files (`pasm2/jmp.yaml` `range: 4 / 13...20`). C3 removed ONE unsourced composite line
> (`instruction_skipping.yaml` `conditional_jumps_hub`) and replaced it with the Silicon Doc's minimum;
> a minimum of 13 does not contradict a 13-to-20 range, and the manual already joins the two
> (`chapter-04-timing.md:141`). The full family is 113 lines, not 87 (11 en-dash forms, 15 `13...20`
> forms) — all left as they are. Applying "13+" would have deleted a sourced upper bound at 113 sites.
> deSilva's F-532 "13+" (v3.0.9, staged) is true and stays.

The removed range (C3; Silicon Doc: "a minimum of 13 clock cycles (one more if the target is not
long-aligned)") stands at 87 lines in 8 files (plus one CHANGELOG line, history): `part-ii/instructions-j.md` (49), `-c` (10), `-t` (8),
`-d` (6), `-i` (3), `-r` (1), `part-iii/appendix-a-encoding-table.md` (8, e.g. "CALL | 4 / 13-20"),
`part-i/chapter-04-timing.md` (2); e.g. instructions-j.md:49 "taken jumps require 13-20 clock cycles
depending on hub timing". The manual's own appendix-b:168, ch04:623, :646 and ch01:202 state the correct
rule. **Fix:** "13+ (one more if the target is not long-aligned)" everywhere; table cells "4 / 13+".

### F-528 — Assembly Reference GETXACC: "both accumulators are cleared" unconditionally, no per-burst procedure — `DONE` (released in Assembly v3.1.11, 2026-10-05, verified on the PDF: page 220)
> **Applied** (`instructions-g.md` GETXACC): two Rev C silicon-note chips after the clear sentence — the
> clear acts only during a Goertzel burst (read before and after, subtract), and a burst's last term lands
> in the next (zero-term burst, count 4, `S[15:12]` = 0, then `WAITXFI`; not for SINC2). Source:
> `getxacc.yaml` silicon_errata.
`part-ii/instructions-g.md:388-410`. P2 Errata E4/E5 (Rev C): clears only during a DDS/Goertzel command;
idle reads return the running total; a read after N clocks holds N-1 terms; read before and after and
subtract (`pasm2/getxacc.yaml`). Owed under «#352» (its body names "Assembly's ... GETXACC ... entries"),
never registered until now. **Fix:** at «#352».

### F-530 — DEBUG_TIMESTAMP taught as "the 64-bit CT value" with no stale-window caveat — `DONE` (low; DEBUG Window half released in v1.1.4, 2026-10-04; Assembly half released in v3.1.11, 2026-10-05, verified on the PDF: page 468)
> **Assembly applied** (`appendix-e-constants.md` DEBUG_TIMESTAMP): a Rev C chip in the DEBUG Window's
> wording, pointing to GETCT for the cure.
> **DEBUG Window half applied and released (v1.1.4, 2026-10-04, `p2-debug-window-manual-v1.1.4`).** ch14 carries
> the rule as a Rev C silicon-note chip (the new platform tag, 3aa14a43): the stamp is the sending cog's own
> counter copy, so a cog whose group of four had no running cog at a wrap is a whole number of wraps behind.
> Source: `special-configuration-symbols.yaml` DEBUG_TIMESTAMP caveat. Verified on the PDF, p136. **Owed:**
> Assembly `appendix-e-constants.md:685`, at the Assembly Reference release («#385»).
D18. DEBUG Window `ch14-multiwindow-pasm.md:132-135`; Assembly `part-iii/appendix-e-constants.md:685`.
`special-configuration-symbols.yaml` caveat: the stamp is the sending cog's own counter copy; a cog in a
stale window stamps one wrap early and prints out of order. **Fix:** one sentence each.

### F-541 — Assembly Reference: crystal/PLL settle times disagree inside the manual — `DONE` (released in Assembly v3.1.11, 2026-10-05, verified on the PDF: pages 76, 222)
> **Settled:** `instructions-h.md:67` is right — 5 ms crystal, 10 ms crystal + PLL (P2 Datasheet :828-834,
> Silicon Doc part3 :576-580, `clock_system.yaml` stabilization_timing, whose `conflict_resolved` notes the
> sourceless "~10 µs"). `chapter-04-timing.md:66` now states the same.
`part-i/chapter-04-timing.md:66` (crystal ~10 ms, PLL ~10 µs) against `part-ii/instructions-h.md:67`
(5 ms crystal, 10 ms crystal + PLL). Seen by the audit, not an inventory fact. **To do:** settle against
the Silicon Doc and the KB (`architecture/clock_system.yaml` stabilization_timing), fix the losing side.

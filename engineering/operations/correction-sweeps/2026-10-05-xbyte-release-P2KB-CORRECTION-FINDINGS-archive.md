# P2KB Correction Findings — ARCHIVE, swept 2026-10-05 (after the XBYTE Guide v1.1.1 release)

> **This is an archive of CLOSED findings. It is never re-edited.** Ask "what is
> outstanding?" of `engineering/operations/P2KB-CORRECTION-FINDINGS.md` alone — never
> re-derive completion state from here. If an archived finding must be reopened, it
> returns as a **new** active finding that references this file.
>
> Contains 2 findings carrying a `DONE` status token: F-537 and F-538, both released in the P2
> Interpreters & Emulators Guide v1.1.1 (tag `p2-xbyte-programming-guide-v1.1.1`) and verified on the
> released PDF on 2026-10-05. Neither was the only finding under its section heading, so no heading
> moves.
>
> Swept by rename-then-trim: the register was `git mv`'d here and copied back; this copy was cut to
> the 2 findings, and the live copy had the same text removed with the edit tools. Every line below is
> the pre-sweep text (commit 962127d1), verbatim; `audit-register-hygiene.py --sweep-check 962127d1`
> proves it.

---

### F-537 — XBYTE guide: SKIPF shared bodies use a relative `call #` before an instruction the pattern may skip — `DONE` (high; released in XBYTE v1.1.1, 2026-10-05, verified on the PDF: pages 26-27, 74; bench EF-092)
> **Applied.** Rule confirmed at `silicon-doc-text.txt:889`. §4.5 states it (where the next line may be skipped,
> the CALL's immediate must be absolute; CALLPA/CALLPB take a register). `call #\pop_two` in all three ALU-body
> copies (§4.4, §15.2, §15.5) and the example (`xbyte-growing-vm.spin2`; .bin differs in that one long only).
> **Evidence-scoping:** of the named sites, only the ALU body has the hazard — its SUB/AND/OR patterns skip the
> `add` after the call. `h_cmplt` (:72) runs with pattern 0 (no skipping) and `br`'s `call #pop_x` is skipped
> together with the line after it (JMP), so both stay relative; every other guide CALL is outside a skip body or
> followed by a never-skipped `ret`. **Bench:** `audit/verification-tests/test-f537-absolute-call-skip.spin2`
> runs the example's two jobs with the absolute form (A, gating: vars 0/15/8/15/1) and with the relative form
> (B, characterization). **Run 2026-10-04 (Stephen), twice, identical → EF-092:** A PASS (0/15/8/15/1);
> B RELATIVE-MISBEHAVES (0/126,768/0/0/0) — the rule is load-bearing on silicon. §4.5 now says so in one
> clause. KB: `instruction_skipping.yaml:112` already states the rule from the Silicon Doc (:889) and needs
> no change; EF-092 joins its sources at the next KB release (F-546; a YAML edit now would hold every
> manual release behind `kb-content-released`). Its SKIP `conditional_block` example (:133) is not affected — the
> rule is for SKIPF sequences.
C18; Silicon Doc "Special SKIPF Branching Rules": a CALL's immediate address must be absolute
(`#\address`) wherever the instruction after it might be skipped. `xbyte-body.md:282-283` (`call #pop_two`
then `add x, y 'a | | |`), :1448-1453, :1563-1576, and the runnable `examples-library/xbyte-growing-vm.spin2:63`
and `:72`. The guide never states the rule (its §4.5 covers only the call-suspends-skipping half). Real
XBYTE code in the reference set writes `call #\label` there (NeoYume `neoyume_lower.spin2`, the PSRAM
drivers). No silicon run of these variants is recorded. **Fix:** `call #\pop_two` (and every such CALL);
state the rule in §4.5; re-run the example's skipping variants on the bench.

### F-538 — XBYTE guide: a cancelled instruction "still spends its clocks"; the 8-level stack "wraps" — `DONE` (low; released in XBYTE v1.1.1, 2026-10-05, verified on the PDF: pages 22, 24, 79, 98)
> **Applied.** Against `silicon-doc-text.txt:780` (cancelled instructions become 2-clock NOPs): §4.1 (two
> sentences) and the §20.1 SKIP row now say each cancelled instruction costs 2 clocks. Stack: §12.4's caution
> heading and §15.6 say "overflows without faulting"; no other wrap claim in the guide. Also in this release:
> E7 as a Rev C note at §5.1 (`rdfast.yaml` silicon_errata), and the guide adopts metadata single-source,
> rights metadata, crossref and silicon notes.
- C12: `xbyte-body.md:224` "SKIP's cost is the cost of the instructions it skips over", :211-212, :2272 —
  the Silicon Doc: cancelled instructions become 2-clock NOPs.
- C4: :1176 "The stack drift wraps with no fault", :1687 "the hardware wraps without faulting" — the
  Silicon Doc says only "8-level hardware stack"; what overflow does is unsourced (the KB removed the same
  "wraps around" claim). The caution itself stands. **Fix:** "each skipped instruction costs 2 clocks";
  "overflows without faulting".

# Campaign — 2026-10 KB findings decided on the bench

**Purpose:** settle on real silicon two questions the 2026-10-04 impact audit («#378») left open,
where a document and the KB disagreed and no source decided it. Stephen, 2026-10-04: "should be
proven on bench so we know truth".

**Result: both `CONFIRMED` → EF-090, EF-091**, each on its first run, 2026-10-03 (Stephen). A third
test, added 2026-10-04 for F-537, `CONFIRMED` → EF-092 (two runs, identical).

| # | Test (`tests/`) | Question | Finding | Verdict | EF |
|---|---|---|---|---|---|
| 1 | `test-f526-sync-tx-prime-in-reset.spin2` | sync serial TX `%11100`, continuous mode: is a word written with WYPIN during reset sent, or lost? | F-526 | `CONFIRMED` — sent (Silicon Doc right; the KB's v1.23.0 rule wrong); enable-first loses the first word and sends the second twice | EF-090 |
| 2 | `test-f540-augs-skip-pattern-bit.spin2` | does the AUGS a `##` operand emits take its own skip-pattern bit? | F-540 | `CONFIRMED-COUNTS` — yes, under SKIP and SKIPF; a skipped instruction leaves its AUGS pending | EF-091 |
| 3 | `test-f537-absolute-call-skip.spin2` | in an XBYTE shared body, does a relative `call #` before a skippable line work, or must it be `call #\`? (added 2026-10-04) | F-537 | `A PASS` — the absolute form runs the guide's VM right; the relative form corrupted 4 of 5 variables | EF-092 |

Both tests need no wiring (F-526 routes its clock and data through the smart pins' internal
relative-pin input selectors on P4-P6; F-540 uses no pins). Each prints its pre-registered outcomes
before measuring and gates on a control. Workspace copies and raw logs live in
`engineering/document-production/manuals/p2-io-and-smart-pins-user-guide/audit/verification-tests/`
and `…/p2-xbyte-programming-guide/audit/verification-tests/` (git-ignored); the sources here are
byte-identical to the builds that ran.

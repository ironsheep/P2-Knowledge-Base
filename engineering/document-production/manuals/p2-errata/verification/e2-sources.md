# E2 verification sidecar: Erratum E2, An Immediate ALTx Takes a Pending AUGS

Chapter: `opus-master/e2-altx-takes-pending-augs.md` (line numbers below are the chapter's,
as of the #360 workaround wording, 2026-09-26). Every number, quotation and code excerpt in
the chapter maps to a source here.

**v0.2.0 reshape (2026-09-26, task #359).** The chapter was restructured to the v0.2.0 shape:
CAUTION box, opening, and the eight fixed headings (*What the P2 is documented to do*, *What
the P2 does*, *What your program sees*, *The fix*, *Why it happens*, *How it was
proven on P2 hardware*, *The test program*, *Status*). New in v0.2.0: the P2 Documentation's
*REGISTER INDIRECTION* statement is quoted (PDOC:1017-1018). **The printed fix now comes from
the rig** (§3a): RIG:466-468, the A5 arm that ran on silicon. The v0.1.0 compile harness HARN is
kept unchanged; the v0.2.0 chapter takes only its one-operand encoding check from it (§4).

**Workaround wording (2026-09-26, task #360; Stephen's decision, voice-guide §2).** The reader's
change is a *workaround*, never a *fix* (a fix is a silicon revision). Section *The fix*
(`{#sec-e2-fix}`) is now *A proven workaround* (`{#sec-e2-workaround}`), rule-first: *What any
workaround must do* (chapter 101-102, the condition as in the front matter's summary table),
then *One way, proven on P2 hardware* (104) and the block. The CAUTION box's third line is
*Workaround* (the condition, chapter 10-11); the status row is *Workaround proven on silicon*.
New prose: chapter 128-129 (other arrangements meet the same condition; none other run). In
ARCHIVE `ARM_FIX` is renamed `ARM_WORKAROUND` (ARCHIVE:48, 51, 53, 315, 324, 333, 409) and the
header purpose says *workaround*: no line added or removed, so every ARCHIVE line number below
still holds, and the object image is byte-identical to the pre-#360 archive (pnut-ts 1.55.8,
`-d` and without). RIG and the logs are the as-run record and keep their own wording.

Path abbreviations:

- **M** = `engineering/document-production/manuals/p2-errata/`
- **LEDGER** = `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md`
- **PDOC** = `engineering/ingestion/sources/silicon-doc/p2-documentation.txt`
- **PBLK** = `engineering/ingestion/sources/silicon-doc/assets/code-2026-08-26/block-002.txt`
  (the same Parallax example, extracted with its column layout intact)
- **RIG** = `M/audit/verification-tests/test-o1-altx-imm-s-steals-augs.spin2`
  (byte-identical to `hardware-verification/campaigns/2026-09-p2-errata-predictions/tests/`
  copy: `cmp` returns no difference)
- **LOG2** = `M/audit/verification-tests/logs/debug_260924-231746.log` (run 2, the build
  on disk: `.bin` 13114 bytes, LOG2:14)
- **LOG1** = `M/audit/verification-tests/logs-orig/debug_260924-204650.log` (run 1, first
  build: `.bin` 13075 bytes, LOG1:14)
- **KB** = `deliverables/ai/P2/language/pasm2/`
- **HARN** = `M/verification/e2-harness-register-s.spin2` (v0.1.0 compile harness)

RIG re-checked 2026-09-26 for v0.2.0: a scratch copy compiled with `/usr/local/bin/pnut-ts -d`
(v1.55.8) wrote 13114 bytes (LOG2:14 size) and is `cmp`-identical to
`M/audit/verification-tests/test-o1-altx-imm-s-steals-augs.bin`; `diff -q` against the campaign
copy prints nothing. The campaign copy has one commit in history (`e3287fb8`); commit
`8b5dd8df` did not touch it.

---

## 1. Raw log lines (verbatim)

LOG2, lines 21 and 25-48:

```
[2026-09-24T23:17:46.845] Cog0  AUGV=$3C5C_0A55 LO=$0000_0055 autoinc=5 AUGVD=$1357_9B3C LOD=$0000_013C
[2026-09-24T23:17:46.846] Cog0  pass 0 ran in cog 1
[2026-09-24T23:17:46.846] Cog0  pass 1 ran in cog 1
[2026-09-24T23:17:46.846] Cog0  pass 2 ran in cog 1
[2026-09-24T23:17:46.846] Cog0  pass0 magic=$0100_A1A1 win cog addr=$0000_0062 idx0 = win addr + 8
[2026-09-24T23:17:46.847] Cog0  A0 ctrl bare MOV #$055 : nchg=1 first win[8]=$0000_0055 dIdx=0 idxRaw=$0000_006A tag=0
[2026-09-24T23:17:46.848] Cog0       changed win[8] = $0000_0055  (sentinel was $5E5E_0008)
[2026-09-24T23:17:46.848] Cog0  A1 ctrl AUGS / MOV : nchg=1 first win[8]=$3C5C_0A55 dIdx=0 idxRaw=$0000_006A tag=1
[2026-09-24T23:17:46.849] Cog0       changed win[8] = $3C5C_0A55  (sentinel was $5E5E_0108)
[2026-09-24T23:17:46.850] Cog0  A2 ctrl ALTD idx,#0 (no AUGS) : nchg=1 first win[8]=$0000_0055 dIdx=0 idxRaw=$0000_006A tag=2
[2026-09-24T23:17:46.850] Cog0       changed win[8] = $0000_0055  (sentinel was $5E5E_0208)
[2026-09-24T23:17:46.851] Cog0  A3 ctrl ALTD idx,reg $A00 (autoinc +5) : nchg=1 first win[8]=$0000_0055 dIdx=5 idxRaw=$0000_006F tag=3
[2026-09-24T23:17:46.852] Cog0       changed win[8] = $0000_0055  (sentinel was $5E5E_0308)
[2026-09-24T23:17:46.852] Cog0  A4 ctrl ALTR idx,#3 (no AUGS) : nchg=1 first win[11]=$0000_0055 dIdx=0 idxRaw=$0000_006A tag=4
[2026-09-24T23:17:46.853] Cog0       changed win[11] = $0000_0055  (sentinel was $5E5E_040B)
[2026-09-24T23:17:46.854] Cog0  A5 ctrl WORKAROUND AUGS / ALTD idx,reg 4 / MOV : nchg=1 first win[12]=$3C5C_0A55 dIdx=0 idxRaw=$0000_006A tag=5
[2026-09-24T23:17:46.854] Cog0       changed win[12] = $3C5C_0A55  (sentinel was $5E5E_050C)
[2026-09-24T23:17:46.855] Cog0  A6 TEST AUGS / ALTD idx,#0 / MOV : nchg=1 first win[8]=$3C5C_0A55 dIdx=5 idxRaw=$0000_006F tag=6
[2026-09-24T23:17:46.856] Cog0       changed win[8] = $3C5C_0A55  (sentinel was $5E5E_0608)
[2026-09-24T23:17:46.856] Cog0  A7 TEST AUGS / ALTR idx,#3 / MOV : nchg=1 first win[11]=$3C5C_0A55 dIdx=5 idxRaw=$0000_006F tag=7
[2026-09-24T23:17:46.857] Cog0       changed win[11] = $3C5C_0A55  (sentinel was $5E5E_070B)
[2026-09-24T23:17:46.863] Cog0  D1 ctrl hub=$1357_9B3C  D2 test hub=$1357_9B3C  idxs before=$0000_0061 after=$0000_0061
[2026-09-24T23:17:46.863] Cog0  passes differing longs vs pass 0: 0
[2026-09-24T23:17:46.864] Cog0  A6 ALTD class=steal-not-cancelled (O1 TRUE)  A7 ALTR class=steal-not-cancelled (O1 TRUE)  D2 AUGD immune=yes
[2026-09-24T23:17:46.880] Cog0  VERDICT: CONFIRMED - immediate-#S ALTD and ALTR both took the AUGS (idx +5) and the target still got $3C5C0A55; AUGD survived ALTS
```

LOG1, lines 21 and 25-48: the same text after the timestamp, line for line (read side by
side; every measured value identical). The lines carrying the numbers:

```
[2026-09-24T20:46:51.500] Cog0  A0 ctrl bare MOV #$055 : nchg=1 first win[8]=$0000_0055 dIdx=0 idxRaw=$0000_006A tag=0
[2026-09-24T20:46:51.501] Cog0  A1 ctrl AUGS / MOV : nchg=1 first win[8]=$3C5C_0A55 dIdx=0 idxRaw=$0000_006A tag=1
[2026-09-24T20:46:51.502] Cog0  A2 ctrl ALTD idx,#0 (no AUGS) : nchg=1 first win[8]=$0000_0055 dIdx=0 idxRaw=$0000_006A tag=2
[2026-09-24T20:46:51.503] Cog0  A3 ctrl ALTD idx,reg $A00 (autoinc +5) : nchg=1 first win[8]=$0000_0055 dIdx=5 idxRaw=$0000_006F tag=3
[2026-09-24T20:46:51.505] Cog0  A4 ctrl ALTR idx,#3 (no AUGS) : nchg=1 first win[11]=$0000_0055 dIdx=0 idxRaw=$0000_006A tag=4
[2026-09-24T20:46:51.506] Cog0  A5 ctrl WORKAROUND AUGS / ALTD idx,reg 4 / MOV : nchg=1 first win[12]=$3C5C_0A55 dIdx=0 idxRaw=$0000_006A tag=5
[2026-09-24T20:46:51.508] Cog0  A6 TEST AUGS / ALTD idx,#0 / MOV : nchg=1 first win[8]=$3C5C_0A55 dIdx=5 idxRaw=$0000_006F tag=6
[2026-09-24T20:46:51.508] Cog0       changed win[8] = $3C5C_0A55  (sentinel was $5E5E_0608)
[2026-09-24T20:46:51.509] Cog0  A7 TEST AUGS / ALTR idx,#3 / MOV : nchg=1 first win[11]=$3C5C_0A55 dIdx=5 idxRaw=$0000_006F tag=7
[2026-09-24T20:46:51.515] Cog0  D1 ctrl hub=$1357_9B3C  D2 test hub=$1357_9B3C  idxs before=$0000_0061 after=$0000_0061
[2026-09-24T20:46:51.516] Cog0  passes differing longs vs pass 0: 0
```

---

## 2. Numbers and facts, by chapter line

| Ch. line | Claim | Source |
|---|---|---|
| 4-5 | CAUTION *Expected*: a nine-bit immediate `#S` leaves the `ALTx`'s `D` register unchanged; section *REGISTER INDIRECTION* | PDOC:1012 (heading), PDOC:1017-1018 ("Normally, a nine-bit #address will be used for S, causing S[17:9] to be zero, so that D is unaffected") |
| 7-8 | CAUTION *Actual*: between `AUGS` and its target the `ALTx` takes the augment too; its `D` moves by bits 17:9 of the augmented value | LOG2:41-44 (A6/A7 `dIdx=5`, target `$3C5C_0A55`); LEDGER:899-903 |
| 10-11 | CAUTION *Workaround*: no immediate-`#S` `ALTx` between an `AUGS` and its target | PDOC:212-216 (the arrangement and Parallax's direction); LOG2:39 (A5); LEDGER:908-909 |
| 14-16 | opening: explicit `AUGS`, immediate-`#S` `ALTx` between it and its target, as in Parallax's example | PDOC:217-227 |
| 16-18 | `##` does not produce the arrangement: the assembler places the `AUGS` immediately before the `##` instruction | KB `augs.yaml`:29-33 ("the compiler will automatically invoke AUGS immediately before"); PDOC:7153-7154 (PTRx case), PDOC:12953-12954 ("use "##" ... to invoke AUGS/AUGD") |
| 18 | Parallax publishes the defect in the P2 Documentation | PDOC:197, 212-216 |
| 22-24 | `AUGS` holds 23 bits for the next literal `#S`; lower 9 from the instruction; augment cancelled / does not persist | KB `augs.yaml`:5-15, 23-24 |
| 24-25 | `ALTx` `S` = register, 9-bit literal or augmented literal | KB `altd.yaml`:5, 9; `altr.yaml`:5, 9; `alts.yaml`:5, 9 |
| 27-29 | *REGISTER INDIRECTION*: `ALTS`/`ALTD`/`ALTR` sum `D[8:0]` and `S[8:0]` into the address substituted into the next instruction; `S` a register base, `D` an index (paraphrase) | PDOC:1012-1016 ("These instructions sum their D[8:0] and S/#[8:0] values to compute an address that is directly substituted into the next instruction's S field, D field, or result register address ... S/# can serve as a register base address and D can be used as an index.") |
| 31-33 | blockquote 1 (exact; the source's line break joined with a single space) | PDOC:1017-1018 |
| 35 | published under KNOWN BUGS | PDOC:197 |
| 37-43 | blockquote 2 (exact; line breaks of the source joined with single spaces) | PDOC:212-216 |
| 45-47 | example `AUGS #$FFFFF123` / `ALTD index,#base` / `ADD 0-0,#$123`; comment "Look out! AUGS will affect #base, too. Use a register, instead." | PDOC:217-227 (columns split by extraction); PBLK:1-3 (intact) |
| 47-49 | Parallax names `AUGS` only for this item; no `AUGD` | PDOC:212-227 (read); KB `augs.yaml`:72 (`scope_note` says the same) |
| 56-57 | `ALTx` receives the augmented `S`: bits 31:9 from `AUGS`, 8:0 its own | LEDGER:899-903; RIG:22-28; KB `altd.yaml`:5, 9, 40-41 |
| 58 | augment not cancelled; target receives it | LOG2:41-44; LEDGER:899-900 |
| 59-60 | target cancelling is Parallax's statement; no instruction after the target was checked | PDOC:213-214; RIG:471-485 (target followed directly by `call #dump`) |
| 62-68 | base unchanged; `S[17:9]` from the `AUGS`, sign-extended into `D`; `$3C5C_0A55`, bits 17:9 = 5; `ALTD idx,#0` and `ALTR idx,#3` each moved `idx` by 5; target wrote `$3C5C_0A55` | LOG2:21 (`autoinc=5`), LOG2:41-44; RIG:136-138; LEDGER:904-906; PDOC:1017 (sign-extended) |
| 70-74 | tested `ALTD`, `ALTR` only; directly adjacent; one augment value; `AUGS` for the `ALTx` itself not tested | RIG:37-57, 466-485; LEDGER:903-906 |
| 76-79 | `AUGD #$1357_9B3C` / `ALTS idxs,#0` / `WRLONG #$13C` wrote `$1357_9B3C`; `idxs` unmoved; one `ALTx` | LOG2:45; RIG:139-140, 492-499; LEDGER:909-912 |
| 83-85 | 9-bit immediate has bits 17:9 clear, so auto-increment 0 on its own | PDOC:1017-1018; KB `altd.yaml`:9 ("9-bit literal"); RIG:26, 30 ("A bare #0 moves it by 0"); LOG2:33, 37 (A2, A4: dIdx=0) |
| 91-93 | redirected to named register; full value; no other register in the 32-register window written | LOG2:41-44 (`nchg=1`, `win[8]`, `win[11]`); RIG:37-39, 143 (`WIN_N = 32`) |
| 95-97 | size of move set by bits 17:9; zero → nothing (by documented split, stated as such); only 5 measured | PDOC:1017-1018; KB `altd.yaml`:5, 40-41; RIG:136 |
| 101-102 | *What any workaround must do*: no immediate-`#S` `ALTx` between an `AUGS` and its target | PDOC:212-216; LOG2:41-44 (the arrangement is what moves `idx`); front matter summary table |
| 104 | *One way*: a register `S` on that `ALTx` | PDOC:215-216 (Parallax's own direction); LOG2:39 (A5) |
| 107-109 | drop-in block | RIG:466-468 (byte-identical; see §3a) |
| 112-113 | guarantee: the `ALTD` takes nothing from the `AUGS`, `idx` does not move, the augment reaches the target; *rule at each use* | LOG2:39-40 (A5: `nchg=1 first win[12]=$3C5C_0A55 dIdx=0`), LOG1:39; LEDGER:908-909; kind per creation-guide §5 |
| 115-117 | `AUGV` = the 32-bit value; `LO` = its low 9 bits; `sreg4` holds base 4 in bits 8:0, zero auto-increment in 17:9 | RIG:136-137 (`AUGV`, `LO = AUGV & $1FF`), RIG:145 (`S4 = 4`), RIG:534 (`sreg4 long S4 ' register S: base 4, auto-index 0`) |
| 118-120 | `AUGV` = `$3C5C_0A55`; `MOV` redirected to the register four along from `idx`'s (`win[12]` vs `win[8]`), which received `$3C5C_0A55`; `idx` unmoved | LOG2:21, LOG2:28 (`idx0 = win addr + 8`), LOG2:39-40 |
| 120-121 | cost: one cog register per distinct `S` value | direct consequence of the register form (the `S` value must be held in a cog register: RIG:534; PDOC:215-216); not a measured claim |
| 123-126 | `ALTD idx` = same word as `ALTD idx,#0`, immediate bit set, `S` = 0; same form the test ran | HARN:35-36 compiled (v0.1.0): both `$F98C0A00` (listing offsets `$40`, `$44`); RIG:113-114 (A6 word `$F98CBA00`, I=1, S=0); RIG:95-98 |
| 125-126 | one-operand form of every `ALTx` has the immediate bit set (so it does not meet the condition) | KB encodings, syntax-2 rows: `altd.yaml`:34, `altr.yaml`:34, `alts.yaml`:34, `altb.yaml`:35, `alti.yaml`:32, `altsn.yaml`:35, `altgn.yaml`:9, `altsb.yaml`:26, `altgb.yaml`:35, `altsw.yaml`:26, `altgw.yaml`:35 (last three bits of the opcode group end in 1 = I) |
| 128-129 | other arrangements that keep every immediate-`#S` `ALTx` out of the `AUGS`-to-target span meet the same condition; none other run on silicon | follows from the condition (PDOC:212-216 names only the in-between arrangement); RIG:37-57 (the arm table: A5 is the only arm of that kind) |
| 131-133 | this way run with `ALTD` only, one augment value, one base; Parallax directs a register `S` for any `ALTx`; no other `ALTx` run with one | RIG:49-51 (A5 is the only register-`S` arm with an `AUGS` pending), RIG:463-469; PDOC:215-216 |
| 137 | `AUGS` changes nothing in memory | KB `augs.yaml`:23-24 |
| 141-144 | the `ALTx` exemption is meant to let the augment reach a later target; Parallax quote "will use and cancel the AUGS value, as expected" | PDOC:213-214 (quote exact); mechanism paraphrased at programmer's-model level from the study brief (not quoted; no names, no line refs) |
| 145-149 | selection of the receiving instruction treats an immediate-`S` `ALTx` like any immediate-`S` instruction; the `ALTx` leaves the augment pending | paraphrase of the study brief's mechanism; outcome confirmed LOG2:41-44 |
| 151-152 | a register `S` has no immediate `S` to augment; "why the workaround holds" | LOG2:39 (A5 `dIdx=0`, `win[12]=$3C5C_0A55`); PDOC:215-216 |
| 154-156 | effect confined to the auto-increment: base bits 8:0 untouched, bits 17:9 move `D` | PDOC:1013-1018; LOG2:41-44 |
| 158-161 | `ALTx` encodings carry an immediate bit for `S` only; `D` always a register | KB `altd.yaml`:29 (`01I DDDDDDDDD SSSSSSSSS`, no L bit), same pattern in every `alt*.yaml` two-operand row; LEDGER:911 |
| 165 | P2 board, nothing on its pins, 200 MHz | RIG:33 ("bare P2 board, no pins, no jumpers"), RIG:132; LEDGER:892-893 |
| 165-169 | PASM cog started by `COGINIT` from `DAT`; debug interrupt cog 0 only `%0000_0001`; no interrupts in measuring cog; cog 0 reads and prints | RIG:33-35, 133, 198, 414-415; LOG2:25-27 (passes ran in cog 1); LEDGER:889-890 |
| 169-172 | window of 32; sentinel per arm and slot; arm A6 slot 8 = `$5E5E_0608`; `idx` = cog address of `win[8]` | RIG:37-39, 143-144, 167, 298, 505-517; LOG2:42; LOG2:28 (`win cog addr=$0000_0062`, `idx0 = win addr + 8`) |
| 172 | window and `idx` copied to hub after each arm | RIG:519-527 |
| 173-174 | augment `$3C5C_0A55`: bits 8:0 `$055`, bits 17:9 = 5 | RIG:136-138; LOG2:21 |
| 176-177 | "moved" = `idx` after minus `idx` before | RIG:308, 327 |
| 181-188 | arm table: every Written / Value / Moved cell | LOG2:29, 31, 33, 35, 37, 39, 41, 43 (and LOG1 same lines); sequences RIG:429-485; `sinc` = `AUTOINC << 9` = `$A00` per LOG2:35 label and RIG:533; `sreg4` = 4 RIG:145, 534 |
| 190 | exactly one window register changed in every arm | `nchg=1` on LOG2:29, 31, 33, 35, 37, 39, 41, 43 |
| 190-191 | no verdict unless controls exact | RIG:220-241 |
| 193-195 | A3: `S[17:9]`=5 moves `idx` by 5, redirected register stays `win[8]` | LOG2:35-36 |
| 195-196 | A5 = the workaround, the three lines printed in *A proven workaround* | RIG:463-469 contains RIG:466-468 (§3a) |
| 199-204 | `$D5D5_D5D5` sentinel; D1 `$1357_9B3C`; D2 `$1357_9B3C`; `idxs` `$0000_0061` before and after; `idxs` = cog address of the hub-pointer register | RIG:168, 487-499, 55-57, 107-108 (`hubd2=$061`); LOG2:45 |
| 206-210 | three passes, fresh cogs, compared long for long, identical; run twice on 2026-09-24 from two builds; values matched | RIG:77-82, 164, 195-198, 243-251; LOG2:25-27, 46; LOG1:25-27, 46; LEDGER:892-894 |
| 212-214 | opcodes read back from the listing; `AUGS` = `$FF1E2E05` | RIG:105-123 (line 109) |
| 218-222 | filename; `pnut-ts -d` or PNut; about 40 lines, one `VERDICT:` or `RIG FAIL:` | RIG:3, 125-128 |
| 233 | "The workaround arm and the `ALTD` test arm differ only in the form of the `ALTD`'s `S`" | RIG:463-477 (A5 `altd idx, sreg4` vs A6 `altd idx, #0`; every other line identical apart from `armn`) |
| 282 | status "Yes — 2026-09-24, on a P2 board at 200 MHz, run twice" | wording fixed by the chapter brief; facts LEDGER:892-894, LOG1:1, LOG2:1 |
| 283 | workaround proven on silicon: Yes, 2026-09-24, rule at each use, register `S` (run with `ALTD`) | LOG2:39, LOG1:39; LEDGER:908-909; LEDGER:893 (date) |

---

## 3. Code excerpts from the test program (verbatim, contiguous; printed lines now mirror ARCHIVE)

**Printed code now mirrors the conformed archive copy (2026-09-26, «#360»); the measuring PASM
is byte-identical to the as-run rig.** ARCHIVE = `examples-library/e2-altx-takes-pending-augs-test.spin2`
(conformed 2026-09-26, task #360: named `ARM_FIX`/`ARM_TD` in place of `#5`/`#6`, `ALTD_REG_BASE`
in place of `S4`, `ALT_INC_SHIFT` in place of the literal `9`; the two `AUGV`/`LO`/`AUTOINC`
and `sinc` lines that grew past K=76 columns with the new names are described in prose instead
of fenced — see chapter 231 and 254-255; PASM measuring image byte-identical to RIG's; later
in #360 `ARM_FIX` became `ARM_WORKAROUND`, see the note at the top).

| Ch. lines (post-#360 wording) | Fence | RIG lines (as-run, history) | ARCHIVE lines (printed) | Max width |
|---|---|---|---|---|
| 106-110 (`pasm2`, *A proven workaround* drop-in; unchanged by #360) | `pasm2` | 466-468 | ARCHIVE:411-413 | 34 |
| 227-228 (`spin2`, `AUGV`/`LO` only; `AUTOINC` moved to prose, chapter 231) | `spin2` | 136-137 | ARCHIVE:28-29 | 75 |
| 236-251 (`pasm2`, A5/A6 arms, named `ARM_WORKAROUND`/`ARM_TD`) | `pasm2` | 463-477 | ARCHIVE:408-422 | 74 |
| 258 (`pasm2`, `sreg4` only; `sinc` moved to prose, chapter 254-255) | `pasm2` | 534 | ARCHIVE:479 | 75 |
| 265-272 (`pasm2`; unchanged by #360) | `pasm2` | 492-499 | ARCHIVE:437-444 | 69 |

Re-check (pre-#360): `grep -n -x -F -f <chapter> <RIG>` listed every RIG line of these five
ranges. Post-#360, the chapter's fences equal the ARCHIVE spans above (verified by
`engineering/tools/verify-example-corpus-identity.py`, GREEN); RIG is kept as the as-run record
(names differ from ARCHIVE; the measuring PASM itself is unchanged). RIG:135 (77 columns) was
deliberately left out of the `spin2` excerpt in both. The A5 comment line (RIG:463 / ARCHIVE:408)
prints the rig's own label `WORKAROUND`; it is carried verbatim (an excerpt is never edited),
and the prose around it calls A5 the workaround.

---

## 3a. The drop-in block (*A proven workaround*): from the rig that ran

Chapter 107-109 is byte-identical to RIG:466-468, the body of arm A5 (the workaround arm):

```
                augs    #AUGV
                altd    idx, sreg4
                mov     0-0, #LO
```

- **Contiguity and width:** consecutive RIG lines; widths 29, 34, 32 columns (K = 76).
- **Symbols:** `AUGV` = `$3C5C_0A55` (RIG:136), `LO` = `AUGV & $1FF` = `$055` (RIG:137),
  `sreg4` = `S4` = 4 (RIG:145, 534), `idx` = cog address of `win[8]` before the arm
  (RIG:516, LOG2:28). Encodings from the listing (RIG:109, 116, 120): `augs #AUGV` =
  `$FF1E2E05`, `altd idx,sreg4` = `$F988BA59` (I=0, register `S`), `mov 0-0,#$055` = `$F6040055`.
- **The run that proved it:** A5 is a control (RIG:49-51, N_CTRL = 6 at RIG:149): the program
  gives no verdict unless it reads `nchg=1`, `win[12]` = `$3C5C_0A55`, `dIdx=0` in every pass
  (RIG:232-235, `expi`/`expv`/`expd` at RIG:361, 369, 377). Run 2 (LOG2, the build on disk):
  LOG2:39-40 `A5 ctrl WORKAROUND AUGS / ALTD idx,reg 4 / MOV : nchg=1 first win[12]=$3C5C_0A55 dIdx=0`,
  three passes bit-identical (LOG2:46 `passes differing longs vs pass 0: 0`). Run 1 (LOG1,
  first build, same measuring code per LEDGER:893-894): LOG1:39, same values; LOG1:46 `0`.
  Both 2026-09-24, P2 board, 200 MHz (LEDGER:892-894).
- **Kind:** rule at each use (the register `S` is applied at each `ALTx` placed between an
  `AUGS` and its target; proven for `ALTD` only).

---

## 4. v0.1.0 workaround snippet: compile record (history)

HARN is kept unchanged. Its snippet (HARN:24-31) was the v0.1.0 chapter's workaround block and
is not printed in v0.2.0. Its encoding check (HARN:35-36) is still the source for the
chapter's one-operand-form paragraph (chapter 123-126). The v0.1.0 record follows.

- Snippet: chapter 94-101 = HARN:24-31 (byte-identical: `grep -n -x -F -f <chapter> <HARN>`
  lists HARN:24-27 and 29-31; 28 is the blank line). Widths: 65, 71, 66, 26, 0, 69, 58, 28.
- Compiler: `/usr/local/bin/pnut-ts` reports `PNut-TS: v1.55.8`.
- Command (the harness was copied to the session scratchpad first, because pnut-ts writes
  its `.lst`/`.bin` beside its input):
  `/usr/local/bin/pnut-ts -l <scratch>/e2-harness-register-s.spin2`
- Result: `pnut-ts: Wrote <scratch>/e2-harness-register-s.bin (6364 bytes)` / `pnut-ts: Done`.
- Listing words (little-endian hex dump, hub offsets): `$08` `$FF1E2E05` (`augs`, same
  word as RIG:109), `$0C` `$F9880A04` (`altd idx,rbase`: I=0, D=`$005`, S=`$004`), `$10`
  `$F6040055` (`mov 0-0,#$055`), `$18` `$00000006` (`rbase` = cog address of `table`),
  `$40` `$F98C0A00` (`altd idx`), `$44` `$F98C0A00` (`altd idx,#0`).
- No `debug()` in the harness, so no `-d`.

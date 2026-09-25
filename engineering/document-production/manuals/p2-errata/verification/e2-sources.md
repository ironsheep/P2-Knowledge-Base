# E2 verification sidecar: Chapter 2, An Immediate ALTx Takes a Pending AUGS

Chapter: `opus-master/e2-altx-takes-pending-augs.md` (line numbers below are the chapter's).
Every number, quotation and code excerpt in the chapter maps to a source here.

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
- **HARN** = `M/audit/verification/e2-harness-register-s.spin2`

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
| 3-6, 46-49, 136-139 | augment fills `S[31:9]`, `ALTx`'s own `S[8:0]` kept; `S[17:9]` becomes the auto-increment; `D` register moves | LEDGER:899-903; KB `altd.yaml`:5, 9, 40-41; `altr.yaml`:5, 9; RIG:22-28 |
| 7-8, 107-111 | workaround confirmed on silicon: register `S` of 4 → `win[12]`=`$3C5C_0A55`, `idx` unmoved | LOG2:39-40, LOG1:39-40; LEDGER:908-909 |
| 12-14 | `AUGS` holds 23 bits for the next literal `#S`; lower 9 from the instruction; augment cancelled / does not persist | KB `augs.yaml`:5-15, 23-24 |
| 14-17 | `ALTx` `S` = register, 9-bit literal or augmented literal; base `S[8:0]`, signed auto-increment `S[17:9]` added to `D` after | KB `altd.yaml`:5, 9; `altr.yaml`:5, 9; `alts.yaml`:5, 9 |
| 19 | published in *P2 Documentation*, KNOWN BUGS | PDOC:197, 212 |
| 21-27 | blockquote (exact; line breaks of the source joined with single spaces) | PDOC:212-216 |
| 29-31 | example `AUGS #$FFFFF123` / `ALTD index,#base` / `ADD 0-0,#$123`; comment "Look out! AUGS will affect #base, too. Use a register, instead." | PDOC:217-227 (columns split by extraction); PBLK:1-3 (intact) |
| 31-33 | Parallax names `AUGS` only for this item; no `AUGD` | PDOC:212-227 (read); KB `augs.yaml`:72 (`scope_note` says the same) |
| 42 | augment not cancelled; target receives it | LOG2:41-44; LEDGER:899-900 |
| 43-44 | target cancelling is Parallax's statement; no instruction after the target was checked | PDOC:213-214; RIG:471-485 (target followed directly by `call #dump`) |
| 50-52 | `$3C5C_0A55`, bits 17:9 = 5; `ALTD idx,#0` and `ALTR idx,#3` each moved `idx` by 5; target wrote `$3C5C_0A55` | LOG2:21 (`autoinc=5`), LOG2:41-44; RIG:136-138; LEDGER:904-906 |
| 54-58 | tested `ALTD`, `ALTR` only; directly adjacent; one augment value; `AUGS` for the `ALTx` itself not tested | RIG:37-57, 466-485; LEDGER:903-906 |
| 60-63 | `AUGD #$1357_9B3C` / `ALTS idxs,#0` / `WRLONG #$13C` wrote `$1357_9B3C`; `idxs` unmoved; one `ALTx` | LOG2:45; RIG:139-140, 492-499; LEDGER:909-912 |
| 67-69 | 9-bit immediate has bits 17:9 clear (0-511) | KB `altd.yaml`:9 ("9-bit literal"); RIG:26, 30 ("A bare #0 moves it by 0"); LOG2:33, 37 (A2, A4: dIdx=0) |
| 75-77 | redirected to named register; full value; no other register in the 32-register window written | LOG2:41-44 (`nchg=1`, `win[8]`, `win[11]`); RIG:37-39, 143 (`WIN_N = 32`) |
| 79-81 | size of move set by bits 17:9; zero → nothing (by documented split, stated as such); only 5 measured | KB `altd.yaml`:5, 40-41; RIG:136 |
| 83-86 | `##` places `AUGS` immediately before its instruction | KB `augs.yaml`:29-33 |
| 94-101 | workaround snippet | HARN:24-31 (byte-identical; see §4) |
| 104-105 | register `S` has no immediate `S` to augment; `idx` unchanged; augment reaches `MOV` | LOG2:39 (A5 `dIdx=0`, `win[12]=$3C5C_0A55`); PDOC:215-216 |
| 110-111 | snippet compiled with `pnut-ts` 1.55.8, not run | §4 below |
| 113-116 | `ALTD idx` = same word as `ALTD idx,#0`, immediate bit set, `S` = 0; same form the test ran | HARN:35-36 compiled: both `$F98C0A00` (listing offsets `$40`, `$44`); RIG:113-114 (A6 word `$F98CBA00`, I=1, S=0); RIG:95-98 |
| 115-116 | one-operand form of every `ALTx` has the immediate bit set | KB encodings, syntax-2 rows: `altd.yaml`:34, `altr.yaml`:34, `alts.yaml`:34, `altb.yaml`:35, `alti.yaml`:32, `altsn.yaml`:35, `altgn.yaml`:9, `altsb.yaml`:26, `altgb.yaml`:35, `altsw.yaml`:26, `altgw.yaml`:35 (last three bits of the opcode group end in 1 = I) |
| 120 | `AUGS` changes nothing in memory | KB `augs.yaml`:23-24 |
| 124-128 | the `ALTx` exemption is meant to let the augment reach a later target; Parallax quote "will use and cancel the AUGS value, as expected" | PDOC:213-214 (quote exact); mechanism paraphrased at programmer's-model level from the study brief (not quoted; no names, no line refs) |
| 128-132 | selection of the receiving instruction treats an immediate-`S` `ALTx` like any immediate-`S` instruction; the `ALTx` leaves the augment pending | paraphrase of the study brief's mechanism; outcome confirmed LOG2:41-44 |
| 141-144 | `ALTx` encodings carry an immediate bit for `S` only; `D` always a register | KB `altd.yaml`:29 (`01I DDDDDDDDD SSSSSSSSS`, no L bit), same pattern in every `alt*.yaml` two-operand row; LEDGER:911 |
| 148 | P2 board, nothing on its pins, 200 MHz | RIG:33 ("bare P2 board, no pins, no jumpers"), RIG:132; LEDGER:892-893 |
| 148-152 | PASM cog started by `COGINIT` from `DAT`; debug interrupt cog 0 only `%0000_0001`; no interrupts in measuring cog; cog 0 reads and prints | RIG:33-35, 133, 198, 414-415; LOG2:25-27 (passes ran in cog 1); LEDGER:889-890 |
| 152-155 | window of 32; sentinel per arm and slot; arm A6 slot 8 = `$5E5E_0608`; `idx` = cog address of `win[8]` | RIG:37-39, 143-144, 167, 298, 505-517; LOG2:42; LOG2:28 (`win cog addr=$0000_0062`, `idx0 = win addr + 8`) |
| 155 | window and `idx` copied to hub after each arm | RIG:519-527 |
| 155-157 | augment `$3C5C_0A55`: bits 8:0 `$055`, bits 17:9 = 5 | RIG:136-138; LOG2:21 |
| 159-160 | "moved" = `idx` after minus `idx` before | RIG:308, 327 |
| 164-171 | arm table: every Written / Value / Moved cell | LOG2:29, 31, 33, 35, 37, 39, 41, 43 (and LOG1 same lines); sequences RIG:429-485; `sinc` = `AUTOINC << 9` = `$A00` per LOG2:35 label and RIG:533; `sreg4` = 4 RIG:145, 534 |
| 173 | exactly one window register changed in every arm | `nchg=1` on LOG2:29, 31, 33, 35, 37, 39, 41, 43 |
| 173-174 | no verdict unless controls exact | RIG:220-241 |
| 176-178 | A3: `S[17:9]`=5 moves `idx` by 5, redirected register stays `win[8]` | LOG2:35-36 |
| 181-186 | `$D5D5_D5D5` sentinel; D1 `$1357_9B3C`; D2 `$1357_9B3C`; `idxs` `$0000_0061` before and after; `idxs` = cog address of the hub-pointer register | RIG:168, 487-499, 55-57, 107-108 (`hubd2=$061`); LOG2:45 |
| 188-192 | three passes, fresh cogs, compared long for long, identical; run twice on 2026-09-24 from two builds; values matched | RIG:77-82, 164, 195-198, 243-251; LOG2:25-27, 46; LOG1:25-27, 46; LEDGER:892-894 |
| 194-196 | opcodes read back from the listing; `AUGS` = `$FF1E2E05` | RIG:105-123 (line 109) |
| 200-204 | filename; `pnut-ts -d` or PNut; about 40 lines, one `VERDICT:` or `RIG FAIL:` | RIG:3, 125-128 |
| 264 | status "Yes — 2026-09-24, on a P2 board at 200 MHz, run twice" | wording fixed by the chapter brief; facts LEDGER:892-894, LOG1:1, LOG2:1 |
| 265 | workaround proven on silicon: Yes | LOG2:39; LEDGER:908-909 |

---

## 3. Code excerpts from the test program (verbatim, contiguous)

| Ch. lines | RIG lines | Max width |
|---|---|---|
| 209-211 (`spin2`) | 136-138 | 76 |
| 218-232 (`pasm2`) | 463-477 | 74 |
| 239-240 (`pasm2`) | 533-534 | 76 |
| 247-254 (`pasm2`) | 492-499 | 69 |

Re-check: `grep -n -x -F -f <chapter> <RIG>` lists every RIG line of these four ranges.
RIG:135 (77 columns) was deliberately left out of the first excerpt.

---

## 4. Workaround snippet: compile record

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

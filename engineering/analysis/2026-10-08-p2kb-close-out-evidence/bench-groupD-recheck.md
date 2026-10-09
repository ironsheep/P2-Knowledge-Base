# Group D — adversarial re-check of the bench queue («#407», 2026-10-09)

**Rule applied (Stephen, 2026-10-08):** *"We only do bench runs for things that are not covered in our
ingested source documentation."* A question survives only if an exhaustive search of every ingested
source finds the sources **silent or contradicting each other**. A question about a tool's limit is never
a bench question. This file tries to kill each question; the study (`2026-10-08-p2kb-close-out-study.md`)
and the register are **not** edited here — §7 below lists the row/table changes for the arbiter to apply.

**Abbreviations.** SD = `sources/silicon-doc/silicon-doc-text.txt` (DOCX capture, newest) · DS =
`sources/p2-datasheet/p2-datasheet-text.txt` · HW = `sources/p2-hardware-manual/p2-hardware-manual-text.txt` ·
TI = `sources/smart-pins-titus/smart-pins-titus-text.txt` · SPN = `sources/smart-pins/smartpins-*.txt` ·
PM = `sources/pasm2-manual/pasm2-manual-text.txt` · CSV = `sources/p2-instructions-csv/…Sheet1.csv` ·
v55 = `sources/spin2-v55/spin2-v55-text.txt` · INT = `external-inputs/source-code/spin-interpreter/v55/Spin2_interpreter.spin2` ·
DBG = `external-inputs/source-code/spin-debugger/v51/Spin2_debugger.spin2` · EF = `external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md`.
All paths are under `engineering/ingestion/` unless they start `deliverables/`.

## 1. Verdicts

| Question | Verdict | One-line reason |
|---|---|---|
| VO-S337 (`INA` of an output-mode pin: pin or latch) | **KILLED** | Datasheet p.27 equivalent schematic (rendered): `IN` is taken from the PIN node through the input buffer; `OUT` reaches only the driver. Change spec in §3.1 |
| VO-F337 (DAC_MODE `%TT=00`, DIR × OUT) | **KILLED** | The two texts do not conflict on this row (DS names the DAC enable, SD the ADC enable); DS p.31 `%101` schematic shows **DAC OE = DIR, ADC ENA = OUT**; EF-055 measured the DAC driving at `TT=00`. Change spec §3.2 |
| VO-S367 (`%11001`/`%11010` ADC enable bits) | **KILLED** (by composition of sourced statements; rider noted) | A input defaults to the pin's read state (SD:3736); that is the ADC bit only in an ADC pad mode (v55:1465-1469, DS p.27/p.31); SD:4262 states it for `%11000`. The page needs the bits; nothing requires measuring "without". §3.3 |
| VO-S157 (`DEBUG(C_Z)` from Spin2) | **KILLED** (mechanism answered; digits not a KB fact) | C/Z are rewritten by the interpreter's own XBYTE dispatch on every bytecode (SD:1046, INT:406 "write flags") — not tied to any Spin2 statement. §3.4 |
| VO-G006b (NCO interval jitter) | **KILLED / retire** | No KB claim depends on it; the documented adder (SD:4004-4012) fixes the interval set arithmetically (integer multiples of the base period). §3.5 |
| VO-J-005 arm B (base 12 vs 8) | **KILLED** | Sources state the field layout (SD:1443-1454; v55:1608-1613 templates) and EF-064/EF-065/EF-059 measured it in three mode families. F-361 can close on that. §6 |
| VO-J-005 arms A,C,D-as-contrast | **KILLED as questions** (kept as in-rig controls) | Capture path SD:1535, v55:1144 worked example; IN rule SD:3706 + the page's own "measured with counters" note. §6 |
| VO-J-006 arms A,B,C,E | **KILLED** | SD:491-504 states default-off, receiver opt-in, writes via the sender's local LUT writes, `SETSE` companion events (SD:2246-2249). §6 |
| **VO-J-028** | **SURVIVES** | Silent per mode for the eight pages; the general rule (SD:3854) is contradicted by per-mode statements and by EF-011 vs EF-090 (mode-dependent). §4.1 |
| **VO-F372** | **SURVIVES** (sources contradict by edition) | HW:1488, TI:1382, `p2-documentation.txt:8885-8886` say yes; SD:4579 omits it and SD:3856 states the opposite general rule. §4.2 |
| **VO-S304** | **SURVIVES** | No source gives the PWM `X` zero case; the only "zero = 65,536" statements are for the DAC modes (SD:3925). EF-014 measured the DAC-noise sibling only. §4.3 |
| **VO-G028** | **SURVIVES (narrowed)** | Pop-past-bottom is stated (SD:1150, "bottom stack value gets copied"); what a 9th **push** discards is not. §4.4 |
| **VO-G006a** | **SURVIVES** (cheap; share the J-028 rig) | `%00111` `Y=0` is an inference from the adder, which the project does not put in the KB (KNOWLEDGE-GAPS G-006); EF-013 is `%00110` only. §4.5 |
| **VO-S059** | **SURVIVES** | Sources name "xoroshiro32+" but give no algorithm or zero case; the one doc that does (`pnut_ts_facts`) prints a different algorithm. §4.6 |
| **VO-S037** | **SURVIVES** (blocks no KB fix) | SD:2020 does not exclude the issuing cog; SD:2053 says "another cog". Delete-the-claim fix needs no bench. §4.7 |
| **VO-J-005** (reduced) | **SURVIVES, reduced** | Only the sustained-rate ceiling and filter skew are source-silent. Rig already authored. §6 |
| **VO-J-006** (reduced) | **SURVIVES, reduced** | Only arm D (block-load path) and arm F (Spin2 sender) are source-silent; they are one test. §6 |

**Counts:** 12 study questions + 2 filed → 5 killed outright (S337, F337, S367, S157, G006b), 7 survive
unchanged in substance (J-028, F372, S304, G028, G006a, S059, S037), 2 survive reduced (J-005, J-006). No
surviving question is about a tool (§5).

**Merges / bundles:** see §8.

## 2. How this search went further than the first one

New or re-read sources, beyond the study's list: **(a)** the rendered pages of the Datasheet
(`external-inputs/archive/Propeller2-P2X8C4M64P-Datasheet-20221101.pdf`, pp.26-32 — the equivalent
pin schematics are images, absent from every text extraction; this killed S337 and F337 and strengthened
S367); **(b)** the rendered Titus PDF pp.20-24 (NCO duty, PWM) — nothing on `Y=0` or PWM `X=0`;
**(c)** the v55 interpreter's XBYTE mode and the debugger's `C_Z` code (S157); **(d)** `external-inputs/pnut_ts_facts/`
(S059 — an upstream lead, not authority); **(e)** the full EF ledger, including entries not on the original list
(EF-011, EF-012, EF-014, EF-019, EF-055, EF-071, EF-090); **(f)** OBEX `4198-USBnew` (F372 — conservative
`DIRL`-before-`WRPIN` order only, silent on the live case); **(g)** the **HDL study** (§2.1).

### 2.1 The HDL study — handled as indicator tier, not cited

`external-inputs/p2-hdl-study/` is, per Stephen 2026-09-26, "not a trusted source until we certify it. It is
only indicators"; it is git-ignored and must not be cited, copied from, or used as a truth root. So: **no
question here is killed by it**, and nothing from it is quoted in this file. For each survivor the table
below records only whether the study carries an indicator, so the step-8 writer knows which bench result will
also certify (or refute) an indicator. **Policy flag for the arbiter:** if an indicator should ever count as
"covered by ingested source", then S304, J-006 D/F and S037 would be in doubt — I have followed the memory
rule that it does not.

| Question | HDL-study indicator present? |
|---|---|
| VO-J-028 | material on writes-during-reset exists (shared-spine and measurement-engine aspects); not evaluated per mode here |
| VO-F372 | no text on the sniffer/drive change (the study's own USB aspect covers other things) |
| VO-S304 | yes, for `X[15:0]` zero; none found for `X[31:16]` zero |
| VO-G028 | depth only; no overflow text |
| VO-G006a | not searched (the NCO behaviour is an arithmetic consequence; a bench result certifies it) |
| VO-S059 | none on the zero state |
| VO-S037 | yes (doorbell semantics); not quoted |
| VO-J-006 D/F | yes (LUT mirror and `COGINIT` reset of sharing) |

## 3. KILLED — change specs

### 3.1 VO-S337 → change spec for S-337 (`language/spin2/concepts/basic-io.yaml:420-428`)

- **Answer (rendered page, verbatim reading):** Datasheet 2022/11/01, p.27, "Equivalent Schematics for Each
  Unique I/O Pin Configuration", `%00000MMMMMMMM – Logic`: the PIN node feeds two inverters, then an XOR with
  M7, then `IN`; `OUT` goes through an XOR with M6 into the DRIVE block's `IN` only. No path from the `OUT` latch
  to `IN`. The same holds for the Schmitt (p.28) and Comparator (p.30) modes. In the "with Feedback" modes
  (pp.27-30) the feedback line is taken from the **buffered pad**, not the latch.
- Text corroboration: SD:3706 and DS:1227-1229 "its IN bit returns the pin's read state".
- **Current text:** `description: "Reading pin that's still in output mode reads output latch, not actual pin"` (`:422`) and the
  `PINREAD(INPUT_PIN) ' Reads output latch, not external signal!` comment (`:425`).
- **Correct text:** reading a pin that is still driving returns the pin's read state — the pad level through the
  input buffer — not the `OUT` latch. With a stronger driver on the net the read shows the net, not what this
  pin is driving.
- **Authority:** Datasheet p.27 (rendered; the figure is not in the text extraction — the arbiter should open
  the PDF page), SD:3706, DS:1227.
- **Search record:** terms `output latch|read state|IN bit returns` in SD, DS, HW, TI, SPN, v55, PM; control hit SD:3706.

### 3.2 VO-F337 → change spec for S-325 / F-337

- **The two texts are not in conflict on the smart-pin-off DAC_MODE `%TT=00` row.** DS:1175 / HW:897 say
  "`DIR enables DAC`, M[7:0] sets DAC level"; SD:3790 says "`OUT enables ADC`, M.[7..0] sets DAC level" under the
  general line "DIR enables output" (SD:3784). DS names the DAC enable, SD names the ADC enable. Each leaves
  the other half unstated. Silicon-doc-era edition `part4-smart-pins.txt:83` and the older capture carry the same
  SD wording.
- **The schematic settles both halves:** Datasheet p.31, `%101MMMMMMMMMMMM – DAC with Optional ADC`: the DAC's `OE`
  is `DIR`; the ADC's `ENA` is `OUT`; the ADC bit goes to `IN`. (Rendered page; not in the text extraction.)
- **Measured:** EF-055 — a `P_DAC_124R_3V` pin at `TT=%00`, driven by `WRPIN` + `DIRH` (rig
  `campaigns/2026-08-manual-corrections/tests/test-f260-goertzel.spin2`, `sig_arm_code` lines 1481-1495: `dirl`, `wrpin #0`,
  `wrpin tw2`, `dirh`; no `OUT` write in that arm) drove with a 1,305-of-2,000 spread. So **the DAC runs on DIR with
  `TT=00`**. Rider: the arm does not log the pin's `OUT` level (it is the cog default, low); if the arbiter wants it
  logged, it is a one-line variant of an existing rig, not a new question.
- **Smart-mode rows are already decided by EF-071** (TT bit 0 clear: `OUT` does nothing; set: `OUT` runs the ADC;
  SD's "ADC" wording is right, DS/HW's "DAC" wording is wrong there; P2 Errata E6).
- **Change spec** (`architecture/smart_pins.yaml` `configuration_format.fields.tt.behavior_by_context`):
  smart pin off, DAC_MODE, `%00`: "DIR enables the DAC; OUT enables the ADC; M[7:0] sets the DAC level" with
  cites DS:1175, SD:3790, Datasheet p.31, EF-055. DAC smart modes `0x`: keep the SD "ADC" wording and add
  EF-071's TT-bit-0 condition. **F-337 can close.**
- **Search record:** `enables DAC|enables ADC|DIR enables|OUT enables|DAC_MODE` in SD, DS, HW, TI, SPN, v55, v51 symbol tables, EF;
  control hits DS:1175, SD:3790, EF-055, EF-071.

### 3.3 VO-S367 → change spec for S-367 (`architecture/smart-pins/smart-pin-11010-adc-scope-trigger.yaml:53,97,131`; and `…-11001-…` with S-364)

- **Sourced chain:** the smart pin's A input defaults to "this pin's read state" (SD:3736 `x000`; the resultant A
  drives IN in non-smart modes, SD:3767). A pad's read state is the **ADC bitstream** only in an ADC pad mode —
  v55:1465-1469 (`P_ADC_*` "ADC … → IN"), Datasheet p.31 `%100` (ADC BIT → IN); in `%000..%011` pad modes the read
  state is a logic/Schmitt level (Datasheet pp.27-30). SD:4262 states the requirement for `%11000`: the A input
  "should be a pin configured for ADC operation (M.[12..10] = %100)". `%11001` samples A on each B rise "so that an
  external delta-sigma ADC may be employed" (SD:4262) — so on-chip ADC use needs the bits; an external modulator does not.
  `%11010`: "the incoming ADC bit is shifted into a tap string" (SD:4513).
- **The page already states the requirement** (`:140` "Requires M[12:10] = %100") and its own PASM literal carries the
  bits (`:77`, `:131`); only the `pinstart(adc_pin, P_ADC_SCOPE, …)` lines (`:53`, `:97`) omit them.
- **Change spec:** make `:53` and `:97` carry the ADC bits the page's PASM literal carries (`P_ADC_SCOPE | P_ADC_1X`),
  and cite SD:3736, SD:4262, v55:1465-1469, Datasheet p.31 for the requirement. State no claim that the mode works
  "without" them — the sources do not say, and the page need not.
- **Rider (honest limit):** there is no sentence naming `%11010` and the ADC bits together; the verdict is a
  composition of three sourced statements, not a quotation. If the arbiter wants a quoted sentence or a
  measurement, VO-S367 can ride as one extra arm in the VO-J-028 `%11001` rig (§8) at no new rig cost.
- **Search record:** `M.?\[12..10\]|ADC operation|ADC bit|incoming ADC|delta-sigma` in SD, DS, HW, TI, SPN, v55; control SD:4262.

### 3.4 VO-S157 → change spec for S-157 (`language/spin2/debug-commands/c-z.yaml`)

- **Question re-asked:** does `DEBUG(C_Z)` after a Spin2 statement print anything tied to the statement? **No.**
- **Mechanism, all in ingested sources:** the Spin2 interpreter runs under XBYTE with mode `SETQ #$1A1` — INT:406
  "begin xbyte, compress Ax..Fx, **write flags**". SD:1046 and table 10 (SD:1054-1057): with the `F` bit set, *"C and Z
  receive bits 1 and 0 of the index field of the bytecode"* on **every** dispatch. The interpreter uses this itself
  (INT:911 `'1F C=1`, `:939` `'35 Z=1`, `:940` `'36 Z=0` — the bytecode numbers' low bits). The `DEBUG` bytecode
  path (INT:821-831) is `pusha / rfvar / sub ptra,x / popa / rfbyte / _ret_ brk` — none writes flags. DBG:323,629-633
  print bits 31/30 of the debug interrupt-return word (`iret`), i.e. the flags at the interrupt.
- **Consequence:** `x := 0` (or any Spin2 statement, or inline PASM — INT:2122 "C/Z=0" at entry to PASM code) cannot
  set the flags `DEBUG(C_Z)` prints; the digits are dispatch artefacts. Which bytecode's low bits are visible
  (`$41` DEBUG itself, or the next bytecode, depending on when the debug interrupt is taken against the `_RET_`
  XBYTE) is **not decided by the sources** and is not a KB fact (an interpreter implementation detail). **Do not state
  the digits.**
- **Change spec (current → correct):** `c-z.yaml:24-77` shows `x := 0` → "Shows: C=0 Z=1 (zero result)", `x := 1` →
  "C=0 Z=0", and four inline-PASM examples that claim the PASM flags are printed. → Replace with: C_Z prints the C and
  Z flags; they are meaningful in PASM (DAT) code only (v55:1006); in Spin2 code they are the interpreter's own
  bytecode-dispatch flags and do not reflect any statement or inline PASM. Remove every Spin2 example that implies
  otherwise. (The PNut-TS rejection of `DEBUG(C_Z)` between PASM instructions stays on punch-list item 10.)
- **Authority:** SD:1046, SD:1054-1057, INT:406, INT:821-831, INT:2122, DBG:323, DBG:629-633.
- **Search record:** `C_Z|c_z|flags` in v55, INT, DBG, SD XBYTE section; control v55:1006.

### 3.5 VO-G006b → retire; close the jitter half of G-006 by mechanism

- The mechanism is fully documented: output reflects `Z[31]` / overflow, `Y` is added into `Z` **at each base period**
  (SD:4004-4012; TI p.20-21). Every output edge therefore lies on a base-period boundary, and for `Y` that does not
  divide 2^32 the interval between rises is one of two adjacent integer multiples of the base period — arithmetic on
  the documented adder, not an observation.
- The KB makes no jitter claim today (gaps spec: "KB depends on nothing"). **Close G-006's jitter half in the gap
  register as "answered by the documented mechanism; no KB statement"** — nothing goes into YAML, consistent with the
  project rule of not putting inference in the KB. No bench; the instrument question (cycle-to-cycle jitter on a pad)
  never arises.
- **Search record:** `jitter|quantiz|interval|rare long` in SD, DS, HW, TI, SPN, EF; control SD:4008.

## 4. SURVIVING — search record and test specification

Common to every spec: pins from the free set only (**P0-P7, P32-P47**); `_clkfreq = 200_000_000`; `DEBUG_COGS =
%0000_0001` (EF-057); all pin and measuring work in a launched PASM cog, reporting from cog 0; compile `pnut-ts -d`;
configuration words compiled and **read from the listing** before the run (EF-065 lesson); predictions and
falsifying outcomes printed before measuring; verdict taxonomy as the exemplars (§9).

### 4.1 VO-J-028 — Y written while DIR is low, eight counter modes

- **Searched (terms · files):** `WYPIN`, `during reset`, `DIR.?low`, `held in reset`, `written while` in SD, DS, HW,
  TI (text and rendered pp.20-24, 36-38, 43), SPN, v55, INT, `p2docs-github-io`, chip-gracey-clarifications,
  forum-threads, from-Chip, `p2-qa-spreadsheet`, EF, OBEX `4198-USBnew`.
- **What is stated:** the general rule — "A smart pin should be configured while its DIR bit is low … WRPIN/WXPIN/WYPIN can
  be used to establish the mode and related parameters" (SD:3854; DS:1234; HW:980; TI:318). Per-mode reset lines give
  `Y` for pulse and transition ("Y is set to zero", SD:3984, :3997), `Y.[15..0]` "captured" for DAC/PWM, `Z` for the
  counter modes (SD:4116-4254), and a **retained** write for sync-serial (SD:4650, :4660). **Silent on `Y` for
  `%01111`, `%10010`-`%10111`, `%11001`.**
- **Why it cannot be derived:** the ledger shows the answer is mode-dependent — EF-011 (pulse, transition, async-TX:
  a `Y` written in reset never triggers; value modes order-independent) against EF-090 (sync-TX: a word written in
  reset **is** sent). The one counter-family control we hold is after-DIRH only (EF-019(a): `%10011` pair, reordered
  init, 0.79 T stable offset).
- **Control hit:** SD:3984 (the statement that exists for pulse/transition); EF-011.
- **P2 question, not a tool:** yes.
- **Rig (bare board — no jumper, no instrument):** measuring pin M = P4; source pin S = P5 running `P_NCO_FREQ | P_OE`
  at a known ratio; M's A input = relative +1 (`P_PLUS1_A`) — the EF-090 / `test-f526` internal-routing technique. Second
  source S2 = P6 where a mode needs B (B = relative +2, or A inverted).
- **Arms, per mode, 5 runs from `WRPIN #0` on all pins:** **B** `DIRL, WRPIN, WXPIN, WYPIN y, DIRH` · **A** `DIRL, WRPIN,
  WXPIN, DIRH, WYPIN y` (the control; EF-011 order) · **Z** `DIRL, WRPIN, WXPIN, DIRH`, `Y` never written (default).
  `y` chosen so A and Z differ observably:
  `%01111` Y=1 with B = A inverted (A-highs minus B-highs ≈ 0 against ≈ N/2) · `%10010` Y=%100|%01 on a **stopped**
  source (timeout raises IN; Y[2]=0 never completes) · `%10011` and `%10100` Y=%11 vs %00 on an asymmetric-duty source
  (edge→edge vs rise→rise totals differ) · `%10101`, `%10110`, `%10111` likewise · `%11001` X[5:4]=%10 (SINC3) with
  `y` = 320 vs the X[3:0] period (IN period differs from 2^k). `%11001` also needs B routed (relative +1 clock).
- **Gates (a failure prints RIG FAIL and NO VERDICT):** path control — S read as a plain pin by M, high then low, 4,096
  of 4,096 / 0 of 4,096; **A must separate from Z** for the mode (else Y is not observable and the mode is INCONCLUSIVE,
  not a pass); source runs (control read before and after).
- **Pass/fail per mode:** *X separates from Y* = every X sample lies outside [min Y, max Y] (the so9 rule). **Y survives**
  if B does not separate from A and B separates from Z (5/5); **Y is lost** if B does not separate from Z and B
  separates from A; anything else INCONCLUSIVE. One verdict line per mode, then a summary of "order-safe" / "reorder
  to the general order" per page — which is exactly what F-386's sweep needs.
- **DEBUG read-out suffices.** No external instrument.

### 4.2 VO-F372 — USB WRPIN sniffer/drive change on a running pair

- **Searched:** `without resetting`, `sniffer`, `new WRPIN`, `%0_11011_0` in SD, `p2-documentation.txt`, HW, TI, SPN,
  `smart-pins-catalog/ingestionSources/mode-11011-usb-host-device`, OBEX 4198/4087/4162 (`usbnew.spin2`), KNOWLEDGE-GAPS, EF.
- **Contradiction, verbatim:** HW:1488 "A new WRPIN can be done to effect such a change without resetting the smart
  pin"; TI:1382, `p2-documentation.txt:8885-8886` the same; SD:4579 omits it; SD:3856 "You could do a WRPIN while DIR is
  high, but the unregulated change in use of the 126 state bits would cause unpredictable and quite certainly useless
  behavior" (about changing the five `%SSSSS` mode bits — a same-mode TT change keeps `%11011`; that reading is
  inference). Working code (`usbnew.spin2:1407-1415`, `:1657-1663`) always uses `DIRL` before `WRPIN`: silent.
  Supporting, not deciding: EF-012 shows a `WRPIN` on a running pin is accepted live (mode → 0).
- **Control hit:** HW:1488. **P2 question:** yes.
- **Simplification versus the gaps spec:** SD:4614 states the receiver sees *all local output*, so **one pair is enough
  and no jumper is needed**: P0 (DM) / P1 (DP), nothing attached. A second pair + two jumpers (P2/P3, P0→P2, P1→P3)
  is the fallback only if self-sense proves ambiguous.
- **Arms (each preceded by `DIRL`/`WRPIN #0` on both pins, then the documented start: `WRPIN #%1_11011_0`, WXPIN baud,
  `DIRH` on both):** (1) **control** — `WYPIN #2` (K); `RDPIN` status bit 1 (K in) high on P0 (gate); `WYPIN #3`
  (J) bit 0 high. (2) **live change to sniffer, DIR high:** `WRPIN #%0_11011_0` on both; `WYPIN #2`; status bit 1 must
  now be **low** (drive off; the host pulls give SE0). (3) **live change back:** `WRPIN #%1_11011_0`; `WYPIN #2`; bit 1 high
  again. (4) **same sequence with a DIR cycle between each `WRPIN`** — the control for what a reset-based reconfigure
  gives. Also (5) send a framed packet (`WYPIN #$80`, bytes) after (3) and verify the status word's bytes — proves the
  pair was not reset or corrupted by the live `WRPIN`.
- **Pass/fail:** **survives** (HW/TI/old SD right) if (2)-(3) match (4); **breaks** (SD v35 right) if (2) or (3) differ from
  (4), or (5) corrupts; INCONCLUSIVE if (1) fails or (4) itself is unstable. Status bits per SD:4618-4629.
- **DEBUG read-out suffices.** Bare board for the self-sense form; jumper-only for the fallback. No instrument.

### 4.3 VO-S304 — PWM triangle / sawtooth with `X[15:0] = 0` and with `X[31:16] = 0`

- **Searched:** `65,?536|65536|X\.?\[15..0\]|X\[15:0\]|base period|frame` in SD (PWM sections :4034-4067, :4088), DS, HW,
  TI (text and rendered pp.22-24), SPN, EF; control SD:3925 and EF-014 (DAC-noise `X=0` → 65,534 measured).
- **Silent for PWM:** SD:4038, :4057, :4059 say only "establishes a base period" / "frame period"; TI:593-659 gives
  `X[15:0]=1`, frame `$200`. TI:511, :551 print "0 < n < 65,536" for the NCO modes (a stated range that excludes zero, not
  a PWM statement). The DAC/NCO "zero = 65,536" (SD:3925) is for `%00001`.
- **P2 question:** yes.
- **Simplification versus the study:** the "second smart pin on a jumper" is **not needed** — each frame completion raises the
  pin's own `IN` (SD:4063 "Y captured, IN is raised"), so the frame period is the interval between `IN` rises.
  **Bare board, no pins used for output** (`TT=%00`: output disabled, SD:3796), measured pin P4.
- **Arms** (sawtooth `%01001`, then triangle `%01000`, `Y=1`, `DIRL`/`WRPIN`/`WXPIN`/`DIRH`, `WYPIN` after): **C** control
  `X=$0010_0010` (16 × 16 = 256 clocks sawtooth, 512 triangle) — period must equal predicted ±2 or RIG FAIL; **Z1**
  `X[15:0]=0`, `X[31:16]=4` (H65536: 4 × 65,536 = 262,144 clocks; H1: ≈ 4 clocks; HSTUCK: no `IN` within 3 × the H65536
  period); **Z2** `X[15:0]=16`, `X[31:16]=0` (H65536: 65,536 × 16 = 1,048,576 clocks; H1: 16; HSTUCK). Interval by
  `GETCT` between `IN` rises, `AKPIN` between them; ≥ 5 intervals per arm; arms in both modes.
- **Pass/fail:** each arm reports which of H65536 / H1 / HSTUCK / OTHER every interval matches (tolerance ±2 clocks);
  deterministic = all intervals agree. A verdict per (mode, field).
- **DEBUG read-out suffices.** Blocks no KB fix: S-304 stays "kept served until the bench decides".

### 4.4 VO-G028 — what the hardware stack does past 8 entries (narrowed)

- **Searched:** `stack` and the overflow family (`overflow|underflow|ninth|9th|wrap|oldest|circular|deeper|nest|full`) in SD, DS, HW, PM,
  CSV, v55, v51, INT, DBG, `p2-documentation.txt`, chip-gracey-clarifications, from-Chip, forum-threads, `pnut_ts_facts`,
  EF; **control hits** SD:166, DS:75, PM:776, PM:5788-5791.
- **What is stated:** depth 8 only; and the **under-run end**: SD:1149-1150 (also `p2-documentation.txt:2480-2481`) "(bottom
  stack value gets copied each _RET_ / RET)". The **over-run end (what a 9th push discards)** is not stated anywhere.
  The debugger saves/restores with exactly 8 `POP`/`PUSH` (DBG:315-322, :400-407) — consistent, silent on a 9th.
- **Narrowed question:** after 9 pushes, which value is gone, and does the pop-past-bottom copy hold across an overflow?
  P2 question: yes.
- **Spec (no pins, no jumper):** one PASM cog, measuring only; empty the stack first (8 `POP`); **arms:** (i) control — 8
  `PUSH` 1..8, 8 `POP` returns 8..1 (must hold or RIG FAIL); (ii) 9 `PUSH` 1..9, 9 `POP` — record all nine; (iii) 9 pops
  after only 8 pushes (stated end; must equal the bottom value repeated, confirming SD:1150 as a control); (iv) nested
  `CALL` nine deep with a distinct return per level, recording each `RET` target. Predictions printed before the run:
  drop-oldest → 9..2 then the bottom (2); drop-newest/ignore → 8..1 then 1; wrap/other → anything else.
- **Pass/fail:** the nine recorded values select exactly one of the pre-registered readings; (i) and (iii) are gates.
  **DEBUG read-out suffices.** Blocks nothing (`stack_operations.yaml:56-57` and `xbyte_engine.yaml:234` assert no behaviour).

### 4.5 VO-G006a — NCO duty `%00111` with `Y = 0`

- **Searched:** `Y.?=.?0|Y is zero|zero`, NCO sections in SD (:4000-4031), HW (:1116-1131), DS, TI (text and rendered p.20-21), SPN,
  EF; control EF-013 (`%00110`, `Y=0`, no events, rig `iosp-titus-verification-batch1.spin2:89`).
- **State:** the `Y=0` outcome follows from the stated adder, but KNOWLEDGE-GAPS G-006 records the standing decision that
  inference does not close a row; EF-013 is `%00110` only. **P2 question:** yes.
- **Spec — share the VO-J-028 rig (§8):** M = P4 (smart pin off, A = relative +1), S = P5 `P_NCO_DUTY | P_OE`, `X=$0000_0064`,
  arms **Y=0** and **Y>0 control** (`Y = $1999_999A`, 1/10 duty): count M-high reads in 4,096 `INA` reads (so9 method) and S's own
  `IN` events by `TESTP`. Also run `%00110` Y=0 as an in-run repeat of EF-013. **Pass:** Y=0 → output reads low in every sample and
  no `IN` event; control → both non-zero (gate). DEBUG only, bare board.

### 4.6 VO-S059 — `??x` with `x = 0`

- **Searched:** `seed|zero|period|never|non-zero` near `xoro32|xoroshiro32|??` in SD, DS, HW, v55, v51, INT, PM, CSV, EF; the
  OBEX `2813-Psuedo-random…` object; `pnut_ts_facts/Random-Number-Usage-Guide.md`; HDL-study indicator (none for zero);
  control DS:1557 / CSV:413.
- **What is stated:** the instruction is "Iterate D with xoroshiro32+ PRNG algorithm and put PRNG result into next instruction's S"
  (CSV:413, DS:1557, PM:4875); `??var` "Iterate long var per XORO32, return pseudo-random value" (v55:412); the interpreter does
  `xoro32 x / mov v,x` (INT:319-320). **No source gives the recurrence, the period, or the zero case.**
- **Upstream lead, not authority:** `external-inputs/pnut_ts_facts/Random-Number-Usage-Guide.md:304-349` asserts "zero seed produces
  zero forever" and "period 2^32 − 1", but prints a three-line xorshift that is **not** the xoroshiro32+ the Parallax documents
  name. It is the kind of text that made the KB's invented algorithm (S-059); probe before carrying (memory:
  *upstream input docs ≠ authority*). SD:69 lists "XORO32 improved" — the silicon may differ from the textbook algorithm.
- **P2 question:** yes (silicon + interpreter behaviour).
- **Spec (no pins):** one Spin2 cog and one PASM cog, DEBUG from cog 0. **Arms:** zero seed — `x := 0`, four `r := ??x`, record the four
  values and `x` after; control seed `x := 1`; control seed `$DEADBEEF` — and for each seed the **same** iteration by a PASM
  `XORO32` loop on the measuring cog; the Spin2 and PASM sequences must agree for the non-zero seeds (gate: proves `??var` ≡ XORO32 on
  this part). Pre-registered: zero seed → all returns 0, `x` stays 0. **Pass/fail:** report the four values and `x`; reading "zero is
  absorbing" requires four zeros and `x = 0`; anything else is the finding (print raw).
- **DEBUG read-out suffices.** Blocks no KB fix: `random_generation.yaml:47-60` loses its invented claims whatever the bench says.

### 4.7 VO-S037 — does `COGATN(1 << COGID())` strobe the issuing cog?

- **Searched:** `own|self|itself|issuing` near `attention|COGATN|POLLATN|WAITATN` in SD, DS, HW (:482-483), PM (:1853), v55 (:526),
  INT (`cogatn_`), KNOWLEDGE-GAPS, SOURCE-ERRATA (E-017/E-001 — operand width only), EF; control SD:2020.
- **State:** SD:2020 "The 16 attention strobe outputs from all cogs are OR'd together to form a composite set of 16 strobes, from
  which each cog receives its particular strobe" — does **not** exclude the issuing cog; SD:2053 "requested by another cog or other
  cogs" reads the other way. No statement either way. **P2 question:** yes.
- **Spec (no pins):** PASM cog and Spin2 cog. **Arms:** (i) control — cog X strobes cog Y (`COGATN #1<<y`); Y's `POLLATN WC` → C=1 (gate;
  also proves POLLATN clears: second poll C=0); (ii) **self, PASM:** `COGATN` own bit, `POLLATN WC`, repeat with `JATN`; (iii) **self,
  Spin2:** `COGATN(1 << COGID())`, `POLLATN()`; (iv) negative control — no strobe, `POLLATN` → 0. **Pass/fail:** (ii)/(iii) equal (i) →
  delivered; equal (iv) → not delivered; never both. **DEBUG read-out suffices.**
- **Not blocking:** `language/spin2/methods/cogatn.yaml:138` ("Cannot signal yourself (no effect)") is unsourced — **delete it now**; the
  bench only decides whether the opposite may be stated.

## 5. Doctrine check — P2, not a tool

All nine survivors (J-028, F372, S304, G028, G006a, S059, S037, J-005 reduced, J-006 reduced) are about silicon
or the interpreter's documented semantics; none is a limit of PNut / pnut-ts / pnut-term-ts. S157 (the one that touched
the DEBUG toolchain) is killed, and its residue — PNut-TS rejecting `DEBUG(C_Z)` between PASM instructions — is already a
punch-list item, not a bench question. S059's Spin2 arm measures the language's `??` against the PASM instruction, i.e. the
documented interpreter-over-silicon behaviour, not a compiler limit.

## 6. VO-J-005 and VO-J-006 — the filed queue, arm by arm

### VO-J-005 (written, not run; `…/p2-io-and-smart-pins-user-guide/audit/verification-tests/test-vo-j-005-streamer-pin-capture.spin2`, 699 lines; replicated copy `campaigns/2026-08-manual-corrections/tests/`)

| Arm | Verdict | Source answer |
|---|---|---|
| A — four static pins, the capture path works | **KILLED as a question** (keep as the rig's gating control) | SD:1535 "1/2/4/8/16/32 pins are read from {INB, INA} … WFBYTE/WFWORD/WFLONG"; v55:1144 Parallax's worked capture of a smart-pin TX through an adjacent pin |
| B — base 12 vs 8 (F-361) | **KILLED** | SD:1443-1454; v55:1608-1613 (`X_4P_4DAC1_WFBYTE %1110_DDDD_WPPP_P00A` …); EF-064, EF-065, EF-059 measured it in three families. F-361 can close on sources + ledger |
| C — IN rule read by the cog | **KILLED** | SD:3706, SD:3845; the page's `verification_status` already records the contrast "observed with smart-pin counters" |
| D — headline contrast in one buffer | **KILLED as a contrast**; **kept as the skew carrier** (one live lane, one edge) | composition of A and C |
| E — sustained ceiling by NCO ladder 1:16 → 1:1 | **SURVIVES** | `pin-capture.yaml:298-301` "NOT STATED … never measured"; SD:1288-1296 give the NCO, not a sustained hub-write rate; SD:2999-3001 give the hub's 1 long/clock peak, not a capture result |
| skew — does `%FFF` filtering delay a lane | **SURVIVES** | `pin-capture.yaml:302-304` "NOT STATED" |

**Recommendation:** the rig stays as written (it already contains every arm and its controls); change **only** the register's
justification: the run is wanted for the **two source-silent facts** (ceiling, skew), not for "the path has never run on silicon".
Result lines for A–D still print as gates. Bare board; DEBUG read-out.

### VO-J-006 (identified, not authored)

| Arm | Verdict | Source answer |
|---|---|---|
| A negative control (`SETLUTS #0` default) | **KILLED** (keep as control) | SD:497 "SETLUTS #0 — disallow writes from other cog (default)" |
| B receiver `SETLUTS #1`; sender writes arrive | **KILLED** | SD:493-499 |
| C direction (receiver's writes do not reach a non-enabling sender) | **KILLED** (keep as control) | SD:493-499 (each cog enables writes *to itself*) |
| E `SETSE1 #%000_00_11AA` fires on a sender write to `$1FC-$1FF` | **KILLED** | SD:2249, SD:504 |
| **D** which writes count as "local lookup RAM writes" — `WRLUT` vs `SETQ2`-block `RDLONG` into the LUT | **SURVIVES** | SD:493 says only "its local lookup RAM writes"; PM/CSV/DS silent |
| **F** a Spin2 cog as sender (the interpreter owns LUT `$010..$1FF`) | **SURVIVES — and merges with D** | v55:806, :834; INT:2044-2048 shows the interpreter fills its LUT with `SETQ2` + `RDLONG` **block loads** — exactly arm D's path; so F's answer is D's answer plus the timing of the receiver's `SETLUTS` against the sender's start |

**Recommendation:** write **one** test, `D+F`, no pins, no jumper: pair via `COGINIT #%1_1_0001`; control = `WRLUT` propagates (arm B,
gate); arm D = block-load into the sender's LUT, receiver reads it back; arm F = Spin2 sender launched into the pair with the
receiver's `SETLUTS #1` set **before** the launch, and again after (the sharing is documented per cog; whether it survives a
`COGINIT` is a further small arm — the HDL indicator suggests it resets, SD:3698 says so only for locks). Report from a cog that is
not measuring (EF-057). DEBUG read-out. Feeds the stand-alone LUT app-note punch-list item and P2AN007.

## 7. Study / register changes proposed (not applied here)

**§5 "Bench questions" table (`2026-10-08-p2kb-close-out-study.md:906-919`):**

| VO id | New status |
|---|---|
| VO-S337 | **removed** — change spec §3.1 (S-337 resolution becomes "change spec") |
| VO-F337 | **removed** — change spec §3.2 (S-325 / F-337 close; keep EF-071 as the smart-mode authority) |
| VO-S367 | **removed** — change spec §3.3 (S-367 resolution becomes "change spec; add ADC bits") |
| VO-S157 | **removed** — change spec §3.4 (S-157 resolution becomes "change spec; no digits stated") |
| VO-G006b | **removed** — close G-006's jitter half by mechanism (§3.5) |
| VO-J-028 | stays; add the `%11001` arm (already in §4.1) |
| VO-F372 | stays; **simplify rig to one pair, no jumper** (§4.2) |
| VO-S304 | stays; **drop the second smart pin and jumper** (§4.3) |
| VO-G028 | stays; narrowed to the overflow half (§4.4) |
| VO-G006a | stays; merged into the J-028 rig (§8) |
| VO-S059, VO-S037 | stay; delete-the-claim fixes proceed without waiting |
| VO-J-005 | stays; justification reduced to ceiling + skew (§6) |
| VO-J-006 | stays; reduced to one `D+F` test (§6) |

**Register:** F-361 `PENDING-VALIDATION` → can close on SD:1443-1454 + v55:1608-1613 + EF-059/064/065 (arm B no longer a gate).
F-337 → closable per §3.2. G-006 jitter half → closed by mechanism.

## 8. Merge and bundle map

**True merges (one test answers both):**

| Merge | Why |
|---|---|
| VO-J-006 arms **D + F** | F reduces to D's block-load path plus start timing (the interpreter loads its LUT by `SETQ2` block read, INT:2044-2048) |
| VO-G006a **into** the VO-J-028 program | same NCO-source + relative-pin-routing rig (`P4` measure / `P5` source / `P6` second source); separate verdict lines |
| VO-S367 (if the arbiter insists on a measurement) **into** the VO-J-028 `%11001` arm | both need an ADC-mode pin on a relative-routed neighbour; a `P_ADC_SCOPE` vs `P_ADC_SCOPE | P_ADC_1X` pair costs two arms |

**Bundle for one bench session (separate files, no wiring, one flash cycle each):** VO-S037, VO-S059, VO-G028 (pure silicon / pure
interpreter), then VO-S304 (bare board, internal `IN` timing), then VO-J-028 + VO-G006a (bare board, relative routing), then VO-F372
(bare board, one pair), then VO-J-006 `D+F`. **Nothing here needs an external instrument; nothing needs a jumper.** (VO-F372's two-pair
fallback is the only jumper case, and it is conditional.) VO-J-005 is bare board already.

## 9. House style — exemplars the step-8 writer should copy

1. **`campaigns/2026-09-p2-errata-predictions/tests/test-so9-dac-mode-adc-enable.spin2`** (EF-071) — the template for every
   neighbour-read smart-pin question (J-028, G006a, S304-by-IN). Copy: header block (`WHAT IS DECIDED`, `RIG`, `DEBUGGER`, configuration
   words **decoded field by field and cross-checked against Spin2 symbol compositions** — control W), `K` path control before and after,
   the **separation rule**, pre-registered `CONFIRMED / REFUTED / INCONCLUSIVE` printed before measuring, `OUT_LOW/OUT_HIGH` set explicitly
   per condition, a measuring PASM cog with a done-flag mailbox, `finish()` with `DEBUG_END_SESSION`, "DEVIATION FROM THE BRIEF" note, verified
   opcodes from the listing.
2. **`campaigns/2026-10-kb-findings/tests/test-f526-sync-tx-prime-in-reset.spin2`** (EF-090) — the same question class as J-028
   (`WYPIN` during reset vs after enable) and the **bare-board relative-pin routing** technique (P4/P5/P6, nothing attached). Copy: arms
   A/B/C with the control arm that both readings agree on, the gate-then-verdict structure, `BOTH-WORK` as a named outcome, per-round
   agreement, the "documented order vs KB's order" framing.
3. **`campaigns/2026-09-p2-errata-predictions/tests/test-divide-by-zero.spin2`** (EF-089) — the template for the no-pin, "no source
   states it, so measure and predict nothing" questions (S059, S037, G028). Copy: marker operation before every repetition so a stale
   result cannot masquerade, 8 repetitions with `DETERMINISTIC / VARIES`, raw values printed, controls with known results gate the rig.

Spec-form exemplar (for the one case that will need an externally-run description): `test-specs/SPEC-VO-P-001-spi-pad-phase.md`
(decision table, two-axis factorial, controls "the run is void without", expected values from the device, "what we will write from each
outcome"). Mandatory notes to carry from it: restrict `DEBUG_COGS` to the reporting cog, report from a non-measuring cog, compile
`pnut-ts -d`, no monitor on P62 in a `-d` build.

## 10. Not checked

- The Titus PDF's other rendered pages (pp.36-38, 43, 45, 47, 51 hold figures for the counter, ADC and USB modes; only pp.20-24 were
  viewed; the text was searched in full).
- `p2docs-github-io` narrative and `external-inputs/p2docs-github-io`: searched for `WYPIN` (no hits) but not read for the other
  questions.
- The HDL study was **not** read per mode (indicator tier; §2.1) — only to record presence/absence.
- `pasm2-manual` rendered figures; the PASM2 manual PDF; Spin2 v51 PDF figures.
- Whether the interpreter's `$1A1` XBYTE mode is the mode in force at every `DEBUG` bytecode (S157): read from the source comment,
  not assembled.
- The OUT level of the EF-055 `TT=00` arm was inferred from the rig code, not from a log line (§3.2 rider).
- The arbiter should open Datasheet pp.27 and 31 (the schematics are the only source for S337 and the DAC/ADC enable split).

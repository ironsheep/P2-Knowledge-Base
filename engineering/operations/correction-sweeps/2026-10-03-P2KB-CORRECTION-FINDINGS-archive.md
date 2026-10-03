# P2KB Correction Findings — ARCHIVE, swept 2026-10-03

> **This is an archive of CLOSED findings. It is never re-edited.** Ask "what is
> outstanding?" of `engineering/operations/P2KB-CORRECTION-FINDINGS.md` alone — never
> re-derive completion state from here. If an archived finding must be reopened, it
> returns as a **new** active finding that references this file.
>
> Contains 45 findings carrying a `DONE` status token: F-440, F-445, F-446, F-447, F-448,
> F-483 … F-505 (23), F-506 … F-520 (15), F-522 — the KB v1.23.0 pass (the bench ledger
> audited against the KB, and the PASM2 references audit) plus older findings flipped to
> `DONE` once their release was verified served (2026-10-03).
>
> Swept by rename-then-trim: the register was `git mv`'d here (history follows this file) and
> copied back; this copy was then cut to the 45 findings' sections (with the section headings
> they sat under, for context), and the live copy had the same entries removed with the edit
> tools. Every entry below is the pre-sweep text (commit 77847910), verbatim, in its original
> order; `audit-register-hygiene.py --sweep-check 77847910` proves every line is accounted
> for. `RESOLVED`, `CONFIRMED` and `PARTIAL` entries were not part of this sweep (F-441, F-521,
> F-523, F-524 stay live).

---

## The bench ledger audited against the KB (2026-10-03, «#374», fixed «#375») — F-506 … F-523

Every hardware run we hold — **EF-001…EF-089 (84 entries) and XF-001…004 (4)**, 88 in all — was
checked against the YAML on disk, not against its ledger "Grounds" line (only 28 of the 84 name a
YAML there, and 9 have none). Read-only fan-out over six slices; **every non-clean verdict was
re-checked by the arbiter against the YAML file and the ledger text** before entering here.

**Verdicts, 88 of 88:** 67 in the KB and correct · 4 in the KB and **wrong** (EF-038, EF-041,
EF-056, EF-069 — three defects) · 8 incomplete · 3 missing · 2 needing verification · 4 not KB
facts (EF-016 not observed; EF-045, EF-046 PNut v55 tool defects — the KB records intent, not
per-version tool bugs; XF-004 an SD-protocol count). One agent verdict was overruled: EF-034's
"2 clk/long" is a short-burst average that includes the hub sync, measured with a 2-clock-resolution
rig, and agrees with the KB's "one long per clock after sync" — clean. Two KB-wide findings rode
along (F-519, F-520). Fix through `yaml-knowledge-base-maintenance`; ship in one `release-yamls`.

### F-506 — `dds-goertzel.yaml` teaches GETXACC as capture-and-clear into a holding register — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Applied 2026-10-03 («#375»).** `reading_results.operation` rewritten to the Rev C model (clear only during a Goertzel burst; N-1 terms; last term in the next burst), `holding_register_protocol` → `reading_protocol` (read before and after, subtract, zero-term burst first), and the XCONT example comment corrected ("the sums since the last read"). Trace: EF-069, EF-056, EF-070; matches `pasm2/getxacc.yaml`.
`architecture/streamer/dds-goertzel.yaml:167-183` (`reading_results.operation`,
`holding_register_protocol`): "Both accumulators are CAPTURED into holding registers and cleared …
Subsequent GETXACC instructions return THE SAME captured values until a new streamer command
executes"; "GETXACC reads a HOLDING REGISTER, not a live accumulator". **The bench disproved it**
(EF-069, EF-056): with the streamer idle or in another mode GETXACC returns the live running total
and clears nothing; a new streamer command does not reset it; only a read during a Goertzel burst
clears. `language/pasm2/getxacc.yaml` (`silicon_errata`, `reading_protocol`) already carries the
bench result — the v1.22.0 fix never reached the streamer page. **Fix:** rewrite :167-183 to the
getxacc.yaml model (read before and after, take the difference; the burst_sums helper for exact
sums).

### F-507 — the latest-wins mailbox pattern says a torn read is impossible — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Applied 2026-10-03 («#375»).** Both files now carry the P2AN007 R3 design the bench validated (0 bad in 20,000 with the ack): the writer posts only when ack == seq; the reader copies the id and every arg, then acks. The pattern's example was fixed (`postCommand` waits; `consumeCommand` copies with `longmove` before acking; compiled with pnut-ts 1.55.8 in a harness); anti-patterns added; "neither side ever blocks" removed. Trace: EF-038; `P2AN007/examples-library/latest-wins-mailbox.spin2`. The second non-blocking alternative p2an007 offered turned out unsafe — F-521.
`language/spin2/patterns/implementation/spin2_latest_wins_mailbox.yaml:5-7` ("a torn read is
impossible without a lock because the seq bump is the single atomic long that gates visibility of
the args") and `architecture/decomposition/data-flow-contracts.yaml:135-137` ("The bump-last ordering
is what makes a torn read impossible without a lock"). **The bench disproved it** (EF-038): with a
worker that does any work between reading the opcode and its arguments, removing the ack tore
20,000 of 20,000 commands; bump-last guards only the first publish, not a second post overwriting
the slot mid-read. The pattern's own example (`consumeCommand`, :44-48) writes `bAckSeq := bCmdSeq`
**before** reading `bCmdArg[]` ("acknowledge BEFORE acting"), which hands the slot back while it is
still being read. `application-notes/p2an007-data-structures-new-facilities.yaml:131` states the
correct rule. **Fix:** both files carry p2an007's R3 rule — the handshake is load-bearing; the writer
posts only when ack == seq, the reader reads the whole payload before acknowledging; a writer that must
never wait packs it into one long (R5); correct the example's order. (p2an007's third option, re-checking
the sequence after copying, is unsafe with a bump-last writer — F-521.)

### F-508 — SCOPE_XY `DOTSIZE` "in pixels" and SCOPE `LINESIZE` with no unit; both are half-pixels — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Applied 2026-10-03 («#375»).** `scope_xy.yaml` DOTSIZE and `scope.yaml` LINESIZE state half-pixels (rendered = n/2); `scope.yaml` DOTSIZE states whole pixels. LOGIC/FFT units left unstated (not benched). Trace: EF-041 (PNut + pnut-term-ts).
`language/spin2/debug-displays/scope_xy.yaml:37`: "DOTSIZE n -- dot diameter in pixels, 2..20".
`language/spin2/debug-displays/scope.yaml:35`: "LINESIZE n -- trace line thickness, 0..32" (no
unit). Measured on PNut and pnut-term-ts (EF-041): SCOPE_XY `DOTSIZE` and SCOPE `LINESIZE` render at
**n/2 pixels** (20 → 10 px, 32 → 16 px); SCOPE `DOTSIZE` is whole pixels (scope.yaml:34 is right).
Spin2 v55 says the same. **Fix:** state half-pixels (rendered size = n/2) on both keys. FFT `DOTSIZE`
shares the whole-pixel path (inferred, not measured); LOGIC/FFT `LINESIZE` units were not benched —
check them against the PNut source before stating a unit.

### F-509 — `pinstart.yaml` presents WYPIN-before-DIRH as the complete, correct sequence — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Applied 2026-10-03 («#375»).** `pinstart.yaml`: the description states that PINSTART's Yval is lost in the trigger and serial-transmit modes (pass 0, WYPIN after), value modes keep it; the misleading note reworded. **Widened in the same file:** `output_enable_note` gave PINSTART's order as "DIRL, WRPIN, WXPIN, DIRH, WYPIN" — corrected to WYPIN before DIRH (Spin2 v55 `spin2-v55-text.txt:537`). **Widened in the family:** `smart-pin-11100-sync-serial-transmit.yaml`'s example passed its data and transition count as PINSTART Yvals — both now Y = 0 then WYPIN after. Trace: EF-011 (and EF-019, the value-mode NCO pass).
`language/spin2/methods/pinstart.yaml:129-150`: `internal_sequence` and `operations` list DIR=0,
WRPIN, WXPIN, **WYPIN, then DIR=1**, and `notes` calls it "Complete smart pin initialization sequence
with proper reset". The bench (EF-011) proved that order **never triggers** the trigger and serial
modes (%00100 pulse, %00101 transition, %11110 async TX: old order 0, new order 1), because Y is held
0 during reset; it is safe for value modes. The rule and the "PINSTART is unsafe for the trigger
modes" warning are in `smart-pin-00101-transition-output.yaml:142-147` and `pasm2/wrpin.yaml:68`, not
on the page a PINSTART user reads. **Fix:** pinstart.yaml says it suits value modes, and that the
trigger and serial modes need reset → WRPIN/WXPIN → DIRH → WYPIN; check `smart-pin-00100…` and
`smart-pin-11110…` carry the order too.

### F-510 — the NCO mode pages never say what Y = 0 does — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Applied 2026-10-03 («#375»).** `smart-pin-00110-nco-frequency.yaml` `y_register.zero`. Narrowed: `%00111`'s Y = 0 is already 0% duty by its own formula, and the bench measured one NCO mode, so that page is unchanged. The page's bare-name `related:` list converted to full paths (findability). Trace: EF-013.
`architecture/smart-pins/smart-pin-00110-nco-frequency.yaml` and `smart-pin-00111-nco-duty.yaml`:
the `y_register` blocks give the frequency formula only. Measured (EF-013): Y = 0 produces **no
output** — the pin stays static (0 events against 200 with Y > 0), as EF-010 found for %00101.
**Fix:** one line in each `y_register` block.

### F-511 — %10010 does not say that RDPIN's acknowledge starts the next measurement — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Applied 2026-10-03 («#375»).** `smart-pin-10010-time-x-a-events.yaml` `flags.acknowledge_restarts`. Trace: EF-015.
`architecture/smart-pins/smart-pin-10010-time-x-a-events.yaml` has no restart statement, though its
frequency example (:46-53) loops on RDPIN and relies on it. Measured (EF-015): two successive
measurements both arrived with no re-WYPIN — the acknowledge restarts the measurement. **Fix:** state
it in the mode page (and in `pasm2/rdpin.yaml` for this mode if the page lists per-mode effects).

### F-512 — the DAC smart-pin mode pages say "OUT enables the ADC" without the TT bit 0 condition — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Applied 2026-10-03 («#375»).** `%00010` and `%00011` `enable` lines and a new `%00001` `adc_enable` line state the TT bit 0 condition and point to `architecture/smart_pins.yaml` silicon_errata. Trace: EF-071.
`architecture/smart-pins/smart-pin-00010-dac-16bit-pseudo-random-dither.yaml:45, :56, :94, :175`
("OUT=1 enables ADC"), and the same claim in `smart-pin-00011-dac-16bit-pwm-dither.yaml`; the
%00001 page carries no ADC rule at all. P2 Errata E6 (EF-071): with `TT` = `%00`, raising OUT runs
nothing; `TT` bit 0 must be set, and the DAC then drives the pin. The rule is in
`architecture/smart_pins.yaml:414` and `spin2/methods/wrpin.yaml:61-64`, not on the three mode pages.
Their examples use `P_OE` (TT bit 0 set), so nothing printed there fails. **Fix:** each of the three
mode pages states the condition and points to the smart_pins.yaml entry.

### F-513 — `dac-routing.yaml` does not say a streamer-fed DAC pin needs `TT` = `%01` (`P_CHANNEL`) — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Applied 2026-10-03 («#375»).** New `pin_setup` block (rule, the TT = %00 failure, pointer to the dds-goertzel worked setup). Trace: EF-063.
`architecture/streamer/dac-routing.yaml` has no TT or P_CHANNEL text. Measured (EF-063): at
`TT` = `%00` the pin ignores the streamer and holds its own level field (spread 1 against 5,330 with
P_CHANNEL). The rule appears only inside `dds-goertzel.yaml:301-307`'s example notes. **Fix:** state
it in dac-routing.yaml (and the X_DACS_* notes in `modes-reference.yaml` if they describe pin setup).

### F-514 — the `DEBUG_TIMESTAMP` entry carries no stale-window caveat — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Applied 2026-10-03 («#375»).** `special-configuration-symbols.yaml` `DEBUG_TIMESTAMP.caveat`, pointing to `pasm2/getct.yaml`. Trace: EF-083.
`language/spin2/constants/special-configuration-symbols.yaml:282, :317-320` describe the stamp as
"the 64-bit CT value" with no caveat. Measured (EF-083): the stamp is taken from the **sending cog's
own** copy of the counter, so a message sent from a cog inside a stale window (P2 Errata E3) is
stamped one wrap early and prints out of time order. The fact is only in `pasm2/getct.yaml:26`.
**Fix:** a caveat on the DEBUG_TIMESTAMP entry pointing to the getct.yaml erratum.

### F-515 — no YAML gives the 2-clock overhead of timing with a GETCT pair — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Applied 2026-10-03 («#375»).** `pasm2/getct.yaml` `measuring_elapsed`. Not added to the Spin2 pages: the figure is a PASM2 measurement and Spin2's GETCT() runs through the interpreter. Trace: EF-035.
Measured (EF-035): two GETCTs bracketing a sequence add **2 clocks** (back-to-back pair = 2; 10 NOPs
= 22; 20 NOPs = 42), so elapsed = end − start − 2. Searched the whole KB (getct.yaml has only the
instruction's own `cycles: 2`). **Fix:** `language/pasm2/getct.yaml`, with a pointer from the Spin2
timing idiom page if it teaches GETCT timing.

### F-516 — three DEBUG display facts the pages do not state — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Applied 2026-10-03 («#375»).** `midi.yaml` COLOR "named or RGB24"; `bitmap.yaml` SET "not clamped; the pixel fed after it does not appear"; `plot.yaml` COLOR: numeric values read through the current color mode (RGB24 by default, so `$RRGGBB` works) and default draw color cyan `$00FFFF`. The PLOT half was confirmed against the PNut source before editing (`p2-debug-window-manual/REF/theory-of-operations/PLOT_Theory_of_Operations.md`: `DefaultPlotColor = clCyan`, §21.1 TranslateColor). Trace: EF-029, EF-050, EF-061.
- `debug-displays/midi.yaml:32`: COLOR is described with names only; MIDI accepts a 24-bit
  `$RRGGBB` (EF-029). Use scope.yaml's wording, "named or RGB24".
- `debug-displays/bitmap.yaml:48`: `SET` gives the ranges but not what an out-of-range SET does. It
  is **not clamped**, and the pixel fed after it does not appear (EF-050; the exact mechanism is not
  isolated — state only that).
- `debug-displays/plot.yaml:49`: COLOR does not say a raw `$RRGGBB` is accepted, nor that the default
  draw colour is cyan (EF-061, from an earlier capture session — confirm both on PNut when fixing).

### F-517 — the write-side SPI alignment pad's failure shape is missing — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Applied 2026-10-03 («#375»).** `streamer_smartpin_control.yaml` `alignment_pad.write_side` — the shape only; the −6 residue is not stated. Trace: XF-001 (SCOPED).
`language/pasm2/concepts/streamer_smartpin_control.yaml:366-397` (`alignment_pad`) covers only the
read side. Partner bench XF-001 (graded SCOPED): for a streamer `P_SYNC_TX` MOSI against a
`P_TRANSITION` SCK only `hp` phases exist (hp = SCK half-period in sysclks) and **exactly one loses**,
silently corrupting whole sectors; a pad safe at one `hp` can be the losing one at another (their
default was safe at hp = 7 and lost at hp = 5). **Fix:** add the shape, write side — one losing
phase per hp, silent corruption, not portable across SCK rates, verify per rate. **Do not** state
their −6 residue: its authors call it "a fit to five points, not a law".

### F-518 — two BITMAP statements rest on less than they claim — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Settled 2026-10-03 («#375») from the PNut source** (`p2-debug-window-manual/REF/theory-of-operations/BITMAP_Theory_of_Operations.md`). SPARSE: the source draws a solid fill plus a round dot and disables sparse below dot size 4 — the YAML stands, unchanged. RATE: the source names TRACE, CLEAR or UPDATE as what un-freezes refresh (RateCycle tests equality against a count that keeps rising); nothing supports "any positive count resumes refreshing", so that sentence was replaced with the sourced one. Searched: the ledger (EF-052), the BITMAP theory of operations.
- `debug-displays/bitmap.yaml:32, :72, :79` state SPARSE (round dots on a solid fill; off below
  DOTSIZE 4) as hardware-verified. EF-042 records that every observation was on pnut-term-ts and the
  PNut leg is void, pending a PNut re-run. Settle with a PNut run (bench) or the PNut source.
- `debug-displays/bitmap.yaml:47`: "A runtime RATE with any positive count resumes refreshing".
  EF-052 tested only that a later TRACE, CLEAR or UPDATE un-freezes it. Check the sentence against the
  PNut Pascal source before keeping it.

### F-519 — ledger and finding IDs written into shipped YAML prose — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Applied 2026-10-03 («#375»).** Measured with the shipped filter itself, not a grep of the tree: 179 payload lines in 99 files carried EF/XF/F/VO ids (IDs inside stripped fields and `# Source` comments are correct and stay). All 179 removed — the id and any tag whose only job was carrying it; every fact kept word for word; wholly-provenance `evidence:` fields renamed `source:` (kept in the repo, stripped on delivery). Every hunk reviewed by word diff. **Gate:** `validate-dod-release.py` `validate_internal_ids` reads the shipped payload (the filter extracted from `fetch-kb-file.sh`) and prints every hit — 0 now; a planted `EF-999` turns it FAIL. **Not in scope here:** repo paths and `file:line` citations in shipped prose — F-523.
**73** YAML files under `deliverables/ai/P2/` carry `EF-NNN`/`XF-NNN` in their text and **45** carry
`F-NNN` — e.g. `spin2/methods/getms.yaml:55` "Hardware-verified on Rev C (EF-080, EF-082)",
`debug-displays/term.yaml:40` "hardware-verification ledger EF-001", `pasm2/getct.yaml:29`. The
v1.19 provenance strip removes provenance **fields** and comments (F-439), not IDs inside content
prose, so every consumer receives identifiers it cannot resolve. Doctrine: the shipped entry states
the fact; provenance stays in the repo. **Fix:** strip the IDs (and "hardware-verified (…)" tags that
only carry them) from content prose, KB-wide; keep the fact sentence. Provenance moves to the
register/ledger. A gate that fails on `\b(EF|XF|F)-\d{3}\b` in shipped prose keeps it out.

### F-520 — `pin-capture.yaml`'s verification status says the IN-repurposing contrast was never measured — `DONE` (served in v1.23.0, verified 2026-10-03)
> **Applied 2026-10-03 («#375»).** Rewritten, not removed: `measured_on_silicon` (the IN contrast, with counters; the command-word and debug-interrupt hazards) and `not_yet_run` (streamer capture into hub RAM itself, which still follows the documentation). No ids or repo paths. Trace: XF-002, XF-003.
`architecture/streamer/pin-capture.yaml:286-302` (`verification_status`): "none has measured the
IN-repurposing contrast on silicon … The mechanism above is documentary". Partner bench XF-002 and
XF-003 now measured both halves (a neighbour-routed plain pin counts the clock; a live smart-pin lane
reads the transfer-complete handshake). The block is also provenance commentary (EF/VO ids, repo
paths) of the F-519 kind. **Fix:** remove the block; the mechanism text above it is now
bench-supported.

### F-522 — `basic-io.yaml` teaches Spin2 `WRPIN(mode, pin)` as correct and the right order as wrong — `DONE` (served in v1.23.0, verified 2026-10-03)
Found 2026-10-03 while fixing F-509. `language/spin2/concepts/basic-io.yaml` anti-pattern
`parameter_order_confusion` labelled `WRPIN(TX_PIN, P_ASYNC_TX)` WRONG ("Pin and mode swapped!") and
`WRPIN(P_ASYNC_TX | P_OE, TX_PIN)` correct, claiming WRPIN and PINSTART take different orders; the
`missing_output_enable` example used `WRPIN(P_PWM_TRIANGLE, PWM_PIN)`. Spin2 v55 (`spin2-v55-text.txt:539`):
`WRPIN (PinField, Data)` — pin first, like PINSTART. **Applied 2026-10-03 («#375»):** both examples
now pin-first; the anti-pattern reworded to the real trap (Spin2 methods take the pin first, the PASM2
instruction `wrpin mode, pin` takes the value first). Swept: every other Spin2 WRPIN/WXPIN/WYPIN call in
the KB is pin-first.

## KB defects surfaced by the PASM2 references audit (2026-10-02, «#352») — F-483 … F-505

The «#352» audit of the Assembly Reference and deSilva read both manuals in full against KB HEAD
(v1.22.0); where the manual was right and the YAML wrong, the defect is logged here. All 23 were
**applied in the same pass** (fix-group agents, every hunk reviewed by the arbiter; each re-verified
against the source cited). **Status `PENDING-VALIDATION` = applied, awaiting publication** — each
flips to `DONE` when the KB release carrying it is served by `p2kb-mcp`. Sources: silicon doc =
`silicon-doc-text.txt`; PASM2 Manual = Parallax *Propeller 2 Assembly Language Manual* (2022/11/01)
text; v55 = Spin2 v55 text.

### F-483 — `setq_block_ops.yaml` block_fill: hub fill with a register D, and a "cog fill" via WRLONG — `DONE` (served in v1.23.0, verified 2026-10-03)
Only an IMMEDIATE D fills; a register D copies that many cog registers to hub (silicon doc :3269).
WRLONG writes hub, so no SETQ form fills cog registers. Fixed both; removed the unsourced FBLOCK tip.

### F-484 — `sar.yaml` "safe for both signed and unsigned integers" — `DONE` (served in v1.23.0, verified 2026-10-03)
SAR copies bit 31 into the vacated bits: right for signed values only; SHR for unsigned.

### F-485 — the SKIP/SKIPF/EXECF concept YAMLs gave SKIPF a branch target, "no cycle consumption", and unsourced rules — `DONE` (served in v1.23.0, verified 2026-10-03)
`concepts/instruction_skipping.yaml` and `concepts/skipf_branching.yaml`, audited claim by claim
against silicon doc :772-891, :2557-2593. Only EXECF carries a target (D[9:0], pattern D[31:10]);
SKIP cancels (2-clock NOP); SKIPF/EXECF step over in cog/LUT except the two cancel cases; skipping
works only outside ISRs and resumes after one; SKIP/REP and SKIPF/REP rules; the CALL/absolute-branch
rules; GETBRK pattern visibility. Removed: "nested SKIP not allowed", AUGS/AUGD rules, "pattern
preserved across interrupts", call-mode bit 31, optimization/best-practice/debugging lists (all
unsourced). `conditional_sequence` comments were inverted; `alternating_operations` (pattern assumed
per REP iteration) removed.

### F-486 — `rep.yaml`: the instruction count D extends via ## / register — `DONE` (served in v1.23.0, verified 2026-10-03)
D is D[8:0] (0-511) in every form; only S extends (silicon doc :757). The manual carried the same
error (fixed there).

### F-487 — `groups/interrupt_resume.yaml` was a placeholder sentence — `DONE` (served in v1.23.0, verified 2026-10-03)
Now: RESIx = `CALLD IJMPx,IRETx WCZ` — returns like RETIx and stores the ISR's resume address, so the
next interrupt resumes the handler at the next instruction (silicon doc :2311-2317, :5478-5481).

### F-488 — IN-flag reset delay shown as two (or three) NOPs — `DONE` (served in v1.23.0, verified 2026-10-03)
`architecture/io_pin_timing.yaml`, `wrpin.yaml`: one NOP (2 clocks) covers it (silicon doc :3847-3850).

### F-489 — CORDIC examples: `#` literals above 511, QSQRT operand order, QMUL carry chain — `DONE` (served in v1.23.0, verified 2026-10-03)
`qrotate.yaml`, `qsqrt.yaml`, `qmul.yaml`: `##` added; QSQRT examples pass low long first ({S:D},
silicon doc :3353); the ADD feeding ADDX gained WC. Compiled.

### F-490 — `hubset.yaml` examples had CC/SS reversed and a mislabelled PLL; `clock_system.yaml` claimed an RCFAST fallback — `DONE` (served in v1.23.0, verified 2026-10-03)
Low nibble is %CC_SS (silicon doc :2621); `pll_200mhz` rebuilt per :2736-2739 (VCO 200 MHz, PPPP=%1111);
PPPP described as VCO/2…/30 and /1 (:2644-2678). "Falls back to RCFAST if the clock fails" has no
source; replaced by the :2726 glitch-hang warning. (The manual's HUBSET entry was wrong too: D[31]
"reset the chip" — fixed there.)

### F-491 — DRVC/DRVH/DRVZ/DRVNZ YAMLs lacked the DIRx-not-data-forwarded note — `DONE` (served in v1.23.0, verified 2026-10-03)
PASM2 Manual narrative :4003-4004, :4054, :4193; DRVL/DRVNOT/DRVRND/DRVNC already carried it.

### F-492 — `pollqmt.yaml` lists WAITQMT — `DONE` (served in v1.23.0, verified 2026-10-03)
There is no WAITQMT (silicon doc :2102; the :2211 list carries the slip).

### F-493 — `muxq.yaml` examples wrote `mov q, …` — `DONE` (served in v1.23.0, verified 2026-10-03)
Q is not addressable; SETQ loads it. Mask constants now match their pin comments.

### F-494 — `concepts/stack_operations.yaml` had PUSHA/POPA (and B) backwards — `DONE` (served in v1.23.0, verified 2026-10-03)
PUSHA = `WRLONG D,PTRA++`, POPA = `RDLONG D,--PTRA` (silicon doc :5475, :5490): an ascending stack.
Every example re-derived (parameter offsets, locals, block push/pop, overflow test); `stack_trace`
used `temp++` on a register (invalid) — now walks with PTRB++.

### F-495 — streamer: XCONT "must have an active command", XINIT S "or hub address", XSTOP "after current command" — `DONE` (served in v1.23.0, verified 2026-10-03)
`xcont.yaml`, `xinit.yaml`, `xzero.yaml`: with the count run down to 0 XCONT/XZERO do not wait
(:1407); S is data / sub-mode / ignored, never a hub address (hub data goes via the FIFO); XSTOP is
`XINIT #0,#0` and stops at once (:1405).

### F-496 — `wypin.yaml`: Y as "base period", "count value", "initiates conversions" — `DONE` (served in v1.23.0, verified 2026-10-03)
PWM: Y[15:0] is the output value (:4088-4089); counter: Y[0] selects count mode (:4133); ADC: Y[13:0]
overrides the period except SINC2 sampling (:4387).

### F-497 — "smart pins MUST be reset (DIR=0) before configuring" — `DONE` (served in v1.23.0, verified 2026-10-03)
`wrpin.yaml`, `architecture/smart_pins.yaml`, `concepts/basic-io.yaml`, `spin2/methods/pinstart.yaml`,
`smart-pin-11100…`, `smart-pin-11101…`: the silicon doc says *should be configured while DIR is low*
(:3854-3856); EF-012 shows WRPIN #0 resets a running smart pin with no DIR cycle.

### F-498 — WAITxxx entries: blanket "Hardware-verified on P2 silicon" and "WC/WZ/WCZ recommended only with a timeout" — `DONE` (served in v1.23.0, verified 2026-10-03)
16 WAIT YAMLs: EF-020 verified the no-SETQ flag clear on WAITSEx only — the others now say "same
mechanism, not run on this instruction"; the effect wording now states both cases (silicon doc
:2082-2086).

### F-499 — cog-number fields: COGATN "bits 7:0", COGID/COGBRK/COGSTOP "lower 3 bits" — `DONE` (served in v1.23.0, verified 2026-10-03)
COGATN D is a 16-bit value, bit n = cog n (silicon doc :2020); COGSTOP takes D[3:0] (:421); COGID
returns D[3:0] (:429); the COGID-WC and COGBRK operand widths come from Parallax's PASM2 Manual,
Dest[2:0] (pasm2-manual-text.txt :1881, :1867). `cog.yaml` "2 bits per COG"
for COGATN fixed too.

### F-500 — `cog.yaml` "at least five clock cycles", unsourced stack wrap; `hubexec.yaml` 9-24 / 3-12 — `DONE` (served in v1.23.0, verified 2026-10-03)
Silicon doc :286 says four (also swept in `skipf_branching.yaml`, `pasm2-getting-started.yaml`); the
"stack wraps (circular buffer)" claim has no source — removed; hub-exec RDLONG/WRLONG are 9...26 /
3...20 (rdlong/wrlong/hub YAMLs); its bare-name references made full paths.

### F-501 — `setq2.yaml` "HUB" in capitals — `DONE` (served in v1.23.0, verified 2026-10-03)

### F-502 — `waitx.yaml` contradicted itself on which flags WC/WZ/WCZ clear — `DONE` (served in v1.23.0, verified 2026-10-03)
A flag column applies only when its effect is given (PASM2 Manual p.30): WC clears C, WZ clears Z,
WCZ both.

### F-503 — `setpat.yaml` did not say C and Z are inputs — `DONE` (served in v1.23.0, verified 2026-10-03)
SETPAT reads C (INA/INB) and Z (==/!=) as inputs and takes no effect suffix (silicon doc :2157-2161).

### F-504 — `IF_RET` listed as an alias of `_RET_` — `DONE` (served in v1.23.0, verified 2026-10-03)
`concepts/conditional_execution.yaml`, `PASM2-ENCODING-REFERENCE.md`: pnut-ts 1.55.8 assembles
`if_ret mov x,#1` as a DAT label `IF_RET` and an UNCONDITIONAL mov (probe 2026-10-02); no Parallax
document lists it (the only on-disk mention is an old compiler-source enum name). Alias removed, a
caution added (IF_RET / IF_RETURN / IF_NEVER are not keywords). Shipped in the Assembly Reference
v3.1.10's Appendix B — removed there too.

### F-505 — pin-family YAMLs gave C/Z "the state of the base bit" without saying ORIGINAL — `DONE` (served in v1.23.0, verified 2026-10-03)
31 DIR*/DRV*/FLT*/OUT* YAMLs: every PASM2 Manual table row reads "Orig DIRx/OUTx base bit"
(pasm2-manual-text :2087-3266); now "the original (pre-instruction) state of the base pin's bit".

## KB defects surfaced by the Assembly Manual deep audit (2026-09-22, «#348») — F-447 … F-453

All six surfaced by the `document-audit` deep pass on the P2 Assembly Language Reference Manual
(`engineering/document-production/manuals/p2-assembly-language-manual/audit/periodic-audit-2026-09-22.md`).
Every one was verified by the arbiter against a primary source, not taken from a subagent's report.
**F-447 and F-448 are applied in this pass**; the rest are open.

### F-447 — F-443's CT-event correction reached three files and stopped; eight sites in six files still said "reaches" — `DONE` (shipped by v1.22.0; verified served 2026-10-03: no "CT … reaches" site in the KB)

> **Applied 2026-09-22.** F-443 (v1.20.0) corrected `addct1/2/3.yaml` `description:` to the
> PASSED/MSB rule and went no further. Still carrying the pre-correction claim, all now fixed:
> `pasm2/addct3.yaml:39` `long_description` (*"The event triggers when System Counter (CT) =
> original Dest + Src"* — `addct1`/`addct2` have no `long_description`, so `addct3` was the lone
> survivor, a valid-YAML/wrong-content instance no gate reads); `pasm2/jct1.yaml:15`,
> `jct2.yaml:15`, `jct3.yaml:15` (*"the system counter reaches the CTn target value"*);
> `spin2/methods/waitct.yaml:4`; `spin2/idioms/timing-delays.yaml:29`;
> `spin2/concepts/timing_operations.yaml:65` and `:70`.
> **Source:** `pasm2/waitct1.yaml` and `pollct1.yaml` `description:` both already carried the MSB
> rule, and the manual states it correctly in four places including a full wraparound justification.
> ⚠ **Evidence tier:** F-443 is a DOCUMENTARY correction — `addct1.yaml` carries no `EF-NNN`
> citation for it. It is corroborated from two independent directions but is not hardware-verified.
> **Why it matters beyond the KB:** `instructions-j.md:93` in the manual was not drift — it was the
> manual faithfully mirroring `jct1.yaml`. Fixing the manual alone would have left the correction
> one regeneration deep.

### F-448 — `event_interrupt_config.yaml` inverts the interrupt priorities, fabricates INT3 as the debug interrupt, and its event-source table is offset from row 9 on — `DONE` (shipped by v1.22.0; verified served 2026-10-03: INT1 highest)

> Four defects in one shipped file, `deliverables/ai/P2/language/pasm2/concepts/event_interrupt_config.yaml`.
> **Applied 2026-09-22.**
>
> 1. **Priority inverted.** `interrupt_levels` gave INT0 `priority: "Lowest"` and INT3
>    `"Highest (Debug)"`, and `priority_and_nesting.priority_rules` said *"INT3 highest priority,
>    can interrupt INT2/1/0"*. **Source (read):** `silicon-doc-text.txt:2264-2270` — *"Each cog has
>    three interrupts: INT1, INT2, and INT3. INT1 has the highest priority and can interrupt INT2
>    and INT3 … INT3 has the lowest priority and can only interrupt non-interrupt code."*
> 2. **INT3 fabricated as the debug interrupt**, in three places. `silicon-doc-text.txt:2395`: the
>    debug interrupt is a hidden **fourth** *"that has priority over all the others"*, reached via
>    `IJMP0`/`IRET0` (INA/INB remapped during the debug ISR, `:2423`), `IJMP0` initialized to `$1F8`
>    on COGINIT.
> 3. ⭐ **`event_sources.selectable_events` was offset/fabricated from row 9 onward** — eight wrong
>    rows plus a fabricated sixteenth (`16_debug: "BRK instruction (INT3)"`; there are only 16
>    sources, 0-15). It had 9="Pin pattern not matched", 10="Hub FIFO ready", 11="Hub FIFO empty",
>    12="ATN from other cog", 13="LOCK acquired", 14="LOCK lost", 15="External event".
>    **Source:** `silicon-doc-text.txt:2276-2291`. **THE MANUAL WAS RIGHT AND RICHER** —
>    `chapter-05-hardware.md:361-383` has all sixteen correct and additionally carries the
>    event-0-versus-SETINTx-code-0 distinction. A genuine KB-wrong / manual-right inversion.
> 4. `interrupt_design` advised *"Reserve INT3 for debug infrastructure"*, which follows from (2).
>
> ⚠ **The KB had two contradictory homes for this fact**: `architecture/interrupts.yaml:36-41` was
> **correct** the whole time. An agent's answer depended on which file it read. That is the
> two-homes-drift mechanism «#349» exists to measure — recorded here as an instance.

## Two findings where the manual was right and the KB was wrong (2026-09-21, Streamer Guide deep audit) — F-445, F-446

Both surfaced by the `document-audit` deep pass on the P2 Streamer Programming Guide
(`engineering/document-production/manuals/p2-streamer-programming-guide/audit/periodic-audit-2026-09-21.md`).
Filed here rather than fixed in the manual because the manual states both facts correctly; the
defect is in the shipped YAML. **Neither carries a manual edit** — the audit report records both
sites as verified-correct so a later pass does not "correct" them.

### F-445 — `clkfreq` lives at hub long `$44`, and nine shipped KB files say `$14` — `DONE` (shipped; verified served 2026-10-03: 0 `$14` sites, 8 `$44`)

> **Applied 2026-09-21.** All nine sites corrected to `#$44` / `hub long $44` (eight PASM2 code
> lines + the one prose line in `smart-pin-00110-nco-frequency.yaml:114`). Source trace:
> `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:358` and `:1731`.
> **Class swept, not just the reported sites:** grepped `deliverables/ai/P2/` for every other
> hard-coded hub-address constant in example code — `rdlong`/`wrlong` against a low hub address,
> and any `clkmode` constant. **None found**, so the class is exactly these nine. Control: the
> same grep shape located all nine `#$14` sites, and returned zero `#$44` sites, confirming the KB
> was uniformly wrong rather than mixed. Gates after the edit: `verify-yaml-format` 10/10 clean;
> `validate-crossref-keys` 3780/3780, 100%. **No manual edit** — the Streamer Guide's
> `:1748`/`:1820` were already correct and are recorded as verified-correct in
> `audit/periodic-audit-2026-09-21.md` §0 so a later pass does not "correct" them.

Nine files in `deliverables/ai/P2/` carry the PASM2 line `rdlong clkf, #$14` with the comment
*"clkfreq lives at hub long $14"*. The address is wrong.

**Authority — the Spin2 v55 language reference, which states it twice:**
- `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:358` —
  `Hub Locations | CLKMODE  CLKFREQ | $00040  $00044 | Clock mode value  Clock frequency value`
- `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:1731` —
  *"clkfreq | The current clock frequency, **located at LONG[$44]**. Initialized with the
  'clkfreq_' value."*
- `:1732` also gives the canonical PASM idiom under Spin2: `RDLONG x,#@clkfreq`.

**Sites (all `rdlong clkf, #$14` unless noted):**

```
language/pasm2/hubset.yaml:70
architecture/streamer/dds-goertzel.yaml:209
architecture/streamer/dds-goertzel.yaml:268
architecture/smart-pins/smart-pin-01101-a-rise-inc-dec-by-b.yaml:64
architecture/smart-pins/smart-pin-10111-count-periods-in-x-clocks.yaml:72
architecture/smart-pins/smart-pin-10110-count-highs-in-x-clocks.yaml:75
architecture/smart-pins/smart-pin-10010-time-x-a-events.yaml:60
architecture/smart-pins/smart-pin-10101-count-ticks-in-x-clocks.yaml:74
architecture/smart-pins/smart-pin-00110-nco-frequency.yaml:114   (prose: "or RDLONG hub $14")
```

**Impact.** This is served YAML. Any agent composing P2 code from the KB reads garbage into `clkf`
and then computes a wrong NCO / baud / period word — silently. It compiles clean; no gate in this
repo reads meaning. The defect spans two domains (`pasm2/` and seven smart-pin mode pages), so treat
it as a **class**: while fixing, sweep every hard-coded hub-address constant in KB example code
rather than only these nine lines.

**Proposed correction:** `rdlong clkf, #$44   ' clkfreq lives at hub long $44` at each site, and the
matching prose at `smart-pin-00110-nco-frequency.yaml:114`.

> ⚠️ **Method note, worth keeping.** A dispatched audit agent returned this as a *manual* defect,
> reasoning that the KB is unanimous across nine files and the manual therefore wrong, and proposed
> changing the manual's two correct lines to `$14`. **Nine copies of one derivation are still one
> derivation.** A peer derivation is not an authority for another peer derivation, and unanimity
> inside a derived tier is correlated error rather than evidence. The agent ran a sound grep control
> and still reached the wrong verdict, because the control tested its *search*, not its *truth root*.
> Applying the returned fix would have broken two working programs that readers copy.

### F-446 — the colorspace converter is not in the streamer's RGB data path — `DONE` (shipped; verified served 2026-10-03: no in-path claim remains)

> **Applied 2026-09-21.** `modes-reference.yaml:89` → `"Hub FIFO → RGB unpack → Pins/DACs"`.
> `overview.yaml` `rgb_video` rewritten to state that the streamer does the unpack and that the
> cog's colorspace converter is a **separate downstream stage** which these modes do not configure;
> its `setup:` line dropped the converter and now reads `"RDFAST before the streamer command"`.
> Source trace: `silicon-doc-text.txt:1478` (the `RDFAST ⇢ RGB ⇢ Pins/DACs` path, streamer does the
> `{R,G,B,0}` translation) and `:1849`/`:1855-1858` (converter is a per-cog DAC-channel stage set by
> `SETCY`/`SETCI`/`SETCQ`/`SETCFRQ`).
>
> **Evidence scoping — the finding was WIDENED from two files to three.** The audit named two;
> sweeping `deliverables/ai/P2/` for "colorspace" found a third carrying the same conflation:
> `language/pasm2/concepts/streamer_smartpin_control.yaml:22` listed a streamer mode as
> `"LUT to pins (via colorspace)"`. The LUT family reaches the pins by the streamer indexing lookup
> RAM, not through the converter; corrected to `"LUT to pins (the streamer indexes lookup RAM)"`.
> All other "colorspace" hits are correct and were left untouched — the five `SETCx` instruction
> pages and `PASM2-ENCODING-REFERENCE.md` describe it as its own unit, and `getbrk.yaml:21` /
> `debug_interrupt.yaml:190` in fact **corroborate** this finding by giving the cog status register
> **separate** bits for `D[22] colorspace converter active` and `D[21] streamer active`.
>
> Gates after the edit: `verify-yaml-format` clean; `validate-crossref-keys` 3780/3780. **No manual
> edit** — the Streamer Guide's `:508` was already correct.

`architecture/streamer/modes-reference.yaml:89` describes the RGB video family as
*"Hub FIFO → **Colorspace converter** → Pins/DACs"*, and `architecture/streamer/overview.yaml:69-70`
repeats it (*"Hub data through colorspace converter"* / `setup: "RDFAST + colorspace converter config"`).
The streamer unpacks RGB itself; the colorspace converter is a separate downstream cog unit.

**Authority — Propeller 2 Documentation v35:**
- `engineering/ingestion/sources/silicon-doc/silicon-doc-text.txt:1478` heads the path
  `RDFAST ⇢ RGB ⇢ Pins/DACs` and states that the streamer translates the pixel values
  *"into {R[7:0], G[7:0], B[7:0], 8'b0} values and output to X3, X2, X1, and X0"* — no converter
  in that path.
- `silicon-doc-text.txt:1849` — *"Each cog has a colorspace converter which can perform ongoing
  matrix transformations and modulation of the cog's 8-bit DAC channels"*, configured by
  `SETCY`/`SETCI`/`SETCQ`/`SETCFRQ` (`:1855-1858`).

**Corroboration.** The Streamer Guide's §15.1 is a complete, compiling VGA program that uses
`X_RFWORD_RGB16` and **never calls `SETCMOD`**. If an RGB mode required converter configuration that
program would not function. Found independently by two audit agents working different themes.

**Proposed correction:** `modes-reference.yaml:89` → `"Hub FIFO → RGB unpack → Pins/DACs"`;
`overview.yaml:69-70` → drop the converter from the description and the `setup:` line. If a pointer
to the converter is wanted, state it as a separate downstream stage, not a step in this path.

---

## Two release-path defects, one root cause — F-440, F-441

### F-440 — v1.19.0's CHANGELOG and ledger both state the `$FFFF`-perpetual correction; it was never applied — `DONE` (shipped from v1.19.1; verified served 2026-10-03: `xinit.yaml` carries the `$FFFF` perpetual rule)

**This is a record that lies about the artifact, and it shipped.** The v1.19.0 CHANGELOG says:

> *"A streamer count of `$FFFF` selects **continuous** streaming. The documented bound read
> `longs * 32 < 65536`, which admits exactly that value... The terminating maximum is `$FFFE`."*

and the YAML-head ledger row says *"GAP-3 from the P2X8C4M64P handoff closed from our own Silicon
Doc."* Neither was true at the tag. `xinit.yaml` still carried `longs * 32 < 65536` with no mention
of `$FFFF`; the fix was **confirmed and then never written**.

**How it happened, because the shape is what matters.** GAP-3 was verified against our own source
(`silicon-doc/part2-pixel-ops.txt:234` — *"By setting the D[15:0] count to its maximal value of
$FFFF, a streamer command will run perpetually"*), written up in the triage as Tier-1/confirmed, and
then carried into the release notes from **the triage** rather than from the diff. Every other claim
in that CHANGELOG had a commit behind it; this one had a conclusion behind it. A release note
assembled from what was decided instead of from what changed will do this, and nothing in the
release path compares the two.

**Found by auditing my own release claims against the tree** when asked where the handoff stood —
not by any gate. All other v1.19.0 claims were checked the same way and hold: ABORT/trap (verified
on the live MCP), `validation_chain`, `map_caveat`, the `-D` correction, the five invented clock
constants (the three surviving `XMUL` hits are the real `XMUL1..XMUL1024` PLL multipliers),
`IJMP0`/`IRET0`, and the trailing-colon labels.

**Applied now:** `xinit.yaml` states that `$FFFF` selects perpetual streaming, that the largest
terminating count is `$FFFE`, and restates the bit-granularity bound as `longs * 32 <= 65534`.
`architecture/streamer/overview.yaml` gains a `count_field` block carrying the terminating/perpetual
split and the trap, cross-linked from `XSTOP`.

**Owed:** v1.19.1, whose CHANGELOG must say plainly that v1.19.0 claimed this and did not carry it.
Correcting the claim quietly would be the same defect a second time.

**Worth building (not built here):** the release path has no check that a CHANGELOG claim
corresponds to a change in the release diff. That is the gate this finding argues for.

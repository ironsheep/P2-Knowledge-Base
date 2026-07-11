# Changeset-Integrity Audit — p2-pasm-desilva-style

**Type:** Independent, adversarial delta-since-last-release audit (read-only)
**Date:** 2026-07-11
**Baseline tag:** `p2-pasm-desilva-style-v3.0.2` (`3aa01b69`)
**HEAD:** `60d0a18a`
**Diff scope:** `git diff p2-pasm-desilva-style-v3.0.2..HEAD -- .../manuals/p2-pasm-desilva-style/`
**Files:** 3 (1 markdown master, 2 example `.spin2`) · **236 changed lines** (128 ins / 120 del) · **~46 distinct hunks**
**Commits behind diff:** `f3e702ed` (Fabrication-audit §6: class-wide correctness sweep A) and `a072ac48` (reconcile example corpora to opus-master, identity GREEN).

## Bottom line
**CLEAN.** Every markdown hunk is a technical correctness fix that de-hypes an over-broad or fabricated claim and traces to a Tier-1 source (Silicon Doc v35 / v35 instruction CSV / Spin2 v55 / P2 datasheet / pnut_ts 1.55) via the per-change proof catalog `engineering/planning/FABRICATION-AUDIT-SWEEP-CATALOG.md`. I independently re-verified the eight highest-risk claims against primary in-repo sources — all faithful. The two example files carry only `COG`→`cog` comment-casing and remain byte-identical to their opus-master fenced blocks. Teaching level is preserved or raised (adds software-pipelining, no-data-stall, and hub-slot nuance). **No `traces-to-nothing`, no `introduces-new-claim`, no `overstates-source`.** Two process notes below (changelog/version not yet bumped — intentional per commit).

## Traceability table

| File(s) | Hunk summary | Traced source | Verdict | Note |
|---|---|---|---|---|
| examples/ch01, ch02 | `COG`→`cog` in comments only (2+3 sites) | Memory rule "use cog not CPU; lowercase"; a072ac48 identity reconcile | faithful | Byte-identical to opus-master blocks; verified lowercase in master L311-312 |
| master | CORDIC "exactly 55 clocks / every time" → "~55 clocks after solver takes command" (×4: L254, L2185, ARM table, hook) | KB p2kbArchCordic: 55-clk latency + hub-rotation slot; Silicon Doc L7291 | faithful | De-hypes fixed-latency to latency+slot-wait |
| master | "each cog has its own CORDIC" → "single solver in the hub, shared by all cogs" (×2) | KB p2kbArchCordic ("shared by all COGs via hub rotation"); SiliconDoc L7270-71 | faithful | Original was a fabrication (per-cog CORDIC) |
| master | CORDIC "overwrites"/"don't queue" → 54-stage pipeline, several ops in flight, read in issue order (×3) | SiliconDoc L7293-7300 ("overlap CORDIC commands…indefinitely"); catalog C-88/C-90 | faithful | |
| master | sine-loop "perfect overlap" → explains real overlap needs cross-iteration software-pipelining | SiliconDoc L7291 + loop body L2210-17; catalog C-84 | faithful | Raises teaching level |
| master | "sine, cosine, tangent" → "sine & cosine (tangent by sin/cos)" | SiliconDoc L7271-85 function list; catalog C-92 | faithful | |
| master | RC osc "~20 MHz" → "RCFAST nominally ~24 MHz (spec'd 20 MHz min)" (×2) | SiliconDoc p2-documentation L473 "nominally 24 MHz"; L502/584 "20MHz+" | faithful | |
| master | egg-beater "at most 8 clocks" → "at most 7 (#cogs-1)" | Hub round-robin, 8-cog worst-case wait = 7 | faithful | |
| master | "Cogs start at 0" → cog-exec starts at cog $000; hub-exec at passed hub addr | Cog/hub exec model; catalog C-73 | faithful | Adds correct nuance |
| master | Exp.2: `rdlong delay, ptrb` → 2-long param block via `ptra[0]/[1]` | COGINIT passes only PTRA; catalog C-76 | faithful | Original read uninitialized PTRB |
| master | MUL "low 32 bits, high word discarded" → "16×16 multiply, complete 32-bit product" (×2) | KB: MUL=16×16→32 (QMUL=32×32→64); v3.0.0 changelog; catalog | faithful | Corrects real semantic error |
| master | `jmp #$-4` "4 longs (addresses)" → "= 4 instructions" | Cog addrs are long-addrs | faithful | |
| master | `mov ptr, @hub_data` → `##@hub_data` (prose + table) | 20-bit hub addr needs `##` immediate | faithful | |
| master | 30-char label "for tool compatibility" → "compiler rejects >30; 32 rejected" | pnut_ts 1.55: >30 errors "Symbol exceeds 30 characters"; catalog | faithful | |
| master | `entry mov ptra, ##buffer_addr` → `mov ptra, buffer_addr` (read stored ptr) | Register holds Spin2-stored hub pointer | faithful | |
| master | "The Flags: C and Z (and Q!)" + "Q flag" → "Q is a 32-bit register (SETQ/SETQ2), not a flag; only C/Z are flags" | Q register semantics; index entry updated in tandem | faithful | Corrects flag-vs-register error |
| master | "Symmetry: every instruction every mode" → "Regularity: nearly every instr shares D,S/# pattern (hub/branch/no-op restricted)" | Encoding reality; catalog C-46 | faithful | |
| master | bare `#addr` "9 bits" → "8 bits (0-255); 9th S-bit selects PTR mode" | RDxxx/WRxxx S-field encoding | faithful | |
| master | RDLONG/WRLONG "masks low bits if unaligned" → "any byte addr, no masking (unlike P1); straddle = +1 clk; only FIFO-wrap needs align" (×2, Ch5 & Ch12) | SiliconDoc; catalog C-145 (unaligned supported) | faithful | Corrects fabricated masking behavior |
| master | conditional-exec "any instr exactly 2 clocks" → "no added clocks/flush; multi-cycle keep larger counts" (×2) | v35 CSV timing; catalog C-80/C-71 | faithful | |
| master | "Rotate a Point in 3 Lines" → "4 Lines"; "coprocessor next to every cog" → "single solver in hub" | Code shows 4 lines; CORDIC shared | faithful | Fixes header/prose inconsistency |
| master | TESTP `if_z…low (Z=1 when pin=0)` → `if_z…high (Z=1 when pin=1)` | **Datasheet: `TESTP {#}D WC/WZ → C/Z = IN[D]`** | faithful | Flag polarity was INVERTED; see Verified §1 |
| master | "pin56 high & pin57 low SAME clock" → "…two clocks later; same-clock needs one instr (OUTA / DRVH+ADDPINS)" | Two seq. instrs = 2 clks apart | faithful | Corrects determinism overclaim |
| master | servo: `waitx ##4_000_000` → `mov rest,##4_000_000 / sub rest,position / waitx rest` | Low time = frame − high pulse | faithful | Logic fix; `rest` scratch reg (teaching fragment) |
| master | "4KB in 4 Instructions / 1000 longs" → "2KB / 512 longs (cog RAM limit)" | Cog RAM = 512 longs; catalog C-62 | faithful | |
| master | FIFO comment "via PTRA" → "via manual pointer dest_ptr" (×2) | Code uses dest_ptr | faithful | Comment accuracy |
| master | Cog-exec "exactly 2 clocks/instr" → "most simple instrs 2 clks (hub 9-16, branch 5+)" | v35 CSV; catalog C-71 | faithful | |
| master | `jmp #\far_away` "\ forces 32-bit" → "20-bit absolute (non-relative)" | Hub addr = 20-bit; catalog C-45 | faithful | |
| master | "Align to 8-byte" (with `alignl`) → "long (4-byte)" | alignl = 4-byte; catalog C-49 | faithful | Fixes internal contradiction |
| master | servo `rdlong width, ptra[index]` → build addr by hand (shl/add) | ptra[n] index is compile-time-only | faithful | Register index illegal |
| master | Optimization timing recomputes: "13 clks"→"~18+", "double speed"→"~10%", "33%"→"~50%", "~6"→"~13+", "~8"→"~14+", "~4 clk"→"~6 clk", "double perf"→"trim overhead" | v35 CSV RDLONG 9-16 / DJNZ taken 4; catalog C-01/C-04 | faithful | De-hypes optimistic timings |
| master | pipeline-stall section: "avoid stalls, interleave" → "P2 has NO data-dependency stalls; result ready next instr" | P2 pipeline forwarding; catalog | faithful | Corrects false hazard advice |
| master | GETCT 64-bit "read upper/lower/upper + retry" → "GETCT WC latches full 64-bit; next GETCT gets matching lower; atomic, no retry" | v35 CSV GETCT row; SiliconDoc L81/L5674; catalog C-131 | faithful | |
| master | `mov value, $200` "$200 is cog RAM" → "$200 not a cog register ($000..$1FF); 9-bit field can't hold it" | SiliconDoc L595/605/983; pnut_ts "Register cannot exceed $1FF"; C-72 | faithful | |
| master | RDLUT/WRLUT "3-clock" → "RDLUT 3 / WRLUT 2" | v35 CSV rows 151/220; catalog C-… | faithful | |
| master | UART/PWM/antipattern: `wrpin ##P_ASYNC_TX` → `\| P_OE` (×3) | SiliconDoc part4 ~L163 "%TT govern OE regardless of DIR"; Spin2 v55 L1525 P_OE; catalog C-… | faithful | Prior example didn't drive output; real fix (see Verified §2) |
| master | WYPIN-last explanation rewritten (held-at-zero → "feed data to running pin; silicon writes WRPIN/WXPIN/WYPIN w/ DIR low then raises") | SiliconDoc config procedure; catalog | faithful | See Note 2 (supersedes v3.0.1 changelog wording) |
| master | Counter IN "threshold reached" → "measurement period complete (result ready)" | Smart-pin counter modes | faithful | |
| master | UART send restructured: send first byte immediately, then wait per subsequent | SiliconDoc async-TX: IN not raised until first WYPIN; catalog C-55 (IOSP parallel) | faithful | |
| master | PWM `wxpin ##period` → `##frame<<16 \| base` (X[31:16]=frame, X[15:0]=base) | Smart-pin PWM X-field layout | faithful | + matching 1kHz exercise split |
| master | ADC `P_ADC_GIO` → `P_ADC_1X` (+1 exercise text) | Spin2 v55 L1466/L1469; catalog C-42 | faithful | GIO measures ground, not the pin |
| master | EVENT table: EVENT_INT "%0000 fired" → "in SETINT turns int OFF; as poll/wait = occurred"; CT "equals"→"reaches/passes" | SETINTx encoding; catalog | faithful | |
| master | Pro-tip: EVENT_* usable w/ WAITSE → "EVENT_* only for SETINT1/2/3; WAITSE/POLLSE are dedicated per-channel opcodes, no event operand" | Instruction set (WAITSE1..4 fixed opcodes) | faithful | |
| master | COGATN "8-bit mask" → "16-bit mask D[15:0], cogs 0..15" | COGATN encoding; catalog C-74 | faithful | |
| master | SETSE1 clear pattern restructured (pollse before wait) | SETSE1 self-clears; re-clear before wait | faithful | |
| master | Appendix A "nearly all instrs exactly 2 clks / count×2" → "most ALU 2 clks; multi-cycle cost more; ×2 is a lower bound" | v35 CSV; catalog C-01 | faithful | |
| master | Index: "Q flag: Ch7" → "Q register: Ch7" | Tandem with Q-register fix | faithful | |

## Independently re-verified against primary in-repo sources (not just the catalog)

1. **TESTP WZ flag polarity** — `engineering/ingestion/sources/p2-datasheet/pasm2-complete-instruction-tables.md` L207: `TESTP {#}D WC/WZ … C/Z = IN[D[5:0]]`. ⇒ Z=1 when pin HIGH. The **new** text is correct; the **baseline** text (Z=1 when pin=0, if_z→low) was inverted. Correction faithful.
2. **P_OE required for smart-pin output** — Silicon Doc part4-smart-pins ("%TT bits govern the pin's output enable, regardless of DIR") + Spin2 v55 L1525 (`P_OE` = "Enable output in smart pin mode"). The prior async-TX example (shipped through v3.0.1) would not drive its output; the `| P_OE` addition is a genuine fix, not an unsourced embellishment.
3. **CORDIC single shared hub solver** — KB `p2kbArchCordic`: "54-stage pipelined CORDIC solver shared by all COGs via hub rotation," 55-clk latency. Confirms per-cog claim was fabricated.
4. **MUL 16×16→32 / QMUL 32×32→64** — KB `p2kbArchCordic` (QMUL 32×32→64) + changelog v3.0.0. Correct.
5. **Unaligned RDLONG/WRLONG** — catalog C-145 cites Silicon Doc; consistent with P2 (vs P1) byte-addressable longs, +1 clk on slice straddle.
6. **RCFAST nominal** — Silicon Doc p2-documentation L473 "Internal 20+ MHz RC oscillator, nominally 24 MHz." Correction faithful.
7. **30-char label limit** — pnut_ts 1.55 rejects >30 ("Symbol exceeds 30 characters"), exactly 30 legal. Correction faithful.
8. **P_ADC_1X vs P_ADC_GIO** — Spin2 v55 L1466 (GIO→IN, calibration) / L1469 (1x→IN, external input). Correct.

## FLAGS

**None.** No hunk overstates, understates, fabricates, or scope-creeps. Adversarial attempts to disprove each of the eight sampled high-risk claims failed — each is grounded in a Tier-1 documentary source or the empirical/compiler ground truth, and the changes uniformly *reduce* over-claiming (they remove "exactly," "every time," "double," "perfect overlap," "each cog has its own") rather than introduce new unverified assertions.

## Process notes (not correctness defects)

1. **No CHANGELOG entry / no version bump yet.** The 236-line sweep landed under `f3e702ed` with the master CHANGELOG top still at v3.0.2 (the baseline) and no version bump — **intentional** per the commit ("No version bumps, no re-render — deferred to coordinated release"). Before this manual is re-released, a changelog entry covering the sweep must be authored and the version bumped; the current HEAD is not yet release-labeled.
2. **WYPIN-ordering wording supersedes the v3.0.1 changelog.** The rewritten WYPIN explanation (silicon's actual WRPIN/WXPIN/WYPIN-while-DIR-low-then-raise procedure) softens the v3.0.1 CHANGELOG's confident "the one ordering correct for *every* mode" claim. Both agree DIRH-last works; when the new changelog entry is written it should reconcile with the v3.0.1 phrasing so the release history reads consistently.
3. **Servo fragment `rest` scratch register.** The corrected servo snippet introduces `rest` without a `res`/`long` declaration — consistent with the manual's other illustrative fragments (not standalone-compilable), and the arithmetic (frame − high-pulse) is correct. Noted only for completeness; not a claim defect.

## Recommendation
**Accept the changeset.** It is a well-sourced, proportionate correctness sweep with per-change proof; it fixes at least one genuinely broken example (async TX missing P_OE), two inverted/fabricated technical claims (TESTP polarity, per-cog CORDIC), and a class of over-optimistic timing figures, while preserving deSilva teaching voice. The only outstanding items are the deferred **changelog entry + version bump** (process note 1), required before public release but explicitly out of scope of this doc-only sweep.

# Rows S-162..S-219 — change specs («#407», 2026-10-09)

Read-only research; nothing under `deliverables/ai/P2/`, `engineering/ingestion/`, the study or the register was edited.
Abbreviations: SD = `sources/silicon-doc/silicon-doc-text.txt`, PM = `sources/pasm2-manual/pasm2-manual-text.txt`,
DS = `sources/p2-datasheet/p2-datasheet-text.txt`, v55 = `sources/spin2-v55/spin2-v55-text.txt`,
CSV = `sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv` (line numbers are **file lines**; the
instruction row is the line, e.g. `CSV:42` = CMP), INT = `external-inputs/source-code/spin-interpreter/v55/Spin2_interpreter.spin2`,
G1 = `rows-S001-S040-specs.md`, G2G3 = `rows-S041-S110-specs.md`, G4G5 = `rows-S111-S161-specs.md` (cited as `S-nnn` rows or `NF-n`).
Paths are under `deliverables/ai/P2/` unless a root is given; every line number is that of the file as read 2026-10-09.

**"compiled"** = the corrected text compiled with `pnut-ts` v1.55.8 (`-q`; `-d` for DEBUG code) in the scratch tree
`/tmp/claude-1000/-workspaces-P2-Knowledge-Base/fd20d1c1-e1ec-45fc-a5bc-7f395c46f9e1/scratchpad/s219/` (probe sources `probes1.py`..`probes9.py`,
helper `lib.py`, compiled sources in `p/`). The probe name follows in parentheses, e.g. `(a162_posx_ex1)`. Where a "bad" form is quoted with its
compiler message, the bad form was compiled too and produced it. **"YAML-parsed"** = the edit was applied to a scratch copy of the file
(`s183_apply.py`) and PyYAML composed it; the served value is printed in `out/s183_apply.txt`. **"compile in sprint"** marks text that was not compiled here
(prose, or YAML-only edits). A code block in `pasm2` fences is the exact text of its probe's instruction lines (a probe adds only the
`DAT / org 0` head and the data registers the page's excerpt leaves out — the gate's `assume` list does the same).
Class sweeps: `sweep.py` (instruction-line scans A-G), `sweep2.py`, `fold_sweep.py`, `hash_sweep.py`, `rep_sweep.py`, `cond_sweep.py`, `at_sweep.py`,
`conassign_sweep.py`, `gate_rule.py` — reports in `out/`.

**States.** Change spec — every row S-162..S-219 except **S-198, S-199** (tooling, RESOLVED 2026-10-09 — one line each). **S-200** is a build spec
(the gate). **S-217** was marked *undetermined*: the sources answer it (PM:1331, "ALTS alters the next instruction regardless of its kind"), so it is a
change spec, no bench. **S-169** was worded "cannot build into a 512 KB hub"; the compiler shows it is **context-dependent** (builds in a Spin2+PASM program,
fails in a PASM-only program) — the spec says so. **No bench question, no reclassification.** S-174 / S-192 / S-188 / S-190 / S-137 / S-042 siblings point at the batch that already holds the rule and
give the exact text for these sites.

---

## G7 rows (`language/pasm2/`, the instruction pages)

## S-162 named constants used as register operands (`posx`, `negx`, `false`, `true`, `ring_mask`; sweep siblings)
Sites and current text: `posx.yaml:18` `cmp     value, POSX     wc  ' Check if value exceeds max positive` · `:24` `mov     limit, POSX` ·
`negx.yaml:18` `cmps    value, NEGX     wc  ' Check if value is below min negative` · `:24` `mov     limit, NEGX` · `false.yaml:18` `mov     flag, FALSE` ·
`:24` `if_e mov  flag, TRUE` · `true.yaml:20` `mov     result, TRUE` · `:22` `if_z mov  result, FALSE` ·
`concepts/multi_cog_synchronization.yaml:179` `incmod  next_head, ring_mask` · `:209` `incmod  tail, ring_mask`.
What the compiler does: `cmp value, POSX wc` → `Register cannot exceed $1FF` `(a162_posx_bad)`; `mov flag, TRUE` **compiles** (8 bytes, `(a162_true_bad)`) and assembles `$FFFF_FFFF` — the
-1 is OR-ed over the instruction word, so it is not a MOV at all (G7 observation O3; punch list 6); `FALSE`/`NEGX` become register 0. A constant is a register
address unless it carries `#` (9-bit) or `##` (augmented).
Beyond the operand, three examples were also meaningless and are rewritten in the same edit: `cmp value, POSX wc` / `if_nc` is "value >= POSX", and CMP's C is the **unsigned**
borrow (CSV:42), so a signed value can never "exceed" POSX; `cmps value, NEGX wc` / `if_c` ("below min negative") can never be true for a 32-bit signed value; `fles value, limit` with limit = POSX is
a no-op (every signed long is <= POSX).
Correct — `posx.yaml` `examples:` (replace both items):
```yaml
examples:
- code: |
    cmp     value, ##POSX   wcz     ' unsigned compare against POSX
    if_a    jmp     #overflow       ' value > POSX: bit 31 is set (negative as a signed long)
  description: Detecting a value above POSX (unsigned compare)
- code: |
    mov     lowest, ##POSX          ' start a running minimum at the largest signed value
    fles    lowest, sample          ' lowest = the smaller of lowest and sample (signed)
  description: Using POSX as the starting value of a running signed minimum
```
`negx.yaml` `examples:`
```yaml
examples:
- code: |
    cmps    value, ##NEGX   wz      ' is value the most negative number?
    if_z    jmp     #at_minimum     ' NEG and ABS of NEGX give NEGX again (two's complement)
  description: Detecting the one value that cannot be negated
- code: |
    mov     highest, ##NEGX         ' start a running maximum at the most negative value
    fges    highest, sample         ' highest = the larger of highest and sample (signed)
  description: Using NEGX as the starting value of a running signed maximum
```
`false.yaml` / `true.yaml` `examples:` (and add to each `notes:` "FALSE fits a 9-bit immediate: `mov flag, #0`. TRUE (-1) does not: write `##TRUE` (the compiler adds an AUGS) or `neg flag, #1`." — all four spellings compiled, `(a162_false_ex_small, a162_true_ex_small)`):
```yaml
examples:
- code: |
    mov     flag, ##FALSE           ' Initialize flag to FALSE
    ' ... some operations ...
    cmp     x, y        wz          ' Compare x and y
    if_e    mov flag, ##TRUE        ' Set flag to TRUE if equal
  description: Using FALSE for initialization
```
```yaml
examples:
- code: |
    cmp     x, #0       wz          ' Compare x with 0
    mov     result, ##TRUE          ' Default to TRUE
    if_z    mov result, ##FALSE     ' Set to FALSE if x was 0
  description: Using TRUE in conditional logic
```
`multi_cog_synchronization.yaml:179`/`:209` → `incmod  next_head, ##ring_mask` / `incmod  tail, ##ring_mask` (full block under S-164, `(a164_ring)`; the unhashed form fails `Register cannot exceed $1FF` `(a164_ring_bad_nohash)`).
The six corrected examples above compiled as `(a162_posx_ex1)` `(a162_posx_ex2)` `(a162_negx_ex1)` `(a162_negx_ex2)` `(a162_false_ex)` `(a162_true_ex)`; their instruction lines are the ones shown in the YAML.
Authority: CSV:42 (CMP: C = borrow of D-S, Z = D==S), CSV:50-53 (FGE/FLE/FGES/FLES), CSV:44 (CMPS); SD:368-379 and the compiler message for `#`/`##` (`Constant must be from 0 to 511`).
**Class sweep** over `deliverables/ai/P2` (`sweep.py` report A: every instruction-line operand that is an ALL-CAPS name or true/false/posx/negx/pi; `sweep2.py`: every name the same file defines with `NAME =` and uses bare as an operand): 229 + 2 hits, triaged — real: the 9 lines above and
**two siblings** `language/pasm2/hubexec.yaml:22` `COGINIT #HUBEXEC+5, @code` and `language/pasm2/cogexec.yaml:22` `COGINIT #COGEXEC+5, @code` (a bare `@label` is a register operand; **compiles silently**, `(a167_hubexec_at_bad)`) → `COGINIT #HUBEXEC+5, ##@code` / `COGINIT #COGEXEC+5, ##@code` `(a167_hubexec)`; the other siblings of that shape are specced already: `labels.yaml:110` (G2G3 S-042) and `spin2/integration/spin2-pasm2-integration.yaml:356,359,360` (`JMP @slowCode` — register-indirect JMP of an address; inside S-102's block 349-366, confirm it is covered). The other ~215 hits are prose/syntax lists (`D,{#}S`, instruction names in lists). **Not detectable by regexp:** a lower-case CON constant < 512 used bare (compiles silently, wrong operand) — the gate's `=con` assume list is the only net; recommend a gate rule "an assumed `=con` name used as a bare D/S operand is a defect" (decision D3).

## S-163 `augd.yaml:53-55` — `AUGD start_reg`
Current: `AUGD   start_reg     ' AUGD here cancels the block-size PTRx delta!` → `Expected "#"` `(a163_bad)`. Correct (`silicon_errata.setq_ptrx_block_size_delta_cancelled.example`, lines 53-55):
```pasm2
SETQ   #16-1         ' ready to load 16 longs
AUGD   #$123456      ' AUGD here cancels the block-size PTRx delta!
RDLONG 0,ptra++      ' ptra incremented by 4 (1 long), not 16*4
```
compiled `(a163_ok)`. Authority: CSV:433 (`AUGD #n`); SD:123 (the erratum). Sweep (`sweep.py` E: AUGS/AUGD with a non-`#` operand): this one line (the other 18 hits are prose that names the instruction).

## S-164 `NAME = value` inside a PASM block with no CON — 6 blocks
Sites: `brk.yaml:31-34` (examples[2]); `concepts/multi_cog_synchronization.yaml:82` (coordination_pattern), `:100` (simple_mutex), `:169-173` (ring_buffer), `:217-218` (mailbox_system), `:307-308` (barrier). Error: `Expected a unique name, BYTE, WORD, LONG, or assembly instruction` at the `=` `(a164_brk_bad)`.
Correct — a `CON` header takes the definitions, `DAT` (+ `org`) the code. `brk.yaml` examples[2] (replace the double-quoted `code:` string with a block scalar):
```yaml
- name: Multi-Level Debug
  description: Different debug levels with codes
  code: |
    CON
      DEBUG_TRACE     = 1
      DEBUG_INFO      = 2
      DEBUG_WARNING   = 3
      DEBUG_ERROR     = 4

    DAT
            org     0
    ' Break with appropriate level
            brk     #DEBUG_WARNING           ' Warning-level break

    ' Debugger filters based on level
  source: debug_infrastructure
```
compiled `(a164_brk)`. `multi_cog_synchronization.yaml` — lines 81-82 become (the code after them is unchanged; a local `.wait` with no global label before it compiles, `(a164_nolabel)`):
```pasm2
CON
  mailbox_base    = $7F000

DAT
        org 0
' COG A writes request
        wrlong  request, ##mailbox_base
        wrlong  #1, ##mailbox_base+4     ' Flag

' COG B polls for request
.wait   rdlong  flag, ##mailbox_base+4
        tjz     flag, #.wait
        rdlong  request, ##mailbox_base
        wrlong  #0, ##mailbox_base+4     ' Clear flag
```
compiled `(a164_nolabel)`. `:99-100` → `CON` / `  SPI_LOCK = 5` / blank / `DAT` / `        org 0`, then the `spi_transaction` code as is `(a164_mutex)`. `:168-173` → `CON` + the five definitions indented two spaces + `DAT` / `org 0`, then the producer/consumer code with **`##ring_mask`** in both `incmod`s `(a164_ring)`. `:216-218` → `CON` / `  mailbox_size = 16` / `  mailbox_base = $7F000` / `DAT` / `org 0`, code as is `(a164_mbox)`. `:306-308` → `CON` / `  barrier_count   = $7FFF0` / `  barrier_target  = 8` / `DAT` / `org 0` — **but see NF-3: the barrier body is wrong in logic, not only in the `=` lines.**
Authority: the compiler message (`NAME = value` is accepted only in a CON block; the same text under `DAT` is rejected, `(a164_brk_bad)`).
**Class sweep** (`conassign_sweep.py`, all `deliverables/ai/P2` YAML scalars with instruction lines, an assignment line and no CON header before it): exactly these 11 `=` lines in `multi_cog_synchronization.yaml` + `brk.yaml:31-34` (its `brk` is outside the sweep's mnemonic list; found by the gate). The 4 further hits (`streamer_smartpin_control.yaml:345-349`) are prose formulas (S-213). No other page.

## S-165 `coginit.yaml` — literal `--or--` lines in examples (4) (and S-172, same edit)
Current `examples:` items 0, 2, 4, 6 each end with `--or--` (lines 50-53, 55-58, 61-62, 64-67). Correct — replace the whole `examples:` list (lines 49-73); one form per item, the equivalent named-constant form as its own item (it was the other half of each "--or--"), and the **SETQ before** the COGINIT (S-172):
```yaml
examples:
- code: |
    COGINIT #1,#$100                 'load and start Cog 1 from Hub RAM $100
- code: |
    COGINIT #COGEXEC+1,#$100         'same, with the named constant
- code: |
    COGINIT #%1_0_0101, PTRA         'skip load and start Cog 5 at PTRA
- code: |
    COGINIT #HUBEXEC+5, PTRA         'same, with the named constant
- code: |
    SETQ    ptra_val                 'ptra_val will go into the target cog's PTRA register
    COGINIT #%0_1_0000, addr         'load and start a free cog at addr
- code: |
    SETQ    ptra_val
    COGINIT #COGEXEC_NEW, addr       'same, with the named constant
- code: |
    COGINIT #%1_1_0001, addr         'skip load, start a free pair of cogs at addr (for LUT RAM sharing)
- code: |
    COGINIT #HUBEXEC_NEW_PAIR, addr  'same, with the named constant
- code: |
    COGINIT id, addr  WC             '(id=HUBEXEC_NEW) skip load, start a free cog at addr; C=0 and id=cog if okay
- code: |
    COGID   myID                     'reload and restart me at Hub RAM PTRB
    COGINIT myID, PTRB
```
compiled (every instruction line) `(a172_coginit)`; `--or--` → `Expected a unique name, BYTE, WORD, LONG, or assembly instruction` `(a172_coginit_or_bad)`. Authority: SD:406-418 (the same forms, no `--or--`; `SETQ ptra_val` on the line **before** `COGINIT #%0_1_0000,addr`), SD:404 ("If COGINIT is preceded by SETQ, the SETQ value will be written into the target cog's PTRA"). The constants: `COGEXEC_NEW = %01_0000`, `HUBEXEC = %10_0000`, `HUBEXEC_NEW_PAIR = %11_0001` (the page's own siblings `cogexec.yaml`, `hubexec.yaml`).
Sweep: `--or--` as a line (sweep.py G): coginit.yaml only. SETQ placed **after** a COGINIT (grep `coginit` with `setq` in the next two lines): coginit.yaml:59-62 only (`architecture/system-registers/ptra-register.yaml:65` has the SETQ first — right).

## S-166 `conditional-debug.yaml:81-95` — `djnz … wz`
Current: `djnz    count, #.loop   wz      ' Z set when done` → `This effect is not allowed for this instruction` `(a166_cdbg3_bad_d)`. DJNZ has no flag effect (CSV:193 `DJNZ D,{#}S`); the DEBUG lines after it could never see a Z. Correct (example 3, whole item):
```yaml
  - code: |
      ' Loop iteration debugging
      DAT             org

      loop            mov     count, #10
      .loop           ' Do work here
                      nop

                      sub     count, #1       wz      ' Z set when done
              if_nz   DEBUG("Iteration: ", udec(count))
              if_nz   jmp     #.loop
              if_z    DEBUG("Loop complete")
                      ret

      count           long    0
    description: "Conditional DEBUG in loop iterations"
```
compiled with `-d` `(a166_cdbg3_d)`. Sweep (`sweep.py` B: a flag effect an instruction does not list, from the CSV syntax column): 4 hits — this line, the two RETI lines (S-187), and `architecture/interrupts.yaml:243` `RETI0 = CALLD INB,INB WCZ` (an alias description of CALLD, which does take WCZ — **not** a defect). No other `djnz … wz|wc`.

## S-167 immediates over 511 with one `#`
Sites (sweep.py C, triaged): `conditional-debug.yaml:102`, `hubexec.yaml:18`, `qlog.yaml:41`, `concepts/cog_hub_execution.yaml:263` (the G8 row's site), `idioms/pin-control.yaml:57` (a named constant, found by the gate), and one new sibling **`architecture/smart-pins/smart-pin-00111-nco-duty.yaml:126`** `WXPIN #1000, pin` → `Constant must be from 0 to 511 (m130)` `(a167_wxpin_bad)`. Four more C hits are false positives (`augd.yaml:82,84` and `augs.yaml:102` are `#n & $1FF` masks, `hardware/addon-rtc.yaml:109` is a "#64013" guide number in prose).
Correct text: `conditional-debug.yaml:102` `test    result, ##$8000_0000 wz  ' Check error bit` `(a167_cdbg4_d)`; `hubexec.yaml:18` `COGINIT #HUBEXEC+1, ##$400   ' Start Cog 1 executing from Hub RAM $400` `(a167_hubexec)`; `qlog.yaml:41` `QLOG    ##1000          ' Begin log conversion` `(a167_qlog)`; `cog_hub_execution.yaml:263` `REP   #4, ##1000` `(a189_fge)`; `pin-control.yaml:57` `"drvl ##addr_bus addpins 15    ' drive 16-pin address bus all low"` `(a167_pin)`; `smart-pin-00111-nco-duty.yaml:126` `WXPIN ##1000, pin` `(a167_wxpin)`. One sweep with S-042.
Authority: the compiler (`Constant must be from 0 to 511 (m130)`); v55:188 ("## for >9 bits"). Also `pin-control.yaml:29` already says `##` is needed above ADDPINS 7. Not detectable by regexp: `#NAME` where NAME is a CON constant >= 512 (the gate catches it).

## S-168 `orgf.yaml:20-45` — code folded onto one line by YAML single-quoting (3 blocks)
Current: three `code: '…'` single-quoted scalars written over several lines **without blank lines**, so every line break folds into a space: examples[0] reads `DAT ORG  0 entry   jmp  #main ' ... some code ...` + `ORGF $100 …`; examples[2] reads as `DAT ' Create fixed-size code block ORG 0 block_start …` (a DAT line with only a comment — the gate passes it vacuously and it contains no ORGF). Correct — block scalars:
```yaml
examples:
- code: |
    DAT
            ORG  0
    entry   jmp  #main
            ' ... some code ...

            ORGF $100            ' Fill with zeros up to address $100
    table   long 1,2,3           ' Table starts exactly at $100
  description: Fill gap to place data at exact address
- code: |
    DAT
            ORG  0
            nop
            nop
            ORGF $10             ' Advance to $10, filling $02-$0F with zeros
    handler jmp  #process
  description: Create padded interrupt vector table
- code: |
    DAT
            ' Create fixed-size code block
            ORG  0
    block_start
            ' ... code ...
            ORGF block_start + 64   ' Ensure block is exactly 64 longs
    block_end
  description: Pad code block to fixed size
```
compiled (with `main` / `process` defined as the gate's assumes do) `(a168_orgf1, a168_orgf2, a168_orgf3)`.
**Class sweep** (`fold_sweep.py`: every multi-line quoted scalar under a code key — code, example(s), quick_example, pattern, syntax, … — that contains instruction text and has at least one line break folding two non-blank lines): 7 hits — orgf.yaml ×3 (this row), `coginit.yaml:50,55,64` (the fold is inside a wrapped *comment*: `…Cog 1 ⏎ from Hub RAM $100` folds into one comment — harmless; it disappears with the S-165 rewrite), `xinit.yaml:39` (a wrapped comment `'' bmode … 1 byte from ⏎ S` — harmless, S-182 rewrites it). No other page loses code to folding.

## S-169 `orgh.yaml:22` — `ORGH $FC000,$FC800`
**Refined diagnosis (compiled, both contexts):** in a **PASM-only** program `ORGH $FC000,$FC800` fails `Program requirement exceeds 512KB hub RAM by 507908 bytes` `(c169_pasmonly_fc)` because ORGH there fills the hub image with zeros up to the address (orgh.yaml:28 says so); in a **Spin2+PASM** program it **compiles** (6296 bytes) `(c169_spin_fc, c169_spin_fc_bare)` — v55:326 uses exactly `ORGH $FC000` as "code which will be moved to its actual ORGH address at runtime", and v55:322 lists `ORGH $FC000,$FC800` as a syntax illustration. So the example is not wrong text, it is an example that is only buildable in one context. Correct — keep the syntax shown but make the **example** build everywhere, and say the context (`examples[2]` and one note):
```yaml
- code: |
    ORGH $400,$800  ' hub origin = $400, origin limit = $800
  description: Set hub origin with an explicit limit
```
compiled in both contexts `(a169_both_400, a169_pasm_400)`. Add to `notes:` "`ORGH $FC000,$FC800` (the v55 syntax illustration) assembles in a Spin2+PASM program, where the origin need not be the code's real location; in a PASM-only program ORGH fills the hub image with zeros up to the address, so an address in the debug mirror ($FC000..$FFFFF, beyond the 512 KB of hub RAM) fails with 'Program requirement exceeds 512KB hub RAM' — compiler-verified". Sibling `guides/pasm2-getting-started.yaml:161` (`"ORGH $FC000,$FC800 -- hub origin = $FC000, origin limit = $FC800"`, a verbatim v55:322 quote): append `(a syntax illustration: it assembles in a Spin2+PASM program; in a PASM-only program ORGH fills the hub image with zeros up to the address)`.
Authority: v55:322, :326-327 (the two program kinds), SD:2399 (the debug mirror); compiler results above. Sweep: `ORGH $F…`/`$FC000` over the tree — orgh.yaml:22, getting-started:161 (and `architecture/hub.yaml:21,225`, `debug_interrupt.yaml:82`, `debug-strategy-guide.yaml:93`, which describe the address range, not code).

## S-170 `xoro32.yaml:49-52` — `MODZ temp,#100` taught as modulo
Current: `MODZ    temp, #100        ' temp = seed mod 100 (0-99)` → `Expected an assembly effect or end of line` `(a170_xoro_bad)`. MODZ is the flag-modify alias `MODZ z {WZ}` (CSV:423); P2 has no modulo instruction — the remainder comes from QDIV + GETQY (CSV:260, :283). Correct (examples[1]):
```pasm2
XORO32  seed              ' Generate 32-bit random
MOV     temp, seed        ' temp = the XORO32 result (this S operand is replaced by it)
SETQ    #0                ' upper half of the dividend = 0 (XORO32 leaves its result in Q)
QDIV    temp, #100
GETQY   temp              ' temp = remainder, 0..99
```
compiled `(a170_xoro_final)`. The `SETQ #0` is deliberate: SD:1183 says XORO32 sets Q to its result and SD:1187 says QDIV without a preceding SETQ zeroes Q; the explicit `SETQ #0` removes the dependence on how that rule is read. Authority: CSV:423, CSV:260 (QDIV: quotient via GETQX, remainder via GETQY), CSV:413 + INT:319-320 (`xoro32 x` / `mov v,x`: the MOV's S is replaced by the result). Sweep: `mod[cz]z?\s+\w+\s*,` over the tree — this line only (`modcz.yaml:2` is the real syntax).

## S-171 `altgb.yaml:59-60` — `altgb ptr, ##$100 ' Auto-increment by 1`
Current (inside the double-quoted `code:` of "String Processing with Auto-Increment"): `.loop   altgb   ptr, ##$100              ' Auto-increment by 1`. ALTGB's auto-index is S[17:9] (sign-extended) added to D after the substitution (CSV:132; PM:1119 "the optional auto-indexer value (usually 0, 1, or -1)"); `##$100` is S[8:0] = $100 (a base of 256 registers) with S[17:9] = 0, so nothing increments (the compiled words show it: `$100` → `AUGS #0`; `$200` → `AUGS #1`, `(a171_altgb_old, a171_altgb)`). Correct: `.loop   altgb   ptr, ##$200              ' Auto-increment by 1`; the whole example, YAML-quoted line unchanged otherwise:
```pasm2
process_string
        mov     ptr, string_addr         ' String start address
.loop   altgb   ptr, ##$200              ' Auto-increment by 1
        getbyte char, 0-0, #0            ' Get next character
        tjz     char, #.done             ' Check for null terminator
        call    #process_char
        jmp     #.loop
.done   ret
```
compiled `(a171_altgb)`. Sweep: `alt[a-z]+ reg, ##` over the tree — this line only; `register_indirection.yaml` and the other ALT pages never use a `##` index step except in the specs below (S-194).

## S-172 `coginit.yaml:59-62` — SETQ after COGINIT
Specced under S-165 (the same `examples:` rewrite puts `SETQ ptra_val` before `COGINIT #%0_1_0000, addr` and before `COGINIT #COGEXEC_NEW, addr`, and removes the SETQ that followed `COGINIT #HUBEXEC+5, PTRA`) `(a172_coginit)`. Authority SD:404, SD:410-411 re-read.

## S-173 `conditional-debug.yaml:70-71` — `if_c_and_z` after `cmp … wcz`
Current: `cmp     a, b            wcz     ' Set both C and Z` then `if_c_and_z    DEBUG("a == b AND overflow")`. CMP's C is the borrow of a-b and Z is a==b (CSV:42), so C = 1 and Z = 1 never occur together: the branch is dead, and "overflow" is not what C means. Correct (example 3):
```yaml
  - code: |
      ' Combined flag conditions
      DAT             org

      analyze         cmp     a, b            wcz     ' C = (a < b), Z = (a == b)
              if_c_and_nz   DEBUG("a < b")
              if_nc_and_z   DEBUG("a == b")
              if_nc_and_nz  DEBUG("a > b")
                      ret

      a               long    0
      b               long    0
    description: "Combined C and Z flag conditions (after CMP, C and Z are never both set)"
```
compiled `-d` `(a173_cdbg2_d)`. The syntax list entry `IF_C_AND_Z - Both carry and zero set` (:19) is right in itself. Sibling in the same file, same edit (the **TEST** class of S-219): example 2, `check_zero      test    value, #$FF     wz      ' Set Z if value is zero` tests only the low byte → `check_zero      cmp     value, #0       wz      ' Set Z if value is zero` `(a173_cdbg_zero_d)`.
Authority: CSV:42, CSV:105 (TEST), CSV:459 (IF_C_AND_Z). Sweep (wrong flag reading after CMP): `if_c_and_z` over the tree — this line only; `conditional_execution.yaml:349-355` ("Wrong condition after CMP") is right.

## S-174 `conditional-debug.yaml:5,12,122,123,142` — "v47"
One gating class with S-153 (G4G5 `rows-S111-S161-specs.md:572-581`, "S-174 sibling … → v50 per v55:61-64"). Exact text:
`:5` `minimum_version: "v50"` · `:12` `  Available in PNut/pnut_ts v50 and later compilers (documented with the v50 notes, v55:61-64). No version directive required.` · `:122` `  - "Available in v50+ compilers - no version directive required"` ·
`:123` `  - "Before v50 only _RET_ could precede a PASM DEBUG instruction; from v50 any condition may (v55:61)"` (the old "caused compile errors" is not in the source) · `:142` `oneliner: "Execute DEBUG only when condition flags match (v50+)"`.
Authority: v55:61-64 (the paragraph after the v50 row at :42 and before the v51 heading at :66; the change log's v47 row, :39, is the task system). Sweep `v47` over `language/pasm2`: these five lines only.

## S-175 `testp.yaml:58-88`, `:30`, `:118` — rising-edge and "XOR" examples
Current example 2: `testp   input_pin           wc   ' Get current state` / `if_nc_and_z  jmp #edge_detected  ' Was 0, now 1` / `muxz    flag_reg, #1             ' Store current state`. After `TESTP … WC`, C is the pin's **current** state, so `if_nc` means it is low *now*; Z is whatever an earlier instruction left; `muxz` stores that stale Z. Example 3: `testp   sensor_pin          wz   ' Test pin, XOR with C` — WZ only writes Z = pin; the XOR form is **XORZ** (CSV:371). Correct:
```yaml
- name: Edge Detection
  description: Detect a rising edge (0 -> 1 transition) on an input pin
  code: |
    ' last_state bit 0 holds the pin state from the previous pass
            testp   input_pin       wc      ' C = current pin state
            testbn  last_state, #0  andc    ' C = high now AND low before = rising edge
            testp   input_pin       wz      ' Z = current pin state
            muxz    last_state, #1          ' remember it for the next pass (MUXZ leaves C alone)
    if_c    jmp     #edge_detected
    ' no edge: continue here
    edge_detected
    ' Handle rising edge event
- name: Conditional Pin Test
  description: Combine a pin state with a condition flag
  code: |
    ' Test pin with XOR based on previous condition
    testb   status, #FLAG_BIT   wz   ' Z = condition flag
    testp   sensor_pin          xorz ' Z = condition flag XOR pin state
    ' Z now indicates: pin state XOR condition
    ' Useful for conditional inversion
  source: debugger_pattern
```
compiled `(a175_edge)` and `(a175_xor)`. `:30` `description: 'Test pin state …'` → `Test the state of pin D[5:0] and write it to C or Z (WC/WZ), or combine it with the existing C or Z flag by AND, OR or XOR (ANDC/ANDZ, ORC/ORZ, XORC/XORZ). Common uses: …` (keep the list); `:118` `oneliner: Test pin state into C or Z, optionally ANDed, ORed or XORed with the existing flag`; `notes:` line 104 `XOR with C flag useful for conditional inversion` → `XORC/XORZ combine the pin with the existing flag (C or Z, matching the suffix)`.
Authority: SD:1984 (`TESTP {#}D WC/WZ/ANDC/ANDZ/ORC/ORZ/XORC/XORZ - read pin D bit in INx and affect C or Z`), SD:5353-5360; CSV:365-372 (TESTP/TESTPN rows, XOR row 371); CSV:61 (TESTBN … ANDC). The Hall example (`testp pin_hall_w wc`, register operands) matches its source `isp_bldc_motor.spin2:2041` where `pin_hall_*` are `res 1` registers — right.
Sweep (wrong flag reading after TESTP): the non-smart-pin TESTP lines were read (`basic-io.yaml:107-115,270-278,348`, `labels.yaml:66-75`, `waitx.yaml:55`, `streamer_smartpin_control.yaml:146-150,176`, `timing-control.yaml:47-48`) and read C correctly; this page's two examples are the only misreadings found. The ~35 `architecture/smart-pins/*` lines (TESTP on the IN flag) were **not** read one by one — see NOT CHECKED.

## S-176 `qlog.yaml:65-71` (+ `:41`) — mantissa shifted away, unloaded register ANDed
Current: `GETQX   log_result` / `SHR     log_result, #27 WZ  ' Extract 5-bit exponent` / `MOV     exponent, log_result` / `AND     mantissa, ##$07FFFFFF  ' Extract 27-bit mantissa` — `mantissa` is never loaded, and the SHR already destroyed the fraction. Correct (examples[2]):
```pasm2
QLOG    number
' ... wait 55 clocks ...
GETQX   log_result
MOV     mantissa, log_result
AND     mantissa, ##$07FFFFFF  ' Extract 27-bit mantissa (fractional exponent)
SHR     log_result, #27 WZ     ' Extract 5-bit exponent
MOV     exponent, log_result
```
compiled `(a176_qlog)`. With S-026 (G1 `rows-S001-S040-specs.md:259`) the **pasm2** `qlog.yaml` prose also needs the base: `:12` `Convert 32-bit unsigned integer to 5:27-bit logarithm format` → `Compute the base-2 logarithm of a 32-bit unsigned integer, as a 5:27-bit fixed-point value` and `:99` oneliner likewise (SD:3393 "Compute log base 2 of D"; the page never says base 2). Authority: CSV:272 (QLOG: `{5'whole_exponent, 27'fractional_exponent}`), SD:3391-3404. Sweep: `qexp.yaml:51-60` (a power example that multiplies a QLOG result by an exponent, no mantissa split) is the only other PASM use of a QLOG result.

## S-177 `xoro32.yaml:16-28`, `:74-76` — invented algorithm and properties (with S-059, S-023, S-170)
The three-line `D ^= D >> 2 / << 1 / >> 1` is a plain xorshift, not xoroshiro32+; "Never produces zero from non-zero seed", "period 2^32-1", "Good statistical properties" and "Faster (2 cycles vs variable)" are unsourced or false (GETRND is 2 clocks too, CSV:285). Sourced: DS:1557 / CSV:413 "Iterate D with xoroshiro32+ PRNG algorithm and put PRNG result into next instruction's S" (shielded from interrupt ✔), SD:1183 (Q is set to the result), INT:319-320. Correct — replace the named blocks:
```yaml
algorithm:
  name: "XORO32 (xoroshiro32+)"
  operation: |
    Iterates the 32-bit state in D with the xoroshiro32+ algorithm. D receives the new state;
    the pseudo-random result replaces the S operand of the next instruction (it is also left in Q).
  properties:
    - "2-clock execution"
    - "Reproducible: the same starting state gives the same sequence"
    - "NOT suitable for cryptography"

critical_warning:
  issue: "Seed with a non-zero value"
  description: |
    Always give XORO32 a non-zero starting state. What a zero state returns is not documented.
  solution: |
    ' Ensure non-zero seed
    GETRND  seed           ' Get a pseudo-random seed
    CMP     seed, #0   WZ  ' Check if zero
    IF_Z    MOV     seed, #1  ' Force non-zero (conditional)
```
(the seed lines compiled `(a177_xoro_seed)`; example 1 `MOV result, seed ' Copy result` → `' result = the XORO32 result (this S operand is replaced); seed = new state` `(a177_xoro_ex1)`; example 3 `GETRND  seed              ' Hardware random seed` → `' Seed from GETRND`.)
```yaml
vs_getrnd:
  xoro32_advantages:
    - "Reproducible sequences"
    - "The state is a register you own, so the sequence does not depend on other cogs or on GETRND"
  getrnd_advantages:
    - "No state to keep and no seeding required"
    - "Draws on the cog's xoroshiro128** PRNG, seeded at boot and iterating every clock (not a true-random source)"
notes:
  - "D holds the new state; the PRNG result replaces the S operand of the next instruction"
  - "Seed D with a non-zero value"
  - "Equivalent to the Spin2 ?? operator, which executes XORO32 (INT:319)"
  - "GETRND is a convenient seed source"
  - "NOT suitable for cryptographic applications"
```
`:106` oneliner → `"Iterate D with xoroshiro32+ PRNG algorithm (seed with a non-zero value)"`. The zero-state *behaviour* stays an open question for G4G5's bench item VO-S059 (this page now only advises). Authority above; GETRND text: v55:567, SD:2852-2859 (G1 S-023). Sweep: S-059's list (`random_generation.yaml`, `op_rand.yaml`) is G4G5; `special_registers.yaml:54` is S-023 below.

## S-178 `locktry.yaml:54-63` — outcome returned by `setd .result`
Current (examples[3]): `        setd    .result, #1          ' Success` … `.fail   setd    .result, #0          ' Failed` / `.result ret` — SETD rewrites the D field of the routine's own RET (a RET has no D; nothing reads it back), so the caller gets nothing and the routine modifies itself. Correct — return the outcome in a register:
```yaml
- name: Multi-Resource Manager
  description: Manage multiple locks for complex operations; the outcome is returned in a register
  code: |
    ' Acquire multiple locks in order (prevent deadlock); result = 1 on success, 0 on failure
    acquire_multi
            locktry #LOCK_A            wc
    if_nc   jmp     #.fail
            locktry #LOCK_B            wc
    if_nc   jmp     #.release_a
            locktry #LOCK_C            wc
    if_nc   jmp     #.release_b

            ' Got all locks - proceed
            mov     result, #1           ' Success
            ret

    .release_b
            lockrel #LOCK_B
    .release_a
            lockrel #LOCK_A
    .fail   mov     result, #0           ' Failed
            ret
  source: complex_synchronization
```
compiled `(a178_locktry)`. Authority: CSV:270 (LOCKTRY C = 1 if got LOCK), CSV:343 (`RET {WC/WZ/WCZ}` has no D operand); SD:3688. Sweep: `setd .` / `sets .` against a `ret` label — only this page (`idioms/self-modifying-code.yaml` modifies instruction operands of non-RET targets, S-198 resolved).

## S-179 `fit.yaml:18,21,34` — "$1F0 … before the special-register area"
Registers $000-$1EF are general purpose, **$1F0-$1F7 are dual-purpose** (RAM unless INT1-3 / CALLD-imm PA,PB / LOC functions are used), and **$1F8-$1FF are the special-purpose registers** (SD:441-456). `FIT $1F0` therefore means "fits in the general-purpose registers", and `FIT $1F8` is the limit "before the special registers". Correct:
`:18` `    FIT  $1F0        '' Ensure code fits in the general-purpose registers (before the dual-purpose $1F0-$1F7)` ·
`:21` `  description: Verify code fits in the general-purpose registers (COG addresses 0-$1EF); $1F0-$1F7 are dual-purpose and $1F8-$1FF special-purpose` ·
`:34` `- 'Common limits: $1F0 (end of the general-purpose registers), $1F8 (before the special-purpose registers; the bare-ORG default), $200 (full COG), $400 (COG + LUT)'` (quoted YAML, one line).
`fit $1F0` and `fit $1F8` both compile `(a179_fit, a179_fit2)`. Authority: SD:441-456; `org.yaml:42` and `guides/pasm2-getting-started.yaml:167-169` already say the same. Sweep: `special-register area|before special` over the tree — fit.yaml only.

## S-180 `hubexec.yaml:47`, `:22` — oneliner and bare `@code`
`:47` `oneliner: Set hub execution mode for subsequent code` → `oneliner: Predefined constant for COGINIT instruction` (identical to `cogexec.yaml:36`; HUBEXEC is `%10_0000`, added into COGINIT's D operand, `hubexec.yaml:9`; nothing is set "for subsequent code"). Same edit: `:22` `COGINIT #HUBEXEC+5, @code` → `COGINIT #HUBEXEC+5, ##@code` `(a167_hubexec)` (S-162 sibling), and `:11` `syntax: 'COGINIT #HUBEXEC+id, #address'` → `'COGINIT #HUBEXEC+id, ##address'` (a hub address does not fit a 9-bit `#`). `cogexec.yaml:22`/`:11` likewise. Authority: SD:376-379, SD:406-413; the pages' own `value`/`description`.

## S-181 `debug.yaml` — encoding/timing "TBD", placeholder description
Current: `:4` `encoding: TBD`, `:11-13` `timing: cycles: TBD / type: TBD`, `:14` `description: Debug instruction. Provides debugging functionality during program execution.`, example = bare `DEBUG`. Sources: v55:1056 (a plain `DEBUG` "resolves to a 'BRK #0' instruction, whereas DEBUG() commands resolve to unique 'BRK #1..255'"), v55:1069 ("a 'BRK #code' instruction is inserted where the DEBUG command was placed … If a cog's debug interrupt is disabled, the 'BRK #code' instruction does nothing, taking two clocks"), v55:897 ("one instruction for each PASM DEBUG statement"), v55:909 (up to 255 DEBUG() statements), v55:61-64 (conditions, `language/pasm2/conditional-debug.yaml`), CSV:355 (BRK). Compiled fact: without `-d` a DEBUG line emits **no code** (0 bytes) `(a181_debug_nod)`; with `-d` the debugger program is added `(a181_debug_d)`. Correct:
```yaml
instruction: DEBUG
syntax: DEBUG | DEBUG(...)
compiler_syntax: DEBUG
encoding: "BRK #code (language/pasm2/brk.yaml): EEEE 1101011 00L DDDDDDDDD 000110110; code 0 for a plain DEBUG, 1..255 for DEBUG(...)"
timing:
  cycles: 2
  type: fixed
description: |
  DEBUG is a compiler directive that places one BRK instruction at that point when the program is compiled with DEBUG enabled; without DEBUG enabled it generates no code.
  A plain DEBUG becomes BRK #0 and launches (or updates) the PASM debugger; DEBUG(...) with output commands becomes BRK #1..255, the code indexing that statement's record in the DEBUG database. If the cog's debug interrupt is disabled the BRK does nothing and takes two clocks. A condition prefix (IF_xx DEBUG(...), v50+) is implemented by an opposite-condition SKIP #1 placed before the BRK.
```
and the example becomes two items: `DEBUG` (`' plain DEBUG: BRK #0, opens or updates the PASM debugger`) and `DEBUG("x = ", sdec(x))`. Keep `compiler_encoding:` (the pnut-ts internals) as is; set `documentation_level: comprehensive`; `oneliner:` `Debug instruction` → `Place a BRK that triggers a DEBUG statement (when DEBUG is enabled)`.
Sweep: `TBD` over `deliverables/ai/P2` — `debug.yaml:4,12,13` only. The four other `documentation_level: minimal` pages (`crcbit`, `crcnib`, `rgbsqz`, `loc`) carry a real encoding, timing and description — short, not stubs.

## S-182 `xinit.yaml:55-72` — receive example without the count
Current: `xinit   wmode, #0        '' Start inputting spi_do bits to hub` with `wmode = $C081_0000 + spi_do<<17` — the streamer count D[15:0] is 0, and a count of 0 means the streamer does not run (SD:1401); the source patches the count in first (`flash_loader.spin2:254-261`: `shl x,#5` / `setword wmode,x,#0` / `shl x,#1` / `wypin x,#spi_ck` / `waitx #3` / `xinit wmode,#0`). Correct (item "High-Speed Data Reception"):
```pasm2
shl     x, #5                    ' number of bits to receive (x = number of longs)
setword wmode, x, #0             ' insert the count into the streamer command
shl     x, #1                    ' two spi_ck transitions per bit
wypin   x, #spi_ck               ' Start spi_ck transitions
waitx   #3                       ' Align spi_ck with spi_do sampling
xinit   wmode, #0                ' Start inputting spi_do bits to hub
waitxfi                          ' Wait for streamer to finish
```
compiled `(a182_xinit)`; and the trailing comment block: `'' wmode = $C081_0000 + spi_do<<17  '' 1-pin input, bytes-msb-first, to hub; D[15:0] (the bit count) is set by the SETWORD above`. The other two examples carry their counts in the constant ($0800, $0008) — right. Authority: SD:1401, `flash_loader.spin2:254-261`. Sweep: `xinit … #0` / `xinit  wmode` over the tree — this page.

---

## G8 rows (`language/pasm2/` concepts, groups, idioms, patterns; + arbiter sweep S-183)

## S-183 YAML eats PASM immediates — plain scalar cut at ` #` (52 served strings in 15 files)
**Mechanism.** A plain YAML scalar ends at a space followed by `#`, so `- MOV reg, #42   ' 9-bit immediate` is served as `MOV reg,`, `syntax: CALLD PA|PB|PTRA|PTRB, #{\}Addr | …` as `CALLD PA|PB|PTRA|PTRB,`, and `- ## forces augmented encoding` as an empty item. The fix is **quoting** the scalar (or `|` for code blocks). `hash_sweep.py` re-derived the arbiter's list independently from the YAML composer (a plain/empty scalar whose source line continues with `#`): 168 such occurrences in the tree, of which **47** have `#` followed by a non-space (= the arbiter's 47, same files, same lines) and **5 more truncating strings the 47 do not include**: `language/pasm2/calld.yaml:51` (lost: ` for relative addressing; omit # for absolute addressing.`), `concepts/addressing_modes.yaml:131` (`- # forces immediate encoding`, served empty) and `concepts/branch_addressing.yaml:40, :41, :80` (`JMP vector # Jump to address in vector` etc. — the code survives, the explanation is lost). The other 116 are deliberate annotations (`- path.yaml  # note`, `133  # note`) and stay.
**Correct — the exact edits** (each applied to a scratch copy and composed with PyYAML: the served value of every item was printed and checked, `s183_apply.py` → `out/s183_apply.txt`; 0 sites still cut). Quote style: single quotes when the text has no apostrophe, double quotes (backslashes doubled) when it has one. The `reg` → `r0` renames (S-008, G1) and the relative/`#@` corrections (below) are folded into the same lines.
```
language/pasm2/adds.yaml
5:  description: '<the existing value, unchanged, wrapped in single quotes — it contains no apostrophe>'
language/pasm2/augd.yaml
75: - description: "Using ## syntax (compiler auto-generates AUGD)"
language/pasm2/augs.yaml
2:  syntax: 'AUGS #Src'
95: - description: "Using ## syntax (compiler inserts AUGS automatically)"
language/pasm2/call.yaml
2:  syntax: 'CALL #{\}Addr | CALL Dest {WC|WZ|WCZ}'
50: - 'CALL #Addr'
51: - 'CALL #\Addr'
language/pasm2/calla.yaml
2:  syntax: 'CALLA #{\}Addr | CALLA Dest {WC|WZ|WCZ}'
language/pasm2/callb.yaml
2:  syntax: 'CALLB #{\}Addr | CALLB Dest {WC|WZ|WCZ}'
language/pasm2/calld.yaml
2:  syntax: 'CALLD PA|PB|PTRA|PTRB, #{\}Addr | CALLD Dest, {#}Src {WC|WZ|WCZ}'
49-51 (one item, three lines):
- "Src is a register, 9-bit literal, or 32-bit augmented literal that contains
  the relative or absolute address to set PC to and optional new C and Z
  states. Use # for relative addressing; omit # for absolute addressing."
58: - 'CALLD PA, #Addr'
59: - 'CALLD PB, #Addr'
60: - 'CALLD PTRA, #Addr'
61: - 'CALLD PTRB, #Addr'
language/pasm2/rep.yaml
15:   - "Instruction count is D[8:0] only (maximum 511 instructions, whether D is #immediate or a register); it does not extend beyond 9 bits"
16:   - "Maximum 511 iterations with #immediate; use ## or register for S up to 2^32-1"
language/pasm2/setxfrq.yaml
39:     notes: 'Use ## for 32-bit immediate values'
language/pasm2/wrpin.yaml
64:   description: 'A smart pin should be configured by WRPIN while DIR is low; WRPIN #0 on a running pin resets it with no DIR cycle'
language/pasm2/xzero.yaml
50:   - XSTOP: 'Stop streamer immediately (alias for XINIT #0,#0)'
language/pasm2/concepts/special_registers.yaml
89:       - "SETQ #15       ' Setup for 16 long transfer"
language/pasm2/concepts/rep_instruction.yaml
15:       - block_size: 'Number of instructions to repeat (0-511: only D[8:0] is used, with # or from a register)'
16:       - count: 'Number of iterations (0-511 with #, 0-2^32-1 with ## or a register; 0 repeats forever)'
```
`concepts/addressing_modes.yaml`:
```
16:       - 9-bit: "#0 to #511 (literal fits the instruction's 9-bit S or D field)"
17:       - 32-bit: '##$0 to ##$FFFFFFFF (full 32-bit literal via an augment prefix)'
19:       - "MOV r0, #42          ' 9-bit immediate"
20:       - "MOV r0, ##1000       ' 32-bit Src immediate (AUGS prefix added)"
21:       - "MOV r0, ##$12345678  ' 32-bit Src immediate (AUGS prefix added)"
48:       - RDLONG r0, PTRA[4]   ' Read from hub[PTRA + 16] (index scaled by 4)
49:       - WRWORD r0, PTRB[-2]  ' Write to hub[PTRB - 4] (index scaled by 2)
61:       - RDLONG r0, PTRA++    ' Read from hub[PTRA], then PTRA += 4
62:       - WRWORD r0, PTRB++    ' Write to hub[PTRB], then PTRB += 2
71:       - RDLONG r0, --PTRA    ' PTRA -= 4, then read from hub[PTRA]
81:       - RDLONG r0, PTRA++[8] ' Read from hub[PTRA], then PTRA += 32
82:       - WRLONG r0, PTRB--[1] ' Write to hub[PTRB], then PTRB -= 4      (S-185)
88:     range: '##$00000 to ##$FFFFF'
90:       - "RDLONG r0, ##$10000  ' Read from hub[$10000]"
91:       - "WRLONG r0, ##buffer  ' Write to hub[buffer]"
99:       - "BITH flags, #7        ' Set bit 7 of flags"
100:      - "BITL flags, #READY_BIT ' Clear READY_BIT"
101:      - "TESTB flags, #4 WC    ' Test bit 4, update C"
110:      - ALTR index            ' Next result register = cog[index]      (S-203)
116:      - "SETQ #15              ' Next RDLONG reads 16 longs"
123:      - "REP #4, #10           ' Repeat next 4 instructions 10 times"
130:    - '## forces augmented encoding'
131:    - '# forces immediate encoding'
```
(`reg` is the Spin2 REG[] keyword and does not compile as a register name — compile `(a183_index)` for lines 48-82; lines 19-21 `(a183_immediate)`; 90-91 `(a183_absolute)`; 99-101 `(a183_bit)`; 116/123 `(a183_misc)`; the bad `PTRB++[-1]` → `PTRA/PTRB index constant must range from 1 to 16` `(a185_bad)`.)
`concepts/special_registers.yaml` (S-008 + S-207): `73` `      - GETCT r0      ' Read system counter` · `74` `      - GETRND r0     ' Get a pseudo-random number` · `75` `      - GETQX  r0     ' Get CORDIC X result` · `76` `      - GETPTR r0     ' Read the current FIFO hub pointer` `(a183_special)`. `concepts/stack_operations.yaml:122,128,133` `reg` → `r0` `(a183_stack)`.
`concepts/branch_addressing.yaml` — the relative/absolute rules are what the quoting edit has to carry, so the whole `addressing_modes:` header (lines 11-43) and the `#@label` lines are corrected together. The source (SD:720) says: "Relative addressing is the default when cog code references cog labels or hub code references hub labels … absolute addressing is … forced by the assembler when crossing between cog and hub … Absolute addressing can be forced by the use of `\` after the `#`"; `@` returns the hub address of a label (SD:724). The page's `#@label` as "relative" is the opposite of SD:733 (`JMP #@cog` — "cog to hub, always absolute"):
```yaml
addressing_modes:
  relative_immediate:
    syntax: "#label"
    encoding: "20-bit immediate address with R = 1: PC += A (A in bytes, signed 20 bits)"
    range: "±512 KB: a 20-bit signed byte offset (SD:731, :748 — a jump to itself is A = $FFFFC = -4)"
    instructions: ["JMP", "CALL", "CALLA", "CALLB", "CALLD"]
    examples:
      - "JMP #forward_label    ' Jump to label (relative)"
      - "CALL #subroutine      ' Call with relative address"
      - "IF_Z JMP #skip_it     ' Conditional relative jump"
    notes: "Relative is the default when cog code references cog labels or hub code references hub labels; the assembler converts the label to a PC-relative offset"

  absolute_immediate:
    syntax: "#\\label"
    encoding: "20-bit absolute address (R = 0)"
    range: "$00000-$FFFFF (entire hub space)"
    instructions: ["JMP", "CALL", "CALLA", "CALLB", "CALLD"]
    examples:
      - "JMP #\\hub_routine      ' Jump to absolute hub address"
      - "CALL #\\$10000          ' Call absolute address"
      - "JMP #cog_routine       ' Jump within cog (relative)"
    notes: "\\ forces absolute addressing. Crossing between cog and hub is always absolute and is forced by the assembler, so # alone is enough there; @label is the hub address of a label defined under ORG"
```
and `:49` `- "JMP #label"          # Relative jump` · `:50` `- "JMP #\\label"          # Absolute jump` (unchanged) · `:58` `- "CALL #label"         # Relative call` · common_patterns `:159` `CALL #subroutine` · `:175` `IF_C CALL #handle_low` · `:176` `IF_NC CALL #handle_high` · `:169` see S-188. `(a183_branch_rel, a183_branch_abs, a183_branch_ptrx, a183_branch_hub)` compiled; `JMP #\\hub_routine` (two backslashes, as the plain scalar served) → `Expected a constant, unary operator, or "("` `(b_dblbs_bad)`.
Authority: the YAML 1.2 plain-scalar rule (` #` starts a comment) + `s183-yaml-hash-truncation-sweep.json`; SD:720-751, CSV:426-431 for the branch forms; CSV:132-147 for the ALT forms. Sweep: this row **is** the sweep; the class rule that finds all 52 is the S-200 gate.

## S-184 `ADDPINS #7` — the count is a plain constant
`concepts/basic-io.yaml`: `:124` `syntax: "DIRH #base_pin ADDPINS #count"` · `:126-127` `DIRH #8 ADDPINS #7  ' Pins 8-15 as outputs` / `DIRL #0 ADDPINS #3  ' Pins 0-3 as inputs` · `:131` OUTH syntax · `:133-134` OUTH/OUTL · `:138` DRVH syntax · `:140` `DRVH #16 ADDPINS #7` · `:157` `example: "#8 ADDPINS #7 = pins 8 through 15"` · `:169`, `:170` · `:357` `DIRH  #16 ADDPINS #7` · `:367` `DIRL  #16 ADDPINS #7`. `ADDPINS #7` → `Expected a constant, unary operator, or "("` `(a184_bad)`. Correct (drop the `#` before the count, everywhere):
```pasm2
DIRH #8 ADDPINS 7  ' Pins 8-15 as outputs
DIRL #0 ADDPINS 3  ' Pins 0-3 as inputs
OUTH #8 ADDPINS 7  ' Pins 8-15 output high
OUTL #0 ADDPINS 3  ' Pins 0-3 output low
DRVH #16 ADDPINS 7 ' Pins 16-23 drive high
```
compiled `(a184_dir)`; `:357`/`:367` `DIRH  #16 ADDPINS 7      ' All outputs` / `DIRL  #16 ADDPINS 7      ' All inputs` `(a184_bus)`. YAML: `:124` `syntax: "DIRH #base_pin ADDPINS count"`, `:131` `"OUTH #base_pin ADDPINS count"`, `:138` `"DRVH #base_pin ADDPINS count"`, `:157` `example: "#8 ADDPINS 7 = pins 8 through 15"`, `:169` `example_no_wrap: "#8 ADDPINS 7 = pins 8-15 (no wrapping)"`, `:170` `example_with_wrap: "#28 ADDPINS 7 = pins 28-31, 0-3 (wraps at 31)"`. The page already has it right at `:120` (`base_pin ADDPINS count`), `:163` (`MOV pin_field, ##%00111_001000` `(a184_pinfield)`), and `idioms/pin-control.yaml:15-17`. Authority: SD:3659 (`pins32 long 0 addpins 31`), `pin-control.yaml:15`. Sweep `addpins[ \t]+#` over the tree: exactly these 13 lines in basic-io.yaml.

## S-185 `addressing_modes.yaml:82` — `PTRB++[-1]`
Current `WRLONG reg, PTRB++[-1]' Write to hub[PTRB], then PTRB -= 4` → `PTRA/PTRB index constant must range from 1 to 16` `(a185_bad)` (masked in the gate by the `reg` error). Correct (listed with S-183): `WRLONG r0, PTRB--[1] ' Write to hub[PTRB], then PTRB -= 4` `(a183_index)`; the page's own `index_range` (`:79`, "1 to 16 … -- forms subtract") already says so. Authority: SD:3172 (`INDEX = 1..16 for ++'s and --'s`), SD:3198-3199. Sweep: `ptr[ab](++|--)\[ *-` over the tree: this line only (the two `PTRA[0]` hits in `object_archetypes.yaml:315,338` are plain indexes, legal).

## S-186 `IF_C NOP` — NOP cannot take a condition
Current `conditional_execution.yaml:219-220` `' Even NOP!` / `IF_C    NOP` → `NOP cannot have a condition or _RET_` `(a186_nop_bad, a186_nop_ret_bad)`: NOP is the all-zero instruction word (CSV:25, `0000 0000000 000 000000000 000000000`), and EEEE = 0000 is `_RET_`, not "never". The page teaches the opposite in six places. Correct:
`:219-220` delete the two lines (the rest of the block compiles `(a186_ok)`) · `:22` `  Every PASM2 instruction except NOP can optionally:` · `:24` `  2. Conditionally update C and Z flags (WC, WZ, WCZ suffixes), on the instructions that list a flag effect (DJNZ, RETI and NOP take none)` · `:29` `  that require branches, P2 can conditionally execute almost any instruction in-place (NOP, the all-zero word, cannot carry a condition or _RET_).` · `:17` FAQ add the answer "Yes, every instruction except NOP" · `:201` `description: "Any instruction except NOP can be conditional"` · `:324` `universal: "Works on all instructions except NOP, not just a subset"` · `:370` `EVERY instruction except NOP can be conditional and can conditionally set flags (where it lists a flag effect).` · `:377` `P2: any instruction except NOP conditional, no pipeline penalties`. The legal stand-in when a "conditional no-op" is wanted is any harmless instruction (`IF_C MOV x, x` compiles). Authority: CSV:25; the compiler message. Sweep (`if_xx nop`, `_ret_ nop`): this one line.

## S-187 `RETI1 WCZ` (and the RETI/RESI description)
Current: `event_interrupt_config.yaml:79` `syntax: "RETI0/1/2/3 {WC/WZ/WCZ}"`, `:81` `behavior: "Pop address from internal stack, restore flags"`, `:82` `example: "RETI1 WCZ  ' Return and restore both flags"`, `:205` `RETI1 WCZ        ' Restore flags` → `This effect is not allowed for this instruction` `(a187_reti_bad)`. RETIx **is** `CALLD INB,IRETx WCZ` (CSV:186-189; SD:2304-2311) — the WCZ is part of the alias. Correct:
```yaml
    RETI0_3:
      syntax: "RETI0/1/2/3"
      operation: "Return from an interrupt service routine; the interrupted address, C and Z are restored"
      behavior: "RETIx is the alias CALLD INB,IRETx WCZ (RETI0: CALLD INB,INB WCZ): it jumps to the address saved in IRETx, restores C and Z from it, and clears the cog's interrupt-busy flag so another interrupt of that level can occur. It takes no WC/WZ/WCZ of its own"
      example: "RETI1  ' Return from the INT1 service routine"
```
`:205` → `        RETI1            ' Restore flags and return (RETIx restores C and Z itself)` `(a187_reti)`. (RESIx lines are S-205.) Sweep: `reti[0-3][ \t]+w` over the tree: these two lines (+ `architecture/interrupts.yaml:243`, a correct alias description).

## S-188 `#` used as the comment character inside PASM blocks
Sites: `concepts/branch_addressing.yaml:110` `JMP #@far_label       # Combined for 32-bit range` and `:169` `JMP #@other_function    # Tail call optimization` — both inside `|` scalars, so the `#` reaches the compiler: `Expected an assembly effect or end of line` (G8 `h_asis*`). PASM2's comment is `'`. Correct: `:169` → `      JMP #other_function    ' Tail call optimization` `(a188_tail)`. `:104-110` (`long_branches`, where `:110` lives) is deleted whole under S-218 (the block's claim is false); if the sprint keeps a block there, the line is `JMP #\far_label       ' absolute 20-bit target` `(a188_long_branch_hash)`. Authority: the page's own `'` comments (`:152`, `:160`); SD:731-751. Sweep: `grep -rniE '(jmp|call|calla|callb|loc)\s+#[@\\A-Za-z0-9_$.]+\s+# '` and the mnemonic-list variant over the whole tree: `# comment` after a PASM instruction occurs **only** in `branch_addressing.yaml` (the 10 plain-scalar list items are S-183 truncations and are quoted there; `:110` and `:169` are the two inside `|` blocks that reach the compiler). The `;` comment character is S-137.

## S-189 P1 `MAX`/`MIN`
`concepts/cog_hub_execution.yaml:266-267` `MAX    peak, data` / `MIN    valley, data` → `Expected a unique name, BYTE, WORD, LONG, or assembly instruction` `(a189_max_bad)`. P2 has FGE/FLE (unsigned) and FGES/FLES (signed): "Force D >= S. If D < S then D = S" keeps the larger (CSV:50-53). Correct (the block `:262-268`, with the S-167 `##1000`):
```pasm2
REP   #4, ##1000
RDLONG data, ptra++
ADD    sum, data
FGE    peak, data          ' peak = the larger of peak and data (unsigned)
FLE    valley, data        ' valley = the smaller of valley and data (unsigned)
RET
```
compiled `(a189_fge)`. P1-class sweep (`sweep.py` D: MAX MIN MAXS MINS WAITPEQ WAITPNE WAITCNT WAITVID JMPRET LOCKSET LOCKCLR COGNEW MOVD MOVS MOVI SUBABS ABSNEG as a mnemonic; plus a grep for `cnt|phsa|frqa|ctra|vcfg` as PASM operands): these two lines only (`CLKSET` hits are the Spin2 method).

## S-190 COGINIT with three operands
Sites: `concepts/cog_hub_execution.yaml:274` `COGINIT #16, #@cog_code, #@parameters`, `concepts/multi_cog_synchronization.yaml:291` `coginit cog_num, #worker_code, work_index` → `Expected an assembly effect or end of line` `(a190_workdist_bad)`. COGINIT takes D (the cog selector) and S (the hub start address, also PTRB); the PTRA value comes from a SETQ **before** it (SD:404-411; CSV:258 `COGINIT {#}D,{#}S {WC}`). Correct:
```pasm2
SETQ    ##@parameters            ' PTRA of the new cog
COGINIT #16, ##@cog_code         ' #16 = %0_1_0000: load and start a free cog; S goes to its PTRB
```
compiled `(a190_initial)`; and in the work-distribution loop (`:291`):
```pasm2
        setq    work_index                  ' PTRA of the new cog
        coginit cog_num, ##@worker_code     ' two operands: cog selector, hub start address
```
compiled in full `(a190_workdist)`. (`#@cog_code` with one `#` could not hold a hub address either — S-167.) Authority: SD:368-398, :404-411. Sweep: `coginit` with three comma-separated operands over the tree: these two lines. With S-165/S-172 those are all the COGINIT defects the sweeps found in `language/pasm2`.

## S-191 `LONG @@method_table` in DAT
`concepts/labels.yaml:112-116` (`object_relative`): `syntax: "@@label"`, `meaning: "Object-relative address"`, `context: "Spin2 or PASM - object method tables"`, `example: "LONG @@method_table"` → `Expected a constant, unary operator, or "("` `(a191_at_bad)`. `@@` is the Spin2 operator that turns an object-relative offset stored in DAT (`LONG @label`) into an absolute hub address; it is not a DAT data expression (v55:300, :308, :425; the same rule as G2G3 S-107, G4G5 S-118). Correct:
```yaml
    object_relative:
      syntax: "@@label"
      meaning: "Absolute hub address from an object-relative offset stored in DAT (a Spin2 operator: hub address of this object + offset)"
      context: "Spin2 methods only - not accepted as a DAT data expression"
      example: "DAT: ptrs LONG @start, @fin  (stores object-relative offsets);  Spin2: addr := @@ptrs[i]"
```
`LONG @start, @fin` compiled `(a191_at_ok)`. (`end` is reserved — S-008.) Sweep: `@@` over `language/pasm2`: this entry only.

## S-192 `$$` as the hub origin
Specced under G4G5 S-119 (`rows-S111-S161-specs.md:243`, "labels.yaml:124-128 … delete the entry"). The exact text for this page: delete `current_hub_address:` (`:124-128`) and make the `$` entry read
```yaml
    current_origin:
      syntax: "$"
      meaning: "Current origin: the cog register address in ORG (cog-exec) code, stepping by 1 per instruction; the hub address in ORGH (hub-exec) code, stepping by 4"
      context: "PASM instructions and data expressions"
      example: "JMP #$-1           ' Jump back one instruction"
```
`LONG $ + 4` under ORGH compiles `(a192_dollar)`; `LONG $$ + 4` → `"$$" (DITTO index) is only allowed within a DITTO block, inside a DAT block` `(a192_dollar_bad)`. Authority: v55:312, :321, :42.

## S-193 an instruction mnemonic used as a constant
`concepts/register_indirection.yaml:64` `MOV exec_reg, ##(ADD | (dst<<9) | src)` → `Expected a constant, unary operator, or "("` `(a193_alti_bad)`. An instruction word is built from numbers: ADD's opcode field is `0001000`, CZI = 0, EEEE = %1111 (CSV:34 `EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS`), so `$F100_0000 | (dst<<9) | src`. Correct:
```pasm2
MOV exec_reg, ##$F100_0000 | (dst<<9) | src   ' an ADD dst, src instruction word
ALTI exec_reg
NOP                     ' This becomes ADD dst, src
```
compiled (`dst`, `src` CON constants) `(a193_alti)`. If the intent is only "execute a stored instruction", the simpler form is a data long holding the instruction: `exec_reg add r0, r1` then `ALTI exec_reg` / `NOP` `(a193_alti_reg)` (CSV:147: ALTI D "Execute D in place of next instruction"). Authority: CSV:34, :147, SD:5470. Sweep: `##\((add|sub|mov|and|or|xor|jmp|call|nop|ret)\b` over the tree: this line only.

## S-194 `ALTS index++` — no such syntax
Sites: `concepts/register_indirection.yaml:95-97` (syntax_variants), `:99-104` (increment_modes example), `:155-161` (array_copy). `ALTS index++` → `Expected an assembly effect or end of line` `(a194_alts_bad)`. ALTx has no `++`/`--`; the post-update is the signed S[17:9] added to D after the substitution: `ALTS D,{#}S` — "D += sign-extended S[17:9]" (CSV:142; PM:1327 "usually 0, 1, or -1"). `##$200` adds 1, `##$3FE00` subtracts 1 (S[17:9] = %1_1111_1111). The two REP block counts were also wrong (S-209). Correct:
```yaml
  increment_modes:
    description: "ALTx adds the sign-extended S[17:9] to D after the substitution (index update)"
    options:
      - "S[17:9] = 0: D unchanged (a plain 9-bit #S)"
      - "S[17:9] = 1: D incremented by 1"
      - "S[17:9] = -1: D decremented by 1"
    syntax_variants:
      - "ALTS index, #base                (no update)"
      - "ALTS index, ##$200 + base        (post-increment)"
      - "ALTS index, ##$3FE00 + base      (post-decrement)"
    examples:
      - |
        MOV index, #0
        REP #3, #10
          ALTS index, ##$200 + table   ' Index increments after use
          MOV sum, 0-0
          ADD total, sum
```
(The instruction forms compiled, `(a194_alts_inc)`.) `array_copy` (`:155-161`), one instruction at a time because an ALTx alters *the next instruction* (S-217):
```pasm2
REP #4, count
ALTS src_ptr, ##$200      ' next S = src_ptr, then src_ptr += 1
MOV  tmp, 0-0             ' tmp = cog[src_ptr]
ALTD dst_ptr, ##$200      ' next D = dst_ptr, then dst_ptr += 1
MOV  0-0, tmp             ' cog[dst_ptr] = tmp
```
compiled `(a194_copy)`. Authority: CSV:140-143, PM:1324-1327. Sweep: `alt[a-z]+ \w+(\+\+|--)` over the tree: these four lines only.

## S-195 `IF_C process_received_byte`
`concepts/streamer_smartpin_control.yaml:127-128` `RDPIN data, #rx_pin WC` / `IF_C process_received_byte` → `Expected an assembly instruction` `(a195_bare_bad)`. Correct: `IF_C CALL #process_received_byte` `(a195_rdpin)`. Authority: CSV:427 (`CALL #{\}A`); the compiler. Sweep (`cond_sweep.py`: a condition prefix followed by a word that is not a mnemonic): this line; the other four hits (`conditional_execution.yaml:338,341,361,365`) are `IF_xx ...` placeholders in prose examples.

## S-196 one-operand `ADDCT1 ##1_000_000` (with S-137 `;`, S-219 part 2)
Sites: `groups/counter_event_jumps.yaml:27-31`, `counter_event_polls.yaml:21-25`, `counter_event_waits.yaml:21-25`: the shared single-quoted `code: 'ADDCT1  ##1_000_000 ⏎ ; ... do work ... ⏎ JCT1    #timeout_handler'`. `ADDCT1 D,{#}S`: D is the register holding the timestamp from GETCT, S the delta (CSV:169; "Adds S into D"); an immediate cannot be D → `Expected a constant, unary operator, or "("` `(a196_one_bad)`; the `;` comment is S-137's error. This replaces S-137's `'' ... do work ...` fix for these three pages (one edit). Correct — and each page's example now exercises **its own** group (jump / poll / wait, S-219 part 2):
`counter_event_jumps.yaml` examples (`:25-33`):
```yaml
examples:
- title: Basic counter timeout pattern
  code: |
    GETCT   t
    ADDCT1  t, ##1_000_000
    ' ... do work ...
    JCT1    #timeout_handler
```
`counter_event_polls.yaml` (`:19-25`):
```yaml
examples:
- title: Basic counter timeout pattern
  code: |
    GETCT   t
    ADDCT1  t, ##1_000_000
    ' ... do work ...
    POLLCT1 wc                 ' C = 1 if the CT1 event flag was set (the flag is cleared)
    if_c    jmp #timeout_handler
```
`counter_event_waits.yaml` (`:19-25`):
```yaml
examples:
- title: Basic counter timeout pattern
  code: |
    GETCT   t
    ADDCT1  t, ##1_000_000
    ' ... do work ...
    WAITCT1                    ' Wait for the CT1 event flag, then clear it
```
compiled `(a196_jumps)` `(a196_polls)` `(a196_waits)`. Also `counter_event_jumps.yaml:13` `timing_details: 'Timing: 1'` (a stub value, O22) → `'JCTx/JNCTx: 2 clocks if not taken, 4 if taken in cog or LUT execution; 2, or 13...20 if taken in hub execution'` (CSV:206 JCT1 row, `2 or 4` / `2 or 13...20`); the polls/waits pages say "See individual instructions" — consistent. Authority: CSV:169 (ADDCT1), :296 (POLLCT1 "Get CT1 event flag into C/Z, then clear it"), :312 (WAITCT1), :206 (JCT1). Sweep: `addct[123]\s+##` one-operand over the tree: these three (this row is G4G5's NF-5).

## S-197 `ptr++` on a register that is not PTRA/PTRB
Sites: `idioms/loop-control.yaml:84` `rdlong  x, ptr++`, `:89` `rdlong  x, src++`, `:90` `wrlong  x, dst++`; `idioms/scratch-storage.yaml:31` `rdlong x, ptr++` → `Expected an assembly effect or end of line` (G8 `q_*`). Post-increment is a PTRA/PTRB expression (CSV:178 `RDLONG D,{#}S/P`, P = a PTRx expression). Correct: `loop-control.yaml:84` `        rdlong  x, ptra++`; `:89` `        rdlong  x, ptra++`; `:90` `        wrlong  x, ptrb++`; `scratch-storage.yaml:31` `        rdlong x, ptra++` `(a197_loop)`. Note the examples cite `flash_loader.spin2` lines 58-59, which read through the FIFO (`rdfast #0,#0` / `rep #2,s` / `rflong v`): the KB lines are an adaptation with `rdlong` — add "adapted from" to `source_example:` (NF-9). Sweep (`cond_sweep.py`: `name++`/`--name` operands that are not PTRA/PTRB): these four lines (+ the three `ALTS … ++` of S-194).

## S-198, S-199 — RESOLVED (tooling)
S-198 (`.local` label defined outside the excerpt): RESOLVED 2026-10-09, assume `label:NAME` / `label:.NAME` (NC21). S-199 (relative `$` address on the first line): RESOLVED 2026-10-09, assume `lead:N` (NC22). Nothing to do; none hides a KB defect.

## S-200 gate: a YAML scalar silently cut by a same-line comment (build spec)
No gate sees S-183: every KB gate reads the **parsed** value, and the cut value parses; `audit-kb-code-compiles.py` compiles the cut string and fails only where the cut leaves illegal code (22 gated sites), so the other 25 of the arbiter's 47 sites (the `syntax:` / prose ones) and the 5 extra ones pass untouched. Build:
- **New** `engineering/tools/validation/audit-yaml-plain-scalar-comment.py`, beside `audit-yaml-duplicate-keys.py`. Algorithm (`hash_sweep.py` is the reference implementation): `yaml.compose(text, SafeLoader)`; for every `ScalarNode` with `style is None`, read the source line at `end_mark.line`; if `line[end_mark.column:]` matches `^\s*#`, record (file, line, served value, lost text). **Flag** when (R1) the character after `#` is not a space, or (R2) the scalar is empty (a key or `- ` item with nothing before the comment), or (R3) the scalar contains whitespace (a multi-word value followed by a comment). **Allow** a comment after a single-token plain scalar with a space after the `#` (`- language/pasm2/rep.yaml  # note`, `133  # Per datasheet`), and the `encoding:  # [bits|write|c|z|clocks] …` header comment.
- Result today (`gate_rule.py`): 168 comment-after-plain-scalar occurrences, **52 flagged** (47 R1 + the 5 listed under S-183); after the S-183 edits: **0**.
- Wire it where `audit-yaml-duplicate-keys.py` is wired: `engineering/tools/validate-dod-release.py` (release) and the edit-time hook that runs the YAML audits, and **arm** it in `engineering/tools/validation/audit-gate-arming.py` with a known-bad control (a scratch YAML holding `- MOV r0, #42  ' x`, which must fail).
- Authority: the YAML 1.2 plain-scalar rule; the S-183 sweep. The two rows ship together (the gate lands with the S-183 edit so the count goes 52 → 0 in one release).

## S-201 `basic-io.yaml:404-405` — LOCKTRY C polarity inverted
Current (`lock_coordination_example`): `LOCKTRY lock_id WC        ' Try to acquire lock` / `IF_C  JMP #try_again      ' C=1 means locked by other COG`. LOCKTRY sets C = 1 when the lock **was taken** (CSV:270 "C = 1 if got LOCK"; SD:3688); the page's retry branch is inverted, and `try_again` is never defined. Correct (`:401-409`):
```yaml
  lock_coordination_example:
    code: |
      ' COG 0 and COG 1 share pin 16
      .try    LOCKTRY lock_id WC        ' Try to acquire lock
      IF_NC   JMP     #.try             ' C=0: another cog holds the lock - try again
              DRVH    #16               ' We have the lock, drive pin
              ' ... do work ...
              DIRL    #16               ' Release pin (tri-state)
              LOCKREL lock_id           ' Release lock
```
compiled `(a201_lock_try)`. Authority: SD:3688, CSV:270; the same subject stated correctly at `multi_cog_synchronization.yaml:30,33-34`. Sweep (LOCKTRY polarity): the 20 `locktry … wc` sites the grep returns (`multi_cog_synchronization.yaml`, `locktry.yaml`, `architecture/locks.yaml:211-317`) all test `if_nc` = failed / `if_c` = got it; this is the only inverted one. G9's S-233 (`locks.yaml:121,142-143,182`, "owner ID is in lock_num") is a different defect on the same subject — the sprint should edit that page in the same pass.

## S-202 `register_indirection.yaml:72-85`, `:171-181` — ALTB addresses register 0
Current: `MOV bit_num, #7` / `ALTB bit_num, #0` / `BITH flags, #0-0        ' Actually sets bit 7` — ALTB replaces the next instruction's **D** field with `(D[13:5] + S) & $1FF` and leaves its S alone, so the target is register 0 (bit_num[13:5] = 0, S = 0) and `flags` is never touched; the bit number stays the literal `#0-0` = 0. The next instruction reads the bit number from its own S operand — the *same register* (SD:546-560 `ALTB bitindex,#base` / `BITC 0,bitindex`). Correct (entry `ALTB`, lines 72-85):
```yaml
  ALTB:
    function: "Substitute the D (register) field of the next BITxxx/TESTB instruction"
    syntax: "ALTB bit_reg, #base"
    operation: "Next instruction's D = (bit_reg[13:5] + base) & $1FF; its S operand supplies the bit number, so name the same register there (bit_reg[4:0])"
    range: "14-bit bit index: register offset in [13:5], bit number in [4:0]"
    examples:
      - |
        MOV bit_num, #7
        ALTB bit_num, #flags
        BITH 0-0, bit_num       ' Actually sets bit 7 of flags
```
compiled `(a202_altb)` (the old form compiles too and is the wrong program `(a202_altb_old)`). `bit_scan` (`:171-181`):
```pasm2
MOV bit_pos, #0
.loop
  ALTB bit_pos, #flags
  TESTB 0-0, bit_pos WC    ' C = bit bit_pos of flags
  IF_C JMP #found
  ADD bit_pos, #1
  CMP bit_pos, #32 WZ
  IF_NZ JMP #.loop
```
compiled `(a202_scan)`. The description line `:75` "Next instruction's bit field = base + bit_reg[4:0]" is the same misreading → replaced by the `operation:` above. Authority: SD:546-560; CSV:144-145 (`ALTB D,{#}S`: "Alter D field of next instruction to (D[13:5] + S) & $1FF"; the one-operand alias is `S = 0`); PM:1063-1064 (the BITxxx S[9:5] caveat: a `SETQ #0` before ALTB+BITxxx forces the single-bit form — add as a note). Sweep: `altb` over the tree: `altb.yaml` (the instruction page) states the rule correctly; only these two blocks misuse it.

## S-203 `register_indirection.yaml:47-51` (+ `addressing_modes.yaml:110`) — ALTR result register
Current: `MOV offset, #3` / `ALTR offset, #0` / `ADD base_reg, value     ' Result goes to base_reg+3` — ALTR sets the result register to `(D + S) & $1FF` = 3 + 0 = **register 3**; the base has to be the S operand. Correct:
```pasm2
MOV offset, #3
ALTR offset, #base_reg
ADD base_reg, value     ' Result goes to base_reg+3
```
compiled `(a203_altr)` (the old form is the program that writes register 3, `(a203_altr_old)`). `addressing_modes.yaml:110` `ALTR index ' Next result = cog[D + index]` → `ALTR index            ' Next result register = cog[index]` (the one-operand form substitutes D[8:0], CSV:139). Authority: SD:529 (`ALTR index,#table` "set next write to table+index"), CSV:138-139.

## S-204 `event_interrupt_config.yaml:240` — `SETINT3 #12 ' ATN event`
Event 12 is "Streamer NCO rollover"; ATN is event **14** (SD:2051, :2053; the page's own table `:104`, `:106`). Correct: `      SETINT3 #14      ' ATN event` `(a204_isr)`. Sweep (every `SETINT[123]` line against its comment, 25 grep hits): all agree except this line (`cog_attention.yaml:181,262` `#14`, `interrupts.yaml:390` `#%1110` are right).

## S-205 `event_interrupt_config.yaml:84-88` — RESIx
Current: `operation: "Resume from interrupt (continue interrupted code)"`, `behavior: "Like RETI but continues interrupted instruction"`, `use: "For interrupts that don't fully handle event"`. RESIx = `CALLD IJMPx,IRETx WCZ` (CSV:182-185; SD:2313-2317): it returns to the interrupted code **and stores the ISR's next address in IJMPx**, so the next interrupt resumes the ISR after the RESI instead of at its start. Correct:
```yaml
    RESI0_3:
      syntax: "RESI0/1/2/3"
      operation: "Return from the interrupt, but resume this ISR at its next instruction when the next interrupt occurs"
      behavior: "RESIx is the alias CALLD IJMPx,IRETx WCZ: it returns to the interrupted code and writes the ISR's next address into IJMPx, so the next interrupt continues after the RESI instead of at the start of the ISR (RETIx leaves IJMPx unchanged)"
      use: "Co-routine style interrupt service routines that keep their place between interrupts"
```
Authority: SD:2313-2317 ("use RESIx to have your ISR resume at the next instruction when the next interrupt occurs"), CSV:182-185. Sweep: `resi[0-3]` over the tree: `groups/interrupt_resume.yaml:13` states the alias correctly (`RESI0 = CALLD INA,INB WCZ`, i.e. `CALLD $1FE,$1FF WCZ`, CSV:185); this page is the only misdescription.

## S-206 CALLA/CALLB — "PTRx = PC+4", "return address in PTRA"
Sites: `concepts/branch_addressing.yaml:64-72` and `:198`; `concepts/stack_operations.yaml:70-78` (+ `:61` CALL "Push PC+4"). CALLA writes `{C, Z, 10'b0, PC[19:0]}` to the **hub long at PTRA++** (CALLB: PTRB++); RETA/RETB read the long at `--PTRA`/`--PTRB` (CSV:344-347, :428-429). So it is a *push onto a hub stack addressed by PTRA/PTRB*, not "PTRx = return address", and it needs a stack in hub RAM (CALLA 5...12 clocks cog, 14...32 hub-exec; RETA 11...18 / 20...40). Correct:
```yaml
  CALLA/CALLB:
    description: "Call with the return address pushed onto a hub stack addressed by PTRA/PTRB"
    operation: "Write {C, Z, 10'b0, PC[19:0]} to the hub long at PTRA++ (CALLB: PTRB++), then jump"
    examples:
      - "CALLA #function       ' Push {C, Z, PC} to hub at PTRA++, then jump"
      - "CALLB #function       ' Push {C, Z, PC} to hub at PTRB++, then jump"
      - "RETA                   ' Return: pop the long at --PTRA"
      - "RETB                   ' Return: pop the long at --PTRB"
    use_case: "Calls nested deeper than the 8-level hardware stack; the stack lives in hub RAM (set PTRA/PTRB first)"
```
`best_practices` `:198`: `Prefer CALLA/CALLB for leaf functions` → `Use CALLA/CALLB when call depth exceeds the 8-level hardware stack (CALL itself costs 4 clocks, CALLA 5...12)`. `stack_operations.yaml`: `:61` `operation: "Push {C, Z, PC} (the address of the next instruction) onto the hardware stack"`; `:71` `operation: "Push {C, Z, PC} to the hub long at PTRA++"`, `:76` `… at PTRB++` (and `return: "Via RETA"` / `"Via RETB"` stay). The calls compile with a stack pointer set `(a206_calla, a183_branch_ptrx)`. Authority: CSV:343-347, :428-429 (the immediate forms). Sweep: `calla|callb` prose over `language/pasm2` — `concepts/cog_hub_execution.yaml:338-339` (instruction-name lists) and `calla.yaml`/`callb.yaml` (correct) are the other hits.

## S-207 `special_registers.yaml:22`, `:76` — GETPTR / "SETPTR"
Current `:22` `- access: Direct use in many instructions, explicit via GETPTR/SETPTR`, `:76` `GETPTR reg     ' Read PTRA/PTRB value`. GETPTR returns the current **hub FIFO pointer** (CSV:352 "Get current FIFO hub pointer into D"; SD:1174); PTRA/PTRB are ordinary registers at $1F8/$1F9 (`MOV x, PTRA`). There is no SETPTR (0 hits for `setptr` in the instruction sheet, SD, PASM2 manual, datasheet and v55; control: `getptr` hits CSV:352 and SD ×4). Correct: `:22` `    - access: Direct as registers ($1F8/$1F9: MOV x, PTRA / MOV PTRA, ##addr) and as pointer expressions (PTRA++, PTRA[index])`; `:76` `      - GETPTR r0     ' Read the current FIFO hub pointer` and add `      - MOV r0, PTRA   ' Read PTRA` `(a183_special)`. Same page (S-023/O8): `:54` `features: True random based on thermal noise` → `features: xoroshiro128** PRNG, seeded at boot, iterating every clock (not a true-random source)`; `:43` `description: Quotient/auxiliary register (32-bit)` → `description: Q register (32-bit): block-transfer count for SETQ/SETQ2, and the 32-bit extension/aux value for CORDIC commands`; `:84` `- Q receives quotient from DIV operations` → `- SETQ sets Q for the next block transfer or CORDIC command; CORDIC results come from GETQX/GETQY (QDIV: quotient in X, remainder in Y)`. Authority: CSV:352, :337 (SETQ), :260; SD:1174; v55:567 (GETRND). Sweep: `setptr` over the tree: this page only.

## S-208 `cordic_solver.yaml:105-109` — POLLQMT as a non-blocking "result ready" test
Current: `POLLQMT             WC    ' C=1 if pipeline empty` / `IF_NC GETQX result        ' Retrieve only if available`. The QMT event flag is set when a GETQX/GETQY **already executed** with no result queued or in progress, and POLLQMT reads-and-clears that history bit (SD:2207-2211); it says nothing about a result still being computed, and GETQX simply waits for the result (CSV:282). The page says so itself at `:155-157`. There is no non-blocking CORDIC "result ready" poll. Correct (replace `non_blocking_check:`, `:105-109`):
```yaml
  no_result_ready_poll:
    description: There is no non-blocking "result ready" test for the CORDIC
    code: |
      QMUL    a, b
      ' ... 55 or more clocks of other work ...
      GETQX   result_lo       ' waits for the result if it is not ready yet
      GETQY   result_hi
    note: "POLLQMT is not a result-ready poll: its flag is set only when a GETQX/GETQY executed with nothing queued or in progress, which is a programming error (event 15). To avoid a stall, schedule the read at least 55 clocks after the command."
```
compiled `(a208_cordic)`. Authority: SD:2054, :2207-2211, :3413; CSV:282. Sweep: `pollqmt` over the tree: this block (`pollqmt.yaml` and `event_system.yaml` describe the event correctly).

## S-209 REP block sizes that do not match the body
Sites: `rep_instruction.yaml:115-119` `REP #32, #32` over 2 instructions; `:135` `REP #2, #16` over 3; `:190-195` `IF_NZ REP #4, count`; `register_indirection.yaml:99-104` `REP #4, #10` over 3 (S-194); `:156-161` `REP #2, count` over 3 (S-194, now 4). REP's D is the number of instructions in the block (SD:757; CSV:257), and a REP skipped by its condition leaves the body to run **once** as ordinary code, while S = 0 repeats forever (SD:759). Correct:
```pasm2
REP #2, #32
SHR input, #1 WC
RCL output, #1
REP #3, #16
RDLONG multiplicand, PTRA++
MUL multiplicand, coefficient
ADD accumulator, multiplicand
```
compiled `(a209_rep)`. `conditional_rep` (`:189-195`):
```pasm2
CMP count, #0 WZ
IF_Z JMP #skip_loop           ' count = 0: REP with S = 0 would repeat forever
REP #4, count
nop                           ' ... four body instructions ...
nop
nop
nop
skip_loop
```
compiled `(a209_cond_rep)`. **Class sweep** (`rep_sweep.py`: a `REP #n,…` and the number of instruction lines that follow): 19 hits, of which exactly the five above are mismatches; the rest are label forms (`REP @.stall`), generic syntax illustrations (`addressing_modes.yaml:123`, `rep_instruction.yaml:17,32`), the stall idiom `REP #99, #1` (cordic_solver.yaml:132, rep_instruction.yaml:152), `architecture/hub.yaml:213` (body followed by a `' Process data` placeholder), `spin2/integration/spin2-pasm2-integration.yaml:119` (RET follows the one-instruction body — right), `cog_hub_execution.yaml:263` (4-instruction body then RET — right), and the S-216 corpus tokens. Authority: SD:757-759, CSV:257.

## S-210 `rep_instruction.yaml:15`, `:22`, `:66-67`, `:94` — block-size range and branches
D is `D[8:0]` only (SD:757): 0..511 whether `#` or a register; only the iteration count S is 32 bits. `rep.yaml:15-16` already says so. Correct:
`:15` (listed under S-183) · `:16` (S-183) · `:19-25` extended form:
```yaml
  extended_form:
    - instruction: "REP #block_size, ##count"
    - parameters:
      - block_size: Number of instructions to repeat (0-511; only D[8:0] is used)
      - count: Extended via AUGS prefix (0 to 2^32-1)
    - example: "REP @.end, ##1000  ' 1000 iterations using AUGS prefix"
    - note: "Compiler automatically emits an AUGS prefix for a count > 511"
```
(`(a210_ext)`); `:67` `    - Maximum 511 iterations with a # immediate; up to 2^32-1 with ## or a register; a count of 0 repeats forever` · `:94` (cannot_contain) `    - Branch instructions are allowed but any branch taken inside the block cancels the REP (SD:775)` — the page's own `:202` teaches `IF_Z JMP #found ' Exits REP block`, and `:68` says "branches cancel REP". Authority: SD:757-759, :775, CSV:257. Sweep: `2\^32` near `REP` over the tree: this page (the instruction page `rep.yaml:12-16` is right).

## S-211 `loop-control.yaml:62-65` — DJNF "max(1, count) times"
DJNF decrements and jumps while the result is not $FFFF_FFFF (CSV:195), so the body runs **count + 1** times: count 0 runs once, count 3 runs four times. Current `:63-65` `- DJNZ: "while not zero" — loop body runs count times; UNSAFE for count=0` / `- DJNF: "at least once, then while not underflowed" — loop body runs max(1, count) times; SAFE for count=0`. Correct (lines inside the `context: |` block scalar): 
```text
        - DJNZ: "while not zero" — loop body runs count times; UNSAFE for count=0
        - DJNF: "at least once, then while not underflowed" — loop body runs
          count + 1 times (count = 0 runs it once; start at count - 1 to run it count times);
          SAFE for count=0
```
Authority: CSV:195 (`DJNF` "Decrement D and jump to S** if result is not $FFFF_FFFF"), the page's own `:58-60`. Sweep: `max\(1` over the tree: this line.

## S-212 `cog_hub_execution.yaml:209-210`, `:220-221` — "REP not available" in hubexec
The same page says REP works in hubexec (`:32-36`, `:100`, `:415-425`; SD:773 "REP works in hub memory, as well, but executes a hidden jump to get back to the top of the repeated instructions"). Correct (`performance_comparison.timing_critical.hubexec`):
```yaml
    hubexec: |
      ' REP also works in hubexec, but its hidden jump back to the top of the block pays
      ' the same branch-refill cost per iteration as a taken DJNZ, so the loop is shown with DJNZ
      MOV   count, #100
      .loop
      ADD   a, b              ' 2 clocks (sequential, FIFO streaming)
      SUB   a, b              ' 2 clocks
      XOR   c, d              ' 2 clocks
      ROL   e, #1             ' 2 clocks
      DJNZ  count, #.loop     ' 13-14 clocks taken (FIFO refill, +1 if misaligned)
      ' Per iteration: 8 (body) + ~13 (DJNZ taken) = ~21 clocks
      ' Total: ~2100 clocks for 100 iterations
      ' Cost difference vs cogexec (~13x in this loop) comes ENTIRELY from
      ' the branch refill (DJNZ here; REP's hidden jump costs the same) - NOT from
      ' per-instruction throughput.
      ' The four ALU ops in the body run at the SAME 2 clocks each.
```
(only `:209-210` and `:220-221` change). Authority: SD:773; the page's `:32-36`. Sweep: `REP not available|lack of REP` over the tree: this block. (Observation NF-8 on the "13-14" figure.)

## S-213 `streamer_smartpin_control.yaml:346` — NCO full scale
Current `bits_per_streamer_clk = 2^32 / SETXFRQ_value`. The streamer NCO adds the frequency into `phase = (phase & $7FFF_FFFF) + frequency`; the multiplier is **$8000_0000** (SD:1288-1296), so one rollover (one streamer step, one bit in a 1-pin mode) every `$8000_0000 / SETXFRQ` sysclks. With the page's own numbers the old formula gives 2^32/$4000_0000 = 4 where the text says 2. Correct (`:341-354`):
```yaml
    rule: |
      When pairing a P_TRANSITION smart pin (clock) with a streamer
      (data) for SPI-style synchronous I/O, the bit rate and edge rate
      must satisfy:
        sysclks_per_streamer_bit = $8000_0000 / SETXFRQ_value
        sysclks_per_SCK_edge     = WXPIN_value
      For lockstep at sysclk/2 SPI:
        SETXFRQ = $4000_0000 (= 1 bit per 2 sysclks)
        WXPIN   = 1          (= 1 sysclk between SCK edges)
        → 1 streamer bit = 2 sysclks = 1 full SCK cycle (2 edges). Lockstep.
```
The worked values (`$4000_0000`, `$2000_0000`) were right. Authority: SD:1288-1296, `setxfrq.yaml:55` (already "$8000_0000 (2^31), not 2^32"). Sweep: `2^32 / (SETXFRQ|freq)` over the tree: this line; `smart-pin-00110-nco-frequency.yaml:174` is the smart pin's own NCO, a different accumulator.

## S-214 `pasm2_hub_synchronization.yaml` — `rdlong … wc ' set C if non-zero`, `waitx ##20-2`
Current `:13` `rdlong  value, hub_ptr  wc      ' Read from hub, set C if non-zero` / `:14` `if_c  jmp  #process_data`; `:17-18` `wait_hub` / `waitx  ##20-2   ' Wait for hub window`. RDLONG WC puts the long's **MSB** in C (CSV:178 "C = MSB of long"); WZ gives Z = (long == 0). WAITX only burns clocks; the hub access aligns itself to the cog's slot (RDLONG 9...16 clocks in cog execution, CSV:178), so there is no hub-window wait to code. Correct (`implementation:`):
```pasm2
' Hub synchronization pattern
hub_write
        wrlong  value, hub_ptr          ' Write to hub (waits for this cog's hub slot by itself)
        add     hub_ptr, #4             ' Advance pointer

hub_read
        rdlong  value, hub_ptr  wz      ' Read from hub, Z = 1 if the long is zero
 if_nz  jmp     #process_data           ' Process if data present
```
(drop the `wait_hub` block and its comment; `value long 0` / `hub_ptr long $4000` stay) compiled `(a214_hubsync)`. Authority: CSV:176-178 (RDBYTE/RDWORD/RDLONG rows: flags and the 9...16 clock hub-read timing). Sweep: `waitx ##20-2` / `hub window` over the tree: this file; `rdlong … wc` followed by a "non-zero" comment: this line.

## S-215 `conditional_execution.yaml:146` — IF_NC_OR_Z "unsigned below/equal"
`%1011` is `IF_NC_OR_Z` = C = 0 **or** Z = 1 (CSV:468); below-or-equal is `%1110` `IF_C_OR_Z` (CSV:478 with IF_LE :480 and IF_BE :481), which the page lists correctly at `:170`. Correct: `    use: "C clear or Z set (after a comparison the same as above-or-equal, IF_AE: Z = 1 implies C = 0)"`. Authority: CSV:468, :478-482. Sweep: `nc_or_z` over the tree — `conditional-debug.yaml:25` ("Carry not set or zero set") is right.

## S-216 `loop-control.yaml:27-35`, `:100` — a "loop" instruction/marker that does not exist
`loop_instruction` (`pattern: "loop"`, "Loop instruction marker", "Loop end marker for REP instruction", examples `sample_cy loop`, `Field loop`, `main loop`, `usage_count: 166`) and `:100` `- language/pasm2/rep.yaml        # LOOP end marker is documented within rep.yaml`. PASM2 has no LOOP instruction or marker: no `LOOP` row in the instruction sheet (grep `-w loop` over the CSV: 0 hits), and in the sources `loop` is only an ordinary label (SD:869 `loop RFBYTE i`, :1660 `loop xcont …`, :2382 `loop drvnot #0`; control: `grep -w REP` hits SD:757). REP's end is `REP @.end, count` (SD:766-771) `(a216_rep_label)`. Correct: delete the whole `loop_instruction` item (`:27-35`) and `:100` → `  - language/pasm2/rep.yaml`. Also (NF-4) `:8` `pattern: "rep #{iterations}, #{instructions}"` has the operands swapped (REP D = instructions, S = iterations). Authority: CSV (no LOOP row), SD:757, :766-771, :869. Sweep: `loop_instruction|LOOP end` over the tree: this file.

## S-217 `register_indirection.yaml:106-113` — back-to-back ALT stacking (answered by the sources)
Current: `ALTS src_index` / `ALTD dst_index` / `MOV 0-0, 0-0           ' Copies from computed to computed`, and `:128` "Back-to-back ALTx possible", against `:186` "Cannot chain (each affects only next instruction)". The sources are **not silent**: "ALTS alters the next instruction regardless of its kind" (PM:1331; the same sentence on every ALTx page, e.g. PM:1306, :1123), so in `ALTS / ALTD / MOV` the ALTS alters the **ALTD**, not the MOV; and the silicon doc's AUGS erratum (SD:129) shows an ALTx is an ordinary pipeline instruction that can be altered/augmented. One ALTx therefore substitutes into one instruction. The way to substitute S and D (and the result register) of one instruction is **ALTI** (SD:601-658). No bench. Correct:
```yaml
  combined_operations:
    description: "ALTx alters only the instruction that follows it; to substitute both S and D of one instruction use ALTI"
    examples:
      - |
        ' Copy with computed source and destination: ptrs[8:0] = source register, ptrs[17:9] = destination register
        MOV  ptrs, ##(dst_reg<<9) | src_reg
        REP  #2, count
        ALTI ptrs, #%111_111      ' next D = ptrs[17:9], next S = ptrs[8:0]; both then step up by 1
        MOV  0-0, 0-0
```
compiled `(a217_alti_pair)`. `:128` → `    - ALTx alters only the next instruction, even when that instruction is itself an ALTx`. `:14-15` `operation: "Next_S = base + index_reg[8:0]"` → append `; then index_reg += sign-extended S[17:9]` (the update that S-194's text now carries). Authority: PM:1324-1331, SD:513-520, :601-658, :129; CSV:142, :146-147. Sweep: `alt[sdr]\s+\w+\s*$` followed by another ALT line, over the tree: `register_indirection.yaml:111-112` only.

## S-218 `branch_addressing.yaml:53`, `:104-110`, `:119-124` — branch timing and "beyond ±1MB"
Current `:53` `pipeline: "2-cycle latency for all jumps"`; `:121-124` "Branch taken: 2-cycle penalty", "Indirect branch: Same 2-cycle penalty", "RET instruction: 2-cycle penalty"; `:104-110` `long_branches: Branches beyond ±1MB … Use AUGS for extended range`. A taken cog-exec branch is **4 clocks** and a hub-exec branch **13...20** (JMP/CALL/RET, CSV:341-343, :426-427; conditional branches DJNZ/TJZ/…: "2 or 4" cog, "2 or 13...20" hub, CSV:193-204); CALLA/CALLB are 5...12 (hub-exec 14...32), RETA/RETB 11...18 (20...40) (CSV:344-347). The hub is 1 MB (20-bit addresses) and AUGS augments the next *#S* operand — `JMP #A` carries its own 20-bit address field (CSV:426, :432), so nothing beyond the 20-bit reach exists. Correct:
```yaml
    timing: "JMP/CALL/RET taken: 4 clocks in cog or LUT execution, 13...20 in hub execution; DJNZ/TJZ-family branches: 2 clocks not taken, 4 taken in cog execution (2, or 13...20, in hub execution)"
```
(replacing `pipeline:` at `:53`), and
```yaml
branch_optimization:
  pipeline_effects:
    - "Branch taken (JMP, CALL, RET, ...): 4 clocks in cog or LUT execution, 13...20 clocks in hub execution"
    - "DJNZ/TJZ-family branches: 2 clocks when not taken"
    - "Indirect branch (JMP register): same 4 / 13...20 clocks"
    - "CALLA/CALLB: 5...12 clocks (cog execution); RETA/RETB: 11...18"
```
and **delete** `long_branches:` (`:104-110`; this also removes the S-188 `#` site at `:110`). Authority: CSV:193-206 (branch rows), :341-347, :426-429; `cog_hub_execution.yaml:26,31` (the page's own numbers). Sweep: `2-cycle` over `language/pasm2`: these four lines.

## S-219 `conditional_execution.yaml:231-234` (and the POLL/WAIT group pages)
Part 1 — current `TEST    value, #$80 WZ    ' Test sign bit` / `IF_Z    ADD sum, value    ' Add if positive`: `#$80` tests bit 7, not bit 31, and TEST WZ sets Z when the masked bits are all **zero** (CSV:105 "Z = ((D & S) == 0)"), so Z = 1 means "bit clear". Correct (`conditional_accumulation`):
```pasm2
TEST    value, ##$8000_0000 WZ    ' Z = 1 when bit 31 (the sign bit) is clear
IF_Z    ADD sum, value            ' Add if non-negative
```
compiled `(a219_test)`; equivalents `CMPS value, #0 WC` / `IF_NC ADD sum, value` `(a219_cmps)` and `TESTB value, #31 WC` / `IF_NC ADD sum, value` `(a219_testb)`. `branchless_min_max` (`:224`): `description: "Find the unsigned minimum without branches"` (CMP is unsigned; use CMPS for signed). Same TEST-class edits: `conditional-debug.yaml:58` (S-173) and `conditional_execution.yaml:309,315` `TEST    flags, #READY_BIT WZ` — if `READY_BIT` is a bit **number** (the page's `#HAVE_LOCK` neighbours are bit numbers) it must be `TESTB    flags, #READY_BIT WC` / `IF_NC JMP #wait_loop` `(a219_ready)`; if it is a mask it is right: the page does not say, so this is **NF-7**, not a change.
Part 2 — `counter_event_polls.yaml:21` and `counter_event_waits.yaml:21` share the JCT1 (jump) example: each page now shows its own instruction — text under **S-196**.
Authority: CSV:105 (TEST), CSV:58 (TESTB). Sweep: `test\s+\w+,\s*#` with `wz|wc` over the tree (`conditional-debug.yaml:58,102`, `special-registers.yaml:281,302`, `instruction_skipping.yaml:145`, `getting-started.yaml:303`, `conditional_execution.yaml:232,309,315`): only `:232` and `conditional-debug.yaml:58` misdescribe; `special-registers.yaml:281` `test INA, #1 wz ' Test if pin 0 is high` is right for IF_NZ (Z = 0 means high).

---

## New findings (outside the rows above; each with authority)
1. **NF-1 — `concepts/special_registers.yaml:96`** "CORDIC results must be read before next CORDIC operation" is false: commands may be overlapped (pipeline 54 clocks, results read in submission order; SD:3413 "it is possible to overlap CORDIC commands … several commands are initially given … then results are read and another command is given") and the sibling `cordic_solver.yaml:159-163` teaches exactly that. Fix: `- CORDIC commands can be overlapped; results come back in submission order (read each with GETQX/GETQY)`. Same page `:25` `Auto-increment/decrement modes (++, --, ++)` repeats `++` — delete the third.
2. **NF-2 — `concepts/addressing_modes.yaml:134-137`** `size_based` ("Values 512-$FFFFF: AUGS augmented" / "Values $100000+: AUGD augmented") contradicts the page's own `:22` (the AUGS/AUGD split is by field, Src vs Dest, not by width) and CSV:432-433 (AUGS = next #S, AUGD = next #D). Fix: `- Values 0-511: Direct immediate (#)` / `- Values 512 and up: augmented immediate (##) — AUGS for a Src literal, AUGD for a Dest literal`.
3. **NF-3 — `concepts/multi_cog_synchronization.yaml:305-334` (`barrier_synchronization`) is wrong in logic, not only in its `=` lines (S-164).** `add old, #1` then `wrlong new, ptra` writes a register `new` that is never loaded; the "retry if changed" compare cannot work (`cmp check, old`), and P2 has no atomic read-modify-write on hub RAM other than a lock. A working one-shot barrier with the same shape (compiled `(a164_barrier_locked)`), counter guarded by a lock:
```pasm2
CON
  barrier_count   = $7FFF0
  barrier_target  = 8
  barrier_lock    = 3

DAT
        org 0
barrier_wait
.lock   locktry #barrier_lock   wc
if_nc   jmp     #.lock
        rdlong  count, ##barrier_count
        add     count, #1
        wrlong  count, ##barrier_count
        lockrel #barrier_lock
        cmp     count, #barrier_target wz
if_z    jmp     #.release
.wait   rdlong  count, ##barrier_count
        cmp     count, #0       wz
if_nz   jmp     #.wait
        ret
.release
        wrlong  #0, ##barrier_count
        cogatn  #$FF
        ret
```
compiled `(a164_barrier_locked)`. Authority: SD:3688 (LOCKTRY), the page's own `lock_operations`. (Design choice D4.)
4. **NF-4 — `idioms/loop-control.yaml:8`** `pattern: "rep #{iterations}, #{instructions}"` has the operands swapped: REP's D is the **instruction count**, S the iterations (`rep #5, #80` = 5 instructions, 80 times). Fix `pattern: "rep #{instructions}, #{iterations}"`. Authority: SD:757, CSV:257.
5. **NF-5 — `concepts/multi_cog_synchronization.yaml:289-290`** (`work_distribution`) `shl work_index, #16` runs on **every** pass of `.loop`, shifting the previously packed cog number out; the intent (index in the upper half, cog number in the lower, passed as PTRA) wants a scratch register: `mov param, work_index` / `shl param, #16` / `or param, cog_num` / `setq param` / `coginit cog_num, ##@worker_code`. Authority: the block's own comments; compile in sprint (S-190 already compiles the `setq`/`coginit` pair).
6. **NF-6 — `concepts/branch_addressing.yaml:15`** `range: "±1MB from current instruction"` for the relative immediate: a 20-bit signed byte offset spans ±512 KB (SD:731, :748 show a jump to itself assembling to A = $FFFFC = -4, i.e. byte units). The corrected block in S-183 carries "±512 KB"; that figure is arithmetic on SD:731/748, not a sentence in a source — drop it if the sprint prefers only quoted facts.
7. **NF-7 — `concepts/conditional_execution.yaml:309,315`** `TEST    flags, #READY_BIT WZ`: if `READY_BIT` is a bit **number** (as `#HAVE_LOCK` is on neighbouring pages) this tests the wrong mask; the page does not say. Undecided: if a number, `TESTB    flags, #READY_BIT WC` / `IF_NC JMP #wait_loop` `(a219_ready)`. Same file `:316` `IF_Z    JMP #$-1        ' Loop on this instruction` → `' Loop back to the TEST above` (`$-1` is the previous instruction; `$` steps by 1 per cog-exec instruction, v55:312).
8. **NF-8 — `concepts/cog_hub_execution.yaml:217`** "13-14 clocks taken" for DJNZ in hubexec versus CSV:193 "2 or 13...20" (and the page's own `:31` "minimum 13 (+1 if not long-aligned)"): the figures `~21` per iteration / `~2100` total are minimums. Undecided which value is typical; say "at least 13".
9. **NF-9 — `idioms/loop-control.yaml:96`, `:66`; `idioms/scratch-storage.yaml:46`** cite `flash_loader.spin2` lines 58-59 (and 60, 78, 84, 286-291) for code that, in the source, reads through the FIFO (`rdfast #0,#0` / `rep #2,s` / `rflong v` / `add @zeroa/4,v wz`, `flash_loader.spin2:56-60`). The KB's `rdlong x, ptra++` lines (S-197) are an adaptation → add "adapted from" to `source_example:` / `source:`.
10. **NF-10 — `architecture/debug_interrupt.yaml:213,231`** `WRLONG  PC, trace_ptr` / `WRLONG  PC, break_log`: `PC` is not a PASM2 register (`special_registers.yaml:15` itself says the PC has "no direct read instruction"). I cannot yet say which register holds the interrupted address inside the debug ISR (the sources read here describe IRET0/INB via `RETI0 = CALLD INB,INB WCZ`, CSV:189) — a finding for the owner of the debug-interrupt rows, not a defect I can fix.
11. **NF-11 — `language/spin2/integration/spin2-pasm2-integration.yaml:356,359,360`** `JMP @slowCode` / `CALL @complexMath` / `JMP @fastCode`: `JMP D` with a bare `@label` is the register-indirect jump of a hub address read as a register (S-162 class). Probably inside S-102's block (349-366) — confirm it is covered; the form to try is `JMP #\@slowCode` / `CALL #\@complexMath` (SD:734 `JMP #\@cog` — compile in sprint, not compiled here).

## Decisions for the sprint / for Stephen
- **D1 (sprint) — S-162 `posx`/`negx` examples.** The old examples were also meaningless (a signed value cannot exceed POSX or fall below NEGX; `fles value, POSX` is a no-op). Rewrite them as the running-minimum / running-maximum and the "most negative number" test (recommended; text given, compiled), or keep the old shapes with only `##` added (smaller diff, keeps vacuous examples). Recommend the rewrite.
- **D2 (sprint) — S-169 `orgh.yaml` example.** `ORGH $400,$800` (recommended: builds in a Spin2+PASM program and in a PASM-only program) · keep `ORGH $FC000,$FC800` with the context note only (it is the v55 illustration, v55:322) · delete the example. The row's wording ("cannot build") should be corrected in the register: it builds in a Spin2+PASM program.
- **D3 (Stephen/arbiter) — gate for bare constants.** A lower-case CON constant < 512 used bare as a D/S operand compiles silently into the wrong operand (S-162, `mov flag, TRUE` class); no regexp finds them. Add a gate rule "an assumed `=con` name used as a bare D/S operand is a defect" to the kb-compile harness (recommended; one assume-list lookup), or accept the residual. Also punch-list 6 (TRUE/NEGX accepted silently) stays a tool item.
- **D4 (sprint) — NF-3 barrier.** Lock-guarded counter (recommended; compiled) · delete the pattern (P2 has no hub atomic add) · keep and mark "illustrative". Recommend the lock version.
- **D5 (sprint) — S-218 `long_branches`.** Delete the block (recommended: its claim is false and it carries the S-188 `#` line) · reword as "AUGS does not extend branches".
- **D6 (sprint) — S-217.** Replace `combined_operations` by the ALTI example (recommended) · delete the item. No bench: PM:1331 answers it.
- **D7 (sprint) — S-183 quoting style.** Quote the scalars in place (recommended: smallest diff, the 52-site gate lands with it) · convert each list to `|` blocks (readable, larger diff). Either is accepted by the S-200 rule.
- **D8 (sprint) — S-200 rule strictness.** R1+R2+R3 flags 52 today and 0 after the S-183 edit (recommended) · flag every comment after a plain scalar (168 today; the 116 deliberate annotations would need an allow-list).
- **D9 (optional, no pins) — silicon confirmation.** None is needed for any row here (every question is answered by an ingested source). If Stephen wants belt and braces for the ALT semantics (S-171, S-202, S-203, S-217): a 15-line pure-PASM program that runs `ALTGB`/`ALTB`/`ALTR`/`ALTS+ALTD` and DEBUGs the registers — no jumpers, any cog.

## Counts
Rows: 58 (S-162..S-219) — change spec 55 (S-162..S-197, S-201..S-219; S-174, S-188, S-190, S-192 point at the batch that holds the rule and give the exact text for these sites; S-217 resolved from the sources; S-169 refined), build spec 1 (S-200), RESOLVED earlier 2 (S-198, S-199). Bench questions: 0. Reclassifications: 0.
Compile tally (`tally.py`, final state of `p/`): **142 probe compiles in 9 probe files** — 119 compiled clean (the corrected forms, and unchanged or silently-compiling counterparts used for comparison: `a162_true_bad`, `a167_hubexec_at_bad`, `a171_altgb_old`, `a202_altb_old`, `a203_altr_old`, `a214_old`, `a219_test_old`, `a173_cdbg_zero_old_d`, `a175_xor_old`), 23 failed as expected, reproducing the quoted compiler messages. YAML-parsed (`s183_apply.py`): 55 line edits + the 3-line `calld.yaml:49-51` item, 0 sites still cut.
**Not compiled here ("compile in sprint"), by row:** S-174 (stamps), S-177 (YAML prose; the seed lines compiled), S-179, S-180 (oneliner/syntax), S-181 (page text; the DEBUG fact compiled), S-184 (syntax lines; the examples compiled), S-186 (prose), S-187 (YAML block; the instruction compiled), S-191 (YAML), S-192 (YAML), S-205, S-206, S-207, S-208 (prose; code compiled), S-210 (YAML lines), S-211, S-212 (the page's own lines + a note), S-213, S-215, S-216, S-217 (prose), S-218 (timing text), S-200 (gate not built), NF-3 and NF-5 text beyond the compiled barrier, NF-11's replacement form. Every PASM instruction line in a `pasm2` fence above is the text of the probe named after it.
Scratch (not part of the repo): `/tmp/claude-1000/-workspaces-P2-Knowledge-Base/fd20d1c1-e1ec-45fc-a5bc-7f395c46f9e1/scratchpad/s219/` — `lib.py`, `probes1.py`..`probes9.py`, `run.py`, `tally.py`, `sweep.py`, `sweep2.py`, `fold_sweep.py`, `hash_sweep.py`, `gate_rule.py`, `rep_sweep.py`, `cond_sweep.py`, `at_sweep.py`, `conassign_sweep.py`, `s183_apply.py`, `s183_list.py`, `cmp_arbiter.py`, `p/` (probe sources + `.bin`), `s183_copy/` (edited YAML copies), `out/` (sweep reports).



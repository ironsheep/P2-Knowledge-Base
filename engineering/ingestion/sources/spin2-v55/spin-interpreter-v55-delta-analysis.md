# Spin2 interpreter v55 - delta analysis against v51

Delta ingestion (ingest-source §0.5). The v51 interpreter is already analysed in
`engineering/ingestion/sources/spin2-v51/spin-interpreter-v51-complete-analysis.md`; this file
records only what v55 changes and what the v55 source now settles. It does not paraphrase the interpreter.

Method: `diff` of the two ingested files (read-only), then targeted reads of the v55 routines.
Line citations are `v55:N` / `v51:N` into the files named in §1.

---

## 1. Source

| Item | v55 (new edition) | v51 (existing edition) |
|------|-------------------|------------------------|
| Path | `engineering/ingestion/external-inputs/source-code/spin-interpreter/v55/Spin2_interpreter.spin2` | `engineering/ingestion/external-inputs/source-code/spin-interpreter/v51/Spin2_interpreter.spin2` |
| md5 | `174468bb85003c9dedadfb2d86beb244` | `3065e3f6c78d162a3c079364ad7c9bf8` |
| Header line (line 4) | `'*  Spin2 Interpreter - v55 - 2026.05.07  *` | `'*  Spin2 Interpreter - v51 - 2025.04.02  *` |
| Lines (`wc -l`) | 3042 | 2960 |

- Line 1 of both files is Chip's own note (`'TESTT add registers stack_start ...`); it is present in v51 as well and is not a v55 change (it is not in the diff).
- Provenance: copied byte-identical from the PNut-TS distribution parts
  (`engineering/document-production/manuals/p2-xbyte-programming-guide/REF-NO-COMMIT/pnut-ts-parts/Spin2_interpreter.spin2`).
  PNut-TS v1.55.8 embeds the compiled image of this exact file (and not the v51 interpreter's); it embeds the v51 debugger source's image. (Arbiter-verified 2026-10-09; not re-run here.)
- Trust tier: Parallax official source (Chip Gracey's interpreter source), same tier as v51.
- The v55 history table used below is `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt` lines 86-142 (v52 :86, v53 :117, v54 :122, v55 :135).

**Limit on attribution.** Only v51 and v55 of the interpreter are held; v52, v53 and v54 are not. A diff change is assigned to a history entry below by matching its content to the entry's text. Where the content matches none, it is listed in §2.5. The diff cannot say which of v52-v55 introduced a change.

---

## 2. The delta, by version-history entry

### 2.1 v52 (2025-10-08), spin2-v55-text.txt:86-116

| History item | Interpreter change | Where |
|--------------|--------------------|-------|
| `MOVBYTS(longvalue, pattern)` | new hub-table entries and routine | table `bc_movbyts word @movbyts_` v55:150 (`$E4`); routine `movbyts_` v55:2519-2523. New; v51 has none. |
| `ENDIANL(longvalue)` | table entry and routine | `bc_endianl` v55:151 (`$E6`); `endianl_ ... movbyts x,#%%0123` v55:2530 |
| `ENDIANW(wordvalue)` | table entry and routine | `bc_endianw` v55:152 (`$E8`); `endianw_ shl x,#16` then falls into `endianl_` v55:2529-2530 |
| `NEXT n` / `QUIT n` (outer REPEAT level) | no interpreter change found; the diff shows no change in the branch routines (`branch` v55:835). Compile-time. | - |
| `DEBUG(DEBUG_END_SESSION)`, TERM colour controls | no interpreter change found. The interpreter's `debug_` (v55:821) is not changed in function; its skip-pattern field is re-encoded (see §2.5). Handled by the debugger / host. | - |

### 2.2 v53 (2026-03-10), spin2-v55-text.txt:117-121

`OFFSETOF(structure.member)`: no interpreter change found. Compile-time constant; nothing in the diff relates to it.

### 2.3 v54 (2026-04-22), spin2-v55-text.txt:122-134

Bitfields on byte/word/long structure members: no v54-specific interpreter change can be identified. The v51 interpreter already had bitfield setup bytecodes (`bc_setup_bfield_pop` v51:789, `bc_setup_bfield_rfvar` v51:790, `bc_setup_bfield_0_31` v51:794); the diff changes bitfield handling only in the v55 way (§2.4). Struct-member bitfields are therefore either compile-time over the existing setup bytecodes or fall under §2.4; the interpreter alone cannot say.

### 2.4 v55 (2026-05-07), spin2-v55-text.txt:135-142

Both v55 items are "one less bytecode" optimisations; both are implemented by new compressed and combined bytecodes in the variable-operator (altcode) table.

**(a) Bitfield read/write take one less bytecode.**
- v51: a bitfield access was a setup bytecode (`bc_setup_bfield_*`) followed by a separate read-var / write-var bytecode (v51:789-794, `bit_imm`/`bit_pop` v51:602-620, routine comment "Setup bitfield (13 longs)").
- v55: setup, read and write are separate bytecodes that each finish the whole access:
  - `bc_read_bfield_pop` `'7B` v55:636, `bc_write_bfield_pop` `'7C` v55:637
  - `bc_read_bfield_rfvar` `'7E` v55:640, `bc_write_bfield_rfvar` `'7F` v55:641
  - `bc_read_bfield_0_31_` `'Cx`/`'Dx` v55:651-652, `bc_write_bfield_0_31_` `'Ex`/`'Fx` v55:654-655
  - routine `bit_imm`/`bit_rfvar`/`bit_pop` rewritten, "Setup/read/write bitfield (23 longs)", v55:778-800; `var_rd`/`var_wr` annotated with the shared letters d-i, v55:803-816.
- Setup bytecodes remain: `bc_setup_bfield_pop` `'7A` v55:635, `bc_setup_bfield_rfvar` `'7D` v55:639, `bc_setup_bfield_0_31_` `'Ax`/`'Bx` v55:648-649 (formerly `'Ex`/`'Fx`, v51:794-795).
- Read-modify-write forms (`++`, `--`, `+=` ...) still use setup then operator: consistent with the history text "excluding read-modify-writes".

**(b) Pointer `++`/`--` takes one less bytecode.**
- v51: a separate bytecode `bc_set_incdec` (`'79`, v51:676, routine `set_inc rfvar incdec`, v51:561) set the step before the operator.
- v55: the step 2..33 is in the bytecode itself: `bc_set_incdec_2_33_` `'8x`/`'9x` v55:645-646 -> `set_incn` v55:739-740 (`mov incdec,pa` then `sub incdec,#inc_adj`). `bc_set_incdec_rfvar` `'15` v55:521 / `set_incr` v55:737 remains for larger steps (the v51 behaviour, renamed).
- Constants: `bc_set_incdec_2_33 = $80`, `inc_adj = bc_set_incdec_2_33 - 2` (yields 2..33), v55:14, 20. This matches the history text "when SIZEOF(Struct) <= 33".

**(c) Mechanism common to (a) and (b).** The altcode (variable-operator) table moved from `orgf $279` (v51:674) to `orgf $215` (v55:519), and the trigger changed from `_ret_ setq2 #$0E1` to `_ret_ setq2 #$081` everywhere it occurs (v55 :742, :775, :797; the v51 sites are the three `setq2 #$0E1` hunks at diff lines 563, 596 and the bitfield routine near 620). The altcode index labels shift by `$64` for the entries that exist in both (see §3).

### 2.5 Interpreter changes that map to NO history entry

Listed plainly; each is an internal rearrangement visible only in the diff.

1. **PINLOW/PINHIGH merged.** v51 had separate `pinl_` (`drvl`) and `pinh_` (`drvh`) (v51:646-647, `bc_pinlow` -> `pinl_`, `bc_pinhigh` -> `pinh_`). v55 has one routine `pinlh drvnz x` (v55:824) with the bytecodes distinguished by Z: `bc_pinlow` `'35 Z=1`, `bc_pinhigh` `'36 Z=0` (v55:939-940). The "Miscellaneous" block shrinks 26 -> 25 longs (v55:819).
2. **LOOKUP/LOOKDOWN/CASE range split.** The `range` routine (v51:1285) is cut down and jumps to a new hub routine `rangeh` (v55:1677) for LOOKUP/LOOKDOWN; LUT footprint 26 -> 15 longs (v55:1220 region comment). The old text is kept inside a `{ }` comment at v55:1666-1675. The encodings of `bc_case_range`, `bc_lookup_range`, `bc_lookdown_range` change (v51:883, :888 -> v55:908, :913-914). The comment "look:" becomes "lookup/lookdown:" (v55:1316 region). I could not tell from the diff that the observable behaviour changed.
3. **Skip-pattern re-encodings, same bytecode functions:** `bc_pop_rfvar` (v51:875 -> v55:900), `bc_debug` (v51:929 -> v55:954), `bc_setup_reg` and `bc_setup_reg_pi` (v51:944-945 -> v55:969-970), `bc_setup_reg_1D8_1F8_` (v51:1044 -> v55:1069). These follow from `reg_ap` now also serving set-incdec (comment "Setup reg variable / Set incdec (14 longs)", v55:720).
4. **Constant `bc_con_n` -> `bc_con_n1_14`** (v51:1043 `bc_con_n`; v55:7, 1068). Value `$A0` is unchanged. The adjust operand `bc_con_n-$2FF` (v51:807) becomes `con_adj` = `bc_con_n1_14 + 1` (v55:19, 852) = `$A1`, still "-1..14".
5. **Code relocations (no content change found):** `return_` v51:1055 -> v55:662; `var_ptr` v51:1076 -> v55:510 (`addbase` v51:800 -> v55:504); the "Miscellaneous (16 longs)" block with `pop2`/`cased` v51:822-839 -> v55:1093-1110.
6. **Trailing comment** "Things to add: FROUND/FTRUNC, #>. / <#., SIN/ASIN, COS/ACOS, TAN/ATAN" at v55:2537-2545 (Chip's to-do list, not implemented, not in v51).

---

## 3. Bytecode table changes

The interpreter has two tables: the hub bytecode table (`bc_* word @routine`, routines called by `bc_hub_bytecode`) and the LUT bytecode (altcode and primary) tables (`bc_* long routine | skip-pattern`). The hex in the comments of the second kind is the LUT index (address minus `$200`).

### 3.1 Added

| Name | Value | Where |
|------|-------|-------|
| `bc_movbyts` | `$E4` | v55:150 |
| `bc_endianl` | `$E6` | v55:151 |
| `bc_endianw` | `$E8` | v55:152 |
| `bc_set_incdec_2_33_` | `'8x`, `'9x` | v55:645-646 |
| `bc_read_bfield_pop` / `bc_write_bfield_pop` | `'7B` / `'7C` | v55:636-637 |
| `bc_read_bfield_rfvar` / `bc_write_bfield_rfvar` | `'7E` / `'7F` | v55:640-641 |
| `bc_read_bfield_0_31_` | `'Cx`, `'Dx` | v55:651-652 |
| `bc_write_bfield_0_31_` | `'Ex`, `'Fx` | v55:654-655 |

New `CON` block, v55:14-20: `bc_set_incdec_2_33 = $80`, `bc_setup_bfield_0_31 = $A0`, `bc_read_bfield_0_31 = $C0`, `bc_write_bfield_0_31 = $E0`, `con_adj`, `inc_adj`. The compressed-main constants (v51:7-12, `$B0`..`$F0`) are unchanged in value; v55:7 adds the name `bc_con_n1_14 = $A0`.

### 3.2 Renamed

| v51 | v55 |
|-----|-----|
| `bc_set_incdec` `'79` v51:676 | `bc_set_incdec_rfvar` `'15` v55:521 |
| `bc_con_n` v51:1043 | `bc_con_n1_14_` v55:1068 (CON `bc_con_n1_14` v55:7) |
| `pinl_` and `pinh_` routines v51:646-647 | one routine `pinlh` v55:824 |
| `set_inc` v51:561 | `set_incr` v55:737 |

### 3.3 Renumbered (altcode index; function unchanged)

Every altcode entry that exists in both editions moved by `-$64`, except the bitfield setup entries (v51 `'DE`, `'DF` -> v55 `'7A`, `'7D`) and the `Ex`/`Fx` immediate setup (-> `Ax`/`Bx`). Examples (v51:N -> v55:N):

| Bytecode | v51 | v55 |
|----------|-----|-----|
| `bc_repeat_var_init_n` | `'7A` :678 | `'16` :523 |
| `bc_repeat_var_init_1` / `_init` / `_loop` | `'7B`/`'7C`/`'7D` :679-681 | `'17`/`'18`/`'19` :524-526 |
| `bc_get_field`, `bc_get_addr` | `'7E`, `'7F` | `'1A`, `'1B` |
| `bc_read`, `bc_write`, `bc_write_push` | `'80`, `'81`, `'82` | `'1C`, `'1D`, `'1E` |
| `bc_var_inc` | `'83` | `'1F` |
| `bc_logand_write` / `bc_logor_write` | `'A5` / `'A7` v51:726/728 | `'41` / `'43` v55:572/574 |
| `bc_frac_write_push` (last operator) | `'DD` v51:787 | `'79` v55:633 |
| `bc_setup_bfield_pop` | `'DE` v51:789 | `'7A` v55:635 |
| `bc_setup_bfield_rfvar` | `'DF` v51:790 | `'7D` v55:639 |
| `bc_setup_bfield_0_31` (immediate) | `'Ex`/`'Fx` v51:794-795 | `'Ax`/`'Bx` v55:648-649 |

The collapse of the 8-way `xbyte` immediates is described at v55:644 ("bytecodes 8x/9x/Ax/Bx/Cx/Dx/Ex/Fx are collapsed at runtime to LUT entries 80/81/82/83/84/85/86/87"); v51:792 says Ex/Fx -> E0/E1.

### 3.4 Removed

No bytecode name is removed outright; each v51 name is either kept (renumbered), renamed, or replaced as in §3.2. `bc_set_incdec` is replaced by `bc_set_incdec_rfvar` + `bc_set_incdec_2_33_`.

### 3.5 Not renumbered

The primary bytecode table `$00`..`$FF` and the hub table before `bc_movbyts` show no value change in the diff (e.g. `bc_call_*` `'08`..`'11` v55:881-891; `bc_logand` `'8C` v55:1043 = v51:1018; `bc_getrnd` `'31` v55:934 = v51:909; `bc_pinread` `$9E` v55:112 = v51:103).

---

## 4. Facts this source now settles

All below are identical in v51 unless stated (the diff has no hunk in these routines).

### 4.1 PINREAD of one pin returns 0 or 1, not -1 (S-061)

`pinread_` (v55:2467-2473; v51:2409-2415): picks `ina` or `inb` from bit 5 of the pin argument, rotates the pin to bit 0 (`ror a,x`), then `shr x,#6` leaves the extra pin count and `zerox a,x` keeps count+1 bits. For a single pin the extra count is 0, so `zerox a,#0` keeps one bit: the result is 0 or 1. It is never -1 (`$FFFFFFFF`). A pin range with ADDPINS n returns an (n+1)-bit value, zero-extended. v51 does not differ.
**S-061 answered by the interpreter**, v55:2467-2473.

### 4.2 AND/OR (`&&`, `||`) operators evaluate both operands (S-094, partial)

`bc_logand` (v55:1043, v51:1018) and `bc_logor` (v55:1045, v51:1020) are `log_mod` bytecodes. `log_mod` (v55:295-310) turns the value in x into a boolean (`mov w,x wz` / `muxnz w,_FFFFFFFF`), pops the second operand (`popa x wz` / `muxnz x,_FFFFFFFF`), then does `and x,w` (&&) or `or x,w` (||). The result is `$FFFFFFFF` (true) or 0, never 1. The operator itself has no jump; both operands are already on the stack when it runs.
Short-circuiting would have to be done by the compiler with a branch around the right operand. Branch bytecodes exist (`jz`/`jnz`/`tjz`/`djnz`, v55:835-845), but the interpreter does not show whether the compiler uses them for `&&`/`||`. **S-094: the interpreter settles the operator's value semantics (non-short-circuit, -1/0 result) but not whether the right operand is skipped.** That part stays open (§5).

### 4.3 BYTEMOVE/WORDMOVE/LONGMOVE overlap handling (S-038)

The three share the routine `bytefill_` (`bc_bytemove word @bytefill_` v55:87, wordmove :91, longmove :95; v51:78, :82, :86). For MOVE the code compares source and destination addresses unsigned and picks the direction: `cmp ptrb,ptra wc` (ptrb = src, ptra = dst), `if_nz_and_nc jmp #move_fwd` (src >= dst), `if_nz_and_c jmp #move_rev` (src < dst), v55:2183-2187 (v51:2127 for the `cmp`). `move_rev` (v55:2220-2239) starts from the ends (`add ptrb,x` / `add ptra,x`) and walks downward; `move_fwd` (v55:2201-2217) walks upward in blocks of up to 16 longs, reading the block before writing it.
So the direction is chosen automatically from address order, the construction that makes overlapping moves safe in either direction. **S-038: answered by the interpreter**: the copy direction is automatic (src >= dst forward, else backward). The fill case (`FILL`) uses the same forward walk. I read this by inspection and did not run it.

### 4.4 REPEAT FROM/TO/STEP direction (S-099, S-263)

`repvari` (v55:345-356; v51:332): pops the terminal and delta; `cmps y,x wc` compares terminal (y) with initial (x); `abs z` takes the absolute value of the STEP; `if_c neg z` negates it when terminal < initial. So the direction comes from FROM/TO; **the sign of STEP is discarded** (`abs`). `repvari1` pushes a step of 1 for the no-STEP form (v55:343). Direction is then fixed in the delta, and `repvarl` (v55:366-381; v51:353) adds the delta each iteration and tests `testb c,#31` (sign of delta) with `cmps` against the terminal, looping while not past it. The terminal is inclusive.
- `REPEAT idx FROM 99 TO 0 STEP -1` (S-263): terminal < initial, delta = -|step| = -1. Counts down; same as `STEP 1`.
- `FROM 10 TO 0 STEP 1` (S-099): delta = -1, counts down 10..0. It is not a zero-iteration loop at the interpreter level. The init bytecode (`repvari`) contains no test that skips the body; the body is reached once and `repvarl` is run at the end of each pass.
- `REPEAT n WITH i` (`repvarin`, v55:322, "0..n-1", followed by `repvari1`): the history text (spin2-v55-text.txt:32) says it needs n > 0, consistent with no pre-test.
- Caveat: a compiler-emitted pre-test before the init bytecode is not visible here; the interpreter only shows there is none inside the routines. These routines are unchanged v51 -> v55.
**S-099 and S-263: answered by the interpreter** (STEP sign ignored; direction from FROM/TO; no skip inside the init), with the compiler caveat above.

### 4.5 GETRND

`bc_getrnd` -> `pushv` family; `_ret_ getrnd x` (v55:1121, v51:1090): pushes the P2 `GETRND` instruction's full 32-bit result. No range reduction or masking in the interpreter. Unchanged.

### 4.6 Task halt bits `taskhlt` (S-156)

`taskhlt res 1` (v55:430, v51:417) is declared after `reg_end` in the cog-register section, among the interpreter registers (v55:428-446), not in the LUT section (the LUT code is `org $210`, v55:498). By count, 11 registers (`v` ... `z`, v55:435-446; `ma res 0` takes none) separate it from the PASM registers that the source places at `$1D8` (v55:451 "pasm-use registers at $1D8"), so `taskhlt` is at `$1CC`. That address is derived by counting, not stated in the source.
- The task pointer list is `taskptr res $20` at `org $100` (v55:161-163), separate from `taskhlt`.
- Bit order: `taskid_` returns `not tasknum & $1F` (v55:2995-2997) and `taskctrl_` takes `y = ~task & $1F` (v55:2959-2960), so halt bit n belongs to task ID 31-n ("reverse order", matching the doc, spin2-v55-text.txt:39 and :149).
- Writes: `taskhlt` bit is cleared on a new task (`bitl taskhlt,tasknum` v55:2947), set/cleared by TASKHALT/TASKCONT (`bitc taskhlt,y` v55:2972), read by TASKCHK (v55:2977), and masked by the switcher (`andn x,taskhlt` v55:3013); with all tasks halted the switcher waits (`tjz x,#tasknextw` v55:3014).
**S-156: answered by the interpreter** (an interpreter cog register, not LUT / not `$200`); `$1CC` is derived.

### 4.7 STRCOPY Max (S-031)

`strcopy_buff` (v55:2310-2318; v51:2252): `w` = Max. The loop reads a byte (`rfbyte y wz`), writes it (`wrbyte y,ptrb++`) and `if_nz djnf w,#.loop` repeats while the byte was nonzero and w has not wrapped to -1. After the loop `_ret_ wrbyte #0,--ptrb` rewrites the last byte written with 0.
- A string longer than Max: Max+1 bytes are read and written (w goes Max -> -1), then the last one is overwritten by 0. Result: Max characters + terminator = Max+1 bytes.
- A shorter string: the terminator is copied by the loop (z=1 ends it), then rewritten with 0.
- Max = 0 gives one byte, a lone 0.
`DJNF` is "decrement, jump if the result is not $FFFF_FFFF" (P2KB `p2kbPasm2Djnf`).
**S-031: answered by the interpreter.** Max is the maximum number of characters; the destination needs Max+1 bytes. Unchanged v51 -> v55.

### 4.8 RECV/SEND inheritance and method-pointer calls (S-033; related S-017)

- `mrecv` and `msend` are cog registers (v55:439-440) saved in every call frame ("drop anchor": `ptr[+4] <-- mrecv`, `ptr[+5] <-- msend`, v55:675-676, pushed by `setq #6-1` at v55:685) and restored on return (`ptra[-3] --> mrecv`, `ptra[-2] --> msend`, v55:1397-1398, popped at v55:1413). They are not changed by a call, so a callee sees the caller's values; any change the callee makes is undone by its return. A cog launch clears them (`setq #ptra-1 ... rdlong 0,ptrb` "clear reg 0..ptra-1 (cancels mrecv/msend)", v55:2038-2039): a new cog starts with none.
- `callsendh` (v55:1537-1544): if `msend` is 0 the SEND is dropped (`tjz msend,#resumeh`); otherwise it calls the method pointer in `msend` (`mov x,msend` then `callptrh`). `callrecvh` (v55:1528-1534): if `mrecv` is 0, RECV() leaves 0 on the stack (`mov x,mrecv`, `resumeh`); otherwise it calls it. Neither copies the pointer into a LONG variable. `call RECV()` / `call SEND(x)` / `call SEND(bytes...)` are bytecodes `'0C`/`'0D`/`'0E` (v55:885-887).
- `callptr`/`callptrh` (v55:708, 1546-1551): the method pointer is a value whose low bits are the vbase and bits [31:20] the method index; `callptrh` sets vbase to it, reads pbase from it, and takes the index from bits [31:20].
- The result count of any call is read from the callee's own header: `calloffh` (v55:1570-1578) merges the callee's params/results into the return word `pb` (`and v,##$7FF00000` / `or pb,v`), and `returnh` takes the return-value count from it (`getnib z,w,#5` v55:1421). `bc_call_ptr` (v55:884) carries no operand. For S-017 this means the interpreter takes the result count from the callee, not the call site; whether the compiler needs `:1` at the call site is compile-time (§5).
**S-033: answered by the interpreter on the mechanism** (registers `mrecv`/`msend` hold method pointers, called through the pointer-call path, inherited by callees, not by a new cog). The *assignment* `SEND := @method` is compiled to a register write whose bytecodes this source does not show.

### 4.9 Summary: which study rows the interpreter answers

| Row | Answered | By |
|-----|----------|----|
| S-038 | Yes (direction automatic) | §4.3, v55:2183-2187 |
| S-061 | Yes (0/1) | §4.1, v55:2467-2473 |
| S-094 | Partly (value semantics yes; short-circuit no) | §4.2, v55:295-310, :1043-1045 |
| S-099 | Yes, with compiler caveat | §4.4, v55:345-356, :366-381 |
| S-031 | Yes (Max chars, Max+1 bytes) | §4.7, v55:2310-2318 |
| S-033 | Yes on the mechanism; assignment syntax is compile-time | §4.8, v55:439-440, :675-685, :1528-1546 |
| S-156 | Yes (interpreter cog register; `$1CC` derived) | §4.6, v55:430 |
| S-263 (related) | Yes, with S-099 | §4.4 |
| S-017 (related) | Result count comes from the callee; call-site syntax not settled | §4.8 |

The study document's own rows were not edited.

---

## 5. Not determinable from this source

1. Whether `&&` / `||` skip the right operand: that is a compiler decision (§4.2). Needs the compiler source (PNut / PNut-TS) or a bench test.
2. Whether the compiler emits a pre-test before a `REPEAT ... FROM ... TO` loop (§4.4). Only the absence of one inside the interpreter's init and loop routines is shown.
3. The syntax of `SEND := @method` as compiled, and whether `data := inputMethod()` without a `:1` result count is accepted or changes the stack (S-017): compile-time.
4. Which of v52, v53, v54, v55 introduced each §2.4/§2.5 change, since no v52-v54 interpreter is held. The changes that I assigned to v55 are assigned by matching the history text, not by version stamps.
5. Whether the LOOKUP/LOOKDOWN/CASE range rewrite (§2.5 item 2) changed observable behaviour. The code was restructured; I did not trace equivalence.
6. `taskhlt` address `$1CC` is derived by counting reservations (§4.6), not stated in the source or checked by assembling it.
7. The debugger for v55: this file does not contain it. The arbiter established (not re-checked here) that PNut-TS v1.55.8 embeds the v51 debugger image, so no newer debugger source exists in the distribution.

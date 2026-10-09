# Rows S-111..S-161 — change specs («#407», 2026-10-09)

Read-only research; nothing under `deliverables/ai/P2/`, `engineering/ingestion/`, the study or the register
was edited. Abbreviations: v55 = `sources/spin2-v55/spin2-v55-text.txt`, SD = `sources/silicon-doc/silicon-doc-text.txt`,
DS = `sources/p2-datasheet/p2-datasheet-text.txt`, INT = `external-inputs/source-code/spin-interpreter/v55/Spin2_interpreter.spin2`
(the study's "v51:417" for `taskhlt res 1` is **INT:430** in the v55 file), DBG = `external-inputs/source-code/spin-debugger/v51/Spin2_debugger.spin2`,
F547 = `f547-operator-cascade-specs.md` (item numbers `#n`), G1 = `rows-S001-S040-specs.md`, G2G3 = `rows-S041-S110-specs.md`.
Paths are under `deliverables/ai/P2/` unless a root is given. Line numbers are those of the files as read 2026-10-09.

**"compiled"** = the corrected text compiled with `pnut-ts` v1.55.8 (`-q`; `-d` for DEBUG code) in the scratch tree
`/tmp/claude-1000/-workspaces-P2-Knowledge-Base/fd20d1c1-e1ec-45fc-a5bc-7f395c46f9e1/scratchpad/s161/` (probe sources
`probes1.py`..`probes10.py`, driver `run.py`, comparer `cmp.py`, tally `tally.py`, sweeps `param_index_sweep.py`, `ptr_sweep.py`,
`designator_sweep.py`). Probe names are given in parentheses, e.g. `(a111_with_ok)`. Wherever an error message is quoted, the "bad" form
was compiled too and produced it. **"compile in sprint"** marks text not compiled here. **"bytes identical"** = the two compiled `.bin`
files are byte-for-byte equal (`cmp.py`), which proves two spellings are the same program. Where a compile proves only legality, the semantic
authority is named separately.

**States.** Change spec — every row S-111..S-161 except: S-123, S-136, S-150 (tooling, **RESOLVED** earlier — one line each),
S-147 (**undetermined**, punch list — one line), S-127 (answered by S-336; spec given for the pages the row names). **One bench question,
VO-S157** (S-157; no pins; a PNut-side compile + DEBUG read). No row needed reclassification beyond the three tooling rows the study
already holds. S-153 / S-090 / S-046 / S-174 are one gating class — the sweep is done once, under S-153. Siblings found by the class sweeps are
listed under each row; those that belong to other study groups are marked *(sibling, group Gn)* — they belong to the same edit.

**Two corrections to settled work that this pass found (details under New findings):** NF-1 (`INA[pin]`/`OUTA[pin]` is a register index,
not a pin bit — G2G3's S-261/S-002 spec keeps `if INA[BUTTON]`, and S-143's own "Spin2 is `!= OUTA[pin]`" is also a register index) and
NF-2 (the typed-pointer page is inverted in every operation, not only the 2 gated blocks).

---

## G4 rows (`language/spin2/keywords/`, `operators/`, `special-symbols/`, `symbols/`, + top-up)

## S-111 `keywords/WITH.yaml` — `WITH object` is not a statement
Sites: `:4-5` (description "Object context specifier for method calls"), `:6` (`syntax: "WITH object"`), `:9-10` (example `WITH serial` / `  str("Hello World")`).
Correct — whole file (compiled `(a111_with_ok)`; calling a child's method compiled `(a111_obj_ok)`):
```
keyword: "WITH"
type: keyword
category: "Control Flow"
description: |
  Part of the REPEAT count form (v40): REPEAT positive_count WITH variable repeats the indented code
  positive_count times while the variable iterates from 0 to positive_count - 1. positive_count must be
  greater than zero. WITH has no other use: it is not a statement and not an object-context specifier.
  A child object's method is called as object_name.method_name(...), one call per statement.
syntax: "REPEAT positive_count WITH variable"
examples:
  - |
    REPEAT 10 WITH i           ' i = 0, 1, ..., 9
      indices[i] := i
```
Bad forms: `WITH serial` → `Expected an instruction or variable` (block line 2 of the probe) `(a111_bad)`; `serial.str("Hello World")` is rejected too — a quoted multi-character literal is not a string value, use `@"Hello World"` (S-014; G1).
Authority: v55:32 (v40: "REPEAT n WITH i 'best way to iterate a variable from 0 to n - 1 … WITH needs n > 0"), :758 (`REPEAT <positive_count> WITH <variable>` — the only WITH in the document), :233-236 (`object_name.method_name(…)`).
Sweep: `\bWITH\b` over `deliverables/ai/P2` — the only other Spin2 hit is `constructs/repeat.yaml:77-90` (`count_with_var`, correct); all other hits are English prose. See NF-3 (`keywords/REPEAT.yaml` omits the WITH form).

## S-112 `keywords/ELSE.yaml`, `ELSEIF.yaml`, `ELSEIFNOT.yaml` — the clause alone is not a program
Sites: `ELSE.yaml:11-12`, `ELSEIF.yaml:11-12`, `ELSEIFNOT.yaml:11-12` (each the only `examples:` entry).
Correct — replace each example by a whole decision tree (all compiled):
```
# ELSE.yaml                                  (a112_else_ok)
examples:
  - |
    IF a
      result := 1
    ELSE
      result := 0

# ELSEIF.yaml                                (a112_elseif_ok)
examples:
  - |
    IF x > 100
      result := @"very high"
    ELSEIF x > 10
      result := @"high"

# ELSEIFNOT.yaml                             (a112_elseifnot_ok)
examples:
  - |
    IF flag
      result := @"true case"
    ELSEIFNOT second
      result := @"false case"
```
and add to each `description:` "Must have the same indentation as the IF/IFNOT that begins the decision tree." The old ELSEIF/ELSEIFNOT examples also assign `"high"` / `"false case"`: a quoted multi-character literal is not a string value (`Expected end of line (m281)`, `(a112_elseif_strlit_bad)`) — the `@"…"` form is the string address (S-014).
Bad: a lone `ELSE` / `ELSEIF x > 10` → `Expected an instruction or variable` `(a112_else_bad)`.
Authority: v55:729-736 (IF / IFNOT with optional ELSEIF / ELSEIFNOT / ELSE; "these keywords must have the same level of indentation").
Sweep: `keywords/IF.yaml`, `IFNOT.yaml` carry whole-tree-compatible heads; no other keyword page's example is a clause alone (`OTHER.yaml`, `CASE_FAST.yaml` are whole CASE bodies).

## S-113 `operators/op_or.yaml:7`, `op_oror.yaml:7` — `abort()` is not a call
Current: `"IF error OR timeout\n  abort()"` · `"IF error || timeout\n  abort()"`.
Correct: `"IF error OR timeout\n  ABORT"` · `"IF error || timeout\n  ABORT -1"` (compiled `(a113_or_ok, a113_oror_ok)`). The `||` form itself is the legal logical OR.
Bad: `abort()` → `Expected an expression term (m172)` `(a113_call_bad)`.
Authority: v55:624 (`ABORT`), :633 (`ABORT ErrorCode`), :636 ("If no value is specified after ABORT, then zero will be returned").
Sweep: `\babort\(` over the tree — only these two lines.

## S-114 `operators/typed-pointers.yaml` — the pointer/pointee roles are inverted
**What the compiler does (bytes identical, probes2):** for `^BYTE ptr` and an ordinary long `p` in the same slot — `x := ptr` ≡ `x := BYTE[p]`; `ptr := $FF` ≡ `BYTE[p] := $FF`; `ptr := @buffer` ≡ `BYTE[p] := @buffer` (the address is written **into the pointed-to byte**, the pointer does not move); `ptr++` ≡ `BYTE[p]++` (increments the pointed-to byte); `ptr[++] := 0` ≡ `BYTE[p++] := 0`; `[ptr] := @buffer` ≡ `p := @buffer`; `[ptr]++` ≡ `p++`; `[ptr]` as a term ≡ `p`; `BYTE[ptr++] := 0` ≡ `BYTE[BYTE[p]++] := 0` `(p_t_read…p_t_bytebr vs p_u_*)`. A result declared `^BYTE p`: `return @buf` ≡ the untyped `return @buf`, and `[p] := @buf` ≡ the untyped `p := @buf`; `p := @buf` is the different (pointee-write) program `(r_return, r_bracket, r_plain, r_untyped_*)`.
**Authority:** v55:249-261 (`ptrvar` = "the pointed-to-variable"; `[ptrvar]` = "the pointer, itself"; `[ptrvar] := @regvar` "point the pointer"; `[ptrvar]++` "post-inc the pointer"; `ptrvar[++]` "read/modify/write the pointed-to-variable, post-inc the pointer"; `@ptrvar` = "the address of the pointed-to variable, equals the pointer variable"), :244-247 (stepping sizes), v45 entry :37 (same list). The interpreter has no typed-pointer bytecode (INT, grep `pointer`) — the compiler lowers pointers to ordinary memory bytecodes, which is what the byte-identity shows.
Sites and corrections (file `operators/typed-pointers.yaml`; every corrected block compiled):
- `:15-22` description — append: "A pointer variable named alone is the variable it points to; `[ptr]` is the pointer itself (v55:248-261)."
- `:53-62` example 2 → (`b114_ex2_local`)
```
      {Spin2_v45}
      VAR
        BYTE  buffer[256]

      PUB example() | ^BYTE ptr
        [ptr] := @buffer          ' Point the pointer at buffer
        ptr := $FF                ' Write through the pointer: buffer[0] := $FF
        [ptr]++                   ' Advance the pointer by 1 byte
    description: "Local pointer: [ptr] := @buffer points it, ptr reads/writes the pointed-to byte, [ptr]++ steps the pointer"
```
- `:64-69` example 3 (also S-049's `LONG length`) → (`b114_ex3_param`; original `b114_ex3_orig_bad` fails `Expected a unique parameter name (m220)`)
```
      {Spin2_v45}
      PUB processBuffer(^BYTE pBuffer, length)
        repeat length
          pBuffer[++] := 0        ' Clear the pointed-to byte, then advance the pointer
```
- `:71-78` example 4 → `PUB getValues() : ^LONG pValues` / `return @values` (`b114_ex4_return`; the original `: ^LONG result` / `result := @values` compiles `(b114_ex4_orig)` but stores the address into the first pointed-to long).
- `:80-93` example 5 → (`b114_ex5_struct`; original fails `Expected ","` `(b114_ex5_orig_bad)`)
```
      {Spin2_v45}
      CON
        STRUCT point(x, y)

      VAR
        point points[10]
        ^point ptr

      PUB example()
        [ptr] := @points[0]       ' Point at the first structure
        ptr.x := 100              ' Member access through the pointer
        [ptr]++                   ' Advance by 8 bytes (size of point)
```
- `:95-153` `operations:` (all lines compiled together in `b114_ops_all`):
```
  address_of:        syntax: "[ptr] := @variable"   description: "Point the pointer at a variable, array element, or structure member"
  read_through_pointer:  syntax: "value := ptr"      description: "Read the pointed-to variable (the pointer's type sets its size)"
  write_through_pointer: syntax: "ptr := value"      description: "Write the pointed-to variable"
  indexed_access:    syntax: "value := ptr[index]"   description: "Element at an index from the pointed-to variable (array syntax)"
  pointer_increment: syntax: "[ptr]++"   description: "Advance the pointer by the element size"      (decrement: "[ptr]--")
  pre_increment:     syntax: "[++]ptr"   description: "Advance the pointer first, then read/modify/write the pointed-to variable"   ("[--]ptr" likewise)
  post_increment:    syntax: "ptr[++]"   description: "Read/modify/write the pointed-to variable, then advance the pointer"           ("ptr[--]" likewise)
  struct_member_access:  syntax: "ptr.member"        (unchanged)
  struct_whole:      syntax: "ptr"       description: "The pointed-to structure as a whole: temp := ptr copies it out, ptr := temp copies one in. [ptr] is the pointer"
  modify_assign_through_pointer: syntax: "ptr += value / ptr |= mask / etc."   operators: "ptr += v", "ptr -= v", "ptr *= v", "ptr |= mask", "ptr &= mask", "ptr ^= mask"
  pointed_value_modification: syntax: "ptr++ / ptr-- / ptr~ / ptr~~"   description: "Modify the pointed-to variable (increment, decrement, clear, set all bits)"
  pointer_value_modification: syntax: "[ptr]++ / [ptr]-- / [ptr]~ / [ptr]~~"   description: "Modify the POINTER itself ([ptr]~ nulls it, [ptr]~~ sets it to -1)"
```
  (delete `bracket_post_increment` / `bracket_pre_increment` — their "Return current address" wording is wrong: the bracket-side form returns the pointed-to variable — and `struct_dereference`'s "[ptr] reads the structure" — `[ptr]` is the pointer.)
- `:164-172` `pointer_arithmetic` keys `"ptr++"` → `"[ptr]++"` (all four).
- `:175-179` `array_traversal` → `[ptr] := @buffer` / `repeat 256` / `ptr[++] := 0` (`b114_array_traversal`).
- `:181-185` `string_length` → `repeat while pStr[++] <> 0` (`b114_string_length`); `:187-191` `string_copy` → `repeat while pSrc <> 0` / `pDest[++] := pSrc[++]` / `pDest := 0` (`b114_string_copy`).
- `:193-199` `structure_array` → `[ptr] := @points` … `[ptr]++` with `CON STRUCT point(x, y)` / `VAR point points[100]` declared (`b114_structure_array`; this also lifts the block's S-123 harness note).
- `:201-210` `linked_list` (with S-115) → (`b115_linked_list`)
```
    CON
      STRUCT node(nxt, data)       ' nxt holds the address of the next node (a plain long member)
    VAR
      ^node head
    PUB traverseList() | ^node current
      [current] := [head]
      repeat while [current] <> 0
        processNode([current])
        [current] := current.nxt
```
- `:212-219` and `:246-251` `ptr := ptrTable[0]` → `[ptr] := ptrTable[0]` (`b114_table_workaround`).
- `:259-262` notes — `:261` → `"[ptr]++ advances the POINTER; ptr++ increments the pointed-to variable"`; `:262` → `"ptr += v modifies the pointed-to variable in place"`.
Sweep: `ptr_sweep.py` (declared pointer names × `:=` / `++` / `BYTE[name`) over every YAML in the tree → hits only in this file (every example, operation, pattern and note line listed above) plus `keywords/STRUCT.yaml:343` (`pCfg := sensor.getConfig()` as the deliberately *wrong* form — correct as it stands). `BYTE/WORD/LONG.yaml` and `method_definition.yaml` mention pointers only in declarations (right).

## S-115 `typed-pointers.yaml:201-210` — self-pointing STRUCT member
Current: `STRUCT node(^node next, data)`. A STRUCT member is BYTE/WORD/LONG/substructure plus a name; `^node` as a member → `Expected ")" (m301)` `(b115_self_bad)`; `next` is also the reserved word NEXT (S-008). Correct: see S-114 `linked_list` (`STRUCT node(nxt, data)`, `[current] := current.nxt`; compiled `b115_linked_list`).
Authority: v55:205 (`STRUCT structname(BYTE|WORD|LONG|substructname membername{[arraysize]}, …)` — no pointer member). Sweep: `STRUCT … \^` over the tree — this line only.

## S-116 `special-symbols/at.yaml:192-196` — pointer result needs a name
Current: `PUB getData() : ^BYTE` / `return @buffer`. Correct (compiled `(b116_getdata_ok)`): `PUB getData() : ^BYTE pData` / `return @buffer`. Bad: `: ^BYTE` alone → `Expected a unique result name (m230)` `(b116_getdata_bad)`. `return @buffer` is right for a pointer result (bytes identical to the untyped `return @buf`, `r_return == r_untyped_return`).
Authority: v55:278, :288 (`{: {^BYTE|^WORD|^LONG|^StructName} Result{, …}}` — the override precedes a result *name*). Sweep: `:\s*\^TYPE\s*$` over the tree — this line only; `guides/spin2-getting-started.yaml:180` and `constructs/method_definition.yaml:181` (`: ^BYTE result`) are already right.

## S-117 `special-symbols/caret_at.yaml:112-127` — a CON constant is one integer
Current: `READY_BITS  = 3..1` / `MODE_BITS   = 7..4` then `^@status_reg.[MODE_BITS]`. Correct (compiled `(a117_ok_addbits)`):
```
      CON
        ERROR_BIT   = 0
        READY_BITS  = 1 ADDBITS 2      ' bits 3..1 (base bit 1, 2 more above it)
        MODE_BITS   = 4 ADDBITS 3      ' bits 7..4
```
(the rest of the example unchanged). The two ADDBITS constants and the literal `.[7..4]` / `.[3..1]` forms compile to **identical bytes** `(a117_ok_addbits == a117_ok_literal)`. Bad: `READY_BITS = 3..1` → `Expected "," or end of line` `(a117_bad)`.
Authority: v55:380 (`CON BitfieldCon = 9 ADDBITS 4 'BitfieldCon useful in PASM, too` → `.[BitfieldCon]` = 13..9), :470 (ADDBITS definition). (The scratch suggestion `MODE_BITS = 7 ADDBITS 3` in the group's sidecar selects bits 10..7, not 7..4 — do not use it.)
Sweep: `NAME = a..b` in CON over the tree — these two lines only.

## S-118 `special-symbols/double_at.yaml` — method addresses cannot be stored with `@` in DAT
Sites: `:78-86` (dispatch example `handler0 LONG @process_type_a`, `CALL(handler_addr)`), `:125-141` (state machine, `stateHandlers LONG @State0, @State1, @State2`).
Current error: `Expected a DAT symbol` at `@State0` `(a118_dat_methods_bad)` — `@name` in DAT takes DAT symbols; a method pointer is `@MethodName` in PUB/PRI code. The `:78-86` block passes the gate only because the harness declares `process_type_a/b` as DAT symbols; `CALL()` takes a PASM address, not a method pointer.
Correct — `:125-141` state machine (compiled `(a118_statemachine_ok)`):
```
      VAR
        LONG stateHandlers[3]
        LONG currentHandler

      PUB Init()
        stateHandlers[0] := @State0       ' @Method in code is a method pointer - no @@ needed
        stateHandlers[1] := @State1
        stateHandlers[2] := @State2
        currentHandler := stateHandlers[0]

      PUB Run()
        currentHandler()                  ' Call through the pointer

      PRI State0()
        currentHandler := stateHandlers[1]    ' Transition to state 1
      PRI State1()
        currentHandler := stateHandlers[2]
      PRI State2()
        currentHandler := stateHandlers[0]
    description: "Method-pointer state machine: @Method in PUB/PRI code (no @@ - these are not stored offsets)"
```
and `:78-86` dispatch → PASM routine entry points, which *are* DAT symbols (compiled `(a118_dispatch_ok)`):
```
      DAT
              orgh
      process_type_a
              _ret_   mov     pa, #1
      process_type_b
              _ret_   mov     pa, #2
      handlers  LONG  @process_type_a, @process_type_b  ' stored as object-relative offsets

      PUB dispatch(type) | handler_addr
        handler_addr := @@handlers[type]          ' absolute hub address of the routine
        CALL(handler_addr)                        ' run it
```
Authority: v55:642-648 (method pointers: "assign a long variable using `@` before the method name"), :300-308 (`@@SymbolName` converts an `@Symbol` stored in DAT data), :820-821 (`CALL(address)` runs PASM in cog registers or hub RAM; the example there uses a DAT `ORGH` routine).
Sweep: `(LONG|WORD)\s+@name` in DAT over the tree — the only method-valued entries are `double_at.yaml:80-81`, `:127`; all other `@` tables point at DAT data (right).

## S-119 `special-symbols/double_dollar.yaml` — `$$` is the DITTO index, not the current address
Sites: `:5-14` (description "1. PASM2 CONTEXT: Current cog address…"), `:16-21` (`contexts.pasm2_address`), `:32-58` (examples 1-3: `jmp #$$`, `entry0 + ($$ - entry0)`, `mov pa, #$$ + 3`), `:102-103`, `:106-107` (notes), `:123` (oneliner).
Compiler: outside a DITTO block `$$` → `"$$" (DITTO index) is only allowed within a DITTO block, inside a DAT block` `(a119_bad_self)`.
Correct:
- description → "`$$` is the DITTO iteration index (v50): inside a DITTO … DITTO END block it iterates from 0 to count - 1. Outside a DITTO block it is an error. It is NOT the current address — the current origin is the single `$` symbol."
- delete `contexts.pasm2_address`; examples 1-3 use `$` (compiled): `jmp #$` `(a119_self)`; `mov pa, #$ - entry0 ' register distance from entry0` `(a119_rel)`; `start mov pa, #$ + 3 ' pa = register address of this instruction + 3` `(a119_fwd)`.
- notes `:102-103` → delete; `:106` ("Context determines meaning…") → delete; `:107` → `"$ is the current origin: the cog register address in cog-exec (ORG) code, stepping by 1 per instruction, or the hub address in hub-exec (ORGH) code, stepping by 4 (v55:312, :321)"`.
- oneliner → `"DITTO iteration index (v50+); not the current address ($)"`.
- DITTO examples 4-6 compile as written except the `reg` label (S-008): rename `reg` → `regs` and declare `regs res 4` (`mov regs + $$, #0`, `(a119_ditto_regs)`; bad `reg + $$` → `Expected a constant, unary operator, or "("` `(a119_ditto_regs_bad_reg)`).
Authority: v55:312 (`JMP #$ '$ is the current origin, which steps by 1 with each cog-exec instruction`), :321 (steps by 4 in hub-exec), :42 (v50: "A special index variable '$$' is available within the block, which iterates from 0 to count - 1"; "To branch within the block, use $ (origin)").
Sweep: `\$\$` over the tree — `special-symbols/double_dollar.yaml` (this row), `assembly-directives/ditto.yaml` and `pasm2/ditto.yaml` (right: index), `spin2-language-complete-map.yaml:109` (name list), and **`pasm2/concepts/labels.yaml:124-128`** *(sibling, group G8)*: `current_hub_address: syntax "$$"` / `meaning "Current Hub address"` / `example "LONG $$ + 4 ' Address of next long"` — same invented meaning; → delete the entry and let `current_cog_address` (`:118-122`) read `syntax "$"`, `meaning "Current origin: cog address in ORG mode, hub address in ORGH mode"`; the example `LONG $ + 4` compiles in ORGH `(nf_labels_dollar_hub)`. See NF-4 for `special-symbols/dollar.yaml` (omits this meaning of `$`).

## S-120 `double_dollar.yaml:92-99` — no `sin()` in constant expressions
Current: `long    round(sin(float($$) * PI / 30.0) * 65535.0)` → `Expected ")" (m301)` `(a120_sin_bad)`.
Correct: replace the example by a table the DITTO block *can* generate (compiled `(a120_squares)`), and say where a sine table comes from:
```
      {Spin2_v50}
      DAT
              org
              DITTO 16
              long    $$ * $$                    ' Generates: 0, 1, 4, 9, ... 225
              DITTO END
    description: "V50+ DITTO: $$ in constant expressions for lookup tables"
```
plus a note: "Constant expressions have FLOAT(), ROUND() and TRUNC() and the float operators but no trigonometric functions; build a sine table at run time with QSIN()" — `table[i] := qsin(65535, i, 64)` for i = 0..15 compiles `(a120_qsin_runtime)`.
Authority: v55:499-501 (the complete float-conversion list), :564 (`QSIN(length, step, stepsInCircle) : y`). Sweep: `sin(` in code over the tree — this line only. **Decision D2** (squares vs delete).

## S-121 prefix `~`/`~~` and `//` as a comment (the P1 carry-over class)
Sites: `special-symbols/~.yaml:7`, `~~.yaml:7` (prefix `~flag` / `~~flag`, `//` comment); and the `//`-comment lines — G5-found: `assembly-directives/fit.yaml:8`, `org.yaml:8`, `orgf.yaml:8`, `res.yaml:8`, `registers/dira.yaml:7`, `registers/dirb.yaml:7`.
Correct:
```
# ~.yaml
description: |
  Post-clear operator (postfix): var~ returns var, then clears all bits of var
examples:
  - "value := flag~  ' use flag, then clear it"
# ~~.yaml
description: |
  Post-set operator (postfix): var~~ returns var, then sets all bits of var (-1)
examples:
  - "value := flag~~  ' use flag, then set it to -1"
```
(compiled `(a121_tilde_ok, a121_tilde2_ok)`). Bad: `~flag` → `Expected an expression term (m172)` `(a121_tilde_bad)`; `value := flag~  // …` → the same error — `//` is the signed-remainder operator `(a121_tilde_comment_bad)`.
`//` → `'` on the six directive/register lines: `FIT $1F0  ' Must fit in cog space` · `ORG 0  ' Start at cog address 0` · `RES 16  ' Reserve 16 registers` · `DIRA := %11111111  ' Set pins 0-7 as outputs` · `DIRB := $FF000000  ' Set pins 56-63 as outputs` (all compiled `(a137_org_alone, a137_fit_alone, a137_res_alone, a137_dira)`); `orgf.yaml:8` → see S-161. Bad: `ORG 0  // …` → `Undefined symbol`; `DIRA := …  // …` → `Expected an expression term (m172)` `(a137_slashslash_bad, a137_dira_slash_bad)`.
Authority: v55:419-420 (`var~`, `var~~` postfix), :333 (comment = apostrophe, rest of line ignored), :459 (`//` signed remainder). F547 #30 (same fix for the `~` pages).
Sweep: prefix `~name`/`~~name` over `language/` — only these two pages (`concepts/operators.yaml:334/352` are prose that already says "postfix"). `\S\s+//\s+[A-Za-z]` over the whole tree — exactly the 8 comment sites above (`op_addmodulo.yaml:52`, `op_divdiv.yaml:4`, `method_definition.yaml:45`, `operators.yaml:188` are genuine `//` operator uses). The prefix-tilde and bare-`!` P1 forms share S-087's P1 class; the `;` comment is S-137.

## S-122 `methods/lookdown.yaml:97-104` — LOOKDOWN is a term, not a statement
Current (`ignoring_return_value`): `wrong:` `LOOKDOWN(char : "A".."Z")  ' Result discarded!` / `process_uppercase()` — not writable at all: `Expected an instruction or variable` `(a122_stmt_bad)`.
Correct — keep the lesson, make the wrong form legal (compiled `(a122_discard_ok, a122_correct)`):
```
  - anti_pattern: "ignoring_return_value"
    description: "Not testing the LOOKDOWN result. LOOKDOWN is an expression term, so it cannot stand alone as a statement; storing the result and never testing it compiles but guards nothing"
    wrong: |
      found := LOOKDOWN(char : "A".."Z")
      process_uppercase()           ' runs for every char: found is never tested
    correct: |
      if LOOKDOWN(char : "A".."Z")
        process_uppercase()
```
Authority: v55:602 (`LOOKDOWN(Value: v1, v2..v3, etc) : Index`), :623 ("built-in methods such as STRSIZE, which return results, can only be used as expression terms").
Sweep: a built-in result method at the start of a statement line, over `language/` — this line only.

## S-123 — RESOLVED (assume kinds `struct:`, `OBJ.struct:`, `NAME:TYPE`, `OBJ.m(N)->T`; NC19a/b). Nothing to do. The `typed-pointers.yaml:193` block now fails only on its S-114 defect — fixed by the S-114 `structure_array` text above.

## S-124 `keywords/STRING.yaml` — STRING() converts nothing
Current: `description: Convert expression to string representation`, `syntax: "STRING(expression)"`, `examples: "text := STRING(number)"` (passes the gate only because `number` is declared a DAT symbol). Correct (compiled `(a124_string_ok)`):
```
description: |
  Compose a zero-terminated string in the object image from quoted characters and values 1..255, and return its address. STRING() converts nothing at run time: every argument must be a constant.
syntax: 'STRING("Text", 13)'
examples:
  - "text := STRING(\"Hello\", 13)   ' address of the zero-terminated string"
```
Bad: `STRING(number)` with a runtime variable → `Expected a constant, unary operator, or "("` `(a124_string_var_bad)`.
Authority: v55:592 (`STRING("Text",13) : StringAddress — Compose a zero-terminated string (quoted characters and values 1..255), return address of string`). `methods/string.yaml` already says this (its `:39` escape claim and `:41` "read-only" are S-032/S-067).
Sweep: `STRING(` + identifier over the tree and "convert … to string" wording over `language/` — `keywords/STRING.yaml` only.

## S-125 `keywords/LOOKUP.yaml:8`, `LOOKDOWN.yaml:8` — a quoted string in a list is characters
Current: `day_name := LOOKUP(day : "Sun", "Mon", "Tue")` · `index := LOOKDOWN(day : "Mon", "Tue", "Wed")`. The first list is a **nine-entry list of characters**: `LOOKUP(day : "Sun", "Mon", "Tue")` and `LOOKUP(day : "S","u","n","M","o","n","T","u","e")` compile to identical bytes `(a125_lookup_chars == a125_lookup_nine)`.
Correct (compiled `(a125_lookup_ptr_ok, a125_lookdown_ptr)`): `day_name := LOOKUP(day : @"Sun", @"Mon", @"Tue")` · `index := LOOKDOWN(letter : "M", "T", "W")` (LOOKDOWN matches a *value*; a day-name match needs STRCOMP or a table walk).
Authority: v55:348 (multi-character quoted text "resolve[s] to 8-bit ASCII values separated by commas"), :600-603 (lists of values and ranges). Sweep: `LOOKUP(/LOOKDOWN(` + multi-character quoted entry over the tree — these two lines; `methods/lookup.yaml`, `lookupz.yaml`, `concepts/table_lookup.yaml` already use `@"…"` entries.

## S-126 `keywords/FILE.yaml` — FILE is a DAT data directive
Current: `category: "Special"`, `description: Compiler directive for file inclusion`, `syntax: "FILE filename"`, example `FILE "config.spin2"`. Correct — whole file (compiled `(a126_file_ok)`):
```
keyword: "FILE"
type: keyword
category: "Data Declaration"
description: |
  DAT directive that includes the bytes of a binary file at that point of a DAT block. FileDat FILE "Filename":
  FileDat is a byte symbol that points to the included data. It does not include Spin2 source (source inclusion is the
  preprocessor's #INCLUDE) and it is not allowed in in-line PASM code.
syntax: 'FileDat FILE "filename"'
examples:
  - 'FileDat FILE "data.bin"   '' FileDat points to the file''s first byte'
related:
  - language/spin2/assembly-directives/file.yaml
```
Bad: `FILE "data.bin"` as a PUB statement → `Expected an instruction or variable` `(a126_file_in_pub_bad)`.
Authority: v55:304 (`FileDat FILE "Filename" 'include binary file, FileDat is a byte symbol that points to file`), :817 (FILE "not allowed within in-line PASM code"). `assembly-directives/file.yaml:1-5, :24, :37` already states this correctly (the keyword page contradicts the directive page).
Sweep: "file inclusion" / `FILE .*\.spin2` over the tree — this page only.

## S-127 `special-symbols/at.yaml` vs `double_at.yaml` — what `@` yields (answered by S-336)
Answer: **in PUB/PRI code `@x` is the hub address; the object-relative form is what `@` stores in DAT data** (`WORD @Str0`). Verified three ways: v55:311 (`COGINIT(16, @IncPins, 0)`, "@IncPins is the hub address of the 'MOV' instruction"); the compiled bytecode — `x := @label` is `4F 08 1B` = *setup byte[pbase + 8]* then *get address* (INT:972 `bc_setup_byte_pbase`, INT:529 `bc_get_addr`), i.e. pbase + offset = an absolute address, while `x := @@tbl` is `55 0B 1C 24` = read the stored word, then *add pbase* (INT:917 `bc_add_pbase`) `(at_code, atat_code listings)`. `double_at.yaml:91-92`, `:155`, `:164-165` are therefore **right**; the wrong side is `at.yaml`.
Edits — `special-symbols/at.yaml`:
- `:10-15` → "In PUB/PRI code @ gives the hub address, ready for COGINIT, BYTE[]/LONG[], BYTEMOVE … (v55:311). The object-relative form applies to @ values STORED IN DAT DATA (`WORD @Str0`, `LONG @Table`): in a Spin2+PASM program they are stored as offsets from the start of the object (v55:308), so convert them with @@ when reading them back (v55:300, :425). In a PASM-only program stored values are absolute."
- `:69-88` `address_types.relative_address` → `context: "@ values stored in DAT data in Spin2+PASM programs"`, description: "Stored as offsets from the start of the object so the object can load anywhere; convert with @@ in PUB/PRI code. `@symbol` written in PUB/PRI code is not stored — it is the hub address." `absolute_address.context` → "PASM-only programs (stored @ values)".
- `:213-214` notes → `"@ in PUB/PRI code is the hub address; an @ value stored in DAT data is object-relative in Spin2+PASM (use @@)"`; `:237` oneliner → `"Address-of operator - hub address of a VAR/DAT variable or method (an @ stored in DAT data is object-relative in Spin2+PASM; convert with @@)"`.
`special-symbols/double_at.yaml:10-12` → "an @symbol written in DAT data is stored RELATIVE to the object's base"; `:145` `spin2_pasm.description` → "@ in DAT data stores relative offsets, @@ converts to absolute". `concepts/addressing.yaml:9-11, :55, :95` is S-336 (NF-1 of G2G3).
Sweep: `RELATIVE|relative to the start of the object|object-relative` over `language/` — `at.yaml`, `double_at.yaml`, `addressing.yaml`, `idioms/memory-access.yaml` (S-107).

## S-128 `special-symbols/hash.yaml:105-112` — cog register map
Current: `$000-$11F: General purpose / user code space` · `$120-$13F: Reserved` · `$140-$1CF: LUT access window` · `$1D0-$1D7: Special hardware registers` · `$1D8-$1DF: PR0-PR7 …` · `$1E0-$1EF: Local variable window (inline PASM)` · `$1F0-$1FF: I/O and special registers`. There is no LUT window inside cog RAM (the LUT is the separate `$200-$3FF` space the page lists two lines later); `$1D0-$1D7` is not named in any source.
Correct:
```
    sections:
      - "$000-$11F: user area - in-line ORG PASM code loads here; free for your own code and data"
      - "$120-$1D7: occupied by the Spin2 interpreter - do not write (it includes the task halt bits, TASKHLT at $1CC)"
      - "$1D8-$1DF: PR0-PR7, general-purpose registers shared by PASM and Spin2"
      - "$1E0-$1EF: the executing method's first 16 long variables, under their own names (in-line PASM)"
      - "$1F0-$1FF: IJMP3 IRET3 IJMP2 IRET2 IJMP1 IRET1 PA PB PTRA PTRB DIRA DIRB OUTA OUTB INA INB"
```
Authority: v55:786 (`$000..$11F`, default limit `$120`), :800-806 ("Avoid writing to $120..$1D7 … since the Spin2 interpreter occupies these areas"; `$1D8..$1DF` PR0..PR7; `$1E0..$1EF`; `$1F0..$1FF`), :360 (register addresses); the compiler's `#TASKHLT` and the assembled interpreter both give `$1CC` (S-156). The page's other register examples (`#PR0 $1D8`, `#OUTA $1FC`, `#DIRA $1FA`, `#INB $1FF`, `#PTRA $1F8`) are right `(a128_addrs)`.
Sweep: "LUT access window" / "Special hardware registers" over the tree — this page only. `:98` `MOV reg, #$FF` uses the reserved word REG as a label (S-008 sibling — rename `regval`).

## S-129 `operators/op_ADDBITS.yaml` — ADDBITS makes a bitfield
Current: `:4` "Add bit count to pin number", `:5` `category: Pin`, `:7` `pin_range := start_pin ADDBITS bit_count`. Correct — whole file (F547 table E; compiled `(a129_addbits)`, `(a129_addbits_lit2)`):
```
operator: "ADDBITS"
type: operator
description: |
  Make a bitfield: x ADDBITS y = (x & $1F) | (y & $1F) << 5 - base bit x in bits 4..0, y additional bits above it in
  bits 9..5. Binary operator, priority 10; assign form var ADDBITS= y (priority 17, PUB/PRI only). ADDPINS is the pinfield twin.
category: Bitfield
examples:
  - "bitfield := 4 ADDBITS 3      ' = $64: base bit 4, 3 more bits above it (bits 7..4)"
  - "value := status.[4 ADDBITS 3]   ' same field as status.[7..4]"
```
`status.[4 ADDBITS 3]` and `status.[7..4]` compile to **identical bytes** `(a129_addbits_lit == a129_addbits_lit2)`.
Authority: v55:470 (`ADDBITS | x ADDBITS y | 10 | var ADDBITS= y | 17 | Make bitfield, (x & $1F) | (y & $1F) << 5`), :379-381 (`.[5 ADDBITS 7]` = 12..5). F547 #E (probe `4 ADDBITS 3` = 100).
Sweep: `ADDBITS` over the tree — `precedence.yaml:44, :66` (right), `pasm2/idioms/pin-control.yaml:65` ("works on bit fields rather than pin ranges" — right).

## S-130 `operators/op_addmodulo.yaml:48-54` — `+//` is the unsigned remainder
Current: `Performs (value % modulus) where % is unsigned modulo.` / `Equivalent to: value // modulus`. The file's own header (`:1-10`) and v55 define `//` as the SIGNED remainder and `+//` as the unsigned one. Correct:
```
operation:
  description: |
    The unsigned remainder of value divided by modulus (both operands treated as unsigned 32-bit).
    Result ranges from 0 to (modulus - 1).
    Gives the same result as value // modulus only while both operands are below $8000_0000 (// is the SIGNED remainder).
  formula: "result = value MOD modulus (unsigned)"
```
Authority: v55:459-460 (`//` "Signed divide, return remainder", `+//` "Unsigned divide, return remainder"); F547 #24-#25 (also re-point `:20-25`, `:144-149` to the v55 operator table row, and #26 for the `(head - tail) +// BUFFER_SIZE` claim). Sweep: "Equivalent to" / "value // modulus" over the tree — `:52` only (`modulo_add.yaml` is the redirect stub).

## S-131 `operators/precedence.yaml` — NOT, ternary scope, invented tokens
Current → correct (F547 #4, #6-#9; compiled evidence added here):
- `:15` `operators: ["!", "NOT", "-", "ABS", "FABS", "ENCOD", …]` → `["!", "-", "-.", "ABS", "FABS", "ENCOD", "DECOD", "BMASK", "ONES", "SQRT", "FSQRT", "QLOG", "QEXP"]` (NOT leaves level 2).
- add a level between 11 and 13: `- level: 12` / `operators: ["!!", "NOT"]` / `type: "Logical NOT"` / `note: "Unary only"`; `:7-9` comment and `:84` "Level 12 is reserved" → "Level 12 is the unary !!/NOT". Compiled: `NOT a == b` is **byte-identical** to `NOT (a == b)` (so NOT binds looser than the level-11 comparisons) and differs from `(NOT a) == b`; `!a == b` is identical to `(!a) == b` (`!` is level 2) `(a131_not_cmp, a131_not_paren_cmp, a131_paren_not_cmp, a131_bitnot_cmp, a131_bitnot_paren)`.
- `:53` `["&&", "AND", "!&&"]` → `["&&", "AND"]`; `:59` `["||", "OR", "!||"]` → `["||", "OR"]` (the `!&&`, `!||` spellings are the invented-token class, F547 #4).
- `:64` `note: "PUB/PRI only"` (ternary) → delete; `:86` → `"Assignment only in PUB/PRI; the ternary is a term in all blocks"` — a CON ternary compiles `(a131_ternary_con: CON x = 1 ? 2 : 3)`.
- `:66` level 17: add the missing assign forms per F547 #9.
Authority: v55:428 (`!!, NOT | !!x | 12`), :429 (`! | !x | 2`), :492-493 (`? : | Term (All blocks) | 16`), :489-491; F547 #6-#9.
Sweep: `PUB/PRI only` and `NOT` placements over `language/spin2/operators/` and `concepts/operators.yaml` — F547 §B/§D already list the rest (S-057).

## S-132 `operators/op_POW.yaml:28-31` — POW groups at level 8
Current: `level: 6` / `same_level: "+, -, +., -."`. Correct: `level: 8` (same list). Compiled byte-identities (POW needs `{Spin2_v51}`; without it `Expected end of line (m281)`, `(a132_pow_nodir)`): `a -. b POW c` ≡ `(a -. b) POW c`; `a POW b -. c` ≡ `(a POW b) -. c`; `a *. b POW c` ≡ `(a *. b) POW c` — POW groups left-to-right with `+ - +. -.`, tighter than the comparisons, looser than `*.` `(a132_pow_minus1/1p, minus2/2p, pow_mul/mulp)`; F547 #12 adds the value probes and the sidecar's O8 the `|` probe (`a | b POW c` ≡ `(a | b) POW c`).
Authority: v55:464-467 (`+ +. - -.` priority 8); the POW priority itself is not stated in v55 (:75-77, :151 only) — the level rests on the compiler. `precedence.yaml` carries no POW row (add one at level 8 with the `{Spin2_v51}` note); the "Returns NaN" notes (`:74-75`) are unsourced (F547 #12). Sweep: `level: 6` in `operators/` — this file only.

## S-133 `methods/longmove.yaml:106-118`, `methods/bytefill.yaml:114-123` — unsourced speed figures
Current: `BYTEMOVE(@dest, @source, 400)  ' ~808 cycles` / `LONGMOVE(@dest, @source, 100)  ' ~408 cycles` / `' Nearly 2x faster for aligned data`; `' 3-10x faster for count > 10`; `alignment_impact: misaligned: "Works but requires byte-by-byte for edges"`.
Correct: delete `performance_benefits.vs_bytemove` and `performance_comparison.bytefill`'s ratio line; replace with — `longmove.yaml`: `note: "BYTEMOVE(dst, src, 400) and LONGMOVE(dst, src, 100) move the same 400 bytes through the same interpreter routine; only the unit of the count differs"`; `bytefill.yaml:123`: `' runs as a cog-resident interpreter routine writing 16-long bursts, not one bytecode per byte'`; delete `alignment_impact` (`:115-118`) or reduce to "the count's low bits give a leading byte and word step; the rest moves as long bursts".
Authority: INT:87, :95 (`bc_bytemove word @bytefill_` but `bc_longmove word @longfill_`), :2166-2168 (`longfill_ shl x,#1` / `wordfill_ shl x,#1` / `bytefill_` — all three then share one routine, so the count is scaled to bytes first), :2185-2187 (forward/reverse chosen by `cmp ptrb,ptra`), :2201-2217 (`move_fwd`: leftover byte/word steps decided by the count's low two bits, then 16-long `setq`/`rdlong`/`wrlong` bursts). The KB publishes no per-operation clock count (cf. `constructs/inline_pasm.yaml:144-148`).
Sweep: `faster|cycles` ratio claims over `methods/` — these two files. The page's `:127-130` "safe for overlapping regions / direction chosen automatically" is **sourced** by INT:2185-2187 (settles S-038's source question).

## S-134 `constructs/if_elseif_else.yaml:217-226` — over-indented statement
Current (`indentation_errors`): `statement2   ' Wrong indent - not in IF block!` (indented deeper than `statement1`). The compiler gives it the **same bytes** as the same-indent version `(a134_over == a134_same)`; only a line **outdented** to the IF's level leaves the block `(a134_out != a134_same)`. Correct:
```
  - pitfall: "indentation_errors"
    description: "A statement indented less than the body ends the IF block; a statement indented more than the first body line stays in the block"
    wrong: |
      IF condition
        statement1
      statement2         ' Outdented - runs always, not part of the IF block
    correct: |
      IF condition
        statement1
        statement2       ' Same indent - both in the IF block
```
Authority: v55:702 ("All these constructs use relative indentation to determine which code falls under their control"), compiler byte-identity above. Sweep: "Wrong indent" over `constructs/` — this pitfall only.

## S-135 operator `category:` values (trivially safe)
| File:line | Current | Correct |
|---|---|---|
| `op_and.yaml:5` | `Unary` | `Logical AND` (vocabulary of `op_andand.yaml:5`) |
| `op_or.yaml:5`, `op_oror.yaml:5` | `Unary` / `Bitwise` | `Logical OR` |
| `op_xor.yaml:5`, `op_xorxor.yaml:5` | `Unary` / `Bitwise` | `Logical XOR` |
| `op_SCA.yaml:5`, `op_SCAS.yaml:5` | `Unary` | `Math` (as `op_FRAC.yaml:8`, same priority 7) |
| `op_ADDBITS.yaml:5` | `Pin` | `Bitfield` (S-129) |
(`op_ADDPINS.yaml:3` `Pin` and `op_not.yaml:5` `Unary` are right.) Also the descriptions: `op_and.yaml:4`, `op_or.yaml:4`, `op_xor.yaml:4`, `op_not.yaml:4`, `op_SCA.yaml:4`, `op_SCAS.yaml:4` end "(also PASM2 instruction)" — delete: the PASM2 `AND`/`OR`/`XOR`/`NOT` are **bitwise** (DS:1398 `D = D & S`, :1482, :1556, :1478) while the Spin2 operators are logical (v55:489-491, :428), and the PASM2 `SCA`/`SCAS` are a different operation (DS:1512-1513 "unsigned (D[15:0] * S[15:0]) >> 16 / signed … >> 14", next instruction's S) from the operators ((x * y) >> 32 / >> 30, v55:461-462). `op_andand.yaml:4` "Boolean AND/NAND" → "Logical AND (returns 0 or -1)" (F547 table E). Authority: v55:461-462, :489-491; F547 §E. Sweep: `^category:` over `operators/` (listed above is the complete set of mislabelled values).

## S-136 — RESOLVED (wrap `spin2-var`; NC18/NC18b). Nothing to do.

---

## G5 rows (`language/spin2/` debug-commands, debug-displays, preprocessor, constants, system-variables, registers, patterns, assembly-directives)

## S-137 `;` is not a comment character
Sites (the study's 17): `assembly-directives/byte.yaml:7-10`, `long.yaml:7-11`, `word.yaml:7-10`, `file.yaml:7-10`. Correct: `;` → `'` on every line, e.g. `- BYTE  $FF              ' Single byte value`, `- WORD  (@label - @base) >> 1  ' Address calculation`, `- datastart  FILE "config.dat"  ' Label the included data` — the 17 lines (with `value`/`label`/`base` declared and the four files present) compile together `(a137_all)`. Bad: `;` → `Unrecognized character []($3b)` `(a137_semicolon_bad)`.
**Class sweep — 27 more lines in 22 files** (code in YAML only; `;` in prose is fine):
- `language/pasm2/` *(sibling, group G7)* `quick_example` lines: `jse1.yaml:46`, `jse2.yaml:46`, `jse3.yaml:46`, `jse4.yaml:46`, `jnse1.yaml:46`, `jnse2.yaml:46`, `jnse3.yaml:46`, `jnse4.yaml:54`, `jct1.yaml:50`, `jct2.yaml:50`, `jct3.yaml:50`, `jnct1.yaml:44`, `jnct2.yaml:44`, `jnct3.yaml:50`, `waitse2.yaml:41`, `waitse3.yaml:41`, `waitse4.yaml:48`, `waitct2.yaml:40`. Current: `quick_example: 'JSE3 #handler  ; Jump if selector 3 event flag is set'` (and the unquoted `quick_example: WAITSE4  ; Wait for selector 4 event flag, then clear it`). Correct (double-quote the scalar so the apostrophe needs no escaping): `quick_example: "JSE3 #handler  ' Jump if selector 3 event flag is set"` · `quick_example: "WAITSE4  ' Wait for selector 4 event flag, then clear it"` (the instruction lines compile with `'`, `(a137_quick_jse3, a137_quick_waitse4)`).
- `language/pasm2/groups/counter_event_waits.yaml:23`, `counter_event_jumps.yaml:29`, `counter_event_polls.yaml:23`: the line `    ; ... do work ...` sits **inside a single-quoted YAML scalar** (`code: 'ADDCT1 …` … `JCT1    #timeout_handler'`), so the fix is `    '' ... do work ...` (doubled apostrophe). Note: the same blocks write `ADDCT1  ##1_000_000` with one operand; `ADDCT1` takes `D,{#}S` — `Expected a constant, unary operator, or "("` `(a137_groups_ok)` — NF-5.
- `architecture/system-registers/complete-system-registers-index.yaml:281, :282, :293, :294, :324, :332` (double-quoted strings): `;` → `'` — e.g. `"MOV $1F8, ##$3000  ' Same as MOV PTRA, ##$3000"` (the instruction text compiles `(a137_sysreg_ok)`).
Authority: v55:333 (`'comment here … initiated by apostrophe, rest of line is ignored`); compiler. Sweep method: `\S {2,};  ?[A-Za-z]`, `[A-Za-z0-9_)\]] ;( |$)`, `^\s*;`, `quick_example:.*;` over the whole tree (the `;` in `community/obex/objects/2848.yaml:16,18` is a smiley in prose). The other comment-character error, `//`, is S-121.

## S-138 `debug-commands/c-z.yaml:40, :51, :61` — `wc, wz` is not an effect pair
Current: `add a, b wc, wz`, `cmp x, y wc, wz`, `shl value, #8 wc, wz` → `Expected end of line (m281)` (the space-only `wc wz` fails too) `(dbg_cz_wc_wz_bad, dbg_cz_wc_wz_nocomma_bad)`. Correct: `wcz` — `add a, b wcz` etc. (compiled `(dbg_cz_wcz_plain)`; the full corrected examples are in S-157). Authority: SD:297-303 (C updated by `WC` or `WCZ`, Z by `WZ` or `WCZ`). Sweep: `wc,\s*wz`, `wc\s+wz` over the tree — these three lines only.

## S-139 `debug-commands/c-z.yaml:66-77` — `if_z` is an instruction prefix, not a Spin2 statement
Current: after an `org … end` block a bare `if_z` line with DEBUG calls indented under it → `Expected an instruction or variable` `(a139_ifz_bad)`. Correct (compiled `(dbg_cz_ex5)`): test the value in Spin2 — the full example is in S-157. If the PASM form is wanted: `if_z  mov result, #1` *inside* `org … end` (`a139_ifz_inline_ok`).
Authority: SD:297-303 and DS (condition prefixes belong to one PASM instruction); v55:788 (`ORG/ORGH must be indented to the intended scope level`). Sweep: `^\s+if_[a-z_]+\s*$` over the tree — this line only.

## S-140 block designators indented in `#IFDEF` branches
Current error: `Block designator must be in first column` at the indented `CON`/`OBJ`/`PUB` of the active branch `(a140_else2_indented_bad)`. Correct: designator in column 1, members under it as before. The 5 gated sites compiled column-1 `(a140_else2, a140_else3, a140_elseifdef2, a140_elseifdef4, a140_endif1)`; the class sweep (`designator_sweep.py`: designator lines inside an open `#IFDEF/#IFNDEF` that are indented relative to their block) finds **27 lines in 5 files**, all to move to column 1:
- `preprocessor/else.yaml:42, :44, :51, :52, :55, :56, :63, :65, :67, :70` (examples 1-3);
- `preprocessor/elseifdef.yaml:59, :62, :65, :68, :99, :100, :102, :103, :105, :106` (examples 2 and 4);
- `preprocessor/elseifndef.yaml:73, :75, :77` (passes today — per the group's note that a single indented `CON` at the very start of a file is accepted — because the one active `CON` is the first active code) `(a140_elseifndef3)`;
- `preprocessor/endif.yaml:29` (`PUB feature_init()`, with its body kept indented);
- `preprocessor/external-symbols.yaml:152, :154, :156` `(a140_extsym)`.
Example (else.yaml ex 2): `#IFDEF CUSTOM_PIN_LAYOUT` / `CON PIN_TX = CUSTOM_TX` / `CON PIN_RX = CUSTOM_RX` / `#ELSE` / `CON PIN_TX = 62` / `CON PIN_RX = 63` / `#ENDIF`. Authority: compiler error text (the v55 text states no column rule; PNut is the ground truth — a rule of PNut-TS only would be a tool limit; the sprint may confirm on PNut). Add one sentence to `preprocessor-overview.yaml` notes: "Block designators (CON, VAR, OBJ, DAT, PUB, PRI) must start in column 1, also inside a conditional branch."

## S-141 `debug-displays/plot.yaml:111` — a backtick in the trailing comment
Current: `DEBUG(`Game CROP 1 `(frame*32) 0 32 32 100 100)   ' blit 32x32 frame (expr needs `(...) to evaluate)` → the error surfaces on the next line, `Expression terms must return a single result` `(dbg_plot_bad)`. Correct (compiled with `-d`, `(dbg_plot_ok)`): `' blit 32x32 frame (the expression needs its own backtick before the parenthesis)`.
Authority: v55:1075 ("a string, containing everything from the backtick to the end of the message, is sent to the graphical DEBUG display parser"), :1084 (subsequent backticks act as escape characters). Sweep (`debug\(.*\)\s*'.*<backtick>` over the tree): `plot.yaml:111` only (`debug-displays/term.yaml:40` is prose).

## S-142 `debug-displays/logic.yaml:102`, `scope.yaml:95` — VAR inside a method listing
Current: `VAR long buff[16]` / `VAR long buff[128]` as the first line of a statement listing → `Block designator must be in first column`. Correct (both compiled with `-d`):
```
# logic.yaml example 4                              (dbg_logic_ok)
      VAR
        long buff[16]                               ' 16 longs x 16 pairs = 256 samples

      PUB main() | i, j, packed
        DEBUG(`LOGIC Pair SAMPLES 256 'D0' 'D1' LONGS_2BIT)
        REPEAT
          REPEAT j FROM 0 TO 15 … (statements unchanged)
# scope.yaml example 4                              (dbg_scope_ok)
      VAR
        long buff[128]                              ' 128 longs x 4 values = 256 A,B sample-sets

      PUB main() | i
        DEBUG(`SCOPE Sig SIZE 256 128 LONGS_8BIT) … (statements unchanged; pack_next_four_samples() is the caller's helper)
```
Authority: v55:852 (VAR declarations form their own block above the PUB that uses them). Sweep: `VAR\s+(long|byte|word)` mid-listing over the tree — only these two (`constructs/abort.yaml:115/199/251` put VAR before PUB, right).

## S-143 `registers/outa.yaml:8` — bare `!OUTA[pin]`
Current: `- "!OUTA[led_pin]"` → `Expected "="` `(a143_bare_not_bad)`. **The study's proposed fix `!= OUTA[led_pin]` compiles but is wrong:** `OUTA[n]` indexes **registers** — byte-identical to `REG[OUTA][n]` and different from the bit form `OUTA.[n]` `(a143_neq_idx == a143_regidx; != a143_neq_bit)` (v55:364-365: "With Index: AnyVar[index]"). Correct (compiled `(a143_neq_bit, a143_pintoggle)`): `- "!= OUTA.[led_pin]   ' toggle the pin bit"` — or the method `PINTOGGLE(led_pin)`.
Authority: v55:429 (`! | !x | 2 | != var | 1 | Bitwise NOT` — the assign form is `!= var`), :366 (bitfield `AnyVar.[bitfield]`). Sweep for the `INA[pin]`/`OUTA[pin]` idiom: NF-1 (17 lines in 9 files). Bare `!OUTA…`/`!DIRA…` statements: `outa.yaml:8` only.

## S-144 `patterns/implementation/spin2_latest_wins_mailbox.yaml:58-59` — CASE with no cases
Current: `case requestedCmd` followed only by a comment → `No cases encountered (m460)` (`other:` alone does not count) `(a144_case_bad, a144_case_other_only)`. Correct (compiled `(a144_case_ok)`):
```
    case requestedCmd
      1: handleCommand1(args[0], args[1])   ' one match line per command id, acting on the local copies (args[])
      other: handleUnknown(requestedCmd)
```
(add `handleCommand1` / `handleUnknown` as the caller's helpers in the pattern's prose, or keep the comment form with one real match line). A match line with no statement compiles `1:` `(a144_case_label_only)`.
Authority: compiler (m460); v55:738-748 (CASE forms). Sweep: `case x` followed by no match line over `patterns/` — this block only.

## S-145 `patterns/implementation/spin2_plugin_system.yaml:17` — `.call()` on a long
Current: `plugin_table[i].call(method)` → `Expected "["` `(a145_plugin_bad)`. Correct (compiled `(a145_plugin_ok, a145_plugin_use)`): `plugin_table[i](method)` — a method pointer held in a long (here an array element) is called as `ptr(params)`; `register_plugin(@hello)` supplies it.
Authority: v55:642-653 (`LongVar(Par1, Par2)`, `@Method`). Sweep: `\]\.(call|invoke|run|exec)\(` over the tree — this line only.

## S-146 `preprocessor/error.yaml:98-103` — `COMPILER_V48_FEATURES` is not predefined
Current: `#IFNDEF COMPILER_V48_FEATURES` / `#ERROR "This code requires compiler v48+ features"` fires on every compile `(a146_bad)`. The predefined symbols are `__DEBUG__` (v55:40) and, in PNut-TS, the `__*__` set listed in `preprocessor/external-symbols.yaml:71-111`; there is no version-test symbol (the preprocessor *is* the v48 feature — an older compiler stops at the first `#`). Correct (compiled `(a146_pnut_ts)`):
```
  - pattern: "require_pnut_ts"
    description: "Stop the build unless the PNut-TS extensions (#ERROR, #WARN, #INCLUDE, #PRAGMA) are available"
    code: |
      #IFNDEF __PNUT_TS__
      #ERROR "This code needs the PNut-TS compiler"
      #ENDIF
```
Authority: v55:40 (`__DEBUG__` "defined when DEBUG compilation is enabled"; the only predefined symbol named), `preprocessor/external-symbols.yaml:91-98` (`__PNUT_TS__`, KB page). **Decision D4** (replace vs delete the pattern). Sweep: `COMPILER_V` over the tree — this block only.

## S-147 — undetermined (one line)
`patterns/applications/multi_instance_coordination.yaml:131` method `initiate_synchronized_operation` (31 characters): v55:166 says names "can be up to 32 characters"; PNut-TS stops at 30 (`DRAFTS/PNUT-TS-PUNCH-LIST.md` item 7; S-251). Not a KB defect if PNut takes 32 — decided by that punch-list check. (If the sprint shortens it anyway: `initiate_sync_operation`, 23 chars, compiled by the reviewer.)

## S-148 `patterns/applications/animation_engine.yaml:46-47` — two 614 KB arrays
Current: `long frame_buffer_a[76800]  ' 320x240 display` / `long frame_buffer_b[76800]` = 2 × 307,200 = 614,400 bytes > 512 KB → `Program requirement exceeds 512KB hub RAM by 97432 bytes` `(a148_big_bad)`. Correct (compiled `(a148_word_ok)`):
```
    word frame_buffer_a[76800]  ' 320x240 pixels at 16 bits = 153,600 bytes
    word frame_buffer_b[76800]
```
(two buffers = 307,200 bytes; the DEBUG build also loses the top 16 KB, v55:900). The rest of the template stays red on S-071 / S-019 (G1, G2G3 specs).
Authority: DS:47 (hub RAM 524,288 bytes), SD:139; compiler. Sweep: array sizes ≥ 5 digits over the tree — these two lines only.

## S-149 `patterns/applications/utility_library.yaml:9-10` — `max` is never defined
Current: `result := min(max(val, low), high)` with only `min`, `constrain`, `map` defined → `Expected an expression term (m172)` `(a149_bad)`. Correct (compiled `(a149_lib)`): add after `min`
```
  PUB max(a, b) : result
    result := a > b ? a : b
```
and note the one-expression form `result := val #> low <# high` (`#>` raises to at least `low`, `<#` caps at `high`; compiled `(a149_oneexpr)`).
Authority: v55:468-469 (`x #> y` "Force x => y", `x <# y` "Force x <= y", priority 9). Sweep: `\b(min|max)\(` over `language/`, `guides/` — this line only.

## S-150 — RESOLVED (`fails_at: eof`, NC20). Nothing to do.

## S-151 `preprocessor/elseifndef.yaml:56-67` — the example's name is too long to show its error
Current: `CONFIGURATION_ERROR_CHECK_SETTINGS` (34 characters) under "This will cause a compile error by using undefined symbol". It fails with `Symbol exceeds 30 characters` `(a151_long_name_orig)`, not an undefined-symbol error — and 34 exceeds even v55's 32 (S-147). Correct (a name of ≤ 30 characters; the build still stops):
```
      #IFDEF CONFIG_ERROR
      CONFIG_ERROR_CHECK_SETTINGS
          ' deliberate build stop: this name is not defined anywhere
      #ENDIF
```
(`CONFIG_ERROR_CHECK_SETTINGS` = 27 characters; it fails `Expected a unique constant name, "#", or STRUCT (m210)` at top level and `Expected an instruction or variable` inside a PUB `(a151_short_name, a151_short_name_inpub)` — so write "a compile error", not "an undefined-symbol error"). Put the designator rule of S-140 into the same edit (the example's `#IFDEF` bodies).
Authority: compiler messages above; v55:166 (limit text). Sweep: other deliberate-error names — `else.yaml:96` `INVALID_CONFIGURATION_ERROR` (26) is within the limit.

## S-152 `preprocessor/preprocessor-overview.yaml:209-224` — `#IF` failure narrative is tool behaviour
Current: the description says the `#IF` line "does not open a conditional … its body compiles UNCONDITIONALLY; the matching #ENDIF is then a stray and the build fails with 'Must be preceeded by #IFDEF or #IFNDEF' … reported at the #ENDIF"; `wrong:` comments `' compiled no matter what BOARD_REV is` / `' error: Must be preceeded…`. pnut-ts 1.55.8 rejects the **`#IF` line itself**: `#if is not a supported preprocessor directive — use #ifdef or #ifndef` `(a152_if_bad)`; PNut's own behaviour for `#IF` is not in v55 (only the `#IFDEF` family, :40). Per doctrine (tool behaviour is not a KB fact) — remove the narrative. Correct:
```
  - anti_pattern: "no_if_expression_directive"
    severity: "compile_error"
    description: >-
      Writing #IF or #ELSEIF. They do not exist: the conditional directives are #IFDEF, #IFNDEF, #ELSEIFDEF, #ELSEIFNDEF,
      #ELSE and #ENDIF (v55 change log, v48), and there is no expression evaluation, so a numeric comparison cannot select
      code. The build fails.
    wrong: |
      #DEFINE BOARD_REV 2
      #IF BOARD_REV == 2          ' no such directive
        ' ...
      #ELSEIF BOARD_REV == 1
        ' ...
      #ENDIF
    correct: (unchanged)
```
(the `fails_at` of the gated `never` entry stays line 2). Authority: v55:40 (the complete directive list). Sweep: "Must be preceeded" / "compiled no matter" over the tree — this block only. (G5's own note: the `correct:` block compiles `(a152_ifdef_ok)`.)

## S-153 gating stamps — "v47"/"v44" class (one sweep for S-153, S-090, S-046, S-174)
Authority: v55:40 (**v48**, 2025-01-06: "Pre-processor added … #DEFINE, #UNDEF, #IFDEF, #IFNDEF, #ELSEIFDEF, #ELSEIFNDEF, #ELSE, #ENDIF"; `__DEBUG__`; up to 8 nesting levels), :37 (**v45**: STRUCT; "backing out and replacing v44 functionality"), :44-64 (the unlabelled notes between the v50 row and the v51 heading — ORGH inline PASM, escape strings, register constants in CON, **conditional PASM DEBUG** — i.e. v50; corroboration, not authority: `external-inputs/pnut-ts-language-updates/OFFICIAL_CHANGELOG_V43-V52.md:269, :313, :428` "(v50)"). The KB itself disagrees with itself: `preprocessor/external-symbols.yaml:5, :14, :276, :304` already say **v48**; the 13 other preprocessor pages say v47.
Edits (all: the stamp text only):
- **Preprocessor core, "v47" → "v48"**: `preprocessor/define.yaml:5, :11, :93, :115` · `ifdef.yaml:5, :12, :102, :123` · `ifndef.yaml:5, :12, :97, :120` · `else.yaml:5, :12, :101, :121` · `elseifdef.yaml:5, :12, :111, :132` · `elseifndef.yaml:5, :12, :95, :115` · `endif.yaml:5, :11, :93, :113` · `undef.yaml:5, :12, :79, :99` · `preprocessor-overview.yaml:5, :11, :304, :383` (`:304` contradicts `:308` "(v48+)"). Wording: `minimum_version: "v48"`; "Available in PNut/pnut_ts v48 and later compilers. No version directive required."; "(v48+)" in notes/oneliners.
- **PNut-TS extensions** `#ERROR`, `#WARN`, `#INCLUDE`, `#PRAGMA EXPORTDEF` (no PNut version exists for them): `error.yaml:5, :127` · `warn.yaml:5, :115` · `include.yaml:5, :190` · `pragma-exportdef.yaml:5, :181` → drop the numeric stamp; `minimum_version: "PNut-TS only"`, oneliners "(PNut-TS extension)". **Decision D5.**
- **S-174** *(sibling, group G7)* `pasm2/conditional-debug.yaml:5, :12, :122, :123, :142` "v47" / "Prior to v47, conditions before DEBUG caused compile errors" → "v50" per v55:61-64 (listed with the v50 notes; the wording "can be now preceded by a condition, not just a _RET_" supports the "earlier only `_RET_`" half; the document does not label that block separately, so say "documented with the v50 notes").
- **S-090** `constructs/blocks.yaml:52, :119` and **S-046** `conventions/vscode-pnut-documentation-style.yaml:238` — specced in G2G3 (`(v44+)` → STRUCT v45 / preprocessor v48; `{Spin2_v44}` refused → `{Spin2_v45}`).
Right and untouched: the TASK pages and `registers/taskhlt.yaml` ({Spin2_v47}, v55:39, :149), `special-symbols/hash.yaml:30, :62, :121, :133` ("#register" v47, v55:39), `c-z.yaml` (v46, v55:38, :148), `typed-pointers.yaml` (v45), DITTO (v50, :42, :150), `op_POW.yaml` (v51).
Sweep method: `v47|v44|Spin2_v4[47]` over the whole tree (listed above is every non-TASK hit). Compile fact: the preprocessor needs no directive and is not keyword-gated (G2G3 S-090 `b090_pp_*`).

## S-154 `patterns/applications/sensor_fusion.yaml:115-116` — integer `*` on a float literal
Current: `gps_weight := sensor_weights[GPS_SENSOR] * 0.3` / `baro_weight := sensor_weights[BARO_SENSOR] * 0.7`. `0.3` is the IEEE bit pattern `$3E99_999A`; the integer `*` multiplies the weight by that number (`(a154_orig)` compiles). The weights are integer percents (`calculate_gps_confidence()` returns 0..100). Correct (compiled `(a154_ok)`, with S-071's rename of the two locals):
```
    gps_weight := sensor_weights[GPS_SENSOR] * 3 / 10
    baro_weight := sensor_weights[BARO_SENSOR] * 7 / 10
```
(float form, if float weights are wanted: `ROUND(FLOAT(sensor_weights[GPS_SENSOR]) *. 0.3)`, `(a154_float_alt)`).
Authority: v55:346 (float values are IEEE-754 bit patterns; "+. -. *. /. treat long values as floats"), :455 (`*.`). Sweep: `\*\s*[0-9]+\.[0-9]+` with the integer `*` over `patterns/` — these two lines (the S-025 sibling `nan.yaml:23` is G1).

## S-155 `patterns/applications/hardware_specific_app.yaml:124-129` — CLKSET's first argument is a mode
Current: `clkset(CRYSTAL_FREQ, CPU_FREQ)` passes 20_000_000 as the clock **mode**. The clock is set by compile-time symbols; the run-time `CLKSET(mode, freq)` needs a mode word. Correct (compiled `(a155_con_ok)`): in the CON block add `_xtlfreq = CRYSTAL_FREQ` and `_clkfreq = CPU_FREQ` (after the two constants), and
```
  PUB setup_board_clocking()
    ' The clock is established before the program starts (compiled mode in CLKMODE, frequency in CLKFREQ)
    custom_hw.configure_timing(clkfreq)
```
Authority: v55:515 (`CLKSET (NewCLKMODE, NewCLKFREQ)`), :1712 (`CON _xtlfreq = 12_000_000 _clkfreq = 148_500_000` selects crystal-plus-PLL), :1730-1732 (`clkfreq`, `clkmode` variables). **Decision D6.** Sweep: `clkset(` over the tree — this call only (`methods/clkset.yaml` is S-021).

## S-156 `registers/taskhlt.yaml:15` — TASKHLT is not at $200
Current: `address: "512 ($200)"` ($200 is LUT space). The compiler places it at **`$1CC`**: `#TASKHLT` pushes `$01CC` (`44 CC 01` in the method bytecode, next to `#PR0` = `$01D8`, `#INA` = `$01FE`) `(a156_addr, listing)`, and assembling the v55 interpreter gives `TASKHLT` at cog register `$1CC` (`pnut-ts -l` of `Spin2_interpreter.spin2`: `DAT_LONG_RES … 1CC0039C … TASKHLT`) — the interpreter's `taskhlt res 1` (INT:430), inside the `$120..$1D7` area v55:806 reserves. Correct: `address: "$1CC (460) - an interpreter register inside the interpreter-occupied $120-$1D7 area"`.
Sibling: `application-notes/p2an005-cooperative-multitasking-tasks.yaml:90` ("TASKHLT @ $200, …") and `:131` ("reversed halt bits @ $200") → `$1CC`.
Authority: INT:430; v55:149 ("Register"), :39 (v47: "#register now returns the register's address"), :806. Sweep: `taskhlt.*(\$200|512)` over the tree — the three lines above.

## S-157 `debug-commands/c-z.yaml:25-77` — what `DEBUG(C_Z)` prints (VO-S157)
What the sources say: v55:1006 ("Output the C and Z flags as 'C=? Z=?'. Useful in PASM code."), :913 ("For PASM, DEBUG() statements can output … C/Z flags"). Mechanism: the debugger prints bit 31 and bit 30 of the debug-interrupt return word as C and Z (DBG:629-633, `.c_z testb iret,#31 wc` / `testb iret,#30 wc`; format DBG:1190-1191) and an interrupt stores the C/Z flags with the return address (SD:2294) — so C_Z shows the cog's flags **at the moment the DEBUG interrupt is taken**. In a Spin2 statement that cog is running the interpreter, whose `debug_` routine ends in `brk pa` (INT:821, :831): the flags are the interpreter's, not "the result of the Spin2 assignment". Nothing in any source gives the values the page prints (`x := 0` → "C=0 Z=1", the `org … end` → "C=1 Z=1", "C=1 means x < y"), and "Reads actual processor flag state at time of DEBUG call" is the only sourced line.
Compiler: `DEBUG(C_Z)` in a Spin2 statement compiles (also after an inline `org … end`); `DEBUG(C_Z)` **between PASM instructions** (DAT or inline) is rejected by pnut-ts 1.55.8 with `Expected "("` while `debug(udec(x))` in PASM compiles `(dbg_t1…dbg_t7, dbg_cz_pasm)` — v55:913 says PASM DEBUG can output the flags: a tool-behaviour question for the PNut-TS punch list, not a KB fact (item for `DRAFTS/PNUT-TS-PUNCH-LIST.md`, Stephen's call).
Correct — remove the printed-value claims (all compiled with `-d`; also S-138/S-139):
```
examples:
  - code: |
      {Spin2_v46}                              ' REQUIRED directive
      PUB flag_demo() | x
        x := 0
        DEBUG(C_Z)
        x := 1
        DEBUG(C_Z)
    description: "Print the C and Z flags at a DEBUG statement (the values are the cog's flags at that moment - see notes)"     (dbg_cz_ex1)
  - code: |
      {Spin2_v46}                              ' REQUIRED directive
      PUB inline_asm_debug() | a, b
        a := $FFFFFFFF
        b := 1
        org
              add     a, b        wcz         ' Add with flag update
        end
        DEBUG("After ADD: ", C_Z)
    description: "Debug inline assembly flag results"                                                                        (dbg_cz_ex2)
  - code: |   (cmp x, y wcz / end / DEBUG("x vs y: ", C_Z))                                                                 (dbg_cz_ex3)
  - code: |   (shl value, #8 wcz / end / DEBUG("After SHL: ", C_Z, " Value: ", UHEX(value)))                                 (dbg_cz_ex4)
  - code: |
      {Spin2_v46}                              ' REQUIRED directive
      PUB conditional_debug() | value
        value := some_operation()
        if value == 0
          DEBUG("Value is ZERO - ", C_Z)
        else
          DEBUG("Value is NON-ZERO - ", C_Z)
    description: "Conditional debugging with flag inspection"                                                                 (dbg_cz_ex5)
notes:   (replace `:111-113`)
  - "Prints the C and Z flags the cog held when the DEBUG interrupt was taken (the interrupt saves them with its return address)"
  - "Documented use is PASM code (v55:1006); in a Spin2 statement the flags are the Spin2 interpreter's own at that point, not the result of the preceding Spin2 statement"
```
Delete the `Shows:`/`C=1 means x < y` comments at `:29, :31, :42, :53`. `flag_meanings` (`:79-99`) is the generic carry/zero definition (DS:1394, 1412, 1525) and stays.
**Bench question VO-S157 (no pins).** (a) On a P2 with PNut, run the five corrected examples above and read the DEBUG window: what does C_Z print after `x := 0`, after the inline `add a, b wcz` (expect C=1 Z=1 by DS:1394 + DBG:629), after `cmp`, after `shl`? (b) Does real **PNut** accept `DEBUG(C_Z)` between PASM instructions (pnut-ts rejects it)? Control: `DEBUG(UDEC(x))` in the same PASM position, and the Spin2-statement form (compiles under pnut-ts). **Sources-silent proof:** terms `C_Z`, `c_z`, `C=?`, `Z=?`, "flag" near DEBUG searched in v55 text (hits :38, :148, :913, :1006), v51 `debug-section.txt:855`, `spin2-v51/spin2-text.txt`, DBG (:577-578, :628-633, :1190-1191), INT (:821-831), `P2-EMPIRICAL-FINDINGS.md` (no hit), `pnut-ts-language-updates/*` (version tables only) — none states a printed value or the PASM syntax; control hit v55:1006. Not jumper-testable (no pins involved). The page edits above do not wait for the answer.

## S-158 `patterns/implementation/spin2_memory_allocation.yaml:5-14` — bytes vs longs
Current: `long heap[1024]` (4096 bytes), `ptr := @heap + heap_ptr` (BYTE offset), `heap_ptr += size`, `if heap_ptr > 1024` → uses 1024 of 4096 bytes; on overflow `heap_ptr` has already advanced. Correct (compiled `(a158_ok)`):
```
  CON
    HEAP_LONGS = 1024
    HEAP_BYTES = HEAP_LONGS * 4

  VAR
    long heap[HEAP_LONGS]
    long heap_ptr                          ' next free offset, in bytes

  PUB alloc(size) : ptr
    size := (size + 3) & !3                ' round up to whole longs
    if heap_ptr + size > HEAP_BYTES
      return 0                             ' out of memory; heap_ptr unchanged
    ptr := @heap + heap_ptr
    heap_ptr += size
```
Authority: v55:262 (variables are packed in declaration order from a long-aligned address), :242 (LONG = 32 bits); `@heap` is a byte address (v55:299). Sweep: `heap_ptr`/`@heap` over the tree — this file only.

## S-159 `patterns/applications/configuration_manager.yaml:5-19` — 109-byte overrun
Current: `config_data` is `long` + `long` + the 11-byte `"DeviceName", 0` = 19 bytes, but `longmove(@config_data, addr, 32)` writes 128 bytes (`memory: "128+ bytes"`). Correct (compiled `(a159_ok)`):
```
  DAT
    config_data
      long DEFAULT_BAUD
      long DEFAULT_PINS
      byte "DeviceName", 0
    config_end

  PUB load_config(addr) : success
    bytemove(@config_data, addr, @config_end - @config_data)   ' 19 bytes, the size of config_data
    success := validate_config()
```
and `resources.memory: "19 bytes of settings (2 longs + the 11-byte name) plus code"`.
Authority: v55:303 (DAT data packed in declaration order; a symbol with no data "takes the size of the previous declaration"), :576-578 (BYTEMOVE counts bytes). Sweep: block copies with a literal count into a DAT/VAR item over `patterns/` — this one (no mechanical pattern for the general case).

## S-160 a parameter indexed as an array (`multi_motor_system.yaml:85`, `multi_display_system.yaml:96`, and a third site)
A parameter is one long. `p[i]` indexes the parameter's *own storage* (the following stack longs), not the memory it points to: `r := p[i]` and `r := long[p][i]` compile to **different** bytes `(a160_idx_param_vs_long != a160_idx_param_vs_long2)`.
Correct (compiled `(a160_motor_ok, a160_comm_ok)`):
- `multi_motor_system.yaml:82-85`: `target_positions[motor_id] := long[new_positions][motor_id]` + comment `' new_positions is the address of an array of MAX_MOTORS longs`.
- `multi_display_system.yaml:93-96`: `current_content[display_id] := long[content_array][display_id]`.
- **new site** `patterns/applications/communication_handler.yaml:13-18`: `buffer[len] := rx_char()` / `if buffer[len] == 13` → `byte[buffer][len] := rx_char()` / `if byte[buffer][len] == 13` (`buffer` is the address of a byte buffer; the original writes into `max` and the result slot).
Authority: v55:284 (parameters, then results, then locals are packed into stack memory in declaration order), :364-365 (`AnyVar[index]`; `LONG[address][index]` / `BYTE[address][index]` index hub memory by address). Sweep: `param_index_sweep.py` — every PUB/PRI plain-long parameter used with `[` inside its own method over the whole tree: exactly these 4 lines in 3 files.

## S-161 `assembly-directives/orgf.yaml` — ORGF fills, it does not align
Current: `:3` "Set origin address with forced alignment", `:8` `ORGF $100  // Align to address $100`. Correct:
```
description: 'Fill with zeros up to a cog address (cog mode only)

  '
syntax: '[''ORGF cog_address'']'
examples:
- ORGF $100  ' Fill with zeros up to cog address $100
```
(compiled `(a161_orgf)`: `org 0` / `nop` / `orgf $10` / `nop`). Bad: `ORGF` after `ORGH` → `ORGF is not allowed in ORGH mode` `(a161_orgf_orgh_bad)`; `//` comment → `Undefined symbol` (S-121).
Authority: v55:315 (`ORGF $040 'fill to cog address $040 with zeros (no symbol allowed before ORGF)`), SD:5592-5594 ("Fill to cog_address with $00 bytes. Must be in cog mode."). `pasm2/orgf.yaml:5-50` already says this correctly. Sweep: "forced alignment" / "Align to address" over the tree — this page only; `guides/pasm2-getting-started.yaml:170` and `pasm2/org.yaml:47` are right.

---

## New findings (outside the rows above; each with authority)
1. **NF-1 — `INA[pin]` / `OUTA[pin]` / `ina[0]` are register indexes, not pin bits.** `INA[n]` compiles **byte-identical to `REG[INA][n]`** (and `!= OUTA[n]` to `!= REG[OUTA][n]`), different from the bit form `INA.[n]` `(n_ina_idx == n_ina_regidx; n_outa_idx_neq == n_outa_regidx_neq)`; v55:364-365 (`AnyVar[index]` indexes; `AnyVar.[bitfield]` selects bits). Sites: `code-examples/smart-pins-002-button-reading.yaml:24, :38` (and the G2G3 S-261/S-002 spec, which keeps `if INA[BUTTON]`); `patterns/implementation/spin2_protocol_implementation.yaml:7-13` (`outa[CS]`, `outa[MOSI]`, `outa[CLK]`, `ina[MISO]`); `patterns/applications/motor_controller.yaml:15, :17` (`outa[STEP_PIN]~~`, `~`); `patterns/applications/hardware_specific_app.yaml:108` (`ina[BUTTON_PIN]`); `registers/ina.yaml:7` (`INA[button_pin]`); `registers/outa.yaml:8`; `architecture/smart-pins/smart-pin-01101-a-rise-inc-dec-by-b.yaml:55`, `smart-pin-01011-quadrature-encoder.yaml:55`, `smart-pin-01110-count-a-edges-optional-b-dec.yaml:54` (`if ina[0]` — reads all of INA, not P0). Fix: `INA.[pin]` / `OUTA.[pin] := …` / `OUTA.[STEP_PIN]~~` (compiled `(a143_ina_bit, a143_outa_bit_ops)`) or `PINREAD`/`PINWRITE`/`PINTOGGLE`. **Decision D8.**
2. **NF-2 — `typed-pointers.yaml` inversion reaches every operation**, not only the two gated blocks (see S-114: byte-identity table). `operations`, `pointer_arithmetic`, `common_patterns`, the pointer table workaround and the notes are all inverted; `gotchas.struct_pointer_obj_returns` (`[pCfg] := sensor.getConfig()`) is the one right place and already contradicts the rest of the page.
3. **NF-3 — `keywords/REPEAT.yaml:6-14` omits forms**: add `REPEAT positive_count WITH variable`, and the test-at-end forms `REPEAT` … `WHILE condition` / `UNTIL condition`. Authority v55:756-773.
4. **NF-4 — `special-symbols/dollar.yaml` describes `$` only as a hexadecimal prefix** (`description: Hexadecimal number prefix`). Add: "`$` alone is the current origin — cog register address in ORG code (steps by 1 per instruction), hub address in ORGH code (steps by 4)" (v55:312, :321; compiled `jmp #$`, `long $ + 4` `(a119_self, nf_labels_dollar_hub)`). Same invented `$$` meaning in `pasm2/concepts/labels.yaml:124-128` — see S-119.
5. **NF-5 — `language/pasm2/groups/counter_event_*.yaml`**: `ADDCT1  ##1_000_000` has one operand; `ADDCT1` takes `D,{#}S` (DS:1851; compile: `Expected a constant, unary operator, or "("` `(a137_groups_ok)`). Fix in the same edit as the S-137 comment lines (compile in sprint with a register operand).
6. **NF-6 — S-038 (G1) source answer:** `methods/longmove.yaml:127-130` / `bytemove.yaml:105-111` "safe for overlapping regions, direction chosen automatically" is sourced by the interpreter: `cmp ptrb,ptra wc` selects `move_fwd` or `move_rev` (INT:2185-2187, :2220-2239). S-038's "possible bench" is not needed.
7. **NF-7 — `preprocessor/external-symbols.yaml:149, :162`** write `pnut_ts -DTARGET_P2_EDGE` / `-D RELEASE -D OPTIMIZE`; the CLI is `-D, --Define <symbol...>` — confirm the glued `-DNAME` form before keeping it (compile in sprint; not tested here).

## Decisions for the sprint / for Stephen
- **D1 (sprint) — S-114 scope.** Rewrite the whole `operations`/`pointer_arithmetic`/`common_patterns` set from the byte-identity table (recommended; text above), or reduce the page to the six verified idioms and delete the rest. Recommend the full rewrite — every line was inverted, and the agent-consumer reading `typed-pointers` is exactly the person who writes `ptr := @buf`.
- **D2 (sprint) — S-120 sine-table example.** Replace with the squares table (recommended: compiles, shows `$$` in an expression, no invented function) or delete the example; the run-time `QSIN()` table goes in a note either way.
- **D3 (sprint) — S-118 `double_at.yaml` examples.** Replace both (recommended; text above — the page is about `@@` and the state machine is really a method-pointer example) or delete the state-machine example and move it to `concepts/method-pointers.yaml`.
- **D4 (sprint) — S-146 `minimum_version_check`.** Replace by the compiled `__PNUT_TS__` guard (recommended; keeps the findability of "version check") or delete the pattern (no portable version-test symbol exists).
- **D5 (sprint) — S-153 stamp for `#ERROR/#WARN/#INCLUDE/#PRAGMA`.** `minimum_version: "PNut-TS only"` and "(PNut-TS extension)" in the oneliners (recommended, matches `external-symbols.yaml:91-98`'s guard advice) or "v48" like the core directives (reads as if PNut had them).
- **D6 (sprint) — S-155 clocking.** `_xtlfreq`/`_clkfreq` in CON and read `clkfreq` (recommended; compiled) or keep a run-time `CLKSET` with a real mode word (needs a PLL-mode constant the page does not have).
- **D7 (Stephen) — register VO-S157** (no pins) in study §5, and decide whether "pnut-ts rejects `DEBUG(C_Z)` between PASM instructions" goes on `DRAFTS/PNUT-TS-PUNCH-LIST.md`. Without the bench the page edits (remove the printed values) are still complete.
- **D8 (Stephen/arbiter) — NF-1 confirmation.** `INA[pin]` as a register index contradicts the earlier S-261/S-002 spec and S-143's study text. Evidence is byte-identity plus v55:364-365; recommend adopting it and re-specifying S-261's `if INA[BUTTON]` as `INA.[BUTTON]` (or PINREAD). One cheap extra confirmation, if wanted: a 3-line hardware run reading `INA[5]` vs `INA.[5]` with P5 jumpered high (P5 is a free pin).
- **D9 (sprint) — S-135 vocabulary.** `Logical AND/OR/XOR`, `Math` for SCA/SCAS, `Bitfield` for ADDBITS (recommended: reuses existing values except `Bitfield`) or a flat `Operator`/`Logical` scheme.

## Counts
Rows: 51 (S-111..S-161) — change spec 47 (S-111..S-122, S-124..S-135, S-137..S-146, S-148, S-149, S-151..S-161; S-127 included as the answered row with its page edits), RESOLVED earlier 3 (S-123, S-136, S-150), undetermined 1 (S-147). Bench question: 1 (VO-S157, inside S-157). Reclassifications: 0.
Compile tally (`tally.py`, final state of the probe files): 222 probe compiles in 10 probe files — 164 compiled clean (the corrected forms, plus the unchanged counterparts used for byte-identity comparisons) and 58 failed as expected, reproducing the quoted errors. Byte-identity comparisons (`cmp.py`) are cited as `X == Y` / `X != Y` pairs in each row.
**Not compiled here ("compile in sprint"), 7:** the YAML-level quoting of the 18 `quick_example` rewrites and the 3 single-quoted `groups/counter_event_*.yaml` scalars (the instruction text compiled; the scalars are YAML); `ADDCT1` two-operand rewrite of NF-5; the corrected `external-symbols.yaml:149/162` `-D` spelling (NF-7); the per-page prose rewrites of S-127, S-128, S-133, S-135, S-153 (text only); the printed C/Z values of S-157 (VO-S157); the rest of the `animation_engine.yaml` template (blocked on S-071/S-019); the `spin2_latest_wins_mailbox` helper stubs as pattern prose.
Scratch (not part of the repo): `/tmp/claude-1000/-workspaces-P2-Knowledge-Base/fd20d1c1-e1ec-45fc-a5bc-7f395c46f9e1/scratchpad/s161/` — `probes1.py`..`probes10.py`, `run.py`, `cmp.py`, `diffbin.py`, `tally.py`, `param_index_sweep.py`, `ptr_sweep.py`, `designator_sweep.py`, `p/` (probe sources, `.bin`, `.lst`, the compiled v55 interpreter listing `interp55.lst`).

# Rows S-041..S-110 — change specs («#407», 2026-10-09)

Read-only research; nothing under `deliverables/ai/P2/`, `engineering/ingestion/`, the study or the register
was edited. Abbreviations: v55 = `sources/spin2-v55/spin2-v55-text.txt`, SD = `sources/silicon-doc/silicon-doc-text.txt`,
DS = `sources/p2-datasheet/p2-datasheet-text.txt`, INT = `external-inputs/source-code/spin-interpreter/v55/Spin2_interpreter.spin2`,
DBG = `external-inputs/source-code/spin-debugger/v51/Spin2_debugger.spin2`, F547 = `f547-operator-cascade-specs.md`
(item numbers `#n`), G1 = `rows-S001-S040-specs.md`. Paths are under `deliverables/ai/P2/`. Line numbers are those of
the files as read 2026-10-09 (current HEAD, uncommitted index files aside).

**"compiled"** = the corrected text compiled with `pnut-ts` v1.55.8 (`-q`; `-d` for DEBUG code) in the scratch
tree `…/scratchpad/s110/` (probe sources `probes1.py`..`probes13.py`, driver `run.py`; probe names are given in
parentheses, e.g. `(a041_ok)`). Wherever an error message is quoted, the "bad" form was compiled too and produced it.
**"compile in sprint"** marks code not compiled here. Numbers come from `arith.py` (arithmetic, CRC-32 emulation of the
CRCBIT definition, REV) and `diffbin.py` (binary diffs). Where a compile only proves legality, the semantic authority
is named separately. Bytes-identical / size claims name the two probes compared.

**States.** change spec — every row S-041..S-110 except S-109 (RESOLVED earlier, 53ff8f9f). S-059 also carries one
**bench question, VO-S059** (no pins) for two sub-claims the sources are silent on. S-094 and S-099, flagged "to
research" in the study, are settled from the interpreter plus compiler output (no bench). S-095 is answered in G1 §S-014
(mechanism added here). No row needed reclassification. Siblings found by the class sweep are listed under each row; those
that belong to other study groups are marked *(sibling, group Gn)* — they belong to the same edit.

---

## G2 rows (`language/spin2/concepts/`, `conventions/`)

## S-041 `concepts/addressing.yaml` — `REG[#myregs + index]`
Sites: `:164`, `:167` (code), `:169-170` (notes), `:180` (`addressing_mode_comparison.cog_register_access.syntax`).
Current: `REG[#myregs + index] := value  ' Write to cog register` · `value := REG[#myregs + index]  ' Read from cog register` ·
`- "# returns cog register address"` · `syntax: "REG[#myreg]"`.
Correct (`:163-170`, compiled `(a041_ok)`):
```
      PUB writeReg(index, value)
        REG[myregs][index] := value    ' Write to cog register

      PUB readReg(index) : value
        value := REG[myregs][index]    ' Read from cog register
    notes:
      - "REG[register][index]: 'register' is a symbol declared in an ORG section; the index is its own [index], not an addition inside the brackets"
      - "#myregs used as a term (outside REG[]) is that register's cog address"
      - "REG[] accesses cog registers from Spin2"
```
`:180` → `syntax: "REG[myreg]  or  REG[myreg][index]"`.
Bad forms: `REG[#myregs + index]` and `REG[myregs + index]` both → `Expected a constant, unary operator, or "("` `(a041_bad_hash, a041_bad_runtime)`; `x := #myregs` compiles `(a041_addr)`.
Authority: v55:364-365 (`REG[register]`, `REG[register][index]`, "'register' may be symbol declared in an ORG section"), :426 (`#reg_symbol`).
Sweep: `REG\[ *#` and `REG\[name ± …` over `deliverables/ai/P2` — only these four lines.

## S-042 `concepts/addressing.yaml:229` — hub address in a 9-bit immediate
Current: `MOV     PA, #@hubData           ' Get hub address into PA`.
Correct (`:225-236`, compiled `(a042_ok)`): `MOV     PA, ##@hubData          ' Get hub address into PA (## = 20-bit augmented immediate)`; and the block also
uses `temp` (`:234`) without declaring it — add `temp    RES     1` after the `JMP     #cogCode` line (cog register, before the ORGH).
Sibling *(group G8)* `pasm2/concepts/labels.yaml:106-110` (`hub_address.example`): `MOV ptr, @hub_data` → `MOV ptr, ##@hub_data`
(`(h042_ok)`; the bare form fails `Register cannot exceed $1FF` once the label is ≥ $200, `(h042_bad_high)`, and silently reads a cog register when low).
Authority: v55:188 ("(## for >9 bits)"), :311 (`@IncPins` is the hub address); compiler m130.

## S-043 `concepts/object_archetypes.yaml:321-371` — "pasm_only_object"
The archetype fails twice: a file with only a DAT block cannot be an OBJ child, and `@obj.dat_label` is not an expression.
Current (`:322-329`): description "Contains only DAT section with PASM code, loaded and called by parent via COGINIT…",
characteristic `- "No Spin2 methods, only DAT/PASM"`, `:365` `cog := COGINIT(COGEXEC_NEW, @pasm_calc.pasm_entry, @params)`.
Correct (compiled, child `_fast_calculator.spin2` + parent `(a043_parent_ok)`):
- description:
```
    description: |
      A child object whose work is done by a PASM program in its own cog. A Spin2
      object needs at least one PUB (a file holding only a DAT block is a PASM-only
      PROGRAM and cannot be an OBJ child), so the object carries one small PUB that
      hands the PASM entry address to the parent. A parent reaches a child's methods
      and constants only, never its DAT labels. Maximum performance for
      compute-intensive tasks.
```
- characteristic → `- "One small PUB returns the PASM entry address; everything else is DAT/PASM"`.
- `object_template`: after `temp       RES     1` (`:352`) add
```

      PUB entry_addr() : addr
      '' Hub address of the PASM entry point, for COGINIT
        addr := @pasm_entry
```
- `parent_usage` `:365` → `cog := COGINIT(COGEXEC_NEW, pasm_calc.entry_addr(), @params)`.
Errors reproduced: DAT-only child → `_dat_only_child.spin2 is a PASM file and cannot be used as a Spin2 object` `(a043_parent_dat_only)`; `@pasm_calc.pasm_entry` →
`Expected an object constant, structure, or method` `(a043_parent_dat_label)`.
Authority: v55:174 ("Objects are files which contain at least one public method"), :178-184 (block table: PUB "Required" for Spin2+PASM programs, "Not Allowed" for PASM-only programs), :233-236 (parent reaches `object_name.method_name()` and `object_name.constant_name`).
Sweep: `language/spin2/patterns/pattern-index.yaml:64` "PASM-Only Object: Maximum performance DAT code" → "PASM Driver Object: a small PUB hands out the entry address of a DAT/PASM program"; no other reference to key `pasm_only_object`. **Decision D2** (the archetype key/name).

## S-044 `:=:` swaps structures, not plain variables
Sites in this group: `concepts/operators.yaml:25`, `:198-200`. Siblings *(group G4)*: `operators/op_swap.yaml` — the whole page (`:5`, `:7-11`, `:15-27`, `:30-35`, `:54-66`, `:68-74`, `:76-84`, `:86-92`, `:94-101`, `:115`) and `keywords/STRUCT.yaml:88`, `:179` (those two are right: structures).
Correct:
- `operators.yaml:25` → `- Assignment: :=, multiple assignment (a, b := b, a), compound forms (+=, -=, etc.); :=: swaps two structure variables (v45)`.
- `operators.yaml:198-200` → `code: "a, b := b, a  ' a and b are swapped (multiple assignment)"`.
- `op_swap.yaml`: `minimum_version: "v46"` → `"v45"` (v55:37); `:11`, `:95`, `:115` "No version directive required"/"v46+" → "requires `{Spin2_v45}` (STRUCT is gated: `"STRUCT" requires {Spin2_v45} or later`, `(b090_struct_nodir)`)";
  description `:7-10` → "Swaps the contents of two structure variables of the same STRUCT type (v45). It is not defined for plain BYTE/WORD/LONG variables or array elements; swap those with multiple assignment, `a, b := b, a`.";
  delete "atomically"/"Exchanges values atomically in single operation" (`:8`, `:24`) and `:99` "uses BYTEMOVE internally" (no source; the interpreter has no swap bytecode for structures, INT:545 is the `\` post-assign); `:15-21` operands → "structure variable (same type)"; `:27` → "Works with structure variables and structure array elements".
  Examples: `[0]` → `a, b := b, a`; `[1]` add `{Spin2_v45}` first line; `[2]` replace by array-of-structure elements `pts[i] :=: pts[j]` with `CON STRUCT point(x, y)` / `VAR point pts[4]` `(f_array_elem_swap)`, and move the byte-array swap to `buffer1[i], buffer2[i] := buffer2[i], buffer1[i]` `(f_multi_assign_swap)`; `[3]` → `long[arr][j], long[arr][j + 1] := long[arr][j + 1], long[arr][j]`; `[4]` → `x, y, z := y, z, x` (rotates; `x` gets old `y`…); `comparison.swap_operator` → `"a, b := b, a"`; note `:100` keep. Add a note: `p1.x :=: p2.x` (a member) is rejected `(f_member_swap)`.
Bad forms rejected: `a :=: b`, `buffer1[i] :=: buffer2[i]`, `long[arr][j] :=: …` all → `Variable needs an operator` `(g044_swap_scalar, g044_swap_arrayelem, g044_swap_longterm)`; structure swap compiles `(a044_struct_swap, f_struct_swap_plain_var_decl)`; `a, b := b, a` compiles `(a044_swap_ok, f_multi_assign_swap)`.
Authority: v55:37 (v45: "structureA :=: structureB 'swap structures' contents"), :866, :495 (`v1,v2 := x,y`: both right-hand values are evaluated before either variable is written); corroboration (community code, not authority): `obex-projects/2852-…/jm_apa102c.spin2:286` (`first, last := last, first`), `2847-…/ansi.spin2:246`.

## S-045 `concepts/object_archetypes.yaml:286-316` — PASM register `pin` collides with PUB parameter `pin`
Current (`:315`): `RDLONG  pin, PTRA[0]` under `PUB start(pin, frequency) : ok` (`:291`).
Correct (`:311-316`, compiled `(a045_ok)`): `RDLONG  pin_reg, PTRA[0]` … and after `' ... PASM implementation` add `pin_reg     RES     1`.
Bad: `pin RES 1` beside parameter `pin` → `Expected a unique parameter name (m221)` `(a045_bad)`. Names are one namespace per object.
Authority: compiler (m221); v55:285/803 (inline PASM sees parameters by name — same namespace). Sweep: `RDLONG +(pin|value|count|…),` over the spin2/guides trees — other hits are pure-PASM contexts with no same-named PUB parameter.

## S-046 `conventions/vscode-pnut-documentation-style.yaml:238`
Current: `{Spin2_v44}` (first line of `templates.well_structured_file.template`). Correct: `{Spin2_v45}` (whole template compiled `(f046_ok)`).
`{Spin2_v44}` → `{Spin2_v44} is no longer supported due to changes in data structures beginning in v45` `(a046_v44)`; v43 and v45 both compile `(a046_v43, a046_v45)`.
Authority: compiler message; v55:37 ("backing out and replacing v44 functionality"). Sweep over `deliverables/ai/P2` for `Spin2_v44` / `v44`: this line plus `constructs/blocks.yaml:52`, `:119` (S-090). **Decision D1** (which version the template shows).

## S-047 `concepts/operators.yaml:279-283` — `??` with no variable
Current: `value := ??              ' Get random 32-bit value` · `value := ?? // 100       ' Random 0-99`; `description: "Random number (XORO32 hardware)"`.
Correct (compiled `(a047_ok)`):
```
  - operator: "??"
    description: "Iterate a long variable per the XORO32 instruction and return a pseudo-random value (??var; PUB/PRI only)"
    example: |
      value := ??seed              ' Iterate seed, get the pseudo-random value
      value := (??seed) +// 100    ' Random 0-99 (+// is the unsigned remainder)
```
Bad: `value := ??` → `Expected a variable (m251)` `(a047_bad)`. Authority: v55:412 (`??var`, "Iterate long var per XORO32, return pseudo-random value"); F547 #20, #33. Sweep: every other `??` in the KB is written `??variable` (grep).

## S-048 `concepts/string_constants.yaml:167-171`
Current: `print_string(@"=== Main Menu ===", 13, 10)` (3 arguments) then `print_string(@@menu_table[i])` (1 argument).
Correct (compiled `(f048_ok)`): replace the first line by
```
        print_string(@"=== Main Menu ===")
        print_char(13)
        print_char(10)
```
Authority: the block's own second call, `print_string` at `:70`, `:187` (one argument). Sweep: none.

## S-049 BYTE/WORD parameters and results do not exist
Sites: `concepts/type-propagation.yaml:24-43`, `:67-87` (summary), `:90-92`, `:105`. Siblings *(group G4)*: `keywords/BYTE.yaml:20-25` and `:45-49`, `keywords/WORD.yaml:20-25`, `:45-48`, `keywords/LONG.yaml:22-27`, `:51-59`, `operators/typed-pointers.yaml:66` (`LONG length` is rejected, the `^BYTE` is fine).
Correct `type-propagation.yaml` (compiled `(a049_ok, j049_type_prop)`):
```
  pub_pri_parameters:
    name: "PUB/PRI Parameters — always long (or pointer); no BYTE/WORD parameters"
    behavior: "A parameter is a long. A ^BYTE, ^WORD, ^LONG or ^StructName override makes that one parameter a pointer; the override applies only to the name it precedes"
    default: "LONG"
    example:
      code: |
        PUB foo(^BYTE a, b, ^WORD c)           ' a=^BYTE pointer, b=LONG (override not sticky), c=^WORD pointer
        PUB foo(^BYTE a, ^BYTE b, ^WORD c)     ' a, b, c all pointers (explicit each)
      explanation: "The ^BYTE before 'a' does NOT carry to 'b'. BYTE a or WORD c in a parameter list is a compile error (m220)."
    gotcha: "Opposite of VAR, where a size carries to the following names on the line"
```
`pub_pri_return_values` likewise: `PUB bar() : ^BYTE status, value` ('status' ^BYTE pointer, 'value' LONG) and `PUB bar() : ^BYTE status, ^BYTE value`; "BYTE status" → m230. `pub_pri_locals` is true as written (`| BYTE temp, count` → count is LONG; `(j049_type_prop)`).
`summary_table`: parameters/returns rows → `sticky: "NO — each name is its own"`, `inline_override: "^BYTE/^WORD/^LONG/^StructName only (pointer), per name"`. `common_mistakes[0]` →
`wrong: "PUB foo(^BYTE a, b)    ' Expecting both to be ^BYTE pointers"` / `correct: "PUB foo(^BYTE a, ^BYTE b)  ' Override each pointer parameter"`; add `wrong: "PUB foo(BYTE a, WORD b)  ' compile error (m220): parameters are longs"` / `correct: "PUB foo(a, b)  ' longs; use ^BYTE/^WORD only for a pointer"`. `notes[3]` (`:105`) delete.
Sibling edits: `BYTE.yaml:20-25` → context "Parameter (pointer)" `syntax: "PUB method(^BYTE param)"` `example: "PUB setBuffer(^BYTE pBuf)"`; context "Return value (pointer)" `syntax: "PUB method() : ^BYTE result"`; same in `WORD.yaml` (^WORD) and `LONG.yaml` (`^LONG`); `LONG.yaml:24` `PUB setAddress(addr)`, `:27` `PUB getValue() : result`; `BYTE.yaml:45-48`, `WORD.yaml:45-48`, `LONG.yaml:51-59` → "In PUB/PRI parameters and results every name is a long (or a pointer when it carries ^BYTE/^WORD/^LONG/^StructName, per name); in locals a size applies only to the name it precedes"; `typed-pointers.yaml:66` → `PUB processBuffer(^BYTE pBuffer, length)` `(j049_keywords_ok)`.
Bad forms: `PUB foo(BYTE a, b, WORD c)`, `PUB foo(LONG a)`, `PUB bar() : BYTE status, value`, `PUB bar() : LONG result` all rejected `(a049_bad_param, a049_bad_long_param, a049_bad_result, a049_bad_long_result, a049_ptr_long)`.
Authority: v55:275-278, :283, :288 (grammar: parameters/results take only `^BYTE|^WORD|^LONG|^StructName`; locals take `{^}BYTE|{^}WORD|{^}LONG|{^}StructName`). DAT row of the page verified on the listing: `mixed LONG $1234, BYTE $56, $9ABC` occupies 9 bytes, `allBytes BYTE 1, WORD 1000, 2` 4 bytes (label offsets `$1C`→`$25`→`$29`, `(j049_type_prop)` listing).

## S-050 result/parameter name equals a CON name (case-insensitive)
`concepts/timing_operations.yaml:463`, `:467`: `PUB check_sensor_read() : ready` / `ready := TRUE` (CON `READY = 2` at `:456`) → `: is_ready` and `is_ready := TRUE` (compiled `(a050_ok)`; bad `(a050_bad)`, m230). Local vs CON `| ready` → m241 `(c050_local)`.
Siblings: *(group G9)* `architecture/smart-pins/smart-pin-11111-async-serial-receive.yaml:126-127` parameter `timeout_ms` vs CON `timeout_ms` (`:110`) → `PUB receive_with_timeout(wait_ms) : value | deadline` / `deadline := getms() + wait_ms` (`(h050_param_ok)`; bad m220 `(h050_param_bad)`); *(group G5)* `patterns/applications/single_communication.yaml:135` `: success` vs CON `SUCCESS` → rename the result `ok` and its uses (reviewer-compiled, tpl r218).
Authority: compiler (m220/m221/m230/m241); v55:288. Names are case-insensitive (see S-071).

## S-051 `conventions/johnny-mac-documentation-style.yaml:143-154` — paren-less P1 method syntax
Current: `pub main` / `  setup` / `pub setup` / `  time.start` / `  serial.start(RX_PIN, TX_PIN, %0000, BAUD_115200)`.
Correct (compiled with stub objects `(f051_ok)`): `pub main()` / `  setup()` / `pub setup()` / `  time.start()` (and an `OBJ` block declaring `time` and `serial` — see S-018 in G1).
Same headers inside the `complete_example` (`:516`, `:525`) are removed with S-070. Bad: `pub main` → `Expected "("` `(a051_bad)`.
Authority: v55:288 (`PUB|PRI MethodName(…)`), :233-236 (calls take `(`). Sweep: header regex `^\s*(pub|pri) +name` without `(` over the tree — only `johnny-mac-documentation-style.yaml:144,150,516,525`.

## S-052 P1 comparison operators `=>` / `=<`
Sites: `conventions/spin2-naming-jonnymac.yaml:325` (`IF (idx => 0) AND (idx =< 15)`) → `IF (idx >= 0) AND (idx <= 15)` (whole complete_example compiled `(f052_naming_ok)`); `conventions/johnny-mac-documentation-style.yaml:541` is inside the P1 listing (S-070). Sibling *(group G5)* `patterns/applications/debug_enabled.yaml:68`, `:73`: `level =< debug_level` / `level =< DEBUG_LEVEL_WARN` → `<=` (`(h052_ok)`).
Bad: `(idx => 0) AND (idx =< 15)` → `Expected ")" (m301)` `(a052_bad)`. `operators.yaml:358` already lists them as P1 forms.
Authority: v55:475, :482 (`<=`, `>=`); F547 §A. Sweep: `=> *[0-9a-z_(-]|=< *…` over `language/spin2` — the three live sites above (the rest are prose arrows `=>`).

## S-053 `concepts/operators.yaml:49-50` — SCAS shift
F547 #13: `description: "Signed scale: (a * b) >> 32"` → `"Signed scale: (a * b) >> 30"`. Authority v55:461-462; OPR Ref #49. Sweep: `SCAS` over `language/spin2` — `op_SCAS.yaml` (stub, F547 §E), `precedence.yaml:32`, `op_addmodulo.yaml:23` carry no shift claim.

## S-054 REV reverses bits 0..y (y+1 bits)
`concepts/operators.yaml:131-133` — F547 #15: `description: "Reverse order of bits 0..y of x and zero-extend"`, `example: "%1010_0011 REV 7  ' Returns %1100_0101"`. `$A3 REV 7` = `$C5`, `$A3 REV 8` = `$18A`, `$A3 REV 31` = `$C500_0000` `(arith.py; F547 arbiter probes)`.
Siblings: `idioms/bit-manipulation.yaml:57-63` *(G3 site)*: `pattern: "{value} REV {bits}"`, `description: Reverse bit order`, examples `data REV 8`, `value REV 32`, `context: Mirror bits within specified range` →
```
  - name: bit_reverse
    pattern: "{value} REV {top_bit}"
    description: Reverse the order of bits 0..top_bit and zero-extend
    examples:
      - "data REV 7      ' reverses the low 8 bits"
      - "value REV 31    ' reverses all 32 bits"
    context: REV takes the index of the top bit to reverse; REV 7 reverses 8 bits, REV 31 all 32
```
`value REV 32` is not a 32-bit reversal: the interpreter takes the low five bits of the operand (INT:241, 244-245: `not w,x` … `shl x,w`), so `REV 32` behaves as `REV 0` (bit 0 only, `$A3 REV 32` = `$1`, arith.py). `constructs/inline_pasm.yaml:236-240` uses the PASM instruction `REV value` ("Reverse all 32 bits") — that is the PASM instruction, correct.
Authority: v55:448; INT:241-245; `operators.yaml:357` (already right).

## S-055 `concepts/operators.yaml:151`
F547 #23: `unsigned_division: "-100 +/ 7 = 613566751 …"` → `613566742`. `(2^32 − 100) // 7 = 613566742` (arith.py); arbiter probe agrees. Authority v55:458. Trivially safe.

## S-056 `DECOD ENCOD (n - 1)` is not "round up to next power of 2"
Sites: `concepts/operators.yaml:194-196`; *(group G4)* `operators/op_ENCOD.yaml:24-27`.
Current: `result := DECOD ENCOD (n - 1)`. Correct (compiled `(e056_ok)`): `result := n > 1 ? DECOD (ENCOD (n - 1) + 1) : 1`.
n = 1→1, 2→2, 3→4, 4→4, 5→8, 8→8, 9→16 (arith.py). The original gives 1 for n = 2 and 2 for n = 3, 4 (power not above n−1); n = 1 needs the guard because `ENCOD 0` = 0.
Authority: v55:434-435 (ENCOD "Encode MSB, 0..31"; DECOD "1 << (x & $1F)"); F547 #23. Sweep: `DECOD ENCOD|next power` over the tree — those two sites.

## S-057 `concepts/operators.yaml:206-208`, `:217-218` — misquoted levels
Current: "…equality '==' (level 13)…" and "…add '+' (level 9)…". Correct: `==` is level **11**, `+` is level **8** (`:207` "(level 11)", `:218` "(level 8)"); the other quoted levels (`&` 4, `<<` 3) are right. Authority v55:464 (+ = 8), :478 (== = 11), :443-451; F547 #17. The rest of the cascade (precedence.yaml etc.) is in F547 §B. Sweep: `level 13|level 9` in `language/spin2` — these two lines.

## S-058 `concepts/operators.yaml:259`, `:280` — unsourced numbers
Current: `note: "P2 has no hardware FPU - float operations are slow (~100x integer)"` · `description: "Random number (XORO32 hardware)"`.
Correct: `note: "P2 has no floating-point hardware instructions: the Spin2 float operators run as software routines in the interpreter (INT:2630-2860); the KB publishes no per-operation timing"` and the `??` description per S-047 ("…per the XORO32 instruction"; the interpreter executes the PASM `xoro32` instruction, INT:319).
Siblings: *(group G4)* `operators/op_rand.yaml:21` ("Single P2 instruction - very fast"), `:135` ("Much faster (single instruction vs 2-9 cycles)"), `:150` ("Equivalent to PASM2 XORO32 instruction") → delete the speed claims; `:150` → "Executes the XORO32 instruction on the cog (INT:319)"; `methods/getrnd.yaml:129` "(2-9 vs 1 cycle)" is in G1 §S-023.
Authority: INT:319, 2630-2860; DS:1557 (XORO32 instruction); `concepts/floating_point.yaml:103-111` (the KB's own no-figure position).

## S-059 `??` / XORO32: the algorithm text, period and zero-state claims are invented
Sites: `concepts/random_generation.yaml:47-60`, `:194` (`description: "Zero seed produces zero forever with XORO32"`), `:200`, `:274`; *(group G4)* `operators/op_rand.yaml:5`, `:11-23`, `:25-33`, `:92-96`, `:147`.
Sourced: the instruction is "xoroshiro32+" (DS:1557 "Iterate D with xoroshiro32+ PRNG algorithm and put PRNG result into next instruction's S"; pasm2-manual-text.txt:681, :4875); `??var` "Iterate long var per XORO32, return pseudo-random value" (v55:412). **Not sourced:** the three-line `state ^= …` pseudo-code (a plain xorshift, not xoroshiro32+), "Period: 2^32 − 1", "never produces zero", "zero seed produces zero forever".
Correct `random_generation.yaml:47-60`:
```
xoro32_algorithm:
  description: |
    The ?? operator iterates a long variable with the XORO32 instruction (the
    xoroshiro32+ algorithm) and returns the pseudo-random value that instruction
    produces. The variable holds the generator state and is updated in place.
  properties:
    - "Fast: one XORO32 instruction on the cog"
    - "Reproducible: the same starting value gives the same sequence"
    - "Seed it with a non-zero value (see the zero-state question below)"
    - "NOT suitable for cryptography"
```
`:194`/`:200` keep the advice "seed non-zero" but drop "forever" until VO-S059 answers; `:274` "XORO32 period is 2^32 - 1 (never returns to zero)" → delete. `op_rand.yaml`: `:5` "Applies the xoroshiro32+ algorithm…" keep; `:11-23` replace by the same description; `:25-33` "Zero seed produces zero forever" → "Seed with a non-zero value"; `:147` delete; `:20` delete. Noise example `sample := (??state >> 24) - 128` compiles `(c059_ok, i059_seed_ok)`.
**Bench question VO-S059 (no pins):** with `x := 0`, what do four successive `??x` return and what is `x` afterwards? Control: `x := 1`. Sources-silent proof: terms `seed|zero|period|never` near `xoro32|xoroshiro32|??` over SD, DS, v55, v51 text, pasm2-manual-text, p2-hardware-manual-text, INT and the EF ledger — only the algorithm name and the 128-bit analogue (SD:2852: "The 1'b1 bit ensures that the overall state will not go to zero", about the main PRNG, not XORO32); control hit DS:1557. Not jumper-testable (nothing to wire); Stephen runs the 6-line program and reads DEBUG.

## S-060 `concepts/random_generation.yaml` — signed remainder, truncation, float scale
(a) `:220-226` `modulo_bias`. Current: `value := GETRND() // 10    ' Slight bias toward 0-5`. `//` is the **signed** remainder: a negative `GETRND()` gives −9..0. Correct:
```
    description: "// is the signed remainder, so a negative random long gives a negative result"
    wrong: |
      value := GETRND() // 10    ' signed remainder: -9..9
    correct: |
      value := GETRND() +// 10   ' unsigned remainder: 0..9 (2^32 mod 10 = 6, so residues 0..5 are one count more likely: 429496730 vs 429496729)
```
(b) `:261-268` `truncating_without_scaling`: `GETRND() +// 256` and `GETRND() & $FF` are the same bits (256 divides 2^32), and every bit of GETRND is equally good — the premise ("losing randomness by masking low bits") is unsourced. Delete the anti-pattern (or restate as "`+//` and `&` give identical results for power-of-two ranges").
(c) `:94-101` `random_float`: `FLOAT(GETRND())` converts a **signed** long and `4294967295.0` rounds to 2^32 in single precision. Correct (compiled `(i060_float_ok)`): `SCALE_FACTOR = 16777216.0   ' 2^24` and `value := FLOAT(GETRND() >> 8) /. SCALE_FACTOR` → [0.0, 1.0); (2^24 − 1)/2^24 < 1 and 2^24 is exact in the 24-bit mantissa (arith.py).
Authority: v55:458-459 (`+//` unsigned, `//` signed remainder), :443 (`>>` inserts zeros), :499; arith.py. Sweep: `// [0-9]` on GETRND in the tree — only `:224`.

## S-061 `concepts/basic-io.yaml:109`, `:295` — PINREAD returns 0/1
Current: `returns: "TRUE (-1) if high, FALSE (0) if low"` · `IF !PINREAD(BUTTON_PIN)  ' Active low: a press pulls the pin to ground`.
Correct: `returns: "1 if high, 0 if low (a single pin is LSB-justified and zero-extended)"`; `:295` → `IF NOT PINREAD(BUTTON_PIN)  ' Active low: a press pulls the pin to ground` (compiled `(a061_ok)`; `PINREAD(BUTTON_PIN) == 0` also `(a061_ok2)`). `!` is bitwise NOT: `!0` = −1 and `!1` = −2, both non-zero, so the original branch ran on every pass.
Authority: INT:2467-2473 (`pinread_`: `ror a,x` / `shr x,#6` / `zerox a,x`); methods/pinread.yaml:13. Sweep: `TRUE (-1)` and `!PINREAD|! *ina` over the tree — only `basic-io.yaml:109`, `:295` (other `TRUE (-1)` hits are COMP/NAN/POLLATN/STRCOMP returns, which are right).

## S-062 pin ranges are written Top..Bottom
`concepts/basic-io.yaml:157-161` Current: `syntax: "bottom_pin..top_pin"` · `example: "8..15 = pins 8 through 15"` · `wrapping_note: "Wraps if top_pin < bottom_pin"`. Correct:
```
  range_operator:
    syntax: "top_pin..bottom_pin"
    example: "15..8 = pins 8 through 15 (same pin field as 8 ADDPINS 7)"
    wrapping_note: "Wraps within the 32-pin block if top_pin < bottom_pin"
    use_case: "Primarily for constants and readability"
```
`pinlow(15..8)` and `pinlow(8 addpins 7)` compile to byte-identical binaries (md5 `d74383f6…`, `(a062_top_bottom, a062_addpins)`); `pinlow(8..15)` differs `(a062_bottom_top, md5 26c28ede…)`.
**Class sweep — nine method pages say "(Bottom..Top)"** *(siblings, group G1)*: `methods/pinhigh.yaml:22`, `pinlow.yaml:22`, `pinfloat.yaml:23`, `pintoggle.yaml:23`, `pinwrite.yaml:23`, `pinread.yaml:23`, `wrpin.yaml:21`, `wxpin.yaml:21`, `wypin.yaml:21` → `Pin range using '..' operator, written Top..Bottom (e.g. 15..8 is pins 8 through 15; wraps within the 32-pin block if Top < Bottom)`; and `pinhigh.yaml:51` "(note: reverse range)" → "(ranges are written Top..Bottom)". The live examples (`PINHIGH(15..8)`, `PINLOW(49..40)`, `PINWRITE(7..0, $FF)`, `PINREAD(5..3)`) are already right.
Authority: v55:390 (`PINLOW (49..40) | 49..40 | 'Top..Bottom' syntax … wraps if Top < Bottom`), :378, :405.

## S-063 `concepts/basic-io.yaml:443-452` — RDPIN does not wait
Current: `description: "RDPIN blocks until data ready - may hang if no data arrives"`, wrong `value := RDPIN(SERIAL_RX)    ' Blocks forever if no data!`.
Correct (compiled `(a063_ok)`): rename `rdpin_returns_stale_value`:
```
  - anti_pattern: "rdpin_without_data_ready_check"
    severity: "wrong_value"
    description: "RDPIN returns immediately with the pin's current result Z and acknowledges the pin; it never waits. With no new data it returns the previous value"
    wrong: |
      value := RDPIN(SERIAL_RX)    ' returns at once - the last byte again if nothing new arrived
    correct: |
      ' The smart pin raises its IN flag when new data is ready; PINREAD sees it
      IF PINREAD(SERIAL_RX)
        value := RDPIN(SERIAL_RX)
```
(The page's `REPEAT UNTIL PINREAD(SERIAL_RX) OR timeout_reached()` loop at `:450` is a reasonable bounded wait and may stay.)
Authority: SD:3720 (`RDPIN D,S/# {WC} - Get smart pin S/# result Z into D, flag into C, ack pin`), :3845, :3854 ("coordinated with the IN signal going high"); INT:1129 (`rdpin_ rdpin x,x wc`, no wait); KB `architecture/smart-pins/smart-pin-11111-async-serial-receive.yaml:130-131` (polls `pinread` then `rdpin`). Sweep: `rdpin.*block|wait.*rdpin` — only this page.

## S-064 `concepts/basic-io.yaml:380-401` — cogs' pin drives are OR'd
Current: `critical_rule.consequence: "Behavior undefined if COGs drive conflicting states (not documented in P2 spec)"`, `hardware_note: "No documented conflict resolution, wire-OR, or priority scheme"`; `:382` `shared_access: "All COGs can access all 64 pins, but each COG's DIR determines if IT drives"`.
Correct:
```
  critical_rule:
    avoid: "Multiple COGs simultaneously setting DIR=1 for the same pin unless their combined result is what you want"
    consequence: "The DIR and OUT bits of all cogs are OR'd before they reach the pins, so a pin is driven when ANY cog has DIR=1 and is high when ANY driving cog has OUT=1; a cog cannot pull a pin low that another cog is driving high"
    hardware_note: "Smart-pin write buses (WRPIN/WXPIN/WYPIN/RDPIN/AKPIN) are OR'd the same way; use RQPIN to read a smart pin from several cogs without bus conflict"
```
`:382` → "All cogs can access all 64 pins; the pin is driven when any cog's DIR bit for it is 1".
Authority: SD:3725; DS:1267-1269. *(sibling, group G8)* `pasm2/concepts/basic-io.yaml:385-395` carries the identical three lines → same text; `pasm2/special-registers.yaml:314`, `architecture/decomposition/resource-ownership.yaml:14,36` already state the OR.

## S-065 `concepts/basic-io.yaml:364-376` — WS2812 bit-bang timings
Current: `WAITUS(1)  ' T1H = 800ns` / `WAITUS(0)  ' T1L = 450ns` / `WAITUS(0)  ' T0H = 400ns` / `WAITUS(1)  ' T0L = 850ns` (`application_examples.ws2812_bit_bang`).
WAITUS takes whole microseconds (v55:550), so 450/400/800/850 ns cannot be produced by it, and no source in the KB supplies the WS2812 pulse widths. Correct: **delete the block `ws2812_bit_bang`** (`:364-376`) and add to `application_examples` a one-line pointer: `ws2812: "Spin2 WAITUS cannot make sub-microsecond pulses; use a WS2812 driver object — see community/quick-bytes/ws2811-ws2812-ws2812b-ws2813-sk6812x-neopixel-object.yaml and OBEX 2857, 2852"`. **Decision D3** (delete vs keep without the nanosecond comments).
Authority: v55:550 (`WAITUS(Microseconds)`); `timing_operations.yaml:194-197` (interpreter overhead unmeasured). Sweep: other `ws2812` files (`decomposition/*`, OBEX 2852/2857) carry no Spin2 timing claim of this kind.

## S-066 `concepts/string_constants.yaml:89-108`, `:190`, `:375` — escapes belong to `@\"…\"` only
Current: table lists `\n \r \t \\ \" \0` as escapes of "strings"; `:190` `print_string(@"\r\n")` (plain form → four literal characters); `:375` `"Escape sequences require version directive for @\"string\" form"`.
Correct: `escape_sequences.table` scoped "`@\"…\"` strings only": rows `\a`=7, `\b`=8, `\t`=9, `\n`=10, `\f`=12, `\r`=13, `\\`=92, `\xNN` (NN = 01..FF); **delete** the `\"` and `\0` rows; add `unknown: "unknown sequences are passed through verbatim (v55:59)"`; `alternative` keeps numeric values (`BYTE "Line 1", 13, 10, …`). `:190` → `print_string(@\"\r\n")`. `:375` → `"Escape strings (@\"…\") need no version directive (they compile with no directive and with {Spin2_v41})"`. A literal double quote inside an escape string: `\x22` (`@\"She said \x22Hello World\x22"` compiled `(a066_quote_x22)`); `@\"…\"…"` fails `Empty string` `(a066_quote_bad)`.
Compile facts: no directive / v41 / v45 / v50 all accept `@\"Line 1\nLine 2"` (identical size, `(a066_nodir_escape, a066_v41_escape, a066_v45_escape, a066_v50_escape)`); `\0`, `\q`, `\d`, `\v`, `\e`, `\'` are rejected `Expected end of line (m281)` and `\x4` / a trailing `\` `Expected a string character (m321)` `(probes4.py)` — this contradicts v55:59 ("unknown sequences are just passed verbatim"): see **Decision D7**.
Sibling (this class) *(group G3)* `constructs/escape-strings.yaml`: delete table row `:46-48` (`\"`), replace example `:81-85` with `debug(zstr(@\"She said \x22Hello World\x22"))  ' Output: She said "Hello World"`; `:117-120`/`:146` `\x00` "Not allowed" — documented range is `\x01..\xFF` (v55:58); pnut-ts accepts `\x00` (`(a066_x00)`), so say "outside the documented range (the byte 0 would end the string for any consumer that stops at zero)"; `:11` and `:142-143` "No version directive required" are right. *(sibling, group G5)* `patterns/applications/hardware_specific_app.yaml:95` `string("Board application started\r\n")` — `STRING()` takes quoted characters and numeric values, no escapes → `string("Board application started", 13, 10)`.
Authority: v55:50-59, :592 (`STRING("Text",13)`: "quoted characters and values 1..255").

## S-067 "read-only" strings — unsourced
Sites: `concepts/string_constants.yaml:21`, `:282`, `:350`, `:353`, `:356`, `:370`; *(group G1)* `methods/string.yaml:41`.
Correct: `:21` `storage: "Object image in hub RAM"`; `:350`/`:353` `location: "Object image in hub RAM (not marked read-only)"`; `:356` `location: "DAT section in hub RAM (writable)"`; `:370` `"@\"\" and STRING() are equivalent: both compose a zero-terminated string in the object image"`; `string.yaml:41` `"Zero-terminated string composed in the object image"`.
`modifying_string_constant` (`:280-293`): rename `modifying_string_literal`, `severity: "bug_risk"`, `description: "A string literal is the program's own stored text: writing through its pointer changes that text (every use of the same pointer sees it). Copy to a buffer first"`; wrong/correct unchanged except the comment `' modifies the literal's stored bytes` and `STRCOPY(@buffer, @"Hello", 9)` (G1 §S-031).
Basis: hub RAM is read/write; nothing in the sources marks object-image data read-only (v55:303 DAT symbols are data and variables). Compiler stores a separate copy per occurrence: one literal 6328 bytes, the same literal in two methods 6368, two different literals 6368 `(d_once, d_twice_same, d_twice_diff)` — so the `duplicate_strings` anti-pattern (`:328-345`) is right.
Authority: v55:303; hub RAM is plain RAM (SD hub sections).

## S-068 `concepts/string_constants.yaml:23`, `:32`, `:176-181`, `:333-345` — bare terms in DEBUG() are characters
Current: `debug(@"Hello, World!")` · `debug(STRING("Line 1", 13, 10, "Line 2"))` · `debug(label_ptr, ": ", UDEC(value))` · `debug(@msg_success)`.
Correct (compiled with `-d`, `(a068_dbg_zstr, a068_dbg_msg)`): `debug(zstr(@"Hello, World!"))` · `ptr := STRING("Error: ", "Invalid")` then `debug(zstr(ptr))` (and for literal text simply `debug("Line 1", 13, 10, "Line 2")` `(a068_dbg_literal)`) · `debug(zstr(label_ptr), ": ", udec(value))` · `debug(zstr(@msg_success))`.
Basis (sources are NOT silent): a quoted string and bare numeric values in DEBUG() are output as text/characters (v55:919: `DEBUG("We got here! Oh, Nooooo ...", 13, 13)`); the way to print a string stored in memory is `ZSTR(hub_pointer)` (v55:938); the debugger's command set has `chr` (output one character) and `str` (inline string) for plain terms and `ZSTR(ptr)`/`LSTR(ptr,len)` for pointers (DBG:1185-1186, 1199, 1203). So `debug(@"Hello")` hands a pointer value to the `chr` path. Residual risk: the compiler could special-case `@"…"` inside DEBUG — nothing in the sources says so and community code writes `zstr(ptr)` / `zstr_(ptr)` (e.g. `obex-projects/4269-FAT32_SD_card_driver/SD card driver.spin2:19` `debug(zstr(@buffer))`, `4261-…/flash_fs_demo.spin2:72`); a one-line DEBUG window test would remove it (optional, not registered). Origin of the claim: the upstream input doc `pnut_ts_facts/String-Constants-Usage-Guide.md:23` (an upstream lead, not authority).
Siblings *(group G3)* `constructs/escape-strings.yaml:58, 61, 68-70, 75-78, 84, 90-91, 97, 103, 105, 107, 114` — every `debug(@\"…")` becomes `debug(zstr(@\"…"))` (compiled `(a068_dbg_escape)`); the "Output:" comments then hold. *(group G5)* `patterns/applications/debug_enabled.yaml` `string(…, variable)` is G5 S-124.

## S-069 `concepts/timing_operations.yaml:180-181`
Current: "us-scale ceiling is ~2.1B us at 200 MHz — rarely a practical concern." Correct: "us-scale ceiling is ~10.7 million us (~10.7 s) at 200 MHz: `clkfreq / 1_000_000 * us` is 200 × us and overflows signed 32-bit above 2^31 / 200 = 10,737,418 us — the same ceiling as the ms variant above." (arith.py: 10737418). Trivially safe.
Sibling in the same block `:164` `better_note`: "Plain clkfreq * us / 1_000_000 overflows once us exceeds ~21 at 200 MHz" → "exceeds ~10 at 200 MHz" (the signed product passes 2^31 at 11 µs: 200 × 11 = 2,200 > 2,147; arith.py "first bad us: 11"). *(New finding NF-4.)*

## S-070 `conventions/johnny-mac-documentation-style.yaml:481-569` — the "Spin2 style" example is a P1 program
Current: `complete_example` ("Complete P1 example …") with `_clkmode = xtal1 + pll16x`, `cnt`, `pub main` (no parentheses), `idx => 0`, `jm_time_80`. The page is the Spin2 standard; the P2 version sits in `spin2-naming-jonnymac.yaml:282-341`.
Correct — replace `complete_example` (`:481-569`) with this P2 port (compiled; the two child objects stubbed, `(a070_p2port)`). Lines `:483-569` become:
```
  description: "Complete example demonstrating all naming conventions, code structure, and documentation standards"
  code: |
    con { timing }

      _clkfreq = 200_000_000                   ' system frequency (PNut sets the clock from this)

      MS_001   = _clkfreq / 1_000              ' ticks in 1ms
      US_001   = _clkfreq / 1_000_000          ' ticks in 1us

    con { io pins }

      IR_IN    = 0     { I }                   ' input from IR sensor
      TX_PIN   = 62                            ' transmit pin
      RX_PIN   = 63                            ' receive pin

    con

      BUF_SIZE = 64                            ' buffer size for packets

    obj

      ' main                                   ' * master Spin2 cog
      time  : "jm_time_200"                    '   timing and delays (200MHz)
      irrx  : "ir_receiver"                    ' * IR input (your own object)

    var

      byte  irpacket[BUF_SIZE]                 ' IR packet buffer
      long  seed                               ' random seed value


    pub main()

      setup()

      repeat
        irrx.get_packet(@irpacket)
        process_packet(@irpacket)


    pub setup()

    '' Setup IO and objects for application

      time.start()                             ' setup timing & delays
      irrx.start(IR_IN)                        ' connect to IR sensor
      seed := getct()                          ' seed random number


    pub process_packet(p_buffer) | idx

    '' Process received IR packet
    '' -- p_buffer points to packet data
    '' -- handles damage calculation

      idx := byte[p_buffer][0] & $0F           ' extract damage index
      if (idx >= 0) and (idx <= 15)
        apply_damage(damage_points(idx))


    pub damage_points(idx) : points

    '' Convert index to damage points
    '' -- transmitted in bullet packet
    '' -- returns 0 for invalid index

      if (idx < 0) or (idx > 15)
        return 0
      else
        return DamageTable[idx]


    pub apply_damage(points)

    '' Apply damage points to player
    '' -- updates health status
    '' -- triggers damage effects

      ' damage processing code here


    dat { pre-initialized data }

      DamageTable   byte  1, 2, 4, 5, 7, 10, 15, 17
                    byte  20, 25, 30, 35, 40, 50, 75, 100
```
Also `:482` description "Complete P1 example …" → "Complete example …". `highlights` (`:571-581`) unchanged ("main() calls setup() pattern" now true).
P1 residue elsewhere: `jm_time_80` is a P1 (80 MHz) object name — the P2 timing object is `jm_time_200` (ingested OBEX 2852/2857 demo copies, `jm_time_200.spin2`, `pub start()`): `johnny-mac-documentation-style.yaml:109` (`time : "jm_time_80"`), `spin2-naming-jonnymac.yaml:125`, `:243`, `:298` → `jm_time_200`. `jm_fullduplexserial` is **not** P1-only: OBEX 2842 ships `jm_fullduplexserial.spin2` (P2), so those occurrences stay (correcting the reviewer's note O21); `jm_elte_irrx` has no P2 copy in the ingested OBEX set — hence the neutral `ir_receiver` above. **Decision D4**.
Authority: v55:546-547 (`GETCT()`; no `cnt`), :475/:482, :288; compiler; OBEX 2842/2852 sources. Related: S-035 (`:531` `cnt`) disappears with the block; S-051, S-052.

## S-071 constants and variables that differ only in case
Sites (conventions): `johnny-mac-documentation-style.yaml:70-92`, `:262-281`, `:334-362`; `spin2-docs-jonnymac.yaml:147-164`, `:216-246`; `spin2-naming-jonnymac.yaml:44-92`, `:209-239`. Siblings: *(group G10)* `language/fundamentals/case-sensitivity.yaml:91-97` (`PUB SetMotorSpeed(speed)` and `Pub SETMotorSPEED(SPEED)` in one block); *(group G5)* `patterns/applications/animation_engine.yaml:97-109` (`type, x, y, vx, vy, data` vs CON `TYPE, X, Y, VX, VY, DATA`), `patterns/applications/sensor_fusion.yaml:110-123` (`gps_alt, baro_alt` vs CON `GPS_ALT, BARO_ALT`).
Correct: constants stay UPPERCASE (`RX_PIN`, `TX_PIN`); the **variables** and `stop()` body become `rx_pin_num`, `tx_pin_num` (e.g. `long rx_pin_num` / `long tx_pin_num` / `long baud_rate`; `if (rx_pin_num >= 0)` / `pinf(rx_pin_num)` / `longfill(@rx_pin_num, -1, 4)` — block incl. a `start(mode, rxpin, txpin, baud)` that stores into them compiled `(a071_ok)`). Add to `naming_conventions` (both Layer pages): `case_insensitive_names: "Spin2 names are not case-sensitive: a constant RX_PIN and a variable rx_pin are the same name (error m240). Variables must differ from constants by more than case."` Bad: `RX_PIN` + `long rx_pin` → `Expected a unique variable name… (m240)` `(a071_bad)`.
`case-sensitivity.yaml:91-97`: split the Good/Poor contrast into two separate blocks. `animation_engine.yaml`: rename the six parameters of `create_animation` (e.g. `anim_type, start_x, start_y, vel_x, vel_y, anim_data`) and their uses in the method; `sensor_fusion.yaml`: rename the two locals (`gps_alt_m`, `baro_alt_m`) and uses `:111-123` (reviewer-compiled, tpl r198/r216).
Authority: compiler m240/m241/m220; v55:288. Also see `spin2-docs-jonnymac.yaml:164`/`johnny-mac…:281` `LONGFILL(@rx_pin, -1, 4)`: the page's VAR example declares three longs, not four (NF-16).

## S-072 two "required" block orders, the compiler accepts any
Sites: `conventions/spin2-formatting-standards.yaml:101-115` (`required_order` CON, OBJ, VAR, DAT, PUB, PRI; rationale "Matches compiler expectations", "Constants defined before use"…) vs `conventions/p2-source-file-organization-standard.yaml:20-35` (`standard_single_section_order` con, dat, obj, var, pub, pri; and `:21-26` blocks repeat freely).
Correct: formatting-standards `:101-115` → `recommended_order` (not required) with rationale "A convention for readability; the compiler accepts blocks in any order and allows them to repeat (a method may use a constant declared in a later CON block)", delete "Matches compiler expectations", "Constants defined before use", "Objects declared before method code", "Variables declared before use". Compiled: PUB/PRI first, then VAR, DAT, OBJ, CON last `(a072_order)`.
**Decision D6** (which single order the KB recommends). Authority: v55:178-184 (block table: no order stated), :191 (the all-block example places DAT last), :199 ("Symbolic constants can be referenced by every block within the file").

## S-073 WYPIN argument order
Sites: `conventions/johnny-mac-documentation-style.yaml:233` (`wypin(txbyte, TX_PIN)`), `:236` (`waitx(TX_BIT_TICKS)`); `conventions/spin2-docs-jonnymac.yaml:110` (`WYPIN(txbyte, TX_PIN)`), `:113` (`WAITX(TX_BIT_TICKS)`); *(group G5)* `patterns/applications/motor_controller.yaml:11` (`wypin(MULDIV64(angle, clkfreq, 1_000_000), pin)`).
Correct: `wypin(TX_PIN, txbyte)` / `WYPIN(TX_PIN, txbyte)` / `wypin(pin, MULDIV64(angle, clkfreq, 1_000_000))`; `waitx(TX_BIT_TICKS)` → `waitct(getct() + TX_BIT_TICKS)` (G1 §S-013); whole `tx` method compiled `(a073_ok)`. `basic-io.yaml:454-464` states the rule correctly.
Authority: v55:541 (`WYPIN(PinField, Data)`). Class sweep: every `WRPIN|WXPIN|WYPIN(` call over the tree (about 150 hits) — only the three above are value-first (`basic-io.yaml:459` is the deliberate "wrong" demonstration).

---

## G3 rows (`language/spin2/constructs/`, `idioms/`, `statements/`, `integration/`)

## S-074 `constructs/blocks.yaml:150-171` — unaligned cog label after byte data
Current (`:165-171`): `message` / `BYTE  "Hello, P2!", 0` (11 bytes) then `sine_table` / `WORD  $0000, $0C8B, $1917, $2590[252]` inside the `ORG   0` region.
Correct (whole block compiled `(b074_ok)`): insert `ALIGNL` before the table:
```
        ' Lookup tables
        ALIGNL
      sine_table
        WORD  $0000, $0C8B, $1917, $2590[252]
```
Bad: `Cog symbol must be long-aligned` `(b074_bad)`. Alternative (also compiled): `ORGH` + `ALIGNL` before the shared data `(b074_orgh)` — keeps hub data out of the cog image (**Decision D8b**, minor).
Sibling *(group G9)* `architecture/smart-pins/smart-pin-11110-async-serial-transmit.yaml:100-102`: `message byte "Hello!", 13, 10, 0` then `data long 0` → add `alignl` before `data` (`(h074_ok)`; bad `(h074_bad)`).
Authority: compiler (`Cog symbol must be long-aligned`); the block's own `ALIGNL` before `mailbox` (`:161`); v55:305 (`ALIGNL` "long-align to hub by emitting 1 to 3 zero bytes").

## S-075 `constructs/if_elseif_else.yaml:60-64`, `case.yaml:76-78` — one-line IF / CASE forms
Current: `- form: "inline_if"` `syntax: "IF condition : single_statement"` `description: "Single-line conditional execution"` `IF button_pressed() : counter++`; `case.yaml`: `- form: "inline_case"` `syntax: "CASE x : 1: a(), 2: b(), OTHER: c()"`.
Correct: **delete both entries** (`if_elseif_else.yaml:60-65`, `case.yaml:76-79`); in `simple_if`'s `description` add "the statement goes on the following indented line — Spin2 has no one-line IF". The legal form compiles `(b075_ok)`; the inline forms fail `Expected end of line (m281)` `(b075_bad, b075_case_inline_bad)`; the page's own `basic_case` form compiles `(b075_case_ok)`.
(A `value : statement` on one line *inside* a CASE is legal — v55:741 — which is probably the origin of the confusion.)
Authority: v55:731-736 (IF forms), :738-748 (CASE forms). Sweep: `^\s*(IF|IFNOT|ELSEIF) … : stmt` over `language`/`guides` — only `if_elseif_else.yaml:64` (the other hits are `LOOKDOWN(x : list)` syntax).

## S-076 `constructs/if_elseif_else.yaml:140-143` — `<<=>` typo
Current: `operator: "<<=>"` · `description: "Signed comparison result (-1, 0, 1)"` · `example: "IF x <<=> y == 1  ' x > y"`.
Correct (compiled `(b076_ok)`): `operator: "<=>"` · `description: "Signed comparison (<,=,> returns -1,0,1)"` · `example: "IF (x <=> y) == 1  ' x > y"` (parentheses: `<=>` and `==` are both priority 11, F547 §A.5). Bad: `x <<=> y` → `Expected an expression term (m172)` `(b076_bad)`.
Authority: v55:488; F547 #A5. Trivially safe.

## S-077 `constructs/if_elseif_else.yaml:187-190` — `ptr.value` on an untyped pointer (and the guard claim)
Current: `IF ptr AND ptr.value > 0   ' Won't access ptr.value if ptr is 0`. Two defects: `.value` needs a typed pointer, and AND does not guard (S-094).
Correct (compiled `(b077_ok)`):
```
  - feature: "guard_a_dereference"
    description: "AND / OR (&&, ||) evaluate BOTH operands, so they cannot guard a dereference; nest the IFs"
    example: |
      {Spin2_v45}
      CON STRUCT node(value)
      VAR ^node ptr           ' typed pointer: ptr.value is the pointed-to member

      IF ptr
        IF ptr.value > 0      ' reached only when ptr <> 0
```
Bad: `ptr.value` on a plain long → `Expected "["` `(b077_plainlong)`.
Siblings: *(group G4)* `special-symbols/at.yaml:175-186` (`ptr.x := 0` on a plain-long `ptr`): declare `^point ptr`, set it with `[ptr] := @points`, step with `[ptr] += 8` — compiled `(h077_ptr_walk)`; *(group G5)* `patterns/applications/array_architecture.yaml:81` `chunk_size := task_data.size / node_count` — `.size` is invented member access on a long: pass the size as a separate parameter (`task_size`) — compile in sprint.
Authority: v55:37 (pointers: "same usage syntax as the variables they point to"), :249-256; S-094 below.

## S-078 `constructs/inline_pasm.yaml:87-105` — `END` closing a DAT section
Current: `cog_code` (`:89-94`) ends `JMP   #cog_entry` / `END`; `hub_exec` (`:99-104`) ends `' PASM2 code for hub execution` / `END`.
Correct: delete the `END` lines (`:94`, `:104`); `hub_exec` keeps a `NOP` so the section has code `(b078_cog_ok, b078_hub_ok)`. Bad: `END` in a DAT section → `Expected a unique name, BYTE, WORD, LONG, or assembly instruction` `(b078_cog_end_bad, b078_hub_end_bad)`. `END` stays in the inline-PASM forms (`basic_inline`).
Sibling *(group G10)* `guides/spin2-getting-started.yaml:133-136` (`DAT { PASM2 code }` / `ORG` / `mov     x, #0` / `END`) → drop `END`, declare `x   long    0` (`(h078_ok)`; bad `(h078_bad)`).
Authority: v55:785-787 (END terminates in-line PASM), :311, :320 (the DAT `ORG`/`ORGH` examples carry no END).

## S-079 `constructs/inline_pasm.yaml:201-213` — `@var` inside inline PASM
Current: `MOV   PTRA, @shared_data` with `shared_data` a VAR long.
Correct (compiled `(b079_ok)`):
```
  - pattern: "hub_variables"
    description: "Access a VAR variable from inline PASM: take its address in Spin2 first"
    code: |
      VAR
        LONG shared_data

      PUB process() | p
        p := @shared_data
        ORG
          RDLONG PA, p
          ADD    PA, #1
          WRLONG PA, p
        END
```
Bad: `@shared_data` inside the ORG → `Expected a DAT symbol` `(b079_bad)` (inline PASM resolves `@name` against DAT symbols only). PTRA, PA, PB may be used inside inline PASM — the interpreter saves and restores PTRA around the call (INT:2119-2129, "can use pa/pb/ptra/ptrb/stack") — so the original `MOV PTRA, …` / `RDLONG PA, PTRA` shape is fine once the address comes from a Spin2 local (`MOV PTRA, p`); the form above is the shorter equivalent.
Authority: compiler (`Expected a DAT symbol`); v55:311, :813; INT:2119-2129.

## S-080 `constructs/inline_pasm.yaml:215-230` — invented `SETCRC` / `CRC`
Current: `SETCRC crc, #$04C11DB7` / `CRC    PA, crc`.
Correct (compiled `(b080_ok)`; algorithm checked below):
```
  - pattern: "inline_optimization"
    description: "Optimize hot spots: CRC-32 (reflected polynomial) of a buffer"
    code: |
      PUB checksum(buffer, size) : crc | ptr, byt
        ptr := buffer
        crc := $FFFF_FFFF

        REPEAT size
          byt := BYTE[ptr++]
          ORG
            REP    #2, #8                 ' 8 bits per byte
            SHR    byt, #1 WC             ' next data bit (LSB first) into C
            CRCBIT crc, ##$EDB88320       ' if (C xor crc[0]) crc = (crc >> 1) xor poly, else crc >> 1
          END

        crc ^= $FFFF_FFFF
```
Verification: emulating the DS:1419 definition of CRCBIT (`If (C XOR D[0]) then D = (D >> 1) XOR S, else D = (D >> 1)`) with `SHR … WC` feeding the data bit gives CRC-32("123456789") = `$CBF43926`, the standard check value (arith.py). The polynomial must be the bit-reversed `$EDB88320` because CRCBIT shifts right. Spin2 alternative for a custom polynomial: `GETCRC(BytePtr, Poly, Count)` (v55:597; G1 §S-024).
Authority: DS:1419-1422 (CRCBIT/CRCNIB), DS:1751 (`REP {#}D,{#}S`: next D instructions, S times), SD:5116-5117 (encodings), v55:597. There is no `SETCRC`/`CRC` instruction (compiler: `Expected instruction, directive, BYTE/WORD/LONG, or END`, `(b080_bad)`). Sweep: `SETCRC` over the tree — this block only.

## S-081 `constructs/method_definition.yaml:108-112`
Current: `PUB clear_array(@array, size)    ' Pass array address`. Correct (compiled with a caller `(b081_ok)`): `PUB clear_array(array, size)    ' array = address of the first long (caller passes @buf); size = number of longs`. Bad: `@array` in a parameter list → `Expected a unique parameter name (m220)` `(b081_bad)`.
Authority: v55:288 (parameters are plain names or `^BYTE|^WORD|^LONG|^StructName` overrides). Sweep: `\(@` in PUB/PRI headers — this block only.

## S-082 `constructs/method_definition.yaml:242-249` — `@this` / method chaining
Current: `- pattern: "method_chaining"` … `PUB set_x(value) : self` / `self := @this    ' Return object reference` / `' Usage: obj.set_x(10).set_y(20).draw()`.
Correct — replace the pattern (compiled `(b082_ok, b082_use)`):
```
  - pattern: "setter_calls"
    description: "Spin2 has no method chaining and no self reference: call each method as its own statement"
    code: |
      VAR
        LONG x, y

      PUB set_x(value)
        x := value

      PUB set_y(value)
        y := value

      ' Usage, from a parent object:
      '   obj.set_x(10)
      '   obj.set_y(20)
      '   obj.draw()
```
Bad: `@this` → `Expected a string, variable, method, or object` `(e082_this)`; `o.set_x(10).set_y(20).draw()` → `Expected end of line (m281)` `(b082_chain_bad)`. `self` is only an ordinary result name `(g082_self_name)`.
Authority: v55:233-236 (an object's method is called as `object_name.method_name({any_parameters})`, one call per term). Sweep: `method chaining|@this|fluent` over the tree — this block only.

## S-083 `constructs/method_definition.yaml:261-268` — "variable_shadowing"
Current: `LONG count` in VAR and `PUB method() | count    ' Local 'count' shadows VAR 'count'` / `count := 10 ' Sets local, not VAR`.
Correct (compiled `(b083_ok)`; bad `(b083_bad)` m241):
```
  - pitfall: "duplicate_names"
    description: "Spin2 has no shadowing: a parameter, result or local with the name of a VAR, DAT or CON symbol of the same object is a compile error (names are unique per object and not case-sensitive)"
    wrong: |
      VAR
        LONG count

      PUB method() | count    ' error (m241): 'count' already names the VAR
        count := 10
    correct: |
      VAR
        LONG count

      PUB method() | cnt2
        cnt2 := 10
        count := cnt2
```
Sibling *(group G10)* `language/fundamentals/variable-scoping-best-practices.yaml` — the whole premise: `:20-29` (`scope_hierarchy.precedence_order` 1..6, "Higher precedence shadows lower") → "Names are unique within an object across parameters, results, locals, VAR, DAT and CON; no scope hides another"; `:50-65` `variable_shadowing` → `duplicate_names` (definition: a duplicate is rejected: m220 parameter, m230 result, m241 local, m221 vs DAT); `:94-145` the three `problematic_code` blocks become "compile error (m230 / m221 / m241)" and the `fixed_code` blocks stay (all compile, `(h083_ok)`); `:152-161` `debugging_shadowing` → symptoms are compile errors `Expected a unique … name`; `:14-18` `metadata.prevents_bugs`/`common_mistakes` reword ("shadowing" → "duplicate names"). `ai_code_generation_rules` (`:163-173`) are right.
Authority: compiler (m220/m221/m230/m241); same fact as S-050/S-071; no source permits shadowing (v55:288).

## S-084 `constructs/repeat.yaml:49-61`, `:195-199` — `REPEAT count WHILE/UNTIL`
Current: variants `pre_test_while` (`REPEAT count WHILE condition`, example `REPEAT 1000 WHILE sensor < threshold`) and `pre_test_until` (`REPEAT timeout UNTIL data_ready()`); pattern `REPEAT 1000 UNTIL IN(pin)` / `WAITUS(100)`.
Correct (compiled `(b084_ok)`): delete the two variants (`:49-61`) and add
```
  - variant: "bounded_wait"
    syntax: |
      REPEAT count
        IF done_condition
          QUIT
    description: "At most count passes, leaving early when the condition is met (Spin2 has no REPEAT count WHILE / UNTIL form)"
    example: |
      REPEAT timeout
        IF data_ready()
          QUIT
        WAITMS(1)
```
`:197-199` (`polling_loop`, also fixes S-085):
```
      REPEAT 1000
        IF PINREAD(pin)
          QUIT
        WAITUS(100)
```
Bad: `REPEAT 1000 WHILE …` → `Expected a variable (m251)`, `REPEAT timeout UNTIL …` → `Expected FROM` `(b084_bad1, b084_bad2)`. Replace the `REPEAT 1000 WHILE sensor < threshold` use by `IF sensor >= threshold` / `QUIT` (in `b084_ok`).
Authority: v55:752-773 (the complete list of REPEAT forms). Sweep: `REPEAT +x +(WHILE|UNTIL)` over the tree — only these three lines.

## S-085 `IN(pin)` is not a method
`constructs/repeat.yaml:198` → `IF PINREAD(pin)` (see S-084). Authority v55:536 (`PINR | PINREAD (PinField) : PinStates`). Sweep: `[^A-Za-z_.]IN\(` over `language`/`guides` — none other.

## S-086 `constructs/repeat.yaml:186-187`
Current: `delay_loop` — `REPEAT WAITMS(1) * 1000    ' Wait 1 second`. Correct (compiled `(b086_ok)`): `description: "Create timing delays"`, `code:` `REPEAT 1000` / `  WAITMS(1)          ' 1000 x 1 ms = 1 second` (or simply `WAITMS(1000)`).
Bad: `Expression terms must return a single result` `(b086_bad)`. Authority v55:551 (`WAITMS(Milliseconds)`, no result). Sweep: `WAIT(MS|US|CT)\(…\) *[*+-]` over the tree — this line only.

## S-087 `idioms/cog-operations.yaml:37-43` — P1 `cognew`
Current: `name: new_cog` `pattern: "cognew(@{code}, @{params})"` `examples: "cognew(@driver, @params)"`, `"cognew(@pasm_code, @mailbox)"`.
Correct (compiled `(b087_ok)`; bad `(b087_bad)`: `Expected an instruction or variable`):
```
  - name: new_cog
    pattern: "coginit(COGEXEC_NEW, @{code}, @{params})"
    description: Start PASM code in the next free cog (P2 replacement for the P1 COGNEW; COGNEW does not exist on P2; Spin2 methods start with COGSPIN(NEWCOG, method(), stack))
    examples:
      - "coginit(COGEXEC_NEW, @driver, @params)"
      - "coginit(COGEXEC_NEW, @pasm_code, @mailbox)"
    context: Launch code in the next available cog; as an expression term it returns the cog id (-1 if none free)
```
Authority: v55:517 (`COGINIT(CogNum, PASMaddr, PTRAvalue)` "returns cog's ID if used as an expression element, -1 = no cog free"), :516 (COGSPIN), :1662. **Decision D9** (keep the idiom name for findability, as above, vs delete).
P1-carry-over sweep (`waitcnt|cnt|cognew|_clkmode|_xinfreq|par|waitpne` etc. over `language/spin2`): only `cog-operations.yaml:37-43`, `johnny-mac-documentation-style.yaml:486-531` (S-070), `methods/getct.yaml:92` (G1 §S-035); the `integration` hits are explanations that these are P1-only.

## S-088 `idioms/pin-operations.yaml:47-62` — invented pin-array syntax
Correct (compiled `(b088_ok)`, includes the short names `PINL/PINH/PINT/PINR`):
```
  - name: pin_range_access
    pattern: "pin<action>({top}..{bottom})"
    description: Operate on a range of pins with one call; the range is written Top..Bottom
    examples:
      - "pinread(7..0)"
      - "pinlow(15..8)"
      - "pinhigh(31..16)"
    context: Read or drive multiple pins simultaneously (PINREAD, PINLOW, PINHIGH, PINFLOAT, PINTOGGLE, PINWRITE)

  - name: pin_toggle
    pattern: "pintoggle({pin})"
    description: Toggle pin state
    examples:
      - "pintoggle(16)"
      - "pintoggle(LED_PIN)"
    context: Invert the current output state of the pin(s)
```
There is no `pina`/`pinl`/`pinh` variable array and no `^^` post-toggle (`pina[0..7]` → `Expected an instruction or variable`, `pinl[8..15]` → `Expected "("`, `(b088_bad)`); `PINL`/`PINH`/`PINT` are the short names of the methods and take a parenthesised PinField.
Sibling *(group G5)* `patterns/applications/hardware_specific_app.yaml:70` `dira[59..58] := %00` → `pinfloat(58 addpins 1)`; `id_pins := ina[59..58]` → `id_pins := pinread(58 addpins 1)` (`(h088_ok)`; bad `(h088_bad)` m311; DIRA/INA also only cover pins 0..31).
Authority: v55:531-536 (short names), :405 (`PINREAD(17..12)`), :390.

## S-089 `constructs/blocks.yaml:46`
Current: `#0, IDLE, RUNNING, ERROR    ' 0, 1, 2, 3`. Correct: `' 0, 1, 2` (three names → 0, 1, 2). Authority v55:217 (`CON #0,a,b,c,d 'a=0, b=1, c=2, d=3`: n names → n values). Sweep: `^\s*#N,…'` enumerations in the tree — only this line. Trivially safe.

## S-090 `constructs/blocks.yaml:52`, `:119` — version gating
Current: `"Can define structures (v44+)"` · `' Conditional compilation (v44+)`. Correct: `"Can define structures (STRUCT, v45+; needs {Spin2_v45})"` · `' Conditional compilation (preprocessor, v48+)`.
Compiled: `CON STRUCT pt(x, y)` with no directive or `{Spin2_v43}` → `"STRUCT" requires {Spin2_v45} or later`; with `{Spin2_v45}` compiles `(b090_struct_nodir, b090_struct_v43, b090_struct_v45)`; `#ifdef … #endif` compiles with no directive, v47 and v48 alike — the preprocessor is not keyword-gated `(b090_pp_nodir, b090_pp_v47, b090_pp_v48)`, so say "added in v48" not "needs {Spin2_v48}".
Authority: v55:37 (v45: "backing out and replacing v44 functionality", "New keyword STRUCT"), :40 (v48 "Pre-processor added"). Sweep: `v44` over the tree — `vscode-pnut-documentation-style.yaml:238` (S-046) and these two.

## S-091 `constructs/inline_pasm.yaml:163-177`, `:363` — parameters are not PR0/PR1
Current: `- First parameter  → PR0 (also addressable as '0')` / `- Second parameter → PR1` / `- Return value     → PR0 (overlaps first parameter)`; `:363` `solution: "Parameters are PR0, PR1, etc."`; `:187-188` comments `' x is PR0, y is PR1` / `' product is PR0 (return)`.
Correct:
```
  method_interface: |
    Method parameters, results and locals map to PASM2 registers BY NAME:
    - The method's first 16 long variables (parameters, then results, then locals,
      in declaration order) are copied to cog registers $1E0..$1EF at the start of the
      block and copied back at END; inside the block each is addressed by its own name.
    - PR0..PR7 ($1D8..$1DF) are separate general-purpose registers shared between
      Spin2 and PASM code. They are not the parameters or the result.
    - Variable budget … (keep the existing paragraph)
```
`:363` → `solution: "Parameters, results and locals are addressed by their own names (the first 16 longs, $1E0..$1EF); PR0..PR7 are separate registers"`. The example comments are replaced with the S-092 example (names only).
Siblings *(group G9)* `architecture/patterns-analysis/asm_integration_analysis.yaml:23`, `:41`, `:88`: "(value1 = PR0, value2 = PR1, ...)" → "(each by its own name; first 16 longs at $1E0..$1EF; PR0..PR7 are separate general-purpose registers)"; `:41` comment → `' by NAME: value1, value2 and result each by their own name.`; `:88` "(first param = PR0, second = PR1, return overlaps PR0)" → "(each addressed by its own name)". The `:34` block already uses names and compiles.
Compiled name-based forms `(b091_pr0, b091_bare_pr)`. Authority: v55:285, :793, :802-803; the page itself `:42-44`, `:170`.

## S-092 `constructs/inline_pasm.yaml:184-189`, `method_definition.yaml:278-285` — MUL then GETQX
Current: `MUL   x, y` / `GETQX product` (inline_pasm), `MUL x, y` / `GETQX result` (method_definition `fast_multiply`).
Correct (compiled `(b092_qmul)`):
```
  example: |
    PUB multiply(x, y) : product
      ORG
        QMUL  x, y        ' CORDIC multiply of the method's own variables
        GETQX product     ' low 32 bits of the 64-bit product (waits for the CORDIC)
      END
```
and `method_definition.yaml:281-285` `PUB fast_multiply(x, y) : result` with `QMUL x, y` / `GETQX result`. Note for both: `MUL x, y` is the 2-clock 16×16 multiply — `x = x[15:0] * y[15:0]`, product left in x (compiled `(b092_mul16)`: `MUL x, y` / `MOV product, x`); GETQX returns a CORDIC result and with none pending waits/raises event 15.
Authority: DS:1455 (`MUL D,{#}S {WZ}  D = unsigned (D[15:0] * S[15:0])`), DS:2011 (`GETQX … Waits, in case result not ready`), DS:2019 (`QMUL … GETQX/GETQY retrieves lower/upper product`), SD:2054 (event 15), p2kb `p2kbPasm2Mul`. Sweep: `MUL`+`GETQX` pairs over the tree — these two blocks only; the page's `cordic_operations` block (`:244-249`) is the same QMUL code (now duplicate — drop it or keep as the CORDIC example).

## S-093 `constructs/inline_pasm.yaml:179-182` — inline labels
Current: `requirement: "Inline PASM labels must start with '.' (e.g. .loop) or ':' (e.g. :next)"` / `reason: "Inline PASM has no global label context; all labels are method-local"`.
Correct: `requirement: "Inline PASM labels are local to the ORG..END block; a plain label (lp), a '.'-prefixed (.lp) or a ':'-prefixed (:lp) label all work"` / `reason: "Inline PASM symbols are not accessible outside the in-line PASM code (v55:813)"`. All three forms compile `(b093_plain_label, b093_dot_label, g093_colon_label)`.
Sibling *(group G3)* `concepts/inline_pasm2.yaml:38` `label_rule: "Inline labels must start with '.' or ':' (method-local only)"` → same text. Authority v55:813.

## S-094 AND / OR do not short-circuit (answered; no bench)
Sites: `constructs/if_elseif_else.yaml:187-190` ("AND/OR stop evaluating when result is known"), `:260` (`evaluation_order: "Left to right with short-circuit"`).
Evidence: (1) the interpreter's `&&` / `||` are plain binary operators on two already-evaluated values — `bc_logand` $8C, `bc_logor` $8E, next to `bc_bitand` $8F (INT:1043-1046), implemented by `log_mod` (INT:292-310: pop both operands, booleanize, `and`/`or`); (2) compiler output: `r := a && f()` and `r := a & f()` compile to binaries of equal size (6304) that differ in **one byte**, `$8C` vs `$8F` at offset `$1899`; `||` vs `|` likewise `$8E` vs `$91` — no branch is emitted, whereas the ternary `a ? f() : 0` adds branch bytes (6308) `(sc_and_call, sc_bitand_call, sc_or_call, sc_bitor_call, sc_ternary_call; diffbin.py)`; the keyword `AND` is byte-identical to `&&` `(sc_and_kw)`. The right operand is therefore always evaluated, left first. Caveat recorded: the compiler evidence is pnut-ts 1.55.8, not PNut itself; the interpreter source is Parallax's.
Correct: `:187-190` per S-077; `:260` → `evaluation_order: "Conditions are tested top to bottom; the first IF/ELSEIF whose condition is non-zero (IFNOT/ELSEIFNOT: zero) runs. AND/OR evaluate both operands, left first."`.
Authority: v55:489-491 (value operators "returns 0 or -1"; nothing about skipping), INT:1043-1046, 292-310. Sweep: `short.circuit|stop evaluating|won't access` over the tree and guarded-dereference shapes `(AND|OR) (BYTE|WORD|LONG)[…` — only `if_elseif_else.yaml`.

## S-095 `constructs/case.yaml:90-96` — "direct string comparison"
Answered in G1 §S-014 (replacement `CASE TRUE` + `STRCOMP`). Mechanism added: a multi-character quoted literal "resolve[s] to 8-bit ASCII values separated by commas" (v55:348) and a CASE match may be a comma list (v55:745), so `"START":` is five single-character matches (S, T, A, R, T) against the target, which here is a pointer. Compiler: the 5-character literal compiles as a CASE match but costs one more byte than `"STAR"` and the same as four single-character matches (G3 O7: 6320 vs 6316 bytes); `x := "START"` is rejected. Interpreter: `casev` compares two longs (INT:1187-1212).
Correct (`feature: string_matching`, compiled `(b095_strcomp)`):
```
  - feature: "string_comparison"
    description: "CASE compares numbers, not strings: a multi-character quoted literal in a match list is a list of single-character values. Compare strings with STRCOMP under CASE TRUE"
    example: |
      CASE TRUE
        STRCOMP(command_string, @"START"): begin_process()
        STRCOMP(command_string, @"STOP"): end_process()
        STRCOMP(command_string, @"PAUSE"): pause_process()
```

## S-096 `constructs/case.yaml:169-177` — variable range bound
Current: `variable_in_range` — `0..max_value: process()  ' Won't work if max_value is variable`.
Compiler accepts it (`(b096_var_range)`), as it accepts a variable match value (`(b096_var_value)`); the interpreter evaluates `value1..value2` bounds from the stack at run time (INT:1301-1331: entry `x = value2`, `ptra[-1] = value1`) and CASE match values likewise (`casev`, INT:1187-1212). Only CASE_FAST needs constants: `CASE_FAST` with `0..max_value` → `Expected a constant, unary operator, or "("` `(b096_fast_var)`.
Correct:
```
  - pitfall: "variable_in_case_fast"
    description: "CASE_FAST needs constant match values and ranges; plain CASE accepts variables and expressions"
    wrong: |
      CASE_FAST x
        0..max_value: process()  ' error: max_value is a variable
    correct: |
      CASE x
        0..max_value: process()  ' CASE evaluates the bounds at run time
```
Authority: v55:750 (CASE_FAST "match values/ranges must be unique constants"), :743-745; INT:1187-1212, 1301-1331; the page's own `design_philosophy` (`:22`, "Can use expressions, not just constants").

## S-097 `constructs/repeat.yaml:35-47` — "post_test" labels on pre-test forms
Current: variants `post_test_while` / `post_test_until` ("test at end") whose examples are `REPEAT WHILE x < 100` / `REPEAT UNTIL button_pressed()`.
Correct (compiled `(e097_ok)`): rename `variant: "pre_test_while"` / `"pre_test_until"` and describe "Condition is tested BEFORE each pass; the body may never run" (delete the two entries' "(test at end)"). The true test-at-end forms are the existing `post_while` / `post_until` (`:91-112`) and `pre_vs_post_condition` (`:114-122`) already lists these two as "Test BEFORE each iteration". (The S-084 deletion removes the other two "pre_test_*" entries, so the names are free.)
Authority: v55:764-773 (`REPEAT WHILE/UNTIL <condition>` "evaluated before"; `REPEAT … WHILE/UNTIL` "evaluated after").

## S-098 `constructs/repeat.yaml:158-159` — loop variable scope
Current: `variable_scope: "Loop variable is local to the REPEAT block"`. Correct: `"The loop variable must already be declared (VAR, parameter, result or local); REPEAT does not create it, and after the loop it holds <last> ± <step> (REPEAT <variable> FROM … TO …)"`. Undeclared `i` → `Expected an expression term (m172)` `(b098_undeclared)`; declared compiles `(b098_declared)`.
Authority: v55:760-763 ("After completion, <variable> = <last> +/- 1" / "+/- <delta>"). Sweep: other "local to the loop|loop variable.*scope" phrases — none.

## S-099 STEP is a magnitude; direction comes from FROM/TO (answered; no bench)
Sites: `constructs/repeat.yaml:72` ("custom step value (can be negative)"), `:161-162` (`step_direction: "FROM/TO automatically determines direction, STEP can override"`), `:221-226` (`wrong_step_direction`: `REPEAT i FROM 10 TO 0 STEP 1    ' Never executes!`).
Evidence: `repvari`: `cmps y,x wc` (terminal vs initial) → `abs z` → `if_c neg z` — the delta is |STEP|, negated when TO is below FROM (INT:353-356); `repvarl` adds the delta and tests the end bound for either sign (INT:366-381). So `FROM 10 TO 0 STEP 1` counts down, and STEP −1 is the same loop. Both forms compile `(g099_a, g099_b, c099_step)` (legality only; semantics from the interpreter).
Correct: `:72` → `description: "Iterate with a custom step size (direction comes from FROM and TO; the sign of STEP is ignored)"`; `:161-162` → `step_direction: "FROM and TO set the direction (up when TO is above FROM, down when below); STEP only sets the size of the step — its sign is ignored"`; replace `:221-226` by
```
  - pitfall: "step_sign_is_ignored"
    description: "The sign of STEP does not choose the direction; FROM versus TO does"
    example: |
      REPEAT i FROM 10 TO 0 STEP 1     ' counts DOWN 10..0: the sign of STEP is ignored
      REPEAT i FROM 10 TO 0 STEP -1    ' the identical loop
    note: "After the loop i = last ± |step|"
```
Authority: v55:760-763 ("stepping by +/-<delta>"), INT:353-381. `guides/spin2-getting-started.yaml:261` (`FROM 99 TO 0 STEP -1`, S-263) is harmless and needs no edit.

## S-100 `integration/spin2-pasm2-integration.yaml:106-131` — CALL(#label) on code that was never loaded
Current: `PUB setup()` / `CALL(#fastLoop)` with `DAT` `ORG $080` / `fastLoop` … `RET`; comment "Code loaded at $080 in cog register space".
Correct (compiled `(c100_ok)`; the original also compiles but calls whatever is in $080, `(c100_orig)`):
```
        - spin2_code: |
            PUB setup()
              REGLOAD(@fastChunk)       ' load the chunk into cog registers $080..
              CALL(#fastLoop)           ' blocks until the PASM code below returns

            DAT
            fastChunk
              WORD fastLoop, fastEnd-fastLoop-1   ' start register, number of registers - 1
              ORG $080
            fastLoop
              REP #1, ##1000            ' repeat next instruction 1000 times
              MOV OUTA, INA
              RET
            fastEnd
          pasm2_code: |
            ' REGLOAD copies the chunk (two header words, then the code) into cog registers $080..$082
            ' CALL(#label) is a blocking call: execution does not return to the caller until the PASM code executes RET
```
Also `:123` "Code loaded at $080 in cog register space" → the REGLOAD line above; `:128` use_case "Background processing loops" → "Calling PASM routines loaded into cog registers"; `:447` `cog_call: "Runs in current cog, can be background or foreground"` → `"Runs in the calling cog and blocks the caller until the PASM code executes RET (CALL starts no background task)"` (the page's own `:126` says so).
Authority: v55:840-843 (REGLOAD chunk, then `CALL(#start)`), :820-821, :556.

## S-101 `integration/spin2-pasm2-integration.yaml:373-419` — chunk ends before `temp` / `shared_flag_addr`
Current: `intEnd` label precedes `temp long 0` / `shared_flag_addr long 0`; header `WORD $110, intEnd-intStart-1`. Listing (`pnut-ts -l`): INTSTART `$110`, INTEND `$117`, TEMP `$117`, SHARED_FLAG_ADDR `$118` → count `$117-$110-1` = 6 registers (`$110..$116`); the two longs are never loaded.
Correct (compiled `(c101_ok)`; listing: INTEND `$119`, TEMP `$117`, SHARED_FLAG_ADDR `$118` → count 8, i.e. 9 registers `$110..$118`): move the two longs above `intEnd`:
```
            handler
              ' Set flag for Spin2
              MOV temp, ##-1
              WRLONG temp, shared_flag_addr
              RETI1
            temp long 0
            shared_flag_addr long 0
            intEnd
```
Authority: v55:842-843 ("the number of registers (longs) to load, minus 1"; the `mathChunk`-style example places data before `finish`). Sweep: other `WORD …,…End-…Start-1` chunk headers — `:173` (`mathChunk`: `temp`/`mresult` before `codeEnd` — right) and `:205` (`setupEnd` after `timerISR` — right).
Related (NF-8): the same page's REGEXEC example `:209-215` keeps its timer target in `PA` — see New findings.

## S-102 `integration/spin2-pasm2-integration.yaml:349-366` — `COGINIT(COGEXEC, …)`
Current: `COGINIT(COGEXEC, @fastCode, 0)  ' Start in cog mode`. Correct (compiled `(c102_ok)`): `COGINIT(COGEXEC_NEW, @fastCode, 0)  ' Start in a free cog, cog mode`.
`COGEXEC` alone is `%00_0000` + CogNumber 0, i.e. it restarts cog 0, the cog running this program. Sibling *(group G9)* `architecture/system-registers/ptra-register.yaml:66`: `COGINIT #0, ##entry_point     ' entry_point goes to new cog's PTRB` → `COGINIT #%0_1_0000, ##entry_point   ' load and start a free cog; entry_point goes to its PTRB` (compiled `(h102_ptra_ok)`; the `#0` original `(h102_ptra_orig)` selects cog 0).
Authority: v55:1660-1662; SD:376-386, :411 (`COGINIT #%0_1_0000,addr 'load and start a free cog at addr`).

## S-103 `constructs/register-constants.yaml:100-110` — RDLONG reads hub, not registers
Current: `INA_ADDR = INA` / `OUTA_ADDR = OUTA`, then `rdlong  value, ##INA_ADDR        ' Read via constant`.
Correct (compiled `(c103_ok)`):
```
  - code: |
      CON
        ' Register addresses for inline assembly
        INA_ADDR = INA
        OUTA_ADDR = OUTA

      PUB fast_io() | value, addr
        addr := INA_ADDR
        org
          alts  addr              ' next instruction's S field := the register at that address
          mov   value, 0          ' reads INA through its address
        end
    description: "Register constants in inline assembly: indirect register access with ALTS"
```
`RDLONG value, ##INA_ADDR` compiles but reads hub RAM at that number `(c103_bad)`.
Authority: SD:507-543 (REGISTER INDIRECTION: `ALTS index,#table` / `MOV OUTA,0` — "output register[table+index]"; `ALTS pointer` form), v55:360 (INA = $1FE), the page's own `restrictions` (`:132`).

## S-104 `constructs/method_definition.yaml:271`
Current: `call_overhead: "~50 clock cycles for call/return"`. Correct: delete the key (the KB publishes no per-method clock count: `constructs/inline_pasm.yaml:144-148`, `methods/pinhigh.yaml:35-38`); `stack_operations` stays. Authority: that stated position; no source gives the number.

## S-105 Spin2 control flow is bytecode, not "compiled to PASM2"
Sites: `constructs/case.yaml:110-113` ("CASE_FAST generates jump tables in COG RAM … deterministic timing"), `:226-246` (`pasm_equivalent`); `if_elseif_else.yaml:259-261` (`overhead: "Minimal - translates to conditional jumps in PASM2"`), `:267-278` (`pasm_equivalent`); `repeat.yaml:164-181` (`pasm_equivalent`), `:256-257` (`overhead: "Minimal - typically 2-4 PASM2 instructions per iteration"`).
Correct:
- `case.yaml:110-113` →
```
  efficiency: |
    CASE_FAST dispatches through an indexed jump table of up to 256 entries in the
    compiled bytecode, branching straight to the matching code instead of testing the
    matches in sequence. It saves time at a possible cost of larger compiled code
    (v55:749). The KB publishes no clock count for it.
```
- delete the three `pasm_equivalent` blocks (**Decision D8**) — they are illustrations of the logic, not compiler output, and one is wrong (NF-5); delete `case.yaml:214-224`'s "O(1)" wording only if you want the table to stay sourced: "Jump table dispatch" is sourced (v55:749), "O(1)" is the usual reading and may stay.
- `if_elseif_else.yaml:259-261` → `evaluation_order` per S-094; `overhead: "The KB publishes no per-statement clock count; Spin2 statements run as interpreter bytecodes"`; `repeat.yaml:256-257` → same wording.
Authority: `constructs/inline_pasm.yaml:144-148` (the KB's own position: "Spin2 method invocations execute via the bytecode interpreter"), v55:791-798, :749; INT:1180-1212 (CASE bytecodes). Also F547 (S-105 appears in its sweep list).

## S-106 `constructs/method_definition.yaml:79-81`, `:106`
Current: `parameter_passing: "Parameters are passed by value (copies made)"` / `note: "Arrays and objects pass references"`; `passing_mechanism: "By value (copy) for simple types"`.
Correct: `description: "Every parameter is a long (or a structure of up to 15 longs, or a pointer when declared ^BYTE/^WORD/^LONG/^StructName), passed by value"`, `note: "An array or an object cannot be passed as such: pass its address (@array) and read it with BYTE[]/WORD[]/LONG[] or a typed pointer"`; `:106` → `passing_mechanism: "By value (a long copy per parameter)"`.
Authority: v55:275-277, :288. Sweep: `pass(es)? references|by reference` in `language/spin2` — none other.

## S-107 `idioms/memory-access.yaml:46-52` — `@@` is not "absolute address of a variable"
Current: `name: absolute_address` / `pattern: "@@{variable}"` / `description: Get absolute hub address` / examples `@@buffer`, `@@code_start`.
Correct (compiled `(c107_ok)`):
```
  - name: absolute_address
    pattern: "@@{table}[{index}]"
    description: Convert an object-relative offset stored in DAT data (e.g. WORD @Str0) to an absolute hub address; @@x = hub address of this object + x. The general address-of operator is @
    examples:
      - "@@StrList[i]"
      - "@@pointer_table[index]"
    context: Reading pointer tables built in DAT with @label entries
```
Authority: v55:300 ("'@@SymbolName' will convert an '@Symbol' in the data to an absolute address"), :308 (`@@StrList[i]`), :425 (`@@x … Hub address of this object + x, 'DAT x long @dat_symbol'`). Sweep: `special-symbols/double_at.yaml`, `special-symbols/at.yaml` state it correctly; the other `absolute address` hits are right.

## S-108 `constructs/next.yaml:52`, `quit.yaml:53`
Current: `abort: "Exits entire method"`. Correct: `abort: "Unwinds the call stack to the nearest trapped call (\method()); with no trap the task or cog stops"` (both files). Authority: `constructs/abort.yaml:35-41`, `:120-131`; v55:624-639. Sweep: `exits entire method` — these two lines only.

## S-109 RESOLVED (53ff8f9f, NC15a/b) — nothing to do.

## S-110 `statements/debug.yaml:212-222`
Current: `features` `- "Automatic type detection for variables"` (`:218`); `usage_notes` `- "DEBUG statements are processed at compile time"` (`:222`).
Correct: `:218` → `- "Output format is chosen per value (UDEC, SDEC, UHEX, UBIN, FDEC, ZSTR …); UHEX/UBIN size themselves to the value"` — the page's own `formatting_functions` (`:82-94`); `:222` → `- "Each DEBUG statement compiles to a BRK instruction that calls the debugger at run time; the compiler ignores DEBUG statements when not compiling for DEBUG"`.
Authority: v55:1056 (DEBUG() resolves to `BRK #1..255`), :897-909, :904 ("DEBUG statements are ignored by the compiler when not compiling for DEBUG mode"), :914, :965 (`UHEX` "auto-size"). Sweep: `automatic type|processed at compile time` over `language`: the other "compile time" hits (DEBUG_MASK / DEBUG_DISABLE code generation) are right.

---

## New findings (outside the rows above; each with authority)
1. **NF-1** `concepts/addressing.yaml:9-11`, `:55`, `:95`: "In Spin2+PASM programs, `@` returns RELATIVE addresses" contradicts `:137-139`, `:293` and v55:311 ("`@IncPins` is the hub address of the 'MOV' instruction"). v55:297-300: object-relative is what `@` *stores in DAT data* (`WORD @Str0`); in PUB/PRI code `@x` is the hub address. Scope "relative" to `@` written in DAT data.
2. **NF-2** `concepts/basic-io.yaml:420-428` (`read_without_input_mode`): "Reading pin that's still in output mode reads output latch, not actual pin" is unsourced; SD:3706 says the IN bit "returns the pin's read state". Candidate bench question, jumper-testable on free pins (P0 `P_HIGH_150K` high, jumpered to P1 driven low, read P0) — not registered here.
3. **NF-3** `constructs/blocks.yaml:90-94` (`memory_allocation`): "LONGs allocated first … WORDs next … BYTEs last" — v55:262: variables are "packed in memory in the order they are declared, beginning at a long-aligned address".
4. **NF-4** `concepts/timing_operations.yaml:164`: "overflows once us exceeds ~21 at 200 MHz" → ~10 (200 × 11 µs > 2^31; arith.py).
5. **NF-5** `constructs/if_elseif_else.yaml:275-278`: `CMP x, #10 WC` / `IF_NC MOV y, #30` / `IF_C MOV y, #20` gives y = 30 for x > 10 (the opposite branch); `CMPS x, #10 WCZ` / `IF_A MOV y, #20` / `IF_BE MOV y, #30` is right and compiles `(e105_pasm)`. Removed with S-105 (Decision D8).
6. **NF-6** `constructs/method_definition.yaml:73-74` (`default_return`): "Methods without declared return values return 0" — using such a method as a term is a compile error, `This method returns no results` `(e074_noresult_term)`; v55:606, :623. → "A method with no declared results returns nothing and cannot be used in an expression".
7. **NF-7** `constructs/inline_pasm.yaml:261-269` (`atomic_operations`, "Uninterruptible sequences"): `RDLONG`/`ADD`/`WRLONG` is not atomic against other cogs, and Spin2 allows interrupts during inline PASM (v55:815). → rename `read_modify_write`, "not atomic: another cog can change the long between read and write; guard shared updates with a LOCK (LOCKTRY/LOCKREL)" (SD:3673-3700).
8. **NF-8** `integration/spin2-pasm2-integration.yaml:209-215` (`regexec_immediate`): the timer ISR keeps its CT target in `PA` (`GETCT PA` / `ADDCT1 PA, …`); PA is the interpreter's scratch (SD:1173 `rfbyte pa`; INT:2455 `cmp pa,…`), so it does not survive between interrupts. v55:847 keeps it in `PR0`. → use `PR0` (compile in sprint).
9. **NF-9** `concepts/method-pointers.yaml:30-31`: `invalid_declarations` entry `type: "LONG ptr : 16"` is not a Spin2 declaration (`Expected "," or end of line`, `(k_mp_decl_colon)`); the error text belongs to *calling* through a bitfield — `lp.[15..0]()` (`(k_mp_bitfield_call)`); `BYTE`/`WORD` pointer variables are rejected at the call, not the assignment `(k_mp_byte_assign, k_mp_byte_call, k_mp_word_call)`.
10. **NF-10** `constructs/escape-strings.yaml:117-120`, `:138-139`, `:146-147`: see S-066 / Decision D7 (`\x00` accepted by pnut-ts though outside the documented `\x01..\xFF`; unknown escapes rejected although v55:59 says passed verbatim; `error_messages` list ("Invalid escape character") does not match pnut-ts's `m281`/`m321`).
11. **NF-11** `conventions/spin2-naming-jonnymac.yaml:318` and `conventions/spin2-formatting-standards.yaml:37`: `serial.start(RX_PIN, TX_PIN, BAUD_115200)` — three arguments; the named object `jm_fullduplexserial` (OBEX 2842) has `pub start(rxpin, txpin, mode, baud)` (line 121); `johnny-mac-documentation-style.yaml:154` already passes four (`%0000` mode). The gate's stub hides the arity (my `f052_naming_ok` used a 3-argument stub; with the real object use `serial.start(RX_PIN, TX_PIN, %0000, BAUD_115200)`).
12. **NF-12** `constructs/repeat.yaml:228-239` (`modifying_loop_variable`, "undefined behavior"): unsourced; the interpreter reads the variable each pass and adds the delta (INT:366-381), so a body that changes it changes the next value deterministically. Reword to "changes the loop's progress; usually a bug" or delete "undefined behavior".
13. **NF-13** `statements/debug.yaml:212` "Non-blocking operation - doesn't halt program execution": unsourced; each DEBUG() statement runs a debug interrupt in the cog and the cogs share the serial pins through LOCK[15] (v55:897-909, :926); EF-057 (`P2-EMPIRICAL-FINDINGS.md:761-771`) measured the debug interrupt corrupting streamer measurements. Remove or restate from those sources.
14. **NF-14** `conventions/johnny-mac-documentation-style.yaml:281` / `spin2-docs-jonnymac.yaml:164` `longfill(@rx_pin, -1, 4)` fills four longs; the pages' VAR example declares three (`rx_pin`, `tx_pin`, `baud_rate`) — different blocks, so **undecided**: check against the real `jm_fullduplexserial.spin2` `stop()` before editing.
15. **NF-15** *(withdrawn — checked, no defect)* `concepts/basic-io.yaml:380` registers `$1FA-$1FF` match v55:360.
16. **NF-16** *(withdrawn — checked, no defect)* `constructs/inline_pasm.yaml:236-240` `REV value  ' Reverse all 32 bits` is the PASM instruction `REV D`, not the Spin2 operator.
17. **NF-17** *Source conflict, no KB change.* `spin2-v55-text.txt:783` ("NEXT and QUIT can each be followed by an integer value 1..16 … default value of 1 … means the current nesting level … 2 would mean the outer") contradicts :92-100 ("NEXT 1 = 1st-outer", range 1..15) and :116 (v52a "changed by one"). The compiler agrees with :92-100: `quit 1` in two nested loops compiles to different bytes than bare `quit`, `quit 2` is `NEXT/QUIT is not sufficiently nested`, 16 and 17 are `NEXT/QUIT level must be from 1 to 15` `(q_bare, q_1, q_2, q_15, q_16, q_17)`. The KB (`next.yaml`, `quit.yaml`, `repeat.yaml:142-149`) matches the compiler and :92-100. Candidate for `engineering/ingestion/SOURCE-ERRATA.md` (Stephen's call).
18. **NF-18** *Cross-check on G1 §S-012 / S-331.* The argument "restoring `$1F0-$1FF` including PTRA corrupts the Spin2 stack pointer" (G1 cites v55:806, INT:2136) holds for the Spin2 methods `SETREGS`/`GETREGS` (INT:2132+: they pop the stack through `ptra`), but **not** for inline PASM or `CALL`ed code: `call_` saves PTRA before the call and restores it after (INT:2119-2129, "can use pa/pb/ptra/ptrb/stack"), and v55:806 says to avoid `$120..$1D7`/LUT `$010..$1FF`, which does not include PTRA at `$1F8`. Keep the distinction when S-331 is written (and see S-079, where PTRA is legal).

## Decisions for the sprint / for Stephen
- **D1 (sprint) — S-046 directive in the template.** `{Spin2_v45}` (compiled; the lowest version the compiler accepts above the refused v44 and the one the KB's own struct pages use) — recommended; or `{Spin2_v43}` (what the template needs, no structures); or omit it. The template uses nothing gated beyond v41.
- **D2 (sprint) — S-043 archetype key.** Keep `pasm_only_object` with the corrected text; or rename to `pasm_driver_object` and keep `pasm_only_object` as an `aliases:` entry (recommended: Parallax's "PASM-only" means a top-level DAT-only *program*, which is exactly what cannot be an OBJ child). Also `pattern-index.yaml:64`.
- **D3 (sprint) — S-065 WS2812 block.** Delete + pointer to the quick-bytes page/OBEX 2857, 2852 (recommended: no source gives WS2812 pulse widths, and WAITUS cannot make sub-µs pulses); or keep the code with the nanosecond comments removed and a "not timing-accurate" note.
- **D4 (sprint) — S-070.** P2 port in place (recommended, text above; objects `jm_time_200` — exists in OBEX 2852/2857 — and a neutral `ir_receiver`); or delete the block and point at `spin2-naming-jonnymac.yaml` `complete_example`. `jm_fullduplexserial` stays (it is a P2 object).
- **D5 (sprint) — S-071 variable names.** Rename the *variables* (`rx_pin_num`, `tx_pin_num`; recommended: fewest edits) or rename the pin constants (`RX_PIN` → e.g. `RX_P`); add the case-insensitivity rule to both naming pages either way.
- **D6 (Stephen) — S-072 single block order.** Layer 2 says CON-OBJ-VAR-DAT-PUB-PRI, the organization standard says con-dat-obj-var-pub-pri, v55:191 shows CON-OBJ-VAR-PUB-PRI-DAT. The compiler accepts any. Options: (a) both pages say "recommended, any order compiles" and name their own order as that layer's convention; (b) pick one order for the KB; (c) drop the order requirement. Recommend (a): the compiler fact is the only sourced one, the order is a style choice between two community standards.
- **D7 (Stephen) — unknown escape sequences.** v55:59 says `\d` passes verbatim; pnut-ts 1.55.8 rejects every unknown escape (`\q`, `\d`, `\0`, `\v`, `\e`, `\'` → m281) and `\x4`, trailing `\` (m321). Options: (a) keep the source rule and add a PNut-TS punch-list entry (doctrine: PNut is ground truth, tool limits are not KB facts); (b) document "avoid unknown escapes — pnut-ts rejects them"; (c) run the one-line test on real PNut (no hardware) to learn which side is right first. Recommend (c) then (a).
- **D8 (sprint) — S-105 `pasm_equivalent` blocks.** Delete the three blocks (recommended: they are not compiler output and one is wrong, NF-5) or relabel them "illustration of the logic" and fix them. D8b: S-074 `ALIGNL` (minimal) vs `ORGH` (cleaner for hub data).
- **D9 (sprint) — S-087.** Keep the `new_cog` idiom as a COGINIT form (above; keeps "new_cog"/"cognew" findable) or delete it (`init_cog` already covers COGINIT).
- **D10 (Stephen) — register VO-S059** (the `??` zero-state question; no pins) in study §5, or accept "seed with a non-zero value" without the mechanism. Also the NF-17 SOURCE-ERRATA entry.

## Counts
Rows: 70 — change spec 69 (S-041..S-108, S-110), RESOLVED 1 (S-109). S-094 and S-099 (marked "to research" with a possible bench) are settled from the interpreter source plus compiler output; S-095 is answered in G1 with the mechanism added here. Bench question: 1 sub-claim (VO-S059, inside S-059). Reclassifications: 0.
Compile tally: 232 probe compiles (good and bad forms) in 13 probe files. About 70 distinct corrected code blocks were compiled here (counted per fix site, bad forms reproduced alongside). **Not compiled here ("compile in sprint"), 5:** `array_architecture.yaml:81` (size passed as a parameter instead of `.size`, S-077); `spin2-pasm2-integration.yaml:209-215` (`PR0` in the REGEXEC ISR, NF-8); `case-sensitivity.yaml:91-97` (the Good/Poor listing split into two blocks, S-071); the page-level prose of `variable-scoping-best-practices.yaml` (its `fixed_code` blocks compile, `(h083_ok)`); the page assembly of `op_swap.yaml` (every example compiled singly, S-044). **Reviewer-compiled, not re-run here, 3:** `single_communication.yaml:135`, `animation_engine.yaml:97-109`, `sensor_fusion.yaml:110-123`. Operator-table text for S-053..S-057 is prose (F547 + `arith.py`).
Scratch (not part of the repo): `p/` probe sources, `probes1.py`..`probes13.py`, `run.py`, `diffbin.py`, `arith.py` under `/tmp/claude-1000/-workspaces-P2-Knowledge-Base/fd20d1c1-e1ec-45fc-a5bc-7f395c46f9e1/scratchpad/s110/`.


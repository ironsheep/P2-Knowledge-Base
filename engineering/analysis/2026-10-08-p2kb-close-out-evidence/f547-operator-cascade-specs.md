# F-547 cascade — page-by-page change specs (close-out study «#406», 2026-10-09)

Authority (REF): `engineering/ingestion/sources/spin2-v55/spin2-v55-operator-reference.md` (rows
"Ref #n"); `T:n` = `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt` line n. Paths below
are under `deliverables/ai/P2/language/spin2/`. Produced by a read-only reviewer; the arbiter ran the
compile probes listed at the end (pnut-ts v1.55.8) and they decide the "probe needed" items.

## A. Invented tokens (S-267, S-270, S-271, S-272)
1. Pages: `operators/op_notandand.yaml:1-5` (`!&&`), `op_eqeqeq.yaml:1-5` (`===`), `op_ltshr.yaml:1-5`
   (`<>>`); `operators/precedence.yaml:53`, `:59`; `constructs/if_elseif_else.yaml:141-143` (`<<=>`).
   `op_lteqgt.yaml:5`, `:12` only say `+<=>` does not exist — correct.
2. No `related:` in any KB YAML points at the three pages (grep `op_notandand|op_eqeqeq|op_ltshr`
   over yaml/md/json/py/txt; other hits are the generated index, the source-lock baseline listing
   them ABSENT, and a historical engineering note).
3. The keys are published (`p2kb_get p2kbSpin2OpOpEqeqeq` returns the page). `modulo_add.yaml:10-13`
   is the precedent for a redirect stub. **Decision for the sprint:** delete, or keep a stub —
   `op_notandand` → `op_andand.yaml`, `op_not.yaml` ("`!&&` is not Spin2; use `&&`/AND or `!!`/NOT");
   `op_eqeqeq` → `op_eqeq.yaml`; `op_ltshr` → `op_ltgt.yaml`, `op_shr.yaml`. All three tokens are
   rejected by the compiler.
4. `precedence.yaml:53` → `["&&", "AND"]`; `:59` → `["||", "OR"]` (Ref #76, #78; T:489, T:491).
5. `if_elseif_else.yaml:141-143`: `operator: "<=>"`; description "Signed comparison (<,=,> returns
   -1,0,1)" (Ref #75; T:488); example `IF (x <=> y) == 1  ' x > y` (parentheses: `<=>` and `==` share
   priority 11).

## B. `operators/precedence.yaml` (S-057, S-131)
6. `:15` level 2: remove `NOT` (`!!`/NOT is term priority 12, Ref #16, T:428); add unary `-.` (Ref #19).
7. Add level 12: `["!!", "NOT"]`, "Logical NOT", unary only; `:8-9`, `:84` "reserved" → "used by
   unary `!!`/NOT".
8. `:61-64` ternary: delete "PUB/PRI only" (Ref #79 "Term (All blocks)"; `x = 1 ? 2 : 3` folds in
   CON); `:86` → "Assignment only in PUB/PRI (`=` in CON); ternary in all blocks".
9. `:66` level 17: add `&&=`, `^^=`, `||=`, `SCA=`, `SCAS=`, `FRAC=`, `=` (CON equate, Ref #81);
   keep `AND=`/`OR=`/`XOR=` marked "accepted by the compiler, not in the table"; note that unary-
   assign forms and var-prefix/postfix forms are assign priority 1 (Ref #1-#10, #16-#29).
10. `:11`: correct as is; note `var\x` as a statement is open (S-280).
11. Levels 1, 3-11, 13-15, 17 otherwise match REF.

## C. `operators/op_POW.yaml` (S-132)
12. `:28-31` `level: 6` → `level: 8`, `same_level: "+, -, +., -."`, associates left — **arbiter
    probes (under `{Spin2_v51}`):** `2.0 POW 3.0 +. 1.0` = 9.0 and `1.0 +. 3.0 POW 2.0` = 16.0 (same
    level, left to right); `2.0 *. 3.0 POW 2.0` = 36.0 and `2.0 POW 3.0 *. 2.0` = 64.0 (`*.` binds
    tighter); `2.0 POW 3.0 POW 2.0` = 64.0 (left). POW needs `{Spin2_v51}` (without it: m281 in PUB,
    "Expected ," in CON) — state the gate (T:151). REF has no POW row (T:75-77, T:151 only). The
    "Returns NaN" notes (`:74-75`) are unsourced.

## D. `concepts/operators.yaml` (S-053, S-054, S-056, S-057, S-058, S-274, S-278)
13. `:50` SCAS → "Signed scale: (a * b) >> 30" (Ref #49; T:462).
14. `:52` FRAC → "Unsigned fraction: (a << 32) / b" (Ref #50; T:463).
15. `:131-139`: REV/ZEROX/SIGNX are binary priority 3 (Ref #35-#37) — move to a binary group; `:132`
    → "Reverse order of bits 0..y of x and zero-extend"; `:133` example: **probe** `$A3 REV 7` = `$C5`
    (%1100_0101, the page's stated result) and `$A3 REV 8` = `$18A` — so the example needs `REV 7`.
16. `:21`: delete "(with +variants for unsigned)" beside `<=>`; list signed, unsigned (+ forms) and
    float (`<. >. <=. >=. ==. <>.`) compares, all priority 11.
17. `:206-218`: `==` is level 11 (Ref #65; T:478), `+` is level 8 (Ref #51; T:464).
18. `:260-276` float list: add `<=.`, `>=.`, `==.`, `<>.`, unary `-.`, FLOAT()/ROUND()/TRUNC() (Ref
    #19, #64, #66, #68, #71, #82-#84); float operators act on raw bits (S-268); CON float behaviour
    (T:503-505).
19. `:259`, `:280` "~100x slower", "XORO32 hardware": unsourced (S-058).
20. `:279-283`: `value := ??` is rejected (m251); form is `value := ??seed` (Ref #3, PUB/PRI only);
    "random 0-99" with signed `//` — use `+// 100`.
21. `:297-317`: `@` add `@method`, `@object.method` (Ref #13); `@@` → "Hub address of this object + x"
    (Ref #14); add post forms and `\`, `!`, `!!`, `^@`, `#` (Ref #6-#8, #11, #15).
22. `:329` citation `:409-491` → `:409-505`.
23. `:151` `-100 +/ 7 = 613566751` → **probe: 613566742**. `:196` (and `op_ENCOD.yaml:27`)
    `DECOD ENCOD (n - 1)` → `DECOD (ENCOD (n - 1) + 1)` for n >= 2 (**probe: n = 5 gives 8**; n = 1
    special-cased).

## E. Stub pages inherited from the summary (S-271, S-273, S-135)
| Page | Current | Correct (Ref #) |
|---|---|---|
| `op_ABS.yaml:3-5` | broken fragment; `category: \`` | "Absolute value", priority 2, `ABS= var` (1), CON float on float constants (#20); category Unary |
| `op_ADDBITS.yaml:4-7` | "Add bit count to pin number"; Pin | "Make bitfield, (x & $1F) \| (y & $1F) << 5", priority 10, `ADDBITS=` 17 (#57); **probe `4 ADDBITS 3` = 100 ($64)** (S-129) |
| `op_ADDPINS.yaml:4-16` | encoding "base_pin + (count << 6)" | add masks (x & $3F) \| (y & $1F) << 6 (#58, T:471), priority 10, `ADDPINS=`; relate `op_ADDBITS` |
| `op_andand.yaml:4`, `op_and.yaml:4-5` | "Boolean AND/NAND"; Unary | "Logical AND (returns 0 or -1)", priority 13, `&&=` (#76); Logical |
| `op_oror`, `op_or`, `op_xorxor`, `op_xor` | Bitwise / Unary | Logical OR 15 `\|\|=` (#78); Logical XOR 14 `^^=` (#77); Logical |
| `op_not.yaml:4-5` | "Logical NOT"; no `!!` | "`!!`, NOT: Logical NOT (0 → -1, non-0 → 0)", priority 12, `!!= var` (1) (#16); alias `!!` |
| `op_eqeq.yaml:4`, `op_ltgt.yaml:4` | "Equal/not equal (logical/bitwise)" | "Equal (returns 0 or -1)", "Not equal (returns 0 or -1)", priority 11; CON float returns 1.0/0.0 (#65, #67; T:504) |
| `op_SCA.yaml`, `op_SCAS.yaml` | "Scale value (also PASM2)"; Unary | "Unsigned scale, (x * y) >> 32"; "Signed scale, (x * y) >> 30"; priority 7 (#48, #49); the PASM2 SCAS is a different operation — drop "also" |
| `op_shl`, `op_shr`, `op_SAR`, `op_ROR`, `op_ROL`, `op_REV`, `op_ZEROX`, `op_SIGNX` | "Bit manipulation" | per-row descriptions (#30-#37), priority 3, assign 17 |
| `op_add`, `op_sub`, `op_mul` | "Integer/float …" | `+` "Add" 8 (#51); `-` binary 8 (#53) and unary negate 2 (#18); `*` "Signed multiply" 7 (#41) |
| `op_adddot`, `op_subdot`, `op_muldot` | "Integer/float …" | float-only: `+.` 8, `-.` 8 and unary 2, `*.` 7; all blocks, no assign (#52, #54, #19, #42) |
| `op_divdot.yaml:4` | "Divide/float/modulo/unsigned" | "Floating-point divide", priority 7 (#44) |
| `op_max.yaml`, `op_min.yaml` | "Max/min limiting" | `#>` "Force x => y, signed" (#55); `<#` "Force x <= y, signed" (#56); priority 9 |
| `op_ternary.yaml:5` | category Assignment | Ternary; priority 16, all blocks (#79) |
| `op_inc.yaml`, `op_dec.yaml` | "…/random" | forms and priority 1, PUB/PRI only (#1, #2, #4, #5) |
| `op_assign.yaml` | "Assignment operator" | add multi-assign and `_`, priority 17, PUB/PRI only (#80) |
| `op_QLOG`, `op_QEXP` | "Quick logarithm / exponential" | table descriptions, priority 2 (#28, #29) (with S-026) |
| `op_SQRT`, `op_FSQRT`, `op_FABS` | "Math" | table descriptions (#26, #27, #21) |
| float compare pages (`op_lteqdot` …) | form right | add "returns 0 or -1", priority 11, all blocks |

`op_FRAC`, `op_div`, `op_divdiv`, `op_adddiv`, `op_lteqgt`, and the signed/unsigned compare pages
match REF (add priority and row only).

## F. `operators/op_addmodulo.yaml` (S-130, S-279)
24. `:20-25`, `:144-149`: re-point to REF row 47 and T:460.
25. `:48-52`: "(value % modulus) … Equivalent to value // modulus" → "unsigned remainder"; same as
    `//` only when both operands are below $8000_0000.
26. `:88`, `:105`, `:122`: `(head - tail) +// BUFFER_SIZE` "any buffer size works" — **probe:
    `-3 +// 30` = 13** (not 27), so it holds only for power-of-2 sizes; restrict the claim or rewrite.

## G. Other pages
27. `spin2-language-schema.yaml` (S-275): `:2`, `:19`, `:43-44`, `:427` (17 priorities), `:447`,
    `:450` (84 rows, 17 levels), `:73-77` block_usage enum vs REF scopes; `:47-51` associativity
    unsourced.
28. `guides/spin2-getting-started.yaml:287-311` (S-252): `:294` → `== <> < > <= >=`; `:299-300`
    logical `AND/&&  OR/||  XOR/^^  NOT/!!`, bitwise `& | ^ !`; `:311` → `var~` post-clear, `var~~`
    post-set, `var!!` post-logical-NOT.
29. `spin2-language-complete-map.yaml:49-62`: unsourced counts (74 / 72 / 100 %); `:60` float
    variants written `.+ .- .* ./` (they are `+. -. *. /.`). **New.**
30. `special-symbols/~.yaml:7`, `~~.yaml:7`: prefix `~flag` — **probe: `w := ~v` rejected (m172),
    `w := v~` accepted** (S-121) → `value := flag~  ' use flag then clear it`.
31. `special-symbols/at.yaml:21`: `block_usage: "All blocks"` vs REF "Term (PUB/PRI only)" (T:421);
    probe `CON x = @y` fails ("Undefined symbol").
32. `concepts/floating_point.yaml:73`: "returns TRUE/FALSE" → "returns 0 or -1" (Ref #61).
33. `op_rand.yaml:4-23`, `:135`, `:150`: algorithm, period and "2-9 cycles" unsourced (S-059,
    S-177); add priority 1, PUB/PRI only, `??var` (Ref #3).
34. Only `spin2-language-schema.yaml:19` and `op_addmodulo.yaml:21`, `:145` cite the old summary.

## H. Coverage gaps (note only — coverage work for the sprint)
35. No page: bitwise `!`, `&`, `^`, `|`; unary `-`; `\`; `=` (CON equate); compound assign forms;
    unary assign forms; postfix `~`, `~~`, `!!`, `!` as operator pages (special-symbols has `~`, `~~`).
36. Not gaps: FLOAT/ROUND/TRUNC (methods/), `@ @@ # ^@ ~ ~~` (special-symbols/), float compares,
    FRAC, `+//`, SCA, SCAS, POW family.
37. `op_swap.yaml` (`:=:`), `op_line_continuation.yaml` (`...`): outside the table; untouched.

## Arbiter probes (pnut-ts v1.55.8, 2026-10-09; `CON x = …` folded into a DAT long)
`-100 +/ 7` = 613566742 · `$A3 REV 7` = $C5 · `$A3 REV 8` = $18A · `4 ADDBITS 3` = 100 ·
`ENCOD 4` = 2 · `DECOD (ENCOD (5-1) + 1)` = 8 · `-3 +// 30` = 13 · `w := ~v` rejected (m172) ·
`w := v~` accepted · `CON x = @y` "Undefined symbol" · POW needs `{Spin2_v51}`; with it:
`3.0 POW 4.0` = 81.0, `2.0 POW 3.0 +. 1.0` = 9.0, `1.0 +. 3.0 POW 2.0` = 16.0,
`2.0 *. 3.0 POW 2.0` = 36.0, `2.0 POW 3.0 *. 2.0` = 64.0, `2.0 POW 3.0 POW 2.0` = 64.0.

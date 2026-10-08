# ENH-03 — the KB compile gate: design

**Status:** DESIGN, phase 1 of a two-phase task («#399»). Nothing is built. Nothing in
`deliverables/ai/P2/`, `engineering/ingestion/`, the skills or the tools was changed by this
pass. Phase 2 is the build tasks in §9, which implement these decisions without re-deciding them.
§11 lists what Stephen still has to rule on.

**Decided (Stephen, 2026-10-08):** ENH-03 is built first and stays a **permanent** part of the
release gate. It is a hard gate in `release-yamls` and an edit-time check in
`yaml-knowledge-base-maintenance` on the files touched. Register: ENH-03 in
`engineering/operations/P2KB-CORRECTION-FINDINGS.md` (the DECIDED note and its design points).
It is the parallel track of `engineering/analysis/2026-10-08-p2kb-close-out-study.md` §1.

**The prototype is gone.** The 2026-08-21 prototype is not anywhere in the repo, so this design
starts from the register's design points and from the measurements in §1. The only surviving
traces are the two ingestion READMEs that describe the same auto-declare technique and its
weakness (§4.3).

---

## 0. What the gate proves, and what it never proves

> **The gate proves LEGALITY only.** A pass means `pnut-ts` accepts the block in the context
> its manifest entry declares. It does **not** mean the code does what the surrounding text says,
> or that any P2 fact it states is right.

F-312 is the proof. Fixing `qvector y_val` so it assembles would have left X and Y swapped, and
the gate would have passed it. F-381 defines a correct example as one that **compiles AND agrees
with sourced facts on every P2 fact it states**. This gate answers the first half only.

That sentence is printed wherever the gate's result is read (§7.4). Everywhere else in this
document, "pass" means "legal".

---

## 1. Measurements this design rests on (2026-10-08)

Every number below comes from a scratch probe written for this design, run against the working
tree at `f3b0be9d`. The probes are **not** project tools and are not kept in the repo. Their
commands are in §12. Build task B1 re-measures the census with the real finder, and that number
replaces these.

### 1.1 Census, re-measured

| Quantity | Register (2026-08-21) | **Measured 2026-10-08** | Producer |
|---|---|---|---|
| YAML files under `deliverables/ai/P2/` | — | **1130** (0 parse errors) | `census.py` |
| Multi-line code-shaped blocks | 1913 in 438 files | **2148 in 490 files** | `census.py` TIER 2 |
| — by shape | — | 929 Spin2 with block keywords · 693 PASM2 · 526 Spin2 statements | `census.py` |
| — containing `debug(` | — | 146 | `census.py` |
| Distinct YAML key names that host them | — | **250** | `analyze2.py` |
| — under a code-named key (`code`, `example(s)`, `usage`, `template`, `implementation`, …) | — | 1389 | `census.py` |
| — under any other key (`description`, `wrong`, `correct`, `pattern`, `syntax`, …) | — | 759 | `census.py` |
| Strings under a code-named key, any shape | — | 2377 in 497 files (1492 multi-line, 885 single-line) | `census.py` TIER 3 |
| — multi-line ones the shape heuristic misses | — | 103 (incl. `#DEFINE`/`#IFDEF` preprocessor examples and shell commands) | `peek_single.py` |
| "Complete programs" | 118 | 831 program-shaped; **426** compile bare, exactly as written | `probe_compile.py` (full run) |

The register's heuristic is lost with the prototype, so the two columns are not like for like.
The 118 versus 426 gap is a difference of definition, not of content. The shape of the problem
is the same in both:

- **Key names do not say what is code.** Code lives under 250 different keys. 345 of the 759
  blocks outside code-named keys compile under some probe wrapper (`analyze2.py`), so a finder
  that reads only `code:`-like keys misses real code.
- **Shape does not say what is code either.** 398 of those 759 fail under every wrapper. The
  failures are dominated by fields such as `description`, `overview`, `rule` and `usage`, which
  is prose: the "166 of 541 were prose" finding, reproduced.

### 1.2 Compiler behaviour the design depends on (probe files `probe/p01`–`p13`)

| # | Probe | Result | Design consequence |
|---|---|---|---|
| a | Undefined symbol (`p01`) | `:3:error:Undefined symbol`. The error gives the **line only**, never the name, and stops at the first one | The compiler alone cannot say *which* name is undeclared (§4.3) |
| b | `pnut-ts --pass elementize --log elementizer -- f.spin2` (`p01`, `p05`) | Every identifier that is not a built-in is logged as `type_undefined, "NAME"` with `Ln#` and column. `DEBUG` is logged as `type_debug`. Each token's successor (`type_left` = `(`) is visible | **This is how we ask the compiler**, with no keyword list. Built-ins (`clkfreq`, `step`, mnemonics) are never `type_undefined` |
| c | Assumed names declared one per line **after** the block, colliding with a block label (`p02`) | `:13:error:Symbol is already defined (m540)`. Line 13 is the **wrapper's** declaration line | The collision can be pinned to exactly one symbol |
| d | Assumed names colliding with a method's parameters and locals (`p03`) | `:4:error:Expected a unique parameter name (m221)`. Line 4 is the **block's** `PUB` line | Collisions with locals land on a block line. The names to drop are the assumed names the elementizer saw on that line |
| e | Assumed name colliding with a method name (`p03`, first run) | `:14:error:Expected a unique name, BYTE, WORD, LONG, or assembly instruction` on the wrapper line | Same as (c), with different wording |
| f | `debug(udec(x), nonsense_token_here(x))` without `-d` (`p05`) | **Compiles** (6292-byte `.bin`) | Without `-d`, DEBUG content is not checked at all |
| g | The same file with `-d` | `:3:error:Expected an expression term (m172)` | `-d` is required to check DEBUG |
| h | Full probe: `-d` applied to every block | 3 legitimate low-clock blocks, none containing DEBUG, fail with `DEBUG requires at least 10 MHz of crystal/external clocking` (`asmclk.yaml`, `special-configuration-symbols.yaml` ×2) | `-d` cannot be blanket. Apply it **iff the block contains a `type_debug` token** (§6) |
| i | Inline PASM with assumed names as hub `DAT` longs (`p11`) | `Register cannot exceed $1FF` | Inline fragments assume names as **locals of the wrapper method** |
| j | The same as wrapper locals (`p10`) | Compiles | — |
| k | P1 `cognew(@driver, @params)` in a Spin2 wrapper (`p08`) | `Expected an instruction or variable` | An undefined **callee** must never be auto-declared. A stub would turn this into a pass |
| l | A lone P1 mnemonic (`waitcnt`) on an indented PASM line (`p09`) | **Compiles**, because it is a label to the assembler | A stated limit (§10) |
| m | `STRUCT` fragment, no directive | `"STRUCT" requires {Spin2_v45} or later` (14 blocks in the full probe) | The compiler names the version. A fragment wrapper adds `{Spin2_vNN}` on line 1 when its entry says so (`p12` compiles) |
| n | External `OBJ`, `FILE` and `#include` targets | `Cannot find jm_time_80.spin2` and similar; `File [utils.spin2] not found in #include (m630)` | An object or file the KB does not ship needs a declared stub (§4.4) |

### 1.3 Cost, measured

| Run | Blocks | Workers | Wall | Per item | Producer |
|---|---|---|---|---|---|
| Sample: every k-th program-shaped and fragment-shaped block | 120 | 1 | **43.0 s** | one `pnut-ts -q -d` compile: mean **0.077 s** (n = 437, max 0.101); one elementize pass: 0.071 s (n = 134); 0.36 s per block, averaged | `probe_compile.py … 60 60` |
| Full: every multi-line candidate, trying up to three wrappers each, with the iterative auto-declare | 2148 | 24 | **54.3 s** | 7546 compiles (mean 0.129 s under contention) + 2396 elementize passes | `probe_compile.py … 831 1317 24` |

**The register's "~0.8 s/block, ~25 min full sweep" is not reproduced.** One compile costs
0.077 s. The gate designed here does **one** compile per block (§4.2: the context is pinned in the
manifest, not searched for at gate time), so the gate costs less than the full probe, which
searched. The probe's 54.3 s at 24 workers is therefore an upper bound for about 2150 blocks on
this container (`nproc` = 24). One sequential compile per block would be about 0.077 s × N. That
figure is arithmetic, not a measurement. B4 measures the built gate on Stephen's machine and
records it.

**Constraint found:** `validate-dod-release.py` `_run_gate` kills an instrument after
`timeout=300`. So the gate runs its compiles in parallel (one worker per CPU), and B4 gives this
gate's runner call a timeout sized from the B4 measurement. It must never inherit 300 s blindly.

---

## 2. Decision 1 — where the classification lives: a SIDECAR manifest

The register asks for a per-block marker: `compile: program | fragment | never` plus a reason.
The question is where it lives.

| Criterion | Inline YAML key beside the block | **Sidecar manifest under `engineering/`** |
|---|---|---|
| **Close-out freeze**: nothing in `deliverables/ai/P2/` changes during the study (study §2) | ✗ About 3000 sites edited in the served tree mid-study (§1.1 candidate count) | ✓ The manifest is outside the served tree |
| **Delivery filter**: provenance-like keys must not be served | ✗ `compile` is not in `remove_fields` (handoff §3). Adding a name needs a KB release and the over-removal check, against the KB's stated preference (handoff §8.4). The format-1 engine does not strip a key that opens a list item (`- compile:` survives; handoff §4, "Exactness details"). 885 code strings are bare list items or single scalars with no sibling mapping to hold a key, so marking them would reshape served content | ✓ Never served: the index generator walks only `deliverables/ai/P2/` (`generate-p2kb-index.py:590`, `ai_path.rglob("*.yaml")`) |
| **Survival across YAML edits** | ✓ Moves with its block | Needs a stable address plus a fingerprint, and a reconciliation that fails loudly (§3.3) |
| Reviewability in the §1.5 change-set audit | Mixed into content hunks | ✓ Its own diff: every reclassification is a visible hunk |

**Decision: a sidecar manifest.** The first two criteria rule out inline keys outright: one is a
recorded freeze and the other is a published interface. Survival is the sidecar's only weakness,
and §3.3 turns every way it can go wrong into a gate failure rather than a silent drift.

**Absence check:** no KB file carries a `compile:` key today, so no name collides.
`grep -rn -E "^\s*-?\s*(compile|compiles|compile_status|compilation_result|syntax_validated)\s*:"
deliverables/ai/P2 --include=*.yaml` returns only `compilation_result`/`syntax_validated` in
`code-examples/` (the control hits) and no `compile:`.

**Layout:** one sidecar per KB file that has candidates, mirroring the tree:
`engineering/tools/validation/kb-compile-manifest/<kb-relative path>`. For example,
`…/kb-compile-manifest/language/pasm2/qvector.yaml`. Mirroring keeps each diff beside its YAML
change. It also makes a sidecar whose KB file was deleted trivially detectable (ORPHAN, §3.3) and
lets the edit-time check read just the touched files' sidecars. The gate script lives beside it as
`engineering/tools/validation/audit-kb-code-compiles.py` (the `audit-*.py` gate convention). Like
`audit-yaml-source-lock.py`, it derives the repo root from the working directory, never from its
own path.

**The manifest carries no compiler version** (PL-004, *cite the edition, never the build*). The
gate runs against whatever `pnut-ts` is installed, and a compiler bump that breaks a block turns
the gate red, which is the gate working.

---

## 3. Decision 2 — finding and addressing a block

### 3.1 The finder casts a net; the manifest decides

The census shows that neither key names nor shape separates code from prose (§1.1). So the finder
does not decide what is code. **It finds candidates, and every candidate must carry a manifest
decision**, including the decision that it is not code. A false positive costs one reviewed
`not-code` line, once (the fingerprint keeps it). A false negative is the real risk, so the net
favours recall:

1. **Every string scalar under a code-named key**, any length. The key list is **data in the
   manifest** (`kb-compile-manifest/_code-keys.yaml`), seeded from the census's host-key table and
   reviewed. It is not a compiler keyword list, and adding a key only widens the net.
2. **Every multi-line string scalar the compiler recognises as code-bearing.** The finder
   elementizes the string (§1.2 b) and takes it when any line opens with a token the compiler
   classes as a block keyword, an instruction, an assembler directive or `DEBUG`, or when any line
   contains an assignment operator. The compiler's own classes do the recognising, so the finder
   holds no keyword list. *Untested here:* whether the elementize pass still sees `#DEFINE`/`#IFDEF`
   lines or the preprocessor has already consumed them. B1 tests this. Either way, the census's
   preprocessor examples sit under code-named keys (they are among the 103 multi-line code-key
   strings the shape heuristic missed), so net 1 catches them.

**Outside the net, stated as a limit (§10):** single-line strings under non-code keys
(`syntax: QVECTOR {#}D,{#}S`, `instruction: QVECTOR`), which are notation; and inline code spans
inside prose (`` `if pin >= 0` ``).

### 3.2 Address

A block's address is **`<kb-relative file>` + `<YAML path>`**, for example
`language/pasm2/qvector.yaml` + `examples[1].code`. Mapping keys are joined with `.`, a sequence
index is `[n]`, and a key that does not match `^[A-Za-z0-9_-]+$` is written `["key"]`. A
multi-document file prefixes `#n:`. The finder walks the PyYAML node graph (`yaml.compose_all`),
the same way the census did, so each scalar also carries its start line for messages.

Messages report the scalar's YAML line and the **block-relative** line of the error. For a
literal block scalar (`|`) the two map one-to-one. For a quoted or folded scalar (`qvector.yaml`'s
examples are single-quoted multi-line strings) they do not, so both are printed.

### 3.3 Fingerprint and reconciliation: survival across edits

Each entry stores `fp`, the first 16 hex digits of the SHA-256 of the **parsed scalar value**.
Reflowing or requoting YAML without changing the code does not change it; changing the code does.
On every run, each file's entries are matched to its current candidates. The fingerprint is tried
first; the path settles ties, such as two identical blocks in one file:

| State | Meaning | Edit-time check | Release gate |
|---|---|---|---|
| MATCH | `fp` and `at` both current | assert the class | assert the class |
| MOVED | `fp` found at a different path (a sibling example was inserted above) | reported; `--refresh` rewrites `at` | **FAIL** until refreshed |
| CHANGED | same `at`, new `fp` | the **carried class is asserted on the new text**; if it holds, `--refresh` rewrites `fp` | **FAIL** until refreshed |
| UNCLASSIFIED | a candidate with no entry | **FAIL** | **FAIL** |
| ORPHAN | an entry whose block, or whose whole KB file, is gone | **FAIL**: deleting the entry records the removal | **FAIL** |

Carrying the class across a CHANGED block is safe, because every class is re-asserted on the new
text. Suppose the class attaches to the wrong block after a combined move-and-edit. A `never`
that lands on legal code compiles and fails; a `program` that lands on a fragment does not
compile and fails. Mis-attachment is loud.

`--refresh` never changes a class, and never adds an assumed name without `--accept-assumes NAME…`
naming it (§4.2). Class changes are hand edits to the sidecar, and they are audited (§8.2).

---

## 4. Decision 3 — giving a fragment its compile context

### 4.1 The entry

```yaml
# engineering/tools/validation/kb-compile-manifest/language/pasm2/qvector.yaml
# ENH-03 compile manifest. LEGALITY ONLY: a pass proves pnut-ts accepts the block in the
# context declared here, never that the code is correct (F-381, F-312).
blocks:
  - at: examples[1].code
    fp: 3f2a9c0d1e5b7a44
    compile: fragment
    wrap: pasm2-dat
    assumes: [x_coord, y_coord, magnitude, phase_angle]
  - at: syntax
    fp: 0b77e1c2a9d04f13
    compile: not-code
    reason: instruction-form notation; D and S/# are operand placeholders
```

Fields: `at`, `fp`, and `compile` (`program | fragment | never | not-code`) are always present.
`reason` is required for `never` and `not-code`. `wrap` and `assumes` are for fragments and
`never` blocks. The optional fields are `spin2_version` (adds `{Spin2_vNN}` on line 1),
`with: [<at>…]` (prepends sibling blocks of the same file, such as the `CON` block an example
relies on), `fails_at` (`never` only, §5) and `finding: F-NNN`. `finding` points at a registered
defect for reporting only. **It never changes the verdict**: a known-broken block stays
`program`/`fragment` and stays red until it is fixed. A broken example is never "parked" as
`never`.

`not-code` is the fourth value the register's three did not need. The register's three classes
cover code; `not-code` is how a candidate the net caught is excluded, with its reason (prose,
notation, a shell command, a listing, a table, terminal output).

### 4.2 Wrappers, and the context pinned in `assumes`

| `wrap` | Text the gate compiles | How each name in `assumes` is declared |
|---|---|---|
| *(none; `compile: program`)* | the block, byte for byte | none allowed: `assumes` must be empty. A program is what compiles **as shown** |
| `spin2-top` | the block as top-level Spin2, plus `PUB __kbgate()` appended when the compiler finds no `PUB`/`DAT` token (the 44 PRI-only/VAR-only "No PUB method or DAT block found" blocks in the full probe) | trailing `DAT name long 0`; `name=con` → trailing `CON name = 0`; `name()->R/N` → `PRI name(p1..pN) : r1..rR` stub; `obj.m(N)` → a generated stub object; `file:NAME` → an empty file in the temp dir |
| `spin2-method` | `PUB __kbgate()` + the block indented two spaces | as `spin2-top` |
| `pasm2-dat` | `DAT` / `org 0` + the block | trailing `DAT name long 0` (cog registers); `name=con` |
| `pasm2-hub` | `DAT` / `orgh` + the block | as `pasm2-dat` (untested in the probe; B2 tests it) |
| `pasm2-inline` | `PUB __kbgate() \| <assumed names as locals>` / `org` + the block indented / `end` | **locals only**: hub `DAT` longs fail (§1.2 i–j) |

**The design's central choice: the gate does not search for context; the manifest pins it.** At
gate time a fragment compiles **once**, with exactly its `assumes` list declared. The searching
(which names are undeclared, which collide, what kind each needs) happens only in the
**proposer** (`--propose`), and its output is reviewed before it enters the manifest. This buys
three things:

1. **A typo cannot become a pass.** An edit that misspells an operand (`P_ADC1X`) or slips in a
   P1 name (`cnt`) introduces a name that is not in `assumes`. The compile then fails with
   `Undefined symbol`, and accepting the name takes `--accept-assumes P_ADC1X`, a visible manifest
   hunk. In an un-pinned auto-declarer, every unknown operand is silently declared, and that hides
   exactly the defect class F-313 shipped (P1 `waitcnt`/`cnt`).
2. **Callees and objects are never invented at gate time.** §1.2 k shows `cognew(…)` failing
   correctly. A gate that auto-stubbed callees would pass it. A method stub exists only when a
   reviewer accepted it in `assumes`.
3. **The gate depends only on compile exit status and the first error line.** The elementizer
   log, a debug interface (§4.3), is used only by the proposer.

### 4.3 The proposer, and the fix for the prototype's collision defect

The prototype (the register) and the ingestion harnesses
(`engineering/ingestion/sources/silicon-doc/assets/code-2026-08-26/README.md:41`,
`…/pasm2-manual/assets/code-2026-08-26/README.md:36-37`) share one weakness. The compiler reports
an error line without naming the symbol, so the auto-declarer **guessed** which token was
undefined, declared names the block defines itself, and produced `Symbol is already defined` on
blocks that compile by hand. The fix has two parts, and both ask the compiler:

1. **Ask which names are undeclared.** Elementize the wrapped block (§1.2 b). The candidate set is
   every `type_undefined` name, with its line and its successor token. A name followed by `(` is a
   callee, and one followed by `.` is an object. Both are proposed as stubs **flagged for review**,
   never declared silently. Every other name is an operand.
2. **Attribute every collision exactly.** Emit the operand declarations **one per line, after the
   block**. Then compile, and loop:
   - a uniqueness error (`already defined`, `Expected a unique …`) **on a declaration line**: that
     line is one name, which the block defines itself, so drop it (§1.2 c, e);
   - a uniqueness error **on a block line** (a `PUB` header's parameters and locals, §1.2 d): drop
     the operand names the elementizer saw on that line;
   - any other error on a block line that holds assumed operands: move those names one step down
     the kind ladder (`DAT long` → `CON = 0`) and retry;
   - otherwise stop. The result is a **proposal**: the dropped names, the final `assumes`, and the
     outcome. The loop is bounded (|names| + 2 compiles); hitting the bound is `HARNESS`, never a
     pass.
   - For `pasm2-inline`, whose locals all sit on one header line, the block-defined names come
     from a preliminary `pasm2-dat` pass, where collisions are attributable.

**Evidence the attribution is the crux.** On the 120-block sample, a first probe run had the
declaration-line index off by one, so it dropped the neighbouring name instead of the colliding
one. That is the same failure shape as guessing. 38 of the 120 blocks ended as harness errors.
With exact attribution: **3 of 120**, all "No PUB method or DAT block found", which `spin2-top`'s
appended `PUB` resolves. Across all 2148 blocks, 1027 needed at least one collision drop, and 48
ended as harness outcomes: 44 PRI/VAR-only, 3 DEBUG-clock (§1.2 h, fixed by §6), and 1 a
`wrong:` example of conflicting clock symbols, which is a `never` candidate.

**The proposer's dependency on a debug log is guarded.** `--pass elementize` exits 1 with
`:1:error:LOOP EXCEEDED EMPTY BUFFER` **after** a complete token dump (§1.2 b). The proposer
ignores that exit status and reads the log. A self-check makes a format change loud: if the
compile reports `Undefined symbol` and the parsed log holds zero `type_undefined` tokens, the
proposer exits 2 ("cannot audit"). A stable machine interface (for example
`pnut-ts --list-undefined`) would retire the log parse. That is §11 Q4.

### 4.4 Objects, files and language level

- **External objects** (`OBJ ser : "jm_serial"`) are not in the KB. The proposer offers
  `obj.method(N)` stubs, generated into the temp dir. A pass then proves the **calling code**
  legal, and the gate's per-block output says the object's API was not checked.
- **`FILE` / `#include` targets** use `file:NAME`, an empty file in the temp dir.
- **Language level:** a fragment that needs `{Spin2_vNN}` declares `spin2_version: NN`. The
  proposer reads NN from the compiler's own "requires {Spin2_vNN}" message. A **program** never
  gets a directive added: a program that needs one and lacks it does not compile as shown, which
  is a defect.

### 4.5 Build artifacts

Outputs go to a temp directory outside the repo, which is removed afterwards. No `.bin` is ever
written into the working tree (an example `.bin` is never committed).

---

## 5. Decision 4 — `never` is asserted to fail, never skipped

The KB teaches anti-patterns. A `never` block is one **meant** not to compile: it teaches the
compile error.

- A `never` entry carries `reason` (what it teaches) and `fails_at`, the block-relative line the
  compiler must reject. It takes `wrap` and `assumes` like a fragment, so the **only** error left
  is the one it teaches.
- The gate compiles it and asserts **failure at `fails_at`**:
  - it compiles → **FAIL**, `NEVER-COMPILES`: the wrongness it teaches has been edited away;
  - it fails elsewhere, or inside the wrapper → **FAIL**, `NEVER-WRONG-REASON`: the teaching error
    may be gone while another remains.
- Asserting the line rather than the message text keeps a compiler's rewording from turning the
  gate red with no content change. The reason lives in `reason`, written for a human.
- **A `wrong:` key is not `never` by default.** Most wrong examples are legal code with wrong
  *behaviour* (F-312 is the type), and they are `program`/`fragment` and must compile. Only an
  example whose point is the compile error is `never`. Moving a block into `never` is an audited
  hunk (§8.2), because that move would otherwise be the cheapest way to silence a red gate.

---

## 6. Decision 5 — DEBUG compiles with `-d`

**Rule: compile with `pnut-ts -d` if and only if the wrapped block contains a `type_debug`
token.** The finder's elementize pass already yields that token, so the rule asks the compiler
and needs no keyword list.

- Without `-d`, garbage inside `debug()` compiles (§1.2 f). So `-d` is mandatory wherever DEBUG
  appears.
- Blanket `-d` falsely fails legal low-clock programs (§1.2 h: three in the KB today). So it is
  not blanket.
- A block that has DEBUG **and** a sub-10 MHz clock fails under `-d`, and that failure is real: its
  debug statements can never run.
- The negative controls pin both sides (§7.3 NC7, NC8).

---

## 7. Decision 6 — outputs, exit codes, negative controls

### 7.1 Modes

| Invocation | Used by | Does |
|---|---|---|
| `audit-kb-code-compiles.py` | §5.5 pre-flight (through `validate-dod-release.py`) | full sweep; release strictness (MOVED/CHANGED fail) |
| `--files F…` | edit-time check | same checks, on the touched files' blocks only |
| `--since REV` | §1.5 change-set audit | the files changed in `REV..HEAD`, plus the manifest diff over the range (§8.2) |
| `--propose --files F…` | classification work | prints proposals (wrap, assumes, flagged callees, outcome). **Never writes the manifest** |
| `--refresh --files F… [--accept-assumes N…]` | after an edit | rewrites `at`/`fp` for blocks that still pass under their class. Prints every change |
| `--negative-control` | DoD runner, before trusting a pass | §7.3 |
| `--json PATH` | any | a machine-readable result to a scratch path |

### 7.2 Output

One line per problem, verdict last, then the scope note, following the instruments the DoD runner
already parses (`_run_gate` reads a verdict line that starts with `PASS`/`FAIL`/`ERROR`):

```
FAIL              code-examples/smart-pins-002-button-reading.yaml:18  code_content.code  [program]  block line 5: Expected an instruction or variable
                  |   DIRL #BUTTON                  ' Make button pin an input
NEVER-COMPILES    language/…/foo.yaml:88  anti_patterns[1].wrong  [never/spin2-method]  expected to fail at block line 3; it compiles
STALE (CHANGED)   language/…/bar.yaml:40  examples[0].code  class still holds; run --refresh after review
UNCLASSIFIED      architecture/…/baz.yaml:120  patterns.x.code  candidate with no manifest entry
FAIL: 4 problems in 4 files — 1 FAIL, 1 NEVER-COMPILES, 1 STALE, 1 UNCLASSIFIED (<n> blocks: <p> program, <f> fragment, <v> never asserted to fail, <x> not-code)
LEGALITY ONLY: a pass means pnut-ts accepts each block in its declared context. It does not
mean the code does what its text says, or that any P2 fact in it is right (F-381: correct =
compiles AND agrees with sourced facts; this gate answers the first half only).
```

(The first line is a real block: §12 E-3.) The run also prints `pnut-ts --version` as run
context. That goes to stdout only and is never written into the manifest or the KB (PL-004).

**Exit codes:** `0` = every block holds its declared class, and nothing is stale, unclassified or
orphaned. `1` = any problem line. `2` = cannot audit: `pnut-ts` not on PATH, the KB tree or the
manifest unreadable, a YAML parse failure, or the proposer self-check (§4.3). "Nothing audited" is
never a pass. A run that finds zero candidates exits 2.

### 7.3 Negative controls (`--negative-control`, all synthetic)

The controls are **synthesized at run time in a temp dir** (a scratch YAML plus a scratch
sidecar), the way the existing instruments mutate a scratch copy. Live KB blocks are not used as
controls, because the close-out will fix them. Each control asserts its expected outcome, and the
run prints `NEGATIVE CONTROL: PASS` only if all of them hold:

| NC | Planted | Must be |
|---|---|---|
| 1 | known-bad `program`: a PASM `DIRL #PIN` written as a Spin2 statement (the smart-pins-002 shape) | FAIL |
| 2 | known-good `program` | PASS |
| 3 | `never` block that compiles | FAIL (`NEVER-COMPILES`) |
| 4 | `never` block failing on a line other than `fails_at` | FAIL (`NEVER-WRONG-REASON`) |
| 5 | fragment defining its own label and method parameters (the collision shape) with a correct `assumes` | PASS |
| 6 | fragment calling P1 `cognew(…)`, nothing assumed | FAIL |
| 7 | `debug()` holding a garbage term | FAIL (proves `-d` is applied) |
| 8 | legal `_rcslow` program with no DEBUG | PASS (proves `-d` is not blanket) |
| 9 | fragment edited to use a new undeclared operand | FAIL (proves `assumes` is pinned) |
| 10 | candidate with no entry · entry with stale `fp` (release mode) · orphan entry | FAIL ×3 |
| 11 | `pnut-ts` replaced by an empty `PATH` | exit 2 |

### 7.4 Where "legality only" is said

1. The gate's stdout, after the verdict (above).
2. `validate-dod-release.py`, as a `result.info("Scope: …")` line, like the constant-fidelity gate.
3. `release-yamls` "What a green gate does NOT certify": a new paragraph (§10).
4. `yaml-knowledge-base-maintenance` §2.6 (§8.3).
5. Each sidecar's header comment (§4.1).
6. Release notes and CHANGELOG: "every code block compiles as declared", never "examples
   verified" or "correct".

---

## 8. Decision 7 — wiring, and cost

### 8.1 Hard gate in `release-yamls` §5.5 (through the DoD runner)

- `validate-dod-release.py` gains `validate_kb_code_compiles()`. It runs `--negative-control`
  first, then the full sweep, through `_run_gate`, so exit 1 and exit 2 both fail the release.
  The scope line from §7.4 goes in it. Its timeout is sized from B4's measurement (§1.3
  constraint).
- `release-yamls` §5.5's command list names the gate (as it names the constant and sourcing
  instruments) and §1's precondition list adds it as BLOCKING.
- `audit-gate-arming.py` then sees the gate invoked by a RUNNER. Without that wiring the meta-gate
  would rightly report it UNWIRED.

### 8.2 The §1.5 change-set audit standing check

This replaces *"Every changed code example compiles (the ENH-03 compile gate, once built)"*:

- `audit-kb-code-compiles.py --since "$PREV"` is clean;
- **the manifest diff over the range is audited like YAML hunks**:
  `git diff "$PREV"..HEAD -- engineering/tools/validation/kb-compile-manifest/`. Every
  reclassification **into `never` or `not-code`**, every new `assumes` name, and every deleted
  entry is a hunk that must be wanted, warranted and justified. Those are the three ways to quiet
  the gate without fixing code, so they are where auditors look.

### 8.3 Edit-time check in `yaml-knowledge-base-maintenance`

A new **§2.6 "Compile the code you touched"**, run after §2.5's format check, with
`--files <edited YAMLs>`:

- any FAIL is fixed in the same pass (the KB rule: *what we see wrong we fix in the same pass*);
- CHANGED/MOVED → review, then `--refresh`. A new name needs `--accept-assumes`;
- UNCLASSIFIED → `--propose`, review, then add the entry;
- the §5 hand-back reports the gate's result with its legality-only line.

Cost at edit time is one compile per block in the touched files, so seconds (§1.3).

---

## 9. Decision 8 — build order

The register's order is (1) markers, (2) collision fix, (3) wire, (4) corrections under it. This
design keeps all four steps but splits (1). The marker's **home** (schema, finder, addresses) is
built first. **Populating** the markers moves after the collision fix, because classification is
proposed by the harness and reviewed. The register itself says not to trust a pass rate until the
collision is fixed. §11 Q1 asks Stephen to confirm this reordering.

| # | Task | Delivers | Done when |
|---|---|---|---|
| **B1** | Manifest home, finder, address, reconciliation (no compiling yet) | `audit-kb-code-compiles.py` (finder, addresses, `fp`, MATCH/MOVED/CHANGED/UNCLASSIFIED/ORPHAN); the empty `kb-compile-manifest/` tree with `_code-keys.yaml` seeded from the census host-key table; the schema in the script's docstring. **The re-measured census, written into the register's ENH-03 entry** (it replaces "1913 / 438 / 118") | NC10 passes; the census is in the register |
| **B2** | Harness and proposer, with the collision fix | the wrappers of §4.2, the `assumes` kinds and stubs, the `-d` rule, `never` assertion, outputs and exit codes, `--propose`/`--refresh`/`--since`, the full `--negative-control` | `NEGATIVE CONTROL: PASS` on all 11 NCs; a proposer run over every candidate, with its HARNESS count reported |
| **B3** | Populate the markers | proposals for every candidate, reviewed by fresh agents per directory, and the arbiter checks each returned claim. Sidecars written. **Every block that fails as `program`/`fragment` becomes a register finding** (by defect class, with its sites). Nothing in the served tree is edited (the study freeze) | zero UNCLASSIFIED; every failure has an F-number in `finding:`; the release gate is red **only** on registered defects |
| **B4** | Wire it | §8.1–§8.3 edits to `validate-dod-release.py`, `release-yamls` (§1, §1.5, §5.5, "What a green gate does NOT certify") and `yaml-knowledge-base-maintenance` (§2.6, §5); the full sweep's wall time measured on Stephen's machine and recorded in the register entry | `audit-gate-arming.py` shows it wired; the DoD run includes it |
| *(B5)* | *Not ENH-03:* the close-out corrections, made under the gate | fixes to the B3 findings; F-381's "compiles" reading | the gate is green before the close-out release |

B3 is the large one (about 3000 candidates, §1.1). B1, B2 and B4 are tooling of ordinary size.
B4 can run alongside B3 once B2 is done, because wiring a gate that is red only on registered
defects is correct: no release happens before the close-out.

---

## 10. What a green gate does NOT certify (carried into `release-yamls`)

- **Behaviour or facts:** legality only (§0).
- **Context is assumed, not proven.** A fragment compiles **given** its `assumes` declarations. A
  reviewer accepted each name, and no tool checked that the name is a sensible placeholder rather
  than a P1 or misspelled built-in.
- **External object APIs:** a stubbed `ser.str(…)` proves the call legal, not that the object has
  that method.
- **A lone word on a PASM line is a label.** `waitcnt` alone on a line compiles (§1.2 l).
- **Outside the net:** single-line strings under non-code keys (notation), and inline code spans
  in prose (§3.1).
- **The installed compiler only.** A pass is a statement about the `pnut-ts` that ran.

---

## 11. Open decisions — SETTLED by the arbiter 2026-10-08 (design APPROVED)

None of the four changes what the KB *is* (D8). Each is a how-to-build call inside a gate Stephen
has already ordered, so it falls in the agent's lane (*The KB gate is total … which files and in
what order is the agent's lane*). They are recorded here, with reasons, for him to see:

1. **Build order B1 → B2 → B3 → B4: CONFIRMED.** Populating markers before the collision fix
   would classify from a harness whose pass rate cannot be trusted, which the register itself
   forbids.
2. **Pinned `assumes`: ADOPTED.** It costs a reviewed name list per fragment. In return, a typo or
   a P1 name can never pass silently (the F-313 class). Correct over fast.
3. **The net's limit: ACCEPTED.** Single-line `syntax:`/`instruction:` strings are operand
   notation, not compilable code, and the limit is stated in §10.
4. **Stable compiler interface: FILED** on `DRAFTS/PNUT-TS-PUNCH-LIST.md`, together with the
   elementize pass's `LOOP EXCEEDED EMPTY BUFFER` exit. Neither blocks the build.

*The original questions, kept for the record:*

1. **Build order.** Confirm B1 (marker home) → B2 (collision fix) → B3 (populate markers) → B4
   (wire), which splits the register's step (1) around step (2) (§9).
2. **Pinned `assumes`.** It costs a reviewed name list on every fragment (about 1800). In return,
   a typo or a P1 name cannot silently pass (§4.2). The alternative, auto-declaring at gate time,
   is cheaper and hides the F-313 class. Recommended: pin.
3. **The net's limit.** Single-line strings under non-code keys stay outside it (§3.1). The
   alternative is to classify the 9389 single-line shape hits too, which are mostly `syntax:` and
   `instruction:` notation (`census.py` tier 1: 11537 shape hits, minus the 2148 multi-line ones).
   Recommended: accept the limit.
4. **A stable compiler interface.** A `pnut-ts` option that lists undeclared identifiers (or
   emits a JSON symbol report) would replace the proposer's elementizer-log parse. It would go to
   `DRAFTS/PNUT-TS-PUNCH-LIST.md`. Not needed to build: only the proposer reads the log, and it is
   self-checked.

---

## 12. Evidence trail

The scratch probes lived in the session scratchpad
`$S = /tmp/claude-1000/-workspaces-P2-Knowledge-Base/fd20d1c1-e1ec-45fc-a5bc-7f395c46f9e1/scratchpad`.
They are not kept. B1 re-measures with the real finder.

- Census: `python3 $S/census.py deliverables/ai/P2 $S/census`, then
  `python3 $S/peek_single.py $S/census/census.json`.
- Sample cost (1 worker): `python3 $S/probe_compile.py $S/census/census-ml.json $S/probe-run 60 60`,
  then `python3 $S/analyze.py $S/probe-run/probe-results.json`.
- Full probe (24 workers): `python3 $S/probe_compile.py $S/census/census-ml.json $S/probe-full 831 1317 24`,
  then `python3 $S/analyze2.py $S/census/census-ml.json $S/probe-full/probe-results.json`.
- Compiler behaviour: `pnut-ts -q [-d] $S/probe/pNN_*.spin2`, and
  `pnut-ts --pass elementize --log elementizer -- $S/probe/p01_undef.spin2`.
- E-1: `pnut-ts -q $S/probe/p13_sp001.spin2` (`code-examples/smart-pins-001-basic-io.yaml:18`).
- E-2: `deliverables/ai/P2/architecture/smart-pins/smart-pin-01010-pwm-smps.yaml:40`
  (`dirh(v_sense)` at YAML line 51; `probe_compile.py` reports block line 11, "Expected an
  instruction or variable").
- E-3: `pnut-ts -q $S/probe/p04_sp002.spin2` (`code-examples/smart-pins-002-button-reading.yaml:18`).

E-1 to E-3 are blocks that do not compile. E-1 and E-3 also carry a served
`compilation_result: "success"`. They were **not** filed here: a correction goes through the
register only, and this task writes one file. They were handed to the arbiter for the register.

# YAML Knowledge Base Audit: PNut V46-V52 Language Updates

**Audit Date**: 2026-01-13
**Source Files**: V46_LANGUAGE_REFERENCE_ADDITIONS.md through V52_LANGUAGE_REFERENCE_ADDITIONS.md
**Auditor**: Claude (Opus 4.5)
**Knowledge Base Path**: `/workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/`

---

## Executive Summary

The P2 Knowledge Base contains **2,034 YAML files** documenting Spin2/PASM2 language features. This audit identifies gaps between the current YAML collection and the new features introduced in PNut versions 46-52.

| Version | New Features | Already Exist | Need Update | Need Creation |
|---------|--------------|---------------|-------------|---------------|
| V46 | 11 | 8 | 2 | 1 |
| V47 | 16 | 7 | 0 | 9 |
| V48 | 1 | 0 | 0 | 1 |
| V49 | 2 | 1 | 1 | 0 |
| V50 | 9 | 2 | 3 | 4 |
| V51a | 8 | 0 | 0 | 8 |
| V52 | 6 | 0 | 2 | 4 |
| **TOTAL** | **53** | **18** | **8** | **27** |

---

## Version Directive Requirements

### Critical: Not All Features Require Directives

**IMPORTANT**: Only SOME features require a `{Spin2_vXX}` version directive. Many features are simply available when using the appropriate compiler version - no directive needed.

**Format**: `{Spin2_vXX}` where XX is the minimum version number

---

### Features REQUIRING Version Directives (Gated)

These features will NOT compile without the directive at the start of the source file:

| Version | Directive | Gated Features |
|---------|-----------|----------------|
| V44 | `{Spin2_v44}` | BYTESWAP, WORDSWAP, LONGSWAP, BYTECOMP, WORDCOMP, LONGCOMP, FILL, COPY, SWAP, COMP, BOOL/BOOL_ debug |
| V45 | `{Spin2_v45}` | STRUCT, SIZEOF |
| V46 | `{Spin2_v46}` | C_Z debug formatter |
| V47 | `{Spin2_v47}` | TASKSPIN, TASKNEXT, TASKSTOP, TASKHALT, TASKCONT, TASKCHK, TASKID, NEWTASK, THISTASK, TASKHLT |
| V50 | `{Spin2_v50}` | DITTO directive only |
| V51 | `{Spin2_v51}` | POW, LOG2, EXP2, LOG10, EXP10, LOG, EXP |
| V52 | `{Spin2_v52}` | ENDIANL, ENDIANW, DEBUG_END_SESSION |

---

### Features NOT Requiring Directives (Compiler-Version Only)

These features work with the appropriate compiler version - NO directive needed:

| Version | Non-Gated Features |
|---------|-------------------|
| V46 | :=: swap operator, DEBUG_MASK, Pointer types (^BYTE, ^WORD, ^LONG) |
| V47 | Preprocessor (#DEFINE, #UNDEF, #IFDEF, #IFNDEF, #ELSE, #ENDIF, etc.), Conditional DEBUG in PASM (IF_x DEBUG) |
| V48 | External preprocessor symbols (-D command line) |
| V49 | Structure export/import, object.struct_t syntax, compiler limits |
| V50 | Escape strings (@\"...\"), ORGH inline assembly, Register constants in CON, PLOT LAYER/CROP, $$ as DITTO index |
| V52 | MOVBYTS function, NEXT level, QUIT level |

---

### YAML Field Requirements

**For GATED features** - Include version fields:

```yaml
requires_version: "Spin2_v51"
version_directive: "{Spin2_v51}"

description: |
  Feature description here.
  REQUIRES: {Spin2_v51} or later version directive at start of source file.

examples:
  - code: |
      {Spin2_v51}                        ' REQUIRED directive
      PUB main() | x
        x := LOG2(8.0)

notes:
  - "REQUIRES {Spin2_v51} or later at start of source file"
```

**For NON-GATED features** - Note compiler version only:

```yaml
minimum_version: "v47"

description: |
  Feature description here.
  Available in PNut/pnut_ts v47 and later compilers. No version directive required.

examples:
  - code: |
      ' No version directive needed - just use v47+ compiler
      #IFDEF DEBUG_MODE
        debug("Debug enabled")
      #ENDIF

notes:
  - "Available in v47+ compilers - no version directive required"
```

---

### Reference

See `VERSION_GATED_FEATURES_REFERENCE.md` for the complete official list from the Spin2 language reference source.

---

## Detailed Audit Results

### V46 Features

| Feature | Type | Gated? | Status | File Path | Action |
|---------|------|--------|--------|-----------|--------|
| STRUCT keyword | Keyword | **YES v45** | EXISTS | `spin2/keywords/STRUCT.yaml` | UPDATE (version note says v45, doc says v46) |
| SIZEOF operator | Method | **YES v45** | EXISTS | `spin2/methods/sizeof.yaml` | UPDATE (add v51a restrictions) |
| :=: swap operator | Operator | NO | EXISTS | `spin2/operators/op_swap.yaml` | UPDATE (expand documentation) |
| BYTESWAP method | Method | **YES v44** | EXISTS | `spin2/methods/byteswap.yaml` | OK |
| BYTECOMP method | Method | **YES v44** | EXISTS | `spin2/methods/bytecomp.yaml` | OK |
| WORDSWAP method | Method | **YES v44** | EXISTS | `spin2/methods/wordswap.yaml` | OK |
| WORDCOMP method | Method | **YES v44** | EXISTS | `spin2/methods/wordcomp.yaml` | OK |
| LONGSWAP method | Method | **YES v44** | EXISTS | `spin2/methods/longswap.yaml` | OK |
| LONGCOMP method | Method | **YES v44** | EXISTS | `spin2/methods/longcomp.yaml` | OK |
| DEBUG_MASK constant | Constant | NO | MISSING | - | CREATE `spin2/constants/debug-mask.yaml` |
| Pointer types (^TYPE) | Syntax | NO | PARTIAL | In STRUCT.yaml | OK (documented in STRUCT) |
| C_Z debug | DEBUG | **YES v46** | MISSING | - | CREATE `spin2/debug-commands/c-z.yaml` |

### V47 Features

| Feature | Type | Gated? | Status | File Path | Action |
|---------|------|--------|--------|-----------|--------|
| #DEFINE | Preprocessor | NO | MISSING | - | CREATE `spin2/preprocessor/define.yaml` |
| #UNDEF | Preprocessor | NO | MISSING | - | CREATE `spin2/preprocessor/undef.yaml` |
| #IFDEF | Preprocessor | NO | MISSING | - | CREATE `spin2/preprocessor/ifdef.yaml` |
| #IFNDEF | Preprocessor | NO | MISSING | - | CREATE `spin2/preprocessor/ifndef.yaml` |
| #ELSEIFDEF | Preprocessor | NO | MISSING | - | CREATE `spin2/preprocessor/elseifdef.yaml` |
| #ELSEIFNDEF | Preprocessor | NO | MISSING | - | CREATE `spin2/preprocessor/elseifndef.yaml` |
| #ELSE | Preprocessor | NO | MISSING | - | CREATE `spin2/preprocessor/else.yaml` |
| #ENDIF | Preprocessor | NO | MISSING | - | CREATE `spin2/preprocessor/endif.yaml` |
| TASKSPIN | Method | **YES v47** | EXISTS | `spin2/methods/taskspin.yaml` | VERIFY version fields |
| TASKSTOP | Method | **YES v47** | EXISTS | `spin2/methods/taskstop.yaml` | VERIFY version fields |
| TASKHALT | Method | **YES v47** | EXISTS | `spin2/methods/taskhalt.yaml` | VERIFY version fields |
| TASKCONT/TASKRESUME | Method | **YES v47** | EXISTS | `spin2/methods/taskresume.yaml` | VERIFY version fields |
| TASKCHK | Method | **YES v47** | EXISTS | `spin2/methods/taskchk.yaml` | VERIFY version fields |
| TASKID | Method | **YES v47** | EXISTS | `spin2/methods/taskid.yaml` | VERIFY version fields |
| TASKNEXT | Method | **YES v47** | EXISTS | `spin2/methods/tasknext.yaml` | VERIFY version fields |
| NEWTASK | Constant | **YES v47** | MISSING | - | CREATE `spin2/constants/newtask.yaml` |
| THISTASK | Constant | **YES v47** | MISSING | - | CREATE `spin2/constants/thistask.yaml` |
| TASKHLT | Register | **YES v47** | MISSING | - | CREATE `spin2/registers/taskhlt.yaml` |
| Conditional DEBUG (PASM) | PASM | NO | MISSING | - | CREATE `pasm2/conditional-debug.yaml` |

### V48 Features

| Feature | Type | Gated? | Status | File Path | Action |
|---------|------|--------|--------|-----------|--------|
| External preprocessor symbols | Compiler | NO | MISSING | - | CREATE `spin2/preprocessor/external-symbols.yaml` |

### V49 Features

| Feature | Type | Gated? | Status | File Path | Action |
|---------|------|--------|--------|-----------|--------|
| Structure export/import | Syntax | NO | PARTIAL | In STRUCT.yaml | UPDATE `spin2/keywords/STRUCT.yaml` |
| object.struct_t syntax | Syntax | NO | PARTIAL | In STRUCT.yaml | UPDATE (add section) |

### V50 Features

| Feature | Type | Gated? | Status | File Path | Action |
|---------|------|--------|--------|-----------|--------|
| Escape strings (@\"...\") | Syntax | NO | MISSING | - | CREATE `spin2/constructs/escape-strings.yaml` |
| Conditional DEBUG (PASM) | PASM | NO | MISSING | - | CREATE (covered in V47 task) |
| DITTO directive | Directive | **YES v50** | EXISTS | `spin2/assembly-directives/ditto.yaml` | OK |
| $$ DITTO index | Symbol | (within DITTO) | PARTIAL | `spin2/special-symbols/double_dollar.yaml` | UPDATE (add DITTO context) |
| ORGH inline assembly | Directive | NO | PARTIAL | `spin2/assembly-directives/orgh.yaml` | UPDATE (add inline usage) |
| Register constants in CON | Syntax | NO | MISSING | - | CREATE `spin2/constructs/register-constants.yaml` |
| PLOT LAYER command | Debug | NO | MISSING | - | UPDATE `spin2/debug-displays/plot.yaml` |
| PLOT CROP command | Debug | NO | MISSING | - | UPDATE (same file) |

### V51a Features

| Feature | Type | Gated? | Status | File Path | Action |
|---------|------|--------|--------|-----------|--------|
| LOG2 function | Operator | **YES v51** | MISSING | - | CREATE `spin2/methods/log2.yaml` |
| LOG10 function | Operator | **YES v51** | MISSING | - | CREATE `spin2/methods/log10.yaml` |
| LOG function | Operator | **YES v51** | MISSING | - | CREATE `spin2/methods/log.yaml` |
| EXP2 function | Operator | **YES v51** | MISSING | - | CREATE `spin2/methods/exp2.yaml` |
| EXP10 function | Operator | **YES v51** | MISSING | - | CREATE `spin2/methods/exp10.yaml` |
| EXP function | Operator | **YES v51** | MISSING | - | CREATE `spin2/methods/exp.yaml` |
| POW operator | Operator | **YES v51** | MISSING | - | CREATE `spin2/operators/op_POW.yaml` |
| SIZEOF restrictions | Method | (see v45) | EXISTS | `spin2/methods/sizeof.yaml` | UPDATE (add restrictions note) |

### V52 Features

| Feature | Type | Gated? | Status | File Path | Action |
|---------|------|--------|--------|-----------|--------|
| MOVBYTS function | Method | NO | MISSING | - | CREATE `spin2/methods/movbyts.yaml` |
| ENDIANL function | Method | **YES v52** | MISSING | - | CREATE `spin2/methods/endianl.yaml` |
| ENDIANW function | Method | **YES v52** | MISSING | - | CREATE `spin2/methods/endianw.yaml` |
| NEXT level | Keyword | NO | EXISTS | `spin2/keywords/NEXT.yaml` | UPDATE (add level param) |
| QUIT level | Keyword | NO | EXISTS | `spin2/keywords/QUIT.yaml` | UPDATE (add level param) |
| DEBUG_END_SESSION | Constant | **YES v52** | MISSING | - | CREATE `spin2/constants/debug-end-session.yaml` |

---

## Sprint Plan

### Sprint Overview

| Sprint | Focus | Files | Est. Effort |
|--------|-------|-------|-------------|
| Sprint 1 | Preprocessor System | 10 files | High |
| Sprint 2 | V51a Math Functions | 8 files | Medium |
| Sprint 3 | V52 Features | 6 files | Medium |
| Sprint 4 | Updates & Fixes | 8 files | Medium |
| Sprint 5 | Debug & Misc | 4 files | Low |
| Release | Validation & Index | - | Low |

---

### Sprint 1: Preprocessor System (V47-V48)

**Priority**: Critical (foundational feature)
**New Directory**: `spin2/preprocessor/`

#### Tasks

1. **Create directory structure**
   - Create `spin2/preprocessor/` directory
   - Create `spin2/preprocessor/preprocessor-overview.yaml` (system overview)

2. **Create preprocessor directive YAMLs** (8 files)
   - `define.yaml` - #DEFINE directive
   - `undef.yaml` - #UNDEF directive
   - `ifdef.yaml` - #IFDEF directive
   - `ifndef.yaml` - #IFNDEF directive
   - `elseifdef.yaml` - #ELSEIFDEF directive
   - `elseifndef.yaml` - #ELSEIFNDEF directive
   - `else.yaml` - #ELSE directive
   - `endif.yaml` - #ENDIF directive

3. **Create external symbols YAML** (V48)
   - `external-symbols.yaml` - Command-line -D option

4. **Create PASM conditional DEBUG YAML**
   - `pasm2/conditional-debug.yaml` - IF_x DEBUG syntax (NOT gated)

5. **Create V47 gated constants/registers** (3 files)
   - `spin2/constants/newtask.yaml` - NEWTASK constant (-1)
   - `spin2/constants/thistask.yaml` - THISTASK constant (-1)
   - `spin2/registers/taskhlt.yaml` - TASKHLT register

6. **Verify version fields on existing TASK* YAMLs** (7 files)
   - Ensure `requires_version: "Spin2_v47"` and `version_directive: "{Spin2_v47}"` present
   - Files: taskspin.yaml, tasknext.yaml, taskstop.yaml, taskhalt.yaml, taskresume.yaml, taskchk.yaml, taskid.yaml

#### Acceptance Criteria
- All preprocessor YAMLs created with complete syntax, examples, and cross-references
- **Preprocessor directives are NOT gated** - use `minimum_version: "v47"` (no directive required)
- **TASK* methods/constants/registers ARE gated** - include `requires_version: "Spin2_v47"`
- Examples show preprocessor usage WITHOUT version directive (just needs v47+ compiler)
- TASK* examples show WITH version directive (required)
- Schema validation passes
- Cross-reference validation passes

---

### Sprint 2: V51a Math Functions

**Priority**: High (commonly needed for engineering applications)

#### Tasks

1. **Create floating-point math function YAMLs** (6 files)
   - `spin2/methods/log2.yaml` - Base-2 logarithm
   - `spin2/methods/log10.yaml` - Base-10 logarithm
   - `spin2/methods/log.yaml` - Natural logarithm
   - `spin2/methods/exp2.yaml` - 2^x exponential
   - `spin2/methods/exp10.yaml` - 10^x exponential
   - `spin2/methods/exp.yaml` - e^x exponential

2. **Create POW operator YAML**
   - `spin2/operators/op_POW.yaml` - x^y binary operator

3. **Update SIZEOF restrictions**
   - Update `spin2/methods/sizeof.yaml` - Add V51a restrictions note

#### Acceptance Criteria
- All 7 new YAMLs created with bytecode references
- **LOG/EXP/POW ARE gated** - include `requires_version: "Spin2_v51"` and `version_directive: "{Spin2_v51}"`
- All code examples begin with `{Spin2_v51}` directive (REQUIRED for these features)
- SIZEOF updated with restriction note
- Examples demonstrate floating-point usage
- Cross-references to CORDIC functions (QLOG, QEXP)

---

### Sprint 3: V52 Features

**Priority**: High (newest features)

#### Tasks

1. **Create byte manipulation function YAMLs** (3 files)
   - `spin2/methods/movbyts.yaml` - Byte rearrangement
   - `spin2/methods/endianl.yaml` - 32-bit endian swap
   - `spin2/methods/endianw.yaml` - 16-bit endian swap

2. **Update flow control keywords** (2 files)
   - Update `spin2/keywords/NEXT.yaml` - Add level parameter
   - Update `spin2/keywords/QUIT.yaml` - Add level parameter

3. **Create DEBUG_END_SESSION constant**
   - `spin2/constants/debug-end-session.yaml`

#### Acceptance Criteria
- All 3 new method YAMLs include quaternary pattern documentation
- **ENDIANL, ENDIANW, DEBUG_END_SESSION ARE gated** - include `requires_version: "Spin2_v52"` and `version_directive: "{Spin2_v52}"`
- **MOVBYTS is NOT gated** - use `minimum_version: "v52"` (no directive required)
- **NEXT/QUIT level are NOT gated** - use `minimum_version: "v52"` (no directive required)
- Gated feature examples include `{Spin2_v52}` directive
- Non-gated feature examples note "v52+ compiler required, no directive needed"
- Bytecode references included

---

### Sprint 4: Updates & Fixes

**Priority**: Medium (improving existing documentation)

#### Tasks

1. **Update STRUCT.yaml**
   - Verify version directive (v45 vs v46)
   - Add V49 structure export/import section
   - Add object.struct_t syntax

2. **Update op_swap.yaml**
   - Expand from minimal stub to full documentation
   - Add atomic behavior notes
   - Add structure swap examples

3. **Update ORGH.yaml**
   - Add V50 ORGH inline assembly in Spin2 methods
   - Add END block requirement
   - Add comparison table (ORG vs ORGH)

4. **Update double_dollar.yaml ($$)**
   - Add DITTO iteration index context
   - Clarify dual meaning (address vs DITTO index)

5. **Update plot.yaml**
   - Add V50 PLOT LAYER command
   - Add V50 PLOT CROP command
   - Add bitmap layer examples

#### Acceptance Criteria
- All 5 updates made with version annotations
- **STRUCT/SIZEOF are gated** - keep existing `requires_version` fields
- **ORGH inline, PLOT LAYER/CROP are NOT gated** - use `minimum_version` field
- **$$ DITTO context is gated** (DITTO itself requires `{Spin2_v50}`)
- New sections clearly marked: "REQUIRES {Spin2_vXX}" for gated, "v50+ compiler" for non-gated
- Updated examples show directive only where required
- No breaking changes to existing content

---

### Sprint 5: Debug & Miscellaneous

**Priority**: Low (edge cases and debug features)

#### Tasks

1. **Create DEBUG_MASK constant** (V46)
   - `spin2/constants/debug-mask.yaml` (NOT gated)

2. **Create C_Z debug formatter** (V46)
   - `spin2/debug-commands/c-z.yaml` - Output C and Z flag states (**GATED v46**)

3. **Create escape strings construct** (V50)
   - `spin2/constructs/escape-strings.yaml`
   - Document all escape sequences (\n, \t, \x00, etc.) (NOT gated)

4. **Create register constants construct** (V50)
   - `spin2/constructs/register-constants.yaml`
   - INA, INB, OUTA, OUTB, DIRA, DIRB in CON blocks (NOT gated)

#### Acceptance Criteria
- All 4 new YAMLs created with appropriate version fields:
  - **DEBUG_MASK is NOT gated** - use `minimum_version: "v46"` (no directive needed)
  - **C_Z debug IS gated** - use `requires_version: "Spin2_v46"` (directive required)
  - **Escape strings are NOT gated** - use `minimum_version: "v50"` (no directive needed)
  - **Register constants are NOT gated** - use `minimum_version: "v50"` (no directive needed)
- Escape sequence table is complete
- C_Z examples include `{Spin2_v46}` directive
- Other examples note compiler version requirement without directive
- Examples show real-world usage

---

### Release Phase

**Priority**: Required

#### Tasks

1. **Run schema validation**
   ```bash
   python tools/validate-yaml-schema.py
   ```

2. **Run cross-reference validation**
   ```bash
   python validate-crossref-keys.py
   ```

3. **Regenerate index**
   ```bash
   python generate-p2kb-index.py
   ```

4. **Run release validation**
   ```bash
   python validate-dod-release.py
   ```

5. **Create version manifest**
   - Document all changes for this release
   - Update language version tracking

#### Acceptance Criteria
- All validation scripts pass with zero errors
- Index regenerated successfully
- Git commit with meaningful message

---

## File Count Summary

| Category | New Files | Updated Files | Verify Fields | Total Work |
|----------|-----------|---------------|---------------|------------|
| Preprocessor | 10 | 0 | 0 | 10 |
| Methods | 9 | 1 | 7 | 17 |
| Operators | 1 | 1 | 0 | 2 |
| Keywords | 0 | 3 | 0 | 3 |
| Constants | 4 | 0 | 0 | 4 |
| Constructs | 2 | 0 | 0 | 2 |
| Directives | 0 | 2 | 0 | 2 |
| Debug | 1 | 1 | 0 | 2 |
| Symbols | 0 | 1 | 0 | 1 |
| PASM | 1 | 0 | 0 | 1 |
| Registers | 1 | 0 | 0 | 1 |
| **TOTAL** | **29** | **9** | **7** | **45** |

**New items discovered from official reference:**
- C_Z debug formatter (v46, gated)
- NEWTASK constant (v47, gated)
- THISTASK constant (v47, gated)
- TASKHLT register (v47, gated)
- Verify version fields on 7 existing TASK* method YAMLs

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Version directive inconsistency (v45 vs v46) | Verify against official PNut changelog |
| TASKRESUME vs TASKCONT naming | Keep both names documented as aliases |
| Preprocessor nesting complexity | Include clear examples up to 8 levels |
| DITTO $$ vs address $$ confusion | Document both contexts explicitly |

---

## Dependencies

- Schema file: `spin2/spin2-language-schema.yaml`
- Validation tools: `validate-crossref-keys.py`, `generate-p2kb-index.py`
- Cross-references must use existing YAML identifiers

---

## Notes

1. **TASKCONT** exists in V47 docs but knowledge base uses **TASKRESUME** - these are aliases. No new file needed; existing file notes this.

2. **Pointer types** (^BYTE, ^WORD, ^LONG, ^struct) are documented within STRUCT.yaml - no separate file needed.

3. **DITTO** (V50) already has excellent documentation - just need to update `$$` symbol file to clarify the DITTO iteration index context.

4. **Conditional DEBUG in PASM** appears in both V47 and V50 docs with slightly different details - combine into one comprehensive YAML.

5. **V44 FILL/COPY/SWAP/COMP** - These methods were **REMOVED in V45** and replaced with structure operators. The existing YAML files for these methods (if any) may document the pre-V45 behavior. The current (V45+) behavior should be documented in STRUCT.yaml as operators.

6. **Structure operator `:=:`** - This is documented in op_swap.yaml but should also be cross-referenced in STRUCT.yaml as a structure operation.

---

## Reference Documents

- `VERSION_GATED_FEATURES_REFERENCE.md` - Official list of gated vs non-gated features
- `OFFICIAL_CHANGELOG_V43-V52.md` - Complete parsed changelog with all details
- `V46_LANGUAGE_REFERENCE_ADDITIONS.md` through `V52_LANGUAGE_REFERENCE_ADDITIONS.md` - Detailed feature documentation

---

## Critical Corrections from Official Changelog

### V44 → V45 Breaking Change
The V44 structure methods **FILL, COPY, SWAP, COMP were REMOVED in V45** and replaced with operators:
- `structure~` replaces FILL (fill with $00)
- `structure~~` replaces FILL (fill with $FF)
- `structA := structB` replaces COPY
- `structA :=: structB` replaces SWAP
- `structA == structB` and `structA <> structB` replace COMP

**Impact**: No need to create separate YAML files for FILL/COPY/SWAP/COMP methods - they should be documented as structure operators within STRUCT.yaml.

### DITTO Index Symbol
The DITTO iteration index is **`$$`** (0 to count-1). The existing ditto.yaml documentation is correct.

### Additional Features Discovered
| Version | Feature | Type | Gated? |
|---------|---------|------|--------|
| V46 | DEBUG_DISABLE | Constant | NO |
| V46 | _AUTOCLK | Constant | NO |
| V47 | #register syntax | Syntax | NO |
| V48 | __DEBUG__ symbol | Preprocessor | NO |
| V51 | Method pointers in structs | Syntax | NO |
| V51 | _[n] ignore returns | Syntax | NO |
| V52 | TERM colors | DEBUG | NO |

---

*This audit was generated by analyzing the pnut-ts-language-updates source files against the existing YAML knowledge base. Updated 2026-01-13 with gated/non-gated classification and corrections from official PNut changelog.*

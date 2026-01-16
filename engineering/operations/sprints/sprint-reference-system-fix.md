# Sprint: Reference System Fix

**Created**: 2026-01-15
**Status**: PLANNED
**Estimated Effort**: 2-3 hours
**Priority**: HIGH - Blocking MCP retrieval reliability

---

## Problem Statement

The P2KB cross-reference system has gaps that cause MCP retrieval failures:

1. **Validator only checks 5 of 15+ reference fields** - Many reference-like fields are not validated
2. **No alias system in index** - Short names like `PINH` cannot resolve to `p2kbSpin2Pinhigh`
3. **90+ broken references** - Using bare filenames or relative paths instead of index keys
4. **Pattern IDs not aliased** - `combines_with: buffer_management` cannot find `p2kbSpin2BufferManagement`

**Root Cause**: References were added organically without a unified resolution strategy.

---

## Solution Architecture

### Index Structure Change (Additive)

```json
{
  "system": { ... },
  "categories": { ... },
  "files": { ... },
  "aliases": {
    "PINH": "p2kbSpin2Pinhigh",
    "buffer_management": "p2kbSpin2BufferManagement",
    "_clkfreq": "p2kbSpin2SymClkfreq",
    "MOV": "p2kbPasm2Mov"
  }
}
```

**Alias sources** (harvested by index generator):
1. `aliases:` field in YAML files (explicit short names)
2. `pattern_id:` field in pattern files (pattern identifier)
3. Instruction/method names (automatic mnemonic aliases)

### Reference Resolution Strategy

All reference fields should contain ONE of:
- **Index key**: `p2kbPasm2Mov` (preferred, explicit)
- **Mnemonic/alias**: `MOV`, `PINH`, `buffer_management` (resolved via aliases)
- **Search hint**: Descriptive text for `see_also` only (informational, not validated)

**Never allowed**:
- Bare filenames: `case.yaml`
- Relative paths: `../instructions/cmp.yaml`
- Absolute paths: `language/spin2/constructs/case.yaml`

---

## Sprint Phases

### Phase 1: Validator Enhancement

**Goal**: See ALL broken references before fixing anything

**Files to modify**:
- `engineering/tools/validate-crossref-keys.py`

**Changes**:
1. Add these fields to `CROSS_REF_FIELDS`:
   ```python
   'related_documentation': 'mnemonic',
   'related_concepts': 'mnemonic',
   'related_constructs': 'mnemonic',
   'related_operators': 'mnemonic',
   'related_pasm': 'mnemonic',
   'related_methods': 'mnemonic',
   'related_instructions': 'mnemonic',
   'combines_with': 'mnemonic',
   'grouped_with': 'mnemonic',
   'related_symbols': 'mnemonic',
   ```

2. Add alias resolution support:
   - Load aliases section from index
   - When resolving reference, check: direct key match → alias lookup → mnemonic transform

3. Report bare filenames and relative paths as ERRORS (not just unresolved)

**Validation**: Run validator, expect ~90+ errors matching our audit

---

### Phase 2: Index Generator Enhancement

**Goal**: Generate aliases section from YAML content

**Files to modify**:
- `engineering/tools/generate-p2kb-index.py`

**Changes**:
1. Harvest `aliases:` field from each YAML:
   ```python
   if 'aliases' in content:
       for alias in content['aliases']:
           aliases[alias.upper()] = key
   ```

2. Harvest `pattern_id:` field from pattern files:
   ```python
   if 'pattern_id' in content:
       aliases[content['pattern_id']] = key
   ```

3. Generate instruction mnemonic aliases:
   ```python
   if 'instruction' in content:
       mnemonic = content['instruction'].upper()
       aliases[mnemonic] = key
   ```

4. Add `aliases` section to output index

**Validation**: Regenerate index, verify aliases section exists with expected entries

---

### Phase 3: YAML Fixes - Alias Declarations

**Goal**: Ensure all files that need aliases declare them

**Files to modify** (6 files with existing aliases - verify format):
- `language/spin2/methods/pinhigh.yaml` - has `aliases: [PINH]`
- `language/spin2/methods/pinfloat.yaml` - has `aliases: [PINF]`
- `language/spin2/methods/pintoggle.yaml` - has `aliases: [PINT]`
- `language/spin2/methods/pinwrite.yaml` - has `aliases: [PINW]`
- `language/spin2/methods/pinread.yaml` - has `aliases: [PINR]`
- `language/spin2/methods/pinlow.yaml` - has `aliases: [PINL]`

**Action**: Verify `aliases` field format is list of strings, uppercase

---

### Phase 4: YAML Fixes - Pattern Files

**Goal**: Ensure pattern_id fields exist and will generate correct aliases

**Files to verify** (54 pattern files):

```
language/spin2/patterns/implementation/spin2_buffer_management.yaml (pattern_id: buffer_management)
language/spin2/patterns/implementation/spin2_memory_allocation.yaml (pattern_id: memory_allocation)
language/spin2/patterns/implementation/spin2_error_handling.yaml (pattern_id: error_handling)
language/spin2/patterns/implementation/spin2_layered_architecture.yaml (pattern_id: layered_architecture)
language/spin2/patterns/implementation/spin2_mailbox_communication.yaml (pattern_id: mailbox_communication)
language/spin2/patterns/implementation/spin2_cog_management.yaml (pattern_id: cog_management)
language/spin2/patterns/implementation/spin2_protocol_implementation.yaml (pattern_id: protocol_implementation)
language/spin2/patterns/implementation/spin2_resource_pool.yaml (pattern_id: resource_pool)
language/spin2/patterns/implementation/spin2_diagnostic_output.yaml (pattern_id: diagnostic_output)
language/spin2/patterns/implementation/spin2_plugin_system.yaml (pattern_id: plugin_system)
language/spin2/patterns/implementation/spin2_shared_memory.yaml (pattern_id: shared_memory)
language/spin2/patterns/implementation/spin2_state_machine.yaml (pattern_id: state_machine)
language/spin2/patterns/implementation/spin2_pin_control.yaml (pattern_id: pin_control)
language/spin2/patterns/implementation/spin2_event_dispatcher.yaml (pattern_id: event_dispatcher)
language/spin2/patterns/implementation/spin2_timing_control.yaml (pattern_id: timing_control)
language/spin2/patterns/applications/data_logger.yaml (pattern_id: data_logger)
language/spin2/patterns/applications/sensor_reader.yaml (pattern_id: sensor_reader)
language/spin2/patterns/applications/configuration_manager.yaml (pattern_id: configuration_manager)
language/spin2/patterns/applications/display_driver.yaml (pattern_id: display_driver)
language/spin2/patterns/applications/communication_handler.yaml (pattern_id: communication_handler)
language/spin2/patterns/applications/motor_controller.yaml (pattern_id: motor_controller)
language/spin2/patterns/applications/audio_processor.yaml (pattern_id: audio_processor)
language/spin2/patterns/applications/test_harness.yaml (pattern_id: test_harness)
language/spin2/patterns/structural/framework_pattern.yaml (pattern_id: framework_pattern)
```

**Action**: Verify each has `pattern_id` field matching what `combines_with` references expect

---

### Phase 5: YAML Fixes - Broken References

**Goal**: Convert all bare filenames and relative paths to resolvable references

#### 5A: related_documentation (8 references in 4 files)

**Note**: Fundamentals keys use `p2kbLanguage*` prefix (verified from index)

| File | Current Reference | Fix To |
|------|-------------------|--------|
| `language/fundamentals/case-sensitivity.yaml` | `../spin2/constructs/method_definition.yaml` | `p2kbSpin2MethodDefinition` |
| `language/fundamentals/case-sensitivity.yaml` | `identifier-rules.yaml` | `p2kbLanguageIdentifierRules` |
| `language/fundamentals/case-sensitivity.yaml` | `variable-scoping-best-practices.yaml` | `p2kbLanguageVariableScopingBestPractices` |
| `language/fundamentals/identifier-rules.yaml` | `case-sensitivity.yaml` | `p2kbLanguageCaseSensitivity` |
| `language/fundamentals/identifier-rules.yaml` | `variable-scoping-best-practices.yaml` | `p2kbLanguageVariableScopingBestPractices` |
| `language/fundamentals/variable-scoping-best-practices.yaml` | `case-sensitivity.yaml` | `p2kbLanguageCaseSensitivity` |
| `language/fundamentals/variable-scoping-best-practices.yaml` | `identifier-rules.yaml` | `p2kbLanguageIdentifierRules` |

#### 5B: related_concepts (12 references in 4 files)

**Note**: PASM2 concept keys use `p2kbPasm2*` prefix without "Concepts" (verified from index)

| File | Current Reference | Fix To |
|------|-------------------|--------|
| `language/fundamentals/pasm-labels.yaml` | `identifier-rules.yaml` | `p2kbLanguageIdentifierRules` |
| `language/fundamentals/pasm-labels.yaml` | `case-sensitivity.yaml` | `p2kbLanguageCaseSensitivity` |
| `language/pasm2/concepts/conditional_execution.yaml` | `../instructions/cmp.yaml` | `CMP` (alias resolves to p2kbPasm2Cmp) |
| `language/pasm2/concepts/conditional_execution.yaml` | `../instructions/test.yaml` | `TEST` (alias resolves to p2kbPasm2Test) |
| `language/pasm2/concepts/conditional_execution.yaml` | `special_registers.yaml` | `p2kbPasm2SpecialRegisters` |
| `language/pasm2/concepts/conditional_execution.yaml` | `cog_hub_execution.yaml` | `p2kbPasm2CogHubExecution` |
| `language/pasm2/concepts/cog_hub_execution.yaml` | `../instructions/jmp.yaml` | `JMP` (alias resolves to p2kbPasm2Jmp) |
| `language/pasm2/concepts/cog_hub_execution.yaml` | `../instructions/call.yaml` | `CALL` (alias resolves to p2kbPasm2Call) |
| `language/pasm2/concepts/cog_hub_execution.yaml` | `../instructions/coginit.yaml` | `COGINIT` (alias resolves to p2kbPasm2Coginit) |
| `language/pasm2/concepts/cog_hub_execution.yaml` | `special_registers.yaml` | `p2kbPasm2SpecialRegisters` |
| `language/pasm2/concepts/cog_hub_execution.yaml` | `rep_instruction.yaml` | `p2kbPasm2RepInstruction` |
| `language/pasm2/concepts/cog_hub_execution.yaml` | `event_interrupt_config.yaml` | `p2kbPasm2EventInterruptConfig` |

#### 5C: related_constructs (18 references in 7 files)

**Note**:
- `p2kbSpin2Abort` exists (construct), `p2kbSpin2KwABORT` is keyword - use construct key
- `var_dat_con_obj.yaml` does not exist as a file - remove or replace with related keyword keys

| File | Current Reference | Fix To |
|------|-------------------|--------|
| `language/spin2/constructs/if_elseif_else.yaml` | `case.yaml` | `p2kbSpin2Case` |
| `language/spin2/constructs/if_elseif_else.yaml` | `repeat.yaml` | `p2kbSpin2Repeat` |
| `language/spin2/constructs/if_elseif_else.yaml` | `abort.yaml` | `p2kbSpin2Abort` |
| `language/spin2/constructs/blocks.yaml` | `method_definition.yaml` | `p2kbSpin2MethodDefinition` |
| `language/spin2/constructs/blocks.yaml` | `inline_pasm.yaml` | `p2kbSpin2InlinePasm` |
| `language/spin2/constructs/inline_pasm.yaml` | `method_definition.yaml` | `p2kbSpin2MethodDefinition` |
| `language/spin2/constructs/inline_pasm.yaml` | `blocks.yaml` | `p2kbSpin2Blocks` |
| `language/spin2/constructs/repeat.yaml` | `if_elseif_else.yaml` | `p2kbSpin2IfElseifElse` |
| `language/spin2/constructs/repeat.yaml` | `case.yaml` | `p2kbSpin2Case` |
| `language/spin2/constructs/repeat.yaml` | `abort.yaml` | `p2kbSpin2Abort` |
| `language/spin2/constructs/case.yaml` | `if_elseif_else.yaml` | `p2kbSpin2IfElseifElse` |
| `language/spin2/constructs/case.yaml` | `repeat.yaml` | `p2kbSpin2Repeat` |
| `language/spin2/constructs/method_definition.yaml` | `blocks.yaml` | `p2kbSpin2Blocks` |
| `language/spin2/constructs/method_definition.yaml` | `var_dat_con_obj.yaml` | REMOVE (file doesn't exist) or replace with `p2kbSpin2KwVAR`, `p2kbSpin2KwDAT`, `p2kbSpin2KwCON` |
| `language/spin2/constructs/method_definition.yaml` | `inline_pasm.yaml` | `p2kbSpin2InlinePasm` |

#### 5D: related_operators (3 references in 1 file)

**Note**: No single "comparison.yaml" or "logical.yaml" exists. These are generic references.
Options:
1. Replace with specific operators: `p2kbSpin2OpOpGt`, `p2kbSpin2OpOpLt`, `p2kbSpin2OpOpEqeq`
2. Replace with the precedence guide: `p2kbSpin2OpPrecedence`
3. REMOVE these generic references since operators are well-documented elsewhere

| File | Current Reference | Recommended Fix |
|------|-------------------|-----------------|
| `language/spin2/constructs/if_elseif_else.yaml` | `operators/comparison.yaml` | REMOVE or use `p2kbSpin2OpPrecedence` |
| `language/spin2/constructs/if_elseif_else.yaml` | `operators/logical.yaml` | REMOVE or use `p2kbSpin2OpOpAndand` |
| `language/spin2/constructs/if_elseif_else.yaml` | `operators/ternary.yaml` | `p2kbSpin2OpOpTernary` |

#### 5E: related_symbols (6 references in 1 file)

**Note**: These symbols (`_clkfreq`, `_xtlfreq`, etc.) are documented in `special-configuration-symbols.yaml`.
The symbols don't have individual YAML files - they're fields within that document.

**Solution**: Add aliases in `special-configuration-symbols.yaml` OR reference the parent document.

| File | Current Reference | Fix To |
|------|-------------------|--------|
| `language/pasm2/asmclk.yaml` | `_clkfreq` | `p2kbSpin2SpecialConfigurationSymbols` |
| `language/pasm2/asmclk.yaml` | `_xtlfreq` | `p2kbSpin2SpecialConfigurationSymbols` |
| `language/pasm2/asmclk.yaml` | `_xinfreq` | `p2kbSpin2SpecialConfigurationSymbols` |
| `language/pasm2/asmclk.yaml` | `_rcslow` | `p2kbSpin2SpecialConfigurationSymbols` |
| `language/pasm2/asmclk.yaml` | `_rcfast` | `p2kbSpin2SpecialConfigurationSymbols` |
| `language/pasm2/asmclk.yaml` | `_AUTOCLK` | `p2kbSpin2SpecialConfigurationSymbols` |

**Alternative**: Add these as aliases in `special-configuration-symbols.yaml`:
```yaml
aliases:
  - _CLKFREQ
  - _clkfreq
  - _XTLFREQ
  - _xtlfreq
  - _XINFREQ
  - _rcslow
  - _rcfast
  - _AUTOCLK
```
This allows `_clkfreq` to resolve via alias to `p2kbSpin2SpecialConfigurationSymbols`.

#### 5F: combines_with (34 references in 29 files) - CRITICAL

**This is the largest category of broken references.**

The `combines_with` field references pattern IDs like `buffer_management`, but these don't resolve to index keys because:
1. The pattern file is `spin2_buffer_management.yaml`
2. The generated key is `p2kbSpin2Spin2BufferManagement`
3. There's no alias mapping `buffer_management` → `p2kbSpin2Spin2BufferManagement`

**Solution**: The index generator harvests `pattern_id` field as an alias. This makes all `combines_with` references work WITHOUT modifying the YAML files.

**Pattern ID → Key Mappings** (to be generated as aliases):

| pattern_id | Generated Key |
|------------|---------------|
| `buffer_management` | `p2kbSpin2Spin2BufferManagement` |
| `memory_allocation` | `p2kbSpin2Spin2MemoryAllocation` |
| `error_handling` | `p2kbSpin2Spin2ErrorHandling` |
| `layered_architecture` | `p2kbSpin2Spin2LayeredArchitecture` |
| `mailbox_communication` | `p2kbSpin2Spin2MailboxCommunication` |
| `cog_management` | `p2kbSpin2Spin2CogManagement` |
| `protocol_implementation` | `p2kbSpin2Spin2ProtocolImplementation` |
| `resource_pool` | `p2kbSpin2Spin2ResourcePool` |
| `diagnostic_output` | `p2kbSpin2Spin2DiagnosticOutput` |
| `plugin_system` | `p2kbSpin2Spin2PluginSystem` |
| `shared_memory` | `p2kbSpin2Spin2SharedMemory` |
| `state_machine` | `p2kbSpin2Spin2StateMachine` |
| `pin_control` | `p2kbSpin2Spin2PinControl` |
| `event_dispatcher` | `p2kbSpin2Spin2EventDispatcher` |
| `timing_control` | `p2kbSpin2Spin2TimingControl` |
| `data_logger` | `p2kbSpin2DataLogger` |
| `sensor_reader` | `p2kbSpin2SensorReader` |
| `configuration_manager` | `p2kbSpin2ConfigurationManager` |
| `display_driver` | `p2kbSpin2DisplayDriver` |
| `communication_handler` | `p2kbSpin2CommunicationHandler` |
| `motor_controller` | `p2kbSpin2MotorController` |
| `audio_processor` | `p2kbSpin2AudioProcessor` |
| `test_harness` | `p2kbSpin2TestHarness` |
| `framework_pattern` | `p2kbSpin2FrameworkPattern` |

**Verification needed**: Each pattern file must have a `pattern_id` field. Check and add if missing.

**Files with combines_with references** (these will auto-resolve once aliases exist):
```
language/spin2/patterns/implementation/spin2_buffer_management.yaml
language/spin2/patterns/implementation/spin2_memory_allocation.yaml
language/spin2/patterns/implementation/spin2_error_handling.yaml
language/spin2/patterns/implementation/spin2_layered_architecture.yaml
language/spin2/patterns/implementation/spin2_mailbox_communication.yaml
language/spin2/patterns/implementation/spin2_cog_management.yaml
language/spin2/patterns/implementation/spin2_protocol_implementation.yaml
language/spin2/patterns/implementation/spin2_resource_pool.yaml
language/spin2/patterns/implementation/spin2_diagnostic_output.yaml
language/spin2/patterns/implementation/spin2_plugin_system.yaml
language/spin2/patterns/implementation/spin2_shared_memory.yaml
language/spin2/patterns/implementation/spin2_state_machine.yaml
language/spin2/patterns/implementation/spin2_pin_control.yaml
language/spin2/patterns/implementation/spin2_event_dispatcher.yaml
language/spin2/patterns/implementation/spin2_timing_control.yaml
language/spin2/patterns/applications/data_logger.yaml
language/spin2/patterns/applications/sensor_reader.yaml
language/spin2/patterns/applications/configuration_manager.yaml
language/spin2/patterns/applications/display_driver.yaml
language/spin2/patterns/applications/communication_handler.yaml
language/spin2/patterns/applications/motor_controller.yaml
language/spin2/patterns/applications/audio_processor.yaml
language/spin2/patterns/applications/test_harness.yaml
language/spin2/patterns/structural/framework_pattern.yaml
```

**Some combines_with references point to patterns that may not exist yet:**
- `timing_control` - exists
- `several_objects` - may not exist (in event_dispatcher.yaml)
- Check for other missing targets during validation

---

### Phase 6: Validation

1. Run updated validator - expect 0 unresolved references
2. Regenerate index with alias support
3. Run validator again to confirm aliases resolve
4. Test MCP server with alias lookups

---

## MCP Server Change Specification

**Document for MCP server maintainer**:

### Change Required: Add Alias Resolution

The `p2kb-index.json` file will now include an `aliases` section:

```json
{
  "system": { "version": "3.3.0", ... },
  "categories": { ... },
  "files": { ... },
  "aliases": {
    "PINH": "p2kbSpin2Pinhigh",
    "MOV": "p2kbPasm2Mov",
    "buffer_management": "p2kbSpin2Spin2BufferManagement",
    "_clkfreq": "p2kbSpin2SpecialConfigurationSymbols",
    "GETQX": "p2kbPasm2Getqx",
    "POP": "p2kbPasm2Pop"
  }
}
```

### Resolution Logic Update

When `p2kb_get` receives a query:

1. **Direct key match**: If query matches a key in `files`, return that file
2. **Alias lookup**: If query matches a key in `aliases`, get the target key, then return that file
3. **Search fallback**: If neither, perform fuzzy search as before

### Example

```
Query: "PINH"
1. Check files["PINH"] → not found
2. Check aliases["PINH"] → "p2kbSpin2Pinhigh"
3. Check files["p2kbSpin2Pinhigh"] → found!
4. Return content from that path
```

### Backward Compatibility

- Existing queries using full keys continue to work unchanged
- New alias queries now resolve correctly
- No breaking changes to API

---

## Files Modified Summary

### Scripts (2 files)
| File | Change |
|------|--------|
| `engineering/tools/validate-crossref-keys.py` | Add 10 new fields, alias resolution |
| `engineering/tools/generate-p2kb-index.py` | Add alias harvesting from `aliases`, `pattern_id`, `instruction` fields |

### YAMLs Requiring Reference Fixes (~20 files)
| Category | Count | Action |
|----------|-------|--------|
| Fundamentals | 4 | Fix `related_documentation`, `related_concepts` paths → keys |
| Constructs | 7 | Fix `related_constructs` bare filenames → keys |
| Concepts | 2 | Fix `related_concepts` relative paths → keys/mnemonics |
| Operators | 1 | Fix `related_operators` paths → keys or remove |
| Directives | 1 | Fix `related_symbols` → parent doc key or add aliases |

### YAMLs Requiring Alias Declarations (~8 files)
| Category | Count | Action |
|----------|-------|--------|
| Pin methods | 6 | Verify `aliases` field format (already exist) |
| Config symbols | 1 | Add `aliases` field with `_clkfreq`, `_xtlfreq`, etc. |
| Special symbols | ~1 | Add aliases if needed |

### YAMLs to Verify pattern_id (~24 files)
All pattern files with `combines_with` references - verify `pattern_id` field exists and matches expected value.

### Total Estimate
- **Scripts**: 2 files
- **YAML fixes**: ~20 files
- **Alias declarations**: ~8 files
- **Verification only**: ~24 files
- **Grand total**: ~30 files requiring edits, ~24 requiring verification

---

## Execution Order

### Stage 1: Tooling Updates
1. **Update validator** (`validate-crossref-keys.py`)
   - Add 10 new reference fields to validation
   - Add alias resolution logic
   - Add detection of bare filenames and relative paths as errors
2. **Run validator** - confirm it detects ~90+ errors (baseline)

### Stage 2: Index Generator Updates
3. **Update index generator** (`generate-p2kb-index.py`)
   - Add alias harvesting from `aliases` field
   - Add alias harvesting from `pattern_id` field
   - Add alias generation from `instruction`/`method` fields
   - Add `aliases` section to output JSON
4. **Regenerate index** with aliases section
5. **Verify** aliases section contains expected entries

### Stage 3: YAML Fixes (in order)
6. **Fix alias declarations** (Phase 3)
   - Verify pin method files have correct `aliases` format
   - Add aliases to `special-configuration-symbols.yaml`
7. **Verify pattern_id fields** (Phase 4)
   - Check all 24 pattern files have `pattern_id`
   - Add missing `pattern_id` fields
8. **Run validator** - combines_with errors should be resolved
9. **Fix fundamentals** (Phase 5A) - 4 files
10. **Fix concepts** (Phase 5B) - 4 files
11. **Fix constructs** (Phase 5C) - 7 files
12. **Fix operators** (Phase 5D) - 1 file
13. **Fix symbols** (Phase 5E) - 1 file
14. **Run validator** after each batch - errors should decrease

### Stage 4: Final Validation
15. **Final validation** - expect 0 unresolved references
16. **Regenerate index** one final time
17. **Run full validation suite** including `validate-dod-release.py`
18. **Commit all changes** with descriptive message

### Stage 5: MCP Server Update (User Action)
19. **User updates MCP server** per specification in this document

---

## Success Criteria

- [ ] Validator checks all 15 reference fields
- [ ] Index contains `aliases` section with 100+ entries
- [ ] All 90+ broken references resolved
- [ ] Validator reports 100% resolution rate
- [ ] MCP retrieval works for alias queries

---

## Notes for Execution

- Work in container mode for full file permissions
- Commit frequently - after each phase if possible
- If uncertain about correct key for a reference, check index first
- Pattern files: verify `pattern_id` value matches `combines_with` usage exactly

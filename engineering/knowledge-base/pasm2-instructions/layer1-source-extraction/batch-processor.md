# Layer 1: Batch Source Extraction Process

## Extraction Strategy
Processing all instructions from `/engineering/ingestion/sources/p2-datasheet/pasm2-complete-instruction-tables.md` through systematic table parsing.

## Instruction Groups Identified
1. **Math and Logic Instructions** (~69 instructions)
2. **Branch Instructions** (~20+ instructions)  
3. **Call/Return Instructions** (~6 instructions)
4. **Memory Instructions** (~30+ instructions)
5. **Hardware Instructions** (~50+ instructions)
6. **Interrupt Instructions** (~15+ instructions)
7. **Cog Control Instructions** (~10+ instructions)
8. **Hub Control Instructions** (~10+ instructions)
9. **Pin Control Instructions** (~30+ instructions)
10. **Lookup Table, Streamer, and Misc Instructions** (~15+ instructions)

## Extraction Process
For each instruction:
1. **Parse**: Extract mnemonic, operands, description, timing
2. **Validate**: Check syntax completeness
3. **Lineage**: Record source location (table, line number)
4. **Quality Gate**: Flag any parsing issues for retry

## Quality Metrics Per Group
- **Extraction Success Rate**: Target >95%
- **Validation Pass Rate**: Target 100%
- **Retry Queue Length**: Track failures
- **Source Lineage Complete**: Track coverage

## Current Status
- **Groups Processed**: 0/10
- **Instructions Extracted**: 0/~450
- **Extraction Failures**: 0
- **Quality Issues**: 0
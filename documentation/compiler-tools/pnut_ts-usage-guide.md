# PNut-TS Compiler Usage Guide for Claude

## Overview
The P2 Spin2/PASM2 compiler (`pnut_ts`) is available in the Claude Code environment for validating and compiling P2 code. This allows Claude to:
1. Validate code snippets in documentation
2. Generate binary and listing files
3. Help developers debug compilation issues
4. Ensure examples are syntactically correct

## Basic Usage

### Simple Compilation
```bash
pnut_ts filename.spin2            # Creates .bin file
pnut_ts -l filename.spin2         # Creates .bin and .lst files
pnut_ts -q filename.spin2         # Quiet mode (errors only)
```

### Common Options
- `-l, --list` - Generate listing file showing compiled bytecode
- `-v, --verbose` - Show detailed compilation messages
- `-q, --quiet` - Suppress non-error output
- `-o, --output <name>` - Specify output filename
- `-d, --debug` - Compile with DEBUG enabled
- `-F, --flashfile` - Generate .flash file for flash programming

### Validation Workflow

#### 1. Validate Documentation Code
```bash
# Create test file from documentation snippet
echo 'DAT
    ORG 0
    DRVH #16
    JMP #$' > test.spin2

# Compile to check syntax
pnut_ts -q test.spin2
```

#### 2. Generate Listing for Analysis
```bash
pnut_ts -l example.spin2
cat example.lst    # View compiled output
```

#### 3. Check Include Paths
```bash
pnut_ts -I /path/to/includes main.spin2
```

## Example: Validating Manual Code

When working on the P2 PASM manual, validate examples:

```bash
# Create temporary file with code from manual
cat > validate.spin2 << 'EOF'
DAT
    ORG 0
start
    DRVH    #16           ' LED on
    WAITX   ##25_000_000  ' Wait 0.5s
    DRVL    #16           ' LED off
    WAITX   ##25_000_000  ' Wait 0.5s
    JMP     #start        ' Loop
EOF

# Compile and check
pnut_ts -l validate.spin2
if [ $? -eq 0 ]; then
    echo "Code compiles successfully!"
    hexdump -C validate.bin | head -2  # Show first 32 bytes
else
    echo "Compilation failed - check syntax"
fi
```

## Advanced Features

### Preprocessor Symbols
```bash
pnut_ts -D DEBUG -D P2_EVAL main.spin2     # Define symbols
pnut_ts -U DEBUG main.spin2                # Undefine symbols
```

### Generate Intermediate Files
```bash
pnut_ts -i main.spin2    # Creates main__pre.spin2 after preprocessing
```

### Flash Programming Files
```bash
pnut_ts -F bootloader.spin2    # Creates .flash file for programming
```

## Integration with Documentation Pipeline

When validating P2 Knowledge Base examples:

```bash
#!/bin/bash
# validate-pasm-examples.sh

EXAMPLES_DIR="sources/pasm2-master/examples"
FAILED=0

for file in $EXAMPLES_DIR/*.spin2; do
    echo "Validating: $file"
    if pnut_ts -q "$file" 2>/dev/null; then
        echo "  ✓ Compiles"
    else
        echo "  ✗ Failed"
        FAILED=$((FAILED + 1))
    fi
done

echo "Validation complete: $FAILED failures"
```

## Error Handling

Common compilation errors and what they mean:

- `Expected unique symbol` - Duplicate label definition
- `Symbol is not defined` - Missing label or constant
- `Expected "#" or constant` - Immediate value required
- `Value exceeds $1FF` - 9-bit immediate overflow

## Version Information

Current compiler version:
```
PNut-TS v1.51.5 (Build date: 7/11/2025)
© 2025 Iron Sheep Productions, LLC., Parallax Inc.
```

## Notes for Claude Instances

1. **Always validate code before including in documentation**
2. **Use `-q` flag for automated validation** (less output to parse)
3. **Check listing files for instruction encodings** when documenting opcodes
4. **Save validated examples** in `sources/validated-examples/`
5. **Report compilation issues** to user for manual review

## Platform Compatibility

The `pnut_ts` compiler is:
- Multi-platform (macOS, Linux, Windows)
- Command-line based (no GUI required)
- Suitable for CI/CD pipelines
- Fast enough for real-time validation

This compiler is production-ready and can be used confidently for all P2 Spin2/PASM2 compilation tasks.
# P2 Knowledge Base Usage Guide

## 🎯 Quick Start

**For AI/Users**: Use `/production/` files - they're clean and ready to use.
**For Debugging**: Check `/_sources/` files - they show extraction details.

## 📁 What's Where

### Production Files (USE THESE)
Clean, single-source-of-truth files for each P2 element:

```
P2/production/
├── instructions/pasm2/     # CPU instructions (add.yaml, sub.yaml, etc.)
├── language/spin2/         # Spin2 methods and operators
├── hardware/               # Board specifications
└── architecture/           # Core components (COG, Hub, CORDIC, etc.)
```

### Source Files (DEBUGGING ONLY)
Multi-layer extraction files with full lineage:

```
P2/production/_sources/     # Original 4-layer extraction files
```

## 📊 Coverage

| Category | Count | Coverage |
|----------|-------|----------|
| PASM2 Instructions | 357 | 100% of real CPU ops |
| Spin2 Methods | 73 | Core language methods |
| Spin2 Operators | 46 | All operators |
| Hardware Specs | 11 | Major boards/modules |
| Architecture | 8 | Core components |
| **Total Files** | **495** | Production ready |

## 🔍 How to Use

### 1. Finding Instructions
```yaml
# Look up ADD instruction
Path: P2/production/instructions/pasm2/add.yaml

# Content:
instruction: ADD
syntax: ADD D,{#}S {WC/WZ/WCZ}
description: Add S into D
timing: {cycles: 2, type: fixed}
```

### 2. Understanding Spin2
```yaml
# Look up DEBUG method
Path: P2/production/language/spin2/methods/debug.yaml

# Content:
method: DEBUG
syntax: DEBUG(...)
description: Output debug information
category: Debugging
```

### 3. Hardware Reference
```yaml
# P2 Eval Board specs
Path: P2/production/hardware/p2_eval_board.yaml
```

### 4. Architecture Details
```yaml
# COG architecture
Path: P2/production/architecture/cog.yaml
```

## ⚠️ Important Notes

### What We Removed
- **83 pseudo-instructions** - Not real CPU operations
  - IF_* conditionals (48 files)
  - Flag conditionals (C_AND_Z, etc.)
  - Comparison conditionals (GT, GE, LT, LE)
  - Assembler aliases (CLR, EMPTY)

### Why Two Versions?
- **Production**: Clean, unified, ready to use
- **Sources**: Preserves extraction history for validation

### Don't Edit Production Files
Production files are generated from sources. To make changes:
1. Edit source files in `_sources/`
2. Run regeneration script
3. Production files will be updated

## 🚀 For AI Code Generation

### Best Practices
1. **Always use production files** for instruction lookup
2. **Check timing information** for performance optimization
3. **Note flag effects** for condition code handling
4. **Reference encoding** for binary generation

### Example Query Flow
```
User: "How do I add two registers?"
1. Check: /production/instructions/pasm2/add.yaml
2. Get: syntax, description, timing, flags
3. Generate: ADD destination, source {WC}
```

## 📈 Quality Assurance

- ✅ **Validated** against P2 Silicon v35 documentation
- ✅ **100% timing coverage** for all instructions
- ✅ **Cross-referenced** with multiple sources
- ✅ **Cleaned** of all non-instructions
- ✅ **Structured** for optimal AI parsing

## 🛠️ Maintenance

### Regenerating Production Files
```bash
python3 engineering/tools/create-all-production-files.py
```

### Validating Coverage
```bash
python3 engineering/knowledge-base/P2/verify-coverage.py
```

### Checking Quality
```bash
python3 engineering/knowledge-base/P2/quality-check.py
```

## 📚 Documentation

- `production/README.md` - Production files overview
- `REORGANIZATION-TRACKER.md` - File movement history
- `manifest.yaml` - Complete content index
- `timing-investigation-report.md` - Timing coverage analysis

## 🎯 Goal

Enable AI to generate production-quality P2 code by providing:
- Complete instruction semantics
- Accurate timing information
- Clear syntax specifications
- Comprehensive hardware details

---

*Knowledge Base v1.1.0 - Production Ready*
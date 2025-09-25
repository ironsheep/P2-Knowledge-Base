# AI Integration Guide for P2 Knowledge Base
*How to use this knowledge base with Claude Code and other AI assistants*

**Repository**: https://github.com/ironsheep/P2-Knowledge-Base

## Quick Start for Claude Code Users

**🚀 [Essential Copy-Paste Templates](CLAUDE-QUICKSTART.md)**  
5 essential templates to get started immediately.

**📚 [Complete Prompt Pattern Library](AI-PROMPT-PATTERNS.md)**  
Comprehensive interaction patterns for all P2 development scenarios.

**🔒 [Privacy Guide for P2 Developers](deliverables/developer-docs/ai-development/Claude-Code-Privacy-Guide-for-P2-Developers.pdf)**  
**Must read!** Learn how to protect your IP while using AI tools for P2 development.

### 1. Access the Repository Directly from GitHub

When starting a new Claude Code conversation, reference this repository:
```
Please use the P2 Knowledge Base directly from GitHub:
https://github.com/ironsheep/P2-Knowledge-Base

CRITICAL INSTRUCTIONS:
1. START with the root manifest for ALL navigation:
   https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/manifests/p2-knowledge-root.yaml

2. FOLLOW the manifest tree - it contains ALL file paths
3. NEVER construct or guess file paths
4. ONLY download .yaml files (all documentation is YAML)
5. NEVER look for .md files in the knowledge base

The manifest tree provides:
- Complete file paths for all 357 PASM2 instructions
- Paths for all 32 Smart Pin modes
- Locations of all Spin2 methods and debug commands
- Every architecture document location

REMEMBER: If it's not in a manifest, it doesn't exist.
DO NOT clone the repository - read files directly from GitHub.
```

### 2. Navigate Using the Manifest System

The knowledge base uses a hierarchical manifest system for efficient navigation:

```yaml
# Start here - the root manifest:
manifests/p2-knowledge-root.yaml
  ↓
# Category manifests:
manifests/pasm2-manifest.yaml         # 357 instructions
manifests/smart-pins-manifest.yaml    # 32 pin modes
manifests/spin2-manifest.yaml         # Language constructs
manifests/architecture-manifest.yaml  # Hardware specs
manifests/patterns-manifest.yaml      # Code examples
manifests/obex-community-manifest.yaml # 113 community objects ✨ NEW!
  ↓
# Individual specifications:
engineering/knowledge-base/P2/language/pasm2/[category]/*.yaml
engineering/knowledge-base/P2/hardware/smart-pins/modes/*.yaml
engineering/knowledge-base/P2/language/spin2/methods/*.yaml
# Community objects:
manifests/categories/[category]-manifest.yaml  # Objects by function
manifests/authors/[author]-manifest.yaml       # Objects by contributor
```

For best results, always start with `p2-knowledge-root.yaml` which provides:
- Complete index of available documentation
- Entry counts for each category
- Direct URLs to category manifests
- Usage examples and navigation patterns

## 🚨 CRITICAL: Use Manifest Navigation ONLY - Never Guess Paths!

### The Golden Rule: Follow the Manifest Tree

**Path Construction Formula (NOW EXPLICIT IN MANIFESTS):**

```
FULL_URL = raw_base_url + base_path + file

Where:
- raw_base_url: From p2-knowledge-root.yaml (ends with /)
- base_path: From category manifest like spin2-manifest.yaml
- file: From the specific entry in the manifest
```

**Real Example:**
```yaml
# From p2-knowledge-root.yaml:
raw_base_url: "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/"

# From spin2-manifest.yaml:
base_path: "engineering/knowledge-base/P2/language/spin2/"

# From entry in manifest:
file: "methods/cogspin.yaml"

# RESULT:
https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/engineering/knowledge-base/P2/language/spin2/methods/cogspin.yaml
```

All file locations are provided by the manifest hierarchy. Start with the root manifest and follow the tree:

```yaml
# 1. ALWAYS START HERE:
manifests/p2-knowledge-root.yaml
    ↓
# 2. Navigate to category manifests (all paths provided):
manifests/spin2-manifest.yaml
    ↓  
# 3. Find specific file paths in the manifest:
methods:
  - name: "locknew"
    path: "engineering/knowledge-base/P2/language/spin2/methods/locknew.yaml"
```

**Key Principles:**
- ✅ **ONLY download .yaml files** (never .md files)
- ✅ **ALL paths come from manifests** (never construct URLs)
- ✅ **Follow the manifest tree** (never search or guess)
- ✅ **Every file is referenced** (if it's not in a manifest, it doesn't exist)

## ⚠️ Common Path Issues - IMPORTANT FOR EXTERNAL CLAUDE

### Correct File Locations (External Claude Often Gets These Wrong)

#### Lock Methods
```yaml
# ✅ CORRECT - Lock methods are individual YAML files:
engineering/knowledge-base/P2/language/spin2/methods/locknew.yaml
engineering/knowledge-base/P2/language/spin2/methods/locktry.yaml
engineering/knowledge-base/P2/language/spin2/methods/lockrel.yaml
engineering/knowledge-base/P2/language/spin2/methods/lockret.yaml
engineering/knowledge-base/P2/language/spin2/methods/lockchk.yaml

# ❌ WRONG - These paths don't exist:
/language/spin2/constructs/methods/lockset.md  # No such file
/language/spin2/methods/lockset.yaml          # No such file
```

#### DEBUG Statement
```yaml
# ✅ CORRECT - DEBUG is in debug-commands:
engineering/knowledge-base/P2/language/spin2/debug-commands/debug.yaml

# ❌ WRONG - These paths don't exist:
/language/spin2/constructs/methods/debug.md   # Wrong directory
/language/spin2/methods/debug.yaml           # Wrong directory
```

**GitHub Raw URLs for External Access:**
```bash
# Lock methods:
https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/engineering/knowledge-base/P2/language/spin2/methods/locknew.yaml

# DEBUG statement:
https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/engineering/knowledge-base/P2/language/spin2/debug-commands/debug.yaml
```

### Example: Finding Lock Methods the RIGHT Way

```yaml
# Step 1: Start with p2-knowledge-root.yaml
# It tells you:
spin2_manifest:
  path: "manifests/spin2-manifest.yaml"
  
# Step 2: Open spin2-manifest.yaml
# It tells you:
methods:
  - category: "Lock Operations"
    files:
      - name: "locknew"
        path: "engineering/knowledge-base/P2/language/spin2/methods/locknew.yaml"
      - name: "locktry"
        path: "engineering/knowledge-base/P2/language/spin2/methods/locktry.yaml"
        
# Step 3: Use the exact path from the manifest
# NEVER guess or construct paths!
```

## 🎯 CRITICAL: P2 Hardware vs OBEX Boundary

### Understanding What P2 Hardware DOESN'T Provide

**The P2 philosophy is different from traditional MCUs!**

Many features that are hardware peripherals on other processors (Arduino, STM32, etc.) are implemented as **OBEX objects** on the P2. The P2 provides flexible building blocks (Smart Pins, COGs), not fixed-function peripherals.

#### What P2 Hardware Provides:
- **Smart Pins**: Configurable I/O (32 modes) - building blocks for protocols
- **COGs**: 8 parallel processors for implementing any protocol
- **CORDIC**: Math engine for calculations
- **Hub RAM**: Shared memory for communication
- **Streamer**: DMA-like data movement

#### What You Need OBEX Objects For:
```yaml
# Traditional MCU Peripherals → P2 OBEX Objects
UART/Serial     → jm_fullduplexserial.spin2 (Object 2842)
SPI Master      → jm_ez_spi.spin2 (Object 2841)  
I2C Master      → jm_i2c.spin2 (Object 2843)
PWM Controller  → jm_pwm.spin2 (various objects)
Servo Control   → jm_servo.spin2 (Object 3161)
NeoPixel/WS2812 → jm_rgbx_pixel.spin2 (Object 3213)
SD Card         → Various SD/FAT32 objects
USB Host/Device → USB objects in development
CAN Bus         → Community CAN objects
Ethernet        → Community Ethernet objects
LCD Display     → Display driver objects
Keyboard/Mouse  → HID objects
```

### When to Search OBEX

**ALWAYS check OBEX when user asks for:**
- "Serial communication" → Not built-in, need OBEX object
- "SPI/I2C/UART" → Protocol objects in OBEX
- "PWM output" → OBEX objects using Smart Pins
- "Read SD card" → File system objects in OBEX
- "Drive servo/motor" → Motor control objects
- "Display on LCD/OLED" → Display drivers
- "USB communication" → USB stack objects
- "Network/Ethernet" → Networking objects
- "Sensor interfaces" → Sensor-specific drivers

### How to Navigate to OBEX Objects

```yaml
# 1. Start with root manifest
manifests/p2-knowledge-root.yaml
  ↓
# 2. Find community_resources section
community_resources:
  url: "manifests/obex/obex-root.yaml"
  ↓
# 3. Navigate to category manifests
manifests/obex/categories/communication-manifest.yaml  # For serial/SPI/I2C
manifests/obex/categories/drivers-manifest.yaml       # For hardware drivers
manifests/obex/categories/display-manifest.yaml       # For displays
manifests/obex/categories/sensors-manifest.yaml       # For sensors
  ↓
# 4. Find specific object with download URL
object_id: '2842'
title: 'Full Duplex Serial'
author: 'Jon McPhalen (jonnymac)'
```

### Example: User Asks "How do I do serial communication on P2?"

**WRONG Response:**
"The P2 has built-in UART..." ❌

**CORRECT Response:**
"The P2 implements serial communication using Smart Pins configured by OBEX objects. Let me find the serial driver for you..."
1. Check `manifests/obex/categories/communication-manifest.yaml`
2. Find Object 2842: "Full Duplex Serial" by jonnymac
3. Provide implementation using the OBEX object

### Golden Rules for P2 Capabilities:

1. **Smart Pins are building blocks, not complete peripherals**
2. **OBEX objects implement the protocols using Smart Pins**
3. **When in doubt, search OBEX first**
4. **Community objects are production-ready** (especially jonnymac's)
5. **Multiple implementations may exist** - check authors and features

## Typical Usage Patterns

### Pattern 1: Code Generation (Updated for OBEX)
```
User: "Using the P2 knowledge base, write code for serial communication at 115200 baud"

Claude will:
1. Recognize serial is NOT a built-in peripheral
2. Check manifests/obex/categories/communication-manifest.yaml
3. Find Object 2842 (Full Duplex Serial)
4. Show how to use jm_fullduplexserial.spin2
5. Configure Smart Pins via the object methods
```

### Pattern 2: Instruction Lookup
```
User: "What PASM2 instructions are available for CORDIC operations?"

Claude will:
1. Check manifests/pasm2-manifest.yaml for CORDIC category
2. List all CORDIC instructions from the category YAML
3. Provide usage examples from the enriched documentation
```

### Pattern 3: Hardware Configuration
```
User: "How do I set up a HUB75 LED matrix display with the P2?"

Claude will:
1. Reference engineering/knowledge-base/P2/hardware/hub75_adapter.yaml
2. Check the driver patterns in external-projects/p2-HUB75-LED-Matrix-Driver/
3. Provide wiring diagram, initialization code, and usage examples
```

### Pattern 4: Community Code Discovery
```
User: "Find me a P2 serial driver"

Claude will:
1. Check manifests/obex-community-manifest.yaml for community objects
2. Find Jon McPhalen's Full Duplex Serial Driver (Object 2842)
3. Provide direct download URL and implementation notes
4. Reference proven community patterns and usage examples
```

### Pattern 5: Debugging Assistance
```
User: "My Smart Pin isn't outputting data. Here's my configuration code..."

Claude will:
1. Compare your code against the Smart Pin mode YAML specification
2. Check for common issues documented in the knowledge base
3. Suggest corrections based on validated patterns
```

## Best Practices for AI Interaction

### 1. Be Specific About Context
Instead of: "Write P2 code"
Use: "Using the P2 PASM2 instruction set, write code to..."

### 2. Reference Documentation Levels
- **Overview**: "Check the manifests/ directory"
- **Detailed**: "Look at the specific YAML in engineering/knowledge-base/"
- **Examples**: "Find patterns in external-projects/"

### 3. Leverage the Structure
The knowledge base is organized hierarchically:
```
manifests/
  ├── p2-knowledge-root.yaml      # START HERE - Main navigation index
  ├── pasm2-manifest.yaml         # 357 instruction categories
  ├── smart-pins-manifest.yaml    # 32 pin modes
  ├── spin2-manifest.yaml         # Language constructs
  ├── architecture-manifest.yaml  # Hardware specs
  └── patterns-manifest.yaml      # Code examples
  
engineering/knowledge-base/P2/     # Detailed specs here
  ├── language/
  │   ├── pasm2/                  # All 357 instructions
  │   └── spin2/                  # Spin2 methods
  ├── hardware/
  │   └── smart-pins/             # 32 pin modes
  └── architecture/               # System design
```

### 4. Use Enriched Instructions
Many PASM2 instructions have been enriched with:
- Detailed descriptions
- Encoding formats
- Usage examples
- Common patterns
- Performance notes

Ask Claude to check if an instruction has enriched documentation.

## Advanced Features

### Smart Pin Configuration Helper
```
User: "I need Smart Pin mode for measuring pulse width"
Claude: [Checks mode 10000_time_a_input.yaml]
        "Use mode %10000_0 for pulse measurement..."
```

### Instruction Encoding Assistant
```
User: "What's the binary encoding for 'ADD D, S'?"
Claude: [References encoding field in ADD instruction YAML]
        "Encoding: EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS"
```

### Multi-COG Coordination
```
User: "Show me patterns for safe multi-COG communication"
Claude: [References patterns from flash_fs and hub75 drivers]
        "Here are proven patterns for COG synchronization..."
```

## Knowledge Base Capabilities

### ✅ Fully Supported
- All 357 PASM2 instructions with categories
- 32 Smart Pin modes with configuration details
- Complete P2 architecture (8 COGs, 512KB hub, etc.)
- Spin2 core language constructs
- Hardware specifications and timing
- Pin control and I/O operations
- CORDIC math operations
- Interrupt handling

### 🚧 Partially Supported
- Spin2 method library (71 methods enriched, more to come)
- USB implementation details
- Advanced video generation
- Some specialized peripherals

### 📚 Example Code Available
- Flash filesystem driver (pure Spin2)
- HUB75 LED matrix driver (Spin2 + PASM2)
- Various test patterns and demos
- Real-world usage patterns

## Troubleshooting

### Issue: Claude can't find specific information
**Solution**: Direct Claude to the manifest first, then the specific YAML path

### Issue: Generated code doesn't compile
**Solution**: Ask Claude to validate against the instruction YAML specifications

### Issue: Unclear about hardware capabilities
**Solution**: Reference manifests/architecture-manifest.yaml for system limits

## Example Conversation Starters

### For Beginners
"I'm new to P2. Using the knowledge base, explain the basic architecture and show me a simple LED blink example."

### For PASM2 Programming
"Using the PASM2 instruction reference, help me write an efficient bit-bang SPI driver."

### For Smart Pins
"I need to configure Smart Pins for quadrature encoder input. Show me the configuration using the knowledge base."

### For System Design
"Based on the P2 architecture docs, help me design a multi-COG data acquisition system."

### For Migration
"I'm porting Arduino code to P2. Using the knowledge base, what are the P2 equivalents?"

## Contributing Back

If you discover patterns, fix documentation, or add examples:
1. Follow CONTRIBUTING.md guidelines
2. Enriched YAMLs go in engineering/knowledge-base/P2/
3. Patterns go in appropriate external-projects/ directories
4. Update relevant manifests

## Tips for Maximum Effectiveness

1. **Start with manifests** - They provide the navigation structure
2. **Use YAML paths** - More reliable than searching
3. **Check enrichment status** - In .ai-manifest.json completeness section
4. **Leverage patterns** - Real code in external-projects/ shows best practices
5. **Be specific** - "Using the P2 knowledge base..." helps Claude focus

## Integration with Other Tools

### VS Code with Claude Code
- Reference the GitHub repository directly
- Use Claude Code's WebFetch capabilities
- Start with p2-knowledge-root.yaml manifest

### GitHub Copilot
- Reference raw.githubusercontent.com URLs in comments
- Point to specific manifest files for context
- Let Copilot fetch YAML structures as needed

### Custom GPTs
- Upload p2-knowledge-root.yaml as primary knowledge
- Configure with raw GitHub URLs for detailed lookups
- Use manifest hierarchy for navigation

## Performance Tips

- The knowledge base is ~80% complete
- PASM2 instructions: 166 enriched, 188 minimal
- Smart Pins: All 32 modes documented
- Best coverage: Architecture, hardware specs
- Growing: Spin2 methods, code examples

## Need Help?

- **Issues**: https://github.com/ironsheep/P2-Knowledge-Base/issues
- **P2 Forums**: https://forums.parallax.com/categories/propeller-2
- **Documentation**: Check README.md for human-readable guides

---

*Remember: This knowledge base is AI-optimized. When working with Claude or other AI assistants, always mention you're using the "P2 Knowledge Base" for best results.*
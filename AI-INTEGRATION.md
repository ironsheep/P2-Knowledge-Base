# AI Integration Guide for P2 Knowledge Base
*How to use this knowledge base with Claude Code and other AI assistants*

**Repository**: https://github.com/ironsheep/P2-Knowledge-Base

## Quick Start for Claude Code Users

**🚀 [Jump to Copy-Paste Templates](CLAUDE-QUICKSTART.md)**  
For ready-to-use prompts and templates, see the CLAUDE-QUICKSTART.md file.

### 1. Clone or Reference the Repository

#### Option A: Direct GitHub Reference (Recommended)
When starting a new Claude Code conversation, reference this repository:
```
Please use the P2 Knowledge Base directly from GitHub:
https://github.com/ironsheep/P2-Knowledge-Base

IMPORTANT: Read files using raw.githubusercontent.com URLs:
Base: https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/

Focus on the manifests/ directory for navigation and 
engineering/knowledge-base/P2/ for detailed specifications.

DO NOT clone - just read files directly from GitHub.
```

#### Option B: Local Clone
```bash
git clone https://github.com/ironsheep/P2-Knowledge-Base.git
cd P2-Knowledge-Base
```
Then tell Claude: "I have the P2 Knowledge Base in my current directory"

### 2. Point Claude to Key Resources

For best results, direct Claude to these specific areas based on your needs:

```
# For instruction reference:
Look at manifests/pasm2-manifest.yaml for instruction categories
Then reference engineering/knowledge-base/P2/language/pasm2/[category]/*.yaml

# For Smart Pins:
Start with manifests/smart-pins-manifest.yaml
Then check engineering/knowledge-base/P2/hardware/smart-pins/modes/*.yaml

# For Spin2 language:
Review manifests/spin2-manifest.yaml
Check engineering/knowledge-base/P2/language/spin2/methods/*.yaml

# For architecture:
Read manifests/architecture-manifest.yaml
Study engineering/knowledge-base/P2/architecture/*.yaml

# For code patterns:
Review engineering/ingestion/external-inputs/source-code/external-projects/*/spin2-patterns-*.md
```

## Typical Usage Patterns

### Pattern 1: Code Generation
```
User: "Using the P2 knowledge base, write PASM2 code to configure a Smart Pin 
      as a UART transmitter at 115200 baud on pin 16"

Claude will:
1. Check smart-pins/modes/00010_sync_tx.yaml for UART TX mode
2. Reference the baud rate calculation formula
3. Generate properly formatted PASM2 code with comments
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

### Pattern 4: Debugging Assistance
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
manifests/                  # Start here for navigation
  ├── pasm2-manifest.yaml   # Instruction categories
  ├── smart-pins-manifest.yaml
  └── architecture-manifest.yaml
  
engineering/knowledge-base/P2/  # Detailed specs here
  ├── language/
  │   ├── pasm2/           # All 357 instructions
  │   └── spin2/           # Spin2 methods
  ├── hardware/
  │   └── smart-pins/      # 32 pin modes
  └── architecture/        # System design
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

### VS Code
- Open the knowledge base folder
- Use Claude Code's file reading capabilities
- Reference specific YAMLs in your prompts

### GitHub Copilot
- Clone the repo locally
- Copilot will index the YAML structures
- Comments referencing the knowledge base help context

### Custom GPTs
- Upload key manifests as knowledge
- Reference the GitHub URLs for detailed lookups
- Use the .ai-manifest.json for capability descriptions

## Performance Tips

- The knowledge base is ~80% complete
- PASM2 instructions: 166 enriched, 188 minimal
- Smart Pins: All 32 modes documented
- Best coverage: Architecture, hardware specs
- Growing: Spin2 methods, code examples

## Need Help?

- **Issues**: https://github.com/IronSheepProductionsLLC/P2-Knowledge-Base/issues
- **P2 Forums**: https://forums.parallax.com/categories/propeller-2
- **Documentation**: Check README.md for human-readable guides

---

*Remember: This knowledge base is AI-optimized. When working with Claude or other AI assistants, always mention you're using the "P2 Knowledge Base" for best results.*
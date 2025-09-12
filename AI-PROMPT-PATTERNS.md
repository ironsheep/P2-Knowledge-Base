# AI Prompt Patterns for P2 Knowledge Base
*Comprehensive interaction library for AI assistants working with P2 development*

## 📚 Common Task Templates

### PASM2 Assembly Programming
```
Using the P2 knowledge base PASM2 instructions in 
engineering/knowledge-base/P2/language/pasm2/, 
help me write assembly code to [DESCRIBE TASK].

Check manifests/pasm2-manifest.yaml for instruction categories.
```

### Smart Pin Configuration
```
I need to configure a P2 Smart Pin for [PURPOSE].
Check engineering/knowledge-base/P2/hardware/smart-pins/modes/
and help me select and configure the right mode.

The mode naming is [5-bit-binary]_[description].yaml
```

### Spin2 High-Level Programming
```
Using the Spin2 method documentation in 
engineering/knowledge-base/P2/language/spin2/methods/,
show me how to [DESCRIBE TASK] in Spin2.

Reference manifests/spin2-manifest.yaml for available methods.
```

### Multi-COG Design
```
I need to design a multi-COG P2 application for [PURPOSE].
Reference the patterns in:
- external-projects/P2-FLASH-FS/ (multi-COG safe patterns)
- external-projects/p2-HUB75-LED-Matrix-Driver/ (COG communication)

Show me the architecture and communication strategy.
```

### Hardware Interfacing
```
I need to interface the P2 with [DEVICE/PROTOCOL].
Check the hardware specs in engineering/knowledge-base/P2/hardware/
and any relevant patterns in external-projects/.

Generate the initialization and communication code.
```

## 🌐 Community Code (OBEX) Discovery Patterns

### Download and Install Objects
```
Download Jon McPhalen's full duplex serial driver and set it up in my project folder

Claude will:
1. Find Object 2842 in manifests/authors/jon_mcphalen_jonnymac-manifest.yaml
2. Provide the download URL: https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB2842
3. Guide you through downloading and extracting to your project
4. Show how to integrate the driver into your P2 project
5. Provide initialization code and usage examples
```

```
I need the BME280 sensor driver - download and set it up for me

Claude will:
1. Find Mike Calyer's Cricket BME280 driver (Object 2815)
2. Provide direct download: obuid=OB2815
3. Show wiring diagram and connection requirements
4. Generate initialization code for your specific use case
5. Include error handling and data reading examples
```

### Query by Author
```
Show me all P2 objects created by jonnymac

Claude will:
1. Reference manifests/authors/jon_mcphalen_jonnymac-manifest.yaml
2. List all 44 objects with descriptions and categories
3. Highlight most popular objects (serial drivers, timing utilities)
4. Provide quality ratings and download statistics
5. Suggest which objects work best together
```

```
What has Stephen Moraco contributed to the P2 community?

Claude will:
1. Check manifests/authors/stephen_m_moraco-manifest.yaml
2. Show 15 objects including LED drivers and development tools
3. Highlight the P2 Cube Demo and LED panels drivers
4. Show creation dates and update history
```

### Query by Capability
```
What P2 display drivers are available in the community?

Claude will:
1. Check manifests/categories/display-manifest.yaml (7 objects)
2. List HUB75, VGA, Nextion, and LED matrix drivers
3. Compare features: resolution, color depth, performance
4. Provide download URLs and compatibility notes
5. Suggest best driver for your specific display type
```

```
Find me sensor drivers for environmental monitoring

Claude will:
1. Search manifests/categories/sensors-manifest.yaml (3 objects)
2. Find BME280 (temperature/humidity/pressure)
3. Locate temperature and humidity sensors
4. Show wiring diagrams and calibration procedures
5. Provide complete environmental monitoring example
```

```
What communication protocols are supported by community drivers?

Claude will:
1. Browse manifests/categories/communication-manifest.yaml (4 objects)
2. List UART, SPI, I2C, and wireless drivers
3. Show ESP32 AT commands and WiFi integration
4. Provide protocol comparison and use cases
5. Include performance benchmarks where available
```

### Advanced Discovery Patterns
```
Find the highest quality motor control objects

Claude will:
1. Check manifests/categories/motors-manifest.yaml (5 objects)
2. Sort by quality scores and community ratings
3. Show stepper, servo, and DC motor controllers
4. Compare real-time performance and precision
5. Provide complete motor control system examples
```

```
Which authors are most active in P2 driver development?

Claude will:
1. Scan all author manifests for object counts
2. List top contributors: Jon McPhalen (44), Stephen Moraco (15), Wuerfel_21 (11)
3. Show specialization areas and contribution trends
4. Highlight collaborative projects and cross-references
```

```
Download and test the top 3 P2 audio drivers

Claude will:
1. Browse manifests/categories/audio-manifest.yaml (5 objects)
2. Rank by community usage and quality metrics
3. Provide download URLs and test procedures
4. Generate audio playback and recording examples
5. Include performance comparison results
```

## 🎯 Specific Component Queries

### Instruction Lookup
```
What P2 instructions are available for [OPERATION TYPE]?
Check the [CATEGORY] section in manifests/pasm2-manifest.yaml
and detailed YAMLs in engineering/knowledge-base/P2/language/pasm2/[category]/
```

### Pin Mode Selection
```
Which Smart Pin mode should I use for [SIGNAL TYPE]?
List relevant modes from engineering/knowledge-base/P2/hardware/smart-pins/modes/
with their binary codes and configuration requirements.
```

### Architecture Questions
```
Explain the P2's [ARCHITECTURAL FEATURE].
Reference engineering/knowledge-base/P2/architecture/
and manifests/architecture-manifest.yaml
```

## 💡 Power User Tips

### Get Enriched Documentation
```
Is the [INSTRUCTION/METHOD] documentation enriched?
Check if it has description, examples, and encoding details
in the YAML file.
```

### Find Code Patterns
```
Show me real-world patterns for [TECHNIQUE].
Search in external-projects/*/spin2-patterns-*.md
for proven implementations.
```

### Validate Generated Code
```
Please validate this code against the P2 specifications:
[PASTE CODE]

Check against the relevant YAML specifications for correctness.
```

## 🎨 Project Templates

### New Driver Development
```
I'm writing a P2 driver for [DEVICE].
Using the driver template patterns from:
- P2-FLASH-FS/spin2-driver-template.spin2
- p2-HUB75-LED-Matrix-Driver/spin2-patterns-hub75.md

Help me structure the driver with proper multi-COG safety.
```

### Real-Time Application
```
I need a real-time P2 application with:
- [LIST REQUIREMENTS]

Using the P2's deterministic timing and multi-COG architecture,
design the system referencing patterns from the knowledge base.
```

### Protocol Implementation
```
Implement [PROTOCOL] on P2.
Use Smart Pins where applicable (check modes/)
and PASM2 for timing-critical sections.
Reference any similar implementations in external-projects/.
```

## ⚡ Quick Lookups

### Get All Instructions in a Category
```
List all P2 [CATEGORY] instructions with brief descriptions.
Use manifests/pasm2-manifest.yaml and the category YAML.
```

### Compare Smart Pin Modes
```
Compare Smart Pin modes for [USE CASE].
Show pros/cons of each applicable mode from modes/*.yaml
```

### Find Spin2 Method
```
How do I [OPERATION] in Spin2?
Check engineering/knowledge-base/P2/language/spin2/methods/
for the appropriate method.
```

## 🔍 Navigation Shortcuts

### By Manifest Type
- **Instructions**: `manifests/pasm2-manifest.yaml`
- **Smart Pins**: `manifests/smart-pins-manifest.yaml`
- **Spin2**: `manifests/spin2-manifest.yaml`
- **Architecture**: `manifests/architecture-manifest.yaml`
- **Hardware**: `manifests/hardware-manifest.yaml`
- **Community**: `manifests/obex-community-manifest.yaml` ✨

### By Knowledge Type
- **PASM2**: `engineering/knowledge-base/P2/language/pasm2/`
- **Spin2**: `engineering/knowledge-base/P2/language/spin2/`
- **Smart Pins**: `engineering/knowledge-base/P2/hardware/smart-pins/`
- **Architecture**: `engineering/knowledge-base/P2/architecture/`

### By Example Type
- **Flash FS**: `external-projects/P2-FLASH-FS/`
- **HUB75 LED**: `external-projects/p2-HUB75-LED-Matrix-Driver/`
- **Patterns**: `*/spin2-patterns-*.md`

### By Community Resources
- **By Category**: `manifests/categories/[category]-manifest.yaml`
- **By Author**: `manifests/authors/[author]-manifest.yaml`
- **Top Contributors**: Jon McPhalen (44), Stephen Moraco (15), Wuerfel_21 (11)

## 🆘 Troubleshooting

### Can't Find Information
```
I can't find information about [TOPIC].
Please check:
1. The manifests/ directory
2. Search in engineering/knowledge-base/P2/
3. Look for patterns in external-projects/
4. Check community resources in manifests/obex-community-manifest.yaml
5. Check the .ai-manifest.json completeness section
```

### Code Not Working
```
This P2 code isn't working as expected:
[PASTE CODE]

Please check it against:
1. Instruction encodings in relevant YAMLs
2. Smart Pin configurations if applicable
3. Known patterns from external-projects/
4. Similar community implementations in OBEX manifests
```

### Need Community Solution
```
I need a community-tested solution for [PROBLEM].
Check manifests/obex-community-manifest.yaml and category manifests
for proven implementations. Compare multiple solutions and recommend
the best approach with download URLs.
```

## 📝 Pattern Guidelines

- Always mention "P2 Knowledge Base" in your prompts
- Start with manifests for navigation
- Use specific YAML paths when possible
- Check enrichment status in .ai-manifest.json
- Reference patterns from real projects
- For community resources, specify author or category for targeted search
- Include download URLs and setup guidance for OBEX objects

---

*This comprehensive pattern library covers all major P2 development scenarios with both official documentation and community resources.*
# Opus Request: Enhance Green Book Tutorial with Images and Examples

## Context
You previously generated the P2 Smart Pins Green Book Tutorial (2,821 lines) which is excellent but lacks images and may be missing some examples from the original source material. We need you to enhance this tutorial by incorporating all visual elements and examples from the original documentation.

## Source Document Summary
**Your enhancement workflow uses these specific sources:**

1. **BASE DOCUMENT**: Your own Green Book Tutorial (P2-Smart-Pins-Green-Book-Tutorial.md)
   - Keep all existing tutorial text and structure
   - This is your foundation - enhance it, don't replace it

2. **IMAGE SOURCES**: 
   - Original Titus Smart Pins document (all timing diagrams, signal flows, waveforms)
   - Our Smart Pins Master Diagram (assets/smart-pins-master-trimmed.png)
   - Insert these images at appropriate narrative points

3. **CODE EXAMPLE SOURCES**:
   - **PASM2**: Audit against Titus document - ensure all PASM2 examples are present
   - **Spin2**: Pull from the original Smart Pins Opus Master (P2-Smart-Pins-Complete-Reference.md)
   - **Configuration**: From Titus document CON blocks

**In short**: Take your Green Book text + Add Titus/our images + Audit Titus PASM2 + Add Opus Master Spin2 = Complete Green Book with Images

## Your Task
Take the existing Green Book Tutorial and create an enhanced version that includes:

### 1. Images to Incorporate
**From the Original Titus Smart Pins Document:**
- All timing diagrams for each mode
- All signal flow diagrams  
- All configuration diagrams
- All waveform examples
- Pin numbering diagrams
- Register layout diagrams

**Our Additional Master Diagram:**
- `![Smart Pin Block Diagram](assets/smart-pins-master-trimmed.png)` - Should appear early in the document as the primary architectural overview

**Image Placement Guidelines:**

**CRITICAL PLACEMENT RULES:**
1. **NEVER place images before headings** - Images must always appear WITHIN section content
2. **Place images at natural pause points** in the narrative where the reader needs visual clarification
3. **Follow this placement hierarchy:**
   - After introducing a concept that needs visualization
   - After describing a process that benefits from a diagram
   - Between explanation and example code
   - After a complex configuration description
   - NEVER as the first element after a heading

**Correct Placement Example:**
```markdown
### Mode %00101: PWM Sawtooth

This mode generates a PWM signal using a sawtooth comparison method. The Smart Pin continuously compares an incrementing counter against the configured threshold value.

![PWM Sawtooth Waveform](assets/P2 SmartPins-220809_page17_img01.png)

The waveform shows how the output toggles when the counter reaches the threshold...
```

**INCORRECT Placement (Never Do This):**
```markdown
### Mode %00101: PWM Sawtooth

![PWM Sawtooth Waveform](assets/P2 SmartPins-220809_page17_img01.png)

This mode generates a PWM signal...
```

**Narrative Flow Considerations:**
- Introduce the concept first with text
- Place the image where it answers the question "what does this look like?"
- Follow the image with text that references what the reader can see
- For complex topics, use multiple images progressively (overview → detail)
- Consider the image as a "visual paragraph" that supports the surrounding text

**Additional Requirements:**
- Use descriptive alt text for accessibility
- All images must reference the `assets/` directory
- Format: `![Descriptive Alt Text](assets/filename.png)`

### 2. Examples Audit and Integration
**Comprehensive Code Example Audit:**

**Step 1: Audit ALL examples from the original Titus document:**
- Every configuration example (CON blocks)
- Every PASM2 assembly example
- Every operational example
- Every use case demonstration

**Step 2: Ensure corresponding Spin2 code exists for EACH example:**
- For every PASM2 example in Titus, there must be a Spin2 equivalent
- **USE THE EXISTING SMART PINS OPUS MASTER** (P2-Smart-Pins-Complete-Reference.md) as your source for Spin2 examples
- This original Opus Master document already contains validated Spin2 implementations for all modes
- Located at: `/documentation/manuals/smart-pins-workshop/opus-master/P2-Smart-Pins-Complete-Reference.md`

**Step 3: Example Structure for Each Mode:**
```
### Mode %XXXXX: [Mode Name]

**Configuration** (from Titus)
```{.configuration}
[CON block settings]
```

**Spin2 Implementation** (from Blue Book Opus Master or newly created)
```spin2
[Spin2 code example]
```

**PASM2 Implementation** (from Titus)
```pasm2
[PASM2 code example]
```
```

**Source Priority for Examples:**
1. **PRIMARY SOURCE**: Use Spin2 examples from the original Smart Pins Opus Master document
   - Path: `/documentation/manuals/smart-pins-workshop/opus-master/P2-Smart-Pins-Complete-Reference.md`
   - This document has complete, validated Spin2 code for all 32 modes
2. If any mode lacks a Spin2 example in the Opus Master, create one based on the Titus PASM2 example
3. Ensure every mode has complete example sets: Configuration + Spin2 + PASM2

**Quality Requirements:**
- Every mode must have at least one complete example set (Config + Spin2 + PASM2)
- Complex modes should have multiple examples showing different use cases
- Examples should build in complexity (simple → advanced)
- Include comments explaining key concepts

### 3. Specific Images by Section

**Part I - Fundamentals:**
- Smart Pin master block diagram (our enhanced version)
- Pin numbering diagram
- Basic configuration flow diagram

**Part II - Smart Pin Modes:**
For EACH of the 32 modes, ensure these images are present where applicable:
- Mode-specific block diagram
- Timing diagram (for synchronous modes)
- Waveform examples (for signal generation modes)
- Signal flow diagram (for measurement modes)

**Example for Mode %00000: DAC Output:**
```markdown
### Mode %00000: DAC Output

[Tutorial text...]

![DAC Output Characteristic](assets/P2 SmartPins-220809_page13_img01.png)

[More tutorial text...]

![DAC Signal Flow](assets/dac-signal-flow.png)
```

### 4. Image References from Blue Book
These specific images from the Blue Book Reference MUST be included:
- `assets/smart-pins-master-trimmed.png` - Master architecture diagram
- `assets/P2 SmartPins-220809_page04_img01.png` - Configuration flow
- `assets/P2 SmartPins-220809_page13_img01.png` - DAC output
- `assets/P2 SmartPins-220809_page15_img01.png` - NCO frequency
- `assets/P2 SmartPins-220809_page17_img01.png` - PWM sawtooth
- `assets/P2 SmartPins-220809_page17_img02.png` - PWM triangle
- `assets/P2 SmartPins-220809_page19_img01.png` - Pulse/cycle output
- `assets/P2 SmartPins-220809_page20_img01.png` - Transition output
- `assets/P2 SmartPins-220809_page21_img01.png` - NCO duty
- `assets/P2 SmartPins-220809_page23_img01.png` - Sync serial TX
- [... and all other mode-specific diagrams from the original]

### 5. Maintain Existing Structure
- Keep all existing tutorial text and explanations
- Keep all semantic div markers (`::: needs-diagram`, etc.)
- Keep the progressive learning approach
- Keep all exercises and key takeaways
- Simply ADD the images and any missing examples

### 6. Quality Checks
Ensure that after enhancement:
- Every Smart Pin mode has at least one diagram
- Every complex timing relationship has a timing diagram
- Every configuration pattern has an example
- Image placement enhances understanding, not interrupts reading flow

## Output Format
Provide the enhanced Green Book Tutorial as a complete markdown document with:
- All images properly referenced
- All examples verified present
- Maintains the ~3000 line tutorial format
- Ready for PDF generation

## IMPORTANT: Document Versioning
**This will be a NEW document, not a replacement:**
- **Original Green Book**: `P2-Smart-Pins-Green-Book-Tutorial.md` (already protected, no images)
- **New Enhanced Version**: `P2-Smart-Pins-Green-Book-Tutorial-With-Images.md`

**File Management:**
1. The original Green Book remains protected at:
   `/documentation/manuals/smart-pins-workshop/opus-master-green-book/P2-Smart-Pins-Green-Book-Tutorial.md`
2. This new enhanced version will be saved as:
   `P2-Smart-Pins-Green-Book-Tutorial-With-Images.md`
3. Both versions will be preserved for different purposes:
   - Original: Historical record of pure tutorial text
   - Enhanced: Production version with full visual support

**Rationale for Separate Documents:**
- Preserves the original generation as a reference
- Allows comparison between text-only and visual versions
- Maintains clear version history
- Each can be protected independently
- Future updates can reference either version as needed

## Note on Image Files
The actual image files exist in our repository. You just need to add the markdown references. Use the exact filenames from the original Titus document (P2 SmartPins-220809_pageXX_imgXX.png format) where applicable.

---

This enhancement will transform the Green Book from a text-only tutorial into a comprehensive visual learning resource that matches or exceeds the reference documentation in clarity and completeness.
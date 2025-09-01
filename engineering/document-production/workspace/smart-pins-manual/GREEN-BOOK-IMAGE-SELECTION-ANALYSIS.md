# Why the Green Book Didn't Use All Available Titus Images

**Date**: 2025-08-30  
**Question**: Why did Opus 4.1 select only 14 of 23 available Smart Pins images?

## Image Selection Analysis

### Available vs Used Breakdown
- **Total Available**: 23 images from Titus Smart Pins extraction  
- **Used in Green Book**: 14 images (60.9%)
- **Unused**: 8 images + 1 overview image (39.1%)

## Most Likely Explanations

### 1. **Tutorial vs Reference Document Strategy**

**The Green Book is a TUTORIAL, not a comprehensive reference**:

- **Reference documents** (like the original Blue Book): Show every detail, every variation, every technical specification
- **Tutorial documents** (like the Green Book): Focus on learning progression, core concepts, essential examples

**Evidence**: The unused images represent:
- **Secondary details** that don't aid initial learning
- **Advanced variations** beyond tutorial scope  
- **Redundant information** that might confuse beginners

### 2. **Pedagogical Image Selection by Opus 4.1**

When Opus 4.1 created the Green Book, it likely applied **educational design principles**:

**Used Images (Teaching-Focused)**:
- `page03_img01` - **Foundation**: Smart Pin block diagram (architectural understanding)
- `page04_img01` - **Process**: Configuration flow (how-to knowledge)
- `page17_img01/02` - **Comparison**: Sawtooth vs Triangle PWM (contrasting concepts)
- `page19_img01` - **Timing**: Quadrature signals (dynamic behavior)
- `page29_img01` - **Classification**: State measurement modes (categorization)

**Unused Images (Detail-Focused)**:
- `page04_img02` - **Secondary config details** (might overwhelm beginners)
- `page16_img01` - **Additional PWM specifics** (beyond core PWM concept)
- `page20/21_img01` - **Encoder timing details** (advanced implementation)
- `page33_img01` - **ADC implementation details** (internal complexity)
- `page46_img02` - **Serial timing variations** (beyond basic understanding)

### 3. **Narrative Flow Optimization**

**Tutorial Writing Best Practices Applied**:

1. **One Concept, One Image**: Each major concept gets exactly the visual aid it needs
2. **Progressive Complexity**: Images support learning sequence, not exhaustive coverage
3. **Cognitive Load Management**: Too many images can overwhelm tutorial readers
4. **Essential vs Nice-to-Have**: Focus on images that are necessary for understanding

### 4. **Content Strategy Differences**

**Original Titus Document Strategy**:
- **Comprehensive reference**: Include every available diagram
- **Technical completeness**: Show all variations and details
- **Expert audience**: Assume readers want maximum information

**Green Book Tutorial Strategy**:  
- **Learning-focused**: Include diagrams that teach effectively
- **Beginner-friendly**: Avoid information overload
- **Practical mastery**: Focus on what users need to get started

## Specific Image Analysis

### Why These Weren't Selected:

**`page04_img02` (Secondary Config)**:
- Primary config flow (page04_img01) already teaches the process
- Secondary details might confuse "how do I configure?" learning goal

**`page16_img01` (PWM Details)**:
- Sawtooth (page17_img01) and Triangle (page17_img02) already demonstrate PWM concepts
- Additional PWM details beyond tutorial scope

**`page20/21_img01` (Encoder Timing)**:
- Basic encoder signals (page19_img01) sufficient for tutorial understanding
- Detailed timing analysis more appropriate for reference material

**`page23_img01` (Period Measurement)**:
- Later measurement modes diagram (page29_img01) more comprehensive
- Earlier diagram possibly redundant or less clear

**`page33_img01` (ADC Details)**:
- Filter response (page31_img01) and scope mode (page32_img01) cover ADC fundamentals
- Internal implementation details beyond tutorial needs

**`page46_img02` (Serial Details)**:
- Basic synchronous timing (page46_img01) teaches the core concept
- Additional serial variations not essential for initial learning

**`smart-pins-master.png` (Overview)**:
- Tutorial starts with architectural diagram (page03_img01) 
- Comprehensive overview might be overwhelming as introduction

## Key Insight: Educational Design at Work

**This image selection demonstrates sophisticated educational design**:

1. **Deliberate curation** over comprehensive inclusion
2. **Learning objectives** driving visual aid selection  
3. **Tutorial effectiveness** prioritized over complete technical coverage
4. **Beginner success** valued over expert reference completeness

## Conclusion

**The unused images weren't "missed" or "forgotten"** - they represent **intentional editorial choices** by Opus 4.1 to create an effective learning document rather than a comprehensive reference.

**This explains**:
- Why the narrative has no gaps or missing references
- Why each used image serves a clear pedagogical purpose
- Why the tutorial flows logically without the unused images
- Why adding unused images would require new narrative content

**The Green Book achieves its goal**: Teaching Smart Pins effectively with exactly the visual aids that support learning, not exhaustive technical documentation.

**Bottom Line**: The image selection reflects **tutorial design expertise**, not oversights.
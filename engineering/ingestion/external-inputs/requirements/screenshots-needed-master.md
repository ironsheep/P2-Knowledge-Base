# Screenshots Needed - Master Request List

## Overview
Consolidated list of all screenshots/images needed from source documents for complete extraction coverage.

---

## SPIN2 v51 Documentation - Terminal Window Images

### req01: DEBUG Terminal Output
- **Source**: SPIN2 v51 Documentation
- **Location**: Look for basic DEBUG terminal output example
- **Title**: "DEBUG Terminal Output" (if titled)
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Shows basic text output in debug terminal
- **Expected**: Terminal window with text/values being displayed
- **Usage**: Terminal Window Manual - Basic Output section

### req02: SCOPE Display - Waveform
- **Source**: SPIN2 v51 Documentation  
- **Location**: DEBUG SCOPE examples section
- **Title**: "SCOPE Display" or similar
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Demonstrates oscilloscope display with waveforms
- **Expected**: Scope window showing sine/square waves with grid
- **Usage**: Terminal Window Manual - Oscilloscope Features

### req03: SCOPE with Anti-aliasing
- **Source**: SPIN2 v51 Documentation
- **Location**: Section mentioning anti-aliasing improvements
- **Title**: "Anti-aliased Scope Display" (if present)
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Shows difference with anti-aliasing enabled
- **Expected**: Smooth waveforms demonstrating AA feature
- **Usage**: Terminal Window Manual - Display Quality section

### req04: PLOT Display Example
- **Source**: SPIN2 v51 Documentation
- **Location**: DEBUG PLOT section
- **Title**: "PLOT Display" or "XY Plot"
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Shows 2D plotting capabilities
- **Expected**: XY plot window with data points or lines
- **Usage**: Terminal Window Manual - Plotting Features

### req05: PLOT with Sprites
- **Source**: SPIN2 v51 Documentation
- **Location**: Section about sprites in PLOT (v35o update)
- **Title**: "PLOT Display with Sprites"
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Demonstrates sprite overlay feature
- **Expected**: Plot window with sprite graphics
- **Usage**: Terminal Window Manual - Advanced Plot Features

### req06: FFT Display
- **Source**: SPIN2 v51 Documentation
- **Location**: DEBUG FFT section (if present)
- **Title**: "FFT Display" or "Frequency Analysis"
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Shows frequency domain analysis
- **Expected**: FFT window with frequency spectrum
- **Usage**: Terminal Window Manual - Signal Analysis

### req07: LOGIC Analyzer Display
- **Source**: SPIN2 v51 Documentation
- **Location**: DEBUG LOGIC section
- **Title**: "LOGIC Display" or "Logic Analyzer"
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Shows digital signal traces
- **Expected**: Logic analyzer window with multiple signal traces
- **Usage**: Terminal Window Manual - Digital Analysis

### req08: LOGIC with Analog Waveforms
- **Source**: SPIN2 v51 Documentation
- **Location**: Section about RANGE keyword for analog display (v48 update)
- **Title**: "LOGIC Display with Analog Waveforms"
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Shows multi-bit groups as analog waveforms
- **Expected**: Logic display with both digital and analog traces
- **Usage**: Terminal Window Manual - Mixed Signal Display

### req09: Multiple DEBUG Windows
- **Source**: SPIN2 v51 Documentation
- **Location**: Example showing multiple windows open
- **Title**: "Multiple DEBUG Windows" (if present)
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Demonstrates multi-window debugging
- **Expected**: Several debug windows arranged on screen
- **Usage**: Terminal Window Manual - Window Management

### req10: Bitmap Layer in PLOT
- **Source**: SPIN2 v51 Documentation
- **Location**: Section about LAYER/CROP commands (v50 update)
- **Title**: "PLOT with Bitmap Background"
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Shows bitmap layer feature for backgrounds
- **Expected**: Plot window with loaded bitmap image
- **Usage**: Terminal Window Manual - Background Layers

---

## SPIN2 v51 Documentation - Debugger Images

### req11: Single-Step Debugger Window (FULL)
- **Source**: SPIN2 v51 Documentation
- **Location**: PASM debugger section (v35s addition)
- **Title**: "PASM Single-Step Debugger"
- **For Extraction**: Single Step Debugger Focused Extraction
- **Purpose**: Shows complete debugger interface layout
- **Expected**: FULL debugger window with ALL regions visible
- **Usage**: Debugger Manual - Interface Overview
- **CRITICAL**: Need the ENTIRE window to show scale/size

### req12: Breakpoint Indicators
- **Source**: SPIN2 v51 Documentation
- **Location**: Breakpoint documentation
- **Title**: "Breakpoints in Code"
- **For Extraction**: Single Step Debugger Focused Extraction
- **Purpose**: Shows how breakpoints appear in editor
- **Expected**: Code with breakpoint markers
- **Usage**: Debugger Manual - Setting Breakpoints

### req13: Register Display
- **Source**: SPIN2 v51 Documentation
- **Location**: Debugger register view section
- **Title**: "Register Values Display"
- **For Extraction**: Single Step Debugger Focused Extraction
- **Purpose**: Shows COG register monitoring
- **Expected**: Register window with hex values
- **Usage**: Debugger Manual - Register Inspection

### req14: Memory View
- **Source**: SPIN2 v51 Documentation
- **Location**: Memory inspection section
- **Title**: "Memory Inspector" (if present)
- **For Extraction**: Single Step Debugger Focused Extraction
- **Purpose**: Shows memory examination features
- **Expected**: Hex dump style memory display
- **Usage**: Debugger Manual - Memory Analysis

### req15: Debugger Code Pane (REGION)
- **Source**: SPIN2 v51 Documentation OR Screenshot
- **Location**: Cropped from full debugger
- **Title**: "Code Execution Pane"
- **For Extraction**: Single Step Debugger Focused Extraction
- **Purpose**: Focus on code display area with current line
- **Expected**: Just the code region with execution pointer
- **Usage**: Debugger Manual - Code Navigation section

### req16: Debugger Register Display (REGION)
- **Source**: SPIN2 v51 Documentation OR Screenshot
- **Location**: Cropped from full debugger
- **Title**: "COG Register Display"
- **For Extraction**: Single Step Debugger Focused Extraction
- **Purpose**: Focus on register values and changes
- **Expected**: Register region showing hex values, maybe with changes highlighted
- **Usage**: Debugger Manual - Register Monitoring section

### req17: Debugger Control Buttons (REGION)
- **Source**: SPIN2 v51 Documentation OR Screenshot
- **Location**: Cropped from full debugger
- **Title**: "Debugger Controls"
- **For Extraction**: Single Step Debugger Focused Extraction
- **Purpose**: Show step/run/pause/stop controls clearly
- **Expected**: Control button bar with labels
- **Usage**: Debugger Manual - Execution Control section

### req18: Two Debuggers Side-by-Side
- **Source**: Screenshot (you'll need to create)
- **Location**: Custom screenshot
- **Title**: "Multiple COG Debugging Reality"
- **For Extraction**: Single Step Debugger Focused Extraction
- **Purpose**: Show screen real estate challenge
- **Expected**: Two debugger windows filling a typical monitor
- **Usage**: Debugger Manual - Multi-COG Debugging Strategies
- **NOTE**: This demonstrates the practical limit of 2 debuggers on screen

---

## Terminal Window Pedagogical Assets

### req19: SCOPE Display Controls (REGION)
- **Source**: SPIN2 v51 OR Screenshot
- **Location**: Cropped from SCOPE window
- **Title**: "SCOPE Control Region"
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Focus on oscilloscope controls
- **Expected**: Trigger, scale, offset controls
- **Usage**: Terminal Window Manual - SCOPE Controls section

### req20: PLOT Display with Multiple Traces
- **Source**: SPIN2 v51 OR Screenshot
- **Location**: PLOT example
- **Title**: "Multi-trace PLOT Display"
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Show multiple data series capability
- **Expected**: XY plot with several colored traces
- **Usage**: Terminal Window Manual - Advanced Plotting

### req21: Color Palette Examples
- **Source**: SPIN2 v51 OR Screenshot
- **Location**: Any DEBUG display
- **Title**: "DEBUG Color Palettes"
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Show different color scheme options
- **Expected**: Same display with different palettes
- **Usage**: Terminal Window Manual - Display Customization

### req22: Multi-Window DEBUG Layout
- **Source**: Screenshot (you'll create)
- **Location**: Custom arrangement
- **Title**: "Multiple DEBUG Windows"
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Show practical multi-window debugging
- **Expected**: 3-4 different DEBUG windows arranged
- **Usage**: Terminal Window Manual - Window Management

---

## P2 Silicon Documentation Images

### req23: Pin Schematic
- **Source**: P2 Documentation v35 PDF
- **Location**: Pages 76-84 (as previously identified)
- **Title**: "P2 Pin Configuration"
- **For Extraction**: Hardware Manual sections
- **Purpose**: Shows physical pin connections
- **Expected**: Detailed pin schematic diagrams
- **Usage**: Hardware Reference - Pin Configuration

### req24: Block Diagram
- **Source**: P2 Documentation v35 PDF
- **Location**: Architecture overview section
- **Title**: "P2 Block Diagram"
- **For Extraction**: Architecture documentation
- **Purpose**: Shows overall chip architecture
- **Expected**: Block diagram with COGs, Hub, Smart Pins
- **Usage**: Architecture Overview - System Design

---

## Priority Notes

**HIGH PRIORITY** (Needed for Terminal/Debugger Manuals):
- req01-req22 (All SPIN2 v51 terminal and debugger screenshots)
- Especially req11 (FULL debugger window) - CRITICAL for showing scale
- Regional screenshots (req15-req17) can be cropped from req11 if needed
- req18 (two debuggers) demonstrates practical limitations

**MEDIUM PRIORITY** (Enhance understanding):
- req23-req24 (Hardware diagrams from Silicon Doc)

**Note**: If any expected images are not present in the documents, please note "NOT FOUND" and we'll identify alternatives or create synthetic examples.

---

## File Naming Convention
Suggested format: `[source]-[page]-[feature].png`
Example: `spin2-v51-p125-scope-antialiasing.png`
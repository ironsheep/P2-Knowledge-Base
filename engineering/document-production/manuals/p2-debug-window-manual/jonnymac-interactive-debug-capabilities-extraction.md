# JonnyMac Interactive Debug Capabilities - Complete Extraction

**Source**: JonnyMac's undocumented debug examples (`jpnnyMac-examples/`)
**Discovery Date**: 2025-09-14
**Significance**: Revolutionary interactive debug capabilities completely missing from SPIN-2 v5.1

---

## 🚀 **MAJOR BREAKTHROUGH DISCOVERY**

JonnyMac has reverse-engineered **advanced interactive BITMAP debugging capabilities** that transform debug windows from passive displays into **interactive graphical applications**. This represents the most significant gap between documented and actual P2 debug capabilities.

---

## 📊 **DISCOVERED CAPABILITIES MATRIX**

### **Interactive Layer Composition System**

| Command | Syntax | Purpose | Example |
|---------|---------|---------|---------|
| `LAYER` | `debug(`window layer N 'file.bmp')` | Load image into layer N | Background graphics, sprite sheets |
| `CROP` | `debug(`window crop N)` | Show entire layer N | Display background layer |
| `CROP` | `debug(`window crop N x y w h)` | Show layer portion at position | Selective updates, animations |
| `CROP` | `debug(`window crop N sx sy sw sh dx dy)` | Copy source region to destination | Sprite positioning, digit displays |

### **PC Input Integration Commands**

| Command | Syntax | Variables Updated | Real-time Capability |
|---------|---------|---------|---------|
| `PC_KEY` | `debug(`window `pc_key(@key))` | Single key variable | Keyboard shortcuts, mode switching |
| `PC_MOUSE` | `debug(`window `pc_mouse(@x))` | x, y, wheeldelta, lbutton, mbutton, rbutton | Click detection, parameter control |

### **Advanced Drawing Commands**

| Command | Syntax | Purpose | Precision Level |
|---------|---------|---------|---------|
| `SET` | `debug(`window set `(x, y))` | Position drawing cursor | Pixel-level positioning |
| `LINE` | `debug(`window line `(x, y))` | Draw line from cursor | Vector graphics |
| `CIRCLE` | `debug(`window circle radius)` | Draw circle at cursor | Geometric shapes |
| `TEXTSTYLE` | `debug(`window textstyle %flags color text size 'text')` | Formatted text output | Professional typography |
| `CARTESIAN` | `debug(`window cartesian 1 0 precise)` | High-precision coordinate system | Fixed-point calculations |
| `LINESIZE` | `debug(`window linesize $400)` | Fixed-point line width | Sub-pixel precision |

---

## 🎮 **INTERACTIVE DEBUG APPLICATIONS DISCOVERED**

### **1. Analog Meter Dashboard** (`jm_debug_analog_meter_050.spin2`)

**Capability**: Professional analog instrumentation with real-time needle movement

**Key Techniques**:
```spin2
' High-precision needle positioning using CORDIC
x1 := qcos(190<<8, aval-1400, 3600)
y1 := qsin(190<<8, aval-1400, 3600)
debug(`amp set `(160<<8, 225<<8))      ' Fixed-point coordinates
debug(`amp line `(x1+160<<8, y1+225<<8))

' Multi-layer digit display with decimal points
debug(`amp crop 1 `(n*45, y2, 45, 60, x1, 161))  ' Source digit from sprite sheet
```

**Applications**:
- Motor control dashboards  
- Sensor monitoring displays
- Real-time parameter visualization
- Professional instrumentation emulation

### **2. LED Binary Display Panel** (`jm_debug_panel_010.spin2`)

**Capability**: Multi-state LED visualization with automatic color management

**Key Techniques**:
```spin2
' Dynamic layer selection based on data
img := value.[bit] + 1 + (ledcolor * value.[bit])  ' Calculate layer: off/red/green
debug(`panel crop `(img, x, y, 50, 50))           ' Update specific LED
```

**Applications**:
- Binary data visualization
- Multi-channel status displays  
- Real-time bit pattern monitoring
- Hardware register visualization

### **3. Interactive Binary Switches** (`jm_debug_switches_030.spin2`)

**Capability**: PC-controllable switches with multi-radix display

**Key Techniques**:
```spin2
' Mouse click detection on specific regions
if (lbutton)
  if (ypos >= 129) && (ypos <= 179)
    case xpos
      265..285 : toggle_bit(0)     ' Precise click zones for each switch

' Multi-radix display with sprite-based digits
x2 := d * 33                       ' Locate digit in sprite sheet
debug(`switches crop 3 `(x2, 0, 33, 50, x1, 28))  ' Place digit from sheet
```

**Applications**:
- Interactive parameter adjustment
- Binary/hex/decimal conversion tools
- Educational bit manipulation
- Configuration interface development

### **4. PlayStation Controller Emulation** (`jm_debug_ps2_controller_020.spin2`)

**Capability**: Real-time hardware interface visualization

**Key Techniques**:
```spin2
' Button state visualization
debug(`ps2 crop `(btnslo.[0]+1, 255, 163, 30, 19))  ' Layer 1=off, 2=on

' Real-time text overlays
debug(`ps2 textstyle %11110000 color black text 14 '`(lx))

' Dynamic circle positioning for analog sticks  
debug(`ps2 set `(238-28+lx, 254-28+ly))
debug(`ps2 circle 15)
```

**Applications**:
- Hardware interface testing
- Real-time input monitoring
- Protocol debugging visualization
- Interactive control system testing

### **5. Digital Display Panel** (`jm_debug_panel_digits_020.spin2`)

**Capability**: Professional 7-segment display emulation

**Key Techniques**:
```spin2
' Sprite-based digit rendering with leading zero suppression
if (i == 0) || (value)                               ' Show digit?
  x2 := d * 44                                       ' Locate in sprite sheet
  debug(`panel crop 3 `(x2, 0, 44, 54, x1, 53))      ' Place from sheet
```

**Applications**:
- Numeric data display
- Counter visualization
- Parameter monitoring
- Professional instrument panels

---

## 🔧 **ADVANCED TECHNICAL CAPABILITIES**

### **Layered Sprite System**
- **Multi-layer image loading** - Background + multiple overlay states
- **Selective layer display** - Show different layers based on data
- **Sprite sheet extraction** - Copy portions of images to create animations
- **State-driven visualization** - Automatic graphic selection based on values

### **High-Precision Graphics**  
- **Fixed-point coordinates** - Sub-pixel positioning accuracy
- **CORDIC integration** - Hardware-accelerated trigonometry for graphics
- **Precise line rendering** - Fractional pixel line widths
- **Professional typography** - Text styling with size and color control

### **Real-time PC Integration**
- **Bidirectional communication** - PC controls P2, P2 updates display
- **Mouse region detection** - Clickable interface zones
- **Keyboard shortcuts** - Mode switching and parameter control
- **Interactive debugging** - Live parameter adjustment during execution

---

## 🎯 **DEVELOPMENT WORKFLOW PATTERNS**

### **Pattern 1: Interactive Instrument Creation**
1. **Design background graphic** with instrument layout
2. **Create sprite sheets** for all possible states/values  
3. **Implement layer system** for state visualization
4. **Add PC input handling** for interactive control
5. **Update display** using selective CROP operations

### **Pattern 2: Real-time Hardware Visualization**
1. **Connect actual hardware** to P2 pins
2. **Create visual representation** matching hardware layout
3. **Map hardware states** to sprite layers
4. **Update graphics** in sync with hardware changes
5. **Add value overlays** for precise measurements

### **Pattern 3: Interactive Development Tools**
1. **Define clickable regions** for parameter control
2. **Implement mouse detection** for user interaction  
3. **Create visual feedback** for user actions
4. **Update calculations** based on user input
5. **Display results** with professional graphics

---

## 📊 **PERFORMANCE CHARACTERISTICS**

### **Update Efficiency**
- **Selective updates** - Only changed regions redrawn
- **Layer caching** - Background graphics loaded once
- **Sprite positioning** - Fast copy operations vs. drawing
- **Minimal data transfer** - Small CROP operations vs. full redraws

### **Interaction Responsiveness**  
- **Real-time input polling** - PC_KEY/PC_MOUSE zero-latency
- **Immediate visual feedback** - Graphics update on same frame
- **Precise click detection** - Pixel-level accuracy for controls
- **Smooth animations** - High-precision coordinate updates

---

## 🔍 **CRITICAL IMPLEMENTATION DETAILS**

### **Layer Management Strategy**
```spin2
' Setup phase - load all required images
debug(`window layer 1 'background.bmp')     ' Base graphics
debug(`window layer 2 'elements_off.bmp')   ' Default state  
debug(`window layer 3 'elements_on.bmp')    ' Active state
debug(`window layer 4 'digits.bmp')         ' Text/numbers
```

### **Efficient Update Pattern**
```spin2
' Runtime - selective updates only
debug(`window crop 1 region_x region_y region_w region_h)  ' Clear area
debug(`window crop 3 src_x src_y src_w src_h dst_x dst_y)   ' Place new graphic
debug(`window update)                                      ' Refresh display
```

### **PC Input Integration Pattern**
```spin2
' Polling loop for user interaction
debug(`window `pc_mouse(@xpos))           ' Get current mouse state
if (lbutton)                             ' Process mouse clicks
  ' Determine clicked region and respond
if (key := PC_KEY())                     ' Process keyboard input
  ' Handle shortcuts and mode changes
```

---

## 🎯 **UNIQUE P2 DEBUG ADVANTAGES REVEALED**

### **Hardware-Software Integration**
- **Real hardware interfaces** - Actual sensors/controllers visualized
- **Silicon-level debugging** - Hardware pins mapped to graphics
- **Multi-COG coordination** - Visual debugging across multiple processors
- **Built-in performance** - No external graphics libraries required

### **Development Workflow Integration**
- **Live parameter tuning** - Adjust values while code runs
- **Visual debugging** - See data relationships graphically
- **Interactive testing** - Control system via mouse/keyboard  
- **Professional presentation** - Client-ready debugging displays

---

## 📋 **MANUAL INTEGRATION PRIORITY**

**CRITICAL**: These interactive capabilities represent the **most significant advancement** in P2 debug window usage. They transform debug windows from:
- ❌ **Passive data display** → ✅ **Interactive development environments**
- ❌ **Text-based debugging** → ✅ **Professional graphical interfaces**  
- ❌ **One-way information** → ✅ **Bidirectional control systems**

**Manual Requirements**:
1. **Dedicated interactive debugging section** - This deserves major coverage
2. **Layer composition tutorial** - Step-by-step sprite system explanation
3. **PC input integration guide** - Mouse/keyboard control patterns
4. **Professional application examples** - Real-world instrument creation
5. **Performance optimization** - Efficient update strategies

This discovery elevates P2 debug capabilities to **professional development tool** status - unique in the embedded microcontroller world.
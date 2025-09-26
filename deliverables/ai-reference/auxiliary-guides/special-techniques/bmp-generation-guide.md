# P2 Plot Window BMP Generation Guide

## Overview
This guide helps AI assistants generate BMP files for P2 debug visualization using the Plot window's layered display system.

## BMP Requirements
- **Format**: 8-bit indexed color (256 color palette)
- **Typical sizes**: 320x240, 640x480, or custom based on need
- **Byte order**: Little-endian
- **Row padding**: Each row padded to 4-byte boundary

## Recommended Tools

### Python with Pillow (Preferred)
```python
from PIL import Image, ImageDraw, ImageFont

# Create 8-bit image with palette
img = Image.new('P', (320, 240))
img.putpalette([...])  # 256 RGB triplets

# Draw operations
draw = ImageDraw.Draw(img)
draw.rectangle([x1, y1, x2, y2], fill=color_index)
draw.text((x, y), "Text", fill=color_index)

# Save as BMP
img.save("output.bmp", "BMP")
```

### Raw Binary Construction
For simple patterns, directly write BMP header and pixel data:
- 14-byte file header
- 40-byte DIB header
- 1024-byte color palette (256 * 4 bytes)
- Pixel data (1 byte per pixel, row-padded)

## Common P2 Debug Visualizations

### 1. Bar Graphs (Queue/Buffer Fill)
```
Description: "10-segment bar, 200x30 pixels, empty=gray(index 7), filled=green(index 2)"
Layer 1: All segments empty
Layer 2: All segments filled
Usage: Crop segments from Layer 2 to show current fill level
```

### 2. LED Arrays
```
Description: "8 LEDs in row, 20px circles, 5px spacing, off=dark red, on=bright red"
Layer 1: All LEDs off
Layer 2: All LEDs on
Layer 3: Individual LED patterns
```

### 3. 7-Segment Displays
```
Description: "4-digit display, segment width=3px, height=15px, off=gray, on=green"
Layers: One per digit value (0-9, A-F)
```

### 4. Game Boards
```
Description: "3x3 grid, 50px squares, 2px grid lines"
Layer 1: Empty board
Layer 2: X markers (blue)
Layer 3: O markers (red)
Layer 4: Win highlights (yellow)
```

## Standard Color Palette (8-bit)

```
Index 0: Black (0, 0, 0)
Index 1: White (255, 255, 255)
Index 2: Red (255, 0, 0)
Index 3: Green (0, 255, 0)
Index 4: Blue (0, 0, 255)
Index 5: Yellow (255, 255, 0)
Index 6: Cyan (0, 255, 255)
Index 7: Magenta (255, 0, 255)
Index 8-15: Grays (gradient)
Index 16-31: User defined
...
```

## Generation Process

1. **Parse Description**: Extract dimensions, colors, element positions
2. **Create Palette**: Build 256-color palette with needed colors
3. **Generate Layers**: Create separate BMPs for each state
4. **Test Patterns**: Include alignment marks if needed

## Example: Queue Visualization

### Input Description
"Queue display: 10 slots horizontal, each 30x40 pixels, spacing 5px, empty=gray, filled=blue,
text overlay showing position numbers 0-9"

### Generation Steps
1. Calculate total width: 10 * 30 + 9 * 5 = 345 pixels
2. Height: 40 pixels
3. Create 3 layers:
   - Layer 1: All slots empty (gray rectangles)
   - Layer 2: All slots filled (blue rectangles)
   - Layer 3: Position numbers (white text)

### Spin2 Integration
```spin2
' In P2 code
debug(`plot myqueue_empty.bmp 0)    ' Load layer 0
debug(`plot myqueue_full.bmp 1)     ' Load layer 1
debug(`plot myqueue_nums.bmp 2)     ' Load layer 2

' Show queue with 3 items
debug(`plot crop 0 0 0 90 40)       ' First 3 slots from full layer
debug(`plot crop 1 90 0 255 40)     ' Rest from empty layer
debug(`plot crop 2 0 0 345 40)      ' Numbers overlay
```

## Testing Generated BMPs

1. **Verify header**: Check magic bytes "BM"
2. **Validate dimensions**: Match requested size
3. **Check palette**: Ensure colors match indices
4. **Test cropping**: Verify alignment for layer composition

## Best Practices

- Keep BMPs small (minimize memory usage)
- Use consistent color indices across layers
- Include reference grid for alignment testing
- Generate both "all on" and "all off" states
- Document color palette used
- Test with actual P2 Plot commands

## Typical Workflow

1. User provides narrative description
2. AI generates Python script to create BMPs
3. Script produces multiple layer BMPs
4. User integrates with P2 debug code
5. Real-time visualization via Plot window crops

This approach enables rich debug visualization without complex drawing code on the P2 itself.
# Solution Strategies for Debug Manual Code Completeness

**Date**: 2025-09-17  
**Problem**: 160 undefined methods make examples unrunnable  
**Goal**: Complete, compilable examples without overwhelming readers

## Strategy 1: Minimal Stub Library (RECOMMENDED)

### Concept
Create a single `debug_stubs.spin2` file with minimal implementations that make examples compile and demonstrate concepts without real hardware.

### Implementation
```spin2
' debug_stubs.spin2 - Include at top of each example
' Provides minimal implementations for all helper methods

CON
  SIMULATED = true  ' Flag for simulation mode
  
VAR
  long sim_counter
  
' === SENSOR STUBS (15 methods) ===
PUB read_sensor() : value
  ' Returns incrementing test data
  return sim_counter++ // 1000

PUB read_temperature() : value  
  ' Returns realistic temp range 20-30°C
  return 20 + (sim_counter++ // 100) / 10
  
PUB read_pressure() : value
  ' Returns atmospheric pressure ±50 hPa
  return 1013 + (sin(sim_counter++, 50))
  
' === DRAWING STUBS (33 methods) ===  
PUB draw_grid(x, y, w, h, spacing)
  ' Simplified grid - just draws outline
  DEBUG(`PLOT LINE `(x, y, x+w, y))
  DEBUG(`PLOT LINE `(x+w, y, x+w, y+h))
  DEBUG(`PLOT LINE `(x+w, y+h, x, y+h))
  DEBUG(`PLOT LINE `(x, y+h, x, y))
  
PUB draw_button(x, y, w, h, label)
  ' Simple rectangle with text
  DEBUG(`PLOT BOX `(x, y, w, h) COLOR WHITE)
  DEBUG(`PLOT TEXT `(x+w/2, y+h/2) 'label' CENTER)

' === EVENT STUBS (12 methods) ===
PUB handle_mouse() : x, y, buttons
  ' Returns simulated mouse movement
  x := 400 + sin(sim_counter++, 200)
  y := 300 + cos(sim_counter, 150)
  buttons := 0
```

### Advantages
- **Single file** to include: `#include "debug_stubs.spin2"`
- **~200 lines total** for all 160 methods
- Examples remain **focused** on debug concepts
- **Actually compiles** and runs
- Shows **realistic data patterns**

### Usage in Manual
```spin2
{{ Chapter 3 Example - Graphics Breakthrough }}
#include "debug_stubs.spin2"  ' Makes example complete

PUB draw_heat_map() | x, y, value, color
  repeat y from 0 to 49
    repeat x from 0 to 49
      value := read_sensor()  ' Now defined in stubs
      color := heat_color(value)
      DEBUG(`PLOT PIXEL `(x, y) COLOR 'color')
```

---

## Strategy 2: Object-Based Mock System

### Concept  
Create mock objects that can be configured for different behaviors.

### Implementation
```spin2
' debug_mocks.spin2
OBJ
  sensor : "mock_sensor"
  display : "mock_display"
  events : "mock_events"
  
PUB setup_mocks(mode)
  sensor.configure(mode)  ' RANDOM, SINE, RAMP, REAL
  display.configure(mode) ' SIMPLE, DETAILED, NONE
  events.configure(mode)  ' SIMULATED, KEYBOARD, NONE
```

### In Examples
```spin2
OBJ
  mock : "debug_mocks"
  
PUB main()
  mock.setup_mocks(mock#DEMO_MODE)
  
  value := mock.sensor.read()  ' Instead of read_sensor()
  mock.display.grid(0, 0, 100, 100)
```

### Advantages
- **Configurable behavior** per example
- **Cleaner namespace** (mock.sensor.read vs read_sensor)
- **Educational value** - shows object usage

### Disadvantages
- More complex for beginners
- Requires understanding objects

---

## Strategy 3: Progressive Disclosure

### Concept
Start with simplified inline code, progressively add complexity.

### Level 1: Inline Constants (Chapters 1-3)
```spin2
PUB basic_example()
  value := 42  ' Simulated sensor reading
  DEBUG(`PLOT POINT 'value')
```

### Level 2: Simple Methods (Chapters 4-6)
```spin2
PUB intermediate_example()
  value := get_demo_value()
  DEBUG(`PLOT POINT 'value')
  
PRI get_demo_value() : result
  return cnt & $FF  ' Simple random-ish value
```

### Level 3: Full Stubs (Chapters 7+)
```spin2
#include "debug_stubs.spin2"

PUB advanced_example()
  value := read_sensor()  ' Full stub library
  process_value(value)
```

### Advantages
- **Gradual complexity** matches learning curve
- Early examples stay **ultra-simple**
- Advanced examples get **full functionality**

---

## Strategy 4: Conditional Compilation

### Concept
Use compiler directives to include/exclude helper code.

```spin2
#ifdef INCLUDE_HELPERS
  #include "debug_helpers_full.spin2"  ' 500+ lines
#else
  #include "debug_helpers_stub.spin2"  ' 50 lines
#endif

PUB example()
  #ifdef INCLUDE_HELPERS
    value := read_sensor()  ' Real implementation
  #else  
    value := 123  ' Hard-coded for simplicity
  #endif
  DEBUG(`PLOT POINT 'value')
```

### Advantages
- **Same source** works both ways
- Readers choose **simple or complete**
- Good for **print vs digital** versions

---

## Strategy 5: Sidebar Implementation Blocks

### Concept
Put helper implementations in formatted sidebars that can be collapsed/ignored.

### In Manual Markdown
```markdown
### Main Example
```spin2
PUB thermal_imager() | x, y, temp
  repeat y from 0 to 31
    repeat x from 0 to 31
      temp := read_thermal_pixel(x, y)
      draw_heat_pixel(x, y, temp)
```

::: helper-implementations
**Helper Methods for This Example:**
```spin2
PRI read_thermal_pixel(x, y) : temp
  ' Simulates thermal camera data
  temp = 20 + sin(x * 10, 5) + cos(y * 10, 5)
  
PRI draw_heat_pixel(x, y, temp)
  color := temp_to_color(temp)
  DEBUG(`PLOT PIXEL `(x*4, y*4) SIZE 4 COLOR 'color')
  
PRI temp_to_color(temp) : color
  ' Maps temperature to color (blue=cold, red=hot)
  if temp < 15
    color := $0000FF  ' Blue
  elseif temp < 25
    color := $00FF00  ' Green
  else
    color := $FF0000  ' Red
```
:::
```

### Advantages
- **Complete code** available but **visually separated**
- Readers can **focus on main concept**
- PDF can **style differently** (gray background, smaller font)

---

## Strategy 6: Example Composition Pattern

### Concept
Build examples from composable pieces.

```spin2
' Each example extends a base template
OBJ
  base : "debug_example_base"
  
PUB main()
  base.setup()  ' Handles all common initialization
  run_example()
  base.cleanup()
  
PUB run_example()
  ' Only the unique part of this example
  repeat
    value := base.get_value()
    DEBUG(`PLOT POINT 'value')
```

---

## RECOMMENDED APPROACH: Hybrid Solution

### Best Practice Combination:

1. **Create `debug_stubs.spin2`** (~200 lines)
   - Minimal but functional implementations
   - Returns realistic simulated data
   - Compiles without errors

2. **Use Progressive Disclosure**
   - Chapters 1-3: Inline values
   - Chapters 4-6: Simple helpers defined in-example  
   - Chapters 7+: Include stub library

3. **Provide Complete Examples Repository**
   ```
   examples/
   ├── debug_stubs.spin2        # Shared stubs
   ├── chapter01/
   │   ├── example_1_1.spin2    # Complete, runnable
   │   └── example_1_2.spin2    
   ├── chapter02/
   └── advanced/
       ├── real_hardware/        # Non-stub versions
       └── production/           # Full implementations
   ```

4. **Mark Stub Usage Clearly**
   ```spin2
   '' Example 3.2: Heat Map Visualization
   '' Uses: debug_stubs.spin2 for sensor simulation
   '' Real hardware: Replace read_sensor() with your ADC code
   ```

### Implementation Priority:

1. **Week 1**: Create minimal `debug_stubs.spin2` with all 160 methods (1-2 lines each)
2. **Week 2**: Enhance 20% most-used stubs with realistic behavior  
3. **Week 3**: Create 5 complete showcase examples
4. **Week 4**: Document stub→real migration path

### File Size Analysis:
```
Current: 84 methods defined across examples
Add:     160 stub methods @ ~3 lines each = 480 lines
Total:   One 500-line stub file + existing examples
Result:  Examples stay clean, everything compiles
```

This approach keeps examples **readable and focused** while ensuring they're **complete and runnable**.
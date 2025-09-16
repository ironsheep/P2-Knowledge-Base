# Chapter 3: Graphics Breakthrough - From Text to Visuals

*When numbers fail to reveal patterns, when text drowns you in detail, when you need to SEE what's happening - welcome to visual debugging.*

## When Text Isn't Enough

You're debugging a servo control system. The numbers look right. The servo jitters. You add more DEBUG statements. More numbers. Still jitters. The problem hides in the numerical noise.

Then you do this:

```spin2
PUB visualize_servo_behavior() | position, target
  DEBUG(`BITMAP ServoPlot SIZE 400 200 RGB16)
  DEBUG(`ServoPlot CLEAR 0)  ' Black background
  
  repeat
    target := get_target_position()
    position := read_actual_position()
    
    ' Plot target in green, actual in red
    DEBUG(`ServoPlot PIXEL `(cnt/1000 & 399) `(100 - target/10) `($07E0))   ' Green
    DEBUG(`ServoPlot PIXEL `(cnt/1000 & 399) `(100 - position/10) `($F800)) ' Red
    
    ' The jitter becomes visible as red oscillations around green line
    ' Pattern reveals resonance at specific frequency - invisible in numbers
```

Suddenly you SEE the resonance pattern. The phase relationship. The exact frequency. Visual debugging just solved in seconds what numbers couldn't reveal in hours.

## Your First Graphics with BITMAP

Let's build your visual debugging foundation. Start simple, end powerful.

### Creating Your Canvas

```spin2
PUB graphics_debug_basics()
  ' Create a graphics window - your visual debugging canvas
  DEBUG(`BITMAP Visual SIZE 320 240 RGB16)
  
  ' Clear to dark blue background
  DEBUG(`Visual CLEAR `($001F))
  
  ' Draw coordinate axes
  DEBUG(`Visual LINE 10 120 310 120 `($FFFF))  ' X axis in white
  DEBUG(`Visual LINE 160 10 160 230 `($FFFF))  ' Y axis in white
  
  ' Now you have a coordinate system for plotting data
```

### From Numbers to Shapes

Watch how the same data transforms when visualized:

```spin2
PUB compare_text_vs_visual() | values[10], i, max_val
  ' Generate test data
  repeat i from 0 to 9
    values[i] := ?GETRND() // 100
  
  ' Text output - functional but hard to interpret
  DEBUG(`TERM TextOut POS 0 0 SIZE 40 10)
  DEBUG(`TextOut "Data values:\n")
  repeat i from 0 to 9
    DEBUG(`TextOut "Value " udec_(i) ": " udec_(values[i]) "\n")
  
  ' Visual output - patterns jump out immediately
  DEBUG(`BITMAP BarGraph POS 0 200 SIZE 200 150 RGB16)
  DEBUG(`BarGraph CLEAR 0)
  
  ' Find max for scaling
  max_val := 0
  repeat i from 0 to 9
    if values[i] > max_val
      max_val := values[i]
  
  ' Draw bars
  repeat i from 0 to 9
    draw_bar(i * 20 + 10, values[i], max_val)

PRI draw_bar(x, value, max) | height, color
  height := (value * 100) / max
  
  ' Color code by value
  if value > 75
    color := $F800  ' Red for high values
  elseif value > 50
    color := $FFE0  ' Yellow for medium
  else
    color := $07E0  ' Green for low
    
  DEBUG(`BarGraph FILLBOX `(x) `(140-height) `(x+15) `(140) `(color))
  DEBUG(`BarGraph TEXT `(x) `(145) udec_(value) `($FFFF))
```

The bars reveal distribution. Colors highlight ranges. Comparisons become instant. This is the power of visual debugging.

## Display Emulation Patterns

Here's a game-changer: emulate hardware displays before building them. Debug your GUI without the GUI hardware.

### Seven-Segment Display Emulation

```spin2
CON
  SEG_WIDTH = 4
  SEG_LENGTH = 20
  
PUB emulate_seven_segment() | digit
  DEBUG(`BITMAP SevenSeg SIZE 300 100 RGB16)
  DEBUG(`SevenSeg CLEAR `($000000))
  
  repeat
    repeat digit from 0 to 9
      draw_digit(50, 20, digit, $FF00)   ' Draw in orange
      waitms(500)
      draw_digit(50, 20, digit, $0000)   ' Erase
      
PRI draw_digit(x, y, digit, color) | segments
  ' Get segment pattern for digit
  segments := lookupz(digit: $3F, $06, $5B, $4F, $66, $6D, $7D, $07, $7F, $6F)
  
  ' Draw each segment if lit
  if segments & $01  ' Segment A (top)
    draw_horizontal_segment(x + SEG_WIDTH, y, color)
  if segments & $02  ' Segment B (top right)
    draw_vertical_segment(x + SEG_WIDTH + SEG_LENGTH, y + SEG_WIDTH, color)
  if segments & $04  ' Segment C (bottom right)
    draw_vertical_segment(x + SEG_WIDTH + SEG_LENGTH, y + SEG_WIDTH + SEG_LENGTH + SEG_WIDTH, color)
  if segments & $08  ' Segment D (bottom)
    draw_horizontal_segment(x + SEG_WIDTH, y + 2*SEG_WIDTH + 2*SEG_LENGTH, color)
  if segments & $10  ' Segment E (bottom left)
    draw_vertical_segment(x, y + SEG_WIDTH + SEG_LENGTH + SEG_WIDTH, color)
  if segments & $20  ' Segment F (top left)
    draw_vertical_segment(x, y + SEG_WIDTH, color)
  if segments & $40  ' Segment G (middle)
    draw_horizontal_segment(x + SEG_WIDTH, y + SEG_WIDTH + SEG_LENGTH, color)

PRI draw_horizontal_segment(x, y, color)
  DEBUG(`SevenSeg FILLBOX `(x) `(y) `(x + SEG_LENGTH) `(y + SEG_WIDTH) `(color))
  
PRI draw_vertical_segment(x, y, color)
  DEBUG(`SevenSeg FILLBOX `(x) `(y) `(x + SEG_WIDTH) `(y + SEG_LENGTH) `(color))
```

You just debugged your seven-segment driver without wiring a single LED. See the patterns. Verify the logic. Perfect the display.

### LCD Character Display Emulation

```spin2
PUB emulate_lcd_display() | line1[20], line2[20]
  DEBUG(`BITMAP LCD SIZE 320 80 RGB16)
  DEBUG(`LCD CLEAR `($0010))  ' Dark green background like real LCD
  
  ' Draw LCD frame
  DEBUG(`LCD BOX 5 5 315 75 `($8410))  ' Gray border
  
  ' Initialize display lines
  bytefill(@line1, " ", 20)
  bytefill(@line2, " ", 20)
  
  ' Simulate LCD operations
  lcd_print(1, "Hello P2!")
  waitms(1000)
  lcd_print(2, "Debug LCD Ready")
  waitms(1000)
  lcd_clear()
  lcd_print(1, "Temperature:")
  lcd_print(2, "72.5 F")
  
PRI lcd_print(line, string) | x, y, char, i
  y := line == 1 ? 20 : 45
  x := 20
  
  repeat i from 0 to strsize(string)-1
    char := byte[string][i]
    ' Draw character (simplified - would use font table in practice)
    DEBUG(`LCD TEXT `(x) `(y) `(char) `($7FE0))  ' Bright green text
    x += 15  ' Character spacing

PRI lcd_clear()
  DEBUG(`LCD FILLBOX 10 15 310 65 `($0010))  ' Clear display area only
```

Perfect your LCD interface before ordering the hardware. Test menu systems. Verify formatting. All visually.

## GUI Development Without Hardware

Build and debug complete graphical interfaces using just the BITMAP window. No display hardware needed.

### Button Interface Emulation

```spin2
PUB virtual_button_panel() | mouse_x, mouse_y, buttons, state[4]
  DEBUG(`BITMAP ButtonPanel SIZE 400 300 RGB16)
  DEBUG(`ButtonPanel CLEAR `($4208))  ' Dark gray background
  
  ' Initialize button states
  repeat i from 0 to 3
    state[i] := FALSE
    
  ' Draw button panel
  draw_button(50, 50, 100, 40, "START", 0, state[0])
  draw_button(180, 50, 100, 40, "STOP", 1, state[1])
  draw_button(50, 120, 100, 40, "RESET", 2, state[2])
  draw_button(180, 120, 100, 40, "MODE", 3, state[3])
  
  repeat
    mouse_x, mouse_y, buttons := DEBUG(PC_MOUSE)
    
    if buttons & 1  ' Left click
      handle_button_click(mouse_x, mouse_y, @state)

PRI draw_button(x, y, w, h, label, id, pressed) | color
  ' 3D button effect
  if pressed
    color := $2104  ' Darker when pressed
    DEBUG(`ButtonPanel FILLBOX `(x+2) `(y+2) `(x+w) `(y+h) `(color))
  else
    color := $6B4D  ' Normal button color
    DEBUG(`ButtonPanel FILLBOX `(x) `(y) `(x+w-2) `(y+h-2) `(color))
    ' Highlight for 3D effect
    DEBUG(`ButtonPanel LINE `(x) `(y) `(x+w-2) `(y) `($9CF3))
    DEBUG(`ButtonPanel LINE `(x) `(y) `(x) `(y+h-2) `($9CF3))
    ' Shadow for 3D effect
    DEBUG(`ButtonPanel LINE `(x+w-2) `(y+2) `(x+w-2) `(y+h-2) `($2104))
    DEBUG(`ButtonPanel LINE `(x+2) `(y+h-2) `(x+w-2) `(y+h-2) `($2104))
  
  ' Center text on button
  text_x := x + (w - strsize(label)*8) / 2
  text_y := y + (h - 8) / 2
  DEBUG(`ButtonPanel TEXT `(text_x) `(text_y) 'label' `($FFFF))

PRI handle_button_click(mx, my, state_ptr) | button_id
  ' Detect which button was clicked
  if my >= 50 and my <= 90
    if mx >= 50 and mx <= 150
      button_id := 0  ' START
    elseif mx >= 180 and mx <= 280
      button_id := 1  ' STOP
  elseif my >= 120 and my <= 160
    if mx >= 50 and mx <= 150
      button_id := 2  ' RESET
    elseif mx >= 180 and mx <= 280
      button_id := 3  ' MODE
  else
    return
    
  ' Toggle button state
  long[state_ptr][button_id] := !long[state_ptr][button_id]
  
  ' Redraw button with new state
  case button_id
    0: draw_button(50, 50, 100, 40, "START", 0, long[state_ptr][0])
       if long[state_ptr][0]
         start_system()
    1: draw_button(180, 50, 100, 40, "STOP", 1, long[state_ptr][1])
       if long[state_ptr][1]
         stop_system()
    2: draw_button(50, 120, 100, 40, "RESET", 2, long[state_ptr][2])
       if long[state_ptr][2]
         reset_system()
    3: draw_button(180, 120, 100, 40, "MODE", 3, long[state_ptr][3])
       toggle_mode()
```

You've created a working button interface. Click detection. Visual feedback. State management. No touchscreen required.

### Gauge and Meter Displays

```spin2
PUB analog_gauge_display() | value, old_value
  DEBUG(`BITMAP Gauge SIZE 300 300 RGB16)
  DEBUG(`Gauge CLEAR `($0000))
  
  ' Draw gauge background
  draw_gauge_face(150, 150, 100)
  
  old_value := 0
  repeat
    value := read_analog_input()
    
    if value <> old_value
      ' Erase old needle
      draw_needle(150, 150, 80, old_value, $0000)
      ' Draw new needle
      draw_needle(150, 150, 80, value, $F800)
      old_value := value
      
    waitms(50)

PRI draw_gauge_face(cx, cy, radius)
  ' Outer circle
  DEBUG(`Gauge CIRCLE `(cx) `(cy) `(radius) `($FFFF))
  DEBUG(`Gauge CIRCLE `(cx) `(cy) `(radius-2) `($8410))
  
  ' Scale markings
  repeat angle from 0 to 270 step 27
    x1 := cx + (radius-10) * cos(angle)
    y1 := cy + (radius-10) * sin(angle)
    x2 := cx + (radius-5) * cos(angle)
    y2 := cy + (radius-5) * sin(angle)
    DEBUG(`Gauge LINE `(x1) `(y1) `(x2) `(y2) `($FFFF))
    
  ' Scale numbers
  DEBUG(`Gauge TEXT `(cx-radius+10) `(cy+10) "0" `($FFFF))
  DEBUG(`Gauge TEXT `(cx-5) `(cy-radius+10) "50" `($FFFF))
  DEBUG(`Gauge TEXT `(cx+radius-20) `(cy+10) "100" `($FFFF))

PRI draw_needle(cx, cy, length, value, color) | angle
  ' Convert value (0-100) to angle (0-270 degrees)
  angle := 135 + (value * 270 / 100)
  
  ' Calculate needle endpoint
  x := cx + length * cos(angle)
  y := cy + length * sin(angle)
  
  ' Draw needle
  DEBUG(`Gauge LINE `(cx) `(cy) `(x) `(y) `(color))
  DEBUG(`Gauge FILLCIRCLE `(cx) `(cy) `(5) `(color))  ' Center cap
```

Professional-looking gauges for your debug display. Watch values sweep smoothly. Spot trends instantly.

## Screenshot Integration Workflows

Document your debug sessions. Capture anomalies. Build visual test reports.

### Automatic Screenshot on Event

```spin2
PUB capture_debug_events() | trigger_count
  DEBUG(`BITMAP Monitor SIZE 400 300 RGB16)
  trigger_count := 0
  
  repeat
    monitor_system()
    
    if error_detected()
      trigger_count++
      capture_screenshot(trigger_count)
      log_error_context(trigger_count)

PRI capture_screenshot(index)
  ' P2 can signal host to capture window
  DEBUG(`Monitor CAPTURE "error_" udec_(index) ".bmp")
  
  ' Visual indicator that screenshot was taken
  flash_border($FF00)  ' Red flash

PRI flash_border(color)
  ' Draw border flash
  DEBUG(`Monitor BOX 0 0 399 299 `(color))
  waitms(100)
  DEBUG(`Monitor BOX 0 0 399 299 `($0000))

PRI log_error_context(index) | timestamp
  timestamp := cnt / clkfreq
  
  ' Create corresponding log entry
  DEBUG(`TERM Log "Screenshot " udec_(index) " at " udec_(timestamp) " seconds\n")
  DEBUG(`Log "System state: " uhex_(get_system_state()) "\n")
  DEBUG(`Log "Error code: " uhex_(get_error_code()) "\n")
  DEBUG(`Log "---\n")
```

### Visual Test Documentation

```spin2
PUB document_test_sequence() | step
  DEBUG(`BITMAP TestDoc SIZE 500 400 RGB16)
  DEBUG(`TERM TestLog POS 520 0 SIZE 40 30)
  
  repeat step from 1 to 5
    DEBUG(`TestDoc CLEAR `($0000))
    DEBUG(`TestDoc TEXT 10 10 "Test Step " udec_(step) `($FFFF))
    
    case step
      1: test_initialization()
         document_step("Initialization", "System powered up")
      2: test_communication()
         document_step("Communication", "Serial link verified")  
      3: test_sensors()
         document_step("Sensors", "All sensors responding")
      4: test_actuators()
         document_step("Actuators", "Motor control verified")
      5: test_integration()
         document_step("Integration", "Full system operational")
         
    DEBUG(`TestDoc CAPTURE "test_step_" udec_(step) ".bmp")
    waitms(2000)

PRI document_step(title, result)
  ' Visual documentation
  DEBUG(`TestDoc TEXT 10 30 'title' `($07E0))  ' Green text
  DEBUG(`TestDoc TEXT 10 50 'result' `($FFFF))
  
  ' Log documentation
  DEBUG(`TestLog 'title' ": " 'result' "\n")
  
  ' Draw checkmark for passed test
  draw_checkmark(450, 30, $07E0)

PRI draw_checkmark(x, y, color)
  DEBUG(`TestDoc LINE `(x) `(y+10) `(x+10) `(y+20) `(color))
  DEBUG(`TestDoc LINE `(x+10) `(y+20) `(x+25) `(y) `(color))
```

## Performance Patterns for Graphics

Graphics debugging must be fast. Here's how to keep your visual debugging responsive.

### The Dirty Rectangle Pattern

```spin2
VAR
  long dirty_x1, dirty_y1, dirty_x2, dirty_y2
  long dirty_flag

PUB efficient_graphics_update()
  DEBUG(`BITMAP Display SIZE 400 300 RGB16)
  
  ' Initial full draw
  draw_complete_display()
  dirty_flag := FALSE
  
  repeat
    if data_changed()
      ' Mark dirty region
      mark_dirty(get_changed_region())
      
    if dirty_flag
      ' Only redraw dirty region
      redraw_region(dirty_x1, dirty_y1, dirty_x2, dirty_y2)
      dirty_flag := FALSE

PRI mark_dirty(x1, y1, x2, y2)
  if !dirty_flag
    dirty_x1 := x1
    dirty_y1 := y1
    dirty_x2 := x2
    dirty_y2 := y2
  else
    ' Expand dirty region
    dirty_x1 := dirty_x1 <# x1
    dirty_y1 := dirty_y1 <# y1
    dirty_x2 := dirty_x2 #> x2
    dirty_y2 := dirty_y2 #> y2
  dirty_flag := TRUE
```

### The Double Buffer Pattern

```spin2
VAR
  word buffer1[320*240/2]  ' Two buffers for 320x240 RGB16
  word buffer2[320*240/2]
  long active_buffer

PUB double_buffered_animation()
  active_buffer := 1
  
  repeat
    ' Draw to inactive buffer
    if active_buffer == 1
      render_frame(@buffer2)
      ' Send complete frame at once
      DEBUG(`Display DUMP @buffer2 `(320*240*2))
      active_buffer := 2
    else
      render_frame(@buffer1)
      DEBUG(`Display DUMP @buffer1 `(320*240*2))
      active_buffer := 1
```

### The Incremental Draw Pattern

```spin2
PUB scrolling_waveform() | x, old_y[320], new_y
  DEBUG(`BITMAP Waveform SIZE 320 200 RGB16)
  DEBUG(`Waveform CLEAR `($0000))
  
  x := 0
  repeat
    new_y := 100 + read_waveform_sample() / 10
    
    ' Erase old column
    DEBUG(`Waveform LINE `(x) `(0) `(x) `(199) `($0000))
    
    ' Draw new sample
    if x > 0
      DEBUG(`Waveform LINE `(x-1) `(old_y[x-1]) `(x) `(new_y) `($07E0))
    
    old_y[x] := new_y
    x := (x + 1) // 320
```

## Building Visual Debug Components

Create reusable visual elements for your debugging toolkit.

### The Oscilloscope Component

```spin2
OBJ
  scope : "debug_scope"
  
PUB use_debug_scope()
  scope.init(`BITMAP Scope SIZE 400 200 RGB16, 4)  ' 4 channels
  scope.set_channel_color(0, $F800)  ' Red
  scope.set_channel_color(1, $07E0)  ' Green
  scope.set_channel_color(2, $001F)  ' Blue
  scope.set_channel_color(3, $FFE0)  ' Yellow
  
  repeat
    scope.add_sample(0, read_channel_0())
    scope.add_sample(1, read_channel_1())
    scope.add_sample(2, read_channel_2())
    scope.add_sample(3, read_channel_3())
    scope.update()
    waitms(10)
```

### The Spectrum Analyzer Component

```spin2
OBJ
  spectrum : "debug_spectrum"
  
PUB use_spectrum_analyzer() | fft_data[128]
  spectrum.init(`BITMAP Spectrum SIZE 512 256 RGB16)
  spectrum.set_range(0, 20_000)  ' 0-20kHz
  
  repeat
    perform_fft(@fft_data)
    spectrum.display(@fft_data, 128)
    waitms(50)
```

## Your Turn: Visual Debug Challenge

Debug this misbehaving graphics routine using visual techniques:

```spin2
PUB buggy_animation()
  ' Should draw smooth rotating line
  ' But it flickers and leaves trails
  
  DEBUG(`BITMAP Rotate SIZE 200 200 RGB16)
  angle := 0
  
  repeat
    x := 100 + 80 * cos(angle)
    y := 100 + 80 * sin(angle)
    DEBUG(`Rotate LINE 100 100 `(x) `(y) `($FFFF))
    angle += 5
    waitms(50)
    ' Problems: Doesn't erase old lines, flickers badly
```

**Your Mission:**
1. Fix the trail problem (hint: erase before draw)
2. Eliminate flicker (hint: clear only the line, not entire screen)
3. Add color that changes with angle
4. Add a second line rotating opposite direction
5. Make it respond to keyboard speed control

## Chapter Summary: Seeing is Debugging

You've broken through from text to visuals:

✓ **Pattern recognition** beats number scanning
✓ **Display emulation** enables hardware-free development
✓ **GUI debugging** without physical interfaces
✓ **Screenshot workflows** document your debugging
✓ **Performance patterns** keep graphics responsive

The BITMAP window transformed your debugging from numerical analysis to visual insight. You can now see patterns that numbers would never reveal, emulate displays before building them, and create complete graphical debugging interfaces.

But we've only scratched the surface. Chapter 4 introduces JonnyMac's revolutionary layer system - a discovery that provides 20× performance improvement and transforms PLOT windows into professional debugging instruments.

---

*Next: Chapter 4 - Layer Composition System: Sprite-Based Debugging*
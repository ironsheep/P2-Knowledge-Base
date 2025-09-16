# Chapter 6: Professional Debug Instruments

*Transform your debug windows into broadcast-quality instruments that rival $10,000 test equipment. Using PLOT windows, CORDIC math, and creative visualization.*

## From Debug Display to Professional Instrument

Watch this transformation. A simple value display becomes a professional analog meter:

```spin2
PUB value_display_basic()
  ' What everyone starts with
  repeat
    value := read_sensor()
    DEBUG("Sensor: ", udec(value))
    
PUB value_display_professional()
  ' What you'll build by chapter's end
  repeat
    value := read_sensor()
    update_analog_meter(value)
    update_digital_readout(value)
    update_bar_graph(value)
    update_trend_chart(value)
    update_peak_indicator(value)
    check_alarm_zones(value)
```

The difference? Professional visualization that reveals patterns, trends, and anomalies at a glance. Let's build these instruments.

## Analog Meter Creation with CORDIC

P2's CORDIC engine isn't just for math - it's your precision instrument designer. Sin, cos, atan2 - all in hardware. Perfect circles. Smooth needles. Professional gauges.

### Building Precision Gauges

```spin2
CON
  GAUGE_CX = 200      ' Gauge center X
  GAUGE_CY = 200      ' Gauge center Y
  GAUGE_RADIUS = 150  ' Gauge radius
  GAUGE_START = 225   ' Start angle (degrees)
  GAUGE_SWEEP = 270   ' Sweep angle (degrees)

PUB create_analog_gauge() | angle, i
  DEBUG(`PLOT Gauge SIZE 400 400)
  
  draw_gauge_face()
  draw_gauge_scale()
  draw_gauge_zones()
  
  repeat
    value := read_sensor()
    angle := value_to_angle(value)
    update_gauge_needle(angle)

PRI draw_gauge_face()
  ' Outer bezel
  repeat i from 0 to 359
    x := GAUGE_CX + (GAUGE_RADIUS + 5) * cos(i)
    y := GAUGE_CY + (GAUGE_RADIUS + 5) * sin(i)
    DEBUG(`Gauge SET `(x<<8) `(y<<8))
    x := GAUGE_CX + (GAUGE_RADIUS + 10) * cos(i)
    y := GAUGE_CY + (GAUGE_RADIUS + 10) * sin(i)
    DEBUG(`Gauge LINE `(x<<8) `(y<<8))
  
  ' Inner face
  DEBUG(`Gauge CIRCLE GAUGE_CX GAUGE_CY GAUGE_RADIUS GRAY)
  DEBUG(`Gauge FILLCIRCLE GAUGE_CX GAUGE_CY `(GAUGE_RADIUS-5) BLACK)

PRI draw_gauge_scale() | angle, i, x1, y1, x2, y2
  ' Major tick marks
  repeat i from 0 to 10
    angle := GAUGE_START - (i * GAUGE_SWEEP / 10)
    
    ' Tick marks
    x1 := GAUGE_CX + (GAUGE_RADIUS - 10) * cos(angle)
    y1 := GAUGE_CY - (GAUGE_RADIUS - 10) * sin(angle)
    x2 := GAUGE_CX + (GAUGE_RADIUS - 25) * cos(angle)
    y2 := GAUGE_CY - (GAUGE_RADIUS - 25) * sin(angle)
    
    DEBUG(`Gauge LINESIZE $300)  ' Thick line
    DEBUG(`Gauge LINE `(x1<<8) `(y1<<8) `(x2<<8) `(y2<<8) WHITE)
    
    ' Scale numbers
    x1 := GAUGE_CX + (GAUGE_RADIUS - 40) * cos(angle)
    y1 := GAUGE_CY - (GAUGE_RADIUS - 40) * sin(angle)
    DEBUG(`Gauge TEXT `(x1) `(y1) udec(i*10) WHITE)
  
  ' Minor tick marks
  repeat i from 0 to 50
    if i // 5 <> 0  ' Skip major tick positions
      angle := GAUGE_START - (i * GAUGE_SWEEP / 50)
      x1 := GAUGE_CX + (GAUGE_RADIUS - 10) * cos(angle)
      y1 := GAUGE_CY - (GAUGE_RADIUS - 10) * sin(angle)
      x2 := GAUGE_CX + (GAUGE_RADIUS - 18) * cos(angle)
      y2 := GAUGE_CY - (GAUGE_RADIUS - 18) * sin(angle)
      
      DEBUG(`Gauge LINESIZE $100)  ' Thin line
      DEBUG(`Gauge LINE `(x1<<8) `(y1<<8) `(x2<<8) `(y2<<8) GRAY)

PRI draw_gauge_zones()
  ' Green zone (0-60)
  draw_arc(GAUGE_CX, GAUGE_CY, GAUGE_RADIUS-8, GAUGE_START, GAUGE_START-162, GREEN)
  
  ' Yellow zone (60-80)
  draw_arc(GAUGE_CX, GAUGE_CY, GAUGE_RADIUS-8, GAUGE_START-162, GAUGE_START-216, YELLOW)
  
  ' Red zone (80-100)
  draw_arc(GAUGE_CX, GAUGE_CY, GAUGE_RADIUS-8, GAUGE_START-216, GAUGE_START-270, RED)

PRI draw_arc(cx, cy, radius, start_angle, end_angle, color) | angle
  DEBUG(`Gauge LINESIZE $500)  ' Thick zone indicator
  
  angle := start_angle
  repeat while angle > end_angle
    x := cx + radius * cos(angle)
    y := cy - radius * sin(angle)
    DEBUG(`Gauge PIXEL `(x) `(y) 'color')
    angle--

VAR
  long last_needle_angle

PRI update_gauge_needle(angle) | x1, y1, x2, y2
  ' Erase old needle
  if last_needle_angle
    draw_needle(last_needle_angle, BLACK)
  
  ' Draw new needle
  draw_needle(angle, RED)
  last_needle_angle := angle
  
  ' Draw center cap
  DEBUG(`Gauge FILLCIRCLE GAUGE_CX GAUGE_CY 10 SILVER)
  DEBUG(`Gauge CIRCLE GAUGE_CX GAUGE_CY 10 BLACK)

PRI draw_needle(angle, color)
  ' Needle shaft
  x1 := GAUGE_CX + 20 * cos(angle + 180)
  y1 := GAUGE_CY - 20 * sin(angle + 180)
  x2 := GAUGE_CX + (GAUGE_RADIUS - 30) * cos(angle)
  y2 := GAUGE_CY - (GAUGE_RADIUS - 30) * sin(angle)
  
  DEBUG(`Gauge LINESIZE $400)
  DEBUG(`Gauge LINE `(x1<<8) `(y1<<8) `(x2<<8) `(y2<<8) 'color')
  
  ' Needle tip (triangle)
  x1 := x2
  y1 := y2
  x2 := GAUGE_CX + (GAUGE_RADIUS - 20) * cos(angle)
  y2 := GAUGE_CY - (GAUGE_RADIUS - 20) * sin(angle)
  
  DEBUG(`Gauge LINESIZE $200)
  DEBUG(`Gauge LINE `(x1<<8) `(y1<<8) `(x2<<8) `(y2<<8) 'color')

PRI value_to_angle(value) : angle
  ' Convert 0-100 value to gauge angle
  angle := GAUGE_START - (value * GAUGE_SWEEP / 100)
```

This gauge looks like it came from a Fluke multimeter. Smooth needle movement. Color zones. Professional scaling. All from CORDIC math and careful visualization.

### Multiple Synchronized Gauges

```spin2
PUB multi_gauge_dashboard()
  DEBUG(`PLOT Dashboard SIZE 800 400)
  
  ' Three gauges side by side
  create_gauge(150, 200, 120, "SPEED")    ' Left gauge
  create_gauge(400, 200, 120, "RPM")      ' Center gauge
  create_gauge(650, 200, 120, "TEMP")     ' Right gauge
  
  repeat
    update_gauge(0, get_speed(), 0, 160)      ' 0-160 MPH
    update_gauge(1, get_rpm(), 0, 8000)       ' 0-8000 RPM
    update_gauge(2, get_temperature(), 0, 250) ' 0-250°F

VAR
  long gauge_cx[3], gauge_cy[3], gauge_radius[3]
  long gauge_last_angle[3]

PRI create_gauge(cx, cy, radius, label)
  static gauge_num
  
  gauge_cx[gauge_num] := cx
  gauge_cy[gauge_num] := cy
  gauge_radius[gauge_num] := radius
  
  ' Draw this gauge's face
  draw_gauge_at(cx, cy, radius, label)
  gauge_num++

PRI update_gauge(num, value, min_val, max_val) | angle
  ' Scale value to 0-100 range
  scaled := ((value - min_val) * 100) / (max_val - min_val)
  
  ' Convert to angle
  angle := 225 - (scaled * 270 / 100)
  
  ' Update needle
  erase_needle_at(gauge_cx[num], gauge_cy[num], gauge_radius[num], gauge_last_angle[num])
  draw_needle_at(gauge_cx[num], gauge_cy[num], gauge_radius[num], angle)
  gauge_last_angle[num] := angle
  
  ' Update digital display
  show_digital_value(gauge_cx[num], gauge_cy[num] + gauge_radius[num] + 30, value)
```

## LED Panel Displays

LEDs communicate status instantly. Build virtual LED panels that outperform physical ones.

### Multi-State LED Arrays

```spin2
CON
  LED_SIZE = 20
  LED_SPACING = 30
  LED_ROWS = 4
  LED_COLS = 8

PUB led_panel_display()
  DEBUG(`PLOT LEDPanel SIZE 300 150)
  
  ' Initialize LED states
  clear_all_leds()
  
  repeat
    update_led_states()
    draw_led_panel()
    waitms(100)

PRI draw_led_panel() | row, col, state, color
  repeat row from 0 to LED_ROWS-1
    repeat col from 0 to LED_COLS-1
      state := get_led_state(row, col)
      color := get_led_color(row, col)
      
      x := 20 + col * LED_SPACING
      y := 20 + row * LED_SPACING
      
      draw_led(x, y, state, color)

PRI draw_led(x, y, state, color)
  if state
    ' LED on - bright center with glow
    DEBUG(`LEDPanel FILLCIRCLE 'x' 'y' `(LED_SIZE/2) 'color')
    DEBUG(`LEDPanel CIRCLE 'x' 'y' `(LED_SIZE/2 + 2) 'dim_color(color)')
    DEBUG(`LEDPanel CIRCLE 'x' 'y' `(LED_SIZE/2 + 4) 'dimmer_color(color)')
  else
    ' LED off - dark
    DEBUG(`LEDPanel FILLCIRCLE 'x' 'y' `(LED_SIZE/2) DARKGRAY)
    DEBUG(`LEDPanel CIRCLE 'x' 'y' `(LED_SIZE/2) GRAY)

PRI dim_color(color) : dimmed
  ' Reduce brightness by 50%
  r := (color >> 11) & $1F
  g := (color >> 5) & $3F
  b := color & $1F
  
  dimmed := ((r/2) << 11) | ((g/2) << 5) | (b/2)

PUB create_vu_meter() | level, i
  DEBUG(`PLOT VUMeter SIZE 400 100)
  
  repeat
    level := get_audio_level()
    
    ' Draw VU meter LEDs
    repeat i from 0 to 19
      x := 20 + i * 18
      y := 50
      
      if i < level * 20 / 100
        ' LED on
        if i < 14
          color := GREEN
        elseif i < 17
          color := YELLOW
        else
          color := RED
          
        draw_rectangular_led(x, y, 15, 30, color, TRUE)
      else
        ' LED off
        draw_rectangular_led(x, y, 15, 30, DARKGRAY, FALSE)

PRI draw_rectangular_led(x, y, w, h, color, lit)
  if lit
    ' Lit LED with gradient effect
    DEBUG(`VUMeter FILLBOX 'x' 'y' `(x+w)' `(y+h)' 'color')
    ' Highlight at top
    DEBUG(`VUMeter LINE 'x' 'y' `(x+w)' 'y' 'bright_color(color)')
    ' Shadow at bottom
    DEBUG(`VUMeter LINE 'x' `(y+h)' `(x+w)' `(y+h)' 'dark_color(color)')
  else
    ' Unlit LED
    DEBUG(`VUMeter FILLBOX 'x' 'y' `(x+w)' `(y+h)' 'color')
    DEBUG(`VUMeter BOX 'x' 'y' `(x+w)' `(y+h)' GRAY)
```

### Seven-Segment and Matrix Displays

```spin2
PUB seven_segment_array() | digit, position
  DEBUG(`PLOT SevenSeg SIZE 500 120)
  
  ' Display 6-digit value
  repeat
    value := get_counter_value()
    
    ' Display each digit
    repeat position from 0 to 5
      digit := (value / pow(10, 5-position)) // 10
      draw_seven_segment(20 + position * 80, 20, digit, RED)

PRI draw_seven_segment(x, y, digit, color)
  ' Segment patterns for 0-9
  segments := lookup(digit: $3F, $06, $5B, $4F, $66, $6D, $7D, $07, $7F, $6F)
  
  ' Draw each segment if lit
  if segments & $01
    draw_h_segment(x + 5, y, color)         ' Top
  if segments & $02
    draw_v_segment(x + 30, y + 5, color)    ' Top right
  if segments & $04
    draw_v_segment(x + 30, y + 35, color)   ' Bottom right
  if segments & $08
    draw_h_segment(x + 5, y + 60, color)    ' Bottom
  if segments & $10
    draw_v_segment(x, y + 35, color)        ' Bottom left
  if segments & $20
    draw_v_segment(x, y + 5, color)         ' Top left
  if segments & $40
    draw_h_segment(x + 5, y + 30, color)    ' Middle

PRI draw_h_segment(x, y, color)
  DEBUG(`SevenSeg FILLBOX 'x' 'y' `(x+20)' `(y+5)' 'color')

PRI draw_v_segment(x, y, color)
  DEBUG(`SevenSeg FILLBOX 'x' 'y' `(x+5)' `(y+25)' 'color')

PUB dot_matrix_display() | row, col, pattern
  DEBUG(`PLOT DotMatrix SIZE 320 320)
  
  ' 32x32 dot matrix
  repeat
    message := get_scroll_message()
    
    repeat offset from 0 to strsize(message) * 8
      ' Clear display
      DEBUG(`DotMatrix CLEAR BLACK)
      
      ' Draw each character
      repeat char_num from 0 to 3
        if offset/8 + char_num < strsize(message)
          char := byte[message][offset/8 + char_num]
          draw_char_matrix(char_num * 8 - (offset & 7), 0, char)
      
      waitms(50)

PRI draw_char_matrix(x, y, char) | row, col, pattern
  ' Get character pattern from font table
  repeat row from 0 to 7
    pattern := font_8x8[char * 8 + row]
    
    repeat col from 0 to 7
      if pattern & (1 << (7-col))
        if x + col >= 0 and x + col < 32
          draw_dot(x + col, y + row, GREEN)

PRI draw_dot(x, y, color)
  x_pos := 10 + x * 10
  y_pos := 10 + y * 10
  DEBUG(`DotMatrix FILLCIRCLE 'x_pos' 'y_pos' 4 'color')
```

## Multi-State Visualization Systems

States need instant recognition. Build visualization systems that communicate complex states at a glance.

### Interactive Binary Switches

```spin2
PUB binary_switch_panel() | i, state
  DEBUG(`PLOT Switches SIZE 600 400)
  
  ' Create 16 switches in 2 rows
  repeat i from 0 to 15
    x := 50 + (i & 7) * 70
    y := 100 + (i / 8) * 150
    
    draw_switch(x, y, i, FALSE)
  
  repeat
    mx, my, buttons := DEBUG(PC_MOUSE)
    
    if buttons & 1
      switch := detect_switch(mx, my)
      if switch >= 0
        toggle_switch(switch)

VAR
  word switch_states

PRI draw_switch(x, y, id, state)
  ' Draw switch body
  DEBUG(`Switches FILLBOX 'x' 'y' `(x+50)' `(y+80)' DARKGRAY)
  DEBUG(`Switches BOX 'x' 'y' `(x+50)' `(y+80)' BLACK)
  
  ' Draw switch lever
  if state
    ' ON position
    lever_y := y + 20
    color := GREEN
  else
    ' OFF position
    lever_y := y + 60
    color := RED
    
  DEBUG(`Switches FILLBOX `(x+15)' 'lever_y' `(x+35)' `(lever_y+20)' 'color')
  DEBUG(`Switches BOX `(x+15)' 'lever_y' `(x+35)' `(lever_y+20)' BLACK)
  
  ' Label
  DEBUG(`Switches TEXT `(x+20)' `(y+90)' udec(id) WHITE)

PRI toggle_switch(id)
  switch_states ^= (1 << id)
  state := (switch_states >> id) & 1
  
  x := 50 + (id & 7) * 70
  y := 100 + (id / 8) * 150
  
  draw_switch(x, y, id, state)
  
  ' Apply switch action
  apply_switch_setting(id, state)
```

### Status Indicator Matrices

```spin2
PUB status_matrix_display()
  DEBUG(`PLOT StatusMatrix SIZE 800 600)
  
  draw_status_grid()
  
  repeat
    update_all_status_indicators()
    waitms(250)

PRI draw_status_grid() | row, col
  ' Draw grid for 8x6 status matrix
  repeat row from 0 to 5
    repeat col from 0 to 7
      x := 50 + col * 90
      y := 50 + row * 90
      
      ' Draw cell
      DEBUG(`StatusMatrix BOX 'x' 'y' `(x+80)' `(y+80)' GRAY)
      
      ' Label
      label := get_status_label(row * 8 + col)
      DEBUG(`StatusMatrix TEXT `(x+5)' `(y+5)' 'label' WHITE)

PRI update_all_status_indicators() | i, status, severity
  repeat i from 0 to 47
    status := get_system_status(i)
    severity := get_status_severity(i)
    
    row := i / 8
    col := i & 7
    x := 50 + col * 90
    y := 50 + row * 90
    
    draw_status_indicator(x + 40, y + 40, status, severity)

PRI draw_status_indicator(x, y, status, severity)
  ' Choose color based on severity
  case severity
    CRITICAL: color := RED
    WARNING:  color := YELLOW
    NORMAL:   color := GREEN
    IDLE:     color := GRAY
  
  ' Choose shape based on status type
  case status & $F0
    STATUS_RUNNING:
      ' Animated spinner
      draw_spinner(x, y, color)
      
    STATUS_ERROR:
      ' Flashing X
      if cnt & $1000000
        draw_x_mark(x, y, color)
        
    STATUS_OK:
      ' Check mark
      draw_check_mark(x, y, color)
      
    STATUS_WAITING:
      ' Pulsing circle
      radius := 10 + (cnt / 1000000) & 7
      DEBUG(`StatusMatrix CIRCLE 'x' 'y' 'radius' 'color')

PRI draw_spinner(x, y, color) | angle
  angle := (cnt / 1000000) & $1FF
  
  repeat i from 0 to 7
    a := angle + i * 45
    x1 := x + 5 * cos(a)
    y1 := y + 5 * sin(a)
    x2 := x + 15 * cos(a)
    y2 := y + 15 * sin(a)
    
    intensity := 255 - (i * 30)
    c := fade_color(color, intensity)
    DEBUG(`StatusMatrix LINE 'x1' 'y1' 'x2' 'y2' 'c')
```

## Hardware Interface Emulation

Debug hardware interfaces before building them. See exactly how your interface will look and behave.

### Control Knob Simulation

```spin2
PUB rotary_encoder_knob() | angle, last_angle, value
  DEBUG(`PLOT Encoder SIZE 300 300)
  
  draw_encoder_body(150, 150, 80)
  angle := 0
  value := 0
  
  repeat
    mx, my, buttons := DEBUG(PC_MOUSE)
    
    if buttons & 1 and distance(mx, my, 150, 150) < 80
      ' Calculate angle from mouse position
      new_angle := atan2(my - 150, mx - 150)
      
      ' Calculate rotation
      delta := angle_difference(new_angle, last_angle)
      value += delta / 10
      
      ' Update display
      draw_encoder_position(150, 150, 80, new_angle)
      show_encoder_value(value)
      
      last_angle := new_angle

PRI draw_encoder_body(cx, cy, radius)
  ' Knob body
  DEBUG(`Encoder FILLCIRCLE 'cx' 'cy' 'radius' DARKGRAY)
  DEBUG(`Encoder CIRCLE 'cx' 'cy' 'radius' BLACK)
  
  ' Grip ridges
  repeat i from 0 to 35
    angle := i * 10
    x1 := cx + (radius - 5) * cos(angle)
    y1 := cy + (radius - 5) * sin(angle)
    x2 := cx + radius * cos(angle)
    y2 := cy + radius * sin(angle)
    DEBUG(`Encoder LINE 'x1' 'y1' 'x2' 'y2' BLACK)

PRI draw_encoder_position(cx, cy, radius, angle)
  ' Clear old position indicator
  DEBUG(`Encoder FILLCIRCLE 'cx' 'cy' `(radius-10)' DARKGRAY)
  
  ' Draw position indicator
  x := cx + (radius - 20) * cos(angle)
  y := cy + (radius - 20) * sin(angle)
  DEBUG(`Encoder FILLCIRCLE 'x' 'y' 5 WHITE)
  
  ' Draw center cap
  DEBUG(`Encoder FILLCIRCLE 'cx' 'cy' 10 SILVER)
```

### Slider Bank Simulation

```spin2
PUB slider_bank_interface() | i, active_slider
  DEBUG(`PLOT Sliders SIZE 800 400)
  
  ' Create 10 vertical sliders
  repeat i from 0 to 9
    create_slider(50 + i * 75, 50, i)
  
  active_slider := -1
  
  repeat
    mx, my, buttons := DEBUG(PC_MOUSE)
    
    if buttons & 1
      ' Check which slider is being dragged
      if active_slider < 0
        active_slider := detect_slider(mx, my)
      
      if active_slider >= 0
        ' Update slider position
        new_value := (350 - my) * 100 / 300
        new_value := new_value #> 0 <# 100
        
        update_slider(active_slider, new_value)
        apply_slider_value(active_slider, new_value)
    else
      active_slider := -1

VAR
  long slider_values[10]

PRI create_slider(x, y, id)
  ' Draw slider track
  DEBUG(`Sliders LINE 'x' 'y' 'x' `(y+300)' GRAY)
  
  ' Draw tick marks
  repeat i from 0 to 10
    ty := y + i * 30
    DEBUG(`Sliders LINE `(x-5)' 'ty' `(x+5)' 'ty' WHITE)
  
  ' Draw initial thumb
  slider_values[id] := 50
  update_slider(id, 50)
  
  ' Label
  DEBUG(`Sliders TEXT `(x-10)' `(y+320)' "Ch" udec(id) WHITE)

PRI update_slider(id, value) | x, y
  slider_values[id] := value
  
  x := 50 + id * 75
  y := 350 - (value * 300 / 100)
  
  ' Clear old thumb
  DEBUG(`Sliders FILLBOX `(x-20)' 50 `(x+20)' 350 BLACK)
  
  ' Redraw track
  DEBUG(`Sliders LINE 'x' 50 'x' 350 GRAY)
  
  ' Draw new thumb
  DEBUG(`Sliders FILLBOX `(x-15)' `(y-10)' `(x+15)' `(y+10)' GREEN)
  DEBUG(`Sliders BOX `(x-15)' `(y-10)' `(x+15)' `(y+10)' WHITE)
  
  ' Value display
  DEBUG(`Sliders TEXT `(x-15)' `(y-25)' udec(value) YELLOW)
```

## Your Turn: Instrument Challenge

Build a complete automotive dashboard with these requirements:

```spin2
PUB dashboard_challenge()
  ' Your mission: Create a professional dashboard with:
  ' 1. Speedometer (0-160 MPH) with needle
  ' 2. Tachometer (0-8000 RPM) with redline
  ' 3. Fuel gauge with warning light
  ' 4. Temperature gauge with zones
  ' 5. Warning light panel (8 lights)
  ' 6. Digital trip computer display
  ' 7. Turn signal indicators
  ' 8. High beam indicator
  
  ' Bonus: Make it respond to keyboard simulation:
  ' Arrow keys: Speed up/down
  ' R: Rev engine
  ' L: Left turn signal
  ' R: Right turn signal
  ' H: High beams
  ' W: Trigger warning
```

## Chapter Summary: Broadcast-Quality Instruments

You've built professional debug instruments:

✓ **Analog gauges** with CORDIC precision
✓ **LED panels** with realistic illumination
✓ **Multi-state displays** for complex visualization
✓ **Binary switches** for interactive control
✓ **Hardware emulation** before physical build

Your debug windows now rival professional test equipment. Analog meters that look real. LED displays that communicate instantly. Control interfaces that work like hardware. All created with PLOT windows and creative visualization.

Chapter 7 introduces the performance revolution: packed data formats that accelerate your debugging by 16×.

---

*Next: Chapter 7 - Packed Data Revolution: 16× Compression*
# Chapter 5: PC Input Integration - Bidirectional Debug Control

*Your keyboard and mouse aren't just for writing code anymore. They're real-time debugging controllers that transform P2 debugging from observation to interaction.*

## The Bidirectional Revolution

Traditional debugging is one-way. Your device outputs. You observe. You stop, modify code, recompile, download, run again. Repeat until exhausted.

P2 debugging is bidirectional. Your device outputs. You observe. You press a key. Your P2 responds. You click. Parameters change. Real-time. No recompiling. This changes everything.

```spin2
PUB traditional_debugging()
  ' One-way: P2 talks, you listen
  repeat
    DEBUG("Sensor: ", udec(sensor_value))
    waitms(100)
    ' Want to change threshold? Stop, edit, recompile, download...

PUB bidirectional_debugging() | key, threshold
  ' Two-way: P2 talks, you control
  threshold := 500
  
  repeat
    DEBUG("Sensor: ", udec(sensor_value), " Threshold: ", udec(threshold))
    
    key := DEBUG(PC_KEY)
    case key
      "+": threshold += 10     ' Adjust in real-time!
      "-": threshold -= 10     ' No recompiling!
      
    if sensor_value > threshold
      trigger_alarm()
```

See the difference? You're in control. Live. This is debugging as it should be.

## Mouse Control Patterns

Your mouse becomes a precision debugging instrument. Click to select. Drag to adjust. Scroll to zoom. Let me show you the patterns that matter.

### Click Detection and Region Mapping

```spin2
CON
  ' Define clickable regions
  BUTTON_START_X = 50
  BUTTON_START_Y = 100
  BUTTON_WIDTH = 100
  BUTTON_HEIGHT = 40
  
PUB mouse_region_control() | mx, my, buttons, region
  DEBUG(`PLOT Control SIZE 640 480)
  
  ' Draw interface
  draw_control_panel()
  
  repeat
    mx, my, buttons := DEBUG(PC_MOUSE)
    
    if buttons & 1  ' Left click
      region := detect_region(mx, my)
      handle_region_click(region)
    
    if buttons & 2  ' Right click
      show_context_menu(mx, my)
      
    if buttons & 4  ' Middle click
      reset_to_defaults()

PRI detect_region(x, y) : region | i
  ' Check button regions
  repeat i from 0 to 5
    if in_button(x, y, i)
      return i + 1
      
  ' Check slider regions
  repeat i from 0 to 3
    if in_slider(x, y, i)
      return i + 10
      
  ' Check plot area
  if x > 200 and x < 600 and y > 50 and y < 400
    return 100
    
  return 0  ' No region

PRI in_button(x, y, index) : result
  bx := BUTTON_START_X
  by := BUTTON_START_Y + (index * 50)
  
  result := x >= bx and x < bx + BUTTON_WIDTH and y >= by and y < by + BUTTON_HEIGHT

PRI handle_region_click(region)
  case region
    1..6:   handle_button(region - 1)
    10..13: handle_slider(region - 10)
    100:    handle_plot_click()
```

### Drag Operations for Value Adjustment

```spin2
VAR
  long drag_active
  long drag_start_x, drag_start_y
  long drag_target
  long drag_original_value

PUB drag_control_system() | mx, my, buttons
  DEBUG(`PLOT DragControl SIZE 800 400)
  
  setup_sliders()
  
  repeat
    mx, my, buttons := DEBUG(PC_MOUSE)
    
    if buttons & 1  ' Left button
      if !drag_active
        ' Start drag
        start_drag_operation(mx, my)
      else
        ' Continue drag
        update_drag(mx, my)
    else
      if drag_active
        ' End drag
        end_drag_operation()

PRI start_drag_operation(x, y) | target
  target := identify_drag_target(x, y)
  
  if target > 0
    drag_active := TRUE
    drag_start_x := x
    drag_start_y := y
    drag_target := target
    drag_original_value := get_control_value(target)
    
    ' Visual feedback
    highlight_control(target)

PRI update_drag(x, y) | delta, new_value
  if !drag_active
    return
    
  ' Calculate drag delta
  case get_control_type(drag_target)
    HORIZONTAL_SLIDER:
      delta := x - drag_start_x
      new_value := drag_original_value + (delta * get_control_range(drag_target) / 200)
      
    VERTICAL_SLIDER:
      delta := drag_start_y - y  ' Inverted for natural feel
      new_value := drag_original_value + (delta * get_control_range(drag_target) / 200)
      
    ROTARY_KNOB:
      ' Calculate angle change
      angle1 := atan2(drag_start_y - 200, drag_start_x - 400)
      angle2 := atan2(y - 200, x - 400)
      delta := angle2 - angle1
      new_value := drag_original_value + (delta * get_control_range(drag_target) / 360)
  
  ' Apply constraints
  new_value := new_value #> get_control_min(drag_target) <# get_control_max(drag_target)
  
  ' Update control
  set_control_value(drag_target, new_value)
  redraw_control(drag_target)
  
  ' Apply to system
  apply_control_value(drag_target, new_value)
```

### Mouse Wheel for Precision Control

```spin2
PUB mouse_wheel_control() | mx, my, buttons, wheel, last_wheel
  DEBUG(`PLOT WheelControl SIZE 640 480)
  
  setup_controls()
  last_wheel := 0
  
  repeat
    mx, my, buttons, wheel := DEBUG(PC_MOUSE)
    
    if wheel <> last_wheel
      delta := wheel - last_wheel
      target := get_hover_target(mx, my)
      
      if target > 0
        adjust_with_wheel(target, delta)
      else
        ' No specific target - zoom/scroll the view
        if buttons & 1
          zoom_view(delta)
        else
          scroll_view(delta)
          
      last_wheel := wheel

PRI adjust_with_wheel(target, delta) | value, increment
  value := get_control_value(target)
  
  ' Fine control with Ctrl, coarse with Shift
  if key_pressed(CTRL)
    increment := 1      ' Fine adjustment
  elseif key_pressed(SHIFT)
    increment := 100    ' Coarse adjustment
  else
    increment := 10     ' Normal adjustment
    
  value += delta * increment
  
  ' Apply and update
  set_control_value(target, value)
  update_control_display(target)
```

## Keyboard Integration

Your keyboard becomes a command center. Shortcuts for everything. Modal controls. Direct value entry. Professional debugging interfaces.

### Shortcut Systems and Mode Switching

```spin2
CON
  ' Operating modes
  MODE_MONITOR = 0
  MODE_CONTROL = 1
  MODE_ANALYZE = 2
  MODE_CONFIGURE = 3

VAR
  long current_mode
  long mode_keys[4]

PUB keyboard_command_center() | key
  setup_modes()
  current_mode := MODE_MONITOR
  
  repeat
    display_current_mode()
    
    key := DEBUG(PC_KEY)
    if key
      process_key_command(key)

PRI process_key_command(key)
  ' Global shortcuts (work in any mode)
  case key
    27:     quit                    ' ESC - Exit
    $70:    set_mode(MODE_MONITOR)  ' F1
    $71:    set_mode(MODE_CONTROL)  ' F2
    $72:    set_mode(MODE_ANALYZE)  ' F3
    $73:    set_mode(MODE_CONFIGURE) ' F4
    " ":    pause_resume()          ' Space - Pause/Resume
    "r", "R": reset_system()        ' R - Reset
    "s", "S": save_configuration()  ' S - Save
    "l", "L": load_configuration()  ' L - Load
    
  ' Mode-specific shortcuts
  case current_mode
    MODE_MONITOR:   process_monitor_keys(key)
    MODE_CONTROL:   process_control_keys(key)
    MODE_ANALYZE:   process_analyze_keys(key)
    MODE_CONFIGURE: process_configure_keys(key)

PRI process_control_keys(key)
  case key
    "1".."9": select_channel(key - "0")
    "+", "=": increase_selected_value()
    "-", "_": decrease_selected_value()
    "[":      decrease_range()
    "]":      increase_range()
    "a", "A": toggle_auto_mode()
    "m", "M": toggle_manual_mode()
    "0":      zero_selected_channel()
    
    ' Arrow keys for navigation
    $C0: select_previous()  ' Up
    $C1: select_next()      ' Down
    $C2: decrease_fine()    ' Left
    $C3: increase_fine()    ' Right
```

### Direct Value Entry System

```spin2
VAR
  byte input_buffer[20]
  long input_position
  long input_active
  long input_target

PUB direct_value_entry() | key, value
  DEBUG(`TERM ValueEntry SIZE 60 20)
  
  repeat
    display_values()
    
    key := DEBUG(PC_KEY)
    
    case key
      "v", "V": start_value_entry()
      "t", "T": start_threshold_entry()
      "p", "P": start_parameter_entry()
      other:
        if input_active
          handle_input_key(key)
        else
          handle_normal_key(key)

PRI start_value_entry()
  input_active := TRUE
  input_target := TARGET_VALUE
  input_position := 0
  bytefill(@input_buffer, 0, 20)
  
  ' Show input prompt
  DEBUG(`ValueEntry GOTOXY 10 10 "Enter value: ")
  show_cursor()

PRI handle_input_key(key) | value
  case key
    "0".."9":
      if input_position < 19
        input_buffer[input_position++] := key
        DEBUG(`ValueEntry 'key')
        
    ".":
      if input_position < 19 and !contains_decimal()
        input_buffer[input_position++] := key
        DEBUG(`ValueEntry ".")
        
    8, 127:  ' Backspace/Delete
      if input_position > 0
        input_position--
        input_buffer[input_position] := 0
        DEBUG(`ValueEntry BSP " " BSP)
        
    13:  ' Enter - accept value
      value := parse_number(@input_buffer)
      apply_value(input_target, value)
      end_input_mode()
      
    27:  ' ESC - cancel
      end_input_mode()

PRI parse_number(buffer) : value | i, decimal_pos, decimal_found
  value := 0
  decimal_pos := 0
  decimal_found := FALSE
  
  repeat i from 0 to strsize(buffer) - 1
    if byte[buffer][i] == "."
      decimal_found := TRUE
      decimal_pos := i
    elseif byte[buffer][i] >= "0" and byte[buffer][i] <= "9"
      if decimal_found
        value := value * 10 + (byte[buffer][i] - "0")
      else
        value := value * 10 + (byte[buffer][i] - "0")
  
  ' Handle decimal scaling
  if decimal_found
    repeat i from decimal_pos + 1 to strsize(buffer) - 1
      value := value / 10
      
  return value
```

## Interactive Parameter Adjustment

Real-time tuning transforms debugging. Watch effects immediately. Find optimal values interactively. No more guess-compile-test cycles.

### Building Adjustment Interfaces

```spin2
OBJ
  pid : "pid_controller"
  
VAR
  long kp_scaled, ki_scaled, kd_scaled  ' Scaled by 1000 for precision
  long setpoint, output
  long selected_param

PUB interactive_pid_tuning() | key, actual
  kp_scaled := 1500  ' 1.5
  ki_scaled := 200   ' 0.2
  kd_scaled := 50    ' 0.05
  setpoint := 1000
  selected_param := 0
  
  setup_pid_display()
  
  repeat
    actual := read_process_variable()
    output := pid.calculate(setpoint, actual, kp_scaled, ki_scaled, kd_scaled)
    apply_control_output(output)
    
    update_pid_display(actual, output)
    plot_response(actual, setpoint)
    
    key := DEBUG(PC_KEY)
    if key
      handle_tuning_key(key)

PRI handle_tuning_key(key)
  case key
    TAB: selected_param := (selected_param + 1) // 3
    
    "+", "=":
      case selected_param
        0: kp_scaled := (kp_scaled + 10) <# 10000
        1: ki_scaled := (ki_scaled + 10) <# 10000
        2: kd_scaled := (kd_scaled + 10) <# 10000
        
    "-", "_":
      case selected_param
        0: kp_scaled := (kp_scaled - 10) #> 0
        1: ki_scaled := (ki_scaled - 10) #> 0
        2: kd_scaled := (kd_scaled - 10) #> 0
    
    "*":  ' Multiply by 2 for coarse adjustment
      case selected_param
        0: kp_scaled := (kp_scaled * 2) <# 10000
        1: ki_scaled := (ki_scaled * 2) <# 10000
        2: kd_scaled := (kd_scaled * 2) <# 10000
        
    "/":  ' Divide by 2 for coarse adjustment
      case selected_param
        0: kp_scaled := kp_scaled / 2
        1: ki_scaled := ki_scaled / 2
        2: kd_scaled := kd_scaled / 2
    
    "s", "S": save_pid_parameters()
    "l", "L": load_pid_parameters()
    "r", "R": reset_to_defaults()
    "a", "A": auto_tune_pid()

PRI update_pid_display(actual, output)
  DEBUG(`TERM PID GOTOXY 10 5)
  DEBUG(`PID "Kp: " fdec(kp_scaled, 1000, 3))
  if selected_param == 0
    DEBUG(`PID " <--")
  
  DEBUG(`PID GOTOXY 10 6)
  DEBUG(`PID "Ki: " fdec(ki_scaled, 1000, 3))
  if selected_param == 1
    DEBUG(`PID " <--")
    
  DEBUG(`PID GOTOXY 10 7)
  DEBUG(`PID "Kd: " fdec(kd_scaled, 1000, 3))
  if selected_param == 2
    DEBUG(`PID " <--")
    
  DEBUG(`PID GOTOXY 10 9)
  DEBUG(`PID "Setpoint: " udec(setpoint) "  ")
  DEBUG(`PID GOTOXY 10 10)
  DEBUG(`PID "Actual:   " udec(actual) "  ")
  DEBUG(`PID GOTOXY 10 11)
  DEBUG(`PID "Output:   " udec(output) "  ")
  DEBUG(`PID GOTOXY 10 12)
  DEBUG(`PID "Error:    " sdec(setpoint - actual) "  ")
```

### Live Parameter Effects

```spin2
PUB see_parameter_effects() | param_value, key
  DEBUG(`PLOT Effects SIZE 800 400)
  
  param_value := 50
  setup_effect_display()
  
  repeat
    ' Apply parameter to multiple visualizations
    show_waveform_effect(param_value)
    show_frequency_effect(param_value)
    show_timing_effect(param_value)
    show_amplitude_effect(param_value)
    
    key := DEBUG(PC_KEY)
    case key
      "+": param_value := (param_value + 1) <# 100
      "-": param_value := (param_value - 1) #> 0
      "*": param_value := (param_value * 2) <# 100
      "/": param_value := param_value / 2
      "5": param_value := 50  ' Return to center
      
    update_parameter_display(param_value)

PRI show_waveform_effect(param) | x, y
  ' Clear waveform area
  DEBUG(`Effects FILLBOX 50 50 350 150 BLACK)
  
  ' Draw waveform with parameter-controlled frequency
  repeat x from 50 to 350
    y := 100 + 40 * sin((x - 50) * param / 10)
    DEBUG(`Effects PIXEL 'x' 'y' GREEN)
    
PRI show_frequency_effect(param) | x, magnitude
  ' Clear spectrum area
  DEBUG(`Effects FILLBOX 400 50 700 150 BLACK)
  
  ' Draw spectrum with parameter-controlled peak
  repeat x from 400 to 700
    magnitude := 50 * exp(-abs(x - 400 - param * 3) / 20)
    DEBUG(`Effects LINE 'x' 150 'x' '(150 - magnitude)' CYAN)
```

## Professional Interface Design

Combine mouse and keyboard for professional debugging interfaces that rival commercial tools.

### Complete Control Panel

```spin2
PUB professional_control_panel() | mx, my, buttons, key
  DEBUG(`PLOT ControlPanel SIZE 1024 768)
  
  setup_control_panel()
  
  repeat
    ' Mouse handling
    mx, my, buttons := DEBUG(PC_MOUSE)
    handle_mouse_events(mx, my, buttons)
    
    ' Keyboard handling
    key := DEBUG(PC_KEY)
    if key
      handle_keyboard_events(key)
    
    ' Update displays
    update_all_displays()

PRI setup_control_panel()
  ' Create tabbed interface
  create_tab("Monitor", 10, 10, 1004, 50)
  create_tab("Control", 10, 10, 1004, 50)
  create_tab("Analyze", 10, 10, 1004, 50)
  create_tab("Configure", 10, 10, 1004, 50)
  
  ' Create control groups
  create_slider_group("Input Levels", 50, 100, 300, 400)
  create_button_group("System Control", 400, 100, 200, 400)
  create_meter_group("Output Monitor", 650, 100, 324, 400)
  create_plot_area("Real-time Data", 50, 520, 924, 228)

PRI create_slider_group(title, x, y, w, h) | i
  ' Draw group frame
  DEBUG(`ControlPanel BOX 'x' 'y' '(x+w)' '(y+h)' WHITE)
  DEBUG(`ControlPanel TEXT '(x+10)' '(y-5)' 'title' WHITE)
  
  ' Create 8 vertical sliders
  repeat i from 0 to 7
    create_vertical_slider(x + 20 + i*35, y + 30, 25, h - 60, i)

PRI create_vertical_slider(x, y, w, h, id)
  ' Draw slider track
  DEBUG(`ControlPanel LINE '(x+w/2)' 'y' '(x+w/2)' '(y+h)' GRAY)
  
  ' Draw slider thumb at current position
  value := get_slider_value(id)
  thumb_y := y + h - (value * h / 100)
  DEBUG(`ControlPanel FILLBOX '(x)' '(thumb_y-5)' '(x+w)' '(thumb_y+5)' GREEN)
  
  ' Draw value display
  DEBUG(`ControlPanel TEXT 'x' '(y+h+10)' udec(value) WHITE)
```

### Context-Sensitive Help

```spin2
VAR
  long help_visible
  long help_topic

PUB context_help_system() | key, mx, my
  help_visible := FALSE
  
  repeat
    key := DEBUG(PC_KEY)
    mx, my, _ := DEBUG(PC_MOUSE)
    
    ' F1 or ? for help
    if key == $70 or key == "?"
      toggle_help()
    
    ' Context-sensitive help on hover
    if !help_visible
      topic := get_hover_topic(mx, my)
      if topic <> help_topic
        show_tooltip(topic, mx, my)
        help_topic := topic
    
    ' ESC closes help
    if key == 27 and help_visible
      hide_help()

PRI show_tooltip(topic, x, y)
  if topic == 0
    return
    
  ' Draw tooltip near cursor
  text := get_help_text(topic)
  w := strsize(text) * 8 + 10
  h := 20
  
  ' Ensure tooltip stays on screen
  if x + w > 1024
    x := 1024 - w
  if y + h > 768
    y := y - h - 5
  else
    y := y + 20
    
  ' Draw tooltip
  DEBUG(`ControlPanel FILLBOX 'x' 'y' '(x+w)' '(y+h)' YELLOW)
  DEBUG(`ControlPanel BOX 'x' 'y' '(x+w)' '(y+h)' BLACK)
  DEBUG(`ControlPanel TEXT '(x+5)' '(y+2)' 'text' BLACK)

PRI get_help_text(topic) : text
  case topic
    TOPIC_SLIDER:    text := string("Drag to adjust, scroll for fine control")
    TOPIC_BUTTON:    text := string("Click to activate, right-click for options")
    TOPIC_PLOT:      text := string("Click to place cursor, drag to zoom")
    TOPIC_VALUE:     text := string("Click to edit, Enter to confirm")
    TOPIC_TAB:       text := string("Click to switch view, Ctrl+Tab to cycle")
```

## Building Debug Control Objects

Create reusable interactive components for every project.

### Interactive Slider Object

```spin2
OBJ
  slider[8] : "debug_slider"
  
PUB demo_slider_object() | i, value
  ' Initialize 8 sliders
  repeat i from 0 to 7
    slider[i].init(50 + i*90, 100, 60, 200, 0, 100, 50)
    slider[i].set_color(GREEN, RED, YELLOW)
    slider[i].set_label(string("Ch ", i+48))
  
  repeat
    ' Update all sliders
    repeat i from 0 to 7
      if slider[i].handle_mouse()
        value := slider[i].get_value()
        apply_channel_value(i, value)
      
      slider[i].draw()
```

### Clickable Button Matrix

```spin2
OBJ
  buttons : "debug_button_matrix"
  
PUB demo_button_matrix() | row, col, state
  buttons.init(100, 100, 8, 4, 60, 40, 10)
  
  ' Label buttons
  repeat row from 0 to 3
    repeat col from 0 to 7
      buttons.set_label(row, col, string("F", row*8+col+1))
  
  repeat
    if buttons.handle_mouse()
      row, col := buttons.get_pressed()
      state := buttons.get_state(row, col)
      handle_button_press(row, col, state)
    
    buttons.draw_all()
```

## Your Turn: Interactive Challenge

Create an interactive debugging interface for this motor control system:

```spin2
PUB motor_control_challenge()
  ' Current non-interactive version
  repeat
    speed := 50  ' Fixed speed
    direction := 1  ' Fixed forward
    
    set_motor(speed, direction)
    DEBUG("Speed: ", udec(speed))
    waitms(10)
```

**Your Mission:**
1. Add keyboard control for speed (arrow keys)
2. Add mouse control for direction (click left/right)
3. Create visual speed slider
4. Add emergency stop button (spacebar and click)
5. Show real-time motor parameters
6. Add preset speed buttons (1-5 for 20/40/60/80/100%)

## Chapter Summary: From Observation to Control

PC input integration transformed your debugging:

✓ **Bidirectional communication** replaces one-way observation
✓ **Real-time parameter adjustment** eliminates recompile cycles
✓ **Mouse precision control** for analog adjustments
✓ **Keyboard shortcuts** for rapid mode changes
✓ **Professional interfaces** rival commercial tools

Your debug windows are no longer passive displays. They're interactive control panels that let you tune, test, and troubleshoot in real-time. Your keyboard and mouse have become debugging instruments as powerful as any logic analyzer or oscilloscope.

Chapter 6 shows you how to build professional debug instruments using all these capabilities together.

---

*Next: Chapter 6 - Professional Debug Instruments*
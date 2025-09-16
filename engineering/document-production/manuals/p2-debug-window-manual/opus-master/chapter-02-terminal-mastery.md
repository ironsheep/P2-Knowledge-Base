# Chapter 2: Terminal Mastery - Interactive Text Debugging

*Transform your chaotic scrolling text into organized, interactive debug displays that respond to your keyboard and mouse.*

## From Scroll Chaos to Organized Control

Remember your last debugging session? Text flying by. Searching for that one value. Missing critical state changes in the blur. Let's fix that permanently.

### The Transformation Begins

**Before: The Scrolling Nightmare**
```spin2
PUB debug_sensors()
  repeat
    DEBUG("Temp: ", udec(temperature))
    DEBUG("Pressure: ", udec(pressure))
    DEBUG("Humidity: ", udec(humidity))
    DEBUG("Light: ", udec(light_level))
    waitms(100)
    
' Output scrolls endlessly:
' Temp: 72
' Pressure: 1013
' Humidity: 45
' Light: 850
' Temp: 73
' Pressure: 1013
' ... (good luck finding that pressure spike)
```

**After: The Professional Dashboard**
```spin2
PUB debug_sensors_pro()
  ' Create organized display
  DEBUG(`TERM Sensors SIZE 40 10 POS 100 100)
  DEBUG(`Sensors CLS)
  
  ' Labels stay put
  DEBUG(`Sensors GOTOXY `(1) `(1) "SENSOR DASHBOARD")
  DEBUG(`Sensors GOTOXY `(1) `(3) "Temperature: ")
  DEBUG(`Sensors GOTOXY `(1) `(4) "Pressure:    ")
  DEBUG(`Sensors GOTOXY `(1) `(5) "Humidity:    ")
  DEBUG(`Sensors GOTOXY `(1) `(6) "Light:       ")
  
  repeat
    ' Values update in place - no scrolling!
    DEBUG(`Sensors GOTOXY `(15) `(3) udec_(temperature) "°F   ")
    DEBUG(`Sensors GOTOXY `(15) `(4) udec_(pressure) " hPa ")
    DEBUG(`Sensors GOTOXY `(15) `(5) udec_(humidity) "%    ")
    DEBUG(`Sensors GOTOXY `(15) `(6) udec_(light_level) " lux ")
    waitms(100)
```

See the difference? Fixed positions. Clean updates. Professional presentation. And we're just getting started.

## PC Input Integration - Bidirectional Communication

Here's where P2 debugging becomes revolutionary. Your keyboard and mouse aren't just for typing code anymore.

### Keyboard Control: Your Debug Remote Control

```spin2
PUB interactive_parameter_tuning() | key, pwm_duty, gain
  pwm_duty := 50
  gain := 100
  
  DEBUG(`TERM Control SIZE 50 15)
  DEBUG(`Control CLS)
  DEBUG(`Control "INTERACTIVE PARAMETER CONTROL\n\n")
  DEBUG(`Control "Keys:\n")
  DEBUG(`Control "  Q/A - Adjust PWM Duty\n")
  DEBUG(`Control "  W/S - Adjust Gain\n")
  DEBUG(`Control "  SPACE - Reset defaults\n")
  DEBUG(`Control "  ESC - Exit\n\n")
  
  repeat
    key := DEBUG(PC_KEY)    ' Read keyboard input
    
    case key
      "Q", "q": pwm_duty := (pwm_duty + 5) <# 100
      "A", "a": pwm_duty := (pwm_duty - 5) #> 0
      "W", "w": gain := (gain + 10) <# 500
      "S", "s": gain := (gain - 10) #> 0
      32:       pwm_duty := 50, gain := 100  ' Space = reset
      27:       quit                          ' ESC = exit
    
    ' Update display
    DEBUG(`Control GOTOXY `(0) `(9))
    DEBUG(`Control "PWM Duty: " udec_(pwm_duty) "%  ")
    DEBUG(`Control GOTOXY `(0) `(10))
    DEBUG(`Control "Gain: " udec_(gain) "     ")
    
    ' Apply parameters to actual system
    set_pwm(pwm_duty)
    set_gain(gain)
```

Now you're tuning parameters in real-time. No recompiling. No downloading. Just immediate interactive control.

### Mouse Integration: Click to Debug

```spin2
PUB mouse_controlled_debugging() | x, y, buttons, zone
  DEBUG(`TERM MouseDebug SIZE 60 20)
  DEBUG(`MouseDebug CLS)
  
  ' Create clickable zones
  DEBUG(`MouseDebug GOTOXY `(5) `(5) "[START]")
  DEBUG(`MouseDebug GOTOXY `(15) `(5) "[STOP]")
  DEBUG(`MouseDebug GOTOXY `(25) `(5) "[RESET]")
  DEBUG(`MouseDebug GOTOXY `(35) `(5) "[PAUSE]")
  
  repeat
    x, y, buttons := DEBUG(PC_MOUSE)
    
    if buttons & 1  ' Left click
      zone := detect_zone(x, y)
      case zone
        1: start_system()
          DEBUG(`MouseDebug GOTOXY `(5) `(10) "System STARTED")
        2: stop_system()
          DEBUG(`MouseDebug GOTOXY `(5) `(10) "System STOPPED")
        3: reset_system()
          DEBUG(`MouseDebug GOTOXY `(5) `(10) "System RESET  ")
        4: pause_system()
          DEBUG(`MouseDebug GOTOXY `(5) `(10) "System PAUSED ")

PRI detect_zone(x, y) : zone
  ' Convert mouse coordinates to terminal zones
  if y == 5
    if x >= 5 and x < 12
      zone := 1  ' START
    elseif x >= 15 and x < 21
      zone := 2  ' STOP
    elseif x >= 25 and x < 32
      zone := 3  ' RESET
    elseif x >= 35 and x < 42
      zone := 4  ' PAUSE
```

Your debug window just became a control panel. Click buttons. Drag sliders. Interactive debugging at its finest.

## Advanced Cursor Control

Professional formatting transforms readability. Let me show you the techniques that matter.

### Multi-Field Selective Updates

```spin2
PUB professional_status_display() | cycle
  DEBUG(`TERM Status SIZE 60 12)
  DEBUG(`Status CLS)
  
  ' Static headers (drawn once)
  DEBUG(`Status COLOR `(CYAN15) GOTOXY `(20) `(1) "SYSTEM STATUS")
  DEBUG(`Status COLOR `(WHITE12) GOTOXY `(2) `(3) "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
  
  ' Field labels (drawn once)
  DEBUG(`Status COLOR `(GREEN10) GOTOXY `(2) `(5) "CPU Load:")
  DEBUG(`Status COLOR `(GREEN10) GOTOXY `(2) `(6) "Memory:")
  DEBUG(`Status COLOR `(GREEN10) GOTOXY `(2) `(7) "Temperature:")
  DEBUG(`Status COLOR `(GREEN10) GOTOXY `(2) `(8) "Uptime:")
  
  repeat
    ' Only update values, not labels
    update_cpu_field()
    update_memory_field()
    update_temperature_field()
    update_uptime_field()
    waitms(250)

PRI update_cpu_field() | load
  load := get_cpu_load()
  DEBUG(`Status GOTOXY `(15) `(5))
  
  ' Color coding based on value
  if load > 80
    DEBUG(`Status COLOR `(RED15))
  elseif load > 60
    DEBUG(`Status COLOR `(YELLOW12))
  else
    DEBUG(`Status COLOR `(GREEN12))
    
  DEBUG(`Status udec_(load) "%  ")
  
PRI update_temperature_field() | temp
  temp := get_temperature()
  DEBUG(`Status GOTOXY `(15) `(7))
  
  ' Visual warning system
  if temp > 85
    DEBUG(`Status COLOR `(RED15) REVERSE "WARNING: ")
  DEBUG(`Status COLOR `(WHITE10) udec_(temp) "°C  ")
```

Notice the pattern? Static elements draw once. Dynamic fields update selectively. No flicker. No waste. Professional.

### Creating Interactive Menus

```spin2
PUB debug_menu_system() | selection, key
  selection := 1
  
  DEBUG(`TERM Menu SIZE 40 15)
  DEBUG(`Menu CLS COLOR `(WHITE12))
  DEBUG(`Menu "DEBUG MODE SELECTION\n\n")
  
  repeat
    ' Draw menu with highlighted selection
    draw_menu_item(1, "1. Monitor Sensors", selection == 1)
    draw_menu_item(2, "2. Test Motors", selection == 2)
    draw_menu_item(3, "3. Check Communications", selection == 3)
    draw_menu_item(4, "4. Memory Dump", selection == 4)
    draw_menu_item(5, "5. Exit Debug Mode", selection == 5)
    
    key := DEBUG(PC_KEY)
    case key
      $C2: selection := (selection - 1) #> 1  ' Up arrow
      $C3: selection := (selection + 1) <# 5  ' Down arrow
      13:  execute_menu_item(selection)       ' Enter
      27:  quit                                ' ESC

PRI draw_menu_item(item, text, selected)
  DEBUG(`Menu GOTOXY `(5) `(item + 3))
  
  if selected
    DEBUG(`Menu COLOR `(BLACK) `(CYAN12) "▶ " 'text' "  ")
  else
    DEBUG(`Menu COLOR `(WHITE10) `(BLACK) "  " 'text' "  ")
```

Professional menu navigation in your debug window. Arrow keys to navigate. Enter to select. Escape to exit. Your users will think you're using a GUI.

## Real-Time Dashboard Displays

Let's build something impressive - a complete system monitor that updates smoothly without flicker.

### The Complete Dashboard Pattern

```spin2
PUB system_monitor_dashboard()
  setup_dashboard_layout()
  
  repeat
    update_performance_section()
    update_communication_section()
    update_sensor_section()
    update_alert_section()
    waitms(100)

PRI setup_dashboard_layout()
  DEBUG(`TERM Dashboard SIZE 80 25)
  DEBUG(`Dashboard CLS)
  
  ' Title bar
  DEBUG(`Dashboard COLOR `(WHITE15) `(BLUE10))
  DEBUG(`Dashboard GOTOXY `(0) `(0))
  repeat 80
    DEBUG(`Dashboard " ")
  DEBUG(`Dashboard GOTOXY `(30) `(0) " P2 SYSTEM MONITOR ")
  
  ' Section dividers
  DEBUG(`Dashboard COLOR `(CYAN8) `(BLACK))
  DEBUG(`Dashboard GOTOXY `(0) `(2) "┌─ Performance ─────────┐")
  DEBUG(`Dashboard GOTOXY `(26) `(2) "┌─ Communication ───────┐")
  DEBUG(`Dashboard GOTOXY `(52) `(2) "┌─ Sensors ─────────────┐")
  DEBUG(`Dashboard GOTOXY `(0) `(15) "┌─ System Alerts ───────────────────────────────────────────────────────────┐")

PRI update_performance_section() | cpu, mem, temp
  cpu := get_cpu_usage()
  mem := get_memory_usage()
  temp := get_core_temp()
  
  ' CPU bar graph
  DEBUG(`Dashboard GOTOXY `(2) `(4) "CPU: [")
  draw_bar(cpu, 20, GREEN12, YELLOW12, RED15)
  DEBUG(`Dashboard "] " udec_(cpu) "%  ")
  
  ' Memory bar graph
  DEBUG(`Dashboard GOTOXY `(2) `(5) "MEM: [")
  draw_bar(mem, 20, GREEN12, YELLOW12, RED15)
  DEBUG(`Dashboard "] " udec_(mem) "%  ")
  
  ' Temperature with color coding
  DEBUG(`Dashboard GOTOXY `(2) `(6) "TEMP: ")
  if temp > 80
    DEBUG(`Dashboard COLOR `(RED15))
  elseif temp > 60
    DEBUG(`Dashboard COLOR `(YELLOW12))
  else
    DEBUG(`Dashboard COLOR `(GREEN12))
  DEBUG(`Dashboard udec_(temp) "°C  ")

PRI draw_bar(value, width, color_low, color_med, color_high) | filled, i
  filled := (value * width) / 100
  
  repeat i from 0 to width-1
    if i < filled
      if value > 80
        DEBUG(`Dashboard COLOR `(color_high) "█")
      elseif value > 60
        DEBUG(`Dashboard COLOR `(color_med) "█")
      else
        DEBUG(`Dashboard COLOR `(color_low) "█")
    else
      DEBUG(`Dashboard COLOR `(WHITE2) "░")
```

This dashboard rivals professional monitoring tools. Bar graphs. Color coding. Multi-section layout. All in a terminal window.

## Performance Patterns for Efficient Terminal Updates

Speed matters in debugging. Here's how to keep your displays responsive.

### The Differential Update Pattern

```spin2
VAR
  long last_values[10]
  
PUB efficient_updates() | i, current_value
  repeat i from 0 to 9
    current_value := read_sensor(i)
    
    ' Only update if changed
    if current_value <> last_values[i]
      DEBUG(`Dashboard GOTOXY `(10) `(i+5))
      DEBUG(`Dashboard udec_(current_value) "    ")
      last_values[i] := current_value
```

### The Buffer and Burst Pattern

```spin2
PUB burst_update() | buffer[20], i
  ' Collect all data first
  repeat i from 0 to 19
    buffer[i] := read_fast_sensor(i)
  
  ' Then update display in one burst
  DEBUG(`Dashboard GOTOXY `(0) `(5))
  repeat i from 0 to 19
    DEBUG(`Dashboard udec_(buffer[i]) " ")
```

### The Priority Zone Pattern

```spin2
PUB priority_updates()
  static counter
  
  counter++
  
  ' Critical values - every cycle
  update_critical_values()
  
  ' Important values - every 10 cycles
  if counter // 10 == 0
    update_important_values()
  
  ' Status values - every 100 cycles
  if counter // 100 == 0
    update_status_values()
```

## Professional Formatting Techniques

The difference between amateur and professional debug output is formatting. Let me show you the patterns that matter.

### Aligned Columns

```spin2
PUB aligned_data_display() | i, name, value
  DEBUG(`Term DATA SIZE 60 20)
  DEBUG(`DATA CLS)
  DEBUG(`DATA "REGISTER DUMP\n\n")
  DEBUG(`DATA "Name          Hex       Decimal   Binary\n")
  DEBUG(`DATA "──────────────────────────────────────────\n")
  
  repeat i from 0 to 15
    name := get_register_name(i)
    value := get_register_value(i)
    
    ' Fixed-width fields ensure alignment
    DEBUG(`DATA 'name')
    pad_to_column(14)
    DEBUG(`DATA "$" uhex_long_(value))
    pad_to_column(24)
    DEBUG(`DATA udec_long_(value))
    pad_to_column(34)
    DEBUG(`DATA "%" ubin_long_(value))
    DEBUG(`DATA "\n")

PRI pad_to_column(col) | current
  current := get_cursor_x()
  repeat while current < col
    DEBUG(`DATA " ")
    current++
```

### Status Indicators

```spin2
PUB visual_status_indicators() | status
  repeat
    status := get_system_status()
    
    DEBUG(`Status GOTOXY `(10) `(5))
    case status
      IDLE:     DEBUG(`Status COLOR `(GREEN12) "● IDLE    ")
      RUNNING:  DEBUG(`Status COLOR `(CYAN15) "► RUNNING ")
      WARNING:  DEBUG(`Status COLOR `(YELLOW15) "⚠ WARNING ")
      ERROR:    DEBUG(`Status COLOR `(RED15) "✖ ERROR   ")
      
    ' Activity spinner
    show_activity_spinner()

VAR
  long spinner_state

PRI show_activity_spinner()
  DEBUG(`Status GOTOXY `(30) `(5))
  case spinner_state++ & 3
    0: DEBUG(`Status "│")
    1: DEBUG(`Status "/")
    2: DEBUG(`Status "─")
    3: DEBUG(`Status "\")
```

### Progress Bars

```spin2
PUB progress_bar_display() | percent, i
  DEBUG(`Progress GOTOXY `(5) `(10) "Processing: [")
  
  repeat percent from 0 to 100
    ' Update percentage
    DEBUG(`Progress GOTOXY `(50) `(10) udec_(percent) "%  ")
    
    ' Update bar
    DEBUG(`Progress GOTOXY `(19) `(10))
    repeat i from 0 to 29
      if i < (percent * 30 / 100)
        DEBUG(`Progress COLOR `(GREEN12) "█")
      else
        DEBUG(`Progress COLOR `(WHITE2) "░")
    
    process_next_item()
    
  DEBUG(`Progress GOTOXY `(5) `(12) COLOR `(GREEN15) "✓ Complete!")
```

## Building Your Debug Toolkit

Let's create reusable debug components you'll use in every project.

### The Universal Status Object

```spin2
OBJ
  status : "debug_status"
  
PUB main()
  status.init(`TERM Status SIZE 40 10)
  status.add_field("CPU", 5, 3, STATUS#PERCENT)
  status.add_field("Memory", 5, 4, STATUS#BYTES)
  status.add_field("Uptime", 5, 5, STATUS#TIME)
  
  repeat
    status.update("CPU", get_cpu_load())
    status.update("Memory", get_memory_used())
    status.update("Uptime", cnt / clkfreq)
    waitms(100)
```

### The Debug Menu Object

```spin2
OBJ
  menu : "debug_menu"
  
PUB main() | choice
  menu.init(`TERM Menu SIZE 40 15)
  menu.add_item("Monitor System")
  menu.add_item("Test Hardware")
  menu.add_item("Dump Memory")
  menu.add_item("Exit")
  
  repeat
    choice := menu.run()
    case choice
      1: monitor_system()
      2: test_hardware()
      3: dump_memory()
      4: quit
```

## Your Turn: Terminal Challenge

Here's broken code. Use your new terminal mastery to debug it:

```spin2
PUB buggy_sensor_monitor()
  ' This should show sensor readings in organized display
  ' But values overlap and display is chaotic
  ' Fix it using proper terminal control
  
  repeat
    DEBUG("Temperature: ", udec(read_temp()))
    DEBUG("Pressure: ", udec(read_pressure()))
    DEBUG("Humidity: ", udec(read_humidity()))
    ' Values overwrite each other!
    waitms(100)
```

**Your Mission:**
1. Create a named terminal window
2. Add proper positioning for each value
3. Implement color coding for out-of-range values
4. Add keyboard control to pause/resume updates
5. Include a visual indicator for update activity

## Chapter Summary: From Chaos to Control

You've transformed your terminal debugging from scrolling chaos to organized control:

✓ **Fixed positioning** eliminates scroll hunting
✓ **PC input integration** enables real-time control
✓ **Professional formatting** improves readability
✓ **Dashboard displays** provide system-wide visibility
✓ **Efficient updates** maintain responsiveness

But more importantly, you've discovered that P2's terminal window isn't just for text output - it's an interactive debugging interface that responds to your keyboard and mouse, creating a bidirectional communication channel that transforms how you debug.

Chapter 3 takes you beyond text into the visual realm with BITMAP windows and your first graphics debugging experiences.

---

*Next: Chapter 3 - Graphics Breakthrough: From Text to Visuals*
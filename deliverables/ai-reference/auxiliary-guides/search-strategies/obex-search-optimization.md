# OBEX Search Optimization Guide for Remote Claude

## Purpose
This guide helps remote Claude instances find relevant OBEX objects more effectively by using broader search strategies rather than limiting searches to specific object types.

## Core Problem
When searching for specific terms like "driver", "sensor", or "display", many relevant objects are missed because they may be categorized differently in OBEX (e.g., under "misc", "demos", or other categories).

## OBEX Statistics Overview
Total Objects: 113
Categories:
- drivers: 49 objects
- misc: 34 objects  
- display: 7 objects
- demos: 5 objects
- audio: 5 objects
- motors: 5 objects
- communication: 4 objects
- sensors: 3 objects
- tools: 1 object

## Search Strategy: Always Cast a Wide Net

### GOLDEN RULE: Search for Objects, Not Types
**Instead of**: "Find me a driver for X"
**Use**: "Find me OBEX objects related to X"

### Why This Works
- Many "drivers" are categorized as "misc" (34 objects)
- Some sensor drivers are in "sensors", others in "drivers", some in "misc"
- Display-related code exists in "drivers", "display", and "demos"
- Communication code spans "drivers", "communication", and "misc"

## Recommended Search Approach

### 1. Primary Search Pattern
When user asks for any hardware-related code, use this search hierarchy:

```yaml
search_strategy:
  step1_broad_keyword:
    description: "Search ALL OBEX objects for the main keyword"
    example: "LED", "SPI", "I2C", "sensor", "display"
    
  step2_related_terms:
    description: "Include related/similar terms"
    examples:
      - LED → [LED, pixel, RGB, WS2812, strip, neopixel]
      - Display → [display, LCD, OLED, screen, graphics, video]
      - Sensor → [sensor, detector, measure, read, monitor]
      - Communication → [serial, UART, I2C, SPI, bus, protocol]
      
  step3_author_search:
    description: "If looking for quality code, search by prolific authors"
    top_authors:
      - "Jon McPhalen (jonnymac)" - 44 objects
      - "Stephen M Moraco" - 15 objects
      - "Wuerfel_21" - 11 objects
```

### 2. Keyword Expansion Mapping

```yaml
keyword_expansions:
  # Hardware Interfaces
  i2c: [i2c, iic, twi, two-wire, 2-wire]
  spi: [spi, serial peripheral, 4-wire, shift]
  uart: [uart, serial, rs232, rs485, async]
  
  # Display Types
  lcd: [lcd, display, screen, text display, character]
  oled: [oled, display, screen, graphic, ssd1306]
  led: [led, pixel, ws2812, rgb, neopixel, strip, matrix]
  
  # Sensors
  temperature: [temp, temperature, thermal, heat, cold, thermometer, dht, ds18b20]
  motion: [motion, movement, accelerometer, gyro, imu, mpu]
  distance: [distance, range, ultrasonic, ping, lidar, proximity]
  light: [light, lux, ambient, photocell, brightness, bh1750]
  
  # Motors & Control
  motor: [motor, servo, stepper, pwm, drive, actuator]
  servo: [servo, pwm, position, angle, rc]
  stepper: [stepper, step, motor, precise, position]
  
  # Audio
  sound: [sound, audio, music, tone, beep, speaker, wav, mp3]
  
  # Communication Protocols
  network: [network, ethernet, wifi, internet, tcp, udp, http]
  wireless: [wireless, rf, radio, bluetooth, ble, zigbee, 433, 915]
```

### 3. Search Examples

#### Bad Search (Too Specific)
```
"Find I2C drivers in OBEX"
Result: Might miss I2C objects in "misc" or "communication" categories
```

#### Good Search (Broad)
```
"Find all OBEX objects that mention I2C, IIC, TWI, or two-wire communication"
Result: Catches all relevant objects regardless of category
```

#### Bad Search (Single Term)
```
"Find LED drivers"
Result: Misses RGB controllers, NeoPixel libraries, display drivers with LED support
```

#### Good Search (Expanded Terms)
```
"Find all OBEX objects related to: LED, RGB, WS2812, NeoPixel, pixel, strip, or addressable lighting"
Result: Comprehensive coverage of LED-related code
```

## Response Format for Remote Claude

When searching OBEX, always return results in this format:

```markdown
## OBEX Search Results

**Search Terms Used**: [list all expanded search terms]

**Objects Found**: [total count]

### Highly Relevant Objects
[List objects that directly match the primary need]

### Related/Alternative Objects  
[List objects that might solve the problem differently]

### Consider Also
[List objects from top authors that might have relevant examples]

**Note**: Searched across ALL categories to ensure comprehensive results.
```

## Implementation Checklist

When remote Claude receives an OBEX request:

1. ✅ **Never limit to specific categories** - Search all 113 objects
2. ✅ **Expand keywords** - Use the keyword expansion mapping
3. ✅ **Include synonyms** - Think of alternative terms
4. ✅ **Check top authors** - Their code often has good examples
5. ✅ **Report broadly** - Show primary matches AND alternatives

## Special Cases

### Hardware Not Listed
If searching for hardware not explicitly in OBEX:
1. Search for the communication protocol (I2C, SPI, UART)
2. Search for similar devices (e.g., "temperature sensor" for any temp sensor)
3. Look in "misc" category - it contains 34 objects with various purposes

### Example Code Needed
When user needs examples:
1. Jon McPhalen's objects (44 total) are typically well-documented
2. Demo objects often show complete implementations
3. Check objects with both SPIN2 and PASM2 for comprehensive examples

## Summary

**Key Insight**: OBEX categorization doesn't always match user mental models. A "driver" might be in "misc", a "sensor" might be in "drivers", and useful code might be in "demos".

**Solution**: Always search broadly across ALL objects using expanded keyword sets rather than limiting to expected categories.

**Result**: Better discovery rate and more options presented to the user.
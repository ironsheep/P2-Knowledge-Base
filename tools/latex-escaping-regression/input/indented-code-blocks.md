# Test Indented Code Blocks

This tests the bug where indented code blocks are being escaped.

## List with Code Blocks

1. **Reset Pin** (optional but recommended)
   ```pasm2
   dirl    #pin            ' Disable pin (Smart Pin OFF)
   ```

2. **Configure Mode**
   ```pasm2
   wrpin   mode_value, #pin ' Write mode configuration
   ```

3. **Set X Parameter** (mode-dependent)
   ```pasm2
   wxpin   x_value, #pin   ' Write X parameter
   ```

## Regular Code Block (not indented)

```spin2
CON
  LED_PIN = 56                  ' P2 Eval board LED
  FREQ_VALUE = 200_000_000     ' 200MHz with underscore
```

## Configuration Block

```{.configuration}
CON
  CONFIG_VALUE = $1234_5678    ' Hex with $ and underscore
```

Regular text with # and $ and _ should be escaped here.
# Smart Pins Template Verification

This document tests the p2kb-smart-pins template with listings to verify the showtabs fix.

## Code Block Test

```spin2
CON
  LED_PIN = 56

PUB main()
  ' Test Smart Pin configuration
  pinstart(LED_PIN, P_TRANSITION | P_OE, clkfreq / 2000, 0)
  
  repeat
    pinwrite(LED_PIN, 1)
    waitms(500)
    pinwrite(LED_PIN, 0)
    waitms(500)
```

This should compile without the `shobtabs undefined` error if templates are fixed.
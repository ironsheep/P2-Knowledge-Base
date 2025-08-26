# Shobtabs Error Reproducer

Minimal document to reproduce the shobtabs undefined error.

## Code Block Test

```spin2
CON
  _clkfreq = 200_000_000
  LED_PIN = 56

PUB main()
  pinstart(LED_PIN, P_TRANSITION | P_OE, clkfreq / 2000, 0)
```

This should trigger the same shobtabs error at line 165 in the lstlisting environment.
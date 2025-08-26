# Code Blocks Test Document

This document tests the `lstset` configuration that has been problematic.

## Spin2 Code Block

```spin2
CON
  _clkfreq = 200_000_000

VAR
  long counter

PUB main() | x
  repeat
    x := ++counter
    debug("Counter: ", udec(x))
    waitms(1000)
```

## PASM2 Code Block

```pasm2
            org     0
            
start       wrpin   ##P_DAC_124R_3V | P_OE, #20
            wypin   #$8000, #20              ' Output mid-scale
            
loop        rdlong  value, ptra
            wypin   value, #20
            jmp     #loop
            
value       long    0
```

## Multiple Code Blocks

First block:
```spin2
PUB setup_dac()
  pinstart(20, P_DAC_124R_3V | P_OE, 0, 0)
  wypin(20, $8000)  ' Output 1.65V
```

Second block:
```pasm2
            mov     outa, #%1010_0000
            mov     dira, #%1111_1111
```

This tests the `lstset` block configuration and code syntax highlighting.
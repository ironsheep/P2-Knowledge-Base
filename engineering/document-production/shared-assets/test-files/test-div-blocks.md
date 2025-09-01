# Test Document for Div-Based Code Blocks

Testing the 3-color pedagogical system with div-wrapped code blocks.

## Spin2 Code (Green)

Regular Spin2 code should render in green:

:::: spin2
```
PUB main() | i
  repeat i from 0 to 9
    debug(dec(i))
```
::::

## Configuration Code (Also Green)

Configuration blocks stay green per pedagogical decision:

:::: spin2
```
WRPIN: %0000_0000_000_0000000000000_01_00001_0
WXPIN: $0000_1234
WYPIN: $0000_5678
```
::::

## PASM2 Code (Yellow)

PASM2 assembly code should render in yellow:

:::: pasm2
```
        org
main    mov     dira, ##$FF
        mov     outa, #1
.loop   shl     outa, #1
        waitx   ##20_000_000
        tjnz    outa, #.loop
        jmp     #main
```
::::

## Antipattern Code (Red)

Code that demonstrates what NOT to do:

:::: antipattern
```
' This won't work - wrong pin mode
WRPIN: %0000_0000_000_0000000000000_11_11111_0
```
::::

## Mixed Example

Here's a complete example showing all three colors:

:::: antipattern
```
' Wrong way - pin not configured
PUB bad_example()
  pinhigh(56)  ' Won't work without configuration
```
::::

:::: spin2
```
' Right way - configure first
PUB good_example()
  wrpin(P_HIGH_1K5, 56)  ' Configure the pin
  pinhigh(56)             ' Now it works
```
::::

:::: pasm2
```
' Assembly equivalent
        wrpin   ##P_HIGH_1K5, #56
        drvh    #56
```
::::

## End of Test
# Chapter 8: Smart Pins Symphony

*64 independent I/O processors*

## The Hook: UART in 3 Instructions

```pasm2
        wrpin   ##P_ASYNC_TX, #PIN    ' Configure as UART TX
        wxpin   ##BAUD_RATE, #PIN     ' Set baud rate
        dirh    #PIN                  ' Enable pin
        ' That's it - hardware UART ready!
        
        wypin   char, #PIN            ' Send a character
        ' No bit-banging required!
```

## Smart Pins Explained

Each of the 64 pins has its own processor that can:
- Generate PWM
- Measure frequency
- Send/receive serial data
- Perform ADC/DAC operations
- Count edges
- Measure pulse widths
- And much more!

## Digital I/O Basics

```pasm2
' Simple output
        drvh    #PIN            ' Drive high
        drvl    #PIN            ' Drive low
        drvnot  #PIN            ' Toggle
        fltl    #PIN            ' Float (high-Z)
        
' Simple input
        testp   #PIN wc         ' Read pin into C flag
```

## PWM and Timing

```pasm2
' PWM output
        wrpin   ##P_PWM_TRIANGLE, #PIN
        wxpin   ##1000, #PIN    ' Period
        wypin   ##500, #PIN     ' 50% duty cycle
        dirh    #PIN            ' Start PWM
```

## Serial Communications

```pasm2
' Async serial (UART)
        wrpin   ##P_ASYNC_TX, #TX_PIN
        wxpin   baud_config, #TX_PIN
        dirh    #TX_PIN
        
' Send byte
        wypin   data, #TX_PIN
        waitx   #20             ' Brief delay
        testp   #TX_PIN wc      ' Check if done
```

## Real-World Example: WS2812 LED Driver

```pasm2
' Smart pin generates precise WS2812 timing
ws2812_setup
        wrpin   ##P_PULSE, #LED_PIN
        wxpin   bit_timing, #LED_PIN
        dirh    #LED_PIN
        
send_rgb
        shl     green, #8
        or      green, red
        shl     green, #8
        or      green, blue
        wypin   green, #LED_PIN  ' Send 24-bit RGB
```

---

*Continue to [Chapter 9: Streaming Data](09-streaming-data.md) →*
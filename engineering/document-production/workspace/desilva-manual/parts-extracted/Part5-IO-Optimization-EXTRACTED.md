
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

---

# Chapter 9: Streaming Data

*Moving data at maximum velocity*

## The Hook: DMA-Like Streaming

```pasm2
        setq    ##1000-1         ' Transfer 1000 longs
        rdlong  buffer, source   ' Happens at maximum speed!
        ' 4KB moved in microseconds!
```

## The Streamer Concept

The streamer is P2's DMA engine:
- Moves data between hub and pins
- Generates video
- Captures high-speed data
- All without CPU intervention

## FIFO Operations

```pasm2
        rdfast  #0, hubaddr     ' Start FIFO read
loop    rflong  data           ' Read from FIFO (no waiting!)
        ' Process data
        djnz    count, #loop
```

---

*Continue to [Chapter 10: Hub Execution](10-hub-execution.md) →*

---

# Chapter 10: Hub Execution

*Breaking free from 512 instructions*

## The Hook: Unlimited Code Size

```pasm2
        orgh    $400            ' Code in hub memory
        org     0               ' But executes like COG code!
        
hub_code
        ' Your code can be megabytes!
        ' No more 512 instruction limit!
```

## COG vs Hub Execution

**COG Execution**:
- Fast (2 clocks per instruction)
- Limited to 512 instructions
- Deterministic timing

**Hub Execution**:
- Slower (2-9 clocks per instruction)
- Unlimited size
- Perfect for large programs

## Mixed Mode Programming

```pasm2
        call    #hub_function   ' Call hub code from COG
        jmp     #cog_code      ' Jump back to COG
        ' Mix and match as needed!
```

---

*Continue to [Chapter 11: Interrupts (If You Must)](11-interrupts-if-you-must.md) →*

---

# Chapter 11: Interrupts (If You Must)

*With great power comes great responsibility*

## The Hook: Yes, P2 Has Interrupts

```pasm2
        setint1 #INT_PINRISE, #BUTTON_PIN  ' Setup interrupt
        ' Your code runs normally...
        ' Until button is pressed!
        
int1_handler
        ' Interrupt code here
        reti1                               ' Return from interrupt
```

## The Interrupt Controversy

P2 has interrupts. Should you use them? Usually NO.

Why? Because you have 8 COGs! Instead of interrupting important work, dedicate a COG to monitoring.

## When to Use Them

Rarely. But sometimes useful for:
- Ultra-low latency response
- Power-saving scenarios
- Legacy code ports

## When NOT to Use Them

Most of the time! Use a dedicated COG instead:
- Cleaner code
- Deterministic timing
- No priority inversion
- Easier debugging

---

*Continue to [Chapter 12: Optimization Mastery](12-optimization-mastery.md) →*

---

# Chapter 12: Optimization Mastery

*Making it faster, smaller, better*

## The Hook: 2x Speed with One Change

```pasm2
' Before: 8 clocks
        rdlong  x, hubaddr
        add     x, #1
        wrlong  x, hubaddr
        
' After: 4 clocks  
        rdlong  x, ptra++
        add     x, #1
        wrlong  x, --ptra
        ' PTRA magic saves cycles!
```

## Pipeline Optimization

Understanding the pipeline:
- Most instructions: 2 clocks
- Hub access: 2-9 clocks
- CORDIC: 55 clocks
- Multiply: 2 clocks

## Instruction Pairing

```pasm2
' These can overlap
        mul     x, y           ' Starts multiply
        add     a, b           ' Executes while multiply runs
        getmulh result         ' Gets multiply result
```

## Memory Access Patterns

```pasm2
' Block transfers are FAST
        setq    #16-1
        rdlong  buffer, hubaddr ' 16 longs in one go!
```

---

*Continue to [Chapter 13: Video Generation](13-video-generation.md) →*

---


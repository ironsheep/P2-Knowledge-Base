# Getting Started with Propeller 2

## What is the Propeller 2?

The Propeller 2 (P2) is a unique multicore microcontroller designed by Parallax Inc. It features:
- 8 symmetric processor cores (COGs)
- 512KB shared hub memory
- 64 Smart I/O pins
- Hardware CORDIC solver for complex math
- No interrupts needed - use multiple cores instead!

## Your First P2 Program

### Hello LED (PASM2 Assembly)

```pasm2
' Blink LED on Pin 56
        ORG     0           ' Start at COG address 0
        
        DRVL    #56         ' Drive pin 56 low (LED on)
        WAITX   ##25_000_000 ' Wait 0.5 seconds at 50MHz
        DRVH    #56         ' Drive pin 56 high (LED off)  
        WAITX   ##25_000_000 ' Wait 0.5 seconds
        JMP     #0          ' Jump back to start
```

### Understanding the Code

1. **ORG 0** - Sets the assembly origin to COG RAM address 0
2. **DRVL/DRVH** - Drive pin Low/High (P2 has powerful pin control)
3. **WAITX** - Wait for specified clock cycles
4. **##** - Large immediate value (> 9 bits)
5. **JMP #0** - Jump to address 0 (infinite loop)

## Key Concepts for Beginners

### 1. The COG Model
- Each COG is independent
- COGs run in parallel
- Each has 512 longs of private RAM
- All COGs share hub memory

### 2. Hub Memory Access
- 512KB shared by all COGs
- "Egg Beater" rotation gives fair access
- Each COG gets a turn every 8 clocks

### 3. No Operating System
- You control everything
- COG 0 starts at power-up
- Launch other COGs as needed
- Direct hardware control

## Next Steps

### Learn About:
1. **COG Communication** - How COGs talk to each other
2. **Smart Pins** - Autonomous I/O processing  
3. **CORDIC Math** - Hardware math acceleration
4. **Hub Execution** - Running code from hub memory

### Tools You'll Need:
- Propeller Tool or FlexProp IDE
- P2 Evaluation Board or P2 Edge Module
- USB cable for programming

## Important Notes

⚠️ **Documentation Status**: This is v0.1 documentation. Some features are not fully documented yet:
- SPIN2 high-level language (coming soon)
- Complete Smart Pin modes (10 of 32 documented)
- Boot process details (pending)

## Example: Launching Multiple COGs

```pasm2
' Main COG launches worker COG
        ORG     0
        
        COGINIT #1, #@worker  ' Start COG 1 with worker code
        
main_loop:
        ' Main COG continues here
        DRVL    #56          ' Blink LED on pin 56
        WAITX   ##50_000_000
        DRVH    #56
        WAITX   ##50_000_000
        JMP     #main_loop
        
        ORG     $100         ' Worker code starts here
worker:
        DRVL    #57          ' Blink different LED on pin 57
        WAITX   ##25_000_000 ' At different rate
        DRVH    #57
        WAITX   ##25_000_000
        JMP     #worker
```

## Resources

- [P2 Architecture Overview](../../developer-reference/architecture.md)
- [PASM2 Instruction Reference](../../quick-reference/pasm2-instructions.md)
- [Smart Pins Introduction](../../developer-reference/smart-pins-intro.md)

---

*P2 Learning Path v0.1.0 - More content coming soon!*
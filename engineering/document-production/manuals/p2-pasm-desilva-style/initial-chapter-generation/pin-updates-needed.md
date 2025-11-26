# Pin Updates Needed in P2 Manual

**Created**: 2025-08-20  
**Purpose**: Track pin number changes required for better pedagogical clarity  
**Status**: ⚠️ CHANGES REQUIRED

## 📍 Summary of Issues

Current manual uses board-specific pins (56-63) which:
1. Won't work without P2 Eval board
2. Create board dependency in basic examples
3. Prevent universal code examples

## 🔴 Required Changes

### Chapter 1: Your First Spin
**19 instances of pin 56/57 found**

#### Line 7 - Introduction
```diff
- I know you're absolutely crazy to have your first instruction executed, so let's not waste any time. Here's a complete PASM2 program that blinks an LED on pin 56 (that's the built-in LED on the P2 Eval board):
+ I know you're absolutely crazy to have your first instruction executed, so let's not waste any time. Here's a complete PASM2 program that blinks an LED on pin 16:
```

#### Lines 13-15 - First Code Example
```diff
-        drvh    #56             ' Drive pin 56 high (LED on)
+        drvh    #16             ' Drive pin 16 high (LED on)
         waitx   ##25_000_000    ' Wait ~0.25 seconds at 100MHz
-        drvl    #56             ' Drive pin 56 low (LED off)  
+        drvl    #16             ' Drive pin 16 low (LED off)  
```

#### After First Example - Add Note
```markdown
### A Note About Pin Numbers
We're using pin 16 in our examples - a safe, general-purpose pin. To use this example:
- **With external LED**: Connect an LED and resistor to pin 16
- **With P2 Eval board LED**: Change 16 to 56 (or 57-63)
- **With P2 Edge board**: Check your board's LED pin assignment

Throughout this manual, we use pins 16-47 for examples to avoid board-specific complications.
```

#### All Other Instances
Replace all remaining instances of:
- `#56` → `#16`
- `pin 56` → `pin 16`
- `pins 56-63` → `pins 16-19` (for multiple LED examples)
- `LED 56` → `LED on pin 16`

### Chapter 2: Architecture Safari
**1 instance found**

#### Line 204
```diff
-        drvnot  #56           ' Toggle LED
+        drvnot  #16           ' Toggle LED
```

### Chapter 2: Multi-COG Example Update
```diff
- coginit(COGEXEC_NEW, @cog_code, 56 + i)  ' Start 4 COGs
+ coginit(COGEXEC_NEW, @cog_code, 16 + i)  ' Start 4 COGs
```

## 📝 Text Updates Needed

### Update "Common Gotchas" Section
```diff
- 2. **Wrong pin number** - The P2 Eval board's LEDs are on pins 56-63. The P2 Edge module might have different assignments.
+ 2. **Wrong pin number** - Our examples use pins 16-47 for universal compatibility. Board LEDs vary: P2 Eval (56-63), P2 Edge (check documentation).
```

## 🎯 Pedagogical Benefits of These Changes

1. **Universal Examples**: Code works on any P2 setup
2. **Clear Pin Identity**: 16 is obviously a pin number, not a magic value
3. **Progressive Learning**: Start generic, specialize later
4. **Reduced Confusion**: No board-specific quirks in fundamentals

## ✅ Implementation Checklist

- [ ] Update all Chapter 1 pin references (19 instances)
- [ ] Add "Note About Pin Numbers" box after first example
- [ ] Update Chapter 2 references (1-2 instances)
- [ ] Review remaining chapters for consistency
- [ ] Update "Common Gotchas" text
- [ ] Verify PWM example uses consistent pins

## 📚 Standard Pin Map (For Reference)

After changes, the manual will use:
```
LEDs:     16-19  (was 56-59)
Buttons:  20-23  (new standard)
Serial:   24-27  (new standard)
PWM:      32-35  (new standard)
Sensors:  40-43  (new standard)
```

## 🔄 Migration Strategy

For readers with P2 Eval boards, include this standard note:
```markdown
**For P2 Eval Board Users**: 
Replace pin 16 with 56 to use the built-in LED, or connect an external LED to pin 16.
```

---

*These changes ensure examples teach concepts, not board specifics.*
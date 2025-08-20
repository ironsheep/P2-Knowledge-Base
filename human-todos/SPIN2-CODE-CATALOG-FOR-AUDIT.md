# SPIN2 Manual Code Examples - Catalog for Audit
*Extracted examples in manual order for Stephen to verify and enrich*

## HOW THIS AUDIT WORKS
1. I list what we extracted in order
2. You verify if we missed any between entries
3. You add metadata for each (what it demonstrates, key concepts, etc.)
4. We build a decorated, trusted source code knowledge base

---

## CODE EXAMPLES CATALOG
*Format: [ID] Page/Section - Brief Description - Status*

### SECTION 1: Language Basics (Pages 1-50 estimated)

#### SPIN2-001
**Location**: Early in manual (CON section introduction)
**Current Extract**:
```spin2
CON
  _clkfreq = 180_000_000
  PINS = 8
  DELAY = _clkfreq / 1000
```
**What We Think It Demonstrates**: Constant declarations
**Trust Level**: ❓ (unverified)
**Your Metadata**: _______________

#### SPIN2-002  
**Location**: Variable section
**Current Extract**:
```spin2
VAR
  long stack[64]
  byte buffer[256]
  word position
```
**What We Think It Demonstrates**: Variable declarations
**Trust Level**: ❓ (unverified)
**Your Metadata**: _______________

#### SPIN2-003
**Location**: Method definition section
**Current Extract**:
```spin2
PUB main() | local
  repeat
    local := getvalue()
    process(local)
```
**What We Think It Demonstrates**: Basic method structure
**Trust Level**: ❓ (unverified)
**Your Metadata**: _______________

[GAP CHECK: Any examples between 003 and 004?] _______________

#### SPIN2-004
**Location**: Control flow section (IF statement)
**Current Extract**:
```spin2
if value > 100
  high_handler()
elseif value > 50
  medium_handler()
else
  low_handler()
```
**What We Think It Demonstrates**: IF/ELSEIF/ELSE
**Trust Level**: ❓ (unverified)
**Your Metadata**: _______________

### SECTION 2: Loops and Iteration (Pages 50-100 estimated)

#### SPIN2-005
**Location**: REPEAT section
**Current Extract**:
```spin2
repeat 10
  toggle(LED_PIN)
  waitms(500)
```
**What We Think It Demonstrates**: Fixed repeat loop
**Trust Level**: ❓ (unverified)
**Your Metadata**: _______________

#### SPIN2-006
**Location**: REPEAT with variable
**Current Extract**:
```spin2
repeat count from 0 to 9
  display(count)
```
**What We Think It Demonstrates**: Repeat with counter
**Trust Level**: ❓ (unverified)
**Your Metadata**: _______________

[GAP CHECK: Any examples between 006 and 007?] _______________

### SECTION 3: Inline PASM2 (Pages 100-150 estimated)

#### SPIN2-007
**Location**: First inline PASM example
**Current Extract**:
```spin2
PUB toggle_pin(pin)
  org
    drvnot pin
    ret
  end
```
**What We Think It Demonstrates**: Simple inline PASM2
**Trust Level**: ❓ (unverified)
**Your Metadata**: _______________

#### SPIN2-008
**Location**: PASM2 with hub access
**Current Extract**:
```spin2
PUB read_hub(addr) : value
  org
    rdlong value, addr
    ret
  end
```
**What We Think It Demonstrates**: Hub memory access from PASM2
**Trust Level**: ❓ (unverified)
**Your Metadata**: _______________

### SECTION 4: Smart Pins (Pages 150-200 estimated)

#### SPIN2-009
**Location**: Smart pin configuration
**Current Extract**:
```spin2
PUB setup_smartpin(pin)
  wrpin(pin, P_HIGH_15K | P_LOW_15K)
  wxpin(pin, $1000)
  dirh(pin)
```
**What We Think It Demonstrates**: Smart pin setup
**Trust Level**: ❓ (unverified)
**Your Metadata**: _______________

[Continue for all 267 examples...]

---

## AUDIT INSTRUCTIONS FOR STEPHEN

### For Each Example Above:
1. **Verify Location**: Is this roughly where it appears?
2. **Check Completeness**: Is the full example shown?
3. **Add Metadata**:
   - What concept does it teach?
   - What's the difficulty level?
   - Any hardware requirements?
   - Common variations?
   - Gotchas/warnings?

### For Gaps Between Examples:
Please note any examples we missed between numbered entries

### Additional Metadata Template:
```
Example ID: SPIN2-XXX
Page Number: ___
Section: ___
Demonstrates: ___
Prerequisites: ___
Key Concepts: ___
Hardware Needed: ___
Difficulty: Beginner/Intermediate/Advanced
Related Examples: ___
Common Mistakes: ___
Variations: ___
```

---

## WHAT THIS GIVES US

Once decorated, each example becomes:
- **Trusted source code** (from official manual)
- **Categorized by concept** (searchable)
- **Linked to documentation** (context preserved)
- **Pattern library source** (for recommendations)
- **Learning progression** (difficulty levels)

---

## NEXT STEPS AFTER AUDIT

1. Create searchable example database
2. Extract patterns from examples
3. Build recommendation engine
4. Generate "show me how to..." responses

---

*This catalog format lets you systematically verify and enrich our extraction*
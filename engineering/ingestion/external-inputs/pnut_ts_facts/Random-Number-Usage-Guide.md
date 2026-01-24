# Random Number Usage Guide

## Overview

The Propeller 2 provides multiple mechanisms for random number generation:

- **GETRND** - Hardware random number from P2's true random number generator
- **??** operator - XORO32 pseudo-random number generator
- **XORO32** - PASM instruction for pseudo-random sequences

**Key Distinction:**
- **GETRND** provides hardware entropy (true randomness) - use for cryptography, unique IDs
- **??** uses XORO32 PRNG - fast, repeatable if seeded, suitable for games, simulations

## Basic Usage

### Hardware Random (GETRND)

```spin2
PUB get_random() : value
  '' Get hardware random 32-bit value

  value := getrnd()

PUB random_pin_state()
  '' Set pin to random state

  pinwrite(LED_PIN, getrnd() & 1)
```

GETRND returns a 32-bit value from the P2's hardware random number generator, which uses thermal noise for entropy.

### PRNG Random (??)

```spin2
VAR
  long seed

PUB init_random()
  '' Initialize PRNG with hardware random seed

  seed := getrnd()

PUB get_prng_random() : value
  '' Get next PRNG value (modifies seed)

  value := ??seed
```

The `??` operator:
- Applies XORO32 algorithm to the variable
- Updates the variable with new state
- Returns the new random value

## Random Range Patterns

### Random Integer in Range

```spin2
PUB random_range(min_val, max_val) : value
  '' Return random integer in [min_val, max_val] inclusive

  value := (getrnd() +// (max_val - min_val + 1)) + min_val

PUB random_0_to_n(n) : value
  '' Return random integer in [0, n-1]

  value := getrnd() +// n
```

**Note:** Use unsigned modulo (`+//`) for proper range limiting with unsigned random values.

### Random Percentage

```spin2
PUB random_percent() : percent
  '' Return random value 0-100

  percent := getrnd() +// 101

PUB chance(percent) : result
  '' Return TRUE with given probability (0-100)

  result := (getrnd() +// 100) < percent
```

### Random Float (0.0 to 1.0)

```spin2
CON
  SCALE_FACTOR = 4294967295.0          ' 2^32 - 1

PUB random_float() : value
  '' Return random float in [0.0, 1.0)

  value := float(getrnd()) /. SCALE_FACTOR

PUB random_float_range(min_val, max_val) : value
  '' Return random float in [min_val, max_val)

  value := random_float() *. (max_val -. min_val) +. min_val
```

## PRNG Seeding

### Seeding from Hardware Random

```spin2
VAR
  long prng_state

PUB seed_prng()
  '' Seed PRNG with hardware entropy

  prng_state := getrnd()
  if prng_state == 0                   ' XORO32 requires non-zero seed
    prng_state := 1

PUB next_random() : value
  value := ??prng_state
```

### Deterministic Seeding (Reproducible)

```spin2
CON
  FIXED_SEED = $DEADBEEF

PUB seed_reproducible()
  '' Seed for reproducible sequence (testing, debugging)

  prng_state := FIXED_SEED

PUB test_prng_sequence() | i, value
  '' Generate same sequence every time

  seed_reproducible()
  repeat i from 0 to 9
    value := ??prng_state
    debug("Random[", udec(i), "] = ", uhex(value))
```

### Time-Based Seeding

```spin2
PUB seed_from_time()
  '' Seed from system counter (less random than GETRND)

  prng_state := getct()
  if prng_state == 0
    prng_state := 1
```

## Patterns

### Random Selection

```spin2
PUB random_element(array_ptr, count) : value
  '' Select random element from array

  value := long[array_ptr][getrnd() +// count]

PUB random_char(str_ptr) : char
  '' Select random character from string

  char := byte[str_ptr][getrnd() +// strlen(str_ptr)]
```

### Weighted Random

```spin2
CON
  ' Cumulative weights (must be sorted ascending)
  WEIGHT_COMMON   = 70                 ' 70% chance
  WEIGHT_UNCOMMON = 90                 ' 20% chance (90-70)
  WEIGHT_RARE     = 100                ' 10% chance (100-90)

PUB weighted_random() : result | roll
  '' Return weighted random category

  roll := getrnd() +// 100
  if roll < WEIGHT_COMMON
    result := CATEGORY_COMMON
  elseif roll < WEIGHT_UNCOMMON
    result := CATEGORY_UNCOMMON
  else
    result := CATEGORY_RARE
```

### Array Shuffle (Fisher-Yates)

```spin2
PUB shuffle(array_ptr, count) | i, j, temp
  '' Shuffle array in place using Fisher-Yates algorithm

  repeat i from count - 1 to 1
    j := getrnd() +// (i + 1)          ' Random index 0..i
    ' Swap elements
    temp := long[array_ptr][i]
    long[array_ptr][i] := long[array_ptr][j]
    long[array_ptr][j] := temp
```

### Noise Generation

```spin2
VAR
  long noise_state

PUB init_noise(seed)
  '' Initialize noise generator

  noise_state := seed
  if noise_state == 0
    noise_state := 1

PUB white_noise() : sample
  '' Generate white noise sample (-128 to 127)

  sample := (??noise_state >> 24) - 128

PUB noise_byte() : sample
  '' Generate noise byte (0-255)

  sample := ??noise_state >> 24
```

### Unique ID Generation

```spin2
PUB generate_uuid(buffer_ptr) | i
  '' Generate 128-bit UUID using hardware random

  repeat i from 0 to 3
    long[buffer_ptr][i] := getrnd()

PUB generate_session_id() : id
  '' Generate unique session identifier

  id := getrnd()
```

### Random Walk

```spin2
VAR
  long position

PUB init_walk(start)
  position := start

PUB random_walk(step_size) : new_pos
  '' Move randomly up or down by step_size

  if getrnd() & 1
    position += step_size
  else
    position -= step_size
  new_pos := position
```

### Monte Carlo Simulation

```spin2
PUB estimate_pi(iterations) : pi_estimate | i, x, y, inside
  '' Estimate PI using Monte Carlo method

  inside := 0
  repeat i from 0 to iterations - 1
    x := random_float()
    y := random_float()
    if (x *. x +. y *. y) <. 1.0
      inside++

  pi_estimate := float(inside) *. 4.0 /. float(iterations)
```

## Hardware vs PRNG Comparison

| Aspect | GETRND (Hardware) | ?? (PRNG) |
|--------|-------------------|-----------|
| Source | Thermal noise | XORO32 algorithm |
| Speed | Slower | Very fast |
| Repeatability | Never repeats | Reproducible with same seed |
| Quality | True random | Pseudo-random |
| Use case | Cryptography, unique IDs | Games, simulations |
| Seed required | No | Yes |

### When to Use GETRND

- Cryptographic key generation
- Unique identifiers (UUIDs, session IDs)
- Security-sensitive applications
- Initial PRNG seeding

### When to Use ??

- Game mechanics (dice rolls, card shuffling)
- Simulations requiring reproducibility
- High-speed random generation
- Testing (reproducible test cases)

## XORO32 Algorithm

The `??` operator implements XORO32:

```
state ^= state >> 2
state ^= state << 1
state ^= state >> 1
return state
```

Properties:
- Period: 2^32 - 1 (never produces zero from non-zero seed)
- Fast: single instruction on P2
- Good statistical properties for non-cryptographic use
- **Not suitable for cryptography**

## Anti-Patterns

### Modulo Bias

```spin2
' WRONG: Modulo bias when range doesn't divide 2^32
value := getrnd() // 10                ' Slight bias toward 0-5

' BETTER: Use unsigned modulo
value := getrnd() +// 10

' BEST: For critical applications, rejection sampling
PUB unbiased_random(max_val) : value | threshold
  threshold := $FFFF_FFFF - ($FFFF_FFFF +// max_val)
  repeat
    value := getrnd()
  until value >= threshold
  value := value +// max_val
```

### Zero Seed

```spin2
' WRONG: Zero seed produces zero forever
VAR
  long state

PUB bad_init()
  state := 0                           ' ??state always returns 0!

' CORRECT: Ensure non-zero seed
PUB good_init()
  state := getrnd()
  if state == 0
    state := 1
```

### PRNG for Security

```spin2
' WRONG: PRNG for security-sensitive operations
PUB bad_generate_key() : key
  key := ??seed                        ' Predictable!

' CORRECT: Use hardware random for security
PUB good_generate_key() : key
  key := getrnd()
```

### Not Seeding PRNG

```spin2
' WRONG: Using uninitialized PRNG
VAR
  long prng

PUB bad_random() : value
  value := ??prng                      ' prng may be 0!

' CORRECT: Always initialize
PUB init()
  prng := getrnd()
  if prng == 0
    prng := 1
```

### Reseeding Too Often

```spin2
' WRONG: Reseeding every call
PUB bad_random() : value
  seed := getrnd()                     ' Slow, wasteful
  value := ??seed

' CORRECT: Seed once, use PRNG
VAR
  long initialized
  long state

PUB random() : value
  if not initialized
    state := getrnd()
    if state == 0
      state := 1
    initialized := TRUE
  value := ??state
```

### Truncating Without Scaling

```spin2
' WRONG: Loses randomness
value := getrnd() & $FF                ' Only uses low 8 bits

' CORRECT: Use all bits via modulo or shift
value := getrnd() +// 256              ' Full 32-bit randomness
value := getrnd() >> 24                ' Use high 8 bits (equally good)
```

## Summary Tables

### Random Functions

| Function | Type | Returns | Use Case |
|----------|------|---------|----------|
| `GETRND()` | Hardware | 32-bit random | Security, unique IDs |
| `??var` | PRNG | 32-bit random | Fast, reproducible |
| `XORO32` | PASM PRNG | 32-bit random | Assembly code |

### Common Patterns

| Pattern | Implementation |
|---------|----------------|
| Range [0, n-1] | `getrnd() +// n` |
| Range [min, max] | `(getrnd() +// (max-min+1)) + min` |
| Boolean (50%) | `getrnd() & 1` |
| Percent chance | `(getrnd() +// 100) < percent` |
| Float [0, 1) | `float(getrnd()) /. 4294967295.0` |

### Seeding Strategies

| Strategy | Code | Use Case |
|----------|------|----------|
| Hardware seed | `state := getrnd()` | Production |
| Fixed seed | `state := $DEADBEEF` | Testing |
| Time seed | `state := getct()` | Quick-and-dirty |

## Related Documentation

- [Operators-Usage-Guide.md](Operators-Usage-Guide.md) - ?? operator details
- [Floating-Point-Usage-Guide.md](Floating-Point-Usage-Guide.md) - Random float generation

# P2 Source Code Study Domains
*Running list of patterns and idioms to extract from source code for AI code generation*

## Core Study Areas

### 1. Object Shapes & Architecture Patterns
- **Object composition patterns**: How objects use other objects
- **Interface patterns**: Public method signatures and conventions
- **Object categories**:
  - Device drivers (direct hardware interface)
  - Protocol drivers (I2C, SPI, UART implementations)
  - Service objects (provide abstracted functionality)
  - Data provider objects (sensors, measurements)
  - Aggregator objects (combine multiple objects)
  - Utility objects (math, string manipulation, etc.)
  - Display/UI objects
  - State machine objects

### 2. Idiomatic Patterns
- **Initialization sequences**: start/stop/init conventions
- **Resource management**: How objects claim and release cogs/pins
- **Error handling patterns**: Return codes, error states
- **Configuration patterns**: How objects accept settings

### 3. Inter-Cog Communication
- **Mailbox patterns**
- **Shared memory protocols**
- **Lock-based synchronization**
- **Command/response patterns**
- **Circular buffer implementations**

### 4. Smart Pin Usage Patterns
- **Common configurations for standard protocols**
- **Pin pairing patterns**
- **Mode combinations**
- **Timing relationships**

### 5. Memory Management Patterns
- **Variable organization in objects**
- **Hub vs Cog RAM usage**
- **Buffer management**
- **Stack sizing patterns**

### 6. Performance Patterns
- **PASM2 optimization idioms**
- **Critical timing patterns**
- **Pipeline optimization**
- **CORDIC usage patterns**

### 7. Timing & Synchronization
- **Clock management**
- **Wait patterns (waitx, waitct, waitse)**
- **Event handling**
- **Interrupt patterns**

### 8. Naming Conventions
- **Method naming patterns**
- **Variable naming conventions**
- **Constant organization**
- **Object file naming**

### 9. Testing & Debug Patterns
- **Debug method patterns**
- **Test harness structures**
- **Serial output patterns**
- **Performance measurement**

### 10. Domain-Specific Patterns
- **Motor control patterns**
- **Sensor reading patterns**
- **Display driving patterns**
- **Audio generation patterns**
- **Communication protocol patterns**

## Object Shape Study Focus

### Key Questions for Object Analysis:
1. **What services does this object provide?** (its purpose)
2. **What objects does it depend on?** (composition)
3. **What is its initialization pattern?** (start/stop/init)
4. **How does it manage resources?** (cogs, pins, memory)
5. **What are its public methods?** (interface)
6. **How does it handle errors?** (error patterns)
7. **What state does it maintain?** (variables, flags)
8. **How does it communicate?** (with cogs, with caller)

### Object Shape Categories to Identify:
- **Singleton drivers** (single instance expected)
- **Multi-instance capable** (multiple copies can coexist)
- **Cog-bound objects** (require dedicated cog)
- **Cog-free objects** (run in caller's cog)
- **Hybrid objects** (can run either way)

### Method Pattern Categories:
- **Lifecycle**: start(), stop(), init()
- **Configuration**: config(), set_*(), enable/disable()
- **Data transfer**: read(), write(), tx(), rx()
- **Status**: ready(), busy(), error()
- **Utility**: convert(), calculate(), format()

---
*This document will be updated as we discover more patterns through source code analysis*
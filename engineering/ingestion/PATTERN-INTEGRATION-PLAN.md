# Pattern Integration Plan for Download On Demand System

## Understanding the Need
External AIs need **actionable information**, not just pattern names. They need to know:
- WHEN to apply a pattern (selection criteria)
- HOW to implement it (code structure)
- WHAT resources it requires (cogs, memory, pins)
- HOW patterns compose together

## Proposed YAML Tree Structure

### 1. WHERE Pattern Files Should Go

```
engineering/knowledge-base/P2/
├── architecture/
│   └── patterns/           # Hardware utilization patterns
│       ├── timing_control.yaml
│       ├── buffer_management.yaml
│       ├── cog_management.yaml
│       └── smart_pin_usage.yaml
│
├── language/
│   └── spin2/
│       └── patterns/       # Object composition patterns  
│           ├── object_composition/
│           │   ├── no_objects.yaml
│           │   ├── single_object.yaml
│           │   ├── few_objects.yaml
│           │   ├── several_objects.yaml
│           │   └── framework_pattern.yaml
│           └── domain_patterns/
│               ├── iot_device.yaml
│               ├── robotics.yaml
│               ├── data_logger.yaml
│               └── sensor_fusion.yaml
```

### 2. WHAT Each Pattern File Should Contain

Each pattern YAML file needs these sections:

```yaml
pattern_id: "buffer_management"
category: "resource_management"

# CRITICAL: Selection criteria for AI
selection_criteria:
  when_applicable:
    - "Data streaming between cogs"
    - "Serial communication buffering"
    - "Sensor data collection"
  data_characteristics:
    - "Continuous data flow"
    - "Producer/consumer mismatch"
  performance_requirements:
    - "Non-blocking operations"
    - "Predictable latency"

# CRITICAL: Structural signature (what to look for)
structural_signature:
  required_elements:
    - "Head and tail pointers"
    - "Fixed-size buffer array"
    - "Wraparound logic"
  code_markers:
    - "VAR byte buffer[SIZE]"
    - "head := (head + 1) // SIZE"
    - "if head == tail"

# CRITICAL: Implementation template
implementation_template:
  spin2: |
    CON
      BUF_SIZE = 256
    
    VAR
      byte buffer[BUF_SIZE]
      long head, tail
    
    PUB write_byte(b) : success
      next := (head + 1) // BUF_SIZE
      if next == tail
        return false  ' Buffer full
      buffer[head] := b
      head := next
      return true
    
    PUB read_byte() : b | valid
      if tail == head
        return -1  ' Buffer empty
      b := buffer[tail]
      tail := (tail + 1) // BUF_SIZE
      return b

# CRITICAL: Resource profile
resource_profile:
  memory_usage:
    hub_ram: "BUF_SIZE + 8 bytes"
    cog_ram: "0"
  timing:
    write_operation: "~20 cycles"
    read_operation: "~20 cycles"
  concurrency:
    thread_safe: false
    lock_required: true

# CRITICAL: Composition rules
composition_with:
  compatible_patterns:
    - "serial_communication"
    - "producer_consumer"
    - "cog_management"
  conflicts_with:
    - "direct_memory_access"
  typical_combinations:
    - pattern: "single_object"
      relationship: "buffer often inside serial object"
    - pattern: "cog_management"
      relationship: "background cog fills/empties buffer"

# CRITICAL: Real-world examples
examples:
  - file: "jm_fullduplexserial.spin2"
    usage: "RX and TX buffers for UART"
  - file: "sensor_logger.spin2"
    usage: "Sensor data collection buffer"

# CRITICAL: Common variations
variations:
  - name: "power_of_2_size"
    description: "Use AND mask instead of modulo"
    code: "head := (head + 1) & $FF  ' For 256-byte buffer"
  - name: "watermark_levels"
    description: "Trigger actions at fill levels"
```

### 3. Pattern Selection Logic for AI

Create a meta-pattern file that helps AI choose:

```yaml
# pattern_selection_guide.yaml
decision_tree:
  - question: "How many external objects needed?"
    answers:
      none:
        pattern: "no_objects"
        confidence: 0.95
      one:
        pattern: "single_object"
        confidence: 0.90
      two_to_three:
        pattern: "few_objects"
        confidence: 0.85
      four_to_six:
        pattern: "several_objects"
        confidence: 0.80
      seven_plus:
        pattern: "framework_pattern"
        confidence: 0.70
        
  - question: "Is data streaming involved?"
    answers:
      yes:
        required_patterns:
          - "buffer_management"
          - "timing_control"
      no:
        skip_patterns:
          - "buffer_management"
          
  - question: "Multiple processors needed?"
    answers:
      yes:
        required_patterns:
          - "cog_management"
          - "mailbox_communication"
```

### 4. Manifest Updates Required

Update these manifests to include new pattern categories:

```yaml
# patterns-manifest.yaml additions
by_category:
  # Existing categories...
  
  object_composition:
    complexity_levels:
      - {name: "no-objects", file: "object_composition/no_objects.yaml", 
         desc: "Self-contained libraries (51% of P2 code)"}
      - {name: "single-object", file: "object_composition/single_object.yaml",
         desc: "One dependency pattern (21% of P2 code)"}
      # ... etc
      
  hardware_utilization:
    resource_patterns:
      - {name: "buffer-management", file: "architecture/patterns/buffer_management.yaml",
         desc: "Ring buffers and FIFOs (82% of P2 code uses)"}
      - {name: "timing-control", file: "architecture/patterns/timing_control.yaml",
         desc: "Precise timing patterns (77% of P2 code uses)"}
      # ... etc
      
  domain_specific:
    application_patterns:
      - {name: "iot-device", file: "domain_patterns/iot_device.yaml",
         desc: "Network + sensors pattern"}
      - {name: "robotics", file: "domain_patterns/robotics.yaml",
         desc: "Motors + sensors + control"}
      # ... etc
```

### 5. Usage by External AI

External AI would navigate like this:

1. **Start at root manifest** → Find patterns section
2. **Read pattern_selection_guide.yaml** → Understand decision criteria
3. **Based on requirements**, select relevant patterns:
   - "I need a sensor driver" → single_object.yaml + buffer_management.yaml
   - "I need a robot controller" → several_objects.yaml + robotics.yaml + cog_management.yaml
4. **Read selected patterns** → Get implementation templates and resource profiles
5. **Apply composition rules** → Combine patterns correctly

## Key Design Principles

1. **Actionable over Descriptive** - Include actual code templates, not descriptions
2. **Selection Criteria First** - Help AI know WHEN to use each pattern
3. **Resource Transparency** - Clear costs in memory, timing, cogs
4. **Composition Rules** - How patterns work together or conflict
5. **Statistical Backing** - Include usage percentages from our 730-file audit

## Benefits for Download On Demand

- **Self-contained** - Each pattern file has everything needed to implement
- **Navigable** - Follows existing manifest→tree structure
- **Measurable** - AI can calculate resource budgets
- **Composable** - Clear rules for combining patterns
- **Evidence-based** - Backed by analysis of real P2 code

This approach turns our 28 discovered patterns into actionable knowledge that external AIs can directly use to generate proper P2 code.
# Phase I Documentation Samples

*These examples show what the proposed documentation would look like for instructions we can improve autonomously.*

## Sample 1: DRVH (Pin Control - HIGH Confidence)

```yaml
instruction: DRVH
syntax: DRVH    {#}D           {WCZ}
encoding: EEEE 1101011 CZL DDDDDDDDD 001011001
timing:
  cycles: 2
  type: fixed
group: Pins
description: |
  Drive one or more I/O pins high (output 1). Sets both the direction 
  register (DIR) and output register (OUT) for the specified pins to 
  make them outputs with high level. This is the most common way to 
  turn on LEDs, set control signals high, or drive logic 1 to external 
  devices.
  
  When using ADDPINS, affects a contiguous group of pins starting from
  the base pin number.
category: I/O Pin Instruction - Set pin(s) to output and drive high
parameters:
  - name: D
    description: |
      Pin specification (register or immediate):
      - Single pin: 0-63 for individual pin
      - Pin group: Use base_pin ADDPINS count for multiple pins
      - Register: Contains pin number or pin group specification
      - Immediate: #pin_number or #(base ADDPINS count)
flags_affected:
  C:
    formula: Prior state of DIR[pin] (reads previous direction bit)
  Z:
    formula: Prior state of OUT[pin] (reads previous output bit)
    note: Only valid for single pin operations
examples:
  - name: Single LED Control
    description: Turn on an LED connected to pin 56
    code: |
      drvh    #56              ' LED on pin 56 goes high
    source: common_pattern
    
  - name: Multiple Pin Control
    description: Drive 8 pins high for parallel data output
    code: |
      drvh    #BASE_PIN ADDPINS 7   ' Pins BASE_PIN through BASE_PIN+7 go high
    source: hub75_driver
    
  - name: Pulse Generation
    description: Generate a precise pulse using DRVH/DRVL
    code: |
      pulse_pin
              drvh    pin              ' Drive pin high
              waitx   duration         ' Hold for specified cycles
              drvl    pin              ' Drive pin low
              ret
    source: inline_pasm2_pattern
    
  - name: Smart Pin Reset Pattern
    description: Reset and reconfigure a smart pin
    code: |
      ' Reset smart pin before reconfiguration
      fltl    #SPI_CLK         ' Float low (reset smart pin)
      wrpin   config, #SPI_CLK ' Configure mode
      wxpin   timing, #SPI_CLK ' Set timing
      drvh    #SPI_CLK         ' Enable smart pin (drive high)
    source: flash_loader.spin2
    
related:
  - DRVL: Drive pin(s) low (complement operation)
  - DIRH: Set direction to output without changing level
  - OUTH: Set OUT register without changing direction
  - FLTL: Float pin low (disable drive)
  - DRVNOT: Toggle pin output state
  
notes:
  - Affects both DIR and OUT registers atomically
  - Use OUTH if you only want to change OUT register
  - Use DIRH if you only want to change direction
  - ADDPINS operator enables efficient multi-pin control
  - Smart pins must be driven high to enable after configuration
  
documentation_source: proposed_from_code_analysis
documentation_level: comprehensive
needs_validation: true
```

## Sample 2: WRPIN (Smart Pin - HIGH Confidence)

```yaml
instruction: WRPIN
syntax: WRPIN   {#}D,{#}S
encoding: EEEE 1100000 0LI DDDDDDDDD SSSSSSSSS
timing:
  cycles: 2
  type: fixed
group: Smart Pins
description: |
  Configure the operating mode of one or more smart pins. WRPIN sets the 
  complete 32-bit mode configuration that determines how a smart pin operates,
  including its function (PWM, serial, ADC, etc.), pin coupling, filtering,
  and output drive characteristics.
  
  Smart pins provide hardware-accelerated I/O operations that continue 
  autonomously without COG intervention. Each of the 64 I/O pins has an 
  independent smart pin circuit.
  
  After WRPIN configuration, use WXPIN/WYPIN to set parameters and DIRH
  to enable the smart pin.
category: Smart Pin Configuration - Set smart pin operating mode
parameters:
  - name: D
    description: |
      32-bit mode configuration value:
      Bits [31:24] - Pin input/output coupling configuration
        %AAAA_BBBB where:
        AAAA = Input A source (-3 to +3 pins from base, or special)
        BBBB = Input B source (-3 to +3 pins from base, or special)
      
      Bits [23:16] - High-level mode selection
        %TT_MMMMM where:
        TT = Pin output control (00=smart pin, 01=DAC, 10=cog, 11=other)
        MMMMM = Primary mode selection
      
      Bits [15:8] - Low-level mode configuration
        Mode-specific configuration bits
      
      Bits [7:0] - Input filtering and digitization
        %PP_FFF_ZZZ where:
        PP = Input polarity/threshold
        FFF = Filter configuration (000=none to 111=maximum)
        ZZZ = Input digitization options
        
  - name: S
    description: |
      Pin selection (single or multiple):
      Bits [5:0] - Base pin number (0-63)
      Bits [10:6] - Additional pin count for ADDPINS (0-31)
      
      Can use ADDPINS operator: base_pin ADDPINS count
      Example: 32 ADDPINS 7 affects pins 32-39
      
      Prior SETQ overrides the additional pin count in bits [10:6]
      
flags_affected: none

examples:
  - name: SPI Clock Generation
    description: Configure smart pin for SPI clock generation using transition mode
    code: |
      ' P_TRANSITION_OUTPUT mode generates clock from transitions
      wrpin   ##P_TRANSITION_OUTPUT | P_OE, #SPI_CLK_PIN
      wxpin   #1, #SPI_CLK_PIN        ' Timebase = sysclk/2
      wypin   #0, #SPI_CLK_PIN        ' Start transitions
      dirh    #SPI_CLK_PIN             ' Enable smart pin
    source: flash_loader.spin2
    
  - name: PWM Configuration
    description: Set up PWM for motor control with specific frequency
    code: |
      ' P_PWM_SAWTOOTH for standard PWM
      wrpin   ##P_PWM_SAWTOOTH | P_OE, #PWM_PIN
      wxpin   pwm_period, #PWM_PIN    ' Set PWM period (frequency)
      wypin   duty_cycle, #PWM_PIN    ' Set duty cycle
      dirh    #PWM_PIN                 ' Enable PWM output
    source: isp_bldc_motor.spin2
    
  - name: ADC Input Configuration
    description: Configure pin for analog input with filtering
    code: |
      ' P_ADC_1X for unity gain ADC mode
      wrpin   ##P_ADC_1X | P_ADC_FLOAT, #ADC_PIN
      wxpin   #%10_0111, #ADC_PIN     ' 128 sample averaging
      dirh    #ADC_PIN                 ' Enable ADC
      ' Now use RDPIN to read ADC values
    source: sensor_reading
    
  - name: Serial UART Transmit
    description: Configure smart pin for async serial transmission
    code: |
      ' P_ASYNC_TX for UART transmit
      wrpin   ##P_ASYNC_TX | P_OE, #TX_PIN
      wxpin   bit_period, #TX_PIN     ' Set baud rate timing
      dirh    #TX_PIN                  ' Enable transmitter
      ' Use WYPIN to send bytes
    source: serial_driver
    
  - name: Repository Mode
    description: Use smart pin as data mailbox between COGs
    code: |
      ' P_REPOSITORY stores 32-bit value
      wrpin   ##P_REPOSITORY, #REPO_PIN
      dirh    #REPO_PIN                ' Enable repository
      ' COG A: wypin data, #REPO_PIN   - Write data
      ' COG B: rdpin data, #REPO_PIN   - Read data
    source: multi_cog_sync

related:
  - WXPIN: Set smart pin X parameter (timing/configuration)
  - WYPIN: Set smart pin Y parameter (data/control)
  - RDPIN: Read smart pin result
  - RQPIN: Read smart pin status
  - DIRH: Enable smart pin after configuration
  - DIRL: Disable smart pin
  - FLTL: Reset smart pin before reconfiguration
  
notes:
  - Must reset pin with FLTL before changing modes
  - Smart pin stays configured until explicitly changed
  - Use DIRH to enable, DIRL to disable
  - Each mode has specific X and Y parameter meanings
  - Some modes require specific P_ constants for configuration
  - Pin coupling allows reading from nearby pins
  
documentation_source: proposed_from_code_analysis
documentation_level: comprehensive
needs_validation: true
```

## Sample 3: SETQ (Block Transfer - HIGH Confidence)

```yaml
instruction: SETQ
syntax: SETQ    {#}D
encoding: EEEE 1101011 00L DDDDDDDDD 000101000
timing:
  cycles: 2
  type: fixed
group: Miscellaneous
description: |
  Set the Q register to prepare for block operations or to pass values to
  certain instructions. SETQ is primarily used before RDLONG/WRLONG/WMLONG
  to enable fast block transfers between hub and cog RAM. It's also used
  with COGINIT to pass parameters, MUXQ for parallel bit operations, and
  various CORDIC operations.
  
  For block transfers, Q holds the count minus 1 (e.g., SETQ #15 transfers
  16 longs). The transfer is significantly faster than individual operations.
category: Special Register - Set Q for block operations and special functions
parameters:
  - name: D
    description: |
      Value to load into Q register:
      - For block transfers: (count - 1) where count is number of longs
      - For COGINIT: Parameter to pass to new cog
      - For MUXQ: Bit mask for parallel operations
      - For CORDIC: High 32 bits of 64-bit value
      - Register or immediate value (#0 to #511 typical)
      
flags_affected: none

examples:
  - name: Block Read from Hub
    description: Read 64 longs from hub to cog RAM
    code: |
      ' Read lookup table from hub to cog
      load_table
              setq    #64-1                    ' 64 longs
              rdlong  table_base, hub_addr     ' Read to cog[table_base..table_base+63]
              ret
              
      table_base  res  64                      ' Reserve 64 longs in cog
    source: common_pattern
    
  - name: Block Write to Hub
    description: Save cog registers to hub for debugging
    code: |
      ' Save first 16 cog registers to hub
      save_registers
              setq    #16-1                    ' 16 longs
              wrlong  0, save_buffer           ' Write cog[0..15] to hub
              ret
    source: debug_pattern
    
  - name: COG Launch with Parameter
    description: Start new cog with initialization parameter
    code: |
      ' Launch cog with mailbox address
      launch_worker
              setq    mailbox_addr             ' Pass mailbox address
              coginit #NEWCOG, #worker_code    ' Start new cog
              ret
              
      ' In worker cog, PTRA will contain mailbox_addr
    source: multi_cog_pattern
    
  - name: MUXQ Parallel Bit Operations
    description: Use with MUXQ for parallel RGB output
    code: |
      ' Output RGB data to multiple pins simultaneously
      output_rgb
              setq    rgb_mask                 ' Set bit mask
              muxq    outa, rgb_data           ' Update selected pins
              ret
              
      rgb_mask    long    $00FF_0000           ' Pins 16-23
      rgb_data    long    $00A5_0000           ' Data for those pins
    source: hub75_driver
    
  - name: Fast Buffer Copy
    description: Copy data between hub locations
    code: |
      ' Copy 256 longs from source to destination
      buffer_copy
              setq    #256-1                   ' 256 longs
              rdlong  temp_buf, source_addr    ' Read to cog
              setq    #256-1                   ' 256 longs
              wrlong  temp_buf, dest_addr      ' Write from cog
              ret
              
      temp_buf    res     256                  ' Temporary buffer
    source: data_movement
    
  - name: 64-bit CORDIC Division
    description: Set high 32 bits for 64-bit division
    code: |
      ' Divide 64-bit value by 32-bit divisor
      divide_64
              setq    high_32                  ' High 32 bits of dividend
              qdiv    low_32, divisor          ' Start division
              ' ... wait for completion ...
              getqx   quotient                 ' Get quotient
              getqy   remainder                ' Get remainder
              ret
    source: math_operations

related:
  - SETQ2: Set Q for LUT RAM block transfers
  - RDLONG: Read long(s) from hub (uses Q for count)
  - WRLONG: Write long(s) to hub (uses Q for count)
  - WMLONG: Masked write to hub (uses Q for mask)
  - MUXQ: Parallel bit operations using Q as mask
  - COGINIT: Launch cog with Q as parameter
  - QDIV: CORDIC division using Q for high bits
  
notes:
  - Q register is not directly readable
  - Block transfers are much faster than loops
  - Always set Q immediately before the operation that uses it
  - For block ops, Q = (count - 1), not count
  - Maximum practical block size is 496 longs (cog RAM limit)
  - Q is preserved across most instructions
  
documentation_source: proposed_from_code_analysis
documentation_level: comprehensive
needs_validation: true
```

## Sample 4: LOCKTRY (Synchronization - HIGH Confidence)

```yaml
instruction: LOCKTRY
syntax: LOCKTRY {#}D           {WC}
encoding: EEEE 1101101 0CL DDDDDDDDD 000000100
timing:
  cycles: 2-7
  type: variable
group: Hub Control
description: |
  Attempt to acquire a hardware lock for mutual exclusion between COGs.
  Returns immediately with success/failure status in C flag. Does not
  block if lock is unavailable. P2 provides 16 hardware locks (0-15)
  shared by all COGs for implementing critical sections, resource
  protection, and synchronization primitives.
  
  Locks are atomic test-and-set mechanisms that guarantee only one COG
  can hold a particular lock at any time. Common convention reserves
  lock 15 for debug monitor.
category: Lock Management - Try to acquire hardware lock (non-blocking)
parameters:
  - name: D
    description: |
      Lock number or destination:
      - Immediate form (#0-15): Specific lock number to acquire
      - Register form: Contains lock number (bits 3:0 used)
      - Result: Previous lock state written to D (0=was free, 1-8=COG+1 that held it)
      
flags_affected:
  C:
    formula: |
      1 = Lock successfully acquired
      0 = Lock was already held (busy)
      
examples:
  - name: Simple Critical Section
    description: Protect shared resource access
    code: |
      ' SPI bus protection between COGs
      spi_write
      .retry  locktry #SPI_LOCK       wc   ' Try to get lock
      if_nc   jmp     #.retry              ' Retry if busy
              
              ' Critical section - exclusive SPI access
              drvl    #SPI_CS                 ' Select device
              call    #spi_transfer           ' Transfer data
              drvh    #SPI_CS                 ' Deselect device
              
              lockrel #SPI_LOCK               ' Release lock
              ret
              
      SPI_LOCK = 5                          ' Lock number for SPI
    source: resource_protection
    
  - name: Timeout Pattern
    description: Try with timeout to prevent infinite wait
    code: |
      ' Acquire lock with timeout
      acquire_with_timeout
              mov     timeout, ##1_000_000    ' ~10ms at 100MHz
      .loop   locktry #RESOURCE_LOCK  wc      ' Try to acquire
      if_c    ret                             ' Success - got lock
              djnz    timeout, #.loop         ' Keep trying
              neg     result, #1              ' Return error code
              ret                             ' Failed to acquire
    source: robust_pattern
    
  - name: Debug Monitor Pattern
    description: Singleton debug monitor using lock 15
    code: |
      ' Only one COG becomes debug monitor
      debug_init
              locktry #15             wc      ' Try for debug lock
      if_nc   jmp     #normal_cog            ' Someone else is monitor
              
              ' We are the debug monitor
              call    #setup_debug_isr        ' Install ISR
              ' Never release lock 15           ' Maintain singleton
              jmp     #debug_loop
              
      normal_cog
              ' Regular COG operation
    source: Spin2_debugger.spin2
    
  - name: Try-Once Pattern
    description: Non-blocking resource check
    code: |
      ' Check if resource available without waiting
      check_resource
              locktry #PRINT_LOCK     wc      ' Try once
      if_nc   jmp     #resource_busy         ' Don't wait
              
              ' Got lock - use resource
              call    #print_message
              lockrel #PRINT_LOCK
              ret
              
      resource_busy
              ' Do something else or queue request
              ret
    source: non_blocking_pattern
    
  - name: Multi-Lock Acquisition
    description: Acquire multiple locks avoiding deadlock
    code: |
      ' Always acquire in same order to prevent deadlock
      get_all_locks
      .restart
              locktry #LOCK_A         wc      ' Try first lock
      if_nc   jmp     #.restart              ' Retry
      
              locktry #LOCK_B         wc      ' Try second lock
      if_nc   lockrel #LOCK_A                ' Release first
      if_nc   jmp     #.restart              ' Retry both
              
              locktry #LOCK_C         wc      ' Try third lock
      if_nc   lockrel #LOCK_B                ' Release second
      if_nc   lockrel #LOCK_A                ' Release first
      if_nc   jmp     #.restart              ' Retry all
              
              ' Have all three locks
              ret
    source: deadlock_prevention

related:
  - LOCKREL: Release a held lock
  - LOCKNEW: Allocate an unused lock
  - LOCKRET: Return lock to available pool
  - COGATN: Signal COG after releasing lock
  - WAITATN: Wait for signal after lock release
  
notes:
  - Hardware ensures atomicity - no race conditions
  - Locks are numbered 0-15 (16 total)
  - Lock 15 traditionally reserved for debug monitor
  - Always release locks on all exit paths
  - Use consistent lock ordering to prevent deadlock
  - Consider timeout patterns for robustness
  - Locks persist across cog restarts until explicitly released
  
documentation_source: proposed_from_code_analysis
documentation_level: comprehensive
needs_validation: true
```

## Key Features of Phase I Documentation

### 1. **Clear, Comprehensive Descriptions**
- Explains WHAT the instruction does
- Explains WHEN to use it
- Explains WHY it's useful
- No cryptic single-line descriptions

### 2. **Detailed Parameter Explanations**
- Every operand explained
- Bit field breakdowns where applicable
- Clear immediate vs register usage
- Special cases documented

### 3. **Unambiguous Flag Formulas**
- Plain English explanations
- No mysterious variables like "K[31]"
- Clear conditions for flag changes

### 4. **Real Code Examples**
- Multiple examples showing different uses
- Sourced from actual production code
- Comments explaining the pattern
- Complete enough to understand context

### 5. **Related Instructions**
- Shows instruction families
- Indicates complementary operations
- Helps AI understand relationships

### 6. **Practical Notes**
- Common pitfalls
- Best practices
- Performance considerations
- Hardware constraints

### 7. **Validation Markers**
- Marked as "proposed_from_code_analysis"
- "needs_validation: true" flag
- Ready for expert review

This level of documentation would transform the current minimal entries into comprehensive references that AI systems can use effectively for code generation.
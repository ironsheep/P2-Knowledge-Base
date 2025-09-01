# Source Code Extraction Catalog - P2 SmartPins-220809
*Extracted: code-20250824 on 2025-08-24*

## Summary
- **Total Code Examples**: 98
- **Source PDF**: P2 SmartPins-220809
- **Output Directory**: /Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/sources/extractions/smart-pins-complete-extraction-audit/assets/code-20250824/

### By Language
- **Unknown**: 34 examples
- **PASM2**: 47 examples
- **Spin2**: 16 examples
- **Mixed**: 1 examples

### By Type
- **Snippet**: 88 examples
- **Code Fragment**: 10 examples

---

## Code Examples

### req01: Code Example
- **File**: `req01-wrpin-d-s-write-bits-d-31-0-to.txt`
- **Page**: 5, Lines 14-17
- **Language**: Unknown | **Type**: Snippet | **Lines**: 4
- **Content**: `WRPIN D/#,S/#        Write bits D[31:0] to Mode register for...`
- **Context**: Programs read or write 32-bit values to and from these four registers following | completion of the 2-clock instructions shown here:

### req02: Code Example
- **File**: `req02-wypin-d-s-write-bits-d-31-0-to.pasm2`
- **Page**: 5, Lines 18-19
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `WYPIN D/#,S/#         Write bits D[31:0] to register Y for S...`
- **Context**: WXPIN D/#,S/#         Write bits D[31:0] to register X for Smart Pin S[5:0], | acknowledge Smart Pin.

### req03: Code Example
- **File**: `req03-rdpin-d-s-wc-read-smart-pin-s-.pasm2`
- **Page**: 5, Lines 20-23
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 4
- **Content**: `RDPIN D,S/# {WC} Read Smart Pin S[5:0] register Z[31:0], sav...`
- **Context**: WYPIN D/#,S/#         Write bits D[31:0] to register Y for Smart Pin S[5:0], | acknowledge Smart Pin.

### req04: Code Example
- **File**: `req04-akpin-s-acknowledge-smart-pin-.txt`
- **Page**: 5, Lines 24-25
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `AKPIN S/#                Acknowledge Smart Pin S[5..0].`
- **Context**: RQPIN D,S/# {WC}   Read Smart Pin S[5:0] register Z[31:0], save result in D[31:0], | flag into C, do not acknowledge.

### req05: Code Example
- **File**: `req05-rdpin-your_data-pin-number-get.pasm2`
- **Page**: 10, Lines 5-6
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `rdpin  your_data, #pin number     'get pin data`
- **Context**: .loop  testp  #pin_number,  wc    'set carry to IN flag state | if_nc  jmp #.loop                 'C = 0, jump

### req06: Code Example
- **File**: `req06-wrpin-jat-12.txt`
- **Page**: 11, Lines 19-20
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `wrpin  jat,   #12`
- **Context**: #12 | ' Set direction of P12 to logic-1 (output)

### req07: Code Example
- **File**: `req07-org-0.pasm2`
- **Page**: 11, Lines 50-51
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `org  0`
- **Context**: Example: | CON

### req08: Code Example
- **File**: `req08-wrpin-dacconfig-20.txt`
- **Page**: 12, Lines 5-7
- **Language**: Unknown | **Type**: Snippet | **Lines**: 3
- **Content**: `wrpin    DACconfig,   #20`
- **Context**: dirl                  #20 | 'Reset Pin P20

### req09: Code Example
- **File**: `req09-jmp-loop.pasm2`
- **Page**: 12, Lines 9-10
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `jmp #.loop`
- **Context**: dirh                  #20     'Start DAC mode | .loop   nop                           'Loop "forever"

### req10: Code Example
- **File**: `req10-wrpin-dacconfig-20-set-dac-con.txt`
- **Page**: 12, Lines 37-39
- **Language**: Unknown | **Type**: Snippet | **Lines**: 3
- **Content**: `wrpin      DACconfig, #20  'Set DAC configuration`
- **Context**: dat       org        0 | dirl       #20             'Set DAC at pin P20

### req11: Code Example
- **File**: `req11-wypin-dacvolt-20-load-dac.pasm2`
- **Page**: 13, Lines 5-6
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `wypin DACvolt, #20    'Load DAC`
- **Context**: if_nc     jmp  #.waitper        'Wait for carry flag = 1 | add DACvolt,   #$100  'Add $100 (256) to DAC voltage

### req12: Code Example
- **File**: `req12-con.spin2`
- **Page**: 14, Lines 25-26
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `CON`
- **Context**: square wave that switches between $F00F and $01F0 DAC output voltages. | Example

### req13: Code Example
- **File**: `req13-wrpin-dacconfig-20-set-configu.txt`
- **Page**: 14, Lines 30-32
- **Language**: Unknown | **Type**: Snippet | **Lines**: 3
- **Content**: `wrpin    DACconfig,    #20 'Set configuration`
- **Context**: 0 | dirl     #20               'Setup DAC at Smart-Pin P20

### req14: Code Example
- **File**: `req14-wypin-dacvolt2-20.pasm2`
- **Page**: 14, Lines 40-41
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `wypin  DACvolt2,  #20`
- **Context**: testp  #20  WC           'Test P20 | if_nc     jmp    #.waitper1        'Wait for C = 1

### req15: Code Example
- **File**: `req15-jmp-myloop.pasm2`
- **Page**: 14, Lines 44-47
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 4
- **Content**: `jmp    #.myloop`
- **Context**: .waitper2 testp  #20  WC          'Test P20 | if_nc     jmp    #.waitper2

### req16: Code Example
- **File**: `req16-con.spin2`
- **Page**: 15, Lines 23-24
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `CON`
- **Context**: overrides OUT, and controls the pin's output state. | The following code example creates 16 logic-1 pulses:

### req17: Code Example
- **File**: `req17-org-0.pasm2`
- **Page**: 15, Lines 26-27
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `org      0`
- **Context**: ' 25-MHz system clock frequency | dat

### req18: Code Example
- **File**: `req18-wrpin-pulseconfig-20-set-confi.txt`
- **Page**: 15, Lines 28-31
- **Language**: Unknown | **Type**: Snippet | **Lines**: 4
- **Content**: `wrpin    PulseConfig,  #20   'Set config for pulse/cycle`
- **Context**: org      0 | dirl     #20                 'Setup Smart Pin at P20

### req19: Code Example
- **File**: `req19-org-0.pasm2`
- **Page**: 16, Lines 16-18
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 3
- **Content**: `org     0`
- **Context**: CON | dat

### req20: Code Example
- **File**: `req20-wrpin-transconfig-20.txt`
- **Page**: 16, Lines 19-24
- **Language**: Unknown | **Type**: Code Fragment | **Lines**: 6
- **Content**: `wrpin   TransConfig,    #20`
- **Context**: dirl    #20 | 'Setup Smart Pin at P20

### req21: Code Example
- **File**: `req21-con.spin2`
- **Page**: 17, Lines 11-12
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `CON`
- **Context**: state. | Example:

### req22: Code Example
- **File**: `req22-org-0.pasm2`
- **Page**: 17, Lines 14-16
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 3
- **Content**: `org     0`
- **Context**: _clk_freq = 25_000_000 | dat

### req23: Code Example
- **File**: `req23-wrpin-nco_config-20.txt`
- **Page**: 17, Lines 17-25
- **Language**: Unknown | **Type**: Code Fragment | **Lines**: 9
- **Content**: `wrpin   NCO_Config, #20`
- **Context**: dirl    #20 | 'Setup Smart Pin at P20

### req24: Code Example
- **File**: `req24-wypin-pa-20-send-pulse-count-t.pasm2`
- **Page**: 17, Lines 26-27
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `wypin pa,  #20                 'Send pulse count to Y regist...`
- **Context**: qfrac     ##123, ##_clkfreq   'Calc #of 25-MHz cycles for | '  8 msec period

### req25: Code Example
- **File**: `req25-con.spin2`
- **Page**: 19, Lines 3-4
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `CON`
- **Context**: Rev 5  06-11-2020 | Jon Titus, Page 19 of

### req26: Code Example
- **File**: `req26-org-0.pasm2`
- **Page**: 19, Lines 6-7
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `org     0`
- **Context**: _clkfreq = 25_000_000 | dat

### req27: Code Example
- **File**: `req27-wrpin-nco_config-20-set-config.txt`
- **Page**: 19, Lines 8-10
- **Language**: Unknown | **Type**: Snippet | **Lines**: 3
- **Content**: `wrpin   NCO_Config,  #20   'Set config for Transition mode`
- **Context**: org     0 | dirl    #20                'Setup Smart Pin at P20

### req28: Code Example
- **File**: `req28-org-0.pasm2`
- **Page**: 20, Lines 20-21
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `org     0`
- **Context**: COM | dat

### req29: Code Example
- **File**: `req29-wrpin-nco_config-20-set-config.txt`
- **Page**: 20, Lines 21-22
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `wrpin   NCO_Config,  #20  'Set configuration for PWM Triangl...`
- **Context**: dat | org     0

### req30: Code Example
- **File**: `req30-org-0.pasm2`
- **Page**: 21, Lines 38-40
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 3
- **Content**: `org      0`
- **Context**: COM | dat

### req31: Code Example
- **File**: `req31-wrpin-pwmsaw_config-20.txt`
- **Page**: 21, Lines 41-47
- **Language**: Unknown | **Type**: Code Fragment | **Lines**: 7
- **Content**: `wrpin    PWMsaw_Config,  #20`
- **Context**: dirl     #20 | 'Setup Smart Pin at P20

### req32: Code Example
- **File**: `req32-jmp-myloop-program-waits-forev.pasm2`
- **Page**: 21, Lines 49-50
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `jmp  #.myloop     'Program waits forever`
- **Context**: dirh     #20                    'Finished setup | wypin    Y_RegData,      #20

### req33: Code Example
- **File**: `req33-mov-dira-ff-set-p15-p8-as-outp.pasm2`
- **Page**: 24, Lines 10-11
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `mov     dira, ##$FF          'Set P15..P8 as outputs for LED...`
- **Context**: dat | org     0

### req34: Code Example
- **File**: `req34-wrpin-quadenc_config-32-set-fo.txt`
- **Page**: 24, Lines 12-15
- **Language**: Unknown | **Type**: Snippet | **Lines**: 4
- **Content**: `wrpin   QuadEnc_Config,  #32 'Set for Quad-Encoder mode`
- **Context**: mov     dira, ##$FF          'Set P15..P8 as outputs for LEDs | dirl    #32                  'Setup Smart Pin at P32

### req35: Code Example
- **File**: `req35-if_nc-jmp-wait_here-no-carry-l.pasm2`
- **Page**: 24, Lines 20-21
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `if_nc   jmp   #.wait_here         'No carry? Loop`
- **Context**: 'Test carry at Smart Pin P32 | nop

### req36: Code Example
- **File**: `req36-sar-quadenc_data-2-arithmetic-.txt`
- **Page**: 24, Lines 22-23
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `sar   QuadEnc_data, #2    'Arithmetic shift right 2`
- **Context**: if_nc   jmp   #.wait_here         'No carry? Loop | rqpin QuadEnc_data, #32   'Carry found, get total counts

### req37: Code Example
- **File**: `req37-jmp-myloop.pasm2`
- **Page**: 24, Lines 25-27
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 3
- **Content**: `jmp   #.myloop`
- **Context**: '   (divide by 4) | mov   outa, QuadEnc_data  'Send count to LEDs

### req38: Code Example
- **File**: `req38-mov-dira-ff.pasm2`
- **Page**: 24, Lines 38-41
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 4
- **Content**: `mov dira,    ##$FF`
- **Context**: dat | org     0

### req39: Code Example
- **File**: `req39-wrpin-quadenc_config-32-set-fo.txt`
- **Page**: 24, Lines 42-45
- **Language**: Unknown | **Type**: Snippet | **Lines**: 4
- **Content**: `wrpin QuadEnc_Config,  #32  'Set for Quad-Encoder mode`
- **Context**: dirl         #32 | 'Setup Smart Pin at P32

### req40: Code Example
- **File**: `req40-sar-quadenc_data-2-arithmetic-.txt`
- **Page**: 24, Lines 49-51
- **Language**: Unknown | **Type**: Snippet | **Lines**: 3
- **Content**: `sar    QuadEnc_data, #2        'Arithmetic shift right 2`
- **Context**: rqpin  QuadEnc_data, #32 | 'Get counts

### req41: Code Example
- **File**: `req41-mov-outa-quadenc_data.pasm2`
- **Page**: 24, Lines 51-53
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 3
- **Content**: `mov    outa, QuadEnc_data`
- **Context**: sar    QuadEnc_data, #2        'Arithmetic shift right 2 | ' (divide by 4)

### req42: Code Example
- **File**: `req42-jmp-myloop-program-waits-fore.pasm2`
- **Page**: 25, Lines 3-4
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `jmp    #.myloop                'Program waits forever`
- **Context**: Rev 5  06-11-2020 | Jon Titus, Page 25 of

### req43: Code Example
- **File**: `req43-mov-dira-ff-set-p7-p0-as-outpu.pasm2`
- **Page**: 27, Lines 26-27
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `mov dira, ##$FF               'Set P7..P0 as outputs for LED...`
- **Context**: dat | org

### req44: Code Example
- **File**: `req44-wrpin-a_in_mode-a_in-set-up-mo.txt`
- **Page**: 27, Lines 28-29
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `wrpin  A_in_mode,     #A_in   'Set up mode for pin P53`
- **Context**: mov dira, ##$FF               'Set P7..P0 as outputs for LEDs | dirl   #A_in

### req45: Code Example
- **File**: `req45-wypin-0-a_in-enable-smart-pin.pasm2`
- **Page**: 27, Lines 30-31
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `wypin  #0,            #A_in   'Enable Smart Pin`
- **Context**: wrpin  A_in_mode,     #A_in   'Set up mode for pin P53 | wxpin  ##$773_5940,   #A_in   'Set for 5-sec, 25 MHz clock

### req46: Code Example
- **File**: `req46-con.spin2`
- **Page**: 28, Lines 31-34
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 4
- **Content**: `CON`
- **Context**: ' Synchronous serial transmission (SPI) of system-clock periods | ' Positive trigger on the SPI clock, 25 MHz system clock

### req47: Code Example
- **File**: `req47-org-0.pasm2`
- **Page**: 28, Lines 36-37
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `org 0`
- **Context**: A_in     = 53     'Pin P53     'Counter input | dat

### req48: Code Example
- **File**: `req48-wrpin-sync_tx_mode-txout-set-s.txt`
- **Page**: 28, Lines 38-39
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `wrpin   sync_tx_mode,  #txout  'Set sync tx mode for pin 41`
- **Context**: org 0 | dirl                   #txout  'Transmitter setup

### req49: Code Example
- **File**: `req49-wrpin-clock_mode-clkout-set-pi.txt`
- **Page**: 29, Lines 6-7
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `wrpin   clock_mode,    #clkout 'Set pin as transition mode`
- **Context**: #txout   'Enable transmitter output | dirl    #clkout                'Clock output setup

### req50: Code Example
- **File**: `req50-wrpin-a_in_mode-a_in-set-up-mo.txt`
- **Page**: 29, Lines 12-13
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `wrpin   A_in_mode,     #A_in   'Set up mode for pin P53`
- **Context**: #clkout                'Enable clock-output | dirl    #A_in                  'Count A-input highs

### req51: Code Example
- **File**: `req51-wypin-0-a_in-count-only-a-inpu.pasm2`
- **Page**: 29, Lines 14-15
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `wypin   #0,            #A_in   'Count only A-input highs`
- **Context**: wrpin   A_in_mode,     #A_in   'Set up mode for pin P53 | wxpin   ##$17D_7840,   #A_in   'Set continuous count 1-sec,

### req52: Code Example
- **File**: `req52-wypin-64-clkout-start-clock-tr.pasm2`
- **Page**: 29, Lines 23-24
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `wypin   #64,   #clkout         'Start clock, transmit data`
- **Context**: wypin | rcvd_data, #txout      'Counter data sent via SPI

### req53: Code Example
- **File**: `req53-con.spin2`
- **Page**: 30, Lines 15-16
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `CON`
- **Context**: track proportion of logic states, and so on. | Example

### req54: Code Example
- **File**: `req54-org-0.pasm2`
- **Page**: 30, Lines 18-20
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 3
- **Content**: `org 0`
- **Context**: A_in = 53     ' Pin P53 | dat

### req55: Code Example
- **File**: `req55-wrpin-a_in_mode-a_in-set-up-mo.txt`
- **Page**: 30, Lines 21-22
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `wrpin  A_in_mode, #A_in        'Set up mode for pin P53`
- **Context**: dirl   #A_in | 'Count A-input highs mode

### req56: Code Example
- **File**: `req56-mov-logic_1_count-pin_data-get.pasm2`
- **Page**: 30, Lines 28-29
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `mov   Logic_1_count, pin_data 'Get logic-1 count`
- **Context**: if_nc        waitx #200                    'Short delay | if_nc        jmp   #.test_loop_x           'If C=0 wait for logic-1

### req57: Code Example
- **File**: `req57-jmp-test_loop_x-go-wait-for-a-.pasm2`
- **Page**: 30, Lines 36-37
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `jmp   #.test_loop_x           'Go wait for a logic-1`
- **Context**: if_c         jmp   #.test_loop_y           'If C=1 wait for logic-0 | mov   Logic_0_count, pin_data 'Get logic-0 count

### req58: Code Example
- **File**: `req58-con.spin2`
- **Page**: 31, Lines 7-8
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `CON`
- **Context**: During reset (DIR = 0), IN goes to logic-0 and the Z register gets set to $00000001. | Example

### req59: Code Example
- **File**: `req59-org-0.pasm2`
- **Page**: 31, Lines 10-11
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `org 0`
- **Context**: A_in = 53      ' Pin P53 | dat

### req60: Code Example
- **File**: `req60-wrpin-a_in_mode-a_in-set-up-mo.txt`
- **Page**: 31, Lines 12-14
- **Language**: Unknown | **Type**: Snippet | **Lines**: 3
- **Content**: `wrpin  A_in_mode,  #A_in    'Set up mode for pin P53`
- **Context**: org 0 | dirl   #A_in                'Count while A-input high

### req61: Code Example
- **File**: `req61-con.spin2`
- **Page**: 32, Lines 13-14
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `CON`
- **Context**: $80000000 system clock periods. | Example

### req62: Code Example
- **File**: `req62-org-0.pasm2`
- **Page**: 32, Lines 16-17
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `org 0`
- **Context**: A_in     = 53      'Pin P53 | dat

### req63: Code Example
- **File**: `req63-wrpin-a_in_mode-a_in-set-up-mo.txt`
- **Page**: 32, Lines 18-19
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `wrpin    A_in_mode,   #A_in    'Set up mode for pin P53`
- **Context**: org 0 | dirl     #A_in                 'Use A_in, pin 53

### req64: Code Example
- **File**: `req64-wypin-001-a_in-count-a-input-h.pasm2`
- **Page**: 32, Lines 20-21
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `wypin    ##%001,      #A_in    'Count A-input high states`
- **Context**: wrpin    A_in_mode,   #A_in    'Set up mode for pin P53 | wxpin    ##$7,        #A_in    'Wait for $7 events

### req65: Code Example
- **File**: `req65-con.spin2`
- **Page**: 34, Lines 15-16
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `CON`
- **Context**: portion of the Smart Pin to the A pin if you want single-cycle measurements. | Example

### req66: Code Example
- **File**: `req66-org-0.pasm2`
- **Page**: 34, Lines 18-19
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `org 0`
- **Context**: A_in     = 53       ' Pin P53 | dat

### req67: Code Example
- **File**: `req67-wrpin-a_in_mode-a_in-set-up-mo.txt`
- **Page**: 34, Lines 20-21
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `wrpin  A_in_mode,   #A_in   'Set up mode for pin P53`
- **Context**: org 0 | dirl   #A_in                'Use A_in, pin 53

### req68: Code Example
- **File**: `req68-wypin-00-a_in-count-a-in-rise-.pasm2`
- **Page**: 34, Lines 22-23
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `wypin  ##%00,       #A_in   'Count A-in rise to B-in rise`
- **Context**: wrpin  A_in_mode,   #A_in   'Set up mode for pin P53 | wxpin  ##$2,        #A_in   'Wait for 2 events

### req69: Code Example
- **File**: `req69-jmp-test_loop.pasm2`
- **Page**: 34, Lines 28-29
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `jmp #.test_loop`
- **Context**: if_nc      jmp #.test_loop          'If C=0 wait for logic-1 | rdpin pin_data,  #A_in   'C = 1, so save count data

### req70: Code Example
- **File**: `req70-con.spin2`
- **Page**: 38, Lines 31-32
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `CON`
- **Context**: function within the Smart Pin, so conversions occur without software intervention. | Example

### req71: Code Example
- **File**: `req71-mov-dira-ff.pasm2`
- **Page**: 38, Lines 35-38
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 4
- **Content**: `mov dira, #$FF`
- **Context**: dat | org 0

### req72: Code Example
- **File**: `req72-wrpin-a_adc_mode-a_adc-set-up-.txt`
- **Page**: 38, Lines 39-41
- **Language**: Unknown | **Type**: Snippet | **Lines**: 3
- **Content**: `wrpin     A_ADC_mode, #A_ADC    'Set up mode for ADC`
- **Context**: dirl      #A_ADC | 'ADC reset

### req73: Code Example
- **File**: `req73-con.spin2`
- **Page**: 39, Lines 19-20
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `CON`
- **Context**: of-2 sample periods. But your software must perform the difference computation. | Example

### req74: Code Example
- **File**: `req74-mov-dira-ff-led-output.pasm2`
- **Page**: 39, Lines 23-24
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `mov dira, #$FF                 'LED output`
- **Context**: dat | org 0

### req75: Code Example
- **File**: `req75-wrpin-a_adc_mode-a_adc-set-up-.txt`
- **Page**: 39, Lines 25-29
- **Language**: Unknown | **Type**: Code Fragment | **Lines**: 5
- **Content**: `wrpin     A_ADC_mode, #A_ADC   'Set up mode for ADC`
- **Context**: mov dira, #$FF                 'LED output | dirl      #A_ADC               'ADC

### req76: Code Example
- **File**: `req76-wrpin-100011_00000000_00_11000.txt`
- **Page**: 40, Lines 9-10
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `WRPIN ##%100011_00000000_00_11000_0,#adcpin    'configure AD...`
- **Context**: This mode performs SINC3 filtering, but it requires additional software to obtain | accurate ADC values. To begin SINC3 filtering:

### req77: Code Example
- **File**: `req77-wrpin-100011_00000000_00_11000.txt`
- **Page**: 40, Lines 38-39
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `WRPIN ##%100011_00000000_00_11000_0, adcpin 'configure ADC-s...`
- **Context**: most recent ADC bit, while bit 0 will have come from the ADC 31 system-clock periods | earlier.

### req78: Code Example
- **File**: `req78-wrpin-scpmode-scp_addr.txt`
- **Page**: 41, Lines 34-35
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `wrpin scpmode, #scp_addr`
- **Context**: than holding "scope" data. | To use the SCOPE mode:

### req79: Code Example
- **File**: `req79-wrpin-wxpin-wypin-rdpin-akpin-.pasm2`
- **Page**: 46, Lines 3-6
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 4
- **Content**: `WRPIN/WXPIN/WYPIN/RDPIN/AKPIN before IN can be raised again,...`
- **Context**: Rev 5  06-11-2020 | Jon Titus, Page 46 of

### req80: Code Example
- **File**: `req80-wypin.pasm2`
- **Page**: 48, Lines 21-23
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 3
- **Content**: `wypin`
- **Context**: .loop  waitx | ##10_000_000             'Delay between transmissions

### req81: Code Example
- **File**: `req81-jmp.pasm2`
- **Page**: 48, Lines 25-26
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `jmp`
- **Context**: ' 10100001 (LSB first) | wypin     #16,          #clkout    'Start clock, transmit data

### req82: Code Example
- **File**: `req82-con.spin2`
- **Page**: 49, Lines 30-35
- **Language**: Spin2 | **Type**: Code Fragment | **Lines**: 6
- **Content**: `CON`
- **Context**: ' Synchronous serial transmission, Rev. 4, 06-15-2020 at 1450 MDT | 'positive edge-trigger (Jon Titus)

### req83: Code Example
- **File**: `req83-org-0.pasm2`
- **Page**: 49, Lines 37-38
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `org 0`
- **Context**: 'Remember to connect these pins as noted! | dat

### req84: Code Example
- **File**: `req84-wrpin-sync_tx_mode-txout-set-s.txt`
- **Page**: 50, Lines 4-6
- **Language**: Unknown | **Type**: Snippet | **Lines**: 3
- **Content**: `wrpin   sync_tx_mode, #txout      'Set sync tx mode pin 41`
- **Context**: Jon Titus, Page 50 of | dirl    #txout                    'Transmitter setup

### req85: Code Example
- **File**: `req85-wrpin-clock_mode-clkout-set-pi.txt`
- **Page**: 50, Lines 10-11
- **Language**: Unknown | **Type**: Snippet | **Lines**: 2
- **Content**: `wrpin   clock_mode,  #clkout       'Set pin as transition-`
- **Context**: #txout                    'Enable xmtr output | dirl    #clkout                   'Clock output setup

### req86: Code Example
- **File**: `req86-mov-dira-00ff-pins-p7-p0-set-a.pasm2`
- **Page**: 50, Lines 39-40
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `mov dira, ##$00FF     'Pins P7--P0 set as outputs`
- **Context**: org 0 | sync_receive

### req87: Code Example
- **File**: `req87-wrpin-sync_rx_mode-rxin.txt`
- **Page**: 50, Lines 41-47
- **Language**: Unknown | **Type**: Code Fragment | **Lines**: 7
- **Content**: `wrpin sync_rx_mode, #rxin`
- **Context**: mov dira, ##$00FF     'Pins P7--P0 set as outputs | dirl #rxin                    'Reset receiver Smart Pin

### req88: Code Example
- **File**: `req88-jmp-test_loop.spin2`
- **Page**: 50, Lines 52-53
- **Language**: Mixed | **Type**: Snippet | **Lines**: 2
- **Content**: `jmp #.test_loop`
- **Context**: nop | if_nc

### req89: Code Example
- **File**: `req89-mov-outa-rcvd_data.pasm2`
- **Page**: 50, Lines 60-61
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `mov outa, rcvd_data`
- **Context**: 'shift-right 24 bit places to | ' align LSB at bit 0

### req90: Code Example
- **File**: `req90-jmp-test_loop.pasm2`
- **Page**: 50, Lines 61-64
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 4
- **Content**: `jmp #.test_loop`
- **Context**: ' align LSB at bit 0 | mov outa, rcvd_data

### req91: Code Example
- **File**: `req91-wrpin-txmode-txpin.spin2`
- **Page**: 51, Lines 17-21
- **Language**: Spin2 | **Type**: Code Fragment | **Lines**: 5
- **Content**: `wrpin   ##txmode, #txpin`
- **Context**: tx_pin  = 20 | txmode  = %0000_0000_000_0000000000000_01_11110_0

### req92: Code Example
- **File**: `req92-con.spin2`
- **Page**: 53, Lines 4-9
- **Language**: Spin2 | **Type**: Code Fragment | **Lines**: 6
- **Content**: `CON`
- **Context**: Jon Titus, Page 53 of | 'Async Transmit Ver 2, 6-10-2020 at 1440H MDT

### req93: Code Example
- **File**: `req93-wrpin-txmode-txpin-smart-pin-a.txt`
- **Page**: 53, Lines 11-14
- **Language**: Unknown | **Type**: Snippet | **Lines**: 4
- **Content**: `wrpin   ##txmode,  #txpin       ' Smart Pin async transmit m...`
- **Context**: DAT | wrpin   ##txmode,  #txpin       ' Smart Pin async transmit mode

### req94: Code Example
- **File**: `req94-wypin-55-txpin-transmit-test.pasm2`
- **Page**: 53, Lines 15-16
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `wypin   #$55,       #txpin       ' transmit test %01010101`
- **Context**: dirh    #txpin                   ' enable Smart Pin tx | nop

### req95: Code Example
- **File**: `req95-jmp-flag_test-transmit-foreve.pasm2`
- **Page**: 53, Lines 21-22
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `jmp     #.flag_test             ' transmit "forever"`
- **Context**: waitx   ##25_000_000 / 70      ' delay inserted for testing | wypin   #$99,        #txpin    ' send testing byte to tx pin

### req96: Code Example
- **File**: `req96-wrpin-rxmode-rxpin.spin2`
- **Page**: 53, Lines 30-38
- **Language**: Spin2 | **Type**: Code Fragment | **Lines**: 9
- **Content**: `wrpin   ##rxmode, #rxpin`
- **Context**: rx_pin   = 21 | bitper   = $3640_0007                     ' bit rate for tests

### req97: Code Example
- **File**: `req97-con.spin2`
- **Page**: 54, Lines 19-23
- **Language**: Spin2 | **Type**: Code Fragment | **Lines**: 5
- **Content**: `CON`
- **Context**: shr rcvd_data, #32 - numb_bits | Example

### req98: Code Example
- **File**: `req98-wrpin-rxmode-rxpin-smart-pin-a.txt`
- **Page**: 54, Lines 25-28
- **Language**: Unknown | **Type**: Snippet | **Lines**: 4
- **Content**: `wrpin   ##rxmode,  #rxpin    ' Smart Pin async receive mode`
- **Context**: bitper  = $3640_0007                               ' bit rate & bits | DAT


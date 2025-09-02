# Titus File to Smart Pin Mode Mapping

**Purpose**: Map available Titus PASM2 examples to Smart Pin modes needing coverage

## Modes Needing PASM2 Examples

### HIGH PRIORITY - Completely Missing PASM2

#### Mode %00000 - Smart Pin OFF
**Current**: 1 Spin2, 0 PASM2
**Available Titus Files**: None specific (may need simple example)
**Action**: Create simple DIRH/DIRL example

#### Mode %00110 - NCO Duty  
**Current**: 1 Spin2, 0 PASM2
**Available Titus Files**:
- req27-wrpin-nco_config-20-set-config.txt
- req29-wrpin-nco_config-20-set-config.txt
**Action**: Use req27 or req29

#### Mode %01100 - Count Rises
**Current**: 2 Spin2, 0 PASM2
**Available Titus Files**:
- req50-wrpin-a_in_mode-a_in-set-up-mo.txt
- req51-wypin-0-a_in-count-only-a-inpu.pasm2
**Action**: Use req50/51 pair

#### Mode %01101 - A-B Encoder (Inc/Dec)
**Current**: 1 Spin2, 0 PASM2
**Available Titus Files**:
- req34-wrpin-quadenc_config-32-set-fo.txt
- req39-wrpin-quadenc_config-32-set-fo.txt
**Action**: Use req34 or req39

#### Mode %01110 - Incremental Encoder
**Current**: 1 Spin2, 0 PASM2
**Available Titus Files**:
- req40-sar-quadenc_data-2-arithmetic-.txt
- req41-mov-outa-quadenc_data.pasm2
**Action**: Use req40/41 pair

#### Mode %01111 - Local/Global Comparator
**Current**: 4 Spin2, 0 PASM2
**Available Titus Files**:
- req55-wrpin-a_in_mode-a_in-set-up-mo.txt
- req60-wrpin-a_in_mode-a_in-set-up-mo.txt
- req63-wrpin-a_in_mode-a_in-set-up-mo.txt
- req67-wrpin-a_in_mode-a_in-set-up-mo.txt
**Action**: Use multiple examples for different comparator configs

#### Mode %11000/%11001 - USB Host/Device
**Current**: 1 Spin2, 0 PASM2
**Available Titus Files**: None specific
**Action**: May need to create or find elsewhere

#### Mode %11111 - ADC Input (CRITICAL - 29 Spin2!)
**Current**: 29 Spin2, 0 PASM2
**Available Titus Files**:
- req72-wrpin-a_adc_mode-a_adc-set-up-.txt
- req75-wrpin-a_adc_mode-a_adc-set-up-.txt
**Action**: Use both, need more examples for various ADC configs

### MEDIUM PRIORITY - Heavily Imbalanced

#### Mode %00010/%00011 - DAC Output
**Current**: 30 Spin2, 2 PASM2
**Available Titus Files**:
- req08-wrpin-dacconfig-20.txt
- req10-wrpin-dacconfig-20-set-dac-con.txt
- req11-wypin-dacvolt-20-load-dac.pasm2
- req13-wrpin-dacconfig-20-set-configu.txt
- req14-wypin-dacvolt2-20.pasm2
**Action**: Add req11 and req14 (both .pasm2)

#### Mode %11011 - Synchronous Serial Transmit
**Current**: 3 Spin2, 1 PASM2
**Available Titus Files**:
- req48-wrpin-sync_tx_mode-txout-set-s.txt
- req84-wrpin-sync_tx_mode-txout-set-s.txt
- req87-wrpin-sync_rx_mode-rxin.txt
**Action**: Add req84 and req87

### LOW PRIORITY - Minor Imbalance

#### Mode %00001 - Repository Mode
**Current**: 3 Spin2, 2 PASM2
**Action**: Already fairly balanced

#### Mode %00101 - NCO Frequency
**Current**: 2 Spin2, 1 PASM2
**Available Titus Files**:
- req23-wrpin-nco_config-20.txt
**Action**: Add req23 if needed

#### Mode %01011 - Quadrature Encoder
**Current**: 2 Spin2, 1 PASM2
**Available Titus Files**:
- req36-sar-quadenc_data-2-arithmetic-.txt
- req41-mov-outa-quadenc_data.pasm2
**Action**: Add req41 for balance

## Summary of Required Actions

### Must Add (0 PASM2 currently):
1. **Mode %00110** - Use NCO duty files
2. **Mode %01100** - Use count files
3. **Mode %01101** - Use encoder files
4. **Mode %01110** - Use incremental encoder files
5. **Mode %01111** - Use comparator files (multiple)
6. **Mode %11111** - Use ADC files (critical - needs many)

### Should Add (heavily imbalanced):
1. **Mode %00010/%00011** - Add more DAC examples
2. **Mode %11011** - Add sync serial examples

### Total Files to Insert:
- Minimum: ~15-20 PASM2 examples for missing modes
- Ideal: ~30-40 PASM2 examples for better balance
- Available: 47 PASM2 files from Titus

## Next Steps:
1. Extract content from identified files
2. Insert after corresponding Spin2 examples
3. Ensure blank lines for proper formatting
4. Compile test with pnut_ts
5. Create V5 document
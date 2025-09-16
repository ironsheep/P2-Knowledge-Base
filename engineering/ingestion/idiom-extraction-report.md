# P2 Idiom Extraction Report
*Analyzed 730 source files*

## Spin2 Idioms (Top 20 by frequency)

### memory_address_of: 16845 occurrences
  - `@gmail`
  - `@started`
  - `@buffer`

### memory_long_array_access: 1667 occurrences
  - `LONG[@rxHeadIdx][portHandle]`
  - `LONG[@txHeadIdx][portHandle]`
  - `LONG[@rxTailIdx][portHandle]`

### cog_cog_id: 1252 occurrences
  - `cogid()`
  - `cogid()`
  - `cogid()`

### loop_repeat_for: 1117 occurrences
  - `repeat i from 0 to BUF_SIZE`
  - `repeat i from 0 to 15`
  - `repeat ch from 0 to 5`

### bit_bit_mask_hex: 988 occurrences
  - `r5 & $0F`
  - `r5 & $F0`
  - `128 & $FF`

### loop_repeat_forever: 908 occurrences
  - `repeat
`
  - `repeat
`
  - `repeat
`

### loop_repeat_while: 673 occurrences
  - `repeat while (c := byte[x++]) <> 0`
  - `repeat while (rxtail == rxhead)                               ' hold while buffer empty`
  - `repeat while (rxcheck() >= 0)`

### pin_timing_delay_ms: 661 occurrences
  - `waitms(1)`
  - `waitms(1)`
  - `waitms(10)`

### memory_byte_array_access: 406 occurrences
  - `BYTE[@rxbuf][portHandle * BUF_SIZE]`
  - `BYTE[@txbuf][portHandle * BUF_SIZE]`
  - `BYTE[@strBuffer][nPortHandle * BUF_SIZE]`

### loop_repeat_until: 249 occurrences
  - `repeat
  until (pinread(rxp))`
  - `repeat until ((b := rxcheck()) >= 0) || (((getct()-t) / mstix) >= ms)`
  - `repeat until ((b := rxcheck()) >= 0) || ((getct()-t) >= tix)`

### loop_repeat_count: 202 occurrences
  - `repeat 10`
  - `repeat 10`
  - `repeat 12`

### pin_pin_low: 133 occurrences
  - `pinlow(TEST_PIN_SNS_LOOP)`
  - `pinlow(TEST_PIN_SNS_LP_ACTV)`
  - `pinlow(apin)`

### pin_pin_high: 116 occurrences
  - `PINHIGH(MTX_LED_PIN_OE)`
  - `PINHIGH(MTX_LED_PIN_OE)`
  - `PINHIGH(MTX_COLOR_PINS)`

### cog_cog_stop: 102 occurrences
  - `cogstop(cog-1)`
  - `cogstop(cog-1)`
  - `cogstop(cog-1)`

### pin_smart_pin_start: 99 occurrences
  - `pinstart(rxp, p_async_rx, bitmode, 0)`
  - `pinstart(rxp, spmode, baudcfg, 0)`
  - `pinstart(txp, spmode, baudcfg, 0)`

### cog_cog_init: 91 occurrences
  - `coginit(COGEXEC_NEW, @uart_mgr, @rxp)`
  - `coginit(COGEXEC_NEW, @uart_mgr, @rxp)`
  - `coginit(cogexec_new, @uart_mgr, @rxp)`

### pin_timing_wait_clock: 87 occurrences
  - `waitct(t += (100 * MS_001)`
  - `waitct(0)`
  - `waitct(getct()`

### pin_timing_delay_us: 82 occurrences
  - `waitus(1)`
  - `waitus(1)`
  - `waitus(1)`

### memory_word_array_access: 57 occurrences
  - `word[@mask_info][mask_number]`
  - `word[@hidpad_report+dev*HIDPAD_REPORT_SIZE][4+axnum]`
  - `word[@hidpad_report+dev*HIDPAD_REPORT_SIZE][4+axnum]`

### pin_pin_float: 48 occurrences
  - `pinfloat(apin)`
  - `pinfloat(apin)`
  - `pinfloat(pin_rst)`


## PASM2 Idioms (Top 20 by frequency)

### register_move: 1774 occurrences
  - `mov	char_cnt, text_cols`
  - `mov	strikethru_line, font_height`
  - `mov	stride, text_cols`

### conditional_z: 641 occurrences
  - `if_z	shl`
  - `if_z	or`
  - `if_z	mov`

### conditional_nz: 621 occurrences
  - `if_nz mov`
  - `if_nz or`
  - `if_nz or`

### register_add: 495 occurrences
  - `add sine_phase,sine_freq`
  - `add toggle_phase,toggle_freq`
  - `add sample,centerfreq`

### conditional_c: 476 occurrences
  - `if_c  add`
  - `if_c  sub`
  - `if_c  sumz`

### conditional_nc: 342 occurrences
  - `if_nc jmp`
  - `if_nc add`
  - `if_nc sub`

### hub_read_long: 215 occurrences
  - `rdlong	basepin_val, ptra`
  - `rdlong  buffer_base, ptra`
  - `rdlong  text_cols, ptra`

### register_or: 192 occurrences
  - `or 	dacmode_s, mycogid`
  - `or	dacmode_c, mycogid`
  - `or	curchar, mask_ffff`

### register_sub: 186 occurrences
  - `sub       fSum,nVel`
  - `sub       nVel,oPos`
  - `sub       nVel,cor`

### loop_instruction: 166 occurrences
  - `sample_cy
loop`
  - `Field loop`
  - `main loop`

### hub_write_long: 140 occurrences
  - `wrlong	pb, ptra`
  - `wrlong    timeCnt,adrTime`
  - `wrlong    nVel,ptrb`

### rep_loop: 109 occurrences
  - `data5                       rep     #5, #80`
  - `addresses 
                            rep     #2, #8`
  - `instructions
                            rep     #2, #2`

### wait_cycles: 44 occurrences
  - `waitx   c`
  - `waitx   c`
  - `waitx   c`

### register_and: 42 occurrences
  - `and	line_effects, field_effects`
  - `and 32,33`
  - `and	cureff, line_effects`

### djnz_loop: 39 occurrences
  - `loop
	djnz	y, #line`
  - `_ret_   djnz    y,#blank`
  - `pinlooptest
                            djnz    a, #pinloop`

### register_xor: 36 occurrences
  - `xor curchar, mask_ffff`
  - `xor curchar, mask_ffff`
  - `xor curchar, mask_ffff`

### pin_drive_low: 4 occurrences
  - `drvl #56`
  - `drvl #56`
  - `drvl #56`

### hub_read_byte: 1 occurrences
  - `rdbyte PR0, PR3`

### hub_write_byte: 1 occurrences
  - `wrbyte PR0, PR3`

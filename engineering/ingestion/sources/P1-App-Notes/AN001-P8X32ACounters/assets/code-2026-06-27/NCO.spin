''Demonstration of NCO counter mode (%00100)
CON
        _clkmode        = xtal1 + pll16x
        _xinfreq        = 5_000_000

PUB NCO_PWM_single_ended_mode
'             mode  PLL        BPIN     APIN
  ctra    := %00100_000 << 23 + 1 << 9 + 0  'Establish mode and APIN (BPIN is ignored)
  frqa    := $8000_0000                     'Set FRQA so PHS[31] toggles every clock
  dira[0] := 1                              'Set APIN to output
  repeat                                    'infinite loop, so counter continues to run
  
''Demonstration of PWM version of NCO/PWM counter mode
CON _clkmode = xtal1 + pll16x
    _xinfreq = 5_000_000

VAR long parameter

PUB go | x
  cognew(@entry, @parameter)
  repeat
    repeat x from 0 to period 'linearly advance parameter from 0 to 100
      parameter := x          'a constant here locks to value x percent high
      waitcnt(1_000_000 + cnt)   'wait a little while before next update

DAT
'assembly cog which updates the PWM cycle on APIN
'for audio PWM, fundamental freq which must be out of auditory range (period < 50µS)
        org

entry   mov dira, diraval              'set APIN to output
        mov ctra, ctraval              'establish counter A mode and APIN
        mov frqa, #1                   'set counter to increment 1 each cycle

        mov time, cnt                  'record current time
        add time, period               'establish next period

:loop   rdlong value, par              'get an up to date pulse width
        waitcnt time, period           'wait until next period
        neg phsa, value                'back up phsa so that it
        jmp #:loop                     'loop for next cycle

diraval long |< 0                      'APIN=0
ctraval long %00100 << 26 + 0          'NCO/PWM APIN=0
period  long 100                       '800kHz (1.25µS period) (_clkfreq / period)                      
time    res 1
value   res 1


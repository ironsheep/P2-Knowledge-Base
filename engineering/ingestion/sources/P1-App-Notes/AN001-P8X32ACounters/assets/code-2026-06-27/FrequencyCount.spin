''Demonstration of the counter used as a frequency counter
CON 
        _clkmode = xtal1 + pll16x
        _XinFREQ = 5_000_000
OBJ
        txt : "VGA_Text"
VAR
        long ctr, frq

PUB Go | freq
        txt.start(16)
        cognew(@entry, @freq)
        
        repeat
          txt.out($00)                  'clear the screen
          txt.dec(freq)                 'display the value (in Hz)                  

DAT
        org

entry   mov     ctra, ctra_             'establish mode and start counter
        mov     frqa, #1                'increment for each edge seen
        mov     cnt_, cnt               'setup time delay
        add     cnt_, cntadd

:loop   waitcnt cnt_, cntadd            'wait for next sample
        mov     new, phsa               'record new count
        mov     temp, new               'make second copy
        sub     new, old                'get delta
        mov     old, temp               'set next delta's base

        wrlong  new, par
        jmp     #:loop

ctra_   long    %01010 << 26 + 7        'mode + APIN
cntadd  long    80_000_000              'wait 1 second, answer in Hz 

cnt_    res     1
new     res     1
old     res     1
temp    res     1
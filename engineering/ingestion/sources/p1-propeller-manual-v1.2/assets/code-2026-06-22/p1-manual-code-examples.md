# P1 Propeller Manual v1.2 — Extracted Code Examples (Pass 2)

Anchored on the manual's Example/For-example markers; pdf-layout indent-preserving extraction.
Page = printed = PDF page. **All `code_validated: false` — flexspin deferred (charter §3).**
Spin1 and PASM1 mixed (DAT/ORG blocks are PASM1). Heuristic boundaries — verify before promotion.


### p52
```spin1
VAR
  byte     Temp                        'Temp is a byte
  byte     Str[25]                     'Str is a byte array
```

### p53
```spin1
DAT
  MyData           byte     64, $AA, 55           'Byte-aligned and byte-sized data
  MyString         byte     "Hello",0             'A string of bytes (characters)
```

### p53
```spin1
DAT
  MyData        byte 64. $AA[8], 55
```

### p55
```spin1
VAR
  word    WordVar
  long    LongVar

PUB Main
  WordVar.byte := 0                    'Set first byte of WordVar to 0
  WordVar.byte[0] := 0                 'Same as above
  WordVar.byte[1] := 100               'Set second byte of WordVar to 100
  LongVar.byte := 25                   'Set first byte of LongVar to 25
  LongVar.byte[0] := 25                'Same as above
  LongVar.byte[1] := 50                'Set second byte of LongVar to 50
```

### p57
```spin1
VAR
  byte          Buff[100]

PUB Main
  bytefill(@Buff, 0, 100)                'Clear Buff to 0
```

### p58
```spin1
VAR
  byte          Buff1[100]
  byte          Buff2[100]

PUB Main
  bytemove(@Buff2, @Buff1, 100)                 'Copy Buff1 to Buff2
```

### p60
```spin1
  case X+Y                               'Test X+Y
    10, 15: !outa[0]                     'X+Y = 10 or 15? Toggle P0
    A*2    : !outa[1]                    'X+Y = A*2? Toggle P1
    30..40: !outa[2]                     'X+Y in 30 to 40? Toggle P2
  X += 5                                 'Add 5 to X
```

### p60
```spin1
  case X+Y                               'Test X+Y
    10, 15: !outa[0]                     'X+Y = 10 or 15? Toggle P0
    25     : !outa[1]                    'X+Y = 25? Toggle P1
    20..30: !outa[2]                     'X+Y in 20 to 30? Toggle P2
    OTHER : !outa[3]                     'Otherwise toggle P3
  X += 5                                 'Add 5 to X
```

### p65
```spin1
CON
  _CLKMODE = XTAL1 + PLL8X
  _CLKFREQ = 32_000_000
```

### p69
```spin1
CON
  _CLKMODE = RCFAST
```

### p70
```spin1
CON
  _CLKMODE = XTAL1
```

### p75
```spin1
PUB StopMyself
  'Stop cog this code is running in
  cogstop(cogid)
```

### p79
```spin1
VAR
  long SqStack[6]                             'Stack space for Square cog
```

### p81
```spin1
PUB Main
  cognew(@Toggle, 0)                                         'Launch Toggle code

DAT
                        org 0                                'Reset assembly pointer
```

### p83
```spin1
VAR
  byte Cog          'Used to store ID of newly started cog
```

### p85
```spin1
CON
  Delay = 500
  Baud = 9600
  AChar = "A"
```

### p87
```spin1
CON
  'Declare modes of operation
  RunTest    = 0
  RunVerbose = 1
  RunBrief   = 2
  RunFull    = 3
```

### p90
```spin1
OBJ
  Num : "Numbers"

PUB SomeRoutine
  Format := Num#DEC               'Set Format to Number's Decimal constant
```

### p100
```spin1
DAT
  byte 64, "A", "String", 0
  word $FFC2, 75000
  long $44332211, 32
```

### p101
```spin1
DAT
  byte $FFAA, $BB995511
```

### p101
```spin1
DAT
  MyData        byte $FF, 25, %1010

PUB GetData | Temp
  Temp := MyData[0]                         'Get first byte of data table
```

### p102
```spin1
DAT
  MyData        byte $FF, 25, %1010

PUB GetData | Temp
  Temp := BYTE[@MyData][0]                  'Get first byte of data table
```

### p102
```spin1
DAT
  MyData           byte    64, $AA[8], 55
```

### p102
```spin1
DAT
                         org 0                                'Reset assembly pointer
```

### p107
```spin1
PUB GetData | Index, Temp
  Index := 0
  repeat
    Temp := byte[Data][Index++] 'Read data into Temp 1 byte at a time
    <do something with Temp>    'Perform task with value in Temp
  while Temp > 0                'Loop until end found
```

### p108
```spin1
  CON
    OneHalf = 0.5
    Ratio   = 2.0 / 5.0
    Miles   = 10e5
```

### p108
```spin1
  CON
    Two          = 2
```

### p110
```spin1
CON
  _FREE        = 1000
```

### p113
```spin1
  if X > 10                               'If X is greater than 10
    !outa[0]                              'Toggle P0
  !outa[1]                                'Toggle P1
```

### p113
```spin1
  if X > 10                               'If X is greater than 10
    !outa[0]                              'Toggle P0
    !outa[1]                              'Toggle P1
  waitcnt(2_000 + cnt)                    'Wait for 2,000 cycles
```

### p114
```spin1
  if X > 100                             'If X is greater than 100
    !outa[0]                             'Toggle P0
  elseif X == 90                         'Else If X = 90
```

### p116
```spin1
  if X > 100                             'If X is greater than 100
    !outa[0]                             'Toggle P0
  elseif X == 90                         'Else If X = 90
    !outa[1]                             'Toggle P1
  elseif X > 50                          'Else If X > 50
    !outa[2]                             'Toggle P2
  else                                   'Otherwise,
    !outa[3]                             'Toggle P3
```

### p123
```spin1
VAR
  byte SemID

PUB SetupSharedResource
```

### p129
```spin1
VAR
  long    Temp                         'Temp is a long (2 words, 4 bytes)
  long    List[25]                     'List is a long array
```

### p129
```spin1
DAT
  MyData     long    640_000, $BB50                        'Long-aligned/sized data
  MyList     byte    long $FF995544, long 1_000            'Byte-aligned/long-sized
```

### p130
```spin1
DAT
  MyData           long     640_000, $BB50[3]
```

### p134
```spin1
VAR
  long          Buff[100]

PUB Main
  longfill(@Buff, 0, 100)                'Clear Buff to 0
```

### p135
```spin1
VAR
  long          Buff1[100]
  long          Buff2[100]

PUB Main
  longmove(@Buff2, @Buff1, 100)                 'Copy Buff1 to Buff2
```

### p141
```spin1
OBJ
  Num : "Numbers"
  Term : "TV_Terminal"
```

### p141
```spin1
PUB Print | S
  S := Num.ToStr(LongVal, Num#DEC)
  Term.Str(@S)
```

### p142
```spin1
OBJ
  PWM[2] : "PWM"
PUB GenPWM
  PWM[0].Start
  PWM[1].Start
```

### p148
```spin1
CON
  OneHalf = 0.5
  Ratio   = 2.0 / 5.0
  Miles   = 10e5
```

### p176
```spin1
  DIRA := %00000100_00110000_00000001_11110000
  OUTA := %01000100_00110000_00000001_10010000
```

### p176
```spin1
  DIRA[10]~~                              'Set P10 to output
  OUTA[10]~                               'Make P10 low
  OUTA[10]~~                              'Make P10 high
```

### p178
```spin1
VAR
  long          Shared                               'Shared variable (Spin & Assy)

PUB Main | Temp
  cognew(@Process, @Shared)                          'Launch assy, pass Shared addr
  repeat
    <do something with Shared vars>

DAT
                          org 0
```

### p183
```spin1
PUB Init
  <initialization code>

PUB MotorPos : Position
  Position := <code to retrieve motor position>

PUB MoveMotor(Position, Speed) : Success | PosIndex
```

### p189
```spin1
  repeat                               'Repeat endlessly
    !outa[25]                          'Toggle P25
    waitcnt(2_000 + cnt)               'Pause for 2,000 cycles
```

### p189
```spin1
  repeat                               'Repeat endlessly
  !outa[25]                            'Toggle P25       <-- This is never run
```

### p190
```spin1
  repeat 10                            'Repeat 10 times
    !outa[25]                          'Toggle P25
  byte[$7000]++                        'Increment RAM location $7000
```

### p193
```spin1
  X := 0
  repeat
    byte[$7000][X] := 0                 'Increment RAM value
    X++                                 'Increment X
  while X < 10                          'Repeat while X is less than 10
```

### p194
```spin1
PUB GetChar : Char
  <do something>
  Char := <retrieved character>                'Set Char (result) to the character
```

### p198
```spin1
  CON
    OneHalf = 0.5
    Smaller = 0.4999
    Rnd1    = round(OneHalf)
    Rnd2    = round(Smaller)
    Rnd3    = round(Smaller * 10.0) + 4
```

### p202
```spin1
        CON
          _STACK        = 3000
```

### p203
```spin1
PUB Main
  if strcomp(@Str1, @Str2)
```

### p206
```spin1
PUB Main
  Print(strsize(@Str1))
  Print(strsize(@Str2))

DAT
  Str1      byte    "Hello World", 0
  Str2      byte    "Testing.", 0
```

### p209
```spin1
  CON
    OneHalf = 0.5
    Bigger = 1.4999
    Int1    = trunc(OneHalf)
    Int2    = trunc(Bigger)
    Int3    = trunc(Bigger * 10.0) + 4
```

### p218
```spin1
CON
  _clkmode = xtal1                           'Set for slow crystal
  _xinfreq = 5_000_000                       'Use 5 MHz accurate crystal

    repeat
     !outa[0]                                'Toggle pin 0
     waitcnt(50_000 + cnt)                   'Wait for 10 ms
```

### p220
```spin1
CON
  _clkfreq = xtal1                          'Set for slow crystal
  _xinfreq = 5_000_000                      'Use 5 MHz accurate crystal

PUB Toggle | Time
  Time := cnt                               'Get current system counter value
  repeat
    waitcnt(Time += 50_000)                 'Wait for 10 ms
    !outa[0]                                'Toggle pin 0
```

### p222
```spin1
   waitpeq(%0100, %1100, 0)                 'Wait for P3 & P2 to be low & high
   outa[0] := 1                             'Set P0 high
```

### p224
```spin1
   waitpeq(%0100, %1100, 0) 'Wait for P3 & P2 to be low & high
   waitpne(%0100, %1100, 0) 'Wait for P3 & P2 to not match prev. state
   outa[0] := 1             'Set P0 high
```

### p228
```spin1
VAR
  word    Temp                         'Temp is a word (2 bytes)
  word    List[25]                     'List is a word array
```

### p229
```spin1
DAT
  MyData     word     640, $AAAA, 5_500                'Word-aligned/word-sized data
  MyList     byte     word $FF99, word 1_000           'Byte-aligned/word-sized data
```

### p229
```spin1
DAT
  MyData           word    640, $AAAA[4], 5_500
```

### p233
```spin1
VAR
  long    LongVar

PUB Main
  LongVar.word := 65000                'Set first word of LongVar to 65000
  LongVar.word[0] := 65000             'Same as above
  LongVar.word[1] := 1                 'Set second word of LongVar to 1
```

### p234
```spin1
VAR
  word          Buff[100]

PUB Main
  wordfill(@Buff, 0, 100)                'Clear Buff to 0
```

### p235
```spin1
VAR
  word          Buff1[100]
  word          Buff2[100]

PUB Main
  wordmove(@Buff2, @Buff1, 100)                 'Copy Buff1 to Buff2
```

### p236
```spin1
        CON
          _CLKMODE = XTAL1 + PLL8X
          _XINFREQ = 4_000_000
```

### p291
```spin1
                      and         temp1, #$20               wc
                      andn        temp2, #$38               wz, nr
     if_c_and_z       jmp         #MoreCode
```

### p292
```spin1
DAT
                      ORG       492
```

### p295
```spin1
                      test      _pins, #$20            wc
                      and       _pins, #$38
                      shl       t1, _pins
                      shr       _pins, #3
                      movd      vcfg, _pins
           if_nc      mov       dira, t1
           if_nc      mov       dirb, #0
           if_c       mov       dira, #0
           if_c       mov       dirb, t1
```

### p328
```spin1
DAT
                      org       0                 'Start at Cog RAM 0
```

### p339
```spin1
DAT
                     ORG     0
```

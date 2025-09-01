# Source Code Extraction Catalog - P2 Spin2 Documentation v51-250425
*Extracted: P2-Knowledge-Base on 2025-08-24*

## Summary
- **Total Code Examples**: 32
- **Source PDF**: P2 Spin2 Documentation v51-250425
- **Output Directory**: /Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/sources/extractions/spin2-v51-complete-extraction-audit/assets/code-20250824/

### By Language
- **Spin2**: 15 examples
- **PASM2**: 16 examples
- **Mixed**: 1 examples

### By Type
- **Snippet**: 31 examples
- **Complete Program**: 1 examples

---

## Code Examples

### req01: Code Example
- **File**: `req01-pub-minimalspin2program.spin2`
- **Page**: 7, Lines 44-46
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 3
- **Content**: `PUB MinimalSpin2Program()`
- **Context**: Spin2 | Program

### req02: Code Example
- **File**: `req02-dat.spin2`
- **Page**: 11, Lines 20-21
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `DAT`
- **Context**: DAT | Symbols and Data

### req03: Code Example
- **File**: `req03-jmp-loop.pasm2`
- **Page**: 11, Lines 94-95
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `JMP     #Loop`
- **Context**: AND     OUTA,#$FF | 'to Spin2 code,#IncPins is the cog address of the 'MOV' instruction

### req04: Code Example
- **File**: `req04-jmp.pasm2`
- **Page**: 11, Lines 96-97
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `JMP     #$`
- **Context**: JMP     #Loop | 'to PASM code,#Loop is the cog address ($001) of the 'ADD' instruction

### req05: Code Example
- **File**: `req05-org.pasm2`
- **Page**: 11, Lines 98-99
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `ORG`
- **Context**: JMP     #$ | '$ is the currentorigin, which steps by 1 with each cog-exec instruction

### req06: Code Example
- **File**: `req06-org-100.pasm2`
- **Page**: 11, Lines 100-101
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `ORG     $100`
- **Context**: ORG | 'set cog-execmode, cog address = $000, cog limit = $1F8 (reg, both defaults)

### req07: Code Example
- **File**: `req07-org-100-120.pasm2`
- **Page**: 11, Lines 102-103
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `ORG     $100,$120`
- **Context**: ORG     $100 | 'set cog-execmode, cog address = $100, cog limit = $1F8 (reg, default limit)

### req08: Code Example
- **File**: `req08-org-200.pasm2`
- **Page**: 11, Lines 104-105
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `ORG     $200`
- **Context**: ORG     $100,$120 | 'set cog-execmode, cog address = $100, cog limit = $120 (reg)

### req09: Code Example
- **File**: `req09-org-300-380.pasm2`
- **Page**: 11, Lines 106-107
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `ORG     $300,$380`
- **Context**: ORG     $200 | 'set cog-execmode, cog address = $200, cog limit = $400 (LUT, default limit)

### req10: Code Example
- **File**: `req10-add-register-1.pasm2`
- **Page**: 11, Lines 108-109
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `ADD     register,#1`
- **Context**: ORG     $300,$380 | 'set cog-execmode, cog address = $300, cog limit = $380 (LUT)

### req11: Code Example
- **File**: `req11-jmp-loop.pasm2`
- **Page**: 12, Lines 10-11
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `JMP     #Loop`
- **Context**: Loop            ADD     OUTA,#1 | 'In Spin2, @IncPinsis the hub address of the 'MOV' instruction

### req12: Code Example
- **File**: `req12-jmp.pasm2`
- **Page**: 12, Lines 12-13
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `JMP     #$`
- **Context**: JMP     #Loop | 'In PASM, Loopis the hub address ($00404) of the 'ADD' instruction

### req13: Code Example
- **File**: `req13-orgh.pasm2`
- **Page**: 12, Lines 14-15
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `ORGH`
- **Context**: JMP     #$ | '$ is the currentorigin, which steps by 4 with each hub-exec instruction

### req14: Code Example
- **File**: `req14-orgh-1000.pasm2`
- **Page**: 12, Lines 16-17
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `ORGH    $1000`
- **Context**: ORGH | 'set hub-execmode, hub origin = $00400, origin limit = $100000 (both defaults)

### req15: Code Example
- **File**: `req15-orgh-fc000.pasm2`
- **Page**: 12, Lines 35-36
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `ORGH    $FC000`
- **Context**: DAT     ORGH | 'set hub-exec mode and setorigin to $400

### req16: Code Example
- **File**: `req16-orgh-400.pasm2`
- **Page**: 12, Lines 45-46
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `ORGH    $400`
- **Context**: DAT     ORGH | 'set hub-exec mode at currenthub address

### req17: Code Example
- **File**: `req17-pinstart-pinfield-mode-xval-yv.pasm2`
- **Page**: 17, Lines 11-12
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 2
- **Content**: `PINSTART(PinField, Mode, Xval, Yval)`
- **Context**: PINR | PINREAD(PinField) : PinStates | Read PinField pin(s).

### req18: Code Example
- **File**: `req18-rdpin-pin-zval.pasm2`
- **Page**: 17, Lines 23-26
- **Language**: PASM2 | **Type**: Snippet | **Lines**: 4
- **Content**: `RDPIN(Pin) : Zval`
- **Context**: AKPIN(PinField) | Acknowledge PinField smart pin(s).

### req19: Code Example
- **File**: `req19-pri-sumpoints-x1-y1-x2-y2-x-y.spin2`
- **Page**: 18, Lines 49-61
- **Language**: Spin2 | **Type**: Complete Program | **Lines**: 13
- **Content**: `PRI SumPoints(x1, y1, x2, y2) : x, y`
- **Context**: x,y := SumPoints(POLXY(rho1,theta1), POLXY(rho2,theta2)) | …where…

### req20: Code Example
- **File**: `req20-pri-sub1-error-sub1-calls-sub2.spin2`
- **Page**: 18, Lines 69-70
- **Language**: Mixed | **Type**: Snippet | **Lines**: 2
- **Content**: `PRI Sub1() : Error    'Sub1 calls Sub2 with an ABORT trap`
- **Context**: Spin2 has an "abort" mechanism for instantly returning, from any depth of nested method calls, back to a base caller which used '\' before the method name. A single return | value can be conveyed from the abort point back to the base caller:

### req21: Code Example
- **File**: `req21-pri-sub3-sub3-aborts-returning.spin2`
- **Page**: 19, Lines 2-3
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `PRI Sub3()            'Sub3 ABORTs, returning to Sub1 with E...`
- **Context**: PINHIGH(0)          'PINHIGH never executes | PRI Sub3()            'Sub3 ABORTs, returning to Sub1 with ErrorCode

### req22: Code Example
- **File**: `req22-pub-go.spin2`
- **Page**: 19, Lines 47-49
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 3
- **Content**: `PUB Go()`
- **Context**: SEND("Hello! ", GetDigit()+"0", 13) | Any methods called within the SEND parameters will inherit the SEND pointer, so that they can do SEND methods, too:

### req23: Code Example
- **File**: `req23-pri-flash-x.spin2`
- **Page**: 20, Lines 1-2
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `PRI Flash() : x`
- **Context**: PRI Flash() : x

### req24: Code Example
- **File**: `req24-pub-go.spin2`
- **Page**: 20, Lines 18-20
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 3
- **Content**: `PUB Go()`
- **Context**: An example of using RECV: | VAR i

### req25: Code Example
- **File**: `req25-pri-getpattern-pattern.spin2`
- **Page**: 20, Lines 23-25
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 3
- **Content**: `PRI GetPattern() : Pattern`
- **Context**: PINWRITE(56 ADDPINS 7, !RECV()) | WAITMS(125)

### req26: Code Example
- **File**: `req26-pub-go-x.spin2`
- **Page**: 22, Lines 28-29
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `PUB go() | x`
- **Context**: Spin2 methods can execute in-line PASM code by preceding the PASM code with an'ORG {start{, limit}' and terminatingit with anEND. 'Start' is the first register intowhich | your PASM code will be assembled and 'limit' is the upper register which must not be encroached upon. Defaults for 'start' and 'limit' are $000 and $120, respectively.

### req27: Code Example
- **File**: `req27-pub-go-p-k.spin2`
- **Page**: 25, Lines 7-9
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 3
- **Content**: `PUB go() | p, k`
- **Context**: FIELD to read, write, or modify the data it points to. | CON _clkfreq = 10_000_000

### req28: Code Example
- **File**: `req28-pub-go-p-k-i.spin2`
- **Page**: 25, Lines 13-15
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 3
- **Content**: `PUB go() | p, k, i`
- **Context**: Here is an example using indexing to affect successive bitfields. | CON _clkfreq = 10_000_000

### req29: Code Example
- **File**: `req29-pub-go-i.spin2`
- **Page**: 29, Lines 66-67
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `PUB go() | i`
- **Context**: Simple DEBUG example in Spin2 | CON _clkfreq = 10_000_000      'set 10 MHz clock (assumes 20 MHz crystal)

### req30: Code Example
- **File**: `req30-pub-go-i-j-k.spin2`
- **Page**: 39, Lines 24-25
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `PUB go() | i, j, k`
- **Context**: Fast Fourier Transform with 1..8 channels,4..2048 points, windowed results, log scale mode | CON _clkfreq = 100_000_000

### req31: Code Example
- **File**: `req31-pub-go-i-j-k.spin2`
- **Page**: 40, Lines 44-45
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `PUB go() | i, j, k`
- **Context**: Spectrograph with 4..2048-point FFT,phase-coloring, and log scale mode | CON _clkfreq = 100_000_000

### req32: Code Example
- **File**: `req32-pri-showbmp-letter-image_addre.spin2`
- **Page**: 46, Lines 16-17
- **Language**: Spin2 | **Type**: Snippet | **Lines**: 2
- **Content**: `PRI showbmp(letter, image_address, lut_offset, lut_size, ima...`
- **Context**: debug(`g `uhex_(byte[i+0]      + byte[i+1] << 8      + byte[i+2] << 16     )) | i += 3


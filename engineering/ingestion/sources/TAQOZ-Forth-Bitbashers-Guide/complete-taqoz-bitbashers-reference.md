# The Bit Bashers Guide to the Parallax P2 — Using TAQOZ ROM Forth

**Source:** `The Bit Bashers Guide to the Parallax P2 ~  Using TAQOZ ROM Forth.docx`
**Extracted:** 2026-08-26, DOCX-primary, document order preserved, intra-cell newlines preserved.

> **The code in this guide is FORTH**, not Spin2/PASM2. `pnut-ts` cannot validate it and was not run.

The Bit Bashers Guide
to the
Parallax P2
Using TAQOZ  Forth
pubdoc link
https://tinyurl.com/taqozguide
PDF version
taqozguide.pdf
Table of Contents

## 


## Foreword


**Table 1**

*r1c1:*
```
TAQOZ Forth is a permanently available programming language resident in the read-only memory (ROM) of the Parallax Propeller 2 microcontroller.
TAQOZ is written by avid embedded systems hardware engineer Peter Jakacki of Brisbane, Australia.
TAQOZ is polite and does not run until asked!
```


Peter explains his reasons for writing this tool:-
'Back in 2012 I decided to write Tachyon Forth for the Parallax Propeller P8X32A or as we refer to it now simply as P1. Briefly, the reason for writing a Forth was not for Forth's sake although the appeal was there for an interactive development environment resident on the P1, but it was to get more out of the limited memory of the P1, but to also do so as fast as was possible for what is essentially a virtual machine with the view that professional commercial products could be produced based on the flexible P1.
Peter Jakacki wrote Tachyon Forth for the Parallax P1 in 2012.  More recently he ported it to the P2, and renamed it Taqoz Forth.  Taqoz forth has proven itself invaluable in testing and developing the P2, and has evolved into a fully fledged development environment.  Taqoz now ships with the p2, occupying just 12kB of the 16kB of ROM.
.
Taqoz’s great strength is that it generates very small programs which can often fit In cog memory, and thus may not suffer from the slowdowns associated with accessing hub memory.  In general stack machine programs are smaller than reister machine programs, because they do not have to name the registers.  On the P2, Taqoz is particularly small because
he native TAQOZ wordcode can address code in a 16-bit address space while dictionary and data may reside anywhere in memory. So having software written in TWC (TAQOZ Word Code) is very compact and fast and 60kB of code represents a very very large program whereas FAT32, Ethernet servers and VGA including the Tachyon kernel and extensions would all fit in around 20kB of code space on the P1.
TAQOZ provides an interactive  debugging environment through its Forth console via a serial terminal emulator. Even without any 'software' it is possible to exercise the hardware and write code on top of the TAQOZ dictionary, thus extending the language's vocabulary of words, all of which are a combination of various functions, constants, variables etc that are referred to by name. Parameters though are passed postfix style so that data is pushed onto a data stack and precede functions.'
This document was compiled by Bob Edwards  with assistance from Peter Jakacki, with information from various Propeller websites and youtube videos. Many thanks Peter for your help. If you would also like to repay Peter for his generosity in putting TAQOZ and it’s source code in the public domain, there would be no better way than to write a paper on TAQOZ application that will help others. It doesn’t have to be polished, you just have to be enthusiastic about the topic.

## Applications

It’s your choice whether or not to use TAQOZ in the Propeller 2 (P2) to make products. You may decide to use this powerful tool in any one or more of the following stages of a product lifecycle:-
Prototype hardware test – All that is required to be working on a prototype board is the P2 microcontroller and it’s communications port to a terminal. Not even the Propeller clock crystal is needed to start with. A series of tests can then be made using TAQOZ to probe in turn the functionality of parts connected to the Propeller. The only 	essential external equipment is a terminal program running on anything from a desktop computer to a mobile phone – no expensive development system or diagnostic probe is needed. At some stage a multimeter or an oscilloscope may be useful too.
Prototyping – Experiments in driving the various parts of the product can be more quickly made in TAQOZ than other languages, even if the final development then takes place in another language. Programming with TAQOZ interactively during prototyping means that the edit-test cycle is much shorter than with a traditional compiler-linker-programmer suite, thus homing in on a solution more swiftly.
Final application – The firmware for the final product can be written in TAQOZ by extending the language incrementally until the full functionality is achieved. 'Write a bit and test a bit' whilst keeping the application functional at all stages is a modern programming paradigm leading to highly reliable products. TAQOZ was used extensively during FPGA emulation of the P2 chip design, so it’s a proven language.
Production test – The application firmware can be bypassed in order to run any number of production test steps written in TAQOZ. The default serial port may be used to communicate with a test operator or automated test equipment.
Maintenance – Communication with products remotely or in the field using TAQOZ enables prompt diagnosis of hardware faults or firmware bugs. Bugs may also be fixed in deployed hardware, given that was an original design objective.
Apart from the serious business of making products other applications are:-
Education – TAQOZ is arguably the simplest programming language to teach children how to flash lights, make loud (rude) noises, make motors wizz round and generally have a great time whilst learning how computers work. Forth (and of course assembler) are as close to the P2 chip as you can get. However TAQOZ requires far less training to get going than with assembler. TAQOZ is both high and low level language combined.
Hobbyist – TAQOZ is ideal for hobbyist experimentation as it’s quick for one person to get results that build in stages into a complex program. Interacting with the hardware at each stage of design is rewarding and keeps your enthusiasm going. Many radio hams build stuff using forth and microcontrollers. TAQOZ runs fast when compared to a basic or python interpreter, bringing ‘stretch’ goals like dsp processing within reach. Hobbyists are notoriously inventive at getting far more out of the hardware than ever thought possible.

## Training in TAQOZ

Learning TAQOZ is easier than learning P2 assembly language.
Self-training is the most available option to learning about TAQOZ aided by a P2 development board and the 'Starting Forth' book'. Once a basic understanding is achieved then the quick reference on the 'TAQOZ - Tachyon P2 Forth in ROM' website, categorizing all the words in ROM by function is an invaluable aid to memory. Try a bit on the development board, see it work, then try some more. Save snippets on file that you find useful. If you intend to write more than small programs in TAQOZ, then reading through the 'Thinking Forth' book is recommended so as to avoid many pitfalls.
The circuit of a minimal computer suitable for learning TAQOZ is shown in Appendix A. The SD card isn’t strictly necessary but allows the user to progress to ‘TAQOZ RELOADED’ - a much extended version with many advanced  features. This can be downloaded from Sourceforge . Full details of the extended version are covered in other papers.
The P2 processor is described in full in the Parallax Propeller 2 Documentation and this unofficial datasheet.
The  Tachyon Forth Wiki and Gems from TAQOZ Thread   have many useful code snippets and information.

## What is TAQOZ

When the P2 silicon was being finalized for production and since all code was designed to run in RAM, it needed a boot ROM which would load from SPI Flash or serial. After Chip Gracey had written this code, it only used 2K of the 16K ROM that would be implemented in the final silicon. While an SD bootloader would also be useful, even that didn't take much memory either and if nothing else was included, then the rest of the ROM would be wasted. However there was nothing that was really useful that could squeeze into the remaining 12K except for a cut-down version of Tachyon Forth that had originally been written for the previous P1 Propeller chip, but had been adapted for the P2 in its many different FPGA iterations. So the decision was mad to incorporate this  "Tachyon O/S" into the ROM and in order to keep it language neutral it was given the new appellation "TAQOZ".
While TAQOZ is Forth, it is a very specific version of Forth for the P2 and with emphasis on being a useful tool for testing and debugging hardware although complete applications can be written very easily too. As long as a P2 has power and the core of the chip and serial connections are functional, then TAQOZ can be used with little more than a serial terminal emulator, either on a PC or phone/tablet. Interactive "one-liners" can be written that exercise the hardware and are useful as a sanity-checker when nothing else seems to work. Even the SD card and FAT32 file system can be checked and files listed, opened and examined etc.
In a nutshell, TAQOZ is the Swiss army tool that is permanently built into every P2 chip.

## Development boards

The only effective way to learn is by doing. Two P2 development boards are presently available:-

**Table 2**

*r1c1:*
```
P2 EVAL board from Parallax Inc. features:

Propeller 2 multicore microcontroller engineering sample Rev C, production approved silicon
Adjustable operating frequency; recommended 180 MHz clock
16 MB SPI Flash memory
64 Smart I/O pins brought out to edge headers, with 54 fully free
Selectable boot mode
Buffered LEDs on eight I/O pins
Onboard 1.8 V 2-Amp switching regulator with short-circuit and over-current fault protection
Onboard LDO 3.3V regulators for low noise analog experiments
Power headers for current measurement and alternative voltage source injection
Dual power inputs via micro-USB sockets; suitable for USB charger (not supplied) or host computer USB port connection
Built-in FTDI to USB programming interface, with TX/RX activity indicator LED
USB current limiter with short-circuit and over-current fault protection
USB power active and USB fault LEDs
MicroSD card socket (card not included)
```



**Table 3**

*r1c1:*
```
P2D2 (Not currently shipping) board from Peter Jakacki features:-

All 64 I/O arranged as two headers of 16x2 0.1" headers
Dual 32 0.05" header or as half-hole castellations.
RPi header extension
Single sided components - surface mountable module 2"x1"
Small size 2"x1.5" or 52x38mm (max = two SD card sizes)
Efficient dual SMPS 1.8V + 3.6V (pre-regulation for 3.3V)
On-board low-noise dual LDO regulators for 3.3V I/O
Sheltered MicroSD (safely facing inward and protected)
I2C controlled SD power & reset
16MB SPI Flash
Smart microUSB serial port (can be overridden via P63,P62)
System support functions via I2C
Smart serial boot mode - no need to disable SD or Flash
Brown-out and supply monitoring and reset & protection
I2C System Watchdog & wake-up
RV-3028 RTC + supercap backup + 32-bit Unix time.
Power and status LED
Large ground and thermal plane on bottom layer inc thermal via array
Prop Plug compatible header with extra pins for USB 5V power
Crystal + I2C programmable Clock Generator - defaults to 20MHz standard
Options for crystal or oscillator only, and flip side microSD, switch and LEDs.
Standalone or pluggable module.
```


A third option for the DIYer is to hand build a board yourself:-

**Table 4**

*r1c2:*
```
The P2 controller chip is available as a 14mm x 14mm exposed-pad 100-pin TQFP package, 0.5mm pin pitch, which can be hand-soldered only if you have good SMD soldering skills.

Alternatively you can solder-paste and oven reflow - no skills required!

Appendix B shows a simple way of converting the serial terminal link to USB or Bluetooth.

Peter Jakacki offers bare P2D2 boards for those who like to build from the roots up.

CAUTION: The P2 has a center pad on the underside that must be soldered through-board to a ground plane for heat sinking. About 2-3W of heat is generated if all 8 COGS are working hard at high clock rate. The center pad must be bonded to power supply 0V for the P2 to function.

CAUTION: Anti-static precautions must be taken to avoid damage to the chip.

For more details see the P2 documentation
```



### 


## 


## Switching on for the first time

Turning on a prototype for the first time was always a scary moment I remember. Would the magic smoke be liberated from any of the parts? After a quick power supply check, the next priority is to see if the processor functions:
(This needs a description of how to plug in a USB cable. )
Connect a serial terminal to the default comms port of the P2 board. At switch on, P2 expects the following connections:-
Pin P63 is used for RXD (data received from a serial terminal)
Pin P62 is used for TXD (transmit data to the serial terminal)
CAUTION: These are 0V - 3.3V logic signals, damage is highly likely to occur if driven outside this range without protection. If you are building hardware, a good idea is to convert these signals to USB or Bluetooth, see Appendix B.
When using a PC, Tera Term for Windows  or Minicom for Linux are useful terminal programs which support colour and file upload..
The baud rate is set to a safe default of 115200 baud 8 bits, no parity, one stop bit, no handshake is used. Just after a reset and from the keyboard, type the two character auto-baud sequence [>] [space] followed by the [escape] key to enter TAQOZ. The ASCII codes for those three characters are $3B $20 $1B. You will be greeted by the startup response and prompt from COG#0:-

**Table 5**

*r1c1:*
```
Cold start
--------------------------------------------------------------------------------------
 Parallax P2 .:.:--TAQOZ--:.:. V1.1--v33h 190219-1900
--------------------------------------------------------------------------------------
TAQOZ#
```


TAQOZ has completely initialised as indicated by 'Cold start', followed by a status response identifying the processor type and TAQOZ version. The default prompt which appears below is 'TAQOZ#', indicating that TAQOZ is waiting for user input from the terminal and the # indicates that it is in decimal mode.
NOTE: The ROM will always do a Cold start since there is no way to autoboot it, but if we had it backed up to Flash then when we do a RESTORE (or ^R) it will not display the Cold start message.
If the [Enter] key is pressed a couple of times, the default prompt will be echoed, each on a new line proving the link is working and you're in business!

### Hints on data entry in TAQOZ

TAQOZ is case sensitive but most uppercase words can be typed in as lowercase since the system retries a second time with any failures by setting the word to uppercase. This will not work for words that are already lowercase but typed in uppercase.
TAQOZ is a 32 bit forth, meaning that from a cold start, all numbers are interpreted as signed or unsigned integers in that range.
It is recommended that numbers other than decimal should always be prefixed rather than relying upon Forth's use of the current base radix. The reason for this is simple. If you were to copy and paste a section of code then the number 100 would be ambiguous unless you knew the context for it. Is it decimal, or hex, or even binary. Better to say 100 for decimal or #100 to override base settings, and $100 for hex and %100 for binary. No other bases are used normally.

#### Number representations

Forth has the ability to change the default number base or radix for input or printing. While this can be handy it is best to leave it at the default of decimal. How then do we input numbers in the common bases of 2 and 16 (binary and hexadecimal)? In C it is common to represent a hex number with a 0x prefix but TAQOZ keeps it simple and short with either the recommended preceding $ prefix or else a lower-case h after the number. Similarly, binary numbers are preceded with % or suffixed by a b. Just for completeness there is the # and d for decimal numbers. 
The # on the end of the TAQOZ prompt indicates current base.
.S will print the contents of the data stack so in this test we use the same digits '100' and enter them with every variation of suffix and prefix, and then examine the stack. I used !SP to initialize and clear the stack beforehand.

**Table 6**

*r1c1:*
```
TAQOZ# 100 #100 100d $100 100h %100 100b .S ---
 DATA STACK (7)
1 $0000_0004 4
2 $0000_0004 4
3 $0000_0100 256
4 $0000_0100 256
5 $0000_0064 100
6 $0000_0064 100
7 $0000_0064 100 ok
```


Character literals can also be entered very easily too without having to resort to looking up the code. To return the ASCII value for a character, enclose it in single quotes so that it forms 3 characters. Likewise to return the control key value for that character prefix it with a single caret.

**Table 7**

*r1c1:*
```
TAQOZ# 'd' .BYTE --- 64 ok
TAQOZ# ^d .BYTE --- 04 ok
```


Then there is the & prefix which is used for what I call decimal bytes, that is the 0 to 255 values separated by dots to indicate a byte in each position. The other similar form is simply using : between decimal bytes

**Table 8**

*r1c1:*
```
TAQOZ# &48.49.50.51 .LONG --- 3031_3233 ok
TAQOZ# 48:49:50:51 .LONG --- 3031_3233 ok
```


Mixing symbols in numbers
As a general rule symbols may be interspersed between the digits without any problems as long as it does not start or end with these symbols such as _ and , etc, and that there is at least one valid digit that is processed.

**Table 9**

*r1c1:*
```
TAQOZ# #P56 1,000 $10_C000 .S ---
 DATA STACK (4)
1 $0010_C000 1097728
2 $0000_03E8 1000
3 $0000_0038 56 ok
```


Pin numbers are documented as P0 to P63 and while these representations are not valid numbers in TAQOZ, all that is needed is a # prefix to force them to be treated as decimal numbers. i.e. #P32 LOW
Double numbers are two 32-bit stack entries which are treated as one 64-bit value and can be specified by ending the number with a dot. (not in ROM)

**Table 10**

| TAQOZ# 1,234,567,890,000,000,000. D. --- 1234567890000000000 ok |
|---|

Print double numbers with D. and other related double number words.
Strings in Forth are normally stored with the address in memory of the string and then a separate count value. But this takes up two values on the stack for each string and complicates SWAP and DUP etc, so the simpler null terminated string format is used instead. Just a a single value pointing to the memory area where the string is stored. To find the length of it there is the fast LEN$ word. To write a literal string use a single double quote which is a Forth word then  follow it by a space and then the literal string terminated with a matching double quote.

**Table 11**

*r1c1:*
```
TAQOZ# " Hello World!" 16 DUMP ---
01002: 48 65 6C 6C 6F 20 57 6F 72 6C 64 21 00 00 10 F8 'Hello World!....' ok
TAQOZ# " Hello World! " " Goodbye cruel world!" SWAP PRINT$ PRINT$ --- Hello World! Goodbye cruel world! ok
```



### 


### Checking the Flash memory works

At reset, the P2 bootloader checks for an SPI Flash memory connected to pins P58 - P61:-

**Table 12**

*r1c1:* Flash and SD card connections

*r1c2:*
```
SPI Flash connections:-
Pin P58 connected to SI (memory signal input)
Pin P59 connected to SO (memory signal output)
Pin P60 connected to CK (memory clock signal)
Pin P61 connected to CS (memory chip select signal)


This schematic is from the P2D2 module which allows for top and bottom mounted SD sockets.
```


Using the '.SF' (short for print serial flash) we can determine if communication with the flash memory is working:-

**Table 13**

| TAQOZ# .sf --- $EF70_1800 $0F0B_2826 $E468_5CF4 ok |
|---|

Above we see the flash memory manufacturer’s  I.D., serial number etc. 
Btw, TAQOZ is case sensitive but most uppercase words can be typed in as lowercase since the system retries a second time with any failures by setting the word to uppercase. This will not work for words that are already lowercase but typed in uppercase.
We can go further and check we can read actual data from memory:-

**Table 14**

*r1c1:*
```
TAQOZ# 0 $40 DUMP ---
00000: FF FF FF FF FF FF FF FF FF FF FF FF 0E 00 0E 00 '................'
00010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '................'
00020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '................'
00030: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '................' ok
```


Above, we’ve entered 0 (the start address) and 40 hex (the number of bytes we wish to see) on the data stack, followed by the TAQOZ word ‘DUMP’ which does what it says on the tin - it takes those two values from the data stack and dumps the first 64 decimal bytes -  in this case from the processor internal RAM to the display.
By using a very similar command line we can read data from the external serial memory - notice the additional TAQOZ word ‘SF’ below used to redirect the DUMP word to read from the flash:-

**Table 15**

*r1c1:*
```
TAQOZ# 0 $40 SF DUMP ---
00000: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF '................'
00010: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF '................'
00020: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF '................'
00030: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF '................' ok
```


The first 64 bytes from serial Flash memory are displayed - how convenient is that?!
Note: DUMP resets back to RAM memory after each dump automatically.

### Checking the Input/Output pin loads

A useful check on the external loads present on the I/O pins can be made using the 'lsio' (short for list the I/O) word:-

**Table 16**

*r1c1:*
```
TAQOZ# lsio ---
P:00000000001111111111222222222233333333334444444444555555555566
P:01234567890123456789012345678901234567890123456789012345678901
=:dddddddd~~~~~~~~~~~~~~~~~~~~~~~~h~~~~~~~~~~~~~~~~~~~~~~~hhhhhh ok
```


I/O pins P0 to P61 are listed across the screen. Immediately below for each pin is shown it’s status. For instance P32, P56 to P61 are shown 'h' where a pull-up resistance has been sensed. P0 to P7  indicate 'd'  where a pull-down resistance has been sensed. So this allows the user to gain some idea about how externally connected circuitry appears to the P2. (For instance - pins P0 to P7 on this particular board are connected to a VGA display with its 75 ohm input impedances - so the lsio command confirms this

### Checking out an SD card

Why SD card I hear you say - my product is a photocopier? Well, there are a number of reasons why you might fit one regardless:-
An SD card socket is very cheap and small these days - you must be truly pushed for space if you can’t fit one.
The capacity available is enormous for the physical size - far outstrips Flash memory for board area. 1TB cards are readily available now - this could hold a small public library!.
The user may need to save and read data on removable media
The product functionality may need to change or expand over its lifetime and an SD card can be swapped out in seconds without many tools. You can’t do that with flash memory.
Maintenance and debug is made much easier by a rolling record of most recent activity
The product needs mass data storage for logging measurements or multimedia sounds, music, speech, graphics and videos etc.
At switch on, TAQOZ expects any SD card present to be connected on pins P58 - P61, see the ‘Flash and SD card connections’ circuit above. Notice that almost all the connections are shared by the flash memory, so no complaints about taking up precious I/O ports there.

#### TAQOZ Compatible SD Cards

SDHC (Secure Digital High Capacity) was established to meet the growing demand for HD (High Definition) video and high resolution image recording now used in many SD-enabled devices. It is the same physical size and shape as standard SD but meets the new SD specification of version 2.0. Cards 2GB or less are SD and not compatible with TAQOZ. TAQOZ has been tested with SDHC cards 4GB to 128 GB and any higher capacity compatible cards should work. Do not expect TAQOZ to work with the SD card you’ve found in your scrap box, do yourself a favour and buy a new SD card from a reputable manufacturer to go into a TAQOZ project.

#### Talking to the card

Anyway - if you have a FAT32 formatted SD card inserted then MOUNT it like this:-

**Table 17**

| TAQOZ# MOUNT --- .SDSC64G 6269_0201 P2 CARD 32k 60,890M ok |
|---|

If the card is successfully initialized it will then attempt to read the partition table and FAT32 information necessary to mount the filesystem and report the card details when successful. In the instance above the card is reported as an SD (SanDIsk) SC64G (Ultra 64GB) with a hardware serial number in hex of 6269_0201. Finally the FAT32 filesystem name of 'P2 CARD' with 32k bytes per cluster and a total capacity after formatting of 60,890 Mbytes.
Use TAQOZ RELOADED for a full suite of SD and FAT32 utilities including a built-in card formatter that is compliant to SD card Associations specifications and can format cards >32GB as FAT32. Windows itself does neither of these.

#### Formatting SD Cards

Ok, you just bought a new SD card and in if it is 32GB or more then  it is already formatted to Microsoft's proprietary exFAT and won't work with TAQOZ as is. Trying to format it in Windows to FAT won't work since it will still format to exFAT. No problem, TAQOZ RELOADED has a formatter built-in as part of its disk utilities. Issue Read/Write/System permissions, an optional cluster size, and the FORMAT command.

**Table 18**

| TAQOZ# 64 KB CLSZ RWS FORMAT --- CARD: SANDISK SD SC128 REV$80 #3188775123 DATE:2018/11 |
|---|

In this case I have overridden the default 4KB cluster size which is too small for the small number of files that TAQOZ will use with gigabytes of storage, and instead select a more efficient 64KB cluster size. The S in RWS means System sectors so that it will format the MBR. In fact it is possible to format just the MBR, or the FAT ENTRIES, or the ROOT directory, using FORMAT.MBR or FORMAT.FAT or FORMAT.ROOT. A 128GB card can take around a minute to format with 64KB clusters while running at 320MHz.  

Once it has finished formatting then it will automatically produce a .DISK report which also includes a latency and speed test.

**Table 19**

*r1c1:*
```
TAQOZ# 64 KB CLSZ RWS FORMAT --- CARD: SANDISK SD SC128 REV$80 #3188775123 DATE:2018/11

 *** OCR ***
 VALUE........................... $C0FF_8000
 RANGE........................... 2.7V to 3.6V

 *** CSD ***
 CARD TYPE....................... SDHC
 LATENCY......................... 1ms+1400 clocks
 SPEED........................... 50MHz
 CLASSES......................... 0 1 0 1 1 0 1 1 0 1 0 1
 BLKLEN.......................... 512
 SIZE............................ 124,868MB
 Iread Vmin...................... 100ma
 Iread Vmax...................... 1ma
 Iwrite Vmin..................... 35ma
 Iwrite Vmax..................... 10ma

 *** SPEEDS ***
 LATENCY......................... 505us,295us,296us,291us,335us,343us,414us,281us,
 SECTOR.......................... 352us,394us,396us,387us,375us,377us,410us,380us,
 BLOCKS.......................... 4,665kB/s @200MHz

 *** MBR ***
 PARTITION....................... 0 00 INACTIVE
 FILE SYSTEM..................... FAT32 LBA
 CHS START....................... 1023,254,63
 CHS END......................... 0,0,0
 FIRST SECTOR.................... $0000_8000
 TOTAL SECTORS................... 249,704,448 = 127,848MB

00170: 0000_0000 0000_0000 0000_0000 0000_0000 '................'

 *** FAT32 ***
 OEM............................. TAQOZ P2
 Byte/Sect....................... 512
 Sect/Clust...................... 128 = 65KB
 FATs............................ 2
 Media........................... F8
 Sect/Track...................... 63
 Heads........................... 255
 Hidden Sectors.................. 32,768 = 16MB
 Sect/Part....................... 249,704,448 = 127,848MB
 Sect/FAT........................ 15,240 = 7MB
 Flags........................... 0
 Ver............................. 00 00
 ROOT Cluster.................... $0000_0002 SECTOR: $0000_F730
 INFO Sector..................... $0001 = $0000_8001
 Backup Sector................... $0006 = $0000_8006
 res............................. 00 00 00 00 00 00 00 00 00 00 00 00
 Drive#.......................... 128
 Ext sig......................... $29 OK!
 Part Serial#.................... $6269_0201 #1651048961
 Volume Name..................... P2 CARD FAT32 ok
```


Linux displays the card as such using the DISKS app (gnome-disks)

### 


### Internal Processor Clock and program timing

When TAQOZ ROM boots it doesn't really know the system RCFAST frequency ( P2s’ default internal clock ). However TAQOZ does have a constant called CLKHZ which returns the frequency of the clock as a constant, the default value of which is 20,000,000. Some parts though can have an RCFAST value as fast as 25MHz due to process variations so if you want to correct CLKHZ so that timing dependent words such as KHZ and ms are accurate, you need to measure RCFAST and then overwrite the frequency value in CLKHZ. How do you that?
For the following exercise we are assuming that you have a scope or a frequency counter.  If you do not have a scope or a frequency counter, it is possible to use two of the pins of the P2 to read the output and display it on your desktop.
What we will do is set up a pin in NCO mode and tell it to divide the system clock so that we can measure it. Assume we are using P48 we set it up to output sysclock/2 like this:-

**Table 20**

| TAQOZ# 48 PIN $8000_0000 NCO ok |
|---|

You should read a value of around 12.5MHz on the scope on PIN48. Double that value and update CLKHZ and check it like this:

**Table 21**

*r1c1:*
```
TAQOZ# 25,344,000 ‘ CLKHZ 2+ ! ok
TAQOZ# CLKHZ . --- 25344000 ok
```


Commas and symbols are optional in numbers and allowed, whatever helps with readability, and this value is stored at the address of CLKHZ plus 2 which points past the first instruction which says "read and push the value of the following 32-bits".
Now double check by setting P48 to 1MHZ (no need to type 48 PIN again if you haven't changed it)

**Table 22**

| TAQOZ# 1 MHz --- ok |
|---|

TIP: If you don't have a scope or frequency counter, no worries, just use a pin with an LED on it, like P56 and get it to blink on and off every 60 seconds:-

**Table 23**

| TAQOZ# 56 PIN 1 HZ 60 WXPIN --- ok |
|---|

Then time how long it actually takes (say) from the LED switching on to switching back off again. Take that time in seconds and let TAQOZ calculate the corrected frequency by scaling the time to what it should be, where actual_f = f * (60/t):-

**Table 24**

| TAQOZ# CLKHZ 60 48 */ . --- 25000000 ok |
|---|

That is much closer to the real value and timing it over a longer period is another way of getting a more accurate value.

## Further interaction with TAQOZ

Forth in general is interactive, accepting a line of text and numbers separated by spaces from the terminal console and then interpreting the text in this input buffer when you hit the enter key. If we type 12 100 * . then when we hit enter the text string will be evaluated as a word 12 which is not in the dictionary and then tries to convert it to a number and push it on the stack. Fortunately it is and so is 100. This takes time to read the word and search the dictionary and then try to convert it to a number. By the time that the * and the . are read and found in the dictionary, and executed, quite some time has passed, maybe many tens of milliseconds or more. Yet if we define a new word that does the same thing and then execute it, it only takes tens of microseconds, mostly in printing the number. The difference is that one interprets the text word by word, and the other just executes code.
TAQOZ tackles this traditional 'text input buffer' and evaluation very differently. First off, there is no line buffer, only a word buffer. Second as each word is entered the word will be checked to see if it's a number, and if it is, it will immediately be compiled into temporary code space as a numeric literal. So 12 and 100 would not be pushed onto the stack after a line is entered, but rather they are compiled, word by word. The same too with the words ‘*’ and  ‘.’ and all the while as new temporary code is compiled, it is automatically terminated with an EXIT, which is the Forth equivalent of a return-from-subroutine. When the enter key is pressed there is no further delay, no need to start interpreting the line, but instead the code that has already been compiled in the temporary memory area is simply executed.

### Advantages of temporary word-by-word compilation

What's the advantage of compiling word by word? Well, we don't need to reserve memory for a long text input buffer, and we also don't lose any time with executing the code when the enter key is pressed. But more importantly, the code is executed at full compilation speed, just as it would be if it were compiled into a definition. Some I/O operations are timing sensitive and can only be timed correctly from compiled code.  But there are other advantages too. For instance, in Forth you can't use 'compile-only' words interactively, but now we are always compiling, you can use them just the same.

**Table 25**

| TAQOZ# 5 6 * 20 > IF ." Greater than 20 " THEN --- Greater than 20 ok |
|---|

Also, you can use BEGIN WHILE REPEAT AGAIN IF ELSE THEN DO LOOP +LOOP FOR NEXT etc although the latter loop words are actually not 'compile-only' words in TAQOZ anyway, since they compile as is, not requiring any branch calculation because DO pushes the branch address onto a separate loop stack.

**Table 26**

*r1c1:*
```
TAQOZ# 0 10 FOR I + NEXT . --- 45 ok
TAQOZ# 0 0 BEGIN OVER + SWAP 1+ SWAP OVER 10 = UNTIL NIP . --- 45 ok
```


To find out more about DO LOOP FOR NEXT etc, look at the Wiki pages for 'LOOPs never return' at the Tachyon SourceForge Wiki.

## Writing your own words in TAQOZ

We’ve just seen that TAQOZ executes a line of code typed in at the terminal, which is great for testing things out, but the code is lost after execution. That doesn’t help us write a program of our own. To do that we need to write a ‘pyramid’ of words that call existing words - extending the TAQOZ system - ending in one master word at the top that is used to start the application. OK, an example of creating a new word is:-

**Table 27**

*r1c1:*
```
TAQOZ# pub MYCOUNT 0 10 FOR I + NEXT . ; ok
TAQOZ# MYCOUNT --- 45 ok
```


Notice the use of the words ‘pub’ at the beginning and ‘;’ at the end to define the start and end of the new word. (When reading ‘Starting Forth’ you’ll notice that ‘pub’ is shown as ‘:’ In TAQOZ the alias ‘pub’ has been added to ‘:’  to appeal to SPIN programmers.)
If we then list the TAQOZ dictionary using ‘WORDS’, we can see our new definition has been added to the list. When typed in, this word behaves like any other built-in TAQOZ function. We’re extending TAQOZ to make our own language to suit the application.
‘pub’ has two sister words ‘pri’ and ‘pre’ which are also used to define new TAQOZ words. Here’s the difference between them:-

**Table 28**

| pub <new word name> … existing TAQOZ words …. ; | Creates a new Forth word as public - it stays forever in the TAQOZ dictionary - well until you switch off again |
|---|---|
| pri …<new word name> … existing TAQOZ words …. ; | Creates a new Forth word as private - but the dictionary entry of this word can be culled later so that further new words cannot be made with it. E.g. For creating hidden words that are only useful within a driver library - the user of the library only gets access to the ‘public’ words. |
| pre <new word name> … existing TAQOZ words …. ; | Creates a new Forth word as preemptive - this word will not compile, it will execute immediately during the compile process. In the book ‘Starting Forth’ this is equivalent to marking the last word compiled with the word IMMEDIATE - read up about why that’s useful and how to force your preemptive word to compile if you want. |


## 


## Saving the TAQOZ image for next time

Having added your new words to TAQOZ, you might want to save the modified system for next time, so you can quickly pick up from where you left off. You may do this with the words:-
TAQOZ ROM

**Table 29**

| BACKUP | Backs up the first 64k of hub memory in the P2 into flash memory (does not automatically restore) |
|---|---|
| RESTORE | Restores the first 64k of hub memory in the P2 from flash memory |

When using TAQOZ RELOADED, more save options become available, but for now the above will get you going with TAQOZ ROM.

**Table 30**

| COMMAND | SHORTCUT | ACTION |
|---|---|---|
| BACKUP <filename> |   | Backup 128kB of code and dictionary in the named file (will not create it) |
| BACKUP MBR | BU | Backup directly from sector 1 for 256 sectors - ignores format (normally reserved in SD cards) |
| BACKUP BIX |   | Backup to _BOOT_P2.BIX file (creates a 128KB file if necessary) |
| BACKUP FLASH | ^F | Creates a second stage loaded in Flash and backs up first 128KB |
| BACKUP DISABLE |   | Disable MBR and Flash backup but leaves .BIX or .BIY untouched |

RAW BOOT SECTOR INFO - MBR SECTOR 0
$174    = SECTOR (4)
$178    = BYTES (4)
$17C    = "ProP" (4)

## TAQOZ and the SMART PINS

Whoa - is that the name of a 70’s pop group? One of the most exciting new features of the P2 processor are the 64 built-in ‘SMART PINS’  available for I/O. Each pin (or group of pins acting together) can be configured to act in any one of the following modes , each a sophisticated analogue or digital I/O subsystem . The modes are:-
8-bit, 120-ohm (3ns) and 1k-ohm DACs with 16-bit oversampling, noise, and high/low digital modes
Delta-sigma ADC with 5 ranges, 2 sources, and VIO/GIO calibration
Several ADC sampling modes: automatic 2n SINC2, adjustable SINC2/SINC3, oscilloscope
Logic, Schmitt, pin-to-pin-comparator, and 8-bit-level-comparator input modes
2/3/5/8-bit-unanimous input filtering with selectable sample rate
Incorporation of inputs from relative pins, -3 to +3
Negative or positive local feedback, with or without clocking
Separate drive modes for high and low output: logic / 1.5 k / 15 k / 150 k / 1 mA / 100 µA / 10 µA / float
Programmable 32-bit clock output, transition output, NCO/duty output
Triangle/sawtooth/SMPS PWM output, 16-bit frame with 16-bit prescaler
Quadrature decoding with 32-bit counter, both position and velocity modes
16 different 32-bit measurements involving one or two signals
USB full-speed and low-speed (via odd/even pin pairs)
Synchronous serial transmit and receive, 1 to 32 bits, up to clock/2 baud rate
Asynchronous serial transmit and receive, 1 to 32 bits, up to clock/3 baud rate
The SMART PINS greatly reduce the code required to interface to the outside world, working as they do in parallel with the COGS that drive them.
Various drive modes are also selectable including various values of pullup or pulldown in terms of resistance, or current.
Parallax have succeeded in making configuration of the SMART PINS as straightforward as possible - which is a real breath of fresh air. Any COG can drive any SMART PIN. TAQOZ naturally includes words for SMART PIN configuration and control. The names of the words have been carefully chosen so as to make their meaning obvious.  Here are some examples to show how few TAQOZ words are required to start exercising the rest of your circuit in earnest:-

### Output a continuous pulse stream

Here’s the code to have P6 emit a continuous 3.3.V high logic tone at 2 kHz 1:1 mark / space ratio:-

**Table 31**

*r1c1:*
```
TAQOZ# 6 PIN 2 KHZ ok
TAQOZ# MUTE ok
```


We can stop the tone again by the 'MUTE' word
OK, how about a sweep tone?:-

**Table 32**

| TAQOZ# 6 PIN 3000 100 DO I HZ 50 ms 100 +LOOP MUTE ok |
|---|

Here we step from 100Hz up to just before 3000Hz as this is when the loop exits, pausing for 50mS at each frequency and stepping on by 100Hz afterwards.

### Output a string to a serial port

We want to make pin P8 act as a serial port. Here’s the code to do that. First we define a ‘SEND$’ word:-

**Table 33**

*r1c1:*
```
TAQOZ# pub SEND$ ( string baud pin ) \ outputs ‘string’ at ‘baud’ rate to SMART PIN number ’pin’
TAQOZ# \ with default no. of bits, parity, no. of stop bits
TAGOZ# PIN TXD DUP LEN$ TXDAT ;
```


This is how that’s used: -

**Table 34**

| TAQOZ# “ Hello World” 115,200 8 SEND$ |
|---|

There had to be a ‘Hello World’ program somewhere in an introduction - so this is it. Seriously - notice how few lines are needed - and even a non-Forth programmer can guess what is going on because of the  word names chosen.

### Output an analogue voltage

We want to output a steady DC voltage in the range 0 - 3.3V on P52:-

**Table 35**

| TAQOZ# 52 PIN 825 mV ok |
|---|

The voltage of 0.825V can be confirmed by multimeter measurement and is being produced by a 12 bit digital to analogue converter. Valid values for word ‘mV’ are in the range 0 - 3300. Any SMART PIN can do this if required, they are all independent  of each other.

### Measure the frequency and duty cycle of a digital  input

This is a more elaborate and probably cryptic example than the rest, but it’s still easy to appreciate that very few lines of source code are needed to achieve the goal. First we define a word to set up the SMART PIN as a  frequency counting input:-

**Table 36**

*r1c1:*
```
pub FREQCNT (clocks mode0..2 --- )
F 2* %00_10101_0 + WRPIN
CLKMHZ * WXPIN %00 WYPIN H
;
```


This word returns raw frequency measurements from the current pin:-

**Table 37**

*r1c1:*
```
pub RAWFREQ? ( uS --- clocks states periods )
3 FOR DUP I FREQCNT AKPIN WAITPIN RQPIN SWAP NEXT DROP
;
```


What follows is a demonstration of using  RAWFREQ?  that displays the frequency and duty cycle on the terminal:-

**Table 38**

*r1c1:*
```
pub .FREQ
100,000 RAWFREQ? ( clocks states periods )
SWAP 1,000 4TH */ .” Duty = “ 2 .DP .” %” ( clocks periods )
CLKHZ ROT */ .” Frequency = “ .DECL .” Hz”
;
```


It’s left, as they say, to the reader to work out what’s going on in detail after becoming more familiar with TAQOZ - and this website explains a little more meanwhile.

## 


## How do I get other cogs running TAQOZ code?

Besides the new SMART PINS on P2, the other amazing feature (which is shared with P1) is that eight independent cores  or 'COGS' are available to run TAQOZ code. Here is a very quick and simple example to run a word in a fresh COG as a task. First however we need to run an instance of TAQOZ in the new COG (TAQOZ isn’t automatically loaded into other COGs).
In this example we will choose COG#1 with two words:-

**Table 39**

| TAQOZ# 1 NEWCOG ok |
|---|

Now that COG#1 has been loaded with a TAQOZ kernel, it is sitting in an IDLE loop waiting for a task to perform. All we need to do is to give it the address of that task. We make a new word BLINKER which runs continuously; the blinking code is placed in a BEGIN AGAIN structure which will loop unconditionally. We then find the address of BLINKER (using the tick symbol $27) and store it where COG#1 will be checking in its task variable:-

**Table 40**

*r1c1:*
```
TAQOZ# pub BLINKER BEGIN 7 HIGH 100 ms & LOW 100 ms AGAIN ; --- ok
TAQOZ# ‘ BLINKER 1 TASK W! ok
```


The last line here would be read aloud as 'address of - BLINKER - 1 TASK - W STORE'.
A more useful way to run a task in another COG is this: We define a new word called RUN:-

**Table 41**

*r1c1:*
```
TAQOZ# pub RUN (task cog --- ) \ Run ‘task’ on COG number ‘cog’
TAQOZ# DUP NEWCOG \ Load the TAQOZ kernel onto our chosen COG
TAQOZ# 5000 WAITX \ Wait for COG to load and initialize (~25us @200MHz)
TAQOZ# TASK W! \ set the COG task to run
TAQOZ# ; ok
```


The new RUN word is ready to be used so we run BLINKER on cog #4:-

**Table 42**

| TAQOZ# ‘ BLINKER 4 RUN ok |
|---|

We now have a way of starting tasks on any COG we like as part of our program. Stopping COG#4 is just as easy:-

**Table 43**

| TAQOZ# 4 COGSTOP ok |
|---|


## P2 start up and the resources TAQOZ uses

Here’s a simplified block diagram of the P2 architecture:-

**Table 44**

*r1c1:* Propeller 2 Block Diagram

*r1c2:*
```
Each COG has 2 blocks of RAM, each of 2 kbytes. One block is termed ‘Register’ RAM, the other ‘Lookup’ RAM.

All COGS can simultaneously read and write from the 512 kbyte Hub RAM, 8, 16 or 32 bits per clock cycle, as determined by the instruction executed.

All COGS can execute code in their own Register and Lookup RAM or the common Hub RAM space.

A call to a COG word stored in the TAQOZ dictionary mostly takes 16 bits.

The TAQOZ address space is 64 kbyte which is shared by the TAQOZ system and user code. The snippets of forth shown in this paper hint at how few words are required to get a job done. Thus, a very large TAQOZ application will fit into the P2.

Immediately after P2 reset, the 16 kbyte P2 ROM loads automatically into the last 16 kbyte of Hub RAM at $FC000. TAQOZ occupies 12 kbyte of that 16 kbyte. When TAQOZ is first run, it copies itself to the first 64 kbyte of hub ram (see Peter’s comment below).

The P2 also has an SPI loader for automatic startup from flash or SD card, so autostarted TAQOZ programs are possible to do.

There is also a serial loader for startup from the host.
```


On TAQOZ memory usage Peter Jakacki comments “The first 64k is barely used and so it will be hard to run out of memory or COGS. TAQOZ RELOADED doesn't fill up 64k either although the dictionary is sitting in the next 64k page, but still has plenty of room. The VGA screen takes about 300k though and playing movies requires an extra 70k”

## 


## Speed of execution compared to other languages

TAQOZ programs execute very quickly compared to equivalent SPIN, Basic or MicroPython programs. TAQOZ execution speed is closer to that of assembly language: Peter Jakacki comments: 'Some things will run 10 times slower compared to assembly code in cog local memory. However some operations are just as fast especially when they involve serial buses such as I2C and SPI etc.'
When the application is going to push the processor hard, it's as well to have some idea of what parts of your program are proving to be bottlenecks. TAQOZ provides you with timing tools with which a word or code section can be timed. Mark the start and end of your timing with LAP and then once that is done you can print the lap result with .LAP. Here’s the words to do that:-

**Table 45**

*r1c1:*
```
TAQOZ# LAP 1,000,000 FOR NEXT LAP .LAP --- 32,000,147 cycles= 160,000,735ns @200MHz ok
TAQOZ# 1,000,000 LAP FOR NEXT LAP .LAP --- 32,000,082 cycles= 160,000,410ns @200MHz ok
TAQOZ# LAP 1,000,000 LAP .LAP --- 58 cycles= 290ns @200MHz ok
```


In this example we time how long it takes an empty FOR NEXT loop to run by looping 1 million times. We can then take the timing value and reduce that from 160ms down to 160ns. But notice the first reading has an additional 735ns or 147 cycles. Where did this come from? Partly from the 1,000,000 and partly from FOR itself when it sets up the loop. By judicious use of the LAP words, the timing can be analyzed minutely.  It takes 290ns just to push a value onto the data stack, but a single loop takes around half of that time.
Here the Sieve of Eratosthenes which compiles using 66 code bytes is timed accurately within a single iteration. Then since it is easy to overclock the P2, we time it again at 340MHz (Small values like 340 are automatically upgraded to MHz)

**Table 46**

*r1c1:*
```
TAQOZ# LAP PRIMES LAP .LAP --- 5,970,457 cycles= 29,852,285ns @200MHz ok
TAQOZ# 340 clkfreq! --- o
TAQOZ# LAP PRIMES LAP .LAP --- 5,970,457 cycles= 17,560,167ns @340MHz ok
```


NOTE: Unlike PC Forths that have not only enormous code memory, they also have enormous resources for the compilation and optimization itself, TAQOZ achieves speed and a small code footprint through an efficient 16-bit wordcode mechanism. There are also many special operations such as SPI transfers as part of the cog assembly code kernel. For instance, SPIRX is a kernel word that can read 512 bytes serially in around 61us or over 8MB/s:-

**Table 47**

| TAQOZ# SDBUF 512 LAP SPIRX LAP .LAP --- 19,521 cycles= 61,003ns @320MHz ok |
|---|


## Inserting Assembly code into TAQOZ programs

When we need even more speed, we can identify the section of code that is crucial, then this can be rewritten as embedded assembly language. A full assembler is available with ‘TAQOZ RELOADED’ - downloadable here. Here’s a brief example of a word written with the assembler to give some idea of how straightforward it is to mix TAQOZ and assembler together:-

**Table 48**

*r1c1:*
```
TAQOZ# code ffibo
06E06: F604_1600 mov x,#0
06E0A: F604_1801 mov y,#1
06E0E: F100_180B l0 add y,x
06E12: FB6C_45FF djnz a,#l2
06E16: 0600_440C _ret_ mov a,y
06E1A: F100_160C l2 add x,y
06E1E: FB6C_45FB djnz a,#l0
06E22: 0600_440B _ret_ mov a,x
 end --- ok
TAQOZ# --- ok
TAQOZ# 46 ffibo . --- 1836311903 ok
TAQOZ# 46 LAP ffibo LAP .LAP --- 1,000 cycles= 4,000ns @250MHz ok
```


A new ‘ffibo’ word is created using the code directive so that the interactive assembler will be activated and the assembler words will be searched first so that assembler mnemonics are not mistaken for Forth words such as and. The TAQOZ prompt is also changed to indent as necessary so that when a line of assembler code is entered it will return to the start of the same line (that's what CR is supposed to do, while LF moves a line down +without changing position), and print the program counter and code.
This code word will look like any other word in the dictionary but of course when it is invoked it executes assembly code in hubexec mode (see P2 docs). We can test out the new fast interactive ffibo word and it works, and then time it. Fast indeed. Code definitions are used sparingly and are only necessary when speed is of the essence and it would make a difference, especially if it is repeated and not blocked by other slow processes.

## 


## Useful TAQOZ diagnostic words

TAQOZ, started from ROM, has the following diagnostic words to help with programming  :-
WORDS - lists the current dictionary of words, including those you’ve added
DUMP and friends - Dump selected memory in various formats
.S - list the contents of the data stack
DEBUG - dumps the data, return and loop stacks, task registers, section of the current code, section of dictionary memory
LAP & .LAP. - time and report code execution
RESET - reset the P2
More tools can be found in the extended TAQOZ RELOADED system. Here’s a taster to tempt you in:-
SEE - disassembly of a compiled word with memory addresses, wordcode, name and value of each component word
DECOMP - reconstitute a compiled word, displaying it as source code
TRACE & UNTRACE - view code as it executes
.VARS -  print all variables in the dictionary with their addresses in memory
.CONS - do the same with constants
… the list is getting longer as TAQOZ is extended by Peter Jakacki and "other enthusiasts" (I wish).

## 


## Creating a standalone program

This is a hint for those eager to make things with TAQOZ ROM.
When the P2 is reset, a built-in program called a boot loader is responsible for copying itself, a machine code monitor and TAQOZ to RAM. The boot loader then checks the Flash memory for an auto-boot user program. To enable a TAQOZ standalone program, two things need to be present in Flash memory: (a) A backup of TAQOZ ROM that includes the user application (See ‘Saving the TAQOZ image’ above) (b) A tiny ‘second stage Flash booter’ tailored for TAQOZ. The second stage Flash booter is loaded into RAM and runs. This loads our TAQOZ backup into RAM and runs the master word of our application.
So here's what to do to create a ‘turnkey’ TAQOZ ROM program that will run immediately when the P2 board is switched on  :-
COMMENT: ROM-wise, it’s a pity that Chip didn’t make it simpler to boot the Flash. He could have had his system and still allowed for both. At present the ROM is not auto-bootable because no allowance was made for that, and neither is control passed to TAQOZ to do its own thing there either. But I was content just to have it in ROM nonetheless. TAQOZ ROM included AUTORUN but it wasn’t of any use because of the way the boot ROM works.
Now the tiny second stage Flash booter will in turn load up the TAQOZ ROM image that was backed up to $F.0000 in Flash and if there is an autorun set then it will be executed on startup. Presto. I will have to go and try this now.
I suppose we could assume that every P2 has a 20MHz clock so I could make the Flash loader snippet with that setting included, and another for RCFAST only.
COMMENT: While my Forth startup routines wait a short while to check for a ^A abort key, the Flash loaded will just load the saved image and run it. It would be up to the user to have an 'abort' function but remember that the P2 EVAL board has DIP switches to disable Flash etc.
N.B. When the SD card based TAQOZ RELOADED is used, other ‘turnkey’ options become available.

## Hints on ‘Good’ Programming Style

Do you fully understand the code you wrote six months ago? TAQOZ, being a Forth dialect, is very easy to hack around in, but the result can be unreadable even a short time later. Much of the forth code to be found on the internet is sub-standard in style. The book ‘Thinking Forth’ has plenty to say about this - but here’s a few headlines:-
Factor your source code: It’s useful to break an application down into a group of files. Each file defines some cohesive part of the program, such as ‘rotary control decoder driver’, ‘stepper motor driver’, ‘lcd display driver’ rising up the application to ‘main’ - or whatever you choose to call the top word that calls the application to life. This is also useful when fixing bugs during development. Reloading a small file which can be tested by itself is quicker than testing, editing and reloading one large one. Such files are more likely to be reused in other projects too.
Factor big words - if a TAQOZ word is getting long, it probably needs factoring into smaller chunks. There may be repeated word phrases that can be factored out as a separate word, which can be reused elsewhere and saves space. Shorter words are easier to read, debug and you are much less likely to take or leave the wrong amount from the stacks. The program will crash if the latter is not fixed.
Choose expressive word names
Choose word names that work in phrases to ‘almost’ read like a spoken language - this needs much practice! This can mean the difference between heavily commented spaghetti code or self-commenting easy to read and debug code.
Favour short words - less typing!
Learn and adopt TAQOZ naming conventions - have a look at source code examples for style hints
Begin all definitions at the left edge of the screen
Define one word per line, the same with variables and constants
Define the radix of each number by using the right TAQOZ prefix / suffix e.g. 100 for decimal (or #100 to be sure), $100 for hex, %100 is binary. Numbers in an unintended radix are a well hidden bug.
Use spacing and indentation liberally - especially when looping code
Include a 'stack effect' comment - what does the word require as inputs on the data stack, what does it leave on completion?
Include a 'purpose' comment - this briefly describes the purpose of the word when executed and if applicable when compiled. (Words that have a separate action at compile time are used to create new types of TAQOZ words e.g. a word to create an array allots the memory space at compile time, but returns the array address at run time)
Ease of maintenance - include an adequate number of other comments for code maintenance purposes
Prototyping versus Development - it can be that a program gets written twice. Once during prototyping which is quick and dirty. Second time, the full scope of the application is better known and is rewritten in an acceptable style, properly factored and so on. The very nature of TAQOZ being a forth system means that a lot of the prototype can be reused.
As Peter puts it: ‘The point here is that you have tested the foundations and real-life characteristics of your hardware and software, much like a wire-wrap prototype so now you have a much better idea of how to approach the problem and almost invariably we find a better and simpler solution in the process so that you end up with the final "pcb".’
What would you rather read when up against a deadline? Page after cryptic page of this:-

**Table 49**

| TAQOZ# pub NOTES 3000 100 DO I HZ 50 ms 100 +LOOP MUTE ; ok |
|---|

Or:-

**Table 50**

*r1c1:*
```
TAQOZ# pub NOTES ( -- ) --- Output a rising set of notes, 100 to 2900Hz via a SMARTPIN
TAQOZ#
TAQOZ# 3000 100 DO --- Set the note range
TAQOZ# I HZ --- Output a note
TAQOZ# 50 ms --- Wait 50ms to define the note length
TAQOZ# 100 +LOOP --- Step up in frequency by 100Hz and repeat
TAQOZ# MUTE --- All done - silence the pin
TAQOZ# ; ok
```


We can debate over the detail, but the latter is preferred, especially when shared between project team members.
Notice the ‘stack effect’ comment in ( ) brackets -
There’s a ‘purpose’ comment at the top of the definition
The other comments use the word ‘---’ so that the TAQOZ compiler ignores the rest of the line. Notice the use of white space and indenting to make it easier on the eye. Now we’re all ‘paperless office’ there’s no need to scrunch it all up tight.
The word would be run like this:-

**Table 51**

| TAQOZ# 6 PIN NOTES ok |
|---|

The pin is selected and the notes are output on that pin.
Roundup
This has been an introduction to bringing a P2 board to life using TAQOZ, help for the newcomer to start writing their first TAQOZ programs and hopefully identified a few useful resources. Anyone who would like to contribute to this document or publish one of their own is very welcome to make contact via the Parallax P2 forum.

## Appendix A Minimal TAQOZ system

This minimal P2 circuit shows the terminal, flash and SD card memory connections that TAQOZ expects. Notice the P2 reset line RESn brought out for convenience to the serial connector. It requires logic low to reset - and should have a pull-up resistor (not shown on the diagram).
Basic Power and Boot Connections

## 


## Appendix B Adapting the serial port

The 3.3V logic level serial port on the P2 is OK for on-board communication, but isn’t rugged enough for going off-board. Also modern computers, tablets and phones don’t use 'RS232' hardware these days. When they did, the signal levels were +/- 25V which would fry the P2.
Here are two options that are very cheap to implement, available from Ebay and the like. Best to choose a reputable source if building this into a final product, though (like the chip built-in to the P2D2 board):-
Serial to USB adapter

**Table 52**

*r1c1:* USB to serial adapter

*r1c2:*
```
This one is dual power supply capable. Don’t forget to move the jumper to the 3V3 position before power on, else the P2 will be damaged. GND, TXD and RXD are directly connected to the P2 serial port.

When the USB connector is plugged into a computer, the data link will usually install automatically as a serial port in your PC’s hardware list.

This one came with a small bundle of jumper wires to push onto the pins.
```


Serial to Bluetooth adapter

**Table 53**

*r1c1:* Bluetooth to serial adapter

*r1c2:*
```
This one’s my favourite data link solution. Why, I hear you ask? Well, I can leave the lab bench and the P2 behind and go and program from the comfort of the sofa!!

The adapters come marked as FC-114, HC05 and so on - best to get one that can act as both master or slave - they’re more versatile. Connecting to the P2 is just like with the USB adapter, RXD, TXD and GND are the essential signals.

These modules default to 9600 baud, but can be reconfigured up to a more respectable 1,382,400 baud - or so it says in the user guide. The module stores the new settings in flash memory. There are many ways of reconfiguring the module, the one I use is a windows program called ‘HC05 configurator’. Here’s a video on usage. The software shows the USB adapter to Bluetooth adapter connections needed for the reconfiguration. If you’ve a box of these bluetooth dongles, stick a label on each showing the chosen settings.

CAUTION: A wireless link can be overheard and broken into - wireless is not as secure as a wired link.
```


Being able to program a remote P2 from the sofa isn’t the only benefit of a wireless serial link:-
The P2 you want to control and monitor may be behind a safety barrier through which you can’t run a cable
The customer is wary of letting you directly connect to the P2 for safety reasons (e.g. It’s part of a running Railway Signalling system)
The P2 is sat at a high voltage w.r.t ground so a direct link would be a hazard to life
The P2 is operating in an electrically noisy environment. Noise current induced on a direct link would crash the PC or P2, whereas a UHF radio link operates well above the broadband hash produced by arcing contacts (typically less than 100MHz)
You can communicate with an array of P2s without cables trailing all over the equipment room
You can make a lower cost open-ended product - everybody already owns the display and keyboard part - it’s the phone in their pocket
Remember any SMART PIN can be a serial port
Terminal software
Tera Term  is a terminal program to communicate with TAQOZ from Windows.
A good terminal program for Linux is Minicom which can be installed from your package manager
They both include the ability to upload source files to the P2. TAQOZ  will immediately compile the incoming stream to executable words, just like a really high-speed user terminal session. There is no need to set any delays in the terminal program - TAQOZ is that fast to compile. This is invaluable when reloading a source file for the umpteenth time.

## About the Author

Bob Edwards is a retired electronics designer, EMC engineer and radio ham G4BBY located in SW U.K.
He’s dabbled with forth programming on and off for 30+ years and regards it as ideal for development of microcontroller applications. It’s one of two programming languages that he finds are fun to use, which makes him productive. Forth programming requires less effort than other languages once you’re reasonably comfortable with it. You can concentrate on the application and not get lost puzzling over complex syntax and development tools.
Forth, invented by Charles Moore, has stood the test of time for 50+ years, created at around the same time as C was by Kernighan and Ritchie.
Forth is quietly being used by a small number of organisations who thoroughly understand the advantages it brings. An ongoing example of that is the use of Forth in Space exploration  where low power, high reliability and small code footprint are essential requirements. The Rosetta probe that intercepted and landed on the Chryumov-Gerasimenko comet in 2014 had no less than ten Forth based processors on board.
How many other languages can claim that?
You will find TAQOZ to be a very powerful, flexible tool in all stages of a products’ lifetime, if you choose to learn enough about it. It may even improve your programming style in other languages! It’s always there, just switch that P2 on and ….
Hopefully this document will get you going
B.E. – June 2020

## 


## References


**Table 54**

*r1c1:* Parallax Forum – exchange ideas with other P2 users, ask the experts and find out where tools and utilities are to be found

*r1c4:*
```
Propeller Live Forum: Testing Hardware with TAQOZ in ROM 
Peter Jakacki and Ray Rodrick - Youtube Video
https://www.youtube.com/watch?v=DfDaXcbk-dY&t=6758s
```

*r2c1:*
```
Starting Forth – free book teaching the fundamentals of Forth Programming by Leo Brodie
https://www.forth.com/starting-forth/
```

*r2c4:*
```
Thinking Forth – free book by Leo Brodie teaching the philosophy of general problem solving and a programming style appropriate to Forth. Well worth the time reading this – avoid developing bad habits that lead to hard-to-manage 'write-only' ‘spaghetti’ code 
https://sourceforge.net/projects/tachyon-forth/files/books/
```

*r3c1:* TAQOZ RELOADED – an extended version of the language to optionally support a full fat32 file system, sound, video and much more that can be saved on flash or SD card

*r3c4:*
```
Forth in Space Applications
https://www.forth.com/resources/space-applications/
```

*r4c1:* Parallax Propeller 2 Documentation v32 - Rev B/C Silicon

*r4c4:* TAQOZ - Tachyon P2 Forth in ROM - the website to go to after this - code examples, SMART PIN examples, keyboard shortcuts and a quick reference to all the words in TAQOZ ROM, sorted into functional groups. Keep the quick reference by your terminal, you’ll use it all the time.

*r5c1:*
```
HC05 Configurator - windows software for setting up Bluetooth to serial adapters
https://forum.arduino.cc/index.php?topic=431547.0
```

*r5c4:*
```
HC 05 bluetooth module configuration software for PC - Youtube video
https://www.youtube.com/watch?v=Fb9w1RoM2yI
```

*r6c1:*
```
Tera term - Windows terminal program for communicating with TAQOZ
https://ttssh2.osdn.jp
```

*r6c4:* Minicom - Linux terminal program for communicating with TAQOZ. Install from your package manager - Click here for help with minicom

*r7c1:*
```
Tachyon Forth Wiki
https://sourceforge.net/p/tachyon-forth/wiki/browse_pages/
```

*r7c4:* GEMS from TAQOZ Thread


to do
auto boot
obex?
send p2d2 and p1 boards & blanks
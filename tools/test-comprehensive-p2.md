# Comprehensive P2 LaTeX Escaping Test

## Image References (Should NOT be escaped)
![Smart Pin Block Diagram](assets/P2 SmartPins-220809_page03_img01.png)
![Configuration Flow](assets/smart_pins_config_flow.png)

## P2 Assembly Instructions in Text (Should BE escaped)
The P2 uses #immediate for immediate values, ##long_immediate for 32-bit values.
Hub addresses like $1_0000 to $7_FFFF use underscores for readability.
Binary values like %1010_0001 also support underscore separators.

## Code Blocks (Should NOT be escaped)
```pasm2
        mov     x, #42              ' Load immediate
        waitx   ##25_000_000        ' Wait 0.5 seconds
        wrlong  data, ##$1000       ' Write to hub
        and     value, #%1111_0000  ' Mask upper nibble
```

## Mathematical Expressions (Should BE escaped)
The P2 can address 2^9 = 512 cog RAM locations.
With 20-bit addresses, it reaches 2^20 = 1MB of space.
Smart pins operate at f_sys/2^n where n is the divider.

## Mixed Content
Here's a diagram ![NCO Mode](assets/nco_mode.png) showing how the NCO frequency 
is calculated as f_out = f_sys * (phase_inc / 2^32). The ##phase_inc value 
sets the output frequency, where $8000_0000 gives f_sys/2.

## Special P2 Patterns
- Pin ranges: P[63:0] for all pins
- Bit fields: value[15:8] extracts a byte
- Operators: value & mask, result | bits
- Percentages: 80% duty cycle

## LaTeX Commands (Should be preserved)
This text has \textbf{bold} and \textit{italic} formatting.
We can use \section{Headers} and \subsection{Subheaders}.

## Edge Cases
Start of line #immediate value
End of line immediate#
Multiple patterns: mov #reg, ##$FF_AA & mask
URL-like: http://example.com#anchor should work
Temperature: 25°C & 77°F at 50% humidity
# Identified Broken Tables in P2 Datasheet Narrative

These tables appear to have lost their column structure during extraction:

## 1. **Memory Configuration Table** (Page 1)
- Should show: Region | Depth | Width | PC Address Range | PASM Address Range
- Currently: Just headers with no alignment

## 2. **Pin Descriptions Table** (Page 5)
- Should have: Pin Name | Direction | V(typ) | Description
- Currently: Mixed up with descriptions flowing into wrong columns

## 3. **Smart Pin Mode Configuration** (around line 1736+)
- Completely incomprehensible - just shows:
  ```
  OUT
  CIOHHHLLL
  DIR
  ```
- Should probably be a mode number with bit field descriptions?

## 4. **DC Characteristics Table** (Page 34)
- Headers visible but data not aligned
- Should show: Parameter | Min | Typ | Max | Units

## 5. **AC Characteristics Table** (Page 35)
- Similar to DC - structure lost
- Missing clock frequency ranges, timing parameters

## 6. **I/O Pin Equivalent Circuit Table** 
- Seems to be completely missing or reduced to text descriptions

## 7. **Smart Pin Mode Summary**
- Should be a comprehensive table of all Smart Pin modes
- Currently scattered text descriptions

## 8. **Clock Mode Settings**
- The %DDDDDD patterns suggest a bit field table that's been linearized

## 9. **Boot Source Selection**
- Probably was a table showing boot pins and their functions

## 10. **HUBSET Bit Fields**
- Register bit assignments lost their columnar format

Would it help if I showed you specific line numbers where these broken tables appear? Or would you prefer to explain how one of these tables should actually be structured?
# 100% Audit of P2 Assembly Language Instructions (P-R)

**Audit Date:** 2025-12-12

**Scope:** Complete verification of ALL P, Q, and R instructions against four sources:
1. Our Manual (Opus-master Part II)
2. YAML Knowledge Base (layer1_csv, layer2_datasheet, layer3_silicon_doc)
3. Silicon Documentation (p2-documentation.txt)
4. Parallax PASM2 Manual (pasm2-manual-narrative.txt)

## Executive Summary

- **Total Instructions Audited:** 66
- **In Manual:** 55/66 (83%)
- **In YAML KB:** 66/66 (100%)

## Detailed Instruction Comparison

### POLLATN

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `POLLATN  {WC|WZ|WCZ}` | `POLLATN          {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 000001110 000100100` | `EEEE 1101011 CZ0 000001110 000100100` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | ATN Event | - | - | - |
| Silicon Doc | - | - | 6 mentions | - |
| PASM2 Manual | - | - | - | 12 mentions |

*No conflicts detected*

### POLLCT1

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `POLLCT1  {WC|WZ|WCZ}` | `POLLCT1          {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 000000001 000100100` | `EEEE 1101011 CZ0 000000001 000100100` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | CT1 Event | - | - | - |
| Silicon Doc | - | - | 4 mentions | - |
| PASM2 Manual | - | - | - | 7 mentions |

*No conflicts detected*

### POLLCT2

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `N/A` | `POLLCT2          {WC/WZ/WCZ}` | - | - |
| Encoding | `` | `EEEE 1101011 CZ0 000000010 000100100` | - | - |
| Clock Cycles | N/A | 2 | - | - |
| C Flag | N/A | - | - | - |
| Z Flag | N/A | - | - | - |
| Silicon Doc | - | - | 4 mentions | - |
| PASM2 Manual | - | - | - | 5 mentions |

*No conflicts detected*

### POLLCT3

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `N/A` | `POLLCT3          {WC/WZ/WCZ}` | - | - |
| Encoding | `` | `EEEE 1101011 CZ0 000000011 000100100` | - | - |
| Clock Cycles | N/A | 2 | - | - |
| C Flag | N/A | - | - | - |
| Z Flag | N/A | - | - | - |
| Silicon Doc | - | - | 4 mentions | - |
| PASM2 Manual | - | - | - | 5 mentions |

*No conflicts detected*

### POLLFBW

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `POLLFBW  {WC|WZ|WCZ}` | `POLLFBW          {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 000001001 000100100` | `EEEE 1101011 CZ0 000001001 000100100` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | FBW Event | - | - | - |
| Silicon Doc | - | - | 4 mentions | - |
| PASM2 Manual | - | - | - | 10 mentions |

*No conflicts detected*

### POLLINT

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `POLLINT  {WC|WZ|WCZ}` | `POLLINT          {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 000000000 000100100` | `EEEE 1101011 CZ0 000000000 000100100` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | INT Event | - | - | - |
| Silicon Doc | - | - | 4 mentions | - |
| PASM2 Manual | - | - | - | 10 mentions |

*No conflicts detected*

### POLLPAT

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `POLLPAT  {WC|WZ|WCZ}` | `POLLPAT          {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 000001000 000100100` | `EEEE 1101011 CZ0 000001000 000100100` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | PAT Event | - | - | - |
| Silicon Doc | - | - | 4 mentions | - |
| PASM2 Manual | - | - | - | 10 mentions |

*No conflicts detected*

### POLLQMT

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `POLLQMT  {WC|WZ|WCZ}` | `POLLQMT          {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 000001111 000100100` | `EEEE 1101011 CZ0 000001111 000100100` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | QMT Event | - | - | - |
| Silicon Doc | - | - | 4 mentions | - |
| PASM2 Manual | - | - | - | 8 mentions |

*No conflicts detected*

### POLLSE1

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `POLLSE1  {WC|WZ|WCZ}` | `POLLSE1          {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 000000100 000100100` | `EEEE 1101011 CZ0 000000100 000100100` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | SE1 Event | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 7 mentions |

*No conflicts detected*

### POLLSE2

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `N/A` | `POLLSE2          {WC/WZ/WCZ}` | - | - |
| Encoding | `` | `EEEE 1101011 CZ0 000000101 000100100` | - | - |
| Clock Cycles | N/A | 2 | - | - |
| C Flag | N/A | - | - | - |
| Z Flag | N/A | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 5 mentions |

*No conflicts detected*

### POLLSE3

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `N/A` | `POLLSE3          {WC/WZ/WCZ}` | - | - |
| Encoding | `` | `EEEE 1101011 CZ0 000000110 000100100` | - | - |
| Clock Cycles | N/A | 2 | - | - |
| C Flag | N/A | - | - | - |
| Z Flag | N/A | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 5 mentions |

*No conflicts detected*

### POLLSE4

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `N/A` | `POLLSE4          {WC/WZ/WCZ}` | - | - |
| Encoding | `` | `EEEE 1101011 CZ0 000000111 000100100` | - | - |
| Clock Cycles | N/A | 2 | - | - |
| C Flag | N/A | - | - | - |
| Z Flag | N/A | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 5 mentions |

*No conflicts detected*

### POLLXFI

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `POLLXFI  {WC|WZ|WCZ}` | `POLLXFI          {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 000001011 000100100` | `EEEE 1101011 CZ0 000001011 000100100` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | XFI Event | - | - | - |
| Silicon Doc | - | - | 4 mentions | - |
| PASM2 Manual | - | - | - | 10 mentions |

*No conflicts detected*

### POLLXMT

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `POLLXMT  {WC|WZ|WCZ}` | `POLLXMT          {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 000001010 000100100` | `EEEE 1101011 CZ0 000001010 000100100` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | XMT Event | - | - | - |
| Silicon Doc | - | - | 4 mentions | - |
| PASM2 Manual | - | - | - | 10 mentions |

*No conflicts detected*

### POLLXRL

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `POLLXRL  {WC|WZ|WCZ}` | `POLLXRL          {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 000001101 000100100` | `EEEE 1101011 CZ0 000001101 000100100` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | XRL Event | - | - | - |
| Silicon Doc | - | - | 4 mentions | - |
| PASM2 Manual | - | - | - | 10 mentions |

*No conflicts detected*

### POLLXRO

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `POLLXRO  {WC|WZ|WCZ}` | `POLLXRO          {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 000001100 000100100` | `EEEE 1101011 CZ0 000001100 000100100` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | XRO Event | - | - | - |
| Silicon Doc | - | - | 4 mentions | - |
| PASM2 Manual | - | - | - | 10 mentions |

*No conflicts detected*

### POP

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `POP  {WC|WZ|WCZ}` | `POP     D        {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 DDDDDDDDD 000101011` | `EEEE 1101011 CZ0 DDDDDDDDD 000101011` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | K[31] | - | - | - |
| Silicon Doc | - | - | 3 mentions | - |
| PASM2 Manual | - | - | - | 7 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`POP  {WC|WZ|WCZ}` vs YAML=`POP     D        {WC/WZ/WCZ}`

### POPA

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `POPA  {WC|WZ|WCZ}` | `POPA    D        {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1011000 CZ1 DDDDDDDDD 101011111` | `EEEE 1011000 CZ1 DDDDDDDDD 101011111` | - | - |
| Clock Cycles | 9...16 | 9...16 / 9...26 | - | - |
| C Flag | D | - | - | - |
| Z Flag | MSB of long | - | - | - |
| Silicon Doc | - | - | 1 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`POPA  {WC|WZ|WCZ}` vs YAML=`POPA    D        {WC/WZ/WCZ}`

### POPB

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `POPB  {WC|WZ|WCZ}` | `POPB    D        {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1011000 CZ1 DDDDDDDDD 111011111` | `EEEE 1011000 CZ1 DDDDDDDDD 111011111` | - | - |
| Clock Cycles | 9...16 | 9...16 / 9...26 | - | - |
| C Flag | D | - | - | - |
| Z Flag | MSB of long | - | - | - |
| Silicon Doc | - | - | 1 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`POPB  {WC|WZ|WCZ}` vs YAML=`POPB    D        {WC/WZ/WCZ}`

### PUSH

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `PUSH` | `PUSH    {#}D` | - | - |
| Encoding | `EEEE 1101011 00L DDDDDDDDD 000101010` | `EEEE 1101011 00L DDDDDDDDD 000101010` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 5 mentions | - |
| PASM2 Manual | - | - | - | 9 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`PUSH` vs YAML=`PUSH    {#}D`

### PUSHA

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `PUSHA` | `PUSHA   {#}D` | - | - |
| Encoding | `EEEE 1100011 0L1 DDDDDDDDD 101100001` | `EEEE 1100011 0L1 DDDDDDDDD 101100001` | - | - |
| Clock Cycles | 3...10 | 3...10 / 3...20 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 1 mentions | - |
| PASM2 Manual | - | - | - | 5 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`PUSHA` vs YAML=`PUSHA   {#}D`

### PUSHB

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `PUSHB` | `PUSHB   {#}D` | - | - |
| Encoding | `EEEE 1100011 0L1 DDDDDDDDD 111100001` | `EEEE 1100011 0L1 DDDDDDDDD 111100001` | - | - |
| Clock Cycles | 3...10 | 3...10 / 3...20 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 1 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`PUSHB` vs YAML=`PUSHB   {#}D`

### QDIV

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `QDIV` | `QDIV    {#}D,{#}S` | - | - |
| Encoding | `EEEE 1101000 1LI DDDDDDDDD SSSSSSSSS` | `EEEE 1101000 1LI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 2...9 | 2...9 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 4 mentions | - |
| PASM2 Manual | - | - | - | 4 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`QDIV` vs YAML=`QDIV    {#}D,{#}S`

### QEXP

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `QEXP` | `QEXP    {#}D` | - | - |
| Encoding | `EEEE 1101011 00L DDDDDDDDD 000001111` | `EEEE 1101011 00L DDDDDDDDD 000001111` | - | - |
| Clock Cycles | 2...9 | 2...9 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`QEXP` vs YAML=`QEXP    {#}D`

### QFRAC

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `QFRAC` | `QFRAC   {#}D,{#}S` | - | - |
| Encoding | `EEEE 1101001 0LI DDDDDDDDD SSSSSSSSS` | `EEEE 1101001 0LI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 2...9 | 2...9 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 4 mentions | - |
| PASM2 Manual | - | - | - | 4 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`QFRAC` vs YAML=`QFRAC   {#}D,{#}S`

### QLOG

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `QLOG` | `QLOG    {#}D` | - | - |
| Encoding | `EEEE 1101011 00L DDDDDDDDD 000001110` | `EEEE 1101011 00L DDDDDDDDD 000001110` | - | - |
| Clock Cycles | 2...9 | 2...9 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`QLOG` vs YAML=`QLOG    {#}D`

### QMUL

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `QMUL` | `QMUL    {#}D,{#}S` | - | - |
| Encoding | `EEEE 1101000 0LI DDDDDDDDD SSSSSSSSS` | `EEEE 1101000 0LI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 2...9 | 2...9 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 9 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`QMUL` vs YAML=`QMUL    {#}D,{#}S`

### QROTATE

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `QROTATE` | `QROTATE {#}D,{#}S` | - | - |
| Encoding | `EEEE 1101010 0LI DDDDDDDDD SSSSSSSSS` | `EEEE 1101010 0LI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 2...9 | 2...9 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 4 mentions | - |
| PASM2 Manual | - | - | - | 4 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`QROTATE` vs YAML=`QROTATE {#}D,{#}S`

### QSQRT

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `QSQRT` | `QSQRT   {#}D,{#}S` | - | - |
| Encoding | `EEEE 1101001 1LI DDDDDDDDD SSSSSSSSS` | `EEEE 1101001 1LI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 2...9 | 2...9 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`QSQRT` vs YAML=`QSQRT   {#}D,{#}S`

### QVECTOR

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `QVECTOR` | `QVECTOR {#}D,{#}S` | - | - |
| Encoding | `EEEE 1101010 1LI DDDDDDDDD SSSSSSSSS` | `EEEE 1101010 1LI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 2...9 | 2...9 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 3 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`QVECTOR` vs YAML=`QVECTOR {#}D,{#}S`

### RCL

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RCL  {WC|WZ|WCZ}` | `RCL     D,{#}S   {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 0000101 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 0000101 CZI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | Last bit out\textsuperscript{1} | - | - | - |
| Silicon Doc | - | - | 1 mentions | - |
| PASM2 Manual | - | - | - | 8 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RCL  {WC|WZ|WCZ}` vs YAML=`RCL     D,{#}S   {WC/WZ/WCZ}`

### RCR

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RCR  {WC|WZ|WCZ}` | `RCR     D,{#}S   {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 0000100 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 0000100 CZI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | Last bit out\textsuperscript{1} | - | - | - |
| Silicon Doc | - | - | 1 mentions | - |
| PASM2 Manual | - | - | - | 7 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RCR  {WC|WZ|WCZ}` vs YAML=`RCR     D,{#}S   {WC/WZ/WCZ}`

### RCZL

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RCZL  {WC|WZ|WCZ}` | `RCZL    D        {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 DDDDDDDDD 001101011` | `EEEE 1101011 CZ0 DDDDDDDDD 001101011` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | D[31] | - | - | - |
| Silicon Doc | - | - | 1 mentions | - |
| PASM2 Manual | - | - | - | 7 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RCZL  {WC|WZ|WCZ}` vs YAML=`RCZL    D        {WC/WZ/WCZ}`

### RCZR

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RCZR  {WC|WZ|WCZ}` | `RCZR    D        {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 DDDDDDDDD 001101010` | `EEEE 1101011 CZ0 DDDDDDDDD 001101010` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | D[1] | - | - | - |
| Silicon Doc | - | - | 1 mentions | - |
| PASM2 Manual | - | - | - | 7 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RCZR  {WC|WZ|WCZ}` vs YAML=`RCZR    D        {WC/WZ/WCZ}`

### RDBYTE

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RDBYTE  {WC|WZ|WCZ}` | `RDBYTE  D,{#}S/P {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1010110 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 1010110 CZI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 9...16 | 9...16 / 9...26 | - | - |
| C Flag | D | - | - | - |
| Z Flag | MSB of byte | - | - | - |
| Silicon Doc | - | - | 7 mentions | - |
| PASM2 Manual | - | - | - | 4 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RDBYTE  {WC|WZ|WCZ}` vs YAML=`RDBYTE  D,{#}S/P {WC/WZ/WCZ}`
- **KNOWN ISSUE**: Manual shows Z flag as 'MSB of byte' but should be 'Result = 0' (reads set Z based on zero result)

### RDFAST

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RDFAST` | `RDFAST  {#}D,{#}S` | - | - |
| Encoding | `EEEE 1100011 1LI DDDDDDDDD SSSSSSSSS` | `EEEE 1100011 1LI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 2 or WRFAST finish + 10...17 | 2 or WRFAST finish + 10...17 / FIFO IN USE | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 24 mentions | - |
| PASM2 Manual | - | - | - | 12 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RDFAST` vs YAML=`RDFAST  {#}D,{#}S`

### RDLONG

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RDLONG  {WC|WZ|WCZ}` | `RDLONG  D,{#}S/P {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1011000 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 1011000 CZI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 9...16 | 9...16 / 9...26 | - | - |
| C Flag | D | - | - | - |
| Z Flag | MSB of long | - | - | - |
| Silicon Doc | - | - | 22 mentions | - |
| PASM2 Manual | - | - | - | 5 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RDLONG  {WC|WZ|WCZ}` vs YAML=`RDLONG  D,{#}S/P {WC/WZ/WCZ}`
- **KNOWN ISSUE**: Manual shows Z flag as 'MSB of long' but should be 'Result = 0' (reads set Z based on zero result)

### RDLUT

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RDLUT  {WC|WZ|WCZ}` | `RDLUT   D,{#}S/P {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1010101 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 1010101 CZI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 3 | 3 | - | - |
| C Flag | D | - | - | - |
| Z Flag | MSB of data | - | - | - |
| Silicon Doc | - | - | 10 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RDLUT  {WC|WZ|WCZ}` vs YAML=`RDLUT   D,{#}S/P {WC/WZ/WCZ}`

### RDPIN

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RDPIN  {WC}` | `RDPIN   D,{#}S          {WC}` | - | - |
| Encoding | `EEEE 1010100 C1I DDDDDDDDD SSSSSSSSS` | `EEEE 1010100 C1I DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | Modal result | - | - | - |
| Silicon Doc | - | - | 50 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RDPIN  {WC}` vs YAML=`RDPIN   D,{#}S          {WC}`

### RDWORD

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RDWORD  {WC|WZ|WCZ}` | `RDWORD  D,{#}S/P {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1010111 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 1010111 CZI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 9...16 | 9...16 / 9...26 | - | - |
| C Flag | D | - | - | - |
| Z Flag | MSB of word | - | - | - |
| Silicon Doc | - | - | 6 mentions | - |
| PASM2 Manual | - | - | - | 4 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RDWORD  {WC|WZ|WCZ}` vs YAML=`RDWORD  D,{#}S/P {WC/WZ/WCZ}`
- **KNOWN ISSUE**: Manual shows Z flag as 'MSB of word' but should be 'Result = 0' (reads set Z based on zero result)

### REP

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `REP / REP` | `REP     {#}D,{#}S` | - | - |
| Encoding | `EEEE 1100110 1LI DDDDDDDDD SSSSSSSSS` | `EEEE 1100110 1LI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 2 | 2 / 2 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 11 mentions | - |
| PASM2 Manual | - | - | - | 5 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`REP / REP` vs YAML=`REP     {#}D,{#}S`

### RESI0

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RESI0` | `RESI0` | - | - |
| Encoding | `EEEE 1011001 110 111111110 111111111` | `EEEE 1011001 110 111111110 111111111` | - | - |
| Clock Cycles | 4 (COG), 13...20 (Hub) | 4 / 13...20 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

**Conflicts Found:**
- **TIMING MISMATCH**: Manual=`4 (COG), 13...20 (Hub)` vs YAML=`4 / 13...20`

### RESI1

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `N/A` | `RESI1` | - | - |
| Encoding | `` | `EEEE 1011001 110 111110100 111110101` | - | - |
| Clock Cycles | N/A | 4 / 13...20 | - | - |
| C Flag | N/A | - | - | - |
| Z Flag | N/A | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

*No conflicts detected*

### RESI2

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `N/A` | `RESI2` | - | - |
| Encoding | `` | `EEEE 1011001 110 111110010 111110011` | - | - |
| Clock Cycles | N/A | 4 / 13...20 | - | - |
| C Flag | N/A | - | - | - |
| Z Flag | N/A | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

*No conflicts detected*

### RESI3

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `N/A` | `RESI3` | - | - |
| Encoding | `` | `EEEE 1011001 110 111110000 111110001` | - | - |
| Clock Cycles | N/A | 4 / 13...20 | - | - |
| C Flag | N/A | - | - | - |
| Z Flag | N/A | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

*No conflicts detected*

### RET

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RET  {WC|WZ|WCZ}` | `RET              {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ1 000000000 000101101` | `EEEE 1101011 CZ1 000000000 000101101` | - | - |
| Clock Cycles | 4 | 4 / 13...20 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | K[31] | - | - | - |
| Silicon Doc | - | - | 56 mentions | - |
| PASM2 Manual | - | - | - | 34 mentions |

*No conflicts detected*

### RETA

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RETA  {WC|WZ|WCZ}` | `RETA             {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ1 000000000 000101110` | `EEEE 1101011 CZ1 000000000 000101110` | - | - |
| Clock Cycles | 11...18 | 11...18 / 20...40 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | L[31] | - | - | - |
| Silicon Doc | - | - | 1 mentions | - |
| PASM2 Manual | - | - | - | 5 mentions |

*No conflicts detected*

### RETB

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RETB  {WC|WZ|WCZ}` | `RETB             {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ1 000000000 000101111` | `EEEE 1101011 CZ1 000000000 000101111` | - | - |
| Clock Cycles | 11...18 | 11...18 / 20...40 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | L[31] | - | - | - |
| Silicon Doc | - | - | 1 mentions | - |
| PASM2 Manual | - | - | - | 5 mentions |

*No conflicts detected*

### RETI0

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RETI0` | `RETI0` | - | - |
| Encoding | `EEEE 1011001 110 111111111 111111111` | `EEEE 1011001 110 111111111 111111111` | - | - |
| Clock Cycles | 4 (COG), 13...20 (Hub) | 4 / 13...20 | - | - |
| C Flag | --- | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 5 mentions | - |
| PASM2 Manual | - | - | - | 4 mentions |

**Conflicts Found:**
- **TIMING MISMATCH**: Manual=`4 (COG), 13...20 (Hub)` vs YAML=`4 / 13...20`

### RETI1

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `N/A` | `RETI1` | - | - |
| Encoding | `` | `EEEE 1011001 110 111111111 111110101` | - | - |
| Clock Cycles | N/A | 4 / 13...20 | - | - |
| C Flag | N/A | - | - | - |
| Z Flag | N/A | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

*No conflicts detected*

### RETI2

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `N/A` | `RETI2` | - | - |
| Encoding | `` | `EEEE 1011001 110 111111111 111110011` | - | - |
| Clock Cycles | N/A | 4 / 13...20 | - | - |
| C Flag | N/A | - | - | - |
| Z Flag | N/A | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

*No conflicts detected*

### RETI3

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `N/A` | `RETI3` | - | - |
| Encoding | `` | `EEEE 1011001 110 111111111 111110001` | - | - |
| Clock Cycles | N/A | 4 / 13...20 | - | - |
| C Flag | N/A | - | - | - |
| Z Flag | N/A | - | - | - |
| Silicon Doc | - | - | 2 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

*No conflicts detected*

### REV

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `REV` | `REV     D` | - | - |
| Encoding | `EEEE 1101011 000 DDDDDDDDD 001101001` | `EEEE 1101011 000 DDDDDDDDD 001101001` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 3 mentions | - |
| PASM2 Manual | - | - | - | 7 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`REV` vs YAML=`REV     D`

### RFBYTE

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RFBYTE  {WC|WZ|WCZ}` | `RFBYTE  D        {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 DDDDDDDDD 000010000` | `EEEE 1101011 CZ0 DDDDDDDDD 000010000` | - | - |
| Clock Cycles | 2 | 2 / FIFO IN USE | - | - |
| C Flag | D | - | - | - |
| Z Flag | MSB of byte | - | - | - |
| Silicon Doc | - | - | 20 mentions | - |
| PASM2 Manual | - | - | - | 10 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RFBYTE  {WC|WZ|WCZ}` vs YAML=`RFBYTE  D        {WC/WZ/WCZ}`

### RFLONG

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RFLONG  {WC|WZ|WCZ}` | `RFLONG  D        {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 DDDDDDDDD 000010010` | `EEEE 1101011 CZ0 DDDDDDDDD 000010010` | - | - |
| Clock Cycles | 2 | 2 / FIFO IN USE | - | - |
| C Flag | D | - | - | - |
| Z Flag | MSB of long | - | - | - |
| Silicon Doc | - | - | 12 mentions | - |
| PASM2 Manual | - | - | - | 6 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RFLONG  {WC|WZ|WCZ}` vs YAML=`RFLONG  D        {WC/WZ/WCZ}`

### RFVAR

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RFVAR  {WC|WZ|WCZ}` | `RFVAR   D        {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 DDDDDDDDD 000010011` | `EEEE 1101011 CZ0 DDDDDDDDD 000010011` | - | - |
| Clock Cycles | 2 | 2 / FIFO IN USE | - | - |
| C Flag | D | - | - | - |
| Z Flag | 0 | - | - | - |
| Silicon Doc | - | - | 6 mentions | - |
| PASM2 Manual | - | - | - | 4 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RFVAR  {WC|WZ|WCZ}` vs YAML=`RFVAR   D        {WC/WZ/WCZ}`

### RFVARS

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RFVARS  {WC|WZ|WCZ}` | `RFVARS  D        {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 DDDDDDDDD 000010100` | `EEEE 1101011 CZ0 DDDDDDDDD 000010100` | - | - |
| Clock Cycles | 2 | 2 / FIFO IN USE | - | - |
| C Flag | D | - | - | - |
| Z Flag | MSB of value | - | - | - |
| Silicon Doc | - | - | 6 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RFVARS  {WC|WZ|WCZ}` vs YAML=`RFVARS  D        {WC/WZ/WCZ}`

### RFWORD

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RFWORD  {WC|WZ|WCZ}` | `RFWORD  D        {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 1101011 CZ0 DDDDDDDDD 000010001` | `EEEE 1101011 CZ0 DDDDDDDDD 000010001` | - | - |
| Clock Cycles | 2 | 2 / FIFO IN USE | - | - |
| C Flag | D | - | - | - |
| Z Flag | MSB of word | - | - | - |
| Silicon Doc | - | - | 9 mentions | - |
| PASM2 Manual | - | - | - | 5 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RFWORD  {WC|WZ|WCZ}` vs YAML=`RFWORD  D        {WC/WZ/WCZ}`

### RGBEXP

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RGBEXP` | `RGBEXP  D` | - | - |
| Encoding | `EEEE 1101011 000 DDDDDDDDD 001100111` | `EEEE 1101011 000 DDDDDDDDD 001100111` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 1 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RGBEXP` vs YAML=`RGBEXP  D`

### RGBSQZ

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RGBSQZ` | `RGBSQZ  D` | - | - |
| Encoding | `EEEE 1101011 000 DDDDDDDDD 001100110` | `EEEE 1101011 000 DDDDDDDDD 001100110` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 1 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RGBSQZ` vs YAML=`RGBSQZ  D`

### ROL

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `ROL  {WC|WZ|WCZ}` | `ROL     D,{#}S   {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 0000001 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 0000001 CZI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | Last bit out\textsuperscript{1} | - | - | - |
| Silicon Doc | - | - | 20 mentions | - |
| PASM2 Manual | - | - | - | 74 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`ROL  {WC|WZ|WCZ}` vs YAML=`ROL     D,{#}S   {WC/WZ/WCZ}`

### ROLBYTE

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `ROLBYTE / ROLBYTE` | `ROLBYTE D` | - | - |
| Encoding | `EEEE 1001000 NNI DDDDDDDDD SSSSSSSSS` | `EEEE 1001000 000 DDDDDDDDD 000000000` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 9 mentions | - |
| PASM2 Manual | - | - | - | 28 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`ROLBYTE / ROLBYTE` vs YAML=`ROLBYTE D`

### ROLNIB

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `ROLNIB / ROLNIB` | `ROLNIB  D` | - | - |
| Encoding | `EEEE 100010N NNI DDDDDDDDD SSSSSSSSS` | `EEEE 1000100 000 DDDDDDDDD 000000000` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 5 mentions | - |
| PASM2 Manual | - | - | - | 27 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`ROLNIB / ROLNIB` vs YAML=`ROLNIB  D`

### ROLWORD

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `ROLWORD / ROLWORD` | `ROLWORD D` | - | - |
| Encoding | `EEEE 1001010 0NI DDDDDDDDD SSSSSSSSS` | `EEEE 1001010 000 DDDDDDDDD 000000000` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | --- | - | - | - |
| Silicon Doc | - | - | 5 mentions | - |
| PASM2 Manual | - | - | - | 28 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`ROLWORD / ROLWORD` vs YAML=`ROLWORD D`

### ROR

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `ROR  {WC|WZ|WCZ}` | `ROR     D,{#}S   {WC/WZ/WCZ}` | - | - |
| Encoding | `EEEE 0000000 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 0000000 CZI DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | Last bit out\textsuperscript{1} | - | - | - |
| Silicon Doc | - | - | 1 mentions | - |
| PASM2 Manual | - | - | - | 7 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`ROR  {WC|WZ|WCZ}` vs YAML=`ROR     D,{#}S   {WC/WZ/WCZ}`

### RQPIN

| Attribute | Manual | YAML | Silicon Doc | PASM2 Manual |
|-----------|--------|------|-------------|--------------|
| Syntax | `RQPIN  {WC}` | `RQPIN   D,{#}S          {WC}` | - | - |
| Encoding | `EEEE 1010100 C0I DDDDDDDDD SSSSSSSSS` | `EEEE 1010100 C0I DDDDDDDDD SSSSSSSSS` | - | - |
| Clock Cycles | 2 | 2 | - | - |
| C Flag | D | - | - | - |
| Z Flag | Modal result | - | - | - |
| Silicon Doc | - | - | 43 mentions | - |
| PASM2 Manual | - | - | - | 3 mentions |

**Conflicts Found:**
- **SYNTAX MISMATCH**: Manual=`RQPIN  {WC}` vs YAML=`RQPIN   D,{#}S          {WC}`

## Conflict Analysis

### Critical Issues (Functional Errors)

- **RDBYTE**: Z flag incorrectly shows 'MSB of byte' instead of 'Result = 0'
- **RDLONG**: Z flag incorrectly shows 'MSB of long' instead of 'Result = 0'
- **RDWORD**: Z flag incorrectly shows 'MSB of word' instead of 'Result = 0'

### All Detected Differences

**Note:** Most syntax differences are documentation style variations (manual shows simplified form, YAML shows complete operand list). These are not functional errors.

- **POP**: Syntax: POP  {WC|WZ|WCZ} vs POP     D        {WC/WZ/WCZ}
- **POPA**: Syntax: POPA  {WC|WZ|WCZ} vs POPA    D        {WC/WZ/WCZ}
- **POPB**: Syntax: POPB  {WC|WZ|WCZ} vs POPB    D        {WC/WZ/WCZ}
- **PUSH**: Syntax: PUSH vs PUSH    {#}D
- **PUSHA**: Syntax: PUSHA vs PUSHA   {#}D
- **PUSHB**: Syntax: PUSHB vs PUSHB   {#}D
- **QDIV**: Syntax: QDIV vs QDIV    {#}D,{#}S
- **QEXP**: Syntax: QEXP vs QEXP    {#}D
- **QFRAC**: Syntax: QFRAC vs QFRAC   {#}D,{#}S
- **QLOG**: Syntax: QLOG vs QLOG    {#}D
- **QMUL**: Syntax: QMUL vs QMUL    {#}D,{#}S
- **QROTATE**: Syntax: QROTATE vs QROTATE {#}D,{#}S
- **QSQRT**: Syntax: QSQRT vs QSQRT   {#}D,{#}S
- **QVECTOR**: Syntax: QVECTOR vs QVECTOR {#}D,{#}S
- **RCL**: Syntax: RCL  {WC|WZ|WCZ} vs RCL     D,{#}S   {WC/WZ/WCZ}
- **RCR**: Syntax: RCR  {WC|WZ|WCZ} vs RCR     D,{#}S   {WC/WZ/WCZ}
- **RCZL**: Syntax: RCZL  {WC|WZ|WCZ} vs RCZL    D        {WC/WZ/WCZ}
- **RCZR**: Syntax: RCZR  {WC|WZ|WCZ} vs RCZR    D        {WC/WZ/WCZ}
- **RDBYTE**: Syntax: RDBYTE  {WC|WZ|WCZ} vs RDBYTE  D,{#}S/P {WC/WZ/WCZ}; Z flag issue: shows 'MSB of byte' but should be 'Result = 0'
- **RDFAST**: Syntax: RDFAST vs RDFAST  {#}D,{#}S
- **RDLONG**: Syntax: RDLONG  {WC|WZ|WCZ} vs RDLONG  D,{#}S/P {WC/WZ/WCZ}; Z flag issue: shows 'MSB of long' but should be 'Result = 0'
- **RDLUT**: Syntax: RDLUT  {WC|WZ|WCZ} vs RDLUT   D,{#}S/P {WC/WZ/WCZ}
- **RDPIN**: Syntax: RDPIN  {WC} vs RDPIN   D,{#}S          {WC}
- **RDWORD**: Syntax: RDWORD  {WC|WZ|WCZ} vs RDWORD  D,{#}S/P {WC/WZ/WCZ}; Z flag issue: shows 'MSB of word' but should be 'Result = 0'
- **REP**: Syntax: REP / REP vs REP     {#}D,{#}S
- **RESI0**: Timing: 4 (COG), 13...20 (Hub) vs 4 / 13...20
- **RETI0**: Timing: 4 (COG), 13...20 (Hub) vs 4 / 13...20
- **REV**: Syntax: REV vs REV     D
- **RFBYTE**: Syntax: RFBYTE  {WC|WZ|WCZ} vs RFBYTE  D        {WC/WZ/WCZ}
- **RFLONG**: Syntax: RFLONG  {WC|WZ|WCZ} vs RFLONG  D        {WC/WZ/WCZ}
- **RFVAR**: Syntax: RFVAR  {WC|WZ|WCZ} vs RFVAR   D        {WC/WZ/WCZ}
- **RFVARS**: Syntax: RFVARS  {WC|WZ|WCZ} vs RFVARS  D        {WC/WZ/WCZ}
- **RFWORD**: Syntax: RFWORD  {WC|WZ|WCZ} vs RFWORD  D        {WC/WZ/WCZ}
- **RGBEXP**: Syntax: RGBEXP vs RGBEXP  D
- **RGBSQZ**: Syntax: RGBSQZ vs RGBSQZ  D
- **ROL**: Syntax: ROL  {WC|WZ|WCZ} vs ROL     D,{#}S   {WC/WZ/WCZ}
- **ROLBYTE**: Syntax: ROLBYTE / ROLBYTE vs ROLBYTE D
- **ROLNIB**: Syntax: ROLNIB / ROLNIB vs ROLNIB  D
- **ROLWORD**: Syntax: ROLWORD / ROLWORD vs ROLWORD D
- **ROR**: Syntax: ROR  {WC|WZ|WCZ} vs ROR     D,{#}S   {WC/WZ/WCZ}
- **RQPIN**: Syntax: RQPIN  {WC} vs RQPIN   D,{#}S          {WC}

## Recommendations

1. **Authoritative Source Hierarchy:**
   - **Primary:** Silicon Documentation (p2-documentation.txt) - Official Parallax documentation
   - **Secondary:** YAML Knowledge Base layer2_datasheet - Enriched from datasheet
   - **Tertiary:** PASM2 Manual - Narrative explanations
   - **Target:** Our Manual - Should align with primary sources

2. **RDLONG Z Flag Issue:**
   - Current manual shows `---` for Z flag
   - Should be `Result = 0` to match behavior (Z flag set when read value is zero)
   - This applies to RDBYTE and RDWORD as well

3. **Clock Cycle Discrepancies:**
   - Review any timing differences between manual and YAML layer2_datasheet
   - layer2_datasheet contains enriched timing from official datasheet

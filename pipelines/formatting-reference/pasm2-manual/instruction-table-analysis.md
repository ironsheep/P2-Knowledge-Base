# PASM2 Instruction Table Format Analysis

**Detailed analysis of instruction reference table formatting from official Parallax manual**

---

## 📊 **Table Structure Analysis**

### **ADD Instruction Format** (add-instruction-table-format.png)

#### **Instruction Header**
- **Instruction name**: "ADD" - Large, bold, black text
- **Category link**: "Math Instruction" - Blue hyperlink
- **Description**: "Add two unsigned values." - Regular text

#### **Syntax Line**
- **Format**: `ADD Dest, {#}Src {WC|WZ|WCZ}`
- **Monospace font**: Technical syntax in monospace/fixed-width font
- **Gray background**: Light gray background bar for syntax

#### **Main Information Table**
**Table styling**:
- **Headers**: Gray background (#E8E8E8 or similar)
- **Borders**: Black thin borders, clean lines
- **Column headers**: COND | INSTR | FX | DEST | SRC | Write | C Flag | Z Flag | Clocks
- **Data row**: White background with black text
- **Encoding**: `EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS`

#### **Content Structure**
1. **Result explanation**: Clear description of what the instruction does
2. **Bullet points**: Clean formatting for parameter explanations
3. **Related instructions**: Blue hyperlinks to related instructions (ADDX, ADDS, ADDSX, SUB)
4. **Detailed explanation**: Paragraph format with technical details
5. **Flag behavior**: Detailed explanation of C and Z flag behavior

---

## 📊 **ADDCT1/2/3 Instruction Format** (addct-instruction-table-format.png)

#### **Multi-Instruction Header**
- **Instruction group**: "ADDCT1/2/3" - Large, bold
- **Description**: "Add counter 1/2/3" 
- **Category link**: "Event Handling Instruction" - Blue hyperlink

#### **Multi-Syntax Format**
```
ADDCT1 Dest, {#}Src
ADDCT2 Dest, {#}Src  
ADDCT3 Dest, {#}Src
```
- **Multiple syntax lines**: Each variant clearly listed
- **Consistent formatting**: Same monospace font and alignment

#### **Expanded Information Table**
**Multiple rows for variants**:
- **ADDCT1**: `EEEE 1010011 00I DDDDDDDDD SSSSSSSSS | D | — | — | 2`
- **ADDCT2**: `EEEE 1010011 01I DDDDDDDDD SSSSSSSSS | D | — | — | 2`  
- **ADDCT3**: `EEEE 1010011 10I DDDDDDDDD SSSSSSSSS | D | — | — | 2`

**Table features**:
- **Same column structure** as ADD instruction
- **Multiple encoding rows** for instruction variants
- **Consistent styling** - same gray headers, black borders
- **Em dashes (—)** for unused flag columns

---

## 🎨 **Visual Design Elements**

### **Typography Hierarchy**
1. **Instruction Name**: ~18pt bold, black
2. **Category Link**: ~11pt regular, blue (#0066CC)
3. **Description**: ~11pt regular, black
4. **Syntax**: ~10pt monospace, black text on light gray background
5. **Table Headers**: ~9pt bold, black text on gray background
6. **Table Data**: ~9pt regular, black text on white background
7. **Body Text**: ~11pt regular, black
8. **Hyperlinks**: ~11pt regular, blue (#0066CC)

### **Color Scheme**
- **Text**: Black (#000000)
- **Hyperlinks**: Blue (#0066CC - Parallax blue)
- **Table headers**: Light gray background (#E8E8E8)
- **Syntax background**: Light gray (#F5F5F5)
- **Table borders**: Black (#000000)
- **Background**: White (#FFFFFF)

### **Spacing & Layout**
- **Section spacing**: Generous white space between sections
- **Table margins**: Clean margins around tables
- **Line height**: ~1.4x for body text readability
- **Table cell padding**: Adequate internal padding for readability

---

## 📋 **Template Requirements**

### **LaTeX Implementation Needs**
1. **Custom instruction table environment**
   - Gray headers with proper formatting
   - Multiple instruction variant support
   - Monospace encoding display
   - Proper column alignment

2. **Syntax formatting command**
   - Light gray background
   - Monospace font
   - Proper horizontal spacing

3. **Hyperlink styling**
   - Parallax blue color
   - Underline or no-underline (needs verification)
   - Consistent with overall design

4. **Multi-instruction support**
   - Handle instruction variants (ADDCT1/2/3)
   - Multiple syntax lines
   - Multiple table rows with same styling

### **Table Column Specifications**
```
COND    | INSTR  | FX  | DEST      | SRC       | Write | C Flag | Z Flag | Clocks
~8%     | ~12%   | ~6% | ~15%      | ~15%      | ~8%   | ~12%   | ~12%   | ~8%
```

This analysis provides the detailed specifications needed to create pixel-perfect instruction reference tables in our P2KB template system.
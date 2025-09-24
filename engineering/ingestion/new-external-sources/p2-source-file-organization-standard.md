# P2 Source File Organization Standard
## Community Best Practices for SPIN2 and PASM2 File Structure

### Overview

This document establishes the **community standard** for organizing P2 source files, regardless of which internal documentation style you choose. These structural conventions ensure that all P2 code follows consistent, professional practices that benefit the entire community.

**Key Principle**: Every P2 source file should be **self-documenting** with proper attribution, clear purpose, and legal compliance.

---

## 1. Universal File Structure

Every P2 source file should follow this organizational pattern:

```spin2
[FILE HEADER - Required]
↓
[CODE SECTIONS - Flexible Organization]
↓  
[LICENSE FOOTER - Required]
```

### Section Organization and Flexibility

**IMPORTANT**: SPIN2 allows **flexible section organization** with these capabilities:

- **CON sections** can be repeated - useful for grouping related constants
- **VAR sections** can be repeated - allows organizing variables by function  
- **DAT sections** can be repeated - enables multiple data/assembly blocks
- **OBJ sections** can be repeated - typically used once but repetition is allowed
- **PUB/PRI sections** are implicit - methods can be mixed throughout

### Standard Single-Section Approach

```spin2
'' [File Header Block]

con { constants and configuration }
  ' Constants, pin assignments, configuration values

dat { shared data and assembly code }  
  ' Shared variables, lookup tables, PASM2 cog code

obj { object dependencies }
  ' Required objects and their purposes

var { instance variables }
  ' Instance-specific state variables

pub [public methods]
  ' Public interface methods

pri [private methods]  
  ' Private helper methods (optional)

con { license }
{{ 
  [License Block]
}}
```

### Functional Grouping Approach (Alternative)

```spin2
'' [File Header Block]

con  ' Core configuration
  MAIN_CLOCK = 200_000_000
  BUFFER_SIZE = 256

obj
  term : "jm_serial"

var  ' Main state variables
  long system_state
  long error_flags

pub start()
pub main_loop()

con  ' Sensor-specific constants
  SENSOR_PIN = 15
  SAMPLE_RATE = 1000

var  ' Sensor variables
  long sensor_reading
  long calibration_offset

pub read_sensor()
pri calibrate_sensor()

dat  ' Sensor lookup table
  calibration_table  long  100, 200, 300, 400

con { license }
{{
  [License Block]
}}
```

---

## 2. File Header Requirements

### Required Header Components

Every P2 source file **must** include these header elements:

#### 1. **File Name Declaration**
```spin2
''   File....... actual_filename.spin2
```
- Must exactly match the actual file name
- Helps identify files when viewing code excerpts
- Critical for debugging and maintenance

#### 2. **Purpose Statement**  
```spin2
''   Purpose.... Clear description of what this object does
```
- One-line preferred, can extend to second line if needed
- Focus on **what** the object provides, not **how** it works
- Should be meaningful to someone seeing the code for the first time

#### 3. **Author Attribution**
```spin2
''   Author..... Full Name "Nickname" LastName
''               Copyright (c) YYYY Full Legal Name
''               -- see below for terms of use
```
- Full name with nickname (if applicable) in quotes
- Copyright year should reflect when code was created/last significantly modified
- Legal name for copyright must match license block
- Reference to license terms creates legal connection

#### 4. **Contact Information** (Recommended)
```spin2
''   E-mail..... author@domain.com
```
- Provides way for community to contact author
- Helpful for reporting issues or requesting enhancements
- Can use GitHub profile or forum username if preferred

#### 5. **Version Information** (Recommended)
```spin2
''   Started.... DD MMM YYYY
''   Updated.... DD MMM YYYY
```
- Started date often omitted if not tracked from beginning
- Updated date should reflect last significant modification
- Date format: DD MMM YYYY (e.g., "15 JUN 2024")

### Header Formatting Standards

#### Standard Header Template:
```spin2
'' =================================================================================================
''
''   File....... filename.spin2
''   Purpose.... Brief but complete description of functionality
''   Author..... Your Name "Nickname" LastName
''               Copyright (c) YYYY Your Legal Name
''               -- see below for terms of use
''   E-mail..... your.email@domain.com
''   Started.... DD MMM YYYY
''   Updated.... DD MMM YYYY
''
'' =================================================================================================
```

#### Formatting Rules:
- **Separator Line**: Use exactly 97 equals signs (`=`) for standard width
- **Double Apostrophes**: All header lines use `''` prefix
- **Dot Leaders**: Minimum 7 dots, extend to align values consistently
- **Blank Lines**: Empty comment lines (`''`) after opening and before closing separators
- **Consistent Alignment**: All values should start at the same column

### Header Examples

#### Minimal Required Header:
```spin2
'' =================================================================================================
''
''   File....... jm_example.spin2
''   Purpose.... Simple example demonstrating basic functionality
''   Author..... Jon "JonnyMac" McPhalen
''               Copyright (c) 2024 Jon McPhalen
''               -- see below for terms of use
''
'' =================================================================================================
```

#### Complete Header with All Optional Fields:
```spin2
'' =================================================================================================
''
''   File....... advanced_sensor.spin2
''   Purpose.... Advanced sensor interface with calibration and filtering
''   Author..... Jane "TechWiz" Smith
''               Copyright (c) 2024 Jane Smith
''               -- see below for terms of use
''   E-mail..... jane.smith@example.com
''   Started.... 15 JAN 2024
''   Updated.... 20 MAR 2024
''   Version.... 2.1
''   Hardware... P2X8C4M64P or compatible
''
'' =================================================================================================
```

---

## 3. Code Section Organization

### Standard Section Order and Purpose

#### CON Section - Constants and Configuration
```spin2
con { constants and configuration }

  ' Hardware pin assignments
  SENSOR_PIN    = 15
  STATUS_LED    = 16
  
  ' Configuration constants
  SAMPLE_RATE   = 1000                  ' samples per second
  BUFFER_SIZE   = 256                   ' must be power of 2
  
  ' Operating parameters
  TIMEOUT_MS    = 5000                  ' 5 second timeout
  MAX_RETRIES   = 3                     ' retry attempts
```

**Best Practices:**
- Group related constants together with comment headers
- Use meaningful names that explain purpose
- Include units in comments (Hz, ms, bytes, etc.)
- Document special requirements (power of 2, valid ranges)

#### DAT Section - Shared Data and Assembly
```spin2
dat { shared data and assembly code }

  ' Shared variables for SPIN2/PASM2 communication
  sensor_reading    long    0           ' latest sensor value
  calibration_data  long    0[16]       ' calibration lookup table
  
  ' Assembly code for time-critical operations
  org
    ' [PASM2 assembly code if needed]
  end
```

**Usage Guidelines:**
- Place variables accessed by both SPIN2 and PASM2 here
- Include lookup tables and constant data arrays
- PASM2 cog code goes here for background operations
- Use clear variable names and document data formats

#### OBJ Section - Object Dependencies
```spin2
obj { object dependencies }

  term    : "jm_serial"                 ' terminal I/O for debugging
  math    : "jm_math_utils"             ' mathematical utility functions  
  sensor  : "advanced_adc"              ' high-resolution ADC interface
```

**Guidelines:**
- List all required objects with clear purpose comments
- Use meaningful instance names, not generic abbreviations
- Consider dependency order if objects depend on each other
- Document why each object is needed

#### VAR Section - Instance Variables  
```spin2
var { instance variables }

  ' Configuration state
  long  operating_mode                  ' current operating mode (0-3)
  long  sample_interval                 ' sampling interval in milliseconds
  
  ' Data buffers  
  long  sample_buffer[BUFFER_SIZE]      ' circular sample buffer
  long  buffer_head                     ' buffer write position
  long  buffer_tail                     ' buffer read position
  
  ' Status tracking
  long  error_flags                     ' error condition bit flags
  long  samples_taken                   ' total samples collected
```

**Organization:**
- Group variables by functional purpose
- Document data types, ranges, and special values
- Explain relationships between related variables
- Use consistent naming conventions

#### PUB Section - Public Methods
```spin2
pub start(mode, pin) : result

'' Initialize sensor interface
'' -- mode: operating mode (0=normal, 1=high-speed, 2=low-power)
'' -- pin: sensor input pin number
'' -- returns 0 for success, error code for failure

pub read_sensor() : value

'' Read current sensor value
'' -- returns calibrated sensor reading (0-1023)

pub stop()

'' Shutdown sensor interface and release resources
```

**Method Organization:**
1. **Main/Entry Point** (if top-level object)
2. **Initialization Methods** (`start`, `begin`, `init`)
3. **Core Functionality** (primary interface methods)
4. **Utility Methods** (helper functions for users)
5. **Status/Query Methods** (`get_status`, `is_ready`, etc.)
6. **Cleanup Methods** (`stop`, `close`, `shutdown`)

#### PRI Section - Private Methods (Optional)
```spin2
pri calculate_average() : result

'' Internal method to calculate running average

pri validate_parameters(mode, pin) : valid

'' Validate initialization parameters
```

**Usage:**
- Include only if needed for code organization
- Document purpose even though methods are private
- Keep private methods focused and single-purpose

---

## 4. License Footer Requirements

### Standard License Block

Every P2 source file **must** end with a license block:

```spin2
con { license }

{{

  Copyright (c) YYYY Your Legal Name

  Terms of Use: MIT License

  Permission is hereby granted, free of charge, to any person obtaining a copy of this
  software and associated documentation files (the "Software"), to deal in the Software
  without restriction, including without limitation the rights to use, copy, modify,
  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so, subject to the following
  conditions:

  The above copyright notice and this permission notice shall be included in all copies
  or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

}}
```

### MIT License Copyright Decoration

The traditional way to decorate the MIT license includes the copyright holder and year at the top:

```spin2
con { license }

{{

  Copyright (c) YYYY Your Legal Name

  Terms of Use: MIT License

  Permission is hereby granted, free of charge, to any person obtaining a copy of this
  software and associated documentation files (the "Software"), to deal in the Software
  without restriction, including without limitation the rights to use, copy, modify,
  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so, subject to the following
  conditions:

  The above copyright notice and this permission notice shall be included in all copies
  or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

}}
```

### License Requirements

1. **Always Include License** - Every source file needs legal terms
2. **Use Standard MIT License** - Community standard for P2 projects
3. **Include Copyright Decoration** - Copyright holder and year at the top of license block
4. **Match Header Copyright** - Copyright year/name must be consistent between header and license
5. **Block Comment Format** - Use `{{ }}` for multi-line license text
6. **End of File Placement** - License block always comes last

### Why License Blocks Matter

- **Legal Protection** - Protects both author and users
- **Clear Usage Terms** - Defines how code can be used/modified/redistributed  
- **Professional Standards** - Shows proper software development practices
- **Community Confidence** - Users know they can safely use the code

---

## 5. Professional Attribution Standards

### Author Attribution Best Practices

#### Full Name with Nickname:
```spin2
''   Author..... Jon "JonnyMac" McPhalen
```
- Helps community members connect code to forum/community identity
- Maintains professional appearance while being personable

#### Multiple Authors:
```spin2
''   Authors.... Jon "JonnyMac" McPhalen (original implementation)
''               Jane Smith (enhancements and optimization)
```
- Credit all significant contributors
- Note specific contributions if helpful

#### Corporate/Organization Attribution:
```spin2
''   Author..... Parallax Inc.
''   Developer.. Jon McPhalen
```
- Clear ownership structure
- Individual developer credit when appropriate

### Copyright Guidelines

#### Single Year:
```spin2
''               Copyright (c) 2024 Author Name
```

#### Range of Years:
```spin2
''               Copyright (c) 2020-2024 Author Name  
```

#### Multiple Copyright Holders:
```spin2
''               Copyright (c) 2024 Original Author
''               Portions Copyright (c) 2024 Contributing Author
```

### Contact Information Standards

#### Email Preferred:
```spin2
''   E-mail..... author@domain.com
```

#### Alternative Contacts:
```spin2
''   GitHub..... github.com/username
''   Forum...... Parallax Forums: @username
```

---

## 6. File Naming and Directory Organization

### File Naming Conventions

#### Standard SPIN2 Files:
- **Format**: `descriptive_name.spin2`
- **Style**: lowercase with underscores
- **Examples**: `sensor_interface.spin2`, `motor_controller.spin2`

#### Object Library Files:
- **Prefix with initials**: `jm_serial.spin2`, `js_math_utils.spin2`
- **Helps identify author/source**
- **Prevents naming conflicts**

#### Project-Specific Files:
- **Include project context**: `robot_main.spin2`, `sensor_test.spin2`
- **Clear purpose identification**

### Directory Structure Recommendations

```
project_name/
├── src/
│   ├── main.spin2              # Top-level application  
│   ├── hardware/
│   │   ├── sensor_driver.spin2 # Hardware interface modules
│   │   └── motor_control.spin2
│   ├── utilities/
│   │   ├── math_helpers.spin2  # Utility functions
│   │   └── string_utils.spin2
│   └── tests/
│       ├── sensor_test.spin2   # Test programs
│       └── motor_test.spin2
├── docs/
│   └── README.md               # Project documentation
└── LICENSE                     # Project-wide license
```

---

## 7. Quality Standards and Compliance

### Pre-Release Checklist

Before sharing P2 source code, verify:

#### File Structure:
- [ ] **Complete file header** with all required components
- [ ] **Proper section organization** (CON, DAT, OBJ, VAR, PUB, PRI)
- [ ] **License block present** at end of file
- [ ] **Consistent formatting** throughout file

#### Attribution:
- [ ] **Author name** matches license copyright
- [ ] **Copyright year** reflects actual development timeframe  
- [ ] **Contact information** current and accessible
- [ ] **Purpose statement** clearly describes functionality

#### Legal Compliance:
- [ ] **MIT license text** exactly matches standard wording
- [ ] **No conflicting license** statements elsewhere in code
- [ ] **All dependencies** properly attributed
- [ ] **Third-party code** properly credited

#### Professional Presentation:
- [ ] **Consistent code style** throughout file
- [ ] **Meaningful variable names** and comments
- [ ] **No profanity** or inappropriate content
- [ ] **Spelling and grammar** checked

### Common Issues to Avoid

#### Header Problems:
- Missing or incomplete file headers
- Copyright year doesn't match development timeline
- File name doesn't match actual filename
- No contact information provided

#### Organization Issues:
- Sections in wrong order
- Mixed public/private methods
- Unclear variable purposes
- Missing object dependencies

#### License Problems:
- No license block at all
- Modified license text
- Copyright mismatch between header and license
- Conflicting license statements

---

## 8. Community Integration

### How This Standard Supports the Community

#### Code Sharing Benefits:
- **Easy identification** of code purpose and author
- **Clear usage terms** reduce legal uncertainty
- **Consistent structure** makes code easier to understand
- **Professional appearance** encourages adoption

#### Maintenance Advantages:
- **Contact information** enables bug reports and questions
- **Update timestamps** help track code currency
- **Clear attribution** prevents ownership confusion
- **Standard structure** simplifies code review

#### Educational Value:
- **Good examples** teach proper software practices
- **Professional standards** elevate community reputation
- **Consistent patterns** reduce learning curve
- **Legal compliance** demonstrates responsibility

### Compatibility with Documentation Styles

This organizational standard works with **any internal documentation style**:

#### With VSCode Spin2 Extension Style:
- File headers provide metadata for hover tooltips
- Method signatures work with IntelliSense
- Comments follow VSCode parsing requirements
- Structure supports extension features

#### With Johnny Mac Documentation Style:
- Headers match Johnny Mac's comprehensive approach
- Section organization follows his proven patterns
- License blocks use his standard MIT implementation
- Professional attribution matches his standards

#### With Other Documentation Approaches:
- Flexible enough for any comment style
- Focuses on structure, not specific documentation format
- Provides foundation that any style can build upon

---

## 9. Implementation Guide

### For New Projects

1. **Start with Template**:
   - Create file template with complete header structure
   - Include standard license block
   - Set up proper section organization

2. **Establish Team Standards**:
   - Agree on naming conventions
   - Set copyright and attribution policies  
   - Create code review checklists

3. **Use Consistent Practices**:
   - Apply same standards to all project files
   - Document team-specific conventions
   - Regular review of compliance

### For Existing Projects

1. **Audit Current Files**:
   - Identify files missing headers
   - Check for inconsistent organization
   - Verify license compliance

2. **Prioritize Updates**:
   - Add headers to public-facing files first
   - Fix legal compliance issues immediately
   - Improve organization during maintenance

3. **Gradual Improvement**:
   - Update files as you modify them
   - Don't try to fix everything at once
   - Focus on files others will use

### Tools and Automation

#### File Templates:
- Create templates for common file types
- Include standard headers and footers
- Customize for team/project needs

#### Verification Scripts:
- Check for required header components
- Validate license block consistency
- Verify section organization

#### Development Environment:
- Configure IDE with standard templates
- Set up linting rules for formatting
- Integration with version control

---

## 10. Examples and Templates

### Complete File Template

```spin2
'' =================================================================================================
''
''   File....... [filename].spin2
''   Purpose.... [Brief description of what this object does]
''   Author..... [Your Name] "[Nickname]" [LastName]
''               Copyright (c) [YYYY] [Your Legal Name]
''               -- see below for terms of use
''   E-mail..... [your.email@domain.com]
''   Started.... [DD MMM YYYY]
''   Updated.... [DD MMM YYYY]
''
'' =================================================================================================


con { constants and configuration }

  ' [Group constants by purpose with descriptive comments]


dat { shared data and assembly code }

  ' [Shared variables for SPIN2/PASM2 communication]
  ' [PASM2 assembly code if needed]


obj { object dependencies }

  ' [Required objects with clear purpose statements]


var { instance variables }

  ' [Instance state variables with clear documentation]


pub main() : result

' [Entry point documentation - style depends on your choice]

  ' [main implementation]


pub start(parameters) : result

' [Initialization method documentation]

  ' [initialization code]


pub stop()

' [Cleanup method documentation]

  ' [cleanup code]


pub [method_name](parameters) : return_values

' [Method documentation using your preferred style]

  ' [method implementation]


pri [helper_method]() : result

' [Private method documentation if needed]

  ' [helper implementation]


con { license }

{{

  Copyright (c) [YYYY] [Your Legal Name]

  Terms of Use: MIT License

  Permission is hereby granted, free of charge, to any person obtaining a copy of this
  software and associated documentation files (the "Software"), to deal in the Software
  without restriction, including without limitation the rights to use, copy, modify,
  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so, subject to the following
  conditions:

  The above copyright notice and this permission notice shall be included in all copies
  or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

}}
```

---

## Conclusion

This P2 Source File Organization Standard provides the **structural foundation** that enables any documentation style to be successful. By establishing consistent requirements for file headers, code organization, and legal attribution, we create a professional framework that benefits the entire P2 community.

### Key Benefits:

- **Universal Structure** - Works with any internal documentation approach
- **Professional Standards** - Elevates the quality of community code
- **Legal Clarity** - Ensures proper attribution and usage terms
- **Easy Maintenance** - Consistent patterns simplify code management
- **Community Growth** - Professional appearance encourages adoption

### Implementation Priority:

1. **File headers** - Most visible improvement with immediate benefit
2. **License blocks** - Essential for legal compliance
3. **Section organization** - Improves code readability and maintenance
4. **Consistent formatting** - Professional polish

By following this standard, P2 developers create code that serves the community well, maintains professional standards, and provides a solid foundation for any documentation style they choose to implement.

---

*This standard is derived from analysis of community best practices and represents the common structural elements found in high-quality P2 source code across multiple documentation styles.*
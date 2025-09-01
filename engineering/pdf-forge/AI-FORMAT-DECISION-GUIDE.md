# AI Format Decision Guide
**Definitive Reference for PDF Forge Request Format Selection**

## 📋 Quick Decision Matrix

| User Intent | Keywords | Format | Script |
|-------------|----------|--------|---------|
| **Create final deliverable** | "generate", "create", "produce", "make" | `document_generation` | `generate-pdf.js` |
| **Test template behavior** | "test", "validate", "debug", "check" | `template_testing` | `watch-shared-workspace.js` |
| **Multiple documents** | "all manuals", "batch", "multiple" | `document_generation` | `generate-pdf.js` |
| **Single template focus** | "this template", "template works" | `template_testing` | `watch-shared-workspace.js` |

---

## 🎯 Format Purpose Definitions

### 📄 Document Generation Format (`document_generation`)
**Purpose**: Create final deliverable PDFs for distribution and publication
**Script**: `generate-pdf.js`
**Workflow**: Production document creation with specific output requirements

**Use When**:
- Creating documents for external distribution
- Generating final versions for publication
- Processing multiple different documents/templates in one job
- Publishing workflow requirements
- Need specific output filenames (Manual-v1.pdf, Guide-v2.pdf)

**Characteristics**:
- Multiple documents per request
- Production-quality output
- Specific naming requirements
- Final deliverable focus

### 🧪 Template Testing Format (`template_testing`)
**Script**: `watch-shared-workspace.js`
**Purpose**: Test template behavior and validate template development

**Use When**:
- Testing ONE template against various scenarios
- Development/debugging workflow for templates
- Template validation before production use
- Interactive template development and iteration
- Debugging template issues

**Characteristics**:
- Single template focus
- Multiple test scenarios
- Development/debugging oriented
- Template behavior validation

---

## 🌳 Decision Tree

```
User Request Received
├─ Contains words: "generate", "create", "produce", "make"?
│  ├─ YES → document_generation
│  └─ NO → Continue to next check
│
├─ Contains words: "test", "validate", "debug", "check"?
│  ├─ YES → template_testing
│  └─ NO → Continue to context analysis
│
├─ Multiple documents mentioned?
│  ├─ YES → document_generation
│  └─ NO → Continue to template focus check
│
├─ Focus on ONE template behavior?
│  ├─ YES → template_testing
│  └─ NO → Ask for clarification
│
└─ Default: Ask user to clarify intent
```

---

## 🔍 Keyword Recognition Patterns

### Document Generation Triggers
**Primary Keywords** (Strong Indicators):
- "generate the manual" → `document_generation`
- "create deliverables" → `document_generation`
- "produce PDFs" → `document_generation`
- "make production PDFs" → `document_generation`
- "build all documents" → `document_generation`

**Secondary Keywords** (Context Dependent):
- "final version", "deliverable", "publication"
- "batch process", "multiple documents"
- "output filename", "specific naming"

### Template Testing Triggers
**Primary Keywords** (Strong Indicators):
- "test this template" → `template_testing`
- "validate template behavior" → `template_testing`
- "debug template issues" → `template_testing`
- "check if template works" → `template_testing`

**Secondary Keywords** (Context Dependent):
- "template development", "iteration"
- "single template", "one template"
- "test scenarios", "test cases"

---

## 📚 Comprehensive Examples

### ✅ Document Generation Examples

**Example 1**: *"Generate the PASM2 manual for publication"*
- **Decision**: `document_generation`
- **Reasoning**: "Generate" + "for publication" indicates final deliverable
- **Script**: `generate-pdf.js`

**Example 2**: *"Create all the user guides we discussed"*
- **Decision**: `document_generation`
- **Reasoning**: "Create" + "all" indicates multiple documents
- **Script**: `generate-pdf.js`

**Example 3**: *"I need the production PDFs for the Smart Pins documentation"*
- **Decision**: `document_generation`
- **Reasoning**: "production PDFs" clearly indicates deliverable workflow
- **Script**: `generate-pdf.js`

**Example 4**: *"Build Manual-v2.1.pdf and Guide-v1.3.pdf"*
- **Decision**: `document_generation`
- **Reasoning**: Specific filenames indicate production output
- **Script**: `generate-pdf.js`

### ✅ Template Testing Examples

**Example 1**: *"Test the DeSilva template with sample content"*
- **Decision**: `template_testing`
- **Reasoning**: "Test" + "template" indicates template validation
- **Script**: `watch-shared-workspace.js`

**Example 2**: *"Check if the Smart Pins template handles code blocks correctly"*
- **Decision**: `template_testing`
- **Reasoning**: "Check if" + template behavior focus
- **Script**: `watch-shared-workspace.js`

**Example 3**: *"Debug why the pagination is breaking in this template"*
- **Decision**: `template_testing`
- **Reasoning**: "Debug" clearly indicates development/testing workflow
- **Script**: `watch-shared-workspace.js`

**Example 4**: *"Validate the template against multiple test documents"*
- **Decision**: `template_testing`
- **Reasoning**: "Validate template" + "test documents" = template testing
- **Script**: `watch-shared-workspace.js`

---

## ⚠️ Edge Cases & Troubleshooting

### 🤔 Ambiguous Scenarios

**Scenario 1**: *"Test the production workflow"*
- **Challenge**: Contains "test" but refers to production
- **Decision**: `document_generation`
- **Reasoning**: "production workflow" overrides "test" keyword
- **Key**: Focus on the object being tested (workflow = production)

**Scenario 2**: *"Generate a test document"*
- **Challenge**: Contains both "generate" and "test"
- **Decision**: `template_testing`
- **Reasoning**: "test document" indicates template testing context
- **Key**: "test document" = input for testing, not deliverable

**Scenario 3**: *"Create a quick test of the template"*
- **Challenge**: Both "create" and "test" present
- **Decision**: `template_testing`
- **Reasoning**: "test of the template" = template validation
- **Key**: What is being tested (template behavior)

### 🚨 Mixed Signal Resolution

**When user says**: *"I want to test generating the manual"*
**Analysis**:
- "test" suggests `template_testing`
- "generating the manual" suggests `document_generation`

**Resolution Process**:
1. **Identify the primary object**: What is being tested?
2. **If testing template behavior** → `template_testing`
3. **If testing production workflow** → `document_generation`
4. **If unclear** → Ask: "Are you testing template behavior or creating a deliverable?"

---

## 🎯 Format Field Usage

### When to Include `format_type`
- **Always include** in request JSON for AI clarity
- **Scripts ignore it** (passive marker for AI systems)
- **Helps future AI sessions** understand request intent

### Format Type Values
```json
{
  "format_type": "document_generation",  // For generate-pdf.js
  // ... rest of request
}
```

```json
{
  "format_type": "template_testing",     // For watch-shared-workspace.js
  // ... rest of request
}
```

---

## 🔄 Transition Scenarios

### From Testing to Production
**Scenario**: User has been testing template, now wants deliverable
**Indicators**: 
- "Now generate the final version"
- "Create the production PDF"
- "I'm satisfied with the template, make the deliverable"

**Action**: Switch to `document_generation` format

### From Production to Testing
**Scenario**: User wants to modify existing deliverable
**Indicators**:
- "Let's test some changes to the template"
- "Debug why the spacing is wrong"
- "Validate this template modification"

**Action**: Switch to `template_testing` format

---

## 🚫 Common Mistakes to Avoid

### ❌ Mistake 1: Keyword-Only Decisions
**Wrong**: Seeing "test" and automatically choosing `template_testing`
**Right**: Analyze what is being tested

### ❌ Mistake 2: Ignoring Context
**Wrong**: "Generate test document" → `document_generation`
**Right**: "Generate test document" → `template_testing` (test document = input)

### ❌ Mistake 3: Missing Multiple Documents
**Wrong**: "Create all manuals" → `template_testing`
**Right**: "Create all manuals" → `document_generation` (multiple documents)

### ❌ Mistake 4: Template vs Document Confusion
**Wrong**: Focusing on document count instead of workflow type
**Right**: Single template testing ≠ single document generation

---

## ✅ Decision Checklist

Before selecting format, verify:

- [ ] **Primary intent identified** (deliverable vs validation)
- [ ] **Keyword analysis completed** (generate/test/create/debug)
- [ ] **Document count considered** (single vs multiple)
- [ ] **Template focus assessed** (template behavior vs document output)
- [ ] **Context clues evaluated** (production, testing, development)
- [ ] **Edge cases ruled out** (not an ambiguous scenario)

---

## 🎯 Zero Ambiguity Goal

**This guide's success metric**: Any AI system should be able to:
1. Read a user request
2. Apply this decision framework
3. Choose the correct format with confidence
4. Handle edge cases systematically
5. Ask for clarification only when truly ambiguous

**If you're unsure after applying this guide**: Ask the user to clarify their primary intent rather than guessing.
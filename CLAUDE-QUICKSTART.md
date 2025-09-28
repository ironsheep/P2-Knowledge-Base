# P2 Knowledge Base QuickStart
*Essential reference for using P2 Knowledge Base with Claude*

## 🚀 For Fresh Claude Session (After /init)

Copy this entire block to Claude to configure it properly:

```
FIRST ACTION: Save these instructions to your CLAUDE.md, replacing any P2 Knowledge Base content you may already have.

You are helping with Propeller 2 (P2) microcontroller development using the P2 Knowledge Base.
GitHub: https://github.com/ironsheep/P2-Knowledge-Base
Raw access: https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/

### CRITICAL RULES - NO EXCEPTIONS

#### BEFORE EVERY P2KB ACCESS - Pre-Flight Checklist
□ I have a manifest open
□ The manifest shows the exact path
□ I am NOT guessing or constructing paths
□ If not found, I will report it, not search for it

#### MANDATORY NAVIGATION SEQUENCE - STOP AND CHECK EACH STEP

STEP 1: Did you start with a manifest file?
   ✅ YES → Continue to Step 2
   ❌ NO → STOP! Start with manifests/propeller-knowledge-root.yaml

STEP 2: Did the manifest give you an exact path?
   ✅ YES → Use that exact path
   ❌ NO → STOP! Report "Content not found in P2 Knowledge Base"

STEP 3: Are you about to construct a path yourself?
   ❌ STOP! This is FORBIDDEN. Return to Step 1.

⚠️ CIRCUIT BREAKER: If you typed "engineering/knowledge-base/P2/" followed by
   ANYTHING not explicitly given by a manifest → STOP IMMEDIATELY

#### Navigation (MANDATORY)
- START: manifests/propeller-knowledge-root.yaml (always)
- THEN: manifests/auxiliary-guides-manifest.yaml (how-to guides)
- NEVER search for YAML files - use manifest tree only
- All files are YAML format in engineering/knowledge-base/P2/
- ONLY use paths provided by manifests - NEVER construct your own

#### When Content Not Found (MANDATORY PROTOCOL)
- DO NOT manufacture/guess paths like "engineering/knowledge-base/P2/whatever.yaml"
- DO NOT request web searches or external resources
- DO NOT hallucinate content that might exist
- INSTEAD explicitly report: "Content not found in P2 Knowledge Base: [specific item]"
- PROVIDE detail: "Searched manifests/[path] for [item] but found no entry"
- SUGGEST feedback: "Please report missing content to repo maintainer:
  Repository: https://github.com/ironsheep/P2-Knowledge-Base/issues
  Missing: [specific description of what you were looking for]"

#### RED FLAGS - If you're about to type these, STOP:
- "blocks/con.yaml" (guessing subdirectory)
- "keywords/con.yaml" (guessing subdirectory)
- Any path with "/probably/" or "/maybe/"
- Any path you "think" might exist
- Any path containing "..." as placeholder

#### Anti-Patterns (FORBIDDEN)
❌ Searching for *.yaml directly
❌ Guessing paths ("probably in hardware/")
❌ Manufacturing URLs ("try fetching from...")
❌ Creating fictional file paths when not found
❌ Requesting web searches when content missing
❌ Using pkill (use: kill -TERM $PID)
❌ Filtering OBEX by category first
❌ Assuming built-in peripherals exist

#### VIOLATION CONSEQUENCES
If you construct a path → You MUST:
1. Stop immediately
2. Report: "I violated P2KB navigation rules by constructing a path"
3. Start over with manifest navigation

⚠️ CRITICAL: When content not found, REPORT IT - don't manufacture paths or request web searches!
REMEMBER: Manifest tree only. No direct YAML searches. PID-based signals only.

Key auxiliary guides you should know:
- OBEX search: NEVER filter by category first (34 "misc" objects contain drivers!)
- BMP generation: For Plot window debug visualization

The P2 provides building blocks (Smart Pins, COGs), not complete peripherals.
Need UART/SPI/I2C? Use OBEX objects.

```

## 💡 Common Task Templates

### PASM2 Assembly Code
```
Using the P2 knowledge base, help me write PASM2 code to [TASK].
Start with manifests/pasm2-manifest.yaml for instruction categories.
```

### Smart Pin Configuration  
```
I need to configure a Smart Pin for [PURPOSE].
Check hardware/smart-pins/modes/ via the manifest tree.
```

### OBEX Community Code
```
Find P2 OBEX objects for [HARDWARE/PROTOCOL].
Search ALL 113 objects via manifests/obex/obex-root.yaml.
Don't filter by category first - many drivers are in 'misc'.
```

### Hardware Testing
```
Test my Spin2 program on P2 hardware.
Use pnut_ts -d for debug compilation.
Capture PID with & and use kill -TERM $PID for cleanup.
```

## ⚠️ Session Management

**Clear conversation every 3-4 hours to maintain performance!**

- ✅ **0-3 hours**: Fast responses, perfect recall
- ⚠️ **3-4 hours**: Slower, may need reminders  
- ❌ **4+ hours**: Degraded performance, clear now

### Session Resume After Clear
```
Continuing P2 development. Previous: [BRIEF SUMMARY]
Check CLAUDE.md for P2 Knowledge Base rules.
Continue with: [SPECIFIC TASK]
```

## 🔑 Key Insights

**OBEX Search**: 34 "misc" objects contain drivers - always search all!

**P2 Philosophy**: Building blocks (COGs, Smart Pins), not complete peripherals.

**File Access**: Follow manifests only, never guess YAML paths.

**Testing**: Use PID-based signals, monitor logs not console.

**GitHub Repos**: 21 OBEX objects have links - mention but don't auto-fetch.

## 🐛 Missing Content Protocol

**When you can't find something in P2 Knowledge Base:**

1. **Report to user exactly what's missing:**
   ```
   Content not found in P2 Knowledge Base:
   - Searched: manifests/[specific path]
   - Looking for: [specific item/instruction/pattern]
   - Context: [what you were trying to accomplish]
   ```

2. **Provide GitHub issue template for user to submit:**
   ```markdown
   Title: Missing content: [specific item]
   
   **What I was looking for:**
   [Specific description]
   
   **Where I expected to find it:**
   manifests/[path] → [expected location]
   
   **Use case:**
   [What I was trying to accomplish]
   
   **Claude session reference:**
   [Date/time if available]
   ```

3. **NEVER:**
   - Make up a path that "should" exist
   - Suggest web searches to find it elsewhere
   - Create hypothetical content
   - Guess at file locations

## 📚 Additional Resources

- **Full Guide**: deliverables/ai-reference/auxiliary-guides/interaction/using-with-ai.md
- **Prompt Patterns**: AI-PROMPT-PATTERNS.md
- **Testing Guide**: auxiliary-guides/special-techniques/hardware-testing-guide.md

---
*Keep this card handy for P2 development with Claude!*

# Project Information Architecture Strategy

## Problem: Comprehensive Versioning vs Workspace Clarity

**Need**: Version everything for disaster recovery  
**Want**: Keep main workspace focused and uncluttered  
**Challenge**: Distinguish "current working documents" from "historical process artifacts"

---

## CURRENT Directory Implementation (as of 2025-08-15)

### **HIDDEN/NON-VERSIONED** (in .gitignore)
```
/import/                              # Source .docx/.xlsx files from Google Docs
/.claude/                             # AI-specific guides and references
/sources/extractions-v1-archived/     # Obsolete V1 PDF extractions (migrated to V2)
*.pdf                                 # All PDF files excluded
.DS_Store                             # macOS metadata
```

### **VERSIONED** (in git)
```
/sources/extractions/                 # V2 extractions (primary, was extractions-v2)
/sources/analysis/                    # Analysis reports
/.sprints/                            # Sprint documentation
/documentation-standards/             # Style guides and templates
```

### **V2 Migration Status**
- V1 extractions archived to `/sources/extractions-v1-archived/` (hidden)
- V2 promoted from `/sources/extractions-v2/` to `/sources/extractions/`
- 80% knowledge coverage achieved (was 55% in V1)
- Source files documented but not committed (.docx/.xlsx from Google Docs)

---

## Proposed Directory Strategy

### **VISIBLE - Main Workspace** (Current state, active work)
```
/
├── engineering/operations/README.md  # Single source of truth - current state (was PROJECT-MASTER.md)
├── /ai-reference/                    # Current deliverables (AI-optimized docs)
├── /documentation-standards/         # Current templates and standards  
├── /sources/                         # Primary source materials
├── /tools/                           # Current utilities and templates
└── /learning-paths/                  # Current educational content
```

### **VERSIONED BUT TUCKED AWAY** (Historical, archived, process evolution)
```
/.project-archives/                   # Hidden directory (git versioned)
├── /sprints/                         # Sprint-specific materials
│   ├── /audit-1/                     # All AUDIT-1 documents
│   │   ├── planning-documents/       # Question exhaustion process
│   │   ├── mcps/                     # Generated MCPs
│   │   ├── execution-artifacts/      # Work outputs
│   │   ├── should-have-considered/   # Mid-sprint realizations
│   │   └── retrospective/            # Learnings and improvements
│   ├── /process-1/                   # All PROCESS-1 documents  
│   └── /validate-1/                  # All VALIDATE-1 documents
├── /methodology-evolution/           # Process improvement history
│   ├── /templates-v1/                # Template versions
│   ├── /templates-v2/
│   └── /lessons-learned/             # Cross-sprint insights
└── /planning-iterations/             # PROJECT-MASTER evolution
    ├── /project-master-v1.md
    ├── /project-master-v2.md
    └── /planning-evolution-notes.md
```

### **Alternative: Date-Based Organization**
```
/.project-archives/
├── /2025-08-14-foundation-work/      # Date-based sprint archives
├── /2025-08-15-audit-1/
└── /2025-08-20-process-1/
```

---

## Document Lifecycle Pattern

### **During Sprint Planning:**
1. Create `/sprints/[sprint-name]/planning-documents/`
2. Accumulate question exhaustion documents
3. Generate MCPs in `/sprints/[sprint-name]/mcps/`

### **During Sprint Execution:**
4. Create work artifacts in `/sprints/[sprint-name]/execution-artifacts/`
5. Add "should have considered" docs as discovered
6. Update current deliverables in main workspace

### **During Sprint Wrap-up:**
7. Create retrospective in `/sprints/[sprint-name]/retrospective/`
8. Archive MCP task data using todo-mcp archive feature
9. Extract process improvements for next sprint

### **Between Sprints:**
10. Review archived materials before next sprint planning
11. Update methodology templates based on learnings
12. Update engineering/operations/README.md with current state

---

## Benefits of This Architecture

### **Visibility Management:**
- **Main workspace**: Clean, focused on current work
- **Archives**: Comprehensive but not cluttering
- **Git history**: Complete version trail for disaster recovery

### **Process Evolution:**
- **Sprint archives**: Show methodology improvements over time
- **Template versions**: Track what worked/didn't work
- **Learnings accumulation**: Each sprint strengthens the next

### **Disaster Recovery:**
- **Everything versioned**: No catastrophic loss possible
- **Clear organization**: Easy to find historical context
- **Process reconstruction**: Can rebuild methodology from archives

---

## Implementation Questions

### **Directory Naming:**
- **Hidden directory** (`.project-archives/`) vs **visible archive** (`/archive/`)?
- **Sprint naming**: `audit-1` vs `2025-08-14-audit-1` vs `sprint-001-audit`?

### **Archive Triggers:**
- **When to archive**: Sprint completion? When starting next sprint?
- **What to archive**: All documents? Only planning/retrospective?
- **Archive format**: Directory copy? Git branch? Compressed?

### **Access Patterns:**
- **Review frequency**: How often do we reference archived materials?
- **Search needs**: How do we find specific learnings across sprints?
- **Integration**: How do archived learnings integrate with current planning?

---

## Recommended Approach

### **Start Simple:**
```
/.sprints/                            # Hidden but not dot-hidden
├── /audit-1/                         # Current sprint materials  
├── /foundation-work/                 # Retroactively archive current docs
└── /methodology/                     # Process evolution tracking
```

### **Evolution:**
- Test this structure with AUDIT-1
- Refine based on actual usage patterns  
- Document what works in sprint retrospective
- Adjust architecture based on real needs

### **Guiding Principles:**
1. **Everything versioned** (disaster recovery)
2. **Main workspace clean** (focus on current work)  
3. **History accessible** (learning from experience)
4. **Easy to find** (logical organization)
5. **Simple to maintain** (sustainable long-term)

---

**Decision Point**: Should we implement this structure before starting AUDIT-1, or start AUDIT-1 and figure out archiving as we go?
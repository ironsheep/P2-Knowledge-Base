# Canonical Naming Directory Rename Plan
*Created: 2025-09-01*

## Purpose
Standardize all document directories to use canonical names consistently across manuals/, workspace/, and outbound/.

## Canonical Names Established

| Document | Canonical Name | 
|----------|---------------|
| deSilva P2 Guide | `p2-pasm-desilva-style` |
| Smart Pins Tutorial (Green Book) | `p2-smart-pins-tutorial` |
| Single-Step Debugger | `p2-single-step-debugger-manual` |
| Debug Terminal | `p2-debug-terminal-manual` |
| PASM2 Reference | `pasm2-reference-manual` |
| Spin2 Manual | `spin2-reference-manual` |
| AI Privacy Guide | `ai-privacy-guide` |

## Directory Renames Required

### 1. deSilva Document Consolidation
```bash
# Manuals directory - already correct
# engineering/document-production/manuals/p2-pasm-desilva-style/ ✓

# Workspace - needs rename and consolidation
git mv engineering/document-production/workspace/desilva-manual \
       engineering/document-production/workspace/p2-pasm-desilva-style

# Remove duplicate (verify empty first)
rm -rf engineering/document-production/workspace/da-silva-p2-manual

# Outbound - needs rename
git mv engineering/document-production/outbound/P2-PASM-deSilva-Style \
       engineering/document-production/outbound/p2-pasm-desilva-style
```

### 2. Smart Pins Document
```bash
# Manuals - needs rename
git mv engineering/document-production/manuals/smart-pins-workshop \
       engineering/document-production/manuals/p2-smart-pins-tutorial

# Workspace - needs rename
git mv engineering/document-production/workspace/smart-pins-manual \
       engineering/document-production/workspace/p2-smart-pins-tutorial

# Outbound - rename Green Book, remove Reference
git mv engineering/document-production/outbound/P2-Smart-Pins-Green-Book \
       engineering/document-production/outbound/p2-smart-pins-tutorial

# Remove old reference version
rm -rf engineering/document-production/outbound/P2-Smart-Pins-Reference
```

### 3. Debug Terminal Document
```bash
# Create manuals directory
mkdir -p engineering/document-production/manuals/p2-debug-terminal-manual
# Move creation guide from workspace if exists

# Workspace - needs rename
git mv engineering/document-production/workspace/p2-debug-window-system-manual \
       engineering/document-production/workspace/p2-debug-terminal-manual

# Remove duplicate/empty
rm -rf engineering/document-production/workspace/terminal-window-manual
rm -rf engineering/document-production/manuals/terminal-window-manual

# Create outbound if needed
mkdir -p engineering/document-production/outbound/p2-debug-terminal-manual
```

### 4. Single-Step Debugger Document
```bash
# Create manuals directory
mkdir -p engineering/document-production/manuals/p2-single-step-debugger-manual
# Move creation guide from workspace if exists

# Workspace - needs rename
git mv engineering/document-production/workspace/debugger-manual \
       engineering/document-production/workspace/p2-single-step-debugger-manual

# Create outbound if needed
mkdir -p engineering/document-production/outbound/p2-single-step-debugger-manual
```

### 5. PASM2 Reference Manual
```bash
# Manuals - needs rename
git mv engineering/document-production/manuals/pasm2-manual \
       engineering/document-production/manuals/pasm2-reference-manual

# Workspace - needs rename
git mv engineering/document-production/workspace/pasm2-user-manual \
       engineering/document-production/workspace/pasm2-reference-manual

# Outbound - needs rename
git mv engineering/document-production/outbound/pasm2-manual-v1 \
       engineering/document-production/outbound/pasm2-reference-manual
```

### 6. Spin2 Reference Manual
```bash
# Create manuals directory
mkdir -p engineering/document-production/manuals/spin2-reference-manual

# Workspace - needs rename
git mv engineering/document-production/workspace/spin2-user-manual \
       engineering/document-production/workspace/spin2-reference-manual

# Create outbound
mkdir -p engineering/document-production/outbound/spin2-reference-manual
```

### 7. AI Privacy Guide
```bash
# Create manuals directory
mkdir -p engineering/document-production/manuals/ai-privacy-guide

# Workspace - already correct
# engineering/document-production/workspace/ai-privacy-guide ✓

# Create outbound (ai-presentation-materials-v1 seems different)
mkdir -p engineering/document-production/outbound/ai-privacy-guide
```

## Execution Order

1. **Backup first**: Create git tag before changes
   ```bash
   git tag pre-canonical-naming-2025-09-01
   ```

2. **Execute renames in order above**

3. **Update mapping.csv** with all moves

4. **Verify work modes still reference correct paths**

5. **Test a PDF generation workflow** to ensure nothing broken

6. **Commit all changes**
   ```bash
   git add -A
   git commit -m "Standardize document directories with canonical names
   
   - Established canonical names for all documents
   - Renamed directories in manuals/, workspace/, and outbound/
   - Updated work mode guides and creation guides
   - Consolidated duplicate directories
   - Removed obsolete Smart Pins Reference version"
   ```

## Verification Checklist

- [ ] All manuals/ directories match canonical names
- [ ] All workspace/ directories match canonical names  
- [ ] All outbound/ directories match canonical names
- [ ] Work mode guides updated with new paths
- [ ] Creation guides have canonical_name field
- [ ] No duplicate directories remain
- [ ] PDF generation workflow still works
- [ ] mapping.csv updated with all moves
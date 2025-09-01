# Asset Consumer Registry
**Primary Extraction**: SPIN2 v51 Complete Extraction Audit  
**Asset Location**: `assets/images-20250815/` (and future import sessions)  
**Registry Purpose**: Track all consumers for automated forwarding when new assets arrive

## Secondary Extractions (Immediate Updates)
**Update Pattern**: Automatic reference file updates when new assets arrive

### `/sources/extractions/spin2-terminal-windows/`
- **Current Assets**: req01, req04, req06, bonus01
- **Reference File**: `assets/images-20250815.md`
- **Focus**: Terminal display, debug output, oscilloscope features
- **Auto-Forward**: All terminal-related screenshots (debug, scope, plot, FFT)

### `/sources/extractions/spin2-debugger/` 
- **Current Assets**: req03
- **Reference File**: `assets/images-20250815.md`
- **Focus**: Single-step debugging, scope displays, debugging interfaces
- **Auto-Forward**: All debugger-related screenshots (scope, breakpoints, variable inspection)

## Documents (Technical Debt Queue)
**Update Pattern**: Deferred to sprint planning via technical debt system

### `/documentation/manuals/terminal-window-manual.md`
- **Available Assets**: req01, req04, req06, bonus01
- **Enhancement Value**: +25% visual learning effectiveness
- **Integration Effort**: Medium (2-3 hours)
- **Debt Location**: `/technical-debt/VISUAL-ASSETS-DEBT.md`
- **Sprint Status**: Ready for V1.0 completion or V1.1 enhancement

### `/documentation/manuals/debugger-manual.md`
- **Available Assets**: req03
- **Enhancement Value**: +15% scope feature comprehension  
- **Integration Effort**: Low (1 hour)
- **Debt Location**: `/technical-debt/VISUAL-ASSETS-DEBT.md`
- **Sprint Status**: Ready for V1.0 completion

## Consumer Update Process

### When New Assets Arrive:

**Step 1: Immediate Updates (Secondary Extractions)**
```
For each secondary extraction in registry:
1. Check asset relevance to extraction focus
2. Update reference file with new relevant assets
3. Maintain session history (images-20250815, images-20250820, etc.)
```

**Step 2: Technical Debt Updates (Documents)**
```
For each document in registry:
1. Assess new assets for document enhancement value
2. Update technical debt entry with new available assets
3. Revise enhancement value and integration effort estimates
4. Mark as ready for sprint selection
```

## Registry Maintenance

### Adding New Consumers:
1. Identify new extraction or document using these assets
2. Add to appropriate category (secondary extraction vs document)
3. Specify asset focus and update pattern
4. Initialize reference file or debt entry

### Asset Session Management:
- Each import session creates new timestamped directory
- Registry tracks cumulative available assets across all sessions
- Reference files update to include assets from multiple sessions
- Technical debt entries aggregate enhancement opportunities

### Focus Area Mapping:
- **Terminal Features**: req01, req04, req06, bonus01, (future terminal-related)
- **Debugger Features**: req03, (future debugger-related)
- **Architecture Diagrams**: (future system-level screenshots)
- **IDE/Development**: (future development environment screenshots)

## Benefits

1. **Complete Visibility**: Primary extraction owner sees all downstream impact
2. **Automated Updates**: Secondary extractions stay current automatically  
3. **Strategic Planning**: Document updates queued for sprint consideration
4. **No Lost Consumers**: Registry prevents missed update targets
5. **Scalable Process**: Easy to add new consumers as knowledge base grows
6. **Session Tracking**: Clear history of when assets became available

## Consumer Addition Examples

### New Secondary Extraction:
```markdown
### `/sources/extractions/spin2-architecture-deep-dive/`
- **Current Assets**: (future architecture screenshots)
- **Reference File**: `assets/images-[DATE].md` 
- **Focus**: System architecture, memory model, timing diagrams
- **Auto-Forward**: All architecture-related screenshots
```

### New Document:
```markdown
### `/documentation/guides/p2-getting-started-guide.md`
- **Available Assets**: (subset of terminal and debugger screenshots)
- **Enhancement Value**: +30% new user onboarding success
- **Integration Effort**: High (comprehensive tutorial revision)
- **Debt Location**: `/technical-debt/VISUAL-ASSETS-DEBT.md`
- **Sprint Status**: Candidate for V1.1 onboarding focus
```

---

**Registry Owner**: Primary extraction maintainer  
**Update Frequency**: Immediately when new assets arrive  
**Review Schedule**: During sprint planning for technical debt prioritization
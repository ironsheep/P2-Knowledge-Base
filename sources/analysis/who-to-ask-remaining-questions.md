# Who To Ask: Remaining P2 Questions Authority Matrix

## Question Authority Hierarchy

### 1. Chip Gracey (P2 Designer) - ULTIMATE AUTHORITY
**Contact**: Via Parallax Forums (@cgracey)
**Authoritative For**:
- Architecture decisions and rationale
- Silicon implementation details  
- Bytecode interpreter internals
- CORDIC algorithm specifics
- Smart Pin internal design
- Boot ROM implementation
- Future roadmap/features
- Design trade-offs and limitations

**Specific Questions for Chip**:
1. Why was Xoroshiro128** chosen for PRNG?
2. What determines the 55-cycle CORDIC pipeline depth?
3. How exactly does hub RAM arbitration work?
4. What is the Spin2 bytecode format specification?
5. What are the undocumented Smart Pin mode bits?
6. How does the PLL filter achieve <2ns jitter?
7. What silicon process allows 390MHz operation?
8. Why 8 cogs instead of 16 in production?

### 2. Jeff Martin (Parallax) - TOOLS & ECOSYSTEM
**Contact**: Via Parallax Forums (@"Jeff Martin")
**Authoritative For**:
- PropellerTool/Spin2 compiler
- Development environment
- Official documentation
- Tool roadmap
- Educational materials

**Specific Questions for Jeff**:
1. What compiler optimizations are performed?
2. How does the debugger protocol work?
3. What are the bytecode performance metrics?
4. When will missing instruction docs be completed?
5. What determines stack size requirements?

### 3. Eric Smith (FlexSpin Developer) - ALTERNATIVE TOOLS
**Contact**: GitHub (@totalspectrum)
**Authoritative For**:
- FlexSpin compiler internals
- C/C++ on P2
- Cross-platform tools
- Performance optimization
- Alternative language support

**Specific Questions for Eric**:
1. What are the FlexSpin optimization strategies?
2. How does FlexC map to P2 architecture?
3. What are the performance differences vs Spin2?
4. How to maximize hub exec efficiency?

### 4. Jon McPhalen (JonnyMac) - PRACTICAL APPLICATIONS
**Contact**: Parallax Forums (@JonnyMac)
**Authoritative For**:
- Real-world P2 applications
- Object library design
- Best practices
- Common patterns
- Professional deployment

**Specific Questions for Jon**:
1. What are production-tested Smart Pin configurations?
2. What are reliable multi-cog communication patterns?
3. How to handle timing-critical applications?
4. What are field-proven error handling approaches?

### 5. Peter Jakacki (Tachyon/TAQOZ) - FORTH & BOOT
**Contact**: Parallax Forums (@"Peter Jakacki")
**Authoritative For**:
- TAQOZ Forth in ROM
- Boot process details
- Low-level debugging
- Performance boundaries
- Alternative architectures

**Specific Questions for Peter**:
1. What TAQOZ ROM functions are available?
2. How to debug boot failures?
3. What are the ROM memory limitations?
4. How to extend TAQOZ functionality?

### 6. Parallax Community Forum - COLLECTIVE KNOWLEDGE
**Contact**: forums.parallax.com
**Authoritative For**:
- Code examples
- Troubleshooting
- Hardware interfacing
- Project implementations
- Workarounds

**Community Questions**:
1. What peripherals have proven drivers?
2. What are common gotchas?
3. What tools does everyone use?
4. What learning resources exist?

## Questions by Authority Level

### ONLY Chip Gracey Can Answer:
- [ ] Exact bytecode encoding format
- [ ] Silicon process specifications
- [ ] Internal arbitration algorithms
- [ ] Design decision rationales
- [ ] Undocumented mode bits
- [ ] Future silicon plans

### Chip or Jeff Can Answer:
- [ ] Official instruction cycle counts
- [ ] Compiler implementation details
- [ ] Debug protocol specification
- [ ] Memory map guarantees
- [ ] Tool development priorities

### Multiple Sources Can Answer:
- [ ] Best practices (Jon, Eric, Community)
- [ ] Performance optimization (Eric, Jon)
- [ ] Peripheral interfacing (Community, Jon)
- [ ] Learning paths (Jeff, Community)
- [ ] Troubleshooting (Peter, Community)

## Contact Strategy

### Phase 1: Documentation Completion
1. **Jeff Martin**: Request missing instruction docs
2. **Jeff Martin**: Request cycle count tables
3. **Jeff Martin**: Request memory map details

### Phase 2: Technical Clarification
1. **Chip Gracey**: Core architecture questions
2. **Chip Gracey**: Silicon/hardware specifics
3. **Chip Gracey**: Design rationale

### Phase 3: Practical Knowledge
1. **Jon McPhalen**: Production patterns
2. **Eric Smith**: Optimization techniques
3. **Community**: Example collection

### Phase 4: Advanced Topics
1. **Peter Jakacki**: Boot/ROM details
2. **Chip Gracey**: Undocumented features
3. **Eric Smith**: Alternative approaches

## Question Priority Matrix

### CRITICAL (Blocks code generation):
- Bytecode format → Chip/Jeff
- Cycle counts → Jeff/Chip
- Stack requirements → Jeff
- Memory map → Jeff

### HIGH (Limits functionality):
- Smart Pin modes → Chip
- CORDIC details → Chip
- Event system → Jeff/Chip
- Debug protocol → Jeff

### MEDIUM (Improves quality):
- Optimization → Eric/Jon
- Best practices → Jon/Community
- Patterns → Jon/Community
- Tools → Jeff/Eric

### LOW (Nice to have):
- History → Chip
- Rationale → Chip
- Future → Chip/Jeff
- Alternatives → Eric/Peter

## Recommended Approach

### Immediate Actions:
1. Compile consolidated question list
2. Post on Parallax Forum (reaches all)
3. Tag specific experts for their domains
4. Create GitHub issues for tool questions

### Documentation Requests:
1. Official Parallax: Missing instruction details
2. FlexSpin repo: Optimization docs
3. Community wiki: Pattern collection

### Follow-up Strategy:
1. Weekly forum participation
2. GitHub issue tracking
3. Document all answers
4. Update knowledge base

## Expected Response Times

- **Forum Questions**: 1-7 days
- **GitHub Issues**: 2-14 days  
- **Direct Contact**: Variable
- **Chip Gracey**: When available (busy)
- **Jeff Martin**: Business hours
- **Community**: 24-48 hours typically

## Question Format Template

```markdown
Subject: [P2 Knowledge Base] Category - Specific Topic

Background: [Why this matters for code generation]
Current Understanding: [What we know]
Specific Question: [Precise technical question]
Impact: [How answer improves AI code generation]

Thank you for helping improve P2 AI assistance!
```

## Conclusion

Most remaining questions require **official Parallax response** (Chip/Jeff) for authoritative answers. Community can fill practical knowledge gaps. Eric Smith best for alternative implementation insights.

**Key Insight**: Many "unknowns" may already be answered in forum threads - systematic forum mining recommended before asking.
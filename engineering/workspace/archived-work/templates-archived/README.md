# Monolithic Templates Archive

**Created**: 2025-08-25  
**Purpose**: Archive of abandoned monolithic template approaches  
**Policy**: NOT FOR PRODUCTION USE - Reference only

## Archival Decision

**Date**: 2025-08-25  
**Reason**: Monolithic templates create unsustainable technical debt:
- 3-4 day debugging cycles  
- Brittle, hard to maintain
- Copy-paste customization nightmares
- Template regression issues

**Solution**: Layered template architecture permanently adopted for all P2 Knowledge Base documents.

## Archive Contents

### Smart Pins Templates (Monolithic - ABANDONED)
- `p2kb-smart-pins-MONOLITHIC.latex` - From pdf-forge-workspace/templates
- `p2kb-smart-pins-workspace-MONOLITHIC.latex` - From workspace/smart-pins-manual  

**Issue**: These were self-contained templates with all Pandoc compatibility, styling, and structure baked in. Caused maintenance nightmares and prevented systematic testing.

**Replacement**: Layered `p2kb-smart-pins.latex` using foundation + content + presentation layers.

## Reference Protocol

- **Claude Access**: Available for reference if needed during development
- **Human Access**: On request only  
- **No Resurrection**: Without full architectural review and approval
- **No Production Use**: Archive is for understanding old approaches only

## Related Documentation

- **Layered Architecture**: `/documentation/pdf-forge-system/layered-template-architecture.md`
- **Current Templates**: `/pdf-forge-workspace/templates/` (layered approach only)
- **Last Known Good**: `/exports/pdf-generation/outbound/*/last-deployed/` (recovery baseline)

---

**POLICY**: P2 Knowledge Base uses layered template architecture ONLY. Monolithic approaches permanently abandoned.
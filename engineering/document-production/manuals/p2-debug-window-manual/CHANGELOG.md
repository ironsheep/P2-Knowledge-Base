# P2 Debug Window System Manual - Change Log

## Version History

### Consistency re-audit vs. KB v1.9.1 - 2026-06-15
- Re-audited manual content against the v1.9.1 DEBUG display-directive YAML
  corrections (findings F-125..F-134). Record: `audit/reaudit-vs-kb-v1.9.1-2026-06-15.md`.
- Added the per-window `` `CLOSE `` runtime command (frees one named window; all
  nine windows) to ch01's shared-commands model, every window chapter's
  clear/save section, and all Appendix A runtime tables. Corrected ch01's stale
  "there is no close command" claim.
- PLOT `SPRITEDEF`: corrected the palette from a fixed "256 colors" to "up to 256
  — supply only the entries your indices use" (ch05 + REF directive matrix),
  matching the Pascal read-until-message-end behavior.
- Confirmed already-consistent: formatter set, code-12 (not form-feed),
  create-then-feed syntax, SCOPE_XY SIZE/POLAR, LUTCOLORS "up to 256".

### Initial Draft - 2025-08-15
- Complete 83KB document created
- Comprehensive coverage of P2 debug capabilities:
  - DEBUG Terminal Window System
  - Single-Step Debugger
  - Interactive debugging features
  - Code instrumentation techniques
- Full technical reference with examples
- Ready for review and enhancement

## Status
- **Current State**: Complete technical draft
- **Size**: 83KB comprehensive documentation
- **Next Steps**: Review, formatting, and PDF generation preparation